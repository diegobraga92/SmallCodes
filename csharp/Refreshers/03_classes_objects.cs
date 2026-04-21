/*
    C# CLASSES AND OBJECTS
    File: 03_classes_objects.cs
    
    This file demonstrates classes and objects in C# programming.
    Covering concepts from junior to upper mid-level.
*/

using System;

namespace CSharpRefresher.ClassesObjects
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Classes and Objects Demonstration ===\n");
            
            DemonstrateClassBasics();
            DemonstrateConstructors();
            DemonstrateProperties();
            DemonstrateMethods();
            DemonstrateStaticMembers();
            DemonstrateStructs();
            DemonstrateRecords();
            
            Console.WriteLine("\n=== Classes and Objects Complete ===");
        }
        
        static void DemonstrateClassBasics()
        {
            Console.WriteLine("============ CLASS BASICS ============\n");
            
            // Creating objects
            Console.WriteLine("=== Creating Objects ===");
            Person person1 = new Person(); // Default constructor
            Person person2 = new Person("Alice", 30); // Parameterized constructor
            var person3 = new Person("Bob", 25); // Using var
            
            Console.WriteLine($"Person 1: {person1.Name}, {person1.Age}");
            Console.WriteLine($"Person 2: {person2.Name}, {person2.Age}");
            Console.WriteLine($"Person 3: {person3.Name}, {person3.Age}");
            
            // Object initializer syntax
            Console.WriteLine("\n=== Object Initializer ===");
            Person person4 = new Person { Name = "Charlie", Age = 35 };
            Console.WriteLine($"Person 4: {person4.Name}, {person4.Age}");
            
            // Null and default values
            Console.WriteLine("\n=== Null and Default Values ===");
            Person nullPerson = null;
            Person defaultPerson = default; // null for reference types
            
            Console.WriteLine($"nullPerson is null: {nullPerson == null}");
            Console.WriteLine($"defaultPerson is null: {defaultPerson == null}");
            
            // Value types vs reference types
            Console.WriteLine("\n=== Value Types vs Reference Types ===");
            Point point1 = new Point(10, 20); // Struct (value type)
            Point point2 = point1; // Copy of value
            point2.X = 30;
            
            Console.WriteLine($"point1: ({point1.X}, {point1.Y})");
            Console.WriteLine($"point2: ({point2.X}, {point2.Y}) (modified copy)");
            
            Person person5 = new Person("David", 40);
            Person person6 = person5; // Reference copy
            person6.Name = "Daniel";
            
            Console.WriteLine($"person5.Name: {person5.Name} (changed through reference)");
            Console.WriteLine($"person6.Name: {person6.Name}");
        }
        
        static void DemonstrateConstructors()
        {
            Console.WriteLine("\n============ CONSTRUCTORS ============\n");
            
            // Default constructor
            Console.WriteLine("=== Default Constructor ===");
            Product product1 = new Product();
            Console.WriteLine($"Product 1: {product1.Name}, ${product1.Price}");
            
            // Parameterized constructor
            Console.WriteLine("\n=== Parameterized Constructor ===");
            Product product2 = new Product("Laptop", 999.99m);
            Console.WriteLine($"Product 2: {product2.Name}, ${product2.Price}");
            
            // Constructor chaining
            Console.WriteLine("\n=== Constructor Chaining ===");
            Product product3 = new Product("Tablet");
            Console.WriteLine($"Product 3: {product3.Name}, ${product3.Price} (default price)");
            
            // Private constructor (singleton pattern)
            Console.WriteLine("\n=== Private Constructor (Singleton) ===");
            Logger logger1 = Logger.Instance;
            Logger logger2 = Logger.Instance;
            
            Console.WriteLine($"logger1 == logger2: {logger1 == logger2} (same instance)");
            logger1.Log("Singleton pattern working!");
            
            // Static constructor
            Console.WriteLine("\n=== Static Constructor ===");
            Console.WriteLine($"Application started at: {AppInfo.StartTime}");
            Console.WriteLine($"App version: {AppInfo.Version}");
            
            // Copy constructor
            Console.WriteLine("\n=== Copy Constructor ===");
            Product original = new Product("Phone", 499.99m);
            Product copy = new Product(original);
            Console.WriteLine($"Original: {original.Name}, ${original.Price}");
            Console.WriteLine($"Copy: {copy.Name}, ${copy.Price}");
            
            // Constructor with validation
            Console.WriteLine("\n=== Constructor with Validation ===");
            try
            {
                Product invalid = new Product("", -10.00m);
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"Validation error: {ex.Message}");
            }
        }
        
        static void DemonstrateProperties()
        {
            Console.WriteLine("\n============ PROPERTIES ============\n");
            
            // Auto-implemented properties
            Console.WriteLine("=== Auto-implemented Properties ===");
            Customer customer1 = new Customer("C001", "Alice");
            Console.WriteLine($"Customer: {customer1.Id}, {customer1.Name}");
            
            // Full properties with backing field
            Console.WriteLine("\n=== Full Properties ===");
            BankAccount account = new BankAccount("ACC123");
            account.Deposit(1000);
            account.Withdraw(200);
            Console.WriteLine($"Account {account.AccountNumber}: Balance = ${account.Balance}");
            
            // Read-only properties
            Console.WriteLine("\n=== Read-only Properties ===");
            Circle circle = new Circle(5.0);
            Console.WriteLine($"Circle radius: {circle.Radius}");
            Console.WriteLine($"Circle area: {circle.Area:F2}");
            Console.WriteLine($"Circle circumference: {circle.Circumference:F2}");
            
            // Init-only properties (C# 9+)
            Console.WriteLine("\n=== Init-only Properties ===");
            var config = new AppConfig 
            { 
                AppName = "MyApp",
                Version = "1.0",
                IsEnabled = true 
            };
            // config.AppName = "NewName"; // ERROR: init-only property
            Console.WriteLine($"Config: {config.AppName} v{config.Version}");
            
            // Computed properties
            Console.WriteLine("\n=== Computed Properties ===");
            Rectangle rect = new Rectangle(10, 5);
            Console.WriteLine($"Rectangle: {rect.Width}x{rect.Height}");
            Console.WriteLine($"Area: {rect.Area}");
            Console.WriteLine($"Perimeter: {rect.Perimeter}");
            Console.WriteLine($"IsSquare: {rect.IsSquare}");
            
            // Property with expression body (C# 6+)
            Console.WriteLine("\n=== Expression-bodied Properties ===");
            Vector2D vector = new Vector2D(3, 4);
            Console.WriteLine($"Vector: ({vector.X}, {vector.Y})");
            Console.WriteLine($"Magnitude: {vector.Magnitude:F2}");
            
            // Indexer properties
            Console.WriteLine("\n=== Indexer Properties ===");
            StringCollection collection = new StringCollection();
            collection[0] = "First";
            collection[1] = "Second";
            collection[2] = "Third";
            
            Console.WriteLine($"collection[0]: {collection[0]}");
            Console.WriteLine($"collection[1]: {collection[1]}");
            Console.WriteLine($"collection[2]: {collection[2]}");
            
            // Property accessibility
            Console.WriteLine("\n=== Property Accessibility ===");
            AccessDemo demo = new AccessDemo();
            demo.PublicProperty = "Public value";
            // demo.PrivateProperty = "Private"; // ERROR: private
            // demo.ProtectedProperty = "Protected"; // ERROR: protected
            
            Console.WriteLine($"Public property: {demo.PublicProperty}");
            Console.WriteLine($"Internal property: {demo.InternalProperty}");
        }
        
        static void DemonstrateMethods()
        {
            Console.WriteLine("\n============ METHODS ============\n");
            
            // Instance methods
            Console.WriteLine("=== Instance Methods ===");
            Calculator calc = new Calculator();
            int sum = calc.Add(5, 3);
            int product = calc.Multiply(4, 6);
            
            Console.WriteLine($"5 + 3 = {sum}");
            Console.WriteLine($"4 * 6 = {product}");
            
            // Method overloading
            Console.WriteLine("\n=== Method Overloading ===");
            Printer printer = new Printer();
            printer.Print("Hello");
            printer.Print("Hello", ConsoleColor.Green);
            printer.Print("Hello", ConsoleColor.Red, 3);
            
            // Virtual/override methods
            Console.WriteLine("\n=== Virtual and Override Methods ===");
            Shape shape1 = new CircleShape(5.0);
            Shape shape2 = new RectangleShape(4.0, 6.0);
            
            Console.WriteLine($"Circle area: {shape1.CalculateArea():F2}");
            Console.WriteLine($"Rectangle area: {shape2.CalculateArea():F2}");
            shape1.Display();
            shape2.Display();
            
            // Extension methods
            Console.WriteLine("\n=== Extension Methods ===");
            string text = "hello world";
            string reversed = text.Reverse();
            bool isPalindrome = "racecar".IsPalindrome();
            
            Console.WriteLine($"'{text}' reversed: '{reversed}'");
            Console.WriteLine($"'racecar' is palindrome: {isPalindrome}");
            
            // Partial methods
            Console.WriteLine("\n=== Partial Methods ===");
            PartialClass partial = new PartialClass();
            partial.CallPartialMethod();
        }
        
        static void DemonstrateStaticMembers()
        {
            Console.WriteLine("\n============ STATIC MEMBERS ============\n");
            
            // Static fields and properties
            Console.WriteLine("=== Static Fields and Properties ===");
            Console.WriteLine($"Current count: {Counter.CurrentCount}");
            Counter.Increment();
            Counter.Increment();
            Console.WriteLine($"After incrementing: {Counter.CurrentCount}");
            
            // Static methods
            Console.WriteLine("\n=== Static Methods ===");
            double celsius = TemperatureConverter.FahrenheitToCelsius(68);
            double fahrenheit = TemperatureConverter.CelsiusToFahrenheit(20);
            
            Console.WriteLine($"68°F = {celsius:F1}°C");
            Console.WriteLine($"20°C = {fahrenheit:F1}°F");
            
            // Static classes
            Console.WriteLine("\n=== Static Classes ===");
            string encoded = Base64Helper.Encode("Hello, World!");
            string decoded = Base64Helper.Decode(encoded);
            
            Console.WriteLine($"Encoded: {encoded}");
            Console.WriteLine($"Decoded: {decoded}");
            
            // Static constructor
            Console.WriteLine("\n=== Static Constructor ===");
            Console.WriteLine($"Database connection string: {DatabaseConfig.ConnectionString}");
            Console.WriteLine($"Max connections: {DatabaseConfig.MaxConnections}");
            
            // Static using (C# 6+)
            Console.WriteLine("\n=== Static Using ===");
            double sinValue = Math.Sin(Math.PI / 2);
            double cosValue = Math.Cos(0);
            
            Console.WriteLine($"sin(π/2) = {sinValue}");
            Console.WriteLine($"cos(0) = {cosValue}");
        }
        
        static void DemonstrateStructs()
        {
            Console.WriteLine("\n============ STRUCTS ============\n");
            
            // Struct basics
            Console.WriteLine("=== Struct Basics ===");
            Coordinate coord1 = new Coordinate(10, 20);
            Coordinate coord2 = coord1; // Value copy
            
            coord2.X = 30;
            Console.WriteLine($"coord1: ({coord1.X}, {coord1.Y})");
            Console.WriteLine($"coord2: ({coord2.X}, {coord2.Y})");
            
            // Struct with methods
            Console.WriteLine("\n=== Struct with Methods ===");
            coord1.Move(5, 5);
            double distance = coord1.DistanceTo(coord2);
            
            Console.WriteLine($"coord1 after move: ({coord1.X}, {coord1.Y})");
            Console.WriteLine($"Distance to coord2: {distance:F2}");
            
            // Readonly struct (C# 7.2+)
            Console.WriteLine("\n=== Readonly Struct ===");
            readonly ReadonlyPoint rp = new ReadonlyPoint(5, 10);
            // rp.X = 15; // ERROR: readonly struct
            Console.WriteLine($"Readonly point: ({rp.X}, {rp.Y})");
            
            // Ref struct (C# 7.2+)
            Console.WriteLine("\n=== Ref Struct ===");
            // RefStruct rs = new RefStruct(); // Can't be boxed or placed on heap
            
            // Struct vs class performance
            Console.WriteLine("\n=== Struct vs Class Performance ===");
            PointStruct[] structArray = new PointStruct[1000];
            PointClass[] classArray = new PointClass[1000];
            
            for (int i = 0; i < 1000; i++)
            {
                structArray[i] = new PointStruct(i, i * 2);
                classArray[i] = new PointClass(i, i * 2);
            }
            
            Console.WriteLine($"Created 1000 structs and 1000 classes");
            Console.WriteLine("Structs are stack-allocated, classes are heap-allocated");
        }
        
        static void DemonstrateRecords()
        {
            Console.WriteLine("\n============ RECORDS (C# 9+) ============\n");
            
            // Record basics
            Console.WriteLine("=== Record Basics ===");
            PersonRecord person1 = new PersonRecord("Alice", "Smith", 30);
            PersonRecord person2 = new PersonRecord("Alice", "Smith", 30);
            
            Console.WriteLine($"person1: {person1}");
            Console.WriteLine($"person2: {person2}");
            Console.WriteLine($"person1 == person2: {person1 == person2} (value equality)");
            Console.WriteLine($"Reference equals: {ReferenceEquals(person1, person2)}");
            
            // With-expressions
            Console.WriteLine("\n=== With-expressions ===");
            PersonRecord person3 = person1 with { Age = 31 };
            Console.WriteLine($"person1: {person1}");
            Console.WriteLine($"person3 (with Age=31): {person3}");
            
            // Positional records
            Console.WriteLine("\n=== Positional Records ===");
            PointRecord point1 = new PointRecord(10, 20);
            PointRecord point2 = point1 with { X = 15 };
            
            var (x, y) = point1; // Deconstruction
            Console.WriteLine($"point1: {point1}");
            Console.WriteLine($"point2: {point2}");
            Console.WriteLine($"Deconstructed: x={x}, y={y}");
            
            // Record inheritance
            Console.WriteLine("\n=== Record Inheritance ===");
            EmployeeRecord emp = new EmployeeRecord("Bob", "Johnson", 35, "E12345");
            Console.WriteLine($"Employee: {emp}");
            Console.WriteLine($"Employee ID: {emp.EmployeeId}");
            
            // Record structs (C# 10+)
            Console.WriteLine("\n=== Record Structs ===");
            PointRecordStruct pointStruct = new PointRecordStruct(5, 10);
            PointRecordStruct moved = pointStruct with { X = pointStruct.X + 5 };
            
            Console.WriteLine($"pointStruct: {pointStruct}");
            Console.WriteLine($"moved: {moved}");
        }
    }
    
    // ============ CLASS DEFINITIONS ============
    
    // Basic class
    class Person
    {
        // Fields
        private string name;
        private int age;
        
        // Properties
        public string Name
        {
            get { return name; }
            set { name = value; }
        }
        
        public int Age
        {
            get { return age; }
            set { age = value; }
        }
        
        // Constructors
        public Person()
        {
            Name = "Unknown";
            Age = 0;
        }
        
        public Person(string name, int age)
        {
            Name = name;
            Age = age;
        }
    }
    
    // Struct (value type)
    struct Point
    {
        public int X;
        public int Y;
        
        public Point(int x, int y)
        {
            X = x;
            Y = y;
        }
    }
    
    // Product class with constructors
    class Product
    {
        public string Name { get; set; }
        public decimal Price { get; set; }
        
        // Default constructor
        public Product()
        {
            Name = "Unnamed";
            Price = 0.00m;
        }
        
        // Parameterized constructor
        public Product(string name, decimal price)
        {
            if (string.IsNullOrWhiteSpace(name))
                throw new ArgumentException("Product name cannot be empty", nameof(name));
            if (price < 0)
                throw new ArgumentException("Price cannot be negative", nameof(price));
                
            Name = name;
            Price = price;
        }
        
        // Constructor chaining
        public Product(string name) : this(name, 9.99m)
        {
        }
        
        // Copy constructor
        public Product(Product other) : this(other.Name, other.Price)
        {
        }
    }
    
    // Singleton pattern with private constructor
    class Logger
    {
        private static Logger instance;
        private static readonly object lockObject = new object();
        
        // Private constructor
        private Logger()
        {
            Console.WriteLine("Logger instance created");
        }
        
        // Public static property to get instance
        public static Logger Instance
        {
            get
            {
                lock (lockObject)
                {
                    return instance ??= new Logger();
                }
            }
        }
        
        public void Log(string message)
        {
            Console.WriteLine($"[LOG] {DateTime.Now:HH:mm:ss}: {message}");
        }
    }
    
    // Static class with static constructor
    static class AppInfo
    {
        public static DateTime StartTime { get; }
        public static string Version { get; } = "1.0.0";
        
        // Static constructor
        static AppInfo()

