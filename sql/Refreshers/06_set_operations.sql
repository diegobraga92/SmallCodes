/*
   SET OPERATIONS - UNION, INTERSECT, EXCEPT
   File: 06_set_operations.sql

   Set operations combine results from multiple SELECT queries.
   They operate on entire result sets (rows), not individual columns.
*/

-- ============================================================================
-- 1. SET OPERATION RULES
-- ============================================================================

/*
   All set operations follow these rules:
   1. Each SELECT must have the same number of columns
   2. Corresponding columns must have compatible data types
   3. Column names come from the first SELECT
   4. Duplicates are removed by default (except UNION ALL)
   5. ORDER BY applies to the final result, placed after last SELECT
*/

-- ============================================================================
-- 2. UNION vs UNION ALL
-- ============================================================================

/*
   UNION:       Combines results, removes duplicates (slower, sorts internally)
   UNION ALL:   Combines results, keeps all rows (faster, no sorting)

   Use UNION when you need distinct results.
   Use UNION ALL when duplicates are acceptable or impossible.
   UNION ALL is almost always faster.
*/

-- UNION: unique active and inactive employees
-- SELECT id, name, 'Active' AS status FROM active_employees
-- UNION
-- SELECT id, name, 'Inactive' AS status FROM former_employees;

-- UNION ALL: all customers from both regions (including duplicates)
-- SELECT customer_id, name FROM customers_north
-- UNION ALL
-- SELECT customer_id, name FROM customers_south;

-- ============================================================================
-- 3. INTERSECT
-- ============================================================================

/*
   INTERSECT returns rows that appear in BOTH result sets.
   Equivalent to INNER JOIN on all columns.
   Not supported in MySQL (use INNER JOIN or EXISTS instead).
*/

-- Customers who have placed orders
-- SELECT id, name FROM customers
-- INTERSECT
-- SELECT customer_id, customer_name FROM orders;

-- Equivalent with JOIN:
-- SELECT DISTINCT c.id, c.name
-- FROM customers c
-- INNER JOIN orders o ON c.id = o.customer_id;

-- ============================================================================
-- 4. EXCEPT (MINUS)
-- ============================================================================

/*
   EXCEPT returns rows from the first query that are NOT in the second.
   Called MINUS in Oracle.
   Not supported in MySQL (use LEFT JOIN or NOT EXISTS instead).
*/

-- Customers who have NOT placed any orders
-- SELECT id, name FROM customers
-- EXCEPT
-- SELECT customer_id, customer_name FROM orders;

-- Equivalent with NOT EXISTS:
-- SELECT c.id, c.name
-- FROM customers c
-- WHERE NOT EXISTS (
--     SELECT 1 FROM orders o WHERE o.customer_id = c.id
-- );

-- ============================================================================
-- 5. ORDER BY with Set Operations
-- ============================================================================

/*
   ORDER BY applies to the entire combined result.
   Must reference column names from the first SELECT.
   Placed at the very end.
*/

-- SELECT first_name, last_name, 'Employee' AS type
-- FROM employees
-- UNION ALL
-- SELECT first_name, last_name, 'Contractor' AS type
-- FROM contractors
-- ORDER BY last_name, first_name;

-- ============================================================================
-- 6. Practical Patterns
-- ============================================================================

-- Pattern 1: Combine data from similar tables (partitioned data)
-- SELECT 'Q1' AS quarter, product_id, SUM(revenue) AS total_revenue
-- FROM sales_q1 GROUP BY product_id
-- UNION ALL
-- SELECT 'Q2' AS quarter, product_id, SUM(revenue) AS total_revenue
-- FROM sales_q2 GROUP BY product_id
-- ORDER BY quarter, product_id;

-- Pattern 2: Find discrepancies between two systems
-- SELECT product_sku, price FROM system_a
-- EXCEPT
-- SELECT product_sku, price FROM system_b;
-- Returns products where prices differ between systems

-- Pattern 3: Full list with type indicator
-- SELECT email, 'user' AS source FROM users
-- UNION ALL
-- SELECT email, 'lead' AS source FROM leads
-- UNION ALL
-- SELECT email, 'newsletter' AS source FROM subscribers;

-- ============================================================================
-- 7. Set Operations vs Joins
-- ============================================================================

/*
   Set operations combine ROWS vertically (stacking).
   Joins combine COLUMNS horizontally (side by side).

   UNION:     rows from A + rows from B (stacked)
   JOIN:      columns from A + columns from B (side by side)

   Choose based on whether you want more rows or more columns.
*/

-- ============================================================================
-- END OF 06_set_operations.sql
-- ============================================================================
