# Creditcard table design and validation in MySQL

A relational database exercise covering column design, primary keys, enforced check constraints, and source reconciliation. The `Creditcard` table contains all eight columns from the supplied spreadsheet and all 15 records from the supplied INSERT document.

The scripts were executed on **MySQL Community Server 9.7.1**. All 15 loaded records matched the INSERT document across every field, and **28 constraint tests passed**. Read the [executed queries and results](evidence/query-results.md) and [constraint test results](evidence/constraint-tests.md).

## Source reconciliation

The spreadsheet and INSERT document contain the same 15 identifiers, but **11 cells across 8 records differ**. The differences include spending amounts, dates, city spellings, and company names. The exercise asks to execute the supplied INSERT statements, so those values are loaded into MySQL. The spreadsheet defines the column names and provides a separate comparison source.

Both original files and both CSV extracts are included. See the [source comparison](docs/source-reconciliation.md) for every difference and the [source manifest](docs/source-review.json) for file hashes and observed text lengths.

## Exercise coverage

| Requirement | Implementation | Executed evidence |
| --- | --- | --- |
| Create `Creditcard` using every Excel column | [01_create_table.sql](sql/01_create_table.sql) creates all eight columns | [SHOW CREATE TABLE](evidence/show-create-table.sql) |
| Display the table structure | [03_inspect_table.sql](sql/03_inspect_table.sql) includes `DESCRIBE`, `SHOW CREATE TABLE`, and metadata queries | [Query results](evidence/query-results.md) |
| Use correct names, types, and character lengths | Source headings retained; `CHAR`, `VARCHAR`, `DECIMAL`, and `DATE` defined explicitly | [Data dictionary](docs/data-dictionary.md) and metadata output |
| Apply suitable constraints | Required fields use `NOT NULL`; the practice identifier has a format check | NULL, format, range, and length tests |
| Add a primary key | `ALTER TABLE ... ADD PRIMARY KEY (CreditcardNum)` | Duplicate identifier rejected with error 1062 |
| Require `Credit_Limit > 0` | Named `CHECK` constraint plus `NOT NULL` | Zero and negative inserts, and a zero-limit update, rejected |
| Execute the supplied INSERT script | [02_insert_records.sql](sql/02_insert_records.sql) preserves all record values | [All 15 loaded rows](evidence/loaded_records.csv) |

## Run in MySQL Workbench

Requires MySQL **8.0.16 or later**, which enforces `CHECK` constraints. The recorded execution is on 9.7.1; other versions have not been run for this project.

1. Connect to your MySQL server in Workbench.
2. Open and execute `sql/00_select_database.sql` to select the dedicated `week08_creditcard` schema.
3. In the same connection, execute `sql/01_create_table.sql` and then `sql/02_insert_records.sql`.
4. Execute `sql/03_inspect_table.sql` and `sql/04_verify_records.sql` to inspect the structure and loaded records.

The schema script deliberately fails if `Creditcard` already exists, and repeating the inserts raises a duplicate-key error. Use a fresh schema for a new run. The scripts do not drop tables or replace existing rows.

From the MySQL command-line client, start in this project directory and run:

```sql
SOURCE sql/00_select_database.sql;
SOURCE sql/01_create_table.sql;
SOURCE sql/02_insert_records.sql;
SOURCE sql/03_inspect_table.sql;
SOURCE sql/04_verify_records.sql;
```

## Reproduce the validation

Python is used only to extract the supplied sources, compare records, and automate tests against MySQL. The database schema and data loading are SQL.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/prepare_sources.py
python scripts/validate_mysql.py --user root --ask-password --database week08_creditcard_check
```

For a local server accessed through a Unix socket, add `--socket /path/to/mysql.sock`. For TCP, `--host` and `--port` are available. Use an account authorised to create the exercise schema. The validator refuses to use an existing schema. Each test is rolled back, and it confirms that the original 15 records remain unchanged. A successful run refreshes `evidence/` with actual server results, version details, and SQL hashes.

## Files

- `sources/` — unchanged Excel and Word files, plus the extracted original SQL text.
- `data/` — separate CSV extracts of the Excel and INSERT records.
- `sql/` — database setup, table creation, inserts, inspection, and verification.
- `docs/` — column decisions, source differences, and provenance.
- `scripts/` — source extraction and MySQL test automation.
- `evidence/` — executed table definitions, queries, records, and test results.

The four-character identifiers belong to this classroom dataset. This exercise does not model full payment-card numbers or provide a production payment-processing design.

## References

- [MySQL CHECK constraints](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html) — enforcement and the interaction with `NULL`.
- [MySQL DECIMAL](https://dev.mysql.com/doc/refman/8.0/en/fixed-point-types.html) — exact numeric storage for the two amount columns.
- [MySQL SHOW COLUMNS](https://dev.mysql.com/doc/refman/8.0/en/show-columns.html) — table structure inspection with `DESCRIBE` and `SHOW COLUMNS`.
