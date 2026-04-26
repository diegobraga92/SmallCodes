/*
   FUNCTIONS & TRIGGERS - User-Defined Functions and Automatic Actions
   File: 15_functions_triggers.sql

   Functions return values and can be used in queries.
   Triggers automatically execute code in response to data changes.
*/

-- ============================================================================
-- 1. SCALAR FUNCTIONS (Return Single Value)
-- ============================================================================

-- PostgreSQL: Calculate full name
-- CREATE OR REPLACE FUNCTION get_full_name(
--     p_first_name VARCHAR,
--     p_last_name VARCHAR
-- )
-- RETURNS VARCHAR
-- LANGUAGE plpgsql
-- IMMUTABLE  -- Same inputs always produce same output
-- AS $$
-- BEGIN
--     RETURN p_first_name || ' ' || p_last_name;
-- END;
-- $$;

-- Usage:
-- SELECT get_full_name('John', 'Doe');  -- Returns 'John Doe'
-- SELECT id, get_full_name(first_name, last_name) AS full_name FROM employees;

-- ============================================================================
-- 2. TABLE FUNCTIONS (Return Result Set)
-- ============================================================================

-- PostgreSQL: Return employees in a department
-- CREATE OR REPLACE FUNCTION get_dept_employees(
--     p_dept_id INT
-- )
-- RETURNS TABLE (
--     employee_id INT,
--     full_name VARCHAR,
--     salary DECIMAL(10,2)
-- )
-- LANGUAGE plpgsql
-- STABLE
-- AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT
--         e.employee_id,
--         e.first_name || ' ' || e.last_name,
--         e.salary
--     FROM employees e
--     WHERE e.department_id = p_dept_id
--     ORDER BY e.last_name;
-- END;
-- $$;

-- Usage:
-- SELECT * FROM get_dept_employees(1);

-- ============================================================================
-- 3. DETERMINISTIC vs NON-DETERMINISTIC
-- ============================================================================

/*
   IMMUTABLE:  Always returns same result for same inputs (can be optimized)
               Example: full name, tax calculation
   STABLE:     Same result within a single query execution
               Example: current user, querying other tables
   VOLATILE:   Can return different results each call
               Example: random(), now(), nextval()
*/

-- ============================================================================
-- 4. TRIGGER BASICS
-- ============================================================================

/*
   A trigger automatically executes a function when a specified event occurs.

   Trigger events: INSERT, UPDATE, DELETE (or a combination)
   Trigger timing: BEFORE, AFTER, INSTEAD OF
   Trigger level:  ROW level (once per row) or STATEMENT level (once per statement)

   Use cases:
   - Audit logging (track who changed what and when)
   - Validation (enforce complex business rules)
   - Derived data (update summary tables)
   - Cascading actions
*/

-- ============================================================================
-- 5. AUDIT TRIGGER (PostgreSQL)
-- ============================================================================

-- First, create the audit table
-- CREATE TABLE employee_audit (
--     audit_id SERIAL PRIMARY KEY,
--     employee_id INT,
--     old_salary DECIMAL(10,2),
--     new_salary DECIMAL(10,2),
--     changed_by VARCHAR(100),
--     changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Create the trigger function
-- CREATE OR REPLACE FUNCTION audit_salary_change()
-- RETURNS TRIGGER
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     IF OLD.salary IS DISTINCT FROM NEW.salary THEN
--         INSERT INTO employee_audit (
--             employee_id, old_salary, new_salary, changed_by
--         ) VALUES (
--             NEW.employee_id,
--             OLD.salary,
--             NEW.salary,
--             CURRENT_USER
--         );
--     END IF;
--     RETURN NEW;
-- END;
-- $$;

-- Attach the trigger
-- CREATE TRIGGER trg_audit_salary
-- AFTER UPDATE OF salary ON employees
-- FOR EACH ROW
-- EXECUTE FUNCTION audit_salary_change();

-- ============================================================================
-- 6. VALIDATION TRIGGER
-- ============================================================================

-- CREATE OR REPLACE FUNCTION validate_employee_insert()
-- RETURNS TRIGGER
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     -- Ensure salary is positive
--     IF NEW.salary <= 0 THEN
--         RAISE EXCEPTION 'Salary must be positive. Got: %', NEW.salary;
--     END IF;
--
--     -- Ensure email is not empty
--     IF NEW.email IS NULL OR NEW.email = '' THEN
--         RAISE EXCEPTION 'Email is required';
--     END IF;
--
--     RETURN NEW;
-- END;
-- $$;

-- CREATE TRIGGER trg_validate_employee
-- BEFORE INSERT ON employees
-- FOR EACH ROW
-- EXECUTE FUNCTION validate_employee_insert();

-- ============================================================================
-- 7. INSTEAD OF TRIGGER (for Views)
-- ============================================================================

/*
   INSTEAD OF triggers allow INSERT/UPDATE/DELETE on views.
   Useful for making complex views updatable.
*/

-- CREATE OR REPLACE FUNCTION insert_employee_via_view()
-- RETURNS TRIGGER
-- LANGUAGE plpgsql
-- AS $$
-- BEGIN
--     INSERT INTO employees (first_name, last_name, email, department_id)
--     VALUES (NEW.first_name, NEW.last_name, NEW.email, NEW.department_id);
--     RETURN NEW;
-- END;
-- $$;

-- CREATE TRIGGER trg_insert_employee_view
-- INSTEAD OF INSERT ON employee_summary_view
-- FOR EACH ROW
-- EXECUTE FUNCTION insert_employee_via_view();

-- ============================================================================
-- 8. TRIGGER BEST PRACTICES
-- ============================================================================

/*
   1. Keep trigger logic simple and fast (they run in the same transaction)
   2. Avoid triggers that call other triggers (cascading triggers)
   3. Be aware of trigger overhead on write operations
   4. Document what each trigger does and why
   5. Test triggers thoroughly (they affect ALL writes to the table)
   6. Consider using application-level logic instead of triggers
   7. Monitor trigger performance in production
   8. Use BEFORE triggers for validation, AFTER triggers for logging
   9. Be careful with statement-level triggers (process all rows at once)
   10. Disable triggers during bulk operations when appropriate
*/

-- ============================================================================
-- END OF 15_functions_triggers.sql
-- ============================================================================
