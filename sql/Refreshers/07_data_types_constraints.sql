/*
   DATA TYPES & CONSTRAINTS - Column Types and Table Constraints
   File: 07_data_types_constraints.sql

   Choosing the right data types and constraints is fundamental
   to good database design. This file covers the most common types
   and all constraint types.
*/

-- ============================================================================
-- 1. NUMERIC DATA TYPES
-- ============================================================================

/*
   Type            | Storage | Range/Precision              | Use Case
   ----------------|---------|------------------------------|---------------------------
   INTEGER/INT     | 4 bytes | -2B to +2B                   | IDs, counters, ages
   SMALLINT        | 2 bytes | -32K to +32K                 | Small ranges
   BIGINT          | 8 bytes | -9 quintillion to +9 quint   | Large IDs, big counters
   TINYINT         | 1 byte  | 0-255 or -128-127            | Flags, small values
   DECIMAL(p,s)    | varies  | Exact precision              | Money, calculations
   NUMERIC(p,s)    | varies  | Exact precision              | Same as DECIMAL
   FLOAT/REAL      | 4/8     | Approximate, floating point  | Scientific, percentages
   SERIAL          | 4 bytes | Auto-incrementing integer    | Auto IDs (PostgreSQL)
*/

-- DECIMAL example: DECIMAL(10, 2) = 10 digits total, 2 after decimal
-- Range: -99999999.99 to 99999999.99

-- When to use DECIMAL vs FLOAT:
-- DECIMAL: exact, for money and precise calculations
-- FLOAT:   approximate, for measurements and scientific data

-- ============================================================================
-- 2. STRING DATA TYPES
-- ============================================================================

/*
   Type            | Description                          | Use Case
   ----------------|--------------------------------------|---------------------------
   CHAR(n)         | Fixed-length, padded with spaces     | Fixed codes (ISO, country)
   VARCHAR(n)      | Variable-length, up to n chars       | Names, emails, descriptions
   TEXT            | Unlimited length (in most DBs)       | Long text, articles, notes
   NCHAR/NVARCHAR  | Unicode strings (SQL Server)         | International text
   CLOB            | Character large object               | Very large text (Oracle)
*/

-- CHAR vs VARCHAR:
-- CHAR(10) always stores 10 characters (padded with spaces)
-- VARCHAR(10) stores only the actual characters (up to 10)
-- VARCHAR is almost always preferred unless the length is truly fixed

-- VARCHAR(255) is a common default, but choose based on actual needs:
-- VARCHAR(50)  for emails
-- VARCHAR(100) for names
-- VARCHAR(500) for short descriptions

-- ============================================================================
-- 3. DATE/TIME DATA TYPES
-- ============================================================================

/*
   Type            | Description                          | Example
   ----------------|--------------------------------------|---------------------------
   DATE            | Date only (no time)                  | '2024-01-15'
   TIME            | Time only (no date)                  | '14:30:00'
   TIMESTAMP       | Date + time                          | '2024-01-15 14:30:00'
   TIMESTAMPTZ     | Date + time + timezone (PostgreSQL)  | '2024-01-15 14:30:00+00'
   DATETIME        | Date + time (MySQL)                  | '2024-01-15 14:30:00'
   INTERVAL        | Time duration (PostgreSQL)           | '1 day' or '3 months'
*/

-- Best practice: Always store timestamps in UTC
-- Convert to local time in the application layer

-- ============================================================================
-- 4. BOOLEAN AND OTHER TYPES
-- ============================================================================

/*
   Type            | Description                          | Notes
   ----------------|--------------------------------------|---------------------------
   BOOLEAN/BOOL    | TRUE, FALSE, NULL                    | PostgreSQL native
                     |                                      | MySQL uses TINYINT(1)
                     |                                      | SQL Server uses BIT
   ENUM            | Predefined list of values            | MySQL, PostgreSQL
   JSON            | JSON data                            | Native in PostgreSQL, MySQL
   JSONB           | Binary JSON (indexable)              | PostgreSQL
   UUID            | Universally Unique Identifier        | PostgreSQL, SQL Server
   BYTEA/BLOB      | Binary data                          | Images, files, encrypted data
   ARRAY           | Array of values                      | PostgreSQL only
   XML             | XML data                             | SQL Server, PostgreSQL
   HSTORE          | Key-value store                      | PostgreSQL extension
*/

-- ============================================================================
-- 5. CONSTRAINTS OVERVIEW
-- ============================================================================

/*
   Constraint      | Description                          | Effect
   ----------------|--------------------------------------|---------------------------
   PRIMARY KEY     | Uniquely identifies each row         | UNIQUE + NOT NULL, indexed
   FOREIGN KEY     | References a PK in another table     | Enforces referential integrity
   UNIQUE          | Ensures all values are distinct      | Creates unique index
   NOT NULL        | Column cannot contain NULL           | Required field
   CHECK           | Validates values against condition   | Custom validation rule
   DEFAULT         | Provides default value               | Used when no value specified
*/

-- ============================================================================
-- 6. PRIMARY KEY
-- ============================================================================

/*
   Every table should have a primary key.
   Can be a single column or composite (multiple columns).
   Automatically creates a unique index.
*/

-- Single column PK
-- CREATE TABLE customers (
--     customer_id INT PRIMARY KEY,
--     name VARCHAR(100) NOT NULL
-- );

-- Composite PK
-- CREATE TABLE order_items (
--     order_id INT,
--     product_id INT,
--     quantity INT NOT NULL,
--     PRIMARY KEY (order_id, product_id)
-- );

-- Auto-incrementing PK (varies by DB)
-- PostgreSQL:  id SERIAL PRIMARY KEY
-- MySQL:       id INT AUTO_INCREMENT PRIMARY KEY
-- SQL Server:  id INT IDENTITY(1,1) PRIMARY KEY
-- SQLite:      id INTEGER PRIMARY KEY AUTOINCREMENT

-- ============================================================================
-- 7. FOREIGN KEY
-- ============================================================================

/*
   Foreign keys enforce referential integrity.
   A value in the FK column must exist in the referenced PK column.
   Can specify actions on DELETE and UPDATE.
*/

-- CREATE TABLE orders (
--     order_id INT PRIMARY KEY,
--     customer_id INT,
--     order_date DATE NOT NULL,
--     FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
-- );

-- With referential actions:
-- CREATE TABLE orders (
--     order_id INT PRIMARY KEY,
--     customer_id INT,
--     FOREIGN KEY (customer_id)
--         REFERENCES customers(customer_id)
--         ON DELETE CASCADE    -- delete orders when customer is deleted
--         ON UPDATE CASCADE    -- update customer_id in orders if it changes
-- );

-- Other actions: ON DELETE SET NULL, ON DELETE RESTRICT, ON DELETE NO ACTION

-- ============================================================================
-- 8. UNIQUE, NOT NULL, CHECK, DEFAULT
-- ============================================================================

-- CREATE TABLE products (
--     product_id   INT PRIMARY KEY,
--     product_code VARCHAR(20) UNIQUE,              -- no duplicates allowed
--     product_name VARCHAR(100) NOT NULL,            -- required field
--     price        DECIMAL(10,2) CHECK (price > 0), -- must be positive
--     stock_count  INT DEFAULT 0,                    -- defaults to 0
--     category     VARCHAR(50) DEFAULT 'General',
--     created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Named constraints (better for error messages)
-- CREATE TABLE employees (
--     employee_id INT PRIMARY KEY,
--     salary DECIMAL(10,2),
--     CONSTRAINT chk_positive_salary CHECK (salary > 0),
--     CONSTRAINT uq_employee_email UNIQUE (email)
-- );

-- ============================================================================
-- 9. CONSTRAINT BEST PRACTICES
-- ============================================================================

/*
   1. Always define a PRIMARY KEY for every table
   2. Use FOREIGN KEYs to maintain data integrity
   3. Add CHECK constraints for business rules at the DB level
   4. Use NOT NULL for required fields
   5. Use DEFAULT values to simplify INSERT statements
   6. Name your constraints explicitly for better error messages
   7. Don't over-constrain: consider performance impact of FKs on writes
   8. Consider deferrable constraints for complex transactions (PostgreSQL)
*/

-- ============================================================================
-- END OF 07_data_types_constraints.sql
-- ============================================================================
