USE financial_db;

-- Q05: Number of records.
SELECT COUNT(*) AS record_count
FROM creditcard;

-- Q06: Number of distinct credit card companies, not card types or records.
SELECT COUNT(DISTINCT Creditcard_company) AS company_count
FROM creditcard;

-- Q07: List of distinct credit card companies.
SELECT DISTINCT Creditcard_company
FROM creditcard
ORDER BY Creditcard_company;

-- Q08: All cards ordered from highest to lowest credit limit.
SELECT *
FROM creditcard
ORDER BY Credit_Limit DESC, CreditcardNum;

-- Q09: Card(s) with the highest limit; retain every tie.
SELECT *
FROM creditcard
WHERE Credit_Limit = (SELECT MAX(Credit_Limit) FROM creditcard)
ORDER BY CreditcardNum;

-- Q10: Cards issued in London.
SELECT *
FROM creditcard
WHERE City = 'London'
ORDER BY CreditcardNum;

-- Q11: Cards issued in Aberdeen with a limit strictly greater than GBP 5,000.
SELECT *
FROM creditcard
WHERE City = 'Aberdeen' AND Credit_Limit > 5000
ORDER BY CreditcardNum;

-- Q12: Cards with any of the three specified credit limits.
SELECT *
FROM creditcard
WHERE Credit_Limit IN (1200, 3000, 4500)
ORDER BY CreditcardNum;

-- Q13: Cards not issued in London. City is NOT NULL in the source schema.
SELECT *
FROM creditcard
WHERE City <> 'London'
ORDER BY CreditcardNum;
