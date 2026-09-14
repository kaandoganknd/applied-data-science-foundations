# Answer-key queries and complete results

Every SELECT statement is extracted unchanged from the supplied Word answer key, including all alternatives. Part 2 numbering restarts at one.

## Part 2 Q01, variant 1

```sql
SELECT COUNT(CreditcardNum) FROM creditcard;
```

| COUNT(CreditcardNum) |
| --- |
| 15 |

## Part 2 Q02, variant 1

```sql
SELECT COUNT(DISTINCT Creditcard_company) FROM creditcard;
```

| COUNT(DISTINCT Creditcard_company) |
| --- |
| 8 |

## Part 2 Q03, variant 1

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

## Part 2 Q04, variant 1

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

## Part 2 Q05, variant 1

```sql
SELECT CreditcardNum, Credit_Limit FROM creditcard ORDER BY Credit_Limit DESC LIMIT 1;
```

| CreditcardNum | Credit_Limit |
| --- | --- |
| 2456 | 50000.00 |

## Part 2 Q05, variant 2

```sql
SELECT CreditcardNum, Credit_Limit FROM creditcard WHERE Credit_Limit = (SELECT MAX(Credit_Limit) FROM creditcard);
```

| CreditcardNum | Credit_Limit |
| --- | --- |
| 2456 | 50000.00 |

## Part 2 Q06, variant 1

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

## Part 2 Q07, variant 1

```sql
SELECT CreditcardNum, City, Credit_Limit FROM creditcard WHERE City LIKE 'Aber%' AND Credit_Limit > 5000;
```

| CreditcardNum | City | Credit_Limit |
| --- | --- | --- |
| 2456 | Aberdeen | 50000.00 |
| 3557 | Aberdeen | 12000.00 |

## Part 2 Q08, variant 1

```sql
SELECT CreditcardNum, Credit_Limit FROM creditcard WHERE Credit_Limit IN (1200, 3000, 4500);
```

| CreditcardNum | Credit_Limit |
| --- | --- |
| 2332 | 3000.00 |
| 3334 | 1200.00 |
| 4489 | 3000.00 |
| 4578 | 4500.00 |

## Part 2 Q09, variant 1

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

## Part 2 Q10, variant 1

```sql
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard WHERE Creditcard_type = 'Mastercard';
```

| Creditcard_type | COUNT(Creditcard_type) |
| --- | --- |
| Mastercard | 8 |

## Part 2 Q10, variant 2

```sql
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard WHERE Creditcard_type = 'Mastercard' OR Creditcard_type = 'Visa' GROUP BY Creditcard_type;
```

| Creditcard_type | COUNT(Creditcard_type) |
| --- | --- |
| Visa | 6 |
| Mastercard | 8 |

## Part 2 Q10, variant 3

```sql
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard GROUP BY Creditcard_type HAVING Creditcard_type = 'Mastercard' OR Creditcard_type = 'Visa';
```

| Creditcard_type | COUNT(Creditcard_type) |
| --- | --- |
| Visa | 6 |
| Mastercard | 8 |

## Part 2 Q11, variant 1

```sql
SELECT City, COUNT(CreditcardNum) FROM creditcard GROUP BY City;
```

| City | COUNT(CreditcardNum) |
| --- | --- |
| London | 5 |
| Birmingham | 3 |
| Aberdeen | 5 |
| Glasgow | 2 |

## Part 2 Q12, variant 1

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

## Part 2 Q13, variant 1

```sql
SELECT City, MIN(Credit_Limit), MAX(Credit_Limit) FROM creditcard GROUP BY City;
```

| City | MIN(Credit_Limit) | MAX(Credit_Limit) |
| --- | --- | --- |
| London | 1500.00 | 10000.00 |
| Birmingham | 3000.00 | 20000.00 |
| Aberdeen | 1200.00 | 50000.00 |
| Glasgow | 4000.00 | 24000.00 |
