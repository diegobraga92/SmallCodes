/*
    C# METHODS AND FUNCTIONS
    Covering: Method declaration, parameters, return types, overloading, local functions
    
    This file demonstrates methods and functions in C# programming.
*/

using System;

namespace CSharpRefresher.Methods
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Methods and Functions Demonstration ===\n");
            
            DemonstrateMethodBasics();
            DemonstrateParameters();
            DemonstrateReturnTypes();
            DemonstrateMethodOverloading();
            DemonstrateLocalFunctions();
            DemonstrateExtensionMethods();
            DemonstrateLambdaExpressions();
            
            Console.WriteLine("\n=== Methods Complete ===");
        }
        
        static void DemonstrateMethodBasics()
        {
            Console.WriteLine("============ METHOD BASICS ============\n");
            
            // Simple method call
            Console.WriteLine("=== Simple Method Call ===");
            SayHello();
            
            // Method with parameters
            Console.WriteLine("\n=== Method with Parameters ===");
            GreetPerson("Alice");
            GreetPerson("Bob", "Good afternoon");
            
            // Method with return value
            Console.WriteLine("\n=== Method with Return Value ===");
            int sum = Add(5, 3);
            Console.WriteLine($"Add(5, 3) = {sum}");
            
            double product = Multiply(2.5, 4.0);
            Console.WriteLine($"Multiply(2.5, 4.0) = {product}");
            
            // Method calling other methods
            Console.WriteLine("\n=== Method Chaining ===");
            int result = AddThenMultiply(2, 3, 4);
            Console.WriteLine($"AddThenMultiply(2, 3, 4) = {result}");
            
            // Static vs instance methods
            Console.WriteLine("\n=== Static vs Instance Methods ===");
            Calculator calc = new Calculator();
            int staticResult = Calculator.StaticAdd(10, 20);
            int instanceResult = calc.InstanceAdd(10, 20);
            Console.WriteLine($"Static method: {staticResult}");
            Console.WriteLine($"Instance method: {instanceResult}");
            
            // Expression-bodied methods (C# 6+)
            Console.WriteLine("\n=== Expression-bodied Methods ===");
            int quickSum = QuickAdd(7, 8);
            Console.WriteLine($"QuickAdd(7, 8) = {quickSum}");
            
            // Method with optional parameters
            Console.WriteLine("\n=== Optional Parameters ===");
            PrintMessage("Hello");
            PrintMessage("Hello", "World");
            PrintMessage("Hello", "World", "!");
            
            // Named arguments
            Console.WriteLine("\n=== Named Arguments ===");
            CreatePerson(name: "Alice", age: 30);
            CreatePerson(age: 25, name: "Bob"); // Order doesn't matter with named arguments
        }
        
        static void DemonstrateParameters()
        {
            Console.WriteLine("\n============ PARAMETER TYPES ============\n");
            
            // Value parameters (default)
            Console.WriteLine("=== Value Parameters ===");
            int x = 5, y = 10;
            Console.WriteLine($"Before SwapByValue: x={x}, y={y}");
            SwapByValue(x, y);
            Console.WriteLine($"After SwapByValue: x={x}, y={y} (unchanged - copies were swapped)");
            
            // Reference parameters (ref)
            Console.WriteLine("\n=== Reference Parameters (ref) ===");
            Console.WriteLine($"Before SwapByRef: x={x}, y={y}");
            SwapByRef(ref x, ref y);
            Console.WriteLine($"After SwapByRef: x={x}, y={y} (actually swapped)");
            
            // Output parameters (out)
            Console.WriteLine("\n=== Output Parameters (out) ===");
            if (TryParseNumber("42", out int parsedValue))
            {
                Console.WriteLine($"Successfully parsed: {parsedValue}");
            }
            
            // Discard out parameter (C# 7+)
            bool success = TryParseNumber("invalid", out _);
            Console.WriteLine($"Parse 'invalid': {success}");
            
            // Multiple out parameters
            GetMinMax(new[] { 5, 2, 8, 1, 9 }, out int min, out int max);
            Console.WriteLine($"Min: {min}, Max: {max}");
            
            // In parameters (C# 7.2+) - read-only reference
            Console.WriteLine("\n=== In Parameters (read-only reference) ===");
            var largeStruct = new LargeStruct(100);
            ProcessLargeStruct(in largeStruct); // Can't modify largeStruct inside method
            
            // Params parameter (variable number of arguments)
            Console.WriteLine("\n=== Params Parameter ===");
            int total1 = Sum(1, 2, 3);
            int total2 = Sum(4, 5, 6, 7, 8);
            int total3 = Sum(); // Zero arguments
            Console.WriteLine($"Sum(1,2,3) = {total1}");
            Console.WriteLine($"Sum(4,5,6,7,8) = {total2}");
            Console.WriteLine($"Sum() = {total3}");
            
            // Optional parameters with default values
            Console.WriteLine("\n=== Optional Parameters ===");
            ConfigureServer("localhost");
            ConfigureServer("localhost", 8080);
            ConfigureServer("localhost", 8080, true);
            
            // Parameter arrays with other parameters
            Console.WriteLine("\n=== Params with Other Parameters ===");
            LogMessages("System", "Starting up...", "Initializing components...", "Ready");
        }
        
        static void DemonstrateReturnTypes()
        {
            Console.WriteLine("\n============ RETURN TYPES ============\n");
            
            // Void return type
            Console.WriteLine("=== Void Return Type ===");
            PrintTimestamp();
            
            // Value type return
            Console.WriteLine("\n=== Value Type Return ===");
            int factorial = CalculateFactorial(5);
            Console.WriteLine($"5! = {factorial}");
            
            // Reference type return
            Console.WriteLine("\n=== Reference Type Return ===");
            string formatted = FormatName("john", "doe");
            Console.WriteLine($"Formatted name: {formatted}");
            
            // Tuple return (C# 7+)
            Console.WriteLine("\n=== Tuple Return ===");
            var stats = GetStatistics(new[] { 1, 2, 3, 4, 5 });
            Console.WriteLine($"Stats: Sum={stats.sum}, Avg={stats.average}, Count={stats.count}");
            
            // Named tuple elements
            var (min, max) = GetMinMaxTuple(new[] { 5, 2, 8, 1, 9 });
            Console.WriteLine($"Min: {min}, Max: {max}");
            
            // Nullable return type
            Console.WriteLine("\n=== Nullable Return Type ===");
            int? maybeNumber = FindNumber(new[] { 1, 2, 3 }, 2);
            Console.WriteLine($"Found 2: {maybeNumber}");
            
            maybeNumber = FindNumber(new[] { 1, 2, 3 }, 5);
            Console.WriteLine($"Found 5: {(maybeNumber.HasValue ? maybeNumber.Value.ToString() : "null")}");
            
            // Generic return type
            Console.WriteLine("\n=== Generic Return Type ===");
            string firstString = GetFirst(new[] { "A", "B", "C" });
            int firstInt = GetFirst(new[] { 1, 2, 3 });
            Console.WriteLine($"First string: {firstString}");
            Console.WriteLine($"First int: {firstInt}");
            
            // Async return type (demonstrated in async file)
            Console.WriteLine("\n=== Multiple Return Values (out parameters) ===");
            bool divisionSuccess = TryDivide(10, 2, out double quotient);
            Console.WriteLine($"10 / 2: Success={divisionSuccess}, Result={quotient}");
            
            divisionSuccess = TryDivide(10, 0, out quotient);
            Console.WriteLine($"10 / 0: Success={divisionSuccess}, Result={quotient}");
        }
        
        static void DemonstrateMethodOverloading()
        {
            Console.WriteLine("\n============ METHOD OVERLOADING ============\n");
            
            // Overloading by parameter type
            Console.WriteLine("=== Overloading by Parameter Type ===");
            Console.WriteLine($"Add(2, 3) = {Add(2, 3)}");
            Console.WriteLine($"Add(2.5, 3.5) = {Add(2.5, 3.5)}");
            Console.WriteLine($"Add(\"Hello\", \" World\") = \"{Add("Hello", " World")}\"");
            
            // Overloading by parameter count
            Console.WriteLine("\n=== Overloading by Parameter Count ===");
            Console.WriteLine($"Calculate(5) = {Calculate(5)}");
            Console.WriteLine($"Calculate(5, 3) = {Calculate(5, 3)}");
            Console.WriteLine($"Calculate(5, 3, 2) = {Calculate(5, 3, 2)}");
            
            // Overloading by parameter modifiers
            Console.WriteLine("\n=== Overloading by Parameter Modifiers ===");
            int value = 5;
            Process(value);           // Calls Process(int)
            Process(ref value);       // Calls Process(ref int)
            Process(out value);       // Calls Process(out int)
            Process(in value);        // Calls Process(in int) if exists
            
            // Cannot overload by return type only
            // int GetValue() and string GetValue() would cause compile error
            
            // Overloading with optional parameters
            Console.WriteLine("\n=== Overloading with Optional Parameters ===");
            ShowMessage("Hello");                 // Calls ShowMessage(string)
            ShowMessage("Hello", "World");        // Calls ShowMessage(string, string)
            ShowMessage("Hello", "World", "!");   // Calls ShowMessage(string, string, string)
            
            // Ambiguity with optional parameters
            // void Process(int x, int y = 0) and void Process(int x) would be ambiguous
        }
        
        static void DemonstrateLocalFunctions()
        {
            Console.WriteLine("\n============ LOCAL FUNCTIONS ============\n");
            
            // Simple local function
            Console.WriteLine("=== Simple Local Function ===");
            int AddLocal(int a, int b) => a + b;
            Console.WriteLine($"AddLocal(3, 4) = {AddLocal(3, 4)}");
            
            // Local function with closure
            Console.WriteLine("\n=== Local Function with Closure ===");
            int multiplier = 3;
            
            int MultiplyBy(int x)
            {
                return x * multiplier; // Captures multiplier from outer scope
            }
            
            Console.WriteLine($"MultiplyBy(5) = {MultiplyBy(5)}");
            multiplier = 5;
            Console.WriteLine($"After changing multiplier, MultiplyBy(5) = {MultiplyBy(5)}");
            
            // Recursive local function
            Console.WriteLine("\n=== Recursive Local Function ===");
            int Fibonacci(int n)
            {
                if (n <= 1) return n;
                return Fibonacci(n - 1) + Fibonacci(n - 2);
            }
            
            Console.Write("Fibonacci sequence: ");
            for (int i = 0; i < 10; i++)
            {
                Console.Write($"{Fibonacci(i)} ");
            }
            Console.WriteLine();
            
            // Local function in a loop
            Console.WriteLine("\n=== Local Function in Loop ===");
            var functions = new System.Collections.Generic.List<Func<int, int>>();
            
            for (int i = 0; i < 3; i++)
            {
                // Each iteration creates a new local function capturing current i
                int CreateMultiplier(int factor)
                {
                    return factor * i; // Captures i by reference (important!)
                }
                functions.Add(CreateMultiplier);
            }
            
            // All functions use i=3 (the final value after loop)
            Console.WriteLine($"All functions use final i value (3):");
            foreach (var func in functions)
            {
                Console.WriteLine($"  func(2) = {func(2)}"); // All print 6
            }
            
            // Fix: capture loop variable in local variable
            Console.WriteLine("\n=== Fixed: Capture Loop Variable Correctly ===");
            functions.Clear();
            
            for (int i = 0; i < 3; i++)
            {
                int current = i; // Capture current value
                int CreateMultiplierFixed(int factor)
                {
                    return factor * current; // Captures current value
                }
                functions.Add(CreateMultiplierFixed);
            }
            
            Console.WriteLine($"Functions capture different i values:");
            for (int j = 0; j < functions.Count; j++)
            {
                Console.WriteLine($"  functions[{j}](2) = {functions[j](2)}");
            }
            
            // Local static function (C# 8+)
            Console.WriteLine("\n=== Local Static Function ===");
            static int StaticAdd(int a, int b) => a + b;
            Console.WriteLine($"StaticAdd(10, 20) = {StaticAdd(10, 20)}");
            
            // Static local functions cannot capture variables from enclosing scope
            // int outerVar = 5;
            // static int CannotCapture() => outerVar; // ERROR
        }
        
        static void DemonstrateExtensionMethods()
        {
            Console.WriteLine("\n============ EXTENSION METHODS ============\n");
            
            // Using extension methods
            Console.WriteLine("=== Using Extension Methods ===");
            string text = "hello world";
            string capitalized = text.Capitalize();
            Console.WriteLine($"\"{text}\".Capitalize() = \"{capitalized}\"");
            
            int number = 5;
            bool isEven = number.IsEven();
            Console.WriteLine($"{number}.IsEven() = {isEven}");
            
            // Extension method on interface
            Console.WriteLine("\n=== Extension Method on Interface ===");
            var list = new System.Collections.Generic.List<int> { 1, 2, 3, 4, 5 };
            string joined = list.JoinToString(", ");
            Console.WriteLine($"List joined: {joined}");
            
            // Chaining extension methods
            Console.WriteLine("\n=== Chaining Extension Methods ===");
            string result = text.Capitalize().Reverse();
            Console.WriteLine($"\"{text}\".Capitalize().Reverse() = \"{result}\"");
            
            // Extension method with generic type
            Console.WriteLine("\n=== Generic Extension Method ===");
            var stack = new System.Collections.Generic.Stack<int>();
            stack.Push(1);
            stack.Push(2);
            stack.Push(3);
            
            bool hasItems = stack.HasItems();
            Console.WriteLine($"Stack has items: {hasItems}");
            
            // Extension method on value type
            Console.WriteLine("\n=== Extension Method on Value Type ===");
            DateTime date = new DateTime(2024, 1, 15);
            bool isWeekend = date.IsWeekend();
            Console.WriteLine($"{date:yyyy-MM-dd} is weekend: {isWeekend}");
        }
        
        static void DemonstrateLambdaExpressions()
        {
            Console.WriteLine("\n============ LAMBDA EXPRESSIONS ============\n");
            
            // Statement lambda
            Console.WriteLine("=== Statement Lambda ===");
            Action<string> printMessage = (message) =>
            {
                Console.WriteLine($"Message: {message}");
            };
            printMessage("Hello from lambda!");
            
            // Expression lambda
            Console.WriteLine("\n=== Expression Lambda ===");
            Func<int, int, int> multiply = (x, y) => x * y;
            Console.WriteLine($"multiply(5, 3) = {multiply(5, 3)}");
            
            // Lambda with no parameters
            Func<string> getGreeting = () => "Hello, World!";
            Console.WriteLine($"getGreeting() = {getGreeting()}");
            
            // Lambda with explicit parameter types
            Func<double, double, double> divide = (double x, double y) => x / y;
            Console.WriteLine($"divide(10.0, 2.0) = {divide(10.0, 2.0)}");
            
            // Lambda capturing outer variables
            Console.WriteLine("\n=== Lambda Capturing Outer Variables ===");
            int factor = 3;
            Func<int, int> multiplier = x => x * factor;
            Console.WriteLine($"multiplier(5) with factor={factor} = {multiplier(5)}");
            
            factor = 5;
            Console.WriteLine($"multiplier(5) with factor={factor} = {multiplier(5)}");
            
            // Lambda in LINQ
            Console.WriteLine("\n=== Lambda in LINQ ===");
            var numbers = new[] { 1, 2, 3, 4, 5 };
            var evenNumbers = numbers.Where(n => n % 2 == 0);
            Console.WriteLine($"Even numbers: {string.Join(", ", evenNumbers)}");
            
            // Lambda as event handler
            Console.WriteLine("\n=== Lambda as Event Handler ===");
            var button = new Button();
            button.Clicked += (sender, e) => Console.WriteLine("Button clicked!");
            // button.SimulateClick(); // Would trigger the event
            
            // Local function vs lambda
            Console.WriteLine("\n=== Local Function vs Lambda ===");
            // Local function can be recursive
            int LocalFactorial(int n) => n <= 1 ? 1 : n * LocalFactorial(n - 1);
            
            // Lambda cannot reference itself directly (need to assign to variable)
            Func<int, int> factorialLambda = null;
            factorialLambda = n => n <= 1 ? 1 : n * factorialLambda(n - 1);
            
            Console.WriteLine($"LocalFactorial(5) = {LocalFactorial(5)}");
            Console.WriteLine($"factorialLambda(5) = {factorialLambda(5)}");
        }
        
        // ============ HELPER METHODS ============
        
        static void SayHello() => Console.WriteLine("Hello!");
        
        static void GreetPerson(string name, string greeting = "Hello")
        {
            Console.WriteLine($"{greeting}, {name}!");
        }
        
        static int Add(int a, int b) => a + b;
        static double Add(double a, double b) => a + b;
        static string Add(string a, string b) => a + b;
        
        static double Multiply(double a, double b) => a * b;
        
        static int AddThenMultiply(int a, int b, int multiplier)
        {
            int sum = Add(a, b);
            return sum * multiplier;
        }
        
        static void PrintMessage(string first, string second = "World", string third = "!")
        {
            Console.WriteLine($"{first} {second}{third}");
        }
        
        static void CreatePerson(string name, int age)
        {
            Console.WriteLine($"Created person: {name}, {age} years old");
        }
        
        static void SwapByValue(int x, int y)
        {
            int temp = x;
            x = y;
            y = temp;
        }
        
        static void SwapByRef(ref int x, ref int y)
        {
            int temp = x;
            x = y;
            y = temp;
        }
        
        static bool TryParseNumber(string input, out int result)
        {
            return int.TryParse(input, out result);
        }
        
        static void GetMinMax(int[] numbers, out int min, out int max)
        {
            min = numbers.Min();
            max = numbers.Max();
        }
        
        struct LargeStruct
        {
            public int Value;
            public LargeStruct(int value) { Value = value; }
        }
        
        static void ProcessLargeStruct(in LargeStruct large)
        {
            Console.WriteLine($"Processing large struct with value: {large.Value}");
            // large.Value = 10; // ERROR: cannot modify in parameter
        }
        
        static int Sum(params int[] numbers)
        {
            return numbers.Sum();
        }
        
        static void ConfigureServer(string host, int port = 80, bool ssl = false)
        {
            Console.WriteLine($"Server: {host}:{port}, SSL: {ssl}");
        }
        
        static void LogMessages(string category, params string[] messages)
        {
            Console.WriteLine($"[{category}] {string.Join(" | ", messages)}");
        }
        
        static void PrintTimestamp()
        {
            Console.WriteLine($"Current time: {DateTime.Now}");
        }
        
        static int CalculateFactorial(int n)
        {
            if (n <= 1) return 1;
            return n * CalculateFactorial(n - 1);
        }
        
        static string FormatName(string firstName, string lastName)
        {
            return $"{char.ToUpper(firstName[0])}{firstName.Substring(1)} {char.ToUpper(lastName[0])}{lastName.Substring(1)}";
        }
        
        static (int sum, double average, int count) GetStatistics(int[] numbers)
        {
            return (numbers.Sum(), numbers.Average(), numbers.Length);
        }
        
        static (int min, int max) GetMinMaxTuple(int[] numbers)
        {
            return (numbers.Min(), numbers.Max());
        }
        
        static int? FindNumber(int[] numbers, int target)
        {
            return numbers.Contains(target) ? target : (int?)null;
        }
        
        static T GetFirst<T>(T[] items)
        {
            return items.Length > 0 ? items[0] : default;
        }
        
        static bool TryDivide(double dividend, double divisor, out double result)
        {
            if (divisor == 0)
            {
                result = 0;
                return false;
            }
            result = dividend / divisor;
            return true;
        }
        
        static int Calculate(int x) => x * 2;
        static int Calculate(int x, int y) => x + y;
        static int Calculate(int x, int y, int z) => x * y * z;
        
        static void Process(int x) => Console.WriteLine($"Process(int): {x}");
        static void Process(ref int x) => Console.WriteLine($"Process(ref int): {x}");
        static void Process(out int x) { x = 10; Console.WriteLine($"Process(out int): {x}"); }
        
        static void ShowMessage(string message) => Console.WriteLine($"ShowMessage(string): {message}");
        static void ShowMessage(string message, string extra) => Console.WriteLine($"ShowMessage(string, string): {message} {extra}");
        static void ShowMessage(string message, string extra, string suffix) => Console.WriteLine($"ShowMessage(string, string, string): {message} {extra}{suffix}");
        
        // Extension method classes
        static class StringExtensions
        {
            public static string Capitalize(this string str)
            {
                if (string.IsNullOrEmpty(str)) return str;
                return char.ToUpper(str[0]) + str.Substring(1).ToLower();
            }
            
            public static string Reverse(this string str)
            {
                char[] chars = str.ToCharArray();
                Array.Reverse(chars);
                return new string(chars);
            }
        }
        
        static class NumberExtensions
        {
            public static bool IsEven(this int number) => number % 2 == 0;
        }
        
        static class CollectionExtensions
        {
            public static string JoinToString<T>(this IEnumerable<T> collection, string separator)
            {
                return string.Join(separator, collection);
            }
        }
        
        static class StackExtensions
        {
            public static bool HasItems<T>(this Stack<T> stack) => stack.Count > 0;
        }
        
        static class DateTimeExtensions
        {
            public static bool IsWeekend(this DateTime date) => date.DayOfWeek == DayOfWeek.Saturday || date.DayOfWeek == DayOfWeek.Sunday;
        }
        
        class Button
        {
            public event EventHandler Clicked;
            public void SimulateClick() => Clicked?.Invoke(this, EventArgs.Empty);
        }
        
        class Calculator
        {
            public static int StaticAdd(int a, int b) => a + b;
            public int InstanceAdd(int a, int b) => a + b;
        }
        
        static int QuickAdd(int a, int b) => a + b;
