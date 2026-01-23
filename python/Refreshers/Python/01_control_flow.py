"""
COMPREHENSIVE PYTHON CONTROL FLOW DEMONSTRATION
This script demonstrates Python control flow constructs with detailed examples.
"""

print("=" * 70)
print("PYTHON CONTROL FLOW CONSTRUCTS")
print("=" * 70)

# ============================================================================
# SECTION 1: IF / ELIF / ELSE STATEMENTS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 1: CONDITIONAL STATEMENTS - if / elif / else")
print("=" * 60)

# ----------------------------------------------------------------------------
# BASIC IF STATEMENT
# ----------------------------------------------------------------------------
print("1.1 Basic if statement:")
temperature = 25

if temperature > 30:
    print("   It's hot outside!")
    
# Nothing prints because temperature (25) is not > 30

temperature = 35
if temperature > 30:
    print(f"   It's hot outside! ({temperature}°C)")

# ----------------------------------------------------------------------------
# IF-ELSE STATEMENT
# ----------------------------------------------------------------------------
print("\n1.2 if-else statement:")

age = 17
if age >= 18:
    print("   You are eligible to vote.")
else:
    print("   You are not eligible to vote yet.")
    years_to_wait = 18 - age
    print(f"   Please wait {years_to_wait} more year(s).")

# ----------------------------------------------------------------------------
# IF-ELIF-ELSE CHAIN
# ----------------------------------------------------------------------------
print("\n1.3 if-elif-else chain:")

score = 85
print(f"   Score: {score}")

if score >= 90:
    grade = "A"
    print("   Excellent!")
elif score >= 80:  # Only checked if first condition is False
    grade = "B"
    print("   Good job!")
elif score >= 70:  # Only checked if all previous conditions are False
    grade = "C"
    print("   Fair.")
elif score >= 60:
    grade = "D"
    print("   Needs improvement.")
else:  # Executed only if all conditions above are False
    grade = "F"
    print("   Failed.")

print(f"   Grade: {grade}")

# ----------------------------------------------------------------------------
# NESTED IF STATEMENTS
# ----------------------------------------------------------------------------
print("\n1.4 Nested if statements:")

is_weekend = True
time = 14  # 24-hour format

print(f"   Is weekend: {is_weekend}, Time: {time}:00")

if is_weekend:
    if time < 12:
        print("   Weekend morning - time to relax!")
    elif time < 18:
        print("   Weekend afternoon - maybe go out?")
    else:
        print("   Weekend evening - movie night!")
else:
    if time < 9:
        print("   Weekday morning - heading to work.")
    elif time < 17:
        print("   Work hours - busy at the office.")
    else:
        print("   Weekday evening - time to unwind.")

# ----------------------------------------------------------------------------
# MULTIPLE CONDITIONS WITH LOGICAL OPERATORS
# ----------------------------------------------------------------------------
print("\n1.5 Multiple conditions with logical operators:")

has_ticket = True
has_id = True
age = 20
is_vip = False

print(f"   Has ticket: {has_ticket}, Has ID: {has_id}, Age: {age}, VIP: {is_vip}")

# Using 'and' - all conditions must be True
if has_ticket and has_id and age >= 18:
    print("   Entry granted.")
else:
    print("   Entry denied.")
    
# Using 'or' - at least one condition must be True
if is_vip or (has_ticket and has_id and age >= 18):
    print("   Welcome to the event!")
else:
    print("   Sorry, you cannot enter.")
    
# Complex conditions with parentheses for clarity
if (has_ticket and has_id) and (age >= 18 or is_vip):
    print("   Complex condition satisfied.")

# ============================================================================
# SECTION 2: FOR LOOPS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 2: FOR LOOPS - Iterating over sequences")
print("=" * 60)

# ----------------------------------------------------------------------------
# BASIC FOR LOOP WITH LISTS
# ----------------------------------------------------------------------------
print("2.1 Basic for loop with lists:")

fruits = ["apple", "banana", "cherry", "date"]

print("   Fruits in the basket:")
for fruit in fruits:
    print(f"     - {fruit}")

# ----------------------------------------------------------------------------
# FOR LOOP WITH INDEX USING range()
# ----------------------------------------------------------------------------
print("\n2.2 for loop with range():")

print("   Counting from 0 to 4:")
for i in range(5):  # range(stop) - 0 to stop-1
    print(f"     Number: {i}")

print("\n   Counting from 2 to 6:")
for i in range(2, 7):  # range(start, stop) - start to stop-1
    print(f"     Number: {i}")

print("\n   Counting even numbers from 0 to 10:")
for i in range(0, 11, 2):  # range(start, stop, step)
    print(f"     Even number: {i}")

print("\n   Counting backwards from 10 to 1:")
for i in range(10, 0, -1):
    print(f"     Countdown: {i}")

# ----------------------------------------------------------------------------
# FOR LOOP WITH INDEX AND VALUE USING enumerate()
# ----------------------------------------------------------------------------
print("\n2.3 for loop with enumerate():")

colors = ["red", "green", "blue", "yellow"]

print("   Colors with their indices:")
for index, color in enumerate(colors):
    print(f"     Index {index}: {color}")

# enumerate() with custom start index
print("\n   Colors with custom starting index (starting at 1):")
for index, color in enumerate(colors, start=1):
    print(f"     Color #{index}: {color}")

# ----------------------------------------------------------------------------
# FOR LOOP WITH MULTIPLE SEQUENCES USING zip()
# ----------------------------------------------------------------------------
print("\n2.4 for loop with zip():")

names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
cities = ["New York", "London", "Paris"]

print("   People information:")
for name, age, city in zip(names, ages, cities):
    print(f"     {name}, {age} years old, from {city}")

# What happens with different length sequences?
short_list = [1, 2, 3]
long_list = ["A", "B", "C", "D", "E"]

print("\n   zip() stops at the shortest sequence:")
for num, letter in zip(short_list, long_list):
    print(f"     {num} -> {letter}")

# ----------------------------------------------------------------------------
# FOR LOOP WITH DICTIONARIES
# ----------------------------------------------------------------------------
print("\n2.5 for loop with dictionaries:")

student = {
    "name": "Alice",
    "age": 20,
    "major": "Computer Science",
    "gpa": 3.8
}

print("   Dictionary keys:")
for key in student:  # or student.keys()
    print(f"     Key: {key}")

print("\n   Dictionary values:")
for value in student.values():
    print(f"     Value: {value}")

print("\n   Dictionary key-value pairs:")
for key, value in student.items():
    print(f"     {key}: {value}")

# ----------------------------------------------------------------------------
# NESTED FOR LOOPS
# ----------------------------------------------------------------------------
print("\n2.6 Nested for loops:")

print("   Multiplication table (1-3):")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"     {i} × {j} = {i * j}")
    print()  # Empty line between tables

# ============================================================================
# SECTION 3: WHILE LOOPS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 3: WHILE LOOPS - Repeating while condition is True")
print("=" * 60)

# ----------------------------------------------------------------------------
# BASIC WHILE LOOP
# ----------------------------------------------------------------------------
print("3.1 Basic while loop:")

count = 1
print("   Counting from 1 to 5:")
while count <= 5:
    print(f"     Count: {count}")
    count += 1  # CRITICAL: Don't forget to update the condition variable!

# ----------------------------------------------------------------------------
# WHILE LOOP WITH USER INPUT
# ----------------------------------------------------------------------------
print("\n3.2 while loop with simulated user input:")

# For demonstration, we'll simulate user input
simulated_inputs = ["yes", "yes", "no"]
input_index = 0

print("   Simulated user input loop:")
response = "yes"
attempts = 0

while response == "yes" and attempts < 5:
    attempts += 1
    print(f"     Attempt {attempts}: Do you want to continue?")
    
    # Simulate getting user input
    if input_index < len(simulated_inputs):
        response = simulated_inputs[input_index]
        input_index += 1
    else:
        response = "no"
    
    print(f"     User said: {response}")

print(f"   Loop ended after {attempts} attempts.")

# ----------------------------------------------------------------------------
# INFINITE LOOP WITH BREAK
# ----------------------------------------------------------------------------
print("\n3.3 Infinite loop with break statement:")

counter = 0
print("   Infinite loop that breaks when counter reaches 5:")
while True:  # This creates an infinite loop
    counter += 1
    print(f"     Counter: {counter}")
    
    if counter >= 5:
        print("     Breaking the infinite loop!")
        break  # Exit the loop immediately

# ----------------------------------------------------------------------------
# WHILE LOOP WITH CONTINUE
# ----------------------------------------------------------------------------
print("\n3.4 while loop with continue statement:")

number = 0
print("   Printing only even numbers from 0 to 10:")
while number <= 10:
    if number % 2 != 0:  # If number is odd
        number += 1
        continue  # Skip to next iteration
    print(f"     Even number: {number}")
    number += 1

# ============================================================================
# SECTION 4: BREAK, CONTINUE, AND PASS
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 4: LOOP CONTROL STATEMENTS - break, continue, pass")
print("=" * 60)

# ----------------------------------------------------------------------------
# BREAK STATEMENT
# ----------------------------------------------------------------------------
print("4.1 break statement - exit loop immediately:")

print("   Searching for a number in a list:")
numbers = [1, 3, 5, 7, 9, 2, 4, 6, 8, 10]
target = 7

for num in numbers:
    print(f"     Checking: {num}")
    if num == target:
        print(f"     Found target {target}! Stopping search.")
        break
    print("     Not found, continuing...")

# ----------------------------------------------------------------------------
# CONTINUE STATEMENT
# ----------------------------------------------------------------------------
print("\n4.2 continue statement - skip current iteration:")

print("   Processing numbers, skipping negatives:")
values = [10, -5, 3, -2, 8, 0, -1, 7]

for value in values:
    if value < 0:
        print(f"     Skipping negative value: {value}")
        continue  # Skip to next iteration
    if value == 0:
        print(f"     Zero found - special case: {value}")
        continue
    result = value * 2
    print(f"     Processing {value}: {value} × 2 = {result}")

# ----------------------------------------------------------------------------
# PASS STATEMENT
# ----------------------------------------------------------------------------
print("\n4.3 pass statement - do nothing (placeholder):")

print("   Using pass as a placeholder:")

# pass is useful when you need syntactically correct but empty code blocks
for i in range(5):
    if i == 2:
        pass  # Do nothing, just a placeholder for future code
    else:
        print(f"     i = {i}")

print("\n   Without pass (would cause syntax error):")
print("   # This code would not run without pass")
print("   # for i in range(5):")
print("   #     if i == 2:")
print("   #         # TODO: Add special handling for i == 2")
print("   #     print(f'i = {i}')")

# ============================================================================
# SECTION 5: RANGE, ENUMERATE, ZIP IN DETAIL
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 5: RANGE, ENUMERATE, ZIP - Detailed Examples")
print("=" * 60)

# ----------------------------------------------------------------------------
# RANGE OBJECT
# ----------------------------------------------------------------------------
print("5.1 range() function in detail:")

# range() doesn't create a list, it creates a range object (memory efficient)
r = range(5)
print(f"   range(5): {r}")
print(f"   Type: {type(r)}")
print(f"   Converted to list: {list(r)}")

print("\n   range() with different parameters:")
print(f"   range(2, 8): {list(range(2, 8))}")
print(f"   range(0, 10, 2): {list(range(0, 10, 2))}")
print(f"   range(10, 0, -2): {list(range(10, 0, -2))}")

# range() is not just for loops
print("\n   Using range() for indexing:")
data = ["a", "b", "c", "d", "e", "f"]
print(f"   Data: {data}")
print("   Every second element:")
for i in range(0, len(data), 2):
    print(f"     data[{i}] = {data[i]}")

# ----------------------------------------------------------------------------
# ENUMERATE OBJECT
# ----------------------------------------------------------------------------
print("\n5.2 enumerate() function in detail:")

# enumerate() returns an enumerate object (iterator)
items = ["apple", "banana", "cherry"]
enum_obj = enumerate(items)
print(f"   enumerate(items): {enum_obj}")
print(f"   Type: {type(enum_obj)}")
print(f"   Converted to list: {list(enum_obj)}")

# enumerate() with different starting index
print("\n   enumerate() with start parameter:")
for index, value in enumerate(items, start=100):
    print(f"     Index {index}: {value}")

# Practical example with enumerate
print("\n   Practical example - finding an item:")
shopping_list = ["milk", "eggs", "bread", "butter"]
item_to_find = "bread"

for position, item in enumerate(shopping_list, 1):
    if item == item_to_find:
        print(f"     Found '{item_to_find}' at position {position}")
        break
else:
    # Note: This else belongs to the for loop, not the if statement!
    # It executes if the loop completes without hitting break
    print(f"     '{item_to_find}' not found in the list")

# ----------------------------------------------------------------------------
# ZIP OBJECT
# ----------------------------------------------------------------------------
print("\n5.3 zip() function in detail:")

# zip() returns a zip object (iterator)
z = zip([1, 2, 3], ["a", "b", "c"])
print(f"   zip([1,2,3], ['a','b','c']): {z}")
print(f"   Type: {type(z)}")
print(f"   Converted to list: {list(z)}")

# zip() with different length sequences
print("\n   zip() with sequences of different lengths:")
numbers = [1, 2, 3, 4, 5]
letters = ["A", "B", "C"]
symbols = ["!", "@", "#", "$"]

print(f"   numbers: {numbers}")
print(f"   letters: {letters}")
print(f"   symbols: {symbols}")

print("\n   zip(numbers, letters, symbols):")
for item in zip(numbers, letters, symbols):
    print(f"     {item}")

print("\n   zip() stops at shortest sequence. To include all,")
print("   use itertools.zip_longest() from itertools module")

# Unzipping - the reverse of zipping
print("\n   Unzipping (reverse of zip):")
pairs = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
names, ages = zip(*pairs)  # The * unpacks the list
print(f"   Pairs: {pairs}")
print(f"   Names: {names}")
print(f"   Ages: {ages}")

# ============================================================================
# SECTION 6: PRACTICAL EXAMPLES PUTTING IT ALL TOGETHER
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 6: PRACTICAL EXAMPLES")
print("=" * 60)

# ----------------------------------------------------------------------------
# EXAMPLE 1: NUMBER GUESSING GAME
# ----------------------------------------------------------------------------
print("6.1 Number Guessing Game Simulation:")

import random

# Simulated game for demonstration
secret_number = random.randint(1, 10)
max_attempts = 3
attempts = 0
guessed_correctly = False

print(f"   Guess the number between 1 and 10. You have {max_attempts} attempts.")

# Simulate user guesses
simulated_guesses = [5, 8, 3]  # Last guess is correct

for guess in simulated_guesses:
    attempts += 1
    print(f"\n   Attempt {attempts}: Your guess: {guess}")
    
    if guess == secret_number:
        print(f"   Congratulations! You guessed the number {secret_number}!")
        guessed_correctly = True
        break
    elif guess < secret_number:
        print("   Too low!")
    else:
        print("   Too high!")
    
    if attempts >= max_attempts:
        print(f"   Game over! The secret number was {secret_number}.")
        break

# ----------------------------------------------------------------------------
# EXAMPLE 2: DATA PROCESSING PIPELINE
# ----------------------------------------------------------------------------
print("\n6.2 Data Processing Pipeline:")

# Simulate processing student records
students = [
    {"name": "Alice", "scores": [85, 92, 78]},
    {"name": "Bob", "scores": [72, 65, 80]},
    {"name": "Charlie", "scores": [90, 95, 88]},
    {"name": "Diana", "scores": [60, 55, 50]},
]

print("   Processing student scores:")
print("   " + "-" * 40)

for student in students:
    name = student["name"]
    scores = student["scores"]
    
    # Calculate average
    total = 0
    count = 0
    for score in scores:
        total += score
        count += 1
    average = total / count if count > 0 else 0
    
    # Determine grade
    if average >= 90:
        grade = "A"
    elif average >= 80:
        grade = "B"
    elif average >= 70:
        grade = "C"
    elif average >= 60:
        grade = "D"
    else:
        grade = "F"
    
    # Print results
    print(f"   Student: {name}")
    print(f"     Scores: {scores}")
    print(f"     Average: {average:.1f}")
    print(f"     Grade: {grade}")
    
    # Check for failing grades
    if grade == "F":
        print(f"     WARNING: {name} is failing!")

# ----------------------------------------------------------------------------
# EXAMPLE 3: PATTERN GENERATION
# ----------------------------------------------------------------------------
print("\n6.3 Pattern Generation with Nested Loops:")

print("   Pattern 1: Right-angled triangle")
for i in range(1, 6):
    for j in range(i):
        print("*", end="")
    print()

print("\n   Pattern 2: Number pyramid")
for i in range(1, 6):
    # Print spaces
    for j in range(5 - i):
        print(" ", end="")
    # Print numbers
    for j in range(1, i + 1):
        print(j, end=" ")
    print()

# ----------------------------------------------------------------------------
# EXAMPLE 4: PRIME NUMBER FINDER
# ----------------------------------------------------------------------------
print("\n6.4 Prime Number Finder (1-30):")

print("   Prime numbers between 1 and 30:")

for num in range(2, 31):
    is_prime = True
    
    # Check if num is divisible by any number from 2 to num-1
    for divisor in range(2, num):
        if num % divisor == 0:
            is_prime = False
            break
    
    if is_prime:
        print(f"     {num} is prime")

# ============================================================================
# SECTION 7: COMMON PITFALLS AND BEST PRACTICES
# ============================================================================

print("\n" + "=" * 60)
print("SECTION 7: COMMON PITFALLS AND BEST PRACTICES")
print("=" * 60)

print("7.1 Common Pitfalls:")

# Pitfall 1: Modifying a list while iterating over it
print("\n   Pitfall 1: Modifying a list while iterating")
numbers = [1, 2, 3, 4, 5]
print(f"   Original list: {numbers}")

# WRONG WAY - can cause unexpected behavior
# for num in numbers:
#     if num % 2 == 0:
#         numbers.remove(num)

# RIGHT WAY - create a copy or use list comprehension
numbers_to_remove = []
for num in numbers:
    if num % 2 == 0:
        numbers_to_remove.append(num)

for num in numbers_to_remove:
    numbers.remove(num)
    
print(f"   After removing evens (wrong approach demo): {numbers}")

# Pitfall 2: Infinite loops
print("\n   Pitfall 2: Forgetting to update loop variable")
print("   # This would create an infinite loop:")
print("   # count = 0")
print("   # while count < 5:")
print("   #     print(count)")
print("   # Missing: count += 1")

# Pitfall 3: Using = instead of == in conditions
print("\n   Pitfall 3: Using = (assignment) instead of == (comparison)")
x = 5
print(f"   x = {x}")

# WRONG: if x = 10:  # SyntaxError in Python
# CORRECT: if x == 10:

print("\n7.2 Best Practices:")

print("   1. Use meaningful variable names in loops")
print("      GOOD: for student in students:")
print("      BAD:  for s in stu_list:")

print("\n   2. Keep loops simple - if it gets complex, extract to a function")
print("      def calculate_average(scores):")
print("          total = sum(scores)")
print("          return total / len(scores) if scores else 0")

print("\n   3. Use enumerate() when you need both index and value")
print("      for i, value in enumerate(my_list):")

print("\n   4. Use zip() when you need to iterate over multiple sequences")
print("      for name, age in zip(names, ages):")

print("\n   5. Use break and continue judiciously - don't overcomplicate")

print("\n   6. Consider using while True with break for input validation:")
print("      while True:")
print("          user_input = input('Enter a number: ')")
print("          if user_input.isdigit():")
print("              break")
print("          print('Invalid input. Try again.')")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print("""
Key Control Flow Concepts Covered:

1. CONDITIONAL STATEMENTS:
   - if: Execute code if condition is True
   - elif: Check additional conditions if previous ones were False
   - else: Execute code if all conditions are False

2. FOR LOOPS:
   - Iterate over sequences (lists, strings, dictionaries, etc.)
   - Can use range() for numeric iteration
   - enumerate() provides both index and value
   - zip() iterates over multiple sequences simultaneously

3. WHILE LOOPS:
   - Repeat while a condition remains True
   - Useful for unknown iteration counts
   - Can create infinite loops (while True)

4. LOOP CONTROL STATEMENTS:
   - break: Exit the loop immediately
   - continue: Skip to the next iteration
   - pass: Do nothing (placeholder)

5. USEFUL FUNCTIONS:
   - range(): Generate sequences of numbers
   - enumerate(): Get index-value pairs
   - zip(): Combine multiple sequences

Remember:
- Python uses indentation (4 spaces) to define code blocks
- Keep loops simple and readable
- Choose the right loop for the task:
  * Use for loops when you know how many iterations
  * Use while loops when iteration depends on a condition
""")

print("=" * 70)
print("END OF CONTROL FLOW DEMONSTRATION")
print("=" * 70)