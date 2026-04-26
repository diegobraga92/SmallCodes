/* ============================================================================
   SQL COMPREHENSIVE REVIEW
   File: _sql_review.sql
   Covers: Quick reference for all SQL topics, common patterns,
           dialect notes, debugging tips, anti-patterns
   ============================================================================ */

/* ============================================================================
   1. SQL STATEMENT CATEGORIES
   ============================================================================ */

/*
   DDL (Data Definition Language)   | CREATE, ALTER, DROP, TRUNCATE, RENAME
   DML (Data Manipulation Language) | SELECT, INSERT, UPDATE, DELETE, MERGE
   DCL (Data Control Language)      | GRANT, REVOKE
   TCL (Transaction Control Lang.)  | BEGIN, COMMIT, ROLLBACK, SAVEPOINT
*/

/* ============================================================================
   2. QUERY EXECUTION ORDER (Logical)
   ============================================================================ */

/*
   FROM/JOIN  →  WHERE  →  GROUP BY  →  HAVING  →  WINDOW  →  SELECT  →  DISTINCT  →  UNION  →  ORDER BY  →  LIMIT/OFFSET
      1           2           3           4          5          6           7          8          9            10

   KEY INSIGHT: Column aliases defined in SELECT (step 6) cannot be used in WHERE (step 2)
                or GROUP BY (step 3). They CAN be used in ORDER BY (step 9) and HAVING (step 4 in some DBs).
*/

/* ============================================================================
   3. COMMON ANTI-PATTERNS
   ============================================================================ */

/*
   ANTI-PATTERN                    | WHY IT'S BAD                          | BETTER APPROACH
   --------------------------------|---------------------------------------|------------------------------------------
   SELECT *                        | Returns unnecessary columns, breaks   | List columns explicitly
                                     | indexes, fragile to schema changes   |
   Non-sargable predicates         | WHERE YEAR(date) = 2024               | WHERE date >= '2024-01-01'
                                     | prevents index usage                 |   AND date < '2025-01-01'
   Implicit type conversion        | WHERE id = '42' (string vs int)       | WHERE id = 42
                                     | skips index                          |
   N+1 queries in loops            | Query inside loop = perf disaster     | JOIN or subquery
   No LIMIT on large queries       | Returns millions of rows              | Always LIMIT unless you need all
   Missing WHERE on UPDATE/DELETE  | Updates/deletes entire table          | Always verify WHERE first
   Over-indexing                   | Slows writes, wastes space            | Index based on query patterns
   Using functions on indexed cols | WHERE UPPER(name) = 'ALICE'          | WHERE name = 'Alice' (case-insensitive collation)
*/

/* ============================================================================
   4. DIALECT DIFFERENCES (Quick Reference)
   ============================================================================ */

/*
   FEATURE              | PostgreSQL        | MySQL             | SQL Server        | SQLite
   ---------------------|-------------------|-------------------|-------------------|-------------------
   Auto-increment       | SERIAL / IDENTITY | AUTO_INCREMENT    | IDENTITY(1,1)     | AUTOINCREMENT
   String concat        | ||                | CONCAT()          | + or CONCAT()     | ||
   LIMIT                | LIMIT n OFFSET m  | LIMIT n OFFSET m  | OFFSET m ROWS     | LIMIT n OFFSET m
                                                  |                   | FETCH NEXT n ONLY |
   ILIKE (case-insens.) | ILIKE             | LIKE (ci by def)  | LIKE (ci by def)  | LIKE (ci by def)
   UPSERT               | ON CONFLICT DO    | ON DUPLICATE KEY  | MERGE             | ON CONFLICT DO
                        | UPDATE SET        | UPDATE            |                   | UPDATE SET
   JSON support         | Native (excellent)| JSON/JSONB        | OPENJSON          | JSON functions
   Full-text search     | tsvector/tsquery  | FULLTEXT index    | FULLTEXT index    | FTS5 extension
   Recursive CTE        | WITH RECURSIVE    | WITH RECURSIVE    | WITH (recursive)  | WITH RECURSIVE
   Window functions     | Full support      | 8.0+ support      | Full support      | 3.25+ support
*/

/* ============================================================================
   5. PERFORMANCE TUNING CHECKLIST
   ============================================================================ */

/*
   ☐ Check query plan (EXPLAIN ANALYZE)
   ☐ Are there appropriate indexes? (check seq scans)
   ☐ Are predicates sargable? (no functions on indexed columns)
   ☐ Is the join order optimal? (smallest result set first)
   ☐ Are statistics up to date? (ANALYZE)
   ☐ Is the query returning more rows than needed? (LIMIT?)
   ☐ Are there unnecessary columns in SELECT?
   ☐ Is N+1 happening? (suboptimal ORM usage)
   ☐ Are composite indexes in the right column order?
   ☐ Is the connection pool sized correctly?
   ☐ Are transactions kept short?
   ☐ Is there index fragmentation? (rebuild/reorg)
*/

/* ============================================================================
   6. COMMON GOTCHAS
   ============================================================================ */

/*
   - NULL != NULL (use IS NULL, not = NULL)
   - NULL in boolean expressions: NULL AND TRUE = NULL (not FALSE)
   - NULL in aggregates: COUNT(col) excludes NULLs, COUNT(*) includes them
   - String comparison is case-sensitive or not depending on collation
   - Floating-point equality is unreliable (use ABS(a - b) < epsilon)
   - ORDER BY with NULLs: NULLS FIRST vs NULLS LAST (varies by DB)
   - JOIN without ON = CROSS JOIN (cartesian product)
   - GROUP BY all non-aggregated columns (or use ANY_VALUE in some DBs)
   - TRUNCATE cannot be rolled back in some DBs (DDL, not DML)
   - AUTOCOMMIT behavior varies by client/driver
*/

/* ============================================================================
   7. USEFUL SYSTEM QUERIES
   ============================================================================ */

-- PostgreSQL: List all tables
-- \dt
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- MySQL: List all tables
-- SHOW TABLES;
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'database_name';

-- SQL Server: List all tables
-- SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';

-- SQLite: List all tables
-- .tables
-- SELECT name FROM sqlite_master WHERE type='table';

-- Check running queries (PostgreSQL)
-- SELECT pid, query, state, wait_event FROM pg_stat_activity;

-- Check slow queries (PostgreSQL)
-- SELECT query, calls, total_time, mean_time FROM pg_stat_statements ORDER BY mean_time DESC;

-- Find unused indexes (PostgreSQL)
-- SELECT schemaname, tablename, indexname, idx_scan FROM pg_stat_user_indexes WHERE idx_scan = 0;

/* ============================================================================
   8. QUICK SYNTAX REFERENCE
   ============================================================================ */

-- SELECT
-- SELECT col1, col2 FROM table WHERE condition GROUP BY col HAVING cond ORDER BY col LIMIT n;

-- JOIN
-- SELECT * FROM a INNER JOIN b ON a.id = b.fk;

-- INSERT
-- INSERT INTO table (col1, col2) VALUES (v1, v2);
-- INSERT INTO table (col1, col2) SELECT col1, col2 FROM other_table;

-- UPDATE
-- UPDATE table SET col1 = v1 WHERE condition;

-- DELETE
-- DELETE FROM table WHERE condition;

-- CREATE TABLE
-- CREATE TABLE t (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL);

-- CREATE INDEX
-- CREATE INDEX idx_name ON table (col1, col2);

-- CTE
-- WITH cte AS (SELECT ...) SELECT * FROM cte;

-- Window function
-- SELECT col, ROW_NUMBER() OVER (PARTITION BY group_col ORDER BY sort_col) AS rn FROM table;

-- Transaction
-- BEGIN; UPDATE ...; DELETE ...; COMMIT; -- or ROLLBACK;
