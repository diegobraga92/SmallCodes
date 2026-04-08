# ============================================
# ENUMERABLES & FUNCTIONAL PATTERNS DEEP DIVE
# ============================================

# ============================================
# 1. DEEP UNDERSTANDING OF ENUMERABLE
# ============================================
puts "=" * 60
puts "1. ENUMERABLE - THE HEART OF RUBY COLLECTIONS"
puts "=" * 60

puts <<~ENUMERABLE_CONCEPT

  ENUMERABLE MODULE:
  • Included in Array, Hash, Range, Set, etc.
  • Provides 60+ methods for traversal, search, sorting
  • Only requires #each to be implemented
  • Forms the foundation of Ruby's functional style
  • Returns Enumerators when called without blocks

ENUMERABLE_CONCEPT

# ----- How Enumerable works -----
puts "\n--- Implementing a custom Enumerable class ---"

class BinaryTree
  include Enumerable
  
  Node = Struct.new(:value, :left, :right)
  
  def initialize
    @root = nil
  end
  
  def insert(value)
    @root = insert_recursive(@root, value)
  end
  
  def each
    return to_enum(:each) unless block_given?
    inorder_traversal(@root, &Proc.new)
  end
  
  private
  
  def insert_recursive(node, value)
    return Node.new(value) if node.nil?
    
    if value < node.value
      node.left = insert_recursive(node.left, value)
    elsif value > node.value
      node.right = insert_recursive(node.right, value)
    end
    node
  end
  
  def inorder_traversal(node, &block)
    return if node.nil?
    inorder_traversal(node.left, &block)
    yield(node.value)
    inorder_traversal(node.right, &block)
  end
end

tree = BinaryTree.new
[5, 3, 7, 1, 4, 6, 8].each { |v| tree.insert(v) }

puts "Tree values in order: #{tree.to_a}"
puts "Tree includes 4? #{tree.include?(4)}"
puts "Tree includes 9? #{tree.include?(9)}"
puts "All values > 0? #{tree.all? { |v| v > 0 }}"
puts "Values > 5: #{tree.select { |v| v > 5 }}"

# ----- Essential Enumerable methods deep dive -----
puts "\n--- Essential Enumerable Methods ---"

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# each - the foundation
puts "\n1. each - iteration"
numbers.each { |n| print "#{n} " }
puts

# map/collect - transformation
puts "\n2. map/collect - transformation"
squares = numbers.map { |n| n ** 2 }
puts "Squares: #{squares}"

# select/find_all - filtering
puts "\n3. select - filtering"
evens = numbers.select { |n| n.even? }
puts "Evens: #{evens}"

# reject - opposite of select
puts "\n4. reject - filtering out"
odds = numbers.reject { |n| n.even? }
puts "Odds: #{odds}"

# reduce/inject - accumulation
puts "\n5. reduce/inject - accumulation"
sum = numbers.reduce(0) { |acc, n| acc + n }
puts "Sum: #{sum}"
product = numbers.reduce(:*)
puts "Product: #{product}"

# find/detect - find first match
puts "\n6. find - first match"
first_large = numbers.find { |n| n > 5 }
puts "First number > 5: #{first_large}"

# any? - check if any match
puts "\n7. any? - exists"
has_even = numbers.any?(&:even?)
puts "Has even? #{has_even}"
has_large = numbers.any? { |n| n > 100 }
puts "Has > 100? #{has_large}"

# all? - check if all match
puts "\n8. all? - all match"
all_positive = numbers.all? { |n| n > 0 }
puts "All positive? #{all_positive}"

# none? - check if none match
puts "\n9. none? - none match"
none_negative = numbers.none? { |n| n < 0 }
puts "None negative? #{none_negative}"

# count - count matches
puts "\n10. count - counting"
count_even = numbers.count(&:even?)
puts "Count of evens: #{count_even}"

# ----- Advanced Enumerable methods -----
puts "\n--- Advanced Enumerable Methods ---"

# each_with_object - accumulate without reduce
puts "\n11. each_with_object - accumulate with object"
hash = numbers.each_with_object({}) do |n, h|
  h[n] = n ** 2
end
puts "Number to square: #{hash}"

# group_by - grouping
puts "\n12. group_by - categorize"
grouped = numbers.group_by { |n| n.even? ? "even" : "odd" }
puts "Grouped by parity: #{grouped}"

# partition - split into two groups
puts "\n13. partition - split"
even, odd = numbers.partition(&:even?)
puts "Evens: #{even}, Odds: #{odd}"

# chunk - group consecutive elements
puts "\n14. chunk - group by condition"
chunks = [1, 2, 2, 3, 3, 3, 4, 5, 5].chunk { |n| n }.to_a
puts "Chunks: #{chunks}"

# flat_map - map and flatten
puts "\n15. flat_map - map then flatten"
nested = [[1, 2], [3, 4], [5, 6]]
flattened = nested.flat_map { |arr| arr.map { |n| n * 2 } }
puts "Flat mapped: #{flattened}"

# zip - combine multiple collections
puts "\n16. zip - combine"
names = ["Alice", "Bob", "Charlie"]
ages = [30, 25, 35}
zipped = names.zip(ages)
puts "Zipped: #{zipped}"

# ----- Working with Hashes and Enumerable -----
puts "\n--- Enumerable with Hashes ---"

users = {
  alice: { name: "Alice", age: 30, role: "admin" },
  bob: { name: "Bob", age: 25, role: "user" },
  charlie: { name: "Charlie", age: 35, role: "admin" },
  diana: { name: "Diana", age: 28, role: "user" }
}

# Hash#each yields key-value pairs
puts "\nIterating over hash:"
users.each do |key, value|
  puts "  #{key}: #{value[:name]} (#{value[:role]})"
end

# Transform keys/values
puts "\nTransforming hash:"
admin_names = users.select { |_, v| v[:role] == "admin" }
                    .map { |k, v| v[:name] }
puts "Admins: #{admin_names}"

# Using with hash directly
puts "\nHash-specific enumerable methods:"
adults = users.select { |_, v| v[:age] > 27 }
puts "Adults: #{adults.keys}"

# ----- Custom Enumerable implementations -----
puts "\n--- Custom Enumerable: Matrix ---"

class Matrix
  include Enumerable
  
  def initialize(rows, cols)
    @rows = rows
    @cols = cols
    @data = Array.new(rows) { Array.new(cols, 0) }
  end
  
  def []=(row, col, value)
    @data[row][col] = value
  end
  
  def [](row, col)
    @data[row][col]
  end
  
  def each
    return to_enum(:each) unless block_given?
    
    @data.each_with_index do |row, i|
      row.each_with_index do |value, j|
        yield(value, i, j)
      end
    end
  end
  
  def to_s
    @data.map { |row| row.join("\t") }.join("\n")
  end
end

matrix = Matrix.new(3, 3)
(0..2).each do |i|
  (0..2).each do |j|
    matrix[i, j] = i * 3 + j + 1
  end
end

puts "Matrix:"
puts matrix

puts "\nAll elements: #{matrix.to_a}"
puts "Sum of all elements: #{matrix.reduce(0) { |sum, (val, i, j)| sum + val }}"
puts "Elements > 5: #{matrix.select { |val, i, j| val > 5 }.map(&:first)}"

# ============================================
# 2. LAZY ENUMERATORS - INFINITE AND EFFICIENT
# ============================================
puts "\n" + "=" * 60
puts "2. LAZY ENUMERATORS - DEFERRED EVALUATION"
puts "=" * 60

puts <<~LAZY_CONCEPT

  LAZY ENUMERATORS:
  • Defer computation until values are needed
  • Work with infinite sequences
  • Improve performance by avoiding intermediate arrays
  • Chain operations without creating temporary collections
  • Use .lazy on any Enumerable

LAZY_CONCEPT

# ----- Basic lazy evaluation -----
puts "\n--- Basic lazy vs eager comparison ---"

def expensive_operation(n)
  puts "  Computing for #{n}"
  sleep(0.1)  # Simulate expensive work
  n * n
end

puts "\nEager evaluation (computes all):"
eager_result = (1..10).map { |n| expensive_operation(n) }
                       .select { |n| n > 25 }
                       .first(3)
puts "Result: #{eager_result}"

puts "\nLazy evaluation (computes only needed):"
lazy_result = (1..10).lazy
                     .map { |n| expensive_operation(n) }
                     .select { |n| n > 25 }
                     .first(3)
puts "Result: #{lazy_result}"

# ----- Infinite sequences with lazy enumerators -----
puts "\n--- Infinite sequences ---"

# Infinite sequence of natural numbers
natural_numbers = (1..Float::INFINITY).lazy

puts "First 10 natural numbers:"
natural_numbers.first(10).each { |n| print "#{n} " }
puts

# Fibonacci sequence with lazy
def fibonacci
  Enumerator.new do |yielder|
    a, b = 0, 1
    loop do
      yielder.yield(a)
      a, b = b, a + b
    end
  end.lazy
end

fib = fibonacci
puts "\nFirst 20 Fibonacci numbers:"
fib.first(20).each { |n| print "#{n} " }
puts

puts "\nFirst 10 even Fibonacci numbers:"
even_fibs = fibonacci.select(&:even?).first(10)
puts even_fibs.join(", ")

# ----- Prime numbers with lazy -----
puts "\n--- Prime numbers generator ---"

def prime_numbers
  Enumerator.new do |yielder|
    n = 2
    loop do
      is_prime = (2..Math.sqrt(n)).none? { |i| n % i == 0 }
      yielder.yield(n) if is_prime
      n += 1
    end
  end.lazy
end

primes = prime_numbers

puts "First 10 primes: #{primes.first(10)}"
puts "Primes between 50 and 100:"
primes.select { |p| p > 50 && p < 100 }.first(10).each { |p| print "#{p} " }
puts

# ----- Performance benefits of lazy evaluation -----
puts "\n--- Performance comparison ---"

require 'benchmark'

n = 1_000_000

Benchmark.bm(15) do |x|
  x.report("Eager:") do
    (1..n).map { |i| i * 2 }
          .select(&:even?)
          .first(5)
  end
  
  x.report("Lazy:") do
    (1..n).lazy
          .map { |i| i * 2 }
          .select(&:even?)
          .first(5)
  end
end

# ----- Lazy processing of large files -----
puts "\n--- Lazy file processing ---"

# Create a large test file
File.open("large_file.txt", "w") do |f|
  1000.times { |i| f.puts "Line #{i}: " + "x" * 100 }
end

puts "\nProcessing large file lazily:"
File.open("large_file.txt") do |file|
  file.lines
      .lazy
      .map(&:chomp)
      .select { |line| line.match?(/Line \d{2,3}:/) }
      .take(5)
      .each { |line| puts "  #{line[0..50]}..." }
end

# ----- Building complex lazy pipelines -----
puts "\n--- Complex lazy pipelines ---"

# Data pipeline: filter, transform, and analyze
class DataPipeline
  def initialize(data_source)
    @data_source = data_source
  end
  
  def analyze
    @data_source.lazy
                .map { |line| parse_line(line) }
                .reject { |record| record[:value].nil? }
                .select { |record| record[:value] > 100 }
                .map { |record| enrich_record(record) }
                .take(10)
                .to_a
  end
  
  private
  
  def parse_line(line)
    parts = line.split(',')
    {
      id: parts[0].to_i,
      name: parts[1],
      value: parts[2]&.to_f
    }
  end
  
  def enrich_record(record)
    record[:value_with_tax] = record[:value] * 1.1
    record[:category] = case record[:value]
                        when 100..500 then "medium"
                        when 501..1000 then "high"
                        else "premium"
                        end
    record
  end
end

# Create test data
File.open("data.csv", "w") do |f|
  1000.times do |i|
    f.puts "#{i},Item_#{i},#{rand(1000)}"
  end
end

pipeline = DataPipeline.new(File.readlines("data.csv"))
results = pipeline.analyze
puts "First 10 enriched records:"
results.each { |r| puts "  #{r}" }

# ============================================
# 3. FUNCTIONAL CHAINING AND TRANSFORMATIONS
# ============================================
puts "\n" + "=" * 60
puts "3. FUNCTIONAL CHAINING AND TRANSFORMATIONS"
puts "=" * 60

puts <<~FUNCTIONAL_CONCEPT

  FUNCTIONAL PATTERNS:
  • Chain operations without side effects
  • Use immutable transformations
  • Compose small, focused functions
  • Leverage Ruby's Enumerable for data pipelines
  • Prefer declarative over imperative style

FUNCTIONAL_CONCEPT

# ----- Building data pipelines -----
puts "\n--- Data processing pipelines ---"

# Example: Process sales data
sales_data = [
  { product: "Laptop", category: "Electronics", price: 999.99, quantity: 2, region: "North" },
  { product: "Mouse", category: "Electronics", price: 29.99, quantity: 10, region: "South" },
  { product: "Desk", category: "Furniture", price: 199.99, quantity: 5, region: "North" },
  { product: "Monitor", category: "Electronics", price: 299.99, quantity: 3, region: "East" },
  { product: "Chair", category: "Furniture", price: 89.99, quantity: 8, region: "West" },
  { product: "Keyboard", category: "Electronics", price: 79.99, quantity: 4, region: "North" }
]

# Imperative approach (harder to read)
puts "Imperative approach:"
electronics_revenue = 0
sales_data.each do |sale|
  if sale[:category] == "Electronics"
    revenue = sale[:price] * sale[:quantity]
    if revenue > 500
      electronics_revenue += revenue
    end
  end
end
puts "Electronics revenue > 500: $#{electronics_revenue}"

# Functional approach (declarative)
puts "\nFunctional approach:"
revenue = sales_data
  .select { |s| s[:category] == "Electronics" }
  .map { |s| s[:price] * s[:quantity] }
  .select { |r| r > 500 }
  .reduce(:+)

puts "Electronics revenue > 500: $#{revenue}"

# ----- Function composition -----
puts "\n--- Function composition ---"

# Define pure functions
def format_currency(amount)
  "$#{'%.2f' % amount}"
end

def apply_discount(percentage)
  ->(amount) { amount * (1 - percentage / 100.0) }
end

def add_tax(tax_rate)
  ->(amount) { amount * (1 + tax_rate) }
end

def round_to_cents
  ->(amount) { amount.round(2) }
end

# Compose functions
calculate_final_price = ->(price, discount, tax_rate) {
  [price]
    .map(&apply_discount.call(discount))
    .map(&add_tax.call(tax_rate))
    .map(&round_to_cents)
    .map(&format_currency)
    .first
}

puts "Original price: $100.00"
puts "After 20% discount and 10% tax: #{calculate_final_price.call(100, 20, 0.1)}"

# ----- Pipeline with custom operators -----
puts "\n--- Building a pipeline DSL ---"

class Pipeline
  def initialize
    @steps = []
  end
  
  def step(&block)
    @steps << block
    self
  end
  
  def call(input)
    @steps.reduce(input) { |value, step| step.call(value) }
  end
end

# Create a data transformation pipeline
pipeline = Pipeline.new
  .step { |data| data.select { |item| item[:active] } }
  .step { |data| data.map { |item| item[:name] } }
  .step { |names| names.map(&:upcase) }
  .step { |names| names.sort }

users_data = [
  { name: "Alice", active: true },
  { name: "Bob", active: false },
  { name: "Charlie", active: true },
  { name: "Diana", active: true }
]

result = pipeline.call(users_data)
puts "Active users: #{result}"

# ----- Chainable transformations with struct -----
puts "\n--- Chainable data transformations ---"

# Create a chainable transformer
class DataTransformer
  attr_reader :data
  
  def initialize(data)
    @data = data
  end
  
  def map(&block)
    DataTransformer.new(@data.map(&block))
  end
  
  def select(&block)
    DataTransformer.new(@data.select(&block))
  end
  
  def reject(&block)
    DataTransformer.new(@data.reject(&block))
  end
  
  def sort_by(&block)
    DataTransformer.new(@data.sort_by(&block))
  end
  
  def take(n)
    DataTransformer.new(@data.take(n))
  end
  
  def to_a
    @data
  end
end

orders = [
  { id: 1, amount: 150, status: "completed", customer: "Alice" },
  { id: 2, amount: 75, status: "pending", customer: "Bob" },
  { id: 3, amount: 200, status: "completed", customer: "Charlie" },
  { id: 4, amount: 50, status: "cancelled", customer: "Alice" },
  { id: 5, amount: 300, status: "completed", customer: "Diana" }
]

result = DataTransformer.new(orders)
  .select { |o| o[:status] == "completed" }
  .reject { |o| o[:amount] < 100 }
  .map { |o| { customer: o[:customer], amount: o[:amount] } }
  .sort_by { |o| -o[:amount] }
  .take(2)
  .to_a

puts "Top completed orders > $100:"
result.each { |o| puts "  #{o[:customer]}: $#{o[:amount]}" }

# ----- Functional patterns with recursion -----
puts "\n--- Recursive transformations ---"

# Process nested structures functionally
def deep_transform(hash, &block)
  hash.each_with_object({}) do |(key, value), result|
    result[key] = case value
                  when Hash
                    deep_transform(value, &block)
                  when Array
                    value.map { |item| item.is_a?(Hash) ? deep_transform(item, &block) : yield(item) }
                  else
                    yield(value)
                  end
  end
end

config = {
  database: {
    host: "localhost",
    port: 5432,
    credentials: {
      username: "admin",
      password: "secret123"
    }
  },
  server: {
    host: "0.0.0.0",
    ports: [3000, 3001, 3002],
    ssl: {
      enabled: true,
      cert_path: "/etc/ssl/cert.pem"
    }
  }
}

# Transform all string values to uppercase
transformed = deep_transform(config) { |value| 
  value.is_a?(String) ? value.upcase : value 
}

puts "Transformed config:"
pp transformed

# ============================================
# 4. ADVANCED ENUMERABLE PATTERNS
# ============================================
puts "\n" + "=" * 60
puts "4. ADVANCED ENUMERABLE PATTERNS"
puts "=" * 60

# ----- Chunk and slice patterns -----
puts "\n--- Chunk and slice operations ---"

data = [1, 1, 2, 2, 2, 3, 4, 4, 5, 5, 5, 5]

puts "Original: #{data}"

# Chunk consecutive equal elements
chunks = data.chunk { |n| n }.to_a
puts "Chunks: #{chunks}"

# Slice after condition
slices = data.slice_after { |n| n.even? }.to_a
puts "Slice after even: #{slices}"

# Slice before condition
slices = data.slice_before { |n| n.odd? }.to_a
puts "Slice before odd: #{slices}"

# Each_cons (consecutive elements)
cons = data.each_cons(3).to_a
puts "Each consecutive 3: #{cons}"

# Each_slice (sliding window)
slices = data.each_slice(3).to_a
puts "Each slice of 3: #{slices}"

# ----- Cycle and repeat patterns -----
puts "\n--- Cycle and repeat ---"

colors = ["red", "green", "blue"]

puts "Cycle 2 times:"
colors.cycle(2).take(6).each { |c| print "#{c} " }
puts

puts "Infinite cycle (take 8):"
colors.cycle.take(8).each { |c| print "#{c} " }
puts

# ----- Enumerator chaining -----
puts "\n--- Enumerator chaining patterns ---"

# Create complex enumerators
enum = (1..Float::INFINITY).lazy
  .map { |n| n * n }
  .select(&:even?)
  .with_index
  .map { |square, idx| "Square #{idx + 1}: #{square}" }
  .take(5)

puts "First 5 even squares with index:"
enum.each { |s| puts "  #{s}" }

# ----- Functional validation pipeline -----
puts "\n--- Validation pipeline ---"

class Validator
  def initialize(rules = [])
    @rules = rules
  end
  
  def add_rule(&rule)
    Validator.new(@rules + [rule])
  end
  
  def validate(data)
    @rules.map { |rule| rule.call(data) }
          .all? { |result| result[:valid] }
  end
  
  def errors(data)
    @rules.map { |rule| rule.call(data) }
          .reject { |result| result[:valid] }
          .map { |result| result[:error] }
  end
end

# Build validation pipeline
user_validator = Validator.new
  .add_rule { |u| { valid: u[:name].present?, error: "Name required" } }
  .add_rule { |u| { valid: u[:email].include?('@'), error: "Invalid email" } }
  .add_rule { |u| { valid: u[:age] >= 18, error: "Must be 18+" } }
  .add_rule { |u| { valid: u[:password].length >= 6, error: "Password too short" } }

valid_user = { name: "Alice", email: "alice@example.com", age: 25, password: "secret123" }
invalid_user = { name: "Bob", email: "bob", age: 16, password: "123" }

puts "Valid user valid? #{user_validator.validate(valid_user)}"
puts "Invalid user valid? #{user_validator.validate(invalid_user)}"
puts "Invalid user errors: #{user_validator.errors(invalid_user)}"

# ============================================
# 5. PERFORMANCE AND BEST PRACTICES
# ============================================
puts "\n" + "=" * 60
puts "5. PERFORMANCE AND BEST PRACTICES"
puts "=" * 60

puts <<~PERFORMANCE

  ENUMERABLE PERFORMANCE CONSIDERATIONS:
  
  1. LAZY EVALUATION
     • Use for large datasets or infinite sequences
     • Avoids creating intermediate arrays
     • Best when you only need a subset of results
  
  2. MEMORY USAGE
     • Eager evaluation creates intermediate arrays
     • Chain operations can create many temporary objects
     • Use .lazy for memory-intensive operations
  
  3. SPEED
     • Built-in methods are implemented in C (fast)
     • Custom blocks are slower than built-in methods
     • Use symbol to proc (&:method) for conciseness
  
  4. READABILITY
     • Chain methods for clarity
     • Break complex chains into named variables
     • Use descriptive intermediate variables

PERFORMANCE

# ----- Benchmarking different approaches -----
puts "\n--- Performance comparison of approaches ---"

require 'benchmark'

large_array = (1..100_000).to_a

Benchmark.bm(15) do |x|
  x.report("Eager:") do
    result = large_array
      .map { |n| n * 2 }
      .select(&:even?)
      .reject { |n| n > 100_000 }
      .first(10)
  end
  
  x.report("Lazy:") do
    result = large_array
      .lazy
      .map { |n| n * 2 }
      .select(&:even?)
      .reject { |n| n > 100_000 }
      .first(10)
  end
  
  x.report("Each:") do
    result = []
    large_array.each do |n|
      val = n * 2
      break if result.size >= 10
      result << val if val.even? && val <= 100_000
    end
  end
end

# ----- Common pitfalls -----
puts "\n--- Common pitfalls and solutions ---"

# Pitfall 1: Modifying collection while iterating
puts "\nPitfall 1: Modifying while iterating"
numbers = [1, 2, 3, 4, 5]

# BAD - This will cause unexpected behavior
begin
  numbers.each do |n|
    numbers.delete(n) if n.even?
  end
  puts "After bad delete: #{numbers}"
rescue => e
  puts "Error: #{e.message}"
end

# GOOD - Use reject! or select!
numbers = [1, 2, 3, 4, 5]
numbers.reject!(&:even?)
puts "After proper delete: #{numbers}"

# Pitfall 2: Forgetting to return enumerator
puts "\nPitfall 2: Forgetting to return enumerator"

class BadEnumerable
  include Enumerable
  
  def each
    # Forgot to handle block_given? case
    [1, 2, 3].each { |n| yield n }
  end
end

class GoodEnumerable
  include Enumerable
  
  def each
    return to_enum(:each) unless block_given?
    [1, 2, 3].each { |n| yield n }
  end
end

bad = BadEnumerable.new
good = GoodEnumerable.new

begin
  bad.map { |n| n * 2 }
rescue LocalJumpError => e
  puts "Bad enumerator error: #{e.message}"
end

good_result = good.map { |n| n * 2 }
puts "Good enumerator result: #{good_result}"

# Pitfall 3: Unnecessary intermediate arrays
puts "\nPitfall 3: Unnecessary intermediate arrays"

def process_data_bad(data)
  data.map { |n| n * 2 }
      .select { |n| n > 10 }
      .reject { |n| n.even? }
      .first(5)
end

def process_data_good(data)
  data.lazy
      .map { |n| n * 2 }
      .select { |n| n > 10 }
      .reject(&:even?)
      .first(5)
end

data = (1..10_000).to_a
puts "Bad approach creates many arrays, good approach is lazy"

# ============================================
# 6. REAL-WORLD EXAMPLES
# ============================================
puts "\n" + "=" * 60
puts "6. REAL-WORLD EXAMPLES"
puts "=" * 60

# ----- Log file analysis -----
puts "\n--- Log file analysis pipeline ---"

# Generate sample log
logs = [
  "2024-01-01 10:00:00 INFO User logged in: alice",
  "2024-01-01 10:01:00 INFO User logged in: bob",
  "2024-01-01 10:02:00 ERROR Database connection failed",
  "2024-01-01 10:03:00 INFO User logged out: alice",
  "2024-01-01 10:04:00 WARN Slow query detected: 2.5s",
  "2024-01-01 10:05:00 ERROR Timeout occurred",
  "2024-01-01 10:06:00 INFO User logged in: charlie",
  "2024-01-01 10:07:00 WARN Memory usage high",
  "2024-01-01 10:08:00 INFO User logged out: bob"
]

class LogAnalyzer
  def initialize(logs)
    @logs = logs
  end
  
  def analyze
    {
      by_level: count_by_level,
      errors: extract_errors,
      warnings: extract_warnings,
      user_activity: user_login_activity,
      timeline: timeline_summary
    }
  end
  
  private
  
  def parse_logs
    @logs.lazy.map do |log|
      timestamp, level, *message = log.split(' ')
      { timestamp: timestamp, level: level, message: message.join(' ') }
    end
  end
  
  def count_by_level
    parse_logs.group_by { |log| log[:level] }
              .map { |level, logs| [level, logs.size] }
              .to_h
  end
  
  def extract_errors
    parse_logs.select { |log| log[:level] == "ERROR" }
              .map { |log| log[:message] }
              .to_a
  end
  
  def extract_warnings
    parse_logs.select { |log| log[:level] == "WARN" }
              .map { |log| log[:message] }
              .to_a
  end
  
  def user_login_activity
    parse_logs.select { |log| log[:message].include?("logged in") }
              .map { |log| log[:message].match(/logged in: (\w+)/)[1] }
              .to_a
  end
  
  def timeline_summary
    parse_logs.map { |log| "#{log[:timestamp]} [#{log[:level]}] #{log[:message][0..30]}..." }
              .to_a
  end
end

analyzer = LogAnalyzer.new(logs)
results = analyzer.analyze

puts "Log Analysis Results:"
puts "  By level: #{results[:by_level]}"
puts "  Errors: #{results[:errors]}"
puts "  Warnings: #{results[:warnings]}"
puts "  User logins: #{results[:user_activity]}"
puts "  Timeline (first 3):"
  results[:timeline].first(3).each { |t| puts "    #{t}" }

# ----- ETL Pipeline with enumerables -----
puts "\n--- ETL Pipeline ---"

# Extract
def extract_data
  [
    { id: 1, name: "Product A", price: 29.99, category: "Electronics", stock: 150 },
    { id: 2, name: "Product B", price: 49.99, category: "Clothing", stock: 80 },
    { id: 3, name: "Product C", price: 19.99, category: "Electronics", stock: 200 },
    { id: 4, name: "Product D", price: 99.99, category: "Home", stock: 45 },
    { id: 5, name: "Product E", price: 14.99, category: "Clothing", stock: 300 }
  ]
end

# Transform
def transform_data(data)
  data.lazy
      .map do |product|
        product[:price_with_tax] = (product[:price] * 1.1).round(2)
        product[:total_value] = product[:stock] * product[:price]
        product[:status] = case product[:stock]
                          when 0 then "out_of_stock"
                          when 1..50 then "low_stock"
                          else "in_stock"
                          end
        product
      end
      .to_a
end

# Load
def load_data(data, format: :summary)
  case format
  when :summary
    {
      total_products: data.size,
      categories: data.group_by { |p| p[:category] }
                      .map { |cat, prods| [cat, prods.size] }
                      .to_h,
      total_value: data.sum { |p| p[:total_value] },
      low_stock: data.select { |p| p[:status] == "low_stock" }
                     .map { |p| p[:name] }
  end
  when :detailed
    data
  end
end

# Run ETL pipeline
extracted = extract_data
transformed = transform_data(extracted)
loaded = load_data(transformed, format: :summary)

puts "\nETL Results:"
puts "  Total products: #{loaded[:total_products]}"
puts "  Categories: #{loaded[:categories]}"
puts "  Total value: $#{loaded[:total_value].round(2)}"
puts "  Low stock items: #{loaded[:low_stock]}"

# ----- Functional data validation pipeline -----
puts "\n--- Functional validation pipeline ---"

class ValidationPipeline
  def initialize(data)
    @data = data
    @validations = []
  end
  
  def validate(rule, error_message)
    @validations << { rule: rule, error: error_message }
    self
  end
  
  def run
    errors = @validations.each_with_object([]) do |validation, errs|
      unless validation[:rule].call(@data)
        errs << validation[:error]
      end
    end
    
    {
      valid: errors.empty?,
      errors: errors,
      data: @data
    }
  end
end

# Define validation rules
user_data = {
  name: "Alice",
  email: "alice@example.com",
  age: 25,
  password: "secret123",
  preferences: { theme: "dark", notifications: true }
}

result = ValidationPipeline.new(user_data)
  .validate(->(u) { u[:name].present? }, "Name is required")
  .validate(->(u) { u[:email].include?('@') }, "Invalid email format")
  .validate(->(u) { u[:age] >= 18 }, "Must be at least 18 years old")
  .validate(->(u) { u[:password].length >= 6 }, "Password must be at least 6 characters")
  .validate(->(u) { u[:preferences][:theme].in?(["light", "dark"]) }, "Invalid theme")
  .run

puts "\nValidation result:"
puts "  Valid: #{result[:valid]}"
puts "  Errors: #{result[:errors]}" unless result[:valid]

# ============================================
# 7. SUMMARY AND BEST PRACTICES
# ============================================
puts "\n" + "=" * 60
puts "7. SUMMARY AND BEST PRACTICES"
puts "=" * 60

puts <<~SUMMARY

  ENUMERABLE BEST PRACTICES:
  
  1. CHOOSE THE RIGHT METHOD
     • map: transform each element
     • select: filter elements
     • reduce: accumulate values
     • each: iterate with side effects
  
  2. USE LAZY ENUMERATORS WISELY
     • For infinite sequences
     • For large datasets where you only need first few
     • To avoid intermediate array creation
     • Not beneficial for small collections
  
  3. COMPOSE PIPELINES CLEANLY
     • Chain methods for readability
     • Break complex chains into named steps
     • Use intermediate variables when helpful
  
  4. CONSIDER PERFORMANCE
     • Built-in methods are faster than custom
     • Lazy evaluation has overhead
     • Benchmark when performance matters
  
  5. AVOID SIDE EFFECTS
     • Use pure transformations when possible
     • Avoid modifying original data
     • Keep functions focused and testable
  
  6. LEVERAGE ENUMERATOR METHODS
     • each_with_index
     • with_index
     • cycle
     • each_cons
     • each_slice

SUMMARY

# Final demonstration: Complex pipeline example
puts "\n--- Complex real-world pipeline ---"

# Process sales data with multiple transformations
sales_data = [
  { date: "2024-01-01", product: "Laptop", category: "Electronics", amount: 1200, quantity: 2, region: "North" },
  { date: "2024-01-01", product: "Mouse", category: "Electronics", amount: 30, quantity: 5, region: "South" },
  { date: "2024-01-02", product: "Desk", category: "Furniture", amount: 200, quantity: 1, region: "North" },
  { date: "2024-01-02", product: "Monitor", category: "Electronics", amount: 300, quantity: 3, region: "East" },
  { date: "2024-01-03", product: "Chair", category: "Furniture", amount: 90, quantity: 4, region: "West" },
  { date: "2024-01-03", product: "Keyboard", category: "Electronics", amount: 80, quantity: 2, region: "North" },
  { date: "2024-01-04", product: "Laptop", category: "Electronics", amount: 1200, quantity: 1, region: "South" },
  { date: "2024-01-04", product: "Mouse", category: "Electronics", amount: 30, quantity: 10, region: "East" },
  { date: "2024-01-05", product: "Desk", category: "Furniture", amount: 200, quantity: 2, region: "West" }
]

# Comprehensive sales analysis pipeline
sales_analysis = sales_data
  .group_by { |sale| sale[:date] }
  .map { |date, sales| 
    {
      date: date,
      total_sales: sales.sum { |s| s[:amount] * s[:quantity] },
      total_quantity: sales.sum { |s| s[:quantity] },
      categories: sales.group_by { |s| s[:category] }
                        .map { |cat, items| 
                          [cat, items.sum { |i| i[:quantity] }] 
                        }.to_h,
      top_product: sales.max_by { |s| s[:amount] * s[:quantity] }[:product]
    }
  }
  .sort_by { |day| day[:date] }
  .each_with_index
  .map { |day, idx| 
    day[:day_number] = idx + 1
    day
  }

puts "Sales Analysis by Day:"
sales_analysis.each do |day|
  puts "\n  Day #{day[:day_number]} (#{day[:date]}):"
  puts "    Total sales: $#{day[:total_sales]}"
  puts "    Total quantity: #{day[:total_quantity]}"
  puts "    Categories: #{day[:categories]}"
  puts "    Top product: #{day[:top_product]}"
end

# Overall statistics
overall = {
  total_revenue: sales_data.sum { |s| s[:amount] * s[:quantity] },
  total_items: sales_data.sum { |s| s[:quantity] },
  category_breakdown: sales_data.group_by { |s| s[:category] }
                                 .map { |cat, items| 
                                   [cat, items.sum { |i| i[:quantity] }] 
                                 }.to_h,
  region_breakdown: sales_data.group_by { |s| s[:region] }
                              .map { |region, items|
                                [region, items.sum { |i| i[:amount] * i[:quantity] }]
                              }.to_h,
  best_selling_product: sales_data.group_by { |s| s[:product] }
                                  .map { |product, items|
                                    [product, items.sum { |i| i[:quantity] }]
                                  }.max_by { |_, qty| qty }[0]
}

puts "\n" + "=" * 40
puts "Overall Statistics:"
puts "  Total Revenue: $#{overall[:total_revenue]}"
puts "  Total Items Sold: #{overall[:total_items]}"
puts "  Category Breakdown: #{overall[:category_breakdown]}"
puts "  Region Revenue: #{overall[:region_breakdown]}"
puts "  Best Selling Product: #{overall[:best_selling_product]}"
puts "=" * 40

puts "\n" + "=" * 60
puts "END OF ENUMERABLES & FUNCTIONAL PATTERNS DEEP DIVE"
puts "=" * 60