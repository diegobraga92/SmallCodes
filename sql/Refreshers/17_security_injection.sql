/*
   SECURITY & SQL INJECTION - Access Control, Injection Prevention
   File: 17_security_injection.sql

   Database security covers access control, encryption, and
   protecting against SQL injection attacks.
*/

-- ============================================================================
-- 1. SQL INJECTION
-- ============================================================================

/*
   SQL injection occurs when user input is concatenated directly
   into SQL queries, allowing attackers to modify the query structure.

   Vulnerable code (application layer):
   query = "SELECT * FROM users WHERE username = '" + userInput + "'"

   If userInput = "' OR '1'='1", the query becomes:
   SELECT * FROM users WHERE username = '' OR '1'='1'
   -- Returns ALL users!

   More dangerous:
   userInput = "'; DROP TABLE users; --"
   SELECT * FROM users WHERE username = ''; DROP TABLE users; --'
*/

-- ============================================================================
-- 2. PREVENTION: PARAMETERIZED QUERIES
-- ============================================================================

/*
   Always use parameterized queries (prepared statements).
   User input is treated as data, not executable SQL.
*/

-- Python (psycopg2):
-- cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

-- Java (JDBC):
-- PreparedStatement stmt = conn.prepareStatement(
--     "SELECT * FROM users WHERE username = ?"
-- );
-- stmt.setString(1, username);

-- C# (ADO.NET):
-- using var cmd = new SqlCommand(
--     "SELECT * FROM users WHERE username = @username", conn
-- );
-- cmd.Parameters.AddWithValue("@username", username);

-- Node.js (pg):
-- client.query('SELECT * FROM users WHERE username = $1', [username]);

-- ============================================================================
-- 3. GRANT / REVOKE - Access Control
-- ============================================================================

/*
   Principle of Least Privilege: grant only the permissions needed.
*/

-- Create a read-only user
-- CREATE USER report_user WITH PASSWORD 'secure_password';
-- GRANT CONNECT ON DATABASE mydb TO report_user;
-- GRANT USAGE ON SCHEMA public TO report_user;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO report_user;

-- Grant specific permissions
-- GRANT SELECT, INSERT ON orders TO app_user;
-- GRANT UPDATE (status) ON orders TO app_user;  -- column-level
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_user;

-- Revoke permissions
-- REVOKE DELETE ON employees FROM app_user;
-- REVOKE ALL PRIVILEGES ON customers FROM report_user;

-- ============================================================================
-- 4. ROLES
-- ============================================================================

/*
   Roles group permissions together for easier management.
*/

-- PostgreSQL:
-- CREATE ROLE read_only;
-- GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only;
-- GRANT read_only TO analyst_john;
-- GRANT read_only TO analyst_jane;

-- CREATE ROLE app_role;
-- GRANT SELECT, INSERT, UPDATE ON orders TO app_role;
-- GRANT SELECT, INSERT ON customers TO app_role;
-- GRANT app_role TO web_app_user;

-- ============================================================================
-- 5. ROW-LEVEL SECURITY (PostgreSQL)
-- ============================================================================

/*
   Row-Level Security (RLS) restricts which rows a user can access.
   Policies are applied automatically based on the current user.
*/

-- Enable RLS on a table
-- ALTER TABLE employees ENABLE ROW LEVEL SECURITY;

-- Create policy: managers can only see their department's employees
-- CREATE POLICY dept_access ON employees
--     FOR ALL
--     USING (department_id = get_user_department(current_user));

-- Create policy: employees can see their own record
-- CREATE POLICY self_access ON employees
--     FOR SELECT
--     USING (email = current_user);

-- ============================================================================
-- 6. ENCRYPTION
-- ============================================================================

/*
   At-rest encryption:
   - TDE (Transparent Data Encryption): encrypts entire database files
   - Column-level encryption: encrypts specific sensitive columns

   In-transit encryption:
   - SSL/TLS connections between client and server
   - Configure in database settings

   Hashing (one-way, for passwords):
   - Use bcrypt, scrypt, or argon2 (application level)
   - Never store plain text passwords
   - Never use MD5 or SHA-1 for passwords
*/

-- PostgreSQL: pgcrypto extension for encryption
-- CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Hash a password:
-- UPDATE users SET password_hash = crypt('user_password', gen_salt('bf'))
-- WHERE id = 1;

-- Verify a password:
-- SELECT id FROM users
-- WHERE username = 'alice'
--   AND password_hash = crypt('entered_password', password_hash);

-- ============================================================================
-- 7. AUDIT LOGGING
-- ============================================================================

/*
   Track who did what and when for compliance and security.
*/

-- CREATE TABLE audit_log (
--     audit_id SERIAL PRIMARY KEY,
--     table_name VARCHAR(100),
--     operation VARCHAR(10),  -- INSERT, UPDATE, DELETE
--     record_id INT,
--     old_values JSONB,
--     new_values JSONB,
--     changed_by VARCHAR(100),
--     changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- ============================================================================
-- 8. SECURITY BEST PRACTICES
-- ============================================================================

/*
   1. Always use parameterized queries (never concatenate user input)
   2. Apply principle of least privilege for database users
   3. Use roles to manage permissions consistently
   4. Encrypt sensitive data at rest and in transit
   5. Hash passwords with strong algorithms (bcrypt/argon2)
   6. Enable SSL/TLS for database connections
   7. Regularly audit permissions and access
   8. Keep database software up to date
   9. Use connection pooling with authentication
   10. Implement row-level security for multi-tenant apps
   11. Never expose database errors to end users
   12. Use database firewalls and network isolation
*/

-- ============================================================================
-- END OF 17_security_injection.sql
-- ============================================================================
