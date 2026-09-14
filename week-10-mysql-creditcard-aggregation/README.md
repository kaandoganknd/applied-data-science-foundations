# Creditcard aggregation and date analysis in MySQL

Grouped spending, available-credit calculations, and date-based queries on the unchanged `financial_db.creditcard` table. This is the **Week 10 home-exercise section**, continuing original questions **18–26** (Part 2 Q14–22). The [preceding project](../week-09-mysql-creditcard-queries/) contains all thirteen initial Part 2 questions and every supplied answer-key alternative.

## Read or run

- [All nine main queries and the additional month-grouping interpretation](sql/questions_18_to_26.sql)
- [Complete executed results](evidence/query-results.md)
- [Original questions](questions.md)
- [Validation and input hashes](evidence/validation.json)

The 15 records have £150,700.00 in combined credit limits, £44,665.21 in recorded spending, and £106,034.79 in remaining credit. Per-card, cardholder, city, and year calculations reconcile with the applicable totals. These are historical exercise records, not current customer accounts.

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

## Interpretation choices

**Month grouping:** Q23 pools the same calendar month across years. Q23B preserves chronology by grouping on year and month. Both are retained because the exercise does not specify which meaning of “each month” is intended.

**Not yet issued:** no card-status column exists. Q24 uses `Issue_Date > @as_of_date` as a future-date proxy; it does not prove actual issuance status. `Issue_Date` is required, so a missing-date query cannot identify unissued cards in this schema. All supplied dates fall in 2018–2020; no future-dated cards match the saved review date of 2026-09-13.

**Remaining credit:** calculated as `Credit_Limit - Totalspent`. Nullable amounts are not converted to zero. The supplied records contain no missing amounts; if new records do, review missingness before interpreting grouped sums, which omit NULL expressions.

## Run in MySQL Workbench

Use the existing exercise table. For a fresh server, first follow the [original setup](../week-08-mysql-creditcard/); do not rerun its INSERT statements on an already populated table.

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
```

Add `--socket /path/to/mysql.sock` for a local Unix socket, or use `--host` and `--port`. Validation runs in a read-only transaction, checks the schema and every source row, compares all result cells against independent Python calculations from the INSERT extract, and checks grouped totals. Full CSV outputs are saved in `evidence/`, including the header-only CSV for Q24's empty result.

The recorded run used MySQL 9.7.1. Nine main queries and the additional month-grouping view passed. The schema and all 15 records remained unchanged.

## Sources and scope

The supplied [W6 full solution](<sources/CREDITCARD SCRIPT W6 - FULL SOLUTION.txt>) is preserved byte-for-byte and is identical to the earlier W7-named solution. The newly supplied Excel file also matches the [existing spreadsheet source](../week-08-mysql-creditcard/sources/Creditcard_table.xls); the documented Excel/INSERT differences remain unchanged. Executed INSERT values control these queries.

The [exercise document](<../week-09-mysql-creditcard-queries/sources/MySQL Activities W8-W9.docx>) supplies the questions. [Employee Departments and Employee Projects](../week-10-mysql-employee-joins/) are the separate Week 10 class exercises.
