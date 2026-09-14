USE financial_db;

-- Q14: Number of Mastercard cards (answer-key Part 2 Q10).
SELECT Creditcard_type, COUNT(*) AS card_count
FROM creditcard
WHERE Creditcard_type = 'Mastercard'
GROUP BY Creditcard_type;

-- Q15: Number of cards in each city (answer-key Part 2 Q11).
SELECT City, COUNT(*) AS card_count
FROM creditcard
GROUP BY City
ORDER BY City;

-- Q16: Number of cards held by each cardholder (answer-key Part 2 Q12).
SELECT CardHolder, COUNT(*) AS card_count
FROM creditcard
GROUP BY CardHolder
ORDER BY CardHolder;

-- Q17: Minimum and maximum credit limits by city (answer-key Part 2 Q13).
SELECT City, MIN(Credit_Limit) AS minimum_credit_limit,
       MAX(Credit_Limit) AS maximum_credit_limit
FROM creditcard
GROUP BY City
ORDER BY City;
