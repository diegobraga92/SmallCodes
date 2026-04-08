# ============================================
# ADVANCED OOP & DESIGN PATTERNS IN RUBY
# ============================================

# ============================================
# 1. COMPOSITION VS INHERITANCE
# ============================================
puts "=" * 60
puts "1. COMPOSITION VS INHERITANCE"
puts "=" * 60

puts <<~CONCEPT

  INHERITANCE: "IS-A" relationship
  • Class inherits behavior from parent class
  • Tight coupling between parent and child
  • Can lead to fragile base class problem
  • Use when there's a clear hierarchical relationship
  
  COMPOSITION: "HAS-A" relationship
  • Objects contain other objects as dependencies
  • Loose coupling, more flexible
  • Easier to test and modify
  • Prefer composition over inheritance (Gang of Four)

CONCEPT

# ----- BAD EXAMPLE: Overusing Inheritance -----
puts "\n--- Bad Example: Rigid inheritance hierarchy ---"

class Animal
  attr_reader :name
  
  def initialize(name)
    @name = name
  end
  
  def eat
    puts "#{name} is eating"
  end
  
  def sleep
    puts "#{name} is sleeping"
  end
end

class Bird < Animal
  def fly
    puts "#{name} is flying"
  end
end

class Penguin < Bird
  # Penguins can't fly! This breaks the Liskov Substitution Principle
  def fly
    puts "#{name} cannot fly - they're flightless birds!"
  end
end

class Dog < Animal
  def bark
    puts "#{name} is barking"
  end
end

puts "Inheritance issues:"
bird = Bird.new("Eagle")
bird.fly  # Works fine

penguin = Penguin.new("Penguin")
penguin.fly  # Breaks the expectation - penguin inherited fly but can't fly

# ----- GOOD EXAMPLE: Composition over Inheritance -----
puts "\n--- Good Example: Using composition for flexible design ---"

# Behaviors as separate modules/classes
module Flyable
  def fly
    puts "#{name} is flying through the air"
  end
end

module Swimmable
  def swim
    puts "#{name} is swimming in the water"
  end
end

module Walkable
  def walk
    puts "#{name} is walking on the ground"
  end
end

# Behavior classes for composition
class FlyingBehavior
  def perform(name)
    puts "#{name} is flying through the air"
  end
end

class SwimmingBehavior
  def perform(name)
    puts "#{name} is swimming in the water"
  end
end

class WalkingBehavior
  def perform(name)
    puts "#{name} is walking on the ground"
  end
end

class NoFlyingBehavior
  def perform(name)
    puts "#{name} cannot fly"
  end
end

# Composed Animal class
class AnimalComposed
  attr_reader :name
  attr_accessor :flying_behavior, :swimming_behavior, :walking_behavior
  
  def initialize(name, flying_behavior = nil, swimming_behavior = nil, walking_behavior = nil)
    @name = name
    @flying_behavior = flying_behavior || WalkingBehavior.new
    @swimming_behavior = swimming_behavior
    @walking_behavior = walking_behavior
  end
  
  def fly
    @flying_behavior.perform(name) if @flying_behavior
  end
  
  def swim
    @swimming_behavior.perform(name) if @swimming_behavior
  end
  
  def walk
    @walking_behavior.perform(name) if @walking_behavior
  end
end

puts "Composition in action:"
eagle = AnimalComposed.new("Eagle", FlyingBehavior.new, nil, WalkingBehavior.new)
eagle.fly
eagle.walk

penguin = AnimalComposed.new("Penguin", NoFlyingBehavior.new, SwimmingBehavior.new, WalkingBehavior.new)
penguin.fly
penguin.swim
penguin.walk

fish = AnimalComposed.new("Salmon", nil, SwimmingBehavior.new, nil)
fish.swim

# ----- Real-world example: Notifications system -----
puts "\n--- Real-world: Notification system with composition ---"

# Composable notification channels
class EmailChannel
  def deliver(notification)
    puts "📧 Sending email to #{notification.user.email}: #{notification.message}"
    # Actual email sending logic
  end
end

class SMSChannel
  def deliver(notification)
    puts "📱 Sending SMS to #{notification.user.phone}: #{notification.message}"
    # Actual SMS sending logic
  end
end

class PushChannel
  def deliver(notification)
    puts "🔔 Sending push notification to #{notification.user.device_token}: #{notification.message}"
    # Actual push notification logic
  end
end

class SlackChannel
  def deliver(notification)
    puts "💬 Sending Slack message to #{notification.user.slack_id}: #{notification.message}"
    # Actual Slack integration
  end
end

# Notification class using composition
class Notification
  attr_reader :user, :message, :channels
  
  def initialize(user, message, channels = [])
    @user = user
    @message = message
    @channels = channels
  end
  
  def deliver
    @channels.each do |channel|
      channel.deliver(self)
    end
  end
  
  def add_channel(channel)
    @channels << channel
  end
end

# User class
class User
  attr_reader :name, :email, :phone, :device_token, :slack_id
  
  def initialize(name, email: nil, phone: nil, device_token: nil, slack_id: nil)
    @name = name
    @email = email
    @phone = phone
    @device_token = device_token
    @slack_id = slack_id
  end
end

puts "\nCreating notifications with different channel combinations:"
user = User.new("Alice", email: "alice@example.com", phone: "+1234567890", slack_id: "@alice")

# User can receive notifications through multiple channels
notification = Notification.new(
  user,
  "Your order has been shipped!",
  [EmailChannel.new, SMSChannel.new]
)
notification.deliver

# Add another channel dynamically
notification.add_channel(PushChannel.new)
puts "\nAfter adding push channel:"
notification.deliver

# ============================================
# 2. MODULES AND MIXINS
# ============================================
puts "\n" + "=" * 60
puts "2. MODULES AND MIXINS"
puts "=" * 60

puts <<~MODULES

  MODULES IN RUBY:
  • Cannot be instantiated
  • Used for namespacing and mixins
  • Provide a way to share behavior across classes
  • Ruby's solution to multiple inheritance
  
  MIXINS:
  • Include module - adds instance methods
  • Extend module - adds class methods
  • Prepend module - method lookup override

MODULES

# ----- Basic module for shared behavior -----
module Loggable
  def log(message, level: :info)
    timestamp = Time.now.strftime("%Y-%m-%d %H:%M:%S")
    puts "[#{timestamp}] [#{level.upcase}] [#{self.class}] #{message}"
  end
  
  def log_error(error)
    log(error.message, level: :error)
    log(error.backtrace.first(3).join("\n"), level: :debug)
  end
end

module Serializable
  def to_hash
    instance_variables.each_with_object({}) do |var, hash|
      key = var.to_s.delete('@')
      hash[key] = instance_variable_get(var)
    end
  end
  
  def to_json
    require 'json'
    to_hash.to_json
  end
  
  def from_hash(hash)
    hash.each do |key, value|
      instance_variable_set("@#{key}", value)
    end
  end
end

# Using modules as mixins
class Product
  include Loggable
  include Serializable
  
  attr_accessor :name, :price, :sku
  
  def initialize(name, price, sku)
    @name = name
    @price = price
    @sku = sku
    log("Product created: #{name}")
  end
  
  def apply_discount(percentage)
    @price -= @price * percentage / 100.0
    log("Discount applied: #{percentage}% - New price: $#{@price}")
  end
end

puts "\nUsing Loggable and Serializable mixins:"
product = Product.new("Laptop", 999.99, "LAP-001")
product.apply_discount(10)
puts "Product as JSON: #{product.to_json}"

# ----- Module for class methods -----
module Findable
  def self.included(base)
    base.extend(ClassMethods)
  end
  
  module ClassMethods
    def find(id)
      puts "Finding #{self.name} with ID: #{id}"
      # Simulated database lookup
      nil
    end
    
    def all
      puts "Retrieving all #{self.name}s"
      []
    end
  end
end

class Customer
  include Findable
  include Loggable
  
  attr_accessor :id, :name, :email
  
  def initialize(id, name, email)
    @id = id
    @name = name
    @email = email
    log("Customer created: #{name}")
  end
end

puts "\nUsing module with class methods:"
Customer.find(123)
Customer.all
customer = Customer.new(1, "Bob Smith", "bob@example.com")

# ----- Using prepend for method wrapping -----
module Timer
  def self.prepended(base)
    puts "Timer module prepended to #{base}"
  end
  
  def method_missing(name, *args, &block)
    if respond_to_missing?(name)
      start_time = Time.now
      result = super
      elapsed = Time.now - start_time
      puts "⏱️  #{name} took #{'%.3f' % elapsed} seconds"
      result
    else
      super
    end
  end
  
  def respond_to_missing?(name, include_private = false)
    true
  end
end

class DataProcessor
  prepend Timer
  
  def process_large_dataset
    sleep(0.5)
    "Processing complete"
  end
  
  def calculate_complex_math
    sleep(0.3)
    42
  end
end

puts "\nUsing prepend to wrap methods:"
processor = DataProcessor.new
processor.process_large_dataset
processor.calculate_complex_math

# ----- Namespacing with modules -----
module ECommerce
  module Models
    class Order
      attr_reader :id, :total
      
      def initialize(id, total)
        @id = id
        @total = total
      end
    end
    
    class Customer
      attr_reader :name
      
      def initialize(name)
        @name = name
      end
    end
  end
  
  module Services
    class PaymentProcessor
      def process(order)
        puts "Processing payment for order ##{order.id}: $#{order.total}"
      end
    end
    
    class EmailService
      def send_confirmation(customer, order)
        puts "Sending confirmation email to #{customer.name} for order ##{order.id}"
      end
    end
  end
end

puts "\nUsing modules for namespacing:"
order = ECommerce::Models::Order.new(12345, 299.99)
customer = ECommerce::Models::Customer.new("Alice")
payment = ECommerce::Services::PaymentProcessor.new
email = ECommerce::Services::EmailService.new

payment.process(order)
email.send_confirmation(customer, order)

# ============================================
# 3. DEPENDENCY INJECTION
# ============================================
puts "\n" + "=" * 60
puts "3. DEPENDENCY INJECTION"
puts "=" * 60

puts <<~DI

  DEPENDENCY INJECTION PRINCIPLES:
  • Dependencies are provided from outside (not created internally)
  • Makes code more testable, flexible, and maintainable
  • Reduces coupling between classes
  • Follows the Dependency Inversion Principle

DI

# ----- BAD EXAMPLE: Tight coupling -----
puts "\n--- Bad Example: Hard-coded dependencies ---"

class ReportGenerator
  def initialize
    # Hard-coded dependency - difficult to test and change
    @database = MySQLDatabase.new
    @formatter = PDFFormatter.new
    @mailer = SMTPMailer.new
  end
  
  def generate_report(data)
    @database.query(data)
    @formatter.format
    @mailer.send
  end
end

# ----- GOOD EXAMPLE: Constructor injection -----
puts "\n--- Good Example: Constructor injection ---"

# Define interfaces (duck typing)
class Database
  def query(sql)
    raise NotImplementedError
  end
end

class Formatter
  def format(data)
    raise NotImplementedError
  end
end

class Mailer
  def send(recipient, subject, body)
    raise NotImplementedError
  end
end

# Concrete implementations
class MySQLDatabase
  def query(sql)
    puts "MySQL: Executing #{sql}"
    [{ id: 1, name: "Product 1", price: 100 }]
  end
end

class PostgresDatabase
  def query(sql)
    puts "PostgreSQL: Executing #{sql}"
    [{ id: 1, name: "Product 1", price: 100 }]
  end
end

class JSONFormatter
  def format(data)
    puts "Formatting as JSON"
    require 'json'
    data.to_json
  end
end

class HTMLFormatter
  def format(data)
    puts "Formatting as HTML"
    "<html><body>#{data}</body></html>"
  end
end

class SMTPMailer
  def send(recipient, subject, body)
    puts "SMTP: Sending to #{recipient}: #{subject}"
  end
end

class SendgridMailer
  def send(recipient, subject, body)
    puts "Sendgrid: Sending to #{recipient}: #{subject}"
  end
end

# ReportGenerator with dependency injection
class ReportGenerator
  attr_reader :database, :formatter, :mailer
  
  def initialize(database, formatter, mailer)
    @database = database
    @formatter = formatter
    @mailer = mailer
  end
  
  def generate_report(sql, recipient)
    # Use injected dependencies
    data = @database.query(sql)
    formatted = @formatter.format(data)
    @mailer.send(recipient, "Daily Report", formatted)
    
    { success: true, data: data }
  end
end

puts "\nCreating report generator with different configurations:"

# Production configuration
production_report = ReportGenerator.new(
  MySQLDatabase.new,
  JSONFormatter.new,
  SMTPMailer.new
)
production_report.generate_report("SELECT * FROM products", "admin@example.com")

# Development configuration (different dependencies)
dev_report = ReportGenerator.new(
  PostgresDatabase.new,
  HTMLFormatter.new,
  SendgridMailer.new
)
dev_report.generate_report("SELECT * FROM products", "dev@example.com")

# ----- Setter injection -----
puts "\n--- Setter injection (flexible dependencies) ---"

class OrderProcessor
  attr_accessor :payment_gateway, :inventory_service, :notification_service
  
  def initialize(payment_gateway = nil)
    @payment_gateway = payment_gateway || DefaultPaymentGateway.new
  end
  
  def process(order)
    # Check inventory (optional dependency)
    if @inventory_service
      return false unless @inventory_service.check_availability(order)
    end
    
    # Process payment
    @payment_gateway.charge(order.total)
    
    # Send notification (optional)
    @notification_service.notify(order.customer, "Order processed") if @notification_service
    
    true
  end
end

# ----- Method injection -----
puts "\n--- Method injection (passing dependencies at call time) ---"

class DataExporter
  def export(data, formatter, writer)
    formatted = formatter.format(data)
    writer.write(formatted)
  end
end

class CSVFormatter
  def format(data)
    data.map { |row| row.join(',') }.join("\n")
  end
end

class FileWriter
  def write(content)
    puts "Writing to file: #{content}"
  end
end

class S3Writer
  def write(content)
    puts "Uploading to S3: #{content}"
  end
end

exporter = DataExporter.new
exporter.export([[1, "Product A"], [2, "Product B"]], CSVFormatter.new, FileWriter.new)
exporter.export([[1, "Product A"], [2, "Product B"]], CSVFormatter.new, S3Writer.new)

# ============================================
# 4. SOLID PRINCIPLES IN RUBY
# ============================================
puts "\n" + "=" * 60
puts "4. SOLID PRINCIPLES IN RUBY"
puts "=" * 60

puts <<~SOLID

  SOLID PRINCIPLES:
  
  S - Single Responsibility Principle (SRP)
      A class should have only one reason to change
      
  O - Open/Closed Principle (OCP)
      Classes should be open for extension but closed for modification
      
  L - Liskov Substitution Principle (LSP)
      Objects should be replaceable with instances of their subtypes
      
  I - Interface Segregation Principle (ISP)
      Many client-specific interfaces are better than one general-purpose interface
      
  D - Dependency Inversion Principle (DIP)
      Depend on abstractions, not concretions

SOLID

# ----- S: Single Responsibility Principle -----
puts "\n--- S: Single Responsibility Principle ---"

# BAD: Class with multiple responsibilities
class BadUserManager
  def create_user(name, email)
    # Validation
    raise "Invalid email" unless email.include?('@')
    
    # Database operation
    puts "Saving user to database"
    
    # Email notification
    puts "Sending welcome email to #{email}"
    
    # Logging
    puts "User created: #{name}"
  end
  
  def delete_user(id)
    # Database operation
    puts "Deleting user from database"
    
    # Audit logging
    puts "Audit: User #{id} deleted"
    
    # Notification
    puts "Sending deletion confirmation"
  end
end

# GOOD: Separated responsibilities
class UserValidator
  def validate_email(email)
    raise "Invalid email" unless email.include?('@')
    true
  end
end

class UserRepository
  def save(user)
    puts "Saving user to database"
  end
  
  def delete(id)
    puts "Deleting user from database"
  end
end

class UserNotifier
  def send_welcome(user)
    puts "Sending welcome email to #{user.email}"
  end
  
  def send_deletion_confirmation(user)
    puts "Sending deletion confirmation"
  end
end

class AuditLogger
  def log(action, details)
    puts "Audit: #{action} - #{details}"
  end
end

class UserManager
  def initialize(validator, repository, notifier, logger)
    @validator = validator
    @repository = repository
    @notifier = notifier
    @logger = logger
  end
  
  def create_user(name, email)
    @validator.validate_email(email)
    user = { name: name, email: email }
    @repository.save(user)
    @notifier.send_welcome(user)
    @logger.log("create_user", "User #{name} created")
  end
  
  def delete_user(id)
    user = { id: id }
    @repository.delete(id)
    @notifier.send_deletion_confirmation(user)
    @logger.log("delete_user", "User #{id} deleted")
  end
end

# ----- O: Open/Closed Principle -----
puts "\n--- O: Open/Closed Principle ---"

# BAD: Modifying existing code to add features
class BadPaymentProcessor
  def process(payment_type, amount)
    if payment_type == :credit_card
      puts "Processing credit card payment: $#{amount}"
    elsif payment_type == :paypal
      puts "Processing PayPal payment: $#{amount}"
    elsif payment_type == :bitcoin  # New feature requires modification
      puts "Processing Bitcoin payment: $#{amount}"
    end
  end
end

# GOOD: Open for extension, closed for modification
class PaymentMethod
  def process(amount)
    raise NotImplementedError
  end
end

class CreditCardPayment < PaymentMethod
  def process(amount)
    puts "Processing credit card payment: $#{amount}"
    { status: :success, transaction_id: "CC_#{Time.now.to_i}" }
  end
end

class PayPalPayment < PaymentMethod
  def process(amount)
    puts "Processing PayPal payment: $#{amount}"
    { status: :success, transaction_id: "PP_#{Time.now.to_i}" }
  end
end

class BitcoinPayment < PaymentMethod
  def process(amount)
    puts "Processing Bitcoin payment: #{amount} BTC"
    { status: :success, transaction_id: "BTC_#{Time.now.to_i}" }
  end
end

class PaymentProcessor
  def process(payment_method, amount)
    payment_method.process(amount)
  end
end

processor = PaymentProcessor.new
processor.process(CreditCardPayment.new, 100)
processor.process(PayPalPayment.new, 50)
processor.process(BitcoinPayment.new, 0.5)  # New feature without modifying existing code

# ----- L: Liskov Substitution Principle -----
puts "\n--- L: Liskov Substitution Principle ---"

# BAD: Violating LSP
class Bird
  def fly
    "Flying"
  end
end

class Ostrich < Bird
  def fly
    raise "Can't fly"  # Violates LSP - can't substitute Bird
  end
end

# GOOD: Following LSP
class BirdLSP
  def move
    raise NotImplementedError
  end
end

class FlyingBird < BirdLSP
  def move
    "Flying"
  end
end

class WalkingBird < BirdLSP
  def move
    "Walking"
  end
end

class Sparrow < FlyingBird; end
class OstrichLSP < WalkingBird; end

def make_bird_move(bird)
  puts bird.move
end

make_bird_move(Sparrow.new)
make_bird_move(OstrichLSP.new)

# ----- I: Interface Segregation Principle -----
puts "\n--- I: Interface Segregation Principle ---"

# BAD: Fat interface
module Worker
  def work; end
  def eat; end
  def sleep; end
  def code; end
  def test; end
  def deploy; end
  def attend_meeting; end
end

class Developer
  include Worker
  # Forced to implement all methods even if not relevant
end

# GOOD: Segregated interfaces
module Workable
  def work; end
end

module Eatable
  def eat; end
end

module Sleepable
  def sleep; end
end

module Codable
  def code; end
end

module Testable
  def test; end
end

module Deployable
  def deploy; end
end

class GoodDeveloper
  include Workable, Eatable, Sleepable, Codable, Testable
  
  def work
    puts "Writing code"
  end
  
  def eat
    puts "Eating lunch"
  end
  
  def sleep
    puts "Sleeping 8 hours"
  end
  
  def code
    puts "Writing Ruby code"
  end
  
  def test
    puts "Writing tests"
  end
end

class Manager
  include Workable, Eatable, Sleepable, AttendMeetingable
  
  def work
    puts "Managing team"
  end
  
  def eat
    puts "Eating at desk"
  end
  
  def sleep
    puts "Sleeping 6 hours"
  end
  
  def attend_meeting
    puts "In meetings all day"
  end
end

# ----- D: Dependency Inversion Principle -----
puts "\n--- D: Dependency Inversion Principle ---"

# BAD: High-level module depends on low-level details
class BadNotificationService
  def send(message)
    # Direct dependency on SMTP
    smtp = SMTPServer.new
    smtp.send_email(message)
  end
end

# GOOD: Depend on abstractions
class MessageSender
  def send(message)
    raise NotImplementedError
  end
end

class EmailSender < MessageSender
  def send(message)
    puts "Sending email: #{message}"
  end
end

class SMSSender < MessageSender
  def send(message)
    puts "Sending SMS: #{message}"
  end
end

class SlackSender < MessageSender
  def send(message)
    puts "Sending Slack message: #{message}"
  end
end

class NotificationService
  def initialize(sender)
    @sender = sender
  end
  
  def notify(message)
    @sender.send(message)
  end
end

service = NotificationService.new(EmailSender.new)
service.notify("Hello via email")

service = NotificationService.new(SlackSender.new)
service.notify("Hello via Slack")

# ============================================
# 5. DESIGN PATTERNS
# ============================================
puts "\n" + "=" * 60
puts "5. DESIGN PATTERNS"
puts "=" * 60

# ----- Factory Pattern -----
puts "\n--- Factory Pattern ---"

class Document
  attr_reader :title, :content
  
  def initialize(title, content)
    @title = title
    @content = content
  end
  
  def export
    raise NotImplementedError
  end
end

class PDFDocument < Document
  def export
    puts "Exporting '#{@title}' as PDF"
    "#{@content}\n[PDF Metadata]"
  end
end

class HTMLDocument < Document
  def export
    puts "Exporting '#{@title}' as HTML"
    "<html><body><h1>#{@title}</h1><p>#{@content}</p></body></html>"
  end
end

class MarkdownDocument < Document
  def export
    puts "Exporting '#{@title}' as Markdown"
    "# #{@title}\n\n#{@content}"
  end
end

class DocumentFactory
  TYPES = {
    pdf: PDFDocument,
    html: HTMLDocument,
    markdown: MarkdownDocument
  }
  
  def self.create(type, title, content)
    klass = TYPES[type.to_sym]
    raise "Unknown document type: #{type}" unless klass
    klass.new(title, content)
  end
end

puts "Factory Pattern Example:"
pdf = DocumentFactory.create(:pdf, "Report 2024", "Annual report content")
pdf.export

html = DocumentFactory.create(:html, "Homepage", "Welcome to our site")
html.export

# ----- Strategy Pattern -----
puts "\n--- Strategy Pattern ---"

class ShippingStrategy
  def calculate(weight, distance)
    raise NotImplementedError
  end
end

class StandardShipping < ShippingStrategy
  def calculate(weight, distance)
    base_cost = 5.0
    weight_cost = weight * 0.5
    distance_cost = distance * 0.1
    (base_cost + weight_cost + distance_cost).round(2)
  end
end

class ExpressShipping < ShippingStrategy
  def calculate(weight, distance)
    base_cost = 10.0
    weight_cost = weight * 1.0
    distance_cost = distance * 0.2
    (base_cost + weight_cost + distance_cost).round(2)
  end
end

class InternationalShipping < ShippingStrategy
  def calculate(weight, distance)
    base_cost = 20.0
    weight_cost = weight * 2.0
    distance_cost = distance * 0.5
    customs_fee = 15.0
    (base_cost + weight_cost + distance_cost + customs_fee).round(2)
  end
end

class Order
  attr_reader :weight, :distance
  attr_accessor :shipping_strategy
  
  def initialize(weight, distance, shipping_strategy = StandardShipping.new)
    @weight = weight
    @distance = distance
    @shipping_strategy = shipping_strategy
  end
  
  def shipping_cost
    @shipping_strategy.calculate(@weight, @distance)
  end
end

puts "\nStrategy Pattern Example:"
order = Order.new(10, 100)
puts "Standard shipping: $#{order.shipping_cost}"

order.shipping_strategy = ExpressShipping.new
puts "Express shipping: $#{order.shipping_cost}"

order.shipping_strategy = InternationalShipping.new
puts "International shipping: $#{order.shipping_cost}"

# ----- Decorator Pattern -----
puts "\n--- Decorator Pattern ---"

class Coffee
  def cost
    2.0
  end
  
  def description
    "Coffee"
  end
end

class CoffeeDecorator
  attr_reader :coffee
  
  def initialize(coffee)
    @coffee = coffee
  end
  
  def cost
    @coffee.cost
  end
  
  def description
    @coffee.description
  end
end

class MilkDecorator < CoffeeDecorator
  def cost
    @coffee.cost + 0.5
  end
  
  def description
    "#{@coffee.description}, with milk"
  end
end

class SugarDecorator < CoffeeDecorator
  def cost
    @coffee.cost + 0.2
  end
  
  def description
    "#{@coffee.description}, with sugar"
  end
end

class WhippedCreamDecorator < CoffeeDecorator
  def cost
    @coffee.cost + 0.7
  end
  
  def description
    "#{@coffee.description}, with whipped cream"
  end
end

class CaramelDecorator < CoffeeDecorator
  def cost
    @coffee.cost + 0.8
  end
  
  def description
    "#{@coffee.description}, with caramel"
  end
end

puts "\nDecorator Pattern Example:"
coffee = Coffee.new
puts "#{coffee.description}: $#{coffee.cost}"

coffee_with_milk = MilkDecorator.new(coffee)
puts "#{coffee_with_milk.description}: $#{coffee_with_milk.cost}"

coffee_with_milk_sugar = SugarDecorator.new(coffee_with_milk)
puts "#{coffee_with_milk_sugar.description}: $#{coffee_with_milk_sugar.cost}"

gourmet_coffee = CaramelDecorator.new(WhippedCreamDecorator.new(MilkDecorator.new(Coffee.new)))
puts "#{gourmet_coffee.description}: $#{gourmet_coffee.cost}"

# ----- Observer Pattern -----
puts "\n--- Observer Pattern ---"

module Observable
  def observers
    @observers ||= []
  end
  
  def add_observer(observer)
    observers << observer
  end
  
  def remove_observer(observer)
    observers.delete(observer)
  end
  
  def notify_observers(event, data)
    observers.each do |observer|
      observer.update(event, data)
    end
  end
end

class Product
  include Observable
  
  attr_reader :name, :price, :stock
  
  def initialize(name, price, stock)
    @name = name
    @price = price
    @stock = stock
  end
  
  def price=(new_price)
    @price = new_price
    notify_observers(:price_change, { product: @name, old_price: @price, new_price: new_price })
  end
  
  def stock=(new_stock)
    @stock = new_stock
    notify_observers(:stock_change, { product: @name, old_stock: @stock, new_stock: new_stock })
  end
end

class InventoryManager
  def update(event, data)
    case event
    when :stock_change
      if data[:new_stock] < 5
        puts "⚠️  INVENTORY ALERT: #{data[:product]} is running low! Only #{data[:new_stock]} left"
      end
    end
  end
end

class PriceTracker
  def update(event, data)
    case event
    when :price_change
      puts "💰 PRICE ALERT: #{data[:product]} price changed to $#{data[:new_price]}"
    end
  end
end

class EmailNotifier
  def update(event, data)
    puts "📧 SENDING EMAIL: #{event} on #{data[:product]}"
  end
end

puts "\nObserver Pattern Example:"
product = Product.new("Laptop", 999.99, 10)

inventory = InventoryManager.new
price_tracker = PriceTracker.new
email = EmailNotifier.new

product.add_observer(inventory)
product.add_observer(price_tracker)
product.add_observer(email)

puts "\nUpdating stock:"
product.stock = 3

puts "\nUpdating price:"
product.price = 899.99

# ----- Singleton Pattern -----
puts "\n--- Singleton Pattern ---"

require 'singleton'

class Configuration
  include Singleton
  
  attr_accessor :api_key, :environment, :debug_mode
  
  def initialize
    @environment = "development"
    @debug_mode = true
    @api_key = "default_key"
    puts "Configuration instance created"
  end
  
  def load_from_file(file)
    puts "Loading configuration from #{file}"
    # Simulate loading configuration
    @environment = "production"
    @api_key = "prod_key_123"
  end
  
  def to_s
    "Config[env=#{@environment}, debug=#{@debug_mode}, api=#{@api_key}]"
  end
end

puts "\nSingleton Pattern Example:"
config1 = Configuration.instance
puts config1

config2 = Configuration.instance
puts "Same instance? #{config1.object_id == config2.object_id}"

config1.api_key = "new_api_key_456"
puts config2  # Shows the same updated value

# ============================================
# 6. PRACTICAL EXAMPLE: E-COMMERCE SYSTEM
# ============================================
puts "\n" + "=" * 60
puts "6. PRACTICAL EXAMPLE: E-COMMERCE SYSTEM"
puts "=" * 60

# Combining multiple patterns in a real-world example

module DiscountStrategy
  class NoDiscount
    def apply(amount)
      amount
    end
  end
  
  class PercentageDiscount
    def initialize(percentage)
      @percentage = percentage
    end
    
    def apply(amount)
      amount * (1 - @percentage / 100.0)
    end
  end
  
  class FixedDiscount
    def initialize(amount)
      @discount_amount = amount
    end
    
    def apply(amount)
      [amount - @discount_amount, 0].max
    end
  end
  
  class BuyOneGetOneFree
    def apply(amount, quantity)
      # Simplified: assumes all items same price
      discountable_quantity = quantity / 2
      amount - (amount / quantity) * discountable_quantity
    end
  end
end

class TaxCalculator
  def self.calculate(amount, region)
    rates = {
      us: 0.08,
      eu: 0.20,
      uk: 0.20,
      default: 0.10
    }
    
    rate = rates[region] || rates[:default]
    amount * rate
  end
end

class PaymentGateway
  def self.process(amount, payment_method)
    puts "Processing $#{amount} via #{payment_method[:type]}"
    { success: true, transaction_id: "TXN_#{Time.now.to_i}" }
  end
end

class OrderItem
  attr_reader :product, :quantity, :unit_price
  
  def initialize(product, quantity, unit_price)
    @product = product
    @quantity = quantity
    @unit_price = unit_price
  end
  
  def subtotal
    @unit_price * @quantity
  end
end

class Order
  attr_reader :items, :discount_strategy, :region, :payment_method
  
  def initialize(region = :us, discount_strategy = DiscountStrategy::NoDiscount.new)
    @items = []
    @region = region
    @discount_strategy = discount_strategy
    @payment_method = nil
  end
  
  def add_item(product, quantity, unit_price)
    @items << OrderItem.new(product, quantity, unit_price)
  end
  
  def subtotal
    @items.sum(&:subtotal)
  end
  
  def discount
    if @discount_strategy.respond_to?(:apply_with_quantity)
      @discount_strategy.apply_with_quantity(subtotal, @items.sum(&:quantity))
    else
      @discount_strategy.apply(subtotal)
    end
  end
  
  def discounted_subtotal
    subtotal - discount
  end
  
  def tax
    TaxCalculator.calculate(discounted_subtotal, @region)
  end
  
  def total
    discounted_subtotal + tax
  end
  
  def set_payment_method(type, details = {})
    @payment_method = { type: type, details: details }
  end
  
  def checkout
    raise "No payment method set" unless @payment_method
    
    puts "\n" + "=" * 40
    puts "ORDER SUMMARY"
    puts "=" * 40
    
    @items.each do |item|
      puts "#{item.product} x#{item.quantity}: $#{item.unit_price} = $#{item.subtotal}"
    end
    
    puts "-" * 40
    puts "Subtotal: $#{'%.2f' % subtotal}"
    puts "Discount: -$#{'%.2f' % discount}" if discount > 0
    puts "Tax: $#{'%.2f' % tax}"
    puts "Total: $#{'%.2f' % total}"
    puts "=" * 40
    
    # Process payment
    result = PaymentGateway.process(total, @payment_method)
    
    if result[:success]
      puts "✅ Order completed! Transaction ID: #{result[:transaction_id]}"
      true
    else
      puts "❌ Payment failed"
      false
    end
  end
end

puts "\nE-COMMERCE SYSTEM DEMONSTRATION:"

# Order with no discount
order1 = Order.new(:us)
order1.add_item("Laptop", 1, 999.99)
order1.add_item("Mouse", 2, 29.99)
order1.set_payment_method(:credit_card, last4: "1234")
order1.checkout

# Order with percentage discount
order2 = Order.new(:us, DiscountStrategy::PercentageDiscount.new(10))
order2.add_item("Smartphone", 1, 699.99)
order2.add_item("Case", 1, 29.99)
order2.set_payment_method(:paypal, email: "user@example.com")
order2.checkout

# Order with fixed discount
order3 = Order.new(:eu, DiscountStrategy::FixedDiscount.new(50))
order3.add_item("Tablet", 1, 399.99)
order3.set_payment_method(:apple_pay)
order3.checkout

# ============================================
# 7. SUMMARY AND BEST PRACTICES
# ============================================
puts "\n" + "=" * 60
puts "7. SUMMARY AND BEST PRACTICES"
puts "=" * 60

puts <<~SUMMARY

  ADVANCED OOP & DESIGN PATTERNS SUMMARY:
  
  COMPOSITION VS INHERITANCE
  ✅ Prefer composition over inheritance
  ✅ Use inheritance for "is-a" relationships
  ✅ Use composition for "has-a" relationships
  ✅ Favor interfaces/roles over deep hierarchies
  
  MODULES AND MIXINS
  ✅ Use modules for shared behavior
  ✅ Use include for instance methods
  ✅ Use extend for class methods
  ✅ Use prepend for method wrapping
  ✅ Use modules for namespacing
  
  DEPENDENCY INJECTION
  ✅ Inject dependencies rather than creating them internally
  ✅ Use constructor injection for required dependencies
  ✅ Use setter injection for optional dependencies
  ✅ Makes code more testable and flexible
  
  SOLID PRINCIPLES
  ✅ Single Responsibility: One reason to change per class
  ✅ Open/Closed: Open for extension, closed for modification
  ✅ Liskov Substitution: Subtypes must be substitutable
  ✅ Interface Segregation: Many specific interfaces > one general
  ✅ Dependency Inversion: Depend on abstractions, not concretions
  
  DESIGN PATTERNS
  ✅ Factory: Encapsulate object creation
  ✅ Strategy: Encapsulate algorithms
  ✅ Decorator: Add behavior dynamically
  ✅ Observer: Notify dependents of changes
  ✅ Singleton: Single instance with global access
  
  WHEN TO USE PATTERNS:
  • Factory: When creation logic is complex
  • Strategy: When multiple algorithms are interchangeable
  • Decorator: When adding responsibilities dynamically
  • Observer: When state changes need to notify others
  • Singleton: When exactly one instance is needed (use sparingly)

SUMMARY

puts "\n" + "=" * 60
puts "END OF ADVANCED OOP & DESIGN PATTERNS DEMONSTRATION"
puts "=" * 60