/*
GO-SPECIFIC PATTERNS & DESIGN PATTERNS IN GO
==============================================
Comprehensive examples covering Go-specific patterns and implementations
of classic design patterns adapted for Go's philosophy.
*/

package main

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"log"
	"net/http"
	"reflect"
	"strings"
	"sync"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

// ============================================================================
// 1. FUNCTIONAL OPTIONS PATTERN (Mid to Senior Level)
// ============================================================================
// The functional options pattern provides a clean way to handle optional
// configuration with sensible defaults, while maintaining readability.

type Server struct {
	host        string
	port        int
	timeout     time.Duration
	maxConn     int
	tlsEnabled  bool
	certFile    string
	keyFile     string
	middlewares []Middleware
	logger      Logger
}

type Middleware func(http.Handler) http.Handler

type Logger interface {
	Infof(format string, args ...interface{})
	Errorf(format string, args ...interface{})
}

type ServerOption func(*Server)

// Functional options
func WithHost(host string) ServerOption {
	return func(s *Server) {
		s.host = host
	}
}

func WithPort(port int) ServerOption {
	return func(s *Server) {
		s.port = port
	}
}

func WithTimeout(timeout time.Duration) ServerOption {
	return func(s *Server) {
		s.timeout = timeout
	}
}

func WithMaxConnections(maxConn int) ServerOption {
	return func(s *Server) {
		s.maxConn = maxConn
	}
}

func WithTLS(certFile, keyFile string) ServerOption {
	return func(s *Server) {
		s.tlsEnabled = true
		s.certFile = certFile
		s.keyFile = keyFile
	}
}

func WithMiddleware(mw Middleware) ServerOption {
	return func(s *Server) {
		s.middlewares = append(s.middlewares, mw)
	}
}

func WithLogger(logger Logger) ServerOption {
	return func(s *Server) {
		s.logger = logger
	}
}

// NewServer creates a new Server with functional options
func NewServer(opts ...ServerOption) *Server {
	// Sensible defaults
	s := &Server{
		host:    "localhost",
		port:    8080,
		timeout: 30 * time.Second,
		maxConn: 100,
		logger:  &DefaultLogger{},
	}

	// Apply all options
	for _, opt := range opts {
		opt(s)
	}

	return s
}

func (s *Server) Start() error {
	s.logger.Infof("Starting server on %s:%d", s.host, s.port)
	s.logger.Infof("Timeout: %v, Max connections: %d", s.timeout, s.maxConn)
	return nil
}

// Mock logger for demonstration
type DefaultLogger struct{}

func (d *DefaultLogger) Infof(format string, args ...interface{}) {
	log.Printf("[INFO] "+format, args...)
}

func (d *DefaultLogger) Errorf(format string, args ...interface{}) {
	log.Printf("[ERROR] "+format, args...)
}

func demonstrateFunctionalOptions() {
	fmt.Println("\n=== 1. FUNCTIONAL OPTIONS PATTERN ===")

	// Basic server with defaults
	server1 := NewServer()
	fmt.Println("Server 1 (defaults):")
	server1.Start()

	// Customized server
	server2 := NewServer(
		WithHost("0.0.0.0"),
		WithPort(9090),
		WithTimeout(60*time.Second),
		WithMaxConnections(500),
		WithMiddleware(func(h http.Handler) http.Handler {
			return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				log.Println("Middleware executed")
				h.ServeHTTP(w, r)
			})
		}),
		WithTLS("cert.pem", "key.pem"),
	)

	fmt.Println("\nServer 2 (customized):")
	server2.Start()

	// Advanced: Configuration struct with functional options
	fmt.Println("\nAdvanced: Configuration Builder Pattern")

	config := NewConfig().
		WithHost("api.example.com").
		WithPort(443).
		WithTimeout(10 * time.Second).
		WithRetries(3).
		Build()

	fmt.Printf("Config: %+v\n", config)
}

// Advanced: Builder pattern combined with functional options
type Config struct {
	Host    string
	Port    int
	Timeout time.Duration
	Retries int
}

type ConfigBuilder struct {
	config Config
}

func NewConfig() *ConfigBuilder {
	return &ConfigBuilder{
		config: Config{
			Host:    "localhost",
			Port:    8080,
			Timeout: 30 * time.Second,
			Retries: 1,
		},
	}
}

func (cb *ConfigBuilder) WithHost(host string) *ConfigBuilder {
	cb.config.Host = host
	return cb
}

func (cb *ConfigBuilder) WithPort(port int) *ConfigBuilder {
	cb.config.Port = port
	return cb
}

func (cb *ConfigBuilder) WithTimeout(timeout time.Duration) *ConfigBuilder {
	cb.config.Timeout = timeout
	return cb
}

func (cb *ConfigBuilder) WithRetries(retries int) *ConfigBuilder {
	cb.config.Retries = retries
	return cb
}

func (cb *ConfigBuilder) Build() Config {
	return cb.config
}

// ============================================================================
// 2. BUILDER PATTERN (Mid Level)
// ============================================================================
// The builder pattern is useful for constructing complex objects step by step.

type Email struct {
	from        string
	to          []string
	cc          []string
	bcc         []string
	subject     string
	body        string
	attachments []string
	priority    string
	headers     map[string]string
}

type EmailBuilder struct {
	email Email
}

func NewEmailBuilder() *EmailBuilder {
	return &EmailBuilder{
		email: Email{
			headers: make(map[string]string),
		},
	}
}

func (eb *EmailBuilder) From(from string) *EmailBuilder {
	eb.email.from = from
	return eb
}

func (eb *EmailBuilder) To(to ...string) *EmailBuilder {
	eb.email.to = append(eb.email.to, to...)
	return eb
}

func (eb *EmailBuilder) Cc(cc ...string) *EmailBuilder {
	eb.email.cc = append(eb.email.cc, cc...)
	return eb
}

func (eb *EmailBuilder) Bcc(bcc ...string) *EmailBuilder {
	eb.email.bcc = append(eb.email.bcc, bcc...)
	return eb
}

func (eb *EmailBuilder) Subject(subject string) *EmailBuilder {
	eb.email.subject = subject
	return eb
}

func (eb *EmailBuilder) Body(body string) *EmailBuilder {
	eb.email.body = body
	return eb
}

func (eb *EmailBuilder) AddAttachment(file string) *EmailBuilder {
	eb.email.attachments = append(eb.email.attachments, file)
	return eb
}

func (eb *EmailBuilder) SetPriority(priority string) *EmailBuilder {
	eb.email.priority = priority
	return eb
}

func (eb *EmailBuilder) AddHeader(key, value string) *EmailBuilder {
	eb.email.headers[key] = value
	return eb
}

func (eb *EmailBuilder) Build() (*Email, error) {
	// Validate email
	if eb.email.from == "" {
		return nil, errors.New("from address is required")
	}
	if len(eb.email.to) == 0 {
		return nil, errors.New("at least one recipient is required")
	}
	if eb.email.subject == "" {
		return nil, errors.New("subject is required")
	}

	return &eb.email, nil
}

// EmailDirector for common email patterns (optional)
type EmailDirector struct{}

func (ed *EmailDirector) BuildWelcomeEmail(user, email string) *EmailBuilder {
	return NewEmailBuilder().
		From("welcome@example.com").
		To(email).
		Subject("Welcome to Our Service!").
		Body(fmt.Sprintf("Dear %s,\n\nWelcome to our platform!", user)).
		AddHeader("X-Email-Type", "welcome")
}

func (ed *EmailDirector) BuildNotificationEmail(to, message string) *EmailBuilder {
	return NewEmailBuilder().
		From("notifications@example.com").
		To(to).
		Subject("Notification").
		Body(message).
		SetPriority("high")
}

func demonstrateBuilderPattern() {
	fmt.Println("\n=== 2. BUILDER PATTERN ===")

	// Build a complex email step by step
	fmt.Println("Building a complex email:")

	email, err := NewEmailBuilder().
		From("sender@example.com").
		To("recipient1@example.com", "recipient2@example.com").
		Cc("manager@example.com").
		Subject("Important Meeting").
		Body("Please join the meeting tomorrow at 10 AM.").
		AddAttachment("agenda.pdf").
		AddHeader("X-Priority", "1").
		Build()

	if err != nil {
		log.Printf("Error building email: %v", err)
	} else {
		fmt.Printf("Email built successfully:\n")
		fmt.Printf("  From: %s\n", email.from)
		fmt.Printf("  To: %v\n", email.to)
		fmt.Printf("  Subject: %s\n", email.subject)
		fmt.Printf("  Attachments: %d\n", len(email.attachments))
	}

	// Using a director for common patterns
	fmt.Println("\nUsing EmailDirector for common patterns:")
	director := &EmailDirector{}

	welcomeEmail := director.BuildWelcomeEmail("John Doe", "john@example.com")
	if email, err := welcomeEmail.Build(); err == nil {
		fmt.Printf("Welcome email: %s\n", email.subject)
	}
}

// ============================================================================
// 3. REPOSITORY PATTERN (Mid to Senior Level)
// ============================================================================
// The repository pattern abstracts data access, making it easier to swap
// data sources and test business logic.

// Domain model
type User struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type Product struct {
	ID       string  `json:"id"`
	Name     string  `json:"name"`
	Price    float64 `json:"price"`
	Category string  `json:"category"`
	InStock  bool    `json:"in_stock"`
}

// Repository interfaces
type UserRepository interface {
	FindByID(ctx context.Context, id string) (*User, error)
	FindByEmail(ctx context.Context, email string) (*User, error)
	FindAll(ctx context.Context, filter UserFilter) ([]*User, error)
	Save(ctx context.Context, user *User) error
	Update(ctx context.Context, user *User) error
	Delete(ctx context.Context, id string) error
	Count(ctx context.Context, filter UserFilter) (int, error)
}

type ProductRepository interface {
	FindByID(ctx context.Context, id string) (*Product, error)
	FindByCategory(ctx context.Context, category string) ([]*Product, error)
	Save(ctx context.Context, product *Product) error
	Update(ctx context.Context, product *Product) error
	Delete(ctx context.Context, id string) error
}

// Filter structs
type UserFilter struct {
	Name  string
	Email string
	Limit int
	Page  int
}

// Concrete implementations

// InMemoryUserRepository - for testing
type InMemoryUserRepository struct {
	mu    sync.RWMutex
	users map[string]*User
}

func NewInMemoryUserRepository() *InMemoryUserRepository {
	return &InMemoryUserRepository{
		users: make(map[string]*User),
	}
}

func (r *InMemoryUserRepository) FindByID(ctx context.Context, id string) (*User, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	user, exists := r.users[id]
	if !exists {
		return nil, fmt.Errorf("user not found: %s", id)
	}
	return user, nil
}

func (r *InMemoryUserRepository) FindByEmail(ctx context.Context, email string) (*User, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	for _, user := range r.users {
		if user.Email == email {
			return user, nil
		}
	}
	return nil, fmt.Errorf("user not found with email: %s", email)
}

func (r *InMemoryUserRepository) FindAll(ctx context.Context, filter UserFilter) ([]*User, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	var users []*User
	for _, user := range r.users {
		// Apply filters
		if filter.Name != "" && !strings.Contains(strings.ToLower(user.Name), strings.ToLower(filter.Name)) {
			continue
		}
		if filter.Email != "" && !strings.Contains(strings.ToLower(user.Email), strings.ToLower(filter.Email)) {
			continue
		}
		users = append(users, user)
	}

	// Apply pagination
	start := filter.Page * filter.Limit
	end := start + filter.Limit
	if start >= len(users) {
		return []*User{}, nil
	}
	if end > len(users) {
		end = len(users)
	}

	return users[start:end], nil
}

func (r *InMemoryUserRepository) Save(ctx context.Context, user *User) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if user.ID == "" {
		user.ID = fmt.Sprintf("user-%d", len(r.users)+1)
	}
	user.CreatedAt = time.Now()
	user.UpdatedAt = time.Now()

	r.users[user.ID] = user
	return nil
}

func (r *InMemoryUserRepository) Update(ctx context.Context, user *User) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.users[user.ID]; !exists {
		return fmt.Errorf("user not found: %s", user.ID)
	}

	user.UpdatedAt = time.Now()
	r.users[user.ID] = user
	return nil
}

func (r *InMemoryUserRepository) Delete(ctx context.Context, id string) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.users[id]; !exists {
		return fmt.Errorf("user not found: %s", id)
	}

	delete(r.users, id)
	return nil
}

func (r *InMemoryUserRepository) Count(ctx context.Context, filter UserFilter) (int, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	count := 0
	for _, user := range r.users {
		if filter.Name != "" && !strings.Contains(strings.ToLower(user.Name), strings.ToLower(filter.Name)) {
			continue
		}
		if filter.Email != "" && !strings.Contains(strings.ToLower(user.Email), strings.ToLower(filter.Email)) {
			continue
		}
		count++
	}

	return count, nil
}

// MySQLUserRepository - for production
type MySQLUserRepository struct {
	db *sql.DB
}

func NewMySQLUserRepository(db *sql.DB) *MySQLUserRepository {
	return &MySQLUserRepository{db: db}
}

func (r *MySQLUserRepository) FindByID(ctx context.Context, id string) (*User, error) {
	query := `SELECT id, name, email, created_at, updated_at FROM users WHERE id = ?`
	row := r.db.QueryRowContext(ctx, query, id)

	var user User
	err := row.Scan(&user.ID, &user.Name, &user.Email, &user.CreatedAt, &user.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("failed to find user: %w", err)
	}

	return &user, nil
}

// Other methods would be implemented similarly...

// Generic Repository with Generics (Go 1.18+)
type Repository[T any] interface {
	FindByID(ctx context.Context, id string) (*T, error)
	Save(ctx context.Context, entity *T) error
	Update(ctx context.Context, entity *T) error
	Delete(ctx context.Context, id string) error
}

type GenericRepository[T any] struct {
	db     *sql.DB
	table  string
	idCol  string
	parser func(*sql.Rows) (*T, error)
}

func NewGenericRepository[T any](db *sql.DB, table, idCol string, parser func(*sql.Rows) (*T, error)) *GenericRepository[T] {
	return &GenericRepository[T]{
		db:     db,
		table:  table,
		idCol:  idCol,
		parser: parser,
	}
}

func (r *GenericRepository[T]) FindByID(ctx context.Context, id string) (*T, error) {
	query := fmt.Sprintf("SELECT * FROM %s WHERE %s = ?", r.table, r.idCol)
	rows, err := r.db.QueryContext(ctx, query, id)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	if !rows.Next() {
		return nil, fmt.Errorf("%s not found", r.table)
	}

	return r.parser(rows)
}

// Service layer using repository
type UserService struct {
	userRepo UserRepository
}

func NewUserService(repo UserRepository) *UserService {
	return &UserService{userRepo: repo}
}

func (s *UserService) RegisterUser(ctx context.Context, name, email string) (*User, error) {
	// Check if email exists
	if _, err := s.userRepo.FindByEmail(ctx, email); err == nil {
		return nil, errors.New("email already registered")
	}

	user := &User{
		Name:  name,
		Email: email,
	}

	if err := s.userRepo.Save(ctx, user); err != nil {
		return nil, fmt.Errorf("failed to save user: %w", err)
	}

	return user, nil
}

func demonstrateRepositoryPattern() {
	fmt.Println("\n=== 3. REPOSITORY PATTERN ===")

	// Create in-memory repository for testing
	repo := NewInMemoryUserRepository()
	service := NewUserService(repo)

	ctx := context.Background()

	// Test the service
	user1, err := service.RegisterUser(ctx, "Alice", "alice@example.com")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Printf("Registered user: %s (%s)\n", user1.Name, user1.ID)
	}

	user2, err := service.RegisterUser(ctx, "Bob", "bob@example.com")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Printf("Registered user: %s (%s)\n", user2.Name, user2.ID)
	}

	// Try to register duplicate email
	_, err = service.RegisterUser(ctx, "Another Alice", "alice@example.com")
	if err != nil {
		fmt.Printf("Expected error: %v\n", err)
	}

	// Find all users
	users, _ := repo.FindAll(ctx, UserFilter{Limit: 10, Page: 0})
	fmt.Printf("Total users: %d\n", len(users))

	// Demonstrate generic repository
	fmt.Println("\nGeneric Repository Pattern (Go 1.18+):")
	fmt.Println("  - Type-safe repositories with generics")
	fmt.Println("  - Reduced boilerplate code")
	fmt.Println("  - Compile-time type checking")
}

// ============================================================================
// 4. WORKER POOLS (Mid to Senior Level)
// ============================================================================
// Worker pools manage concurrent processing of tasks with controlled
// parallelism and graceful shutdown.

type Task struct {
	ID       string
	Payload  interface{}
	Attempts int
	Priority int // Higher number = higher priority
}

type TaskResult struct {
	TaskID   string
	Result   interface{}
	Error    error
	Duration time.Duration
}

type WorkerPool struct {
	workerCount  int
	taskQueue    chan Task
	resultQueue  chan TaskResult
	quit         chan struct{}
	wg           sync.WaitGroup
	metrics      *PoolMetrics
	priorityMode bool
}

type PoolMetrics struct {
	TasksProcessed uint64
	TasksFailed    uint64
	TotalDuration  time.Duration
	mu             sync.RWMutex
}

func NewWorkerPool(workerCount, queueSize int) *WorkerPool {
	pool := &WorkerPool{
		workerCount: workerCount,
		taskQueue:   make(chan Task, queueSize),
		resultQueue: make(chan TaskResult, queueSize),
		quit:        make(chan struct{}),
		metrics:     &PoolMetrics{},
	}

	pool.wg.Add(workerCount)
	for i := 0; i < workerCount; i++ {
		go pool.worker(i)
	}

	return pool
}

// WithPriority enables priority-based task processing
func (wp *WorkerPool) WithPriority() *WorkerPool {
	wp.priorityMode = true
	// In a real implementation, you'd use a priority queue
	return wp
}

func (wp *WorkerPool) Submit(task Task) error {
	select {
	case wp.taskQueue <- task:
		return nil
	default:
		return errors.New("worker pool queue is full")
	}
}

func (wp *WorkerPool) SubmitWithTimeout(task Task, timeout time.Duration) error {
	select {
	case wp.taskQueue <- task:
		return nil
	case <-time.After(timeout):
		return errors.New("submission timeout")
	}
}

func (wp *WorkerPool) worker(id int) {
	defer wp.wg.Done()

	for {
		select {
		case task := <-wp.taskQueue:
			start := time.Now()

			result, err := wp.processTask(task)
			duration := time.Since(start)

			wp.resultQueue <- TaskResult{
				TaskID:   task.ID,
				Result:   result,
				Error:    err,
				Duration: duration,
			}

			// Update metrics
			wp.metrics.mu.Lock()
			wp.metrics.TasksProcessed++
			wp.metrics.TotalDuration += duration
			if err != nil {
				wp.metrics.TasksFailed++
			}
			wp.metrics.mu.Unlock()

			log.Printf("Worker %d processed task %s in %v", id, task.ID, duration)

		case <-wp.quit:
			log.Printf("Worker %d shutting down", id)
			return
		}
	}
}

func (wp *WorkerPool) processTask(task Task) (interface{}, error) {
	// Simulate different types of tasks
	switch payload := task.Payload.(type) {
	case string:
		// String processing task
		time.Sleep(time.Duration(10+task.Attempts*5) * time.Millisecond)
		return strings.ToUpper(payload), nil

	case []int:
		// Number processing task
		time.Sleep(time.Duration(len(payload)) * time.Millisecond)
		sum := 0
		for _, n := range payload {
			sum += n
		}
		return sum, nil

	case func() (interface{}, error):
		// Function task
		return payload()

	default:
		return nil, fmt.Errorf("unsupported task type: %T", payload)
	}
}

func (wp *WorkerPool) Results() <-chan TaskResult {
	return wp.resultQueue
}

func (wp *WorkerPool) Stop() {
	close(wp.quit)
	wp.wg.Wait()
	close(wp.resultQueue)
}

func (wp *WorkerPool) Metrics() *PoolMetrics {
	return wp.metrics
}

// Advanced: Dynamic worker pool that scales based on load
type DynamicWorkerPool struct {
	minWorkers int
	maxWorkers int
	scaleUp    chan struct{}
	scaleDown  chan struct{}
	workers    []*worker
	mu         sync.RWMutex
	metrics    *DynamicMetrics
}

type worker struct {
	id      int
	tasks   chan Task
	quit    chan struct{}
	stopped chan struct{}
}

type DynamicMetrics struct {
	ActiveWorkers int
	QueueSize     int
	Throughput    float64
}

func NewDynamicWorkerPool(min, max, queueSize int) *DynamicWorkerPool {
	pool := &DynamicWorkerPool{
		minWorkers: min,
		maxWorkers: max,
		scaleUp:    make(chan struct{}, 100),
		scaleDown:  make(chan struct{}, 100),
		metrics:    &DynamicMetrics{},
	}

	// Start with minimum workers
	for i := 0; i < min; i++ {
		pool.addWorker(i)
	}

	// Start scaler goroutine
	go pool.scaler()

	return pool
}

func (dwp *DynamicWorkerPool) addWorker(id int) {
	dwp.mu.Lock()
	defer dwp.mu.Unlock()

	w := &worker{
		id:      id,
		tasks:   make(chan Task, 10),
		quit:    make(chan struct{}),
		stopped: make(chan struct{}),
	}

	dwp.workers = append(dwp.workers, w)
	dwp.metrics.ActiveWorkers++

	go w.run(dwp.metrics)
}

func (w *worker) run(metrics *DynamicMetrics) {
	defer close(w.stopped)

	for {
		select {
		case task := <-w.tasks:
			// Process task
			time.Sleep(50 * time.Millisecond) // Simulate work
			log.Printf("Worker %d processed task %s", w.id, task.ID)

		case <-w.quit:
			return
		}
	}
}

func (dwp *DynamicWorkerPool) scaler() {
	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			dwp.adjustWorkers()
		}
	}
}

func (dwp *DynamicWorkerPool) adjustWorkers() {
	dwp.mu.RLock()
	current := len(dwp.workers)
	dwp.mu.RUnlock()

	// Simplified scaling logic
	// In reality, you'd use queue size, CPU usage, etc.
	if current < dwp.maxWorkers && len(dwp.scaleUp) > 0 {
		dwp.addWorker(current)
	} else if current > dwp.minWorkers && len(dwp.scaleDown) > 0 {
		dwp.removeWorker()
	}
}

func (dwp *DynamicWorkerPool) removeWorker() {
	dwp.mu.Lock()
	defer dwp.mu.Unlock()

	if len(dwp.workers) == 0 {
		return
	}

	// Remove last worker
	w := dwp.workers[len(dwp.workers)-1]
	close(w.quit)
	<-w.stopped

	dwp.workers = dwp.workers[:len(dwp.workers)-1]
	dwp.metrics.ActiveWorkers--
}

func demonstrateWorkerPools() {
	fmt.Println("\n=== 4. WORKER POOLS ===")

	// Basic worker pool
	fmt.Println("Basic Worker Pool:")
	pool := NewWorkerPool(3, 100)

	// Submit tasks
	for i := 0; i < 10; i++ {
		task := Task{
			ID:      fmt.Sprintf("task-%d", i),
			Payload: fmt.Sprintf("payload-%d", i),
		}
		if err := pool.Submit(task); err != nil {
			log.Printf("Failed to submit task %s: %v", task.ID, err)
		}
	}

	// Collect results (in a separate goroutine)
	go func() {
		for result := range pool.Results() {
			if result.Error != nil {
				fmt.Printf("Task %s failed: %v\n", result.TaskID, result.Error)
			} else {
				fmt.Printf("Task %s completed in %v: %v\n",
					result.TaskID, result.Duration, result.Result)
			}
		}
	}()

	// Wait for tasks to complete
	time.Sleep(1 * time.Second)
	pool.Stop()

	// Show metrics
	metrics := pool.Metrics()
	fmt.Printf("\nMetrics: Processed: %d, Failed: %d, Avg Time: %v\n",
		metrics.TasksProcessed, metrics.TasksFailed,
		metrics.TotalDuration/time.Duration(metrics.TasksProcessed))

	// Advanced patterns
	fmt.Println("\nAdvanced Worker Pool Patterns:")
	fmt.Println("1. Priority-based task processing")
	fmt.Println("2. Dynamic worker scaling")
	fmt.Println("3. Task batching for efficiency")
	fmt.Println("4. Circuit breakers for failing tasks")
	fmt.Println("5. Dead letter queues for failed tasks")

	// Example: Worker pool with context and cancellation
	ctxPool := NewWorkerPoolWithContext(2, 50)
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	ctxPool.Start(ctx)

	// Submit tasks with context
	for i := 0; i < 5; i++ {
		go func(i int) {
			task := Task{ID: fmt.Sprintf("ctx-task-%d", i), Payload: i}
			if err := ctxPool.SubmitWithContext(ctx, task); err != nil {
				fmt.Printf("Task %d submission error: %v\n", i, err)
			}
		}(i)
	}

	time.Sleep(500 * time.Millisecond)
}

// Worker pool with context support
type WorkerPoolWithContext struct {
	workers   int
	taskQueue chan Task
	ctx       context.Context
	cancel    context.CancelFunc
	wg        sync.WaitGroup
}

func NewWorkerPoolWithContext(workers, queueSize int) *WorkerPoolWithContext {
	return &WorkerPoolWithContext{
		workers:   workers,
		taskQueue: make(chan Task, queueSize),
	}
}

func (wp *WorkerPoolWithContext) Start(ctx context.Context) {
	wp.ctx, wp.cancel = context.WithCancel(ctx)
	wp.wg.Add(wp.workers)

	for i := 0; i < wp.workers; i++ {
		go wp.worker(i)
	}
}

func (wp *WorkerPoolWithContext) SubmitWithContext(ctx context.Context, task Task) error {
	select {
	case <-ctx.Done():
		return ctx.Err()
	case <-wp.ctx.Done():
		return wp.ctx.Err()
	case wp.taskQueue <- task:
		return nil
	}
}

func (wp *WorkerPoolWithContext) worker(id int) {
	defer wp.wg.Done()

	for {
		select {
		case <-wp.ctx.Done():
			return
		case task := <-wp.taskQueue:
			// Process task with context
			select {
			case <-wp.ctx.Done():
				return
			default:
				fmt.Printf("Worker %d processing task %s\n", id, task.ID)
				time.Sleep(100 * time.Millisecond)
			}
		}
	}
}

func (wp *WorkerPoolWithContext) Stop() {
	if wp.cancel != nil {
		wp.cancel()
	}
	wp.wg.Wait()
}

// ============================================================================
// 5. PIPELINE PATTERN (Senior Level)
// ============================================================================
// Pipeline pattern for data processing with multiple stages.

// Stage represents a processing stage in the pipeline
type Stage[T any, U any] struct {
	processor func(T) (U, error)
	parallel  int // Number of parallel processors
}

// Pipeline connects multiple stages
type Pipeline[T any] struct {
	stages []interface{}
	input  chan T
	output chan interface{}
	errors chan error
	wg     sync.WaitGroup
}

func NewPipeline[T any]() *Pipeline[T] {
	return &Pipeline[T]{
		input:  make(chan T, 100),
		output: make(chan interface{}, 100),
		errors: make(chan error, 100),
	}
}

func (p *Pipeline[T]) AddStage(processor interface{}) *Pipeline[T] {
	p.stages = append(p.stages, processor)
	return p
}

func (p *Pipeline[T]) Run(ctx context.Context) {
	// Create channels between stages
	channels := make([]chan interface{}, len(p.stages)+1)
	for i := range channels {
		channels[i] = make(chan interface{}, 100)
	}

	// Connect input to first stage
	go func() {
		for item := range p.input {
			channels[0] <- item
		}
		close(channels[0])
	}()

	// Create stages
	for i, stage := range p.stages {
		p.wg.Add(1)
		go p.runStage(ctx, i, stage, channels[i], channels[i+1])
	}

	// Connect last stage to output
	go func() {
		for item := range channels[len(channels)-1] {
			p.output <- item
		}
		close(p.output)
	}()
}

func (p *Pipeline[T]) runStage(ctx context.Context, idx int, stage interface{}, in, out chan interface{}) {
	defer p.wg.Done()

	switch s := stage.(type) {
	case func(string) (string, error):
		for item := range in {
			select {
			case <-ctx.Done():
				return
			default:
				if str, ok := item.(string); ok {
					result, err := s(str)
					if err != nil {
						p.errors <- err
					} else {
						out <- result
					}
				}
			}
		}
	// Add more type cases as needed
	default:
		// Generic processing
		for item := range in {
			select {
			case <-ctx.Done():
				return
			default:
				out <- item // Just pass through
			}
		}
	}

	close(out)
}

func (p *Pipeline[T]) Input() chan<- T {
	return p.input
}

func (p *Pipeline[T]) Output() <-chan interface{} {
	return p.output
}

func (p *Pipeline[T]) Errors() <-chan error {
	return p.errors
}

func (p *Pipeline[T]) Wait() {
	p.wg.Wait()
}

// Example: Data processing pipeline
func demonstratePipelinePattern() {
	fmt.Println("\n=== 5. PIPELINE PATTERN ===")

	// Create a data processing pipeline
	pipeline := NewPipeline[string]()

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// Define pipeline stages
	stage1 := func(input string) (string, error) {
		time.Sleep(10 * time.Millisecond)
		return strings.ToUpper(input), nil
	}

	stage2 := func(input string) (string, error) {
		time.Sleep(20 * time.Millisecond)
		return strings.ReplaceAll(input, " ", "_"), nil
	}

	stage3 := func(input string) (string, error) {
		time.Sleep(15 * time.Millisecond)
		return "processed:" + input, nil
	}

	// Build pipeline
	pipeline.
		AddStage(stage1).
		AddStage(stage2).
		AddStage(stage3)

	// Start pipeline
	pipeline.Run(ctx)

	// Feed data into pipeline
	go func() {
		inputs := []string{
			"hello world",
			"golang pipeline",
			"concurrent processing",
			"design patterns",
		}

		for _, input := range inputs {
			select {
			case <-ctx.Done():
				return
			case pipeline.Input() <- input:
			}
		}
		close(pipeline.Input())
	}()

	// Collect results
	go func() {
		for result := range pipeline.Output() {
			fmt.Printf("Pipeline output: %v\n", result)
		}
	}()

	// Collect errors
	go func() {
		for err := range pipeline.Errors() {
			fmt.Printf("Pipeline error: %v\n", err)
		}
	}()

	// Wait for pipeline to complete
	time.Sleep(1 * time.Second)
	pipeline.Wait()

	// Advanced: Fan-out/Fan-in pattern
	fmt.Println("\nAdvanced: Fan-out/Fan-in Pattern")
	demonstrateFanOutFanIn()
}

func demonstrateFanOutFanIn() {
	// Generate data
	data := make(chan int, 100)
	go func() {
		for i := 1; i <= 100; i++ {
			data <- i
		}
		close(data)
	}()

	// Fan-out: Multiple workers process data
	numWorkers := 5
	workerResults := make([]chan int, numWorkers)

	for i := 0; i < numWorkers; i++ {
		workerResults[i] = make(chan int, 10)
		go worker(i, data, workerResults[i])
	}

	// Fan-in: Combine results
	finalResult := make(chan int)
	go fanIn(workerResults, finalResult)

	// Process final results
	var sum int
	for result := range finalResult {
		sum += result
	}

	fmt.Printf("Fan-out/Fan-in result: Sum = %d\n", sum)
}

func worker(id int, in <-chan int, out chan<- int) {
	for n := range in {
		// Simulate processing
		result := n * 2
		out <- result
	}
	close(out)
}

func fanIn(inputs []chan int, output chan<- int) {
	var wg sync.WaitGroup

	for _, ch := range inputs {
		wg.Add(1)
		go func(c <-chan int) {
			defer wg.Done()
			for n := range c {
				output <- n
			}
		}(ch)
	}

	wg.Wait()
	close(output)
}

// ============================================================================
// 6. DEPENDENCY INJECTION (Mid to Senior Level)
// ============================================================================
// Dependency injection promotes loose coupling and testability.

// Service interfaces
type UserService interface {
	GetUser(id string) (*User, error)
	CreateUser(user *User) error
}

type EmailService interface {
	SendWelcomeEmail(email, name string) error
}

type PaymentService interface {
	ProcessPayment(amount float64) error
}

// Concrete implementations
type RealUserService struct {
	repo UserRepository
}

func NewRealUserService(repo UserRepository) *RealUserService {
	return &RealUserService{repo: repo}
}

func (s *RealUserService) GetUser(id string) (*User, error) {
	ctx := context.Background()
	return s.repo.FindByID(ctx, id)
}

func (s *RealUserService) CreateUser(user *User) error {
	ctx := context.Background()
	return s.repo.Save(ctx, user)
}

type RealEmailService struct {
	smtpHost string
	smtpPort int
}

func NewRealEmailService(host string, port int) *RealEmailService {
	return &RealEmailService{
		smtpHost: host,
		smtpPort: port,
	}
}

func (s *RealEmailService) SendWelcomeEmail(email, name string) error {
	// Simulate sending email
	fmt.Printf("Sending welcome email to %s <%s>\n", name, email)
	return nil
}

type RealPaymentService struct {
	apiKey string
}

func NewRealPaymentService(apiKey string) *RealPaymentService {
	return &RealPaymentService{apiKey: apiKey}
}

func (s *RealPaymentService) ProcessPayment(amount float64) error {
	// Simulate payment processing
	fmt.Printf("Processing payment of $%.2f\n", amount)
	return nil
}

// Mock implementations for testing
type MockUserService struct {
	users map[string]*User
}

func NewMockUserService() *MockUserService {
	return &MockUserService{
		users: make(map[string]*User),
	}
}

func (s *MockUserService) GetUser(id string) (*User, error) {
	user, exists := s.users[id]
	if !exists {
		return nil, fmt.Errorf("user not found")
	}
	return user, nil
}

func (s *MockUserService) CreateUser(user *User) error {
	s.users[user.ID] = user
	return nil
}

// Container for dependencies
type Container struct {
	userService    UserService
	emailService   EmailService
	paymentService PaymentService
	config         *Config
}

func NewContainer() *Container {
	return &Container{}
}

// Setter injection
func (c *Container) SetUserService(service UserService) {
	c.userService = service
}

func (c *Container) SetEmailService(service EmailService) {
	c.emailService = service
}

func (c *Container) SetPaymentService(service PaymentService) {
	c.paymentService = service
}

func (c *Container) SetConfig(config *Config) {
	c.config = config
}

// Constructor injection example
type RegistrationHandler struct {
	userService    UserService
	emailService   EmailService
	paymentService PaymentService
}

func NewRegistrationHandler(
	userService UserService,
	emailService EmailService,
	paymentService PaymentService,
) *RegistrationHandler {
	return &RegistrationHandler{
		userService:    userService,
		emailService:   emailService,
		paymentService: paymentService,
	}
}

func (h *RegistrationHandler) Register(user *User, plan string) error {
	// Create user
	if err := h.userService.CreateUser(user); err != nil {
		return fmt.Errorf("failed to create user: %w", err)
	}

	// Send welcome email
	if err := h.emailService.SendWelcomeEmail(user.Email, user.Name); err != nil {
		// Log error but don't fail registration
		fmt.Printf("Failed to send welcome email: %v\n", err)
	}

	// Process payment if premium plan
	if plan == "premium" {
		if err := h.paymentService.ProcessPayment(99.99); err != nil {
			return fmt.Errorf("payment failed: %w", err)
		}
	}

	return nil
}

// Wire (Dependency injection framework) style initialization
func InitializeApp() (*RegistrationHandler, error) {
	// Create dependencies
	config := &Config{
		Host:    "localhost",
		Port:    8080,
		Timeout: 30 * time.Second,
	}

	// In real app, this would be a real database connection
	userRepo := NewInMemoryUserRepository()
	userService := NewRealUserService(userRepo)
	emailService := NewRealEmailService("smtp.example.com", 587)
	paymentService := NewRealPaymentService("api_key_123")

	// Create handler with dependencies
	handler := NewRegistrationHandler(
		userService,
		emailService,
		paymentService,
	)

	return handler, nil
}

// Factory pattern for creating services
type ServiceFactory struct {
	config *Config
}

func NewServiceFactory(config *Config) *ServiceFactory {
	return &ServiceFactory{config: config}
}

func (f *ServiceFactory) CreateUserService() UserService {
	// Based on config, return appropriate implementation
	if f.config.Host == "test" {
		return NewMockUserService()
	}
	return NewRealUserService(NewInMemoryUserRepository())
}

// Dependency injection with context
type ServiceLocator struct {
	services map[string]interface{}
	mu       sync.RWMutex
}

func NewServiceLocator() *ServiceLocator {
	return &ServiceLocator{
		services: make(map[string]interface{}),
	}
}

func (sl *ServiceLocator) Register(name string, service interface{}) {
	sl.mu.Lock()
	defer sl.mu.Unlock()
	sl.services[name] = service
}

func (sl *ServiceLocator) Get(name string) (interface{}, bool) {
	sl.mu.RLock()
	defer sl.mu.RUnlock()
	service, exists := sl.services[name]
	return service, exists
}

func demonstrateDependencyInjection() {
	fmt.Println("\n=== 6. DEPENDENCY INJECTION ===")

	fmt.Println("1. Constructor Injection Example:")

	// Create mock services for testing
	mockUserService := NewMockUserService()
	mockEmailService := &MockEmailService{}
	mockPaymentService := &MockPaymentService{}

	// Inject dependencies via constructor
	handler := NewRegistrationHandler(
		mockUserService,
		mockEmailService,
		mockPaymentService,
	)

	// Test registration
	user := &User{
		ID:    "test-123",
		Name:  "Test User",
		Email: "test@example.com",
	}

	if err := handler.Register(user, "premium"); err != nil {
		fmt.Printf("Registration error: %v\n", err)
	} else {
		fmt.Println("Registration successful!")
	}

	fmt.Println("\n2. Setter Injection Example:")

	container := NewContainer()
	container.SetUserService(mockUserService)
	container.SetEmailService(mockEmailService)
	container.SetPaymentService(mockPaymentService)

	fmt.Println("Dependencies set in container")

	fmt.Println("\n3. Factory Pattern Example:")

	config := &Config{Host: "test"}
	factory := NewServiceFactory(config)
	userService := factory.CreateUserService()

	fmt.Printf("Created user service: %T\n", userService)

	fmt.Println("\n4. Service Locator Pattern:")

	locator := NewServiceLocator()
	locator.Register("userService", mockUserService)
	locator.Register("emailService", mockEmailService)

	if service, exists := locator.Get("userService"); exists {
		fmt.Printf("Retrieved service: %T\n", service)
	}

	// Advanced: DI Container with reflection
	fmt.Println("\n5. Reflection-based DI Container:")
	diContainer := NewDIContainer()
	diContainer.Register(UserService{}, func() interface{} {
		return mockUserService
	})

	// Wire-style initialization
	fmt.Println("\n6. Wire-style Initialization:")
	appHandler, err := InitializeApp()
	if err != nil {
		fmt.Printf("Failed to initialize app: %v\n", err)
	} else {
		fmt.Printf("App initialized: %T\n", appHandler)
	}
}

// Mock implementations
type MockEmailService struct{}

func (m *MockEmailService) SendWelcomeEmail(email, name string) error {
	fmt.Printf("[MOCK] Welcome email sent to %s\n", email)
	return nil
}

type MockPaymentService struct{}

func (m *MockPaymentService) ProcessPayment(amount float64) error {
	fmt.Printf("[MOCK] Processed payment of $%.2f\n", amount)
	return nil
}

// Advanced: Reflection-based DI Container
type DIContainer struct {
	services map[reflect.Type]func() interface{}
	mu       sync.RWMutex
}

func NewDIContainer() *DIContainer {
	return &DIContainer{
		services: make(map[reflect.Type]func() interface{}),
	}
}

func (c *DIContainer) Register(serviceType interface{}, factory func() interface{}) {
	c.mu.Lock()
	defer c.mu.Unlock()

	t := reflect.TypeOf(serviceType)
	c.services[t] = factory
}

func (c *DIContainer) Resolve(serviceType interface{}) (interface{}, error) {
	c.mu.RLock()
	defer c.mu.RUnlock()

	t := reflect.TypeOf(serviceType)
	factory, exists := c.services[t]
	if !exists {
		return nil, fmt.Errorf("service not registered: %v", t)
	}

	return factory(), nil
}

// ============================================================================
// MAIN FUNCTION - RUN ALL DEMONSTRATIONS
// ============================================================================
func main() {
	fmt.Println("GO-SPECIFIC PATTERNS & DESIGN PATTERNS DEMO")
	fmt.Println("=============================================")

	// Run all demonstrations
	demonstrateFunctionalOptions()
	demonstrateBuilderPattern()
	demonstrateRepositoryPattern()
	demonstrateWorkerPools()
	demonstratePipelinePattern()
	demonstrateDependencyInjection()

	fmt.Println("\n=== PATTERN SELECTION GUIDE ===")
	fmt.Println("\nWhen to use each pattern:")
	patterns := []struct {
		Pattern    string
		BestFor    string
		Complexity string
	}{
		{"Functional Options", "Configuring objects with many optional parameters", "Low"},
		{"Builder Pattern", "Constructing complex objects step by step", "Low-Medium"},
		{"Repository Pattern", "Abstracting data access for testability", "Medium"},
		{"Worker Pools", "Processing tasks concurrently with controlled parallelism", "Medium-High"},
		{"Pipeline Pattern", "Data processing with multiple sequential stages", "High"},
		{"Dependency Injection", "Managing dependencies for testable, maintainable code", "Medium"},
	}

	for _, p := range patterns {
		fmt.Printf("  • %-25s: %-45s (%s)\n", p.Pattern, p.BestFor, p.Complexity)
	}

	fmt.Println("\nGO-SPECIFIC CONSIDERATIONS:")
	fmt.Println("  • Leverage interfaces for abstraction")
	fmt.Println("  • Use composition over inheritance")
	fmt.Println("  • Embrace simplicity and clarity")
	fmt.Println("  • Write testable code from the start")
	fmt.Println("  • Use the standard library patterns as reference")

	fmt.Println("\nADDITIONAL GO PATTERNS TO EXPLORE:")
	additionalPatterns := []string{
		"Middleware pattern for HTTP handlers",
		"Strategy pattern with function types",
		"Observer pattern with channels",
		"Decorator pattern with function wrappers",
		"Singleton pattern with sync.Once",
		"Command pattern with interface{}",
		"Adapter pattern for interface compatibility",
	}

	for i, pattern := range additionalPatterns {
		fmt.Printf("  %d. %s\n", i+1, pattern)
	}
}

/*
INSTRUCTIONS TO RUN:
====================
1. This code demonstrates patterns - most examples are self-contained
2. To run: go run main.go
3. Some patterns may require additional packages for full implementation:
   - Database patterns: github.com/go-sql-driver/mysql
   - HTTP patterns: net/http package (standard library)
4. The examples use simplified implementations for clarity

KEY TAKEAWAYS:
==============
- Functional options provide clean, readable configuration
- Builder pattern helps construct complex objects
- Repository pattern abstracts data access for testability
- Worker pools manage concurrent processing efficiently
- Pipeline pattern enables complex data processing flows
- Dependency injection promotes loose coupling and testability
- Go's simplicity encourages composition over complex inheritance
- Interfaces are powerful for abstraction in Go
- Context should be used for cancellation and timeouts
- Always consider error handling in pattern implementations

REMEMBER:
=========
- Choose patterns that solve your specific problem
- Keep implementations simple and readable
- Write tests for your pattern implementations
- Consider performance implications
- Document the pattern's purpose and usage
- Follow Go community conventions and idioms
*/
