-- Use a dedicated schema. Existing tables are never dropped or overwritten.
CREATE DATABASE IF NOT EXISTS week08_creditcard
    CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE week08_creditcard;
