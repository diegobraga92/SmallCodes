# ============================================
# RUBY COMMAND LINE & TOOLING DEMONSTRATION
# ============================================

# This file demonstrates various ways to run Ruby code,
# use interactive consoles, and debug effectively.

# ============================================
# 1. RUNNING RUBY SCRIPTS
# ============================================
puts "=" * 60
puts "1. RUNNING RUBY SCRIPTS"
puts "=" * 60

puts <<~USAGE

  WAYS TO RUN RUBY SCRIPTS:
  
  1. Basic execution:
     $ ruby script.rb
     
  2. With shebang line (#!/usr/bin/env ruby):
     $ chmod +x script.rb
     $ ./script.rb
     
  3. One-liner execution:
     $ ruby -e "puts 'Hello World'"
     
  4. Run with warnings enabled:
     $ ruby -w script.rb
     
  5. Run with debugging:
     $ ruby -d script.rb
     
  6. Check syntax without running:
     $ ruby -c script.rb
     
  7. Load path modification:
     $ ruby -Ilib script.rb
     
  8. Run with environment variables:
     $ DEBUG=true ruby script.rb

USAGE

# Demonstrate different execution modes
if __FILE__ == $PROGRAM_NAME
  puts "✅ This script is being run directly"
  puts "   File: #{__FILE__}"
  puts "   Program name: #{$PROGRAM_NAME}"
  puts "   Ruby version: #{RUBY_VERSION}"
  puts "   Ruby platform: #{RUBY_PLATFORM}"
end

# Demonstrate command-line arguments
puts "\n--- Command-line arguments ---"
puts "Arguments count: #{ARGV.length}"
puts "Arguments: #{ARGV.inspect}" if ARGV.any?
puts "To see arguments, run: ruby cli_demo.rb arg1 arg2 arg3"

# ============================================
# 2. USING IRB (INTERACTIVE RUBY)
# ============================================
puts "\n" + "=" * 60
puts "2. USING IRB (INTERACTIVE RUBY)"
puts "=" * 60

puts <<~IRB_GUIDE

  IRB COMMANDS AND TIPS:
  
  Starting IRB:
    $ irb
    $ irb --simple-prompt    # Simpler prompt
    $ irb --noecho           # Don't echo return values
    $ irb -r ./file.rb       # Load a file before starting
  
  Useful IRB Commands:
    help                    # Show help
    conf                    # Show configuration
    show_doc [method]       # Show documentation
    ls [object]             # List methods
    show_source [method]    # Show source code (if available)
    hist                    # Show command history
  
  Navigation:
    Ctrl + P / Ctrl + N     # Previous/Next command
    Ctrl + A / Ctrl + E     # Beginning/End of line
    Ctrl + R                # Search history
    Tab                     # Auto-completion
  
  Example IRB Session:
    >> name = "Ruby"
    => "Ruby"
    >> name.upcase
    => "RUBY"
    >> 10.times { |i| puts i }
    0
    1
    ...
    9
    => 10
    >> exit

IRB_GUIDE

# Demonstrate loading files in IRB
puts "\n--- Loading files in IRB ---"
puts <<~LOAD_EXAMPLE
  # Inside IRB, you can load files with:
  load 'filename.rb'     # Loads every time (good for development)
  require 'filename'     # Loads once (good for libraries)
  require_relative 'filename'  # Load relative to current file
  
  # Example:
  >> load 'cli_demo.rb'  # This would load this file
LOAD_EXAMPLE

# ============================================
# 3. USING PRY (ADVANCED DEBUGGING)
# ============================================
puts "\n" + "=" * 60
puts "3. USING PRY (ADVANCED DEBUGGING)"
puts "=" * 60

puts <<~PRY_GUIDE

  PRY - A POWERFUL ALTERNATIVE TO IRB
  
  Installation:
    $ gem install pry
    $ gem install pry-byebug  # For debugging
    $ gem install pry-doc     # For documentation
  
  Starting Pry:
    $ pry
    $ pry -r ./file.rb        # Load file before starting
  
  Essential Pry Commands:
    help                        # Show help
    ls                          # List methods/constants
    ls -M                       # List methods only
    cd [object]                 # Change context
    show-doc [method]           # Show documentation
    show-source [method]        # Show source code
    $ [command]                 # Run shell command
    !!!                         # Reset session
    exit                        # Exit pry
  
  Debugging with pry-byebug:
    binding.pry                 # Breakpoint
    next                        # Step over
    step                        # Step into
    continue                    # Continue execution
    break [line]                # Set breakpoint
    backtrace                   # Show call stack
    wtf?                        # Show exception details
  
  Example Pry Session:
    [1] pry(main)> cd Array
    [2] pry(Array):1> ls -M
    Array methods: 
      []       all?      any?     ...
    [3] pry(Array):1> cd ..
    [4] pry(main)> show-doc String#upcase
    [5] pry(main)> binding.pry  # In code, this creates breakpoint

PRY_GUIDE

# Demo method that would be used with Pry
def calculate_sum(numbers)
  # If pry is available, you could add a breakpoint here
  # binding.pry if defined?(Pry)
  
  result = numbers.reduce(0) { |sum, n| sum + n }
  result
end

puts "\n--- Pry breakpoint example ---"
puts "Add 'binding.pry' to any method for debugging:"
puts <<~PRY_EXAMPLE
  def complex_calculation(data)
    binding.pry  # Execution will pause here when running with pry
    result = data.map { |x| x * 2 }
    result.select { |x| x > 10 }
  end
PRY_EXAMPLE

# ============================================
# 4. BASIC DEBUGGING TECHNIQUES
# ============================================
puts "\n" + "=" * 60
puts "4. BASIC DEBUGGING TECHNIQUES"
puts "=" * 60

# ----- puts debugging -----
puts "\n--- puts debugging ---"

def calculate_average(numbers)
  puts "DEBUG: calculate_average called with #{numbers.inspect}"
  
  if numbers.empty?
    puts "DEBUG: Empty array detected, returning nil"
    return nil
  end
  
  sum = numbers.reduce(0) { |total, n| total + n }
  puts "DEBUG: Sum = #{sum}"
  
  average = sum.to_f / numbers.length
  puts "DEBUG: Average = #{average}"
  
  average
end

puts "\nUsing puts for debugging:"
result = calculate_average([10, 20, 30, 40])
puts "Result: #{result}"

# ----- pp (pretty print) debugging -----
puts "\n--- pp (pretty print) debugging ---"

require 'pp'

complex_data = {
  users: [
    { id: 1, name: "Alice", preferences: { theme: "dark", notifications: true } },
    { id: 2, name: "Bob", preferences: { theme: "light", notifications: false } },
    { id: 3, name: "Charlie", preferences: { theme: "auto", notifications: true } }
  ],
  metadata: {
    created_at: Time.now,
    version: "1.0.0",
    tags: ["production", "debug"]
  }
}

puts "Using puts (hard to read):"
puts complex_data

puts "\nUsing pp (pretty printed):"
pp complex_data

# ----- Custom debugging method -----
puts "\n--- Custom debug logger ---"

class DebugLogger
  attr_reader :enabled
  
  def initialize(enabled = true)
    @enabled = enabled
    @indent_level = 0
  end
  
  def enable
    @enabled = true
  end
  
  def disable
    @enabled = false
  end
  
  def log(message, level: :info)
    return unless @enabled
    
    prefix = case level
             when :debug then "🔍 DEBUG: "
             when :info  then "ℹ️  INFO: "
             when :warn  then "⚠️  WARN: "
             when :error then "❌ ERROR: "
             else "📝 LOG: "
             end
    
    puts "#{'  ' * @indent_level}#{prefix}#{message}"
  end
  
  def indent
    @indent_level += 1
    yield if block_given?
  ensure
    @indent_level -= 1
  end
end

logger = DebugLogger.new(true)

def process_order(order, logger)
  logger.log("Processing order #{order[:id]}")
  
  logger.indent do
    logger.log("Validating items...")
    
    if order[:items].empty?
      logger.log("No items found!", level: :warn)
      return false
    end
    
    logger.log("Calculating total...", level: :debug)
    total = order[:items].sum { |item| item[:price] * item[:quantity] }
    logger.log("Total: $#{total}")
    
    logger.log("Checking inventory...")
    # Simulate inventory check
    sleep(0.1)
    logger.log("Inventory check passed", level: :debug)
  end
  
  logger.log("Order #{order[:id]} processed successfully")
  true
end

order = {
  id: 12345,
  items: [
    { name: "Widget", price: 19.99, quantity: 2 },
    { name: "Gadget", price: 29.99, quantity: 1 }
  ]
}

puts "\nUsing custom debug logger:"
process_order(order, logger)

# ----- Using $DEBUG global flag -----
puts "\n--- Using $DEBUG global flag ---"

$DEBUG = true  # Set with ruby -d or $DEBUG=true

def debug_example
  puts "Debug: Entering method" if $DEBUG
  result = 10 * 5
  puts "Debug: Result = #{result}" if $DEBUG
  result
end

debug_example
puts "Set $DEBUG = true for verbose output"

# ----- Using caller for stack traces -----
puts "\n--- Using caller for stack traces ---"

def method_one
  method_two
end

def method_two
  method_three
end

def method_three
  puts "\nCurrent stack trace:"
  caller.each_with_index do |call, index|
    puts "  #{index + 1}: #{call}"
  end
end

method_one

# ----- Inspecting objects -----
puts "\n--- Object inspection methods ---"

class Person
  attr_reader :name, :age, :email
  
  def initialize(name, age, email)
    @name = name
    @age = age
    @email = email
  end
  
  def to_s
    "Person: #{@name}"
  end
  
  def inspect
    "#<Person @name=#{@name.inspect} @age=#{@age} @email=#{@email.inspect}>"
  end
end

person = Person.new("Alice", 30, "alice@example.com")

puts "puts: #{person}"           # Uses to_s
puts "p: #{person.inspect}"      # Uses inspect
puts "pp:"
pp person                        # Pretty print

# ----- Timing execution -----
puts "\n--- Timing execution ---"

def time_execution(label)
  start_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  result = yield
  end_time = Process.clock_gettime(Process::CLOCK_MONOTONIC)
  elapsed = end_time - start_time
  puts "#{label} took #{'%.3f' % elapsed} seconds"
  result
end

result = time_execution("Sleep example") do
  sleep(0.5)
  "Done"
end

# ============================================
# 5. DEBUGGING TECHNIQUES DEMONSTRATION
# ============================================
puts "\n" + "=" * 60
puts "5. DEBUGGING TECHNIQUES DEMONSTRATION"
puts "=" * 60

# Create a buggy method to debug
def buggy_calculator(prices, tax_rate = 0.1)
  # Bug: doesn't handle empty array
  # Bug: integer division instead of float
  # Bug: modifies original array
  
  puts "DEBUG: prices = #{prices.inspect}" if $DEBUG
  puts "DEBUG: tax_rate = #{tax_rate}" if $DEBUG
  
  subtotal = prices.reduce(:+)  # Bug: returns nil for empty array
  
  puts "DEBUG: subtotal = #{subtotal}" if $DEBUG
  
  tax = subtotal * tax_rate
  total = subtotal + tax
  
  # Bug: modifies original array by adding new element
  prices << total
  
  puts "DEBUG: total = #{total}" if $DEBUG
  
  total
end

# Debugging approach 1: Add debug prints
puts "\n--- Approach 1: Add debug prints ---"
begin
  result = buggy_calculator([10, 20, 30])
  puts "Result: #{result}"
  
  # This will show the bug
  result = buggy_calculator([])
  puts "Result: #{result}"
rescue => e
  puts "Error: #{e.message}"
end

# Debugging approach 2: Use pp for complex objects
puts "\n--- Approach 2: Use pp for complex objects ---"

def debug_with_pp(data)
  puts "\n=== DEBUG INFO ==="
  pp data
  puts "=================="
end

debug_with_pp({ method: "buggy_calculator", args: [10, 20, 30], result: 66 })

# Debugging approach 3: Use tap for inline debugging
puts "\n--- Approach 3: Use tap for inline debugging ---"

result = [10, 20, 30]
  .map { |n| n * 2 }
  .tap { |arr| puts "After map: #{arr.inspect}" }
  .select { |n| n > 30 }
  .tap { |arr| puts "After select: #{arr.inspect}" }
  .reduce(:+)

puts "Final result: #{result}"

# Debugging approach 4: Rescue and inspect
puts "\n--- Approach 4: Rescue and inspect errors ---"

def safe_calculator(prices, tax_rate = 0.1)
  begin
    subtotal = prices.reduce(:+)
    raise "No items to calculate" if subtotal.nil?
    
    tax = subtotal * tax_rate
    total = subtotal + tax
    
    { success: true, total: total, subtotal: subtotal, tax: tax }
  rescue => e
    { success: false, error: e.message, backtrace: e.backtrace.first(3) }
  end
end

result = safe_calculator([10, 20, 30])
pp result

result = safe_calculator([])
pp result

# ============================================
# 6. COMMAND-LINE UTILITIES
# ============================================
puts "\n" + "=" * 60
puts "6. COMMAND-LINE UTILITIES"
puts "=" * 60

# ----- ARGV parsing -----
puts "\n--- Parsing command-line arguments ---"

class ArgumentParser
  attr_reader :options, :arguments
  
  def initialize
    @options = {}
    @arguments = []
    parse
  end
  
  def parse
    ARGV.each_with_index do |arg, index|
      case arg
      when '-h', '--help'
        @options[:help] = true
      when '-v', '--verbose'
        @options[:verbose] = true
      when '-d', '--debug'
        @options[:debug] = true
      when '--file'
        @options[:file] = ARGV[index + 1] if ARGV[index + 1]
      else
        @arguments << arg unless arg.start_with?('-')
      end
    end
  end
  
  def help_text
    <<~HELP
      Usage: ruby cli_demo.rb [options] [arguments]
      
      Options:
        -h, --help      Show this help message
        -v, --verbose   Enable verbose output
        -d, --debug     Enable debug mode
        --file FILE     Specify a file to process
      
      Examples:
        ruby cli_demo.rb -v data.txt
        ruby cli_demo.rb --debug --file input.json
        ruby cli_demo.rb arg1 arg2 arg3
    HELP
  end
end

# Uncomment to test with command-line arguments
# parser = ArgumentParser.new
# if parser.options[:help]
#   puts parser.help_text
# else
#   puts "Options: #{parser.options.inspect}"
#   puts "Arguments: #{parser.arguments.inspect}"
# end

# ----- Environment variables -----
puts "\n--- Using environment variables ---"

def debug_mode?
  ENV['DEBUG'] == 'true' || ENV['RUBY_DEBUG'] == 'true'
end

def log_level
  ENV['LOG_LEVEL'] || 'info'
end

puts "DEBUG mode: #{debug_mode?}"
puts "LOG_LEVEL: #{log_level}"
puts "To set: DEBUG=true ruby cli_demo.rb"

# ----- Exit codes -----
puts "\n--- Exit codes ---"

def successful_operation
  puts "Operation completed successfully"
  exit(0)  # Success
end

def failed_operation
  puts "Operation failed"
  exit(1)  # General error
end

def usage_error
  puts "Invalid arguments"
  exit(64)  # Command line usage error
end

puts "Common exit codes:"
puts "  0 - Success"
puts "  1 - General error"
puts "  64 - Command line usage error"
puts "  65 - Data format error"
puts "  66 - Cannot open input"

# ============================================
# 7. DEBUGGING CHEAT SHEET
# ============================================
puts "\n" + "=" * 60
puts "7. DEBUGGING CHEAT SHEET"
puts "=" * 60

puts <<~CHEAT_SHEET

  QUICK DEBUGGING REFERENCE:
  
  Basic Techniques:
    puts var                 # Simple output
    p var                    # Output with inspect
    pp var                   # Pretty print
    ap var                   # Awesome print (if gem installed)
    var.inspect              # Get string representation
    var.to_s                 # String representation
    
  Inspecting Objects:
    var.class                # Show class
    var.methods              # List all methods
    var.methods - Object.methods  # List custom methods
    var.instance_variables   # List instance variables
    
  Control Flow Debugging:
    $DEBUG = true            # Enable debug mode
    warn "message"           # Print to stderr
    raise "message"          # Raise exception with message
    
  Tracing:
    caller                   # Show stack trace
    __FILE__                 # Current file
    __LINE__                 # Current line
    __method__               # Current method
    
  Execution:
    $0                       # Program name
    $$                       # Process ID
    ARGV                     # Command-line arguments
    ENV                      # Environment variables
    
  Performance:
    require 'benchmark'      # Benchmarking library
    Benchmark.measure { code }  # Measure execution time
    
  Example:
    require 'benchmark'
    time = Benchmark.measure do
      1000.times { |i| i * i }
    end
    puts time

CHEAT_SHEET

# ============================================
# 8. PRACTICAL DEBUGGING EXAMPLE
# ============================================
puts "\n" + "=" * 60
puts "8. PRACTICAL DEBUGGING EXAMPLE"
puts "=" * 60

# A more complex example with multiple bugs to debug
class ShoppingCart
  attr_reader :items
  
  def initialize
    @items = []
    @logger = DebugLogger.new(debug_mode?)
  end
  
  def add_item(product, quantity = 1)
    @logger.log("Adding #{quantity}x #{product[:name]}", level: :debug)
    
    existing_item = @items.find { |item| item[:product][:id] == product[:id] }
    
    if existing_item
      existing_item[:quantity] += quantity
      @logger.log("Updated existing item, new quantity: #{existing_item[:quantity]}", level: :debug)
    else
      @items << { product: product, quantity: quantity }
      @logger.log("Added new item", level: :debug)
    end
  end
  
  def total
    @logger.log("Calculating total for #{@items.size} items", level: :debug)
    
    subtotal = @items.sum do |item|
      price = item[:product][:price]
      quantity = item[:quantity]
      @logger.log("  #{item[:product][:name]}: #{quantity} x $#{price} = $#{price * quantity}", level: :debug)
      price * quantity
    end
    
    @logger.log("Subtotal: $#{subtotal}", level: :debug)
    
    # Apply discount if total > $100
    discount = subtotal > 100 ? subtotal * 0.1 : 0
    @logger.log("Discount: $#{discount}", level: :debug) if discount > 0
    
    tax = (subtotal - discount) * 0.1
    @logger.log("Tax: $#{tax}", level: :debug)
    
    final_total = subtotal - discount + tax
    @logger.log("Final total: $#{final_total}", level: :debug)
    
    final_total
  end
  
  def debug_info
    puts "\n=== SHOPPING CART DEBUG INFO ==="
    puts "Items count: #{@items.size}"
    puts "Total value: $#{total}"
    puts "Items:"
    @items.each do |item|
      puts "  - #{item[:product][:name]}: #{item[:quantity]} x $#{item[:product][:price]}"
    end
    puts "================================"
  end
end

# Test the shopping cart
puts "\n--- Running ShoppingCart example ---"

cart = ShoppingCart.new

products = [
  { id: 1, name: "Laptop", price: 999.99 },
  { id: 2, name: "Mouse", price: 29.99 },
  { id: 3, name: "Keyboard", price: 89.99 }
]

cart.add_item(products[0], 1)
cart.add_item(products[1], 2)
cart.add_item(products[2], 1)
cart.add_item(products[1], 1)  # Add more mice

puts "\nFinal total: $#{cart.total.round(2)}"
cart.debug_info

# ============================================
# 9. SUMMARY AND BEST PRACTICES
# ============================================
puts "\n" + "=" * 60
puts "9. DEBUGGING BEST PRACTICES SUMMARY"
puts "=" * 60

puts <<~SUMMARY

  ✅ DEBUGGING BEST PRACTICES:
  
  1. Start Simple:
     • Use puts/p to verify assumptions
     • Check method inputs and outputs
     • Verify data types with .class
  
  2. Use Proper Tools:
     • IRB for quick experiments
     • Pry for complex debugging sessions
     • Byebug for step-by-step debugging
  
  3. Write Testable Code:
     • Small, focused methods
     • Descriptive variable names
     • Single responsibility principle
  
  4. Log Strategically:
     • Log at appropriate levels (debug, info, error)
     • Include context (timestamps, IDs)
     • Don't log sensitive information
  
  5. Use Version Control:
     • Commit before major debugging
     • Use git bisect to find bugs
     • Keep debugging code separate
  
  6. Learn from Errors:
     • Read the full error message
     • Look at the stack trace
     • Understand the root cause
  
  7. Systematic Approach:
     • Reproduce the bug consistently
     • Isolate the problem area
     • Test one hypothesis at a time
     • Verify the fix works
  
  8. Document Debug Sessions:
     • Note what you tried
     • Record what worked
     • Share learnings with team

SUMMARY

puts "\n" + "=" * 60
puts "END OF COMMAND LINE & TOOLING DEMONSTRATION"
puts "=" * 60