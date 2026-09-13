SELECT CreditcardNum, Creditcard_company, Creditcard_type, Credit_Limit,
       Totalspent, City, CardHolder, Issue_Date
FROM Creditcard
ORDER BY CreditcardNum;

SELECT COUNT(*) AS row_count,
       COUNT(DISTINCT CreditcardNum) AS distinct_identifiers,
       SUM(Credit_Limit <= 0) AS nonpositive_limits,
       SUM(Credit_Limit IS NULL) AS missing_limits,
       SUM(Credit_Limit) AS total_credit_limit,
       SUM(Totalspent) AS total_spent
FROM Creditcard;
