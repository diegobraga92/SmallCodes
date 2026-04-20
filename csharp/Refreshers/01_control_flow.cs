/*
    C# CONTROL FLOW
    Covering: Conditional statements, loops, pattern matching, jump statements
    
    This file demonstrates control flow structures in C# programming.
*/

using System;

namespace CSharpRefresher.ControlFlow
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Control Flow Demonstration ===\n");
            
            DemonstrateConditionals();
            DemonstrateLoops();
            DemonstratePatternMatching();
            DemonstrateJumpStatements();
            
            Console.WriteLine("\n=== Control Flow Complete ===");
        }
        
        static void DemonstrateConditionals()
        {
            Console.WriteLine("============ CONDITIONAL STATEMENTS ============\n");
            
            int x = 10;
            
            // if-else statement
            Console.WriteLine("=== if-else Statement ===");
            if (x > 5)
            {
                Console.WriteLine("x is greater than 5");
            }
            else if (x == 5)
            {
                Console.WriteLine("x equals 5");
            }
            else
            {
                Console.WriteLine("x is less than 5");
            }
            
            // Nested if statements
            Console.WriteLine("\n=== Nested if Statements ===");
            int y = 15;
            if (x > 0)
            {
                if (y > 0)
                {
                    Console.WriteLine("Both x and y are positive");
                }
                else
                {
                    Console.WriteLine("x is positive but y is not");
                }
            }
            
            // Ternary operator (conditional operator)
            Console.WriteLine("\n=== Ternary Operator ===");
            string result = x > 5 ? "greater than 5" : "5 or less";
            Console.WriteLine($"x is {result}");
            
            // Nested ternary (use with caution - can be hard to read)
            string grade = x >= 90 ? "A" : 
                          x >= 80 ? "B" : 
                          x >= 70 ? "C" : 
                          x >= 60 ? "D" : "F";
            Console.WriteLine($"Grade for score {x}: {grade}");
            
            // Traditional switch statement
            Console.WriteLine("\n=== Traditional switch Statement ===");
            int dayOfWeek = 3;
            switch (dayOfWeek)
            {
                case 1:
                    Console.WriteLine("Monday");
                    break;
                case 2:
                    Console.WriteLine("Tuesday");
                    break;
                case 3:
                    Console.WriteLine("Wednesday");
                    break;
                case 4:
                    Console.WriteLine("Thursday");
                    break;
                case 5:
                    Console.WriteLine("Friday");
                    break;
                case 6:
                case 7:
                    Console.WriteLine("Weekend");
                    break;
                default:
                    Console.WriteLine("Invalid day");
                    break;
            }
            
            // Switch statement with goto case
            Console.WriteLine("\n=== switch with goto case ===");
            int value = 2;
            switch (value)
            {
                case 1:
                    Console.WriteLine("Case 1");
                    break;
                case 2:
                    Console.WriteLine("Case 2");
                    goto case 1; // Jump to case 1
                default:
                    Console.WriteLine("Default");
                    break;
            }
            
            // Switch expression (C# 8+)
            Console.WriteLine("\n=== Switch Expression (C# 8+) ===");
            string dayName = dayOfWeek switch
            {
                1 => "Monday",
                2 => "Tuesday",
                3 => "Wednesday",
                4 => "Thursday",
                5 => "Friday",
                6 or 7 => "Weekend", // Pattern combinators (C# 9+)
                _ => "Invalid day"   // Discard pattern for default
            };
            Console.WriteLine($"Day {dayOfWeek}: {dayName}");
            
            // Switch expression with property patterns
            var person = new { Name = "Alice", Age = 25 };
            string category = person switch
            {
                { Age: < 13 } => "Child",
                { Age: >= 13 and < 20 } => "Teenager", // Relational patterns (C# 9+)
                { Age: >= 20 and < 65 } => "Adult",
                { Age: >= 65 } => "Senior",
                _ => "Unknown"
            };
            Console.WriteLine($"{person.Name} ({person.Age}) is a {category}");
        }
        
        static void DemonstrateLoops()
        {
            Console.WriteLine("\n============ LOOPS ============\n");
            
            // for loop
            Console.WriteLine("=== for Loop ===");
            Console.Write("Counting 0 to 4: ");
            for (int i = 0; i < 5; i++)
            {
                Console.Write($"{i} ");
            }
            Console.WriteLine();
            
            // for loop with multiple variables
            Console.Write("\nMultiple variables in for loop: ");
            for (int i = 0, j = 10; i < 5; i++, j--)
            {
                Console.Write($"({i},{j}) ");
            }
            Console.WriteLine();
            
            // Infinite for loop (with break)
            Console.Write("\nInfinite for loop (breaks at 5): ");
            for (int i = 0; ; i++)
            {
                Console.Write($"{i} ");
                if (i >= 5) break;
            }
            Console.WriteLine();
            
            // while loop
            Console.WriteLine("\n=== while Loop ===");
            Console.Write("Counting 0 to 4: ");
            int count = 0;
            while (count < 5)
            {
                Console.Write($"{count} ");
                count++;
            }
            Console.WriteLine();
            
            // while loop with condition check at start
            Console.Write("\nwhile with condition (skips if false): ");
            int value = 10;
            while (value < 5)
            {
                Console.Write($"{value} "); // Never executes
            }
            Console.WriteLine("(loop skipped)");
            
            // do-while loop
            Console.WriteLine("\n=== do-while Loop ===");
            Console.Write("Counting 0 to 4: ");
            count = 0;
            do
            {
                Console.Write($"{count} ");
                count++;
            } while (count < 5);
            Console.WriteLine();
            
            // do-while executes at least once
            Console.Write("\ndo-while (executes once even if false): ");
            value = 10;
            do
            {
                Console.Write($"{value} "); // Executes once
            } while (value < 5);
            Console.WriteLine();
            
            // foreach loop
            Console.WriteLine("\n=== foreach Loop ===");
            int[] numbers = { 1, 2, 3, 4, 5 };
            Console.Write("Array elements: ");
            foreach (int num in numbers)
            {
                Console.Write($"{num} ");
            }
            Console.WriteLine();
            
            // foreach with strings
            Console.Write("\nString characters: ");
            string text = "Hello";
            foreach (char c in text)
            {
                Console.Write($"{c} ");
            }
            Console.WriteLine();
            
            // foreach with collections
            Console.Write("\nList elements: ");
            var list = new System.Collections.Generic.List<string> { "A", "B", "C" };
            foreach (var item in list)
            {
                Console.Write($"{item} ");
            }
            Console.WriteLine();
            
            // Nested loops
            Console.WriteLine("\n=== Nested Loops ===");
            Console.WriteLine("Multiplication table (1-3):");
            for (int i = 1; i <= 3; i++)
            {
                for (int j = 1; j <= 3; j++)
                {
                    Console.Write($"{i * j}\t");
                }
                Console.WriteLine();
            }
        }
        
        static void DemonstratePatternMatching()
        {
            Console.WriteLine("\n============ PATTERN MATCHING ============\n");
            
            // Type patterns
            Console.WriteLine("=== Type Patterns ===");
            object obj = 42;
            
            if (obj is int number)
            {
                Console.WriteLine($"It's an integer: {number}");
            }
            
            // Type pattern in switch
            Console.WriteLine("\n=== Type Patterns in switch ===");
            object value = "Hello";
            
            switch (value)
            {
                case int i:
                    Console.WriteLine($"It's an integer: {i}");
                    break;
                case string s:
                    Console.WriteLine($"It's a string: {s}");
                    break;
                case double d:
                    Console.WriteLine($"It's a double: {d}");
                    break;
                default:
                    Console.WriteLine("Unknown type");
                    break;
            }
            
            // Property patterns (C# 8+)
            Console.WriteLine("\n=== Property Patterns ===");
            var person = new { Name = "Bob", Age = 30, City = "New York" };
            
            if (person is { Age: >= 18 })
            {
                Console.WriteLine($"{person.Name} is an adult");
            }
            
            // Property patterns in switch expression
            string message = person switch
            {
                { Age: < 13 } => $"{person.Name} is a child",
                { Age: >= 13 and < 20 } => $"{person.Name} is a teenager",
                { Age: >= 20 and < 65, City: "New York" } => $"{person.Name} is a New York adult",
                { Age: >= 20 and < 65 } => $"{person.Name} is an adult",
                { Age: >= 65 } => $"{person.Name} is a senior",
                _ => "Unknown"
            };
            Console.WriteLine(message);
            
            // Tuple patterns
            Console.WriteLine("\n=== Tuple Patterns ===");
            var point = (5, 10);
            
            string quadrant = point switch
            {
                (0, 0) => "Origin",
                (var x, var y) when x > 0 && y > 0 => "Quadrant I",
                (var x, var y) when x < 0 && y > 0 => "Quadrant II",
                (var x, var y) when x < 0 && y < 0 => "Quadrant III",
                (var x, var y) when x > 0 && y < 0 => "Quadrant IV",
                (_, 0) => "On X-axis",
                (0, _) => "On Y-axis",
                _ => "Unknown"
            };
            Console.WriteLine($"Point {point} is in {quadrant}");
            
            // Positional patterns (with deconstruction)
            Console.WriteLine("\n=== Positional Patterns ===");
            var student = new Student("Alice", 20);
            
            string status = student switch
            {
                ("Alice", _) => "This is Alice!",
                (_, < 18) => "Underage student",
                (var name, var age) => $"{name} is {age} years old"
            };
            Console.WriteLine(status);
            
            // Relational patterns (C# 9+)
            Console.WriteLine("\n=== Relational Patterns ===");
            int score = 85;
            
            string grade = score switch
            {
                >= 90 => "A",
                >= 80 => "B",
                >= 70 => "C",
                >= 60 => "D",
                < 60 => "F",
                _ => "Invalid"
            };
            Console.WriteLine($"Score {score}: Grade {grade}");
            
            // Logical patterns (C# 9+)
            Console.WriteLine("\n=== Logical Patterns ===");
            object data = 42;
            
            string description = data switch
            {
                int i when i is > 0 and < 100 => "Positive two-digit number",
                int i when i is < 0 or > 1000 => "Out of normal range",
                string s when s is not null and not "" => "Non-empty string",
                null => "Null value",
                _ => "Other"
            };
            Console.WriteLine(description);
        }
        
        static void DemonstrateJumpStatements()
        {
            Console.WriteLine("\n============ JUMP STATEMENTS ============\n");
            
            // break statement
            Console.WriteLine("=== break Statement ===");
            Console.Write("Breaking at 5: ");
            for (int i = 0; i < 10; i++)
            {
                if (i == 5) break;
                Console.Write($"{i} ");
            }
            Console.WriteLine();
            
            // continue statement
            Console.WriteLine("\n=== continue Statement ===");
            Console.Write("Skipping even numbers: ");
            for (int i = 0; i < 10; i++)
            {
                if (i % 2 == 0) continue;
                Console.Write($"{i} ");
            }
            Console.WriteLine();
            
            // goto statement (use sparingly!)
            Console.WriteLine("\n=== goto Statement ===");
            Console.Write("Using goto: ");
            for (int i = 0; i < 10; i++)
            {
                if (i == 3) goto SkipToEnd;
                Console.Write($"{i} ");
            }
            SkipToEnd:
            Console.WriteLine(" (jumped to SkipToEnd)");
            
            // goto in switch (already shown)
            // return statement
            Console.WriteLine("\n=== return Statement ===");
            int result = Multiply(5, 3);
            Console.WriteLine($"Multiply(5, 3) = {result}");
            
            // Early return
            Console.Write("Early return example: ");
            string message = GetGreeting(14);
            Console.WriteLine(message);
            
            message = GetGreeting(20);
            Console.WriteLine(message);
            
            // throw statement (exception handling)
            Console.WriteLine("\n=== throw Statement ===");
            try
            {
                ValidateAge(-5);
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"Caught exception: {ex.Message}");
            }
            
            // yield return (in iterator methods)
            Console.WriteLine("\n=== yield return (Iterator) ===");
            Console.Write("First 5 even numbers: ");
            foreach (int even in GetEvenNumbers(5))
            {
                Console.Write($"{even} ");
            }
            Console.WriteLine();
        }
        
        // Helper methods for jump statements
        static int Multiply(int a, int b)
        {
            return a * b; // return statement
        }
        
        static string GetGreeting(int hour)
        {
            if (hour < 12) return "Good morning!"; // Early return
            if (hour < 18) return "Good afternoon!";
            return "Good evening!";
        }
        
        static void ValidateAge(int age)
        {
            if (age < 0)
            {
                throw new ArgumentException("Age cannot be negative", nameof(age));
            }
            Console.WriteLine($"Valid age: {age}");
        }
        
        static System.Collections.Generic.IEnumerable<int> GetEvenNumbers(int count)
        {
            for (int i = 0; i < count; i++)
            {
                yield return i * 2; // yield return
            }
        }
    }
    
    // Helper class for pattern matching
    class Student
    {
        public string Name { get; }
        public int Age { get; }
        
        public Student(string name, int age)
        {
            Name = name;
            Age = age;
        }
        
        // Deconstruct method for positional patterns
        public void Deconstruct(out string name, out int age)
        {
            name = Name;
            age = Age;
        }
    }
}