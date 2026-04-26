/*
   INDEXES & PERFORMANCE BASICS - Query Plans, Index Types
   File: 11_indexes_performance.sql

   Indexes are the primary tool for improving query performance.
   This file covers index fundamentals and how to read query plans.
*/

-- ============================================================================
-- 1. WHAT IS AN INDEX?
-- ============================================================================

/*
   An index is a data structure (usually a B-tree) that improves
   the speed of data retrieval operations on a table.

   Analogy: The index at the back of a book.
   - Without index: scan every page to find what you need (full table scan)
   - With index: look up the term, go directly to the page (index scan)

   Trade-off: Indexes speed up SELECT but slow down INSERT/UPDATE/DELETE
   (because the index must be maintained on every write).
*/

-- ============================================================================
-- 2. B-TREE INDEX (Default)
-- ============================================================================

/*
   B-tree (Balanced Tree) is the default index type in all major databases.
   Efficient for:
   - Equality: WHERE id = 42
   - Range:    WHERE price BETWEEN 10 AND 50
   - Prefix:   WHERE name LIKE 'Smith%'
   - Sorting:  ORDER BY name
   - Joins:    ON a.id = b.fk

   Not efficient for:
   - Wildcard at start: WHERE name LIKE '%smith'
   - Functions on column: WHERE YEAR(date) = 2024
*/

-- CREATE INDEX idx_employees_last_name ON employees(last_name);
-- CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- ============================================================================
-- 3. COMPOSITE (MULTI-COLUMN) INDEXES
-- ============================================================================

/*
   A composite index covers multiple columns.
   Column order matters significantly!

   Rule: Leftmost prefix rule
   An index on (A, B, C) can efficiently support:
   - WHERE conditions on A
   - WHERE conditions on A AND B
   - WHERE conditions on A AND B AND C
   - ORDER BY A, B, C

   It CANNOT efficiently support:
   - WHERE conditions on B alone
   - WHERE conditions on C alone
   - WHERE conditions on B AND C
*/

-- Good for queries filtering by department AND salary
-- CREATE INDEX idx_dept_salary ON employees(department_id, salary);

-- This index helps:
-- SELECT * FROM employees WHERE department_id = 3 AND salary > 50000;
-- SELECT * FROM employees WHERE department_id = 3 ORDER BY salary;

-- This index does NOT help (department_id is missing):
-- SELECT * FROM employees WHERE salary > 50000;

-- ============================================================================
-- 4. UNIQUE INDEX
-- ============================================================================

/*
   Ensures all values in the indexed column(s) are unique.
   Automatically created when you define a UNIQUE or PRIMARY KEY constraint.
*/

-- CREATE UNIQUE INDEX idx_employees_email ON employees(email);

-- ============================================================================
-- 5. PARTIAL INDEX (PostgreSQL)
-- ============================================================================

/*
   A partial index only includes rows that satisfy a WHERE condition.
   Smaller index = faster reads and writes.
*/

-- Only index active employees (smaller index)
-- CREATE INDEX idx_active_employees ON employees(last_name)
-- WHERE is_active = TRUE;

-- This query uses the partial index:
-- SELECT * FROM employees WHERE is_active = TRUE AND last_name = 'Smith';

-- This query does NOT use it:
-- SELECT * FROM employees WHERE last_name = 'Smith';

-- ============================================================================
-- 6. COVERING INDEX (Index-Only Scan)
-- ============================================================================

/*
   A covering index contains ALL columns needed by a query.
   The database can answer the query entirely from the index,
   without touching the table at all (index-only scan).
*/

-- If queries only need these columns:
-- CREATE INDEX idx_covering ON employees(department_id, salary, last_name);

-- This query can be answered from the index alone:
-- SELECT last_name, salary FROM employees WHERE department_id = 3;

-- ============================================================================
-- 7. EXPLAIN - Reading Query Plans
-- ============================================================================

/*
   EXPLAIN shows how the database plans to execute a query.
   EXPLAIN ANALYZE actually runs the query and shows actual timings.

   Key terms in query plans:
   - Seq Scan: Full table scan (bad for large tables)
   - Index Scan: Uses index to find rows (good)
   - Index Only Scan: All data from index (excellent)
   - Bitmap Scan: Combines multiple indexes (good for many matches)
   - Nested Loop: For each row in A, scan B (good for small result sets)
   - Hash Join: Build hash table of A, probe with B (good for medium sets)
   - Merge Join: Sort both, merge (good for large sorted sets)
*/

-- EXPLAIN ANALYZE SELECT * FROM employees WHERE last_name = 'Smith';
-- EXPLAIN ANALYZE SELECT * FROM employees WHERE department_id = 3;

-- ============================================================================
-- 8. WHEN INDEXES ARE NOT USED
-- ============================================================================

/*
   An index may not be used when:
   1. The table is very small (seq scan is cheaper)
   2. The query returns a large percentage of rows (>5-10%)
   3. Functions are applied to the indexed column
   4. Data type mismatch (implicit conversion)
   5. Leading wildcard in LIKE: '%smith'
   6. OR conditions (may use bitmap scan instead)
*/

-- Index NOT used (function on column):
-- SELECT * FROM employees WHERE UPPER(last_name) = 'SMITH';

-- Index used (sargable):
-- SELECT * FROM employees WHERE last_name = 'Smith';

-- ============================================================================
-- 9. INDEX MAINTENANCE
-- ============================================================================

/*
   Over time, indexes can become fragmented.
   Regular maintenance keeps them efficient.

   PostgreSQL:
   - REINDEX INDEX idx_name;
   - REINDEX TABLE table_name;

   SQL Server:
   - ALTER INDEX idx_name ON table_name REBUILD;
   - ALTER INDEX idx_name ON table_name REORGANIZE;

   MySQL:
   - OPTIMIZE TABLE table_name;
*/

-- ============================================================================
-- 10. INDEX BEST PRACTICES
-- ============================================================================

/*
   1. Index columns used in WHERE, JOIN, and ORDER BY
   2. Index foreign key columns (they're used in JOINs)
   3. Prefer composite indexes over multiple single-column indexes
   4. Put high-selectivity columns first in composite indexes
   5. Don't over-index: each index slows writes
   6. Monitor unused indexes and remove them
   7. Consider partial indexes for filtered queries
   8. Use covering indexes for critical queries
   9. Test with EXPLAIN ANALYZE before and after
   10. Rebuild indexes periodically based on write volume
*/

-- ============================================================================
-- END OF 11_indexes_performance.sql
-- ============================================================================
