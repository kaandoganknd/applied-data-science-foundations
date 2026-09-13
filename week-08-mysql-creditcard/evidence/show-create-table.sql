CREATE TABLE `Creditcard` (
  `CreditcardNum` char(4) NOT NULL,
  `Creditcard_company` varchar(50) NOT NULL,
  `Creditcard_type` varchar(30) NOT NULL,
  `Credit_Limit` decimal(10,2) NOT NULL,
  `Totalspent` decimal(10,2) NOT NULL,
  `City` varchar(50) NOT NULL,
  `CardHolder` varchar(100) NOT NULL,
  `Issue_Date` date NOT NULL,
  PRIMARY KEY (`CreditcardNum`),
  CONSTRAINT `chk_credit_limit_positive` CHECK ((`Credit_Limit` > 0)),
  CONSTRAINT `chk_practice_card_identifier` CHECK (regexp_like(`CreditcardNum`,_utf8mb4'^[0-9]{4}$',_utf8mb4'c'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
