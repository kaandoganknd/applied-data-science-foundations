CREATE TABLE IF NOT EXISTS creditcard (
	CreditcardNum SMALLINT PRIMARY KEY,
    Creditcard_company VARCHAR(100) NOT NULL,
    Creditcard_type VARCHAR(50)  NOT NULL,
    Credit_Limit DECIMAL(9,2),
    Totalspent DECIMAL(9,2),
    City VARCHAR(50) NOT NULL,
    CardHolder VARCHAR(100) NOT NULL,
    Issue_Date DATE NOT NULL,
    CONSTRAINT cc_ch_creditlimit CHECK (Credit_Limit > 0)
);
