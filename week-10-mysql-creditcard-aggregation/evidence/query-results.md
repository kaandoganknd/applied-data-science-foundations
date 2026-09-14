# Executed aggregation and date queries

MySQL 9.7.1; unchanged 15-record reference table. Q24 as-of date: **2026-09-13**.

Currency: GBP as stated in the exercises. Complete result tables are retained below.

## Q18. Maximum, minimum, and total credit limit by city (Part 2 Q14).

```sql
SELECT City, MAX(Credit_Limit) AS maximum_credit_limit,
       MIN(Credit_Limit) AS minimum_credit_limit,
       SUM(Credit_Limit) AS total_credit_limit
FROM creditcard
GROUP BY City
ORDER BY City;
```

| City | maximum_credit_limit | minimum_credit_limit | total_credit_limit |
| --- | --- | --- | --- |
| Aberdeen | 50000.00 | 1200.00 | 72700.00 |
| Birmingham | 20000.00 | 3000.00 | 26000.00 |
| Glasgow | 24000.00 | 4000.00 | 28000.00 |
| London | 10000.00 | 1500.00 | 24000.00 |

## Q19. Minimum and maximum spending by cardholder (Part 2 Q15).

```sql
SELECT CardHolder, MIN(Totalspent) AS minimum_spent, MAX(Totalspent) AS maximum_spent
FROM creditcard
GROUP BY CardHolder
ORDER BY CardHolder;
```

| CardHolder | minimum_spent | maximum_spent |
| --- | --- | --- |
| John Mackay | 2300.50 | 7325.50 |
| John Smith | 3500.39 | 3500.39 |
| Julia Kathy | 3450.75 | 4325.60 |
| Krystal Jones | 3476.50 | 3476.50 |
| Mario Brothers | 867.30 | 2567.77 |
| Paul Carter | 1200.00 | 1450.45 |
| Paul Jones | 1234.40 | 2300.00 |
| Stanley Mathews | 5420.75 | 5420.75 |

## Q20. Total credit used by each cardholder (Part 2 Q16).

```sql
SELECT CardHolder, SUM(Totalspent) AS total_credit_used
FROM creditcard
GROUP BY CardHolder
ORDER BY CardHolder;
```

| CardHolder | total_credit_used |
| --- | --- |
| John Mackay | 9626.00 |
| John Smith | 3500.39 |
| Julia Kathy | 11778.45 |
| Krystal Jones | 3476.50 |
| Mario Brothers | 3435.07 |
| Paul Carter | 2650.45 |
| Paul Jones | 4777.60 |
| Stanley Mathews | 5420.75 |

## Q21. Remaining amount on each credit card (Part 2 Q17).

```sql
SELECT CreditcardNum, CardHolder, Credit_Limit, Totalspent,
       Credit_Limit - Totalspent AS remaining_credit
FROM creditcard
ORDER BY CreditcardNum;
```

| CreditcardNum | CardHolder | Credit_Limit | Totalspent | remaining_credit |
| --- | --- | --- | --- | --- |
| 1212 | Krystal Jones | 5000.00 | 3476.50 | 1523.50 |
| 2332 | Paul Carter | 3000.00 | 1200.00 | 1800.00 |
| 2456 | Mario Brothers | 50000.00 | 2567.77 | 47432.23 |
| 3333 | Paul Jones | 3500.00 | 1243.20 | 2256.80 |
| 3334 | Mario Brothers | 1200.00 | 867.30 | 332.70 |
| 3343 | John Mackay | 4000.00 | 2300.50 | 1699.50 |
| 3434 | Stanley Mathews | 20000.00 | 5420.75 | 14579.25 |
| 3554 | Julia Kathy | 5000.00 | 3450.75 | 1549.25 |
| 3556 | Paul Jones | 4000.00 | 2300.00 | 1700.00 |
| 3557 | Julia Kathy | 12000.00 | 4002.10 | 7997.90 |
| 4323 | John Mackay | 24000.00 | 7325.50 | 16674.50 |
| 4456 | John Smith | 10000.00 | 3500.39 | 6499.61 |
| 4489 | Paul Carter | 3000.00 | 1450.45 | 1549.55 |
| 4535 | Paul Jones | 1500.00 | 1234.40 | 265.60 |
| 4578 | Julia Kathy | 4500.00 | 4325.60 | 174.40 |

## Q22. Number of cards issued in each year (Part 2 Q18).

```sql
SELECT YEAR(Issue_Date) AS issue_year, COUNT(*) AS card_count
FROM creditcard
GROUP BY YEAR(Issue_Date)
ORDER BY issue_year;
```

| issue_year | card_count |
| --- | --- |
| 2018 | 5 |
| 2019 | 7 |
| 2020 | 3 |

## Q23. Number of cards issued in each calendar month, pooled across years (Part 2 Q19).

```sql
SELECT MONTH(Issue_Date) AS issue_month, MONTHNAME(Issue_Date) AS month_name,
       COUNT(*) AS card_count
FROM creditcard
GROUP BY MONTH(Issue_Date), MONTHNAME(Issue_Date)
ORDER BY issue_month;
```

| issue_month | month_name | card_count |
| --- | --- | --- |
| 1 | January | 3 |
| 3 | March | 1 |
| 4 | April | 3 |
| 5 | May | 3 |
| 7 | July | 1 |
| 10 | October | 2 |
| 11 | November | 1 |
| 12 | December | 1 |

## Q23B. Alternative chronological year-month grouping; years remain separate.

```sql
SELECT DATE_FORMAT(Issue_Date, '%Y-%m') AS issue_year_month, COUNT(*) AS card_count
FROM creditcard
GROUP BY DATE_FORMAT(Issue_Date, '%Y-%m')
ORDER BY issue_year_month;
```

| issue_year_month | card_count |
| --- | --- |
| 2018-04 | 1 |
| 2018-05 | 1 |
| 2018-10 | 2 |
| 2018-12 | 1 |
| 2019-01 | 1 |
| 2019-03 | 1 |
| 2019-04 | 2 |
| 2019-05 | 1 |
| 2019-07 | 1 |
| 2019-11 | 1 |
| 2020-01 | 2 |
| 2020-05 | 1 |

## Q24. Future-dated cards as of @as_of_date: a proxy for not yet issued (Part 2 Q20).

```sql
SELECT *
FROM creditcard
WHERE Issue_Date > @as_of_date
ORDER BY Issue_Date, CreditcardNum;
```

| CreditcardNum | Creditcard_company | Creditcard_type | Credit_Limit | Totalspent | City | CardHolder | Issue_Date |
| --- | --- | --- | --- | --- | --- | --- | --- |

No matching rows.

This identifies future-dated records only. There is no issue-status field, so it cannot independently establish actual issuance. Issue_Date is NOT NULL; all supplied dates are in 2018–2020.

## Q25. Total remaining credit across each cardholder's cards (Part 2 Q21).

```sql
SELECT CardHolder, SUM(Credit_Limit - Totalspent) AS total_remaining_credit
FROM creditcard
GROUP BY CardHolder
ORDER BY CardHolder;
```

| CardHolder | total_remaining_credit |
| --- | --- |
| John Mackay | 18374.00 |
| John Smith | 6499.61 |
| Julia Kathy | 9721.55 |
| Krystal Jones | 1523.50 |
| Mario Brothers | 47764.93 |
| Paul Carter | 3349.55 |
| Paul Jones | 4222.40 |
| Stanley Mathews | 14579.25 |

## Q26. Remaining credit grouped by the card's issue year (Part 2 Q22).

```sql
SELECT YEAR(Issue_Date) AS issue_year,
       SUM(Credit_Limit - Totalspent) AS total_remaining_credit
FROM creditcard
GROUP BY YEAR(Issue_Date)
ORDER BY issue_year;
```

| issue_year | total_remaining_credit |
| --- | --- |
| 2018 | 32987.16 |
| 2019 | 23184.20 |
| 2020 | 49863.43 |

## Reconciliation

| Measure | Value |
| --- | --- |
| Total credit limit | 150700.00 |
| Total spent | 44665.21 |
| Total remaining credit | 106034.79 |

Per-card, per-holder, and per-year remaining-credit totals reconcile. The year, month-of-year, and year-month counts each reconcile to 15 cards.
