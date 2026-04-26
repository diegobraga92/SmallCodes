/*
   FUNCTIONS & EXPRESSIONS - Scalar Functions, CASE, COALESCE
   File: 02_functions_expressions.sql

   SQL provides many built-in functions to transform and compute data.
   This file covers scalar functions (operate on a single value/row)
   and conditional expressions.
*/

-- ============================================================================
-- 1. STRING FUNCTIONS
-- ============================================================================

/*
   Function        | Description                    | Example
   ----------------|--------------------------------|---------------------------
   UPPER(str)      | Convert to uppercase           | UPPER('hello') → 'HELLO'
   LOWER(str)      | Convert to lowercase           | LOWER('HELLO') → 'hello'
   LENGTH(str)     | String length                  | LENGTH('hello') → 5
   TRIM(str)       | Remove leading/trailing spaces | TRIM('  hi  ') → 'hi'
   LTRIM(str)      | Remove leading spaces          | LTRIM('  hi') → 'hi'
   RTRIM(str)      | Remove trailing spaces         | RTRIM('hi  ') → 'hi'
   SUBSTRING(str, start, len) | Extract substring    | SUBSTRING('hello', 2, 3) → 'ell'
   CONCAT(a, b)    | Concatenate strings            | CONCAT('a', 'b') → 'ab'
   REPLACE(str, from, to) | Replace substring       | REPLACE('abc', 'b', 'x') → 'axc'
   INSTR(str, substr) | Find position of substring  | INSTR('hello', 'l') → 3
*/

-- String function examples (conceptual)
-- SELECT
--     UPPER(first_name) AS upper_name,
--     LOWER(email) AS lower_email,
--     LENGTH(product_code) AS code_length,
--     TRIM('  extra spaces  ') AS trimmed,
--     SUBSTRING(description, 1, 50) AS preview,
--     CONCAT(first_name, ' ', last_name) AS full_name
-- FROM employees;

-- String concatenation varies by database:
-- PostgreSQL/SQLite: 'Hello' || ' ' || 'World'
-- MySQL: CONCAT('Hello', ' ', 'World')
-- SQL Server: 'Hello' + ' ' + 'World' or CONCAT()

-- ============================================================================
-- 2. NUMERIC FUNCTIONS
-- ============================================================================

/*
   Function        | Description                    | Example
   ----------------|--------------------------------|---------------------------
   ROUND(n, d)     | Round to d decimal places      | ROUND(3.14159, 2) → 3.14
   CEIL(n)         | Round up to nearest integer    | CEIL(3.14) → 4
   FLOOR(n)        | Round down to nearest integer  | FLOOR(3.14) → 3
   ABS(n)          | Absolute value                 | ABS(-5) → 5
   MOD(a, b)       | Remainder of a / b             | MOD(10, 3) → 1
   POWER(a, b)     | a raised to power b            | POWER(2, 3) → 8
   SQRT(n)         | Square root                    | SQRT(16) → 4
   RANDOM()        | Random number (0 to 1)         | RANDOM() → 0.374...
*/

-- SELECT
--     ROUND(price, 2) AS rounded_price,
--     CEIL(price) AS ceiling_price,
--     FLOOR(price) AS floor_price,
--     ABS(balance) AS abs_balance,
--     quantity * price AS line_total
-- FROM order_items;

-- ============================================================================
-- 3. DATE/TIME FUNCTIONS
-- ============================================================================

/*
   Date functions vary significantly between databases.
   Common patterns shown with PostgreSQL syntax first,
   then alternatives for other databases.

   PostgreSQL:
   - EXTRACT(YEAR FROM date_col)  → extract year
   - DATE_TRUNC('month', date_col) → truncate to month
   - date_col + INTERVAL '1 day'  → add interval
   - AGE(date1, date2)            → difference
   - NOW() / CURRENT_TIMESTAMP    → current timestamp

   MySQL:
   - YEAR(date_col)
   - DATE_FORMAT(date_col, '%Y-%m-%d')
   - DATE_ADD(date_col, INTERVAL 1 DAY)
   - DATEDIFF(date1, date2)
   - NOW()

   SQL Server:
   - DATEPART(YEAR, date_col)
   - FORMAT(date_col, 'yyyy-MM-dd')
   - DATEADD(DAY, 1, date_col)
   - DATEDIFF(DAY, date1, date2)
   - GETDATE()
*/

-- PostgreSQL examples:
-- SELECT
--     EXTRACT(YEAR FROM hire_date) AS hire_year,
--     EXTRACT(MONTH FROM hire_date) AS hire_month,
--     hire_date + INTERVAL '30 days' AS review_date,
--     AGE(NOW(), hire_date) AS tenure
-- FROM employees;

-- MySQL examples:
-- SELECT
--     YEAR(hire_date) AS hire_year,
--     MONTH(hire_date) AS hire_month,
--     DATE_ADD(hire_date, INTERVAL 30 DAY) AS review_date,
--     DATEDIFF(NOW(), hire_date) AS days_employed
-- FROM employees;

-- ============================================================================
-- 4. TYPE CASTING / CONVERSION
-- ============================================================================

/*
   Casting converts a value from one data type to another.

   PostgreSQL: value::type or CAST(value AS type)
   MySQL:      CAST(value AS type) or CONVERT(value, type)
   SQL Server: CAST(value AS type) or CONVERT(type, value)
   SQLite:     CAST(value AS type)
*/

-- SELECT
--     '123'::INTEGER AS string_to_int,           -- PostgreSQL
--     CAST('2024-01-15' AS DATE) AS string_to_date,
--     CAST(price AS DECIMAL(10, 2)) AS decimal_price,
--     CAST(quantity AS VARCHAR) AS int_to_string;

-- ============================================================================
-- 5. CASE EXPRESSIONS
-- ============================================================================

/*
   CASE is SQL's way of doing if-then-else logic.
   Two forms:
   1. Simple CASE: compares one expression to multiple values
   2. Searched CASE: evaluates multiple boolean conditions
*/

-- Simple CASE (compare one value)
-- SELECT
--     product_name,
--     category,
--     CASE category
--         WHEN 'Electronics' THEN 'Tech'
--         WHEN 'Books'       THEN 'Media'
--         WHEN 'Clothing'    THEN 'Apparel'
--         ELSE 'Other'
--     END AS category_group
-- FROM products;

-- Searched CASE (boolean conditions)
-- SELECT
--     order_id,
--     total_amount,
--     CASE
--         WHEN total_amount >= 1000 THEN 'High Value'
--         WHEN total_amount >= 500  THEN 'Medium Value'
--         WHEN total_amount >= 100  THEN 'Standard'
--         ELSE 'Low Value'
--     END AS order_tier
-- FROM orders;

-- CASE in WHERE clause
-- SELECT * FROM employees
-- WHERE
--     CASE
--         WHEN department = 'Sales' THEN salary > 50000
--         WHEN department = 'Engineering' THEN salary > 80000
--         ELSE salary > 40000
--     END;

-- ============================================================================
-- 6. COALESCE AND NULLIF
-- ============================================================================

/*
   COALESCE(value1, value2, ..., default)
   Returns the first non-NULL value in the list.
   Great for providing default values.

   NULLIF(expr1, expr2)
   Returns NULL if expr1 = expr2, otherwise returns expr1.
   Useful for preventing division by zero.
*/

-- COALESCE: Replace NULL with a default
-- SELECT
--     first_name,
--     COALESCE(phone, email, 'No Contact Info') AS contact,
--     COALESCE(discount, 0) AS discount_rate
-- FROM customers;

-- NULLIF: Prevent division by zero
-- SELECT
--     product_name,
--     revenue,
--     units_sold,
--     revenue / NULLIF(units_sold, 0) AS revenue_per_unit
-- FROM sales;

-- ============================================================================
-- 7. COMBINING FUNCTIONS
-- ============================================================================

-- SELECT
--     UPPER(TRIM(last_name)) AS clean_last_name,
--     ROUND(salary * 1.1, 0) AS projected_salary,
--     CASE
--         WHEN EXTRACT(YEAR FROM AGE(NOW(), hire_date)) >= 5
--         THEN 'Tenured'
--         ELSE 'New'
--     END AS employment_status
-- FROM employees;

-- ============================================================================
-- END OF 02_functions_expressions.sql
-- ============================================================================
