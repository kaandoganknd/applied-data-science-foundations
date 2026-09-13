# Source reconciliation

Both supplied files contain 15 records and the same 15 identifiers. Matching by `CreditcardNum`, rather than row position, reveals 11 different cells across 8 records. Row order also differs for two identifiers. Neither source has duplicate identifiers or missing fields.

The spreadsheet defines the required columns. The Word document supplies the records to load because the final exercise step explicitly asks to execute that INSERT script. Differences are retained in the separate source extracts; no mixed or silently corrected dataset is created.

| Identifier | Column | Excel value | INSERT document value loaded |
| --- | --- | --- | --- |
| 1212 | Totalspent | 3476.00 | 3476.50 |
| 2456 | City | Aberdeem | Aberdeen |
| 2456 | Issue_Date | 2020-01-22 | 2020-01-20 |
| 3334 | Creditcard_company | Virgin Credit Card | Virgin Credit |
| 3334 | City | Aberdeeen | Aberdeen |
| 3343 | Creditcard_company | Virgin Credit Card | Virgin Credit |
| 3554 | City | Aberdeeen | Aberdeen |
| 3557 | City | Aberdeeen | Aberdeen |
| 3557 | Issue_Date | 2020-04-20 | 2018-04-20 |
| 4535 | Totalspent | 1235.40 | 1234.40 |
| 4578 | Issue_Date | 2020-02-29 | 2020-01-22 |

The comparison is also available as [CSV](source-differences.csv). [source-review.json](source-review.json) records the SHA-256 hashes of the unchanged original files and maximum observed text lengths across both sources.

## Reproduction and loaded totals

`scripts/prepare_sources.py` extracts all 15 INSERT statements from the Word file, checks their column list, and converts the Excel data with its stored date system. It produces the two CSV extracts, the comparison, and the runnable INSERT script. The original statement text remains in `sources/original_inserts.sql` for inspection; use the normalized `sql/02_insert_records.sql` for the runnable workflow.

The MySQL validation then compares every loaded field against a fresh extraction of the Word file. The verified loaded totals are **15 records**, **150,700.00 in credit limits**, and **44,665.21 in total spending**. Monetary units are not specified by these source files, so no currency symbol is assigned.

The supplied workbook is `.xls`, although the activity text refers to `Creditcard.csv`. Both the unchanged workbook and a readable CSV extract are provided. Formatting normalization is limited to date notation, identifier text, two-decimal amount display, and consistent table/column casing.
