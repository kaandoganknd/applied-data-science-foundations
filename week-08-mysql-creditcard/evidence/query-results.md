# Executed MySQL queries

MySQL 9.7.1 (MySQL Community Server - GPL). All results below were fetched from the server.

```sql
DESCRIBE creditcard;
```

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| CreditcardNum | smallint | NO | PRI | NULL |  |
| Creditcard_company | varchar(100) | NO |  | NULL |  |
| Creditcard_type | varchar(50) | NO |  | NULL |  |
| Credit_Limit | decimal(9,2) | YES |  | NULL |  |
| Totalspent | decimal(9,2) | YES |  | NULL |  |
| City | varchar(50) | NO |  | NULL |  |
| CardHolder | varchar(100) | NO |  | NULL |  |
| Issue_Date | date | NO |  | NULL |  |

```sql
SHOW CREATE TABLE creditcard;
```

```sql
CREATE TABLE `creditcard` (
  `CreditcardNum` smallint NOT NULL,
  `Creditcard_company` varchar(100) NOT NULL,
  `Creditcard_type` varchar(50) NOT NULL,
  `Credit_Limit` decimal(9,2) DEFAULT NULL,
  `Totalspent` decimal(9,2) DEFAULT NULL,
  `City` varchar(50) NOT NULL,
  `CardHolder` varchar(100) NOT NULL,
  `Issue_Date` date NOT NULL,
  PRIMARY KEY (`CreditcardNum`),
  CONSTRAINT `cc_ch_creditlimit` CHECK ((`Credit_Limit` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```

```sql
SHOW INDEX FROM creditcard;
```

| Table | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| creditcard | 0 | PRIMARY | 1 | CreditcardNum | A | 2 | NULL | NULL |  | BTREE |  |  | YES | NULL |

```sql
SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH,
       NUMERIC_PRECISION, NUMERIC_SCALE, COLUMN_KEY
FROM information_schema.COLUMNS
WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'creditcard'
ORDER BY ORDINAL_POSITION;
```

| COLUMN_NAME | COLUMN_TYPE | IS_NULLABLE | CHARACTER_MAXIMUM_LENGTH | NUMERIC_PRECISION | NUMERIC_SCALE | COLUMN_KEY |
| --- | --- | --- | --- | --- | --- | --- |
| CreditcardNum | smallint | NO | NULL | 5 | 0 | PRI |
| Creditcard_company | varchar(100) | NO | 100 | NULL | NULL |  |
| Creditcard_type | varchar(50) | NO | 50 | NULL | NULL |  |
| Credit_Limit | decimal(9,2) | YES | NULL | 9 | 2 |  |
| Totalspent | decimal(9,2) | YES | NULL | 9 | 2 |  |
| City | varchar(50) | NO | 50 | NULL | NULL |  |
| CardHolder | varchar(100) | NO | 100 | NULL | NULL |  |
| Issue_Date | date | NO | NULL | NULL | NULL |  |

```sql
SELECT tc.CONSTRAINT_NAME, tc.CONSTRAINT_TYPE, tc.ENFORCED, cc.CHECK_CLAUSE
FROM information_schema.TABLE_CONSTRAINTS AS tc
LEFT JOIN information_schema.CHECK_CONSTRAINTS AS cc
    ON cc.CONSTRAINT_SCHEMA = tc.CONSTRAINT_SCHEMA
   AND cc.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
WHERE tc.TABLE_SCHEMA = DATABASE() AND tc.TABLE_NAME = 'creditcard'
ORDER BY tc.CONSTRAINT_TYPE, tc.CONSTRAINT_NAME;
```

| CONSTRAINT_NAME | CONSTRAINT_TYPE | ENFORCED | CHECK_CLAUSE |
| --- | --- | --- | --- |
| cc_ch_creditlimit | CHECK | YES | (`Credit_Limit` > 0) |
| PRIMARY | PRIMARY KEY | YES | NULL |

```sql
SELECT CreditcardNum, Creditcard_company, Creditcard_type, Credit_Limit,
       Totalspent, City, CardHolder, Issue_Date
FROM creditcard
ORDER BY CreditcardNum;
```

| CreditcardNum | Creditcard_company | Creditcard_type | Credit_Limit | Totalspent | City | CardHolder | Issue_Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1212 | Capital One | Visa | 5000.00 | 3476.50 | London | Krystal Jones | 2019-11-12 |
| 2332 | Capital One | Visa | 3000.00 | 1200.00 | Birmingham | Paul Carter | 2019-07-05 |
| 2456 | Coutts Bank | Mastercard | 50000.00 | 2567.77 | Aberdeen | Mario Brothers | 2020-01-20 |
| 3333 | American Express | American Express | 3500.00 | 1243.20 | London | Paul Jones | 2020-05-02 |
| 3334 | Virgin Credit | Mastercard | 1200.00 | 867.30 | Aberdeen | Mario Brothers | 2019-01-17 |
| 3343 | Virgin Credit | Visa | 4000.00 | 2300.50 | Glasgow | John Mackay | 2019-03-03 |
| 3434 | Capital One | Mastercard | 20000.00 | 5420.75 | Birmingham | Stanley Mathews | 2019-05-02 |
| 3554 | MBNA | Visa | 5000.00 | 3450.75 | Aberdeen | Julia Kathy | 2019-04-04 |
| 3556 | Egg | Mastercard | 4000.00 | 2300.00 | London | Paul Jones | 2019-04-20 |
| 3557 | Natwest | Visa | 12000.00 | 4002.10 | Aberdeen | Julia Kathy | 2018-04-20 |
| 4323 | Natwest | Mastercard | 24000.00 | 7325.50 | Glasgow | John Mackay | 2018-10-10 |
| 4456 | Barclaycard | Mastercard | 10000.00 | 3500.39 | London | John Smith | 2018-10-11 |
| 4489 | Natwest | Visa | 3000.00 | 1450.45 | Birmingham | Paul Carter | 2018-05-04 |
| 4535 | Egg | Mastercard | 1500.00 | 1234.40 | London | Paul Jones | 2018-12-12 |
| 4578 | Barclaycard | Mastercard | 4500.00 | 4325.60 | Aberdeen | Julia Kathy | 2020-01-22 |

```sql
SELECT COUNT(*) AS row_count,
       COUNT(DISTINCT CreditcardNum) AS distinct_identifiers,
       SUM(Credit_Limit <= 0) AS nonpositive_limits,
       SUM(Credit_Limit IS NULL) AS missing_limits,
       SUM(Credit_Limit) AS total_credit_limit,
       SUM(Totalspent) AS total_spent
FROM creditcard;
```

| row_count | distinct_identifiers | nonpositive_limits | missing_limits | total_credit_limit | total_spent |
| --- | --- | --- | --- | --- | --- |
| 15 | 15 | 0.00 | 0.00 | 150700.00 | 44665.21 |
