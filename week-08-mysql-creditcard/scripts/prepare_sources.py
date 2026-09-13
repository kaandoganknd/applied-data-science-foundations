"""Extract both supplied files and reconcile records without changing source values."""

import csv
import hashlib
import json
import re
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import xlrd
from docx import Document

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ["CreditcardNum", "Creditcard_company", "Creditcard_type", "Credit_Limit",
          "Totalspent", "City", "CardHolder", "Issue_Date"]
AMOUNTS = {"Credit_Limit", "Totalspent"}


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_sources():
    book = xlrd.open_workbook(ROOT / "sources/Creditcard_table.xls")
    sheet = book.sheet_by_name("Creditcard_table")
    if sheet.row_values(0) != FIELDS:
        raise ValueError("Unexpected Excel column names or order")
    excel = []
    for index in range(1, sheet.nrows):
        row = dict(zip(FIELDS, sheet.row_values(index)))
        identifier = row["CreditcardNum"]
        if not float(identifier).is_integer():
            raise ValueError("Non-integer identifier in Excel")
        row["CreditcardNum"] = str(int(identifier))
        row["Issue_Date"] = xlrd.xldate_as_datetime(row["Issue_Date"], book.datemode).date().isoformat()
        for name in AMOUNTS:
            row[name] = format(Decimal(str(row[name])).quantize(Decimal(".01")), ".2f")
        excel.append(row)

    document = Document(ROOT / "sources/INSERT INTO CreditCard.docx")
    statements = [p.text.strip() for p in document.paragraphs if p.text.strip()]
    inserts = []
    for statement in statements:
        match = re.fullmatch(r"INSERT INTO CreditCard\((.*?)\) values \((.*?)\);", statement)
        if not match:
            raise ValueError("Unexpected statement in supplied document")
        columns = [c.strip() for c in match[1].split(",")]
        if [c.lower() for c in columns] != [c.lower() for c in FIELDS]:
            raise ValueError("Unexpected INSERT columns")
        values = next(csv.reader([match[2]], quotechar="'", skipinitialspace=True))
        if len(values) != len(FIELDS):
            raise ValueError("Unexpected value count")
        row = dict(zip(FIELDS, values))
        for name in AMOUNTS:
            row[name] = format(Decimal(row[name]).quantize(Decimal(".01")), ".2f")
        row["Issue_Date"] = datetime.strptime(row["Issue_Date"], "%Y/%m/%d").date().isoformat()
        inserts.append(row)
    for rows in (excel, inserts):
        if len(rows) != 15 or len({r['CreditcardNum'] for r in rows}) != 15:
            raise ValueError("Expected 15 unique practice records in each source")
        if any(v == "" for row in rows for v in row.values()):
            raise ValueError("Blank source value")
    return excel, inserts, statements


def main():
    excel, inserts, statements = read_sources()
    for name, rows in [("creditcard_excel.csv", excel), ("creditcard_insert.csv", inserts)]:
        write_csv(ROOT / "data" / name, FIELDS, rows)
    (ROOT / "sources/original_inserts.sql").write_text("\n".join(statements) + "\n", encoding="utf-8")
    left = {r["CreditcardNum"]: r for r in excel}
    right = {r["CreditcardNum"]: r for r in inserts}
    if left.keys() != right.keys():
        raise ValueError("The sources have different identifiers")
    differences = [dict(CreditcardNum=key, column=field, excel_value=left[key][field],
                        insert_document_value=right[key][field])
                   for key in sorted(left) for field in FIELDS if left[key][field] != right[key][field]]
    write_csv(ROOT / "docs/source-differences.csv",
              ["CreditcardNum", "column", "excel_value", "insert_document_value"], differences)
    source_files = [ROOT / "sources/Creditcard_table.xls", ROOT / "sources/INSERT INTO CreditCard.docx"]
    review = {
        "files": {p.name: {"sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in source_files},
        "excel_rows": len(excel), "insert_rows": len(inserts),
        "different_cells": len(differences),
        "records_with_differences": len({r['CreditcardNum'] for r in differences}),
        "column_max_characters_across_both_sources": {
            c: max(len(r[c]) for r in excel + inserts) for c in FIELDS},
        "loaded_values": "INSERT INTO CreditCard.docx",
        "normalizations": ["Excel serial dates and SQL dates converted to YYYY-MM-DD",
                           "Excel numeric identifiers converted to four-character strings",
                           "Table name standardized to Creditcard; Totalspent matches Excel heading",
                           "Money displayed with two decimal places"]}
    (ROOT / "docs/source-review.json").write_text(json.dumps(review, indent=2) + "\n", encoding="utf-8")
    sql = ["-- All 15 records from the supplied INSERT document; values are preserved.",
           "-- Identifier case and date notation are standardized for MySQL portability.",
           "START TRANSACTION;", ""]
    for row in inserts:
        values = [row[c] if c in AMOUNTS else "'" + row[c].replace("'", "''") + "'" for c in FIELDS]
        sql.append("INSERT INTO Creditcard (" + ", ".join(FIELDS) + ")\nVALUES (" + ", ".join(values) + ");\n")
    sql.append("COMMIT;")
    (ROOT / "sql/02_insert_records.sql").write_text("\n".join(sql) + "\n", encoding="utf-8")
    print(json.dumps(review, indent=2))
    for row in differences:
        print(row)


if __name__ == "__main__":
    main()
