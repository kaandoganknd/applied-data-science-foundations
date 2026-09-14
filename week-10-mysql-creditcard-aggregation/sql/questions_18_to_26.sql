USE financial_db;
-- Set @as_of_date before running to reproduce a historical review date.
SET @as_of_date = COALESCE(@as_of_date, CURRENT_DATE());

-- Q18: Maximum, minimum, and total credit limit by city (Part 2 Q14).
SELECT City, MAX(Credit_Limit) AS maximum_credit_limit,
       MIN(Credit_Limit) AS minimum_credit_limit,
       SUM(Credit_Limit) AS total_credit_limit
FROM creditcard
GROUP BY City
ORDER BY City;

-- Q19: Minimum and maximum spending by cardholder (Part 2 Q15).
SELECT CardHolder, MIN(Totalspent) AS minimum_spent, MAX(Totalspent) AS maximum_spent
FROM creditcard
GROUP BY CardHolder
ORDER BY CardHolder;

-- Q20: Total credit used by each cardholder (Part 2 Q16).
SELECT CardHolder, SUM(Totalspent) AS total_credit_used
FROM creditcard
GROUP BY CardHolder
ORDER BY CardHolder;

-- Q21: Remaining amount on each credit card (Part 2 Q17).
SELECT CreditcardNum, CardHolder, Credit_Limit, Totalspent,
       Credit_Limit - Totalspent AS remaining_credit
FROM creditcard
ORDER BY CreditcardNum;

-- Q22: Number of cards issued in each year (Part 2 Q18).
SELECT YEAR(Issue_Date) AS issue_year, COUNT(*) AS card_count
FROM creditcard
GROUP BY YEAR(Issue_Date)
ORDER BY issue_year;

-- Q23: Number of cards issued in each calendar month, pooled across years (Part 2 Q19).
SELECT MONTH(Issue_Date) AS issue_month, MONTHNAME(Issue_Date) AS month_name,
       COUNT(*) AS card_count
FROM creditcard
GROUP BY MONTH(Issue_Date), MONTHNAME(Issue_Date)
ORDER BY issue_month;

-- Q23B: Alternative chronological year-month grouping; years remain separate.
SELECT DATE_FORMAT(Issue_Date, '%Y-%m') AS issue_year_month, COUNT(*) AS card_count
FROM creditcard
GROUP BY DATE_FORMAT(Issue_Date, '%Y-%m')
ORDER BY issue_year_month;

-- Q24: Future-dated cards as of @as_of_date: a proxy for not yet issued (Part 2 Q20).
SELECT *
FROM creditcard
WHERE Issue_Date > @as_of_date
ORDER BY Issue_Date, CreditcardNum;

-- Q25: Total remaining credit across each cardholder's cards (Part 2 Q21).
SELECT CardHolder, SUM(Credit_Limit - Totalspent) AS total_remaining_credit
FROM creditcard
GROUP BY CardHolder
ORDER BY CardHolder;

-- Q26: Remaining credit grouped by the card's issue year (Part 2 Q22).
SELECT YEAR(Issue_Date) AS issue_year,
       SUM(Credit_Limit - Totalspent) AS total_remaining_credit
FROM creditcard
GROUP BY YEAR(Issue_Date)
ORDER BY issue_year;
