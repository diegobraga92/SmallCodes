/*
GO ADVANCED CONCURRENCY COMPREHENSIVE GUIDE
This file demonstrates advanced Go concurrency concepts with practical examples.
Run with race detection: go test -race ./...
*/

package advanced_concurrency

import (
	"context"
	"fmt"
	"log"
	"sync"
	"sync/atomic"
	"testing"
	"time"
)

// ============================================================================
// 1. CONTEXT PROPAGATION
// ============================================================================

// Context carries deadlines, cancellation signals, and request-scoped values

func workerWithContext(ctx context.Context, id int, wg *sync.WaitGroup) {
	defer wg.Done()

	log.Printf("Worker %d starting", id)

	// Simulate work
	select {
	case <-time.After(time.Duration(id) * time.Second):
		log.Printf("Worker %d completed work", id)
	case <-ctx.Done():
		log.Printf("Worker %d cancelled: %v", id, ctx.Err())
		return
	}
}

func TestContextPropagation(t *testing.T) {
	// Create a context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	var wg sync.WaitGroup

	// Start 5 workers
	for i := 1; i <= 5; i++ {
		wg.Add(1)
		go workerWithContext(ctx, i, &wg)
	}

	// Wait for all workers or timeout
	wg.Wait()
}

// Context with values for request-scoped data
type contextKey string

const userIDKey contextKey = "userID"
const requestIDKey contextKey = "requestID"

func processRequest(ctx context.Context) {
	// Retrieve values from context
	userID, ok := ctx.Value(userIDKey).(string)
	if !ok {
		log.Println("No user ID in context")
		return
	}

	requestID, ok := ctx.Value(requestIDKey).(string)
	if !ok {
		log.Println("No request ID in context")
		return
	}

	log.Printf("Processing request %s for user %s", requestID, userID)

	// Pass context to downstream functions
	processUserData(ctx, userID)
}

func processUserData(ctx context.Context, userID string) {
	// Context is propagated down the call chain
	if deadline, ok := ctx.Deadline(); ok {
		log.Printf("Must complete by: %v", deadline)
	}

	// Check if context is still valid
	select {
	case <-ctx.Done():
		log.Printf("Context cancelled: %v", ctx.Err())
		return
	default:
		// Continue processing
	}
}

// ============================================================================
// 2. CANCELLATION & TIMEOUTS
// ============================================================================

func TestCancellationPatterns(t *testing.T) {
	// 1. WithCancel - manual cancellation
	ctx1, cancel1 := context.WithCancel(context.Background())
	go func() {
		time.Sleep(100 * time.Millisecond)
		cancel1() // Cancel the context
	}()

	select {
	case <-time.After(time.Second):
		t.Error("Should have been cancelled")
	case <-ctx1.Done():
		log.Println("Context 1 cancelled as expected")
	}

	// 2. WithTimeout - automatic cancellation after duration
	ctx2, cancel2 := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel2()

	select {
	case <-time.After(time.Second):
		t.Error("Should have timed out")
	case <-ctx2.Done():
		log.Println("Context 2 timed out as expected")
	}

	// 3. WithDeadline - cancel at specific time
	deadline := time.Now().Add(100 * time.Millisecond)
	ctx3, cancel3 := context.WithDeadline(context.Background(), deadline)
	defer cancel3()

	select {
	case <-time.After(time.Second):
		t.Error("Should have reached deadline")
	case <-ctx3.Done():
		log.Println("Context 3 reached deadline")
	}

	// 4. Nested contexts - child inherits parent's deadline/cancellation
	parentCtx, parentCancel := context.WithTimeout(context.Background(), time.Second)
	defer parentCancel()

	childCtx, childCancel := context.WithTimeout(parentCtx, 2*time.Second) // Child timeout longer than parent
	defer childCancel()

	// Child will cancel when parent times out (1 second), not at its own timeout (2 seconds)
	start := time.Now()
	<-childCtx.Done()
	elapsed := time.Since(start)

	if elapsed > 1100*time.Millisecond {
		t.Errorf("Child should have cancelled with parent, took %v", elapsed)
	}
}

// Graceful shutdown with cancellation
func serverWithGracefulShutdown(t *testing.T) {
	ctx, cancel := context.WithCancel(context.Background())
	var wg sync.WaitGroup

	// Simulate server components
	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			serverComponent(ctx, id)
		}(i)
	}

	// Simulate shutdown signal after 2 seconds
	time.Sleep(2 * time.Second)
	log.Println("Shutdown signal received")
	cancel() // Cancel all components

	// Wait for graceful shutdown
	shutdownComplete := make(chan struct{})
	go func() {
		wg.Wait()
		close(shutdownComplete)
	}()

	select {
	case <-shutdownComplete:
		log.Println("Graceful shutdown completed")
	case <-time.After(3 * time.Second):
		log.Println("Forced shutdown - components didn't finish in time")
	}
}

func serverComponent(ctx context.Context, id int) {
	ticker := time.NewTicker(500 * time.Millisecond)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			log.Printf("Component %d: still processing...", id)
		case <-ctx.Done():
			log.Printf("Component %d: cleaning up...", id)
			time.Sleep(100 * time.Millisecond) // Simulate cleanup
			log.Printf("Component %d: shutdown complete", id)
			return
		}
	}
}

// ============================================================================
// 3. SYNC PACKAGE - WaitGroup
// ============================================================================

func TestWaitGroup(t *testing.T) {
	var wg sync.WaitGroup
	results := make([]int, 0)
	var mu sync.Mutex // For safe slice access

	// Start multiple goroutines
	for i := 0; i < 5; i++ {
		wg.Add(1) // Increment counter BEFORE starting goroutine

		go func(id int) {
			defer wg.Done() // Decrement counter when done

			// Simulate work
			time.Sleep(time.Duration(id) * 100 * time.Millisecond)

			// Safely append result
			mu.Lock()
			results = append(results, id)
			mu.Unlock()

			log.Printf("Goroutine %d completed", id)
		}(i)
	}

	// Wait for all goroutines to complete
	wg.Wait()

	if len(results) != 5 {
		t.Errorf("Expected 5 results, got %d", len(results))
	}
	log.Printf("All goroutines completed. Results: %v", results)
}

// Common WaitGroup anti-pattern: Adding after starting goroutine
func waitGroupAntiPattern() {
	var wg sync.WaitGroup

	for i := 0; i < 3; i++ {
		go func(id int) {
			wg.Add(1) // WRONG: Might not execute before wg.Wait()
			defer wg.Done()
			// Work...
		}(i)
	}

	wg.Wait() // Might exit early!
}

// ============================================================================
// 4. SYNC PACKAGE - Mutex & RWMutex
// ============================================================================

type BankAccount struct {
	balance float64
	mu      sync.RWMutex // Protects balance
	name    string
	muName  sync.Mutex // Separate mutex for different fields
}

func (b *BankAccount) Deposit(amount float64) {
	b.mu.Lock()
	defer b.mu.Unlock()

	// Critical section
	b.balance += amount
	log.Printf("Deposited %.2f, new balance: %.2f", amount, b.balance)
}

func (b *BankAccount) Withdraw(amount float64) bool {
	b.mu.Lock()
	defer b.mu.Unlock()

	// Critical section
	if b.balance >= amount {
		b.balance -= amount
		log.Printf("Withdrew %.2f, new balance: %.2f", amount, b.balance)
		return true
	}
	log.Printf("Insufficient funds: %.2f < %.2f", b.balance, amount)
	return false
}

func (b *BankAccount) Balance() float64 {
	b.mu.RLock() // Read lock - multiple readers allowed
	defer b.mu.RUnlock()
	return b.balance
}

func (b *BankAccount) Transfer(to *BankAccount, amount float64) bool {
	// To avoid deadlock, always lock mutexes in consistent order
	// One approach: lock based on account name/ID
	if b.name < to.name {
		b.mu.Lock()
		to.mu.Lock()
	} else {
		to.mu.Lock()
		b.mu.Lock()
	}
	defer b.mu.Unlock()
	defer to.mu.Unlock()

	if b.balance >= amount {
		b.balance -= amount
		to.balance += amount
		return true
	}
	return false
}

func TestMutexPatterns(t *testing.T) {
	account := &BankAccount{balance: 1000, name: "Account1"}

	// Concurrent deposits and withdrawals
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			if id%2 == 0 {
				account.Deposit(100)
			} else {
				account.Withdraw(50)
			}
		}(i)
	}

	// Concurrent readers
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			balance := account.Balance()
			log.Printf("Current balance: %.2f", balance)
		}()
	}

	wg.Wait()
	finalBalance := account.Balance()
	if finalBalance != 1000+(5*100)-(5*50) {
		t.Errorf("Unexpected final balance: %.2f", finalBalance)
	}
}

// ============================================================================
// 5. SYNC PACKAGE - Once
// ============================================================================

type Singleton struct {
	value string
}

var (
	instance *Singleton
	once     sync.Once
)

func GetSingleton() *Singleton {
	once.Do(func() {
		log.Println("Initializing singleton")
		instance = &Singleton{value: "I am a singleton"}
		// Simulate expensive initialization
		time.Sleep(100 * time.Millisecond)
	})
	return instance
}

func TestSyncOnce(t *testing.T) {
	var wg sync.WaitGroup
	results := make(chan *Singleton, 10)

	// Multiple goroutines trying to get singleton
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			singleton := GetSingleton()
			results <- singleton
			log.Printf("Goroutine %d got singleton", id)
		}(i)
	}

	wg.Wait()
	close(results)

	// Verify all got the same instance
	first := <-results
	for singleton := range results {
		if singleton != first {
			t.Error("Got different singleton instances!")
		}
	}
}

// Once for lazy initialization
type LazyConfig struct {
	config map[string]string
	once   sync.Once
}

func (l *LazyConfig) Get(key string) string {
	l.once.Do(func() {
		log.Println("Loading configuration...")
		l.config = loadConfigFromFile()
	})
	return l.config[key]
}

func loadConfigFromFile() map[string]string {
	// Simulate slow config loading
	time.Sleep(200 * time.Millisecond)
	return map[string]string{"key": "value"}
}

// ============================================================================
// 6. SYNC PACKAGE - Cond (Condition Variables)
// ============================================================================

// Cond is used for signaling between goroutines

type WorkerPool struct {
	jobs    []string
	mu      sync.Mutex
	cond    *sync.Cond
	stopped bool
}

func NewWorkerPool() *WorkerPool {
	wp := &WorkerPool{
		jobs: make([]string, 0),
	}
	wp.cond = sync.NewCond(&wp.mu)
	return wp
}

func (wp *WorkerPool) AddJob(job string) {
	wp.mu.Lock()
	wp.jobs = append(wp.jobs, job)
	wp.mu.Unlock()
	wp.cond.Signal() // Wake one waiting worker
}

func (wp *WorkerPool) AddJobBroadcast(job string) {
	wp.mu.Lock()
	wp.jobs = append(wp.jobs, job)
	wp.mu.Unlock()
	wp.cond.Broadcast() // Wake all waiting workers
}

func (wp *WorkerPool) GetJob() (string, bool) {
	wp.mu.Lock()
	defer wp.mu.Unlock()

	// Wait for job or shutdown
	for len(wp.jobs) == 0 && !wp.stopped {
		wp.cond.Wait() // Releases mutex while waiting, reacquires when signaled
	}

	if wp.stopped && len(wp.jobs) == 0 {
		return "", false
	}

	job := wp.jobs[0]
	wp.jobs = wp.jobs[1:]
	return job, true
}

func (wp *WorkerPool) Stop() {
	wp.mu.Lock()
	wp.stopped = true
	wp.mu.Unlock()
	wp.cond.Broadcast() // Wake all waiting workers
}

func TestConditionVariables(t *testing.T) {
	pool := NewWorkerPool()
	var wg sync.WaitGroup

	// Start workers
	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for {
				job, ok := pool.GetJob()
				if !ok {
					log.Printf("Worker %d stopping", workerID)
					return
				}
				log.Printf("Worker %d processing: %s", workerID, job)
				time.Sleep(100 * time.Millisecond)
			}
		}(i)
	}

	// Add jobs
	for i := 0; i < 5; i++ {
		pool.AddJob(fmt.Sprintf("Job-%d", i))
		time.Sleep(50 * time.Millisecond)
	}

	// Wait for jobs to be processed
	time.Sleep(1 * time.Second)

	// Add more jobs with broadcast
	pool.AddJobBroadcast("Priority-Job")

	time.Sleep(500 * time.Millisecond)

	// Shutdown
	pool.Stop()
	wg.Wait()
}

// ============================================================================
// 7. ATOMIC OPERATIONS (sync/atomic)
// ============================================================================

// Atomic operations are lock-free and faster for simple operations

type AtomicCounter struct {
	count int64
}

func (c *AtomicCounter) Increment() {
	atomic.AddInt64(&c.count, 1)
}

func (c *AtomicCounter) Decrement() {
	atomic.AddInt64(&c.count, -1)
}

func (c *AtomicCounter) Value() int64 {
	return atomic.LoadInt64(&c.count)
}

func (c *AtomicCounter) CompareAndSwap(old, new int64) bool {
	return atomic.CompareAndSwapInt64(&c.count, old, new)
}

func TestAtomicOperations(t *testing.T) {
	var counter AtomicCounter
	var wg sync.WaitGroup

	// 1000 goroutines incrementing
	for i := 0; i < 1000; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			counter.Increment()
		}()
	}

	wg.Wait()

	if counter.Value() != 1000 {
		t.Errorf("Expected 1000, got %d", counter.Value())
	}

	// Test CAS (Compare-And-Swap) pattern
	success := counter.CompareAndSwap(1000, 2000)
	if !success {
		t.Error("CAS should have succeeded")
	}

	success = counter.CompareAndSwap(1000, 3000) // Should fail
	if success {
		t.Error("CAS should have failed")
	}
}

// Atomic value for arbitrary types
type Config struct {
	Timeout time.Duration
	MaxConn int
}

func TestAtomicValue(t *testing.T) {
	var config atomic.Value

	// Store initial config
	config.Store(&Config{
		Timeout: 5 * time.Second,
		MaxConn: 100,
	})

	// Multiple readers
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			c := config.Load().(*Config)
			log.Printf("Reader %d: Timeout=%v, MaxConn=%d",
				id, c.Timeout, c.MaxConn)
		}(i)
	}

	// Update config atomically
	newConfig := &Config{
		Timeout: 10 * time.Second,
		MaxConn: 200,
	}
	config.Store(newConfig)

	wg.Wait()
}

// ============================================================================
// 8. AVOIDING RACE CONDITIONS
// ============================================================================

// Race condition example
func raceConditionExample(t *testing.T) {
	var counter int

	// This will trigger race detector
	for i := 0; i < 10; i++ {
		go func() {
			counter++ // Data race!
		}()
	}

	time.Sleep(100 * time.Millisecond)
}

// Solutions for race conditions:

// 1. Use mutex
func safeWithMutex() {
	var counter int
	var mu sync.Mutex

	for i := 0; i < 10; i++ {
		go func() {
			mu.Lock()
			counter++
			mu.Unlock()
		}()
	}
}

// 2. Use atomic operations
func safeWithAtomic() {
	var counter int64

	for i := 0; i < 10; i++ {
		go func() {
			atomic.AddInt64(&counter, 1)
		}()
	}
}

// 3. Use channels (share by communicating)
func safeWithChannel() {
	counter := 0
	ch := make(chan int, 10) // Buffered channel

	// Single writer goroutine
	go func() {
		for i := 0; i < 10; i++ {
			ch <- i
		}
		close(ch)
	}()

	// Single reader goroutine
	go func() {
		for range ch {
			counter++
		}
	}()

	time.Sleep(100 * time.Millisecond)
}

// 4. Immutable data structures
type ImmutableCounter struct {
	value int
}

func (c ImmutableCounter) Increment() ImmutableCounter {
	return ImmutableCounter{value: c.value + 1}
}

// ============================================================================
// 9. DEADLOCKS & LIVELOCKS
// ============================================================================

// Deadlock example: Two goroutines waiting for each other
func deadlockExample(t *testing.T) {
	var mu1, mu2 sync.Mutex

	go func() {
		mu1.Lock()
		time.Sleep(10 * time.Millisecond)
		mu2.Lock() // Will wait forever

		// Critical section
		mu2.Unlock()
		mu1.Unlock()
	}()

	go func() {
		mu2.Lock()
		time.Sleep(10 * time.Millisecond)
		mu1.Lock() // Will wait forever

		// Critical section
		mu1.Unlock()
		mu2.Unlock()
	}()

	// Wait and see deadlock
	time.Sleep(1 * time.Second)
}

// Avoiding deadlocks:
// 1. Always lock mutexes in consistent order
func noDeadlockWithOrdering() {
	var mu1, mu2 sync.Mutex

	// Always lock mu1 before mu2
	go func() {
		mu1.Lock()
		mu2.Lock()
		// Work...
		mu2.Unlock()
		mu1.Unlock()
	}()

	go func() {
		mu1.Lock()
		mu2.Lock()
		// Work...
		mu2.Unlock()
		mu1.Unlock()
	}()
}

// 2. Use timeout with TryLock (Go 1.18+)
func tryLockExample() {
	var mu sync.Mutex

	// Try to acquire lock with timeout
	acquired := make(chan bool)
	go func() {
		start := time.Now()
		for time.Since(start) < 100*time.Millisecond {
			if mu.TryLock() {
				acquired <- true
				mu.Unlock()
				return
			}
			time.Sleep(10 * time.Millisecond)
		}
		acquired <- false
	}()

	// Hold lock for a while
	mu.Lock()
	time.Sleep(50 * time.Millisecond)
	mu.Unlock()

	if <-acquired {
		log.Println("Lock acquired successfully")
	}
}

// 3. Detect deadlocks with timeout pattern
func withTimeoutMutex(ctx context.Context, mu *sync.Mutex) error {
	select {
	case <-ctx.Done():
		return ctx.Err()
	default:
	}

	// Try to acquire lock
	ch := make(chan struct{})
	go func() {
		mu.Lock()
		close(ch)
	}()

	select {
	case <-ch:
		// Lock acquired
		return nil
	case <-ctx.Done():
		// Timeout or cancellation
		return ctx.Err()
	}
}

// Livelock example: Goroutines too polite, never make progress
func livelockExample() {
	var mu1, mu2 sync.Mutex
	mu1.Lock()
	mu2.Lock()

	go func() {
		for {
			if mu1.TryLock() {
				time.Sleep(10 * time.Millisecond)
				if mu2.TryLock() {
					log.Println("Goroutine 1 acquired both locks")
					mu2.Unlock()
					mu1.Unlock()
					return
				}
				mu1.Unlock()
			}
			time.Sleep(10 * time.Millisecond) // Backoff
		}
	}()

	go func() {
		for {
			if mu2.TryLock() {
				time.Sleep(10 * time.Millisecond)
				if mu1.TryLock() {
					log.Println("Goroutine 2 acquired both locks")
					mu1.Unlock()
					mu2.Unlock()
					return
				}
				mu2.Unlock()
			}
			time.Sleep(10 * time.Millisecond) // Backoff
		}
	}()

	// Release locks after delay
	go func() {
		time.Sleep(100 * time.Millisecond)
		mu1.Unlock()
		mu2.Unlock()
	}()

	time.Sleep(1 * time.Second)
}

// ============================================================================
// 10. RACE DETECTOR (go test -race)
// ============================================================================

// Run tests with: go test -race ./...

// Data race example that race detector will catch
func TestDataRace(t *testing.T) {
	var shared int

	// Reader goroutine
	go func() {
		for i := 0; i < 100; i++ {
			_ = shared // Read without synchronization
		}
	}()

	// Writer goroutine
	go func() {
		for i := 0; i < 100; i++ {
			shared = i // Write without synchronization
		}
	}()

	time.Sleep(100 * time.Millisecond)
}

// False sharing example (performance issue)
type FalseSharing struct {
	a int64
	_ [56]byte // Padding to put on different cache lines (64 bytes typical cache line)
	b int64
}

func TestFalseSharing(t *testing.T) {
	var data FalseSharing

	go func() {
		for i := 0; i < 1000000; i++ {
			atomic.AddInt64(&data.a, 1)
		}
	}()

	go func() {
		for i := 0; i < 1000000; i++ {
			atomic.AddInt64(&data.b, 1)
		}
	}()

	time.Sleep(1 * time.Second)
}

// ============================================================================
// 11. ADVANCED PATTERNS
// ============================================================================

// Worker pool with graceful shutdown
type WorkerPoolAdvanced struct {
	workers   int
	taskQueue chan func()
	wg        sync.WaitGroup
	ctx       context.Context
	cancel    context.CancelFunc
}

func NewWorkerPoolAdvanced(workers int) *WorkerPoolAdvanced {
	ctx, cancel := context.WithCancel(context.Background())
	pool := &WorkerPoolAdvanced{
		workers:   workers,
		taskQueue: make(chan func(), 100),
		ctx:       ctx,
		cancel:    cancel,
	}

	pool.startWorkers()
	return pool
}

func (p *WorkerPoolAdvanced) startWorkers() {
	for i := 0; i < p.workers; i++ {
		p.wg.Add(1)
		go p.worker(i)
	}
}

func (p *WorkerPoolAdvanced) worker(id int) {
	defer p.wg.Done()

	for {
		select {
		case task := <-p.taskQueue:
			task()
		case <-p.ctx.Done():
			log.Printf("Worker %d shutting down", id)
			return
		}
	}
}

func (p *WorkerPoolAdvanced) Submit(task func()) error {
	select {
	case p.taskQueue <- task:
		return nil
	case <-p.ctx.Done():
		return fmt.Errorf("worker pool stopped")
	}
}

func (p *WorkerPoolAdvanced) Stop() {
	p.cancel()
	p.wg.Wait()
	close(p.taskQueue)
}

// Rate limiter using token bucket
type RateLimiter struct {
	tokens     int64
	maxTokens  int64
	refillRate time.Duration
	lastRefill time.Time
	mu         sync.Mutex
}

func NewRateLimiter(maxTokens int64, refillRate time.Duration) *RateLimiter {
	return &RateLimiter{
		tokens:     maxTokens,
		maxTokens:  maxTokens,
		refillRate: refillRate,
		lastRefill: time.Now(),
	}
}

func (r *RateLimiter) Allow() bool {
	r.mu.Lock()
	defer r.mu.Unlock()

	// Refill tokens
	now := time.Now()
	elapsed := now.Sub(r.lastRefill)
	tokensToAdd := int64(elapsed / r.refillRate)

	if tokensToAdd > 0 {
		r.tokens = min(r.maxTokens, r.tokens+tokensToAdd)
		r.lastRefill = now
	}

	if r.tokens > 0 {
		r.tokens--
		return true
	}
	return false
}

// ============================================================================
// 12. CONCURRENCY PATTERNS
// ============================================================================

// Fan-out, fan-in pattern
func TestFanOutFanIn(t *testing.T) {
	// Generate work
	workCh := make(chan int, 100)
	go func() {
		for i := 0; i < 100; i++ {
			workCh <- i
		}
		close(workCh)
	}()

	// Fan-out: multiple workers process work
	const numWorkers = 5
	resultCh := make(chan int, 100)

	var wg sync.WaitGroup
	for i := 0; i < numWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for work := range workCh {
				// Process work
				result := work * 2
				resultCh <- result
				log.Printf("Worker %d processed %d -> %d", workerID, work, result)
			}
		}(i)
	}

	// Close result channel when all workers done
	go func() {
		wg.Wait()
		close(resultCh)
	}()

	// Fan-in: collect all results
	var results []int
	for result := range resultCh {
		results = append(results, result)
	}

	log.Printf("Processed %d items", len(results))
}

// Pipeline pattern
func TestPipelinePattern(t *testing.T) {
	// Stage 1: Generate numbers
	gen := func(ctx context.Context, nums ...int) <-chan int {
		out := make(chan int)
		go func() {
			defer close(out)
			for _, n := range nums {
				select {
				case out <- n:
				case <-ctx.Done():
					return
				}
			}
		}()
		return out
	}

	// Stage 2: Square numbers
	square := func(ctx context.Context, in <-chan int) <-chan int {
		out := make(chan int)
		go func() {
			defer close(out)
			for n := range in {
				select {
				case out <- n * n:
				case <-ctx.Done():
					return
				}
			}
		}()
		return out
	}

	// Stage 3: Add 1
	addOne := func(ctx context.Context, in <-chan int) <-chan int {
		out := make(chan int)
		go func() {
			defer close(out)
			for n := range in {
				select {
				case out <- n + 1:
				case <-ctx.Done():
					return
				}
			}
		}()
		return out
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	// Build pipeline: gen -> square -> addOne
	squared := square(ctx, gen(ctx, 1, 2, 3, 4, 5))
	result := addOne(ctx, squared)

	// Collect results
	var results []int
	for r := range result {
		results = append(results, r)
		log.Printf("Result: %d", r)
	}

	if len(results) != 5 {
		t.Errorf("Expected 5 results, got %d", len(results))
	}
}

// ============================================================================
// BEST PRACTICES SUMMARY
// ============================================================================

/*
1. Prefer channels for coordination, mutexes for state protection
2. Use context for cancellation and timeouts
3. Always call WaitGroup.Add() before starting goroutine
4. Use RWMutex when reads greatly outnumber writes
5. Use atomic operations for simple counters/flags
6. Always run tests with -race flag in CI
7. Avoid global variables in concurrent code
8. Use sync.Once for thread-safe initialization
9. Design for immutability where possible
10. Use proper locking order to prevent deadlocks
11. Consider using worker pools for resource management
12. Implement graceful shutdown with context cancellation
13. Profile concurrent applications to find bottlenecks
14. Use buffered channels when producer/consumer rates differ
15. Keep critical sections as small as possible
*/

// Helper function for tests
func min(a, b int64) int64 {
	if a < b {
		return a
	}
	return b
}
