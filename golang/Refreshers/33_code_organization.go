/*
GO CODE ORGANIZATION & ARCHITECTURE
This comprehensive guide covers project structure, package design, and architectural patterns
for building maintainable, scalable Go applications from junior to senior level.
*/

// ==================== PROJECT STRUCTURE LAYOUTS ====================

/*
STANDARD GO PROJECT LAYOUT (Production-ready structure):
https://github.com/golang-standards/project-layout

.
├── cmd/                          # Application entry points
│   ├── api/                      # REST API server
│   │   └── main.go              # Composition root
│   ├── cli/                      # CLI application
│   │   └── main.go
│   └── worker/                   # Background worker
│       └── main.go
│
├── internal/                     # Private application code (cannot be imported by others)
│   ├── app/                      # Application layer (use cases)
│   │   ├── service/             # Application services
│   │   ├── dto/                 # Data Transfer Objects
│   │   └── command/             # CQRS commands
│   │
│   ├── domain/                   # Domain layer (business logic)
│   │   ├── entity/              # Domain entities
│   │   ├── valueobject/         # Value objects
│   │   ├── repository/          # Repository interfaces
│   │   └── service/             # Domain services
│   │
│   └── infrastructure/          # Infrastructure layer (external concerns)
│       ├── persistence/         # Database implementations
│       │   ├── mysql/           # MySQL-specific code
│       │   ├── postgres/        # PostgreSQL-specific code
│       │   └── redis/           # Redis implementation
│       ├── http/                # HTTP handlers
│       │   ├── handler/         # Request handlers
│       │   ├── middleware/      # HTTP middleware
│       │   └── router/          # Router setup
│       ├── messaging/           # Message brokers (Kafka, RabbitMQ)
│       ├── cache/               # Cache implementations
│       └── config/              # Configuration loading
│
├── pkg/                          # Public reusable packages (optional, careful!)
│   ├── errors/                  # Custom error types
│   ├── logger/                  # Logging utilities
│   ├── validator/               # Validation library
│   └── pagination/              # Pagination utilities
│
├── api/                          # API contracts
│   ├── rest/                    # REST API specs (OpenAPI/Swagger)
│   └── proto/                   # gRPC protobuf definitions
│
├── web/                          # Web assets (if applicable)
│   ├── static/                  # Static files
│   └── template/                # HTML templates
│
├── scripts/                      # Build/deployment scripts
├── deployments/                  # Deployment configs (Docker, K8s)
├── test/                         # Additional test files
│
├── go.mod                       # Module definition
├── go.sum                       # Dependency checksums
├── Makefile                     # Common tasks
├── Dockerfile                   # Container definition
└── README.md                    # Documentation
*/

// ==================== PACKAGE DESIGN PRINCIPLES ====================

/*
PACKAGE DESIGN GUIDELINES:

1. Package by layer (traditional):
   internal/
     ├── repository/
     ├── service/
     ├── handler/
     └── model/

2. Package by feature (vertical slice):
   internal/
     ├── user/
     │   ├── repository.go
     │   ├── service.go
     │   └── handler.go
     ├── order/
     │   ├── repository.go
     │   ├── service.go
     │   └── handler.go
     └── product/

3. Package by component (hexagonal):
   internal/
     ├── domain/
     ├── application/
     └── infrastructure/

RECOMMENDATION: Start with package-by-feature for monoliths,
move to package-by-component as complexity grows.
*/

// ==================== DOMAIN LAYER (Clean Architecture Core) ====================

// internal/domain/user/entity.go
package user

import (
	"errors"
	"time"
)

// Entity represents a business concept with identity
type User struct {
	ID        UserID
	Email     Email
	Name      string
	Status    UserStatus
	CreatedAt time.Time
	UpdatedAt time.Time
}

// Value Object - defined by attributes, immutable
type Email string

func NewEmail(value string) (Email, error) {
	// Validation logic
	if !isValidEmail(value) {
		return "", errors.New("invalid email format")
	}
	return Email(value), nil
}

func (e Email) String() string {
	return string(e)
}

func isValidEmail(email string) bool {
	// Simple validation for example
	return len(email) > 3 && strings.Contains(email, "@")
}

// Entity ID type for type safety
type UserID string

func NewUserID(id string) UserID {
	return UserID(id)
}

// Domain types
type UserStatus string

const (
	UserStatusActive   UserStatus = "active"
	UserStatusInactive UserStatus = "inactive"
	UserStatusBanned   UserStatus = "banned"
)

// Domain errors
var (
	ErrUserNotFound      = errors.New("user not found")
	ErrEmailAlreadyInUse = errors.New("email already in use")
	ErrInvalidUserStatus = errors.New("invalid user status")
)

// Domain business rules (methods on entities)
func (u *User) Activate() error {
	if u.Status == UserStatusBanned {
		return errors.New("cannot activate banned user")
	}
	u.Status = UserStatusActive
	u.UpdatedAt = time.Now()
	return nil
}

func (u *User) Deactivate() error {
	u.Status = UserStatusInactive
	u.UpdatedAt = time.Now()
	return nil
}

func (u *User) UpdateEmail(newEmail Email) error {
	if u.Email == newEmail {
		return nil // No change needed
	}
	
	// Business rule: Email changes require re-verification
	u.Email = newEmail
	u.Status = UserStatusInactive // Require reactivation
	u.UpdatedAt = time.Now()
	return nil
}

// ==================== REPOSITORY PATTERN (Domain Layer) ====================

// internal/domain/user/repository.go
package user

import "context"

// Repository interface defines WHAT we need, not HOW
type Repository interface {
	// Query methods
	FindByID(ctx context.Context, id UserID) (*User, error)
	FindByEmail(ctx context.Context, email Email) (*User, error)
	List(ctx context.Context, filter UserFilter) ([]*User, error)
	Count(ctx context.Context, filter UserFilter) (int, error)
	
	// Command methods
	Save(ctx context.Context, user *User) error
	Update(ctx context.Context, user *User) error
	Delete(ctx context.Context, id UserID) error
	
	// Complex queries (consider separating into QueryService for CQRS)
	FindActiveUsers(ctx context.Context) ([]*User, error)
}

// Specification/Filter pattern
type UserFilter struct {
	Status  *UserStatus
	Email   *string
	CreatedAfter *time.Time
	Limit   int
	Offset  int
}

// Domain Service for operations that don't fit in a single entity
type DomainService interface {
	GenerateUsername(email Email) (string, error)
	ValidatePasswordStrength(password string) error
}

// ==================== APPLICATION LAYER ====================

// internal/app/user/service.go
package service

import (
	"context"
	"errors"
	"time"

	"project/internal/domain/user"
)

// DTOs for input/output (separate from domain entities)
type CreateUserRequest struct {
	Email    string `json:"email" validate:"required,email"`
	Name     string `json:"name" validate:"required"`
	Password string `json:"password" validate:"required,min=8"`
}

type UserResponse struct {
	ID        string    `json:"id"`
	Email     string    `json:"email"`
	Name      string    `json:"name"`
	Status    string    `json:"status"`
	CreatedAt time.Time `json:"created_at"`
}

// Application Service orchestrates domain objects
type UserService struct {
	repo           user.Repository
	passwordHasher PasswordHasher
	eventPublisher EventPublisher
	// Additional dependencies
}

// Dependency Injection via constructor
func NewUserService(
	repo user.Repository,
	hasher PasswordHasher,
	publisher EventPublisher,
) *UserService {
	return &UserService{
		repo:           repo,
		passwordHasher: hasher,
		eventPublisher: publisher,
	}
}

// Application-level use case
func (s *UserService) CreateUser(ctx context.Context, req CreateUserRequest) (*UserResponse, error) {
	// 1. Validate input
	if err := validateCreateUserRequest(req); err != nil {
		return nil, err
	}
	
	// 2. Check business rules
	email, err := user.NewEmail(req.Email)
	if err != nil {
		return nil, err
	}
	
	// Check if user already exists
	existing, err := s.repo.FindByEmail(ctx, email)
	if err != nil && !errors.Is(err, user.ErrUserNotFound) {
		return nil, err
	}
	if existing != nil {
		return nil, user.ErrEmailAlreadyInUse
	}
	
	// 3. Create domain entity
	userEntity := &user.User{
		ID:        user.NewUserID(generateID()),
		Email:     email,
		Name:      req.Name,
		Status:    user.UserStatusActive,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
	
	// 4. Apply business rules
	if err := userEntity.Activate(); err != nil {
		return nil, err
	}
	
	// 5. Persist
	if err := s.repo.Save(ctx, userEntity); err != nil {
		return nil, err
	}
	
	// 6. Publish domain events
	if err := s.eventPublisher.Publish(ctx, UserCreatedEvent{
		UserID:    string(userEntity.ID),
		Email:     string(userEntity.Email),
		Timestamp: time.Now(),
	}); err != nil {
		// Log but don't fail - eventual consistency
	}
	
	// 7. Return response
	return &UserResponse{
		ID:        string(userEntity.ID),
		Email:     string(userEntity.Email),
		Name:      userEntity.Name,
		Status:    string(userEntity.Status),
		CreatedAt: userEntity.CreatedAt,
	}, nil
}

func (s *UserService) GetUser(ctx context.Context, userID string) (*UserResponse, error) {
	id := user.NewUserID(userID)
	userEntity, err := s.repo.FindByID(ctx, id)
	if err != nil {
		return nil, err
	}
	
	return &UserResponse{
		ID:        string(userEntity.ID),
		Email:     string(userEntity.Email),
		Name:      userEntity.Name,
		Status:    string(userEntity.Status),
		CreatedAt: userEntity.CreatedAt,
	}, nil
}

// ==================== INFRASTRUCTURE LAYER ====================

// internal/infrastructure/persistence/mysql/user_repository.go
package mysql

import (
	"context"
	"database/sql"
	"time"

	"project/internal/domain/user"
)

// MySQL implementation of user.Repository
type UserRepository struct {
	db *sql.DB
}

func NewUserRepository(db *sql.DB) *UserRepository {
	return &UserRepository{db: db}
}

func (r *UserRepository) FindByID(ctx context.Context, id user.UserID) (*user.User, error) {
	query := `
		SELECT id, email, name, status, created_at, updated_at 
		FROM users 
		WHERE id = ? AND deleted_at IS NULL
	`
	
	var u userEntity
	err := r.db.QueryRowContext(ctx, query, string(id)).Scan(
		&u.ID,
		&u.Email,
		&u.Name,
		&u.Status,
		&u.CreatedAt,
		&u.UpdatedAt,
	)
	
	if err == sql.ErrNoRows {
		return nil, user.ErrUserNotFound
	}
	if err != nil {
		return nil, err
	}
	
	return mapToDomain(u), nil
}

func (r *UserRepository) Save(ctx context.Context, u *user.User) error {
	query := `
		INSERT INTO users (id, email, name, status, created_at, updated_at)
		VALUES (?, ?, ?, ?, ?, ?)
		ON DUPLICATE KEY UPDATE
			email = VALUES(email),
			name = VALUES(name),
			status = VALUES(status),
			updated_at = VALUES(updated_at)
	`
	
	_, err := r.db.ExecContext(ctx, query,
		string(u.ID),
		string(u.Email),
		u.Name,
		string(u.Status),
		u.CreatedAt,
		u.UpdatedAt,
	)
	
	return err
}

// Database entity (separate from domain entity)
type userEntity struct {
	ID        string
	Email     string
	Name      string
	Status    string
	CreatedAt time.Time
	UpdatedAt time.Time
}

func mapToDomain(e userEntity) *user.User {
	return &user.User{
		ID:        user.NewUserID(e.ID),
		Email:     user.Email(e.Email),
		Name:      e.Name,
		Status:    user.UserStatus(e.Status),
		CreatedAt: e.CreatedAt,
		UpdatedAt: e.UpdatedAt,
	}
}

// ==================== HTTP LAYER (Presentation) ====================

// internal/infrastructure/http/handler/user_handler.go
package handler

import (
	"encoding/json"
	"net/http"

	"project/internal/app/service"
)

type UserHandler struct {
	service *service.UserService
}

func NewUserHandler(svc *service.UserService) *UserHandler {
	return &UserHandler{service: svc}
}

func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
	var req service.CreateUserRequest
	
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondError(w, http.StatusBadRequest, "Invalid request body")
		return
	}
	
	// Validate input
	if err := validate.Struct(req); err != nil {
		respondError(w, http.StatusBadRequest, err.Error())
		return
	}
	
	user, err := h.service.CreateUser(r.Context(), req)
	if err != nil {
		switch err {
		case user.ErrEmailAlreadyInUse:
			respondError(w, http.StatusConflict, "Email already in use")
		case user.ErrUserNotFound:
			respondError(w, http.StatusNotFound, "User not found")
		default:
			respondError(w, http.StatusInternalServerError, "Internal server error")
		}
		return
	}
	
	respondJSON(w, http.StatusCreated, user)
}

func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
	userID := r.PathValue("id")
	
	user, err := h.service.GetUser(r.Context(), userID)
	if err != nil {
		if errors.Is(err, user.ErrUserNotFound) {
			respondError(w, http.StatusNotFound, "User not found")
			return
		}
		respondError(w, http.StatusInternalServerError, "Internal server error")
		return
	}
	
	respondJSON(w, http.StatusOK, user)
}

// ==================== HEXAGONAL ARCHITECTURE PORTS & ADAPTERS ====================

/*
HEXAGONAL ARCHITECTURE (Ports & Adapters):

Primary Ports (Driving - Input):
  - HTTP Handlers (REST API)
  - gRPC Services
  - CLI Commands
  - Message Consumers

Secondary Ports (Driven - Output):
  - Repository Interfaces
  - External Service Clients
  - Message Publishers
  - Cache Interfaces

Adapters (Implementations):
  - HTTP Handler (implements Primary Port)
  - PostgreSQL Repository (implements Repository Port)
  - Redis Cache (implements Cache Port)
  - Kafka Publisher (implements Message Publisher Port)
*/

// internal/domain/port/repository.go (Port definition)
package port

import (
	"context"
	"project/internal/domain/user"
)

// Repository Port
type UserRepository interface {
	FindByID(ctx context.Context, id user.UserID) (*user.User, error)
	Save(ctx context.Context, user *user.User) error
	// ... other methods
}

// internal/domain/port/messaging.go
package port

import "context"

// Event Publisher Port
type EventPublisher interface {
	Publish(ctx context.Context, event interface{}) error
	Subscribe(eventType string, handler EventHandler)
}

type EventHandler func(ctx context.Context, event interface{}) error

// ==================== COMPOSITION ROOT ====================

// cmd/api/main.go - Composition Root
package main

import (
	"database/sql"
	"log"
	"net/http"
	"os"

	"project/internal/app/service"
	"project/internal/infrastructure/http/handler"
	"project/internal/infrastructure/http/middleware"
	"project/internal/infrastructure/http/router"
	"project/internal/infrastructure/persistence/mysql"
)

func main() {
	// 1. Load configuration
	cfg := loadConfig()
	
	// 2. Initialize infrastructure dependencies
	db := initDatabase(cfg.DatabaseURL)
	redis := initRedis(cfg.RedisURL)
	
	// 3. Create adapters (implementations)
	userRepo := mysql.NewUserRepository(db)
	eventPublisher := NewKafkaEventPublisher(cfg.KafkaBrokers)
	
	// 4. Create domain services
	passwordHasher := NewBcryptPasswordHasher()
	
	// 5. Create application services with dependencies
	userService := service.NewUserService(
		userRepo,
		passwordHasher,
		eventPublisher,
	)
	
	// 6. Create handlers
	userHandler := handler.NewUserHandler(userService)
	
	// 7. Setup router with middleware
	r := router.NewRouter()
	
	// Global middleware
	r.Use(middleware.Logger)
	r.Use(middleware.Recovery)
	r.Use(middleware.CORS)
	
	// Routes
	r.Post("/users", userHandler.CreateUser)
	r.Get("/users/{id}", userHandler.GetUser)
	
	// 8. Start server
	server := &http.Server{
		Addr:         cfg.HTTPAddr,
		Handler:      r,
		ReadTimeout:  cfg.ReadTimeout,
		WriteTimeout: cfg.WriteTimeout,
		IdleTimeout:  cfg.IdleTimeout,
	}
	
	log.Printf("Starting server on %s", cfg.HTTPAddr)
	if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("Server failed: %v", err)
	}
}

// ==================== DOMAIN-DRIVEN DESIGN BASICS ====================

/*
DDD BUILDING BLOCKS IN GO:

1. Bounded Contexts:
   - User Management Context
   - Order Processing Context  
   - Inventory Context
   - Each with its own domain model

2. Aggregates:
   - Order (aggregate root)
   - OrderItem (entity within Order aggregate)
   - Rules: External references by ID only

3. Value Objects:
   - Money, Address, Email (immutable, no identity)
   - Compared by value, not reference

4. Domain Events:
   - OrderPlaced, PaymentReceived
   - Used for eventual consistency between bounded contexts

5. Repositories:
   - Per aggregate, not per entity
   - Return aggregate roots
*/

// Example of bounded context separation
// internal/order/domain/order.go
package order

type Order struct {
	ID         OrderID
	CustomerID customer.CustomerID // Reference by ID only
	Items      []OrderItem
	Status     OrderStatus
}

type OrderItem struct {
	ProductID product.ProductID // Reference by ID
	Quantity  int
	Price     Money
}

// internal/customer/domain/customer.go  
package customer

type Customer struct {
	ID   CustomerID
	Name string
}

// ==================== FACTORY PATTERN FOR COMPLEX OBJECTS ====================

// internal/domain/user/factory.go
package user

type Factory struct {
	passwordHasher PasswordHasher
	idGenerator    IDGenerator
}

func NewFactory(hasher PasswordHasher, generator IDGenerator) *Factory {
	return &Factory{
		passwordHasher: hasher,
		idGenerator:    generator,
	}
}

func (f *Factory) CreateUser(email Email, name, rawPassword string) (*User, error) {
	// Validate inputs
	if name == "" {
		return nil, errors.New("name cannot be empty")
	}
	
	// Hash password
	hashedPassword, err := f.passwordHasher.Hash(rawPassword)
	if err != nil {
		return nil, err
	}
	
	// Generate username from email
	username := generateUsernameFromEmail(string(email))
	
	return &User{
		ID:           UserID(f.idGenerator.Generate()),
		Email:        email,
		Name:         name,
		Username:     username,
		PasswordHash: hashedPassword,
		Status:       UserStatusActive,
		CreatedAt:    time.Now(),
		UpdatedAt:    time.Now(),
	}, nil
}

// ==================== EVENT-DRIVEN ARCHITECTURE ====================

// internal/domain/user/event.go
package user

import "time"

type DomainEvent interface {
	AggregateID() string
	EventType() string
	OccurredAt() time.Time
}

type UserCreatedEvent struct {
	UserID    string
	Email     string
	Name      string
	Timestamp time.Time
}

func (e UserCreatedEvent) AggregateID() string { return e.UserID }
func (e UserCreatedEvent) EventType() string   { return "user.created" }
func (e UserCreatedEvent) OccurredAt() time.Time { return e.Timestamp }

type UserEmailUpdatedEvent struct {
	UserID    string
	OldEmail  string
	NewEmail  string
	Timestamp time.Time
}

// ==================== CQRS PATTERN ====================

// For complex queries, separate from command side
// internal/app/user/query_service.go
package service

import "context"

type UserQueryService interface {
	GetUserProfile(ctx context.Context, userID string) (*UserProfile, error)
	ListUsers(ctx context.Context, filter UserFilter) ([]*UserSummary, error)
	SearchUsers(ctx context.Context, query string) ([]*UserSearchResult, error)
}

// Read models optimized for queries
type UserProfile struct {
	ID        string
	Email     string
	Name      string
	CreatedAt time.Time
	Stats     UserStats
}

type UserStats struct {
	TotalOrders   int
	TotalSpent    float64
	LastLogin     time.Time
}

// Separate database for reads (optional, for high-scale systems)
type UserQueryRepository interface {
	FindProfileByID(ctx context.Context, id string) (*UserProfile, error)
}

// ==================== TESTING STRATEGY ====================

/*
TESTING PYRAMID FOR CLEAN ARCHITECTURE:

1. Domain Layer: Unit tests (no external dependencies)
2. Application Layer: Integration tests (mocked repositories)
3. Infrastructure Layer: Integration tests (real dependencies)
4. HTTP Layer: Handler tests (mocked services)
5. End-to-End: API tests (full system)

USE TEST CONTAINERS FOR EXTERNAL DEPENDENCIES.
*/

// Example domain unit test
func TestUser_Activate(t *testing.T) {
	user := &User{
		ID:     UserID("123"),
		Status: UserStatusInactive,
	}
	
	err := user.Activate()
	assert.NoError(t, err)
	assert.Equal(t, UserStatusActive, user.Status)
	assert.False(t, user.UpdatedAt.IsZero())
}

// Example integration test with mocked repository
func TestUserService_CreateUser(t *testing.T) {
	mockRepo := new(MockUserRepository)
	mockHasher := new(MockPasswordHasher)
	mockPublisher := new(MockEventPublisher)
	
	service := NewUserService(mockRepo, mockHasher, mockPublisher)
	
	// Setup mocks
	mockRepo.On("FindByEmail", mock.Anything, mock.Anything).
		Return(nil, user.ErrUserNotFound)
	mockRepo.On("Save", mock.Anything, mock.Anything).
		Return(nil)
	
	// Execute
	req := CreateUserRequest{
		Email:    "test@example.com",
		Name:     "Test User",
		Password: "password123",
	}
	
	response, err := service.CreateUser(context.Background(), req)
	
	// Verify
	assert.NoError(t, err)
	assert.NotNil(t, response)
	assert.Equal(t, "test@example.com", response.Email)
	mockRepo.AssertExpectations(t)
}

// ==================== DEPENDENCY MANAGEMENT ====================

// Use wire (https://github.com/google/wire) for larger projects
// internal/wire/wire.go
package wire

import (
	"github.com/google/wire"
	
	"project/internal/app/service"
	"project/internal/infrastructure/http/handler"
	"project/internal/infrastructure/persistence/mysql"
)

// Wire set for User domain
var UserSet = wire.NewSet(
	mysql.NewUserRepository,
	service.NewUserService,
	handler.NewUserHandler,
	NewBcryptPasswordHasher,
	NewKafkaEventPublisher,
)

// Wire provider set for the entire application
var AppSet = wire.NewSet(
	wire.Struct(new(App), "*"),
	UserSet,
	OrderSet,
	ProductSet,
)

// ==================== CONFIGURATION MANAGEMENT ====================

// internal/infrastructure/config/config.go
package config

import (
	"os"
	"strconv"
	"time"
)

type Config struct {
	HTTPAddr     string
	ReadTimeout  time.Duration
	WriteTimeout time.Duration
	
	DatabaseURL string
	RedisURL    string
	
	KafkaBrokers []string
}

func Load() (*Config, error) {
	return &Config{
		HTTPAddr:     getEnv("HTTP_ADDR", ":8080"),
		ReadTimeout:  parseDuration(getEnv("READ_TIMEOUT", "10s")),
		WriteTimeout: parseDuration(getEnv("WRITE_TIMEOUT", "10s")),
		
		DatabaseURL: getEnv("DATABASE_URL", ""),
		RedisURL:    getEnv("REDIS_URL", ""),
		
		KafkaBrokers: splitCSV(getEnv("KAFKA_BROKERS", "")),
	}, nil
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}

// ==================== ERROR HANDLING STRATEGY ====================

// pkg/errors/errors.go (public package if needed)
package errors

import "fmt"

type ErrorCode string

const (
	CodeNotFound     ErrorCode = "NOT_FOUND"
	CodeInvalidInput ErrorCode = "INVALID_INPUT"
	CodeConflict     ErrorCode = "CONFLICT"
	CodeInternal     ErrorCode = "INTERNAL_ERROR"
)

type AppError struct {
	Code    ErrorCode
	Message string
	Err     error // Wrapped error
}

func (e *AppError) Error() string {
	if e.Err != nil {
		return fmt.Sprintf("%s: %s: %v", e.Code, e.Message, e.Err)
	}
	return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

func (e *AppError) Unwrap() error {
	return e.Err
}

func NewNotFoundError(message string, err error) *AppError {
	return &AppError{
		Code:    CodeNotFound,
		Message: message,
		Err:     err,
	}
}

// ==================== LOGGING STRATEGY ====================

// pkg/logger/logger.go
package logger

import (
	"context"
	"log"
	"os"
)

type Logger interface {
	Debug(ctx context.Context, msg string, fields ...Field)
	Info(ctx context.Context, msg string, fields ...Field)
	Error(ctx context.Context, msg string, fields ...Field)
}

// Structured logging with context
func (l *Logger) Info(ctx context.Context, msg string, fields ...Field) {
	entry := l.withContext(ctx).WithFields(fields...)
	entry.Info(msg)
}

// ==================== PRACTICAL ADVICE ====================

/*
ORGANIZATION EVOLUTION PATH:

Phase 1: Small Project (<3 developers)
  - Flat structure
  - Package by layer (handler, service, repository)
  - Simple dependency injection

Phase 2: Medium Project (3-10 developers)  
  - Package by feature (user/, order/, product/)
  - Clean Architecture with domain/internal separation
  - Wire for dependency injection

Phase 3: Large Project (>10 developers)
  - Multiple bounded contexts
  - Package by component (domain/, app/, infrastructure/)
  - Consider microservices for independent deployment
  - Event-driven communication

KEY PRINCIPLES:

1. Dependency Rule: Source code dependencies point inward
2. Stable Abstractions: Inner layers are more abstract
3. Separate Concerns: Business logic independent of frameworks
4. Testability: Each layer independently testable
5. Evolution: Structure should evolve with the project

COMMON PITFALLS TO AVOID:

1. Don't create too many small packages
2. Don't make everything public (use internal/)
3. Don't tie business logic to framework details
4. Don't over-engineer too early
5. Don't ignore package cohesion
*/

// Helper functions (would be in separate files)
var (
	validate   = validator.New()
	generateID = func() string { return uuid.New().String() }
)

type PasswordHasher interface{}
type EventPublisher interface{}
type IDGenerator interface{}
type App struct{}

func loadConfig() *Config { return &Config{} }
func initDatabase(url string) *sql.DB { return nil }
func initRedis(url string) interface{} { return nil }

func validateCreateUserRequest(req service.CreateUserRequest) error { return nil }
func generateUsernameFromEmail(email string) string { return "" }

func NewKafkaEventPublisher(brokers []string) EventPublisher { return nil }
func NewBcryptPasswordHasher() PasswordHasher { return nil }

func respondError(w http.ResponseWriter, code int, message string) {
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(map[string]string{"error": message})
}

func respondJSON(w http.ResponseWriter, code int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	json.NewEncoder(w).Encode(data)
}

// Mock types for testing examples
type MockUserRepository struct{ mock.Mock }
type MockPasswordHasher struct{ mock.Mock }
type MockEventPublisher struct{ mock.Mock }

func (m *MockUserRepository) FindByEmail(ctx context.Context, email user.Email) (*user.User, error) {
	args := m.Called(ctx, email)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*user.User), args.Error(1)
}

func (m *MockUserRepository) Save(ctx context.Context, user *user.User) error {
	args := m.Called(ctx, user)
	return args.Error(0)
}

// Mock assertion library
type mock struct{ Mock }
type Mock struct{}
func (m *Mock) On(method string, args ...interface{}) *Call { return &Call{} }
func (m *Mock) Called(args ...interface{}) []interface{} { return nil }
func (m *Mock) AssertExpectations(t interface{}) {}
type Call struct{}
func (c *Call) Return(args ...interface{}) *Call { return c }

// Testing assertions
func assertNoError(t interface{}, err error) {}
func assertEqual(t interface{}, expected, actual interface{}) {}
func assertNotNil(t interface{}, v interface{}) {}
func assertFalse(t interface{}, v bool) {}

// UUID package
type uuid struct{}
func (u uuid) New() uuid { return uuid{} }
func (u uuid) String() string { return "" }
var UUID = uuid{}

// Validator package
type validator struct{}
func (v *validator) New() *validator { return v }
func (v *validator) Struct(s interface{}) error { return nil }

// Strings package
var strings = struct {
	Contains func(string, string) bool
}{
	Contains: func(s, substr string) bool { return true },
}