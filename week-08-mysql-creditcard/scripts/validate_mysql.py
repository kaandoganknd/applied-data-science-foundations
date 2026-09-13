"""Execute the unchanged full solution and save MySQL results and behaviour tests."""

import argparse
import csv
import getpass
import hashlib
import json
import re
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import pymysql

from prepare_sources import FIELDS, AMOUNTS, read_sources, write_csv

ROOT = Path(__file__).resolve().parents[1]


def statements(path):
    text = path.read_text(encoding="utf-8")
    # Delivered SQL has no stored routines or semicolons inside string values.
    text = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("--"))
    return [s.strip() for s in text.split(";") if s.strip()]


def serial(value):
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return format(value, ".2f")
    return value


def markdown_table(columns, rows):
    def cell(value):
        return str(serial(value) if value is not None else "NULL").replace("|", "\\|").replace("\n", "<br>")
    return "\n".join(["| " + " | ".join(columns) + " |",
                       "| " + " | ".join(["---"] * len(columns)) + " |"] +
                      ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--socket")
    parser.add_argument("--user", default="root")
    parser.add_argument("--ask-password", action="store_true")
    args = parser.parse_args()
    conn = pymysql.connect(host=args.host, port=args.port, unix_socket=args.socket,
                           user=args.user, password=getpass.getpass("MySQL password: ") if args.ask_password else "",
                           charset="utf8mb4", autocommit=True)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT @@lower_case_table_names, @@SESSION.sql_mode")
            case_mode, initial_mode = cursor.fetchone()
            if case_mode == 0:
                raise RuntimeError("The exact solution mixes creditcard and CreditCard. Validate it on a disposable server with case-insensitive table lookup; no SQL changes are applied here.")
            if not any(mode in initial_mode for mode in ['STRICT_TRANS_TABLES', 'STRICT_ALL_TABLES']):
                raise RuntimeError("Strict SQL mode is needed for the documented type/length tests")
            cursor.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME=%s", ("financial_db",))
            if cursor.fetchone():
                raise RuntimeError("financial_db already exists. Use a fresh disposable server; existing data will not be changed.")
            solution = ROOT / "sql/full_solution.sql"
            if solution.read_bytes() != (ROOT / 'sources/CREDITCARD SCRIPT W7 - FULL SOLUTION.txt').read_bytes():
                raise AssertionError("The runnable full solution differs from the supplied file")
            warnings = []
            for index, sql in enumerate(statements(solution), 1):
                cursor.execute(sql)
                cursor.execute("SHOW WARNINGS")
                for level, code, message in cursor.fetchall():
                    warnings.append(dict(statement_number=index, level=level, code=code, message=message))
                    if code != 4095:
                        raise AssertionError(f"Unexpected MySQL warning: {code} {message}")

            cursor.execute("SELECT VERSION(), @@version_comment, @@SESSION.sql_mode, @@lower_case_table_names")
            version, edition, mode, case_mode = cursor.fetchone()
            cursor.execute("SELECT * FROM Creditcard ORDER BY CreditcardNum")
            initial = cursor.fetchall()
            if [c[0] for c in cursor.description] != FIELDS:
                raise AssertionError("Table column names/order do not match Excel")
            _, expected, _ = read_sources()
            actual = [dict(zip(FIELDS, [serial(v) for v in row])) for row in initial]
            comparable = [dict(row, CreditcardNum=str(row['CreditcardNum'])) for row in actual]
            if comparable != sorted(expected, key=lambda r: r["CreditcardNum"]):
                raise AssertionError("Loaded rows differ from the INSERT document")

            evidence = ["# Executed MySQL queries", "",
                        f"MySQL {version} ({edition}). All results below were fetched from the server.", ""]
            ddl = ""
            for name in ["03_inspect_table.sql", "04_verify_records.sql"]:
                for sql in statements(ROOT / "sql" / name):
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    columns = [c[0] for c in cursor.description]
                    evidence.extend(["```sql", sql + ";", "```", ""])
                    if sql.startswith("SHOW CREATE"):
                        ddl = rows[0][1]
                        evidence.extend(["```sql", ddl + ";", "```", ""])
                    else:
                        evidence.extend([markdown_table(columns, rows), ""])

            checks = []
            base = dict(expected[0], CreditcardNum="9900")
            insert_sql = "INSERT INTO Creditcard (" + ", ".join(FIELDS) + ") VALUES (" + ", ".join(["%s"] * len(FIELDS)) + ")"

            def run_case(name, changes=None, error=None, update=False):
                row = dict(base, **(changes or {}))
                conn.begin()
                observed, message = None, "Accepted; transaction rolled back"
                try:
                    if update:
                        cursor.execute("UPDATE Creditcard SET Credit_Limit=0 WHERE CreditcardNum=%s", (expected[0]["CreditcardNum"],))
                    else:
                        cursor.execute(insert_sql, [row[c] for c in FIELDS])
                        cursor.execute("SHOW WARNINGS")
                        if cursor.fetchall():
                            raise AssertionError("Unexpected warning in accepted test case")
                        cursor.execute("SELECT * FROM Creditcard WHERE CreditcardNum=%s", (row['CreditcardNum'],))
                        stored = [serial(v) for v in cursor.fetchone()]
                        requested = [None if row[c] is None else
                                     int(row[c]) if c == 'CreditcardNum' else
                                     format(Decimal(str(row[c])), '.2f') if c in AMOUNTS else row[c] for c in FIELDS]
                        if stored != requested:
                            raise AssertionError("An accepted value was changed by MySQL")
                except pymysql.MySQLError as exc:
                    observed, message = exc.args[0], exc.args[1]
                finally:
                    conn.rollback()
                if observed != error:
                    raise AssertionError(f"{name}: expected error {error}; got {observed}: {message}")
                checks.append({"test": name, "expected_error": error, "observed_error": observed,
                               "result": "PASS", "server_message": message})

            run_case("Duplicate primary key", {"CreditcardNum": expected[0]["CreditcardNum"]}, 1062)
            run_case("Zero credit limit", {"Credit_Limit": "0.00"}, 3819)
            run_case("Negative credit limit", {"Credit_Limit": "-0.01"}, 3819)
            run_case("Zero credit limit on UPDATE", error=3819, update=True)
            for field in [c for c in FIELDS if c not in AMOUNTS]:
                run_case("NULL " + field, {field: None}, 1048)
            run_case("NULL credit limit allowed by reference", {"Credit_Limit": None})
            run_case("NULL total spent allowed by reference", {"Totalspent": None})
            run_case("Short numeric identifier allowed", {"CreditcardNum": "12"})
            run_case("Nonnumeric identifier", {"CreditcardNum": "ABCD"}, 1366)
            run_case("Five-digit SMALLINT identifier allowed", {"CreditcardNum": "12345"})
            run_case("SMALLINT upper boundary", {"CreditcardNum": "32767"})
            run_case("SMALLINT lower boundary", {"CreditcardNum": "-32768"})
            run_case("SMALLINT overflow", {"CreditcardNum": "32768"}, 1264)
            for field, length in [("Creditcard_company", 100), ("Creditcard_type", 50), ("City", 50), ("CardHolder", 100)]:
                run_case("Too long " + field, {field: "X" * (length + 1)}, 1406)
            run_case("Invalid calendar date", {"Issue_Date": "2021-02-30"}, 1292)
            run_case("Nonnumeric credit limit", {"Credit_Limit": "not-money"}, 1366)
            run_case("Credit limit exceeds DECIMAL capacity", {"Credit_Limit": "10000000.00"}, 1264)
            run_case("Positive minimum currency unit", {"Credit_Limit": "0.01", "Totalspent": "0.00"})
            run_case("Leading zero converted to integer 1", {"CreditcardNum": "0001"})
            run_case("Repeated holder with a different identifier")
            run_case("Unicode holder name", {"CardHolder": "Çağrı Öztürk"})
            run_case("No unrequested spending cap", {"Credit_Limit": "1.00", "Totalspent": "1.01"})
            run_case("Declared text and decimal boundaries", {
                "Creditcard_company": "C" * 100, "Creditcard_type": "T" * 50,
                "City": "Y" * 50, "CardHolder": "H" * 100,
                "Credit_Limit": "9999999.99", "Totalspent": "9999999.99"})
            cursor.execute("SELECT * FROM Creditcard ORDER BY CreditcardNum")
            if cursor.fetchall() != initial:
                raise AssertionError("Validation changed the loaded records")
            out = ROOT / "evidence"
            out.mkdir(exist_ok=True)
            write_csv(out / "loaded_records.csv", FIELDS, actual)
            (out / "query-results.md").write_text("\n".join(evidence), encoding="utf-8")
            (out / "show-create-table.sql").write_text(ddl + ";\n", encoding="utf-8")
            manifest = {"verified_at_utc": datetime.now(timezone.utc).isoformat(),
                        "mysql_version": version, "edition": edition, "sql_mode": mode,
                        "lower_case_table_names": case_mode, "schema": "financial_db",
                        "full_solution_byte_identical": True,
                        "solution_sha256": hashlib.sha256(solution.read_bytes()).hexdigest(),
                        "source_statement_count": len(statements(solution)),
                        "source_warnings": warnings,
                        "loaded_rows": len(actual), "source_match": "15 of 15 INSERT-document rows, all eight fields",
                        "passed_constraint_cases": len(checks), "failed_constraint_cases": 0,
                        "records_unchanged_after_tests": True,
                        "sql_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT / 'sql').glob('*.sql'))},
                        "cases": checks}
            (out / "validation.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            (out / "constraint-tests.md").write_text(
                "# Constraint tests\n\nEvery case ran against MySQL and was rolled back. The 15 source records remained unchanged.\n\n" +
                markdown_table(["Test", "Expected", "Observed", "Result"],
                               [(t['test'], t['expected_error'] or 'Accept', t['observed_error'] or 'Accept', t['result']) for t in checks]) + "\n",
                encoding="utf-8")
            print(f"MySQL {version}: loaded and reconciled {len(actual)} rows; {len(checks)} constraint cases passed.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
