/*
   SUBQUERIES & CTEs - Nested Queries and Common Table Expressions
   File: 05_subqueries_ctes.sql

   Subqueries (inner queries) allow you to use the result of one query
   inside another. CTEs (WITH clauses) make complex queries more readable
   by breaking them into named, reusable steps.
*/

-- ============================================================================
-- 1. SCALAR SUBQUERIES
-- ============================================================================

/*
   A scalar subquery returns a single value (one row, one column).
   Can be used anywhere a single value is expected:
   - SELECT clause
   - WHERE clause
   - SET clause (in UPDATE)
*/

-- Scalar subquery in SELECT
-- SELECT
--     employee_id,
--     first_name,
--     last_name,
--     salary,
--     (SELECT AVG(salary) FROM employees) AS company_avg_salary,
--     salary - (SELECT AVG(salary) FROM employees) AS diff_from_avg
-- FROM employees;

-- Scalar subquery in WHERE
-- SELECT first_name, last_name, salary
-- FROM employees
-- WHERE salary > (SELECT AVG(salary) FROM employees);

-- Scalar subquery in UPDATE
-- UPDATE products
-- SET price = price * 1.1
-- WHERE category_id = (
--     SELECT id FROM categories WHERE name = 'Electronics'
-- );

-- ============================================================================
-- 2. ROW SUBQUERIES
-- ============================================================================

/*
   A row subquery returns a single row with multiple columns.
   Can be used with row constructors.
*/

-- SELECT employee_id, first_name, last_name
-- FROM employees
-- WHERE (department, salary) = (
--     SELECT department, MAX(salary)
--     FROM employees
--     WHERE department = 'Engineering'
--     GROUP BY department
-- );

-- ============================================================================
-- 3. TABLE SUBQUERIES (Derived Tables)
-- ============================================================================

/*
   A table subquery returns multiple rows and columns.
   Must have an alias when used in FROM clause.
   Also called a "derived table" or "inline view".
*/

-- Find departments where avg salary > company avg
-- SELECT dept_stats.department, dept_stats.avg_salary
-- FROM (
--     SELECT
--         department,
--         AVG(salary) AS avg_salary,
--         COUNT(*) AS emp_count
--     FROM employees
--     GROUP BY department
-- ) AS dept_stats
-- WHERE dept_stats.avg_salary > (
--     SELECT AVG(salary) FROM employees
-- );

-- ============================================================================
-- 4. EXISTS / NOT EXISTS
-- ============================================================================

/*
   EXISTS returns TRUE if the subquery returns at least one row.
   NOT EXISTS returns TRUE if the subquery returns zero rows.
   Often more efficient than IN for large result sets.
   Uses correlated subquery pattern.
*/

-- Find departments that have at least one employee
-- SELECT d.id, d.name
-- FROM departments d
-- WHERE EXISTS (
--     SELECT 1
--     FROM employees e
--     WHERE e.dept_id = d.id
-- );

-- Find customers who have never placed an order
-- SELECT c.id, c.name, c.email
-- FROM customers c
-- WHERE NOT EXISTS (
--     SELECT 1
--     FROM orders o
--     WHERE o.customer_id = c.id
-- );

-- ============================================================================
-- 5. IN / NOT IN with Subqueries
-- ============================================================================

/*
   IN checks if a value matches any value returned by the subquery.
   NOT IN can be tricky with NULLs (returns no rows if subquery has NULL).
   Prefer NOT EXISTS over NOT IN when NULLs are possible.
*/

-- IN with subquery
-- SELECT first_name, last_name
-- FROM employees
-- WHERE department_id IN (
--     SELECT id FROM departments WHERE active = TRUE
-- );

-- NOT IN (watch out for NULLs!)
-- SELECT name FROM customers
-- WHERE id NOT IN (
--     SELECT customer_id FROM orders WHERE customer_id IS NOT NULL
-- );
-- Safer: use NOT EXISTS instead

-- ============================================================================
-- 6. ANY / ALL
-- ============================================================================

/*
   ANY: compares a value to each value returned by the subquery.
        Returns TRUE if ANY comparison is TRUE.
   ALL: compares a value to each value returned by the subquery.
        Returns TRUE if ALL comparisons are TRUE.

   = ANY is equivalent to IN
   <> ALL is equivalent to NOT IN
*/

-- Find employees who earn more than ANY salesperson
-- SELECT first_name, last_name, salary
-- FROM employees
-- WHERE salary > ANY (
--     SELECT salary FROM employees WHERE department = 'Sales'
-- );

-- Find employees who earn more than ALL salespeople
-- SELECT first_name, last_name, salary
-- FROM employees
-- WHERE salary > ALL (
--     SELECT salary FROM employees WHERE department = 'Sales'
-- );

-- ============================================================================
-- 7. CORRELATED SUBQUERIES
-- ============================================================================

/*
   A correlated subquery references columns from the outer query.
   It is re-evaluated for EVERY row in the outer query.
   Can be slow on large tables, but very powerful.
*/

-- Find employees who earn more than the average in their department
-- SELECT e.first_name, e.last_name, e.department, e.salary
-- FROM employees e
-- WHERE e.salary > (
--     SELECT AVG(salary)
--     FROM employees
--     WHERE department = e.department
-- );

-- Find the most recent order for each customer
-- SELECT o1.customer_id, o1.order_id, o1.order_date
-- FROM orders o1
-- WHERE o1.order_date = (
--     SELECT MAX(o2.order_date)
--     FROM orders o2
--     WHERE o2.customer_id = o1.customer_id
-- );

-- ============================================================================
-- 8. COMMON TABLE EXPRESSIONS (CTEs / WITH clause)
-- ============================================================================

/*
   CTEs define temporary named result sets that exist for the duration
   of a single query. They make complex queries much more readable.

   Syntax:
   WITH cte_name AS (
       SELECT ...
   )
   SELECT * FROM cte_name;
*/

-- Basic CTE
-- WITH dept_avg AS (
--     SELECT
--         department,
--         AVG(salary) AS avg_salary
--     FROM employees
--     GROUP BY department
-- )
-- SELECT e.first_name, e.last_name, e.department, e.salary, d.avg_salary
-- FROM employees e
-- INNER JOIN dept_avg d ON e.department = d.department
-- WHERE e.salary > d.avg_salary;

-- Multiple CTEs
-- WITH
--     dept_stats AS (
--         SELECT department, AVG(salary) AS avg_sal, COUNT(*) AS cnt
--         FROM employees GROUP BY department
--     ),
--     high_performers AS (
--         SELECT * FROM employees WHERE rating >= 4
--     )
-- SELECT d.department, d.avg_sal, d.cnt, COUNT(hp.id) AS high_performers
-- FROM dept_stats d
-- LEFT JOIN high_performers hp ON d.department = hp.department
-- GROUP BY d.department, d.avg_sal, d.cnt;

-- ============================================================================
-- 9. RECURSIVE CTEs
-- ============================================================================

/*
   Recursive CTEs reference themselves. Useful for:
   - Hierarchical data (org charts, category trees)
   - Graph traversal
   - Generating sequences

   Structure:
   WITH RECURSIVE cte AS (
       -- Anchor: base case (non-recursive)
       SELECT ...
       UNION ALL
       -- Recursive: references cte itself
       SELECT ... FROM cte WHERE ...
   )
   SELECT * FROM cte;
*/

-- Generate a number sequence 1 to 10
-- WITH RECURSIVE numbers AS (
--     SELECT 1 AS n
--     UNION ALL
--     SELECT n + 1 FROM numbers WHERE n < 10
-- )
-- SELECT * FROM numbers;

-- Organizational hierarchy
-- WITH RECURSIVE org_chart AS (
--     -- Anchor: top-level manager
--     SELECT id, name, manager_id, 1 AS level
--     FROM employees
--     WHERE manager_id IS NULL
--
--     UNION ALL
--
--     -- Recursive: direct reports
--     SELECT e.id, e.name, e.manager_id, oc.level + 1
--     FROM employees e
--     INNER JOIN org_chart oc ON e.manager_id = oc.id
-- )
-- SELECT * FROM org_chart ORDER BY level, name;

-- ============================================================================
-- 10. SUBQUERY vs CTE vs JOIN - When to Use What
-- ============================================================================

/*
   Use a JOIN when:
   - You need columns from multiple related tables
   - The relationship is straightforward

   Use a subquery when:
   - You need a single aggregated value for comparison
   - You're checking existence (EXISTS)
   - The inner query is simple and used once

   Use a CTE when:
   - The same subquery is used multiple times
   - You need recursion
   - You want to break a complex query into readable steps
   - You need to reference the result multiple times
*/

-- ============================================================================
-- END OF 05_subqueries_ctes.sql
-- ============================================================================
