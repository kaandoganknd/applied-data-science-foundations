# Creditcard aggregation and date analysis in MySQL

Grouped spending, available-credit calculations, and date-based queries on the unchanged `financial_db.creditcard` table. This **Week 10 home-exercise section** now includes the complete W9-W10 solutions: **26 Part 2 questions and 29 SELECT variants**. The original question sheet and its queries are also retained; the two documents differ at Part 2 Q14 and Q20, and the solutions add Q23–26.

The [preceding project](../week-09-mysql-creditcard-queries/) covers the first thirteen Part 2 questions. Their source statements are unchanged in the newer answer key.

## Read or run

- [Complete W9-W10 answer key: all 26 questions and alternatives](sql/answer_key_part2.sql)
- [Every answer-key result table](evidence/answer-key/query-results.md) and [validation record](evidence/answer-key/validation.json)
- [Question-by-question coverage and source differences](answer-key-coverage.md)
- [Earlier question sheet: nine main queries and the month-grouping alternative](sql/questions_18_to_26.sql)
- [Earlier-sheet results](evidence/query-results.md), [question text](questions.md), and [validation](evidence/validation.json)

The 15 records have £150,700.00 in combined credit limits, £44,665.21 in recorded spending, and £106,034.79 in remaining credit. Per-card, cardholder, city, and year calculations reconcile with the applicable totals. These are historical exercise records, not current customer accounts.

### Earlier question sheet

| Original question | Part 2 | Query |
|---|---|---|
| 18 | 14 | Maximum, minimum, and sum of credit limits by city |
| 19 | 15 | Minimum and maximum spending by cardholder |
| 20 | 16 | Total credit used by cardholder |
| 21 | 17 | Remaining credit on each card |
| 22 | 18 | Card counts by issue year |
| 23 | 19 | Card counts by calendar month; additional year-month view |
| 24 | 20 | Future-dated records, with an explicit interpretation limit |
| 25 | 21 | Total remaining credit by cardholder |
| 26 | 22 | Remaining credit by issue year |

### W9-W10 solutions: changed and additional questions

| Answer-key question | Query | Result on the supplied records |
|---|---|---|
| AK14 | Minimum/maximum limits and total **spending** by city | Spending reconciles to £44,665.21 |
| AK20 | Cards issued strictly after 2020-01-01 | 3 cards |
| AK23 | Remaining credit by calendar month | 8 months; £106,034.79 in total |
| AK24 | Issue date plus 18 months | Expiry dates for all 15 cards |
| AK25 | Issue date plus 17 months | Replacement dates for all 15 cards |
| AK26 | Card limits above the rounded average | 4 cards; average limit £10,046.67 |

`AK` labels follow Part 2 of the newer solutions document; they do not replace the original Q18–26 numbering. The complete answer-key file also retains both highest-limit alternatives and all three Mastercard/Visa variants.

## Interpretation choices

**Month grouping:** Q23 pools the same calendar month across years. Q23B preserves chronology by grouping on year and month. Both are retained because the exercise does not specify which meaning of “each month” is intended.

**Not yet issued:** no card-status column exists. Q24 uses `Issue_Date > @as_of_date` as a future-date proxy; it does not prove actual issuance status. `Issue_Date` is required, so a missing-date query cannot identify unissued cards in this schema. All supplied dates fall in 2018–2020; no future-dated cards match the saved review date of 2026-09-13.

**Remaining credit:** calculated as `Credit_Limit - Totalspent`. Nullable amounts are not converted to zero. The supplied records contain no missing amounts; if new records do, review missingness before interpreting grouped sums, which omit NULL expressions.

**Expiry and replacement:** AK24 and AK25 use the exercise assumptions of 18 and 17 calendar months from issue, not real bank policy. Month-end dates can make issue + 17 months differ from expiry − 1 month; the original formula is retained, and date-boundary checks are included with the results.

**Above-average limit:** AK26 follows the answer key's mean rounded to two decimals and compares individual card limits, not each holder's combined limit. The source statements are preserved rather than silently changing the threshold.

## Run in MySQL Workbench

Use the existing exercise table. For a fresh server, first follow the [original setup](../week-08-mysql-creditcard/); do not rerun its INSERT statements on an already populated table.

For the complete newer solutions, open and run `sql/answer_key_part2.sql` from the beginning. AK26 sets its session variable immediately before using it. No review date is needed for this file.

To reproduce the saved date-dependent result, run this before opening `sql/questions_18_to_26.sql`:

```sql
SET @as_of_date = '2026-09-13';
```

Without an explicit date, the script uses the current date when the session variable is unset. All statements are read-only queries or session-variable assignments. The source table is not altered.

## Reproduce validation

Clone the full repository so the shared source and helper files remain available. From this directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate_aggregations.py --user root --ask-password --as-of 2026-09-13
python scripts/validate_answer_key.py --user root --ask-password
```

Add `--socket /path/to/mysql.sock` for a local Unix socket, or use `--host` and `--port`. Validation runs in a read-only transaction, checks the schema and every source row, compares all result cells against independent Python calculations from the INSERT extract, and checks grouped totals. Full CSV outputs are saved in `evidence/`, including the header-only CSV for Q24's empty result.

The recorded runs used MySQL 9.7.1. The earlier nine main queries and additional month-grouping view passed. The newer validator verifies every SQL statement against the DOCX, runs all 29 SELECT variants, independently computes their expected results from the reference CSV, tests date boundaries, and reconciles grouped totals. Complete results and one CSV per variant are saved under `evidence/answer-key/`. The schema and all 15 records remained unchanged.

## Sources and scope

The supplied [W6 full solution](<sources/CREDITCARD SCRIPT W6 - FULL SOLUTION.txt>) is preserved byte-for-byte and is identical to the earlier W7-named solution. The newly supplied Excel file also matches the [existing spreadsheet source](../week-08-mysql-creditcard/sources/Creditcard_table.xls); the documented Excel/INSERT differences remain unchanged. Executed INSERT values control these queries.

The [earlier exercise document](<../week-09-mysql-creditcard-queries/sources/MySQL Activities W8-W9.docx>) and [W9-W10 solutions document](<sources/MySQL Activities W9-W10 - Solutions.docx>) are both retained unchanged. Their differing questions are documented rather than treated as interchangeable. [Employee Departments and Employee Projects](../week-10-mysql-employee-joins/) are the separate Week 10 class exercises.
