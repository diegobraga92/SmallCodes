/*
   BEYOND SQL - NoSQL, NewSQL, Polyglot Persistence
   File: 21_beyond_sql.sql

   While SQL databases excel at structured data with relationships,
   other database types are better suited for specific use cases.
   This file covers when to go beyond traditional SQL.
*/

-- ============================================================================
-- 1. SQL vs NoSQL OVERVIEW
-- ============================================================================

/*
   SQL Databases (Relational):
   - Structured schema (tables, columns, types)
   - ACID transactions
   - Strong consistency
   - Complex queries (JOINs, aggregations)
   - Examples: PostgreSQL, MySQL, SQL Server, SQLite

   NoSQL Databases:
   - Flexible/ schema-less
   - BASE (Basically Available, Soft state, Eventually consistent)
   - Horizontal scaling
   - Specialized for specific data models
   - Examples: MongoDB, Redis, Cassandra, Neo4j
*/

-- ============================================================================
-- 2. DOCUMENT DATABASES (MongoDB, Couchbase)
-- ============================================================================

/*
   Data model: JSON-like documents
   Best for: Content management, catalogs, event logging
   Strengths: Schema flexibility, nested data, horizontal scaling
   Weaknesses: Complex joins, multi-document transactions

   When to use:
   - Rapidly evolving schema
   - Hierarchical/nested data
   - Prototyping and MVPs
   - Content management systems

   When to avoid:
   - Highly relational data
   - Complex transactions across entities
   - Strict consistency requirements
*/

-- ============================================================================
-- 3. KEY-VALUE STORES (Redis, DynamoDB, Riak)
-- ============================================================================

/*
   Data model: Key → Value (simple lookup)
   Best for: Caching, session management, real-time data
   Strengths: Extremely fast, simple, scalable
   Weaknesses: Limited query capabilities

   Redis special features:
   - In-memory (sub-millisecond latency)
   - Data structures: strings, hashes, lists, sets, sorted sets
   - Pub/Sub messaging
   - TTL (time-to-live) for automatic expiration
   - Persistence options (RDB, AOF)

   When to use:
   - Caching layer
   - Session storage
   - Rate limiting
   - Real-time leaderboards
   - Message queues
*/

-- ============================================================================
-- 4. COLUMN-FAMILY STORES (Cassandra, HBase)
-- ============================================================================

/*
   Data model: Wide-column store (rows with many columns)
   Best for: Time-series data, IoT, large-scale analytics
   Strengths: Massive scalability, high write throughput
   Weaknesses: No JOINs, limited query patterns

   When to use:
   - Time-series data (metrics, logs)
   - IoT sensor data
   - Recommendation engines
   - Large-scale write-heavy workloads

   When to avoid:
   - Complex queries
   - Ad-hoc reporting
   - Strong consistency requirements
*/

-- ============================================================================
-- 5. GRAPH DATABASES (Neo4j, ArangoDB)
-- ============================================================================

/*
   Data model: Nodes (entities) and Edges (relationships)
   Best for: Social networks, recommendation engines, fraud detection
   Strengths: Relationship traversal, graph algorithms
   Weaknesses: Not good for tabular data, aggregations

   When to use:
   - Social networks (friends, followers)
   - Recommendation engines
   - Fraud detection (pattern analysis)
   - Network/infrastructure mapping
   - Knowledge graphs

   When to avoid:
   - Simple CRUD applications
   - Aggregation-heavy reporting
*/

-- ============================================================================
-- 6. NEWSQL (CockroachDB, YugabyteDB, Spanner)
-- ============================================================================

/*
   NewSQL combines SQL's ACID guarantees with NoSQL's horizontal scaling.

   Features:
   - SQL interface (PostgreSQL-compatible in many cases)
   - ACID transactions across nodes
   - Horizontal scaling
   - Geo-distribution

   When to use:
   - Need SQL + horizontal scaling
   - Global applications (multi-region)
   - Financial systems requiring strong consistency at scale
*/

-- ============================================================================
-- 7. TIME-SERIES DATABASES (InfluxDB, TimescaleDB)
-- ============================================================================

/*
   Specialized for time-stamped data.

   TimescaleDB: PostgreSQL extension (SQL-compatible)
   InfluxDB: Purpose-built, uses its own query language (Flux)

   Features:
   - Automatic data retention policies
   - Continuous aggregations (downsampling)
   - Time-based partitioning
   - Specialized compression

   When to use:
   - Metrics and monitoring
   - IoT sensor data
   - Financial tick data
   - Application performance monitoring
*/

-- ============================================================================
-- 8. FULL-TEXT SEARCH
-- ============================================================================

/*
   Built-in full-text search in SQL databases:

   PostgreSQL: tsvector/tsquery
   MySQL: FULLTEXT index
   SQL Server: FULLTEXT index
   SQLite: FTS5 extension

   For advanced search: Elasticsearch, Meilisearch, Algolia
*/

-- PostgreSQL full-text search:
-- CREATE INDEX idx_articles_fts ON articles
-- USING GIN(to_tsvector('english', title || ' ' || body));

-- SELECT title
-- FROM articles
-- WHERE to_tsvector('english', title || ' ' || body)
--       @@ to_tsquery('english', 'database & performance');

-- ============================================================================
-- 9. POLYGLOT PERSISTENCE
-- ============================================================================

/*
   Using multiple database types in the same application,
   each optimized for its specific use case.

   Example architecture:
   - PostgreSQL: Core business data (users, orders, products)
   - Redis: Session cache, rate limiting
   - Elasticsearch: Full-text search
   - Cassandra: Event logging and analytics
   - Neo4j: Recommendation engine

   Challenges:
   - Data synchronization across systems
   - Transactional consistency across databases
   - Operational complexity
   - Increased infrastructure costs
*/

-- ============================================================================
-- 10. CHOOSING THE RIGHT DATABASE
-- ============================================================================

/*
   Decision framework:

   1. Is the data highly relational?
      YES → SQL database
      NO  → Consider NoSQL

   2. Do you need ACID transactions?
      YES → SQL or NewSQL
      NO  → Consider NoSQL

   3. What's the primary access pattern?
      - Key lookups: Key-value store
      - Complex queries: SQL
      - Graph traversal: Graph database
      - Time-series: Time-series database
      - Full-text search: Search engine

   4. Scale requirements?
      - Single node: Any SQL database
      - Multi-node reads: SQL with read replicas
      - Multi-node writes: NewSQL or NoSQL

   5. Consistency requirements?
      - Strong consistency: SQL, NewSQL
      - Eventual consistency: Most NoSQL
*/

-- ============================================================================
-- END OF 21_beyond_sql.sql
-- ============================================================================
