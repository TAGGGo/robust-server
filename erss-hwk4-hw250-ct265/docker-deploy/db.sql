DROP TABLE IF EXISTS consumer_order CASCADE;
DROP TABLE IF EXISTS position CASCADE;
DROP TYPE IF EXISTS order_status CASCADE;
DROP TABLE IF EXISTS symbol CASCADE;
DROP TABLE IF EXISTS account CASCADE;

CREATE TYPE order_status AS ENUM (
    'canceled',
    'open',
    'executed'
);

CREATE TABLE account (
    account_id SERIAL PRIMARY KEY,
    balance DECIMAL,
    ts timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE symbol (
    symbol_id SERIAL PRIMARY KEY,
    name varchar,
    ts timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE position (
    position_id SERIAL PRIMARY KEY,
    amount real NOT NULL,
    account_id int NOT NULL,
    symbol_id int NOT NULL,
    ts timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(account_id) REFERENCES account(account_id) ON DELETE CASCADE,
    FOREIGN KEY(symbol_id) REFERENCES symbol(symbol_id) ON DELETE CASCADE
);

CREATE TABLE consumer_order (
    order_id SERIAL PRIMARY KEY,
    account_id int NOT NULL,
    trans_id SERIAL NOT NULL,
    symbol_id int NOT NULL,
    amount real NOT NULL,
    limit_price real NOT NULL,
    status order_status NOT NULL,
    ts timestamp WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(account_id) REFERENCES account(account_id) ON DELETE CASCADE,
    FOREIGN KEY(symbol_id) REFERENCES symbol(symbol_id) ON DELETE CASCADE
);

ALTER TABLE position ADD CONSTRAINT unique_setting UNIQUE (account_id, symbol_id);
ALTER TABLE symbol ADD CONSTRAINT unique_symbolname UNIQUE (name);