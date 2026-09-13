# Creditcard table design and validation in MySQL

A relational database exercise reproduced from the supplied **CREDITCARD SCRIPT W7 - FULL SOLUTION.txt**. The [runnable full solution](sql/full_solution.sql) is byte-for-byte identical to that file, including its original line endings, names, data types, constraints, and INSERT statements. It creates `financial_db.creditcard` with eight columns and 15 records.

The unchanged full solution was executed on **MySQL Community Server 9.7.1**. All 15 loaded records matched the source across every field, and **31 schema behaviour tests passed**. These include acceptance tests for nullable amounts and numeric identifiers, as specified by the solution. Read the [executed queries and results](evidence/query-results.md) and [test results](evidence/constraint-tests.md).

The source filename says W7, while the activity originally supplied with this project says Week 8. The existing project path is retained; the source filename is preserved exactly. See [reference alignment](docs/reference-alignment.md) for the changes from the earlier portfolio implementation.

## Source reconciliation

The spreadsheet and INSERT document contain the same 15 identifiers, but **11 cells across 8 records differ**. The differences include spending amounts, dates, city spellings, and company names. The exercise asks to execute the supplied INSERT statements, so those values are loaded into MySQL. The spreadsheet defines the column names and provides a separate comparison source.

All three original source files and both CSV extracts are included. The full solution's 15 INSERT statements match the earlier Word document. See the [source comparison](docs/source-reconciliation.md) for every difference and the [source manifest](docs/source-review.json) for file hashes and observed text lengths.

## Exercise coverage

| Requirement | Implementation | Executed evidence |
| --- | --- | --- |
| Create the table using every Excel column | [Full solution](sql/full_solution.sql) creates `creditcard` with all eight columns | [SHOW CREATE TABLE](evidence/show-create-table.sql) |
| Display the table structure | [03_inspect_table.sql](sql/03_inspect_table.sql) includes `DESCRIBE`, `SHOW CREATE TABLE`, and metadata queries | [Query results](evidence/query-results.md) |
| Use source names, types, and character lengths | `SMALLINT`, `VARCHAR`, `DECIMAL(9,2)`, and `DATE` match the full solution | [Data dictionary](docs/data-dictionary.md) and metadata output |
| Apply the reference constraints | Required text/date fields use `NOT NULL`; both amounts remain nullable | NULL, range, and length tests |
| Add a primary key | Inline `CreditcardNum SMALLINT PRIMARY KEY`, as in the solution | Duplicate identifier rejected with error 1062 |
| Require `Credit_Limit > 0` | `cc_ch_creditlimit CHECK (Credit_Limit > 0)` | Zero/negative limits rejected; `NULL` accepted, as defined by the source |
| Execute the supplied INSERT script | [02_insert_records.sql](sql/02_insert_records.sql) preserves all record values | [All 15 loaded rows](evidence/loaded_records.csv) |

## Run in MySQL Workbench

Requires MySQL **8.0.16 or later**, which enforces `CHECK` constraints. The recorded execution is on 9.7.1; other versions have not been run for this project.

1. Connect to a fresh exercise server with no existing `financial_db` schema.
2. Open and execute `sql/full_solution.sql` once.
3. In the same connection, execute `sql/03_inspect_table.sql` and `sql/04_verify_records.sql` to inspect the structure and loaded records.

The source uses `IF NOT EXISTS` for the database and table, but its INSERT statements are not idempotent: a second run raises duplicate-key errors. The split files `00`, `01`, and `02` contain the same statements for step-by-step reading; run either the full solution or those three files, not both.

The original solution mixes `creditcard` and `CreditCard`. The verified server used `lower_case_table_names=2`; the unchanged script can fail on a server with case-sensitive table lookup. It also uses dates with `/`, which produced 15 MySQL deprecation warnings (4095) without rejecting any records. These source behaviours are preserved and recorded in [validation.json](evidence/validation.json).

From the MySQL command-line client, start in this project directory and run:

```sql
SOURCE sql/full_solution.sql;
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
python scripts/validate_mysql.py --user root --ask-password
```

For a local server accessed through a Unix socket, add `--socket /path/to/mysql.sock`. For TCP, `--host` and `--port` are available. Use an account authorised to create `financial_db` on a fresh exercise server. The validator refuses an existing `financial_db`, case-sensitive table lookup, or a session without strict SQL mode. Each test is rolled back, and it confirms that the original 15 records remain unchanged. A successful run refreshes `evidence/` with actual server results, source warnings, version details, and SQL hashes.

## Files

- `sources/` — unchanged full-solution text, Excel and Word files, plus the extracted Word INSERT text.
- `data/` — separate CSV extracts of the Excel and INSERT records.
- `sql/` — database setup, table creation, inserts, inspection, and verification.
- `docs/` — column decisions, source differences, and provenance.
- `scripts/` — source extraction and MySQL test automation.
- `evidence/` — executed table definitions, queries, records, and test results.

The supplied four-digit identifiers are stored as `SMALLINT` in the reference. Leading zeros are therefore not preserved. This exercise does not model full payment-card numbers or provide a production payment-processing design.

## References

- [MySQL CHECK constraints](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html) — enforcement and the interaction with `NULL`.
- [MySQL DECIMAL](https://dev.mysql.com/doc/refman/8.0/en/fixed-point-types.html) — exact numeric storage for the two amount columns.
- [MySQL SHOW COLUMNS](https://dev.mysql.com/doc/refman/8.0/en/show-columns.html) — table structure inspection with `DESCRIBE` and `SHOW COLUMNS`.
