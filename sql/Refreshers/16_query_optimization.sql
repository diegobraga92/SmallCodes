/*
   QUERY OPTIMIZATION - EXPLAIN Plans, Join Strategies, Rewriting
   File: 16_query_optimization.sql

   Moving beyond basic indexing, this file covers how to analyze
   and optimize query performance using execution plans and
   query rewriting techniques.
*/

-- ============================================================================
-- 1. EXPLAIN PLAN DEEP DIVE
-- ============================================================================

/*
   EXPLAIN shows the query plan without executing.
   EXPLAIN ANALYZE executes the query and shows actual timings.

   Key metrics in EXPLAIN ANALYZE output:
   - actual time: actual execution time (startup..total)
   - rows: actual number of rows returned
   - loops: how many times the node was executed
   - cost: optimizer's estimated cost (startup..total)
   - width: estimated width of output rows in bytes
*/

-- Basic usage:
-- EXPLAIN SELECT * FROM employees WHERE department_id = 1;
-- EXPLAIN ANALYZE SELECT * FROM employees WHERE department_id = 1;

-- ============================================================================
-- 2. SCAN TYPES
-- ============================================================================

/*
   Sequential Scan (Seq Scan):
   - Reads entire table from start to finish
   - Efficient for small tables or when retrieving >10% of rows
   - Bad for large tables with selective queries

   Index Scan:
   - Uses index to find matching rows, then fetches from table
   - Good for selective queries (returning few rows)
   - Two steps: index lookup + table access

   Index Only Scan:
   - All needed data is in the index itself
   - No table access needed (fastest)
   - Requires covering index

   Bitmap Scan:
   - Combines multiple indexes
   - Good for queries with OR conditions or multiple filters
   - Two steps: bitmap index scan + bitmap heap scan
*/

-- ============================================================================
-- 3. JOIN STRATEGIES
-- ============================================================================

/*
   Nested Loop Join:
   - For each row in outer table, scan inner table
   - Best for small result sets (< 1000 rows)
   - Efficient when inner table has an index
   - O(outer_rows × inner_access_cost)

   Hash Join:
   - Build hash table on smaller table, probe with larger
   - Best for medium to large result sets
   - No index needed on join columns
   - O(outer_rows + inner_rows)

   Merge Join:
   - Sort both tables, then merge
   - Best for large sorted result sets
   - Requires sorted input (index or explicit sort)
   - O(outer_rows + inner_rows)
*/

-- Force a specific join type (PostgreSQL):
-- SET enable_nestloop = OFF;
-- SET enable_hashjoin = OFF;
-- SET enable_mergejoin = OFF;

-- ============================================================================
-- 4. SARGBLE PREDICATES
-- ============================================================================

/*
   Sargable (Search ARGument ABLE): predicates that can use indexes.

   SARGBLE (can use index):           NON-SARGBLE (cannot use index):
   WHERE date >= '2024-01-01'         WHERE YEAR(date) = 2024
   WHERE price = 100                  WHERE price * 1.1 > 100
   WHERE name = 'Smith'               WHERE UPPER(name) = 'SMITH'
   WHERE amount BETWEEN 10 AND 20     WHERE amount + 5 > 15
   WHERE id = 42                      WHERE CAST(id AS VARCHAR) = '42'
*/

-- Fix non-sargable queries:
-- BAD:  SELECT * FROM orders WHERE YEAR(order_date) = 2024;
-- GOOD: SELECT * FROM orders WHERE order_date >= '2024-01-01'
--                              AND order_date < '2025-01-01';

-- BAD:  SELECT * FROM products WHERE price * 1.1 > 100;
-- GOOD: SELECT * FROM products WHERE price > 100 / 1.1;

-- ============================================================================
-- 5. QUERY REWRITING TECHNIQUES
-- ============================================================================

-- Technique 1: Replace OR with UNION ALL
-- BAD:
-- SELECT * FROM employees WHERE department = 'Engineering' OR department = 'Sales';
-- GOOD:
-- SELECT * FROM employees WHERE department = 'Engineering'
-- UNION ALL
-- SELECT * FROM employees WHERE department = 'Sales';

-- Technique 2: Use EXISTS instead of DISTINCT with JOIN
-- BAD (returns duplicate customers if they have multiple orders):
-- SELECT DISTINCT c.* FROM customers c
-- JOIN orders o ON c.id = o.customer_id;
-- GOOD:
-- SELECT c.* FROM customers c
-- WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.id);

-- Technique 3: Use IN instead of OR
-- BAD:  WHERE department = 'Eng' OR department = 'Sales' OR department = 'Mktg'
-- GOOD: WHERE department IN ('Eng', 'Sales', 'Mktg')

-- Technique 4: Avoid SELECT *
-- BAD:  SELECT * FROM employees WHERE ...
-- GOOD: SELECT employee_id, first_name, last_name FROM employees WHERE ...

-- ============================================================================
-- 6. MATERIALIZED VIEWS
-- ============================================================================

/*
   Materialized views store query results physically.
   They are refreshed on demand (not automatically).
   Great for expensive aggregations used in reports.
*/

-- PostgreSQL:
-- CREATE MATERIALIZED VIEW monthly_sales_summary AS
-- SELECT
--     DATE_TRUNC('month', order_date) AS month,
--     product_id,
--     SUM(quantity) AS units_sold,
--     SUM(total_amount) AS revenue
-- FROM orders
-- GROUP BY DATE_TRUNC('month', order_date), product_id;
--
-- CREATE INDEX idx_monthly_sales_month ON monthly_sales_summary(month);
--
-- -- Refresh (can be scheduled):
-- REFRESH MATERIALIZED VIEW monthly_sales_summary;

-- ============================================================================
-- 7. STATISTICS
-- ============================================================================

/*
   The query optimizer uses table statistics to estimate row counts.
   Outdated statistics lead to poor query plans.
*/

-- PostgreSQL:
-- ANALYZE employees;  -- Update statistics for one table
-- ANALYZE;            -- Update statistics for all tables

-- MySQL:
-- ANALYZE TABLE employees;

-- SQL Server:
-- UPDATE STATISTICS employees;

-- ============================================================================
-- 8. OPTIMIZATION PROCESS
-- ============================================================================

/*
   1. Identify slow queries (logs, monitoring, user reports)
   2. Get the query plan (EXPLAIN ANALYZE)
   3. Look for sequential scans on large tables
   4. Check if appropriate indexes exist
   5. Check if predicates are sargable
   6. Check join order and strategies
   7. Check for outdated statistics
   8. Apply fix (index, rewrite, or schema change)
   9. Verify improvement with EXPLAIN ANALYZE
   10. Monitor in production
*/

-- ============================================================================
-- END OF 16_query_optimization.sql
-- ============================================================================
