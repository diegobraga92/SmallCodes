# ============================================
# RUBY LANGUAGE BASICS - COMPREHENSIVE GUIDE
# ============================================

# ============================================
# 1. SYNTAX, VARIABLES, AND CONSTANTS
# ============================================

# Comments start with # - everything after is ignored

# Statements don't need semicolons (though they can be used)
puts "Hello, World!"  # This prints to console with newline
print "No newline"    # This prints without newline

# VARIABLES
# Local variables - start with lowercase or _
name = "Alice"
age = 30
_score = 95  # Underscore is valid start

# Reassigning variables
age = 31  # Now age is 31

# Parallel assignment
a, b, c = 1, 2, 3  # a=1, b=2, c=3

# Swap variables without temp variable
x = 5
y = 10
x, y = y, x  # Now x=10, y=5

# CONSTANTS - start with capital letter
PI = 3.14159
MAX_USERS = 100

# Ruby warns but doesn't error if you change a constant
# Try to avoid this - constants should... be constant!
PI = 3.14  # Warning: already initialized constant

# Global variables - start with $ (avoid these generally)
$global_counter = 0

# Instance variables - start with @ (used in classes)
@user_name = "Bob"

# Class variables - start with @@ (used in classes)
@@total_instances = 0

# Variable interpolation in strings (only works with double quotes)
puts "Hello, #{name}! You are #{age} years old."
# Single quotes don't interpolate
puts 'Hello, #{name}!'  # Prints literally: Hello, #{name}!

# ============================================
# 2. PRIMITIVE TYPES
# ============================================

# In Ruby, almost everything is an object!

# STRINGS
greeting = "Hello"
multi_line = """
This is a
multi-line
string
"""

# String operations
puts greeting.length        # => 5
puts greeting.upcase        # => "HELLO"
puts greeting.downcase      # => "hello"
puts greeting.reverse       # => "olleH"
puts greeting.include?("ll") # => true
puts greeting * 3            # => "HelloHelloHello"

# String concatenation
first = "Hello"
last = "World"
full = first + " " + last    # => "Hello World"

# String interpolation (already seen)
age = 25
puts "I am #{age} years old"  # => "I am 25 years old"

# INTEGERS
count = 42
negative = -15
large = 1_000_000  # Underscores for readability (same as 1000000)

# Integer methods
puts count.even?      # => true
puts count.odd?       # => false
puts count.next       # => 43 (same as count + 1)
puts count.to_s       # => "42" (convert to string)

# Different number bases
binary = 0b1010       # 10 in decimal
octal = 012           # 10 in decimal (leading zero)
hex = 0xA             # 10 in decimal

# FLOATS (decimal numbers)
price = 19.99
temperature = -5.5
scientific = 2.5e3    # 2500.0

# Float operations
puts price.round       # => 20
puts price.floor       # => 19
puts price.ceil        # => 20

# Watch out for float precision issues!
puts 0.1 + 0.2         # => 0.30000000000000004 (not exactly 0.3!)

# BOOLEANS
is_active = true
is_deleted = false

# Everything in Ruby is truthy except false and nil
# So these are all considered "truthy" in conditionals:
truthy_examples = [0, "", [], {}, "false", nil.nil?]

# NIL (represents nothing/absence)
empty_value = nil
puts empty_value.nil?  # => true

# ============================================
# 3. CONTROL FLOW
# ============================================

# IF STATEMENTS
age = 18

if age >= 18
  puts "You can vote"
end

# One-line if (modifier form)
puts "You're an adult" if age >= 18

# IF-ELSE
temperature = 25

if temperature > 30
  puts "It's hot!"
elsif temperature > 20
  puts "It's warm"
else
  puts "It's cool"
end

# UNLESS (opposite of if)
is_weekend = false

unless is_weekend
  puts "Time to work!"
end

# One-line unless
puts "Sleep in!" unless is_weekend

# TERNARY OPERATOR (inline if-else)
status = age >= 18 ? "adult" : "minor"
puts status

# CASE STATEMENTS (like switch in other languages)
grade = 'B'

case grade
when 'A'
  puts "Excellent!"
when 'B'
  puts "Good job!"
when 'C'
  puts "Fair"
else
  puts "Need improvement"
end

# Case with ranges
score = 85

case score
when 90..100
  puts "A"
when 80...90  # Three dots excludes the end (90)
  puts "B"
when 70...80
  puts "C"
else
  puts "F"
end

# Case with multiple conditions
car = "Tesla"

case car
when "Toyota", "Honda", "Nissan"
  puts "Japanese car"
when "Ford", "Chevrolet"
  puts "American car"
when "Tesla"
  puts "Electric car"
else
  puts "Unknown origin"
end

# LOOPS

# WHILE loop
counter = 1
while counter <= 5
  puts "Count: #{counter}"
  counter += 1  # No ++ operator in Ruby!
end

# UNTIL loop (opposite of while)
counter = 1
until counter > 5
  puts "Until count: #{counter}"
  counter += 1
end

# FOR loop (less common in Ruby, but works)
for i in 1..5
  puts "For loop: #{i}"
end

# LOOP method (infinite loop unless broken)
counter = 1
loop do
  puts "Loop iteration: #{counter}"
  counter += 1
  break if counter > 3
end

# NEXT (skip iteration) and BREAK (exit loop)
(1..10).each do |num|
  next if num.even?   # Skip even numbers
  puts "Odd: #{num}"
  break if num == 5   # Stop at 5
end

# TIMES loop
3.times { |i| puts "Time #{i}" }

# UPTO and DOWNTO
1.upto(3) { |i| puts "Upto: #{i}" }
5.downto(1) { |i| puts "Downto: #{i}" }

# ============================================
# 4. METHODS (FUNCTIONS)
# ============================================

# Basic method definition
def greet
  puts "Hello!"
end

# Call the method
greet

# Method with parameters
def greet_person(name)
  puts "Hello, #{name}!"
end

greet_person("Alice")

# Method with default parameters
def greet_with_title(name, title = "Mr.")
  puts "Hello, #{title} #{name}!"
end

greet_with_title("Smith")        # => "Hello, Mr. Smith!"
greet_with_title("Jones", "Ms.") # => "Hello, Ms. Jones!"

# Method with explicit return
def add(a, b)
  return a + b  # Explicit return
end

puts add(5, 3)  # => 8

# Implicit return (last evaluated expression)
def multiply(a, b)
  a * b  # Ruby returns the last expression automatically
end

puts multiply(4, 3)  # => 12

# Method with multiple parameters and hash (common pattern)
def create_user(name, options = {})
  age = options[:age] || 18  # Default age
  city = options[:city] || "Unknown"
  
  puts "Created user #{name}, age #{age}, from #{city}"
end

create_user("Bob", { age: 25, city: "NYC" })
# Ruby allows omitting braces when hash is last argument
create_user("Alice", age: 30, city: "Boston")

# Method with variable number of arguments (*splat)
def sum(*numbers)
  total = 0
  numbers.each { |n| total += n }
  total
end

puts sum(1, 2, 3, 4, 5)  # => 15

# Method with keyword arguments (Ruby 2.0+)
def introduce(name:, age:, city: "Unknown")
  puts "#{name} is #{age} years old from #{city}"
end

introduce(name: "Charlie", age: 28)
introduce(name: "Diana", age: 32, city: "Chicago")

# Predicate methods (end with ?) return boolean
def adult?(age)
  age >= 18
end

puts adult?(20)  # => true
puts adult?(15)  # => false

# Dangerous methods (end with !) often modify the object
text = "hello"
puts text.upcase    # => "HELLO" (returns new string)
puts text           # => "hello" (original unchanged)

puts text.upcase!   # => "HELLO" (modifies original)
puts text           # => "HELLO" (original changed!)

# Method aliases
def calculate_total(price, tax)
  price + tax
end

alias total_cost calculate_total  # Now total_cost does same thing
puts total_cost(100, 10)  # => 110

# ============================================
# 5. BLOCKS AND BASIC ITERATION
# ============================================

# BLOCKS: chunks of code that can be passed to methods
# Two syntax styles: braces {} for single line, do/end for multi-line

# Simple block with braces
3.times { puts "Hello from block" }

# Block with do/end (for multi-line)
3.times do
  puts "Multi-line"
  puts "block example"
end

# Block with parameters
[1, 2, 3].each do |number|
  puts "Number: #{number}"
end

# Single-line block with parameter
[1, 2, 3].each { |n| puts "Num: #{n}" }

# BASIC ITERATION METHODS

# EACH - iterate through collection, returns original collection
puts "\n--- EACH ---"
numbers = [1, 2, 3, 4, 5]
numbers.each do |num|
  puts "Each: #{num}"
end
# numbers is unchanged

# EACH with index
puts "\n--- EACH WITH INDEX ---"
fruits = ["apple", "banana", "cherry"]
fruits.each_with_index do |fruit, index|
  puts "#{index}: #{fruit}"
end

# MAP (aka COLLECT) - transforms each element, returns new array
puts "\n--- MAP ---"
numbers = [1, 2, 3, 4, 5]
squared = numbers.map { |n| n * n }
puts "Original: #{numbers}"  # => [1, 2, 3, 4, 5]
puts "Squared: #{squared}"   # => [1, 4, 9, 16, 25]

# Map with more complex transformation
names = ["alice", "bob", "charlie"]
capitalized = names.map do |name|
  name.capitalize  # First letter uppercase
end
puts capitalized  # => ["Alice", "Bob", "Charlie"]

# SELECT (aka FIND_ALL) - filters elements, returns new array
puts "\n--- SELECT ---"
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = numbers.select { |n| n.even? }
puts "Even: #{even_numbers}"  # => [2, 4, 6]

# Select with more complex condition
words = ["cat", "elephant", "dog", "hippopotamus", "bird"]
long_words = words.select { |word| word.length > 5 }
puts "Long words: #{long_words}"  # => ["elephant", "hippopotamus"]

# REJECT - opposite of select
odd_numbers = numbers.reject { |n| n.even? }
puts "Odd: #{odd_numbers}"  # => [1, 3, 5]

# COMBINING ITERATORS
puts "\n--- COMBINING ITERATORS ---"
numbers = [1, 2, 3, 4, 5, 6]

# Get squares of even numbers
result = numbers
  .select { |n| n.even? }  # First filter
  .map { |n| n * n }       # Then transform

puts "Squares of evens: #{result}"  # => [4, 16, 36]

# YIELD - calling blocks from custom methods
puts "\n--- CUSTOM METHODS WITH BLOCKS ---"

def repeat_three_times
  yield if block_given?  # Only yield if block provided
end

repeat_three_times { puts "Called with block!" }
# This won't error because we check block_given?

def perform_operation(x, y)
  if block_given?
    yield(x, y)
  else
    x + y  # Default behavior
  end
end

puts perform_operation(5, 3)                     # => 8 (default)
puts perform_operation(5, 3) { |a, b| a * b }    # => 15
puts perform_operation(5, 3) { |a, b| a - b }    # => 2

# &block syntax - capture block as a Proc
def math_operation(a, b, &operation)
  if operation
    operation.call(a, b)
  else
    "No operation given"
  end
end

puts math_operation(10, 5) { |x, y| x / y }  # => 2

# Block as a variable
addition = Proc.new { |x, y| x + y }
puts addition.call(3, 4)  # => 7

multiplication = ->(x, y) { x * y }  # Lambda syntax
puts multiplication.call(3, 4)       # => 12

# MORE USEFUL ENUMERABLE METHODS

# FIND/DETECT - returns first matching element
puts "\n--- FIND ---"
numbers = [1, 2, 3, 4, 5]
first_even = numbers.find { |n| n.even? }
puts "First even: #{first_even}"  # => 2

# ANY? - returns true if any element matches
puts numbers.any? { |n| n > 4 }    # => true
puts numbers.any? { |n| n > 10 }   # => false

# ALL? - returns true if all elements match
puts numbers.all? { |n| n > 0 }    # => true
puts numbers.all? { |n| n.even? }  # => false

# NONE? - returns true if no elements match
puts numbers.none? { |n| n > 10 }  # => true

# REDUCE/INJECT - accumulate value
sum = numbers.reduce(0) { |total, n| total + n }
puts "Sum: #{sum}"  # => 15

# Shortcut syntax
product = numbers.reduce(:*)  # Multiply all
puts "Product: #{product}"    # => 120

# Working with hashes
puts "\n--- HASH ITERATION ---"
person = { name: "John", age: 30, city: "London" }

person.each do |key, value|
  puts "#{key}: #{value}"
end

# Transform hash keys/values
upgraded = person.map { |k, v| [k.to_s.upcase, v] }.to_h
puts upgraded  # => {"NAME"=>"John", "AGE"=>30, "CITY"=>"London"}

# RANGES with iterators
puts "\n--- RANGES ---"
(1..5).each { |i| print "#{i} " }  # => 1 2 3 4 5 (inclusive)
puts
(1...5).each { |i| print "#{i} " } # => 1 2 3 4 (exclusive)

# ============================================
# PUTTING IT ALL TOGETHER - EXAMPLE PROGRAM
# ============================================

puts "\n" + "="*40
puts "COMPREHENSIVE EXAMPLE"
puts "="*40

# A small program that processes student grades
class GradeProcessor
  PASSING_GRADE = 60  # Constant
  
  def initialize(students_data)
    @students = students_data  # Instance variable
  end
  
  def calculate_average
    total = @students.reduce(0) do |sum, student|
      sum + student[:grade]
    end
    total.to_f / @students.length
  end
  
  def passing_students
    @students.select { |s| s[:grade] >= PASSING_GRADE }
  end
  
  def failing_students
    @students.reject { |s| s[:grade] >= PASSING_GRADE }
  end
  
  def print_report
    puts "GRADE REPORT"
    puts "-" * 20
    
    @students.each do |student|
      status = student[:grade] >= PASSING_GRADE ? "PASS" : "FAIL"
      puts "#{student[:name]}: #{student[:grade]} - #{status}"
    end
    
    puts "\nClass Average: #{calculate_average.round(1)}"
    puts "Passing: #{passing_students.count}"
    puts "Failing: #{failing_students.count}"
  end
  
  def award_bonus(extra_points)
    @students.map! do |student|
      # Create new hash with updated grade (don't mutate original)
      student.merge(grade: student[:grade] + extra_points)
    end
  end
end

# Create some student data
students = [
  { name: "Alice", grade: 85 },
  { name: "Bob", grade: 45 },
  { name: "Charlie", grade: 72 },
  { name: "Diana", grade: 90 },
  { name: "Eve", grade: 58 }
]

processor = GradeProcessor.new(students)
processor.print_report

puts "\nAfter bonus points..."
processor.award_bonus(5)
processor.print_report

# ============================================
# COMMON PITFALLS AND BEST PRACTICES
# ============================================

puts "\n" + "="*40
puts "COMMON PITFALLS AND TIPS"
puts "="*40

# 1. Variable scope in blocks
x = 10
3.times do |i|
  x = i  # This modifies the outer x!
  y = 20 # This is only visible inside block
end
puts "x: #{x}"  # => 2 (modified)
# puts y  # Would error - y doesn't exist here

# 2. Block parameters shadow outer variables
value = "outer"
[1, 2].each do |value|  # This parameter shadows outer variable
  puts "Inner: #{value}"
end
puts "Outer: #{value}"  # => "outer" (unchanged)

# 3. Return from blocks
def test_block
  [1, 2, 3].each do |n|
    return "Returned from block" if n == 2  # Returns from method!
  end
  "Never reached if block returns"
end

puts test_block  # => "Returned from block"

# 4. Use descriptive variable names in blocks
# Good:
[1, 2, 3].map { |number| number * 2 }

# Avoid:
[1, 2, 3].map { |x| x * 2 }  # x is too vague

# 5. Prefer each over for loops (more Ruby-ish)
# Good:
[1, 2, 3].each { |n| puts n }

# Less common:
for n in [1, 2, 3]  # Works but not idiomatic
  puts n
end

# 6. Use unless carefully - don't overcomplicate
# Good:
puts "Done" unless processing?

# Avoid (harder to read):
unless !processing? && !completed?  # Double negatives!
  puts "???"
end

# 7. Constants can be changed (but shouldn't be)
MY_CONSTANT = [1, 2, 3]
MY_CONSTANT << 4  # This works! (modifying, not reassigning)
puts MY_CONSTANT  # => [1, 2, 3, 4]
# MY_CONSTANT = [5, 6, 7]  # This warns (reassignment)

puts "\nRuby basics complete! 🎉"