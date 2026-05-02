-- CONTACTS
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INT
);

-- GROUPS
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- PHONES (1-to-many)
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INT REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20),
    type VARCHAR(10) CHECK (type IN ('home','work','mobile'))
);
