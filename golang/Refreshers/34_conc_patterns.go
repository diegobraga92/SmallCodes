/*
GOLANG CONCURRENCY PATTERNS GUIDE
From Junior to Senior Developer Concepts
=========================================
*/

package main

import (
	"context"
	"errors"
	"fmt"
	"log"
	"math/rand"
	"runtime"
	"sync"
	"sync/atomic"
	"time"
)

// ============================================================================
// 1. FAN-IN/FAN-OUT - Parallel Processing Patterns
// ============================================================================

// Fan-out: Distribute work to multiple goroutines
// Fan-in: Collect results from multiple goroutines

type FanInFanOut struct{}

func (ffo *FanInFanOut) Demonstrate() {
	fmt.Println("=== Fan-in/Fan-out Patterns ===")
	
	// Example: Processing multiple URLs concurrently
	urls := []string{
		"https://api.example.com/users",
		"https://api.example.com/products",
		"https://api.example.com/orders",
		"https://api.example.com/inventory",
		"https://api.example.com/payments",
	}
	
	// FAN-OUT: Start multiple workers
	// FAN-IN: Collect all results
	
	results := ffo.ProcessURLsConcurrently(urls, 3)
	fmt.Printf("Processed %d URLs, got %d results\n", len(urls), len(results))
}

// Pattern 1: Simple Fan-out with WaitGroup
func (ffo *FanInFanOut) SimpleFanOut(urls []string) []string {
	var wg sync.WaitGroup
	results := make([]string, len(urls))
	
	for i, url := range urls {
		wg.Add(1)
		go func(idx int, u string) {
			defer wg.Done()
			// Simulate processing
			time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
			results[idx] = fmt.Sprintf("Processed: %s", u)
		}(i, url)
	}
	
	wg.Wait()
	return results
}

// Pattern 2: Fan-out with results channel (better for larger datasets)
func (ffo *FanInFanOut) FanOutWithChannels(urls []string, workers int) []string {
	// Input channel
	input := make(chan string, len(urls))
	
	// Output channel
	output := make(chan string, len(urls))
	
	// Start workers
	var wg sync.WaitGroup
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for url := range input {
				// Simulate processing
				time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
				result := fmt.Sprintf("Worker %d: Processed %s", workerID, url)
				output <- result
			}
		}(i)
	}
	
	// Send all URLs to input channel
	for _, url := range urls {
		input <- url
	}
	close(input) // Important: close input channel to signal workers to stop
	
	// Wait for all workers to finish
	wg.Wait()
	close(output)
	
	// Collect results
	var results []string
	for result := range output {
		results = append(results, result)
	}
	
	return results
}

// Pattern 3: Fan-in pattern (merge multiple channels into one)
func (ffo *FanInFanOut) FanIn(channels ...<-chan int) <-chan int {
	var wg sync.WaitGroup
	merged := make(chan int)
	
	// Start a goroutine for each input channel
	output := func(c <-chan int) {
		defer wg.Done()
		for n := range c {
			merged <- n
		}
	}
	
	wg.Add(len(channels))
	for _, c := range channels {
		go output(c)
	}
	
	// Close merged channel when all inputs are closed
	go func() {
		wg.Wait()
		close(merged)
	}()
	
	return merged
}

// Pattern 4: Dynamic Fan-in/Fan-out with error handling
func (ffo *FanInFanOut) ProcessURLsConcurrently(urls []string, maxWorkers int) []Result {
	// Validate inputs
	if maxWorkers <= 0 {
		maxWorkers = runtime.NumCPU()
	}
	
	// Create buffered channels
	jobs := make(chan Job, len(urls))
	results := make(chan Result, len(urls))
	errors := make(chan error, len(urls))
	
	// Start worker pool
	var wg sync.WaitGroup
	for i := 0; i < maxWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			ffo.worker(workerID, jobs, results, errors)
		}(i)
	}
	
	// Send jobs
	for i, url := range urls {
		jobs <- Job{ID: i, URL: url}
	}
	close(jobs)
	
	// Wait for all workers to complete
	wg.Wait()
	close(results)
	close(errors)
	
	// Collect results and errors
	var allResults []Result
	for result := range results {
		allResults = append(allResults, result)
	}
	
	// Handle errors
	for err := range errors {
		log.Printf("Processing error: %v", err)
	}
	
	return allResults
}

func (ffo *FanInFanOut) worker(id int, jobs <-chan Job, results chan<- Result, errChan chan<- error) {
	for job := range jobs {
		// Process job with timeout
		ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
		result, err := ffo.processJob(ctx, job)
		cancel()
		
		if err != nil {
			errChan <- fmt.Errorf("worker %d: job %d failed: %w", id, job.ID, err)
			continue
		}
		
		results <- result
	}
}

func (ffo *FanInFanOut) processJob(ctx context.Context, job Job) (Result, error) {
	select {
	case <-ctx.Done():
		return Result{}, ctx.Err()
	default:
		// Simulate processing
		time.Sleep(time.Duration(rand.Intn(150)) * time.Millisecond)
		
		// Simulate occasional failure
		if rand.Float32() < 0.1 {
			return Result{}, errors.New("random processing failure")
		}
		
		return Result{
			JobID:   job.ID,
			Content: fmt.Sprintf("Processed: %s", job.URL),
		}, nil
	}
}

type Job struct {
	ID  int
	URL string
}

type Result struct {
	JobID   int
	Content string
}

// ============================================================================
// 2. WORKER POOLS - Controlled Concurrency
// ============================================================================

type WorkerPool struct {
	workers   int
	jobs      chan Job
	results   chan Result
	wg        sync.WaitGroup
	errors    chan error
	ctx       context.Context
	cancel    context.CancelFunc
	completed int64
	failed    int64
}

// Pattern 1: Fixed-size worker pool with graceful shutdown
func NewWorkerPool(workers int, bufferSize int) *WorkerPool {
	if workers <= 0 {
		workers = runtime.NumCPU()
	}
	
	ctx, cancel := context.WithCancel(context.Background())
	
	return &WorkerPool{
		workers: workers,
		jobs:    make(chan Job, bufferSize),
		results: make(chan Result, bufferSize),
		errors:  make(chan error, bufferSize),
		ctx:     ctx,
		cancel:  cancel,
	}
}

func (wp *WorkerPool) Start() {
	for i := 0; i < wp.workers; i++ {
		wp.wg.Add(1)
		go wp.worker(i)
	}
	
	// Start error collector
	go wp.collectErrors()
}

func (wp *WorkerPool) worker(id int) {
	defer wp.wg.Done()
	
	for {
		select {
		case <-wp.ctx.Done():
			return
		case job, ok := <-wp.jobs:
			if !ok {
				return
			}
			
			// Process job with timeout
			ctx, cancel := context.WithTimeout(wp.ctx, 5*time.Second)
			result, err := wp.processJob(ctx, job)
			cancel()
			
			if err != nil {
				atomic.AddInt64(&wp.failed, 1)
				wp.errors <- fmt.Errorf("worker %d: job %d failed: %w", id, job.ID, err)
				continue
			}
			
			atomic.AddInt64(&wp.completed, 1)
			wp.results <- result
		}
	}
}

func (wp *WorkerPool) processJob(ctx context.Context, job Job) (Result, error) {
	// Simulate work
	select {
	case <-ctx.Done():
		return Result{}, ctx.Err()
	case <-time.After(time.Duration(rand.Intn(200)) * time.Millisecond):
		return Result{
			JobID:   job.ID,
			Content: fmt.Sprintf("Worker processed job %d", job.ID),
		}, nil
	}
}

func (wp *WorkerPool) Submit(job Job) error {
	select {
	case <-wp.ctx.Done():
		return errors.New("worker pool stopped")
	case wp.jobs <- job:
		return nil
	}
}

func (wp *WorkerPool) Results() <-chan Result {
	return wp.results
}

func (wp *WorkerPool) Errors() <-chan error {
	return wp.errors
}

func (wp *WorkerPool) Stats() (completed, failed int64) {
	return atomic.LoadInt64(&wp.completed), atomic.LoadInt64(&wp.failed)
}

func (wp *WorkerPool) Stop() {
	wp.cancel()        // Signal workers to stop
	close(wp.jobs)     // Close jobs channel
	wp.wg.Wait()       // Wait for all workers to finish
	close(wp.results)  // Close results channel
	close(wp.errors)   // Close errors channel
}

func (wp *WorkerPool) collectErrors() {
	for err := range wp.errors {
		// In production: log to monitoring system
		log.Printf("Worker pool error: %v", err)
	}
}

// Pattern 2: Worker pool with priority queue
type PriorityWorkerPool struct {
	highPriority chan Job
	normalPriority chan Job
	results       chan Result
	workers       int
	wg            sync.WaitGroup
}

func NewPriorityWorkerPool(workers int) *PriorityWorkerPool {
	return &PriorityWorkerPool{
		highPriority:   make(chan Job, 100),
		normalPriority: make(chan Job, 1000),
		results:        make(chan Result, 1100),
		workers:        workers,
	}
}

func (pwp *PriorityWorkerPool) Start() {
	for i := 0; i < pwp.workers; i++ {
		pwp.wg.Add(1)
		go pwp.priorityWorker(i)
	}
}

func (pwp *PriorityWorkerPool) priorityWorker(id int) {
	defer pwp.wg.Done()
	
	for {
		select {
		case job := <-pwp.highPriority:
			// Process high priority job first
			result := pwp.processWithPriority(job, "high")
			pwp.results <- result
		default:
			// If no high priority jobs, check normal priority
			select {
			case job := <-pwp.highPriority:
				result := pwp.processWithPriority(job, "high")
				pwp.results <- result
			case job := <-pwp.normalPriority:
				result := pwp.processWithPriority(job, "normal")
				pwp.results <- result
			case <-time.After(100 * time.Millisecond):
				// No jobs, worker can exit if pool is stopping
				return
			}
		}
	}
}

func (pwp *PriorityWorkerPool) processWithPriority(job Job, priority string) Result {
	time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
	return Result{
		JobID:   job.ID,
		Content: fmt.Sprintf("%s priority job %d processed", priority, job.ID),
	}
}

// Pattern 3: Worker pool with dynamic scaling
type DynamicWorkerPool struct {
	minWorkers   int
	maxWorkers   int
	jobs         chan Job
	results      chan Result
	workerCount  int32
	idleWorkers  int32
	scaleUp      chan struct{}
	scaleDown    chan struct{}
	quit         chan struct{}
	wg           sync.WaitGroup
}

func NewDynamicWorkerPool(min, max int, queueSize int) *DynamicWorkerPool {
	if min <= 0 {
		min = 1
	}
	if max < min {
		max = min * 2
	}
	
	pool := &DynamicWorkerPool{
		minWorkers:  min,
		maxWorkers:  max,
		jobs:        make(chan Job, queueSize),
		results:     make(chan Result, queueSize),
		scaleUp:     make(chan struct{}, 1),
		scaleDown:   make(chan struct{}, 1),
		quit:        make(chan struct{}),
	}
	
	// Start with minimum workers
	for i := 0; i < min; i++ {
		pool.addWorker()
	}
	
	// Start autoscaler
	go pool.autoscale()
	
	return pool
}

func (dwp *DynamicWorkerPool) addWorker() {
	atomic.AddInt32(&dwp.workerCount, 1)
	dwp.wg.Add(1)
	
	go func() {
		defer dwp.wg.Done()
		defer atomic.AddInt32(&dwp.workerCount, -1)
		
		idle := true
		
		for {
			select {
			case <-dwp.quit:
				return
			case job, ok := <-dwp.jobs:
				if !ok {
					return
				}
				
				idle = false
				atomic.AddInt32(&dwp.idleWorkers, -1)
				
				// Process job
				result := dwp.processJob(job)
				dwp.results <- result
				
				idle = true
				atomic.AddInt32(&dwp.idleWorkers, 1)
				
				// Check if we should scale down
				if atomic.LoadInt32(&dwp.idleWorkers) > int32(dwp.minWorkers) {
					select {
					case dwp.scaleDown <- struct{}{}:
					default:
					}
				}
			}
		}
	}()
}

func (dwp *DynamicWorkerPool) autoscale() {
	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()
	
	for {
		select {
		case <-dwp.quit:
			return
		case <-dwp.scaleUp:
			current := atomic.LoadInt32(&dwp.workerCount)
			if current < int32(dwp.maxWorkers) {
				dwp.addWorker()
			}
		case <-dwp.scaleDown:
			current := atomic.LoadInt32(&dwp.workerCount)
			idle := atomic.LoadInt32(&dwp.idleWorkers)
			
			// Scale down if we have more idle workers than needed
			if current > int32(dwp.minWorkers) && idle > int32(dwp.minWorkers) {
				// Signal one worker to exit by closing jobs channel?
				// In real implementation, you'd need a better strategy
			}
		case <-ticker.C:
			// Check if we need to scale based on queue length
			queueLen := len(dwp.jobs)
			currentWorkers := atomic.LoadInt32(&dwp.workerCount)
			
			if queueLen > int(currentWorkers)*10 && currentWorkers < int32(dwp.maxWorkers) {
				select {
				case dwp.scaleUp <- struct{}{}:
				default:
				}
			}
		}
	}
}

func (dwp *DynamicWorkerPool) processJob(job Job) Result {
	time.Sleep(time.Duration(rand.Intn(200)) * time.Millisecond)
	return Result{
		JobID:   job.ID,
		Content: fmt.Sprintf("Dynamic worker processed job %d", job.ID),
	}
}

func (dwp *DynamicWorkerPool) Submit(job Job) error {
	select {
	case <-dwp.quit:
		return errors.New("pool stopped")
	case dwp.jobs <- job:
		// Check if we need to scale up
		if len(dwp.jobs) > int(atomic.LoadInt32(&dwp.workerCount))*5 {
			select {
			case dwp.scaleUp <- struct{}{}:
			default:
			}
		}
		return nil
	}
}

// ============================================================================
// 3. PIPELINE PATTERN - Processing Stages
// ============================================================================

type Pipeline struct{}

func (p *Pipeline) Demonstrate() {
	fmt.Println("=== Pipeline Pattern ===")
	
	// Three-stage pipeline: Generate -> Process -> Store
	numbers := p.Generate(1, 10)
	squared := p.Square(numbers)
	result := p.Collect(squared)
	
	fmt.Printf("Pipeline result: %v\n", result)
}

// Pattern 1: Simple pipeline
func (p *Pipeline) Generate(start, end int) <-chan int {
	out := make(chan int)
	
	go func() {
		defer close(out)
		for i := start; i <= end; i++ {
			out <- i
		}
	}()
	
	return out
}

func (p *Pipeline) Square(in <-chan int) <-chan int {
	out := make(chan int)
	
	go func() {
		defer close(out)
		for n := range in {
			time.Sleep(50 * time.Millisecond) // Simulate work
			out <- n * n
		}
	}()
	
	return out
}

func (p *Pipeline) Collect(in <-chan int) []int {
	var result []int
	for n := range in {
		result = append(result, n)
	}
	return result
}

// Pattern 2: Generic pipeline with stages
type Stage func(<-chan interface{}) <-chan interface{}

func (p *Pipeline) Pipeline(input <-chan interface{}, stages ...Stage) <-chan interface{} {
	var output <-chan interface{} = input
	
	for _, stage := range stages {
		output = stage(output)
	}
	
	return output
}

// Example stages
func FilterStage(predicate func(interface{}) bool) Stage {
	return func(in <-chan interface{}) <-chan interface{} {
		out := make(chan interface{})
		
		go func() {
			defer close(out)
			for item := range in {
				if predicate(item) {
					out <- item
				}
			}
		}()
		
		return out
	}
}

func TransformStage(transform func(interface{}) interface{}) Stage {
	return func(in <-chan interface{}) <-chan interface{} {
		out := make(chan interface{})
		
		go func() {
			defer close(out)
			for item := range in {
				out <- transform(item)
			}
		}()
		
		return out
	}
}

// Pattern 3: Pipeline with error handling
type PipelineWithErrors struct{}

func (pwe *PipelineWithErrors) ProcessPipeline() {
	// Create pipeline stages
	gen := pwe.GenerateWithErrors(1, 10)
	processed := pwe.ProcessWithErrors(gen)
	results, errors := pwe.CollectWithErrors(processed)
	
	// Handle results and errors
	for {
		select {
		case result, ok := <-results:
			if !ok {
				results = nil
			} else {
				fmt.Printf("Result: %v\n", result)
			}
		case err, ok := <-errors:
			if !ok {
				errors = nil
			} else {
				fmt.Printf("Error: %v\n", err)
			}
		}
		
		if results == nil && errors == nil {
			break
		}
	}
}

func (pwe *PipelineWithErrors) GenerateWithErrors(start, end int) <-chan interface{} {
	out := make(chan interface{})
	
	go func() {
		defer close(out)
		for i := start; i <= end; i++ {
			// Simulate occasional error
			if i == 5 {
				out <- errors.New("generation error at 5")
				continue
			}
			out <- i
		}
	}()
	
	return out
}

func (pwe *PipelineWithErrors) ProcessWithErrors(in <-chan interface{}) <-chan interface{} {
	out := make(chan interface{})
	
	go func() {
		defer close(out)
		for item := range in {
			// If item is an error, pass it through
			if err, ok := item.(error); ok {
				out <- err
				continue
			}
			
			// Process number
			n := item.(int)
			// Simulate processing error
			if n == 7 {
				out <- errors.New("processing error at 7")
				continue
			}
			
			out <- n * 2
		}
	}()
	
	return out
}

func (pwe *PipelineWithErrors) CollectWithErrors(in <-chan interface{}) (<-chan interface{}, <-chan error) {
	results := make(chan interface{})
	errors := make(chan error)
	
	go func() {
		defer close(results)
		defer close(errors)
		
		for item := range in {
			switch v := item.(type) {
			case error:
				errors <- v
			default:
				results <- v
			}
		}
	}()
	
	return results, errors
}

// Pattern 4: Bounded pipeline (limited parallelism per stage)
type BoundedPipeline struct {
	concurrency int
}

func NewBoundedPipeline(concurrency int) *BoundedPipeline {
	return &BoundedPipeline{concurrency: concurrency}
}

func (bp *BoundedPipeline) Process(data []int) []int {
	// Stage 1: Generate
	stage1 := make(chan int, 100)
	go func() {
		defer close(stage1)
		for _, n := range data {
			stage1 <- n
		}
	}()
	
	// Stage 2: Process with bounded concurrency
	stage2 := bp.boundedStage(stage1, bp.processItem, bp.concurrency)
	
	// Stage 3: Collect
	var results []int
	for result := range stage2 {
		results = append(results, result)
	}
	
	return results
}

func (bp *BoundedPipeline) boundedStage(in <-chan int, process func(int) int, workers int) <-chan int {
	out := make(chan int)
	var wg sync.WaitGroup
	
	// Start workers
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for item := range in {
				result := process(item)
				out <- result
			}
		}()
	}
	
	// Close output when all workers are done
	go func() {
		wg.Wait()
		close(out)
	}()
	
	return out
}

func (bp *BoundedPipeline) processItem(n int) int {
	time.Sleep(100 * time.Millisecond)
	return n * n
}

// ============================================================================
// 4. PRODUCER-CONSUMER PATTERNS
// ============================================================================

type ProducerConsumer struct{}

func (pc *ProducerConsumer) Demonstrate() {
	fmt.Println("=== Producer-Consumer Patterns ===")
	
	// Pattern 1: Single producer, single consumer
	pc.SingleProducerSingleConsumer()
	
	// Pattern 2: Multiple producers, multiple consumers
	pc.MultipleProducersConsumers()
	
	// Pattern 3: Producer with rate limiting
	pc.RateLimitedProducer()
}

// Pattern 1: Single producer, single consumer
func (pc *ProducerConsumer) SingleProducerSingleConsumer() {
	ch := make(chan int, 10)
	done := make(chan struct{})
	
	// Producer
	go func() {
		defer close(ch)
		for i := 0; i < 10; i++ {
			ch <- i
			time.Sleep(50 * time.Millisecond)
		}
	}()
	
	// Consumer
	go func() {
		defer close(done)
		for n := range ch {
			fmt.Printf("Consumed: %d\n", n)
			time.Sleep(100 * time.Millisecond)
		}
	}()
	
	<-done
}

// Pattern 2: Multiple producers, multiple consumers
func (pc *ProducerConsumer) MultipleProducersConsumers() {
	data := make(chan int, 100)
	done := make(chan struct{})
	
	// Start multiple producers
	var wgProducers sync.WaitGroup
	for i := 0; i < 3; i++ {
		wgProducers.Add(1)
		go func(producerID int) {
			defer wgProducers.Done()
			for j := 0; j < 5; j++ {
				value := producerID*100 + j
				data <- value
				fmt.Printf("Producer %d produced: %d\n", producerID, value)
				time.Sleep(time.Duration(rand.Intn(50)) * time.Millisecond)
			}
		}(i)
	}
	
	// Close data channel when all producers are done
	go func() {
		wgProducers.Wait()
		close(data)
	}()
	
	// Start multiple consumers
	var wgConsumers sync.WaitGroup
	for i := 0; i < 2; i++ {
		wgConsumers.Add(1)
		go func(consumerID int) {
			defer wgConsumers.Done()
			for value := range data {
				fmt.Printf("Consumer %d consumed: %d\n", consumerID, value)
				time.Sleep(time.Duration(rand.Intn(100)) * time.Millisecond)
			}
		}(i)
	}
	
	// Signal when all consumers are done
	go func() {
		wgConsumers.Wait()
		close(done)
	}()
	
	<-done
}

// Pattern 3: Producer with rate limiting
func (pc *ProducerConsumer) RateLimitedProducer() {
	ch := make(chan int, 20)
	done := make(chan struct{})
	
	// Rate limiter: 10 items per second
	limiter := time.NewTicker(100 * time.Millisecond)
	defer limiter.Stop()
	
	// Producer with rate limiting
	go func() {
		defer close(ch)
		for i := 0; i < 20; i++ {
			<-limiter.C // Wait for rate limiter
			ch <- i
			fmt.Printf("Produced (rate-limited): %d\n", i)
		}
	}()
	
	// Consumer
	go func() {
		defer close(done)
		for n := range ch {
			fmt.Printf("Consumed: %d\n", n)
		}
	}()
	
	<-done
}

// Pattern 4: Producer-consumer with poison pill
func (pc *ProducerConsumer) WithPoisonPill() {
	ch := make(chan interface{}, 10)
	done := make(chan struct{})
	
	// Producer
	go func() {
		for i := 0; i < 15; i++ {
			ch <- i
		}
		// Send poison pill
		ch <- "POISON_PILL"
		close(ch)
	}()
	
	// Consumer
	go func() {
		defer close(done)
		for item := range ch {
			if item == "POISON_PILL" {
				fmt.Println("Received poison pill, stopping...")
				break
			}
			fmt.Printf("Consumed: %v\n", item)
		}
	}()
	
	<-done
}

// Pattern 5: Producer-consumer with graceful shutdown
type ProducerConsumerSystem struct {
	producerStop chan struct{}
	consumerStop chan struct{}
	data         chan interface{}
	wg           sync.WaitGroup
}

func NewProducerConsumerSystem(bufferSize int) *ProducerConsumerSystem {
	return &ProducerConsumerSystem{
		producerStop: make(chan struct{}),
		consumerStop: make(chan struct{}),
		data:         make(chan interface{}, bufferSize),
	}
}

func (pcs *ProducerConsumerSystem) StartProducers(numProducers int) {
	for i := 0; i < numProducers; i++ {
		pcs.wg.Add(1)
		go pcs.producer(i)
	}
}

func (pcs *ProducerConsumerSystem) StartConsumers(numConsumers int) {
	for i := 0; i < numConsumers; i++ {
		pcs.wg.Add(1)
		go pcs.consumer(i)
	}
}

func (pcs *ProducerConsumerSystem) producer(id int) {
	defer pcs.wg.Done()
	
	for {
		select {
		case <-pcs.producerStop:
			fmt.Printf("Producer %d stopping\n", id)
			return
		default:
			// Produce data
			data := fmt.Sprintf("data from producer %d", id)
			select {
			case pcs.data <- data:
				// Successfully sent
				time.Sleep(100 * time.Millisecond)
			case <-time.After(50 * time.Millisecond):
				// Buffer full, try again
			}
		}
	}
}

func (pcs *ProducerConsumerSystem) consumer(id int) {
	defer pcs.wg.Done()
	
	for {
		select {
		case <-pcs.consumerStop:
			fmt.Printf("Consumer %d stopping\n", id)
			return
		case data, ok := <-pcs.data:
			if !ok {
				return
			}
			fmt.Printf("Consumer %d received: %s\n", id, data)
			time.Sleep(150 * time.Millisecond)
		}
	}
}

func (pcs *ProducerConsumerSystem) Stop() {
	// Stop producers first
	close(pcs.producerStop)
	
	// Wait a bit for producers to stop producing
	time.Sleep(200 * time.Millisecond)
	
	// Stop consumers
	close(pcs.consumerStop)
	
	// Wait for all goroutines to finish
	pcs.wg.Wait()
	
	// Close data channel
	close(pcs.data)
}

// ============================================================================
// 5. ERROR HANDLING IN CONCURRENT CODE
// ============================================================================

type ConcurrentErrorHandling struct{}

func (ceh *ConcurrentErrorHandling) Demonstrate() {
	fmt.Println("=== Error Handling in Concurrent Code ===")
	
	// Pattern 1: Error channel
	ceh.ErrorChannelPattern()
	
	// Pattern 2: Result with error
	ceh.ResultWithErrorPattern()
	
	// Pattern 3: Error group
	ceh.ErrorGroupPattern()
	
	// Pattern 4: Panic recovery in goroutines
	ceh.PanicRecovery()
}

// Pattern 1: Error channel
func (ceh *ConcurrentErrorHandling) ErrorChannelPattern() {
	workers := 3
	jobs := make(chan int, 10)
	results := make(chan string, 10)
	errors := make(chan error, 10)
	done := make(chan struct{})
	
	var wg sync.WaitGroup
	
	// Start workers
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()
			for job := range jobs {
				result, err := ceh.processJob(job)
				if err != nil {
					errors <- fmt.Errorf("worker %d: %w", workerID, err)
					continue
				}
				results <- result
			}
		}(i)
	}
	
	// Send jobs
	go func() {
		for i := 0; i < 10; i++ {
			jobs <- i
		}
		close(jobs)
	}()
	
	// Wait and collect
	go func() {
		wg.Wait()
		close(results)
		close(errors)
		close(done)
	}()
	
	// Process results and errors
	<-done
	
	// Drain results
	for result := range results {
		fmt.Printf("Result: %s\n", result)
	}
	
	// Drain errors
	for err := range errors {
		fmt.Printf("Error: %v\n", err)
	}
}

func (ceh *ConcurrentErrorHandling) processJob(job int) (string, error) {
	// Simulate occasional error
	if job%3 == 0 {
		return "", fmt.Errorf("job %d failed", job)
	}
	
	time.Sleep(50 * time.Millisecond)
	return fmt.Sprintf("processed job %d", job), nil
}

// Pattern 2: Result with error struct
type ResultOrError struct {
	Result string
	Error  error
}

func (ceh *ConcurrentErrorHandling) ResultWithErrorPattern() {
	workers := 2
	jobs := make(chan int, 5)
	results := make(chan ResultOrError, 5)
	
	var wg sync.WaitGroup
	
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for job := range jobs {
				result, err := ceh.processJob(job)
				results <- ResultOrError{Result: result, Error: err}
			}
		}()
	}
	
	// Send jobs
	for i := 0; i < 5; i++ {
		jobs <- i
	}
	close(jobs)
	
	// Wait and close
	go func() {
		wg.Wait()
		close(results)
	}()
	
	// Process results
	for roe := range results {
		if roe.Error != nil {
			fmt.Printf("Error: %v\n", roe.Error)
			continue
		}
		fmt.Printf("Success: %s\n", roe.Result)
	}
}

// Pattern 3: Using errgroup for coordinated error handling
import "golang.org/x/sync/errgroup"

func (ceh *ConcurrentErrorHandling) ErrorGroupPattern() {
	var g errgroup.Group
	
	// Run multiple operations
	for i := 0; i < 3; i++ {
		i := i // Capture loop variable
		g.Go(func() error {
			return ceh.operation(i)
		})
	}
	
	// Wait for all operations to complete
	if err := g.Wait(); err != nil {
		fmt.Printf("One or more operations failed: %v\n", err)
	} else {
		fmt.Println("All operations completed successfully")
	}
}

func (ceh *ConcurrentErrorHandling) operation(id int) error {
	// Simulate work with occasional failure
	if id == 1 {
		return fmt.Errorf("operation %d failed", id)
	}
	
	time.Sleep(100 * time.Millisecond)
	fmt.Printf("Operation %d completed\n", id)
	return nil
}

// Pattern 4: Panic recovery in goroutines
func (ceh *ConcurrentErrorHandling) PanicRecovery() {
	var wg sync.WaitGroup
	errors := make(chan error, 5)
	
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			
			// Recover from panic
			defer func() {
				if r := recover(); r != nil {
					errors <- fmt.Errorf("goroutine %d panicked: %v", id, r)
				}
			}()
			
			// Simulate work that might panic
			ceh.workThatMightPanic(id)
		}(i)
	}
	
	wg.Wait()
	close(errors)
	
	// Check for panics
	for err := range errors {
		fmt.Printf("Recovered from panic: %v\n", err)
	}
}

func (ceh *ConcurrentErrorHandling) workThatMightPanic(id int) {
	// Simulate panic
	if id == 2 {
		panic(fmt.Sprintf("intentional panic in worker %d", id))
	}
	
	time.Sleep(50 * time.Millisecond)
	fmt.Printf("Worker %d completed normally\n", id)
}

// Pattern 5: Timeout and cancellation with error propagation
func (ceh *ConcurrentErrorHandling) WithTimeout() error {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()
	
	results := make(chan string, 1)
	errors := make(chan error, 1)
	
	go func() {
		// Simulate work that might fail
		result, err := ceh.longRunningOperation()
		if err != nil {
			errors <- err
			return
		}
		results <- result
	}()
	
	select {
	case <-ctx.Done():
		return fmt.Errorf("operation timed out: %w", ctx.Err())
	case err := <-errors:
		return fmt.Errorf("operation failed: %w", err)
	case result := <-results:
		fmt.Printf("Operation succeeded: %s\n", result)
		return nil
	}
}

func (ceh *ConcurrentErrorHandling) longRunningOperation() (string, error) {
	// Simulate long operation
	time.Sleep(2 * time.Second)
	return "result", nil
}

// Pattern 6: Retry with exponential backoff in concurrent code
type RetryableOperation struct {
	maxRetries int
	backoff    time.Duration
}

func NewRetryableOperation(maxRetries int, initialBackoff time.Duration) *RetryableOperation {
	return &RetryableOperation{
		maxRetries: maxRetries,
		backoff:    initialBackoff,
	}
}

func (ro *RetryableOperation) Execute(operation func() error) error {
	var lastErr error
	
	for i := 0; i < ro.maxRetries; i++ {
		err := operation()
		if err == nil {
			return nil
		}
		
		lastErr = err
		
		// Check if error is retryable
		if !ro.isRetryableError(err) {
			return err
		}
		
		// Wait before retry
		if i < ro.maxRetries-1 {
			time.Sleep(ro.backoff * time.Duration(1<<uint(i))) // Exponential backoff
		}
	}
	
	return fmt.Errorf("max retries exceeded: %w", lastErr)
}

func (ro *RetryableOperation) isRetryableError(err error) bool {
	// Define what errors are retryable
	return true // Simplified for example
}

// ============================================================================
// COMPREHENSIVE EXAMPLE: Image Processing Pipeline
// ============================================================================

type ImageProcessingPipeline struct {
	downloadQueue   chan string
	resizeQueue     chan Image
	filterQueue     chan Image
	uploadQueue     chan Image
	results         chan Result
	errors          chan error
	downloadWorkers int
	resizeWorkers   int
	filterWorkers   int
	uploadWorkers   int
}

type Image struct {
	ID       string
	URL      string
	Data     []byte
	Metadata map[string]string
}

func NewImageProcessingPipeline() *ImageProcessingPipeline {
	return &ImageProcessingPipeline{
		downloadQueue:   make(chan string, 100),
		resizeQueue:     make(chan Image, 100),
		filterQueue:     make(chan Image, 100),
		uploadQueue:     make(chan Image, 100),
		results:         make(chan Result, 100),
		errors:          make(chan error, 100),
		downloadWorkers: 5,
		resizeWorkers:   3,
		filterWorkers:   2,
		uploadWorkers:   2,
	}
}

func (ipp *ImageProcessingPipeline) Start() {
	// Start download workers
	for i := 0; i < ipp.downloadWorkers; i++ {
		go ipp.downloadWorker(i)
	}
	
	// Start resize workers
	for i := 0; i < ipp.resizeWorkers; i++ {
		go ipp.resizeWorker(i)
	}
	
	// Start filter workers
	for i := 0; i < ipp.filterWorkers; i++ {
		go ipp.filterWorker(i)
	}
	
	// Start upload workers
	for i := 0; i < ipp.uploadWorkers; i++ {
		go ipp.uploadWorker(i)
	}
	
	// Start error handler
	go ipp.errorHandler()
}

func (ipp *ImageProcessingPipeline) ProcessImage(url string) {
	ipp.downloadQueue <- url
}

func (ipp *ImageProcessingPipeline) downloadWorker(id int) {
	for url := range ipp.downloadQueue {
		image, err := ipp.downloadImage(url)
		if err != nil {
			ipp.errors <- fmt.Errorf("download worker %d: %w", id, err)
			continue
		}
		
		ipp.resizeQueue <- image
	}
}

func (ipp *ImageProcessingPipeline) resizeWorker(id int) {
	for image := range ipp.resizeQueue {
		resized, err := ipp.resizeImage(image)
		if err != nil {
			ipp.errors <- fmt.Errorf("resize worker %d: %w", id, err)
			continue
		}
		
		ipp.filterQueue <- resized
	}
}

func (ipp *ImageProcessingPipeline) filterWorker(id int) {
	for image := range ipp.filterQueue {
		filtered, err := ipp.applyFilter(image)
		if err != nil {
			ipp.errors <- fmt.Errorf("filter worker %d: %w", id, err)
			continue
		}
		
		ipp.uploadQueue <- filtered
	}
}

func (ipp *ImageProcessingPipeline) uploadWorker(id int) {
	for image := range ipp.uploadQueue {
		result, err := ipp.uploadImage(image)
		if err != nil {
			ipp.errors <- fmt.Errorf("upload worker %d: %w", id, err)
			continue
		}
		
		ipp.results <- result
	}
}

func (ipp *ImageProcessingPipeline) errorHandler() {
	for err := range ipp.errors {
		// Log error, send to monitoring, etc.
		log.Printf("Image processing error: %v", err)
	}
}

func (ipp *ImageProcessingPipeline) downloadImage(url string) (Image, error) {
	// Simulate download
	time.Sleep(100 * time.Millisecond)
	return Image{
		ID:       generateID(),
		URL:      url,
		Data:     []byte("fake image data"),
		Metadata: map[string]string{"source": url},
	}, nil
}

func (ipp *ImageProcessingPipeline) resizeImage(img Image) (Image, error) {
	// Simulate resize
	time.Sleep(150 * time.Millisecond)
	img.Metadata["resized"] = "true"
	return img, nil
}

func (ipp *ImageProcessingPipeline) applyFilter(img Image) (Image, error) {
	// Simulate filter application
	time.Sleep(200 * time.Millisecond)
	img.Metadata["filtered"] = "true"
	return img, nil
}

func (ipp *ImageProcessingPipeline) uploadImage(img Image) (Result, error) {
	// Simulate upload
	time.Sleep(100 * time.Millisecond)
	return Result{
		JobID:   0, // Would be actual job ID
		Content: fmt.Sprintf("Uploaded image %s", img.ID),
	}, nil
}

// ============================================================================
// MAIN FUNCTION - DEMONSTRATION
// ============================================================================

func main() {
	fmt.Println("=== Go Concurrency Patterns ===")
	
	// 1. Fan-in/Fan-out
	ffo := &FanInFanOut{}
	ffo.Demonstrate()
	
	// 2. Worker Pools
	fmt.Println("\n--- Worker Pool Example ---")
	wp := NewWorkerPool(3, 10)
	wp.Start()
	
	// Submit jobs
	for i := 0; i < 10; i++ {
		wp.Submit(Job{ID: i, URL: fmt.Sprintf("job-%d", i)})
	}
	
	// Collect results
	go func() {
		for result := range wp.Results() {
			fmt.Printf("Result: %v\n", result.Content)
		}
	}()
	
	// Wait a bit, then stop
	time.Sleep(1 * time.Second)
	wp.Stop()
	
	completed, failed := wp.Stats()
	fmt.Printf("Worker pool stats: completed=%d, failed=%d\n", completed, failed)
	
	// 3. Pipeline Pattern
	fmt.Println("\n--- Pipeline Example ---")
	pipeline := &Pipeline{}
	pipeline.Demonstrate()
	
	// 4. Producer-Consumer
	fmt.Println("\n--- Producer-Consumer Example ---")
	pc := &ProducerConsumer{}
	pc.MultipleProducersConsumers()
	
	// 5. Error Handling
	fmt.Println("\n--- Error Handling Example ---")
	ceh := &ConcurrentErrorHandling{}
	ceh.ErrorGroupPattern()
	
	// 6. Comprehensive Example
	fmt.Println("\n--- Image Processing Pipeline ---")
	ipp := NewImageProcessingPipeline()
	ipp.Start()
	
	// Process some images
	for i := 0; i < 5; i++ {
		url := fmt.Sprintf("https://example.com/image%d.jpg", i)
		ipp.ProcessImage(url)
	}
	
	// Wait for processing
	time.Sleep(2 * time.Second)
	
	fmt.Println("\n=== Key Takeaways ===")
	fmt.Println("1. Fan-out distributes work, fan-in collects results")
	fmt.Println("2. Worker pools control concurrency and resource usage")
	fmt.Println("3. Pipelines organize processing into stages")
	fmt.Println("4. Producer-consumer patterns decouple producers and consumers")
	fmt.Println("5. Always handle errors in goroutines - don't let them panic silently")
	fmt.Println("6. Use context for cancellation and timeouts")
	fmt.Println("7. Recover from panics in goroutines")
	fmt.Println("8. Use wait groups to coordinate goroutines")
	fmt.Println("9. Buffered channels can prevent deadlocks")
	fmt.Println("10. Monitor goroutine counts and channel capacities")
	
	// Prevent immediate exit
	time.Sleep(500 * time.Millisecond)
}

func generateID() string {
	return fmt.Sprintf("id_%d", time.Now().UnixNano())
}

// Additional best practices:
// 1. Always use defer wg.Done()
// 2. Close channels from the producer side
// 3. Use select with default for non-blocking operations
// 4. Set GOMAXPROCS for CPU-bound work
// 5. Use sync.Pool for heavy object allocation
// 6. Avoid goroutine leaks with proper shutdown
// 7. Use atomic operations for counters
// 8. Prefer channels over mutexes for coordination
// 9. Use sync.Once for initialization
// 10. Profile with pprof to find bottlenecks