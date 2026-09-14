# Creditcard queries in MySQL

Counting, sorting, subqueries, and conditional selection on the same eight-column Creditcard table used in the [table design project](../week-08-mysql-creditcard/). The schema and all 15 source records are unchanged.

This activity covers **all thirteen Part 2 questions in the answer key**, plus the existing Part 1 setup. In the original exercise's continuous numbering, these are setup Q1–4 and retrieval Q5–17. All six subparts of the schema question are retained.

## Queries and results

- Run [original Q5–13](sql/questions_05_to_13.sql) and [original Q14–17](sql/questions_14_to_17.sql).
- [Run every answer-key SELECT verbatim, including alternatives](sql/answer_key_part2.sql).
- [Read every query and its complete output](evidence/query-results.md)
- [Check the original questions](docs/questions.md)
- [View execution checks and source hashes](evidence/validation.json)
- [Read all sixteen answer-key query outputs](evidence/answer-key-results.md)

| Original question | Coverage |
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
| 14 / Part 2 Q10. Count Mastercard cards | Eight cards; both Mastercard/Visa alternatives are retained in the answer-key script |
| 15 / Part 2 Q11. Count cards by city | `GROUP BY City` |
| 16 / Part 2 Q12. Count cards by cardholder | `GROUP BY CardHolder` |
| 17 / Part 2 Q13. Minimum/maximum limit by city | Grouped `MIN` and `MAX` |

The answer key confirms descending sorting for original Q8. Original Q9 selects the highest-limit card(s). Company counts refer to distinct issuers, not card types or card records. No names, amounts, or city spellings are cleaned or replaced.

The portfolio queries return additional columns and deterministic ordering. `COUNT(*)` and the key's `COUNT(CreditcardNum)` agree because the key is non-null. The answer key's `LIKE 'Aber%'` and the portfolio's `City = 'Aberdeen'` match this dataset, but are not identical filters for every possible city name. The reference script preserves both highest-limit alternatives and both Mastercard/Visa variants exactly; every variant was executed and checked against the source records.

## Run in MySQL Workbench

1. Use the existing `financial_db.creditcard` table created from the reference solution. If starting fresh, follow the [setup instructions](../week-08-mysql-creditcard/#run-in-mysql-workbench) once.
2. Execute `sql/questions_05_to_13.sql`, then `sql/questions_14_to_17.sql`. Alternatively, execute `sql/answer_key_part2.sql` to follow the answer key verbatim.
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

The saved results were executed on MySQL 9.7.1. All thirteen main-query comparisons and sixteen answer-key variants passed, and the schema and records remained unchanged. Each main query has a separate CSV in `evidence/`, alongside complete Markdown results and the machine-readable validation record.

## Source

[MySQL Activities W8-W9.docx](<sources/MySQL Activities W8-W9.docx>) and [MySQL Activities W8- Solutions.docx](<sources/MySQL Activities W8- Solutions.docx>) are preserved unchanged. The first document contains 26 continuously numbered questions; the answer key separates four setup questions from thirteen Part 2 questions. The earlier portfolio stopped at original Q13; original Q14–17 have now been added to complete the answer-key scope. Original Q18–26 continue in [Week 10](../week-10-mysql-creditcard-aggregation/).

The supplied W7 full solution remains the controlling schema/data source in the preceding project. The W6-named copy supplied later is byte-for-byte identical.
