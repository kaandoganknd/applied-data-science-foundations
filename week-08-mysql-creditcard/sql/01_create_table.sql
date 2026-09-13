-- MySQL 8.0.16 or later is required for enforced CHECK constraints.
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION,ONLY_FULL_GROUP_BY';

CREATE TABLE Creditcard (
    CreditcardNum        CHAR(4)         NOT NULL,
    Creditcard_company   VARCHAR(50)     NOT NULL,
    Creditcard_type      VARCHAR(30)     NOT NULL,
    Credit_Limit         DECIMAL(10, 2)  NOT NULL,
    Totalspent           DECIMAL(10, 2)  NOT NULL,
    City                 VARCHAR(50)     NOT NULL,
    CardHolder           VARCHAR(100)    NOT NULL,
    Issue_Date           DATE            NOT NULL
) ENGINE = InnoDB
  DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

-- Add the primary key and the required positive credit limit constraint.
ALTER TABLE Creditcard
    ADD PRIMARY KEY (CreditcardNum);

ALTER TABLE Creditcard
    ADD CONSTRAINT chk_credit_limit_positive CHECK (Credit_Limit > 0);

-- The supplied practice identifiers are exactly four numeric characters.
ALTER TABLE Creditcard
    ADD CONSTRAINT chk_practice_card_identifier
        CHECK (REGEXP_LIKE(CreditcardNum, '^[0-9]{4}$', 'c'));
