/*
   WINDOW FUNCTIONS - OVER, PARTITION BY, Ranking, Analytics
   File: 13_window_functions.sql

   Window functions perform calculations across a set of rows related
   to the current row. Unlike GROUP BY, they do NOT collapse rows -
   each row retains its identity while gaining access to aggregate data.
*/

-- ============================================================================
-- 1. WINDOW FUNCTION SYNTAX
-- ============================================================================

/*
   function_name() OVER (
       [PARTITION BY col1, col2, ...]
       [ORDER BY col1, col2, ...]
       [frame_specification]
   )

   - PARTITION BY: divides rows into groups (like GROUP BY without collapsing)
   - ORDER BY: defines the order within each partition
   - Frame: defines which rows to include relative to current row
*/

-- ============================================================================
-- 2. RANKING FUNCTIONS
-- ============================================================================

/*
   Function        | Description
   ----------------|-----------------------------------------------
   ROW_NUMBER()    | Unique sequential number (1, 2, 3, ...)
   RANK()          | Rank with gaps for ties (1, 1, 3, ...)
   DENSE_RANK()    | Rank without gaps for ties (1, 1, 2, ...)
   NTILE(n)        | Divides rows into n buckets (1 to n)
*/

-- ROW_NUMBER: unique rank per employee within each department
-- SELECT
--     first_name,
--     last_name,
--     department,
--     salary,
--     ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rank
-- FROM employees;

-- RANK vs DENSE_RANK vs ROW_NUMBER
-- SELECT
--     department,
--     salary,
--     ROW_NUMBER() OVER (ORDER BY salary DESC) AS row_num,
--     RANK() OVER (ORDER BY salary DESC) AS rank,
--     DENSE_RANK() OVER (ORDER BY salary DESC) AS dense_rank
-- FROM employees;

-- NTILE: divide employees into 4 salary quartiles
-- SELECT
--     first_name,
--     last_name,
--     salary,
--     NTILE(4) OVER (ORDER BY salary DESC) AS salary_quartile
-- FROM employees;

-- ============================================================================
-- 3. VALUE FUNCTIONS (Accessing Other Rows)
-- ============================================================================

/*
   Function        | Description
   ----------------|-----------------------------------------------
   LAG(col, n)     | Access value from n rows BEFORE current
   LEAD(col, n)    | Access value from n rows AFTER current
   FIRST_VALUE(col)| First value in the window
   LAST_VALUE(col) | Last value in the window
   NTH_VALUE(col, n)| nth value in the window
*/

-- LAG: compare each employee's salary to the previous one
-- SELECT
--     department,
--     first_name,
--     salary,
--     LAG(salary, 1) OVER (PARTITION BY department ORDER BY salary DESC) AS prev_salary,
--     salary - LAG(salary, 1) OVER (PARTITION BY department ORDER BY salary DESC) AS diff
-- FROM employees;

-- LEAD: compare to next employee
-- SELECT
--     department,
--     first_name,
--     salary,
--     LEAD(salary, 1) OVER (PARTITION BY department ORDER BY salary DESC) AS next_salary
-- FROM employees;

-- FIRST_VALUE: highest salary in each department
-- SELECT
--     department,
--     first_name,
--     salary,
--     FIRST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS dept_max_salary,
--     salary - FIRST_VALUE(salary) OVER (PARTITION BY department ORDER BY salary DESC) AS gap_to_max
-- FROM employees;

-- ============================================================================
-- 4. AGGREGATE WINDOW FUNCTIONS
-- ============================================================================

/*
   Any aggregate function (SUM, AVG, COUNT, MIN, MAX) can be used
   as a window function by adding OVER().
*/

-- Running total of sales by date
-- SELECT
--     order_date,
--     total_amount,
--     SUM(total_amount) OVER (ORDER BY order_date) AS running_total
-- FROM orders;

-- Running total within each customer
-- SELECT
--     customer_id,
--     order_date,
--     total_amount,
--     SUM(total_amount) OVER (
--         PARTITION BY customer_id
--         ORDER BY order_date
--     ) AS customer_running_total
-- FROM orders;

-- Moving average (3-day)
-- SELECT
--     order_date,
--     total_amount,
--     AVG(total_amount) OVER (
--         ORDER BY order_date
--         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
--     ) AS moving_avg_3days
-- FROM orders;

-- Percentage of total per department
-- SELECT
--     department,
--     first_name,
--     salary,
--     ROUND(
--         100.0 * salary / SUM(salary) OVER (PARTITION BY department),
--         2
--     ) AS pct_of_dept_salary
-- FROM employees;

-- ============================================================================
-- 5. FRAME SPECIFICATION
-- ============================================================================

/*
   Frame defines which rows to include in the calculation.

   ROWS BETWEEN
       { UNBOUNDED PRECEDING | n PRECEDING | CURRENT ROW }
   AND
       { UNBOUNDED FOLLOWING | n FOLLOWING | CURRENT ROW }

   Common frames:
   - ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW (default with ORDER BY)
   - ROWS BETWEEN 3 PRECEDING AND 3 FOLLOWING
   - ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
   - RANGE vs ROWS: RANGE treats ties as equal, ROWS does not
*/

-- Default frame with ORDER BY: UNBOUNDED PRECEDING to CURRENT ROW
-- SELECT
--     order_date,
--     amount,
--     SUM(amount) OVER (ORDER BY order_date) AS default_frame
-- FROM orders;

-- Explicit frame: all rows in partition
-- SELECT
--     department,
--     salary,
--     SUM(salary) OVER (
--         PARTITION BY department
--         ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
--     ) AS total_dept_salary
-- FROM employees;

-- ============================================================================
-- 6. PRACTICAL PATTERNS
-- ============================================================================

-- Pattern 1: Find top N per group
-- SELECT * FROM (
--     SELECT
--         department,
--         first_name,
--         last_name,
--         salary,
--         ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) AS rn
--     FROM employees
-- ) ranked
-- WHERE rn <= 3;  -- top 3 per department

-- Pattern 2: Year-over-year comparison
-- SELECT
--     EXTRACT(YEAR FROM order_date) AS year,
--     SUM(amount) AS total_sales,
--     LAG(SUM(amount), 1) OVER (ORDER BY EXTRACT(YEAR FROM order_date)) AS prev_year_sales,
--     ROUND(
--         100.0 * (SUM(amount) - LAG(SUM(amount), 1) OVER (ORDER BY EXTRACT(YEAR FROM order_date)))
--         / NULLIF(LAG(SUM(amount), 1) OVER (ORDER BY EXTRACT(YEAR FROM order_date)), 0),
--         2
--     ) AS yoy_growth_pct
-- FROM orders
-- GROUP BY EXTRACT(YEAR FROM order_date);

-- Pattern 3: Remove duplicates (keep first occurrence)
-- DELETE FROM products
-- WHERE id IN (
--     SELECT id FROM (
--         SELECT
--             id,
--             ROW_NUMBER() OVER (PARTITION BY product_code ORDER BY id) AS rn
--         FROM products
--     ) dup
--     WHERE rn > 1
-- );

-- ============================================================================
-- 7. WINDOW vs GROUP BY
-- ============================================================================

/*
   GROUP BY:  Collapses rows, returns one row per group
   WINDOW:    Preserves all rows, adds aggregated values to each row

   Use GROUP BY when you want summary data.
   Use WINDOW when you want detail data WITH summary context.
*/

-- ============================================================================
-- END OF 13_window_functions.sql
-- ============================================================================
