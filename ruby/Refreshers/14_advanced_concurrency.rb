# ============================================
# RUBY ADVANCED CONCURRENCY AND PARALLELISM
# ============================================

puts "=" * 60
puts "RUBY ADVANCED CONCURRENCY - THREADS, RACTORS, AND ASYNC"
puts "=" * 60

# ============================================
# 1. UNDERSTANDING THE GIL/GVL
# ============================================

puts "\n" + "=" * 40
puts "1. THE GLOBAL VM LOCK (GVL/GIL)"
puts "=" * 40

puts <<~GVL_EXPLANATION

  GVL (GLOBAL VM LOCK) / GIL (GLOBAL INTERPRETER LOCK):
  
  WHAT IT IS:
  • A mutex that protects Ruby's internal data structures
  • Prevents multiple threads from executing Ruby code simultaneously
  • Only ONE thread can execute Ruby code at a time per process
  
  IMPLICATIONS:
  • CPU-bound operations won't benefit from multi-threading
  • I/O-bound operations CAN benefit (GVL released during I/O)
  • True parallelism requires multiple processes, not threads
  
  WHY IT EXISTS:
  • Simplifies C extension development
  • Protects Ruby's garbage collector
  • Maintains memory consistency
  
  I/O-BOUND vs CPU-BOUND:
  ✓ I/O-bound (network, disk): Use threads (GVL released during I/O)
  ✗ CPU-bound (calculations): Use processes or Ractors
  
  Ruby 3.0+ introduces Ractors for true parallelism!

GVL_EXPLANATION

# ============================================
# 2. THREADS BASICS REVIEW
# ============================================

puts "\n" + "=" * 40
puts "2. THREAD BASICS"
puts "=" * 40

# Creating threads
thread1 = Thread.new do
  3.times do |i|
    puts "Thread 1: #{i}"
    sleep 0.1
  end
end

thread2 = Thread.new do
  3.times do |i|
    puts "Thread 2: #{i}"
    sleep 0.1
  end
end

# Wait for threads to complete
thread1.join
thread2.join

puts "\n--- Thread with parameters ---"

# Thread with parameters
thread = Thread.new("Alice", 30) do |name, age|
  puts "Name: #{name}, Age: #{age}"
end

thread.join

# Thread return value
thread = Thread.new do
  sleep 0.1
  42  # Return value
end

result = thread.value  # Joins and returns value
puts "\nThread result: #{result}"

# ============================================
# 3. THREAD SAFETY AND SYNCHRONIZATION
# ============================================

puts "\n" + "=" * 40
puts "3. THREAD SAFETY"
puts "=" * 40

# Race condition example (UNSAFE)
puts "\n--- Race Condition (Unsafe) ---"

counter = 0
threads = 10.times.map do
  Thread.new do
    100.times { counter += 1 }
  end
end

threads.each(&:join)
puts "Counter (unsafe): #{counter} (expected 1000)"

# Using Mutex for thread safety
puts "\n--- Using Mutex (Safe) ---"

counter = 0
mutex = Mutex.new

threads = 10.times.map do
  Thread.new do
    100.times do
      mutex.synchronize do
        counter += 1
      end
    end
  end
end

threads.each(&:join)
puts "Counter (safe): #{counter}"

# ============================================
# 4. ADVANCED SYNCHRONIZATION PRIMITIVES
# ============================================

puts "\n" + "=" * 40
puts "4. ADVANCED SYNCHRONIZATION"
puts "=" * 40

# ConditionVariable - waiting for conditions
puts "\n--- ConditionVariable ---"

require 'thread'

mutex = Mutex.new
cv = ConditionVariable.new
data = []

producer = Thread.new do
  5.times do |i|
    sleep 0.1
    mutex.synchronize do
      data << i
      puts "Produced: #{i}"
      cv.signal  # Wake up one waiting thread
    end
  end
end

consumer = Thread.new do
  5.times do
    mutex.synchronize do
      while data.empty?
        cv.wait(mutex)  # Release mutex and wait for signal
      end
      item = data.shift
      puts "Consumed: #{item}"
    end
  end
end

producer.join
consumer.join

# Queue - thread-safe data structure
puts "\n--- Thread-Safe Queue ---"

require 'thread'

queue = Queue.new

producer = Thread.new do
  5.times do |i|
    sleep 0.1
    queue << i
    puts "Queued: #{i}"
  end
  queue.close  # Signal no more items
end

consumer = Thread.new do
  while (item = queue.pop)
    puts "Dequeued: #{item}"
  end
rescue ThreadError => e
  puts "Queue closed"
end

producer.join
consumer.join

# ============================================
# 5. THREAD POOLS
# ============================================

puts "\n" + "=" * 40
puts "5. THREAD POOLS"
puts "=" * 40

class SimpleThreadPool
  def initialize(size)
    @size = size
    @queue = Queue.new
    @threads = []
    
    @size.times do
      @threads << Thread.new do
        loop do
          job = @queue.pop
          break if job == :shutdown
          job.call rescue nil
        end
      end
    end
  end
  
  def schedule(&block)
    @queue << block
  end
  
  def shutdown
    @size.times { @queue << :shutdown }
    @threads.each(&:join)
  end
end

# Usage
pool = SimpleThreadPool.new(3)

puts "\n--- Thread Pool Execution ---"

10.times do |i|
  pool.schedule do
    puts "Task #{i} executed by #{Thread.current.object_id}"
    sleep 0.1
  end
end

pool.shutdown
puts "All tasks completed"

# ============================================
# 6. RACTORS - TRUE PARALLELISM (Ruby 3.0+)
# ============================================

puts "\n" + "=" * 40
puts "6. RACTORS - TRUE PARALLELISM"
puts "=" * 40

puts <<~RACTOR_INTRO

  RACTORS (Ruby 3.0+):
  • Actor-like concurrent entities
  • Run in parallel (bypass GVL for Ruby code)
  • Share nothing by default (isolated)
  • Communicate via message passing
  
  KEY CONCEPTS:
  • Each Ractor has its own GVL
  • Objects are either:
    - Copied (frozen)
    - Moved (transferred)
    - Shareable (frozen literals, classes, modules)
  
  USE CASES:
  • CPU-bound parallel processing
  • Data processing pipelines
  • Concurrent algorithms

RACTOR_INTRO

# Basic Ractor example
if RUBY_VERSION >= '3.0.0'
  puts "\n--- Basic Ractor ---"
  
  r = Ractor.new do
    result = 5 * 5
    result  # Returned from Ractor
  end
  
  puts "Ractor result: #{r.take}"  # Receive result
  
  # Ractor with parameters
  r = Ractor.new(10, 20) do |a, b|
    a + b
  end
  
  puts "Ractor sum: #{r.take}"
  
  # Ractor with message passing
  puts "\n--- Ractor Message Passing ---"
  
  worker = Ractor.new do
    loop do
      msg = Ractor.receive  # Block until message received
      break if msg == :stop
      puts "Worker received: #{msg}"
      result = msg * 2
      Ractor.yield result  # Send result back
    end
  end
  
  # Send messages
  worker.send(5)
  puts "Main received: #{worker.take}"
  
  worker.send(10)
  puts "Main received: #{worker.take}"
  
  worker.send(:stop)
  
  # Parallel computation with Ractors
  puts "\n--- Parallel Computation ---"
  
  def parallel_map(array)
    ractors = array.map do |item|
      Ractor.new(item) do |n|
        n * n  # CPU-intensive work
      end
    end
    
    ractors.map(&:take)
  end
  
  numbers = [1, 2, 3, 4, 5]
  results = parallel_map(numbers)
  puts "Parallel map results: #{results}"
  
else
  puts "\nRactors require Ruby 3.0+. Current version: #{RUBY_VERSION}"
end

# ============================================
# 7. FORK-BASED PARALLELISM
# ============================================

puts "\n" + "=" * 40
puts "7. PROCESS FORKING"
puts "=" * 40

puts <<~FORK_EXPLANATION

  PROCESS FORKING:
  • Creates a complete copy of the current process
  • True parallelism (separate memory space)
  • No GVL sharing (each process has its own)
  • Higher memory overhead than threads
  
  WHEN TO USE:
  • CPU-bound tasks needing true parallelism
  • Want to isolate work completely
  • Pre-Ruby 3.0 (no Ractors)

FORK_EXPLANATION

# Simple fork example
puts "\n--- Simple Fork ---"

if Process.respond_to?(:fork)
  pid = fork do
    puts "Child process: #{Process.pid}"
    sleep 1
    exit 42  # Exit with status code
  end
  
  puts "Parent process: #{Process.pid}, child: #{pid}"
  
  # Wait for child and get exit status
  Process.wait(pid)
  exit_status = $?.exitstatus
  puts "Child exited with status: #{exit_status}"
  
  # Parallel processing with fork
  puts "\n--- Parallel Processing with Fork ---"
  
  def parallel_process(items)
    pids = items.map do |item|
      fork do
        result = item * item  # CPU work
        exit result  # Return via exit code (limited!)
      end
    end
    
    # Wait for all children
    pids.map do |pid|
      Process.wait(pid)
      $?.exitstatus
    end
  end
  
  results = parallel_process([1, 2, 3, 4, 5])
  puts "Fork results: #{results}"
  
else
  puts "\nForking not supported on this platform (e.g., Windows)"
end

# ============================================
# 8. CONCURRENT-RUBY GEM
# ============================================

puts "\n" + "=" * 40
puts "8. CONCURRENT-RUBY GEM"
puts "=" * 40

puts <<~CONCURRENT_RUBY

  CONCURRENT-RUBY:
  Industry-standard gem for concurrency tools
  gem install concurrent-ruby
  
  PROVIDES:
  • Thread pools (FixedThreadPool, CachedThreadPool)
  • Promises and Futures
  • Actors
  • Atomic variables
  • Thread-safe data structures
  • And much more...
  
  EXAMPLES:

CONCURRENT_RUBY

=begin
require 'concurrent'

# Thread Pool Executor
pool = Concurrent::FixedThreadPool.new(5)

10.times do |i|
  pool.post do
    puts "Task #{i} on thread #{Thread.current.object_id}"
    sleep 0.1
  end
end

pool.shutdown
pool.wait_for_termination

# Promises
promise = Concurrent::Promise.execute do
  sleep 0.1
  42
end

puts promise.value  # Blocks until complete

# Futures
future = Concurrent::Future.execute do
  sleep 0.1
  "Result"
end

puts future.value  # Blocks until complete

# Atomic variables
counter = Concurrent::AtomicFixnum.new(0)

threads = 10.times.map do
  Thread.new do
    100.times { counter.increment }
  end
end

threads.each(&:join)
puts "Atomic counter: #{counter.value}"

# Concurrent Array
array = Concurrent::Array.new

threads = 10.times.map do |i|
  Thread.new do
    10.times { array << i }
  end
end

threads.each(&:join)
puts "Array size: #{array.size}"

# Actors
class CounterActor < Concurrent::Actor::Context
  def initialize
    @count = 0
  end
  
  def on_message(msg)
    case msg
    when :increment
      @count += 1
    when :value
      @count
    end
  end
end

actor = CounterActor.spawn(:counter)
actor << :increment
actor << :increment
actor << :increment
puts "Actor count: #{actor.ask!(:value)}"
=end

# ============================================
# 9. ASYNC/AWAIT PATTERN (FIBER-BASED)
# ============================================

puts "\n" + "=" * 40
puts "9. FIBERS AND ASYNC I/O"
puts "=" * 40

puts <<~FIBERS

  FIBERS:
  • Lightweight concurrency primitive
  • Cooperative (manual yielding)
  • Used for async I/O patterns
  • Foundation for async gems (Async, EventMachine)
  
  CHARACTERISTICS:
  • Very lightweight (thousands possible)
  • Manual scheduling (yield/resume)
  • Single-threaded cooperative multitasking

FIBERS

# Basic Fiber example
puts "\n--- Basic Fiber ---"

fiber = Fiber.new do
  puts "Fiber: Started"
  Fiber.yield "First yield"
  puts "Fiber: Resumed"
  Fiber.yield "Second yield"
  puts "Fiber: Resumed again"
  "Final return"
end

puts "Main: #{fiber.resume}"  # "First yield"
puts "Main: #{fiber.resume}"  # "Second yield"
puts "Main: #{fiber.resume}"  # "Final return"

# Producer-Consumer with Fiber
puts "\n--- Producer-Consumer Fiber ---"

producer = Fiber.new do
  5.times do |i|
    puts "Producing: #{i}"
    Fiber.yield i
  end
  nil
end

while (item = producer.resume)
  puts "Consuming: #{item}"
end

# ============================================
# 10. BEST PRACTICES
# ============================================

puts "\n" + "=" * 40
puts "10. CONCURRENCY BEST PRACTICES"
puts "=" * 40

puts <<~BEST_PRACTICES

  CHOOSING THE RIGHT TOOL:
  
  THREADS:
  ✓ I/O-bound operations (HTTP, DB, file I/O)
  ✓ Waiting for external resources
  ✓ Moderate number of concurrent tasks
  ✗ CPU-bound calculations
  ✗ True parallelism needs
  
  RACTORS (Ruby 3.0+):
  ✓ CPU-bound parallel processing
  ✓ Truly independent computations
  ✓ Data processing pipelines
  ✗ Need shared mutable state
  ✗ Legacy Ruby versions
  
  PROCESSES (Fork):
  ✓ CPU-bound tasks (pre-Ruby 3.0)
  ✓ Complete isolation needed
  ✓ Fault tolerance (process crashes don't affect others)
  ✗ High memory overhead
  ✗ Complex inter-process communication
  
  FIBERS:
  ✓ Async I/O patterns
  ✓ Cooperative multitasking
  ✓ Need thousands of "threads"
  ✗ Blocking operations
  
  GENERAL PRINCIPLES:
  ✓ Start with single-threaded
  ✓ Measure before optimizing
  ✓ Use thread-safe data structures
  ✓ Minimize shared mutable state
  ✓ Use higher-level abstractions (concurrent-ruby)
  ✓ Handle errors in threads/ractors
  ✓ Always join/close threads/ractors
  ✓ Profile under realistic load
  
  THREAD SAFETY:
  ✓ Use Mutex for critical sections
  ✓ Use Queue for producer-consumer
  ✓ Prefer immutable data
  ✓ Use atomic operations when possible
  ✓ Minimize lock scope
  ✗ Don't nest locks (deadlock risk)
  ✗ Don't hold locks during I/O
  
  DEBUGGING:
  • Thread.list to see all threads
  • Thread.current.backtrace for stack trace
  • Use logging, not puts (thread-safe)
  • Test with race condition detectors
  • Use thread-safe logger

BEST_PRACTICES

# ============================================
# 11. COMMON PATTERNS
# ============================================

puts "\n" + "=" * 40
puts "11. COMMON CONCURRENCY PATTERNS"
puts "=" * 40

# Worker pool pattern
puts "\n--- Worker Pool Pattern ---"

class WorkerPool
  def initialize(size)
    @queue = Queue.new
    @workers = Array.new(size) do
      Thread.new do
        loop do
          job = @queue.pop
          break if job == :shutdown
          begin
            job.call
          rescue => e
            puts "Worker error: #{e.message}"
          end
        end
      end
    end
  end
  
  def add_work(&block)
    @queue << block
  end
  
  def shutdown
    @workers.size.times { @queue << :shutdown }
    @workers.each(&:join)
  end
end

pool = WorkerPool.new(2)

5.times do |i|
  pool.add_work { puts "Work item #{i}" }
end

pool.shutdown

# Producer-Consumer pattern
puts "\n--- Producer-Consumer Pattern ---"

queue = Queue.new

producer = Thread.new do
  5.times do |i|
    sleep 0.05
    queue << "Item #{i}"
  end
  queue.close
end

consumers = 2.times.map do |id|
  Thread.new do
    loop do
      begin
        item = queue.pop(true)  # non-blocking
        puts "Consumer #{id} got: #{item}"
      rescue ThreadError
        break if queue.closed?
      end
    end
  end
end

producer.join
consumers.each(&:join)

puts "\n=== Complete ==="

# ============================================
# SUMMARY
# ============================================

puts <<~SUMMARY

  RUBY CONCURRENCY LANDSCAPE:
  
  1. THREADS (Built-in):
     • Good for I/O-bound tasks
     • Limited by GVL for CPU-bound
  
  2. RACTORS (Ruby 3.0+):
     • True parallelism
     • Best for CPU-bound tasks
  
  3. PROCESSES (Fork):
     • Pre-Ruby 3.0 parallelism
     • Higher overhead
  
  4. FIBERS:
     • Cooperative multitasking
     • Foundation for async
  
  5. GEMS:
     • concurrent-ruby: Thread pools, promises
     • async: Async I/O framework
     • celluloid: Actor-based (legacy)
  
  CHOOSE BASED ON:
  • Task type (I/O vs CPU)
  • Ruby version
  • Complexity tolerance
  • Performance requirements

SUMMARY
