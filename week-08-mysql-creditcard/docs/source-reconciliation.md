# Source reconciliation

Both supplied files contain 15 records and the same 15 identifiers. Matching by `CreditcardNum`, rather than row position, reveals 11 different cells across 8 records. Row order also differs for two identifiers. Neither source has duplicate identifiers or missing fields.

The supplied full solution now defines both the schema and INSERT statements. Its 15 INSERT statements match the earlier Word document exactly. The spreadsheet remains the comparison source; the 11 earlier differences below are unchanged.

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

`scripts/prepare_sources.py` checks all 15 full-solution INSERT statements against the Word file and converts the Excel data with its stored date system. It preserves the full solution byte-for-byte as `sql/full_solution.sql`, extracts its setup, schema, and INSERT statements into files `00` to `02`, and produces the two comparison CSVs. The original Word statement text also remains in `sources/original_inserts.sql`.

The MySQL validation then compares every loaded field against a fresh extraction of the Word file. The verified loaded totals are **15 records**, **150,700.00 in credit limits**, and **44,665.21 in total spending**. Monetary units are not specified by these source files, so no currency symbol is assigned.

The supplied workbook is `.xls`, although the activity text refers to `Creditcard.csv`. Both the unchanged workbook and a readable CSV extract are provided. CSV display formatting uses ISO dates and two decimal places. No identifier, date-notation, whitespace, or line-ending changes are applied to the complete runnable solution file.
