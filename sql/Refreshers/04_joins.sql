/*
   JOINS - Combining Data from Multiple Tables
   File: 04_joins.sql

   Joins are the heart of relational databases. They allow you to
   combine rows from two or more tables based on related columns.
*/

-- ============================================================================
-- 1. SAMPLE TABLES (Conceptual Schema)
-- ============================================================================

/*
   employees                          departments
   +----+--------+--------+------+    +----+------------------+
   | id | name   | dept_id| sal  |    | id | name             |
   +----+--------+--------+------+    +----+------------------+
   | 1  | Alice  | 1      | 70k  |    | 1  | Engineering      |
   | 2  | Bob    | 2      | 60k  |    | 2  | Sales            |
   | 3  | Carol  | 1      | 80k  |    | 3  | Marketing        |
   | 4  | Dave   | NULL   | 50k  |    +----+------------------+
   +----+--------+--------+------+
*/

-- ============================================================================
-- 2. INNER JOIN
-- ============================================================================

/*
   INNER JOIN returns rows where there is a match in BOTH tables.
   This is the most common type of join.

   If a row in the left table has no match in the right table,
   it is excluded from the results.
*/

-- Basic INNER JOIN
-- SELECT
--     e.name AS employee_name,
--     d.name AS department_name
-- FROM employees e
-- INNER JOIN departments d ON e.dept_id = d.id;

-- Result:
-- Alice  | Engineering
-- Bob    | Sales
-- Carol  | Engineering
-- (Dave is excluded because dept_id is NULL)

-- INNER JOIN with additional conditions
-- SELECT
--     e.name,
--     d.name AS department,
--     e.salary
-- FROM employees e
-- INNER JOIN departments d ON e.dept_id = d.id
-- WHERE e.salary > 60000;

-- ============================================================================
-- 3. LEFT JOIN (LEFT OUTER JOIN)
-- ============================================================================

/*
   LEFT JOIN returns ALL rows from the left table,
   and matching rows from the right table.
   If no match exists, right table columns are NULL.
*/

-- SELECT
--     e.name AS employee_name,
--     d.name AS department_name
-- FROM employees e
-- LEFT JOIN departments d ON e.dept_id = d.id;

-- Result:
-- Alice  | Engineering
-- Bob    | Sales
-- Carol  | Engineering
-- Dave   | NULL  (no matching department)

-- Find employees without a department
-- SELECT e.name
-- FROM employees e
-- LEFT JOIN departments d ON e.dept_id = d.id
-- WHERE d.id IS NULL;

-- ============================================================================
-- 4. RIGHT JOIN (RIGHT OUTER JOIN)
-- ============================================================================

/*
   RIGHT JOIN is the mirror of LEFT JOIN.
   Returns ALL rows from the right table.
   Less common than LEFT JOIN (can usually rewrite as LEFT JOIN).
*/

-- SELECT
--     e.name AS employee_name,
--     d.name AS department_name
-- FROM employees e
-- RIGHT JOIN departments d ON e.dept_id = d.id;

-- Result:
-- Alice  | Engineering
-- Bob    | Sales
-- Carol  | Engineering
-- NULL   | Marketing  (no employees in Marketing)

-- ============================================================================
-- 5. FULL JOIN (FULL OUTER JOIN)
-- ============================================================================

/*
   FULL JOIN returns ALL rows from BOTH tables.
   NULLs fill in where there is no match.
   Not supported in MySQL (use UNION of LEFT and RIGHT joins).
*/

-- SELECT
--     e.name AS employee_name,
--     d.name AS department_name
-- FROM employees e
-- FULL JOIN departments d ON e.dept_id = d.id;

-- Result:
-- Alice  | Engineering
-- Bob    | Sales
-- Carol  | Engineering
-- Dave   | NULL
-- NULL   | Marketing

-- ============================================================================
-- 6. CROSS JOIN
-- ============================================================================

/*
   CROSS JOIN produces a Cartesian product.
   Every row from table A is paired with every row from table B.
   No ON clause needed (and should not have one).

   Result: rows(A) × rows(B) rows
   Use with caution on large tables!
*/

-- SELECT
--     e.name AS employee,
--     d.name AS department
-- FROM employees e
-- CROSS JOIN departments d;

-- With 4 employees and 3 departments, this returns 12 rows.

-- ============================================================================
-- 7. SELF JOIN
-- ============================================================================

/*
   A self-join joins a table to itself.
   Useful for hierarchical data (employees and managers).
   Requires table aliases to distinguish the two roles.
*/

-- Find employees and their managers
-- SELECT
--     e.name AS employee_name,
--     m.name AS manager_name
-- FROM employees e
-- LEFT JOIN employees m ON e.manager_id = m.id;

-- Find employees who earn more than their manager
-- SELECT
--     e.name AS employee_name,
--     e.salary AS employee_salary,
--     m.name AS manager_name,
--     m.salary AS manager_salary
-- FROM employees e
-- INNER JOIN employees m ON e.manager_id = m.id
-- WHERE e.salary > m.salary;

-- ============================================================================
-- 8. JOINING MULTIPLE TABLES
-- ============================================================================

/*
   You can join more than two tables in a single query.
   Each join adds another table to the result.
*/

-- Three-table join: orders → customers → products
-- SELECT
--     o.order_id,
--     c.name AS customer_name,
--     p.product_name,
--     oi.quantity,
--     oi.unit_price
-- FROM orders o
-- INNER JOIN customers c ON o.customer_id = c.id
-- INNER JOIN order_items oi ON o.id = oi.order_id
-- INNER JOIN products p ON oi.product_id = p.id;

-- ============================================================================
-- 9. JOIN CONDITIONS vs WHERE CONDITIONS
-- ============================================================================

/*
   Conditions in ON clause are evaluated during the join.
   Conditions in WHERE clause are evaluated after the join.

   For INNER JOIN: ON + WHERE produces the same result.
   For LEFT JOIN:  ON + WHERE can produce different results!
*/

-- LEFT JOIN with condition in ON (keeps all left rows)
-- SELECT e.name, d.name
-- FROM employees e
-- LEFT JOIN departments d ON e.dept_id = d.id AND d.name = 'Engineering';

-- Result: All employees, but only Engineering dept names shown
-- Alice  | Engineering
-- Bob    | NULL
-- Carol  | Engineering
-- Dave   | NULL

-- LEFT JOIN with condition in WHERE (filters after join, loses left rows)
-- SELECT e.name, d.name
-- FROM employees e
-- LEFT JOIN departments d ON e.dept_id = d.id
-- WHERE d.name = 'Engineering';

-- Result: Only employees in Engineering
-- Alice  | Engineering
-- Carol  | Engineering

-- ============================================================================
-- 10. NATURAL JOIN (Use with Caution)
-- ============================================================================

/*
   NATURAL JOIN automatically joins on columns with the same name.
   Convenient but dangerous: you don't control the join condition.
   Schema changes can silently break your query.
*/

-- SELECT * FROM employees NATURAL JOIN departments;
-- Joins on columns with matching names (e.g., both have 'id')

-- ============================================================================
-- 11. JOIN BEST PRACTICES
-- ============================================================================

/*
   1. Always use table aliases (e, d, o) for readability
   2. Always specify the join type explicitly (INNER, LEFT, etc.)
   3. Always use ON clause (never WHERE for join conditions)
   4. Be explicit about join conditions (avoid NATURAL JOIN)
   5. Consider join order for performance (smallest result set first)
   6. Use LEFT JOIN when you need to preserve all rows from one side
   7. Test with small data before running on production
*/

-- ============================================================================
-- END OF 04_joins.sql
-- ============================================================================
