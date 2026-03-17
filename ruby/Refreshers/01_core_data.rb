# ============================================
# RUBY CORE DATA STRUCTURES - COMPREHENSIVE GUIDE
# ============================================

# ============================================
# 1. ARRAYS - ORDERED, INDEX-BASED COLLECTIONS
# ============================================

puts "\n" + "="*60
puts "ARRAYS - FOUNDATIONS"
puts "="*60

# CREATION - Different ways to create arrays

# Literal notation
empty_array = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, true, nil, [1, 2]]  # Can mix types
puts "Mixed array: #{mixed.inspect}"

# Using Array.new
zeros = Array.new(5, 0)           # => [0, 0, 0, 0, 0]
puts "Zeros: #{zeros.inspect}"

# With block for computed values
squares = Array.new(5) { |i| i * i }  # => [0, 1, 4, 9, 16]
puts "Squares: #{squares.inspect}"

# %w and %i shortcuts (word arrays and symbol arrays)
words = %w(apple banana cherry)           # => ["apple", "banana", "cherry"]
symbols = %i(red green blue)               # => [:red, :green, :blue]
puts "Words with %w: #{words.inspect}"
puts "Symbols with %i: #{symbols.inspect}"

# Using to_a (to array) on ranges
range_array = (1..5).to_a                  # => [1, 2, 3, 4, 5]
puts "Range to array: #{range_array.inspect}"

# ACCESSING ELEMENTS

puts "\n--- ACCESSING ARRAY ELEMENTS ---"
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

# By index (0-based)
puts fruits[0]          # => "apple"
puts fruits[2]          # => "cherry"
puts fruits[-1]         # => "elderberry" (last element)
puts fruits[-2]         # => "date" (second from last)

# Using fetch (raises error if out of bounds, vs nil with [])
puts fruits.fetch(1)    # => "banana"
# puts fruits.fetch(10) # Raises IndexError

# fetch with default
puts fruits.fetch(10, "default")  # => "default"

# Multiple elements
puts fruits[1..3].inspect          # => ["banana", "cherry", "date"]
puts fruits[1...3].inspect         # => ["banana", "cherry"] (excludes end)
puts fruits[1, 3].inspect          # => ["banana", "cherry", "date"] (start, length)

# First and last
puts fruits.first          # => "apple"
puts fruits.last           # => "elderberry"
puts fruits.first(2).inspect  # => ["apple", "banana"]
puts fruits.last(2).inspect   # => ["date", "elderberry"]

# values_at - get specific indices
puts fruits.values_at(0, 2, 4).inspect  # => ["apple", "cherry", "elderberry"]

# index and rindex - find position of element
puts fruits.index("cherry")          # => 2 (first occurrence)
puts fruits.index("not there")       # => nil
puts fruits.rindex("e")              # finds from end

# MANIPULATION - ADDING ELEMENTS

puts "\n--- ADDING TO ARRAYS ---"
arr = [1, 2, 3]

# Push to end (<< and push)
arr << 4                    # => [1, 2, 3, 4]
arr.push(5)                 # => [1, 2, 3, 4, 5]
arr.push(6, 7, 8)           # => [1, 2, 3, 4, 5, 6, 7, 8]
puts "After pushes: #{arr.inspect}"

# Insert at specific position
arr.insert(2, "inserted")   # Insert at index 2: [1, 2, "inserted", 3, 4, 5, 6, 7, 8]
puts "After insert: #{arr.inspect}"

# Unshift - add to beginning
arr.unshift(0)              # => [0, 1, 2, "inserted", 3, 4, 5, 6, 7, 8]
arr.unshift(-2, -1)         # => [-2, -1, 0, 1, 2, "inserted", 3, 4, 5, 6, 7, 8]
puts "After unshift: #{arr.inspect}"

# Concatenation
a = [1, 2, 3]
b = [4, 5, 6]
concat_result = a + b        # => [1, 2, 3, 4, 5, 6] (new array)
a.concat(b)                  # => [1, 2, 3, 4, 5, 6] (modifies a)
puts "After concat: #{a.inspect}"

# REMOVING ELEMENTS

puts "\n--- REMOVING FROM ARRAYS ---"
items = [1, 2, 3, 4, 5, 3, 6, 7]

# Pop - remove from end
last = items.pop            # => 7, items = [1, 2, 3, 4, 5, 3, 6]
puts "Popped: #{last}, items now: #{items.inspect}"

# Pop multiple
last_two = items.pop(2)     # => [3, 6], items = [1, 2, 3, 4, 5]
puts "Popped two: #{last_two.inspect}, items now: #{items.inspect}"

# Shift - remove from beginning
first = items.shift         # => 1, items = [2, 3, 4, 5]
puts "Shifted: #{first}, items now: #{items.inspect}"

# Shift multiple
first_two = items.shift(2)  # => [2, 3], items = [4, 5]
puts "Shifted two: #{first_two.inspect}, items now: #{items.inspect}"

# Delete by value (all occurrences)
nums = [1, 2, 3, 2, 4, 2, 5]
nums.delete(2)              # => 2, nums = [1, 3, 4, 5]
puts "After delete(2): #{nums.inspect}"

# Delete at specific index
nums = [1, 2, 3, 4, 5]
removed = nums.delete_at(2) # => 3, nums = [1, 2, 4, 5]
puts "After delete_at(2): #{nums.inspect}, removed: #{removed}"

# Delete if - with block
nums = [1, 2, 3, 4, 5, 6]
nums.delete_if { |n| n.even? }  # => [1, 3, 5]
puts "After delete_if even: #{nums.inspect}"

# Compact - remove nil values
with_nils = [1, nil, 2, nil, 3]
puts with_nils.compact.inspect     # => [1, 2, 3] (non-destructive)
puts with_nils.compact!.inspect    # Destructive version

# Uniq - remove duplicates
dupes = [1, 2, 2, 3, 3, 3, 4]
puts dupes.uniq.inspect            # => [1, 2, 3, 4]
puts dupes.uniq!.inspect           # Destructive

# Clear - remove all elements
temp = [1, 2, 3]
temp.clear                        # => []
puts "After clear: #{temp.inspect}"

# TRANSFORMING ARRAYS

puts "\n--- TRANSFORMING ARRAYS ---"
original = [1, 2, 3, 4, 5]

# Map/collect - transform each element
doubled = original.map { |n| n * 2 }
puts "Original: #{original.inspect}"
puts "Doubled: #{doubled.inspect}"

# Map with index
mapped_with_index = original.map.with_index { |n, i| "#{i}:#{n}" }
puts "With index: #{mapped_with_index.inspect}"

# Select/filter - keep elements matching condition
evens = original.select { |n| n.even? }
puts "Evens: #{evens.inspect}"

# Reject - opposite of select
odds = original.reject { |n| n.even? }
puts "Odds: #{odds.inspect}"

# Partition - split into two arrays
evens, odds = original.partition { |n| n.even? }
puts "Partition - evens: #{evens.inspect}, odds: #{odds.inspect}"

# Flatten - nested arrays to single level
nested = [1, [2, 3], [4, [5, 6]]]
puts "Flatten: #{nested.flatten.inspect}"
puts "Flatten level 1: #{nested.flatten(1).inspect}"  # Only one level

# Reverse
puts "Reverse: #{original.reverse.inspect}"

# Rotate
puts "Rotate: #{original.rotate.inspect}"     # => [2, 3, 4, 5, 1]
puts "Rotate 2: #{original.rotate(2).inspect}" # => [3, 4, 5, 1, 2]

# Shuffle (randomize)
puts "Shuffle: #{original.shuffle.inspect}"

# Sample (random element)
puts "Sample: #{original.sample}"
puts "Sample 3: #{original.sample(3).inspect}"

# Join - to string
letters = ["a", "b", "c"]
puts letters.join                     # => "abc"
puts letters.join("-")                # => "a-b-c"

# ITERATION

puts "\n--- ARRAY ITERATION ---"
colors = ["red", "green", "blue"]

# Each - basic iteration
colors.each do |color|
  puts "Color: #{color}"
end

# Each with index
colors.each_with_index do |color, index|
  puts "#{index}: #{color}"
end

# Reverse each
colors.reverse_each do |color|
  puts "Reverse: #{color}"
end

# Times with index
array = []
5.times { |i| array << i * 10 }
puts "Built with times: #{array.inspect}"

# SET OPERATIONS

puts "\n--- SET OPERATIONS WITH ARRAYS ---"
a = [1, 2, 3, 4, 5]
b = [3, 4, 5, 6, 7]

# Union (|) - combine, remove duplicates
union = a | b
puts "Union: #{union.inspect}"  # => [1, 2, 3, 4, 5, 6, 7]

# Intersection (&) - common elements
intersection = a & b
puts "Intersection: #{intersection.inspect}"  # => [3, 4, 5]

# Difference (-) - elements in a but not in b
difference = a - b
puts "Difference: #{difference.inspect}"  # => [1, 2]

# ARRAY COMPARISON

puts "\n--- ARRAY COMPARISON ---"
arr1 = [1, 2, 3]
arr2 = [1, 2, 3]
arr3 = [1, 2, 4]

puts arr1 == arr2   # => true (same content)
puts arr1 == arr3   # => false

puts arr1 <=> arr2  # => 0 (equal)
puts arr1 <=> arr3  # => -1 (arr1 less than arr3)
puts arr3 <=> arr1  # => 1 (arr3 greater than arr1)

# Check if array includes element
puts arr1.include?(2)   # => true
puts arr1.include?(5)   # => false

# ============================================
# 2. SYMBOLS VS STRINGS - KEY DIFFERENCES
# ============================================

puts "\n" + "="*60
puts "SYMBOLS VS STRINGS - DEEP DIVE"
puts "="*60

# CREATION
string1 = "hello"
string2 = "hello"
symbol1 = :hello
symbol2 = :hello

# OBJECT ID (identity) - Symbols with same name are THE SAME object
puts "\n--- OBJECT IDENTITY ---"
puts "String 1 object_id: #{string1.object_id}"
puts "String 2 object_id: #{string2.object_id}"
puts "Same string? #{string1.object_id == string2.object_id}"  # => false

puts "Symbol 1 object_id: #{symbol1.object_id}"
puts "Symbol 2 object_id: #{symbol2.object_id}"
puts "Same symbol? #{symbol1.object_id == symbol2.object_id}"   # => true!

# MEMORY AND PERFORMANCE
puts "\n--- MEMORY & PERFORMANCE ---"
require 'benchmark'

puts "Creating 1000 unique strings vs symbols:"
Benchmark.bm do |x|
  x.report("Strings:") { 1000.times { |i| "string_#{i}" } }
  x.report("Symbols:") { 1000.times { |i| :"symbol_#{i}" } }
end

# Symbols are immutable, strings are mutable
puts "\n--- IMMUTABILITY ---"
str = "hello"
sym = :hello

str << " world"  # Works - string modified
# sym << " world" # Error! Symbol can't be modified

puts "String after modification: #{str}"
puts "Symbol remains: #{sym}"

# CONVERSION
puts "\n--- CONVERSION BETWEEN TYPES ---"
str = "hello"
sym = :hello

# String to symbol
puts str.to_sym                # => :hello
puts str.intern                # => :hello (same as to_sym)

# Symbol to string
puts sym.to_s                  # => "hello"
puts sym.id2name               # => "hello"
puts sym.inspect               # => ":hello"

# String vs Symbol methods
puts "\n--- AVAILABLE METHODS ---"
puts "String methods count: #{'hello'.methods.count}"
puts "Symbol methods count: #{:hello.methods.count}"

# Common use cases for symbols
puts "\n--- SYMBOL USE CASES ---"

# 1. Hash keys (most common)
person = { name: "Alice", age: 30, city: "NYC" }
# This is syntactic sugar for { :name => "Alice", :age => 30, :city => "NYC" }

# 2. Method arguments/options
def process_data(data, format: :json, validate: true)
  puts "Processing as #{format} with validation: #{validate}"
end

process_data(some_data, format: :xml)  # Using symbols for options

# 3. Enum-like values
statuses = [:pending, :processing, :completed, :failed]
current = :pending

# 4. As identifiers
def send_notification(user, type: :email)
  puts "Sending #{type} to #{user}"
end

# SYMBOLS VS STRINGS IN HASHES
puts "\n--- SYMBOLS VS STRINGS IN HASHES ---"
hash_with_symbols = { name: "Alice", age: 30 }
hash_with_strings = { "name" => "Alice", "age" => 30 }

puts "Symbol hash access: #{hash_with_symbols[:name]}"      # => "Alice"
puts "Symbol hash with string: #{hash_with_symbols['name']}" # => nil!

puts "String hash access: #{hash_with_strings['name']}"      # => "Alice"
puts "String hash with symbol: #{hash_with_strings[:name]}"  # => nil!

# Converting hash keys
string_keys_hash = { "first_name" => "Bob", "last_name" => "Smith" }
symbol_keys_hash = string_keys_hash.transform_keys(&:to_sym)
puts "Converted to symbols: #{symbol_keys_hash.inspect}"

# ============================================
# 3. COMMON ENUMERABLE METHODS (BEYOND BASIC)
# ============================================

puts "\n" + "="*60
puts "ENUMERABLE METHODS - COMPREHENSIVE"
puts "="*60

# Enumerable is a module included by Array, Hash, Range, and more
collection = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# COUNTING AND STATISTICS
puts "\n--- COUNTING & STATISTICS ---"
puts "Count: #{collection.count}"
puts "Count of 5s: #{collection.count(5)}"
puts "Count of evens: #{collection.count { |n| n.even? }}"
puts "Size: #{collection.size}"           # Alias for count
puts "Length: #{collection.length}"        # Also same

puts "Sum: #{collection.sum}"
puts "Min: #{collection.min}"
puts "Max: #{collection.max}"
puts "Minmax: #{collection.minmax.inspect}"
puts "Average: #{collection.sum.to_f / collection.count}"

# GROUPING AND SORTING
puts "\n--- GROUPING & SORTING ---"

# Group by
grouped = collection.group_by { |n| n.even? ? "even" : "odd" }
puts "Grouped by parity: #{grouped.inspect}"
# => {"odd"=>[3, 1, 1, 5, 9, 5, 3, 5], "even"=>[4, 2, 6]}

# Tally (Ruby 2.7+) - count occurrences
tally = collection.tally
puts "Tally: #{tally.inspect}"  # => {3=>2, 1=>2, 4=>1, 5=>3, 9=>1, 2=>1, 6=>1}

# Sort
puts "Sorted: #{collection.sort.inspect}"
puts "Sorted descending: #{collection.sort.reverse.inspect}"
puts "Sorted with block: #{collection.sort { |a, b| b <=> a }.inspect}"

# Sort by
words = ["apple", "kiwi", "banana", "cherry", "date"]
sorted_by_length = words.sort_by { |w| w.length }
puts "Sorted by length: #{sorted_by_length.inspect}"
# => ["kiwi", "date", "apple", "banana", "cherry"]

# SEARCHING AND FILTERING
puts "\n--- ADVANCED SEARCHING ---"

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Find/detect - first match
first_even = numbers.find { |n| n.even? }
puts "First even: #{first_even}"  # => 2

# Find_all/select - all matches (we've seen)
# Find_index - index of first match
index_of_first_even = numbers.find_index { |n| n.even? }
puts "Index of first even: #{index_of_first_even}"  # => 1

# Select with multiple conditions
special = numbers.select { |n| n > 3 && n < 8 && n.odd? }
puts "Special numbers: #{special.inspect}"  # => [5, 7]

# Grep - pattern matching (uses ===)
fruits = ["apple", "banana", "cherry", "apricot", "blueberry"]
grep_a = fruits.grep(/^a/)  # Starts with 'a'
puts "Grep 'a': #{grep_a.inspect}"  # => ["apple", "apricot"]

# Grep with block transformation
grep_with_block = fruits.grep(/^b/) { |f| f.upcase }
puts "Grep with block: #{grep_with_block.inspect}"  # => ["BANANA", "BLUEBERRY"]

# REDUCTION AND ACCUMULATION
puts "\n--- REDUCTION ---"

# Inject/reduce - accumulate
sum = numbers.reduce(0) { |acc, n| acc + n }
puts "Sum with reduce: #{sum}"

# Shorter syntax
product = numbers.reduce(:*)
puts "Product: #{product}"

# Building hash with reduce
word_lengths = fruits.reduce({}) do |hash, fruit|
  hash[fruit] = fruit.length
  hash
end
puts "Word lengths: #{word_lengths.inspect}"

# Each_with_object (similar but always returns the object)
word_lengths2 = fruits.each_with_object({}) do |fruit, hash|
  hash[fruit] = fruit.length
end
puts "Each with object: #{word_lengths2.inspect}"

# COMBINATORICS
puts "\n--- COMBINATORICS ---"

letters = ["a", "b", "c"]

# Permutations
perms = letters.permutation(2).to_a
puts "Permutations of 2: #{perms.inspect}"

# Combinations
combs = letters.combination(2).to_a
puts "Combinations of 2: #{combs.inspect}"

# Repeated permutations
repeated_perms = letters.repeated_permutation(2).to_a
puts "Repeated permutations: #{repeated_perms.inspect}"

# Product (Cartesian product)
product = letters.product([1, 2])
puts "Product with [1,2]: #{product.inspect}"

# Zipping arrays
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["NYC", "LA", "Chicago"]

zipped = names.zip(ages, cities)
puts "Zipped: #{zipped.inspect}"
# => [["Alice", 25, "NYC"], ["Bob", 30, "LA"], ["Charlie", 35, "Chicago"]]

# Unzipping (transpose)
unzipped = zipped.transpose
puts "Transposed: #{unzipped.inspect}"
# => [["Alice", "Bob", "Charlie"], [25, 30, 35], ["NYC", "LA", "Chicago"]]

# CHAINING ENUMERABLES
puts "\n--- CHAINING ---"

result = (1..20)
  .select { |n| n.even? }
  .reject { |n| n % 4 == 0 }
  .map { |n| n * 3 }
  .take(3)

puts "Chained result: #{result.inspect}"  # First 3 even not divisible by 4, times 3

# LAZY ENUMERATION (for large/infinite collections)
puts "\n--- LAZY ENUMERATION ---"

# Without lazy - eager evaluation (creates intermediate arrays)
def eager_example
  (1..Float::INFINITY)
    .select { |n| n.even? }
    .first(5)  # This would run forever without .lazy!
rescue
  puts "Eager with infinite range would crash!"
end

# With lazy - on-demand evaluation
lazy_result = (1..Float::INFINITY)
  .lazy
  .select { |n| n.even? }
  .map { |n| n * n }
  .first(5)

puts "Lazy result (first 5 even squares): #{lazy_result.inspect}"

# Lazy works with files too
def process_large_file_lazily
  puts "Processing file lazily (example)"
  # File.foreach("large_file.txt").lazy.select { |line| line.include?("error") }.first(10)
end

# ============================================
# 4. HASHES - KEY-VALUE PAIRS
# ============================================

puts "\n" + "="*60
puts "HASHES - DEEP DIVE"
puts "="*60

# CREATION
puts "\n--- HASH CREATION ---"

# Literal syntax
empty = {}
person = { "name" => "Alice", "age" => 30, "city" => "NYC" }
person_symbols = { name: "Alice", age: 30, city: "NYC" }  # Ruby 1.9+ syntax

# Using Hash.new with default value
default_hash = Hash.new(0)  # Default value for missing keys is 0
default_hash["count"] += 1
puts "Default hash: #{default_hash.inspect}"  # => {"count"=>1}
puts "Missing key: #{default_hash["missing"]}"  # => 0

# Hash.new with block for dynamic defaults
dynamic_hash = Hash.new { |hash, key| hash[key] = [] }
dynamic_hash["users"] << "Alice"
dynamic_hash["users"] << "Bob"
puts "Dynamic hash: #{dynamic_hash.inspect}"  # => {"users"=>["Alice", "Bob"]}

# Using Hash[] constructor
hash1 = Hash["a", 1, "b", 2]           # => {"a"=>1, "b"=>2}
hash2 = Hash[[["a", 1], ["b", 2]]]      # From array of pairs
hash3 = Hash[ {a: 1, b: 2} ]            # From another hash
puts "Hash[] examples: #{hash1.inspect}"

# ACCESSING ELEMENTS
puts "\n--- HASH ACCESS ---"

settings = { theme: "dark", volume: 80, notifications: true }

# Basic access
puts settings[:theme]           # => "dark"
puts settings["theme"]          # => nil (different key type)

# Fetch (raises error if missing)
puts settings.fetch(:volume)    # => 80
# puts settings.fetch(:missing) # Raises KeyError
puts settings.fetch(:missing, "default")  # => "default"

# Fetch with block
value = settings.fetch(:missing) { |key| "Key #{key} not found" }
puts value  # => "Key missing not found"

# values_at - get multiple values
puts settings.values_at(:theme, :notifications).inspect  # => ["dark", true]

# Dig - access nested hashes safely
nested = { user: { profile: { name: "Alice", age: 30 } } }
puts nested.dig(:user, :profile, :name)     # => "Alice"
puts nested.dig(:user, :settings, :color)   # => nil (no error)

# MODIFYING HASHES
puts "\n--- HASH MODIFICATION ---"
config = {}

# Adding/updating
config[:host] = "localhost"
config[:port] = 3000
puts "After adds: #{config.inspect}"

# Multiple updates at once
config.merge!(username: "admin", password: "secret")
puts "After merge!: #{config.inspect}"

# Conditional updates
config[:debug] = true unless config.key?(:debug)

# Store (alias for []=)
config.store(:timeout, 30)
puts "After store: #{config.inspect}"

# REMOVING ELEMENTS
puts "\n--- HASH REMOVAL ---"
user = { name: "Alice", age: 30, city: "NYC", phone: "123-4567" }

# Delete by key
removed = user.delete(:phone)
puts "Removed: #{removed}, hash now: #{user.inspect}"

# Delete if - with block
user.delete_if { |key, value| key == :city || value.is_a?(Integer) }
puts "After delete_if: #{user.inspect}"  # Only :name remains

# Shift - remove first key-value pair
first = user.shift
puts "Shifted: #{first.inspect}, hash now: #{user.inspect}"

# Clear
user.clear
puts "After clear: #{user.inspect}"

# ITERATING OVER HASHES
puts "\n--- HASH ITERATION ---"
inventory = { apples: 5, bananas: 3, cherries: 10 }

# Each (key-value)
inventory.each do |item, quantity|
  puts "We have #{quantity} #{item}"
end

# Each with index
inventory.each_with_index do |(item, quantity), index|
  puts "#{index}: #{item} - #{quantity}"
end

# Each_key (just keys)
inventory.each_key { |item| puts "Item: #{item}" }

# Each_value (just values)
inventory.each_value { |qty| puts "Quantity: #{qty}" }

# Map over hash (returns array)
mapped = inventory.map { |item, qty| "#{item}: #{qty}" }
puts "Mapped: #{mapped.inspect}"

# TRANSFORMING HASHES
puts "\n--- HASH TRANSFORMATION ---"
original = { a: 1, b: 2, c: 3 }

# Transform keys
upcased_keys = original.transform_keys { |k| k.to_s.upcase }
puts "Transform keys: #{upcased_keys.inspect}"

# Transform values
doubled_values = original.transform_values { |v| v * 2 }
puts "Transform values: #{doubled_values.inspect}"

# Invert (swap keys and values)
inverted = original.invert
puts "Inverted: #{inverted.inspect}"  # => {1=>:a, 2=>:b, 3=>:c}

# Select/filter
gt_one = original.select { |k, v| v > 1 }
puts "Select v>1: #{gt_one.inspect}"

# Reject
lte_one = original.reject { |k, v| v > 1 }
puts "Reject v>1: #{lte_one.inspect}"

# MERGING HASHES
puts "\n--- HASH MERGING ---"
defaults = { host: "localhost", port: 80, debug: false }
custom = { port: 3000, debug: true, ssl: true }

# Merge (non-destructive)
merged = defaults.merge(custom)
puts "Merged: #{merged.inspect}"
puts "Defaults unchanged: #{defaults.inspect}"

# Merge with block for conflict resolution
merged_with_block = defaults.merge(custom) do |key, default_val, custom_val|
  if key == :port
    default_val + custom_val  # Sum ports instead of override
  else
    custom_val  # Default to custom value
  end
end
puts "Merge with block: #{merged_with_block.inspect}"

# CONVERTING HASHES
puts "\n--- HASH CONVERSION ---"
hash = { a: 1, b: 2, c: 3 }

# To array
to_array = hash.to_a
puts "To array: #{to_array.inspect}"  # => [[:a, 1], [:b, 2], [:c, 3]]

# Flatten (with optional level)
flattened = hash.flatten
puts "Flattened: #{flattened.inspect}"  # => [:a, 1, :b, 2, :c, 3]

# To hash (identity)
back_to_hash = to_array.to_h
puts "Back to hash: #{back_to_hash.inspect}"

# ============================================
# 5. ALGORITHMIC THINKING - SEARCH, FILTER, TRANSFORM
# ============================================

puts "\n" + "="*60
puts "ALGORITHMIC THINKING - REAL PROBLEMS"
puts "="*60

# PROBLEM 1: FIND DUPLICATES
puts "\n--- FINDING DUPLICATES ---"

def find_duplicates(array)
  seen = {}
  duplicates = []
  
  array.each do |item|
    if seen[item]
      duplicates << item unless duplicates.include?(item)
    else
      seen[item] = true
    end
  end
  
  duplicates
end

# More Ruby-ish version
def find_duplicates_rubyish(array)
  array.group_by { |e| e }.select { |_, v| v.size > 1 }.keys
end

test_array = [1, 2, 3, 2, 4, 5, 3, 6, 1, 7, 8, 1]
puts "Original: #{test_array.inspect}"
puts "Duplicates (manual): #{find_duplicates(test_array).inspect}"
puts "Duplicates (rubyish): #{find_duplicates_rubyish(test_array).inspect}"

# PROBLEM 2: FREQUENCY ANALYSIS
puts "\n--- FREQUENCY ANALYSIS ---"

def word_frequency(text)
  # Normalize: downcase, remove punctuation, split
  words = text.downcase.gsub(/[^a-z\s]/, '').split
  
  # Count frequencies
  frequencies = words.each_with_object(Hash.new(0)) do |word, counts|
    counts[word] += 1
  end
  
  # Sort by frequency descending
  frequencies.sort_by { |_, count| -count }.to_h
end

sample_text = "The cat in the hat. The cat sat on the mat. The cat!"
frequencies = word_frequency(sample_text)
puts "Word frequencies: #{frequencies.inspect}"

# PROBLEM 3: COMMON ELEMENTS
puts "\n--- FINDING COMMON ELEMENTS ---"

def common_elements(*arrays)
  return [] if arrays.empty?
  
  # Start with first array as reference
  reference = arrays.first
  
  # Intersection with all others
  arrays[1..-1].each do |array|
    reference &= array
  end
  
  reference
end

a1 = [1, 2, 3, 4, 5]
a2 = [3, 4, 5, 6, 7]
a3 = [5, 6, 7, 8, 9]

puts "Common elements: #{common_elements(a1, a2, a3).inspect}"  # => [5]

# PROBLEM 4: GROUP BY CATEGORY
puts "\n--- GROUPING BY CATEGORY ---"

products = [
  { name: "Laptop", category: "electronics", price: 1000 },
  { name: "Shirt", category: "clothing", price: 25 },
  { name: "Phone", category: "electronics", price: 500 },
  { name: "Jeans", category: "clothing", price: 60 },
  { name: "Book", category: "media", price: 15 }
]

# Group by category
by_category = products.group_by { |p| p[:category] }
puts "Grouped by category:"
by_category.each do |category, items|
  puts "  #{category}: #{items.map { |i| i[:name] }.join(', ')}"
end

# Calculate average price per category
avg_price_by_category = products
  .group_by { |p| p[:category] }
  .transform_values do |items|
    total = items.sum { |i| i[:price] }
    (total.to_f / items.size).round(2)
  end

puts "Average price by category: #{avg_price_by_category.inspect}"

# PROBLEM 5: PAGINATION
puts "\n--- PAGINATION ALGORITHM ---"

class Paginator
  attr_reader :items, :page_size
  
  def initialize(items, page_size = 10)
    @items = items
    @page_size = page_size
  end
  
  def page(page_number)
    start_index = (page_number - 1) * page_size
    items[start_index, page_size] || []
  end
  
  def total_pages
    (items.length.to_f / page_size).ceil
  end
  
  def each_page
    return enum_for(:each_page) unless block_given?
    
    1.upto(total_pages) do |page_num|
      yield page(page_num), page_num, page_num == total_pages
    end
  end
end

data = (1..27).to_a
paginator = Paginator.new(data, 10)

puts "Page 1: #{paginator.page(1).inspect}"
puts "Page 2: #{paginator.page(2).inspect}"
puts "Page 3: #{paginator.page(3).inspect}"
puts "Total pages: #{paginator.total_pages}"

puts "Iterating through pages:"
paginator.each_page do |page_data, page_num, is_last|
  puts "Page #{page_num}: #{page_data.first}..#{page_data.last} #{'(last)' if is_last}"
end

# PROBLEM 6: SEARCH ALGORITHMS
puts "\n--- SEARCH ALGORITHMS ---"

# Linear search (unsorted)
def linear_search(array, target)
  array.each_with_index do |item, index|
    return index if item == target
  end
  nil
end

# Binary search (sorted array)
def binary_search(array, target)
  left = 0
  right = array.length - 1
  
  while left <= right
    mid = (left + right) / 2
    guess = array[mid]
    
    if guess == target
      return mid
    elsif guess > target
      right = mid - 1
    else
      left = mid + 1
    end
  end
  
  nil
end

sorted = [1, 3, 5, 7, 9, 11, 13, 15, 17]
puts "Binary search for 9: index #{binary_search(sorted, 9)}"
puts "Binary search for 6: #{binary_search(sorted, 6) || 'not found'}"

# PROBLEM 7: DATA TRANSFORMATION PIPELINES
puts "\n--- TRANSFORMATION PIPELINES ---"

class DataPipeline
  def initialize(data)
    @data = data
    @transformations = []
  end
  
  def filter(&block)
    @transformations << ->(data) { data.select(&block) }
    self
  end
  
  def map(&block)
    @transformations << ->(data) { data.map(&block) }
    self
  end
  
  def reduce(initial, &block)
    @transformations << ->(data) { data.reduce(initial, &block) }
    self
  end
  
  def execute
    @transformations.reduce(@data) do |result, transformation|
      transformation.call(result)
    end
  end
end

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

result = DataPipeline.new(numbers)
  .filter { |n| n.even? }
  .map { |n| n * n }
  .reduce(0) { |sum, n| sum + n }
  .execute

puts "Pipeline result (sum of squares of evens): #{result}"

# PROBLEM 8: CACHING/MEMOIZATION
puts "\n--- CACHING PATTERNS ---"

class Fibonacci
  def initialize
    @cache = { 0 => 0, 1 => 1 }
  end
  
  def calculate(n)
    return @cache[n] if @cache.key?(n)
    
    @cache[n] = calculate(n - 1) + calculate(n - 2)
  end
  
  def stats
    puts "Cache size: #{@cache.size}"
    puts "Cached values: #{@cache.keys.sort.inspect}"
  end
end

fib = Fibonacci.new
puts "Fibonacci(10): #{fib.calculate(10)}"
puts "Fibonacci(20): #{fib.calculate(20)}"
puts "Fibonacci(15): #{fib.calculate(15)} (cached!)"
fib.stats

# PROBLEM 9: RATE LIMITING / WINDOWING
puts "\n--- SLIDING WINDOW ---"

def max_subarray_sum(array, window_size)
  return 0 if array.empty? || window_size <= 0
  
  # Calculate first window sum
  current_sum = array[0...window_size].sum
  max_sum = current_sum
  
  # Slide the window
  (window_size...array.length).each do |i|
    # Remove leftmost, add rightmost
    current_sum = current_sum - array[i - window_size] + array[i]
    max_sum = [max_sum, current_sum].max
  end
  
  max_sum
end

stock_prices = [100, 102, 98, 105, 107, 103, 99, 110]
puts "Stock prices: #{stock_prices.inspect}"
puts "Max 3-day sum: #{max_subarray_sum(stock_prices, 3)}"

# PROBLEM 10: REAL-WORLD DATA PROCESSING
puts "\n--- REAL-WORLD DATA PROCESSING ---"

# Simulated log entries
log_entries = [
  { timestamp: "2023-01-01 10:00", user: "alice", action: "login", success: true },
  { timestamp: "2023-01-01 10:05", user: "bob", action: "login", success: true },
  { timestamp: "2023-01-01 10:10", user: "alice", action: "purchase", success: true },
  { timestamp: "2023-01-01 10:15", user: "charlie", action: "login", success: false },
  { timestamp: "2023-01-01 10:20", user: "alice", action: "logout", success: true },
  { timestamp: "2023-01-01 10:25", user: "bob", action: "purchase", success: true },
  { timestamp: "2023-01-01 10:30", user: "charlie", action: "login", success: true },
  { timestamp: "2023-01-01 10:35", user: "david", action: "login", success: true }
]

# Analysis functions
def analyze_logs(logs)
  {
    total_entries: logs.count,
    unique_users: logs.map { |e| e[:user] }.uniq.count,
    success_rate: logs.count { |e| e[:success] }.to_f / logs.count * 100,
    actions: logs.group_by { |e| e[:action] }.transform_values(&:count),
    user_activity: logs.group_by { |e| e[:user] }
                       .transform_values { |entries| entries.map { |e| e[:action] } },
    failed_logins: logs.select { |e| e[:action] == "login" && !e[:success] }.count
  }
end

stats = analyze_logs(log_entries)
puts "Log Analysis Results:"
stats.each do |key, value|
  puts "  #{key}: #{value.inspect}"
end

# SUMMARY: THINKING LIKE A RUBYIST
puts "\n" + "="*60
puts "SUMMARY - RUBY DATA STRUCTURES PRINCIPLES"
puts "="*60

puts """
1. ARRAYS: Use for ordered collections, stacks, queues
   - Prefer specific methods over manual loops
   - Remember destructive (!) vs non-destructive versions

2. SYMBOLS vs STRINGS:
   - Symbols: immutable, unique, good for identifiers/keys
   - Strings: mutable, good for text manipulation
   - Convert as needed: to_sym, to_s

3. ENUMERABLE is your friend:
   - Learn the 20+ methods - they eliminate most loops
   - Chain them for readable transformations
   - Use lazy for large/infinite collections

4. HASHES are extremely versatile:
   - Great for lookup tables, caches, grouped data
   - Default values and blocks for dynamic behavior
   - transform_keys/values for easy modification

5. ALGORITHMIC THINKING:
   - Break problems into transformations
   - Use Ruby's built-in methods first
   - Optimize only when necessary
   - Think in terms of data flow, not steps
"""