/*
    C# LAMBDA EXPRESSIONS
    File: 10_lambda_expressions.cs
    
    This file demonstrates lambda expressions in C# programming,
    covering concepts from junior to upper mid-level. Lambda expressions
    provide a concise way to represent anonymous methods using => syntax,
    enabling functional programming patterns in C#.
    
    Key Concepts Covered:
    1. Lambda Expression Syntax and Types
    2. Expression Lambdas vs Statement Lambdas
    3. Lambda Parameters and Type Inference
    4. Captured Variables and Closures
    5. Lambda Expressions with LINQ
    6. Lambda Expressions with Delegates
    7. Lambda Expressions with Events
    8. Performance Considerations
    9. Functional Programming Patterns
    10. Real-world Lambda Usage Patterns
*/

using System;
using System.Collections.Generic;
using System.Linq;

namespace CSharpRefresher.LambdaExpressions
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Lambda Expressions Demonstration ===\n");
            
            DemonstrateLambdaSyntax();
            DemonstrateExpressionVsStatementLambdas();
            DemonstrateLambdaParameters();
            DemonstrateVariableCaptureAndClosures();
            DemonstrateLambdasWithLinq();
            DemonstrateLambdasWithDelegates();
            DemonstrateLambdasWithEvents();
            DemonstratePerformanceConsiderations();
            DemonstrateFunctionalPatterns();
            DemonstrateRealWorldPatterns();
            
            Console.WriteLine("\n=== Lambda Expressions Complete ===");
        }
        
        static void DemonstrateLambdaSyntax()
        {
            Console.WriteLine("============ LAMBDA SYNTAX ============\n");
            
            // ============ BASIC LAMBDA SYNTAX ============
            Console.WriteLine("=== 1. Basic Lambda Syntax ===");
            
            // Lambda expression with explicit parameter type
            Func<int, int> squareExplicit = (int x) => x * x;
            
            // Lambda expression with implicit parameter type
            Func<int, int> squareImplicit = (x) => x * x;
            
            // Lambda expression with single parameter (parentheses optional)
            Func<int, int> squareNoParens = x => x * x;
            
            // Lambda expression with multiple parameters
            Func<int, int, int> add = (x, y) => x + y;
            
            // Lambda expression with no parameters
            Func<string> getMessage = () => "Hello, World!";
            
            Console.WriteLine($"Square explicit (5): {squareExplicit(5)}");
            Console.WriteLine($"Square implicit (5): {squareImplicit(5)}");
            Console.WriteLine($"Square no parens (5): {squareNoParens(5)}");
            Console.WriteLine($"Add (3, 4): {add(3, 4)}");
            Console.WriteLine($"Get message: {getMessage()}");
            
            // ============ LAMBDA ASSIGNMENT CONTEXTS ============
            Console.WriteLine("\n=== 2. Lambda Assignment Contexts ===");
            
            // Assign to delegate variable
            Action<string> logAction = message => Console.WriteLine($"[LOG] {message}");
            logAction("Testing action delegate");
            
            // Use as argument to method
            List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };
            var evenNumbers = numbers.Where(x => x % 2 == 0);
            Console.WriteLine($"Even numbers: {string.Join(", ", evenNumbers)}");
            
            // Return from method
            Func<int, Func<int, int>> createMultiplier = factor => x => x * factor;
            var doubleIt = createMultiplier(2);
            var tripleIt = createMultiplier(3);
            Console.WriteLine($"Double 10: {doubleIt(10)}");
            Console.WriteLine($"Triple 10: {tripleIt(10)}");
            
            // ============ LAMBDA TYPE INFERENCE ============
            Console.WriteLine("\n=== 3. Lambda Type Inference ===");
            
            // Compiler infers types from context
            var processNumber = (int x) => x * 2; // Explicit parameter type
            var processNumberImplicit = (int x) => x * 2; // Same but explicit
            
            // Type inference with method groups
            Func<string, int> stringLength = s => s.Length;
            Console.WriteLine($"Length of 'hello': {stringLength("hello")}");
            
            // Cannot infer from lambda alone (requires context)
            // var ambiguous = x => x * 2; // Error: cannot infer type
            
            // But works with explicit delegate type
            Func<int, int> works = x => x * 2;
            
            // ============ LAMBDA EXPRESSION TREES ============
            Console.WriteLine("\n=== 4. Lambda Expression Trees ===");
            
            // Expression lambda (can be converted to expression tree)
            System.Linq.Expressions.Expression<Func<int, int>> expression = x => x * x;
            
            Console.WriteLine($"Expression: {expression}");
            Console.WriteLine($"Expression body: {expression.Body}");
            Console.WriteLine($"Expression parameters: {expression.Parameters.Count}");
            
            // Compile expression tree to delegate
            Func<int, int> compiled = expression.Compile();
            Console.WriteLine($"Compiled result (5): {compiled(5)}");
            
            // Expression trees enable LINQ to SQL, Entity Framework, etc.
            Console.WriteLine("Expression trees enable query translation in ORMs");
        }
        
        static void DemonstrateExpressionVsStatementLambdas()
        {
            Console.WriteLine("\n============ EXPRESSION VS STATEMENT LAMBDAS ============\n");
            
            // ============ EXPRESSION LAMBDAS ============
            Console.WriteLine("=== 1. Expression Lambdas ===");
            
            // Single expression, returns value implicitly
            Func<int, int, int> multiply = (x, y) => x * y;
            Func<string, bool> isLong = s => s.Length > 10;
            Action<string> greet = name => Console.WriteLine($"Hello, {name}!");
            
            Console.WriteLine($"Multiply 6 * 7: {multiply(6, 7)}");
            Console.WriteLine($"Is 'hello' long? {isLong("hello")}");
            greet("Alice");
            
            // Expression lambda with method call
            Func<string, string> toUpper = s => s.ToUpper();
            Console.WriteLine($"ToUpper 'test': {toUpper("test")}");
            
            // ============ STATEMENT LAMBDAS ============
            Console.WriteLine("\n=== 2. Statement Lambdas ===");
            
            // Multiple statements in { }
            Func<int, int, int> complexCalculation = (x, y) =>
            {
                int sum = x + y;
                int product = x * y;
                return sum + product;
            };
            
            Action<int> processNumber = n =>
            {
                Console.WriteLine($"Processing number: {n}");
                if (n % 2 == 0)
                    Console.WriteLine("  Number is even");
                else
                    Console.WriteLine("  Number is odd");
                Console.WriteLine("  Processing complete");
            };
            
            Console.WriteLine($"Complex calculation (2, 3): {complexCalculation(2, 3)}");
            processNumber(42);
            
            // Statement lambda with local variables
            Func<int, int> factorial = n =>
            {
                int result = 1;
                for (int i = 1; i <= n; i++)
                    result *= i;
                return result;
            };
            
            Console.WriteLine($"Factorial 5: {factorial(5)}");
            
            // ============ WHEN TO USE WHICH ============
            Console.WriteLine("\n=== 3. When to Use Which ===");
            
            Console.WriteLine("""
                Expression Lambdas:
                • Single expression
                • Implicit return
                • Clean, concise
                • Good for simple operations
                • Can be expression trees
                
                Statement Lambdas:
                • Multiple statements
                • Explicit return required
                • Can have local variables
                • Good for complex logic
                • Cannot be expression trees
                """);
            
            // ============ PRACTICAL EXAMPLES ============
            Console.WriteLine("\n=== 4. Practical Examples ===");
            
            // Expression lambda in LINQ
            var numbers = Enumerable.Range(1, 10);
            var squares = numbers.Select(n => n * n);
            Console.WriteLine($"Squares: {string.Join(", ", squares)}");
            
            // Statement lambda for complex filtering
            var filtered = numbers.Where(n =>
            {
                bool isPrime = n > 1;
                for (int i = 2; i <= Math.Sqrt(n); i++)
                {
                    if (n % i == 0)
                    {
                        isPrime = false;
                        break;
                    }
                }
                return isPrime;
            });
            Console.WriteLine($"Primes: {string.Join(", ", filtered)}");
            
            // Mixed usage
            var processed = numbers.Select(n =>
            {
                if (n % 2 == 0)
                    return $"Even: {n}";
                else
                    return $"Odd: {n}";
            });
            Console.WriteLine($"Processed: {string.Join(", ", processed.Take(5))}...");
        }
        
        static void DemonstrateLambdaParameters()
        {
            Console.WriteLine("\n============ LAMBDA PARAMETERS ============\n");
            
            // ============ PARAMETER TYPES ============
            Console.WriteLine("=== 1. Parameter Types ===");
            
            // Explicit parameter types
            Func<int, double, string> formatExplicit = (int x, double y) => $"{x}: {y:F2}";
            
            // Implicit parameter types (inferred from delegate type)
            Func<int, double, string> formatImplicit = (x, y) => $"{x}: {y:F2}";
            
            // Mix of explicit and implicit (all must be explicit or all implicit)
            // Func<int, double, string> invalid = (int x, y) => $"{x}: {y}"; // Error
            
            Console.WriteLine($"Format explicit: {formatExplicit(5, 3.14159)}");
            Console.WriteLine($"Format implicit: {formatImplicit(5, 3.14159)}");
            
            // ============ DISCARDS (C# 7.0+) ============
            Console.WriteLine("\n=== 2. Discards (_) ===");
            
            // Discard unused parameters
            Action<string, int> logWithId = (message, _) => Console.WriteLine(message);
            logWithId("Important message", 12345);
            
            // Multiple discards
            Action<int, int, int> ignoreAll = (_, _, _) => Console.WriteLine("All ignored");
            ignoreAll(1, 2, 3);
            
            // Discard in expression
            Func<int, int> process = input => 
            {
                _ = input * 2; // Discard intermediate result
                return input + 1;
            };
            Console.WriteLine($"Process 5: {process(5)}");
            
            // ============ PARAMETER MODIFIERS ============
            Console.WriteLine("\n=== 3. Parameter Modifiers ===");
            
            // out parameters (C# 7.0+)
            Func<string, bool> tryParseInt = (string s) => int.TryParse(s, out _);
            Console.WriteLine($"TryParse '123': {tryParseInt("123")}");
            Console.WriteLine($"TryParse 'abc': {tryParseInt("abc")}");
            
            // ref parameters (C# 7.2+)
            Func<int, int, int> swapAndSum = (ref int a, ref int b) =>
            {
                int temp = a;
                a = b;
                b = temp;
                return a + b;
            };
            
            int x = 5, y = 10;
            // Note: Cannot use ref parameters with lambda assigned to Func/Action
            // Need custom delegate
            delegate int RefFunc(ref int a, ref int b);
            
            // ============ PARAMETER NAMING PATTERNS ============
            Console.WriteLine("\n=== 4. Parameter Naming Patterns ===");
            
            // Descriptive names
            Func<DateTime, DateTime, int> calculateDaysBetween = (startDate, endDate) => 
                (endDate - startDate).Days;
            
            // Short names for simple operations
            Func<int, int, int> add = (a, b) => a + b;
            
            // Use _ for unused parameters
            EventHandler<EventArgs> handler = (sender, _) => 
                Console.WriteLine($"Event from {sender}");
            
            // Context-appropriate names
            var users = new List<string> { "Alice", "Bob", "Charlie" };
            var upperUsers = users.Select(user => user.ToUpper());
            Console.WriteLine($"Upper users: {string.Join(", ", upperUsers)}");
            
            // ============ TUPLES IN LAMBDAS (C# 7.0+) ============
            Console.WriteLine("\n=== 5. Tuples in Lambdas ===");
            
            // Lambda with tuple parameters
            Func<(int x, int y), int> tupleAdd = point => point.x + point.y;
            Console.WriteLine($"Tuple add (3, 4): {tupleAdd((3, 4))}");
            
            // Deconstruct tuple in lambda
            Func<(int width, int height), int> area = dim => dim.width * dim.height;
            Console.WriteLine($"Area 5x6: {area((5, 6))}");
            
            // Return tuple from lambda
            Func<int, int, (int sum, int product)> calculate = (a, b) => (a + b, a * b);
            var result = calculate(3, 4);
            Console.WriteLine($"Calculate 3,4: sum={result.sum}, product={result.product}");
        }
        
        static void DemonstrateVariableCaptureAndClosures()
        {
            Console.WriteLine("\n============ VARIABLE CAPTURE AND CLOSURES ============\n");
            
            // ============ VARIABLE CAPTURE BASICS ============
            Console.WriteLine("=== 1. Variable Capture Basics ===");
            
            int multiplier = 2;
            
            // Lambda captures local variable 'multiplier'
            Func<int, int> multiply = x => x * multiplier;
            
            Console.WriteLine($"Multiply 5 (multiplier=2): {multiply(5)}");
            
            // Changing captured variable affects lambda
            multiplier = 3;
            Console.WriteLine($"Multiply 5 (multiplier=3): {multiply(5)}");
            
            // ============ CLOSURE BEHAVIOR ============
            Console.WriteLine("\n=== 2. Closure Behavior ===");
            
            List<Func<int>> functions = new List<Func<int>>();
            
            for (int i = 0; i < 3; i++)
            {
                // Captures variable 'i' - but be careful!
                functions.Add(() => i);
            }
            
            Console.WriteLine("Loop capture (common pitfall):");
            foreach (var func in functions)
            {
                Console.WriteLine($"  Function result: {func()}"); // All print 3!
            }
            
            // ============ FIXING LOOP CAPTURE ============
            Console.WriteLine("\n=== 3. Fixing Loop Capture ===");
            
            List<Func<int>> fixedFunctions = new List<Func<int>>();
            
            for (int i = 0; i < 3; i++)
            {
                int current = i; // Local copy for each iteration
                fixedFunctions.Add(() => current);
            }
            
            Console.WriteLine("Fixed loop capture:");
            foreach (var func in fixedFunctions)
            {
                Console.WriteLine($"  Function result: {func()}"); // 0, 1, 2
            }
            
            // ============ CAPTURED VARIABLE LIFETIME ============
            Console.WriteLine("\n=== 4. Captured Variable Lifetime ===");
            
            Func<Func<int>> createCounter = () =>
            {
                int count = 0;
                return () => ++count;
            };
            
            var counter1 = createCounter();
            var counter2 = createCounter();
            
            Console.WriteLine("Independent closures:");
            Console.WriteLine($"Counter1: {counter1()}, {counter1()}, {counter1()}");
            Console.WriteLine($"Counter2: {counter2()}, {counter2()}");
            
            // ============ CAPTURING DIFFERENT VARIABLE TYPES ============
            Console.WriteLine("\n=== 5. Capturing Different Variable Types ===");
            
            // Capturing value types
            int value = 10;
            Func<int> getValue = () => value;
            value = 20;
            Console.WriteLine($"Captured value type: {getValue()}"); // 20
            
            // Capturing reference types
            List<string> list = new List<string> { "a", "b" };
            Func<int> getCount = () => list.Count;
            list.Add("c");
            Console.WriteLine($"Captured reference type: {getCount()}"); // 3
            
            // Capturing 'this' (instance members)
            var processor = new DataProcessor(100);
            Func<int> process = () => processor.Process();
            Console.WriteLine($"Capturing instance: {process()}");
            
            // ============ CLOSURE IMPLEMENTATION DETAILS ============
            Console.WriteLine("\n=== 6. Closure Implementation Details ===");
            
            Console.WriteLine("""
                How closures work:
                • Captured variables are promoted to heap-allocated objects
                • Compiler generates closure classes
                • Each closure instance has its own state
                • Variables are shared by all lambdas capturing them
                
                Performance considerations:
                • Closures have allocation overhead
                • May affect garbage collection
                • Generally fine for most use cases
                • Avoid in performance-critical loops
                """);
            
            // ============ REAL-WORLD CLOSURE PATTERNS ============
            Console.WriteLine("\n=== 7. Real-world Closure Patterns ===");
            
            // Factory pattern with configuration
            Func<string, Func<string>> createGreeter = greeting =>
            {
                return name => $"{greeting}, {name}!";
            };
            
            var helloGreeter = createGreeter("Hello");
            var heyGreeter = createGreeter("Hey");
            
            Console.WriteLine($"Hello greeter: {helloGreeter("Alice")}");
            Console.WriteLine($"Hey greeter: {heyGreeter("Bob")}");
            
            // Configuration closure
            Func<int, Func<int, int>> createCalculator = baseValue =>
            {
                return x => x + baseValue;
            };
            
            var addFive = createCalculator(5);
            var addTen = createCalculator(10);
            
            Console.WriteLine($"Add five to 3: {addFive(3)}");
            Console.WriteLine($"Add ten to 3: {addTen(3)}");
        }
        
        static void DemonstrateLambdasWithLinq()
        {
            Console.WriteLine("\n============ LAMBDAS WITH LINQ ============\n");
            
            // ============ BASIC LINQ WITH LAMBDAS ============
            Console.WriteLine("=== 1. Basic LINQ with Lambdas ===");
            
            var numbers = Enumerable.Range(1, 20);
            
            // Where with lambda
            var evens = numbers.Where(n => n % 2 == 0);
            Console.WriteLine($"Evens: {string.Join(", ", evens.Take(5))}...");
            
            // Select with lambda
            var squares = numbers.Select(n => n * n);
            Console.WriteLine($"Squares: {string.Join(", ", squares.Take(5))}...");
            
            // OrderBy with lambda
            var ordered = numbers.OrderBy(n => -n); // Descending
            Console.WriteLine($"Ordered descending: {string.Join(", ", ordered.Take(5))}...");
            
            // ============ COMPLEX LINQ OPERATIONS ============
            Console.WriteLine("\n=== 2. Complex LINQ Operations ===");
            
            var people = new List<Person>
            {
                new Person("Alice", 30),
                new Person("Bob", 25),
                new Person("Charlie", 35),
                new Person("Diana", 28),
                new Person("Eve", 40)
            };
            
            // Multiple operations
            var result = people
                .Where(p => p.Age > 25)
                .OrderBy(p => p.Name)
                .Select(p => $"{p.Name} ({p.Age})")
                .ToList();
            
            Console.WriteLine("People over 25:");
            foreach (var person in result)
                Console.WriteLine($"  {person}");
            
            // GroupBy with lambda
            var ageGroups = people
                .GroupBy(p => p.Age / 10) // Group by decade
                .OrderBy(g => g.Key);
            
            Console.WriteLine("\nAge groups by decade:");
            foreach (var group in ageGroups)
            {
                Console.WriteLine($"  {group.Key * 10}s: {string.Join(", ", group.Select(p => p.Name))}");
            }
            
            // ============ AGGREGATE OPERATIONS ============
            Console.WriteLine("\n=== 3. Aggregate Operations ===");
            
            // Sum with lambda
            int totalAge = people.Sum(p => p.Age);
            Console.WriteLine($"Total age: {totalAge}");
            
            // Average with lambda
            double averageAge = people.Average(p => p.Age);
            Console.WriteLine($"Average age: {averageAge:F1}");
            
            // Max/Min with lambda
            int maxAge = people.Max(p => p.Age);
            int minAge = people.Min(p => p.Age);
            Console.WriteLine($"Age range: {minAge}-{maxAge}");
            
            // Aggregate with lambda
            string allNames = people.Aggregate("", (current, p) => 
                current + (current == "" ? "" : ", ") + p.Name);
            Console.WriteLine($"All names: {allNames}");
            
            // ============ QUERY SYNTAX VS METHOD SYNTAX ============
            Console.WriteLine("\n=== 4. Query Syntax vs Method Syntax ===");
            
            // Query syntax (SQL-like)
            var querySyntax = from p in people
                            where p.Age > 30
                            orderby p.Name descending
                            select p.Name;
            
            // Method syntax (lambda-based)
            var methodSyntax = people
                .Where(p => p.Age > 30)
                .OrderByDescending(p => p.Name)
                .Select(p => p.Name);
            
            Console.WriteLine("People over 30 (both syntaxes produce same result):");
            Console.WriteLine($"  Query syntax: {string.Join(", ", querySyntax)}");
            Console.WriteLine($"  Method syntax: {string.Join(", ", methodSyntax)}");
            
            // ============ CUSTOM LINQ OPERATORS ============
            Console.WriteLine("\n=== 5. Custom LINQ Operators ===");
            
            // Custom Where with index
            var indexed = people.Where((p, index) => index % 2 == 0);
            Console.WriteLine("Every other person:");
            foreach (var person in indexed)
                Console.WriteLine($"  {person.Name}");
            
            // Select with index
            var indexedNames = people.Select((p, index) => $"{index}: {p.Name}");
            Console.WriteLine("\nIndexed names:");
            foreach (var name in indexedNames)
                Console.WriteLine($"  {name}");
            
            // ============ PERFORMANCE CONSIDERATIONS ============
            Console.WriteLine("\n=== 6. Performance Considerations ===");
            
            Console.WriteLine("""
                LINQ with lambdas performance tips:
                
                1. Deferred execution:
                   • Queries aren't executed until enumerated
                   • Allows query composition
                   • Be mindful of multiple enumerations
                
                2. Materialization:
                   • Use .ToList() or .ToArray() to cache results
                   • Prevents re-execution of expensive operations
                
                3. N+1 queries:
                   • Avoid querying inside loops
                   • Use joins or Include() in EF
                
                4. Lambda allocation:
                   • Lambdas create delegate instances
                   • Can cause GC pressure in tight loops
                   • Consider static lambdas (C# 9.0+)
                """);
        }
        
        static void DemonstrateLambdasWithDelegates()
        {
            Console.WriteLine("\n============ LAMBDAS WITH DELEGATES ============\n");
            
            // ============ LAMBDA TO DELEGATE CONVERSION ============
            Console.WriteLine("=== 1. Lambda to Delegate Conversion ===");
            
            // Implicit conversion to delegate
            Action<string> log = message => Console.WriteLine($"[LOG] {DateTime.Now:HH:mm:ss} {message}");
            log("Application started");
            
            // Func delegate with lambda
            Func<int, int, int> add = (a, b) => a + b;
            Console.WriteLine($"Add 5 + 3: {add(5, 3)}");
            
            // Predicate delegate with lambda
            Predicate<int> isEven = x => x % 2 == 0;
            Console.WriteLine($"Is 42 even? {isEven(42)}");
            
            // Comparison delegate with lambda
            Comparison<string> lengthCompare = (s1, s2) => s1.Length.CompareTo(s2.Length);
            Console.WriteLine($"Compare 'hello' and 'hi': {lengthCompare("hello", "hi")}");
            
            // ============ MULTICAST DELEGATES WITH LAMBDAS ============
            Console.WriteLine("\n=== 2. Multicast Delegates with Lambdas ===");
            
            Action<string> multiLog = null;
            
            // Add multiple lambdas
            multiLog += msg => Console.WriteLine($"[INFO] {msg}");
            multiLog += msg => Console.WriteLine($"[DEBUG] {msg}");
            multiLog += msg => Console.WriteLine($"[AUDIT] {msg}");
            
            Console.WriteLine("Multicast delegate invocation:");
            multiLog("Processing complete");
            
            // Remove a lambda (need reference)
            Action<string> debugLog = msg => Console.WriteLine($"[DEBUG] {msg}");
            multiLog += debugLog;
            multiLog -= debugLog;
            
            // ============ DELEGATE COVARIANCE/CONTRAVARIANCE ============
            Console.WriteLine("\n=== 3. Delegate Covariance/Contravariance ===");
            
            // Contravariance in input parameters
            Action<object> broadAction = obj => Console.WriteLine($"Object: {obj}");
            Action<string> specificAction = broadAction; // Contravariant
            specificAction("Hello");
            
            // Covariance in return type
            Func<string> specificFunc = () => "Hello";
            Func<object> broadFunc = specificFunc; // Covariant
            Console.WriteLine($"Broad func: {broadFunc()}");
            
            // ============ CUSTOM DELEGATES WITH LAMBDAS ============
            Console.WriteLine("\n=== 4. Custom Delegates with Lambdas ===");
            
            // Custom delegate type
            delegate int MathOperation(int x, int y);
            
            MathOperation customAdd = (x, y) => x + y;
            MathOperation customMultiply = (x, y) => x * y;
            
            Console.WriteLine($"Custom add: {customAdd(5, 3)}");
            Console.WriteLine($"Custom multiply: {customMultiply(5, 3)}");
            
            // Generic custom delegate
            delegate T Transformer<T>(T input);
            
            Transformer<int> doubleIt = x => x * 2;
            Transformer<string> reverseIt = s => new string(s.Reverse().ToArray());
            
            Console.WriteLine($"Double 21: {doubleIt(21)}");
            Console.WriteLine($"Reverse 'hello': {reverseIt("hello")}");
            
            // ============ DELEGATE COMBINATION ============
            Console.WriteLine("\n=== 5. Delegate Combination ===");
            
            Func<int, int> increment = x => x + 1;
            Func<int, int> square = x => x * x;
            
            // Compose functions manually
            Func<int, int> incrementThenSquare = x => square(increment(x));
            Console.WriteLine($"Increment then square 5: {incrementThenSquare(5)}");
            
            // Using function composition
            Func<int, int> squareThenIncrement = x => increment(square(x));
            Console.WriteLine($"Square then increment 5: {squareThenIncrement(5)}");
            
            // ============ REAL-WORLD DELEGATE PATTERNS ============
            Console.WriteLine("\n=== 6. Real-world Delegate Patterns ===");
            
            // Strategy pattern
            Func<Order, decimal> regularShipping = order => 5.00m;
            Func<Order, decimal> expressShipping = order => 15.00m;
            Func<Order, decimal> freeShipping = order => 0m;
            
            var order = new Order { Total = 100.00m };
            
            Console.WriteLine("Shipping costs:");
            Console.WriteLine($"  Regular: {regularShipping(order):C}");
            Console.WriteLine($"  Express: {expressShipping(order):C}");
            Console.WriteLine($"  Free: {freeShipping(order):C}");
            
            // Command pattern
            Action[] commands = new Action[]
            {
                () => Console.WriteLine("Command 1 executed"),
                () => Console.WriteLine("Command 2 executed"),
                () => Console.WriteLine("Command 3 executed")
            };
            
            Console.WriteLine("\nExecuting commands:");
            foreach (var command in commands)
                command();
            
            // Factory pattern
            Func<string, Func<string>> messageFactory = prefix => 
                name => $"{prefix}, {name}!";
            
            var helloFactory = messageFactory("Hello");
            var welcomeFactory = messageFactory("Welcome");
            
            Console.WriteLine($"\nHello factory: {helloFactory("Alice")}");
            Console.WriteLine($"Welcome factory: {welcomeFactory("Bob")}");
        }
        
        static void DemonstrateLambdasWithEvents()
        {
            Console.WriteLine("\n============ LAMBDAS WITH EVENTS ============\n");
            
            // ============ EVENT SUBSCRIPTION WITH LAMBDAS ============
            Console.WriteLine("=== 1. Event Subscription with Lambdas ===");
            
            class Button
            {
                public event EventHandler Clicked;
                
                public void OnClick()
                {
                    Clicked?.Invoke(this, EventArgs.Empty);
                }
            }
            
            Button button = new Button();
            
            // Subscribe with lambda
            button.Clicked += (sender, e) => 
                Console.WriteLine("Button clicked (lambda)");
            
            // Subscribe with anonymous method
            button.Clicked += delegate (object sender, EventArgs e)
            {
                Console.WriteLine("Button clicked (anonymous method)");
            };
            
            Console.WriteLine("Clicking button:");
            button.OnClick();
            
            // ============ LAMBDA CAPTURE IN EVENTS ============
            Console.WriteLine("\n=== 2. Lambda Capture in Events ===");
            
            class TemperatureSensor
            {
                public event EventHandler<double> TemperatureChanged;
                
                private double currentTemp;
                public double Temperature
                {
                    get => currentTemp;
                    set
                    {
                        if (currentTemp != value)
                        {
                            currentTemp = value;
                            TemperatureChanged?.Invoke(this, value);
                        }
                    }
                }
            }
            
            TemperatureSensor sensor = new TemperatureSensor();
            double previousTemp = 20.0;
            
            // Lambda captures local variable
            sensor.TemperatureChanged += (sender, newTemp) =>
            {
                Console.WriteLine($"Temperature changed from {previousTemp}°C to {newTemp}°C");
                previousTemp = newTemp;
            };
            
            Console.WriteLine("Changing temperature:");
            sensor.Temperature = 22.5;
            sensor.Temperature = 25.0;
            sensor.Temperature = 23.0;
            
            // ============ EVENT UNSUBSCRIPTION ISSUES ============
            Console.WriteLine("\n=== 3. Event Unsubscription Issues ===");
            
            // Cannot unsubscribe anonymous lambda without reference
            EventHandler<double> handler = (sender, temp) => 
                Console.WriteLine($"Handler: {temp}°C");
            
            sensor.TemperatureChanged += handler;
            Console.WriteLine("\nWith named handler:");
            sensor.Temperature = 30.0;
            
            sensor.TemperatureChanged -= handler;
            Console.WriteLine("After removing handler:");
            sensor.Temperature = 35.0;
            
            // ============ MULTIPLE EVENT HANDLERS ============
            Console.WriteLine("\n=== 4. Multiple Event Handlers ===");
            
            var eventSource = new EventSource();
            
            // Add multiple lambda handlers
            for (int i = 0; i < 3; i++)
            {
                int id = i; // Capture current value
                eventSource.EventOccurred += (sender, e) =>
                    Console.WriteLine($"Handler {id} received event");
            }
            
            Console.WriteLine("Multiple handlers:");
            eventSource.RaiseEvent();
            
            // ============ EVENT FILTERING WITH LAMBDAS ============
            Console.WriteLine("\n=== 5. Event Filtering with Lambdas ===");
            
            class DataProcessor
            {
                public event EventHandler<DataEventArgs> DataProcessed;
                
                public void ProcessData(string data)
                {
                    Console.WriteLine($"Processing: {data}");
                    DataProcessed?.Invoke(this, new DataEventArgs(data));
                }
            }
            
            DataProcessor processor = new DataProcessor();
            
            // Filter events with lambda
            processor.DataProcessed += (sender, e) =>
            {
                if (e.Data.Length > 5)
                    Console.WriteLine($"  Long data processed: {e.Data}");
            };
            
            processor.DataProcessed += (sender, e) =>
            {
                if (e.Data.Contains("error", StringComparison.OrdinalIgnoreCase))
                    Console.WriteLine($"  Error data detected: {e.Data}");
            };
            
            Console.WriteLine("Processing data with filters:");
            processor.ProcessData("Hello");
            processor.ProcessData("Hello World");
            processor.ProcessData("Error occurred");
            
            // ============ ASYNC EVENT HANDLERS ============
            Console.WriteLine("\n=== 6. Async Event Handlers ===");
            
            class AsyncEventSource
            {
                public event EventHandler<EventArgs> AsyncEvent;
                
                public async Task RaiseEventAsync()
                {
                    Console.WriteLine("Raising async event...");
                    AsyncEvent?.Invoke(this, EventArgs.Empty);
                    await Task.Delay(100);
                }
            }
            
            AsyncEventSource asyncSource = new AsyncEventSource();
            
            asyncSource.AsyncEvent += async (sender, e) =>
            {
                await Task.Delay(50);
                Console.WriteLine("Async handler completed");
            };
            
            Console.WriteLine("Async event handling:");
            await asyncSource.RaiseEventAsync();
        }
        
        static void DemonstratePerformanceConsiderations()
        {
            Console.WriteLine("\n============ PERFORMANCE CONSIDERATIONS ============\n");
            
            // ============ LAMBDA ALLOCATION OVERHEAD ============
            Console.WriteLine("=== 1. Lambda Allocation Overhead ===");
            
            Console.WriteLine("""
                Lambda expressions create:
                • Delegate instances (heap allocation)
                • Closure objects (if capturing variables)
                • Potential GC pressure in tight loops
                
                Example allocations:
                """);
            
            // Each lambda creates a new delegate instance
            Func<int, int>[] functions = new Func<int, int>[1000];
            
            for (int i = 0; i < functions.Length; i++)
            {
                functions[i] = x => x * i; // Creates 1000 delegate instances
            }
            
            Console.WriteLine($"Created {functions.Length} lambda delegates");
            
            // ============ STATIC LAMBDAS (C# 9.0+) ============
            Console.WriteLine("\n=== 2. Static Lambdas (C# 9.0+) ===");
            
            // Static lambda doesn't capture 'this' or local variables
            var staticLambda = static (int x) => x * x;
            
            // Can't capture instance or local variables
            // int factor = 2;
            // var invalid = static (int x) => x * factor; // Error
            
            Console.WriteLine("Static lambda advantages:");
            Console.WriteLine("  • No closure allocation");
            Console.WriteLine("  • Can be cached as static field");
            Console.WriteLine("  • Better performance in hot paths");
            
            // ============ LAMBDA CACHING PATTERNS ============
            Console.WriteLine("\n=== 3. Lambda Caching Patterns ===");
            
            // Cache frequently used lambdas
            static readonly Func<int, int, int> cachedAdd = (x, y) => x + y;
            static readonly Func<string, string> cachedUpper = s => s.ToUpper();
            
            Console.WriteLine("Cached lambda usage:");
            Console.WriteLine($"  Cached add: {cachedAdd(5, 3)}");
            Console.WriteLine($"  Cached upper: {cachedUpper("test")}");
            
            // Factory for reusable lambdas
            Func<int, Func<int, int>> createMultiplier = null;
            createMultiplier = factor => 
            {
                // Cache created multipliers
                var cache = new Dictionary<int, Func<int, int>>();
                return f =>
                {
                    if (!cache.TryGetValue(factor, out var multiplier))
                    {
                        multiplier = x => x * factor;
                        cache[factor] = multiplier;
                    }
                    return multiplier(f);
                };
            };
            
            // ============ LINQ PERFORMANCE ============
            Console.WriteLine("\n=== 4. LINQ Performance ===");
            
            var data = Enumerable.Range(1, 10000).ToList();
            
            // Inefficient: multiple enumerations
            var inefficient = data.Where(x => x % 2 == 0)
                                 .Where(x => x > 1000)
                                 .Select(x => x * 2)
                                 .ToList();
            
            // More efficient: combined conditions
            var efficient = data.Where(x => x % 2 == 0 && x > 1000)
                               .Select(x => x * 2)
                               .ToList();
            
            Console.WriteLine($"Inefficient count: {inefficient.Count}");
            Console.WriteLine($"Efficient count: {efficient.Count}");
            
            // ============ BENCHMARK COMPARISON ============
            Console.WriteLine("\n=== 5. Benchmark Comparison ===");
            
            Console.WriteLine("""
                Performance tips:
                
                1. Avoid lambda allocations in loops:
                   Bad: for(...) items.Where(x => x > threshold)
                   Good: var predicate = (int x) => x > threshold;
                         for(...) items.Where(predicate)
                
                2. Use static lambdas when possible
                
                3. Cache delegate instances
                
                4. Combine LINQ operations
                
                5. Consider manual loops for performance-critical code
                
                6. Profile before optimizing!
                """);
        }
        
        static void DemonstrateFunctionalPatterns()
        {
            Console.WriteLine("\n============ FUNCTIONAL PROGRAMMING PATTERNS ============\n");
            
            // ============ HIGHER-ORDER FUNCTIONS ============
            Console.WriteLine("=== 1. Higher-Order Functions ===");
            
            // Function that takes a function as parameter
            List<int> TransformList(List<int> list, Func<int, int> transformer)
            {
                var result = new List<int>();
                foreach (var item in list)
                    result.Add(transformer(item));
                return result;
            }
            
            var numbers = new List<int> { 1, 2, 3, 4, 5 };
            
            var doubled = TransformList(numbers, x => x * 2);
            var squared = TransformList(numbers, x => x * x);
            
            Console.WriteLine($"Original: {string.Join(", ", numbers)}");
            Console.WriteLine($"Doubled: {string.Join(", ", doubled)}");
            Console.WriteLine($"Squared: {string.Join(", ", squared)}");
            
            // Function that returns a function
            Func<int, Func<int, int>> CreateMultiplier()
            {
                return factor => x => x * factor;
            }
            
            var multiplyBy3 = CreateMultiplier()(3);
            Console.WriteLine($"Multiply 5 by 3: {multiplyBy3(5)}");
            
            // ============ FUNCTION COMPOSITION ============
            Console.WriteLine("\n=== 2. Function Composition ===");
            
            // Compose two functions: f(g(x))
            Func<Func<A, B>, Func<B, C>, Func<A, C>> Compose<A, B, C> = 
                (f, g) => x => g(f(x));
            
            Func<int, int> addOne = x => x + 1;
            Func<int, int> square = x => x * x;
            
            var addOneThenSquare = Compose(addOne, square);
            Console.WriteLine($"Add one then square 5: {addOneThenSquare(5)}");
            
            // Multiple composition
            Func<int, string> toString = x => x.ToString();
            var pipeline = Compose(addOneThenSquare, toString);
            Console.WriteLine($"Pipeline result: {pipeline(5)}");
            
            // ============ CURRYING AND PARTIAL APPLICATION ============
            Console.WriteLine("\n=== 3. Currying and Partial Application ===");
            
            // Curry a function: f(x, y) -> f(x)(y)
            Func<int, Func<int, int>> CurriedAdd = x => y => x + y;
            
            var addFive = CurriedAdd(5);
            Console.WriteLine($"Add five to 3: {addFive(3)}");
            
            // Partial application
            Func<int, int, int, int> AddThreeNumbers = (a, b, c) => a + b + c;
            
            // Partially apply first argument
            Func<int, int, int> AddToTen = (b, c) => AddThreeNumbers(10, b, c);
            Console.WriteLine($"Add to ten: 5 + 7 = {AddToTen(5, 7)}");
            
            // ============ IMMUTABILITY AND PURE FUNCTIONS ============
            Console.WriteLine("\n=== 4. Immutability and Pure Functions ===");
            
            // Pure function: no side effects, same input -> same output
            Func<int, int, int> PureAdd = (x, y) => x + y;
            
            // Impure function: has side effects
            int total = 0;
            Action<int> ImpureAdd = x => total += x;
            
            Console.WriteLine($"Pure add 3 + 4: {PureAdd(3, 4)}");
            ImpureAdd(3);
            ImpureAdd(4);
            Console.WriteLine($"Impure add result: {total}");
            
            // ============ MONAD PATTERNS WITH LAMBDAS ============
            Console.WriteLine("\n=== 5. Monad Patterns with Lambdas ===");
            
            // Maybe/Option monad pattern
            class Maybe<T>
            {
                private readonly T value;
                private readonly bool hasValue;
                
                private Maybe(T value, bool hasValue)
                {
                    this.value = value;
                    this.hasValue = hasValue;
                }
                
                public static Maybe<T> Some(T value) => new Maybe<T>(value, true);
                public static Maybe<T> None() => new Maybe<T>(default, false);
                
                public Maybe<U> Bind<U>(Func<T, Maybe<U>> func)
                {
                    return hasValue ? func(value) : Maybe<U>.None();
                }
                
                public override string ToString() => 
                    hasValue ? $"Some({value})" : "None";
            }
            
            Maybe<int> maybeFive = Maybe<int>.Some(5);
            Maybe<int> maybeNone = Maybe<int>.None();
            
            Func<int, Maybe<int>> addOneMaybe = x => Maybe<int>.Some(x + 1);
            Func<int, Maybe<int>> squareMaybe = x => Maybe<int>.Some(x * x);
            
            var result1 = maybeFive.Bind(addOneMaybe).Bind(squareMaybe);
            var result2 = maybeNone.Bind(addOneMaybe).Bind(squareMaybe);
            
            Console.WriteLine($"Maybe chain (Some 5): {result1}");
            Console.WriteLine($"Maybe chain (None): {result2}");
            
            // ============ FUNCTIONAL DATA TRANSFORMATIONS ============
            Console.WriteLine("\n=== 6. Functional Data Transformations ===");
            
            // Map, Filter, Reduce pattern
            var data = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
            
            // Map (Select)
            var mapped = data.Select(x => x * 2);
            
            // Filter (Where)
            var filtered = mapped.Where(x => x % 3 == 0);
            
            // Reduce (Aggregate)
            var reduced = filtered.Aggregate(0, (acc, x) => acc + x);
            
            Console.WriteLine($"Data: {string.Join(", ", data)}");
            Console.WriteLine($"Mapped (x2): {string.Join(", ", mapped)}");
            Console.WriteLine($"Filtered (divisible by 3): {string.Join(", ", filtered)}");
            Console.WriteLine($"Reduced (sum): {reduced}");
            
            // Pipeline all operations
            var pipelineResult = data
                .Select(x => x * 2)
                .Where(x => x % 3 == 0)
                .Aggregate(0, (acc, x) => acc + x);
            
            Console.WriteLine($"Pipeline result: {pipelineResult}");
        }
        
        static void DemonstrateRealWorldPatterns()
        {
            Console.WriteLine("\n============ REAL-WORLD PATTERNS ============\n");
            
            // ============ DEPENDENCY INJECTION WITH LAMBDAS ============
            Console.WriteLine("=== 1. Dependency Injection with Lambdas ===");
            
            // Factory method using lambda
            Func<ILogger> createLogger = () => new ConsoleLogger();
            Func<IDatabase> createDatabase = () => new SqlDatabase();
            
            var service = new UserService(createLogger(), createDatabase());
            Console.WriteLine("Service created with lambda factories");
            
            // Configuration with lambda
            var config = new ServiceConfiguration()
                .WithLogger(() => new FileLogger("app.log"))
                .WithDatabase(() => new InMemoryDatabase());
            
            // ============ MIDDLEWARE PIPELINE ============
            Console.WriteLine("\n=== 2. Middleware Pipeline ===");
            
            // Request/response with middleware
            Func<Request, Response> pipeline = request =>
            {
                Console.WriteLine($"Processing request: {request.Path}");
                return new Response { StatusCode = 200, Body = "Hello" };
            };
            
            // Add middleware with lambda
            Func<Func<Request, Response>, Func<Request, Response>> AddLogging = 
                next => request =>
                {
                    Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Starting request");
                    var response = next(request);
                    Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] Completed request");
                    return response;
                };
            
            Func<Func<Request, Response>, Func<Request, Response>> AddAuth = 
                next => request =>
                {
                    if (request.Headers.ContainsKey("Authorization"))
                        return next(request);
                    else
                        return new Response { StatusCode = 401, Body = "Unauthorized" };
                };
            
            // Compose middleware
            var app = AddLogging(AddAuth(pipeline));
            app(new Request { Path = "/api/test", Headers = new() });
            
            // ============ CACHING WITH LAMBDAS ============
            Console.WriteLine("\n=== 3. Caching with Lambdas ===");
            
            // Memoization pattern
            Func<T, R> Memoize<T, R>(Func<T, R> func) where T : notnull
            {
                var cache = new Dictionary<T, R>();
                return arg =>
                {
                    if (!cache.TryGetValue(arg, out var result))
                    {
                        result = func(arg);
                        cache[arg] = result;
                    }
                    return result;
                };
            }
            
            // Expensive calculation
            Func<int, int> ExpensiveCalculation = n =>
            {
                Console.WriteLine($"  Calculating for {n}...");
                Thread.Sleep(100); // Simulate work
                return n * n;
            };
            
            var memoized = Memoize(ExpensiveCalculation);
            
            Console.WriteLine("Memoization test:");
            Console.WriteLine($"  First call (5): {memoized(5)}");
            Console.WriteLine($"  Second call (5): {memoized(5)}");
            Console.WriteLine($"  First call (10): {memoized(10)}");
            Console.WriteLine($"  Second call (10): {memoized(10)}");
            
            // ============ RETRY PATTERN ============
            Console.WriteLine("\n=== 4. Retry Pattern ===");
            
            Func<T> Retry<T>(Func<T> operation, int maxRetries)
            {
                for (int i = 0; i < maxRetries; i++)
                {
                    try
                    {
                        return operation();
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"  Attempt {i + 1} failed: {ex.Message}");
                        if (i == maxRetries - 1) throw;
                        Thread.Sleep(100 * (i + 1));
                    }
                }
                throw new InvalidOperationException("Should not reach here");
            }
            
            int attempt = 0;
            Func<int> UnreliableOperation = () =>
            {
                attempt++;
                if (attempt < 3)
                    throw new Exception($"Attempt {attempt} failed");
                return 42;
            };
            
            Console.WriteLine("Retry pattern:");
            try
            {
                var result = Retry(UnreliableOperation, 3);
                Console.WriteLine($"  Success: {result}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"  Final failure: {ex.Message}");
            }
            
            // ============ EVENT SOURCING PATTERNS ============
            Console.WriteLine("\n=== 5. Event Sourcing Patterns ===");
            
            // Command handler with lambda
            Func<Command, Event> HandleCreateUser = command =>
            {
                Console.WriteLine($"  Creating user: {command.Data}");
                return new Event($"UserCreated:{command.Data}");
            };
            
            Func<Command, Event> HandleUpdateUser = command =>
            {
                Console.WriteLine($"  Updating user: {command.Data}");
                return new Event($"UserUpdated:{command.Data}");
            };
            
            // Command dispatcher
            var handlers = new Dictionary<string, Func<Command, Event>>
            {
                ["CreateUser"] = HandleCreateUser,
                ["UpdateUser"] = HandleUpdateUser
            };
            
            Console.WriteLine("Event sourcing commands:");
            foreach (var cmd in new[] { "CreateUser", "UpdateUser", "InvalidCommand" })
            {
                if (handlers.TryGetValue(cmd, out var handler))
                {
                    var evt = handler(new Command { Data = "test" });
                    Console.WriteLine($"  {cmd}: {evt.Type}");
                }
                else
                {
                    Console.WriteLine($"  No handler for: {cmd}");
                }
            }
            
            // ============ SUMMARY ============
            Console.WriteLine("\n=== 6. Summary ===");
            Console.WriteLine("""
                Lambda expressions are powerful tools in C#:
                
                Key Takeaways:
                1. Use for concise anonymous methods
                2. Enable functional programming patterns
                3. Essential for LINQ and event handling
                4. Be mindful of performance and closures
                5. Follow best practices for maintainability
                
                Best Practices:
                • Use meaningful parameter names
                • Keep lambdas short and focused
                • Avoid complex logic in lambdas
                • Consider static lambdas when possible
                • Cache frequently used delegates
                • Document non-obvious closures
                
                Advanced Patterns:
                • Higher-order functions
                • Function composition
                • Currying and partial application
                • Memoization and caching
                • Middleware pipelines
                • Command/event patterns
                """);
        }
    }
    
    // Supporting classes
    class Person
    {
        public string Name { get; }
        public int Age { get; }
        
        public Person(string name, int age)
        {
            Name = name;
            Age = age;
        }
    }
    
    class DataProcessor
    {
        private int baseValue;
        
        public DataProcessor(int baseValue)
        {
            this.baseValue = baseValue;
        }
        
        public int Process()
        {
            return baseValue * 2;
        }
    }
    
    class Order
    {
        public decimal Total { get; set; }
    }
    
    class EventSource
    {
        public event EventHandler EventOccurred;
        
        public void RaiseEvent()
        {
            EventOccurred?.Invoke(this, EventArgs.Empty);
        }
    }
    
    class DataEventArgs : EventArgs
    {
        public string Data { get; }
        
        public DataEventArgs(string data)
        {
            Data = data;
        }
    }
    
    // Interface definitions for DI example
    interface ILogger { }
    interface IDatabase { }
    class ConsoleLogger : ILogger { }
    class FileLogger : ILogger 
    { 
        public FileLogger(string path) { }
    }
    class SqlDatabase : IDatabase { }
    class InMemoryDatabase : IDatabase { }
    class UserService
    {
        public UserService(ILogger logger, IDatabase database) { }
    }
    
    class ServiceConfiguration
    {
        public ServiceConfiguration WithLogger(Func<ILogger> factory) => this;
        public ServiceConfiguration WithDatabase(Func<IDatabase> factory) => this;
    }
    
    class Request
    {
        public string Path { get; set; }
        public Dictionary<string, string> Headers { get; set; } = new();
    }
    
    class Response
    {
        public int StatusCode { get; set; }
        public string Body { get; set; }
    }
    
    class Command
    {
        public string Data { get; set; }
    }
    
    class Event
    {
        public string Type { get; }
        
        public Event(string type)
        {
            Type = type;
        }
    }
}