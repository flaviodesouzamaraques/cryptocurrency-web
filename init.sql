CREATE TABLE cryptocurrency_quotes (
        symbol VARCHAR(3) NOT NULL,
        price_currency VARCHAR(3) NOT NULL,
        price_amount FLOAT NOT NULL,
        timestamp TIMESTAMP NOT NULL,
        primary key (symbol, price_currency, timestamp)

);

CREATE TABLE users (
    id serial PRIMARY KEY,
    name VARCHAR ( 50 ) NOT NULL,
    password VARCHAR ( 50 ) NOT NULL,
    email VARCHAR ( 255 ) UNIQUE NOT NULL

);

ALTER TABLE public.users ALTER COLUMN "password" TYPE varchar(255) USING "password"::varchar;
