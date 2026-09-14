-- All Part 2 statements from MySQL Activities W9-W10 - Solutions.docx.
-- Original statement text and alternatives retained; comments identify questions.
USE financial_db;

-- AK01: Number of records.
SELECT COUNT(CreditcardNum) FROM creditcard;

-- AK02: Number of different credit card companies.
SELECT COUNT(DISTINCT Creditcard_company) FROM creditcard;

-- AK03: List of credit card companies.
SELECT DISTINCT Creditcard_company FROM creditcard;

-- AK04: Credit cards ordered by highest limit.
SELECT CreditcardNum, Credit_Limit FROM creditcard ORDER BY Credit_Limit DESC;

-- AK05: Highest credit limit; both source alternatives.
SELECT CreditcardNum, Credit_Limit FROM creditcard ORDER BY Credit_Limit DESC LIMIT 1;
SELECT CreditcardNum, Credit_Limit FROM creditcard WHERE Credit_Limit = (SELECT MAX(Credit_Limit) FROM creditcard);

-- AK06: Cards issued in London.
SELECT CreditcardNum, City FROM creditcard WHERE City = 'London';

-- AK07: Aberdeen cards above GBP 5,000; source prefix predicate retained.
SELECT CreditcardNum, City, Credit_Limit FROM creditcard WHERE City LIKE 'Aber%' AND Credit_Limit > 5000;

-- AK08: Specified credit limits.
SELECT CreditcardNum, Credit_Limit FROM creditcard WHERE Credit_Limit IN (1200, 3000, 4500);

-- AK09: Cards not issued in London.
SELECT CreditcardNum, City FROM creditcard WHERE City <> 'London';

-- AK10: Mastercard count, plus both Mastercard/Visa alternatives.
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard WHERE Creditcard_type = 'Mastercard';
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard WHERE Creditcard_type = 'Mastercard' OR Creditcard_type = 'Visa' GROUP BY Creditcard_type;
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard GROUP BY Creditcard_type HAVING Creditcard_type = 'Mastercard' OR Creditcard_type = 'Visa';

-- AK11: Number of cards by city.
SELECT City, COUNT(CreditcardNum) FROM creditcard GROUP BY City;

-- AK12: Number of cards by cardholder.
SELECT CardHolder, COUNT(CreditcardNum) FROM creditcard GROUP BY CardHolder;

-- AK13: Minimum and maximum credit limits by city.
SELECT City, MIN(Credit_Limit), MAX(Credit_Limit) FROM creditcard GROUP BY City;

-- AK14: Minimum/maximum limits and total SPENDING by city.
SELECT City, MIN(Credit_Limit), MAX(Credit_Limit), SUM(TotalSpent) FROM creditcard GROUP BY City;

-- AK15: Minimum and maximum spending by cardholder.
SELECT Cardholder, MIN(TotalSpent), MAX(TotalSpent) FROM creditcard GROUP BY Cardholder;

-- AK16: Total credit used by cardholder.
SELECT Cardholder, SUM(TotalSpent) FROM creditcard GROUP BY Cardholder;

-- AK17: Remaining amount on each card.
SELECT CreditcardNum, (Credit_Limit - TotalSpent) AS RemainingAmount FROM creditcard;

-- AK18: Number of cards by issue year.
SELECT YEAR(Issue_Date), COUNT(CreditcardNum) FROM creditcard GROUP BY YEAR(Issue_Date);

-- AK19: Number of cards by calendar month, pooled across years.
SELECT MONTH(Issue_Date), COUNT(CreditcardNum) FROM creditcard GROUP BY MONTH(Issue_Date);

-- AK20: Cards issued strictly after January 1, 2020.
SELECT CreditcardNum, Issue_Date FROM creditcard WHERE Issue_Date > '2020-01-01';

-- AK21: Total remaining credit by cardholder.
SELECT Cardholder, SUM(Credit_Limit - TotalSpent) FROM creditcard GROUP BY Cardholder;

-- AK22: Remaining credit by issue year.
SELECT YEAR(Issue_Date), SUM(Credit_Limit - TotalSpent) FROM creditcard GROUP BY YEAR(Issue_Date);

-- AK23: Remaining credit by calendar month, pooled across years.
SELECT MONTH(Issue_Date), SUM(Credit_Limit - TotalSpent) FROM creditcard GROUP BY MONTH(Issue_Date);

-- AK24: Expiry date, assuming an 18-month term.
SELECT CreditcardNum, Issue_Date, DATE_ADD(Issue_Date, INTERVAL 18 MONTH) AS Expiry_Date FROM creditcard;

-- AK25: Replacement posting date, following the source's 17-month formula.
SELECT CreditcardNum, Issue_Date, DATE_ADD(Issue_Date, INTERVAL 18 MONTH) AS Expiry_Date, DATE_ADD(Issue_Date, INTERVAL 17 MONTH) AS Replacement_Date FROM creditcard;

-- AK26: Card limits above the rounded average; original session variable retained.
SET @AvgCredLimit = ROUND((SELECT AVG(Credit_Limit) FROM creditcard), 2);
SELECT Cardholder, Credit_Limit, @AvgCredLimit AS AvgCredit_Limit FROM creditcard WHERE Credit_Limit > @AvgCredLimit;
