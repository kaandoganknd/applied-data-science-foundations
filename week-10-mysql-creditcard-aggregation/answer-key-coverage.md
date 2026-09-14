# W9-W10 answer-key coverage

All 26 Part 2 questions are in [answer_key_part2.sql](sql/answer_key_part2.sql), with [complete executed outputs](evidence/answer-key/query-results.md). AK labels follow the newer solutions document. Original Q labels include the four setup questions and therefore have a four-question offset.

| Part 2 | Topic | Earlier portfolio counterpart | Current coverage |
|---|---|---|---|
| AK01 | Record count | Q05 | Included |
| AK02 | Distinct company count | Q06 | Included |
| AK03 | Distinct company list | Q07 | Included |
| AK04 | Descending credit limits | Q08 | Included |
| AK05 | Highest credit limit | Q09 | Both source variants included |
| AK06 | London cards | Q10 | Included |
| AK07 | Aberdeen prefix and limit > 5000 | Q11 | Exact source prefix query included |
| AK08 | Limits of 1200, 3000, 4500 | Q12 | Included |
| AK09 | Non-London cards | Q13 | Included |
| AK10 | Mastercard count; Mastercard/Visa grouping | Q14 | All three source variants included |
| AK11 | Cards per city | Q15 | Included |
| AK12 | Cards per holder | Q16 | Included |
| AK13 | Minimum/maximum city limits | Q17 | Included |
| AK14 | Minimum/maximum limits and city spending | Q18 asks for total limits | New spending variant included; old limit query retained |
| AK15 | Minimum/maximum holder spending | Q19 | Included |
| AK16 | Total holder spending | Q20 | Included |
| AK17 | Remaining credit per card | Q21 | Included |
| AK18 | Cards per issue year | Q22 | Included |
| AK19 | Cards per calendar month | Q23 | Included; earlier Q23B retains year-month grouping |
| AK20 | Issue date after 2020-01-01 | Q24 asks for not-yet-issued cards | Fixed-cutoff query included; old future-date proxy retained |
| AK21 | Remaining credit per holder | Q25 | Included |
| AK22 | Remaining credit per issue year | Q26 | Included |
| AK23 | Remaining credit per calendar month | Not in earlier sheet | Added |
| AK24 | Expiry after 18 months | Not in earlier sheet | Added |
| AK25 | Replacement posting after 17 months | Not in earlier sheet | Added |
| AK26 | Limits above rounded average | Not in earlier sheet | Added |

## Source differences

- **Part 2 Q14:** the earlier sheet explicitly asks for the sum of credit limits. The newer solutions ask for total spending and use `SUM(TotalSpent)`. These are different measures; both queries and results remain available.
- **Part 2 Q20:** the earlier sheet asks about cards not yet issued. The newer solutions use a fixed `Issue_Date > '2020-01-01'` filter. The newer result is three cards, whereas the historical data have no future-dated cards at the earlier saved review date. These are different populations, not a display error.
- **AK23:** the source groups January with January across all years. It is a month-of-year summary, not a chronological balance history.
- **AK24–25:** the dates are calculated under the exercise assumptions, not verified expiry or dispatch events. AK25 preserves `Issue_Date + 17 months`; for some month-end dates this differs from subtracting one month from the calculated expiry.
- **AK26:** the answer key rounds the mean before filtering and returns one row per qualifying card. Repeated names would be legitimate if a holder had multiple qualifying cards.

The first thirteen questions contain the same 16 SELECT variants as the previous answer key. The complete file preserves source column projections, aliases, predicates, statement order, and alternatives. Existing broader `SELECT *` versions remain in their original files. `LIMIT 1` and maximum-equality variants agree on these records but differ if the maximum is tied; the `Aber%` predicate can also match places other than Aberdeen in a different dataset.

The document's internal title refers to “WEEK 4”, while its supplied filename says “W9-W10”. The filename is retained; coverage is determined from the document's Part 2 content.

## Sources and checks

- [W9-W10 solutions, unchanged](<sources/MySQL Activities W9-W10 - Solutions.docx>)
- [Earlier question sheet, unchanged](<../week-09-mysql-creditcard-queries/sources/MySQL Activities W8-W9.docx>)
- [Earlier answer key, unchanged](<../week-09-mysql-creditcard-queries/sources/MySQL Activities W8- Solutions.docx>)
- [Validation, hashes, all result rows, and date checks](evidence/answer-key/validation.json)

Validation runs in a read-only transaction against the supplied 15 INSERT records. It compares results as multisets, retaining duplicates, and verifies the specified descending sort separately. No production or real customer database is used.
