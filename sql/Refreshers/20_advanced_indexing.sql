/*
   ADVANCED INDEXING - Covering Indexes, Partial, Functional, Maintenance
   File: 20_advanced_indexing.sql

   Beyond basic B-tree indexes, advanced indexing techniques
   can dramatically improve query performance for specific patterns.
*/

-- ============================================================================
-- 1. COVERING INDEXES (Index-Only Scans)
-- ============================================================================

/*
   A covering index contains ALL columns needed by a query.
   The database can answer the query entirely from the index,
   never touching the table. This is the fastest scan type.

   PostgreSQL: INCLUDE columns (since 11)
   SQL Server: INCLUDE columns
   MySQL: All columns in a composite index are included
*/

-- PostgreSQL: Index with included columns
-- CREATE INDEX idx_employees_dept_salary
-- ON employees(department_id)
-- INCLUDE (first_name, last_name, salary);

-- This query uses index-only scan:
-- SELECT first_name, last_name, salary
-- FROM employees
-- WHERE department_id = 3;

-- SQL Server: Included columns
-- CREATE INDEX idx_employees_dept
-- ON employees(department_id)
-- INCLUDE (first_name, last_name, salary);

-- ============================================================================
-- 2. PARTIAL INDEXES (PostgreSQL)
-- ============================================================================

/*
   A partial index only includes rows that satisfy a WHERE clause.
   Smaller index = faster reads, less storage, less write overhead.

   Best for:
   - Queries that always filter on a status column
   - Soft-delete patterns (WHERE deleted_at IS NULL)
   - Active/inactive filtering
*/

-- Index only active orders
-- CREATE INDEX idx_active_orders
-- ON orders(customer_id, order_date)
-- WHERE status NOT IN ('cancelled', 'archived');

-- This query uses the partial index:
-- SELECT * FROM orders
-- WHERE customer_id = 42
--   AND status NOT IN ('cancelled', 'archived')
-- ORDER BY order_date;

-- This query does NOT use it:
-- SELECT * FROM orders WHERE customer_id = 42;

-- ============================================================================
-- 3. FUNCTIONAL / EXPRESSION INDEXES
-- ============================================================================

/*
   Indexes on expressions or function results.
   Useful when queries use functions on columns.

   PostgreSQL: CREATE INDEX ON table (function(column))
   SQL Server: CREATE INDEX ON table (computed_column)
   MySQL:      CREATE INDEX ON table ((expression)) (8.0.13+)
*/

-- PostgreSQL: Index on lowercase email
-- CREATE INDEX idx_employees_email_lower
-- ON employees(LOWER(email));

-- This query uses the index:
-- SELECT * FROM employees WHERE LOWER(email) = 'alice@company.com';

-- PostgreSQL: Index on date part
-- CREATE INDEX idx_orders_year_month
-- ON orders(EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date));

-- This query uses the index:
-- SELECT * FROM orders
-- WHERE EXTRACT(YEAR FROM order_date) = 2024
--   AND EXTRACT(MONTH FROM order_date) = 1;

-- ============================================================================
-- 4. CLUSTERED vs NON-CLUSTERED INDEXES
-- ============================================================================

/*
   Clustered Index:
   - Determines the physical order of data in the table
   - One per table (data is stored in index order)
   - Primary key is clustered by default in MySQL/SQL Server
   - PostgreSQL does NOT use clustered indexes (uses heap)

   Non-Clustered Index:
   - Separate structure from the data
   - Multiple per table
   - Contains pointers to the actual data rows
   - Default index type in all databases
*/

-- SQL Server: Create clustered index
-- CREATE CLUSTERED INDEX idx_orders_order_date
-- ON orders(order_date);

-- MySQL: Primary key is always clustered
-- CREATE TABLE users (
--     id INT PRIMARY KEY,  -- clustered
--     name VARCHAR(100)
-- );

-- ============================================================================
-- 5. INDEX MAINTENANCE
-- ============================================================================

/*
   Over time, indexes become fragmented:
   - Pages become partially empty (after deletes)
   - Logical order differs from physical order (after updates)
   - Index depth increases

   Rebuild: Creates new index from scratch (more thorough)
   Reorganize: Defragments leaf level (lighter operation)
*/

-- PostgreSQL:
-- REINDEX INDEX idx_name;                    -- rebuild
-- REINDEX TABLE table_name;                  -- rebuild all indexes
-- REINDEX TABLE CONCURRENTLY table_name;     -- non-blocking (PG 12+)

-- SQL Server:
-- ALTER INDEX idx_name ON table_name REBUILD;
-- ALTER INDEX idx_name ON table_name REORGANIZE;

-- MySQL:
-- OPTIMIZE TABLE table_name;  -- rebuilds indexes + reclaims space

-- ============================================================================
-- 6. INDEX USAGE STATISTICS
-- ============================================================================

-- PostgreSQL: Check index usage
-- SELECT
--     schemaname,
--     tablename,
--     indexname,
--     idx_scan,        -- number of index scans
--     idx_tup_read,    -- tuples read from index
--     idx_tup_fetch    -- tuples fetched from table
-- FROM pg_stat_user_indexes
-- ORDER BY idx_scan;

-- Find unused indexes (no scans):
-- SELECT schemaname, tablename, indexname, idx_scan
-- FROM pg_stat_user_indexes
-- WHERE idx_scan = 0
-- ORDER BY tablename;

-- ============================================================================
-- 7. INDEX SELECTIVITY
-- ============================================================================

/*
   Selectivity = number of distinct values / total rows
   High selectivity (close to 1): good for indexing (e.g., email)
   Low selectivity (close to 0): bad for indexing (e.g., gender)

   Rule of thumb: index columns with high selectivity first
   in composite indexes.
*/

-- ============================================================================
-- 8. ADVANCED INDEX BEST PRACTICES
-- ============================================================================

/*
   1. Use covering indexes for critical, frequent queries
   2. Use partial indexes for filtered queries (PostgreSQL)
   3. Use expression indexes for function-based queries
   4. Monitor index usage and remove unused indexes
   5. Schedule regular index maintenance
   6. Consider index size vs performance benefit
   7. Test index changes with realistic data volumes
   8. Use CREATE INDEX CONCURRENTLY for zero-downtime changes
   9. Be aware of index impact on write performance
   10. Document why each index exists (purpose, queries it serves)
*/

-- ============================================================================
-- END OF 20_advanced_indexing.sql
-- ============================================================================
