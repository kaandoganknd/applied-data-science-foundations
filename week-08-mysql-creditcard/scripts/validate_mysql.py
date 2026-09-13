"""Execute the delivered SQL in a fresh MySQL schema and save actual results."""

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
    parser.add_argument("--database", default="week08_creditcard")
    args = parser.parse_args()
    if not re.fullmatch(r"week08_creditcard(?:_[a-z0-9_]+)?", args.database):
        parser.error("Use week08_creditcard or a name beginning week08_creditcard_")
    conn = pymysql.connect(host=args.host, port=args.port, unix_socket=args.socket,
                           user=args.user, password=getpass.getpass("MySQL password: ") if args.ask_password else "",
                           charset="utf8mb4", autocommit=True)
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT SCHEMA_NAME FROM information_schema.SCHEMATA WHERE SCHEMA_NAME=%s", (args.database,))
            if cursor.fetchone():
                raise RuntimeError("Schema already exists. Choose a fresh --database name; existing data will not be changed.")
            setup = statements(ROOT / "sql/00_select_database.sql")
            for sql in setup:
                cursor.execute(sql.replace("week08_creditcard", args.database))
            for name in ["01_create_table.sql", "02_insert_records.sql"]:
                for sql in statements(ROOT / "sql" / name):
                    cursor.execute(sql)
                    cursor.execute("SHOW WARNINGS")
                    if cursor.fetchall():
                        raise AssertionError(f"MySQL reported a warning while executing {name}")

            cursor.execute("SELECT VERSION(), @@version_comment, @@SESSION.sql_mode, @@lower_case_table_names")
            version, edition, mode, case_mode = cursor.fetchone()
            cursor.execute("SELECT * FROM Creditcard ORDER BY CreditcardNum")
            initial = cursor.fetchall()
            if [c[0] for c in cursor.description] != FIELDS:
                raise AssertionError("Table column names/order do not match Excel")
            _, expected, _ = read_sources()
            actual = [dict(zip(FIELDS, [serial(v) for v in row])) for row in initial]
            if actual != sorted(expected, key=lambda r: r["CreditcardNum"]):
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
                        requested = [format(Decimal(str(row[c])), '.2f') if c in AMOUNTS else row[c] for c in FIELDS]
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
            for field in FIELDS:
                run_case("NULL " + field, {field: None}, 1048)
            run_case("Short practice identifier", {"CreditcardNum": "12"}, 3819)
            run_case("Nonnumeric practice identifier", {"CreditcardNum": "ABCD"}, 3819)
            run_case("Identifier exceeds four characters", {"CreditcardNum": "12345"}, 1406)
            for field, length in [("Creditcard_company", 50), ("Creditcard_type", 30), ("City", 50), ("CardHolder", 100)]:
                run_case("Too long " + field, {field: "X" * (length + 1)}, 1406)
            run_case("Invalid calendar date", {"Issue_Date": "2021-02-30"}, 1292)
            run_case("Nonnumeric credit limit", {"Credit_Limit": "not-money"}, 1366)
            run_case("Credit limit exceeds DECIMAL capacity", {"Credit_Limit": "100000000.00"}, 1264)
            run_case("Positive minimum currency unit", {"Credit_Limit": "0.01", "Totalspent": "0.00"})
            run_case("Leading zero identifier", {"CreditcardNum": "0001"})
            run_case("Repeated holder with a different identifier")
            run_case("Unicode holder name", {"CardHolder": "Çağrı Öztürk"})
            run_case("No unrequested spending cap", {"Credit_Limit": "1.00", "Totalspent": "1.01"})
            run_case("Declared text and decimal boundaries", {
                "Creditcard_company": "C" * 50, "Creditcard_type": "T" * 30,
                "City": "Y" * 50, "CardHolder": "H" * 100,
                "Credit_Limit": "99999999.99", "Totalspent": "99999999.99"})
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
                        "lower_case_table_names": case_mode, "schema": args.database,
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
