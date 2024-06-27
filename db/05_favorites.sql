CREATE TABLE IF NOT EXISTS favorites (
    country_code CHAR(2) PRIMARY KEY REFERENCES countries (code)
);