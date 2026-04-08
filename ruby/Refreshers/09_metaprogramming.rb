# ============================================
# RUBY METAPROGRAMMING DEEP DIVE
# ============================================

# ============================================
# 1. DEFINE_METHOD - DYNAMIC METHOD CREATION
# ============================================
puts "=" * 60
puts "1. DEFINE_METHOD - CREATING METHODS DYNAMICALLY"
puts "=" * 60

puts <<~DEFINE_METHOD_CONCEPT

  DEFINE_METHOD:
  • Creates methods dynamically at runtime
  • Takes a method name and a block as the method body
  • Allows for programmatic method generation
  • Great for reducing boilerplate code
  • Creates instance methods when called in class context

DEFINE_METHOD_CONCEPT

# ----- Basic define_method usage -----
puts "\n--- Basic define_method ---"

class DynamicCalculator
  # Define methods dynamically
  [:add, :subtract, :multiply, :divide].each do |operation|
    define_method(operation) do |a, b|
      case operation
      when :add
        a + b
      when :subtract
        a - b
      when :multiply
        a * b
      when :divide
        raise "Cannot divide by zero" if b == 0
        a.to_f / b
      end
    end
  end
end

calc = DynamicCalculator.new
puts "Add: #{calc.add(10, 5)}"
puts "Subtract: #{calc.subtract(10, 5)}"
puts "Multiply: #{calc.multiply(10, 5)}"
puts "Divide: #{calc.divide(10, 5)}"

# ----- Creating attribute-like methods -----
puts "\n--- Creating dynamic attribute methods ---"

class DynamicAttributes
  def initialize
    @attributes = {}
  end
  
  # Create dynamic getters and setters
  [:name, :email, :age, :address].each do |attr|
    define_method("#{attr}=") do |value|
      @attributes[attr] = value
    end
    
    define_method(attr) do
      @attributes[attr]
    end
  end
end

obj = DynamicAttributes.new
obj.name = "Alice"
obj.email = "alice@example.com"
obj.age = 30

puts "Name: #{obj.name}"
puts "Email: #{obj.email}"
puts "Age: #{obj.age}"

# ----- Complex example: Creating query methods dynamically -----
puts "\n--- Creating dynamic query methods ---"

class User
  attr_accessor :name, :email, :role, :active
  
  def initialize(attributes = {})
    attributes.each do |key, value|
      instance_variable_set("@#{key}", value) if respond_to?(key.to_sym)
    end
  end
  
  # Dynamically create predicate methods
  [:admin?, :active?, :inactive?, :guest?].each do |method_name|
    define_method(method_name) do
      case method_name
      when :admin?
        @role == :admin
      when :active?
        @active == true
      when :inactive?
        @active == false
      when :guest?
        @role == :guest
      end
    end
  end
  
  # Dynamic finder pattern
  class << self
    def find_by(attribute, value)
      # In real app, this would query a database
      puts "Finding user by #{attribute} = #{value}"
      # Simulate finding
      new(attribute => value, role: :user, active: true)
    end
    
    # Create dynamic finders (find_by_name, find_by_email, etc.)
    [:name, :email, :role].each do |attr|
      define_method("find_by_#{attr}") do |value|
        find_by(attr, value)
      end
    end
  end
end

user = User.find_by_name("Bob")
puts "User: #{user.inspect}"

admin = User.new(name: "Charlie", role: :admin, active: true)
puts "Admin? #{admin.admin?}"
puts "Active? #{admin.active?}"

# ----- define_method with closures -----
puts "\n--- define_method capturing closures ---"

def create_accessor(attribute)
  define_method(attribute) do
    instance_variable_get("@#{attribute}")
  end
  
  define_method("#{attribute}=") do |value|
    instance_variable_set("@#{attribute}", value)
  end
end

class Product
  create_accessor :name
  create_accessor :price
  create_accessor :sku
  
  def initialize(name, price, sku)
    @name = name
    @price = price
    @sku = sku
  end
end

product = Product.new("Laptop", 999.99, "LAP-001")
puts "Product: #{product.name}, Price: $#{product.price}, SKU: #{product.sku}"

# ============================================
# 2. METHOD_MISSING - CATCHING UNDEFINED METHODS
# ============================================
puts "\n" + "=" * 60
puts "2. METHOD_MISSING - THE GHOST METHOD PATTERN"
puts "=" * 60

puts <<~METHOD_MISSING_CONCEPT

  METHOD_MISSING:
  • Hook method called when an undefined method is invoked
  • Receives method name, arguments, and block
  • Powerful for creating dynamic proxies and DSLs
  • Must be used with respond_to_missing? for proper reflection
  • Can be dangerous if overused (performance, debugging difficulty)

METHOD_MISSING_CONCEPT

# ----- Basic method_missing example -----
puts "\n--- Basic method_missing ---"

class DynamicProxy
  def method_missing(method_name, *args, &block)
    puts "Method '#{method_name}' called with args: #{args}"
    puts "Block given: #{block_given?}"
    
    # Return a dynamic response
    "You called #{method_name} with #{args.join(', ')}"
  end
  
  def respond_to_missing?(method_name, include_private = false)
    # Claim to respond to any method
    true
  end
end

proxy = DynamicProxy.new
puts proxy.hello("world")
puts proxy.calculate(10, 20, 30)
puts proxy.do_something { puts "Block!" }

# ----- Ghost methods: Building a flexible API -----
puts "\n--- Ghost methods for flexible API ---"

class FlexiblePerson
  def initialize
    @attributes = {}
  end
  
  def method_missing(method_name, *args, &block)
    attr_name = method_name.to_s
    
    # Handle setters (methods ending with =)
    if attr_name.end_with?('=')
      @attributes[attr_name.chop.to_sym] = args.first
    # Handle getters
    elsif @attributes.key?(method_name)
      @attributes[method_name]
    else
      super
    end
  end
  
  def respond_to_missing?(method_name, include_private = false)
    attr_name = method_name.to_s
    @attributes.key?(method_name) || attr_name.end_with?('=') || super
  end
end

person = FlexiblePerson.new
person.name = "Alice"
person.age = 30
person.city = "New York"

puts "Name: #{person.name}"
puts "Age: #{person.age}"
puts "City: #{person.city}"

# ----- Building a DSL with method_missing -----
puts "\n--- Building a DSL with method_missing ---"

class QueryDSL
  def initialize
    @conditions = []
  end
  
  def method_missing(method_name, *args, &block)
    # Capture conditions like: where_name_eq("Alice")
    if method_name.to_s.start_with?('where_')
      condition = method_name.to_s.sub('where_', '')
      @conditions << { condition: condition, args: args }
      self
    else
      super
    end
  end
  
  def execute(collection)
    collection.select do |item|
      @conditions.all? do |condition|
        evaluate_condition(item, condition)
      end
    end
  end
  
  private
  
  def evaluate_condition(item, condition)
    # Parse condition like "name_eq" -> compare name == value
    parts = condition[:condition].split('_')
    attr = parts[0].to_sym
    operator = parts[1]
    value = condition[:args].first
    
    case operator
    when 'eq'
      item.send(attr) == value
    when 'gt'
      item.send(attr) > value
    when 'lt'
      item.send(attr) < value
    when 'contains'
      item.send(attr).to_s.include?(value.to_s)
    else
      true
    end
  end
end

class UserRecord
  attr_accessor :name, :age, :city
  
  def initialize(name, age, city)
    @name = name
    @age = age
    @city = city
  end
end

users = [
  UserRecord.new("Alice", 30, "New York"),
  UserRecord.new("Bob", 25, "Boston"),
  UserRecord.new("Charlie", 35, "New York"),
  UserRecord.new("Diana", 28, "Chicago")
]

query = QueryDSL.new
  .where_name_eq("Alice")
  .execute(users)

puts "Name equals Alice:"
query.each { |u| puts "  #{u.name}" }

query = QueryDSL.new
  .where_age_gt(28)
  .where_city_eq("New York")
  .execute(users)

puts "\nAge > 28 and City = New York:"
query.each { |u| puts "  #{u.name} (#{u.age})" }

# ----- method_missing for delegation -----
puts "\n--- Delegation with method_missing ---"

class ArrayWrapper
  def initialize(array)
    @array = array
  end
  
  def method_missing(method_name, *args, &block)
    if @array.respond_to?(method_name)
      @array.send(method_name, *args, &block)
    else
      super
    end
  end
  
  def respond_to_missing?(method_name, include_private = false)
    @array.respond_to?(method_name) || super
  end
end

wrapper = ArrayWrapper.new([1, 2, 3, 4, 5])
puts "Length: #{wrapper.length}"
puts "First: #{wrapper.first}"
puts "Map: #{wrapper.map { |x| x * 2 }}"
puts "Include? 3: #{wrapper.include?(3)}"

# ----- method_missing performance considerations -----
puts "\n--- Responding to method_missing properly ---"

class ProperProxy
  def initialize(target)
    @target = target
  end
  
  def method_missing(method_name, *args, &block)
    if @target.respond_to?(method_name)
      @target.send(method_name, *args, &block)
    else
      super
    end
  end
  
  def respond_to_missing?(method_name, include_private = false)
    @target.respond_to?(method_name) || super
  end
  
  # Define methods that should not go through method_missing for performance
  def inspect
    @target.inspect
  end
end

proxy = ProperProxy.new("Hello World")
puts "Upcase: #{proxy.upcase}"
puts "Downcase: #{proxy.downcase}"
puts "Responds to upcase? #{proxy.respond_to?(:upcase)}"

# ============================================
# 3. REFLECTION - INTROSPECTING OBJECTS
# ============================================
puts "\n" + "=" * 60
puts "3. REFLECTION - SEND AND RESPOND_TO?"
puts "=" * 60

puts <<~REFLECTION_CONCEPT

  REFLECTION METHODS:
  
  SEND:
  • Dynamically call methods by name
  • Can call private methods (use with caution)
  • Useful for metaprogramming and callbacks
  
  RESPOND_TO?:
  • Check if an object responds to a method
  • Works with method_missing if respond_to_missing? is implemented
  • Essential for duck typing and safe method invocation
  
  PUBLIC_SEND:
  • Like send but only calls public methods
  • Safer alternative to send

REFLECTION_CONCEPT

# ----- Using send for dynamic dispatch -----
puts "\n--- Dynamic method dispatch with send ---"

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
    a / b if b != 0
  end
  
  private
  
  def secret_calculation(a, b)
    a ** b
  end
end

calc = Calculator.new

# Dynamically choose which method to call
operations = [:add, :subtract, :multiply, :divide]
operations.each do |op|
  result = calc.send(op, 10, 5)
  puts "#{op}: #{result}"
end

# send can call private methods (use with caution!)
private_result = calc.send(:secret_calculation, 2, 3)
puts "Private method via send: #{private_result}"

# Use public_send for safety
begin
  result = calc.public_send(:secret_calculation, 2, 3)
rescue NoMethodError => e
  puts "public_send can't call private methods: #{e.message}"
end

# ----- Building a command pattern with send -----
puts "\n--- Command pattern with send ---"

class CommandProcessor
  def initialize
    @commands = {}
  end
  
  def register_command(name, &block)
    @commands[name] = block
  end
  
  def execute(command, *args)
    if @commands.key?(command)
      @commands[command].call(*args)
    else
      puts "Unknown command: #{command}"
    end
  end
end

processor = CommandProcessor.new
processor.register_command(:greet) { |name| puts "Hello, #{name}!" }
processor.register_command(:calculate) { |a, b, op| a.send(op, b) }
processor.register_command(:status) { puts "System status: OK" }

processor.execute(:greet, "Alice")
processor.execute(:calculate, 10, 5, :*)
processor.execute(:status)

# ----- respond_to? for safe method invocation -----
puts "\n--- Safe method invocation with respond_to? ---"

def safe_invoke(obj, method_name, *args)
  if obj.respond_to?(method_name)
    obj.send(method_name, *args)
  else
    puts "Object #{obj.class} does not respond to #{method_name}"
    nil
  end
end

[1, "hello", [1, 2, 3], { a: 1 }].each do |obj|
  result = safe_invoke(obj, :upcase)
  puts "#{obj.class}: #{result}"
end

# ----- respond_to? with method_missing -----
puts "\n--- respond_to? with method_missing ---"

class FlexibleHash
  def initialize
    @data = {}
  end
  
  def method_missing(method_name, *args)
    attr = method_name.to_s
    
    if attr.end_with?('=')
      @data[attr.chop.to_sym] = args.first
    elsif @data.key?(method_name)
      @data[method_name]
    else
      super
    end
  end
  
  def respond_to_missing?(method_name, include_private = false)
    attr = method_name.to_s
    @data.key?(method_name) || attr.end_with?('=') || super
  end
end

flex = FlexibleHash.new
flex.name = "Dynamic"
flex.age = 25

puts "respond_to? :name: #{flex.respond_to?(:name)}"
puts "respond_to? :age: #{flex.respond_to?(:age)}"
puts "respond_to? :city: #{flex.respond_to?(:city)}"

# ----- Using send with method names from external sources -----
puts "\n--- Dynamic method invocation from data ---"

class Shape
  def area(shape_type, *dimensions)
    send("area_#{shape_type}", *dimensions)
  rescue NoMethodError
    puts "Unknown shape: #{shape_type}"
    nil
  end
  
  private
  
  def area_circle(radius)
    Math::PI * radius ** 2
  end
  
  def area_rectangle(width, height)
    width * height
  end
  
  def area_triangle(base, height)
    0.5 * base * height
  end
end

shape = Shape.new
puts "Circle area: #{shape.area(:circle, 5)}"
puts "Rectangle area: #{shape.area(:rectangle, 10, 20)}"
puts "Triangle area: #{shape.area(:triangle, 8, 6)}"

# ============================================
# 4. CLASS_EVAL VS INSTANCE_EVAL
# ============================================
puts "\n" + "=" * 60
puts "4. CLASS_EVAL VS INSTANCE_EVAL"
puts "=" * 60

puts <<~EVAL_CONCEPT

  CLASS_EVAL:
  • Evaluates code in the context of a class (self = class)
  • Defines class methods and class variables
  • Can open class context from any scope
  
  INSTANCE_EVAL:
  • Evaluates code in the context of an instance (self = instance)
  • Defines singleton methods on the instance
  • Can access instance variables directly
  
  KEY DIFFERENCE: self context and what methods get defined

EVAL_CONCEPT

# ----- Basic class_eval vs instance_eval -----
puts "\n--- Basic comparison ---"

class EvalDemo
  def initialize
    @value = 42
  end
end

# class_eval: self is the class
EvalDemo.class_eval do
  # This defines a class method
  def self.class_method
    "Class method from class_eval"
  end
  
  # This defines an instance method
  def instance_method
    "Instance method from class_eval"
  end
end

# instance_eval: self is the instance
demo = EvalDemo.new
demo.instance_eval do
  # This defines a singleton method on this instance
  def singleton_method
    "Singleton method from instance_eval"
  end
  
  # Can access instance variables directly
  puts "Accessing instance variable: @value = #{@value}"
end

puts EvalDemo.class_method
puts demo.instance_method
puts demo.singleton_method

# ----- class_eval for adding methods to classes -----
puts "\n--- Using class_eval to add methods dynamically ---"

class Product
  attr_accessor :name, :price
  
  def initialize(name, price)
    @name = name
    @price = price
  end
end

# Add methods to all instances using class_eval
Product.class_eval do
  def with_tax(tax_rate = 0.1)
    price * (1 + tax_rate)
  end
  
  def discount(percentage)
    price * (1 - percentage / 100.0)
  end
  
  # Add class method
  def self.find(id)
    puts "Finding product with ID: #{id}"
    # Simulate database lookup
    new("Found Product", 99.99)
  end
end

product = Product.new("Laptop", 1000)
puts "Price with tax: $#{product.with_tax}"
puts "20% discount: $#{product.discount(20)}"
found = Product.find(123)
puts "Found: #{found.name}"

# ----- instance_eval for object-specific behavior -----
puts "\n--- Using instance_eval for object customization ---"

class Server
  attr_reader :host, :port
  
  def initialize(host, port)
    @host = host
    @port = port
  end
end

# Create a server instance and customize it
server = Server.new("localhost", 3000)

# Add singleton methods to this specific server
server.instance_eval do
  def start
    puts "Starting server at #{@host}:#{@port}"
  end
  
  def stop
    puts "Stopping server"
  end
  
  # Add an attribute just for this instance
  @status = :stopped
  
  def status
    @status
  end
  
  def status=(value)
    @status = value
  end
end

server.start
server.status = :running
puts "Status: #{server.status}"

# Another server instance doesn't have these methods
server2 = Server.new("localhost", 3001)
begin
  server2.start
rescue NoMethodError => e
  puts "server2 doesn't have start method: #{e.message}"
end

# ----- class_eval for DSL creation -----
puts "\n--- Building DSL with class_eval ---"

class Model
  def self.attr_accessor(*attrs)
    attrs.each do |attr|
      # Use class_eval to define methods in the class context
      class_eval <<-RUBY, __FILE__, __LINE__ + 1
        def #{attr}
          @#{attr}
        end
        
        def #{attr}=(value)
          @#{attr} = value
        end
      RUBY
    end
  end
  
  def self.belongs_to(association)
    class_eval <<-RUBY, __FILE__, __LINE__ + 1
      def #{association}
        # Simulate association lookup
        puts "Fetching #{association}"
        nil
      end
    RUBY
  end
end

class User < Model
  attr_accessor :name, :email, :age
  belongs_to :company
end

user = User.new
user.name = "Alice"
user.email = "alice@example.com"
puts "User: #{user.name}, #{user.email}"
user.company

# ----- instance_eval for configuration DSL -----
puts "\n--- Configuration DSL with instance_eval ---"

class Configuration
  attr_reader :settings
  
  def initialize
    @settings = {}
  end
  
  def configure(&block)
    instance_eval(&block)
  end
  
  def set(key, value)
    @settings[key] = value
  end
  
  def database(params)
    @settings[:database] = params
  end
  
  def server(params)
    @settings[:server] = params
  end
end

config = Configuration.new
config.configure do
  set :app_name, "MyApp"
  set :environment, "production"
  set :debug, false
  
  database do
    { adapter: "postgresql", host: "localhost", port: 5432 }
  end
  
  server do
    { host: "0.0.0.0", port: 3000, workers: 4 }
  end
end

puts "Configuration:"
pp config.settings

# ----- Combining class_eval and instance_eval -----
puts "\n--- Combining both for powerful DSLs ---"

class Resource
  class << self
    def define_attributes(*attrs)
      # class_eval for instance methods
      class_eval do
        attrs.each do |attr|
          define_method(attr) do
            instance_variable_get("@#{attr}")
          end
          
          define_method("#{attr}=") do |value|
            instance_variable_set("@#{attr}", value)
          end
        end
      end
      
      # instance_eval for class-level tracking
      instance_eval do
        define_method(:attributes) { attrs }
      end
    end
  end
end

class Post < Resource
  define_attributes :title, :body, :author, :published_at
end

post = Post.new
post.title = "Metaprogramming in Ruby"
post.body = "This is a deep dive..."
puts "Post: #{post.title}"
puts "Post attributes: #{Post.attributes}"

# ============================================
# 5. OPEN CLASSES AND MONKEY PATCHING
# ============================================
puts "\n" + "=" * 60
puts "5. OPEN CLASSES AND MONKEY PATCHING"
puts "=" * 60

puts <<~MONKEY_PATCHING

  OPEN CLASSES:
  • Ruby classes can be reopened and modified at any time
  • Add, modify, or remove methods from existing classes
  • Powerful but dangerous if used carelessly
  
  MONKEY PATCHING:
  • Modifying core classes (String, Array, etc.)
  • Can lead to conflicts with other code
  • Should be used sparingly and with caution
  • Better to use refinements (Ruby 2.0+) for safe modifications
  
  RISKS:
  • Breaking existing code that depends on original behavior
  • Method name collisions with future Ruby versions
  • Difficult to debug and maintain
  • Incompatible with other gems

MONKEY_PATCHING

# ----- Basic open class example -----
puts "\n--- Reopening classes ---"

# Original class
class String
  def word_count
    split.size
  end
end

puts "Hello world Ruby".word_count

# Reopen to add more methods
class String
  def vowel_count
    downcase.count('aeiou')
  end
  
  def consonant_count
    downcase.count('bcdfghjklmnpqrstvwxyz')
  end
end

puts "Hello world Ruby".vowel_count
puts "Hello world Ruby".consonant_count

# ----- Dangerous monkey patching -----
puts "\n--- Dangerous monkey patching example ---"

# Before patching
puts "Original Array#sum behavior:"
puts [1, 2, 3].sum  # Works if Ruby 2.4+, otherwise NoMethodError

# Dangerous patch - changing core behavior
class Array
  alias_method :original_sum, :sum if method_defined?(:sum)
  
  def sum
    puts "WARNING: Using custom sum!"
    inject(0) { |total, n| total + n }
  end
end

puts "\nAfter patching:"
puts [1, 2, 3].sum  # Now uses custom method

# This can break other code that expects original behavior
# Restore original if needed
if method_defined?(:original_sum)
  class Array
    alias_method :sum, :original_sum
  end
  puts "\nRestored original sum: #{[1, 2, 3].sum}"
end

# ----- Safer alternative: Refinements -----
puts "\n--- Refinements - Safe alternative to monkey patching ---"

module StringExtensions
  refine String do
    def word_count
      split.size
    end
    
    def reverse_words
      split.reverse.join(' ')
    end
    
    def to_slug
      downcase.gsub(/\s+/, '-').gsub(/[^a-z0-9-]/, '')
    end
  end
end

# Without refinement
puts "\nWithout refinement:"
str = "Hello World Ruby"
begin
  puts str.word_count
rescue NoMethodError => e
  puts "word_count not available: #{e.message}"
end

# Using refinement
module MyApp
  using StringExtensions
  
  puts "\nWith refinement:"
  str = "Hello World Ruby"
  puts "Word count: #{str.word_count}"
  puts "Reverse words: #{str.reverse_words}"
  puts "Slug: #{str.to_slug}"
end

# Outside the module, refinement is not active
begin
  puts "Outside refinement: #{str.word_count}"
rescue NoMethodError => e
  puts "word_count not available: #{e.message}"
end

# ----- Real-world example: Safe extension pattern -----
puts "\n--- Safe extension pattern ---"

module SafeExtensions
  module String
    refine ::String do
      def blank?
        !self || empty? || strip.empty?
      end
      
      def present?
        !blank?
      end
    end
  end
  
  module Array
    refine ::Array do
      def blank?
        empty?
      end
      
      def present?
        !blank?
      end
    end
  end
  
  module NilClass
    refine ::NilClass do
      def blank?
        true
      end
      
      def present?
        false
      end
    end
  end
end

class FormValidator
  using SafeExtensions::String
  using SafeExtensions::Array
  using SafeExtensions::NilClass
  
  def initialize(data)
    @data = data
  end
  
  def valid?
    @data[:name].present? && @data[:tags].present?
  end
end

validator = FormValidator.new(name: "", tags: [])
puts "Valid? #{validator.valid?}"  # false

validator2 = FormValidator.new(name: "Ruby", tags: ["metaprogramming"])
puts "Valid? #{validator2.valid?}"  # true

# ----- The risks of monkey patching -----
puts "\n--- Risks demonstration ---"

# Example of conflicting monkey patches
module FirstPatch
  refine String do
    def to_json
      "FIRST: #{super}"
    end
  end
end

module SecondPatch
  refine String do
    def to_json
      "SECOND: #{super}"
    end
  end
end

class ConflictDemo
  using FirstPatch
  
  def test1
    "test".to_json
  end
end

class ConflictDemo2
  using SecondPatch
  
  def test2
    "test".to_json
  end
end

puts "First patch: #{ConflictDemo.new.test1}"
puts "Second patch: #{ConflictDemo2.new.test2}"

# The issue: different parts of code may expect different behavior
puts "\nProblem: Different parts of code have different expectations!"
puts "This can lead to subtle bugs and maintenance nightmares."

# ============================================
# 6. ADVANCED METAPROGRAMMING PATTERNS
# ============================================
puts "\n" + "=" * 60
puts "6. ADVANCED METAPROGRAMMING PATTERNS"
puts "=" * 60

# ----- Dynamic method delegation -----
puts "\n--- Dynamic delegation pattern ---"

class Delegator
  def initialize(target)
    @target = target
  end
  
  def method_missing(method_name, *args, &block)
    if @target.respond_to?(method_name)
      puts "Delegating #{method_name} to #{@target.class}"
      @target.send(method_name, *args, &block)
    else
      super
    end
  end
  
  def respond_to_missing?(method_name, include_private = false)
    @target.respond_to?(method_name) || super
  end
end

array = [1, 2, 3, 4, 5]
delegator = Delegator.new(array)

puts delegator.size
puts delegator.first(3)
puts delegator.map { |x| x * 2 }

# ----- Creating proxy objects -----
puts "\n--- Proxy pattern with method_missing ---"

class LoggingProxy
  def initialize(target)
    @target = target
  end
  
  def method_missing(method_name, *args, &block)
    if @target.respond_to?(method_name)
      puts "[LOG] Calling #{method_name} with args: #{args}"
      start_time = Time.now
      result = @target.send(method_name, *args, &block)
      elapsed = Time.now - start_time
      puts "[LOG] #{method_name} took #{'%.3f' % elapsed} seconds"
      result
    else
      super
    end
  end
  
  def respond_to_missing?(method_name, include_private = false)
    @target.respond_to?(method_name) || super
  end
end

class DatabaseQuery
  def slow_query
    sleep(0.5)
    "Query results"
  end
  
  def fast_query
    "Fast results"
  end
end

db = DatabaseQuery.new
proxy = LoggingProxy.new(db)

puts proxy.slow_query
puts proxy.fast_query

# ----- Attribute DSL with define_method -----
puts "\n--- Creating an attribute DSL ---"

module AttributeDSL
  def self.included(base)
    base.extend(ClassMethods)
  end
  
  module ClassMethods
    def attribute(name, options = {})
      # Store attribute metadata
      @attributes ||= {}
      @attributes[name] = options
      
      # Create getter
      define_method(name) do
        instance_variable_get("@#{name}")
      end
      
      # Create setter with validation
      define_method("#{name}=") do |value|
        if options[:type] && !value.is_a?(options[:type])
          raise TypeError, "#{name} must be a #{options[:type]}"
        end
        
        if options[:required] && value.nil?
          raise ArgumentError, "#{name} is required"
        end
        
        instance_variable_set("@#{name}", value)
      end
      
      # Create predicate for boolean attributes
      if options[:type] == TrueClass || options[:type] == FalseClass
        define_method("#{name}?") do
          instance_variable_get("@#{name}")
        end
      end
    end
    
    def attributes
      @attributes || {}
    end
  end
end

class UserProfile
  include AttributeDSL
  
  attribute :name, type: String, required: true
  attribute :age, type: Integer
  attribute :email, type: String, required: true
  attribute :active, type: TrueClass, default: true
  attribute :role, type: Symbol, default: :user
end

profile = UserProfile.new
profile.name = "Alice"
profile.email = "alice@example.com"
profile.age = 30
profile.active = true

puts "Name: #{profile.name}"
puts "Age: #{profile.age}"
puts "Active? #{profile.active?}"
puts "Role: #{profile.role}"

# ----- Method generation from data -----
puts "\n--- Generating methods from external data ---"

class DynamicAPI
  def self.load_apis(apis)
    apis.each do |api_name, endpoints|
      define_method(api_name) do
        puts "Calling #{api_name} API..."
        endpoints.each do |endpoint|
          puts "  - #{endpoint}"
        end
        { status: :ok, data: endpoints }
      end
    end
  end
end

api_config = {
  user_api: ["/users", "/users/:id", "/users/create"],
  product_api: ["/products", "/products/:id", "/products/search"],
  order_api: ["/orders", "/orders/:id", "/orders/status"]
}

DynamicAPI.load_apis(api_config)
api = DynamicAPI.new
api.user_api
api.product_api
api.order_api

# ============================================
# 7. BEST PRACTICES AND WARNINGS
# ============================================
puts "\n" + "=" * 60
puts "7. BEST PRACTICES AND WARNINGS"
puts "=" * 60

puts <<~BEST_PRACTICES

  METAPROGRAMMING BEST PRACTICES:
  
  ✅ DO:
  • Use define_method for creating multiple similar methods
  • Implement respond_to_missing? when using method_missing
  • Use refinements instead of monkey patching core classes
  • Document metaprogramming code thoroughly
  • Test metaprogramming code extensively
  • Use class_eval/instance_eval for DSLs
  • Prefer public_send over send for safety
  
  ❌ DON'T:
  • Don't monkey patch core classes globally
  • Don't overuse method_missing (performance hit)
  • Don't use send with user input without whitelisting
  • Don't create methods that obscure code readability
  • Don't use metaprogramming when simple inheritance suffices
  • Don't forget that metaprogramming can make debugging harder
  
  ⚠️  WARNINGS:
  • Metaprogramming can slow down method lookup
  • Debugging dynamic methods is harder than static ones
  • IDE support for dynamic methods is limited
  • Future Ruby versions may change behavior
  • Team members may not understand metaprogramming code

BEST_PRACTICES

# ----- Safe method delegation pattern -----
puts "\n--- Safe delegation with whitelist ---"

class SafeDelegator
  ALLOWED_METHODS = [:name, :age, :email, :to_s, :inspect]
  
  def initialize(target)
    @target = target
  end
  
  def method_missing(method_name, *args, &block)
    if ALLOWED_METHODS.include?(method_name) && @target.respond_to?(method_name)
      @target.send(method_name, *args, &block)
    else
      super
    end
  end
  
  def respond_to_missing?(method_name, include_private = false)
    ALLOWED_METHODS.include?(method_name) && @target.respond_to?(method_name)
  end
end

class SensitiveUser
  attr_reader :name, :age, :email, :password, :credit_card
  
  def initialize
    @name = "Alice"
    @age = 30
    @email = "alice@example.com"
    @password = "secret123"
    @credit_card = "4111-1111-1111-1111"
  end
end

user = SensitiveUser.new
delegator = SafeDelegator.new(user)

puts "Name: #{delegator.name}"
puts "Age: #{delegator.age}"

begin
  puts "Password: #{delegator.password}"
rescue NoMethodError => e
  puts "Cannot access password: #{e.message}"
end

# ============================================
# 8. SUMMARY CHEAT SHEET
# ============================================
puts "\n" + "=" * 60
puts "8. QUICK REFERENCE CHEAT SHEET"
puts "=" * 60

puts <<~CHEAT_SHEET

  METAPROGRAMMING METHODS SUMMARY:
  
  ┌─────────────────────┬────────────────────────────────────────────────┐
  │ Method              │ Purpose                                        │
  ├─────────────────────┼────────────────────────────────────────────────┤
  │ define_method       │ Create instance methods dynamically           │
  │ method_missing      │ Handle undefined method calls                 │
  │ send/public_send    │ Dynamically invoke methods                    │
  │ respond_to?         │ Check if object responds to method            │
  │ respond_to_missing? │ Make method_missing work with respond_to?     │
  │ class_eval          │ Evaluate in class context (self = class)      │
  │ instance_eval       │ Evaluate in instance context (self = instance)│
  │ instance_variable_* │ Access instance variables dynamically         │
  │ const_*             │ Work with constants dynamically               │
  │ class_variable_*    │ Work with class variables dynamically         │
  └─────────────────────┴────────────────────────────────────────────────┘
  
  COMMON PATTERNS:
  
  # Dynamic attribute access
  obj.send("\#{attr}=", value)
  obj.send(attr)
  
  # Safe method invocation
  obj.respond_to?(method) ? obj.send(method) : default_value
  
  # Creating multiple methods
  [:a, :b, :c].each do |method|
    define_method(method) { puts method }
  end
  
  # Delegation
  def method_missing(name, *args)
    target.send(name, *args) if target.respond_to?(name)
  end
  
  # DSL with instance_eval
  def configure(&block)
    instance_eval(&block)
  end
  
  # Safe monkey patching (refinements)
  module MyExtensions
    refine String do
      def new_method; end
    end
  end
  
  # Method generation from data
  data.each do |key, value|
    define_method(key) { value }
  end

CHEAT_SHEET

puts "\n" + "=" * 60
puts "END OF METAPROGRAMMING DEEP DIVE"
puts "=" * 60