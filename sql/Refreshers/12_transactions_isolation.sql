/*
   TRANSACTIONS & ISOLATION LEVELS - ACID, Concurrency Control
   File: 12_transactions_isolation.sql

   Transactions group multiple operations into a single unit of work.
   Isolation levels control how transactions interact with each other.
*/

-- ============================================================================
-- 1. ACID PROPERTIES
-- ============================================================================

/*
   A - Atomicity: All operations complete, or none do (all-or-nothing)
   C - Consistency: Transaction brings database from one valid state to another
   I - Isolation: Concurrent transactions don't interfere with each other
   D - Durability: Committed changes persist even after system failure
*/

-- ============================================================================
-- 2. BASIC TRANSACTION SYNTAX
-- ============================================================================

-- BEGIN;
-- UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
-- COMMIT;

-- If something goes wrong:
-- BEGIN;
-- UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- -- Oops, system crash or error detected
-- ROLLBACK;  -- Undo the partial update

-- ============================================================================
-- 3. SAVEPOINTS
-- ============================================================================

/*
   Savepoints allow partial rollback within a transaction.
   You can roll back to a savepoint without aborting the entire transaction.
*/

-- BEGIN;
-- UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- SAVEPOINT after_debit;
--
-- UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
-- -- Something went wrong with the credit
-- ROLLBACK TO SAVEPOINT after_debit;
--
-- -- Try a different approach
-- UPDATE accounts SET balance = balance + 100 WHERE account_id = 3;
-- COMMIT;

-- ============================================================================
-- 4. ISOLATION LEVELS
-- ============================================================================

/*
   From lowest to highest isolation:

   Level                    | Dirty Read | Non-Repeatable Read | Phantom Read
   -------------------------|------------|---------------------|-------------
   READ UNCOMMITTED         | Possible   | Possible            | Possible
   READ COMMITTED           | Safe       | Possible            | Possible
   REPEATABLE READ          | Safe       | Safe                | Possible
   SERIALIZABLE             | Safe       | Safe                | Safe

   Dirty Read:        Read uncommitted changes from another transaction
   Non-Repeatable Read: Same query returns different results in same transaction
   Phantom Read:      New rows appear that match a WHERE condition in same transaction
*/

-- ============================================================================
-- 5. READ UNCOMMITTED
-- ============================================================================

/*
   Lowest isolation level.
   Can read data modified by other transactions before they commit.
   Rarely used in practice due to dirty read risk.
*/

-- SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
-- BEGIN;
-- SELECT balance FROM accounts WHERE account_id = 1;
-- -- May see uncommitted changes from other transactions!
-- COMMIT;

-- ============================================================================
-- 6. READ COMMITTED (Default in PostgreSQL, SQL Server, Oracle)
-- ============================================================================

/*
   Each query sees only committed data.
   Prevents dirty reads.
   Default in most databases.

   Non-repeatable reads are possible:
   Two SELECTs in the same transaction may see different data
   if another transaction commits between them.
*/

-- SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
-- BEGIN;
-- SELECT balance FROM accounts WHERE account_id = 1;  -- sees 1000
-- -- Another transaction updates balance to 900 and commits
-- SELECT balance FROM accounts WHERE account_id = 1;  -- sees 900 (different!)
-- COMMIT;

-- ============================================================================
-- 7. REPEATABLE READ
-- ============================================================================

/*
   Guarantees that if you read a row twice, you see the same data.
   Prevents dirty reads and non-repeatable reads.
   Default in MySQL.

   Phantom reads are still possible:
   New rows matching the WHERE clause can appear.
*/

-- SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
-- BEGIN;
-- SELECT * FROM orders WHERE customer_id = 1;  -- sees 5 orders
-- -- Another transaction inserts a new order for customer 1 and commits
-- SELECT * FROM orders WHERE customer_id = 1;  -- still sees 5 orders (repeatable)
-- -- But a new query with different conditions might see phantoms
-- COMMIT;

-- ============================================================================
-- 8. SERIALIZABLE
-- ============================================================================

/*
   Highest isolation level.
   Transactions execute as if they ran one after another (serially).
   Prevents all concurrency anomalies.
   Can cause more transaction failures (retry logic needed).
*/

-- SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- BEGIN;
-- -- All operations are completely isolated
-- UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
-- UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
-- COMMIT;

-- ============================================================================
-- 9. SETTING ISOLATION LEVEL (Database-Specific)
-- ============================================================================

/*
   PostgreSQL:
   SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
   (Can only be set at the start of a transaction)

   MySQL:
   SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
   SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

   SQL Server:
   SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

   SQLite:
   Only supports SERIALIZABLE (default) and READ UNCOMMITTED
*/

-- ============================================================================
-- 10. DEADLOCKS
-- ============================================================================

/*
   A deadlock occurs when two transactions each hold a lock
   that the other needs.

   Transaction A:                    Transaction B:
   UPDATE accounts SET ... WHERE id=1;  UPDATE accounts SET ... WHERE id=2;
   UPDATE accounts SET ... WHERE id=2;  UPDATE accounts SET ... WHERE id=1;
   -- DEADLOCK!                       -- DEADLOCK!

   Prevention:
   - Access resources in the same order (always update id=1 before id=2)
   - Keep transactions short
   - Use appropriate isolation levels
   - Implement retry logic for deadlock victims
*/

-- ============================================================================
-- 11. TRANSACTION BEST PRACTICES
-- ============================================================================

/*
   1. Keep transactions as short as possible
   2. Don't wait for user input inside a transaction
   3. Access resources in a consistent order to prevent deadlocks
   4. Use the lowest isolation level that meets your requirements
   5. Always handle transaction failures with retry logic
   6. Be aware of auto-commit behavior (varies by client/driver)
   7. Monitor for long-running transactions
   8. Use SET lock_timeout to prevent indefinite waits
*/

-- ============================================================================
-- END OF 12_transactions_isolation.sql
-- ============================================================================
