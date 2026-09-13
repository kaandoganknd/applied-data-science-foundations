# Constraint tests

Every case ran against MySQL and was rolled back. The 15 source records remained unchanged.

| Test | Expected | Observed | Result |
| --- | --- | --- | --- |
| Duplicate primary key | 1062 | 1062 | PASS |
| Zero credit limit | 3819 | 3819 | PASS |
| Negative credit limit | 3819 | 3819 | PASS |
| Zero credit limit on UPDATE | 3819 | 3819 | PASS |
| NULL CreditcardNum | 1048 | 1048 | PASS |
| NULL Creditcard_company | 1048 | 1048 | PASS |
| NULL Creditcard_type | 1048 | 1048 | PASS |
| NULL City | 1048 | 1048 | PASS |
| NULL CardHolder | 1048 | 1048 | PASS |
| NULL Issue_Date | 1048 | 1048 | PASS |
| NULL credit limit allowed by reference | Accept | Accept | PASS |
| NULL total spent allowed by reference | Accept | Accept | PASS |
| Short numeric identifier allowed | Accept | Accept | PASS |
| Nonnumeric identifier | 1366 | 1366 | PASS |
| Five-digit SMALLINT identifier allowed | Accept | Accept | PASS |
| SMALLINT upper boundary | Accept | Accept | PASS |
| SMALLINT lower boundary | Accept | Accept | PASS |
| SMALLINT overflow | 1264 | 1264 | PASS |
| Too long Creditcard_company | 1406 | 1406 | PASS |
| Too long Creditcard_type | 1406 | 1406 | PASS |
| Too long City | 1406 | 1406 | PASS |
| Too long CardHolder | 1406 | 1406 | PASS |
| Invalid calendar date | 1292 | 1292 | PASS |
| Nonnumeric credit limit | 1366 | 1366 | PASS |
| Credit limit exceeds DECIMAL capacity | 1264 | 1264 | PASS |
| Positive minimum currency unit | Accept | Accept | PASS |
| Leading zero converted to integer 1 | Accept | Accept | PASS |
| Repeated holder with a different identifier | Accept | Accept | PASS |
| Unicode holder name | Accept | Accept | PASS |
| No unrequested spending cap | Accept | Accept | PASS |
| Declared text and decimal boundaries | Accept | Accept | PASS |
