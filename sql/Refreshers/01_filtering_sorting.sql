/*
   FILTERING & SORTING - WHERE Operators, ORDER BY, LIMIT
   File: 01_filtering_sorting.sql

   Building on basic SELECT, this file covers all the ways to
   filter and order data. These are the most frequently used
   SQL features in day-to-day work.
*/

-- ============================================================================
-- 1. COMPARISON OPERATORS
-- ============================================================================

/*
   Operator  | Meaning                  | Example
   ----------|--------------------------|---------------------------
   =         | Equal to                 | price = 100
   <> or !=  | Not equal to             | status <> 'inactive'
   >         | Greater than             | quantity > 0
   <         | Less than                | age < 18
   >=        | Greater than or equal    | score >= 90
   <=        | Less than or equal       | price <= 50
*/

-- SELECT * FROM products WHERE price = 19.99;
-- SELECT * FROM products WHERE price > 100;
-- SELECT * FROM products WHERE quantity < 0;  -- find negative inventory

-- ============================================================================
-- 2. LOGICAL OPERATORS: AND, OR, NOT
-- ============================================================================

/*
   AND: Both conditions must be true
   OR:  At least one condition must be true
   NOT: Reverses a condition

   Operator precedence: NOT > AND > OR
   Use parentheses to make precedence explicit!
*/

-- AND: Find products that are both expensive AND in stock
-- SELECT * FROM products
-- WHERE price > 100 AND stock_count > 0;

-- OR: Find products in either category
-- SELECT * FROM products
-- WHERE category = 'Electronics' OR category = 'Books';

-- Combining AND and OR (parentheses matter!)
-- SELECT * FROM orders
-- WHERE (status = 'pending' OR status = 'processing')
--   AND created_at >= '2024-01-01';

-- NOT: Find non-cancelled orders
-- SELECT * FROM orders
-- WHERE NOT status = 'cancelled';
-- Equivalent to: WHERE status <> 'cancelled'

-- ============================================================================
-- 3. IN OPERATOR
-- ============================================================================

/*
   IN checks if a value matches ANY value in a list.
   More readable than multiple OR conditions.
   Can also use subqueries (covered later).
*/

-- SELECT * FROM employees
-- WHERE department IN ('Engineering', 'Sales', 'Marketing');

-- Equivalent to:
-- SELECT * FROM employees
-- WHERE department = 'Engineering'
--    OR department = 'Sales'
--    OR department = 'Marketing';

-- NOT IN: Exclude a list of values
-- SELECT * FROM products
-- WHERE category NOT IN ('Discontinued', 'Obsolete');

-- ============================================================================
-- 4. BETWEEN OPERATOR
-- ============================================================================

/*
   BETWEEN is inclusive of both endpoints.
   Works with numbers, dates, and strings.
*/

-- Numeric range
-- SELECT * FROM products WHERE price BETWEEN 10 AND 50;
-- Equivalent to: price >= 10 AND price <= 50

-- Date range
-- SELECT * FROM orders
-- WHERE order_date BETWEEN '2024-01-01' AND '2024-12-31';

-- NOT BETWEEN
-- SELECT * FROM employees
-- WHERE salary NOT BETWEEN 30000 AND 100000;

-- ============================================================================
-- 5. LIKE OPERATOR - Pattern Matching
-- ============================================================================

/*
   % matches any sequence of characters (including zero)
   _ matches exactly one character

   Pattern    | Matches
   -----------|--------------------------------
   'A%'       | Starts with 'A'
   '%son%'    | Contains 'son' anywhere
   '%son'     | Ends with 'son'
   '_at'      | Exactly 3 chars, ends with 'at'
   'A_%_%'    | Starts with 'A', at least 3 chars
*/

-- SELECT * FROM customers WHERE last_name LIKE 'Smith%';
-- SELECT * FROM products WHERE product_name LIKE '%organic%';
-- SELECT * FROM employees WHERE email LIKE '%@company.com';

-- Case sensitivity of LIKE varies by database:
-- PostgreSQL: LIKE is case-sensitive, ILIKE is case-insensitive
-- MySQL/SQLite: LIKE is case-insensitive by default
-- SQL Server: LIKE is case-insensitive by default

-- ============================================================================
-- 6. IS NULL / IS NOT NULL
-- ============================================================================

/*
   NULL represents missing or unknown data.
   You CANNOT use = NULL or <> NULL to check for NULL.
   Always use IS NULL or IS NOT NULL.
*/

-- SELECT * FROM customers WHERE phone IS NULL;       -- no phone number
-- SELECT * FROM employees WHERE manager_id IS NULL;  -- top-level managers
-- SELECT * FROM orders WHERE shipped_date IS NOT NULL;  -- already shipped

-- ============================================================================
-- 7. ORDER BY - Sorting Results
-- ============================================================================

/*
   ORDER BY sorts the result set.
   ASC  = ascending (default, smallest first)
   DESC = descending (largest first)

   Can sort by:
   - Column name
   - Column alias
   - Column position (1-based, not recommended)
   - Expression
*/

-- Single column sort
-- SELECT first_name, last_name, salary
-- FROM employees
-- ORDER BY salary DESC;  -- highest paid first

-- Multiple columns sort
-- SELECT department, last_name, first_name
-- FROM employees
-- ORDER BY department ASC, last_name ASC;

-- Sort by column position (fragile, avoid in production)
-- SELECT first_name, last_name, hire_date
-- FROM employees
-- ORDER BY 3 DESC;  -- sorts by hire_date (3rd column)

-- Sort with NULLs handling
-- PostgreSQL: ORDER BY column NULLS LAST
-- MySQL: NULLs sort before non-NULLs in ASC order
-- SQL Server: NULLs sort before non-NULLs in ASC order
-- SELECT * FROM employees ORDER BY manager_id ASC NULLS LAST;

-- ============================================================================
-- 8. LIMIT / OFFSET - Pagination
-- ============================================================================

/*
   LIMIT restricts the number of rows returned.
   OFFSET skips a number of rows before returning results.
   Together they implement pagination.

   Syntax varies by database:
   PostgreSQL/MySQL/SQLite: LIMIT n OFFSET m
   SQL Server: OFFSET m ROWS FETCH NEXT n ROWS ONLY
*/

-- Top 10 highest paid employees
-- SELECT first_name, last_name, salary
-- FROM employees
-- ORDER BY salary DESC
-- LIMIT 10;

-- Pagination: page 2 with 20 items per page
-- SELECT * FROM products
-- ORDER BY product_id
-- LIMIT 20 OFFSET 20;  -- skips first 20, returns next 20

-- SQL Server equivalent (2012+):
-- SELECT * FROM products
-- ORDER BY product_id
-- OFFSET 20 ROWS FETCH NEXT 20 ROWS ONLY;

-- ============================================================================
-- 9. COMBINING ALL CLAUSES
-- ============================================================================

-- Full query with filtering, sorting, and limiting
-- SELECT
--     product_name,
--     category,
--     price,
--     stock_count
-- FROM products
-- WHERE category = 'Electronics'
--   AND price BETWEEN 50 AND 500
--   AND stock_count > 0
-- ORDER BY price ASC, product_name ASC
-- LIMIT 25;

-- ============================================================================
-- 10. PRACTICE PATTERNS
-- ============================================================================

-- Find recently hired employees in specific departments
-- SELECT employee_id, first_name, last_name, hire_date, department
-- FROM employees
-- WHERE department IN ('Engineering', 'Product')
--   AND hire_date >= '2023-01-01'
-- ORDER BY hire_date DESC;

-- Find customers with incomplete profiles
-- SELECT customer_id, first_name, last_name, email
-- FROM customers
-- WHERE phone IS NULL
--    OR address IS NULL
--    OR email IS NULL;

-- ============================================================================
-- END OF 01_filtering_sorting.sql
-- ============================================================================
