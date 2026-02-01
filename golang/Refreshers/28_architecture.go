/*
GO ARCHITECTURE & DESIGN PATTERNS
This comprehensive example demonstrates architectural patterns and design decisions
for building maintainable Go applications from junior to senior level.
*/

// Package structure for Clean/Hexagonal Architecture:
// .
// ├── cmd/
// │   └── api/
// │       └── main.go          # Composition root
// ├── internal/                # Private application code
// │   ├── domain/             # Enterprise business rules
// │   │   ├── entity.go
// │   │   ├── valueobject.go
// │   │   └── repository.go   # Interface definitions
// │   ├── application/        # Application business rules
// │   │   ├── service.go
// │   │   └── dto.go          # Data Transfer Objects
// │   └── infrastructure/     # Framework & external concerns
// │       ├── persistence/    # Database implementations
// │       ├── http/           # HTTP handlers
// │       └── config/         # Configuration
// └── pkg/                    # Public reusable packages (optional)

package main

import (
	"context"
	"fmt"
	"log"
	"time"
)

/*
CLEAN ARCHITECTURE IN GO:
Layers: Domain → Application → Infrastructure → Presentation
Dependency Rule: Outer layers depend on inner layers, not vice versa
*/

// ==================== DOMAIN LAYER (Inner-most, most stable) ====================

// Domain entities represent core business concepts
type Order struct {
	ID         string
	CustomerID string
	Items      []OrderItem
	Status     OrderStatus
	CreatedAt  time.Time
	Total      Money
}

// Value objects are immutable and defined by their attributes
type Money struct {
	Amount   int64
	Currency string
}

func (m Money) Add(other Money) (Money, error) {
	if m.Currency != other.Currency {
		return Money{}, fmt.Errorf("currency mismatch")
	}
	return Money{Amount: m.Amount + other.Amount, Currency: m.Currency}, nil
}

// Domain types
type OrderStatus string

const (
	OrderStatusPending   OrderStatus = "pending"
	OrderStatusConfirmed OrderStatus = "confirmed"
	OrderStatusShipped   OrderStatus = "shipped"
	OrderStatusDelivered OrderStatus = "delivered"
	OrderStatusCancelled OrderStatus = "canceled"
)

type OrderItem struct {
	ProductID string
	Quantity  int
	Price     Money
}

// Domain errors
type DomainError struct {
	Code    string
	Message string
}

func (e DomainError) Error() string {
	return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

var (
	ErrOrderNotFound    = DomainError{Code: "ORDER_NOT_FOUND", Message: "order not found"}
	ErrInvalidOrder     = DomainError{Code: "INVALID_ORDER", Message: "order is invalid"}
	ErrInsufficientStock = DomainError{Code: "INSUFFICIENT_STOCK", Message: "insufficient stock"}
)

// Domain business rules
func (o *Order) Validate() error {
	if o.CustomerID == "" {
		return fmt.Errorf("customer id is required")
	}
	if len(o.Items) == 0 {
		return fmt.Errorf("order must have at least one item")
	}
	if o.Total.Amount <= 0 {
		return fmt.Errorf("total must be positive")
	}
	return nil
}

func (o *Order) Cancel() error {
	if o.Status == OrderStatusShipped || o.Status == OrderStatusDelivered {
		return fmt.Errorf("cannot cancel shipped or delivered order")
	}
	o.Status = OrderStatusCancelled
	return nil
}

// ==================== REPOSITORY INTERFACES (Defined in Domain Layer) ====================

// Repository interfaces define what we need, not how it's implemented
type OrderRepository interface {
	FindByID(ctx context.Context, id string) (*Order, error)
	FindByCustomerID(ctx context.Context, customerID string) ([]*Order, error)
	Save(ctx context.Context, order *Order) error
	Update(ctx context.Context, order *Order) error
	Delete(ctx context.Context, id string) error
}

type ProductRepository interface {
	CheckStock(ctx context.Context, productID string, quantity int) (bool, error)
	ReserveStock(ctx context.Context, productID string, quantity int) error
}

// Domain service for complex business logic that doesn't belong to a single entity
type OrderDomainService interface {
	CalculateDiscount(order *Order) (Money, error)
	ValidateBusinessRules(order *Order) error
}

/*
HEXAGONAL ARCHITECTURE (Ports & Adapters):
Similar to Clean Architecture but emphasizes ports (interfaces) and adapters (implementations)
*/

// ==================== PORTS (Interfaces that define I/O) ====================

// Primary/Driving Ports (Incoming - what the application does)
type OrderService interface {
	PlaceOrder(ctx context.Context, cmd PlaceOrderCommand) (*Order, error)
	CancelOrder(ctx context.Context, orderID string) error
	GetOrder(ctx context.Context, orderID string) (*Order, error)
}

// Secondary/Driven Ports (Outgoing - what the application needs)
// Already defined above: OrderRepository, ProductRepository

// ==================== APPLICATION LAYER ====================

// DTOs for input/output (separate from domain entities)
type PlaceOrderCommand struct {
	CustomerID string
	Items      []OrderItemDTO
}

type OrderItemDTO struct {
	ProductID string `json:"product_id"`
	Quantity  int    `json:"quantity"`
}

type OrderResponse struct {
	ID         string               `json:"id"`
	CustomerID string               `json:"customer_id"`
	Items      []OrderItemResponse  `json:"items"`
	Status     string               `json:"status"`
	Total      MoneyResponse        `json:"total"`
	CreatedAt  time.Time            `json:"created_at"`
}

type OrderItemResponse struct {
	ProductID string        `json:"product_id"`
	Quantity  int           `json:"quantity"`
	Price     MoneyResponse `json:"price"`
}

type MoneyResponse struct {
	Amount   int64  `json:"amount"`
	Currency string `json:"currency"`
	Formatted string `json:"formatted"` // Presentation concern
}

// Application Service orchestrates domain objects and repositories
type orderServiceImpl struct {
	orderRepo   OrderRepository
	productRepo ProductRepository
	// Additional dependencies: payment service, notification service, etc.
}

// DEPENDENCY INJECTION (Manual, idiomatic Go)
// Constructor injection - dependencies provided at creation time
func NewOrderService(
	orderRepo OrderRepository,
	productRepo ProductRepository,
) OrderService {
	return &orderServiceImpl{
		orderRepo:   orderRepo,
		productRepo: productRepo,
	}
}

// Option pattern for optional dependencies
type OrderServiceOption func(*orderServiceImpl)

func WithLogger(logger *log.Logger) OrderServiceOption {
	return func(s *orderServiceImpl) {
		// s.logger = logger
	}
}

func NewOrderServiceWithOptions(
	orderRepo OrderRepository,
	productRepo ProductRepository,
	opts ...OrderServiceOption,
) OrderService {
	svc := &orderServiceImpl{
		orderRepo:   orderRepo,
		productRepo: productRepo,
	}
	
	for _, opt := range opts {
		opt(svc)
	}
	
	return svc
}

// Application service method
func (s *orderServiceImpl) PlaceOrder(ctx context.Context, cmd PlaceOrderCommand) (*Order, error) {
	// 1. Validate input
	if cmd.CustomerID == "" {
		return nil, fmt.Errorf("customer id is required")
	}
	
	// 2. Check stock for all items
	for _, item := range cmd.Items {
		available, err := s.productRepo.CheckStock(ctx, item.ProductID, item.Quantity)
		if err != nil {
			return nil, fmt.Errorf("failed to check stock: %w", err)
		}
		if !available {
			return nil, ErrInsufficientStock
		}
	}
	
	// 3. Create domain entity
	order := &Order{
		ID:         generateID(),
		CustomerID: cmd.CustomerID,
		Status:     OrderStatusPending,
		CreatedAt:  time.Now(),
	}
	
	// Convert DTO items to domain items
	for _, item := range cmd.Items {
		// In real app: fetch product price from repository
		order.Items = append(order.Items, OrderItem{
			ProductID: item.ProductID,
			Quantity:  item.Quantity,
			Price:     Money{Amount: 1000, Currency: "USD"}, // Example
		})
	}
	
	// 4. Calculate total
	total := Money{Amount: 0, Currency: "USD"}
	for _, item := range order.Items {
		// Simplified calculation
		itemTotal := Money{
			Amount:   item.Price.Amount * int64(item.Quantity),
			Currency: item.Price.Currency,
		}
		var err error
		total, err = total.Add(itemTotal)
		if err != nil {
			return nil, err
		}
	}
	order.Total = total
	
	// 5. Validate domain rules
	if err := order.Validate(); err != nil {
		return nil, fmt.Errorf("invalid order: %w", err)
	}
	
	// 6. Reserve stock
	for _, item := range order.Items {
		if err := s.productRepo.ReserveStock(ctx, item.ProductID, item.Quantity); err != nil {
			return nil, fmt.Errorf("failed to reserve stock: %w", err)
		}
	}
	
	// 7. Persist
	if err := s.orderRepo.Save(ctx, order); err != nil {
		// Compensating transaction: release reserved stock
		// In production: use Saga pattern for distributed transactions
		return nil, fmt.Errorf("failed to save order: %w", err)
	}
	
	return order, nil
}

func (s *orderServiceImpl) CancelOrder(ctx context.Context, orderID string) error {
	order, err := s.orderRepo.FindByID(ctx, orderID)
	if err != nil {
		return err
	}
	
	if err := order.Cancel(); err != nil {
		return err
	}
	
	return s.orderRepo.Update(ctx, order)
}

func (s *orderServiceImpl) GetOrder(ctx context.Context, orderID string) (*Order, error) {
	return s.orderRepo.FindByID(ctx, orderID)
}

// ==================== INFRASTRUCTURE LAYER ====================

// Adapters implement the ports defined by the domain/application layers

// Database adapter for OrderRepository
type PostgreSQLOrderRepository struct {
	db     interface{} // *sql.DB in real implementation
	logger *log.Logger
}

func NewPostgreSQLOrderRepository(db interface{}, logger *log.Logger) OrderRepository {
	return &PostgreSQLOrderRepository{
		db:     db,
		logger: logger,
	}
}

func (r *PostgreSQLOrderRepository) FindByID(ctx context.Context, id string) (*Order, error) {
	r.logger.Printf("Querying order %s from PostgreSQL", id)
	// Implementation using database/sql
	return &Order{ID: id}, nil
}

func (r *PostgreSQLOrderRepository) FindByCustomerID(ctx context.Context, customerID string) ([]*Order, error) {
	return nil, nil
}

func (r *PostgreSQLOrderRepository) Save(ctx context.Context, order *Order) error {
	r.logger.Printf("Saving order %s to PostgreSQL", order.ID)
	return nil
}

func (r *PostgreSQLOrderRepository) Update(ctx context.Context, order *Order) error {
	return nil
}

func (r *PostgreSQLOrderRepository) Delete(ctx context.Context, id string) error {
	return nil
}

// In-memory adapter for testing
type InMemoryOrderRepository struct {
	orders map[string]*Order
	mu     sync.RWMutex
}

func NewInMemoryOrderRepository() OrderRepository {
	return &InMemoryOrderRepository{
		orders: make(map[string]*Order),
	}
}

func (r *InMemoryOrderRepository) FindByID(ctx context.Context, id string) (*Order, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	
	order, exists := r.orders[id]
	if !exists {
		return nil, ErrOrderNotFound
	}
	return order, nil
}

func (r *InMemoryOrderRepository) Save(ctx context.Context, order *Order) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	
	r.orders[order.ID] = order
	return nil
}

// HTTP adapter (primary adapter)
type HTTPHandler struct {
	orderService OrderService
}

func NewHTTPHandler(orderService OrderService) *HTTPHandler {
	return &HTTPHandler{
		orderService: orderService,
	}
}

func (h *HTTPHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// Route to appropriate handler
}

// ==================== COMPOSITION ROOT ====================

func main() {
	// DEPENDENCY INJECTION CONTAINER (Manual composition)
	// Wire up all dependencies in one place
	
	// 1. Infrastructure dependencies
	logger := log.New(os.Stdout, "ORDER_API ", log.LstdFlags)
	
	// Simulate database connection
	var db interface{}
	
	// 2. Create repositories (choose implementation based on config)
	var orderRepo OrderRepository
	var productRepo ProductRepository
	
	env := os.Getenv("APP_ENV")
	if env == "test" {
		// Use in-memory for testing
		orderRepo = NewInMemoryOrderRepository()
		productRepo = NewInMemoryProductRepository()
	} else {
		// Use PostgreSQL for production
		orderRepo = NewPostgreSQLOrderRepository(db, logger)
		productRepo = NewPostgreSQLProductRepository(db, logger)
	}
	
	// 3. Create application service with dependencies
	orderService := NewOrderService(orderRepo, productRepo)
	
	// 4. Create HTTP handler with application service
	handler := NewHTTPHandler(orderService)
	
	// 5. Start server
	server := &http.Server{
		Addr:    ":8080",
		Handler: handler,
	}
	
	logger.Println("Starting server on :8080")
	if err := server.ListenAndServe(); err != nil {
		logger.Fatalf("Server failed: %v", err)
	}
}

/*
DOMAIN-DRIVEN DESIGN (Lightweight in Go):

1. Ubiquitous Language:
   - Use same terms in code as in business conversations
   - Order, Customer, Product, Inventory, Shipment

2. Bounded Contexts:
   - OrderContext: Order, OrderItem, OrderRepository
   - InventoryContext: Product, Stock, Reservation
   - Separate packages for each context

3. Aggregates:
   - Order is an aggregate root
   - OrderItem are entities within the Order aggregate
   - External references use ID only (CustomerID, not Customer)

4. Value Objects:
   - Money, Address, Email (immutable, no identity)

5. Domain Events:
   - OrderPlaced, OrderCancelled, PaymentReceived
*/

// Domain Event
type DomainEvent interface {
	AggregateID() string
	EventType() string
	OccurredAt() time.Time
}

type OrderPlacedEvent struct {
	OrderID    string
	CustomerID string
	Total      Money
	Items      []OrderItem
	Timestamp  time.Time
}

func (e OrderPlacedEvent) AggregateID() string { return e.OrderID }
func (e OrderPlacedEvent) EventType() string   { return "order.placed" }
func (e OrderPlacedEvent) OccurredAt() time.Time { return e.Timestamp }

// Event Bus interface
type EventBus interface {
	Publish(ctx context.Context, events ...DomainEvent) error
	Subscribe(eventType string, handler EventHandler)
}

/*
MONOLITH vs MICROSERVICES TRADEOFFS:

MONOLITH ADVANTAGES:
1. Simple deployment - one binary
2. Easy refactoring - shared types
3. ACID transactions across domain
4. Simple monitoring and logging
5. No network latency for internal calls

MONOLITH DISADVANTAGES:
1. Tight coupling
2. Can't scale components independently
3. Single point of failure
4. Difficult for large teams to work concurrently
5. Technology lock-in

MICROSERVICES ADVANTAGES:
1. Independent deployment and scaling
2. Technology diversity per service
3. Team autonomy
4. Fault isolation
5. Evolutionary design

MICROSERVICES DISADVANTAGES:
1. Distributed system complexity
2. Network latency and failures
3. Data consistency challenges (eventual consistency)
4. Operational overhead (monitoring, tracing, deployment)
5. Testing complexity

GUIDELINES FOR GO:
- Start with modular monolith using Clean Architecture
- Split to microservices when:
  * Team grows beyond 8-10 developers
  * Different scaling requirements per component
  * Different technology needs
  * Clear bounded contexts identified
- Use gRPC/protobuf for service communication
- Implement API Gateway for external access
- Use event-driven architecture for decoupling
*/

// Example of service boundaries in a modular monolith
package order // internal/order/
package inventory // internal/inventory/
package payment // internal/payment/
package shipping // internal/shipping/

// Communication between modules (in-process, type-safe)
type OrderModule struct {
	service OrderService
}

type InventoryModule struct {
	service InventoryService
}

// Event-driven communication between modules
func (m *OrderModule) PlaceOrder(ctx context.Context, cmd PlaceOrderCommand) error {
	order, err := m.service.PlaceOrder(ctx, cmd)
	if err != nil {
		return err
	}
	
	// Publish domain event
	event := OrderPlacedEvent{
		OrderID:    order.ID,
		CustomerID: order.CustomerID,
		Total:      order.Total,
		Items:      order.Items,
		Timestamp:  time.Now(),
	}
	
	// In-process event bus for monolith
	eventBus.Publish(ctx, event)
	
	return nil
}

// Consumer in another module
type InventoryModule struct {
	eventBus EventBus
}

func (m *InventoryModule) Start() {
	m.eventBus.Subscribe("order.placed", m.handleOrderPlaced)
}

func (m *InventoryModule) handleOrderPlaced(ctx context.Context, event OrderPlacedEvent) error {
	// Update inventory based on order
	for _, item := range event.Items {
		// Reserve stock
	}
	return nil
}

/*
PRACTICAL ADVICE FOR SENIOR DEVELOPERS:

1. Start Simple:
   - Begin with package-by-layer if unsure
   - Refactor to package-by-feature when boundaries are clear
   - Use internal/ package to prevent external dependencies

2. Dependency Injection:
   - Use constructor injection for required dependencies
   - Use option pattern for optional dependencies
   - Avoid global state and init() functions
   - Consider using wire (google/wire) for large projects

3. Testing Strategy:
   - Domain layer: unit tests
   - Application layer: integration tests with mocked repositories
   - Infrastructure layer: integration tests with real dependencies
   - Use testcontainers for external services

4. Error Handling:
   - Domain errors: define error types in domain layer
   - Application errors: wrap domain errors with context
   - Presentation errors: convert to HTTP status codes
   - Use errors.Is() and errors.As() for error inspection

5. Repository Pattern Nuances:
   - Query methods should return domain entities or value objects
   - Consider CQRS for complex queries
   - Use specification pattern for complex queries

6. Transaction Management:
   - Use context.Context for transaction boundaries
   - Implement Unit of Work pattern for complex operations
   - Consider eventual consistency for distributed systems
*/

// Unit of Work pattern
type UnitOfWork interface {
	Begin(ctx context.Context) (context.Context, error)
	Commit(ctx context.Context) error
	Rollback(ctx context.Context) error
}

type OrderServiceWithUoW struct {
	uow UnitOfWork
}

func (s *OrderServiceWithUoW) PlaceOrder(ctx context.Context, cmd PlaceOrderCommand) (*Order, error) {
	ctx, err := s.uow.Begin(ctx)
	if err != nil {
		return nil, err
	}
	
	defer func() {
		if r := recover(); r != nil {
			s.uow.Rollback(ctx)
			panic(r)
		}
	}()
	
	order, err := s.placeOrder(ctx, cmd)
	if err != nil {
		s.uow.Rollback(ctx)
		return nil, err
	}
	
	if err := s.uow.Commit(ctx); err != nil {
		return nil, err
	}
	
	return order, nil
}

// Helper functions
func generateID() string {
	return fmt.Sprintf("order_%d", time.Now().UnixNano())
}

type InMemoryProductRepository struct{}
func NewInMemoryProductRepository() ProductRepository { return &InMemoryProductRepository{} }
func (r *InMemoryProductRepository) CheckStock(ctx context.Context, productID string, quantity int) (bool, error) {
	return true, nil
}
func (r *InMemoryProductRepository) ReserveStock(ctx context.Context, productID string, quantity int) error {
	return nil
}

type PostgreSQLProductRepository struct {
	db interface{}
	logger *log.Logger
}
func NewPostgreSQLProductRepository(db interface{}, logger *log.Logger) ProductRepository {
	return &PostgreSQLProductRepository{db: db, logger: logger}
}
func (r *PostgreSQLProductRepository) CheckStock(ctx context.Context, productID string, quantity int) (bool, error) {
	return true, nil
}
func (r *PostgreSQLProductRepository) ReserveStock(ctx context.Context, productID string, quantity int) error {
	return nil
}

var eventBus EventBus
var sync.Mutex

type InventoryService interface{}