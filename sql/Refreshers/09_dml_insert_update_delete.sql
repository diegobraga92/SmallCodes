/*
   DML - INSERT, UPDATE, DELETE, MERGE
   File: 09_dml_insert_update_delete.sql

   Data Manipulation Language (DML) statements modify the data
   stored in tables. These are the write operations.
*/

-- ============================================================================
-- 1. INSERT - Adding New Rows
-- ============================================================================

-- Insert a single row (specifying columns)
-- INSERT INTO employees (employee_id, first_name, last_name, email, hire_date, salary, department_id)
-- VALUES (101, 'John', 'Doe', 'john.doe@company.com', '2024-01-15', 75000, 1);

-- Insert with default values (omitting columns with defaults)
-- INSERT INTO employees (employee_id, first_name, last_name, email)
-- VALUES (102, 'Jane', 'Smith', 'jane.smith@company.com');
-- hire_date defaults to CURRENT_DATE, salary defaults to NULL

-- Insert multiple rows in one statement
-- INSERT INTO departments (department_id, department_name) VALUES
--     (1, 'Engineering'),
--     (2, 'Sales'),
--     (3, 'Marketing'),
--     (4, 'Human Resources');

-- Insert from SELECT (copy data between tables)
-- INSERT INTO employees_archive (employee_id, first_name, last_name, email, salary)
-- SELECT employee_id, first_name, last_name, email, salary
-- FROM employees
-- WHERE is_active = FALSE;

-- INSERT ... ON CONFLICT (PostgreSQL UPSERT)
-- INSERT INTO customers (customer_id, email, name)
-- VALUES (1, 'alice@example.com', 'Alice')
-- ON CONFLICT (customer_id) DO UPDATE SET
--     email = EXCLUDED.email,
--     name = EXCLUDED.name;

-- INSERT ... ON DUPLICATE KEY (MySQL UPSERT)
-- INSERT INTO customers (customer_id, email, name)
-- VALUES (1, 'alice@example.com', 'Alice')
-- ON DUPLICATE KEY UPDATE
--     email = VALUES(email),
--     name = VALUES(name);

-- INSERT ... RETURNING (PostgreSQL, SQLite)
-- INSERT INTO employees (first_name, last_name, email)
-- VALUES ('Bob', 'Brown', 'bob@company.com')
-- RETURNING employee_id, created_at;

-- ============================================================================
-- 2. UPDATE - Modifying Existing Rows
-- ============================================================================

-- Basic UPDATE
-- UPDATE employees
-- SET salary = 80000
-- WHERE employee_id = 101;

-- Update multiple columns
-- UPDATE employees
-- SET
--     salary = salary * 1.1,
--     last_review_date = CURRENT_DATE
-- WHERE department_id = 1;

-- Update with subquery
-- UPDATE products
-- SET price = price * 1.05
-- WHERE category_id = (
--     SELECT category_id FROM categories WHERE category_name = 'Electronics'
-- );

-- Update with JOIN (PostgreSQL, SQL Server)
-- UPDATE employees e
-- SET salary = salary * 1.15
-- FROM departments d
-- WHERE e.department_id = d.department_id
--   AND d.department_name = 'Engineering';

-- Update with JOIN (MySQL)
-- UPDATE employees e
-- INNER JOIN departments d ON e.department_id = d.department_id
-- SET e.salary = e.salary * 1.15
-- WHERE d.department_name = 'Engineering';

-- ============================================================================
-- 3. DELETE - Removing Rows
-- ============================================================================

-- Delete specific rows
-- DELETE FROM employees
-- WHERE is_active = FALSE;

-- Delete all rows (use with caution!)
-- DELETE FROM temp_data;
-- TRUNCATE is faster for this purpose

-- Delete with subquery
-- DELETE FROM orders
-- WHERE customer_id IN (
--     SELECT customer_id FROM customers WHERE status = 'inactive'
-- );

-- Delete using JOIN (PostgreSQL, SQL Server)
-- DELETE FROM employees e
-- USING departments d
-- WHERE e.department_id = d.department_id
--   AND d.department_name = 'Obsolete';

-- ============================================================================
-- 4. DELETE vs TRUNCATE vs DROP
-- ============================================================================

/*
   DELETE                          | TRUNCATE                      | DROP
   --------------------------------|-------------------------------|---------------------------
   DML (can be rolled back)        | DDL (may not be rollbackable) | DDL
   Removes rows one by one         | Removes all rows at once      | Removes entire table
   Slower on large tables          | Very fast                     | Very fast
   Can have WHERE clause           | No WHERE clause               | No WHERE clause
   Does NOT reset auto-increment   | Resets auto-increment         | Removes table structure
   Fires triggers                  | Does not fire triggers        | Does not fire triggers
   Locks each row                  | Locks table                   | Locks table
*/

-- ============================================================================
-- 5. MERGE (UPSERT)
-- ============================================================================

/*
   MERGE (also called UPSERT) inserts new rows or updates existing ones.
   Available in SQL Server, PostgreSQL (via ON CONFLICT), MySQL (via ON DUPLICATE KEY).
*/

-- SQL Server MERGE
-- MERGE INTO products AS target
-- USING updated_prices AS source ON target.product_id = source.product_id
-- WHEN MATCHED THEN
--     UPDATE SET target.price = source.price
-- WHEN NOT MATCHED THEN
--     INSERT (product_id, product_name, price)
--     VALUES (source.product_id, source.product_name, source.price);

-- ============================================================================
-- 6. DML BEST PRACTICES
-- ============================================================================

/*
   1. Always use WHERE in UPDATE/DELETE (test with SELECT first!)
   2. Use transactions for multi-row operations
   3. Consider batch size for large inserts (1000-5000 rows per batch)
   4. Use INSERT ... VALUES for small sets, INSERT ... SELECT for bulk
   5. Be aware of trigger overhead on write operations
   6. Use RETURNING clause to get auto-generated values (PostgreSQL)
   7. Consider locking implications of concurrent writes
   8. Always back up before mass UPDATE/DELETE operations
*/

-- Safe update pattern: SELECT first, then UPDATE
-- BEGIN;
-- SELECT * FROM employees WHERE department_id = 10;  -- verify
-- UPDATE employees SET salary = salary * 1.1 WHERE department_id = 10;
-- COMMIT;

-- ============================================================================
-- END OF 09_dml_insert_update_delete.sql
-- ============================================================================
