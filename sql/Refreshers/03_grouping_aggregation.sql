/*
   GROUPING & AGGREGATION - GROUP BY, HAVING, Aggregate Functions
   File: 03_grouping_aggregation.sql

   Aggregate functions combine multiple rows into a single result.
   GROUP BY divides rows into groups and applies aggregates per group.
   HAVING filters groups (like WHERE filters rows).
*/

-- ============================================================================
-- 1. AGGREGATE FUNCTIONS
-- ============================================================================

/*
   Function    | Description                          | NULL handling
   ------------|--------------------------------------|---------------------------
   COUNT(*)    | Count all rows                       | Includes NULLs
   COUNT(col)  | Count non-NULL values in column      | Excludes NULLs
   COUNT(DISTINCT col) | Count unique non-NULL values | Excludes NULLs
   SUM(col)    | Sum of values                        | Ignores NULLs
   AVG(col)    | Average of values                    | Ignores NULLs
   MIN(col)    | Minimum value                        | Ignores NULLs
   MAX(col)    | Maximum value                        | Ignores NULLs
*/

-- Basic aggregate examples (conceptual)
-- SELECT
--     COUNT(*) AS total_employees,
--     COUNT(manager_id) AS employees_with_manager,  -- excludes NULLs
--     COUNT(DISTINCT department) AS unique_departments,
--     AVG(salary) AS average_salary,
--     SUM(salary) AS total_salary,
--     MIN(salary) AS min_salary,
--     MAX(salary) AS max_salary
-- FROM employees;

-- ============================================================================
-- 2. GROUP BY - Grouping Rows
-- ============================================================================

/*
   GROUP BY divides the result set into groups.
   Each group produces one row in the output.
   All non-aggregated columns in SELECT must appear in GROUP BY.
*/

-- Count employees per department
-- SELECT
--     department,
--     COUNT(*) AS employee_count
-- FROM employees
-- GROUP BY department;

-- Average salary by department
-- SELECT
--     department,
--     ROUND(AVG(salary), 2) AS avg_salary,
--     MAX(salary) AS max_salary,
--     MIN(salary) AS min_salary
-- FROM employees
-- GROUP BY department;

-- Multiple columns in GROUP BY
-- SELECT
--     department,
--     job_title,
--     COUNT(*) AS employee_count,
--     AVG(salary) AS avg_salary
-- FROM employees
-- GROUP BY department, job_title
-- ORDER BY department, job_title;

-- ============================================================================
-- 3. HAVING - Filtering Groups
-- ============================================================================

/*
   HAVING filters groups AFTER aggregation.
   WHERE filters rows BEFORE aggregation.
   You can use both in the same query.
*/

-- Find departments with more than 10 employees
-- SELECT
--     department,
--     COUNT(*) AS employee_count
-- FROM employees
-- GROUP BY department
-- HAVING COUNT(*) > 10;

-- Find departments with average salary > $80,000
-- SELECT
--     department,
--     ROUND(AVG(salary), 2) AS avg_salary
-- FROM employees
-- GROUP BY department
-- HAVING AVG(salary) > 80000;

-- WHERE + GROUP BY + HAVING combined
-- SELECT
--     department,
--     COUNT(*) AS employee_count,
--     ROUND(AVG(salary), 2) AS avg_salary
-- FROM employees
-- WHERE hire_date >= '2020-01-01'  -- filter rows first
-- GROUP BY department
-- HAVING COUNT(*) >= 5              -- filter groups after
-- ORDER BY avg_salary DESC;

-- ============================================================================
-- 4. EXECUTION ORDER (Critical!)
-- ============================================================================

/*
   FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY

   This means:
   - WHERE cannot use aggregate functions (aggregation hasn't happened yet)
   - HAVING CAN use aggregate functions
   - Column aliases from SELECT cannot be used in HAVING (in standard SQL)
     (Some DBs like MySQL and PostgreSQL allow it, but it's not portable)
*/

-- WRONG: WHERE with aggregate
-- SELECT department, AVG(salary)
-- FROM employees
-- WHERE AVG(salary) > 50000   -- ERROR: cannot use aggregate in WHERE
-- GROUP BY department;

-- RIGHT: Use HAVING instead
-- SELECT department, AVG(salary)
-- FROM employees
-- GROUP BY department
-- HAVING AVG(salary) > 50000;

-- ============================================================================
-- 5. GROUP BY WITH ROLLUP / CUBE
-- ============================================================================

/*
   ROLLUP generates subtotals and grand totals.
   CUBE generates all possible combinations of subtotals.
   GROUPING SETS allows custom combinations.

   Supported in PostgreSQL, MySQL, SQL Server.
   SQLite supports GROUPING SETS from version 3.34.0.
*/

-- ROLLUP: subtotals per department + grand total
-- SELECT
--     COALESCE(department, 'ALL DEPARTMENTS') AS department,
--     COUNT(*) AS employee_count,
--     ROUND(AVG(salary), 2) AS avg_salary
-- FROM employees
-- GROUP BY ROLLUP(department);

-- ============================================================================
-- 6. COMMON AGGREGATION PATTERNS
-- ============================================================================

-- Pattern 1: Count with percentage
-- SELECT
--     department,
--     COUNT(*) AS count,
--     ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS percentage
-- FROM employees
-- GROUP BY department
-- ORDER BY count DESC;

-- Pattern 2: Find most common value per group
-- SELECT
--     department,
--     job_title,
--     COUNT(*) AS count
-- FROM employees
-- GROUP BY department, job_title
-- HAVING COUNT(*) = (
--     SELECT MAX(cnt) FROM (
--         SELECT COUNT(*) AS cnt
--         FROM employees e2
--         WHERE e2.department = employees.department
--         GROUP BY job_title
--     ) AS sub
-- );

-- Pattern 3: Multiple aggregates in one query
-- SELECT
--     customer_id,
--     COUNT(*) AS order_count,
--     SUM(total_amount) AS total_spent,
--     AVG(total_amount) AS avg_order_value,
--     MIN(order_date) AS first_order,
--     MAX(order_date) AS last_order
-- FROM orders
-- GROUP BY customer_id
-- HAVING COUNT(*) > 1;  -- repeat customers only

-- ============================================================================
-- 7. AGGREGATE FUNCTION DETAILS
-- ============================================================================

/*
   COUNT(*) vs COUNT(column):
   - COUNT(*) counts all rows including those with all NULLs
   - COUNT(column) counts non-NULL values in that column

   AVG(column):
   - SUM(column) / COUNT(column) for non-NULL values
   - NULLs are ignored, not treated as zero

   SUM(column):
   - Returns NULL if all values are NULL (not zero)
   - Use COALESCE(SUM(column), 0) to get zero instead
*/

-- Demonstration of NULL handling in aggregates
-- SELECT
--     COUNT(*) AS total_rows,
--     COUNT(manager_id) AS rows_with_manager,
--     AVG(COALESCE(salary, 0)) AS avg_including_nulls,
--     AVG(salary) AS avg_excluding_nulls
-- FROM employees;

-- ============================================================================
-- END OF 03_grouping_aggregation.sql
-- ============================================================================
