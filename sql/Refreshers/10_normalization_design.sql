/*
   NORMALIZATION & DATABASE DESIGN - Schema Design Principles
   File: 10_normalization_design.sql

   Normalization is the process of organizing data to reduce redundancy
   and improve data integrity. This file covers the normal forms and
   practical schema design patterns.
*/

-- ============================================================================
-- 1. WHY NORMALIZE?
-- ============================================================================

/*
   Benefits of normalization:
   - Eliminates data redundancy (same data stored in multiple places)
   - Prevents update anomalies (updating in one place but not another)
   - Prevents insertion anomalies (can't add data because of missing related data)
   - Prevents deletion anomalies (deleting one fact deletes unrelated facts)
   - Ensures data consistency and integrity

   Trade-offs:
   - More tables = more joins = potentially slower queries
   - Denormalization can improve read performance at the cost of write complexity
*/

-- ============================================================================
-- 2. FIRST NORMAL FORM (1NF)
-- ============================================================================

/*
   A table is in 1NF if:
   1. Each column contains atomic (indivisible) values
   2. Each column contains values of a single type
   3. Each row is unique (has a primary key)
   4. No repeating groups of columns

   VIOLATION: Multiple values in one column
   orders
   +----+-----------------------+
   | id | products              |
   +----+-----------------------+
   | 1  | 'Apple, Banana, Pear' |  ← comma-separated list
   +----+-----------------------+

   FIX: Create separate rows or a related table
   order_items
   +----------+-----------+
   | order_id | product   |
   +----------+-----------+
   | 1        | Apple     |
   | 1        | Banana    |
   | 1        | Pear      |
   +----------+-----------+
*/

-- ============================================================================
-- 3. SECOND NORMAL FORM (2NF)
-- ============================================================================

/*
   A table is in 2NF if:
   1. It is in 1NF
   2. All non-key columns are fully functionally dependent on the ENTIRE primary key
      (No partial dependencies)

   VIOLATION: Table with composite PK where some columns depend on only part of the PK
   order_details (PK: order_id + product_id)
   +----------+------------+---------+-------------+
   | order_id | product_id | qty     | product_name|  ← product_name depends only on product_id
   +----------+------------+---------+-------------+

   FIX: Split into two tables
   order_items (PK: order_id + product_id)
   +----------+------------+-----+
   | order_id | product_id | qty |
   +----------+------------+-----+

   products (PK: product_id)
   +------------+--------------+
   | product_id | product_name |
   +------------+--------------+
*/

-- ============================================================================
-- 4. THIRD NORMAL FORM (3NF)
-- ============================================================================

/*
   A table is in 3NF if:
   1. It is in 2NF
   2. All non-key columns are directly dependent on the primary key
      (No transitive dependencies: A → B → C)

   VIOLATION: Column depends on another non-key column
   employees
   +----+-----------+-----------+----------------+
   | id | name      | dept_id   | dept_location  |  ← dept_location depends on dept_id, not on id
   +----+-----------+-----------+----------------+

   FIX: Split into two tables
   employees
   +----+-----------+---------+
   | id | name      | dept_id |
   +----+-----------+---------+

   departments
   +---------+----------------+
   | dept_id | dept_location  |
   +---------+----------------+
*/

-- ============================================================================
-- 5. BOYCE-CODD NORMAL FORM (BCNF)
-- ============================================================================

/*
   BCNF is a stricter version of 3NF.
   A table is in BCNF if for every functional dependency X → Y,
   X is a superkey (a column or set of columns that uniquely identifies a row).

   BCNF violations are rare in practice but can occur with overlapping
   candidate keys.
*/

-- ============================================================================
-- 6. DENORMALIZATION - When to Break the Rules
-- ============================================================================

/*
   Denormalization is intentionally adding redundancy for performance.

   When to denormalize:
   - Read-heavy workloads (reporting, analytics)
   - When joins are too expensive
   - Pre-computed aggregates for dashboards
   - Caching frequently accessed data

   Example: Storing customer_name in orders table
   (normally would JOIN with customers table)
   - Pro: Faster reads, no join needed
   - Con: Must update both tables if customer name changes

   Best practice: Start normalized, denormalize only when
   performance measurements show it's necessary.
*/

-- ============================================================================
-- 7. ENTITY-RELATIONSHIP DESIGN PATTERNS
-- ============================================================================

/*
   One-to-One (1:1)
   - One user has one profile
   - Can be same table or separate (for security/performance)
   CREATE TABLE users (id INT PRIMARY KEY, ...);
   CREATE TABLE user_profiles (
       user_id INT PRIMARY KEY REFERENCES users(id),
       bio TEXT, avatar_url VARCHAR(500)
   );

   One-to-Many (1:N)
   - One department has many employees
   - Most common relationship
   CREATE TABLE departments (id INT PRIMARY KEY, ...);
   CREATE TABLE employees (
       id INT PRIMARY KEY,
       dept_id INT REFERENCES departments(id),
       ...
   );

   Many-to-Many (M:N)
   - One student can take many courses, one course has many students
   - Requires a junction/join table
   CREATE TABLE students (id INT PRIMARY KEY, ...);
   CREATE TABLE courses (id INT PRIMARY KEY, ...);
   CREATE TABLE enrollments (
       student_id INT REFERENCES students(id),
       course_id INT REFERENCES courses(id),
       enrollment_date DATE,
       PRIMARY KEY (student_id, course_id)
   );
*/

-- ============================================================================
-- 8. NAMING CONVENTIONS
-- ============================================================================

/*
   Tables:     plural or singular? Be consistent. (users or user)
               snake_case: order_items, product_categories
   Columns:    snake_case: first_name, created_at
   PK column:  id or table_name_id (user_id)
   FK column:  referenced_table_name_id (customer_id, product_id)
   Indexes:    idx_table_name_column(s)
   Constraints: pk_table_name, fk_table_name_ref_table, uq_table_name_col
   Views:      vw_entity_name or entity_summary
*/

-- ============================================================================
-- 9. COMMON DESIGN MISTAKES
-- ============================================================================

/*
   1. Using the same column for multiple purposes (overloading)
   2. Not using a surrogate key when natural key is unstable
   3. Storing derived data that can be calculated (without good reason)
   4. Using VARCHAR for dates or numbers
   5. Not indexing foreign keys
   6. Creating too many tables (over-normalization)
   7. Using EAV (Entity-Attribute-Value) anti-pattern
   8. Storing JSON when relational structure is known and stable
*/

-- ============================================================================
-- END OF 10_normalization_design.sql
-- ============================================================================
