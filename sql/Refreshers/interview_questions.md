# SQL Technical Interview Questions

Comprehensive interview questions covering all 22 SQL refresher files, organized by topic and difficulty level.

---

## 🟢 JUNIOR LEVEL (Fundamentals)

### SQL Basics & Query Structure

1. **What is SQL, and what makes it a "declarative" language? How does that differ from imperative programming?**

   *Key points: SQL is declarative — you specify WHAT data you want, not HOW to get it. Imperative programming (e.g., Python, C++) requires step-by-step instructions. The database engine decides the execution plan.*

2. **What is the difference between DDL, DML, DCL, and TCL? Give examples of each.**

   *Key points: DDL (CREATE, ALTER, DROP) — schema changes. DML (SELECT, INSERT, UPDATE, DELETE) — data manipulation. DCL (GRANT, REVOKE) — permissions. TCL (COMMIT, ROLLBACK, SAVEPOINT) — transaction control.*

3. **Explain the logical execution order of a SQL query (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT). Why does this matter when using column aliases?**

   *Key points: FROM (tables) → WHERE (filter rows) → GROUP BY (group) → HAVING (filter groups) → SELECT (compute expressions) → ORDER BY (sort) → LIMIT (paginate). Aliases defined in SELECT can't be used in WHERE/GROUP BY/HAVING because they don't exist yet.*

4. **What is NULL in SQL? Why can't you use `= NULL` to check for NULL values?**

   *Key points: NULL represents unknown/missing value, not zero or empty. `= NULL` always returns NULL (not TRUE/FALSE) because NULL is not equal to anything. Use `IS NULL` or `IS NOT NULL` instead.*

5. **What is the difference between `COUNT(*)`, `COUNT(column)`, and `COUNT(DISTINCT column)`?**

   *Key points: `COUNT(*)` counts all rows including NULLs. `COUNT(column)` counts non-NULL values in that column. `COUNT(DISTINCT column)` counts unique non-NULL values.*

6. **What is the difference between `DELETE`, `TRUNCATE`, and `DROP`? When would you use each?**

   *Key points: `DELETE` removes rows (can be rolled back, fires triggers, slower). `TRUNCATE` removes all rows quickly (minimal logging, can't filter, resets auto-increment). `DROP` removes the entire table structure.*

### Filtering & Sorting

7. **Explain the difference between `WHERE` and `HAVING`. Can you use aggregate functions in `WHERE`? Why or why not?**

   *Key points: `WHERE` filters rows before aggregation. `HAVING` filters groups after aggregation. You can't use aggregates in `WHERE` because aggregation hasn't happened yet at that stage.*

8. **What is the difference between `IN` and `BETWEEN`? When would you use each?**

   *Key points: `IN` checks membership in a set of values. `BETWEEN` checks if a value is in a range (inclusive). Use `IN` for discrete values, `BETWEEN` for continuous ranges.*

9. **How does the `LIKE` operator work? What do `%` and `_` represent?**

   *Key points: `%` matches any sequence of characters (including empty). `_` matches exactly one character. Example: `LIKE 'J%'` matches strings starting with 'J'.*

10. **What does `COALESCE` do? Give a practical example of when you'd use it.**

    *Key points: Returns the first non-NULL value from a list of arguments. Example: `COALESCE(phone, email, 'No contact')` — uses phone if available, falls back to email, then to default text.*

11. **What is the difference between `UNION` and `UNION ALL`? Which is faster and why?**

    *Key points: `UNION` removes duplicates (adds a sort/distinct step). `UNION ALL` keeps all rows including duplicates. `UNION ALL` is faster because it avoids the deduplication overhead.*

12. **How does `ORDER BY` handle NULLs? How can you control NULL positioning (NULLS FIRST / NULLS LAST)?**

    *Key points: Default behavior varies by database (PostgreSQL: NULLs last for ASC, first for DESC). Use `NULLS FIRST` or `NULLS LAST` to explicitly control positioning.*

### Joins

13. **Explain the difference between `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, and `FULL OUTER JOIN`. Draw a Venn diagram for each.**

    *Key points: INNER JOIN — matching rows only. LEFT JOIN — all left table rows + matching right. RIGHT JOIN — all right table rows + matching left. FULL OUTER JOIN — all rows from both tables, NULLs where no match.*

14. **What is a `CROSS JOIN` and when would you use it? What caution should you take?**

    *Key points: Produces Cartesian product (every row from table A × every row from table B). Used for generating combinations (e.g., dates × products). Caution: can produce huge result sets.*

15. **What is a self-join? Give a practical example (e.g., employees and managers).**

    *Key points: Joining a table to itself using different aliases. Example: `SELECT e.name, m.name FROM employees e JOIN employees m ON e.manager_id = m.id` to get employee-manager pairs.*

16. **What is the difference between putting a condition in the `ON` clause vs. the `WHERE` clause of a `LEFT JOIN`?**

    *Key points: `ON` filters rows from the right table before the join (preserves left table rows). `WHERE` filters after the join (can turn LEFT JOIN into INNER JOIN by removing NULL rows).*

17. **Why is `NATURAL JOIN` considered dangerous?**

    *Key points: Automatically joins on all columns with the same name. Schema changes (adding/renaming columns) silently change the join behavior. Can produce unexpected results. Always prefer explicit `USING` or `ON`.*

### Data Types & Constraints

18. **What is the difference between `CHAR(n)` and `VARCHAR(n)`? When would you choose one over the other?**

    *Key points: `CHAR(n)` is fixed-length (pads with spaces). `VARCHAR(n)` is variable-length (only stores actual characters). Use `CHAR` for fixed-length codes (e.g., ISO country codes), `VARCHAR` for variable text.*

19. **What is the difference between `DECIMAL` and `FLOAT`? When should you use each?**

    *Key points: `DECIMAL` is exact (fixed-point) — use for money. `FLOAT` is approximate (floating-point) — use for scientific calculations where small rounding is acceptable.*

20. **Explain the purpose of each constraint type: `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `CHECK`, `DEFAULT`.**

    *Key points: PRIMARY KEY = unique identifier (unique + not null). FOREIGN KEY = references another table. UNIQUE = no duplicates allowed. NOT NULL = value required. CHECK = validates condition. DEFAULT = fallback value.*

21. **What is a composite primary key? Give an example of when you'd use one.**

    *Key points: A primary key consisting of multiple columns. Example: `order_items` table with `(order_id, product_id)` as composite PK — each product appears once per order.*

22. **What are the referential actions for foreign keys (`CASCADE`, `SET NULL`, `RESTRICT`, `NO ACTION`)? Explain each.**

    *Key points: CASCADE — delete/update child rows when parent is deleted/updated. SET NULL — set child FK to NULL. RESTRICT — prevent parent deletion if children exist. NO ACTION — similar to RESTRICT but checked at end of transaction.*

### DDL & DML

23. **How do you add a column to an existing table? How do you add a foreign key constraint?**

    *Key points: `ALTER TABLE table ADD COLUMN column type;`. `ALTER TABLE child ADD CONSTRAINT fk_name FOREIGN KEY (col) REFERENCES parent(col);`.*

24. **What is the `INSERT ... ON CONFLICT` (PostgreSQL) or `ON DUPLICATE KEY UPDATE` (MySQL) pattern called? How does it work?**

    *Key points: Upsert pattern. Attempts INSERT; if a unique/primary key conflict occurs, performs UPDATE instead. PostgreSQL: `INSERT ... ON CONFLICT (id) DO UPDATE SET col = EXCLUDED.col`.*

25. **What is the `RETURNING` clause in PostgreSQL? When is it useful?**

    *Key points: Returns values from inserted/updated/deleted rows. Useful for getting auto-generated IDs or default values without a separate SELECT query.*

26. **How do you safely perform a mass `UPDATE` or `DELETE`? What precautions should you take?**

    *Key points: Use transactions (BEGIN/COMMIT). Test with SELECT first. Use LIMIT/batching for large tables. Check WHERE conditions carefully. Have a rollback plan. Run during maintenance windows.*

---

## 🟡 MID-LEVEL (Intermediate)

### Subqueries & CTEs

27. **What is the difference between a scalar subquery, a row subquery, and a table subquery (derived table)?**

    *Key points: Scalar returns single value (used in SELECT/WHERE). Row subquery returns one row (compared with row constructors). Table subquery returns multiple rows/columns (used in FROM clause as derived table).*

28. **What is a correlated subquery? How does it differ from a non-correlated subquery? When might it be slow?**

    *Key points: Correlated subquery references outer query columns and executes once per outer row. Non-correlated executes once independently. Correlated subqueries can be slow on large datasets because they run per row.*

29. **What is the difference between `EXISTS` and `IN`? When would you prefer one over the other?**

    *Key points: `EXISTS` checks for existence (stops on first match). `IN` compares values (may need to materialize subquery result). Prefer `EXISTS` for large subquery results and when checking NULL-containing data.*

30. **What is a CTE (Common Table Expression)? How does it improve query readability?**

    *Key points: Named temporary result set defined with `WITH`. Improves readability by breaking complex queries into named steps. Can be referenced multiple times in the main query.*

31. **What is a recursive CTE? Give an example of a practical use case (e.g., org chart, category tree).**

    *Key points: CTE that references itself using `UNION ALL` with an anchor member and recursive member. Use cases: org charts, category hierarchies, graph traversal, Fibonacci sequence.*

32. **When would you choose a CTE over a subquery? When would you choose a subquery over a join?**

    *Key points: CTE for readability, reusability, and recursion. Subquery for simple single-use cases. Join over subquery when the subquery can be rewritten as a join (usually more efficient).*

### Set Operations

33. **What are the rules for set operations (`UNION`, `INTERSECT`, `EXCEPT`)? What must be true about the SELECT statements?**

    *Key points: Both SELECTs must have the same number of columns. Corresponding columns must have compatible data types. Column names come from the first SELECT.*

34. **How do you implement `INTERSECT` or `EXCEPT` in MySQL, which doesn't support them natively?**

    *Key points: `INTERSECT` = `INNER JOIN` with `DISTINCT`. `EXCEPT` = `LEFT JOIN` with `WHERE right.id IS NULL`. Or use `NOT IN`/`NOT EXISTS`.*

35. **What is the difference between a set operation (vertical combination) and a join (horizontal combination)?**

    *Key points: Set operations stack rows vertically (more rows). Joins combine columns horizontally (more columns).*

### Aggregation & Grouping

36. **What is the difference between `GROUP BY` and `DISTINCT`? When would you use each?**

    *Key points: `DISTINCT` removes duplicate rows. `GROUP BY` groups rows for aggregation. Use `DISTINCT` for simple deduplication, `GROUP BY` when you need aggregate functions (COUNT, SUM, AVG).*

37. **What is `GROUP BY ROLLUP`? What about `CUBE` and `GROUPING SETS`?**

    *Key points: ROLLUP generates subtotals and grand total (hierarchical). CUBE generates all possible combinations of grouping columns. GROUPING SETS lets you specify exactly which groupings you want.*

38. **Why can't you use `WHERE` to filter aggregated data? What should you use instead?**

    *Key points: `WHERE` filters rows before aggregation. Use `HAVING` to filter after aggregation (on grouped/aggregated results).*

39. **How does `AVG()` handle NULL values? How does `SUM()` handle NULLs?**

    *Key points: Both ignore NULL values. `AVG()` divides by count of non-NULL values. `SUM()` returns NULL if all values are NULL, otherwise sum of non-NULL values.*

### Window Functions

40. **What is a window function? How does it differ from `GROUP BY`?**

    *Key points: Window function performs calculation across a set of rows related to the current row without collapsing them. `GROUP BY` collapses rows into groups. Window functions preserve individual rows.*

41. **Explain the syntax: `function() OVER (PARTITION BY ... ORDER BY ... frame_specification)`.**

    *Key points: `PARTITION BY` divides rows into groups. `ORDER BY` defines ordering within each partition. Frame specification (ROWS/RANGE) defines which rows are included in the calculation.*

42. **What is the difference between `ROW_NUMBER()`, `RANK()`, and `DENSE_RANK()`? Give an example where they produce different results.**

    *Key points: `ROW_NUMBER()` assigns unique sequential numbers. `RANK()` gives same rank to ties, skips next rank. `DENSE_RANK()` gives same rank to ties, no skipping. Example: values (10,20,20,30) → ROW_NUMBER: 1,2,3,4; RANK: 1,2,2,4; DENSE_RANK: 1,2,2,3.*

43. **What do `LAG()` and `LEAD()` do? Give a practical example (e.g., year-over-year comparison).**

    *Key points: `LAG()` accesses previous row's value. `LEAD()` accesses next row's value. Example: `LAG(sales) OVER (ORDER BY year)` to compare current year sales with previous year.*

44. **What is a window frame? Explain `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.**

    *Key points: Frame defines which rows are included in the window calculation. `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` includes all rows from the start of the partition up to the current row — used for running totals.*

45. **How would you find the top 3 highest-paid employees per department using window functions?**

    *Key points: Use `ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC)` as rn, then filter `WHERE rn <= 3`.*

### Normalization & Database Design

46. **Explain the three normal forms (1NF, 2NF, 3NF). What problem does each solve?**

    *Key points: 1NF — atomic columns, no repeating groups. 2NF — 1NF + no partial dependencies (all non-key columns depend on full PK). 3NF — 2NF + no transitive dependencies (non-key columns depend only on PK).*

47. **What is denormalization? When would you intentionally denormalize a schema?**

    *Key points: Adding redundant data to improve read performance. Use when: read-heavy workloads, complex joins are slow, reporting/analytics queries need pre-computed data. Trade-off: write complexity and data inconsistency risk.*

48. **How do you model a many-to-many relationship in a relational database?**

    *Key points: Create a junction/link table with foreign keys to both related tables. Example: `students` ← `enrollments` → `courses`. The junction table often has a composite primary key.*

49. **What is the Entity-Attribute-Value (EAV) anti-pattern? Why is it problematic?**

    *Key points: Storing attributes as rows (entity_id, attribute_name, value) instead of columns. Problems: complex queries, no type enforcement, poor performance, difficult validation. Use JSON columns or proper schema instead.*

50. **What naming conventions do you follow for tables, columns, indexes, and constraints?**

    *Key points: Tables: plural nouns (users, orders). Columns: snake_case (first_name). PK: `table_name_pkey`. FK: `fk_child_parent`. Index: `idx_table_column`. Unique: `uq_table_column`.*

### Indexes & Performance

51. **What is a B-tree index? What types of queries does it optimize?**

    *Key points: Balanced tree structure that enables fast lookups, range scans, and sorting. Optimizes: equality (`=`), range (`>`, `<`, `BETWEEN`), prefix matching (`LIKE 'abc%'`), and `ORDER BY`.*

52. **What is the leftmost prefix rule for composite indexes? Give an example.**

    *Key points: A composite index on (a, b, c) can be used for queries on (a), (a, b), and (a, b, c). It cannot be used for queries on (b) or (c) alone. The leftmost column must be used first.*

53. **What is a covering index? What is an index-only scan?**

    *Key points: An index that contains all columns needed by a query. Enables index-only scans where the database reads only the index without accessing the table. Improves performance significantly.*

54. **What is a partial index (PostgreSQL)? When would you use one?**

    *Key points: Index on a subset of rows using a WHERE clause. Example: `CREATE INDEX idx_active_users ON users (email) WHERE active = true`. Saves space and improves performance for filtered queries.*

55. **What makes a predicate "sargable"? Give examples of sargable vs. non-sargable conditions.**

    *Key points: Sargable (Search ARGument ABLE) — can use index. Examples: `WHERE date = '2024-01-01'` (sargable), `WHERE YEAR(date) = 2024` (non-sargable — wraps column in function).*

56. **Why might an index not be used even when it exists on the column?**

    *Key points: Non-sargable conditions (function wrapping), low selectivity (returns too many rows), small table (seq scan is faster), outdated statistics, type mismatch, `LIKE '%pattern'` (leading wildcard).*

57. **How do you read an `EXPLAIN ANALYZE` output? What do Seq Scan, Index Scan, and Index Only Scan mean?**

    *Key points: Seq Scan — full table scan (slow on large tables). Index Scan — uses index to find rows, then fetches from table. Index Only Scan — reads all needed data from index alone (fastest). Look for high cost, actual time, and row estimates.*

### Transactions & Isolation

58. **What does ACID stand for? Explain each property.**

    *Key points: Atomicity — all or nothing. Consistency — data remains valid. Isolation — concurrent transactions don't interfere. Durability — committed data survives crashes.*

59. **What are the four transaction isolation levels? What anomalies does each prevent (dirty read, non-repeatable read, phantom read)?**

    *Key points: Read Uncommitted — prevents nothing. Read Committed — prevents dirty reads. Repeatable Read — prevents dirty + non-repeatable reads. Serializable — prevents all anomalies.*

60. **What is the default isolation level in PostgreSQL? In MySQL? In SQL Server?**

    *Key points: PostgreSQL — Read Committed. MySQL (InnoDB) — Repeatable Read. SQL Server — Read Committed.*

61. **What is a deadlock? How can you prevent deadlocks?**

    *Key points: Two or more transactions waiting for each other's locks. Prevention: access tables in consistent order, keep transactions short, use similar lock granularity, implement retry logic.*

62. **What is a savepoint? How does it differ from a full `ROLLBACK`?**

    *Key points: Savepoint marks a point within a transaction that you can roll back to without aborting the entire transaction. `ROLLBACK TO savepoint` undoes changes after that point but keeps the transaction active.*

63. **What is optimistic locking vs. pessimistic locking? How would you implement optimistic locking in SQL?**

    *Key points: Optimistic — assume no conflict, check at commit (use version column). Pessimistic — lock rows upfront (`SELECT ... FOR UPDATE`). Optimistic implementation: add `version` column, increment on update, check version in WHERE clause.*

---

## 🔴 UPPER-MID TO SENIOR LEVEL

### Stored Procedures & Functions

64. **What is the difference between a stored procedure and a function? When would you use each?**

    *Key points: Functions return a single value/table, can be used in SELECT. Procedures can have side effects (INSERT/UPDATE), use transactions, return multiple result sets. Use functions for computations, procedures for business logic operations.*

65. **What are the benefits and drawbacks of putting business logic in stored procedures vs. application code?**

    *Key points: Benefits: proximity to data, reduced network round-trips, consistent across all apps. Drawbacks: harder to version/test/debug, vendor lock-in, limited tooling, can hide complexity.*

66. **How do you handle errors in a stored procedure? Give an example with `RAISE EXCEPTION` or `TRY/CATCH`.**

    *Key points: PostgreSQL uses `RAISE EXCEPTION 'message'`. SQL Server uses `BEGIN TRY ... END TRY BEGIN CATCH ... END CATCH`. Always include meaningful error messages and rollback on failure.*

67. **When would you use a cursor in a stored procedure? What are the performance implications?**

    *Key points: Use cursors when you need row-by-row processing (complex calculations, calling external APIs). Performance: much slower than set-based operations. Always prefer set-based solutions first.*

68. **How do you prevent SQL injection when using dynamic SQL inside a stored procedure?**

    *Key points: Use `EXECUTE ... USING` (parameterized dynamic SQL) instead of string concatenation. Validate and sanitize inputs. Use `quote_ident()` for identifiers, `quote_literal()` for values.*

### Triggers

69. **What is a trigger? What events can fire a trigger (INSERT, UPDATE, DELETE)?**

    *Key points: A trigger is a stored procedure that automatically executes in response to database events. Events: INSERT, UPDATE, DELETE, and sometimes TRUNCATE.*

70. **What is the difference between a `BEFORE` trigger and an `AFTER` trigger? When would you use each?**

    *Key points: BEFORE — runs before the operation, can modify the new row or reject it (validation). AFTER — runs after the operation, used for logging, auditing, cascading changes.*

71. **What is an `INSTEAD OF` trigger? When is it used?**

    *Key points: Replaces the triggering operation entirely. Used primarily on views to make non-updatable views updatable. Example: inserting into a view that spans multiple tables.*

72. **What is the difference between a row-level trigger and a statement-level trigger?**

    *Key points: Row-level fires once per affected row (access to OLD and NEW values). Statement-level fires once per SQL statement regardless of rows affected. Row-level is more common for validation/auditing.*

73. **What are the risks of using triggers? When should you avoid them?**

    *Key points: Risks: hidden complexity (invisible logic), debugging difficulty, performance impact (row-level triggers on bulk operations), cascading trigger chains. Avoid when logic can be in application code.*

74. **How would you implement an audit log using triggers?**

    *Key points: Create audit table with columns (table_name, operation, old_data, new_data, changed_by, changed_at). Create AFTER INSERT/UPDATE/DELETE triggers that insert into audit table using OLD and NEW row values.*

### Query Optimization

75. **Describe your process for optimizing a slow query from start to finish.**

    *Key points: 1) Identify slow query (logs, monitoring). 2) Run EXPLAIN ANALYZE. 3) Check for full table scans, missing indexes. 4) Review join order and types. 5) Check for non-sargable conditions. 6) Consider rewriting (CTEs, temp tables, denormalization). 7) Test changes. 8) Monitor.*

76. **What is the difference between a Nested Loop Join, a Hash Join, and a Merge Join? When is each optimal?**

    *Key points: Nested Loop — for small tables with index (O(n*m)). Hash Join — for large unsorted tables (build hash table). Merge Join — for large sorted tables (O(n+m)).*

77. **What is a materialized view? How does it differ from a regular view? When would you use one?**

    *Key points: Materialized view stores the query result physically (like a table). Regular view is just a saved query (virtual). Use materialized views for expensive aggregations that don't need real-time freshness.*

78. **How do outdated statistics affect query performance? How do you update them?**

    *Key points: Outdated statistics cause poor execution plan choices (wrong join type, wrong index). Update with `ANALYZE` (PostgreSQL), `UPDATE STATISTICS` (SQL Server), `ANALYZE TABLE` (MySQL).*

79. **What is the `FOR UPDATE` clause? When would you use `FOR UPDATE SKIP LOCKED`?**

    *Key points: `FOR UPDATE` locks selected rows for update (pessimistic locking). `SKIP LOCKED` skips rows already locked by other transactions — useful for job queues where multiple workers pick jobs.*

80. **How would you optimize a pagination query with `LIMIT/OFFSET` for large offsets?**

    *Key points: Offset pagination gets slower with larger offsets (scans all skipped rows). Alternatives: keyset pagination (`WHERE id > last_seen_id ORDER BY id LIMIT 20`), or using a covering index.*

### Security & SQL Injection

81. **What is SQL injection? Give an example of how it works.**

    *Key points: Injecting malicious SQL through user input. Example: `username = "' OR '1'='1"` turns `SELECT * FROM users WHERE username = '' OR '1'='1'` — returns all users.*

82. **How do parameterized queries prevent SQL injection?**

    *Key points: Parameters are sent separately from SQL structure. The database treats them as data, not executable code. User input can never alter the query structure.*

83. **What is the principle of least privilege in database security? How do you implement it?**

    *Key points: Grant only the minimum permissions needed. Implement: separate read/write users, schema-specific permissions, revoke unnecessary default privileges, use roles instead of per-user grants.*

84. **What is Row-Level Security (RLS)? When would you use it?**

    *Key points: RLS restricts which rows a user can see based on a policy function. Use for multi-tenant applications where each tenant should only see their own data.*

85. **How do you encrypt sensitive data at rest and in transit in a database?**

    *Key points: At rest: TDE (Transparent Data Encryption), column-level encryption (pgcrypto), encrypted filesystem. In transit: TLS/SSL connections, enforce `sslmode=require`.*

86. **How should passwords be stored in a database? What algorithms should you use?**

    *Key points: Never store plain text. Use slow hashing algorithms: bcrypt, Argon2, PBKDF2, scrypt. Always use unique salts per password. Never use MD5, SHA-1, or unsalted hashes.*

### Concurrency & Locking

87. **Explain how MVCC (Multi-Version Concurrency Control) works. How does it allow readers to not block writers?**

    *Key points: Each transaction sees a snapshot of data at a point in time. Readers see the committed version as of their snapshot start. Writers create new row versions. Readers don't block writers, writers don't block readers.*

88. **What is the difference between row-level, page-level, and table-level locks?**

    *Key points: Row-level — locks individual rows (high concurrency, more overhead). Page-level — locks a page of rows (balance). Table-level — locks entire table (low concurrency, less overhead).*

89. **What is lock escalation? Which databases support it?**

    *Key points: Converting many fine-grained locks (row-level) into fewer coarse-grained locks (table-level) to reduce overhead. Supported by SQL Server and MySQL (InnoDB). PostgreSQL doesn't escalate.*

90. **How do you monitor current locks and blocking queries in PostgreSQL or MySQL?**

    *Key points: PostgreSQL: `pg_locks` view, `pg_stat_activity`. MySQL: `SHOW PROCESSLIST`, `INFORMATION_SCHEMA.INNODB_LOCKS`, `SHOW ENGINE INNODB STATUS`.*

91. **What is the `SKIP LOCKED` clause? How is it useful for job queues?**

    *Key points: `SELECT ... FOR UPDATE SKIP LOCKED` skips rows locked by other transactions. Essential for job queues: multiple workers can safely pick different jobs without contention.*

### Migrations & Schema Changes

92. **What are database migrations? Why are they important?**

    *Key points: Version-controlled, incremental schema changes. Important for: reproducibility, team collaboration, rollback capability, deployment automation, tracking schema history.*

93. **How do you safely add a column with a default value to a large production table?**

    *Key points: PostgreSQL 11+: `ALTER TABLE ADD COLUMN ... DEFAULT ...` is instant (metadata only). Older versions: add column without default, then batch update in chunks, then set default.*

94. **How do you create an index without blocking writes on a production table?**

    *Key points: PostgreSQL: `CREATE INDEX CONCURRENTLY`. MySQL: `ALTER TABLE ... ADD INDEX ... ALGORITHM=INPLACE, LOCK=NONE`. These allow concurrent reads and writes during index creation.*

95. **What is the difference between `CREATE INDEX` and `CREATE INDEX CONCURRENTLY` (PostgreSQL)?**

    *Key points: Regular `CREATE INDEX` blocks writes (takes ACCESS EXCLUSIVE lock). `CREATE INDEX CONCURRENTLY` allows writes during creation but takes longer and uses more resources.*

96. **How do you handle rollback migrations?**

    *Key points: Write reversible migrations (up and down functions). Test rollbacks before production. For destructive changes (DROP COLUMN), deploy in phases: first make column optional, then drop in a later migration.*

### Advanced Indexing

97. **What is a covering index? How does it enable index-only scans?**

    *Key points: An index that includes all columns needed by a query (either as key columns or INCLUDE columns). The database can satisfy the query entirely from the index without touching the table heap.*

98. **What is a functional/expression index? Give an example of when you'd use one.**

    *Key points: Index on the result of a function or expression. Example: `CREATE INDEX idx_lower_email ON users (LOWER(email))` — enables fast lookups on `WHERE LOWER(email) = 'user@example.com'`.*

99. **What is a clustered index vs. a non-clustered index? Which databases support clustered indexes?**

    *Key points: Clustered index determines physical row order (one per table). Non-clustered index is a separate structure with pointers. Supported by: MySQL (InnoDB PK is clustered), SQL Server (can specify). PostgreSQL doesn't have clustered indexes (uses heap).*

100. **How do you identify unused indexes? What should you do with them?**

     *Key points: PostgreSQL: `pg_stat_user_indexes` with `idx_scan = 0`. MySQL: `performance_schema.table_io_waits_summary_by_index_usage`. Drop unused indexes to save write overhead and storage space.*

101. **What is index selectivity? How does it affect index usefulness?**

     *Key points: Ratio of distinct values to total rows. High selectivity (close to 1) = index is very useful (e.g., primary key). Low selectivity (close to 0) = index may not be used (e.g., boolean column with 50/50 split).*

### Beyond SQL

102. **When would you choose a NoSQL database over a SQL database?**

     *Key points: Flexible schema (rapid prototyping), high write throughput, horizontal scaling, unstructured data, simple key-value access patterns. Examples: document stores for content management, key-value for caching.*

103. **What is polyglot persistence? Give an example architecture using multiple database types.**

     *Key points: Using different database types for different use cases. Example: PostgreSQL for transactions, Redis for caching, Elasticsearch for search, MongoDB for catalog data, Cassandra for time-series metrics.*

104. **When would you use a document database (MongoDB) vs. a relational database?**

     *Key points: Document DB for: nested/self-contained data, flexible schema, rapid iteration. Relational for: complex relationships, joins, ACID compliance, structured data with clear schema.*

105. **When would you use a graph database (Neo4j) vs. a relational database?**

     *Key points: Graph DB for: highly connected data, relationship-heavy queries (friend-of-friend, recommendation engines), pathfinding. Relational for: tabular data, aggregations, reporting.*

106. **What is NewSQL? How does it differ from traditional SQL databases?**

     *Key points: NewSQL databases (CockroachDB, YugabyteDB, Spanner) provide SQL interface with horizontal scalability and distributed ACID transactions. Traditional SQL scales vertically; NewSQL scales horizontally.*

### Design & Architecture

107. **How would you design a database schema for a multi-tenant SaaS application?**

     *Key points: Three approaches: 1) Separate database per tenant (strongest isolation). 2) Separate schema per tenant. 3) Shared table with tenant_id column (simplest, needs RLS). Choose based on isolation requirements and tenant count.*

108. **How would you implement soft deletes? What are the trade-offs?**

     *Key points: Add `deleted_at TIMESTAMP` column (NULL = active, timestamp = deleted). Queries need `WHERE deleted_at IS NULL`. Trade-offs: more complex queries, storage growth, need to handle unique constraints. Benefits: recoverability, audit trail.*

109. **How would you design a database for an e-commerce platform with products, categories, orders, and inventory?**

     *Key points: Products (id, name, price, category_id). Categories (id, name, parent_id). Orders (id, user_id, status, created_at). Order_Items (order_id, product_id, quantity, price). Inventory (product_id, quantity, warehouse_id). Use transactions for order placement.*

110. **How do you handle time zones in a database? Should you store timestamps in UTC?**

     *Key points: Always store in UTC using TIMESTAMP WITH TIME ZONE. Convert to local time in application layer. Never use server local time. Store user's timezone preference separately for display.*

111. **How would you implement a full-text search feature using SQL?**

     *Key points: PostgreSQL: `GIN` index on `to_tsvector('english', column)`, query with `to_tsquery('english', 'search terms')`. MySQL: `FULLTEXT` index, `MATCH ... AGAINST`. For complex search, consider Elasticsearch.*

112. **What strategies would you use to archive or purge old data from a large production database?**

     *Key points: Partitioning by date (DROP old partitions). Batch delete in small chunks (e.g., 1000 rows at a time). Move to archive tables/database. Use pg_archive or separate cold storage. Schedule during low-traffic periods.*

---

## 💡 BONUS: Behavioral & Problem-Solving Questions

113. **Describe a time you optimized a slow query. What was the problem, and what did you do?**

     *Key points: Identify the bottleneck (EXPLAIN ANALYZE). Common fixes: add missing index, rewrite non-sargable WHERE, replace correlated subquery with join, add covering index, use materialized view for complex aggregations.*

114. **Have you ever dealt with a deadlock in production? How did you diagnose and resolve it?**

     *Key points: Check database logs for deadlock reports. Identify conflicting transactions. Fix: ensure consistent lock ordering, keep transactions short, use retry logic, consider lowering isolation level if appropriate.*

115. **How would you migrate a large production table from one schema to another with zero downtime?**

     *Key points: Use blue-green deployment: create new table, sync data via triggers/logical replication, gradually switch reads/writes. Or use versioned columns and dual-write pattern. Test thoroughly, have rollback plan.*

116. **How do you approach database capacity planning? What metrics do you monitor?**

     *Key points: Monitor: disk space growth rate, CPU usage, connection count, query throughput, slow query count, replication lag, cache hit ratio. Plan for 2x growth. Use historical trends for forecasting.*

117. **Describe a situation where denormalization was the right choice. What trade-offs did you make?**

     *Key points: Example: adding `order_total` to orders table instead of computing from order_items. Trade-offs: faster reads, simpler queries vs. data redundancy, need to keep in sync, more complex writes.*

118. **How do you test database changes before deploying to production?**

     *Key points: Use staging environment with production-like data volume. Run migrations in CI/CD pipeline. Test with EXPLAIN ANALYZE. Use database testing frameworks (pgTAP, tSQLt). Performance test with realistic data sizes.*

119. **How would you design a rate-limiting system using a database?**

     *Key points: Use a counter table (user_id, endpoint, window_start, count). Increment with atomic UPDATE. Check count before allowing request. For high throughput, use Redis instead. PostgreSQL advisory locks for distributed rate limiting.*

120. **What's your experience with ORMs vs. raw SQL? When would you choose one over the other?**

     *Key points: ORMs for: rapid development, CRUD operations, migration management, type safety. Raw SQL for: complex queries, performance-critical operations, bulk operations, reporting. Best practice: use ORM for 80%, raw SQL for 20%.*
