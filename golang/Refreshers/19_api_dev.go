package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"strings"
	"time"

	// Third-party libraries for different frameworks
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-playground/validator/v10"
	"github.com/gorilla/mux"
	"golang.org/x/time/rate"
)

// =============================================
// 1. NET/HTTP INTERNALS
// =============================================

func NetHTTPInternals() {
	// Understanding the http.Server struct
	server := &http.Server{
		Addr:           ":8080",
		Handler:        http.DefaultServeMux,
		ReadTimeout:    15 * time.Second,
		WriteTimeout:   30 * time.Second,
		IdleTimeout:    120 * time.Second,
		MaxHeaderBytes: 1 << 20, // 1MB
	}

	// http.Request internals
	fmt.Println("=== HTTP Request Structure ===")
	fmt.Println("Request contains:")
	fmt.Println("- Method (GET, POST, etc.)")
	fmt.Println("- URL (parsed)")
	fmt.Println("- Proto (HTTP/1.1, HTTP/2)")
	fmt.Println("- Header (map[string][]string)")
	fmt.Println("- Body (io.ReadCloser)")
	fmt.Println("- ContentLength")
	fmt.Println("- Host")
	fmt.Println("- RemoteAddr")
	fmt.Println("- TLS (if using HTTPS)")
	fmt.Println("- Context (carries deadlines, cancellation)")

	// http.ResponseWriter interface
	fmt.Println("\n=== ResponseWriter Interface ===")
	fmt.Println("Methods:")
	fmt.Println("- Header() http.Header")
	fmt.Println("- Write([]byte) (int, error)")
	fmt.Println("- WriteHeader(statusCode int)")

	// Understanding Handler interface
	type Handler interface {
		ServeHTTP(http.ResponseWriter, *http.Request)
	}
}

// =============================================
// 2. HTTP HANDLERS & MIDDLEWARE (Standard Library)
// =============================================

// HandlerFunc type conversion
func basicHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, %s!", r.URL.Path[1:])
}

// Custom handler type
type MyHandler struct{}

func (h *MyHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{
		"message": "Hello from custom handler",
		"method":  r.Method,
		"path":    r.URL.Path,
	})
}

// =============================================
// 3. MIDDLEWARE PATTERNS
// =============================================

// Chainable middleware pattern
type Middleware func(http.Handler) http.Handler

// Logging middleware
func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		// Wrap response writer to capture status code
		rw := &responseLogger{w: w, status: 200}

		next.ServeHTTP(rw, r)

		log.Printf("%s %s %d %s", r.Method, r.URL.Path, rw.status, time.Since(start))
	})
}

type responseLogger struct {
	w      http.ResponseWriter
	status int
}

func (rl *responseLogger) Header() http.Header {
	return rl.w.Header()
}

func (rl *responseLogger) Write(b []byte) (int, error) {
	return rl.w.Write(b)
}

func (rl *responseLogger) WriteHeader(statusCode int) {
	rl.status = statusCode
	rl.w.WriteHeader(statusCode)
}

// Authentication middleware
func authMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		token := r.Header.Get("Authorization")
		if token == "" {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}

		// Validate token (simplified)
		if !strings.HasPrefix(token, "Bearer ") {
			http.Error(w, "Invalid token format", http.StatusUnauthorized)
			return
		}

		// Add user info to context
		ctx := context.WithValue(r.Context(), "userID", "123")
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

// Chain multiple middleware
func chain(middlewares ...Middleware) Middleware {
	return func(next http.Handler) http.Handler {
		for i := len(middlewares) - 1; i >= 0; i-- {
			next = middlewares[i](next)
		}
		return next
	}
}

// =============================================
// 4. ROUTING STRATEGIES
// =============================================

func RoutingExamples() {
	// Standard library routing with http.ServeMux
	mux := http.NewServeMux()

	// Basic route
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "Home page")
	})

	// Route with pattern
	mux.HandleFunc("/users/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "Users page")
	})

	// Route parameters (standard library doesn't have built-in)
	mux.HandleFunc("/users/", func(w http.ResponseWriter, r *http.Request) {
		// Manual parsing
		path := r.URL.Path
		if strings.HasPrefix(path, "/users/") {
			userID := path[len("/users/"):]
			fmt.Fprintf(w, "User ID: %s", userID)
		}
	})

	// Subrouting
	userMux := http.NewServeMux()
	userMux.HandleFunc("/profile", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "User profile")
	})
	mux.Handle("/users/", http.StripPrefix("/users", userMux))
}

// =============================================
// 5. RESTful API DESIGN
// =============================================

type User struct {
	ID        string    `json:"id" xml:"id"`
	Name      string    `json:"name" xml:"name"`
	Email     string    `json:"email" xml:"email"`
	CreatedAt time.Time `json:"created_at" xml:"created_at"`
}

type UserService struct {
	users map[string]User
}

// RESTful User Resource
func (s *UserService) SetupRoutes(router *mux.Router) {
	// CRUD operations following REST conventions
	router.HandleFunc("/users", s.CreateUser).Methods("POST")
	router.HandleFunc("/users", s.ListUsers).Methods("GET")
	router.HandleFunc("/users/{id}", s.GetUser).Methods("GET")
	router.HandleFunc("/users/{id}", s.UpdateUser).Methods("PUT")
	router.HandleFunc("/users/{id}", s.PartialUpdateUser).Methods("PATCH")
	router.HandleFunc("/users/{id}", s.DeleteUser).Methods("DELETE")

	// Nested resources
	router.HandleFunc("/users/{id}/posts", s.GetUserPosts).Methods("GET")
}

func (s *UserService) CreateUser(w http.ResponseWriter, r *http.Request) {
	var user User
	if err := json.NewDecoder(r.Body).Decode(&user); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Generate ID
	user.ID = "user_" + strconv.FormatInt(time.Now().UnixNano(), 10)
	user.CreatedAt = time.Now()

	s.users[user.ID] = user

	w.Header().Set("Location", "/users/"+user.ID)
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}

func (s *UserService) GetUser(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	user, exists := s.users[id]
	if !exists {
		http.Error(w, "User not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(user)
}

// =============================================
// 6. JSON SERIALIZATION & VALIDATION
// =============================================

// Struct tags for JSON
type Product struct {
	ID        string     `json:"id"`
	Name      string     `json:"name"`
	Price     float64    `json:"price"`
	SKU       string     `json:"sku"`
	Category  string     `json:"category,omitempty"` // omit if empty
	Tags      []string   `json:"tags"`
	CreatedAt time.Time  `json:"created_at"`
	UpdatedAt *time.Time `json:"updated_at,omitempty"` // pointer to omit null

	// Custom JSON field name
	InventoryCount int `json:"-"` // Always omit
}

// Custom JSON marshaling
func (p Product) MarshalJSON() ([]byte, error) {
	type Alias Product
	return json.Marshal(&struct {
		Alias
		FormattedPrice string `json:"formatted_price"`
	}{
		Alias:          (Alias)(p),
		FormattedPrice: fmt.Sprintf("$%.2f", p.Price),
	})
}

// Validation using go-playground/validator
var validate = validator.New()

type CreateUserRequest struct {
	Name     string `json:"name" validate:"required,min=2,max=100"`
	Email    string `json:"email" validate:"required,email"`
	Age      int    `json:"age" validate:"gte=0,lte=130"`
	Password string `json:"password" validate:"required,min=8"`
}

func validateUserRequest(w http.ResponseWriter, r *http.Request) {
	var req CreateUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Validate struct
	if err := validate.Struct(req); err != nil {
		validationErrors := err.(validator.ValidationErrors)
		http.Error(w, validationErrors.Error(), http.StatusBadRequest)
		return
	}

	// Process valid request...
}

// =============================================
// 7. ERROR RESPONSES & STATUS CODES
// =============================================

type APIError struct {
	StatusCode int    `json:"status_code"`
	Message    string `json:"message"`
	Code       string `json:"code,omitempty"`
	Details    any    `json:"details,omitempty"`
	Timestamp  string `json:"timestamp"`
}

func NewAPIError(statusCode int, message, code string) *APIError {
	return &APIError{
		StatusCode: statusCode,
		Message:    message,
		Code:       code,
		Timestamp:  time.Now().UTC().Format(time.RFC3339),
	}
}

func WriteJSONError(w http.ResponseWriter, err *APIError) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(err.StatusCode)
	json.NewEncoder(w).Encode(err)
}

// Common HTTP status code usage
func StatusCodeExamples() {
	fmt.Println("=== Common HTTP Status Codes ===")
	fmt.Println("2xx - Success:")
	fmt.Println("200 OK - Standard response")
	fmt.Println("201 Created - Resource created")
	fmt.Println("204 No Content - Success, no body")

	fmt.Println("\n3xx - Redirection:")
	fmt.Println("301 Moved Permanently")
	fmt.Println("302 Found - Temporary redirect")
	fmt.Println("304 Not Modified - Cached response")

	fmt.Println("\n4xx - Client Errors:")
	fmt.Println("400 Bad Request - Invalid request")
	fmt.Println("401 Unauthorized - Authentication needed")
	fmt.Println("403 Forbidden - No permission")
	fmt.Println("404 Not Found - Resource not found")
	fmt.Println("422 Unprocessable Entity - Validation error")
	fmt.Println("429 Too Many Requests - Rate limiting")

	fmt.Println("\n5xx - Server Errors:")
	fmt.Println("500 Internal Server Error")
	fmt.Println("502 Bad Gateway")
	fmt.Println("503 Service Unavailable")
	fmt.Println("504 Gateway Timeout")
}

// =============================================
// 8. PAGINATION, FILTERING, SORTING
// =============================================

type PaginationParams struct {
	Page     int    `json:"page" query:"page"`
	PageSize int    `json:"page_size" query:"page_size"`
	SortBy   string `json:"sort_by" query:"sort_by"`
	SortDir  string `json:"sort_dir" query:"sort_dir"` // asc or desc
}

type FilterParams struct {
	Name     string `json:"name" query:"name"`
	Category string `json:"category" query:"category"`
	MinPrice string `json:"min_price" query:"min_price"`
	MaxPrice string `json:"max_price" query:"max_price"`
}

type PaginatedResponse[T any] struct {
	Data       []T   `json:"data"`
	Page       int   `json:"page"`
	PageSize   int   `json:"page_size"`
	TotalCount int64 `json:"total_count"`
	TotalPages int   `json:"total_pages"`
	HasNext    bool  `json:"has_next"`
	HasPrev    bool  `json:"has_prev"`
}

func handleListUsers(w http.ResponseWriter, r *http.Request) {
	// Parse query parameters
	query := r.URL.Query()

	page, _ := strconv.Atoi(query.Get("page"))
	if page < 1 {
		page = 1
	}

	pageSize, _ := strconv.Atoi(query.Get("page_size"))
	if pageSize < 1 || pageSize > 100 {
		pageSize = 20 // Default
	}

	sortBy := query.Get("sort_by")
	if sortBy == "" {
		sortBy = "created_at"
	}

	// Build filter from query params
	filters := make(map[string]interface{})
	if name := query.Get("name"); name != "" {
		filters["name"] = name
	}
	if category := query.Get("category"); category != "" {
		filters["category"] = category
	}

	// Calculate offset
	offset := (page - 1) * pageSize

	// In real app, pass to database
	fmt.Printf("Page: %d, Size: %d, Sort: %s, Filters: %v\n",
		page, pageSize, sortBy, filters)

	// Return paginated response
	response := PaginatedResponse[User]{
		Data:       []User{},
		Page:       page,
		PageSize:   pageSize,
		TotalCount: 100,
		TotalPages: 5,
		HasNext:    page < 5,
		HasPrev:    page > 1,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

// =============================================
// 9. POPULAR WEB FRAMEWORKS
// =============================================

// GIN Framework Example
func GinExample() {
	/*
	   // Uncomment to use Gin
	   router := gin.Default()

	   // Middleware
	   router.Use(gin.Logger())
	   router.Use(gin.Recovery())

	   // Routes
	   router.GET("/users", func(c *gin.Context) {
	       c.JSON(200, gin.H{
	           "message": "GET users",
	       })
	   })

	   router.POST("/users", func(c *gin.Context) {
	       var user User
	       if err := c.ShouldBindJSON(&user); err != nil {
	           c.JSON(400, gin.H{"error": err.Error()})
	           return
	       }
	       c.JSON(201, user)
	   })

	   // Path parameters
	   router.GET("/users/:id", func(c *gin.Context) {
	       id := c.Param("id")
	       c.JSON(200, gin.H{"id": id})
	   })

	   // Query parameters
	   router.GET("/search", func(c *gin.Context) {
	       query := c.Query("q")
	       c.JSON(200, gin.H{"query": query})
	   })
	*/
}

// Echo Framework Example
func EchoExample() {
	/*
	   e := echo.New()

	   // Middleware
	   e.Use(middleware.Logger())
	   e.Use(middleware.Recover())

	   // Routes
	   e.GET("/", func(c echo.Context) error {
	       return c.String(200, "Hello, World!")
	   })

	   e.POST("/users", func(c echo.Context) error {
	       u := new(User)
	       if err := c.Bind(u); err != nil {
	           return err
	       }
	       return c.JSON(201, u)
	   })

	   // Group routes
	   api := e.Group("/api")
	   api.Use(middleware.JWT([]byte("secret")))
	   api.GET("/users", getUsers)
	*/
}

// Chi Framework Example
func ChiExample() {
	r := chi.NewRouter()

	// Chi middleware
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Timeout(60 * time.Second))

	// Routes
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("Welcome"))
	})

	// Route groups
	r.Route("/users", func(r chi.Router) {
		r.Use(authMiddleware)

		r.Get("/", func(w http.ResponseWriter, r *http.Request) {
			w.Write([]byte("List users"))
		})

		r.Post("/", func(w http.ResponseWriter, r *http.Request) {
			w.Write([]byte("Create user"))
		})

		// Subroutes with path parameters
		r.Route("/{userID}", func(r chi.Router) {
			r.Get("/", func(w http.ResponseWriter, r *http.Request) {
				userID := chi.URLParam(r, "userID")
				w.Write([]byte("User: " + userID))
			})

			r.Put("/", func(w http.ResponseWriter, r *http.Request) {
				w.Write([]byte("Update user"))
			})

			r.Delete("/", func(w http.ResponseWriter, r *http.Request) {
				w.Write([]byte("Delete user"))
			})
		})
	})

	// File server
	r.Handle("/static/*", http.StripPrefix("/static/",
		http.FileServer(http.Dir("./static"))))
}

// Fiber Example
func FiberExample() {
	/*
	   app := fiber.New()

	   // Middleware
	   app.Use(logger.New())
	   app.Use(recover.New())

	   // Routes
	   app.Get("/", func(c *fiber.Ctx) error {
	       return c.SendString("Hello, World!")
	   })

	   // JSON response
	   app.Get("/json", func(c *fiber.Ctx) error {
	       return c.JSON(fiber.Map{
	           "message": "Hello JSON",
	       })
	   })

	   // Path parameters
	   app.Get("/users/:id", func(c *fiber.Ctx) error {
	       return c.SendString("User: " + c.Params("id"))
	   })
	*/
}

// =============================================
// 10. REQUEST/VALIDATION MIDDLEWARE
// =============================================

// Validation middleware using validator
func ValidationMiddleware(next http.HandlerFunc, v interface{}) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// Decode request body
		if err := json.NewDecoder(r.Body).Decode(v); err != nil {
			WriteJSONError(w, NewAPIError(http.StatusBadRequest,
				"Invalid JSON", "INVALID_JSON"))
			return
		}

		// Validate using go-playground/validator
		if err := validate.Struct(v); err != nil {
			validationErrors := make(map[string]string)
			for _, err := range err.(validator.ValidationErrors) {
				validationErrors[err.Field()] = err.Tag()
			}

			WriteJSONError(w, &APIError{
				StatusCode: http.StatusUnprocessableEntity,
				Message:    "Validation failed",
				Code:       "VALIDATION_ERROR",
				Details:    validationErrors,
				Timestamp:  time.Now().UTC().Format(time.RFC3339),
			})
			return
		}

		// Store validated data in context
		ctx := context.WithValue(r.Context(), "validated_data", v)
		next.ServeHTTP(w, r.WithContext(ctx))
	}
}

// =============================================
// 11. API VERSIONING STRATEGIES
// =============================================

// Strategy 1: URL Path versioning
func URLPathVersioning() {
	router := mux.NewRouter()

	// API v1
	v1 := router.PathPrefix("/api/v1").Subrouter()
	v1.HandleFunc("/users", v1GetUsers).Methods("GET")
	v1.HandleFunc("/users/{id}", v1GetUser).Methods("GET")

	// API v2
	v2 := router.PathPrefix("/api/v2").Subrouter()
	v2.HandleFunc("/users", v2GetUsers).Methods("GET")
	v2.HandleFunc("/users/{id}", v2GetUser).Methods("GET")
}

// Strategy 2: Header versioning
func HeaderVersioning(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		version := r.Header.Get("API-Version")
		if version == "" {
			version = "v1" // Default version
		}

		// Add version to context
		ctx := context.WithValue(r.Context(), "api_version", version)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

// Strategy 3: Accept header versioning
func AcceptHeaderVersioning(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		accept := r.Header.Get("Accept")

		var version string
		if strings.Contains(accept, "application/vnd.myapp.v2+json") {
			version = "v2"
		} else if strings.Contains(accept, "application/vnd.myapp.v1+json") {
			version = "v1"
		} else {
			version = "v1" // Default
		}

		ctx := context.WithValue(r.Context(), "api_version", version)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

func v1GetUsers(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(map[string]string{
		"version": "v1",
		"message": "Users API v1",
	})
}

func v2GetUsers(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(map[string]string{
		"version": "v2",
		"message": "Users API v2 with enhanced features",
	})
}

// =============================================
// 12. RATE LIMITING
// =============================================

type RateLimiter struct {
	limiter *rate.Limiter
}

func NewRateLimiter(r rate.Limit, b int) *RateLimiter {
	return &RateLimiter{
		limiter: rate.NewLimiter(r, b),
	}
}

func (rl *RateLimiter) Limit(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if !rl.limiter.Allow() {
			WriteJSONError(w, NewAPIError(http.StatusTooManyRequests,
				"Rate limit exceeded", "RATE_LIMITED"))
			return
		}
		next.ServeHTTP(w, r)
	})
}

// IP-based rate limiting
type IPRateLimiter struct {
	ips map[string]*rate.Limiter
	mu  sync.RWMutex
	r   rate.Limit
	b   int
}

func NewIPRateLimiter(r rate.Limit, b int) *IPRateLimiter {
	return &IPRateLimiter{
		ips: make(map[string]*rate.Limiter),
		r:   r,
		b:   b,
	}
}

func (i *IPRateLimiter) AddIP(ip string) *rate.Limiter {
	i.mu.Lock()
	defer i.mu.Unlock()

	limiter := rate.NewLimiter(i.r, i.b)
	i.ips[ip] = limiter

	return limiter
}

func (i *IPRateLimiter) GetLimiter(ip string) *rate.Limiter {
	i.mu.Lock()
	limiter, exists := i.ips[ip]

	if !exists {
		i.mu.Unlock()
		return i.AddIP(ip)
	}

	i.mu.Unlock()
	return limiter
}

func (i *IPRateLimiter) Middleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ip := strings.Split(r.RemoteAddr, ":")[0]
		limiter := i.GetLimiter(ip)

		if !limiter.Allow() {
			WriteJSONError(w, NewAPIError(http.StatusTooManyRequests,
				"Rate limit exceeded", "RATE_LIMITED"))
			return
		}

		next.ServeHTTP(w, r)
	})
}

// =============================================
// 13. SWAGGER/OPENAPI DOCUMENTATION
// =============================================

// Using swaggo/swag for Go Swagger documentation
// Install: go get -u github.com/swaggo/swag/cmd/swag

// @title Users API
// @version 1.0
// @description This is a sample users API
// @termsOfService http://swagger.io/terms/

// @contact.name API Support
// @contact.email support@myapi.com

// @license.name Apache 2.0
// @license.url http://www.apache.org/licenses/LICENSE-2.0.html

// @host localhost:8080
// @BasePath /api/v1

// @securityDefinitions.apikey ApiKeyAuth
// @in header
// @name Authorization

// GetUsers godoc
// @Summary List users
// @Description Get list of users with pagination
// @Tags users
// @Accept json
// @Produce json
// @Param page query int false "Page number"
// @Param limit query int false "Items per page"
// @Param name query string false "Filter by name"
// @Success 200 {object} PaginatedResponse[User]
// @Failure 400 {object} APIError
// @Failure 500 {object} APIError
// @Router /users [get]
func GetUsersHandler(w http.ResponseWriter, r *http.Request) {
	// Handler implementation
}

// CreateUser godoc
// @Summary Create a new user
// @Description Create a new user with the input payload
// @Tags users
// @Accept json
// @Produce json
// @Param user body CreateUserRequest true "User data"
// @Success 201 {object} User
// @Failure 400 {object} APIError
// @Failure 422 {object} APIError
// @Failure 500 {object} APIError
// @Router /users [post]
func CreateUserHandler(w http.ResponseWriter, r *http.Request) {
	// Handler implementation
}

// =============================================
// 14. GRAPHQL WITH GQLGEN
// =============================================

/*
// gqlgen requires code generation
// Create schema.graphql:

schema {
    query: Query
    mutation: Mutation
}

type Query {
    users: [User!]!
    user(id: ID!): User
}

type Mutation {
    createUser(input: NewUser!): User!
    updateUser(id: ID!, input: UpdateUser!): User!
}

type User {
    id: ID!
    name: String!
    email: String!
    createdAt: Time!
}

input NewUser {
    name: String!
    email: String!
}

input UpdateUser {
    name: String
    email: String
}

scalar Time

// Generate code: go run github.com/99designs/gqlgen generate

// Resolver implementation
type userResolver struct{}

func (r *userResolver) Users(ctx context.Context) ([]*User, error) {
    // Return users from database
    return []*User{
        {ID: "1", Name: "John", Email: "john@example.com"},
    }, nil
}

func (r *userResolver) CreateUser(ctx context.Context, input NewUser) (*User, error) {
    // Create user in database
    user := &User{
        ID:   generateID(),
        Name: input.Name,
        Email: input.Email,
        CreatedAt: time.Now(),
    }
    return user, nil
}
*/

// =============================================
// 15. COMPLETE API SERVER EXAMPLE
// =============================================

type APIServer struct {
	router      *chi.Mux
	userService *UserService
	rateLimiter *IPRateLimiter
}

func NewAPIServer() *APIServer {
	server := &APIServer{
		router:      chi.NewRouter(),
		userService: &UserService{users: make(map[string]User)},
		rateLimiter: NewIPRateLimiter(rate.Limit(10), 30), // 10 req/sec, burst 30
	}

	server.setupRoutes()
	return server
}

func (s *APIServer) setupRoutes() {
	r := s.router

	// Global middleware
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(s.rateLimiter.Middleware)

	// Health check
	r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{
			"status": "healthy",
			"time":   time.Now().UTC().Format(time.RFC3339),
		})
	})

	// API routes with versioning
	r.Route("/api/v1", func(r chi.Router) {
		// Public routes
		r.Post("/auth/login", s.handleLogin)
		r.Post("/auth/register", s.handleRegister)

		// Protected routes
		r.Group(func(r chi.Router) {
			r.Use(authMiddleware)

			r.Route("/users", func(r chi.Router) {
				r.Get("/", s.handleListUsers)   // GET /api/v1/users?page=1&limit=20
				r.Post("/", s.handleCreateUser) // POST /api/v1/users

				r.Route("/{userID}", func(r chi.Router) {
					r.Get("/", s.handleGetUser)       // GET /api/v1/users/{id}
					r.Put("/", s.handleUpdateUser)    // PUT /api/v1/users/{id}
					r.Delete("/", s.handleDeleteUser) // DELETE /api/v1/users/{id}
				})
			})
		})
	})

	// Swagger UI (if configured)
	r.Handle("/swagger/*", http.StripPrefix("/swagger/",
		http.FileServer(http.Dir("./swagger"))))
}

func (s *APIServer) handleLogin(w http.ResponseWriter, r *http.Request) {
	// Login implementation
	w.Write([]byte("Login endpoint"))
}

func (s *APIServer) handleRegister(w http.ResponseWriter, r *http.Request) {
	var req CreateUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		WriteJSONError(w, NewAPIError(http.StatusBadRequest,
			"Invalid request", "INVALID_REQUEST"))
		return
	}

	// Validate
	if err := validate.Struct(req); err != nil {
		WriteJSONError(w, NewAPIError(http.StatusUnprocessableEntity,
			"Validation failed", "VALIDATION_ERROR"))
		return
	}

	// Create user
	user := User{
		ID:        "user_" + strconv.FormatInt(time.Now().UnixNano(), 10),
		Name:      req.Name,
		Email:     req.Email,
		CreatedAt: time.Now(),
	}

	s.userService.users[user.ID] = user

	w.Header().Set("Location", "/api/v1/users/"+user.ID)
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}

func (s *APIServer) handleListUsers(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query()
	page, _ := strconv.Atoi(query.Get("page"))
	limit, _ := strconv.Atoi(query.Get("limit"))

	if page < 1 {
		page = 1
	}
	if limit < 1 || limit > 100 {
		limit = 20
	}

	// Get users from service (simplified)
	users := make([]User, 0, len(s.userService.users))
	for _, user := range s.userService.users {
		users = append(users, user)
	}

	// Apply pagination
	start := (page - 1) * limit
	end := start + limit
	if start > len(users) {
		start = len(users)
	}
	if end > len(users) {
		end = len(users)
	}

	paginatedUsers := users[start:end]

	response := PaginatedResponse[User]{
		Data:       paginatedUsers,
		Page:       page,
		PageSize:   limit,
		TotalCount: int64(len(users)),
		TotalPages: (len(users) + limit - 1) / limit,
		HasNext:    end < len(users),
		HasPrev:    page > 1,
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func (s *APIServer) handleCreateUser(w http.ResponseWriter, r *http.Request) {
	s.handleRegister(w, r) // Reuse same logic for now
}

func (s *APIServer) handleGetUser(w http.ResponseWriter, r *http.Request) {
	userID := chi.URLParam(r, "userID")

	user, exists := s.userService.users[userID]
	if !exists {
		WriteJSONError(w, NewAPIError(http.StatusNotFound,
			"User not found", "USER_NOT_FOUND"))
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(user)
}

func (s *APIServer) Start(addr string) error {
	fmt.Printf("Server starting on %s\n", addr)
	return http.ListenAndServe(addr, s.router)
}

// =============================================
// MAIN FUNCTION - DEMO
// =============================================

func main() {
	fmt.Println("=== Go HTTP & API Development Demo ===\n")

	// 1. Show HTTP internals
	NetHTTPInternals()

	// 2. Demonstrate middleware chain
	fmt.Println("\n=== Middleware Chain ===")
	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "Final handler")
	})

	// Create middleware chain
	chain := chain(
		loggingMiddleware,
		authMiddleware,
	)

	wrappedHandler := chain(handler)
	fmt.Println("Handler wrapped with logging and auth middleware")

	// 3. Demonstrate routing strategies
	fmt.Println("\n=== Routing Strategies ===")
	RoutingExamples()

	// 4. Show JSON validation
	fmt.Println("\n=== JSON Validation ===")
	validUser := CreateUserRequest{
		Name:     "John Doe",
		Email:    "john@example.com",
		Age:      30,
		Password: "secure123",
	}

	if err := validate.Struct(validUser); err != nil {
		fmt.Printf("Validation error: %v\n", err)
	} else {
		fmt.Println("User validation passed")
	}

	// 5. Show pagination
	fmt.Println("\n=== Pagination Example ===")
	fmt.Println("Query: /users?page=2&page_size=10&sort_by=name&name=John")

	// 6. Show status codes
	StatusCodeExamples()

	// 7. Start demo server
	fmt.Println("\n=== Starting Demo Server ===")

	server := NewAPIServer()

	// Start server in goroutine for demo
	go func() {
		if err := server.Start(":8080"); err != nil {
			log.Fatal(err)
		}
	}()

	// Keep main running for demo
	fmt.Println("Demo server running on http://localhost:8080")
	fmt.Println("Endpoints:")
	fmt.Println("  GET  /health")
	fmt.Println("  GET  /api/v1/users")
	fmt.Println("  POST /api/v1/auth/register")
	fmt.Println("\nPress Ctrl+C to exit")

	select {} // Block forever
}

// Helper functions
var sync struct {
	sync.RWMutex
}

// For compilation
func init() {
	// Initialize validator
	validate = validator.New()
}
