/*
GO CONCEPTS: BUILD, DEPLOY & OPERATE
This comprehensive example demonstrates key concepts from junior to senior level.

CROSS-COMPILATION & STATIC BINARIES:
Go can compile for different OS/architecture combinations and create static binaries.
*/

package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

// To cross-compile, use GOOS and GOARCH environment variables:
//   GOOS=linux GOARCH=amd64 go build -o app-linux-amd64 .
//   GOOS=windows GOARCH=amd64 go build -o app-windows-amd64.exe .
//   GOOS=darwin GOARCH=arm64 go build -o app-macos-arm64 .
//
// Static binaries (no external dependencies):
//   CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' -o static-app .

// Service represents a long-running service with graceful shutdown
type Service struct {
	server   *http.Server
	wg       sync.WaitGroup
	shutdown chan struct{}
}

func main() {
	// Create service with health check endpoint
	svc := &Service{
		shutdown: make(chan struct{}),
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/", svc.handler)
	mux.HandleFunc("/health", svc.healthCheck)
	mux.HandleFunc("/ready", svc.readyCheck)

	svc.server = &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}

	// Start graceful shutdown listener
	go svc.listenForShutdown()

	// Start the server
	log.Println("Starting server on :8080")
	if err := svc.server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("Server error: %v", err)
	}

	// Wait for all goroutines to finish
	svc.wg.Wait()
	log.Println("Service shutdown complete")
}

func (s *Service) handler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello from Go service!\n")
}

// HEALTH CHECKS: Essential for containerized applications
// Liveness probe - is the application running?
func (s *Service) healthCheck(w http.ResponseWriter, r *http.Request) {
	// Check application health (database connections, external dependencies)
	select {
	case <-s.shutdown:
		w.WriteHeader(http.StatusServiceUnavailable)
		fmt.Fprintf(w, "SHUTTING_DOWN")
	default:
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "HEALTHY")
	}
}

// Readiness probe - is the application ready to receive traffic?
func (s *Service) readyCheck(w http.ResponseWriter, r *http.Request) {
	// Simulate startup delay
	if time.Since(startTime) < 5*time.Second {
		w.WriteHeader(http.StatusServiceUnavailable)
		fmt.Fprintf(w, "NOT_READY")
		return
	}

	// Check if all dependencies are available
	if !checkDependencies() {
		w.WriteHeader(http.StatusServiceUnavailable)
		fmt.Fprintf(w, "DEPENDENCIES_UNAVAILABLE")
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "READY")
}

func checkDependencies() bool {
	// In real app, check DB, cache, external services
	return true
}

var startTime = time.Now()

// GRACEFUL SHUTDOWN: Handle SIGTERM/SIGINT signals
func (s *Service) listenForShutdown() {
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	<-sigChan
	log.Println("Shutdown signal received")

	// Close shutdown channel to signal to health checks
	close(s.shutdown)

	// Create shutdown context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	// Stop accepting new connections
	if err := s.server.Shutdown(ctx); err != nil {
		log.Printf("Server shutdown error: %v", err)
	}

	// Wait for background tasks to complete
	s.wg.Wait()
	log.Println("Background tasks completed")
}

// Background worker with graceful shutdown support
func (s *Service) startWorker(id int) {
	s.wg.Add(1)
	go func() {
		defer s.wg.Done()

		ticker := time.NewTicker(10 * time.Second)
		defer ticker.Stop()

		for {
			select {
			case <-ticker.C:
				log.Printf("Worker %d: Processing...", id)
				// Do work
			case <-s.shutdown:
				log.Printf("Worker %d: Shutting down...", id)
				// Cleanup resources
				time.Sleep(2 * time.Second) // Simulate cleanup
				log.Printf("Worker %d: Shutdown complete", id)
				return
			}
		}
	}()
}

/*
DOCKERIZING GO APPS - Dockerfile example:

# Multi-stage build for smaller image size
# Stage 1: Build
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Download dependencies (cached layer)
COPY go.mod go.sum ./
RUN go mod download

# Copy source and build
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -ldflags '-extldflags "-static"' -o app .

# Stage 2: Runtime
FROM scratch

# Add CA certificates for HTTPS (if needed)
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/

# Copy static binary from builder
COPY --from=builder /app/app /app

# Add health check (essential for containers)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD ["/app", "health"] || wget -q --spider http://localhost:8080/health || exit 1

EXPOSE 8080

# Non-root user for security
USER 1000:1000

ENTRYPOINT ["/app"]

Multi-stage builds benefits:
1. Final image is much smaller (scratch base = ~0MB)
2. No build tools or source code in production image
3. Better security (fewer packages, non-root user)

CI/CD PIPELINE EXAMPLE (.github/workflows/go.yml):

name: Go CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Set up Go
      uses: actions/setup-go@v4
      with:
        go-version: '1.21'

    - name: Run tests
      run: go test -v -race ./...

    - name: Run security scan
      run: go vet ./...

  build:
    needs: test
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [linux, windows, darwin]
        arch: [amd64, arm64]

    steps:
    - uses: actions/checkout@v4

    - name: Build for ${{ matrix.os }}/${{ matrix.arch }}
      run: |
        GOOS=${{ matrix.os }} GOARCH=${{ matrix.arch }} CGO_ENABLED=0 \
        go build -ldflags="-w -s" -o app-${{ matrix.os }}-${{ matrix.arch }} .

  docker:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to DockerHub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: |
          user/app:latest
          user/app:${{ github.sha }}
        platforms: linux/amd64,linux/arm64
        cache-from: type=gha
        cache-to: type=gha,mode=max

OPERATIONAL CONSIDERATIONS:

1. Metrics and Observability:
   - Use Prometheus metrics: github.com/prometheus/client_golang
   - Structured logging with context
   - Distributed tracing with OpenTelemetry

2. Configuration:
   - 12-factor app: config via environment variables
   - Use viper or envconfig for config management

3. Deployment:
   - Kubernetes deployments with readiness/liveness probes
   - Horizontal Pod Autoscaler based on metrics
   - Rolling updates with proper health checks

4. Monitoring:
   - Application metrics (request rate, latency, errors)
   - Business metrics
   - Infrastructure metrics

5. Production Practices:
   - Always set GOMAXPROCS (automatically done in Go 1.21+)
   - Use pprof for profiling: import _ "net/http/pprof"
   - Implement circuit breakers for external calls
   - Use connection pooling for databases
*/

// Example of structured logging with context
type StructuredLogger struct {
	*log.Logger
}

func (l *StructuredLogger) LogRequest(r *http.Request, status int, duration time.Duration) {
	l.Printf("method=%s path=%s status=%d duration=%v ip=%s user_agent=%s",
		r.Method, r.URL.Path, status, duration,
		r.RemoteAddr, r.UserAgent())
}

// Example of configuration via environment
type Config struct {
	Port        int    `env:"PORT" default:"8080"`
	DatabaseURL string `env:"DATABASE_URL" required:"true"`
	Debug       bool   `env:"DEBUG" default:"false"`
}

// Example of metrics collection
func instrumentHandler(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()

		// Wrap response writer to capture status code
		rw := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

		next.ServeHTTP(rw, r)

		duration := time.Since(start)

		// In production, send to metrics system (Prometheus, etc.)
		log.Printf("request_completed method=%s path=%s status=%d duration_ms=%d",
			r.Method, r.URL.Path, rw.statusCode, duration.Milliseconds())
	})
}

type responseWriter struct {
	http.ResponseWriter
	statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.statusCode = code
	rw.ResponseWriter.WriteHeader(code)
}

// Run with: go run main.go
// Build static binary: CGO_ENABLED=0 go build -ldflags="-w -s" -o app .
// Docker build: docker build -t go-app .
// Docker run: docker run -p 8080:8080 -e PORT=8080 go-app
