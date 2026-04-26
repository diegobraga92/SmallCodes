/*
   SQL BASICS - SELECT, FROM, WHERE, and Core Syntax
   File: 00_sql_basics.sql

   This file covers the fundamental structure of SQL queries.
   SQL (Structured Query Language) is the standard language for
   relational database management systems.

   KEY CONCEPTS:
   - SQL is declarative: you say WHAT you want, not HOW to get it
   - The database engine figures out the execution plan
   - SQL keywords are case-insensitive (SELECT = select = Select)
   - Table/column names may be case-sensitive depending on the DB
   - Statements end with a semicolon (;)
*/

-- ============================================================================
-- 1. BASIC SELECT STATEMENT
-- ============================================================================

-- The simplest query: select all columns from a table
-- SELECT * FROM employees;

-- Better practice: specify columns explicitly
-- SELECT employee_id, first_name, last_name, salary FROM employees;

-- Selecting literal values (no table needed)
SELECT 'Hello, SQL!' AS greeting;
-- Result: 'Hello, SQL!'

-- Selecting expressions
SELECT 1 + 1 AS sum_result;
-- Result: 2

-- Multiple expressions
SELECT
    10 AS number,
    'text' AS string_value,
    3.14159 AS pi,
    CURRENT_DATE AS today;
-- CURRENT_DATE returns today's date (varies by DB)

-- ============================================================================
-- 2. THE WHERE CLAUSE - Filtering Rows
-- ============================================================================

-- WHERE filters rows BEFORE they are returned
-- SELECT * FROM employees WHERE department = 'Engineering';

-- Comparison operators
-- =    Equal to
-- <>   Not equal to (also != in some DBs)
-- >    Greater than
-- <    Less than
-- >=   Greater than or equal
-- <=   Less than or equal

-- Examples (conceptual - tables may not exist):
-- SELECT * FROM products WHERE price > 100;
-- SELECT * FROM orders WHERE status <> 'cancelled';
-- SELECT * FROM users WHERE age >= 18;

-- ============================================================================
-- 3. COMMENTS IN SQL
-- ============================================================================

-- Single line comment (double dash)

/*
   Multi-line comment
   Can span multiple lines
   Useful for documenting complex queries
*/

-- ============================================================================
-- 4. CASE CONVENTIONS
-- ============================================================================

/*
   Common styles:
   1. UPPERCASE keywords: SELECT, FROM, WHERE (traditional)
   2. lowercase keywords: select, from, where (modern)
   3. snake_case for tables/columns: employee_salary, order_items
   4. PascalCase for tables: Employee, OrderItem (SQL Server convention)

   Consistency within a project matters more than the specific style.
   This file uses UPPERCASE for keywords and snake_case for identifiers.
*/

-- ============================================================================
-- 5. NULL CONCEPT
-- ============================================================================

/*
   NULL represents "unknown" or "no value"
   - NULL is NOT zero, empty string, or false
   - NULL != NULL (you cannot use = to compare NULLs)
   - Use IS NULL or IS NOT NULL to check for NULL
   - Any arithmetic with NULL results in NULL
*/

-- Checking for NULL
-- SELECT * FROM customers WHERE email IS NULL;
-- SELECT * FROM customers WHERE email IS NOT NULL;

-- NULL in expressions
SELECT NULL + 5 AS null_result;  -- Result: NULL
SELECT NULL || 'text' AS null_concat;  -- Result: NULL (in some DBs)

-- ============================================================================
-- 6. ALIASES (AS)
-- ============================================================================

/*
   Aliases give a temporary name to a column or table
   - The AS keyword is optional in most DBs
   - Useful for making output more readable
   - Required when using expressions or functions
*/

-- Column alias
SELECT
    first_name AS "First Name",
    last_name  AS "Last Name"
-- FROM employees;

-- Table alias (essential for joins, covered later)
-- SELECT e.first_name, d.department_name
-- FROM employees AS e
-- JOIN departments AS d ON e.dept_id = d.dept_id;

-- ============================================================================
-- 7. DISTINCT - Removing Duplicates
-- ============================================================================

/*
   DISTINCT removes duplicate rows from the result set.
   It applies to ALL selected columns, not just one.
*/

-- SELECT DISTINCT department FROM employees;
-- SELECT DISTINCT city, state FROM addresses;  -- unique combinations

-- ============================================================================
-- 8. LITERALS AND DATA TYPES (Overview)
-- ============================================================================

/*
   String literals:   'single quotes' (standard SQL)
   Number literals:   42, 3.14, -10
   Date literals:     '2024-01-15' (ISO format, varies by DB)
   Boolean literals:  TRUE, FALSE (not all DBs support natively)
   NULL literal:      NULL
*/

-- String literal examples
SELECT 'Hello World' AS greeting;
SELECT 'It''s SQL'   AS escaped_quote;  -- Single quote escaped with another quote

-- ============================================================================
-- 9. PRACTICAL EXAMPLES (Conceptual)
-- ============================================================================

-- Example 1: Find active users
-- SELECT user_id, username, email
-- FROM users
-- WHERE active = TRUE;

-- Example 2: Get recent orders
-- SELECT order_id, customer_id, order_date, total_amount
-- FROM orders
-- WHERE order_date >= '2024-01-01';

-- Example 3: Count employees per department
-- SELECT department_id, COUNT(*) AS employee_count
-- FROM employees
-- GROUP BY department_id;

-- ============================================================================
-- 10. COMMON MISTAKES
-- ============================================================================

/*
   MISTAKE 1: Using = NULL instead of IS NULL
   WRONG:  WHERE name = NULL
   RIGHT:  WHERE name IS NULL

   MISTAKE 2: Missing semicolon
   WRONG:  SELECT * FROM table
   RIGHT:  SELECT * FROM table;

   MISTAKE 3: Using double quotes for strings (in most DBs)
   WRONG:  WHERE name = "Alice"   (double quotes = identifiers in standard SQL)
   RIGHT:  WHERE name = 'Alice'

   MISTAKE 4: Forgetting that string comparisons may be case-sensitive
   'alice' may not match 'Alice' depending on collation settings
*/

-- ============================================================================
-- END OF 00_sql_basics.sql
-- ============================================================================
