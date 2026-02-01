/*
GOLANG MICROSERVICES & DISTRIBUTED SYSTEMS GUIDE - PART 2
Advanced Concepts with Practical Implementations
===================================================
*/

// ============================================================================
// 1. gRPC WITH PROTOCOL BUFFERS - High-Performance RPC Framework
// ============================================================================

package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/keepalive"
	"google.golang.org/grpc/metadata"
	"google.golang.org/grpc/reflection"
	"google.golang.org/grpc/status"
)

// STEP 1: Define Protocol Buffers (.proto file)
/*
// user_service.proto
syntax = "proto3";

package user.v1;

option go_package = "github.com/yourorg/proto/user/v1;userv1";

import "google/protobuf/timestamp.proto";
import "google/api/annotations.proto"; // For REST mapping

// Service definition
service UserService {
  // Unary RPC
  rpc GetUser(GetUserRequest) returns (UserResponse) {
    option (google.api.http) = {
      get: "/v1/users/{user_id}"
    };
  }
  
  // Server streaming
  rpc ListUsers(ListUsersRequest) returns (stream UserResponse);
  
  // Client streaming
  rpc CreateUsers(stream CreateUserRequest) returns (CreateUsersResponse);
  
  // Bidirectional streaming
  rpc Chat(stream ChatMessage) returns (stream ChatMessage);
  
  // With deadlines
  rpc SearchUsers(SearchUsersRequest) returns (SearchUsersResponse) {
    option (google.api.http) = {
      post: "/v1/users:search"
      body: "*"
    };
  }
}

// Message definitions
message GetUserRequest {
  string user_id = 1;  // Field numbers 1-15 use 1 byte, 16-2047 use 2 bytes
}

message UserResponse {
  string id = 1;
  string name = 2;
  string email = 3;
  UserStatus status = 4;
  google.protobuf.Timestamp created_at = 5;
  google.protobuf.Timestamp updated_at = 6;
  map<string, string> metadata = 7;  // Proto3 supports maps
  repeated string tags = 8;          // Repeated fields (arrays)
}

enum UserStatus {
  USER_STATUS_UNSPECIFIED = 0;  // Always have a zero value
  USER_STATUS_ACTIVE = 1;
  USER_STATUS_INACTIVE = 2;
  USER_STATUS_SUSPENDED = 3;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
  string filter = 3;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
  string password = 3;
}

message CreateUsersResponse {
  repeated UserResponse users = 1;
  int32 created_count = 2;
}

message SearchUsersRequest {
  string query = 1;
  int32 limit = 2;
}

message SearchUsersResponse {
  repeated UserResponse users = 1;
  string next_page_token = 2;
  int32 total_count = 3;
}

message ChatMessage {
  string user_id = 1;
  string message = 2;
  google.protobuf.Timestamp timestamp = 3;
}

// Error definitions
message ErrorDetail {
  string code = 1;
  string message = 2;
  map<string, string> metadata = 3;
}
*/

// STEP 2: Generate Go code from .proto files
/*
# Generate gRPC code
protoc \
  --go_out=. \
  --go_opt=paths=source_relative \
  --go-grpc_out=. \
  --go-grpc_opt=paths=source_relative \
  user_service.proto

# With HTTP annotations for gRPC-Gateway
protoc \
  --grpc-gateway_out=. \
  --grpc-gateway_opt=paths=source_relative \
  user_service.proto
*/

// STEP 3: Implement gRPC Server
type UserServiceServer struct {
	userv1.UnimplementedUserServiceServer // Embed for forward compatibility
	userStore UserStore
}

func NewUserServiceServer(store UserStore) *UserServiceServer {
	return &UserServiceServer{userStore: store}
}

// Unary RPC implementation
func (s *UserServiceServer) GetUser(ctx context.Context, req *userv1.GetUserRequest) (*userv1.UserResponse, error) {
	// Extract metadata from context
	if md, ok := metadata.FromIncomingContext(ctx); ok {
		log.Printf("Request metadata: %v", md)
	}

	// Check deadline
	if deadline, ok := ctx.Deadline(); ok {
		if time.Until(deadline) < 50*time.Millisecond {
			return nil, status.Error(codes.DeadlineExceeded, "not enough time remaining")
		}
	}

	// Business logic
	user, err := s.userStore.GetUser(req.UserId)
	if err != nil {
		// Convert to gRPC status error
		st := status.New(codes.NotFound, "user not found")
		ds, err := st.WithDetails(&userv1.ErrorDetail{
			Code:    "USER_NOT_FOUND",
			Message: fmt.Sprintf("User %s not found", req.UserId),
		})
		if err == nil {
			return nil, ds.Err()
		}
		return nil, st.Err()
	}

	// Return response
	return &userv1.UserResponse{
		Id:        user.ID,
		Name:      user.Name,
		Email:     user.Email,
		Status:    userv1.UserStatus(user.Status),
		CreatedAt: timestamppb.New(user.CreatedAt),
		Metadata:  user.Metadata,
	}, nil
}

// Server Streaming implementation
func (s *UserServiceServer) ListUsers(req *userv1.ListUsersRequest, stream userv1.UserService_ListUsersServer) error {
	users, err := s.userStore.ListUsers(req.Filter, int(req.PageSize))
	if err != nil {
		return status.Error(codes.Internal, err.Error())
	}

	// Stream users one by one
	for _, user := range users {
		resp := &userv1.UserResponse{
			Id:    user.ID,
			Name:  user.Name,
			Email: user.Email,
		}
		
		// Check if client is still connected
		if err := stream.Send(resp); err != nil {
			return err
		}
		
		// Small delay for demonstration
		time.Sleep(10 * time.Millisecond)
	}
	
	return nil
}

// Bidirectional Streaming implementation
func (s *UserServiceServer) Chat(stream userv1.UserService_ChatServer) error {
	for {
		msg, err := stream.Recv()
		if err != nil {
			return err
		}
		
		// Process message
		response := &userv1.ChatMessage{
			UserId:    msg.UserId,
			Message:   fmt.Sprintf("Echo: %s", msg.Message),
			Timestamp: timestamppb.New(time.Now()),
		}
		
		// Send response
		if err := stream.Send(response); err != nil {
			return err
		}
	}
}

// STEP 4: Start gRPC Server with advanced configuration
func StartGRPCServer(addr string, store UserStore) error {
	// Server options
	opts := []grpc.ServerOption{
		// Keepalive enforcement
		grpc.KeepaliveEnforcementPolicy(keepalive.EnforcementPolicy{
			MinTime:             30 * time.Second,
			PermitWithoutStream: true,
		}),
		
		// Keepalive parameters
		grpc.KeepaliveParams(keepalive.ServerParameters{
			Time:    60 * time.Second,
			Timeout: 20 * time.Second,
		}),
		
		// Max message size (4MB)
		grpc.MaxRecvMsgSize(4 * 1024 * 1024),
		grpc.MaxSendMsgSize(4 * 1024 * 1024),
		
		// Connection timeout
		grpc.ConnectionTimeout(10 * time.Second),
		
		// Unary interceptor for logging/auth
		grpc.UnaryInterceptor(unaryInterceptor),
		
		// Stream interceptor
		grpc.StreamInterceptor(streamInterceptor),
		
		// Multiple interceptors (chain)
		grpc.ChainUnaryInterceptor(
			loggingUnaryInterceptor,
			authUnaryInterceptor,
			recoveryUnaryInterceptor,
		),
	}
	
	// Add TLS if needed
	if certFile != "" && keyFile != "" {
		creds, err := credentials.NewServerTLSFromFile(certFile, keyFile)
		if err != nil {
			return err
		}
		opts = append(opts, grpc.Creds(creds))
	}
	
	// Create server
	server := grpc.NewServer(opts...)
	
	// Register services
	userService := NewUserServiceServer(store)
	userv1.RegisterUserServiceServer(server, userService)
	
	// Register reflection for debugging
	reflection.Register(server)
	
	// Start listening
	lis, err := net.Listen("tcp", addr)
	if err != nil {
		return err
	}
	
	log.Printf("gRPC server listening on %s", addr)
	return server.Serve(lis)
}

// Interceptors
func unaryInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	start := time.Now()
	
	// Pre-processing
	log.Printf("Method: %s, Request: %v", info.FullMethod, req)
	
	// Call handler
	resp, err := handler(ctx, req)
	
	// Post-processing
	duration := time.Since(start)
	log.Printf("Method: %s, Duration: %v, Error: %v", info.FullMethod, duration, err)
	
	return resp, err
}

func loggingUnaryInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	log.Printf("gRPC method %s called", info.FullMethod)
	return handler(ctx, req)
}

func authUnaryInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (interface{}, error) {
	// Extract token from metadata
	md, ok := metadata.FromIncomingContext(ctx)
	if !ok {
		return nil, status.Error(codes.Unauthenticated, "missing metadata")
	}
	
	tokens := md.Get("authorization")
	if len(tokens) == 0 {
		return nil, status.Error(codes.Unauthenticated, "missing authorization token")
	}
	
	// Validate token
	if !validateToken(tokens[0]) {
		return nil, status.Error(codes.Unauthenticated, "invalid token")
	}
	
	return handler(ctx, req)
}

func recoveryUnaryInterceptor(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (resp interface{}, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = status.Errorf(codes.Internal, "panic recovered: %v", r)
			log.Printf("Panic recovered in %s: %v", info.FullMethod, r)
		}
	}()
	
	return handler(ctx, req)
}

func streamInterceptor(srv interface{}, ss grpc.ServerStream, info *grpc.StreamServerInfo, handler grpc.StreamHandler) error {
	log.Printf("Stream method %s started", info.FullMethod)
	err := handler(srv, ss)
	log.Printf("Stream method %s ended: %v", info.FullMethod, err)
	return err
}

// STEP 5: gRPC Client
type UserServiceClient struct {
	client userv1.UserServiceClient
	conn   *grpc.ClientConn
}

func NewUserServiceClient(addr string) (*UserServiceClient, error) {
	// Client options
	opts := []grpc.DialOption{
		grpc.WithInsecure(), // Use WithTransportCredentials for TLS
		grpc.WithDefaultCallOptions(
			grpc.MaxCallRecvMsgSize(4*1024*1024),
			grpc.MaxCallSendMsgSize(4*1024*1024),
		),
		grpc.WithUnaryInterceptor(clientUnaryInterceptor),
		grpc.WithStreamInterceptor(clientStreamInterceptor),
		grpc.WithTimeout(30 * time.Second),
	}
	
	// Dial server
	conn, err := grpc.Dial(addr, opts...)
	if err != nil {
		return nil, err
	}
	
	client := userv1.NewUserServiceClient(conn)
	return &UserServiceClient{client: client, conn: conn}, nil
}

func (c *UserServiceClient) GetUserWithTimeout(userID string, timeout time.Duration) (*userv1.UserResponse, error) {
	ctx, cancel := context.WithTimeout(context.Background(), timeout)
	defer cancel()
	
	// Add metadata
	md := metadata.Pairs(
		"authorization", "Bearer token123",
		"request-id", generateRequestID(),
	)
	ctx = metadata.NewOutgoingContext(ctx, md)
	
	// Make call with retry
	var resp *userv1.UserResponse
	var err error
	
	for i := 0; i < 3; i++ {
		resp, err = c.client.GetUser(ctx, &userv1.GetUserRequest{UserId: userID})
		if err == nil {
			break
		}
		
		// Check if error is retryable
		if !isRetryableError(err) {
			break
		}
		
		time.Sleep(time.Duration(i+1) * 100 * time.Millisecond)
	}
	
	return resp, err
}

func (c *UserServiceClient) ListUsersStream(filter string) ([]*userv1.UserResponse, error) {
	ctx := context.Background()
	stream, err := c.client.ListUsers(ctx, &userv1.ListUsersRequest{Filter: filter})
	if err != nil {
		return nil, err
	}
	
	var users []*userv1.UserResponse
	for {
		user, err := stream.Recv()
		if err != nil {
			if err == io.EOF {
				break
			}
			return nil, err
		}
		users = append(users, user)
	}
	
	return users, nil
}

func (c *UserServiceClient) Close() {
	c.conn.Close()
}

// ============================================================================
// 2. REST vs gRPC COMPARISONS - When to Use Which
// ============================================================================

type ProtocolComparison struct{}

func (pc *ProtocolComparison) CompareProtocols() {
	fmt.Println("=== REST vs gRPC Comparison ===")
	
	// Use REST when:
	// 1. Public APIs for external clients
	// 2. Browser-based clients
	// 3. Simple CRUD operations
	// 4. Need human-readable payloads
	// 5. Leveraging HTTP caching
	// 6. Existing REST infrastructure
	
	// Use gRPC when:
	// 1. Internal microservices communication
	// 2. Need high performance/low latency
	// 3. Streaming capabilities required
	// 4. Strongly-typed contracts
	// 5. Bi-directional communication
	// 6. Polyglot environments
}

// Hybrid Approach: gRPC with REST Gateway
func StartHybridServer(grpcAddr, restAddr string) error {
	// Start gRPC server
	grpcServer := grpc.NewServer()
	userv1.RegisterUserServiceServer(grpcServer, &UserServiceServer{})
	
	// Create gRPC-Gateway mux
	gwmux := runtime.NewServeMux(
		runtime.WithMarshalerOption(runtime.MIMEWildcard, &runtime.JSONPb{
			MarshalOptions: protojson.MarshalOptions{
				UseProtoNames:   true,
				EmitUnpopulated: true,
			},
		}),
	)
	
	// Register gRPC-Gateway endpoints
	ctx := context.Background()
	opts := []grpc.DialOption{grpc.WithInsecure()}
	err := userv1.RegisterUserServiceHandlerFromEndpoint(ctx, gwmux, grpcAddr, opts)
	if err != nil {
		return err
	}
	
	// Start REST proxy
	mux := http.NewServeMux()
	mux.Handle("/", gwmux)
	
	// Add Swagger/OpenAPI
	mux.Handle("/swagger/", http.StripPrefix("/swagger/", http.FileServer(http.Dir("./swagger"))))
	
	// Start servers
	go func() {
		log.Printf("REST gateway listening on %s", restAddr)
		http.ListenAndServe(restAddr, mux)
	}()
	
	log.Printf("gRPC server listening on %s", grpcAddr)
	lis, _ := net.Listen("tcp", grpcAddr)
	return grpcServer.Serve(lis)
}

// ============================================================================
// 3. SERVICE DISCOVERY - Dynamic Service Location
// ============================================================================

import (
	"sync"
	"time"

	"github.com/hashicorp/consul/api"
	"github.com/serialx/hashring"
)

// Pattern 1: Client-side discovery
type ServiceDiscoveryClient struct {
	consulClient *api.Client
	cache        map[string][]string
	cacheTTL     time.Duration
	lastUpdated  time.Time
	mu           sync.RWMutex
}

func NewServiceDiscoveryClient(consulAddr string) (*ServiceDiscoveryClient, error) {
	config := api.DefaultConfig()
	config.Address = consulAddr
	
	client, err := api.NewClient(config)
	if err != nil {
		return nil, err
	}
	
	return &ServiceDiscoveryClient{
		consulClient: client,
		cache:        make(map[string][]string),
		cacheTTL:     30 * time.Second,
	}, nil
}

func (sdc *ServiceDiscoveryClient) Discover(serviceName string) ([]string, error) {
	// Check cache first
	sdc.mu.RLock()
	if time.Since(sdc.lastUpdated) < sdc.cacheTTL {
		if endpoints, ok := sdc.cache[serviceName]; ok {
			sdc.mu.RUnlock()
			return endpoints, nil
		}
	}
	sdc.mu.RUnlock()
	
	// Query Consul
	services, _, err := sdc.consulClient.Health().Service(serviceName, "", true, nil)
	if err != nil {
		return nil, err
	}
	
	// Extract endpoints
	var endpoints []string
	for _, service := range services {
		addr := service.Service.Address
		if addr == "" {
			addr = service.Node.Address
		}
		endpoint := fmt.Sprintf("%s:%d", addr, service.Service.Port)
		endpoints = append(endpoints, endpoint)
	}
	
	// Update cache
	sdc.mu.Lock()
	sdc.cache[serviceName] = endpoints
	sdc.lastUpdated = time.Now()
	sdc.mu.Unlock()
	
	return endpoints, nil
}

// Pattern 2: Server-side discovery (Load Balancer)
type LoadBalancedDiscovery struct {
	services map[string]*hashring.HashRing
	mu       sync.RWMutex
}

func NewLoadBalancedDiscovery() *LoadBalancedDiscovery {
	return &LoadBalancedDiscovery{
		services: make(map[string]*hashring.HashRing),
	}
}

func (lbd *LoadBalancedDiscovery) RegisterService(serviceName string, endpoints []string) {
	lbd.mu.Lock()
	defer lbd.mu.Unlock()
	
	nodes := make([]string, len(endpoints))
	for i, endpoint := range endpoints {
		nodes[i] = endpoint
	}
	
	lbd.services[serviceName] = hashring.New(nodes)
}

func (lbd *LoadBalancedDiscovery) GetEndpoint(serviceName, key string) (string, error) {
	lbd.mu.RLock()
	defer lbd.mu.RUnlock()
	
	ring, ok := lbd.services[serviceName]
	if !ok {
		return "", fmt.Errorf("service %s not found", serviceName)
	}
	
	endpoint, ok := ring.GetNode(key)
	if !ok {
		return "", fmt.Errorf("no endpoints available for service %s", serviceName)
	}
	
	return endpoint, nil
}

// Pattern 3: DNS-based service discovery
type DNSDiscovery struct {
	resolver *net.Resolver
	cache    map[string][]string
	mu       sync.RWMutex
}

func NewDNSDiscovery() *DNSDiscovery {
	return &DNSDiscovery{
		resolver: &net.Resolver{
			PreferGo: true,
		},
		cache: make(map[string][]string),
	}
}

func (dd *DNSDiscovery) LookupService(serviceName string) ([]string, error) {
	// Use SRV records: _grpc._tcp.service.namespace.svc.cluster.local
	srvName := fmt.Sprintf("_grpc._tcp.%s.svc.cluster.local", serviceName)
	
	_, addrs, err := dd.resolver.LookupSRV("", "", srvName)
	if err != nil {
		return nil, err
	}
	
	var endpoints []string
	for _, addr := range addrs {
		endpoint := fmt.Sprintf("%s:%d", addr.Target, addr.Port)
		endpoints = append(endpoints, endpoint)
	}
	
	return endpoints, nil
}

// Service registration
func RegisterWithConsul(serviceName, address string, port int, healthCheck string) error {
	config := api.DefaultConfig()
	client, err := api.NewClient(config)
	if err != nil {
		return err
	}
	
	registration := &api.AgentServiceRegistration{
		ID:      fmt.Sprintf("%s-%s", serviceName, address),
		Name:    serviceName,
		Address: address,
		Port:    port,
		Check: &api.AgentServiceCheck{
			HTTP:     healthCheck,
			Interval: "10s",
			Timeout:  "5s",
		},
		Tags: []string{"grpc", "v1"},
	}
	
	return client.Agent().ServiceRegister(registration)
}

// ============================================================================
// 4. CIRCUIT BREAKERS AND RESILIENCE PATTERNS
// ============================================================================

import (
	"github.com/afex/hystrix-go/hystrix"
	"github.com/sony/gobreaker"
)

// Pattern 1: Hystrix-style circuit breaker
type ResilientClient struct {
	circuitName string
	timeout     time.Duration
	maxRequests int
}

func NewResilientClient(name string) *ResilientClient {
	// Configure circuit breaker
	hystrix.ConfigureCommand(name, hystrix.CommandConfig{
		Timeout:                1000,               // ms
		MaxConcurrentRequests:  100,                // max concurrent requests
		RequestVolumeThreshold: 20,                 // min requests before tripping
		SleepWindow:           5000,               // ms to wait after tripping
		ErrorPercentThreshold: 50,                 // % errors to trip
	})
	
	return &ResilientClient{
		circuitName: name,
		timeout:     1 * time.Second,
		maxRequests: 100,
	}
}

func (rc *ResilientClient) Execute(fn func() error) error {
	// Execute with circuit breaker
	errChan := hystrix.Go(rc.circuitName, func() error {
		return fn()
	}, func(err error) error {
		// Fallback function
		log.Printf("Circuit open, using fallback: %v", err)
		return rc.fallback()
	})
	
	return <-errChan
}

func (rc *ResilientClient) fallback() error {
	// Implement fallback logic
	return fmt.Errorf("service unavailable, using fallback")
}

// Pattern 2: GoBreaker with more granular control
type CircuitBreakerManager struct {
	breakers map[string]*gobreaker.CircuitBreaker
	mu       sync.RWMutex
}

func NewCircuitBreakerManager() *CircuitBreakerManager {
	return &CircuitBreakerManager{
		breakers: make(map[string]*gobreaker.CircuitBreaker),
	}
}

func (cbm *CircuitBreakerManager) GetOrCreate(name string) *gobreaker.CircuitBreaker {
	cbm.mu.RLock()
	if cb, ok := cbm.breakers[name]; ok {
		cbm.mu.RUnlock()
		return cb
	}
	cbm.mu.RUnlock()
	
	cbm.mu.Lock()
	defer cbm.mu.Unlock()
	
	// Double-check
	if cb, ok := cbm.breakers[name]; ok {
		return cb
	}
	
	cb := gobreaker.NewCircuitBreaker(gobreaker.Settings{
		Name:        name,
		MaxRequests: 5, // Half-open state max requests
		Interval:    30 * time.Second,
		Timeout:     60 * time.Second,
		ReadyToTrip: func(counts gobreaker.Counts) bool {
			// Custom trip logic
			return counts.ConsecutiveFailures > 5 ||
				(counts.TotalFailures > 10 && 
					float64(counts.TotalFailures)/float64(counts.Requests) > 0.6)
		},
		OnStateChange: func(name string, from, to gobreaker.State) {
			log.Printf("Circuit %s: %s -> %s", name, from, to)
		},
	})
	
	cbm.breakers[name] = cb
	return cb
}

// Pattern 3: Bulkhead pattern - resource isolation
type Bulkhead struct {
	semaphore chan struct{}
	timeout   time.Duration
}

func NewBulkhead(maxConcurrent int, timeout time.Duration) *Bulkhead {
	return &Bulkhead{
		semaphore: make(chan struct{}, maxConcurrent),
		timeout:   timeout,
	}
}

func (b *Bulkhead) Execute(fn func() (interface{}, error)) (interface{}, error) {
	select {
	case b.semaphore <- struct{}{}:
		defer func() { <-b.semaphore }()
		return fn()
	case <-time.After(b.timeout):
		return nil, fmt.Errorf("bulkhead timeout")
	}
}

// Pattern 4: Retry with exponential backoff and circuit breaker
type ResilientCall struct {
	circuitBreaker *gobreaker.CircuitBreaker
	maxRetries     int
	baseDelay      time.Duration
	maxDelay       time.Duration
}

func NewResilientCall(circuitName string) *ResilientCall {
	cbm := NewCircuitBreakerManager()
	
	return &ResilientCall{
		circuitBreaker: cbm.GetOrCreate(circuitName),
		maxRetries:     3,
		baseDelay:      100 * time.Millisecond,
		maxDelay:       5 * time.Second,
	}
}

func (rc *ResilientCall) Execute(fn func() (interface{}, error)) (interface{}, error) {
	// Use circuit breaker
	return rc.circuitBreaker.Execute(func() (interface{}, error) {
		var lastErr error
		
		for i := 0; i < rc.maxRetries; i++ {
			result, err := fn()
			if err == nil {
				return result, nil
			}
			
			lastErr = err
			
			// Check if error is retryable
			if !isRetryableError(err) {
				break
			}
			
			// Calculate delay with exponential backoff and jitter
			delay := rc.calculateDelay(i)
			time.Sleep(delay)
		}
		
		return nil, lastErr
	})
}

func (rc *ResilientCall) calculateDelay(retry int) time.Duration {
	delay := rc.baseDelay * time.Duration(1<<uint(retry)) // Exponential
	if delay > rc.maxDelay {
		delay = rc.maxDelay
	}
	
	// Add jitter (±20%)
	jitter := time.Duration(float64(delay) * 0.2 * (rand.Float64()*2 - 1))
	return delay + jitter
}

// Pattern 5: Timeout and cancellation propagation
type TimeoutManager struct {
	defaultTimeout time.Duration
}

func NewTimeoutManager(defaultTimeout time.Duration) *TimeoutManager {
	return &TimeoutManager{defaultTimeout: defaultTimeout}
}

func (tm *TimeoutManager) WithTimeout(ctx context.Context, fn func(context.Context) error) error {
	ctx, cancel := context.WithTimeout(ctx, tm.defaultTimeout)
	defer cancel()
	
	// Create done channel
	done := make(chan error, 1)
	
	go func() {
		done <- fn(ctx)
	}()
	
	select {
	case err := <-done:
		return err
	case <-ctx.Done():
		return ctx.Err()
	}
}

// ============================================================================
// 5. MESSAGE QUEUES (RabbitMQ, Kafka)
// ============================================================================

import (
	"github.com/streadway/amqp"
	"github.com/segmentio/kafka-go"
)

// RabbitMQ Implementation
type RabbitMQClient struct {
	conn    *amqp.Connection
	channel *amqp.Channel
	queues  map[string]amqp.Queue
	mu      sync.RWMutex
}

func NewRabbitMQClient(url string) (*RabbitMQClient, error) {
	conn, err := amqp.Dial(url)
	if err != nil {
		return nil, err
	}
	
	channel, err := conn.Channel()
	if err != nil {
		conn.Close()
		return nil, err
	}
	
	return &RabbitMQClient{
		conn:    conn,
		channel: channel,
		queues:  make(map[string]amqp.Queue),
	}, nil
}

func (rmq *RabbitMQClient) DeclareQueue(queueName string, durable, autoDelete bool) error {
	queue, err := rmq.channel.QueueDeclare(
		queueName,   // name
		durable,     // durable
		autoDelete,  // autoDelete
		false,       // exclusive
		false,       // noWait
		nil,         // arguments
	)
	if err != nil {
		return err
	}
	
	rmq.mu.Lock()
	rmq.queues[queueName] = queue
	rmq.mu.Unlock()
	
	return nil
}

func (rmq *RabbitMQClient) Publish(queueName string, body []byte, headers map[string]interface{}) error {
	// Ensure queue exists
	rmq.mu.RLock()
	_, exists := rmq.queues[queueName]
	rmq.mu.RUnlock()
	
	if !exists {
		if err := rmq.DeclareQueue(queueName, true, false); err != nil {
			return err
		}
	}
	
	// Publish message
	return rmq.channel.Publish(
		"",        // exchange
		queueName, // routing key
		false,     // mandatory
		false,     // immediate
		amqp.Publishing{
			ContentType:  "application/json",
			Body:         body,
			Headers:      amqp.Table(headers),
			DeliveryMode: amqp.Persistent, // Persistent message
			Timestamp:    time.Now(),
			MessageId:    generateMessageID(),
		},
	)
}

func (rmq *RabbitMQClient) Consume(queueName string, handler func([]byte) error) error {
	// Start consuming
	msgs, err := rmq.channel.Consume(
		queueName, // queue
		"",        // consumer
		false,     // autoAck (manual ack for reliability)
		false,     // exclusive
		false,     // noLocal
		false,     // noWait
		nil,       // args
	)
	if err != nil {
		return err
	}
	
	// Process messages
	go func() {
		for msg := range msgs {
			// Process message
			if err := handler(msg.Body); err != nil {
				// Negative acknowledgement - requeue
				msg.Nack(false, true)
			} else {
				// Positive acknowledgement
				msg.Ack(false)
			}
		}
	}()
	
	return nil
}

// Dead Letter Exchange (DLX) for error handling
func (rmq *RabbitMQClient) DeclareQueueWithDLX(queueName, dlxName string) error {
	args := amqp.Table{
		"x-dead-letter-exchange": dlxName,
		"x-message-ttl":          60000, // 60 seconds
	}
	
	queue, err := rmq.channel.QueueDeclare(
		queueName,
		true,  // durable
		false, // autoDelete
		false, // exclusive
		false, // noWait
		args,
	)
	if err != nil {
		return err
	}
	
	rmq.mu.Lock()
	rmq.queues[queueName] = queue
	rmq.mu.Unlock()
	
	return nil
}

// Kafka Implementation
type KafkaProducer struct {
	writer *kafka.Writer
}

func NewKafkaProducer(brokers []string, topic string) *KafkaProducer {
	writer := &kafka.Writer{
		Addr:     kafka.TCP(brokers...),
		Topic:    topic,
		Balancer: &kafka.LeastBytes{}, // Partition balancing strategy
		Async:    true,                 // Async writes for higher throughput
		Completion: func(messages []kafka.Message, err error) {
			// Callback for async writes
			if err != nil {
				log.Printf("Failed to write messages: %v", err)
			}
		},
	}
	
	return &KafkaProducer{writer: writer}
}

func (kp *KafkaProducer) Produce(key, value []byte, headers map[string]string) error {
	// Convert headers
	kafkaHeaders := make([]kafka.Header, 0, len(headers))
	for k, v := range headers {
		kafkaHeaders = append(kafkaHeaders, kafka.Header{
			Key:   k,
			Value: []byte(v),
		})
	}
	
	// Write message
	return kp.writer.WriteMessages(context.Background(),
		kafka.Message{
			Key:     key,
			Value:   value,
			Headers: kafkaHeaders,
			Time:    time.Now(),
		},
	)
}

func (kp *KafkaProducer) Close() error {
	return kp.writer.Close()
}

type KafkaConsumer struct {
	reader *kafka.Reader
}

func NewKafkaConsumer(brokers []string, topic, groupID string) *KafkaConsumer {
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  brokers,
		Topic:    topic,
		GroupID:  groupID,
		MinBytes: 10e3, // 10KB
		MaxBytes: 10e6, // 10MB
		MaxWait:  1 * time.Second,
	})
	
	return &KafkaConsumer{reader: reader}
}

func (kc *KafkaConsumer) Consume(handler func(key, value []byte) error) error {
	for {
		ctx := context.Background()
		msg, err := kc.reader.FetchMessage(ctx)
		if err != nil {
			return err
		}
		
		// Process message
		if err := handler(msg.Key, msg.Value); err != nil {
			return err
		}
		
		// Commit offset
		if err := kc.reader.CommitMessages(ctx, msg); err != nil {
			return err
		}
	}
}

// Message Queue Patterns
type MessageQueuePatterns struct{}

func (mqp *MessageQueuePatterns) DemonstratePatterns() {
	fmt.Println("=== Message Queue Patterns ===")
	
	// 1. Point-to-Point (Queue)
	// - Single consumer processes each message
	// - RabbitMQ queues, Kafka with single consumer group
	
	// 2. Publish-Subscribe (Pub/Sub)
	// - Multiple consumers receive same message
	// - RabbitMQ exchanges, Kafka topics
	
	// 3. Request-Reply (RPC over MQ)
	// - Send request, wait for response on reply queue
	// - Correlation ID pattern
	
	// 4. Dead Letter Queues (DLQ)
	// - Failed messages go to DLQ for inspection
	
	// 5. Competing Consumers
	// - Multiple consumers compete for messages
	// - Load balancing across consumers
	
	// 6. Message Priority
	// - Higher priority messages processed first
	
	// 7. Message TTL
	// - Messages expire after time limit
}

// ============================================================================
// 6. RPC FRAMEWORKS (Twirp, gRPC-Gateway)
// ============================================================================

// Twirp Implementation
/*
// user.proto for Twirp
syntax = "proto3";

package user;

option go_package = "./user";

service UserService {
  rpc GetUser(GetUserRequest) returns (UserResponse);
  rpc CreateUser(CreateUserRequest) returns (UserResponse);
}

message GetUserRequest {
  string id = 1;
}

message CreateUserRequest {
  string name = 1;
  string email = 2;
}

message UserResponse {
  string id = 1;
  string name = 2;
  string email = 3;
}
*/

type TwirpUserService struct{}

func (tus *TwirpUserService) GetUser(ctx context.Context, req *user.GetUserRequest) (*user.UserResponse, error) {
	// Twirp automatically handles JSON/Protobuf encoding
	return &user.UserResponse{
		Id:    req.Id,
		Name:  "John Doe",
		Email: "john@example.com",
	}, nil
}

func (tus *TwirpUserService) CreateUser(ctx context.Context, req *user.CreateUserRequest) (*user.UserResponse, error) {
	// Generate ID
	id := generateID()
	
	return &user.UserResponse{
		Id:    id,
		Name:  req.Name,
		Email: req.Email,
	}, nil
}

func StartTwirpServer() {
	// Create Twirp handler
	handler := user.NewUserServiceServer(&TwirpUserService{})
	
	// Serve both Protobuf and JSON
	mux := http.NewServeMux()
	mux.Handle(handler.PathPrefix(), handler)
	
	// Add CORS middleware
	corsHandler := cors.Default().Handler(mux)
	
	log.Println("Twirp server listening on :8080")
	http.ListenAndServe(":8080", corsHandler)
}

// gRPC-Gateway Implementation
/*
// Already shown in section 2
// Generates RESTful HTTP API from gRPC service definitions
*/

// Comparison: Twirp vs gRPC
type RPCComparison struct{}

func (rc *RPCComparison) Compare() {
	fmt.Println("=== Twirp vs gRPC Comparison ===")
	
	fmt.Println("Twirp Advantages:")
	fmt.Println("- Simple, no streaming support needed")
	fmt.Println("- Automatic JSON/Protobuf support")
	fmt.Println("- Easy HTTP/1.1 compatibility")
	fmt.Println("- Smaller dependency footprint")
	fmt.Println("- Generated clients in multiple languages")
	
	fmt.Println("\ngRPC Advantages:")
	fmt.Println("- High performance (HTTP/2, binary protobuf)")
	fmt.Println("- Built-in streaming (unary, server, client, bidirectional)")
	fmt.Println"- Advanced features (compression, interceptors, load balancing)")
	fmt.Println("- Mature ecosystem")
	fmt.Println("- Production-ready at scale")
}

// Custom RPC Framework Example
type CustomRPC struct {
	handlers map[string]func([]byte) ([]byte, error)
	mu       sync.RWMutex
}

func NewCustomRPC() *CustomRPC {
	return &CustomRPC{
		handlers: make(map[string]func([]byte) ([]byte, error)),
	}
}

func (crpc *CustomRPC) Register(method string, handler func([]byte) ([]byte, error)) {
	crpc.mu.Lock()
	defer crpc.mu.Unlock()
	crpc.handlers[method] = handler
}

func (crpc *CustomRPC) HandleRequest(method string, data []byte) ([]byte, error) {
	crpc.mu.RLock()
	handler, exists := crpc.handlers[method]
	crpc.mu.RUnlock()
	
	if !exists {
		return nil, fmt.Errorf("method %s not found", method)
	}
	
	return handler(data)
}

// ============================================================================
// PRACTICAL INTEGRATION - Complete Microservice Architecture
// ============================================================================

type MicroserviceArchitecture struct {
	// Service registry
	serviceDiscovery *ServiceDiscoveryClient
	
	// Communication
	grpcClients   map[string]*grpc.ClientConn
	messageQueues map[string]MessageQueue
	
	// Resilience
	circuitBreakers *CircuitBreakerManager
	retryStrategies map[string]*ResilientCall
	
	// Observability
	logger  *zap.Logger
	metrics *prometheus.Registry
	tracer  trace.Tracer
	
	mu sync.RWMutex
}

func NewMicroserviceArchitecture() (*MicroserviceArchitecture, error) {
	// Initialize service discovery
	sd, err := NewServiceDiscoveryClient("consul:8500")
	if err != nil {
		return nil, err
	}
	
	// Initialize circuit breakers
	cb := NewCircuitBreakerManager()
	
	// Initialize observability
	logger, _ := zap.NewProduction()
	
	return &MicroserviceArchitecture{
		serviceDiscovery: sd,
		grpcClients:      make(map[string]*grpc.ClientConn),
		messageQueues:    make(map[string]MessageQueue),
		circuitBreakers:  cb,
		retryStrategies:  make(map[string]*ResilientCall),
		logger:           logger,
	}, nil
}

func (ma *MicroserviceArchitecture) CallService(serviceName, method string, request interface{}) (interface{}, error) {
	// 1. Discover service endpoints
	endpoints, err := ma.serviceDiscovery.Discover(serviceName)
	if err != nil {
		return nil, fmt.Errorf("service discovery failed: %w", err)
	}
	
	if len(endpoints) == 0 {
		return nil, fmt.Errorf("no endpoints available for %s", serviceName)
	}
	
	// 2. Get or create circuit breaker
	cb := ma.circuitBreakers.GetOrCreate(serviceName)
	
	// 3. Execute with circuit breaker
	return cb.Execute(func() (interface{}, error) {
		// 4. Load balancing - select endpoint
		endpoint := ma.selectEndpoint(endpoints, request)
		
		// 5. Get or create gRPC client
		client, err := ma.getGRPCClient(serviceName, endpoint)
		if err != nil {
			return nil, err
		}
		
		// 6. Make the call with timeout
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		
		// 7. Add tracing
		ctx = ma.injectTraceContext(ctx)
		
		// 8. Make actual RPC call (implementation depends on service)
		return ma.makeRPC(ctx, client, method, request)
	})
}

func (ma *MicroserviceArchitecture) selectEndpoint(endpoints []string, request interface{}) string {
	// Simple round-robin for demonstration
	// In production: use consistent hashing, least connections, etc.
	ma.mu.Lock()
	defer ma.mu.Unlock()
	
	// Round-robin selection
	if ma.lastSelected == nil {
		ma.lastSelected = make(map[string]int)
	}
	
	idx := ma.lastSelected[serviceName] % len(endpoints)
	ma.lastSelected[serviceName] = (idx + 1) % len(endpoints)
	
	return endpoints[idx]
}

func (ma *MicroserviceArchitecture) getGRPCClient(serviceName, endpoint string) (*grpc.ClientConn, error) {
	ma.mu.RLock()
	if conn, ok := ma.grpcClients[endpoint]; ok {
		ma.mu.RUnlock()
		return conn, nil
	}
	ma.mu.RUnlock()
	
	ma.mu.Lock()
	defer ma.mu.Unlock()
	
	// Double-check
	if conn, ok := ma.grpcClients[endpoint]; ok {
		return conn, nil
	}
	
	// Create new connection
	conn, err := grpc.Dial(endpoint,
		grpc.WithInsecure(),
		grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy":"round_robin"}`),
		grpc.WithUnaryInterceptor(ma.clientInterceptor),
	)
	if err != nil {
		return nil, err
	}
	
	ma.grpcClients[endpoint] = conn
	return conn, nil
}

func (ma *MicroserviceArchitecture) clientInterceptor(
	ctx context.Context,
	method string,
	req, reply interface{},
	cc *grpc.ClientConn,
	invoker grpc.UnaryInvoker,
	opts ...grpc.CallOption,
) error {
	// Start timer
	start := time.Now()
	
	// Add metadata
	md, _ := metadata.FromOutgoingContext(ctx)
	if md == nil {
		md = metadata.New(nil)
	}
	md.Set("request-id", generateRequestID())
	ctx = metadata.NewOutgoingContext(ctx, md)
	
	// Make the call
	err := invoker(ctx, method, req, reply, cc, opts...)
	
	// Record metrics
	duration := time.Since(start)
	status := "success"
	if err != nil {
		status = "error"
	}
	
	// Record metric
	ma.recordRPCMetric(method, status, duration)
	
	return err
}

// ============================================================================
// MAIN DEMONSTRATION
// ============================================================================

func main() {
	fmt.Println("=== Advanced Microservices & Distributed Systems ===")
	
	// 1. gRPC Server
	fmt.Println("\n1. Starting gRPC server...")
	// StartGRPCServer(":50051", userStore)
	
	// 2. Service Discovery
	fmt.Println("\n2. Initializing service discovery...")
	sd, _ := NewServiceDiscoveryClient("localhost:8500")
	endpoints, _ := sd.Discover("user-service")
	fmt.Printf("Discovered endpoints: %v\n", endpoints)
	
	// 3. Circuit Breaker
	fmt.Println("\n3. Setting up circuit breakers...")
	cb := NewCircuitBreakerManager()
	userServiceCB := cb.GetOrCreate("user-service")
	
	// Test circuit breaker
	result, err := userServiceCB.Execute(func() (interface{}, error) {
		// Simulate service call
		return "success", nil
	})
	fmt.Printf("Circuit breaker result: %v, error: %v\n", result, err)
	
	// 4. Message Queue
	fmt.Println("\n4. Setting up RabbitMQ...")
	rmq, _ := NewRabbitMQClient("amqp://guest:guest@localhost:5672/")
	rmq.DeclareQueue("user.events", true, false)
	rmq.Publish("user.events", []byte(`{"event":"user.created"}`), nil)
	
	// 5. RPC Framework Comparison
	fmt.Println("\n5. RPC Framework Comparison:")
	comparison := &RPCComparison{}
	comparison.Compare()
	
	// 6. Complete Architecture
	fmt.Println("\n6. Complete Microservice Architecture:")
	arch, _ := NewMicroserviceArchitecture()
	
	// Simulate service call
	go func() {
		result, err := arch.CallService("user-service", "GetUser", &userv1.GetUserRequest{UserId: "123"})
		fmt.Printf("Service call result: %v, error: %v\n", result, err)
	}()
	
	fmt.Println("\n=== Key Takeaways ===")
	fmt.Println("1. gRPC with Protobuf is ideal for internal service communication")
	fmt.Println("2. Use REST/gRPC-Gateway for external/public APIs")
	fmt.Println("3. Service discovery is critical for dynamic environments")
	fmt.Println("4. Circuit breakers prevent cascading failures")
	fmt.Println("5. Message queues enable async communication and decoupling")
	fmt.Println("6. Choose RPC framework based on requirements (Twirp for simplicity, gRPC for features)")
	fmt.Println("7. Always implement retries with exponential backoff")
	fmt.Println("8. Use bulkheads to isolate failures")
	fmt.Println("9. Monitor circuit breaker states")
	fmt.Println("10. Test failure scenarios regularly")
	
	// Keep server running
	select {}
}

// Helper functions
func validateToken(token string) bool {
	return token == "valid-token"
}

func generateRequestID() string {
	return fmt.Sprintf("req_%d", time.Now().UnixNano())
}

func generateMessageID() string {
	return fmt.Sprintf("msg_%d", time.Now().UnixNano())
}

func generateID() string {
	return fmt.Sprintf("id_%d", time.Now().UnixNano())
}

func isRetryableError(err error) bool {
	// Check error type for retryability
	if err == nil {
		return false
	}
	
	// Network errors are retryable
	if _, ok := err.(interface{ Timeout() bool }); ok {
		return true
	}
	
	// gRPC status codes that are retryable
	if st, ok := status.FromError(err); ok {
		switch st.Code() {
		case codes.DeadlineExceeded,
			codes.ResourceExhausted,
			codes.Unavailable,
			codes.Internal,
			codes.DataLoss:
			return true
		default:
			return false
		}
	}
	
	return false
}

func clientUnaryInterceptor(ctx context.Context, method string, req, reply interface{}, cc *grpc.ClientConn, invoker grpc.UnaryInvoker, opts ...grpc.CallOption) error {
	// Add logging, metrics, tracing
	start := time.Now()
	err := invoker(ctx, method, req, reply, cc, opts...)
	duration := time.Since(start)
	
	log.Printf("gRPC call %s took %v, error: %v", method, duration, err)
	return err
}

func clientStreamInterceptor(ctx context.Context, desc *grpc.StreamDesc, cc *grpc.ClientConn, method string, streamer grpc.Streamer, opts ...grpc.CallOption) (grpc.ClientStream, error) {
	log.Printf("Starting stream: %s", method)
	return streamer(ctx, desc, cc, method, opts...)
}

type UserStore interface {
	GetUser(id string) (*User, error)
	ListUsers(filter string, limit int) ([]*User, error)
}

type User struct {
	ID        string
	Name      string
	Email     string
	Status    int
	CreatedAt time.Time
	Metadata  map[string]string
}

// Mock implementations
var (
	certFile = ""
	keyFile  = ""
)