# Columns and constraints in the supplied solution

The schema below follows the full solution exactly. Although the source records contain no missing fields, `Credit_Limit` and `Totalspent` are nullable in the supplied table definition. No additional constraints are added. `DECIMAL(9,2)` stores nine digits in total, including two decimal places.

| Column | MySQL definition | Source observation | Reason |
| --- | --- | --- | --- |
| `CreditcardNum` | `SMALLINT PRIMARY KEY` | All 15 source identifiers have four digits | Signed integer key, from -32,768 to 32,767; leading zeros are not preserved |
| `Creditcard_company` | `VARCHAR(100) NOT NULL` | Longest supplied label is 18 characters | Capacity matches the full solution |
| `Creditcard_type` | `VARCHAR(50) NOT NULL` | Longest supplied label is 16 characters | Capacity matches the full solution |
| `Credit_Limit` | `DECIMAL(9,2)` | Values range from 1,200.00 to 50,000.00 | Positive values or NULL are accepted under the reference CHECK |
| `Totalspent` | `DECIMAL(9,2)` | INSERT values range from 867.30 to 7,325.50 | Nullable exact two-decimal amount |
| `City` | `VARCHAR(50) NOT NULL` | Longest observed city value is 10 characters | Allows every source spelling and future longer city names |
| `CardHolder` | `VARCHAR(100) NOT NULL` | Longest supplied name is 15 characters | Names are variable-length and may recur on different cards |
| `Issue_Date` | `DATE NOT NULL` | Calendar dates without time components | Stored as a date rather than an Excel serial number or free-form string |

The solution does not specify a storage engine, character set, or collation. The verified server supplied InnoDB and utf8mb4 defaults, recorded by `SHOW CREATE TABLE`. Length and invalid-value rejection tests ran under that server's strict SQL mode.

## Keys and checks

- `CreditcardNum SMALLINT PRIMARY KEY` defines the key inline. Duplicate and null identifiers are rejected.
- `cc_ch_creditlimit CHECK (Credit_Limit > 0)` rejects zero and negative limits on inserts and updates. It accepts NULL because the column is nullable and the CHECK expression then evaluates to unknown. This is retained to match the source.
- There is no four-digit identifier constraint. Shorter and five-digit integers within the SMALLINT range are accepted; leading zeros are converted to an integer value.
- Names, companies, cities, and card types are not unique keys. Several records share these values.

No rule requiring `Totalspent <= Credit_Limit` is supplied, so none is invented. A test confirms that the schema accepts a higher spending value. No foreign keys are introduced because the task supplies a single table and no referenced entity definitions.

## Case and date notation

The supplied solution creates `creditcard` but inserts into `CreditCard`. Both spellings are preserved. The verified macOS server resolves them to the same table with `lower_case_table_names=2`. A case-sensitive server may report that the INSERT target does not exist. The `Totalspent`/`TotalSpent` difference is also preserved; MySQL column names are case insensitive.

The runnable solution preserves `YYYY/MM/DD` dates exactly. MySQL 9.7.1 accepted them and emitted warning 4095 for each INSERT, recommending hyphens. The comparison CSVs display dates as `YYYY-MM-DD`; this display conversion does not modify the original SQL files.

References: [CHECK constraints](https://dev.mysql.com/doc/refman/8.0/en/create-table-check-constraints.html), [DECIMAL types](https://dev.mysql.com/doc/refman/8.0/en/fixed-point-types.html), [identifier case sensitivity](https://dev.mysql.com/doc/refman/26.7/en/identifier-case-sensitivity.html).
