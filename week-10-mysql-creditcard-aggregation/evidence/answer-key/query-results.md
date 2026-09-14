# W9-W10 answer key: complete executed results

MySQL 9.7.1; all 26 Part 2 questions and 29 SELECT variants. Every result cell was checked against independent calculations on the 15 reference records.

AK numbering follows the W9-W10 solutions document. SQL statements are unchanged; row order is only guaranteed where the source specifies ORDER BY.

The source setup is in Week 8. Differences from the earlier question sheet are explained in [coverage notes](../../answer-key-coverage.md).

## AK01. Write a query that will display the number of records in the table.

```sql
SELECT COUNT(CreditcardNum) FROM creditcard;
```

| COUNT(CreditcardNum) |
| --- |
| 15 |

## AK02. Write a query that will display the number of different credit card companies in the table.

```sql
SELECT COUNT(DISTINCT Creditcard_company) FROM creditcard;
```

| COUNT(DISTINCT Creditcard_company) |
| --- |
| 8 |

## AK03. Write a query that will display a list of credit card companies from the table.

```sql
SELECT DISTINCT Creditcard_company FROM creditcard;
```

| Creditcard_company |
| --- |
| Capital One |
| Coutts Bank |
| American Express |
| Virgin Credit |
| MBNA |
| Egg |
| Natwest |
| Barclaycard |

## AK04. Write a query that will display a list of credit cards, ordered by the highest credit limit.

```sql
SELECT CreditcardNum, Credit_Limit FROM creditcard ORDER BY Credit_Limit DESC;
```

| CreditcardNum | Credit_Limit |
| --- | --- |
| 2456 | 50000.00 |
| 4323 | 24000.00 |
| 3434 | 20000.00 |
| 3557 | 12000.00 |
| 4456 | 10000.00 |
| 1212 | 5000.00 |
| 3554 | 5000.00 |
| 4578 | 4500.00 |
| 3343 | 4000.00 |
| 3556 | 4000.00 |
| 3333 | 3500.00 |
| 2332 | 3000.00 |
| 4489 | 3000.00 |
| 4535 | 1500.00 |
| 3334 | 1200.00 |

## AK05. Write a query that will display the credit card with the highest credit card limit.

### Variant 1

```sql
SELECT CreditcardNum, Credit_Limit FROM creditcard ORDER BY Credit_Limit DESC LIMIT 1;
```

| CreditcardNum | Credit_Limit |
| --- | --- |
| 2456 | 50000.00 |

### Variant 2

```sql
SELECT CreditcardNum, Credit_Limit FROM creditcard WHERE Credit_Limit = (SELECT MAX(Credit_Limit) FROM creditcard);
```

| CreditcardNum | Credit_Limit |
| --- | --- |
| 2456 | 50000.00 |

## AK06. Write a query to find all credit cards that was issued in London.

```sql
SELECT CreditcardNum, City FROM creditcard WHERE City = 'London';
```

| CreditcardNum | City |
| --- | --- |
| 1212 | London |
| 3333 | London |
| 3556 | London |
| 4456 | London |
| 4535 | London |

## AK07. List all credit cards that were issued in Aberdeen with credit limit more than £5000.

```sql
SELECT CreditcardNum, City, Credit_Limit FROM creditcard WHERE City LIKE 'Aber%' AND Credit_Limit > 5000;
```

| CreditcardNum | City | Credit_Limit |
| --- | --- | --- |
| 2456 | Aberdeen | 50000.00 |
| 3557 | Aberdeen | 12000.00 |

## AK08. List all credit cards that were issued with credit limits of £1200, £3000 and £4500.

```sql
SELECT CreditcardNum, Credit_Limit FROM creditcard WHERE Credit_Limit IN (1200, 3000, 4500);
```

| CreditcardNum | Credit_Limit |
| --- | --- |
| 2332 | 3000.00 |
| 3334 | 1200.00 |
| 4489 | 3000.00 |
| 4578 | 4500.00 |

## AK09. List all credit cards that were not issued in London?

```sql
SELECT CreditcardNum, City FROM creditcard WHERE City <> 'London';
```

| CreditcardNum | City |
| --- | --- |
| 2332 | Birmingham |
| 2456 | Aberdeen |
| 3334 | Aberdeen |
| 3343 | Glasgow |
| 3434 | Birmingham |
| 3554 | Aberdeen |
| 3557 | Aberdeen |
| 4323 | Glasgow |
| 4489 | Birmingham |
| 4578 | Aberdeen |

## AK10. Find the number of Mastercard that was issued?

### Variant 1

```sql
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard WHERE Creditcard_type = 'Mastercard';
```

| Creditcard_type | COUNT(Creditcard_type) |
| --- | --- |
| Mastercard | 8 |

### Variant 2

```sql
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard WHERE Creditcard_type = 'Mastercard' OR Creditcard_type = 'Visa' GROUP BY Creditcard_type;
```

| Creditcard_type | COUNT(Creditcard_type) |
| --- | --- |
| Visa | 6 |
| Mastercard | 8 |

### Variant 3

```sql
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard GROUP BY Creditcard_type HAVING Creditcard_type = 'Mastercard' OR Creditcard_type = 'Visa';
```

| Creditcard_type | COUNT(Creditcard_type) |
| --- | --- |
| Visa | 6 |
| Mastercard | 8 |

## AK11. Find the number of credit cards that were issued in each city?

```sql
SELECT City, COUNT(CreditcardNum) FROM creditcard GROUP BY City;
```

| City | COUNT(CreditcardNum) |
| --- | --- |
| London | 5 |
| Birmingham | 3 |
| Aberdeen | 5 |
| Glasgow | 2 |

## AK12. Display the number of credit cards that was issued for each cardholder?

```sql
SELECT CardHolder, COUNT(CreditcardNum) FROM creditcard GROUP BY CardHolder;
```

| CardHolder | COUNT(CreditcardNum) |
| --- | --- |
| Krystal Jones | 1 |
| Paul Carter | 2 |
| Mario Brothers | 2 |
| Paul Jones | 3 |
| John Mackay | 2 |
| Stanley Mathews | 1 |
| Julia Kathy | 3 |
| John Smith | 1 |

## AK13. What is the minimum and maximum credit limit for each city?

```sql
SELECT City, MIN(Credit_Limit), MAX(Credit_Limit) FROM creditcard GROUP BY City;
```

| City | MIN(Credit_Limit) | MAX(Credit_Limit) |
| --- | --- | --- |
| London | 1500.00 | 10000.00 |
| Birmingham | 3000.00 | 20000.00 |
| Aberdeen | 1200.00 | 50000.00 |
| Glasgow | 4000.00 | 24000.00 |

## AK14. What are the maximum credit limit, minimum credit limit and the sum of all spend for each city?

```sql
SELECT City, MIN(Credit_Limit), MAX(Credit_Limit), SUM(TotalSpent) FROM creditcard GROUP BY City;
```

| City | MIN(Credit_Limit) | MAX(Credit_Limit) | SUM(TotalSpent) |
| --- | --- | --- | --- |
| London | 1500.00 | 10000.00 | 11754.49 |
| Birmingham | 3000.00 | 20000.00 | 8071.20 |
| Aberdeen | 1200.00 | 50000.00 | 15213.52 |
| Glasgow | 4000.00 | 24000.00 | 9626.00 |

## AK15. What is the minimum and the maximum spending by each cardholder?

```sql
SELECT Cardholder, MIN(TotalSpent), MAX(TotalSpent) FROM creditcard GROUP BY Cardholder;
```

| Cardholder | MIN(TotalSpent) | MAX(TotalSpent) |
| --- | --- | --- |
| Krystal Jones | 3476.50 | 3476.50 |
| Paul Carter | 1200.00 | 1450.45 |
| Mario Brothers | 867.30 | 2567.77 |
| Paul Jones | 1234.40 | 2300.00 |
| John Mackay | 2300.50 | 7325.50 |
| Stanley Mathews | 5420.75 | 5420.75 |
| Julia Kathy | 3450.75 | 4325.60 |
| John Smith | 3500.39 | 3500.39 |

## AK16. Write a query that will display the total amount of credit used by each cardholder?

```sql
SELECT Cardholder, SUM(TotalSpent) FROM creditcard GROUP BY Cardholder;
```

| Cardholder | SUM(TotalSpent) |
| --- | --- |
| Krystal Jones | 3476.50 |
| Paul Carter | 2650.45 |
| Mario Brothers | 3435.07 |
| Paul Jones | 4777.60 |
| John Mackay | 9626.00 |
| Stanley Mathews | 5420.75 |
| Julia Kathy | 11778.45 |
| John Smith | 3500.39 |

## AK17. Write a query to display the remaining amount on each credit card?

```sql
SELECT CreditcardNum, (Credit_Limit - TotalSpent) AS RemainingAmount FROM creditcard;
```

| CreditcardNum | RemainingAmount |
| --- | --- |
| 1212 | 1523.50 |
| 2332 | 1800.00 |
| 2456 | 47432.23 |
| 3333 | 2256.80 |
| 3334 | 332.70 |
| 3343 | 1699.50 |
| 3434 | 14579.25 |
| 3554 | 1549.25 |
| 3556 | 1700.00 |
| 3557 | 7997.90 |
| 4323 | 16674.50 |
| 4456 | 6499.61 |
| 4489 | 1549.55 |
| 4535 | 265.60 |
| 4578 | 174.40 |

## AK18. Write a query to find the number of credit cards issued in each year from the table.

```sql
SELECT YEAR(Issue_Date), COUNT(CreditcardNum) FROM creditcard GROUP BY YEAR(Issue_Date);
```

| YEAR(Issue_Date) | COUNT(CreditcardNum) |
| --- | --- |
| 2019 | 7 |
| 2020 | 3 |
| 2018 | 5 |

## AK19. Write a query to find the number of credit card issued by each month.

```sql
SELECT MONTH(Issue_Date), COUNT(CreditcardNum) FROM creditcard GROUP BY MONTH(Issue_Date);
```

| MONTH(Issue_Date) | COUNT(CreditcardNum) |
| --- | --- |
| 11 | 1 |
| 7 | 1 |
| 1 | 3 |
| 5 | 3 |
| 3 | 1 |
| 4 | 3 |
| 10 | 2 |
| 12 | 1 |

## AK20. Write a query that will display all the credit cards that where issued after January 1st 2020.

```sql
SELECT CreditcardNum, Issue_Date FROM creditcard WHERE Issue_Date > '2020-01-01';
```

| CreditcardNum | Issue_Date |
| --- | --- |
| 2456 | 2020-01-20 |
| 3333 | 2020-05-02 |
| 4578 | 2020-01-22 |

## AK21. Write a query to display the total amount of credit left to each of the Cardholder from all their credit cards.

```sql
SELECT Cardholder, SUM(Credit_Limit - TotalSpent) FROM creditcard GROUP BY Cardholder;
```

| Cardholder | SUM(Credit_Limit - TotalSpent) |
| --- | --- |
| Krystal Jones | 1523.50 |
| Paul Carter | 3349.55 |
| Mario Brothers | 47764.93 |
| Paul Jones | 4222.40 |
| John Mackay | 18374.00 |
| Stanley Mathews | 14579.25 |
| Julia Kathy | 9721.55 |
| John Smith | 6499.61 |

## AK22. Write a query that will display the remaining credit on all cards by each year of issue.

```sql
SELECT YEAR(Issue_Date), SUM(Credit_Limit - TotalSpent) FROM creditcard GROUP BY YEAR(Issue_Date);
```

| YEAR(Issue_Date) | SUM(Credit_Limit - TotalSpent) |
| --- | --- |
| 2019 | 23184.20 |
| 2020 | 49863.43 |
| 2018 | 32987.16 |

## AK23. Write a query that will display the remaining credit on the cards by the month they were issued.

```sql
SELECT MONTH(Issue_Date), SUM(Credit_Limit - TotalSpent) FROM creditcard GROUP BY MONTH(Issue_Date);
```

| MONTH(Issue_Date) | SUM(Credit_Limit - TotalSpent) |
| --- | --- |
| 11 | 1523.50 |
| 7 | 1800.00 |
| 1 | 47939.33 |
| 5 | 18385.60 |
| 3 | 1699.50 |
| 4 | 11247.15 |
| 10 | 23174.11 |
| 12 | 265.60 |

## AK24. Assuming each card expires in 18 months, write a query to display the date when each card will expire?

```sql
SELECT CreditcardNum, Issue_Date, DATE_ADD(Issue_Date, INTERVAL 18 MONTH) AS Expiry_Date FROM creditcard;
```

| CreditcardNum | Issue_Date | Expiry_Date |
| --- | --- | --- |
| 1212 | 2019-11-12 | 2021-05-12 |
| 2332 | 2019-07-05 | 2021-01-05 |
| 2456 | 2020-01-20 | 2021-07-20 |
| 3333 | 2020-05-02 | 2021-11-02 |
| 3334 | 2019-01-17 | 2020-07-17 |
| 3343 | 2019-03-03 | 2020-09-03 |
| 3434 | 2019-05-02 | 2020-11-02 |
| 3554 | 2019-04-04 | 2020-10-04 |
| 3556 | 2019-04-20 | 2020-10-20 |
| 3557 | 2018-04-20 | 2019-10-20 |
| 4323 | 2018-10-10 | 2020-04-10 |
| 4456 | 2018-10-11 | 2020-04-11 |
| 4489 | 2018-05-04 | 2019-11-04 |
| 4535 | 2018-12-12 | 2020-06-12 |
| 4578 | 2020-01-22 | 2021-07-22 |

## AK25. Assuming a new card is sent to each of the cardholder a month before the card expire, write a query to display the date a new card should be posted to the cardholder?

```sql
SELECT CreditcardNum, Issue_Date, DATE_ADD(Issue_Date, INTERVAL 18 MONTH) AS Expiry_Date, DATE_ADD(Issue_Date, INTERVAL 17 MONTH) AS Replacement_Date FROM creditcard;
```

| CreditcardNum | Issue_Date | Expiry_Date | Replacement_Date |
| --- | --- | --- | --- |
| 1212 | 2019-11-12 | 2021-05-12 | 2021-04-12 |
| 2332 | 2019-07-05 | 2021-01-05 | 2020-12-05 |
| 2456 | 2020-01-20 | 2021-07-20 | 2021-06-20 |
| 3333 | 2020-05-02 | 2021-11-02 | 2021-10-02 |
| 3334 | 2019-01-17 | 2020-07-17 | 2020-06-17 |
| 3343 | 2019-03-03 | 2020-09-03 | 2020-08-03 |
| 3434 | 2019-05-02 | 2020-11-02 | 2020-10-02 |
| 3554 | 2019-04-04 | 2020-10-04 | 2020-09-04 |
| 3556 | 2019-04-20 | 2020-10-20 | 2020-09-20 |
| 3557 | 2018-04-20 | 2019-10-20 | 2019-09-20 |
| 4323 | 2018-10-10 | 2020-04-10 | 2020-03-10 |
| 4456 | 2018-10-11 | 2020-04-11 | 2020-03-11 |
| 4489 | 2018-05-04 | 2019-11-04 | 2019-10-04 |
| 4535 | 2018-12-12 | 2020-06-12 | 2020-05-12 |
| 4578 | 2020-01-22 | 2021-07-22 | 2021-06-22 |

## AK26. Write a query to display all cardholders who have a credit limit higher than the average credit limit in the table.

```sql
SET @AvgCredLimit = ROUND((SELECT AVG(Credit_Limit) FROM creditcard), 2);
```

```sql
SELECT Cardholder, Credit_Limit, @AvgCredLimit AS AvgCredit_Limit FROM creditcard WHERE Credit_Limit > @AvgCredLimit;
```

| Cardholder | Credit_Limit | AvgCredit_Limit |
| --- | --- | --- |
| Mario Brothers | 50000.00 | 10046.67 |
| Stanley Mathews | 20000.00 | 10046.67 |
| Julia Kathy | 12000.00 | 10046.67 |
| John Mackay | 24000.00 | 10046.67 |

## Date checks

| Issue date | 18-month expiry | 17-month replacement |
| --- | --- | --- |
| 2020-02-29 | 2021-08-29 | 2021-07-29 |
| 2020-08-31 | 2022-02-28 | 2022-01-31 |
| 2020-01-01 | 2021-07-01 | 2021-06-01 |

The strict 2020-01-01 cutoff excludes that date and includes 2020-01-02. Month-end dates can make issue date + 17 months differ from expiry date - 1 month; AK25 preserves the supplied formula.
