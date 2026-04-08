# ============================================
# DEMONSTRATION OF RUBY OOP CONCEPTS
# ============================================

# 1. CLASS DEFINITION AND ENCAPSULATION
# --------------------------------------
class Vehicle
  # CLASS VARIABLE - shared across all instances and subclasses
  @@total_vehicles = 0
  @@vehicle_types = {}
  
  # ATTRIBUTES with different access levels (encapsulation)
  # attr_reader: creates a getter method (read-only)
  attr_reader :id, :fuel_level
  
  # attr_writer: creates a setter method (write-only)
  attr_writer :nickname
  
  # attr_accessor: creates both getter and setter methods
  attr_accessor :model, :year
  
  # CLASS METHODS - called on the class itself, not instances
  # Using 'self.' prefix defines a class method
  def self.total_vehicles
    @@total_vehicles
  end
  
  def self.vehicle_types
    @@vehicle_types
  end
  
  # Class method to track vehicles by type
  def self.add_vehicle_type(type)
    @@vehicle_types[type] = (@@vehicle_types[type] || 0) + 1
  end
  
  # CONSTRUCTOR (initialize method)
  # Called automatically when new object is created
  def initialize(model, year)
    @model = model      # instance variable
    @year = year        # instance variable
    @fuel_level = 100   # instance variable with default value
    @id = generate_id   # private method call
    
    # Track this vehicle
    @@total_vehicles += 1
    self.class.add_vehicle_type(self.class.to_s)
  end
  
  # INSTANCE METHOD
  # Can be called on individual objects
  def start_engine
    if @fuel_level > 0
      puts "🚗 #{get_vehicle_info}: Engine started!"
      consume_fuel(5)
      true
    else
      puts "⛔ #{get_vehicle_info}: Out of fuel!"
      false
    end
  end
  
  # INSTANCE METHOD with self (explicit receiver)
  def refuel(amount)
    # self here refers to the current instance
    self.fuel_level += amount if amount > 0
    puts "⛽ #{get_vehicle_info}: Fueled up to #{@fuel_level}%"
  end
  
  # ENCAPSULATION - protected method
  # Can be called only within the class or subclasses
  protected
  
  def consume_fuel(amount)
    @fuel_level -= amount if @fuel_level >= amount
    @fuel_level = 0 if @fuel_level < 0
  end
  
  # ENCAPSULATION - private method
  # Cannot be called with an explicit receiver
  private
  
  def generate_id
    "#{self.class.name[0]}-#{rand(1000..9999)}"
  end
  
  def get_vehicle_info
    "#{@year} #{@model} (ID: #{@id})"
  end
  
  # Custom setter method with validation
  def fuel_level=(value)
    @fuel_level = [value, 0, 100].sort[1]  # Clamp between 0 and 100
  end
end

# 2. INHERITANCE
# ----------------
class Car < Vehicle
  # Class variable specific to Car
  @@total_cars = 0
  
  attr_accessor :number_of_doors, :car_type
  
  def self.total_cars
    @@total_cars
  end
  
  def initialize(model, year, number_of_doors = 4, car_type = "sedan")
    # super calls the parent class initialize method
    super(model, year)
    @number_of_doors = number_of_doors
    @car_type = car_type
    @@total_cars += 1
  end
  
  # METHOD OVERRIDING
  def start_engine
    puts "🔑 Turning key in ignition..."
    # Call parent method using 'super'
    super
    puts "🎵 Playing engine sound: Vroom vroom!"
  end
  
  # Additional instance method
  def honk
    puts "📢 #{get_vehicle_info}: Beep beep!"
  end
  
  # Demonstrating self in different context
  def self.car_statistics
    # self here refers to the Car class
    puts "Total Cars: #{@@total_cars}"
    puts "Total Vehicles: #{self.total_vehicles}"
  end
end

class Motorcycle < Vehicle
  attr_accessor :has_sidecar
  
  def initialize(model, year, has_sidecar = false)
    super(model, year)
    @has_sidecar = has_sidecar
  end
  
  # METHOD OVERRIDING with different behavior
  def start_engine
    puts "🏍️ Kick-starting motorcycle..."
    super
    puts "🔊 Revving sound: Vroom!"
  end
  
  def wheelie
    puts "🎯 #{get_vehicle_info}: Doing a wheelie!" if @fuel_level > 10
    consume_fuel(10)
  end
  
  # Demonstrating self in instance method
  def display_info
    # self here refers to the current motorcycle instance
    puts "Motorcycle Info: #{self.model} (#{self.year})"
    puts "Sidecar: #{self.has_sidecar ? 'Yes' : 'No'}"
    puts "Fuel: #{self.fuel_level}%"
  end
  
  private
  
  def get_vehicle_info
    # Overriding private method for motorcycle-specific formatting
    "🏍️ #{super}"
  end
end

# 3. DEMONSTRATION AND USAGE
# ----------------------------
puts "=" * 50
puts "RUBY OOP DEMONSTRATION"
puts "=" * 50

# Creating objects (instances)
puts "\n1. CREATING OBJECTS:"
puts "-" * 30
car1 = Car.new("Toyota Camry", 2022, 4, "sedan")
car2 = Car.new("Honda Civic", 2023, 2, "coupe")
motorcycle = Motorcycle.new("Harley Davidson", 2021, false)

# Accessing attributes (using getters/setters)
puts "\n2. ACCESSING ATTRIBUTES:"
puts "-" * 30
puts "Car model: #{car1.model}"           # attr_accessor (getter)
puts "Car year: #{car1.year}"             # attr_accessor (getter)
puts "Car ID: #{car1.id}"                 # attr_reader (getter)
puts "Car fuel level: #{car1.fuel_level}" # attr_reader (getter)

# Using setters
car1.nickname = "My Baby"                 # attr_writer (setter)
car1.model = "Toyota Camry XLE"           # attr_accessor (setter)
puts "Updated model: #{car1.model}"

# Demonstrating encapsulation
puts "\n3. ENCAPSULATION:"
puts "-" * 30
puts "Can read fuel_level: #{car1.fuel_level}"
# puts car1.consume_fuel(10)  # ERROR: protected method, can't call directly
# puts car1.generate_id       # ERROR: private method, can't call directly
puts "✅ Private/protected methods cannot be accessed from outside"

# Calling instance methods
puts "\n4. INSTANCE METHODS:"
puts "-" * 30
car1.start_engine
motorcycle.start_engine
motorcycle.wheelie
car1.honk if car1.is_a?(Car)

# Demonstrating self in different contexts
puts "\n5. SELF IN DIFFERENT CONTEXTS:"
puts "-" * 30
puts "In instance method (display_info):"
motorcycle.display_info
puts "\nIn class method (car_statistics):"
Car.car_statistics

# Class methods
puts "\n6. CLASS METHODS:"
puts "-" * 30
puts "Total Vehicles: #{Vehicle.total_vehicles}"
puts "Total Cars: #{Car.total_cars}"
puts "Vehicle Types Count: #{Vehicle.vehicle_types}"

# Inheritance demonstration
puts "\n7. INHERITANCE HIERARCHY:"
puts "-" * 30
puts "Car is a Vehicle: #{car1.is_a?(Vehicle)}"
puts "Motorcycle is a Vehicle: #{motorcycle.is_a?(Vehicle)}"
puts "Vehicle is not a Car: #{Vehicle.is_a?(Car) ? 'Yes' : 'No'}"
puts "Car ancestors: #{Car.ancestors[0..2].join(' -> ')}"

# Polymorphism through inheritance
puts "\n8. POLYMORPHISM (same method, different behaviors):"
puts "-" * 30
[car1, car2, motorcycle].each do |vehicle|
  puts "\nStarting #{vehicle.class}:"
  vehicle.start_engine
end

# Additional OOP concept: duck typing
puts "\n9. DUCK TYPING DEMONSTRATION:"
puts "-" * 30
def test_vehicle(vehicle)
  # Ruby doesn't care about the class, just if it responds to methods
  if vehicle.respond_to?(:start_engine) && vehicle.respond_to?(:refuel)
    puts "✅ #{vehicle.class} can start and refuel"
    vehicle.refuel(20)
  end
end

test_vehicle(car1)
test_vehicle(motorcycle)

puts "\n" + "=" * 50
puts "END OF DEMONSTRATION"
puts "=" * 50