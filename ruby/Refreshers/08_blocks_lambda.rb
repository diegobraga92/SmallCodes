# ============================================
# BLOCKS, PROCS, AND LAMBDAS DEEP DIVE
# ============================================

# ============================================
# 1. BLOCKS - THE RUBY WAY
# ============================================
puts "=" * 60
puts "1. BLOCKS - RUBY'S ANONYMOUS FUNCTIONS"
puts "=" * 60

puts <<~BLOCK_CONCEPT

  BLOCKS - KEY CONCEPTS:
  • Anonymous chunks of code (not objects by themselves)
  • Attached to method calls
  • Can capture surrounding variables (closures)
  • Cannot be saved to variables (unlike procs/lambdas)
  • Use `yield` to execute block inside method
  • Can accept parameters between |pipes|

BLOCK_CONCEPT

# ----- Basic block syntax -----
puts "\n--- Basic block syntax ---"

# Single line block with curly braces
[1, 2, 3].each { |n| puts n * 2 }

# Multi-line block with do/end
[1, 2, 3].each do |n|
  squared = n * n
  puts "#{n}^2 = #{squared}"
end

# ----- Yielding to blocks -----
puts "\n--- Yielding to blocks ---"

def greet
  puts "Before yield"
  yield if block_given?  # Check if block provided
  puts "After yield"
end

greet { puts "Hello from the block!" }

# Yielding with parameters
def repeat(n)
  n.times do |i|
    yield(i) if block_given?
  end
end

repeat(3) { |i| puts "Iteration #{i}" }

# Returning values from blocks
def transform(array)
  result = []
  array.each do |item|
    result << yield(item) if block_given?
  end
  result
end

transformed = transform([1, 2, 3]) { |n| n * 10 }
puts "Transformed: #{transformed}"

# ----- Blocks with multiple yields -----
puts "\n--- Multiple yields and block parameters ---"

def find_element(array)
  array.each do |item|
    if yield(item)
      return item
    end
  end
  nil
end

numbers = [10, 20, 30, 40, 50]
found = find_element(numbers) { |n| n > 25 }
puts "Found element > 25: #{found}"

# ----- Block with multiple parameters -----
puts "\n--- Blocks with multiple parameters ---"

def process_pair(hash)
  hash.each do |key, value|
    yield(key, value)
  end
end

person = { name: "Alice", age: 30, city: "New York" }
process_pair(person) do |key, value|
  puts "#{key.capitalize}: #{value}"
end

# ----- Blocks can access outer variables (closures) -----
puts "\n--- Blocks as closures ---"

multiplier = 5
numbers = [1, 2, 3, 4, 5]

multiplied = numbers.map { |n| n * multiplier }  # Captures multiplier
puts "Multiplied by #{multiplier}: #{multiplied}"

# Dynamic closure - captures variable at runtime
def create_multiplier(factor)
  lambda { |n| n * factor }  # Captures factor
end

double = create_multiplier(2)
triple = create_multiplier(3)

puts "Double 5: #{double.call(5)}"
puts "Triple 5: #{triple.call(5)}"

# ----- Custom iterator example -----
puts "\n--- Custom iterator: each_with_custom_index ---"

class Array
  def each_with_custom_index(start = 0)
    index = start
    each do |item|
      yield(item, index)
      index += 1
    end
  end
end

["a", "b", "c"].each_with_custom_index(10) do |letter, idx|
  puts "Item #{idx}: #{letter}"
end

# ----- Block to Proc conversion (&block) -----
puts "\n--- Converting block to proc with & ---"

def execute_with_logging(&block)
  puts "Starting execution..."
  puts "Block class: #{block.class}"  # Block becomes Proc
  result = block.call if block
  puts "Execution finished. Result: #{result}"
  result
end

execute_with_logging { 5 * 10 }

# Passing block to another method
def logger(&block)
  puts "Logging started"
  result = yield if block_given?
  puts "Logging ended"
  result
end

def calculator(a, b, &operation)
  logger do
    operation.call(a, b)
  end
end

result = calculator(10, 5) { |x, y| x * y }
puts "Calculator result: #{result}"

# ============================================
# 2. PROCS - REUSABLE BLOCKS
# ============================================
puts "\n" + "=" * 60
puts "2. PROCS - REUSABLE BLOCKS AS OBJECTS"
puts "=" * 60

puts <<~PROC_CONCEPT

  PROCS - KEY CHARACTERISTICS:
  • Proc objects are blocks that have been objectified
  • Created with Proc.new or proc
  • Can be stored in variables and passed around
  • Return behavior: returns from the enclosing method (not just proc)
  • `return` in a proc returns from the method that contains it
  • Less strict about argument count

PROC_CONCEPT

# ----- Creating procs -----
puts "\n--- Creating procs ---"

# Method 1: Proc.new
proc1 = Proc.new { |name| puts "Hello, #{name}!" }

# Method 2: Kernel.proc
proc2 = proc { |name| puts "Hi, #{name}!" }

# Method 3: lambda (different behavior, covered later)
proc3 = ->(name) { puts "Hey, #{name}!" }

proc1.call("Alice")
proc2.call("Bob")
proc3.call("Charlie")

# ----- Procs as closures -----
puts "\n--- Procs as closures ---"

def create_counter
  count = 0
  Proc.new do
    count += 1
    puts "Count: #{count}"
  end
end

counter1 = create_counter
counter2 = create_counter

counter1.call  # Count: 1
counter1.call  # Count: 2
counter2.call  # Count: 1 (separate closure)
counter1.call  # Count: 3

# ----- Procs with different argument handling -----
puts "\n--- Proc argument handling (flexible) ---"

flexible_proc = Proc.new { |a, b, c| puts "a=#{a}, b=#{b}, c=#{c}" }

puts "Proc with 2 arguments:"
flexible_proc.call(1, 2)          # c is nil

puts "\nProc with 4 arguments:"
flexible_proc.call(1, 2, 3, 4)    # Extra arguments ignored

puts "\nProc with array splat:"
flexible_proc.call([1, 2, 3])     # Array treated as single argument

# ----- Proc return behavior -----
puts "\n--- Proc return behavior (returns from enclosing method) ---"

def proc_return_example
  proc = Proc.new do
    puts "Inside proc"
    return "Returning from proc"
    puts "This line never executes"
  end
  
  puts "Before calling proc"
  result = proc.call
  puts "After calling proc (this line won't execute)"
  result
end

puts "Calling method with proc:"
begin
  result = proc_return_example
  puts "Method returned: #{result}"
rescue => e
  puts "Error: #{e.message}"
end

puts "\nWhy? The proc's return returns from the method, not just the proc!"

# Workaround: Use next instead of return
def proc_next_example
  proc = Proc.new do
    puts "Inside proc"
    next "Returning from proc with next"
    puts "This line never executes"
  end
  
  puts "Before calling proc"
  result = proc.call
  puts "After calling proc (this DOES execute)"
  result
end

puts "\nUsing next in proc:"
result = proc_next_example
puts "Method returned: #{result}"

# ----- Procs as method arguments -----
puts "\n--- Procs as method arguments ---"

def perform_operation(operation, a, b)
  operation.call(a, b)
end

add = Proc.new { |x, y| x + y }
multiply = proc { |x, y| x * y }
subtract = ->(x, y) { x - y }

puts "Addition: #{perform_operation(add, 10, 5)}"
puts "Multiplication: #{perform_operation(multiply, 10, 5)}"
puts "Subtraction: #{perform_operation(subtract, 10, 5)}"

# ----- Building DSL with procs -----
puts "\n--- Building a simple DSL with procs ---"

class Configuration
  attr_reader :settings
  
  def initialize
    @settings = {}
  end
  
  def configure(&block)
    instance_eval(&block) if block_given?
  end
  
  def set(key, value)
    @settings[key] = value
  end
  
  def database(config)
    @settings[:database] = config
  end
  
  def server(config)
    @settings[:server] = config
  end
end

config = Configuration.new
config.configure do
  set :app_name, "MyApp"
  set :version, "1.0.0"
  
  database do
    { adapter: "postgresql", host: "localhost", port: 5432 }
  end
  
  server do
    { host: "0.0.0.0", port: 3000, workers: 4 }
  end
end

puts "DSL Configuration:"
pp config.settings

# ============================================
# 3. LAMBDAS - ANONYMOUS FUNCTIONS
# ============================================
puts "\n" + "=" * 60
puts "3. LAMBDAS - STRICT ANONYMOUS FUNCTIONS"
puts "=" * 60

puts <<~LAMBDA_CONCEPT

  LAMBDAS - KEY CHARACTERISTICS:
  • Also Proc objects, but with different behavior
  • Created with `lambda` or `->` (stabby lambda)
  • Strict about argument count (like methods)
  • Return behavior: returns from the lambda itself, not enclosing method
  • Behaves more like a regular method
  • Often preferred over procs for their predictability

LAMBDA_CONCEPT

# ----- Creating lambdas -----
puts "\n--- Creating lambdas ---"

# Method 1: lambda keyword
lambda1 = lambda { |name| puts "Hello, #{name}!" }

# Method 2: stabby lambda (preferred in modern Ruby)
lambda2 = ->(name) { puts "Hi, #{name}!" }

# Method 3: stabby lambda with no arguments
lambda3 = -> { puts "No arguments needed!" }

lambda1.call("Alice")
lambda2.call("Bob")
lambda3.call

# ----- Lambda argument handling (strict) -----
puts "\n--- Lambda argument handling (strict) ---"

strict_lambda = ->(a, b, c) { puts "a=#{a}, b=#{b}, c=#{c}" }

puts "Lambda with 3 arguments:"
strict_lambda.call(1, 2, 3)

puts "\nLambda with 2 arguments (raises error):"
begin
  strict_lambda.call(1, 2)
rescue ArgumentError => e
  puts "Error: #{e.message}"
end

puts "\nLambda with 4 arguments (raises error):"
begin
  strict_lambda.call(1, 2, 3, 4)
rescue ArgumentError => e
  puts "Error: #{e.message}"
end

# ----- Lambda return behavior -----
puts "\n--- Lambda return behavior (returns from lambda only) ---"

def lambda_return_example
  my_lambda = lambda do
    puts "Inside lambda"
    return "Returning from lambda"
    puts "This line never executes"
  end
  
  puts "Before calling lambda"
  result = my_lambda.call
  puts "After calling lambda (this DOES execute)"
  result
end

puts "Calling method with lambda:"
result = lambda_return_example
puts "Method returned: #{result}"

# ----- Lambdas vs Procs comparison -----
puts "\n--- Lambdas vs Procs: Side-by-side comparison ---"

puts "\n1. Argument handling:"
proc_argh = Proc.new { |a, b| puts "Proc: a=#{a}, b=#{b}" }
lambda_argh = ->(a, b) { puts "Lambda: a=#{a}, b=#{b}" }

puts "Proc with wrong arity:"
proc_argh.call(1)           # b is nil
proc_argh.call(1, 2, 3)     # Extra ignored

puts "\nLambda with wrong arity:"
begin
  lambda_argh.call(1)
rescue ArgumentError => e
  puts "Lambda error: #{e.message}"
end

puts "\n2. Return behavior:"
def proc_vs_lambda
  proc_obj = Proc.new { return "Proc return" }
  lambda_obj = -> { return "Lambda return" }
  
  puts "Calling proc:"
  proc_result = proc_obj.call
  puts "This line won't execute if proc returns from method"
  
  puts "Calling lambda:"
  lambda_result = lambda_obj.call
  puts "This line DOES execute"
  
  "Method return"
end

puts "Result: #{proc_vs_lambda}"

puts "\n3. Break behavior:"
def proc_break
  proc = Proc.new { break "Proc break" }
  proc.call
  "After proc call"
end

def lambda_break
  lambda = -> { break "Lambda break" }
  lambda.call
  "After lambda call"
end

puts "Proc break: #{proc_break}"
puts "Lambda break: #{lambda_break}"

# ----- Lambdas in functional programming -----
puts "\n--- Lambdas in functional programming ---"

# Composition with lambdas
add_one = ->(x) { x + 1 }
multiply_by_two = ->(x) { x * 2 }
square = ->(x) { x * x }

def compose(*functions)
  ->(x) {
    functions.reduce(x) { |value, func| func.call(value) }
  }
end

composed = compose(add_one, multiply_by_two, square)
puts "Composed functions: add_one -> multiply_by_two -> square"
puts "Result for 3: #{composed.call(3)}"  # (3+1)*2 = 8, 8^2 = 64

# Currying with lambdas
puts "\n--- Currying with lambdas ---"

add_three = ->(a, b, c) { a + b + c }
curried_add = add_three.curry

add_five = curried_add.call(5)
add_five_and_three = add_five.call(3)
result = add_five_and_three.call(2)

puts "Curried addition: #{result}"

# More concise currying
increment_by = ->(amount, value) { value + amount }.curry
increment_by_10 = increment_by.call(10)

puts "Increment by 10: #{increment_by_10.call(5)}"

# ----- Memoization with lambdas -----
puts "\n--- Memoization with lambdas ---"

class Fibonacci
  def self.memoized
    @memoized ||= lambda do |n|
      return n if n <= 1
      @memoized.call(n - 1) + @memoized.call(n - 2)
    end
  end
end

puts "Memoized Fibonacci(10): #{Fibonacci.memoized.call(10)}"
puts "Memoized Fibonacci(20): #{Fibonacci.memoized.call(20)}"

# ============================================
# 4. CLOSURES DEEP DIVE
# ============================================
puts "\n" + "=" * 60
puts "4. CLOSURES DEEP DIVE"
puts "=" * 60

puts <<~CLOSURE_CONCEPT

  CLOSURES - KEY CONCEPTS:
  • Blocks/Procs/Lambdas capture the surrounding environment
  • They remember variables from the scope where they were defined
  • Each closure has its own binding
  • Allows for creating function factories and encapsulating state
  • Forms the basis for many functional programming patterns

CLOSURE_CONCEPT

# ----- Variable capture -----
puts "\n--- Variable capture in closures ---"

def create_multipliers
  multipliers = []
  
  (1..5).each do |i|
    # Each lambda captures its own i
    multipliers << ->(x) { x * i }
  end
  
  multipliers
end

multipliers = create_multipliers
puts "Multiply by 3: #{multipliers[2].call(10)}"  # 10 * 3 = 30
puts "Multiply by 5: #{multipliers[4].call(10)}"  # 10 * 5 = 50

# ----- Shared vs independent variables -----
puts "\n--- Shared vs independent closures ---"

# Shared variable (common pitfall)
def create_counter_shared
  counter = 0
  [
    -> { counter += 1 },  # Both lambdas share same counter
    -> { counter += 1 }
  ]
end

shared = create_counter_shared
puts "Shared counter:"
puts "First: #{shared[0].call}"  # 1
puts "Second: #{shared[1].call}" # 2
puts "First again: #{shared[0].call}" # 3

# Independent variables
def create_counter_independent
  [
    lambda { 
      counter = 0
      -> { counter += 1 }
    }.call,
    lambda {
      counter = 0
      -> { counter += 1 }
    }.call
  ]
end

independent = create_counter_independent
puts "\nIndependent counters:"
puts "First: #{independent[0].call}"  # 1
puts "Second: #{independent[1].call}" # 1
puts "First: #{independent[0].call}"  # 2
puts "Second: #{independent[1].call}" # 2

# ----- Closure with mutable state -----
puts "\n--- Encapsulating state with closures ---"

def bank_account(initial_balance)
  balance = initial_balance
  
  {
    deposit: ->(amount) {
      raise "Invalid amount" if amount <= 0
      balance += amount
      puts "Deposited $#{amount}. New balance: $#{balance}"
    },
    withdraw: ->(amount) {
      raise "Invalid amount" if amount <= 0
      raise "Insufficient funds" if amount > balance
      balance -= amount
      puts "Withdrew $#{amount}. New balance: $#{balance}"
    },
    balance: -> { balance }
  }
end

account = bank_account(1000)
account[:deposit].call(500)
account[:withdraw].call(200)
puts "Current balance: $#{account[:balance].call}"

# Attempt to directly access balance (can't - it's encapsulated)
begin
  puts account[:balance]  # This is a lambda, not the balance
rescue => e
  puts "Balance is properly encapsulated"
end

# ----- Creating DSL with closures -----
puts "\n--- Building a query DSL with closures ---"

class QueryBuilder
  def initialize
    @conditions = []
  end
  
  def where(&block)
    @conditions << block
    self
  end
  
  def execute(collection)
    collection.select do |item|
      @conditions.all? { |condition| condition.call(item) }
    end
  end
end

users = [
  { name: "Alice", age: 25, active: true },
  { name: "Bob", age: 30, active: false },
  { name: "Charlie", age: 35, active: true },
  { name: "David", age: 20, active: true }
]

query = QueryBuilder.new
  .where { |u| u[:active] == true }
  .where { |u| u[:age] > 25 }

active_over_25 = query.execute(users)
puts "Active users over 25:"
active_over_25.each { |u| puts "  #{u[:name]}" }

# ============================================
# 5. YIELDING AND CUSTOM ITERATORS
# ============================================
puts "\n" + "=" * 60
puts "5. YIELDING AND CUSTOM ITERATORS"
puts "=" * 60

# ----- The yield keyword -----
puts "\n--- Understanding yield ---"

def simple_yield
  puts "Before yield"
  yield if block_given?
  puts "After yield"
end

simple_yield { puts "In the block!" }

# ----- Yielding with arguments -----
puts "\n--- Yielding with arguments ---"

def times_table(n)
  (1..10).each do |i|
    result = yield(i, n) if block_given?
    puts "#{i} x #{n} = #{result}"
  end
end

times_table(5) do |i, n|
  i * n
end

# ----- Yielding with return values -----
puts "\n--- Using yield return values ---"

def map(array)
  result = []
  array.each do |item|
    result << yield(item)
  end
  result
end

mapped = map([1, 2, 3, 4, 5]) { |n| n ** 2 }
puts "Squared: #{mapped}"

# ----- Yielding multiple values -----
puts "\n--- Yielding multiple values ---"

def each_pair(hash)
  hash.each do |key, value|
    yield(key, value)
  end
end

person = { name: "Alice", age: 30, city: "New York" }
each_pair(person) do |key, value|
  puts "#{key}: #{value}"
end

# ----- Custom iterator: each_with_index implementation -----
puts "\n--- Custom each_with_index ---"

class Array
  def my_each_with_index
    index = 0
    each do |item|
      yield(item, index)
      index += 1
    end
  end
end

["apple", "banana", "cherry"].my_each_with_index do |fruit, idx|
  puts "#{idx}: #{fruit}"
end

# ----- Custom iterator: each_cons (consecutive elements) -----
puts "\n--- Custom each_cons (consecutive pairs) ---"

class Array
  def each_cons(n)
    return to_enum(:each_cons, n) unless block_given?
    
    (0..length - n).each do |i|
      yield(self[i, n])
    end
    self
  end
end

[1, 2, 3, 4, 5].each_cons(3) do |group|
  puts "Group: #{group}"
end

# ----- Custom iterator with lazy evaluation -----
puts "\n--- Lazy iterator with yielding ---"

class LazyRange
  def initialize(start, finish)
    @start = start
    @finish = finish
    @current = start
  end
  
  def each
    while @current <= @finish
      yield(@current)
      @current += 1
    end
  end
  
  def map
    return to_enum(:map) unless block_given?
    
    result = []
    each do |value|
      result << yield(value)
    end
    result
  end
  
  def select
    return to_enum(:select) unless block_given?
    
    result = []
    each do |value|
      result << value if yield(value)
    end
    result
  end
end

range = LazyRange.new(1, 10)
squares = range.map { |n| n ** 2 }
puts "Squares: #{squares}"

evens = range.select { |n| n.even? }
puts "Evens: #{evens}"

# ----- Complex iterator: tree traversal -----
puts "\n--- Tree traversal with yield ---"

class TreeNode
  attr_accessor :value, :left, :right
  
  def initialize(value)
    @value = value
    @left = nil
    @right = nil
  end
  
  def inorder(&block)
    return to_enum(:inorder) unless block_given?
    
    @left&.inorder(&block)
    yield(value)
    @right&.inorder(&block)
  end
  
  def preorder(&block)
    return to_enum(:preorder) unless block_given?
    
    yield(value)
    @left&.preorder(&block)
    @right&.preorder(&block)
  end
  
  def postorder(&block)
    return to_enum(:postorder) unless block_given?
    
    @left&.postorder(&block)
    @right&.postorder(&block)
    yield(value)
  end
end

# Build a binary search tree
root = TreeNode.new(50)
root.left = TreeNode.new(30)
root.right = TreeNode.new(70)
root.left.left = TreeNode.new(20)
root.left.right = TreeNode.new(40)
root.right.left = TreeNode.new(60)
root.right.right = TreeNode.new(80)

puts "Inorder traversal (sorted):"
root.inorder { |v| print "#{v} " }
puts

puts "Preorder traversal:"
root.preorder { |v| print "#{v} " }
puts

puts "Postorder traversal:"
root.postorder { |v| print "#{v} " }
puts

# ----- Enumerator and lazy evaluation -----
puts "\n--- Using Enumerator with blocks ---"

def fibonacci_sequence
  Enumerator.new do |yielder|
    a, b = 0, 1
    loop do
      yielder.yield(a)
      a, b = b, a + b
    end
  end
end

fib = fibonacci_sequence
puts "First 10 Fibonacci numbers:"
fib.take(10).each { |n| print "#{n} " }
puts

# Lazy evaluation with infinite sequences
puts "\nFirst 5 even Fibonacci numbers:"
even_fibs = fibonacci_sequence.lazy.select(&:even?).take(5).to_a
puts even_fibs.join(", ")

# ============================================
# 6. ADVANCED PATTERNS WITH BLOCKS/PROCS/LAMBDAS
# ============================================
puts "\n" + "=" * 60
puts "6. ADVANCED PATTERNS"
puts "=" * 60

# ----- Method memoization with lambda -----
puts "\n--- Memoization pattern ---"

def memoize(method_name)
  cache = {}
  
  original_method = instance_method(method_name)
  
  define_method(method_name) do |*args|
    if cache.key?(args)
      cache[args]
    else
      cache[args] = original_method.bind(self).call(*args)
    end
  end
end

class ExpensiveCalculator
  def expensive_computation(n)
    puts "Computing for #{n}..."
    sleep(0.5)  # Simulate expensive operation
    n * n
  end
  
  memoize :expensive_computation
end

calc = ExpensiveCalculator.new
puts calc.expensive_computation(5)  # Computes
puts calc.expensive_computation(5)  # Returns from cache
puts calc.expensive_computation(10) # Computes new value

# ----- Callback system with blocks -----
puts "\n--- Callback system ---"

class EventEmitter
  def initialize
    @handlers = {}
  end
  
  def on(event, &handler)
    @handlers[event] ||= []
    @handlers[event] << handler
  end
  
  def emit(event, *args)
    if @handlers[event]
      @handlers[event].each do |handler|
        handler.call(*args)
      end
    end
  end
  
  def once(event, &handler)
    once_handler = lambda do |*args|
      handler.call(*args)
      @handlers[event].delete(once_handler)
    end
    on(event, &once_handler)
  end
end

emitter = EventEmitter.new

emitter.on(:user_login) do |user|
  puts "User #{user} logged in"
end

emitter.once(:app_start) do
  puts "App started (this runs only once)"
end

emitter.emit(:user_login, "Alice")
emitter.emit(:user_login, "Bob")
emitter.emit(:app_start)
emitter.emit(:app_start)  # Won't trigger

# ----- Retry pattern with blocks -----
puts "\n--- Retry pattern ---"

def with_retry(max_retries: 3, delay: 1, &block)
  attempts = 0
  begin
    attempts += 1
    yield
  rescue => e
    if attempts < max_retries
      puts "Attempt #{attempts} failed: #{e.message}. Retrying in #{delay}s..."
      sleep(delay)
      retry
    else
      puts "Failed after #{max_retries} attempts"
      raise
    end
  end
end

# Simulate unreliable operation
attempts = 0
begin
  with_retry(max_retries: 5, delay: 0.1) do
    attempts += 1
    if attempts < 4
      raise "Temporary network error"
    end
    puts "Operation succeeded on attempt #{attempts}"
  end
rescue => e
  puts "Final error: #{e.message}"
end

# ----- Resource management pattern -----
puts "\n--- Resource management with ensure and yield ---"

class DatabaseConnection
  def initialize
    puts "Opening database connection"
  end
  
  def query(sql)
    puts "Executing: #{sql}"
    "Result set"
  end
  
  def close
    puts "Closing database connection"
  end
end

def with_database(&block)
  db = DatabaseConnection.new
  begin
    yield(db)
  ensure
    db.close
  end
end

with_database do |db|
  result = db.query("SELECT * FROM users")
  puts "Got: #{result}"
end

# ----- Pipeline pattern -----
puts "\n--- Pipeline pattern with procs ---"

class Pipeline
  def initialize
    @stages = []
  end
  
  def add_stage(&stage)
    @stages << stage
    self
  end
  
  def execute(input)
    @stages.reduce(input) { |value, stage| stage.call(value) }
  end
end

pipeline = Pipeline.new
  .add_stage { |data| data.map(&:strip) }
  .add_stage { |data| data.reject(&:empty?) }
  .add_stage { |data| data.map(&:upcase) }
  .add_stage { |data| data.sort }

input = ["  hello  ", "", "  world  ", "ruby", "  ", "PROGRAMMING"]
result = pipeline.execute(input)
puts "Pipeline result: #{result}"

# ============================================
# 7. PERFORMANCE AND BEST PRACTICES
# ============================================
puts "\n" + "=" * 60
puts "7. PERFORMANCE AND BEST PRACTICES"
puts "=" * 60

puts <<~BEST_PRACTICES

  WHEN TO USE WHAT:
  
  BLOCKS:
  ✓ Simple, one-off operations
  ✓ Iterators and callbacks
  ✓ DSLs and configuration
  ✓ When you don't need to store the code
  
  PROCS:
  ✓ When you need to store and reuse blocks
  ✓ When argument count flexibility is needed
  ✓ When you want return to affect enclosing scope
  ✓ Callbacks and handlers
  
  LAMBDAS:
  ✓ When you need strict argument checking
  ✓ For functional programming patterns
  ✓ When you want return to only exit the lambda
  ✓ As method-like anonymous functions
  
  PERFORMANCE TIPS:
  • Blocks are slightly faster than Procs/Lambdas
  • Use &block for method-to-block conversion
  • Avoid creating many procs/lambdas in tight loops
  • Use lambda when you need method-like behavior
  
  COMMON PITFALLS:
  1. Forgetting to check block_given? before yield
  2. Variable capture in loops (use closure or each)
  3. Using return in procs when you meant next
  4. Argument count mismatch with lambdas
  5. Performance impact of creating many closures

BEST_PRACTICES

# Benchmarking demonstration
puts "\n--- Performance comparison ---"

require 'benchmark'

n = 100_000

Benchmark.bm(10) do |x|
  x.report("Block:") do
    n.times do |i|
      [1, 2, 3].map { |v| v * i }
    end
  end
  
  x.report("Proc:") do
    proc = Proc.new { |v, i| v * i }
    n.times do |i|
      [1, 2, 3].map { |v| proc.call(v, i) }
    end
  end
  
  x.report("Lambda:") do
    lambda = ->(v, i) { v * i }
    n.times do |i|
      [1, 2, 3].map { |v| lambda.call(v, i) }
    end
  end
end

# ============================================
# 8. SUMMARY CHEAT SHEET
# ============================================
puts "\n" + "=" * 60
puts "8. QUICK REFERENCE CHEAT SHEET"
puts "=" * 60

puts <<~CHEAT_SHEET

  SYNTAX COMPARISON:
  ┌─────────────────┬──────────────────┬──────────────────┬──────────────────┐
  │ Feature         │ Block            │ Proc             │ Lambda           │
  ├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ Creation        │ { |x| x*2 }      │ Proc.new {|x| x*2}│ lambda {|x| x*2}│
  │                 │ do...end         │ proc {|x| x*2}    │ ->(x) { x*2 }   │
  ├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ Object?         │ No               │ Yes (Proc)       │ Yes (Proc)       │
  ├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ Arity           │ Flexible         │ Flexible         │ Strict           │
  ├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ Return behavior │ From method      │ From method      │ From lambda only │
  ├─────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │ Use case        │ Iterators, DSLs  │ Reusable blocks  │ Functions, FP    │
  └─────────────────┴──────────────────┴──────────────────┴──────────────────┘
  
  COMMON METHODS:
  • block_given?      - Check if block provided
  • yield             - Call block
  • &block            - Convert block to proc
  • call              - Execute proc/lambda
  • curry             - Create curried lambda
  • to_proc           - Convert to proc
  • lambda?           - Check if proc is lambda
  
  QUICK EXAMPLES:
  
  # Block
  def with_logging
    puts "Start"
    result = yield if block_given?
    puts "End"
    result
  end
  
  # Proc
  add = Proc.new { |a,b| a + b }
  add.call(2,3)  # => 5
  
  # Lambda
  multiply = ->(a,b) { a * b }
  multiply.call(2,3)  # => 6
  
  # Converting symbol to proc
  ["a", "b", "c"].map(&:upcase)  # => ["A", "B", "C"]
  
  # Currying
  add_three = ->(a,b,c) { a + b + c }.curry
  add_ten = add_three.call(10)
  add_ten.call(5, 3)  # => 18

CHEAT_SHEET

puts "\n" + "=" * 60
puts "END OF BLOCKS, PROCS, AND LAMBDAS DEEP DIVE"
puts "=" * 60