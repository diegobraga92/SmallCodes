// ============================================
// GO CONCURRENCY BASICS - COMPREHENSIVE GUIDE
// ============================================

package main

import (
	"context"
	"fmt"
	"math/rand"
	"runtime"
	"sync"
	"sync/atomic"
	"time"
)

// ============================================
// 1. GOROUTINES - LIGHTWEIGHT THREADS
// ============================================

func goroutinesDemo() {
	fmt.Println("\n=== 1. Goroutines ===")

	// Goroutines are lightweight threads managed by the Go runtime
	// They have small stack (2KB initially, grows as needed)
	// Cheap to create (compared to OS threads)

	// Starting a goroutine
	fmt.Println("Starting goroutines...")

	// Simple goroutine
	go func() {
		fmt.Println("Goroutine 1: Running concurrently")
	}()

	// Goroutine with parameters
	message := "Hello from goroutine"
	go func(msg string) {
		fmt.Printf("Goroutine 2: %s\n", msg)
	}(message)

	// Wait for goroutines to complete (naive way - better ways later)
	time.Sleep(100 * time.Millisecond)

	// Multiple goroutines
	fmt.Println("\nStarting 5 goroutines:")
	for i := 0; i < 5; i++ {
		id := i
		go func() {
			time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
			fmt.Printf("  Goroutine %d completed\n", id)
		}()
	}

	time.Sleep(200 * time.Millisecond)

	// Goroutine scheduling
	fmt.Printf("\nCurrent number of goroutines: %d\n", runtime.NumGoroutine())
	fmt.Printf("Number of CPU cores: %d\n", runtime.NumCPU())

	// Setting GOMAXPROCS
	prev := runtime.GOMAXPROCS(2) // Use 2 processors
	fmt.Printf("Previous GOMAXPROCS: %d\n", prev)
	runtime.GOMAXPROCS(prev) // Restore

	// Common pattern: Goroutine with loop
	done := make(chan bool)
	go func() {
		for i := 0; i < 3; i++ {
			fmt.Printf("  Looping goroutine: iteration %d\n", i)
			time.Sleep(50 * time.Millisecond)
		}
		done <- true
	}()

	<-done // Wait for completion

	// Important: main() function doesn't wait for goroutines
	// Goroutines exit when main exits!
}

// ============================================
// 2. CHANNELS - COMMUNICATION BETWEEN GOROUTINES
// ============================================

func channelsDemo() {
	fmt.Println("\n=== 2. Channels ===")

	// Channels are typed conduits for goroutine communication
	// They provide synchronization and data transfer

	// Creating channels
	var unbufferedChan chan int          // nil channel
	unbufferedChan = make(chan int)      // unbuffered channel (capacity 0)
	bufferedChan := make(chan string, 3) // buffered channel (capacity 3)

	fmt.Printf("Unbuffered channel: %v\n", unbufferedChan)
	fmt.Printf("Buffered channel (cap=3): %v\n", bufferedChan)

	// Unbuffered channels (synchronous)
	fmt.Println("\n=== Unbuffered Channels ===")
	fmt.Println("Send blocks until receiver is ready")
	fmt.Println("Receive blocks until sender is ready")

	// Example: Ping-pong with unbuffered channel
	pingPongChan := make(chan string)

	go func() {
		msg := <-pingPongChan // Wait for ping
		fmt.Printf("  Received: %s\n", msg)
		pingPongChan <- "pong" // Send pong
	}()

	pingPongChan <- "ping" // Send ping
	msg := <-pingPongChan  // Wait for pong
	fmt.Printf("  Received: %s\n", msg)

	// Buffered channels (asynchronous to a point)
	fmt.Println("\n=== Buffered Channels ===")
	fmt.Println("Send only blocks when buffer is full")
	fmt.Println("Receive only blocks when buffer is empty")

	bufChan := make(chan int, 2)

	// Can send twice without blocking
	bufChan <- 1
	bufChan <- 2

	// Third send would block (buffer full)
	go func() {
		time.Sleep(100 * time.Millisecond)
		<-bufChan // Make room
	}()

	bufChan <- 3 // Will block briefly until space

	// Receive values
	fmt.Printf("Received: %d\n", <-bufChan)
	fmt.Printf("Received: %d\n", <-bufChan)
	fmt.Printf("Received: %d\n", <-bufChan)

	// Channel operations
	fmt.Println("\n=== Channel Operations ===")

	// Closing channels
	ch := make(chan int)
	go func() {
		for i := 0; i < 3; i++ {
			ch <- i
		}
		close(ch) // Close channel after sending
	}()

	// Receiving from closed channel
	for {
		value, ok := <-ch
		if !ok {
			fmt.Println("Channel closed")
			break
		}
		fmt.Printf("Received: %d\n", value)
	}

	// Range over channel
	ch2 := make(chan string, 2)
	ch2 <- "first"
	ch2 <- "second"
	close(ch2)

	fmt.Println("Range over channel:")
	for item := range ch2 {
		fmt.Printf("  %s\n", item)
	}

	// nil channels
	var nilChan chan int
	// nilChan <- 1 // Would block forever (deadlock!)
	// <-nilChan    // Would block forever
	fmt.Println("nil channels block forever on send/receive")
}

// ============================================
// 3. CHANNEL DIRECTION (<-chan, chan<-)
// ============================================

func channelDirectionDemo() {
	fmt.Println("\n=== 3. Channel Direction ===")

	// Channel types can be restricted to send-only or receive-only
	// This improves type safety and code clarity

	// Producer function (send-only channel)
	producer := func(ch chan<- int) {
		for i := 0; i < 3; i++ {
			ch <- i
			time.Sleep(100 * time.Millisecond)
		}
		close(ch)
	}

	// Consumer function (receive-only channel)
	consumer := func(ch <-chan int) {
		for value := range ch {
			fmt.Printf("Consumer received: %d\n", value)
		}
	}

	// Create channel
	ch := make(chan int)

	// Start producer and consumer
	go producer(ch)
	go consumer(ch)

	time.Sleep(500 * time.Millisecond)

	// Example with return channel
	fmt.Println("\n=== Return Channel Example ===")

	getPrimes := func(n int) <-chan int {
		ch := make(chan int)
		go func() {
			defer close(ch)
			for i := 2; i <= n; i++ {
				if isPrime(i) {
					ch <- i
				}
			}
		}()
		return ch // Returns receive-only channel
	}

	primes := getPrimes(20)
	fmt.Print("Primes under 20: ")
	for prime := range primes {
		fmt.Printf("%d ", prime)
	}
	fmt.Println()

	// Bidirectional to unidirectional conversion
	fmt.Println("\n=== Channel Conversion ===")
	bidiChan := make(chan string)

	var sendOnly chan<- string = bidiChan    // Convert to send-only
	var receiveOnly <-chan string = bidiChan // Convert to receive-only

	go func() {
		sendOnly <- "Hello"
		close(sendOnly)
	}()

	msg := <-receiveOnly
	fmt.Printf("Received through directional channels: %s\n", msg)
}

func isPrime(n int) bool {
	if n < 2 {
		return false
	}
	for i := 2; i*i <= n; i++ {
		if n%i == 0 {
			return false
		}
	}
	return true
}

// ============================================
// 4. SELECT - MULTIPLEXING CHANNELS
// ============================================

func selectDemo() {
	fmt.Println("\n=== 4. Select Statement ===")

	// select allows waiting on multiple channel operations
	// It's like switch but for channels

	// Basic select
	fmt.Println("=== Basic Select ===")
	ch1 := make(chan string)
	ch2 := make(chan string)

	go func() {
		time.Sleep(100 * time.Millisecond)
		ch1 <- "from ch1"
	}()

	go func() {
		time.Sleep(50 * time.Millisecond)
		ch2 <- "from ch2"
	}()

	// select picks the first channel that's ready
	select {
	case msg1 := <-ch1:
		fmt.Printf("Received: %s\n", msg1)
	case msg2 := <-ch2:
		fmt.Printf("Received: %s\n", msg2)
	case <-time.After(200 * time.Millisecond):
		fmt.Println("Timeout!")
	}

	// Non-blocking select with default
	fmt.Println("\n=== Non-blocking Select ===")
	ch := make(chan int)

	select {
	case val := <-ch:
		fmt.Printf("Got value: %d\n", val)
	default:
		fmt.Println("No value ready (non-blocking)")
	}

	// Select with send and receive
	fmt.Println("\n=== Select with Send ===")
	ch3 := make(chan string, 1)
	ch4 := make(chan string, 1)

	ch3 <- "test"

	select {
	case ch4 <- "to ch4":
		fmt.Println("Sent to ch4")
	case msg := <-ch3:
		fmt.Printf("Received from ch3: %s\n", msg)
	}

	// Random selection when multiple ready
	fmt.Println("\n=== Random Selection ===")
	chA := make(chan string)
	chB := make(chan string)

	// When multiple cases are ready, select chooses randomly
	for i := 0; i < 10; i++ {
		go func() { chA <- "A" }()
		go func() { chB <- "B" }()

		select {
		case <-chA:
			fmt.Print("A")
		case <-chB:
			fmt.Print("B")
		}
	}
	fmt.Println()

	// Continuous select with loop
	fmt.Println("\n=== Continuous Select ===")
	ticker := time.NewTicker(100 * time.Millisecond)
	done := make(chan bool)

	go func() {
		time.Sleep(450 * time.Millisecond)
		done <- true
	}()

	count := 0
loop:
	for {
		select {
		case <-ticker.C:
			count++
			fmt.Printf("Tick %d\n", count)
		case <-done:
			fmt.Println("Done!")
			ticker.Stop()
			break loop
		}
	}
}

// ============================================
// 5. WORKER POOLS
// ============================================

func workerPoolsDemo() {
	fmt.Println("\n=== 5. Worker Pools ===")

	// Worker pools allow limiting concurrent goroutines
	// Useful for controlling resource usage

	// Simple worker pool
	fmt.Println("=== Simple Worker Pool ===")

	worker := func(id int, jobs <-chan int, results chan<- int) {
		for job := range jobs {
			fmt.Printf("Worker %d processing job %d\n", id, job)
			time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
			results <- job * 2 // Process job
		}
	}

	// Create channels
	numJobs := 10
	jobs := make(chan int, numJobs)
	results := make(chan int, numJobs)

	// Start workers
	numWorkers := 3
	for w := 1; w <= numWorkers; w++ {
		go worker(w, jobs, results)
	}

	// Send jobs
	for j := 1; j <= numJobs; j++ {
		jobs <- j
	}
	close(jobs)

	// Collect results
	for r := 1; r <= numJobs; r++ {
		<-results
	}

	// Worker pool with wait groups
	fmt.Println("\n=== Worker Pool with WaitGroup ===")

	type Task struct {
		ID   int
		Data string
	}

	processTask := func(task Task) string {
		time.Sleep(time.Duration(rand.Intn(50)) * time.Millisecond)
		return fmt.Sprintf("Processed: %s", task.Data)
	}

	tasks := make(chan Task, 20)
	var wg sync.WaitGroup

	// Create worker pool
	for i := 0; i < 4; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for task := range tasks {
				result := processTask(task)
				fmt.Printf("Worker %d: %s (task %d)\n", workerID, result, task.ID)
			}
		}(i)
	}

	// Send tasks
	for i := 0; i < 10; i++ {
		tasks <- Task{ID: i, Data: fmt.Sprintf("task-%d", i)}
	}
	close(tasks)

	// Wait for all workers
	wg.Wait()
	fmt.Println("All workers completed")

	// Dynamic worker pool
	fmt.Println("\n=== Dynamic Worker Pool ===")

	workerPool := func(workerCount int, taskCount int) {
		tasks := make(chan int, taskCount)
		var wg sync.WaitGroup

		// Start workers
		for i := 0; i < workerCount; i++ {
			wg.Add(1)
			go func(id int) {
				defer wg.Done()
				for task := range tasks {
					// Simulate work
					time.Sleep(10 * time.Millisecond)
					_ = task
				}
			}(i)
		}

		// Send tasks
		for i := 0; i < taskCount; i++ {
			tasks <- i
		}
		close(tasks)

		wg.Wait()
		fmt.Printf("Completed %d tasks with %d workers\n", taskCount, workerCount)
	}

	workerPool(5, 50)
}

// ============================================
// 6. COMMON CONCURRENCY PATTERNS
// ============================================

func commonPatternsDemo() {
	fmt.Println("\n=== 6. Common Concurrency Patterns ===")

	// Pattern 1: Generator
	fmt.Println("=== Pattern 1: Generator ===")

	numberGenerator := func(start, end int) <-chan int {
		ch := make(chan int)
		go func() {
			for i := start; i <= end; i++ {
				ch <- i
			}
			close(ch)
		}()
		return ch
	}

	numbers := numberGenerator(1, 5)
	for n := range numbers {
		fmt.Printf("Generated: %d\n", n)
	}

	// Pattern 2: Fan-out/Fan-in
	fmt.Println("\n=== Pattern 2: Fan-out/Fan-in ===")

	producer := func(nums ...int) <-chan int {
		out := make(chan int)
		go func() {
			for _, n := range nums {
				out <- n
			}
			close(out)
		}()
		return out
	}

	squareWorker := func(in <-chan int) <-chan int {
		out := make(chan int)
		go func() {
			for n := range in {
				out <- n * n
			}
			close(out)
		}()
		return out
	}

	merge := func(channels ...<-chan int) <-chan int {
		var wg sync.WaitGroup
		out := make(chan int)

		// Start output goroutine for each input channel
		output := func(c <-chan int) {
			defer wg.Done()
			for n := range c {
				out <- n
			}
		}

		wg.Add(len(channels))
		for _, c := range channels {
			go output(c)
		}

		// Close out when all outputs are done
		go func() {
			wg.Wait()
			close(out)
		}()

		return out
	}

	// Create producer
	in := producer(1, 2, 3, 4, 5)

	// Fan-out: Distribute work to multiple workers
	c1 := squareWorker(in)
	c2 := squareWorker(in)

	// Fan-in: Merge results
	for result := range merge(c1, c2) {
		fmt.Printf("Square: %d\n", result)
	}

	// Pattern 3: Pipeline
	fmt.Println("\n=== Pattern 3: Pipeline ===")

	// Stage 1: Generate numbers
	generate := func(done <-chan struct{}, nums ...int) <-chan int {
		out := make(chan int)
		go func() {
			defer close(out)
			for _, n := range nums {
				select {
				case out <- n:
				case <-done:
					return
				}
			}
		}()
		return out
	}

	// Stage 2: Square numbers
	square := func(done <-chan struct{}, in <-chan int) <-chan int {
		out := make(chan int)
		go func() {
			defer close(out)
			for n := range in {
				select {
				case out <- n * n:
				case <-done:
					return
				}
			}
		}()
		return out
	}

	// Stage 3: Add 10
	addTen := func(done <-chan struct{}, in <-chan int) <-chan int {
		out := make(chan int)
		go func() {
			defer close(out)
			for n := range in {
				select {
				case out <- n + 10:
				case <-done:
					return
				}
			}
		}()
		return out
	}

	done := make(chan struct{})
	defer close(done)

	// Build pipeline
	nums := generate(done, 1, 2, 3, 4)
	squares := square(done, nums)
	results := addTen(done, squares)

	for res := range results {
		fmt.Printf("Pipeline result: %d\n", res)
	}

	// Pattern 4: Rate Limiting
	fmt.Println("\n=== Pattern 4: Rate Limiting ===")

	requests := make(chan int, 5)
	for i := 1; i <= 5; i++ {
		requests <- i
	}
	close(requests)

	// Rate limiter
	limiter := time.Tick(200 * time.Millisecond)

	for req := range requests {
		<-limiter // Wait for next tick
		fmt.Printf("Processing request %d at %v\n", req, time.Now())
	}

	// Pattern 5: Context with cancellation
	fmt.Println("\n=== Pattern 5: Context Cancellation ===")

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	go func() {
		select {
		case <-time.After(500 * time.Millisecond):
			fmt.Println("Operation timed out")
			cancel()
		case <-ctx.Done():
			fmt.Println("Operation cancelled")
		}
	}()

	// Pattern 6: Worker pool with error handling
	fmt.Println("\n=== Pattern 6: Worker Pool with Errors ===")

	type Result struct {
		Value int
		Error error
	}

	workerWithError := func(id int, jobs <-chan int, results chan<- Result) {
		for job := range jobs {
			if job%3 == 0 { // Simulate error
				results <- Result{Error: fmt.Errorf("job %d is divisible by 3", job)}
			} else {
				time.Sleep(50 * time.Millisecond)
				results <- Result{Value: job * 2}
			}
		}
	}

	jobChan := make(chan int, 10)
	resultChan := make(chan Result, 10)

	// Start workers
	for i := 0; i < 3; i++ {
		go workerWithError(i, jobChan, resultChan)
	}

	// Send jobs
	go func() {
		for i := 1; i <= 10; i++ {
			jobChan <- i
		}
		close(jobChan)
	}()

	// Collect results
	for i := 1; i <= 10; i++ {
		result := <-resultChan
		if result.Error != nil {
			fmt.Printf("Error: %v\n", result.Error)
		} else {
			fmt.Printf("Success: %d\n", result.Value)
		}
	}

	// Pattern 7: Pub/Sub
	fmt.Println("\n=== Pattern 7: Pub/Sub ===")

	type Subscriber chan string

	broker := struct {
		subscribers []Subscriber
		sync.RWMutex
	}{
		subscribers: make([]Subscriber, 0),
	}

	subscribe := func() Subscriber {
		broker.Lock()
		defer broker.Unlock()
		ch := make(Subscriber, 10)
		broker.subscribers = append(broker.subscribers, ch)
		return ch
	}

	publish := func(message string) {
		broker.RLock()
		defer broker.RUnlock()
		for _, sub := range broker.subscribers {
			select {
			case sub <- message:
			default:
				// Skip slow subscribers
			}
		}
	}

	// Create subscribers
	sub1 := subscribe()
	sub2 := subscribe()

	// Start subscribers
	go func() {
		for msg := range sub1 {
			fmt.Printf("Subscriber 1: %s\n", msg)
		}
	}()

	go func() {
		for msg := range sub2 {
			fmt.Printf("Subscriber 2: %s\n", msg)
		}
	}()

	// Publish messages
	publish("Hello")
	publish("World")

	time.Sleep(100 * time.Millisecond)
	close(sub1)
	close(sub2)
}

// ============================================
// 7. SYNCHRONIZATION PRIMITIVES
// ============================================

func syncPrimitivesDemo() {
	fmt.Println("\n=== 7. Synchronization Primitives ===")

	// WaitGroup
	fmt.Println("=== WaitGroup ===")
	var wg sync.WaitGroup

	for i := 0; i < 3; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			time.Sleep(time.Duration(id*100) * time.Millisecond)
			fmt.Printf("Goroutine %d done\n", id)
		}(i)
	}

	wg.Wait()
	fmt.Println("All goroutines completed")

	// Mutex
	fmt.Println("\n=== Mutex ===")
	var (
		mu    sync.Mutex
		count int
	)

	for i := 0; i < 10; i++ {
		go func() {
			mu.Lock()
			count++
			mu.Unlock()
		}()
	}

	time.Sleep(100 * time.Millisecond)
	fmt.Printf("Count: %d\n", count)

	// RWMutex (Reader/Writer lock)
	fmt.Println("\n=== RWMutex ===")
	var (
		rwmu   sync.RWMutex
		shared int
	)

	// Multiple readers can read concurrently
	for i := 0; i < 5; i++ {
		go func(id int) {
			rwmu.RLock()
			fmt.Printf("Reader %d: value = %d\n", id, shared)
			rwmu.RUnlock()
		}(i)
	}

	// Only one writer at a time
	go func() {
		rwmu.Lock()
		shared = 42
		rwmu.Unlock()
	}()

	time.Sleep(100 * time.Millisecond)

	// Once
	fmt.Println("\n=== Once ===")
	var once sync.Once
	initialize := func() {
		fmt.Println("Initialized once")
	}

	for i := 0; i < 5; i++ {
		go once.Do(initialize)
	}

	time.Sleep(100 * time.Millisecond)

	// Atomic operations
	fmt.Println("\n=== Atomic Operations ===")
	var atomicCounter int32

	for i := 0; i < 10; i++ {
		go func() {
			atomic.AddInt32(&atomicCounter, 1)
		}()
	}

	time.Sleep(100 * time.Millisecond)
	fmt.Printf("Atomic counter: %d\n", atomic.LoadInt32(&atomicCounter))

	// Cond (Condition variable)
	fmt.Println("\n=== Condition Variable ===")
	var (
		condMu sync.Mutex
		cond   = sync.NewCond(&condMu)
		ready  bool
	)

	// Waiter
	go func() {
		condMu.Lock()
		for !ready {
			cond.Wait() // Releases lock, waits, reacquires lock
		}
		fmt.Println("Condition met!")
		condMu.Unlock()
	}()

	// Signaler
	time.Sleep(100 * time.Millisecond)
	condMu.Lock()
	ready = true
	cond.Signal() // Wake one waiter
	condMu.Unlock()

	time.Sleep(100 * time.Millisecond)
}

// ============================================
// MAIN FUNCTION
// ============================================

func main() {
	fmt.Println("=== GO CONCURRENCY BASICS ===\n")

	// Run all demonstrations
	goroutinesDemo()
	channelsDemo()
	channelDirectionDemo()
	selectDemo()
	workerPoolsDemo()
	commonPatternsDemo()
	syncPrimitivesDemo()

	fmt.Println("\n=== END OF DEMONSTRATION ===")

	// Final cleanup
	time.Sleep(200 * time.Millisecond)
	fmt.Printf("\nFinal goroutine count: %d\n", runtime.NumGoroutine())
}

// ============================================
// KEY TAKEAWAYS FOR DEVELOPERS
// ============================================

// JUNIOR DEVELOPERS:
// 1. Use `go` keyword to start goroutines
// 2. Use channels for goroutine communication (don't share memory!)
// 3. Always close channels when done sending
// 4. Use WaitGroup to wait for goroutines to complete
// 5. Prefer unbuffered channels for synchronization

// MID-LEVEL DEVELOPERS:
// 1. Master select statement for multiplexing channels
// 2. Use buffered channels when producer/consumer rates differ
// 3. Implement worker pools to limit concurrency
// 4. Use context for cancellation and timeouts
// 5. Understand channel direction for better APIs
// 6. Use sync.Once for one-time initialization

// SENIOR DEVELOPERS:
// 1. Design with pipeline patterns (fan-out/fan-in)
// 2. Implement graceful shutdown patterns
// 3. Use atomic operations for lock-free counters
// 4. Implement backpressure with buffered channels
// 5. Use RWMutex for read-heavy workloads
// 6. Design for cancellation and timeout at all levels
// 7. Implement circuit breakers and rate limiters

// PERFORMANCE TIPS:
// 1. Limit goroutine creation (use worker pools)
// 2. Use buffered channels to reduce blocking
// 3. Batch operations when possible
// 4. Use sync.Pool for object reuse
// 5. Prefer channels over mutexes for coordination

// SAFETY & ROBUSTNESS:
// 1. Always handle channel closure
// 2. Use contexts to propagate cancellation
// 3. Implement timeouts for all blocking operations
// 4. Handle panics in goroutines (use recover)
// 5. Monitor goroutine leaks
// 6. Use race detector: go run -race

// COMMON PITFALLS:
// 1. Goroutine leaks (forgetting to close channels)
// 2. Deadlocks (circular channel dependencies)
// 3. Race conditions (shared memory without sync)
// 4. Blocking forever (nil channels, no receiver)
// 5. Closing closed channels (panic)
// 6. Send on closed channel (panic)

// PRODUCTION PATTERNS:
// 1. Graceful shutdown with context
// 2. Worker pools with dynamic scaling
// 3. Health checks and circuit breakers
// 4. Request/response with correlation IDs
// 5. Load balancing across workers
// 6. Monitoring goroutine counts

// DEBUGGING TIPS:
// 1. Use runtime.NumGoroutine() to check leaks
// 2. Add timeouts to all channel operations
// 3. Use panic/recover in critical goroutines
// 4. Log goroutine IDs for tracing
// 5. Use pprof for profiling goroutines

// TESTING CONCURRENT CODE:
// 1. Use go test -race
// 2. Test with different GOMAXPROCS values
// 3. Use timeouts in tests
// 4. Test for race conditions
// 5. Use deterministic random seeds

// MEMORY MANAGEMENT:
// 1. Goroutines have small initial stack (2KB)
// 2. Stacks grow and shrink as needed
// 3. Channel buffers consume memory
// 4. Be mindful of goroutine-local variables
// 5. Use sync.Pool for expensive allocations

// SCALING CONSIDERATIONS:
// 1. More goroutines != faster
// 2. Consider Amdahl's law (sequential parts limit speedup)
// 3. Monitor context switching overhead
// 4. Balance between goroutines and OS threads
// 5. Consider NUMA architectures for high-performance
