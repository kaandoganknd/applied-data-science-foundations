USE financial_db;

-- Part 2 Q01, variant 1
SELECT COUNT(CreditcardNum) FROM creditcard;

-- Part 2 Q02, variant 1
SELECT COUNT(DISTINCT Creditcard_company) FROM creditcard;

-- Part 2 Q03, variant 1
SELECT DISTINCT Creditcard_company FROM creditcard;

-- Part 2 Q04, variant 1
SELECT CreditcardNum, Credit_Limit FROM creditcard ORDER BY Credit_Limit DESC;

-- Part 2 Q05, variant 1
SELECT CreditcardNum, Credit_Limit FROM creditcard ORDER BY Credit_Limit DESC LIMIT 1;

-- Part 2 Q05, variant 2
SELECT CreditcardNum, Credit_Limit FROM creditcard WHERE Credit_Limit = (SELECT MAX(Credit_Limit) FROM creditcard);

-- Part 2 Q06, variant 1
SELECT CreditcardNum, City FROM creditcard WHERE City = 'London';

-- Part 2 Q07, variant 1
SELECT CreditcardNum, City, Credit_Limit FROM creditcard WHERE City LIKE 'Aber%' AND Credit_Limit > 5000;

-- Part 2 Q08, variant 1
SELECT CreditcardNum, Credit_Limit FROM creditcard WHERE Credit_Limit IN (1200, 3000, 4500);

-- Part 2 Q09, variant 1
SELECT CreditcardNum, City FROM creditcard WHERE City <> 'London';

-- Part 2 Q10, variant 1
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard WHERE Creditcard_type = 'Mastercard';

-- Part 2 Q10, variant 2
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard WHERE Creditcard_type = 'Mastercard' OR Creditcard_type = 'Visa' GROUP BY Creditcard_type;

-- Part 2 Q10, variant 3
SELECT Creditcard_type, COUNT(Creditcard_type) FROM creditcard GROUP BY Creditcard_type HAVING Creditcard_type = 'Mastercard' OR Creditcard_type = 'Visa';

-- Part 2 Q11, variant 1
SELECT City, COUNT(CreditcardNum) FROM creditcard GROUP BY City;

-- Part 2 Q12, variant 1
SELECT CardHolder, COUNT(CreditcardNum) FROM creditcard GROUP BY CardHolder;

-- Part 2 Q13, variant 1
SELECT City, MIN(Credit_Limit), MAX(Credit_Limit) FROM creditcard GROUP BY City;
