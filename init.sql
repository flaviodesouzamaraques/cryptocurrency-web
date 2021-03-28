CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "cryptocurrency_quotes" (
        symbol VARCHAR(3) NOT NULL,
        price_currency VARCHAR(3) NOT NULL,
        price_amount NUMERIC NOT NULL,
        timestamp DATETIME NOT NULL,
        primary key (symbol, price_currency, timestamp)

);

