# ============================================
# RUBY STANDARD LIBRARY BASICS DEMONSTRATION
# ============================================

# First, let's require the necessary libraries
require 'json'        # For JSON parsing and generation
require 'date'        # For advanced date handling
require 'time'        # For time parsing and formatting
require 'fileutils'   # For file operations (optional, but useful)

# ============================================
# 1. FILE I/O (READING AND WRITING FILES)
# ============================================
puts "=" * 60
puts "1. FILE I/O OPERATIONS"
puts "=" * 60

# ----- WRITING TO FILES -----
# Method 1: Using File.open with a block (automatically closes the file)
puts "\n--- Writing to files ---"

# Writing a simple text file
File.open("sample.txt", "w") do |file|
  # "w" mode: write (overwrites if file exists)
  file.puts "Hello, Ruby File I/O!"
  file.puts "This is line 2"
  file.write "This line has no newline"
  file.write " - continuing on same line\n"
  file.print "Using print method\n"
end
puts "✅ Created sample.txt with content"

# Writing with different modes
File.open("log.txt", "a") do |file|
  # "a" mode: append (adds to end of file)
  file.puts "[#{Time.now}] Application started"
  file.puts "[#{Time.now}] User logged in"
end
puts "✅ Appended to log.txt"

# Writing binary data
File.open("data.bin", "wb") do |file|
  # "wb" mode: binary write
  file.write([65, 66, 67, 68].pack('C*'))  # Writes A, B, C, D as bytes
end
puts "✅ Created binary file"

# ----- READING FROM FILES -----
puts "\n--- Reading from files ---"

# Method 1: Read entire file into a string
content = File.read("sample.txt")
puts "Full file content (read method):"
puts content

# Method 2: Read lines into an array
lines = File.readlines("sample.txt")
puts "\nLines array:"
lines.each_with_index do |line, index|
  puts "  Line #{index + 1}: #{line.chomp}"  # chomp removes newline
end

# Method 3: Read line by line using File.open with block
puts "\nReading line by line:"
File.open("sample.txt", "r") do |file|
  # "r" mode: read (default)
  while line = file.gets
    print "  > #{line}"
  end
end

# Method 4: Read with each_line iterator
puts "\nUsing each_line:"
File.foreach("sample.txt") do |line|
  print "  >> #{line}"
end

# ----- FILE INFORMATION AND OPERATIONS -----
puts "\n--- File information ---"

# Check if file exists
if File.exist?("sample.txt")
  puts "✅ sample.txt exists"
  puts "  Size: #{File.size("sample.txt")} bytes"
  puts "  Directory? #{File.directory?("sample.txt")}"
  puts "  File? #{File.file?("sample.txt")}"
  puts "  Readable? #{File.readable?("sample.txt")}"
  puts "  Writable? #{File.writable?("sample.txt")}"
  puts "  Modified: #{File.mtime("sample.txt")}"
end

# File operations
File.rename("sample.txt", "renamed_sample.txt") if File.exist?("sample.txt")
puts "✅ Renamed sample.txt to renamed_sample.txt"

# Copy file (using FileUtils module)
FileUtils.cp("renamed_sample.txt", "copy_of_sample.txt")
puts "✅ Created copy_of_sample.txt"

# Delete file (commented out to keep files for later examples)
# File.delete("copy_of_sample.txt")
# puts "✅ Deleted copy_of_sample.txt"

# ============================================
# 2. WORKING WITH JSON
# ============================================
puts "\n" + "=" * 60
puts "2. JSON OPERATIONS"
puts "=" * 60

# ----- Ruby Hash to JSON -----
puts "\n--- Ruby to JSON conversion ---"

# Create a complex Ruby data structure
user_data = {
  id: 12345,
  name: "John Doe",
  email: "john@example.com",
  age: 30,
  is_active: true,
  hobbies: ["reading", "cycling", "photography"],
  address: {
    street: "123 Main St",
    city: "New York",
    zip_code: "10001",
    coordinates: {
      lat: 40.7128,
      lng: -74.0060
    }
  },
  created_at: Time.now.to_s
}

# Convert Ruby object to JSON string
json_string = JSON.generate(user_data)
puts "Ruby to JSON:"
puts json_string

# Pretty print JSON (human readable)
pretty_json = JSON.pretty_generate(user_data)
puts "\nPretty printed JSON:"
puts pretty_json

# Write JSON to file
File.open("user_data.json", "w") do |file|
  file.write(JSON.pretty_generate(user_data))
end
puts "\n✅ Saved user_data.json"

# ----- JSON to Ruby -----
puts "\n--- JSON to Ruby conversion ---"

# Read JSON from file
json_content = File.read("user_data.json")
parsed_data = JSON.parse(json_content)

puts "Parsed JSON to Ruby:"
puts "  Name: #{parsed_data['name']}"
puts "  Email: #{parsed_data['email']}"
puts "  First hobby: #{parsed_data['hobbies'][0]}"
puts "  City: #{parsed_data['address']['city']}"

# Symbolize keys (convert string keys to symbols)
symbolized_data = JSON.parse(json_content, symbolize_names: true)
puts "\nWith symbolized keys:"
puts "  Name: #{symbolized_data[:name]}"
puts "  City: #{symbolized_data[:address][:city]}"

# Handling JSON errors
puts "\n--- Error handling ---"
invalid_json = "{name: 'John', age: 30}"  # Invalid JSON (keys must be quoted)
begin
  JSON.parse(invalid_json)
rescue JSON::ParserError => e
  puts "❌ JSON parsing error: #{e.message}"
end

# ============================================
# 3. TIME AND DATE HANDLING
# ============================================
puts "\n" + "=" * 60
puts "3. TIME AND DATE HANDLING"
puts "=" * 60

# ----- Time Class (dates and times with timezone) -----
puts "\n--- Time class ---"

# Current time
now = Time.now
puts "Current time: #{now}"
puts "  Year: #{now.year}"
puts "  Month: #{now.month}"
puts "  Day: #{now.day}"
puts "  Hour: #{now.hour}"
puts "  Minute: #{now.min}"
puts "  Second: #{now.sec}"
puts "  Day of week: #{now.wday} (0=Sunday)"
puts "  Day of year: #{now.yday}"
puts "  Timezone: #{now.zone}"
puts "  UTC offset: #{now.utc_offset / 3600} hours"
puts "  Unix timestamp: #{now.to_i}"

# Creating specific times
specific_time = Time.new(2024, 12, 25, 10, 30, 45)
puts "\nChristmas 2024 at 10:30:45: #{specific_time}"

# UTC time
utc_time = Time.utc(2024, 12, 25, 10, 30, 45)
puts "UTC time: #{utc_time}"

# Parsing time strings
parsed_time = Time.parse("2024-12-25 10:30:45")
puts "Parsed time: #{parsed_time}"

# Time calculations
puts "\n--- Time calculations ---"
future = now + (7 * 24 * 60 * 60)  # Add 7 days
puts "One week from now: #{future}"

past = now - (30 * 24 * 60 * 60)   # Subtract 30 days
puts "30 days ago: #{past}"

# Time differences
diff = future - now
puts "Days difference: #{(diff / (24 * 60 * 60)).to_i} days"

# Formatting times
puts "\n--- Time formatting ---"
puts "Default: #{now}"
puts "ISO 8601: #{now.iso8601}"
puts "RFC 2822: #{now.rfc2822}"
puts "Custom format: #{now.strftime("%B %d, %Y at %I:%M %p")}"
puts "  %Y-%m-%d: #{now.strftime("%Y-%m-%d")}"
puts "  %H:%M:%S: #{now.strftime("%H:%M:%S")}"
puts "  %A, %B %d: #{now.strftime("%A, %B %d")}"

# ----- Date Class (dates only) -----
puts "\n--- Date class ---"

# Current date
today = Date.today
puts "Today: #{today}"
puts "  Year: #{today.year}"
puts "  Month: #{today.month}"
puts "  Day: #{today.day}"

# Creating dates
specific_date = Date.new(2024, 12, 25)
puts "Christmas 2024: #{specific_date}"

# Parsing dates
parsed_date = Date.parse("2024-12-25")
puts "Parsed date: #{parsed_date}"

# Date calculations
puts "\n--- Date calculations ---"
puts "Day of week: #{specific_date.strftime("%A")}"
puts "Leap year? #{specific_date.leap?}"
puts "Next month: #{specific_date.next_month}"
puts "Previous month: #{specific_date.prev_month}"
puts "Days in month: #{specific_date.next_month.prev_day.day}"

# Date ranges
puts "\n--- Date ranges ---"
date_range = (Date.today..Date.today + 7)
puts "Next 7 days:"
date_range.each do |date|
  puts "  #{date.strftime("%A, %B %d")}"
end

# ----- DateTime Class (combines Date and Time) -----
puts "\n--- DateTime class ---"

# Create DateTime
dt = DateTime.now
puts "Current DateTime: #{dt}"
puts "  ISO 8601: #{dt.iso8601}"
puts "  RFC 3339: #{dt.rfc3339}"

# ============================================
# 4. BUILT-IN MODULES
# ============================================
puts "\n" + "=" * 60
puts "4. BUILT-IN MODULES"
puts "=" * 60

# ----- Enumerable Module -----
puts "\n--- Enumerable module ---"
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

puts "Numbers: #{numbers}"
puts "Even numbers: #{numbers.select { |n| n.even? }}"
puts "Odd numbers: #{numbers.reject { |n| n.even? }}"
puts "Sum: #{numbers.reduce(:+)}"
puts "Product: #{numbers.inject(:*)}"
puts "Doubled: #{numbers.map { |n| n * 2 }}"
puts "Any > 5? #{numbers.any? { |n| n > 5 }}"
puts "All > 0? #{numbers.all? { |n| n > 0 }}"
puts "First 3: #{numbers.take(3)}"
puts "Group by even/odd: #{numbers.group_by { |n| n.even? ? 'even' : 'odd' }}"

# ----- Comparable Module -----
puts "\n--- Comparable module ---"

class Person
  include Comparable
  
  attr_reader :name, :age
  
  def initialize(name, age)
    @name = name
    @age = age
  end
  
  # Define the comparison method for Comparable
  def <=>(other)
    @age <=> other.age
  end
  
  def to_s
    "#{@name} (#{@age})"
  end
end

people = [
  Person.new("Alice", 30),
  Person.new("Bob", 25),
  Person.new("Charlie", 35)
]

puts "People: #{people.join(', ')}"
puts "Sorted by age: #{people.sort.join(', ')}"
puts "Oldest: #{people.max}"
puts "Youngest: #{people.min}"
puts "Is Alice older than Bob? #{people[0] > people[1]}"
puts "Is Charlie between Bob and Alice? #{people[2].between?(people[1], people[0])}"

# ----- Kernel Module -----
puts "\n--- Kernel module (always available) ---"

# puts, print, p (debugging)
puts "Using puts (with newline)"
print "Using print "
print "(no newline)\n"
p "Using p (inspect)"  # Shows object representation

# Type checking
puts "\nType checking:"
puts "  42 is Integer? #{42.is_a?(Integer)}"
puts "  3.14 is Float? #{3.14.is_a?(Float)}"
puts "  'hello' is String? {'hello'}.is_a?(String)}"

# Looping
puts "\nLooping:"
3.times { |i| print "#{i} " }
puts
(1..5).each { |i| print "#{i} " }
puts

# Sleeping (pausing execution)
puts "\nSleeping for 1 second..."
sleep(1)
puts "Woke up!"

# ----- Math Module -----
puts "\n--- Math module ---"
puts "PI: #{Math::PI}"
puts "E: #{Math::E}"
puts "Square root of 16: #{Math.sqrt(16)}"
puts "Sin(90°): #{Math.sin(Math::PI / 2)}"
puts "Log10(100): #{Math.log10(100)}"
puts "2^8: #{2 ** 8}"

# ----- FileUtils Module -----
puts "\n--- FileUtils module ---"

# Create directory
FileUtils.mkdir_p("test_directory/subdirectory") unless Dir.exist?("test_directory")
puts "✅ Created test_directory/subdirectory"

# List directory contents
puts "Directory contents:"
Dir.entries(".").select { |f| File.file?(f) && f.end_with?('.txt', '.json') }.each do |file|
  puts "  - #{file}"
end

# Clean up (commented to keep files)
# FileUtils.rm_rf("test_directory")
# puts "✅ Removed test_directory"

# ============================================
# 5. PRACTICAL EXAMPLE: DATA PROCESSING PIPELINE
# ============================================
puts "\n" + "=" * 60
puts "5. PRACTICAL EXAMPLE: DATA PROCESSING PIPELINE"
puts "=" * 60

# Create sample data file
sample_data = [
  { name: "Product A", price: 29.99, in_stock: true, last_updated: Time.now.to_s },
  { name: "Product B", price: 49.99, in_stock: false, last_updated: Time.now.to_s },
  { name: "Product C", price: 19.99, in_stock: true, last_updated: Time.now.to_s }
]

# Write to JSON
File.open("products.json", "w") do |file|
  file.write(JSON.pretty_generate(sample_data))
end
puts "✅ Created products.json"

# Read, process, and write back
puts "\nProcessing products data:"

File.open("products.json", "r") do |file|
  data = JSON.parse(file.read, symbolize_names: true)
  
  # Process data
  processed_data = data.map do |product|
    product[:price_with_tax] = (product[:price] * 1.1).round(2)
    product[:status] = product[:in_stock] ? "Available" : "Out of Stock"
    product[:processed_at] = Time.now.strftime("%Y-%m-%d %H:%M:%S")
    product
  end
  
  # Write processed data
  File.open("processed_products.json", "w") do |outfile|
    outfile.write(JSON.pretty_generate(processed_data))
  end
  
  puts "  Processed #{processed_data.size} products"
  puts "  Output saved to processed_products.json"
end

# Log the operation
File.open("processing.log", "a") do |log|
  log.puts "[#{Time.now.iso8601}] Processed products data - #{sample_data.size} records"
end
puts "✅ Logged operation to processing.log"

# Display summary
puts "\n--- Processing Summary ---"
puts "Generated files:"
puts "  - products.json (original data)"
puts "  - processed_products.json (processed data)"
puts "  - processing.log (operation log)"
puts "  - user_data.json (user data)"
puts "  - log.txt (application log)"

puts "\n" + "=" * 60
puts "END OF RUBY STANDARD LIBRARY DEMONSTRATION"
puts "=" * 60