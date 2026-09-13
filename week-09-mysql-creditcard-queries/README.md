# Creditcard queries in MySQL

Counting, sorting, subqueries, and conditional selection on the same eight-column Creditcard table used in the [table design project](../week-08-mysql-creditcard/). The schema and all 15 source records are unchanged.

This activity covers **questions 1–13** in the supplied exercise. Questions 1–4 are the existing setup and validation; questions 5–13 add nine retrieval queries. The original Word numbering is retained, including all six subparts of question 3.

## Queries and results

- [Run the SQL](sql/questions_05_to_13.sql)
- [Read every query and its complete output](evidence/query-results.md)
- [Check the original questions](docs/questions.md)
- [View execution checks and source hashes](evidence/validation.json)

| Question | Coverage |
| --- | --- |
| 1. Create the table with every source column | [Unchanged full solution](../week-08-mysql-creditcard/sql/full_solution.sql) |
| 2. Display its structure | Fresh `DESCRIBE` output in [query results](evidence/query-results.md) |
| 3a–3f. Names, types, lengths, constraints, primary key, positive limit | [Verified schema](evidence/table-structure.sql) and [constraint tests](../week-08-mysql-creditcard/evidence/constraint-tests.md) |
| 4. Execute the supplied INSERT statements | [Setup and original 15 records](../week-08-mysql-creditcard/); this run checks every stored field against that source |
| 5. Count records | `COUNT(*)` |
| 6. Count companies | `COUNT(DISTINCT Creditcard_company)` |
| 7. List companies | `DISTINCT` with alphabetical ordering |
| 8. Order cards by highest limit | Descending limit, then identifier for deterministic ties |
| 9. Find the highest-limit card | `MAX` subquery; returns all ties |
| 10. Select London cards | Equality filter |
| 11. Select Aberdeen cards above £5,000 | `AND` with a strictly greater-than comparison |
| 12. Select limits of £1,200, £3,000, or £4,500 | `IN` |
| 13. Select cards outside London | `<>`; `City` is required by the source schema |

Question 8's wording is ambiguous. It is interpreted as listing all cards in descending credit-limit order; question 9 separately selects only the highest-limit card(s). Company counts refer to distinct issuers, not card types or card records. No names, amounts, or city spellings are cleaned or replaced.

## Run in MySQL Workbench

1. Use the existing `financial_db.creditcard` table created from the reference solution. If starting fresh, follow the [setup instructions](../week-08-mysql-creditcard/#run-in-mysql-workbench) once.
2. Open and execute `sql/questions_05_to_13.sql`.
3. Compare each result tab with [the saved outputs](evidence/query-results.md).

Do not rerun the original INSERT script on an already populated table. The Week 9 SQL contains only database selection and read-only queries; it does not create, update, or delete records. The setup's case-sensitivity and date-format caveats still apply.

## Reproduce the checks

From this directory, on a server containing the unchanged exercise table:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/run_queries.py --user root --ask-password
```

For a local Unix socket, add `--socket /path/to/mysql.sock`; TCP connections also accept `--host` and `--port`. The runner reads the existing table in a read-only transaction, checks the schema and all source records, executes every query, and compares every returned cell with independent calculations from the reference INSERT extract. A mismatch stops the run without changing the table. For strict source matching, its schema comparison includes the reference engine, charset, and collation shown in `SHOW CREATE TABLE`.

The saved results were executed on MySQL 9.7.1. All nine query comparisons passed, and the schema and records remained unchanged. Each query has a separate CSV in `evidence/`, alongside the complete Markdown results and machine-readable validation record.

## Source

[MySQL Activities W8-W9.docx](<sources/MySQL Activities W8-W9.docx>) is preserved unchanged. It contains 26 main questions; this folder completes the requested first 13 only. The supplied W7 full solution remains the controlling schema/data source in the preceding project.
