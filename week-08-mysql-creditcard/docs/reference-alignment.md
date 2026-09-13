# Alignment with the full solution

The supplied `CREDITCARD SCRIPT W7 - FULL SOLUTION.txt` supersedes the earlier portfolio schema. Its complete contents are preserved in `sources/` and copied byte-for-byte to `sql/full_solution.sql`. The current executed evidence is from this unchanged solution.

| Item | Earlier portfolio implementation | Current full solution |
| --- | --- | --- |
| Database | `week08_creditcard` | `financial_db` |
| Table creation | `CREATE TABLE Creditcard` | `CREATE TABLE IF NOT EXISTS creditcard` |
| Identifier | `CHAR(4)` | `SMALLINT PRIMARY KEY` |
| Company length | `VARCHAR(50)` | `VARCHAR(100)` |
| Card type length | `VARCHAR(30)` | `VARCHAR(50)` |
| Both amounts | `DECIMAL(10,2) NOT NULL` | `DECIMAL(9,2)`, nullable |
| Primary key declaration | Separate `ALTER TABLE` | Inline in the column definition |
| Credit-limit check | `chk_credit_limit_positive` | `cc_ch_creditlimit` |
| Four-digit check | Additional format constraint | None in the solution |
| Dates in INSERT statements | Hyphen separators | Original slash separators |
| Table-name casing | Standardized | Original `creditcard` / `CreditCard` mix |
| Engine, charset, strict mode | Explicitly set by project SQL | Inherited from server/session defaults |
| INSERT transaction wrapper | Added transaction | No added wrapper |

All 15 record values remain the same. The earlier schema was a stricter independent design, not an exact reproduction of this later-supplied solution. Its former validation results are superseded by the current 31 tests, including accepted NULL amounts and numeric-identifier behaviour.

The exact-copy SHA-256 is `5ca38881ae8c529d0a263b61f335a4570bdd32951a0c9da268751de664c86f79`. Git preserves the source and full SQL file's original CRLF line endings through the project `.gitattributes` file.

## Execution conditions

The solution completed on MySQL 9.7.1 with case-insensitive table lookup (`lower_case_table_names=2`) and strict SQL mode. All 18 source statements executed, producing 15 records. The slash-date notation generated 15 warnings with code 4095; these were recorded rather than silently removed. The test runner rolls back every test and confirms the 15 loaded records are unchanged.

The inspection and verification queries are separate supporting files. They do not change the supplied solution or its loaded records. The project path retains the original Week 8 activity label; the reference file retains its W7 filename.
