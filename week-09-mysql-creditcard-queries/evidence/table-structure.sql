CREATE TABLE `creditcard` (
  `CreditcardNum` smallint NOT NULL,
  `Creditcard_company` varchar(100) NOT NULL,
  `Creditcard_type` varchar(50) NOT NULL,
  `Credit_Limit` decimal(9,2) DEFAULT NULL,
  `Totalspent` decimal(9,2) DEFAULT NULL,
  `City` varchar(50) NOT NULL,
  `CardHolder` varchar(100) NOT NULL,
  `Issue_Date` date NOT NULL,
  PRIMARY KEY (`CreditcardNum`),
  CONSTRAINT `cc_ch_creditlimit` CHECK ((`Credit_Limit` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
