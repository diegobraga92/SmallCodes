# ============================================
# RUBY TESTING FUNDAMENTALS DEMONSTRATION
# ============================================

# This file demonstrates testing concepts and practices
# Note: This is a teaching file - tests are typically in separate files

# ============================================
# 1. BASIC UNIT TESTING CONCEPTS
# ============================================
puts "=" * 60
puts "1. BASIC UNIT TESTING CONCEPTS"
puts "=" * 60

puts <<~CONCEPTS

  WHAT IS UNIT TESTING?
  • Testing individual units of code (methods, classes) in isolation
  • Verifying that each component works as expected
  • Automated tests that can be run repeatedly
  
  KEY TESTING PRINCIPLES:
  
  1. TEST ISOLATION
     • Tests should not depend on each other
     • Each test runs in its own context
     • External dependencies should be mocked/stubbed
  
  2. ARRANGE-ACT-ASSERT (AAA) PATTERN
     • Arrange: Set up test data and conditions
     • Act: Execute the code being tested
     • Assert: Verify the expected outcome
  
  3. TEST COVERAGE
     • Test happy paths (normal behavior)
     • Test edge cases (boundary conditions)
     • Test error cases (exception handling)
  
  4. TEST NAMING CONVENTIONS
     • test_method_name_behavior
     • test_method_name_when_condition
     • Descriptive and self-documenting
  
  5. RED-GREEN-REFACTOR CYCLE
     • RED: Write a failing test
     • GREEN: Make the test pass
     • REFACTOR: Improve code while keeping tests green

CONCEPTS

# ============================================
# 2. SAMPLE CLASS TO TEST
# ============================================
puts "=" * 60
puts "2. SAMPLE CLASS FOR TESTING"
puts "=" * 60

# A simple calculator class to demonstrate testing
class Calculator
  def add(a, b)
    a + b
  end
  
  def subtract(a, b)
    a - b
  end
  
  def multiply(a, b)
    a * b
  end
  
  def divide(a, b)
    raise ArgumentError, "Cannot divide by zero" if b == 0
    a.to_f / b
  end
  
  def power(base, exponent)
    result = 1
    exponent.times { result *= base }
    result
  end
  
  def factorial(n)
    raise ArgumentError, "Factorial not defined for negative numbers" if n < 0
    return 1 if n <= 1
    n * factorial(n - 1)
  end
  
  def percentage(value, percent)
    value * percent / 100.0
  end
end

# A bank account class for more complex testing
class BankAccount
  attr_reader :balance, :account_number, :transaction_history
  
  def initialize(account_number, initial_balance = 0)
    @account_number = account_number
    @balance = initial_balance
    @transaction_history = []
    log_transaction(:initial_deposit, initial_balance) if initial_balance > 0
  end
  
  def deposit(amount)
    raise ArgumentError, "Deposit amount must be positive" if amount <= 0
    @balance += amount
    log_transaction(:deposit, amount)
    true
  end
  
  def withdraw(amount)
    raise ArgumentError, "Withdrawal amount must be positive" if amount <= 0
    raise InsufficientFundsError, "Insufficient funds" if amount > @balance
    @balance -= amount
    log_transaction(:withdrawal, amount)
    true
  end
  
  def transfer(amount, target_account)
    raise ArgumentError, "Transfer amount must be positive" if amount <= 0
    raise ArgumentError, "Invalid target account" unless target_account.is_a?(BankAccount)
    
    begin
      withdraw(amount)
      target_account.deposit(amount)
      log_transaction(:transfer_out, amount, target_account.account_number)
      true
    rescue => e
      # In a real system, you'd want proper rollback
      raise TransferError, "Transfer failed: #{e.message}"
    end
  end
  
  def statement
    @transaction_history.map do |transaction|
      format_transaction(transaction)
    end
  end
  
  private
  
  def log_transaction(type, amount, target = nil)
    @transaction_history << {
      type: type,
      amount: amount,
      balance: @balance,
      timestamp: Time.now,
      target: target
    }
  end
  
  def format_transaction(transaction)
    timestamp = transaction[:timestamp].strftime("%Y-%m-%d %H:%M:%S")
    case transaction[:type]
    when :deposit
      "#{timestamp} | DEPOSIT    | +$#{transaction[:amount]} | Balance: $#{transaction[:balance]}"
    when :withdrawal
      "#{timestamp} | WITHDRAWAL | -$#{transaction[:amount]} | Balance: $#{transaction[:balance]}"
    when :transfer_out
      "#{timestamp} | TRANSFER   | -$#{transaction[:amount]} to #{transaction[:target]} | Balance: $#{transaction[:balance]}"
    else
      "#{timestamp} | #{transaction[:type].to_s.upcase} | $#{transaction[:amount]} | Balance: $#{transaction[:balance]}"
    end
  end
end

# Custom error classes
class InsufficientFundsError < StandardError; end
class TransferError < StandardError; end

# ============================================
# 3. MINITEST FRAMEWORK
# ============================================
puts "\n" + "=" * 60
puts "3. MINITEST FRAMEWORK"
puts "=" * 60

puts <<~MINITEST_INTRO

  MINITEST - RUBY'S BUILT-IN TESTING FRAMEWORK
  
  Installation (already included in Ruby):
    # No installation needed - part of Ruby standard library
  
  Two Main Approaches:
    1. Test::Unit style (assertion-based)
    2. Spec style (expectation-based)
  
  Key Assertions:
    assert(boolean, message)           # Pass if boolean is true
    assert_equal(expected, actual)     # Pass if expected == actual
    assert_nil(object)                 # Pass if object is nil
    assert_raises(error) { ... }       # Pass if block raises error
    refute(boolean)                    # Opposite of assert
    assert_includes(collection, obj)   # Pass if collection includes obj
    assert_match(pattern, string)      # Pass if string matches pattern

MINITEST_INTRO

# Minitest test example (in comments since it would normally be in a separate file)
puts <<~MINITEST_EXAMPLE

  # Example Minitest test file: test_calculator.rb
  # Run with: ruby test_calculator.rb
  
  require 'minitest/autorun'
  require_relative 'calculator'
  
  class TestCalculator < Minitest::Test
    def setup
      # This runs before each test
      @calc = Calculator.new
    end
    
    def teardown
      # This runs after each test (cleanup)
    end
    
    def test_add
      assert_equal 5, @calc.add(2, 3)
      assert_equal 0, @calc.add(-1, 1)
      assert_equal -5, @calc.add(-2, -3)
    end
    
    def test_divide
      assert_equal 2.5, @calc.divide(5, 2)
      assert_equal 2.0, @calc.divide(4, 2)
      
      error = assert_raises(ArgumentError) do
        @calc.divide(10, 0)
      end
      assert_equal "Cannot divide by zero", error.message
    end
    
    def test_factorial
      assert_equal 1, @calc.factorial(0)
      assert_equal 1, @calc.factorial(1)
      assert_equal 120, @calc.factorial(5)
      
      assert_raises(ArgumentError) do
        @calc.factorial(-1)
      end
    end
  end

MINITEST_EXAMPLE

# ============================================
# 4. RSPEC FRAMEWORK
# ============================================
puts "\n" + "=" * 60
puts "4. RSPEC FRAMEWORK"
puts "=" * 60

puts <<~RSPEC_INTRO

  RSPEC - BEHAVIOR-DRIVEN DEVELOPMENT (BDD) FRAMEWORK
  
  Installation:
    $ gem install rspec
    $ rspec --init  # Creates spec/spec_helper.rb
  
  Key Concepts:
    describe   # Groups related tests
    context    # Specific scenario within a describe
    it         # Individual test example
    expect     # Sets up expectations
    before     # Setup code that runs before examples
    let        # Lazy-evaluated variables
  
  Matchers:
    expect(value).to eq(expected)              # Equality
    expect(value).to be_truthy                 # Truthiness
    expect(value).to be_falsey                 # Falsiness
    expect(value).to be_nil                    # Nil check
    expect { ... }.to raise_error(Error)       # Exception
    expect(collection).to include(item)        # Inclusion
    expect(string).to match(/pattern/)         # Regex match
    expect(array).to have_attributes(size: 3)  # Attributes

RSPEC_INTRO

# RSpec test example (in comments since it would normally be in a separate file)
puts <<~RSPEC_EXAMPLE

  # Example RSpec test file: spec/calculator_spec.rb
  # Run with: rspec spec/calculator_spec.rb
  
  require 'rspec'
  require_relative '../calculator'
  
  RSpec.describe Calculator do
    let(:calculator) { Calculator.new }
    
    describe '#add' do
      it 'adds two positive numbers' do
        expect(calculator.add(2, 3)).to eq(5)
      end
      
      it 'adds negative numbers' do
        expect(calculator.add(-1, -2)).to eq(-3)
      end
      
      context 'with mixed signs' do
        it 'adds positive and negative numbers' do
          expect(calculator.add(5, -3)).to eq(2)
        end
      end
    end
    
    describe '#divide' do
      it 'divides two numbers' do
        expect(calculator.divide(10, 2)).to eq(5.0)
      end
      
      it 'returns a float result' do
        expect(calculator.divide(5, 2)).to eq(2.5)
      end
      
      context 'when dividing by zero' do
        it 'raises an ArgumentError' do
          expect { calculator.divide(10, 0) }.to raise_error(ArgumentError, "Cannot divide by zero")
        end
      end
    end
    
    describe '#factorial' do
      it 'returns 1 for 0!' do
        expect(calculator.factorial(0)).to eq(1)
      end
      
      it 'calculates factorial for positive numbers' do
        expect(calculator.factorial(5)).to eq(120)
      end
      
      it 'raises error for negative numbers' do
        expect { calculator.factorial(-1) }.to raise_error(ArgumentError)
      end
    end
  end

RSPEC_EXAMPLE

# ============================================
# 5. WRITING SIMPLE TEST CASES
# ============================================
puts "\n" + "=" * 60
puts "5. WRITING SIMPLE TEST CASES"
puts "=" * 60

puts "\n--- Test Case Patterns ---"

puts <<~TEST_PATTERNS

  1. TESTING HAPPY PATH (Normal Operation)
  ----------------------------------------
  # Test that the method works correctly with valid inputs
  
  def test_deposit_increases_balance
    account = BankAccount.new("12345", 100)
    account.deposit(50)
    assert_equal 150, account.balance
  end
  
  2. TESTING EDGE CASES (Boundary Conditions)
  -------------------------------------------
  # Test behavior at boundaries
  
  def test_deposit_with_minimum_amount
    account = BankAccount.new("12345", 0)
    account.deposit(0.01)
    assert_equal 0.01, account.balance
  end
  
  3. TESTING ERROR CONDITIONS
  ---------------------------
  # Test that errors are raised appropriately
  
  def test_withdraw_more_than_balance
    account = BankAccount.new("12345", 100)
    assert_raises(InsufficientFundsError) do
      account.withdraw(150)
    end
  end
  
  4. TESTING STATE CHANGES
  ------------------------
  # Test that operations modify state correctly
  
  def test_transaction_history
    account = BankAccount.new("12345", 100)
    account.deposit(50)
    account.withdraw(30)
    
    assert_equal 2, account.transaction_history.length
    assert_equal :deposit, account.transaction_history[0][:type]
    assert_equal :withdrawal, account.transaction_history[1][:type]
  end
  
  5. TESTING WITH FIXTURES
  ------------------------
  # Use setup/before to create test data
  
  class TestBankAccount < Minitest::Test
    def setup
      @account = BankAccount.new("12345", 100)
      @target = BankAccount.new("67890", 50)
    end
    
    def test_transfer
      @account.transfer(50, @target)
      assert_equal 50, @account.balance
      assert_equal 100, @target.balance
    end
  end

TEST_PATTERNS

# ============================================
# 6. PRACTICAL TESTING DEMONSTRATION
# ============================================
puts "\n" + "=" * 60
puts "6. PRACTICAL TESTING DEMONSTRATION"
puts "=" * 60

# Create a simple test runner to demonstrate testing concepts
class SimpleTestRunner
  def initialize
    @tests = []
    @passed = 0
    @failed = 0
  end
  
  def test(name, &block)
    @tests << { name: name, block: block }
  end
  
  def assert(condition, message = "Assertion failed")
    unless condition
      raise message
    end
  end
  
  def assert_equal(expected, actual, message = nil)
    message ||= "Expected #{expected.inspect}, got #{actual.inspect}"
    assert(expected == actual, message)
  end
  
  def assert_raises(error_class, &block)
    begin
      block.call
    rescue error_class => e
      return e
    rescue => e
      raise "Expected #{error_class}, but got #{e.class}"
    end
    raise "Expected #{error_class}, but no exception was raised"
  end
  
  def run
    puts "\nRunning tests...\n\n"
    
    @tests.each do |test|
      begin
        test[:block].call
        puts "✅ #{test[:name]}"
        @passed += 1
      rescue => e
        puts "❌ #{test[:name]}"
        puts "   #{e.message}"
        @failed += 1
      end
    end
    
    puts "\n" + "=" * 40
    puts "Results: #{@passed} passed, #{@failed} failed"
    puts "=" * 40
  end
end

# Create test suite using our simple test runner
runner = SimpleTestRunner.new

# Test the Calculator class
runner.test "Calculator#add adds two numbers" do
  calc = Calculator.new
  runner.assert_equal(5, calc.add(2, 3))
  runner.assert_equal(0, calc.add(-1, 1))
  runner.assert_equal(-5, calc.add(-2, -3))
end

runner.test "Calculator#subtract subtracts numbers" do
  calc = Calculator.new
  runner.assert_equal(2, calc.subtract(5, 3))
  runner.assert_equal(-2, calc.subtract(3, 5))
  runner.assert_equal(0, calc.subtract(5, 5))
end

runner.test "Calculator#multiply multiplies numbers" do
  calc = Calculator.new
  runner.assert_equal(15, calc.multiply(3, 5))
  runner.assert_equal(0, calc.multiply(0, 5))
  runner.assert_equal(-10, calc.multiply(-2, 5))
end

runner.test "Calculator#divide divides numbers" do
  calc = Calculator.new
  runner.assert_equal(2.5, calc.divide(5, 2))
  runner.assert_equal(2.0, calc.divide(4, 2))
end

runner.test "Calculator#divide raises error when dividing by zero" do
  calc = Calculator.new
  runner.assert_raises(ArgumentError) do
    calc.divide(10, 0)
  end
end

runner.test "Calculator#factorial returns 1 for 0" do
  calc = Calculator.new
  runner.assert_equal(1, calc.factorial(0))
end

runner.test "Calculator#factorial calculates factorial for positive numbers" do
  calc = Calculator.new
  runner.assert_equal(1, calc.factorial(1))
  runner.assert_equal(120, calc.factorial(5))
end

runner.test "Calculator#factorial raises error for negative numbers" do
  calc = Calculator.new
  runner.assert_raises(ArgumentError) do
    calc.factorial(-1)
  end
end

# Test the BankAccount class
runner.test "BankAccount#initialize sets initial balance" do
  account = BankAccount.new("12345", 100)
  runner.assert_equal(100, account.balance)
  runner.assert_equal("12345", account.account_number)
end

runner.test "BankAccount#deposit increases balance" do
  account = BankAccount.new("12345", 100)
  account.deposit(50)
  runner.assert_equal(150, account.balance)
end

runner.test "BankAccount#deposit raises error for negative amount" do
  account = BankAccount.new("12345", 100)
  runner.assert_raises(ArgumentError) do
    account.deposit(-50)
  end
end

runner.test "BankAccount#withdraw decreases balance" do
  account = BankAccount.new("12345", 100)
  account.withdraw(30)
  runner.assert_equal(70, account.balance)
end

runner.test "BankAccount#withdraw raises error for insufficient funds" do
  account = BankAccount.new("12345", 100)
  runner.assert_raises(InsufficientFundsError) do
    account.withdraw(150)
  end
end

runner.test "BankAccount#transfer moves money between accounts" do
  account1 = BankAccount.new("12345", 100)
  account2 = BankAccount.new("67890", 50)
  
  account1.transfer(30, account2)
  
  runner.assert_equal(70, account1.balance)
  runner.assert_equal(80, account2.balance)
end

runner.test "BankAccount#transfer raises error for invalid account" do
  account = BankAccount.new("12345", 100)
  runner.assert_raises(ArgumentError) do
    account.transfer(50, nil)
  end
end

runner.test "BankAccount#statement returns transaction history" do
  account = BankAccount.new("12345", 100)
  account.deposit(50)
  account.withdraw(30)
  
  statement = account.statement
  runner.assert_equal(3, statement.length) # Initial deposit + deposit + withdrawal
end

# Run the tests
runner.run

# ============================================
# 7. TEST DOUBLES (MOCKS AND STUBS)
# ============================================
puts "\n" + "=" * 60
puts "7. TEST DOUBLES (MOCKS AND STUBS)"
puts "=" * 60

puts <<~DOUBLES

  TEST DOUBLES - REPLACING DEPENDENCIES IN TESTS
  
  Types of Test Doubles:
  
  1. STUB
     • Returns predefined responses
     • Used to isolate the code under test
     • Example: Stubbing a database call to return test data
  
  2. MOCK
     • Expects specific calls with specific arguments
     • Verifies interaction between objects
     • Example: Ensuring a method was called with correct parameters
  
  3. SPY
     • Records calls for later verification
     • Less strict than mocks
     • Example: Checking that a logger received a message
  
  4. FAKE
     • Lightweight implementation of a dependency
     • Example: In-memory database for testing
  
  Example with RSpec:
  
  # spec/notification_service_spec.rb
  RSpec.describe NotificationService do
    let(:email_service) { double("EmailService") }
    let(:service) { NotificationService.new(email_service) }
    
    it "sends welcome email" do
      # Stubbing
      allow(email_service).to receive(:send_email)
        .with("user@example.com", "Welcome!")
        .and_return(true)
      
      # Act
      service.send_welcome("user@example.com")
      
      # Assert (mock verification)
      expect(email_service).to have_received(:send_email)
        .with("user@example.com", "Welcome!")
    end
  end

DOUBLES

# ============================================
# 8. TEST ORGANIZATION BEST PRACTICES
# ============================================
puts "\n" + "=" * 60
puts "8. TEST ORGANIZATION BEST PRACTICES"
puts "=" * 60

puts <<~BEST_PRACTICES

  TEST ORGANIZATION PATTERNS:
  
  1. DIRECTORY STRUCTURE
  ----------------------
  project/
    ├── lib/               # Source code
    │   ├── calculator.rb
    │   └── bank_account.rb
    ├── test/              # Minitest tests
    │   ├── test_helper.rb
    │   ├── test_calculator.rb
    │   └── test_bank_account.rb
    └── spec/              # RSpec tests
        ├── spec_helper.rb
        ├── calculator_spec.rb
        └── bank_account_spec.rb
  
  2. NAMING CONVENTIONS
  --------------------
  • Test files: test_classname.rb or classname_spec.rb
  • Test methods: test_method_name_scenario
  • Describe blocks: ClassName, #instance_method, .class_method
  • It blocks: describes behavior in plain English
  
  3. TEST HELPER PATTERNS
  -----------------------
  # test_helper.rb
  require 'minitest/autorun'
  require 'minitest/reporters'
  Minitest::Reporters.use!
  
  # Common setup methods
  module TestHelper
    def create_test_account
      BankAccount.new("TEST001", 1000)
    end
    
    def create_test_products
      [
        Product.new("Widget", 19.99),
        Product.new("Gadget", 29.99)
      ]
    end
  end
  
  4. FACTORIES AND FIXTURES
  -------------------------
  # Using factory_bot (RSpec)
  FactoryBot.define do
    factory :user do
      name { "John Doe" }
      email { "john@example.com" }
      age { 30 }
    end
  end
  
  # Using fixtures (Minitest)
  # test/fixtures/users.yml
  john:
    name: John Doe
    email: john@example.com
    age: 30
  
  5. TAGGING AND FILTERING
  ------------------------
  # RSpec tagging
  it "sends email", :slow do
    # ...
  end
  
  # Run only slow tests
  # rspec --tag slow
  
  # Minitest filtering
  # ruby test/test_calculator.rb --name test_add

BEST_PRACTICES

# ============================================
# 9. COMPLETE TESTING EXAMPLE
# ============================================
puts "\n" + "=" * 60
puts "9. COMPLETE TESTING EXAMPLE"
puts "=" * 60

puts <<~FULL_EXAMPLE

  # Complete Minitest Example: test_bank_account.rb
  
  require 'minitest/autorun'
  require_relative '../lib/bank_account'
  
  class TestBankAccount < Minitest::Test
    def setup
      @account = BankAccount.new("12345", 1000)
      @target = BankAccount.new("67890", 500)
    end
    
    # Happy path tests
    def test_initialization
      assert_equal 1000, @account.balance
      assert_equal "12345", @account.account_number
      assert_empty @account.transaction_history
    end
    
    def test_deposit
      @account.deposit(500)
      assert_equal 1500, @account.balance
      assert_equal 1, @account.transaction_history.length
      assert_equal :deposit, @account.transaction_history.last[:type]
    end
    
    # Edge case tests
    def test_deposit_with_small_amount
      @account.deposit(0.01)
      assert_equal 1000.01, @account.balance
    end
    
    def test_withdraw_exact_balance
      @account.withdraw(1000)
      assert_equal 0, @account.balance
    end
    
    # Error condition tests
    def test_deposit_negative_amount
      assert_raises(ArgumentError) do
        @account.deposit(-100)
      end
    end
    
    def test_withdraw_insufficient_funds
      assert_raises(InsufficientFundsError) do
        @account.withdraw(2000)
      end
    end
    
    # Interaction tests
    def test_transfer_between_accounts
      @account.transfer(300, @target)
      
      assert_equal 700, @account.balance
      assert_equal 800, @target.balance
    end
    
    def test_transfer_rollback_on_failure
      # This would test that transfers are atomic
      # In a real system, you'd test rollback behavior
    end
    
    # State change tests
    def test_transaction_history_logging
      @account.deposit(200)
      @account.withdraw(100)
      
      history = @account.transaction_history
      assert_equal 2, history.length
      assert_equal :deposit, history[0][:type]
      assert_equal 200, history[0][:amount]
      assert_equal :withdrawal, history[1][:type]
      assert_equal 100, history[1][:amount]
    end
  end

FULL_EXAMPLE

# ============================================
# 10. TESTING CHEAT SHEET
# ============================================
puts "\n" + "=" * 60
puts "10. TESTING CHEAT SHEET"
puts "=" * 60

puts <<~CHEAT_SHEET

  MINITEST QUICK REFERENCE:
  -------------------------
  # Basic structure
  class TestClassName < Minitest::Test
    def setup; end
    def teardown; end
    
    def test_method_name
      assert_equal expected, actual
      assert_raises(Error) { code }
    end
  end
  
  # Common assertions
  assert(boolean, msg)                    # Pass if boolean is true
  assert_equal(expected, actual)          # Pass if expected == actual
  assert_nil(obj)                         # Pass if obj is nil
  assert_raises(Error) { ... }            # Pass if block raises Error
  assert_includes(collection, obj)        # Pass if collection includes obj
  assert_match(pattern, string)           # Pass if string matches pattern
  assert_respond_to(obj, method)          # Pass if obj responds to method
  refute(boolean)                         # Opposite of assert
  refute_empty(collection)                # Pass if collection not empty
  
  RSPEC QUICK REFERENCE:
  ----------------------
  # Basic structure
  RSpec.describe ClassName do
    let(:variable) { value }
    
    before { setup_code }
    after { cleanup_code }
    
    describe "#method_name" do
      context "when condition" do
        it "does something" do
          expect(actual).to eq(expected)
        end
      end
    end
  end
  
  # Common matchers
  expect(value).to eq(expected)              # Equality
  expect(value).to be_truthy                 # Truthiness
  expect(value).to be_falsey                 # Falsiness
  expect(value).to be_nil                    # Nil check
  expect(value).to be > 5                    # Comparison
  expect(collection).to include(item)        # Inclusion
  expect(string).to match(/pattern/)         # Regex match
  expect { ... }.to raise_error(Error)       # Exception
  expect(array).to have_attributes(size: 3)  # Attributes
  expect(obj).to respond_to(:method)         # Method existence
  
  RUNNING TESTS:
  -------------
  # Minitest
  ruby test/test_file.rb                    # Run single file
  ruby test/test_file.rb --name test_name   # Run specific test
  ruby test/                                # Run all tests
  
  # RSpec
  rspec                                     # Run all specs
  rspec spec/file_spec.rb                   # Run single file
  rspec spec/file_spec.rb:42                # Run test at line 42
  rspec --tag focus                         # Run tagged tests
  rspec --format documentation              # Verbose output

CHEAT_SHEET

puts "\n" + "=" * 60
puts "END OF TESTING FUNDAMENTALS DEMONSTRATION"
puts "=" * 60