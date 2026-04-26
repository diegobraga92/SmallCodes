/*
   STORED PROCEDURES - Procedural Logic in the Database
   File: 14_stored_procedures.sql

   Stored procedures allow you to write procedural code (loops,
   conditionals, error handling) that runs inside the database.
   Syntax varies significantly between databases.
*/

-- ============================================================================
-- 1. WHAT ARE STORED PROCEDURES?
-- ============================================================================

/*
   Benefits:
   - Encapsulate business logic close to the data
   - Reduce network round-trips (multiple operations in one call)
   - Reusable across applications
   - Enhanced security (users can execute without direct table access)
   - Consistent execution plan caching

   Drawbacks:
   - Database-specific (portability issues)
   - Harder to version control and test
   - Can hide complexity
   - Debugging is more difficult than application code
*/

-- ============================================================================
-- 2. BASIC PROCEDURE (PostgreSQL PL/pgSQL)
-- ============================================================================

-- CREATE OR REPLACE PROCEDURE get_employee_count(
--     IN dept_id INT,
--     OUT emp_count INT
-- )
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     SELECT COUNT(*) INTO emp_count
--     FROM employees
--     WHERE department_id = dept_id;
-- END;
-- $$;

-- Call the procedure:
-- CALL get_employee_count(1, NULL);

-- ============================================================================
-- 3. PROCEDURE WITH MULTIPLE OPERATIONS
-- ============================================================================

-- CREATE OR REPLACE PROCEDURE transfer_funds(
--     IN from_account INT,
--     IN to_account INT,
--     IN amount DECIMAL(10,2)
-- )
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     -- Start implicit transaction
--     UPDATE accounts SET balance = balance - amount WHERE id = from_account;
--     UPDATE accounts SET balance = balance + amount WHERE id = to_account;
--     -- Commit on success, rollback on error
-- END;
-- $$;

-- ============================================================================
-- 4. PROCEDURE WITH ERROR HANDLING
-- ============================================================================

-- CREATE OR REPLACE PROCEDURE safe_transfer(
--     IN from_account INT,
--     IN to_account INT,
--     IN amount DECIMAL(10,2)
-- )
-- LANGUAGE plpgsql
-- AS $$
-- DECLARE
--     current_balance DECIMAL(10,2);
-- BEGIN
--     -- Check balance
--     SELECT balance INTO current_balance
--     FROM accounts WHERE id = from_account;
--
--     IF current_balance < amount THEN
--         RAISE EXCEPTION 'Insufficient funds. Balance: %, Required: %',
--                         current_balance, amount;
--     END IF;
--
--     UPDATE accounts SET balance = balance - amount WHERE id = from_account;
--     UPDATE accounts SET balance = balance + amount WHERE id = to_account;
--
--     EXCEPTION
--         WHEN OTHERS THEN
--             RAISE NOTICE 'Transfer failed: %', SQLERRM;
--             RAISE;
-- END;
-- $$;

-- ============================================================================
-- 5. PROCEDURE WITH CURSOR (Row-by-Row Processing)
-- ============================================================================

-- CREATE OR REPLACE PROCEDURE apply_annual_bonus(
--     IN bonus_pct DECIMAL(5,2)
-- )
-- LANGUAGE plpgsql
-- AS $$
-- DECLARE
--     emp_record RECORD;
-- BEGIN
--     FOR emp_record IN
--         SELECT id, salary, performance_rating
--         FROM employees
--         WHERE is_active = TRUE
--     LOOP
--         UPDATE employees
--         SET salary = salary * (1 + bonus_pct / 100)
--         WHERE id = emp_record.id;
--     END LOOP;
-- END;
-- $$;

-- ============================================================================
-- 6. SQL SERVER PROCEDURE
-- ============================================================================

-- CREATE PROCEDURE GetEmployeesByDepartment
--     @DeptId INT,
--     @MinSalary DECIMAL(10,2) = 0
-- AS
-- BEGIN
--     SET NOCOUNT ON;
--
--     SELECT employee_id, first_name, last_name, salary
--     FROM employees
--     WHERE department_id = @DeptId
--       AND salary >= @MinSalary
--     ORDER BY salary DESC;
-- END;
-- GO
--
-- EXEC GetEmployeesByDepartment @DeptId = 1, @MinSalary = 50000;

-- ============================================================================
-- 7. MySQL PROCEDURE
-- ============================================================================

-- DELIMITER //
--
-- CREATE PROCEDURE GetDepartmentStats(IN dept_id INT)
-- BEGIN
--     SELECT
--         COUNT(*) AS emp_count,
--         AVG(salary) AS avg_salary,
--         MAX(salary) AS max_salary
--     FROM employees
--     WHERE department_id = dept_id;
-- END //
--
-- DELIMITER ;
--
-- CALL GetDepartmentStats(1);

-- ============================================================================
-- 8. PROCEDURE vs FUNCTION
-- ============================================================================

/*
   PROCEDURE                          | FUNCTION
   -----------------------------------|-----------------------------------
   Can have IN, OUT, INOUT parameters | Only IN parameters
   Cannot be used in SELECT           | Can be used in SELECT, WHERE, etc.
   Can call other procedures          | Can call other functions
   Can modify data (INSERT/UPDATE)    | Should be read-only (ideally)
   Cannot return a value              | Must return a value
   Supports transactions              | Runs within parent transaction
   CALL procedure()                   | SELECT function()
*/

-- ============================================================================
-- 9. BEST PRACTICES
-- ============================================================================

/*
   1. Keep procedures focused on a single task
   2. Use meaningful parameter names
   3. Always handle errors and edge cases
   4. Document expected behavior in comments
   5. Avoid dynamic SQL when possible (SQL injection risk)
   6. Test with both valid and invalid inputs
   7. Monitor procedure performance (long-running procedures)
   8. Consider set-based operations over row-by-row (cursor) processing
   9. Version control your procedures alongside application code
   10. Use transactions explicitly for multi-step operations
*/

-- ============================================================================
-- END OF 14_stored_procedures.sql
-- ============================================================================
