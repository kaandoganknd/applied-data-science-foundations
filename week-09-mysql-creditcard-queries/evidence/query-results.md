# Executed Creditcard queries

MySQL 9.7.1. Read-only queries on the 15 unchanged reference records in `financial_db.creditcard`.

Questions 1–4 use the existing setup; the structure below was read again in this run. Original Q5–17 cover all thirteen Part 2 questions, in source order with complete outputs.

## Table structure (Q2–Q3)

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

## Q05. Number of records.

```sql
SELECT COUNT(*) AS record_count
FROM creditcard;
```

| record_count |
| --- |
| 15 |

Rows returned: 1.

## Q06. Number of distinct credit card companies, not card types or records.

```sql
SELECT COUNT(DISTINCT Creditcard_company) AS company_count
FROM creditcard;
```

| company_count |
| --- |
| 8 |

Rows returned: 1.

## Q07. List of distinct credit card companies.

```sql
SELECT DISTINCT Creditcard_company
FROM creditcard
ORDER BY Creditcard_company;
```

| Creditcard_company |
| --- |
| American Express |
| Barclaycard |
| Capital One |
| Coutts Bank |
| Egg |
| MBNA |
| Natwest |
| Virgin Credit |

Rows returned: 8.

## Q08. All cards ordered from highest to lowest credit limit.

```sql
SELECT *
FROM creditcard
ORDER BY Credit_Limit DESC, CreditcardNum;
```

| CreditcardNum | Creditcard_company | Creditcard_type | Credit_Limit | Totalspent | City | CardHolder | Issue_Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2456 | Coutts Bank | Mastercard | 50000.00 | 2567.77 | Aberdeen | Mario Brothers | 2020-01-20 |
| 4323 | Natwest | Mastercard | 24000.00 | 7325.50 | Glasgow | John Mackay | 2018-10-10 |
| 3434 | Capital One | Mastercard | 20000.00 | 5420.75 | Birmingham | Stanley Mathews | 2019-05-02 |
| 3557 | Natwest | Visa | 12000.00 | 4002.10 | Aberdeen | Julia Kathy | 2018-04-20 |
| 4456 | Barclaycard | Mastercard | 10000.00 | 3500.39 | London | John Smith | 2018-10-11 |
| 1212 | Capital One | Visa | 5000.00 | 3476.50 | London | Krystal Jones | 2019-11-12 |
| 3554 | MBNA | Visa | 5000.00 | 3450.75 | Aberdeen | Julia Kathy | 2019-04-04 |
| 4578 | Barclaycard | Mastercard | 4500.00 | 4325.60 | Aberdeen | Julia Kathy | 2020-01-22 |
| 3343 | Virgin Credit | Visa | 4000.00 | 2300.50 | Glasgow | John Mackay | 2019-03-03 |
| 3556 | Egg | Mastercard | 4000.00 | 2300.00 | London | Paul Jones | 2019-04-20 |
| 3333 | American Express | American Express | 3500.00 | 1243.20 | London | Paul Jones | 2020-05-02 |
| 2332 | Capital One | Visa | 3000.00 | 1200.00 | Birmingham | Paul Carter | 2019-07-05 |
| 4489 | Natwest | Visa | 3000.00 | 1450.45 | Birmingham | Paul Carter | 2018-05-04 |
| 4535 | Egg | Mastercard | 1500.00 | 1234.40 | London | Paul Jones | 2018-12-12 |
| 3334 | Virgin Credit | Mastercard | 1200.00 | 867.30 | Aberdeen | Mario Brothers | 2019-01-17 |

Rows returned: 15.

The answer key confirms descending sorting for Q8; Q9 separately selects the maximum-limit card(s).

## Q09. Card(s) with the highest limit; retain every tie.

```sql
SELECT *
FROM creditcard
WHERE Credit_Limit = (SELECT MAX(Credit_Limit) FROM creditcard)
ORDER BY CreditcardNum;
```

| CreditcardNum | Creditcard_company | Creditcard_type | Credit_Limit | Totalspent | City | CardHolder | Issue_Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2456 | Coutts Bank | Mastercard | 50000.00 | 2567.77 | Aberdeen | Mario Brothers | 2020-01-20 |

Rows returned: 1.

## Q10. Cards issued in London.

```sql
SELECT *
FROM creditcard
WHERE City = 'London'
ORDER BY CreditcardNum;
```

| CreditcardNum | Creditcard_company | Creditcard_type | Credit_Limit | Totalspent | City | CardHolder | Issue_Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1212 | Capital One | Visa | 5000.00 | 3476.50 | London | Krystal Jones | 2019-11-12 |
| 3333 | American Express | American Express | 3500.00 | 1243.20 | London | Paul Jones | 2020-05-02 |
| 3556 | Egg | Mastercard | 4000.00 | 2300.00 | London | Paul Jones | 2019-04-20 |
| 4456 | Barclaycard | Mastercard | 10000.00 | 3500.39 | London | John Smith | 2018-10-11 |
| 4535 | Egg | Mastercard | 1500.00 | 1234.40 | London | Paul Jones | 2018-12-12 |

Rows returned: 5.

## Q11. Cards issued in Aberdeen with a limit strictly greater than GBP 5,000.

```sql
SELECT *
FROM creditcard
WHERE City = 'Aberdeen' AND Credit_Limit > 5000
ORDER BY CreditcardNum;
```

| CreditcardNum | Creditcard_company | Creditcard_type | Credit_Limit | Totalspent | City | CardHolder | Issue_Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2456 | Coutts Bank | Mastercard | 50000.00 | 2567.77 | Aberdeen | Mario Brothers | 2020-01-20 |
| 3557 | Natwest | Visa | 12000.00 | 4002.10 | Aberdeen | Julia Kathy | 2018-04-20 |

Rows returned: 2.

## Q12. Cards with any of the three specified credit limits.

```sql
SELECT *
FROM creditcard
WHERE Credit_Limit IN (1200, 3000, 4500)
ORDER BY CreditcardNum;
```

| CreditcardNum | Creditcard_company | Creditcard_type | Credit_Limit | Totalspent | City | CardHolder | Issue_Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2332 | Capital One | Visa | 3000.00 | 1200.00 | Birmingham | Paul Carter | 2019-07-05 |
| 3334 | Virgin Credit | Mastercard | 1200.00 | 867.30 | Aberdeen | Mario Brothers | 2019-01-17 |
| 4489 | Natwest | Visa | 3000.00 | 1450.45 | Birmingham | Paul Carter | 2018-05-04 |
| 4578 | Barclaycard | Mastercard | 4500.00 | 4325.60 | Aberdeen | Julia Kathy | 2020-01-22 |

Rows returned: 4.

## Q13. Cards not issued in London. City is NOT NULL in the source schema.

```sql
SELECT *
FROM creditcard
WHERE City <> 'London'
ORDER BY CreditcardNum;
```

| CreditcardNum | Creditcard_company | Creditcard_type | Credit_Limit | Totalspent | City | CardHolder | Issue_Date |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2332 | Capital One | Visa | 3000.00 | 1200.00 | Birmingham | Paul Carter | 2019-07-05 |
| 2456 | Coutts Bank | Mastercard | 50000.00 | 2567.77 | Aberdeen | Mario Brothers | 2020-01-20 |
| 3334 | Virgin Credit | Mastercard | 1200.00 | 867.30 | Aberdeen | Mario Brothers | 2019-01-17 |
| 3343 | Virgin Credit | Visa | 4000.00 | 2300.50 | Glasgow | John Mackay | 2019-03-03 |
| 3434 | Capital One | Mastercard | 20000.00 | 5420.75 | Birmingham | Stanley Mathews | 2019-05-02 |
| 3554 | MBNA | Visa | 5000.00 | 3450.75 | Aberdeen | Julia Kathy | 2019-04-04 |
| 3557 | Natwest | Visa | 12000.00 | 4002.10 | Aberdeen | Julia Kathy | 2018-04-20 |
| 4323 | Natwest | Mastercard | 24000.00 | 7325.50 | Glasgow | John Mackay | 2018-10-10 |
| 4489 | Natwest | Visa | 3000.00 | 1450.45 | Birmingham | Paul Carter | 2018-05-04 |
| 4578 | Barclaycard | Mastercard | 4500.00 | 4325.60 | Aberdeen | Julia Kathy | 2020-01-22 |

Rows returned: 10.

## Q14. Number of Mastercard cards (answer-key Part 2 Q10).

```sql
SELECT Creditcard_type, COUNT(*) AS card_count
FROM creditcard
WHERE Creditcard_type = 'Mastercard'
GROUP BY Creditcard_type;
```

| Creditcard_type | card_count |
| --- | --- |
| Mastercard | 8 |

Rows returned: 1.

## Q15. Number of cards in each city (answer-key Part 2 Q11).

```sql
SELECT City, COUNT(*) AS card_count
FROM creditcard
GROUP BY City
ORDER BY City;
```

| City | card_count |
| --- | --- |
| Aberdeen | 5 |
| Birmingham | 3 |
| Glasgow | 2 |
| London | 5 |

Rows returned: 4.

## Q16. Number of cards held by each cardholder (answer-key Part 2 Q12).

```sql
SELECT CardHolder, COUNT(*) AS card_count
FROM creditcard
GROUP BY CardHolder
ORDER BY CardHolder;
```

| CardHolder | card_count |
| --- | --- |
| John Mackay | 2 |
| John Smith | 1 |
| Julia Kathy | 3 |
| Krystal Jones | 1 |
| Mario Brothers | 2 |
| Paul Carter | 2 |
| Paul Jones | 3 |
| Stanley Mathews | 1 |

Rows returned: 8.

## Q17. Minimum and maximum credit limits by city (answer-key Part 2 Q13).

```sql
SELECT City, MIN(Credit_Limit) AS minimum_credit_limit,
       MAX(Credit_Limit) AS maximum_credit_limit
FROM creditcard
GROUP BY City
ORDER BY City;
```

| City | minimum_credit_limit | maximum_credit_limit |
| --- | --- | --- |
| Aberdeen | 1200.00 | 50000.00 |
| Birmingham | 3000.00 | 20000.00 |
| Glasgow | 4000.00 | 24000.00 |
| London | 1500.00 | 10000.00 |

Rows returned: 4.
