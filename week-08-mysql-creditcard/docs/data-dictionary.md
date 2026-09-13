# Column and constraint decisions

Column names and their order follow the spreadsheet. All eight fields are required in this exercise, so all are `NOT NULL`. The source files contain no missing fields. Numeric precision and string capacity are separate concepts: `DECIMAL(10,2)` allows ten digits in total, including two decimal places; `VARCHAR(50)` allows up to fifty characters.

| Column | MySQL definition | Source observation | Reason |
| --- | --- | --- | --- |
| `CreditcardNum` | `CHAR(4) NOT NULL` | All 15 source identifiers have four digits | A fixed-width identifier; preserves leading zeros and acts as the primary key |
| `Creditcard_company` | `VARCHAR(50) NOT NULL` | Longest supplied label is 18 characters | Allows every label in both sources, with room for longer names |
| `Creditcard_type` | `VARCHAR(30) NOT NULL` | Longest supplied label is 16 characters | Stores the supplied card type as text without restricting the domain to the current sample |
| `Credit_Limit` | `DECIMAL(10,2) NOT NULL` | Values range from 1,200.00 to 50,000.00 | Exact two-decimal amount; a named constraint requires a value above zero |
| `Totalspent` | `DECIMAL(10,2) NOT NULL` | INSERT values range from 867.30 to 7,325.50 | Exact two-decimal amount without floating-point approximation |
| `City` | `VARCHAR(50) NOT NULL` | Longest observed city value is 10 characters | Allows every source spelling and future longer city names |
| `CardHolder` | `VARCHAR(100) NOT NULL` | Longest supplied name is 15 characters | Names are variable-length and may recur on different cards |
| `Issue_Date` | `DATE NOT NULL` | Calendar dates without time components | Stored as a date rather than an Excel serial number or free-form string |

`utf8mb4` supports names containing accented and other Unicode characters. The validator checks that a Unicode name is stored unchanged, that values at each declared text limit are accepted, and that overlong values are rejected under the selected strict SQL mode.

## Keys and checks

- `PRIMARY KEY (CreditcardNum)` enforces unique, non-null identifiers. The task explicitly asks to add the key, so it is a separate `ALTER TABLE` step.
- `chk_credit_limit_positive` enforces `Credit_Limit > 0` on both inserts and updates. `NOT NULL` is also necessary: a check alone does not reject an unknown result caused by a null value.
- `chk_practice_card_identifier` enforces four digits, matching the identifiers in this exercise. It is an additional documented design choice, not a claim about real payment-card number lengths.
- Names, companies, cities, and card types are not unique keys. Several records share these values.

No rule requiring `Totalspent <= Credit_Limit` is supplied, so none is invented. A test confirms that the schema accepts a higher spending value. No foreign keys are introduced because the task supplies a single table and no referenced entity definitions.

## Case and date notation

The exercise names the table `Creditcard`; the Word document writes `CreditCard`. The runnable scripts consistently use `Creditcard` to avoid operating-system-dependent table-name case behaviour. The spreadsheet spells `Totalspent`, while the Word INSERT list spells `TotalSpent`; the public schema follows the spreadsheet. MySQL column names are case insensitive.

Dates are written as `YYYY-MM-DD` in the runnable INSERT script. This changes notation only: the year, month, and day from the Word document are preserved. Excel serial dates are decoded independently for the comparison CSV.

References: [CHECK constraints](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html), [DECIMAL types](https://dev.mysql.com/doc/refman/8.0/en/fixed-point-types.html), [identifier case sensitivity](https://dev.mysql.com/doc/refman/26.7/en/identifier-case-sensitivity.html).
