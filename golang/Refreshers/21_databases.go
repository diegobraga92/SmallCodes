/*
================================================================================
GOLANG DATABASES & PERSISTENCE - JUNIOR TO SENIOR CONCEPTS
================================================================================
This comprehensive example demonstrates database operations in Go, from basic
SQL to advanced patterns, ORMs, NoSQL, and best practices.
*/

package main

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"time"
	// SQL Drivers (commented - actual imports would be based on chosen DB)
	// _ "github.com/lib/pq"                   // PostgreSQL
	// _ "github.com/go-sql-driver/mysql"      // MySQL
	// _ "modernc.org/sqlite"                  // SQLite (pure Go)
	// ORM and query builders
	// "github.com/jmoiron/sqlx"               // sqlx - extended SQL package
	// "gorm.io/gorm"                         // GORM - full ORM
	// NoSQL clients
	// "go.mongodb.org/mongo-driver/mongo"    // MongoDB official driver
	// "github.com/go-redis/redis/v8"         // Redis client
	// Migration tools
	// "github.com/golang-migrate/migrate/v4" // Database migrations
)

/*
-------------------------------------------------------------------------------
1. SQL BASICS WITH GO - database/sql PACKAGE
-------------------------------------------------------------------------------
Go's database/sql package provides a generic interface for SQL databases.
It's minimal, safe, and forces explicit handling of connections and errors.
*/

// Database configurations
type DBConfig struct {
	Driver   string
	Host     string
	Port     int
	User     string
	Password string
	DBName   string
	SSLMode  string // PostgreSQL specific
	Params   map[string]string
}

// Example configurations
var (
	postgresConfig = DBConfig{
		Driver:   "postgres",
		Host:     "localhost",
		Port:     5432,
		User:     "postgres",
		Password: "password",
		DBName:   "mydb",
		SSLMode:  "disable",
	}

	mysqlConfig = DBConfig{
		Driver:   "mysql",
		Host:     "localhost",
		Port:     3306,
		User:     "root",
		Password: "password",
		DBName:   "mydb",
		Params: map[string]string{
			"parseTime": "true",
			"charset":   "utf8mb4",
		},
	}

	sqliteConfig = DBConfig{
		Driver: "sqlite3",
		DBName: "./data.db",
		Params: map[string]string{
			"_journal_mode": "WAL",
			"_cache_size":   "10000",
		},
	}
)

// Domain models
type User struct {
	ID        int64     `db:"id" json:"id"`
	Username  string    `db:"username" json:"username"`
	Email     string    `db:"email" json:"email"`
	Age       int       `db:"age" json:"age"`
	Active    bool      `db:"active" json:"active"`
	CreatedAt time.Time `db:"created_at" json:"created_at"`
	UpdatedAt time.Time `db:"updated_at" json:"updated_at"`
}

type Order struct {
	ID        int64     `db:"id" json:"id"`
	UserID    int64     `db:"user_id" json:"user_id"`
	Amount    float64   `db:"amount" json:"amount"`
	Status    string    `db:"status" json:"status"`
	CreatedAt time.Time `db:"created_at" json:"created_at"`
}

type Product struct {
	ID          int64   `db:"id" json:"id"`
	Name        string  `db:"name" json:"name"`
	Description string  `db:"description" json:"description"`
	Price       float64 `db:"price" json:"price"`
	Stock       int     `db:"stock" json:"stock"`
}

/*
-------------------------------------------------------------------------------
2. DATABASE/SQL - BASIC OPERATIONS
-------------------------------------------------------------------------------
*/

// Database represents a wrapper around sql.DB with helper methods
type Database struct {
	*sql.DB
	driver string
}

// NewDatabase creates and configures a database connection
func NewDatabase(config DBConfig) (*Database, error) {
	// Build DSN based on driver
	var dsn string
	switch config.Driver {
	case "postgres":
		dsn = fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=%s",
			config.Host, config.Port, config.User, config.Password, config.DBName, config.SSLMode)
	case "mysql":
		params := ""
		for k, v := range config.Params {
			if params != "" {
				params += "&"
			}
			params += fmt.Sprintf("%s=%s", k, v)
		}
		dsn = fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?%s",
			config.User, config.Password, config.Host, config.Port, config.DBName, params)
	case "sqlite3":
		dsn = config.DBName
	default:
		return nil, fmt.Errorf("unsupported driver: %s", config.Driver)
	}

	// Open connection (doesn't actually connect yet - lazy initialization)
	db, err := sql.Open(config.Driver, dsn)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	// Configure connection pool (IMPORTANT!)
	configureConnectionPool(db)

	// Verify connection
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := db.PingContext(ctx); err != nil {
		db.Close()
		return nil, fmt.Errorf("failed to ping database: %w", err)
	}

	return &Database{DB: db, driver: config.Driver}, nil
}

func configureConnectionPool(db *sql.DB) {
	// Set maximum number of open connections
	db.SetMaxOpenConns(25)

	// Set maximum number of idle connections
	db.SetMaxIdleConns(10)

	// Set maximum lifetime of a connection
	db.SetConnMaxLifetime(5 * time.Minute)

	// Set maximum idle time
	db.SetConnMaxIdleTime(1 * time.Minute)
}

// Basic CRUD operations using database/sql
func (db *Database) CreateUser(user *User) error {
	query := `
		INSERT INTO users (username, email, age, active, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6)
		RETURNING id
	`

	now := time.Now()
	user.CreatedAt = now
	user.UpdatedAt = now

	// Use QueryRow for single row insert with RETURNING
	err := db.QueryRow(
		query,
		user.Username,
		user.Email,
		user.Age,
		user.Active,
		user.CreatedAt,
		user.UpdatedAt,
	).Scan(&user.ID)

	if err != nil {
		return fmt.Errorf("failed to create user: %w", err)
	}

	return nil
}

func (db *Database) GetUserByID(id int64) (*User, error) {
	query := `
		SELECT id, username, email, age, active, created_at, updated_at
		FROM users
		WHERE id = $1
	`

	user := &User{}
	err := db.QueryRow(query, id).Scan(
		&user.ID,
		&user.Username,
		&user.Email,
		&user.Age,
		&user.Active,
		&user.CreatedAt,
		&user.UpdatedAt,
	)

	if err != nil {
		if err == sql.ErrNoRows {
			return nil, fmt.Errorf("user not found: %w", err)
		}
		return nil, fmt.Errorf("failed to get user: %w", err)
	}

	return user, nil
}

func (db *Database) GetUsers(limit, offset int) ([]User, error) {
	query := `
		SELECT id, username, email, age, active, created_at, updated_at
		FROM users
		ORDER BY created_at DESC
		LIMIT $1 OFFSET $2
	`

	rows, err := db.Query(query, limit, offset)
	if err != nil {
		return nil, fmt.Errorf("failed to query users: %w", err)
	}
	defer rows.Close()

	var users []User
	for rows.Next() {
		var user User
		err := rows.Scan(
			&user.ID,
			&user.Username,
			&user.Email,
			&user.Age,
			&user.Active,
			&user.CreatedAt,
			&user.UpdatedAt,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan user: %w", err)
		}
		users = append(users, user)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("rows error: %w", err)
	}

	return users, nil
}

func (db *Database) UpdateUser(user *User) error {
	query := `
		UPDATE users
		SET username = $1, email = $2, age = $3, active = $4, updated_at = $5
		WHERE id = $6
	`

	user.UpdatedAt = time.Now()
	result, err := db.Exec(
		query,
		user.Username,
		user.Email,
		user.Age,
		user.Active,
		user.UpdatedAt,
		user.ID,
	)

	if err != nil {
		return fmt.Errorf("failed to update user: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return fmt.Errorf("user not found")
	}

	return nil
}

func (db *Database) DeleteUser(id int64) error {
	query := `DELETE FROM users WHERE id = $1`

	result, err := db.Exec(query, id)
	if err != nil {
		return fmt.Errorf("failed to delete user: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return fmt.Errorf("user not found")
	}

	return nil
}

/*
-------------------------------------------------------------------------------
3. CONNECTION POOLING IN PRACTICE
-------------------------------------------------------------------------------
database/sql has built-in connection pooling. Key configurations:
*/

func demonstrateConnectionPooling() {
	fmt.Println("\n=== Connection Pooling Best Practices ===")

	// Connection pool metrics example
	type PoolStats struct {
		OpenConnections   int
		InUse             int
		Idle              int
		WaitCount         int64
		WaitDuration      time.Duration
		MaxIdleClosed     int64
		MaxLifetimeClosed int64
	}

	// Monitor pool stats periodically
	go func() {
		ticker := time.NewTicker(30 * time.Second)
		defer ticker.Stop()

		for range ticker.C {
			stats := sql.DBStats{}
			// In real code, you'd get stats from your db instance
			fmt.Printf("Pool Stats: %+v\n", stats)
		}
	}()
}

/*
-------------------------------------------------------------------------------
4. TRANSACTIONS - ACID OPERATIONS
-------------------------------------------------------------------------------
Transactions ensure data integrity across multiple operations.
*/

func (db *Database) CreateOrderWithTransaction(userID int64, items []OrderItem) (*Order, error) {
	// Start transaction
	tx, err := db.Begin()
	if err != nil {
		return nil, fmt.Errorf("failed to begin transaction: %w", err)
	}

	// Defer rollback in case of error
	defer func() {
		if err != nil {
			tx.Rollback()
		}
	}()

	// Create order
	order := &Order{
		UserID:    userID,
		Amount:    0, // Will be calculated
		Status:    "pending",
		CreatedAt: time.Now(),
	}

	query := `
		INSERT INTO orders (user_id, amount, status, created_at)
		VALUES ($1, $2, $3, $4)
		RETURNING id
	`

	err = tx.QueryRow(
		query,
		order.UserID,
		order.Amount,
		order.Status,
		order.CreatedAt,
	).Scan(&order.ID)
	if err != nil {
		return nil, fmt.Errorf("failed to create order: %w", err)
	}

	// Add order items and calculate total
	var totalAmount float64
	for _, item := range items {
		// Get product price
		var price float64
		err = tx.QueryRow("SELECT price FROM products WHERE id = $1", item.ProductID).Scan(&price)
		if err != nil {
			return nil, fmt.Errorf("failed to get product price: %w", err)
		}

		// Check stock
		var stock int
		err = tx.QueryRow("SELECT stock FROM products WHERE id = $1 FOR UPDATE", item.ProductID).Scan(&stock)
		if err != nil {
			return nil, fmt.Errorf("failed to check stock: %w", err)
		}

		if stock < item.Quantity {
			return nil, fmt.Errorf("insufficient stock for product %d", item.ProductID)
		}

		// Update stock
		_, err = tx.Exec(
			"UPDATE products SET stock = stock - $1 WHERE id = $2",
			item.Quantity,
			item.ProductID,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to update stock: %w", err)
		}

		// Add order item
		_, err = tx.Exec(
			"INSERT INTO order_items (order_id, product_id, quantity, price) VALUES ($1, $2, $3, $4)",
			order.ID,
			item.ProductID,
			item.Quantity,
			price,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to add order item: %w", err)
		}

		totalAmount += price * float64(item.Quantity)
	}

	// Update order total
	_, err = tx.Exec("UPDATE orders SET amount = $1 WHERE id = $2", totalAmount, order.ID)
	if err != nil {
		return nil, fmt.Errorf("failed to update order amount: %w", err)
	}

	// Commit transaction
	if err := tx.Commit(); err != nil {
		return nil, fmt.Errorf("failed to commit transaction: %w", err)
	}

	order.Amount = totalAmount
	return order, nil
}

// Transaction isolation levels (PostgreSQL example)
func (db *Database) TransferFundsWithIsolation(from, to int64, amount float64) error {
	tx, err := db.BeginTx(context.Background(), &sql.TxOptions{
		Isolation: sql.LevelSerializable, // Highest isolation level
		ReadOnly:  false,
	})
	if err != nil {
		return fmt.Errorf("failed to begin transaction: %w", err)
	}

	defer func() {
		if err != nil {
			tx.Rollback()
		}
	}()

	// Check sender balance
	var balance float64
	err = tx.QueryRow("SELECT balance FROM accounts WHERE id = $1", from).Scan(&balance)
	if err != nil {
		return fmt.Errorf("failed to get sender balance: %w", err)
	}

	if balance < amount {
		return errors.New("insufficient funds")
	}

	// Deduct from sender
	_, err = tx.Exec("UPDATE accounts SET balance = balance - $1 WHERE id = $2", amount, from)
	if err != nil {
		return fmt.Errorf("failed to deduct from sender: %w", err)
	}

	// Add to receiver
	_, err = tx.Exec("UPDATE accounts SET balance = balance + $1 WHERE id = $2", amount, to)
	if err != nil {
		return fmt.Errorf("failed to add to receiver: %w", err)
	}

	// Add transaction record
	_, err = tx.Exec(
		"INSERT INTO transactions (from_account, to_account, amount) VALUES ($1, $2, $3)",
		from, to, amount,
	)
	if err != nil {
		return fmt.Errorf("failed to record transaction: %w", err)
	}

	return tx.Commit()
}

type OrderItem struct {
	ProductID int64
	Quantity  int
}

/*
-------------------------------------------------------------------------------
5. PREPARED STATEMENTS - PERFORMANCE & SECURITY
-------------------------------------------------------------------------------
Prepared statements improve performance and prevent SQL injection.
*/

type PreparedStatements struct {
	createUser   *sql.Stmt
	getUserByID  *sql.Stmt
	updateUser   *sql.Stmt
	deleteUser   *sql.Stmt
	getUsersPage *sql.Stmt
}

func (db *Database) PrepareStatements() (*PreparedStatements, error) {
	var err error
	ps := &PreparedStatements{}

	// Prepare all statements
	ps.createUser, err = db.Prepare(`
		INSERT INTO users (username, email, age, active, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6)
		RETURNING id
	`)
	if err != nil {
		return nil, fmt.Errorf("failed to prepare createUser: %w", err)
	}

	ps.getUserByID, err = db.Prepare(`
		SELECT id, username, email, age, active, created_at, updated_at
		FROM users
		WHERE id = $1
	`)
	if err != nil {
		return nil, fmt.Errorf("failed to prepare getUserByID: %w", err)
	}

	ps.updateUser, err = db.Prepare(`
		UPDATE users
		SET username = $1, email = $2, age = $3, active = $4, updated_at = $5
		WHERE id = $6
	`)
	if err != nil {
		return nil, fmt.Errorf("failed to prepare updateUser: %w", err)
	}

	ps.deleteUser, err = db.Prepare(`DELETE FROM users WHERE id = $1`)
	if err != nil {
		return nil, fmt.Errorf("failed to prepare deleteUser: %w", err)
	}

	ps.getUsersPage, err = db.Prepare(`
		SELECT id, username, email, age, active, created_at, updated_at
		FROM users
		ORDER BY created_at DESC
		LIMIT $1 OFFSET $2
	`)
	if err != nil {
		return nil, fmt.Errorf("failed to prepare getUsersPage: %w", err)
	}

	return ps, nil
}

// Using prepared statements
func (ps *PreparedStatements) CreateUserPrepared(user *User) error {
	now := time.Now()
	user.CreatedAt = now
	user.UpdatedAt = now

	err := ps.createUser.QueryRow(
		user.Username,
		user.Email,
		user.Age,
		user.Active,
		user.CreatedAt,
		user.UpdatedAt,
	).Scan(&user.ID)

	if err != nil {
		return fmt.Errorf("failed to create user with prepared statement: %w", err)
	}

	return nil
}

/*
-------------------------------------------------------------------------------
6. MIGRATIONS - DATABASE SCHEMA MANAGEMENT
-------------------------------------------------------------------------------
*/

// Migration represents a database schema change
type Migration struct {
	Version int
	Name    string
	Up      string
	Down    string
}

var migrations = []Migration{
	{
		Version: 1,
		Name:    "create_users_table",
		Up: `
			CREATE TABLE users (
				id SERIAL PRIMARY KEY,
				username VARCHAR(100) UNIQUE NOT NULL,
				email VARCHAR(255) UNIQUE NOT NULL,
				age INTEGER NOT NULL,
				active BOOLEAN DEFAULT true,
				created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
				updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
			);
			
			CREATE INDEX idx_users_email ON users(email);
			CREATE INDEX idx_users_created_at ON users(created_at);
		`,
		Down: `DROP TABLE users;`,
	},
	{
		Version: 2,
		Name:    "create_orders_table",
		Up: `
			CREATE TABLE orders (
				id SERIAL PRIMARY KEY,
				user_id INTEGER REFERENCES users(id),
				amount DECIMAL(10, 2) NOT NULL,
				status VARCHAR(50) DEFAULT 'pending',
				created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
			);
			
			CREATE INDEX idx_orders_user_id ON orders(user_id);
			CREATE INDEX idx_orders_status ON orders(status);
		`,
		Down: `DROP TABLE orders;`,
	},
	{
		Version: 3,
		Name:    "add_phone_to_users",
		Up:      `ALTER TABLE users ADD COLUMN phone VARCHAR(20);`,
		Down:    `ALTER TABLE users DROP COLUMN phone;`,
	},
}

type Migrator struct {
	db *Database
}

func NewMigrator(db *Database) *Migrator {
	return &Migrator{db: db}
}

func (m *Migrator) CreateMigrationsTable() error {
	query := `
		CREATE TABLE IF NOT EXISTS migrations (
			version INTEGER PRIMARY KEY,
			name VARCHAR(255) NOT NULL,
			applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
		)
	`
	_, err := m.db.Exec(query)
	return err
}

func (m *Migrator) GetAppliedMigrations() (map[int]bool, error) {
	applied := make(map[int]bool)

	rows, err := m.db.Query("SELECT version FROM migrations ORDER BY version")
	if err != nil {
		// Table might not exist yet
		return applied, nil
	}
	defer rows.Close()

	for rows.Next() {
		var version int
		if err := rows.Scan(&version); err != nil {
			return nil, err
		}
		applied[version] = true
	}

	return applied, rows.Err()
}

func (m *Migrator) Migrate() error {
	// Create migrations table if not exists
	if err := m.CreateMigrationsTable(); err != nil {
		return fmt.Errorf("failed to create migrations table: %w", err)
	}

	// Get already applied migrations
	applied, err := m.GetAppliedMigrations()
	if err != nil {
		return fmt.Errorf("failed to get applied migrations: %w", err)
	}

	// Apply migrations in order
	for _, migration := range migrations {
		if applied[migration.Version] {
			fmt.Printf("Migration %d (%s) already applied\n", migration.Version, migration.Name)
			continue
		}

		// Start transaction for each migration
		tx, err := m.db.Begin()
		if err != nil {
			return fmt.Errorf("failed to begin transaction for migration %d: %w", migration.Version, err)
		}

		// Apply migration
		if _, err := tx.Exec(migration.Up); err != nil {
			tx.Rollback()
			return fmt.Errorf("failed to apply migration %d (%s): %w", migration.Version, migration.Name, err)
		}

		// Record migration
		if _, err := tx.Exec(
			"INSERT INTO migrations (version, name) VALUES ($1, $2)",
			migration.Version,
			migration.Name,
		); err != nil {
			tx.Rollback()
			return fmt.Errorf("failed to record migration %d: %w", migration.Version, err)
		}

		// Commit
		if err := tx.Commit(); err != nil {
			return fmt.Errorf("failed to commit migration %d: %w", migration.Version, err)
		}

		fmt.Printf("Applied migration %d: %s\n", migration.Version, migration.Name)
	}

	return nil
}

/*
-------------------------------------------------------------------------------
7. NOSQL BASICS - MONGODB CONCEPTS
-------------------------------------------------------------------------------
*/

// MongoDB document structures
type MongoUser struct {
	ID        string    `bson:"_id,omitempty" json:"id"`
	Username  string    `bson:"username" json:"username"`
	Email     string    `bson:"email" json:"email"`
	Profile   Profile   `bson:"profile" json:"profile"`
	Settings  Settings  `bson:"settings" json:"settings"`
	CreatedAt time.Time `bson:"created_at" json:"created_at"`
	UpdatedAt time.Time `bson:"updated_at" json:"updated_at"`
}

type Profile struct {
	FirstName string   `bson:"first_name" json:"first_name"`
	LastName  string   `bson:"last_name" json:"last_name"`
	Age       int      `bson:"age" json:"age"`
	Interests []string `bson:"interests" json:"interests"`
	Address   Address  `bson:"address" json:"address"`
}

type Address struct {
	Street  string `bson:"street" json:"street"`
	City    string `bson:"city" json:"city"`
	Country string `bson:"country" json:"country"`
	ZipCode string `bson:"zip_code" json:"zip_code"`
}

type Settings struct {
	EmailNotifications bool `bson:"email_notifications" json:"email_notifications"`
	SMSNotifications   bool `bson:"sms_notifications" json:"sms_notifications"`
	TwoFactorAuth      bool `bson:"two_factor_auth" json:"two_factor_auth"`
}

// MongoDB repository interface
type MongoDBRepository interface {
	Insert(ctx context.Context, collection string, document interface{}) (string, error)
	FindByID(ctx context.Context, collection string, id string, result interface{}) error
	FindOne(ctx context.Context, collection string, filter interface{}, result interface{}) error
	Find(ctx context.Context, collection string, filter interface{}, results interface{}) error
	UpdateOne(ctx context.Context, collection string, filter, update interface{}) (int64, error)
	DeleteOne(ctx context.Context, collection string, filter interface{}) (int64, error)
	Aggregate(ctx context.Context, collection string, pipeline interface{}, results interface{}) error
}

/*
-------------------------------------------------------------------------------
8. REDIS BASICS - CACHING & SESSIONS
-------------------------------------------------------------------------------
*/

// Redis repository interface
type RedisRepository interface {
	Set(ctx context.Context, key string, value interface{}, expiration time.Duration) error
	Get(ctx context.Context, key string) (string, error)
	GetStruct(ctx context.Context, key string, result interface{}) error
	Delete(ctx context.Context, keys ...string) (int64, error)
	Exists(ctx context.Context, keys ...string) (int64, error)
	Incr(ctx context.Context, key string) (int64, error)
	Decr(ctx context.Context, key string) (int64, error)
	HSet(ctx context.Context, key string, values ...interface{}) error
	HGet(ctx context.Context, key, field string) (string, error)
	HGetAll(ctx context.Context, key string) (map[string]string, error)
	LPush(ctx context.Context, key string, values ...interface{}) error
	LRange(ctx context.Context, key string, start, stop int64) ([]string, error)
	SAdd(ctx context.Context, key string, members ...interface{}) error
	SMembers(ctx context.Context, key string) ([]string, error)
	ZAdd(ctx context.Context, key string, members ...*Z) error
	ZRange(ctx context.Context, key string, start, stop int64) ([]string, error)
	Expire(ctx context.Context, key string, expiration time.Duration) error
	Pipeline() Pipeline
}

type Z struct {
	Score  float64
	Member interface{}
}

type Pipeline interface {
	Set(key string, value interface{}, expiration time.Duration)
	Get(key string)
	Exec(ctx context.Context) ([]interface{}, error)
}

// Cache implementation using Redis
type Cache struct {
	redis RedisRepository
	ttl   time.Duration
}

func NewCache(redis RedisRepository, ttl time.Duration) *Cache {
	return &Cache{redis: redis, ttl: ttl}
}

func (c *Cache) GetOrSet(ctx context.Context, key string, fn func() (interface{}, error)) (string, error) {
	// Try to get from cache
	val, err := c.redis.Get(ctx, key)
	if err == nil && val != "" {
		return val, nil
	}

	// Execute function to get data
	data, err := fn()
	if err != nil {
		return "", err
	}

	// Marshal to JSON
	jsonData, err := json.Marshal(data)
	if err != nil {
		return "", err
	}

	// Store in cache
	err = c.redis.Set(ctx, key, string(jsonData), c.ttl)
	if err != nil {
		// Log but don't fail if cache set fails
		fmt.Printf("Failed to set cache key %s: %v\n", key, err)
	}

	return string(jsonData), nil
}

func (c *Cache) InvalidatePattern(ctx context.Context, pattern string) error {
	// Note: Redis doesn't have a direct pattern delete.
	// In real implementation, you might use SCAN or maintain a set of keys.
	return nil
}

/*
-------------------------------------------------------------------------------
9. ORM VS QUERY BUILDERS
-------------------------------------------------------------------------------
*/

// GORM example (commented - actual implementation would require GORM import)
type GORMRepository struct {
	// db *gorm.DB
}

func (r *GORMRepository) CreateUser(user *User) error {
	// Example GORM usage:
	// result := r.db.Create(user)
	// return result.Error
	return nil
}

func (r *GORMRepository) GetUserWithOrders(userID int64) (*User, error) {
	// Example GORM eager loading:
	// var user User
	// err := r.db.Preload("Orders").Preload("Orders.Items").First(&user, userID).Error
	// return &user, err
	return nil, nil
}

// SQLx example (commented - actual implementation would require sqlx import)
type SQLxRepository struct {
	// db *sqlx.DB
}

func (r *SQLxRepository) GetUserByEmail(email string) (*User, error) {
	// Example sqlx usage:
	// var user User
	// err := r.db.Get(&user, "SELECT * FROM users WHERE email = $1", email)
	// return &user, err
	return nil, nil
}

func (r *SQLxRepository) GetUsersWithPagination(limit, offset int) ([]User, error) {
	// Example sqlx usage:
	// var users []User
	// err := r.db.Select(&users, "SELECT * FROM users LIMIT $1 OFFSET $2", limit, offset)
	// return users, err
	return nil, nil
}

// Query Builder pattern (simple example)
type QueryBuilder struct {
	table   string
	fields  []string
	wheres  []string
	args    []interface{}
	orderBy string
	limit   int
	offset  int
}

func NewQueryBuilder(table string) *QueryBuilder {
	return &QueryBuilder{table: table}
}

func (qb *QueryBuilder) Select(fields ...string) *QueryBuilder {
	qb.fields = fields
	return qb
}

func (qb *QueryBuilder) Where(condition string, args ...interface{}) *QueryBuilder {
	qb.wheres = append(qb.wheres, condition)
	qb.args = append(qb.args, args...)
	return qb
}

func (qb *QueryBuilder) OrderBy(field string, desc bool) *QueryBuilder {
	order := "ASC"
	if desc {
		order = "DESC"
	}
	qb.orderBy = fmt.Sprintf("%s %s", field, order)
	return qb
}

func (qb *QueryBuilder) Limit(limit int) *QueryBuilder {
	qb.limit = limit
	return qb
}

func (qb *QueryBuilder) Offset(offset int) *QueryBuilder {
	qb.offset = offset
	return qb
}

func (qb *QueryBuilder) Build() (string, []interface{}) {
	// Build SELECT clause
	fields := "*"
	if len(qb.fields) > 0 {
		fields = strings.Join(qb.fields, ", ")
	}

	query := fmt.Sprintf("SELECT %s FROM %s", fields, qb.table)

	// Build WHERE clause
	if len(qb.wheres) > 0 {
		query += " WHERE " + strings.Join(qb.wheres, " AND ")
	}

	// Build ORDER BY clause
	if qb.orderBy != "" {
		query += " ORDER BY " + qb.orderBy
	}

	// Build LIMIT and OFFSET clauses
	if qb.limit > 0 {
		query += fmt.Sprintf(" LIMIT %d", qb.limit)
	}
	if qb.offset > 0 {
		query += fmt.Sprintf(" OFFSET %d", qb.offset)
	}

	return query, qb.args
}

/*
-------------------------------------------------------------------------------
10. REPOSITORY PATTERN - ABSTRACTING DATA ACCESS
-------------------------------------------------------------------------------
*/

// Repository interface defines data access operations
type UserRepository interface {
	Create(ctx context.Context, user *User) error
	GetByID(ctx context.Context, id int64) (*User, error)
	GetByEmail(ctx context.Context, email string) (*User, error)
	Update(ctx context.Context, user *User) error
	Delete(ctx context.Context, id int64) error
	List(ctx context.Context, filter UserFilter, pagination Pagination) ([]User, error)
}

type UserFilter struct {
	Username string
	Email    string
	Active   *bool
	MinAge   int
	MaxAge   int
}

type Pagination struct {
	Limit  int
	Offset int
	SortBy string
	Asc    bool
}

// SQL implementation of UserRepository
type SQLUserRepository struct {
	db *Database
}

func NewSQLUserRepository(db *Database) *SQLUserRepository {
	return &SQLUserRepository{db: db}
}

func (r *SQLUserRepository) Create(ctx context.Context, user *User) error {
	query := `
		INSERT INTO users (username, email, age, active, created_at, updated_at)
		VALUES ($1, $2, $3, $4, $5, $6)
		RETURNING id
	`

	now := time.Now()
	user.CreatedAt = now
	user.UpdatedAt = now

	err := r.db.QueryRowContext(ctx, query,
		user.Username,
		user.Email,
		user.Age,
		user.Active,
		user.CreatedAt,
		user.UpdatedAt,
	).Scan(&user.ID)

	if err != nil {
		return fmt.Errorf("failed to create user: %w", err)
	}

	return nil
}

func (r *SQLUserRepository) GetByID(ctx context.Context, id int64) (*User, error) {
	query := `
		SELECT id, username, email, age, active, created_at, updated_at
		FROM users
		WHERE id = $1
	`

	user := &User{}
	err := r.db.QueryRowContext(ctx, query, id).Scan(
		&user.ID,
		&user.Username,
		&user.Email,
		&user.Age,
		&user.Active,
		&user.CreatedAt,
		&user.UpdatedAt,
	)

	if err != nil {
		if err == sql.ErrNoRows {
			return nil, ErrNotFound
		}
		return nil, fmt.Errorf("failed to get user: %w", err)
	}

	return user, nil
}

func (r *SQLUserRepository) GetByEmail(ctx context.Context, email string) (*User, error) {
	query := `
		SELECT id, username, email, age, active, created_at, updated_at
		FROM users
		WHERE email = $1
	`

	user := &User{}
	err := r.db.QueryRowContext(ctx, query, email).Scan(
		&user.ID,
		&user.Username,
		&user.Email,
		&user.Age,
		&user.Active,
		&user.CreatedAt,
		&user.UpdatedAt,
	)

	if err != nil {
		if err == sql.ErrNoRows {
			return nil, ErrNotFound
		}
		return nil, fmt.Errorf("failed to get user by email: %w", err)
	}

	return user, nil
}

func (r *SQLUserRepository) Update(ctx context.Context, user *User) error {
	query := `
		UPDATE users
		SET username = $1, email = $2, age = $3, active = $4, updated_at = $5
		WHERE id = $6
	`

	user.UpdatedAt = time.Now()
	result, err := r.db.ExecContext(ctx, query,
		user.Username,
		user.Email,
		user.Age,
		user.Active,
		user.UpdatedAt,
		user.ID,
	)

	if err != nil {
		return fmt.Errorf("failed to update user: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return ErrNotFound
	}

	return nil
}

func (r *SQLUserRepository) Delete(ctx context.Context, id int64) error {
	query := `DELETE FROM users WHERE id = $1`

	result, err := r.db.ExecContext(ctx, query, id)
	if err != nil {
		return fmt.Errorf("failed to delete user: %w", err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("failed to get rows affected: %w", err)
	}

	if rowsAffected == 0 {
		return ErrNotFound
	}

	return nil
}

func (r *SQLUserRepository) List(ctx context.Context, filter UserFilter, pagination Pagination) ([]User, error) {
	// Build query dynamically
	query := `
		SELECT id, username, email, age, active, created_at, updated_at
		FROM users
		WHERE 1=1
	`
	args := []interface{}{}
	argPos := 1

	if filter.Username != "" {
		query += fmt.Sprintf(" AND username LIKE $%d", argPos)
		args = append(args, "%"+filter.Username+"%")
		argPos++
	}

	if filter.Email != "" {
		query += fmt.Sprintf(" AND email LIKE $%d", argPos)
		args = append(args, "%"+filter.Email+"%")
		argPos++
	}

	if filter.Active != nil {
		query += fmt.Sprintf(" AND active = $%d", argPos)
		args = append(args, *filter.Active)
		argPos++
	}

	if filter.MinAge > 0 {
		query += fmt.Sprintf(" AND age >= $%d", argPos)
		args = append(args, filter.MinAge)
		argPos++
	}

	if filter.MaxAge > 0 {
		query += fmt.Sprintf(" AND age <= $%d", argPos)
		args = append(args, filter.MaxAge)
		argPos++
	}

	// Add ordering
	if pagination.SortBy != "" {
		order := "ASC"
		if !pagination.Asc {
			order = "DESC"
		}
		query += fmt.Sprintf(" ORDER BY %s %s", pagination.SortBy, order)
	} else {
		query += " ORDER BY created_at DESC"
	}

	// Add pagination
	if pagination.Limit > 0 {
		query += fmt.Sprintf(" LIMIT $%d", argPos)
		args = append(args, pagination.Limit)
		argPos++
	}

	if pagination.Offset > 0 {
		query += fmt.Sprintf(" OFFSET $%d", argPos)
		args = append(args, pagination.Offset)
	}

	// Execute query
	rows, err := r.db.QueryContext(ctx, query, args...)
	if err != nil {
		return nil, fmt.Errorf("failed to query users: %w", err)
	}
	defer rows.Close()

	var users []User
	for rows.Next() {
		var user User
		err := rows.Scan(
			&user.ID,
			&user.Username,
			&user.Email,
			&user.Age,
			&user.Active,
			&user.CreatedAt,
			&user.UpdatedAt,
		)
		if err != nil {
			return nil, fmt.Errorf("failed to scan user: %w", err)
		}
		users = append(users, user)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("rows error: %w", err)
	}

	return users, nil
}

var ErrNotFound = errors.New("not found")

/*
-------------------------------------------------------------------------------
MAIN DEMONSTRATION
-------------------------------------------------------------------------------
*/

func main() {
	fmt.Println("=== Go Databases & Persistence Examples ===")

	// In a real application, you would:
	// 1. Load configuration from environment or config file
	// 2. Initialize database connection
	// 3. Run migrations
	// 4. Start application

	// Example workflow:
	demoWorkflow()
}

func demoWorkflow() {
	fmt.Println("\n=== Database Workflow Demonstration ===")

	// 1. Database setup (simulated)
	fmt.Println("1. Setting up database connection...")

	// In real code:
	// db, err := NewDatabase(postgresConfig)
	// if err != nil { log.Fatal(err) }
	// defer db.Close()

	// 2. Run migrations
	fmt.Println("2. Running migrations...")
	// migrator := NewMigrator(db)
	// if err := migrator.Migrate(); err != nil { log.Fatal(err) }

	// 3. Create repository
	fmt.Println("3. Creating repository...")
	// repo := NewSQLUserRepository(db)

	// 4. Demonstrate CRUD operations
	fmt.Println("4. Demonstrating CRUD operations...")
	demoCRUDOperations()

	// 5. Demonstrate transactions
	fmt.Println("5. Demonstrating transactions...")
	demoTransactions()

	// 6. Demonstrate prepared statements
	fmt.Println("6. Demonstrating prepared statements...")
	demoPreparedStatements()

	// 7. Demonstrate connection pooling
	fmt.Println("7. Demonstrating connection pooling...")
	demoConnectionPooling()

	// 8. Demonstrate query builder
	fmt.Println("8. Demonstrating query builder...")
	demoQueryBuilder()

	fmt.Println("\n=== Workflow Complete ===")
}

func demoCRUDOperations() {
	// Simulated operations
	fmt.Println("  • Create user")
	fmt.Println("  • Read user")
	fmt.Println("  • Update user")
	fmt.Println("  • Delete user")
	fmt.Println("  • List users with pagination")
}

func demoTransactions() {
	fmt.Println("  • Transfer funds with serializable isolation")
	fmt.Println("  • Create order with inventory check")
	fmt.Println("  • Bulk operations with rollback on error")
}

func demoPreparedStatements() {
	fmt.Println("  • Prepare common queries")
	fmt.Println("  • Execute with parameters")
	fmt.Println("  • Reuse statements for performance")
}

func demoConnectionPooling() {
	fmt.Println("  • Configure max open connections: 25")
	fmt.Println("  • Configure max idle connections: 10")
	fmt.Println("  • Configure connection lifetime: 5 minutes")
	fmt.Println("  • Monitor pool statistics")
}

func demoQueryBuilder() {
	qb := NewQueryBuilder("users").
		Select("id", "username", "email").
		Where("active = ?", true).
		Where("age >= ?", 18).
		OrderBy("created_at", true).
		Limit(10).
		Offset(0)

	query, args := qb.Build()
	fmt.Printf("  Built query: %s\n", query)
	fmt.Printf("  Args: %v\n", args)
}

func printBestPractices() {
	fmt.Println("\n" + string(os.PathSeparator) + strings.Repeat("=", 70))
	fmt.Println("DATABASE BEST PRACTICES")
	fmt.Println(strings.Repeat("=", 70))

	practices := []struct {
		Area     string
		Practice string
	}{
		{"Connections", "Use connection pooling with appropriate limits"},
		{"Errors", "Always check and handle database errors"},
		{"Security", "Use prepared statements to prevent SQL injection"},
		{"Performance", "Create indexes on frequently queried columns"},
		{"Transactions", "Use transactions for multiple related operations"},
		{"Timeouts", "Always use context with timeouts for database operations"},
		{"Monitoring", "Log slow queries and monitor connection pool health"},
		{"Migrations", "Use migration tools for schema changes"},
		{"Testing", "Test with transaction rollback or test database"},
		{"Backups", "Regularly backup and test restore procedures"},
	}

	for _, p := range practices {
		fmt.Printf("\n%-20s: %s", p.Area, p.Practice)
	}

	fmt.Println("\n\n" + strings.Repeat("=", 70))
	fmt.Println("TOOL RECOMMENDATIONS")
	fmt.Println(strings.Repeat("=", 70))

	tools := []struct {
		Category string
		Tool     string
		Purpose  string
	}{
		{"SQL Drivers", "lib/pq, go-sql-driver/mysql, modernc.org/sqlite", "Database connectivity"},
		{"Query Builders", "sqlx", "Extended SQL functionality"},
		{"ORMs", "GORM", "Full ORM with relationships"},
		{"NoSQL", "mongo-driver, go-redis", "MongoDB and Redis clients"},
		{"Migrations", "golang-migrate/migrate", "Database schema management"},
		{"Testing", "testcontainers-go", "Docker-based test databases"},
		{"Monitoring", "prometheus, grafana", "Query performance monitoring"},
	}

	for _, t := range tools {
		fmt.Printf("\n%-15s: %-30s - %s", t.Category, t.Tool, t.Purpose)
	}
}

// Helper function for string operations
var strings struct {
	Join  func(elems []string, sep string) string
	Split func(s, sep string) []string
}

// Note: The actual code would require proper imports and implementations
// This example serves as a comprehensive guide and template for real implementations
