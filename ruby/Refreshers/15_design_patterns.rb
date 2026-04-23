# ============================================
# RUBY DESIGN PATTERNS
# ============================================

puts "=" * 60
puts "RUBY DESIGN PATTERNS - FROM JUNIOR TO SENIOR"
puts "=" * 60

# ============================================
# 1. SINGLETON PATTERN
# ============================================

puts "\n" + "=" * 40
puts "1. SINGLETON PATTERN"
puts "=" * 40

puts <<~SINGLETON_INTRO

  SINGLETON:
  • Ensures a class has only one instance
  • Provides global access to that instance
  • Useful for: configuration, logging, caching

SINGLETON_INTRO

# Method 1: Using Ruby's Singleton module
require 'singleton'

class DatabaseConnection
  include Singleton
  
  attr_reader :connected_at
  
  def initialize
    @connected_at = Time.now
    puts "Database connection created at #{@connected_at}"
  end
  
  def query(sql)
    "Executing: #{sql}"
  end
end

# Usage
db1 = DatabaseConnection.instance
db2 = DatabaseConnection.instance

puts "Same instance? #{db1.object_id == db2.object_id}"
puts db1.query("SELECT * FROM users")

# Method 2: Manual singleton (more control)
class Logger
  @instance = nil
  
  def self.instance
    @instance ||= new
  end
  
  private_class_method :new
  
  def log(message)
    puts "[LOG] #{message}"
  end
end

logger = Logger.instance
logger.log("Application started")

# ============================================================================
# 2. FACTORY PATTERN
# ============================================================================

puts "\n" + "=" * 40
puts "2. FACTORY PATTERN"
puts "=" * 40

puts <<~FACTORY_INTRO

  FACTORY:
  • Creates objects without specifying exact class
  • Encapsulates object creation logic
  • Useful when creation is complex or conditional

FACTORY_INTRO

# Simple Factory
class Animal
  def speak
    raise NotImplementedError, "Subclass must implement"
  end
end

class Dog < Animal
  def speak
    "Woof!"
  end
end

class Cat < Animal
  def speak
    "Meow!"
  end
end

class Bird < Animal
  def speak
    "Tweet!"
  end
end

class AnimalFactory
  def self.create(type)
    case type
    when :dog
      Dog.new
    when :cat
      Cat.new
    when :bird
      Bird.new
    else
      raise ArgumentError, "Unknown animal type: #{type}"
    end
  end
end

# Usage
animal = AnimalFactory.create(:dog)
puts "Animal says: #{animal.speak}"

# Factory Method Pattern
class Document
  def initialize
    @pages = []
  end
  
  def create_page
    raise NotImplementedError, "Subclass must implement"
  end
  
  def add_page
    @pages << create_page
  end
end

class PDFDocument < Document
  def create_page
    PDFPage.new
  end
end

class WordDocument < Document
  def create_page
    WordPage.new
  end
end

class PDFPage
  def render
    "Rendering PDF page"
  end
end

class WordPage
  def render
    "Rendering Word page"
  end
end

# ============================================================================
# 3. BUILDER PATTERN
# ============================================================================

puts "\n" + "=" * 40
puts "3. BUILDER PATTERN"
puts "=" * 40

puts <<~BUILDER_INTRO

  BUILDER:
  • Constructs complex objects step by step
  • Separates construction from representation
  • Useful for objects with many optional parameters

BUILDER_INTRO

class User
  attr_accessor :name, :email, :age, :address, :phone
  
  def initialize
    yield(self) if block_given?
  end
  
  def to_s
    "User(name: #{@name}, email: #{@email}, age: #{@age})"
  end
end

# Usage with block
user = User.new do |u|
  u.name = "Alice"
  u.email = "alice@example.com"
  u.age = 30
  u.address = "123 Main St"
end

puts user

# Classic Builder Pattern
class HttpRequest
  attr_reader :method, :url, :headers, :body
  
  def initialize(builder)
    @method = builder.method
    @url = builder.url
    @headers = builder.headers
    @body = builder.body
  end
  
  class Builder
    attr_accessor :method, :url, :headers, :body
    
    def initialize
      @method = 'GET'
      @headers = {}
      @body = nil
    end
    
    def method(method)
      @method = method
      self
    end
    
    def url(url)
      @url = url
      self
    end
    
    def header(key, value)
      @headers[key] = value
      self
    end
    
    def body(body)
      @body = body
      self
    end
    
    def build
      HttpRequest.new(self)
    end
  end
end

# Usage
request = HttpRequest::Builder.new
  .method('POST')
  .url('https://api.example.com/users')
  .header('Content-Type', 'application/json')
  .body('{"name": "Alice"}')
  .build

puts "Request: #{request.method} #{request.url}"

# ============================================================================
# 4. OBSERVER PATTERN
# ============================================================================

puts "\n" + "=" * 40
puts "4. OBSERVER PATTERN"
puts "=" * 40

puts <<~OBSERVER_INTRO

  OBSERVER:
  • Defines one-to-many dependency
  • When one object changes, notifies all dependents
  • Useful for event systems, pub/sub

OBSERVER_INTRO

# Ruby has built-in Observable module
require 'observer'

class StockTicker
  include Observable
  
  def initialize(symbol)
    @symbol = symbol
    @price = 0
  end
  
  def update_price(price)
    @price = price
    changed  # Mark as changed
    notify_observers(@symbol, @price)  # Notify observers
  end
end

class PriceDisplay
  def update(symbol, price)
    puts "Display: #{symbol} is now $#{price}"
  end
end

class PriceAlert
  def initialize(threshold)
    @threshold = threshold
  end
  
  def update(symbol, price)
    if price > @threshold
      puts "ALERT: #{symbol} exceeded $#{@threshold}! Current: $#{price}"
    end
  end
end

# Usage
ticker = StockTicker.new("AAPL")
display = PriceDisplay.new
alert = PriceAlert.new(150)

ticker.add_observer(display)
ticker.add_observer(alert)

ticker.update_price(145)
ticker.update_price(155)

# ============================================================================
# 5. STRATEGY PATTERN
# ============================================================================

puts "\n" + "=" * 40
puts "5. STRATEGY PATTERN"
puts "=" * 40

puts <<~STRATEGY_INTRO

  STRATEGY:
  • Defines family of algorithms
  • Makes them interchangeable
  • Encapsulates behavior in separate classes

STRATEGY_INTRO

# Payment strategies
class PaymentStrategy
  def pay(amount)
    raise NotImplementedError
  end
end

class CreditCardPayment < PaymentStrategy
  def initialize(card_number)
    @card_number = card_number
  end
  
  def pay(amount)
    puts "Paid $#{amount} with credit card ending in #{@card_number[-4..]}"
  end
end

class PayPalPayment < PaymentStrategy
  def initialize(email)
    @email = email
  end
  
  def pay(amount)
    puts "Paid $#{amount} with PayPal account #{@email}"
  end
end

class BitcoinPayment < PaymentStrategy
  def initialize(address)
    @address = address
  end
  
  def pay(amount)
    puts "Paid $#{amount} with Bitcoin to #{@address}"
  end
end

class ShoppingCart
  def initialize(payment_strategy)
    @payment_strategy = payment_strategy
    @items = []
  end
  
  def add_item(item, price)
    @items << { item: item, price: price }
  end
  
  def checkout
    total = @items.sum { |item| item[:price] }
    @payment_strategy.pay(total)
  end
end

# Usage
cart = ShoppingCart.new(CreditCardPayment.new("1234567890123456"))
cart.add_item("Book", 29.99)
cart.add_item("Pen", 4.99)
cart.checkout

# Using blocks as strategies (Ruby idiom)
class Formatter
  def initialize(&format_block)
    @format_block = format_block
  end
  
  def format(data)
    @format_block.call(data)
  end
end

json_formatter = Formatter.new { |data| data.to_json }
xml_formatter = Formatter.new { |data| "<data>#{data}</data>" }

# ============================================================================
# 6. DECORATOR PATTERN
# ============================================================================

puts "\n" + "=" * 40
puts "6. DECORATOR PATTERN"
puts "=" * 40

puts <<~DECORATOR_INTRO

  DECORATOR:
  • Adds behavior to objects dynamically
  • Alternative to subclassing
  • Wraps original object with new functionality

DECORATOR_INTRO

# Coffee example
class Coffee
  def cost
    2.0
  end
  
  def description
    "Simple coffee"
  end
end

class MilkDecorator
  def initialize(coffee)
    @coffee = coffee
  end
  
  def cost
    @coffee.cost + 0.5
  end
  
  def description
    "#{@coffee.description}, milk"
  end
end

class SugarDecorator
  def initialize(coffee)
    @coffee = coffee
  end
  
  def cost
    @coffee.cost + 0.2
  end
  
  def description
    "#{@coffee.description}, sugar"
  end
end

class WhipDecorator
  def initialize(coffee)
    @coffee = coffee
  end
  
  def cost
    @coffee.cost + 0.7
  end
  
  def description
    "#{@coffee.description}, whipped cream"
  end
end

# Usage
coffee = Coffee.new
coffee = MilkDecorator.new(coffee)
coffee = SugarDecorator.new(coffee)
coffee = WhipDecorator.new(coffee)

puts "#{coffee.description}: $#{coffee.cost}"

# Using SimpleDelegator (Ruby way)
require 'delegate'

class CoffeeWithMilk < SimpleDelegator
  def cost
    __getobj__.cost + 0.5
  end
  
  def description
    "#{__getobj__.description}, milk"
  end
end

simple_coffee = Coffee.new
fancy_coffee = CoffeeWithMilk.new(simple_coffee)
puts "#{fancy_coffee.description}: $#{fancy_coffee.cost}"

# ============================================================================
# 7. ADAPTER PATTERN
# ============================================================================

puts "\n" + "=" * 40
puts "7. ADAPTER PATTERN"
puts "=" * 40

puts <<~ADAPTER_INTRO

  ADAPTER:
  • Converts interface of class into another interface
  • Allows incompatible interfaces to work together
  • Wrapper around existing class

ADAPTER_INTRO

# Legacy payment system
class LegacyPaymentGateway
  def process_payment_old_way(card_info, amount_in_cents)
    puts "Legacy: Processing #{amount_in_cents} cents"
    { success: true, transaction_id: "LEG-#{rand(1000)}" }
  end
end

# Modern interface
class ModernPaymentProcessor
  def process(amount:, card:)
    raise NotImplementedError
  end
end

# Adapter
class PaymentAdapter < ModernPaymentProcessor
  def initialize
    @legacy_gateway = LegacyPaymentGateway.new
  end
  
  def process(amount:, card:)
    amount_in_cents = (amount * 100).to_i
    result = @legacy_gateway.process_payment_old_way(card, amount_in_cents)
    
    {
      success: result[:success],
      transaction_id: result[:transaction_id],
      amount: amount
    }
  end
end

# Usage
processor = PaymentAdapter.new
result = processor.process(amount: 49.99, card: "4111111111111111")
puts "Modern result: #{result}"

# ============================================================================
# 8. TEMPLATE METHOD PATTERN
# ============================================================================

puts "\n" + "=" * 40
puts "8. TEMPLATE METHOD PATTERN"
puts "=" * 40

puts <<~TEMPLATE_INTRO

  TEMPLATE METHOD:
  • Defines skeleton of algorithm in base class
  • Subclasses override specific steps
  • Promotes code reuse

TEMPLATE_INTRO

class DataMiner
  # Template method
  def mine(path)
    file = open_file(path)
    data = extract_data(file)
    parsed = parse_data(data)
    analyzed = analyze(parsed)
    report = send_report(analyzed)
    close_file(file)
    report
  end
  
  def open_file(path)
    puts "Opening file: #{path}"
    path
  end
  
  def extract_data(file)
    raise NotImplementedError, "Subclass must implement"
  end
  
  def parse_data(data)
    raise NotImplementedError, "Subclass must implement"
  end
  
  def analyze(data)
    puts "Analyzing data..."
    data
  end
  
  def send_report(data)
    puts "Sending report..."
    "Report sent"
  end
  
  def close_file(file)
    puts "Closing file: #{file}"
  end
end

class CSVDataMiner < DataMiner
  def extract_data(file)
    puts "Extracting CSV data"
    "csv,data,here"
  end
  
  def parse_data(data)
    puts "Parsing CSV"
    data.split(',')
  end
end

class JSONDataMiner < DataMiner
  def extract_data(file)
    puts "Extracting JSON data"
    '{"key": "value"}'
  end
  
  def parse_data(data)
    puts "Parsing JSON"
    require 'json'
    JSON.parse(data)
  end
end

# Usage
puts "\n--- CSV Mining ---"
csv_miner = CSVDataMiner.new
csv_miner.mine("data.csv")

puts "\n--- JSON Mining ---"
json_miner = JSONDataMiner.new
json_miner.mine("data.json")

# ============================================================================
# 9. COMMAND PATTERN
# ============================================================================

puts "\n" + "=" * 40
puts "9. COMMAND PATTERN"
puts "=" * 40

puts <<~COMMAND_INTRO

  COMMAND:
  • Encapsulates request as object
  • Allows parameterization and queuing
  • Supports undo/redo operations

COMMAND_INTRO

class Command
  def execute
    raise NotImplementedError
  end
  
  def undo
    raise NotImplementedError
  end
end

class Document
  attr_accessor :content
  
  def initialize
    @content = ""
  end
end

class InsertTextCommand < Command
  def initialize(document, text, position)
    @document = document
    @text = text
    @position = position
  end
  
  def execute
    @document.content.insert(@position, @text)
    puts "Inserted: '#{@text}'"
  end
  
  def undo
    @document.content.slice!(@position, @text.length)
    puts "Undid insert: '#{@text}'"
  end
end

class DeleteTextCommand < Command
  def initialize(document, start_pos, length)
    @document = document
    @start_pos = start_pos
    @length = length
    @deleted_text = nil
  end
  
  def execute
    @deleted_text = @document.content.slice!(@start_pos, @length)
    puts "Deleted: '#{@deleted_text}'"
  end
  
  def undo
    @document.content.insert(@start_pos, @deleted_text)
    puts "Undid delete: '#{@deleted_text}'"
  end
end

class CommandHistory
  def initialize
    @commands = []
    @current = -1
  end
  
  def execute(command)
    command.execute
    @commands = @commands[0..@current]
    @commands << command
    @current += 1
  end
  
  def undo
    if @current >= 0
      @commands[@current].undo
      @current -= 1
    else
      puts "Nothing to undo"
    end
  end
  
  def redo
    if @current < @commands.length - 1
      @current += 1
      @commands[@current].execute
    else
      puts "Nothing to redo"
    end
  end
end

# Usage
doc = Document.new
history = CommandHistory.new

history.execute(InsertTextCommand.new(doc, "Hello", 0))
history.execute(InsertTextCommand.new(doc, " World", 5))
puts "Content: '#{doc.content}'"

history.undo
puts "After undo: '#{doc.content}'"

history.redo
puts "After redo: '#{doc.content}'"

# ============================================================================
# 10. MODULE MIXIN PATTERN (RUBY-SPECIFIC)
# ============================================================================

puts "\n" + "=" * 40
puts "10. MODULE MIXIN PATTERN"
puts "=" * 40

puts <<~MIXIN_INTRO

  MODULE MIXINS:
  • Ruby's answer to multiple inheritance
  • Share behavior across classes
  • More flexible than inheritance

MIXIN_INTRO

module Timestampable
  def created_at
    @created_at ||= Time.now
  end
  
  def updated_at
    @updated_at || created_at
  end
  
  def touch
    @updated_at = Time.now
  end
end

module Sluggable
  def slug
    @slug ||= name.downcase.gsub(/\s+/, '-')
  end
end

class Post
  include Timestampable
  include Sluggable
  
  attr_accessor :name, :content
  
  def initialize(name, content)
    @name = name
    @content = content
  end
end

class User
  include Timestampable
  
  attr_accessor :name, :email
  
  def initialize(name, email)
    @name = name
    @email = email
  end
end

# Usage
post = Post.new("My First Post", "Content here")
puts "Post created: #{post.created_at}"
puts "Post slug: #{post.slug}"

sleep 0.1
post.touch
puts "Post updated: #{post.updated_at}"

user = User.new("Alice", "alice@example.com")
puts "User created: #{user.created_at}"

# ============================================================================
# 11. BEST PRACTICES
# ============================================================================

puts "\n" + "=" * 40
puts "11. DESIGN PATTERN BEST PRACTICES"
puts "=" * 40

puts <<~BEST_PRACTICES

  WHEN TO USE PATTERNS:
  ✓ Solve recurring problems
  ✓ Improve code maintainability
  ✓ Communicate design intent
  ✗ Don't force patterns where they don't fit
  ✗ Don't over-engineer simple problems
  
  RUBY-SPECIFIC CONSIDERATIONS:
  • Duck typing reduces need for some patterns
  • Blocks/procs replace some behavioral patterns
  • Modules/mixins replace some structural patterns
  • Dynamic typing simplifies some creational patterns
  
  PATTERN SELECTION:
  
  Object Creation:
  • Singleton: One instance needed
  • Factory: Complex creation logic
  • Builder: Many optional parameters
  
  Behavior:
  • Strategy: Interchangeable algorithms
  • Observer: Event notification
  • Command: Encapsulate actions
  • Template Method: Shared algorithm structure
  
  Structure:
  • Decorator: Add behavior dynamically
  • Adapter: Interface compatibility
  • Mixin: Share behavior (Ruby-specific)
  
  AVOID ANTI-PATTERNS:
  ✗ God Object: One class does everything
  ✗ Spaghetti Code: No structure
  ✗ Copy-Paste Programming: Duplicate code
  ✗ Golden Hammer: Using same pattern everywhere
  ✗ Premature Optimization: Patterns before need

BEST_PRACTICES

puts "\n=== Complete ==="
