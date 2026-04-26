/*
   DDL - CREATE, ALTER, DROP, and Schema Management
   File: 08_ddl_create_alter.sql

   Data Definition Language (DDL) statements define and modify
   the structure of database objects: tables, indexes, views, schemas.
*/

-- ============================================================================
-- 1. CREATE TABLE
-- ============================================================================

-- Basic CREATE TABLE
-- CREATE TABLE employees (
--     employee_id   INT PRIMARY KEY,
--     first_name    VARCHAR(50) NOT NULL,
--     last_name     VARCHAR(50) NOT NULL,
--     email         VARCHAR(100) UNIQUE NOT NULL,
--     hire_date     DATE NOT NULL DEFAULT CURRENT_DATE,
--     salary        DECIMAL(10,2) CHECK (salary > 0),
--     department_id INT,
--     is_active     BOOLEAN DEFAULT TRUE
-- );

-- CREATE TABLE with foreign key
-- CREATE TABLE departments (
--     department_id   INT PRIMARY KEY,
--     department_name VARCHAR(100) NOT NULL,
--     manager_id      INT,
--     budget          DECIMAL(12,2),
--     FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
-- );

-- CREATE TABLE with composite primary key
-- CREATE TABLE project_assignments (
--     employee_id  INT,
--     project_id   INT,
--     start_date   DATE NOT NULL,
--     end_date     DATE,
--     role         VARCHAR(50),
--     PRIMARY KEY (employee_id, project_id),
--     FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
--     FOREIGN KEY (project_id) REFERENCES projects(project_id)
-- );

-- CREATE TABLE with IF NOT EXISTS (avoids error if table exists)
-- CREATE TABLE IF NOT EXISTS audit_log (
--     id          SERIAL PRIMARY KEY,
--     table_name  VARCHAR(100),
--     action      VARCHAR(20),
--     old_data    JSONB,
--     new_data    JSONB,
--     changed_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- CREATE TABLE ... AS (create from query results)
-- CREATE TABLE high_value_customers AS
-- SELECT * FROM customers WHERE total_spent > 10000;

-- ============================================================================
-- 2. TEMPORARY TABLES
-- ============================================================================

/*
   Temporary tables exist only for the duration of a session or transaction.
   Useful for intermediate results in complex processing.
*/

-- CREATE TEMP TABLE temp_order_summary AS
-- SELECT customer_id, COUNT(*) AS order_count, SUM(total) AS total_spent
-- FROM orders
-- GROUP BY customer_id;

-- ============================================================================
-- 3. ALTER TABLE
-- ============================================================================

-- Add a column
-- ALTER TABLE employees ADD COLUMN phone VARCHAR(20);

-- Add a column with default value
-- ALTER TABLE employees ADD COLUMN bonus DECIMAL(10,2) DEFAULT 0;

-- Drop a column
-- ALTER TABLE employees DROP COLUMN phone;

-- Modify column data type
-- PostgreSQL: ALTER TABLE employees ALTER COLUMN salary TYPE NUMERIC(12,2);
-- MySQL:      ALTER TABLE employees MODIFY COLUMN salary DECIMAL(12,2);
-- SQL Server: ALTER TABLE employees ALTER COLUMN salary DECIMAL(12,2);

-- Rename a column
-- PostgreSQL: ALTER TABLE employees RENAME COLUMN salary TO base_salary;
-- MySQL:      ALTER TABLE employees CHANGE COLUMN salary base_salary DECIMAL(10,2);
-- SQL Server: EXEC sp_rename 'employees.salary', 'base_salary', 'COLUMN';

-- Add a constraint
-- ALTER TABLE employees ADD CONSTRAINT uq_email UNIQUE (email);
-- ALTER TABLE employees ADD CONSTRAINT chk_salary CHECK (salary > 0);
-- ALTER TABLE employees ALTER COLUMN first_name SET NOT NULL;

-- Drop a constraint
-- ALTER TABLE employees DROP CONSTRAINT uq_email;
-- ALTER TABLE employees ALTER COLUMN first_name DROP NOT NULL;

-- Add a foreign key
-- ALTER TABLE employees
-- ADD CONSTRAINT fk_department
-- FOREIGN KEY (department_id) REFERENCES departments(department_id);

-- Set default value
-- ALTER TABLE employees ALTER COLUMN is_active SET DEFAULT TRUE;

-- ============================================================================
-- 4. DROP TABLE
-- ============================================================================

-- DROP TABLE employees;                    -- removes table (error if not exists)
-- DROP TABLE IF EXISTS employees;          -- safe drop
-- DROP TABLE employees CASCADE;            -- drops dependent objects too (PostgreSQL)

-- ============================================================================
-- 5. TRUNCATE TABLE
-- ============================================================================

/*
   TRUNCATE removes ALL rows from a table.
   Faster than DELETE without WHERE (no row-by-row logging).
   Cannot be rolled back in some databases (DDL, not DML).
   Resets auto-increment counters in most databases.
*/

-- TRUNCATE TABLE temp_data;
-- TRUNCATE TABLE orders RESTART IDENTITY;  -- PostgreSQL: reset sequence

-- ============================================================================
-- 6. CREATE / DROP INDEX
-- ============================================================================

-- Basic index
-- CREATE INDEX idx_employees_last_name ON employees(last_name);

-- Unique index
-- CREATE UNIQUE INDEX idx_employees_email ON employees(email);

-- Composite index
-- CREATE INDEX idx_employees_dept_salary ON employees(department_id, salary);

-- Partial index (PostgreSQL)
-- CREATE INDEX idx_active_employees ON employees(last_name)
-- WHERE is_active = TRUE;

-- Drop index
-- DROP INDEX idx_employees_last_name;
-- DROP INDEX IF EXISTS idx_employees_last_name;

-- ============================================================================
-- 7. CREATE / DROP VIEW
-- ============================================================================

/*
   A view is a saved SELECT query that acts like a virtual table.
   Can simplify complex queries and provide security (hide columns).
*/

-- Create a view
-- CREATE VIEW active_employees AS
-- SELECT employee_id, first_name, last_name, email, department_id
-- FROM employees
-- WHERE is_active = TRUE;

-- Create a view with aggregation
-- CREATE VIEW department_summary AS
-- SELECT
--     d.department_name,
--     COUNT(e.employee_id) AS employee_count,
--     AVG(e.salary) AS avg_salary,
--     SUM(e.salary) AS total_salary
-- FROM departments d
-- LEFT JOIN employees e ON d.department_id = e.department_id
-- GROUP BY d.department_name;

-- Query a view (same as table)
-- SELECT * FROM active_employees WHERE department_id = 1;

-- Drop a view
-- DROP VIEW IF EXISTS active_employees;

-- Materialized view (PostgreSQL, Oracle)
-- Stores the result physically, can be refreshed
-- CREATE MATERIALIZED VIEW monthly_sales AS
-- SELECT
--     DATE_TRUNC('month', order_date) AS month,
--     SUM(total_amount) AS total_sales
-- FROM orders
-- GROUP BY DATE_TRUNC('month', order_date);
--
-- REFRESH MATERIALIZED VIEW monthly_sales;

-- ============================================================================
-- 8. DATABASE AND SCHEMA OPERATIONS
-- ============================================================================

-- Create database
-- CREATE DATABASE my_app;
-- CREATE DATABASE my_app WITH ENCODING 'UTF8' LC_COLLATE 'en_US.UTF-8';

-- Create schema (logical grouping within a database)
-- CREATE SCHEMA sales;
-- CREATE TABLE sales.orders ( ... );  -- table in sales schema

-- Drop database
-- DROP DATABASE IF EXISTS my_app;

-- ============================================================================
-- 9. RENAME
-- ============================================================================

-- Rename table
-- ALTER TABLE old_name RENAME TO new_name;

-- Rename database (varies by DB)
-- PostgreSQL: ALTER DATABASE old_name RENAME TO new_name;
-- (Must have no active connections)

-- ============================================================================
-- 10. DDL BEST PRACTICES
-- ============================================================================

/*
   1. Always use IF EXISTS / IF NOT EXISTS in scripts
   2. Use transactions for DDL changes when possible (PostgreSQL supports this)
   3. Test schema changes on a staging environment first
   4. Version control your DDL scripts (migrations)
   5. Consider the impact of adding columns to large tables
   6. Adding a column with a DEFAULT value can lock large tables
   7. Use meaningful names for constraints and indexes
   8. Document schema decisions in comments
*/

-- Transactional DDL (PostgreSQL)
-- BEGIN;
-- ALTER TABLE employees ADD COLUMN middle_name VARCHAR(50);
-- ALTER TABLE employees ADD CONSTRAINT chk_middle_name
--     CHECK (middle_name IS NULL OR LENGTH(middle_name) > 0);
-- COMMIT;
-- -- Or ROLLBACK if something goes wrong

-- ============================================================================
-- END OF 08_ddl_create_alter.sql
-- ============================================================================
