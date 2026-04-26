/*
   DATABASE MIGRATIONS - Schema Versioning and Change Management
   File: 19_database_migrations.sql

   Migrations are version-controlled scripts that evolve the database
   schema over time. They ensure consistent schema across environments.
*/

-- ============================================================================
-- 1. WHY MIGRATIONS?
-- ============================================================================

/*
   Problems without migrations:
   - Schema changes are manual and error-prone
   - Different environments get out of sync
   - No history of schema changes
   - Rolling back changes is difficult
   - Team collaboration is messy

   Benefits of migrations:
   - Version-controlled schema changes
   - Reproducible environments
   - Automated deployment
   - Rollback capability
   - Team collaboration
*/

-- ============================================================================
-- 2. MIGRATION TOOLS
-- ============================================================================

/*
   Tool            | Language    | Database Support
   ----------------|-------------|---------------------------
   Flyway          | Java        | PostgreSQL, MySQL, SQL Server, Oracle, SQLite
   Liquibase       | Java/XML    | PostgreSQL, MySQL, SQL Server, Oracle, SQLite
   Alembic         | Python      | PostgreSQL, MySQL, SQL Server, SQLite
   ActiveRecord    | Ruby        | PostgreSQL, MySQL, SQL Server, SQLite
   Prisma Migrate  | TypeScript  | PostgreSQL, MySQL, SQL Server, SQLite
   goose           | Go          | PostgreSQL, MySQL, SQL Server, SQLite
   golang-migrate  | Go          | PostgreSQL, MySQL, SQL Server, SQLite
*/

-- ============================================================================
-- 3. MIGRATION FILE CONVENTION
-- ============================================================================

/*
   Typical naming convention:
   V{version}__{description}.sql

   Examples:
   V1__create_users_table.sql
   V2__add_email_to_users.sql
   V3__create_orders_table.sql
   V4__add_foreign_keys.sql
*/

-- ============================================================================
-- 4. EXAMPLE MIGRATION: V1__create_users_table.sql
-- ============================================================================

-- -- V1__create_users_table.sql
-- CREATE TABLE users (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(50) UNIQUE NOT NULL,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     password_hash VARCHAR(255) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
--
-- CREATE INDEX idx_users_email ON users(email);

-- ============================================================================
-- 5. EXAMPLE MIGRATION: V2__add_profile.sql
-- ============================================================================

-- -- V2__add_profile.sql
-- CREATE TABLE user_profiles (
--     user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
--     first_name VARCHAR(100),
--     last_name VARCHAR(100),
--     bio TEXT,
--     avatar_url VARCHAR(500)
-- );
--
-- ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;

-- ============================================================================
-- 6. ROLLBACK MIGRATIONS
-- ============================================================================

/*
   Some tools support undo/rollback migrations.
   Naming: V1__description.sql + V1__description__rollback.sql

   Flyway: supports undo migrations (V1__description__undo.sql)
   Liquibase: supports rollback tags in changelog
   Alembic: supports downgrade() functions
*/

-- Rollback for V1:
-- -- V1__create_users_table__undo.sql
-- DROP TABLE IF EXISTS users;

-- Rollback for V2:
-- -- V2__add_profile__undo.sql
-- DROP TABLE IF EXISTS user_profiles;
-- ALTER TABLE users DROP COLUMN IF EXISTS is_active;

-- ============================================================================
-- 7. MIGRATION BEST PRACTICES
-- ============================================================================

/*
   1. One migration per logical change
   2. Always test migrations on a copy of production data
   3. Write both forward and rollback migrations
   4. Never modify an already-applied migration (create a new one)
   5. Use transactions for atomic migrations (when supported)
   6. Consider performance impact on large tables
   7. Avoid long-running migrations during peak hours
   8. Use CI/CD to automatically run migrations
   9. Monitor migration execution time
   10. Keep migration files in version control alongside application code
*/

-- ============================================================================
-- 8. SAFE SCHEMA CHANGES FOR LARGE TABLES
-- ============================================================================

/*
   Adding a column with a default value:
   - PostgreSQL 11+: ALTER TABLE ... ADD COLUMN ... DEFAULT ... (instant)
   - Older versions: Add column without default, then UPDATE in batches

   Adding an index:
   - PostgreSQL: CREATE INDEX CONCURRENTLY (non-blocking)
   - MySQL: supports online DDL (ALGORITHM=INPLACE, LOCK=NONE)
   - SQL Server: CREATE INDEX WITH (ONLINE=ON)

   Changing a column type:
   - Add new column, copy data in batches, swap, drop old
   - Or use tools like pt-online-schema-change (Percona)
*/

-- Non-blocking index creation (PostgreSQL):
-- CREATE INDEX CONCURRENTLY idx_orders_customer_id ON orders(customer_id);

-- Online index creation (SQL Server):
-- CREATE INDEX idx_orders_customer_id ON orders(customer_id)
-- WITH (ONLINE = ON);

-- ============================================================================
-- 9. MIGRATION WORKFLOW
-- ============================================================================

/*
   1. Developer creates migration file locally
   2. Tests migration on local database
   3. Commits migration to version control
   4. CI/CD runs migration on staging environment
   5. Tests pass on staging
   6. Migration is applied to production (automated or manual)
   7. Monitor for errors or performance issues
   8. If issues: apply rollback migration
*/

-- ============================================================================
-- END OF 19_database_migrations.sql
-- ============================================================================
