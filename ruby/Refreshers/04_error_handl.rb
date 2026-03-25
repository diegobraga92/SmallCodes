# ============================================
# RUBY ERROR HANDLING DEMONSTRATION
# ============================================

# ============================================
# 1. BASIC EXCEPTION HANDLING
# ============================================
puts "=" * 60
puts "1. BASIC EXCEPTION HANDLING (begin/rescue/ensure)"
puts "=" * 60

# ----- Basic begin/rescue block -----
puts "\n--- Basic rescue ---"

begin
  # Code that might raise an exception
  result = 10 / 0
  puts "This line will never execute"
rescue
  # This block executes when any exception occurs
  puts "❌ An error occurred: Division by zero"
end

# ----- Rescuing specific exception types -----
puts "\n--- Rescuing specific exceptions ---"

begin
  # Try to open a file that doesn't exist
  File.open("non_existent_file.txt", "r")
rescue Errno::ENOENT
  puts "❌ File not found error"
rescue Errno::EACCES
  puts "❌ Permission denied error"
rescue StandardError => e
  puts "❌ Generic error: #{e.message}"
end

# ----- Accessing exception object -----
puts "\n--- Accessing exception details ---"

begin
  numbers = [1, 2, 3]
  value = numbers[5] / 0  # This will raise ZeroDivisionError
rescue ZeroDivisionError => e
  puts "❌ Exception class: #{e.class}"
  puts "❌ Exception message: #{e.message}"
  puts "❌ Backtrace (first 3 lines):"
  e.backtrace.first(3).each { |line| puts "    #{line}" }
end

# ----- Using retry -----
puts "\n--- Using retry ---"

attempts = 0
begin
  attempts += 1
  puts "Attempt ##{attempts}"
  
  # Simulate an unreliable operation
  if attempts < 3
    raise "Temporary failure"
  end
  
  puts "✅ Operation succeeded after #{attempts} attempts"
rescue => e
  puts "  ⚠️  #{e.message}"
  if attempts < 3
    puts "  🔄 Retrying..."
    retry  # This will re-execute the begin block
  else
    puts "  ❌ Giving up after #{attempts} attempts"
  end
end

# ----- Using ensure -----
puts "\n--- Using ensure (cleanup code) ---"

file = nil
begin
  file = File.open("ensure_test.txt", "w")
  file.puts "Writing some content"
  # Simulate an error
  raise "Something went wrong while writing"
  file.puts "This line won't execute"
rescue => e
  puts "❌ Error occurred: #{e.message}"
ensure
  # This block ALWAYS executes, even if an error occurred
  if file && !file.closed?
    file.close
    puts "✅ File was closed in ensure block"
  end
  puts "✅ Cleanup completed"
end

# ----- Multiple rescue conditions in one line -----
puts "\n--- Multiple rescue conditions ---"

def safe_division(a, b)
  a / b
rescue ZeroDivisionError
  "Cannot divide by zero"
rescue TypeError
  "Invalid type provided"
rescue => e
  "Unexpected error: #{e.message}"
end

puts "10 / 2 = #{safe_division(10, 2)}"
puts "10 / 0 = #{safe_division(10, 0)}"
puts "10 / 'a' = #{safe_division(10, 'a')}"

# ============================================
# 2. RAISING CUSTOM ERRORS
# ============================================
puts "\n" + "=" * 60
puts "2. RAISING CUSTOM ERRORS"
puts "=" * 60

# ----- Defining custom error classes -----
puts "\n--- Defining custom error classes ---"

# Custom error class inheriting from StandardError
class ValidationError < StandardError
  attr_reader :field, :invalid_value
  
  def initialize(message, field = nil, invalid_value = nil)
    super(message)
    @field = field
    @invalid_value = invalid_value
  end
  
  def details
    "Field '#{@field}' with value '#{@invalid_value}' is invalid"
  end
end

class AuthenticationError < StandardError; end
class AuthorizationError < StandardError; end
class RateLimitError < StandardError; end

# ----- Raising custom errors -----
puts "\n--- Raising custom errors ---"

class UserService
  MAX_LOGIN_ATTEMPTS = 3
  
  def initialize
    @login_attempts = {}
  end
  
  def authenticate(username, password)
    # Validate input
    raise ValidationError.new("Username cannot be empty", :username, username) if username.to_s.strip.empty?
    raise ValidationError.new("Password cannot be empty", :password, "***hidden***") if password.to_s.strip.empty?
    
    # Check rate limiting
    @login_attempts[username] ||= 0
    @login_attempts[username] += 1
    
    if @login_attempts[username] > MAX_LOGIN_ATTEMPTS
      raise RateLimitError, "Too many login attempts for user: #{username}"
    end
    
    # Simulate authentication (always fails for demo)
    if username == "admin" && password == "secret"
      puts "✅ Authentication successful"
      @login_attempts[username] = 0  # Reset on success
      return true
    else
      raise AuthenticationError, "Invalid username or password"
    end
  end
  
  def perform_admin_action(user)
    raise AuthorizationError, "User is not authorized for admin actions" unless user == "admin"
    puts "✅ Admin action performed"
  end
end

# ----- Using custom errors -----
puts "\n--- Using custom errors ---"

service = UserService.new

# Test various scenarios
test_cases = [
  ["", "password"],        # Empty username
  ["user", ""],            # Empty password
  ["wrong", "wrong"],      # Invalid credentials
  ["admin", "secret"]      # Valid credentials (will succeed)
]

test_cases.each do |username, password|
  puts "\nAttempting login with: #{username.inspect}, #{password.inspect}"
  begin
    service.authenticate(username, password)
  rescue ValidationError => e
    puts "❌ Validation failed: #{e.message}"
    puts "   Details: #{e.details}"
  rescue AuthenticationError => e
    puts "❌ Authentication failed: #{e.message}"
  rescue RateLimitError => e
    puts "❌ Rate limit exceeded: #{e.message}"
  rescue => e
    puts "❌ Unexpected error: #{e.class} - #{e.message}"
  end
end

# Test rate limiting
puts "\n--- Testing rate limiting ---"
3.times do |i|
  begin
    service.authenticate("attacker", "wrong_password")
  rescue AuthenticationError => e
    puts "  Attempt #{i + 1}: #{e.message}"
  rescue RateLimitError => e
    puts "  ⚠️  #{e.message}"
  end
end

# ----- Raising errors with custom backtrace -----
puts "\n--- Raising with custom backtrace ---"

def custom_error_example
  raise StandardError, "Something went wrong", caller
rescue StandardError => e
  puts "Error: #{e.message}"
  puts "Custom backtrace:"
  e.backtrace.first(3).each { |line| puts "  #{line}" }
end

custom_error_example

# ============================================
# 3. COMMON RUBY ERRORS
# ============================================
puts "\n" + "=" * 60
puts "3. COMMON RUBY ERRORS"
puts "=" * 60

# ----- NameError -----
puts "\n--- NameError (undefined variable/constant) ---"

begin
  puts undefined_variable  # This variable doesn't exist
rescue NameError => e
  puts "❌ NameError: #{e.message}"
end

begin
  puts NonExistentClass.new
rescue NameError => e
  puts "❌ NameError: #{e.message}"
end

# ----- NoMethodError -----
puts "\n--- NoMethodError (method doesn't exist) ---"

begin
  "string".non_existent_method
rescue NoMethodError => e
  puts "❌ NoMethodError: #{e.message}"
  puts "   Tip: #{e.name} method doesn't exist on String class"
end

# ----- ArgumentError -----
puts "\n--- ArgumentError (wrong number/type of arguments) ---"

begin
  [1, 2, 3].first(1, 2)  # first only accepts 0 or 1 argument
rescue ArgumentError => e
  puts "❌ ArgumentError: #{e.message}"
end

def greet(name, title)
  puts "Hello, #{title} #{name}"
end

begin
  greet("John")  # Missing title argument
rescue ArgumentError => e
  puts "❌ ArgumentError: #{e.message}"
end

# ----- TypeError -----
puts "\n--- TypeError (wrong object type) ---"

begin
  "5" + 3  # Can't add string and integer
rescue TypeError => e
  puts "❌ TypeError: #{e.message}"
end

begin
  [1, 2, 3] + "4"  # Can't add array and string
rescue TypeError => e
  puts "❌ TypeError: #{e.message}"
end

# ----- ZeroDivisionError -----
puts "\n--- ZeroDivisionError ---"

begin
  result = 42 / 0
rescue ZeroDivisionError => e
  puts "❌ ZeroDivisionError: #{e.message}"
end

# ----- IndexError -----
puts "\n--- IndexError (array/hash index out of bounds) ---"

begin
  array = [1, 2, 3]
  value = array[10]  # This doesn't raise error, returns nil
  value = array.fetch(10)  # This raises IndexError
rescue IndexError => e
  puts "❌ IndexError: #{e.message}"
end

begin
  hash = {a: 1, b: 2}
  value = hash.fetch(:z)  # Key not found
rescue KeyError => e
  puts "❌ KeyError: #{e.message}"
end

# ----- RuntimeError -----
puts "\n--- RuntimeError (generic error) ---"

begin
  raise "Something bad happened"
rescue RuntimeError => e
  puts "❌ RuntimeError: #{e.message}"
end

# ----- SystemCallError / Errno -----
puts "\n--- SystemCallError (system-related errors) ---"

begin
  File.open("/nonexistent/path/file.txt", "r")
rescue Errno::ENOENT => e
  puts "❌ Errno::ENOENT: #{e.message}"
  puts "   Errno code: #{e.errno}"
end

begin
  File.chmod(0000, "/etc/passwd")  # Might raise permission error
rescue Errno::EACCES => e
  puts "❌ Errno::EACCES: #{e.message}"
rescue => e
  puts "❌ Other error: #{e.message}"
end

# ----- LoadError -----
puts "\n--- LoadError (cannot load file) ---"

begin
  require 'non_existent_gem'
rescue LoadError => e
  puts "❌ LoadError: #{e.message}"
end

# ----- SyntaxError -----
puts "\n--- SyntaxError (code compilation error) ---"

begin
  eval "if true"  # Incomplete syntax
rescue SyntaxError => e
  puts "❌ SyntaxError: #{e.message}"
end

# ----- Exception Hierarchy Demonstration -----
puts "\n" + "=" * 60
puts "EXCEPTION HIERARCHY DEMONSTRATION"
puts "=" * 60

def show_error_hierarchy(error_class, level = 0)
  indent = "  " * level
  puts "#{indent}#{error_class}"
  
  # Show superclass unless we reached the top
  if error_class.superclass && error_class.superclass != Object
    show_error_hierarchy(error_class.superclass, level + 1)
  end
end

puts "\nStandardError hierarchy:"
show_error_hierarchy(StandardError)

puts "\n\nCustom error hierarchy:"
show_error_hierarchy(ValidationError)

# ============================================
# 4. ADVANCED ERROR HANDLING PATTERNS
# ============================================
puts "\n" + "=" * 60
puts "4. ADVANCED ERROR HANDLING PATTERNS"
puts "=" * 60

# ----- Method-level rescue with implicit begin -----
puts "\n--- Method-level rescue ---"

def risky_operation(value)
  result = 100 / value
  puts "Result: #{result}"
rescue ZeroDivisionError
  puts "❌ Cannot divide by zero"
rescue TypeError
  puts "❌ Invalid type provided"
  # The rescue block is implicitly wrapped around the entire method
end

risky_operation(10)
risky_operation(0)
risky_operation("a")

# ----- Using rescue as a modifier -----
puts "\n--- Rescue modifier (inline rescue) ---"

def divide_safely(a, b)
  a / b rescue "Division failed: #{$!.message}"
end

puts "10 / 2 = #{divide_safely(10, 2)}"
puts "10 / 0 = #{divide_safely(10, 0)}"

# Using rescue with assignment
value = risky_calculation rescue default_value = 0
puts "Default value: #{default_value}"

# ----- Catching multiple exceptions with array -----
puts "\n--- Catching multiple exceptions ---"

def process_data(data)
  # This will rescue any of the listed exceptions
  Integer(data)
rescue ArgumentError, TypeError => e
  puts "❌ Invalid data type: #{e.message}"
rescue ZeroDivisionError, NoMethodError => e
  puts "❌ Calculation error: #{e.message}"
end

process_data("123")
process_data("abc")
process_data(nil)

# ----- Creating a retry with limit pattern -----
puts "\n--- Retry with limit pattern ---"

class RetryableOperation
  def self.with_retry(max_retries: 3, &block)
    attempts = 0
    begin
      attempts += 1
      yield
    rescue => e
      if attempts < max_retries
        puts "  Attempt #{attempts} failed: #{e.message}. Retrying..."
        sleep(0.5)
        retry
      else
        puts "  ❌ Failed after #{max_retries} attempts: #{e.message}"
        raise e  # Re-raise the error after max retries
      end
    end
  end
end

puts "\nUsing retryable operation:"
begin
  RetryableOperation.with_retry(max_retries: 3) do
    # Simulate a flaky operation
    if rand < 0.7
      raise "Network timeout"
    end
    puts "✅ Operation succeeded!"
  end
rescue => e
  puts "Final error: #{e.message}"
end

# ----- Ensuring cleanup with begin/ensure only -----
puts "\n--- Ensure without rescue ---"

def with_database_connection
  puts "Opening database connection..."
  begin
    yield
  ensure
    puts "Closing database connection..."
    # This always runs, even if the block raises an error
  end
end

begin
  with_database_connection do
    puts "Performing database operations..."
    raise "Database query failed!"  # This will be propagated
  end
rescue => e
  puts "❌ Caught error: #{e.message}"
end

# ----- Nested exception handling -----
puts "\n--- Nested exception handling ---"

begin
  puts "Outer block starting"
  
  begin
    puts "  Inner block starting"
    raise "Inner error"
  rescue => e
    puts "  Inner rescue: #{e.message}"
    raise "Wrapped: #{e.message}"  # Re-raise a new error
  ensure
    puts "  Inner ensure block"
  end
  
rescue => e
  puts "Outer rescue: #{e.message}"
  puts "Original cause: #{e.cause}" if e.respond_to?(:cause)
ensure
  puts "Outer ensure block"
end

# ----- Custom exception with cause -----
puts "\n--- Exception chaining with cause ---"

class DatabaseError < StandardError; end
class ValidationError < StandardError; end

begin
  begin
    # Original error
    raise ValidationError, "Invalid email format"
  rescue => original_error
    # Raise a new error with the original as cause
    raise DatabaseError, "Failed to save user", cause: original_error
  end
rescue DatabaseError => e
  puts "Error: #{e.message}"
  if e.cause
    puts "Caused by: #{e.cause.class} - #{e.cause.message}"
  end
end

# ============================================
# 5. PRACTICAL EXAMPLE: BANK ACCOUNT SYSTEM
# ============================================
puts "\n" + "=" * 60
puts "5. PRACTICAL EXAMPLE: BANK ACCOUNT WITH ERROR HANDLING"
puts "=" * 60

# Custom exceptions for banking domain
class InsufficientFundsError < StandardError
  attr_reader :current_balance, :attempted_amount
  
  def initialize(current_balance, attempted_amount)
    @current_balance = current_balance
    @attempted_amount = attempted_amount
    super("Insufficient funds: attempted to withdraw $#{attempted_amount}, balance is $#{current_balance}")
  end
end

class AccountFrozenError < StandardError; end
class NegativeDepositError < StandardError; end
class AccountNotFoundError < StandardError; end

class BankAccount
  attr_reader :account_number, :balance, :frozen
  
  def initialize(account_number, initial_balance = 0)
    @account_number = account_number
    @balance = initial_balance
    @frozen = false
    @transaction_log = []
  end
  
  def deposit(amount)
    # Validate input
    raise ArgumentError, "Amount must be positive" if amount <= 0
    raise AccountFrozenError, "Account is frozen" if @frozen
    
    @balance += amount
    log_transaction(:deposit, amount)
    puts "✅ Deposited $#{amount}. New balance: $#{@balance}"
  rescue ArgumentError => e
    puts "❌ Invalid deposit: #{e.message}"
    raise
  end
  
  def withdraw(amount)
    # Multiple validations
    raise ArgumentError, "Amount must be positive" if amount <= 0
    raise AccountFrozenError, "Account is frozen" if @frozen
    raise InsufficientFundsError.new(@balance, amount) if amount > @balance
    
    @balance -= amount
    log_transaction(:withdraw, amount)
    puts "✅ Withdrew $#{amount}. New balance: $#{@balance}"
  rescue InsufficientFundsError => e
    puts "❌ Withdrawal failed: #{e.message}"
    raise
  rescue => e
    puts "❌ Withdrawal error: #{e.message}"
    raise
  end
  
  def transfer(amount, target_account)
    raise ArgumentError, "Invalid target account" unless target_account.is_a?(BankAccount)
    
    # Use atomic operation with rollback capability
    begin
      puts "\n--- Transfer $#{amount} from #{@account_number} to #{target_account.account_number} ---"
      
      # Withdraw from this account
      withdraw(amount)
      
      # Deposit to target account
      target_account.deposit(amount)
      
      puts "✅ Transfer completed successfully"
    rescue StandardError => e
      puts "❌ Transfer failed: #{e.message}"
      puts "  Rolling back transaction..."
      
      # Attempt to rollback (if withdrawal happened but deposit failed)
      if @balance_changed
        # In a real system, you'd have proper rollback logic
        puts "  Note: In production, this would use database transactions"
      end
      
      raise TransactionError, "Transfer failed: #{e.message}"
    end
  end
  
  def freeze
    @frozen = true
    puts "🔒 Account #{@account_number} frozen"
  end
  
  def unfreeze
    @frozen = false
    puts "🔓 Account #{@account_number} unfrozen"
  end
  
  private
  
  def log_transaction(type, amount)
    @transaction_log << {
      type: type,
      amount: amount,
      timestamp: Time.now,
      balance_after: @balance
    }
  end
end

class TransactionError < StandardError; end

# Demonstration of bank account system
puts "\n--- Bank Account System Demonstration ---"

# Create accounts
account1 = BankAccount.new("12345", 1000)
account2 = BankAccount.new("67890", 500)

# Test various scenarios
test_scenarios = [
  -> { account1.deposit(500) },                    # Success
  -> { account1.withdraw(200) },                   # Success
  -> { account1.withdraw(2000) },                  # Insufficient funds
  -> { account1.deposit(-50) },                    # Invalid amount
  -> { account1.transfer(300, account2) },         # Success
  -> { account1.freeze },
  -> { account1.withdraw(100) },                   # Account frozen
  -> { account1.unfreeze },
  -> { account1.withdraw(100) },                   # Success after unfreeze
  -> { account1.transfer(10000, account2) }        # Insufficient funds during transfer
]

test_scenarios.each_with_index do |scenario, index|
  puts "\n--- Scenario #{index + 1} ---"
  begin
    scenario.call
  rescue StandardError => e
    puts "⚠️  Error caught: #{e.class} - #{e.message}"
    # Continue to next scenario
  end
end

# Display final balances
puts "\n--- Final Account Balances ---"
puts "Account 1 (#{account1.account_number}): $#{account1.balance}"
puts "Account 2 (#{account2.account_number}): $#{account2.balance}"

# ============================================
# 6. ERROR HANDLING BEST PRACTICES
# ============================================
puts "\n" + "=" * 60
puts "6. ERROR HANDLING BEST PRACTICES SUMMARY"
puts "=" * 60

puts <<~BEST_PRACTICES
  
  ✅ DO:
  • Rescue specific exceptions, not Exception
  • Use ensure for cleanup (closing files, DB connections)
  • Create custom error classes for domain-specific errors
  • Log errors with context for debugging
  • Use retry for transient failures
  • Handle errors at the appropriate level
  • Include meaningful error messages
  • Use exception chaining (cause) for error context
  
  ❌ DON'T:
  • Don't rescue Exception (it catches SystemExit, Interrupt)
  • Don't ignore errors with empty rescue blocks
  • Don't use exceptions for normal flow control
  • Don't return error codes instead of raising exceptions
  • Don't rescue errors you can't handle
  • Don't expose sensitive information in error messages
  
  🎯 Common Exception Hierarchy:
  Exception
    ├── NoMemoryError
    ├── ScriptError
    │   ├── LoadError
    │   ├── NotImplementedError
    │   └── SyntaxError
    ├── SignalException
    │   └── Interrupt
    ├── StandardError (rescue this by default)
    │   ├── ArgumentError
    │   ├── IOError
    │   ├── IndexError
    │   ├── NameError
    │   │   └── NoMethodError
    │   ├── RuntimeError
    │   ├── TypeError
    │   └── ZeroDivisionError
    └── SystemExit

BEST_PRACTICES

puts "\n" + "=" * 60
puts "END OF ERROR HANDLING DEMONSTRATION"
puts "=" * 60