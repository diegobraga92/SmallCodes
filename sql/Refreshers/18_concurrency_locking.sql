/*
   CONCURRENCY & LOCKING - Lock Types, Deadlocks, MVCC
   File: 18_concurrency_locking.sql

   When multiple users access the database simultaneously,
   locking mechanisms prevent data corruption while maximizing
   concurrency.
*/

-- ============================================================================
-- 1. MVCC (Multi-Version Concurrency Control)
-- ============================================================================

/*
   MVCC is used by PostgreSQL, Oracle, MySQL (InnoDB), and SQLite.
   Each transaction sees a snapshot of data as of a point in time.
   Readers never block writers, and writers never block readers.

   How it works:
   - Each row has hidden version metadata
   - When a row is updated, a new version is created
   - Old versions are kept for transactions that need them
   - Old versions are cleaned up by VACUUM (PostgreSQL) or purge (MySQL)

   Benefits:
   - High concurrency (reads don't block writes)
   - Consistent snapshots per transaction
   - No read locks needed
*/

-- ============================================================================
-- 2. LOCK TYPES
-- ============================================================================

/*
   Row-level locks:
   - Most granular, best concurrency
   - Used by InnoDB (MySQL), PostgreSQL, SQL Server
   - Types: shared (read) and exclusive (write)

   Page-level locks:
   - Locks a page of data (multiple rows)
   - Used by older MySQL storage engines

   Table-level locks:
   - Locks entire table
   - Used by MyISAM (MySQL), during DDL operations
   - Simple but poor concurrency
*/

-- ============================================================================
-- 3. EXPLICIT LOCKING
-- ============================================================================

-- Row-level lock (PostgreSQL):
-- BEGIN;
-- SELECT * FROM accounts WHERE id = 1 FOR UPDATE;  -- exclusive lock
-- UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- COMMIT;

-- Row-level lock with SKIP LOCKED (PostgreSQL 9.5+):
-- Useful for job queues: skip rows locked by other transactions
-- BEGIN;
-- SELECT * FROM jobs WHERE status = 'pending'
-- ORDER BY created_at
-- LIMIT 1
-- FOR UPDATE SKIP LOCKED;
-- -- Process the job...
-- COMMIT;

-- Shared lock (SQL Server):
-- BEGIN TRANSACTION;
-- SELECT * FROM accounts WITH (HOLDLOCK) WHERE id = 1;
-- -- Other transactions can read but not update
-- COMMIT;

-- Table-level lock (MySQL):
-- LOCK TABLES employees READ;   -- shared lock
-- LOCK TABLES employees WRITE;  -- exclusive lock
-- UNLOCK TABLES;

-- ============================================================================
-- 4. LOCK MONITORING
-- ============================================================================

-- PostgreSQL: View current locks
-- SELECT
--     pid,
--     locktype,
--     relation::regclass AS table_name,
--     mode,
--     granted,
--     query
-- FROM pg_locks
-- JOIN pg_stat_activity USING (pid)
-- WHERE NOT pid = pg_backend_pid();

-- MySQL: View current locks
-- SHOW OPEN TABLES WHERE In_use > 0;
-- SELECT * FROM information_schema.INNODB_LOCKS;
-- SELECT * FROM information_schema.INNODB_LOCK_WAITS;

-- SQL Server: View current locks
-- SELECT * FROM sys.dm_tran_locks;
-- SELECT * FROM sys.dm_exec_requests WHERE blocking_session_id > 0;

-- ============================================================================
-- 5. DEADLOCK DETECTION AND PREVENTION
-- ============================================================================

/*
   Deadlock: Transaction A waits for B, B waits for A (circular wait).

   Database deadlock detection:
   - PostgreSQL: detects deadlocks and aborts one transaction
   - MySQL: detects deadlocks and rolls back the smallest transaction
   - SQL Server: detects deadlocks and chooses a victim

   Prevention strategies:
   1. Access tables in the same order across all transactions
   2. Keep transactions short
   3. Use appropriate isolation levels
   4. Use indexes to reduce lock ranges
   5. Consider optimistic locking for low-contention scenarios
*/

-- ============================================================================
-- 6. OPTIMISTIC vs PESSIMISTIC LOCKING
-- ============================================================================

/*
   Pessimistic Locking:
   - Lock the row when you read it (SELECT FOR UPDATE)
   - Prevents conflicts before they happen
   - Best for high-contention scenarios
   - Can reduce concurrency

   Optimistic Locking:
   - Don't lock when reading
   - Check for conflicts before writing (version column)
   - Best for low-contention scenarios
   - Requires retry logic on conflict
*/

-- Optimistic locking with version column:
-- CREATE TABLE accounts (
--     id INT PRIMARY KEY,
--     balance DECIMAL(10,2),
--     version INT DEFAULT 1
-- );

-- Application code pattern:
-- BEGIN;
-- SELECT balance, version FROM accounts WHERE id = 1;
-- -- version = 5
-- UPDATE accounts
-- SET balance = balance - 100, version = version + 1
-- WHERE id = 1 AND version = 5;
-- -- If affected rows = 0, another transaction modified it
-- -- Retry the entire operation
-- COMMIT;

-- ============================================================================
-- 7. LOCK ESCALATION
-- ============================================================================

/*
   Lock escalation: database converts many row locks into a table lock.
   Happens when a transaction locks more rows than a threshold.

   SQL Server: escalates at 5,000 locks
   MySQL: no escalation (row locks remain row locks)
   PostgreSQL: no escalation

   To prevent escalation:
   - Process rows in smaller batches
   - Ensure indexes are used (reduces lock range)
   - Consider partitioning large tables
*/

-- ============================================================================
-- 8. CONCURRENCY BEST PRACTICES
-- ============================================================================

/*
   1. Keep transactions as short as possible
   2. Access resources in a consistent order
   3. Use SELECT FOR UPDATE only when necessary
   4. Consider optimistic locking for read-heavy workloads
   5. Monitor for long-running transactions and deadlocks
   6. Use appropriate isolation levels (not always SERIALIZABLE)
   7. Implement retry logic for deadlock victims
   8. Use SKIP LOCKED for job queues (PostgreSQL)
   9. Ensure proper indexing to minimize lock ranges
   10. Test concurrency behavior under load
*/

-- ============================================================================
-- END OF 18_concurrency_locking.sql
-- ============================================================================
