USE stocks;
CREATE TABLE stock_prices (
    symbol VARCHAR(255) NOT NULL,
    date TIMESTAMP NOT NULL,
    open FLOAT NOT NULL,
    close FLOAT NOT NULL,
    high FLOAT NOT NULL,
    low FLOAT NOT NULL,
    volume INT NOT NULL,
    PRIMARY KEY (symbol, date)
    );

CREATE TABLE stock_info (
    symbol VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (symbol)
    )