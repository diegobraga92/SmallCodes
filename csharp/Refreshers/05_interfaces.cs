/*
    C# INTERFACES
    File: 05_interfaces.cs
    
    This file demonstrates interfaces in C# programming, covering concepts from
    junior to upper mid-level. Interfaces define contracts that classes must
    implement, enabling polymorphism and loose coupling.
    
    Key Concepts Covered:
    1. Interface Declaration and Implementation
    2. Multiple Interface Implementation
    3. Explicit Interface Implementation
    4. Default Interface Methods (C# 8.0+)
    5. Interface Inheritance
    6. Interface vs Abstract Class
    7. Dependency Injection with Interfaces
    8. Real-world Interface Patterns
*/

using System;
using System.Collections.Generic;

namespace CSharpRefresher.Interfaces
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Interfaces Demonstration ===\n");
            
            DemonstrateBasicInterfaces();
            DemonstrateMultipleInterfaces();
            DemonstrateExplicitImplementation();
            DemonstrateDefaultInterfaceMethods();
            DemonstrateInterfaceInheritance();
            DemonstrateInterfaceVsAbstractClass();
            DemonstrateDependencyInjection();
            DemonstrateRealWorldPatterns();
            
            Console.WriteLine("\n=== Interfaces Complete ===");
        }
        
        static void DemonstrateBasicInterfaces()
        {
            Console.WriteLine("============ BASIC INTERFACES ============\n");
            
            // ============ INTERFACE DECLARATION ============
            Console.WriteLine("=== 1. Interface Declaration ===");
            Console.WriteLine("""
                // Interface declaration syntax:
                // public interface IInterfaceName
                // {
                //     returnType MethodName(parameters);
                //     returnType PropertyName { get; set; }
                //     event EventHandler EventName;
                // }
                
                Key points:
                • No implementation (except default methods in C# 8.0+)
                • No fields (only properties, methods, events, indexers)
                • All members are implicitly public and abstract
                • Naming convention: Starts with 'I' (e.g., ILogger, IEnumerable)
                """);
            
            // ============ BASIC IMPLEMENTATION ============
            Console.WriteLine("\n=== 2. Basic Implementation ===");
            
            // Create instances using interface types
            ILogger consoleLogger = new ConsoleLogger();
            ILogger fileLogger = new FileLogger("app.log");
            
            // Call interface methods
            consoleLogger.Log("This message goes to console");
            fileLogger.Log("This message goes to file");
            
            // Interface properties
            Console.WriteLine($"\nConsole logger level: {consoleLogger.LogLevel}");
            Console.WriteLine($"File logger level: {fileLogger.LogLevel}");
            
            // Interface events (demonstration)
            ConsoleLogger advancedLogger = new ConsoleLogger();
            advancedLogger.LogMessageLogged += (sender, message) => 
                Console.WriteLine($"Event: Message '{message}' was logged");
            advancedLogger.Log("Test event");
            
            // ============ POLYMORPHISM WITH INTERFACES ============
            Console.WriteLine("\n=== 3. Polymorphism with Interfaces ===");
            
            List<ILogger> loggers = new List<ILogger>
            {
                new ConsoleLogger(),
                new FileLogger("log1.txt"),
                new DatabaseLogger()
            };
            
            Console.WriteLine("Processing multiple loggers through interface:");
            foreach (var logger in loggers)
            {
                logger.Log($"Message for {logger.GetType().Name}");
            }
        }
        
        static void DemonstrateMultipleInterfaces()
        {
            Console.WriteLine("\n============ MULTIPLE INTERFACES ============\n");
            
            // ============ CLASS IMPLEMENTING MULTIPLE INTERFACES ============
            Console.WriteLine("=== 1. Multiple Interface Implementation ===");
            
            // Create a device that implements multiple interfaces
            MultiFunctionDevice mfd = new MultiFunctionDevice();
            
            // Can use each interface separately
            IPrinter printer = mfd;
            IScanner scanner = mfd;
            IFaxMachine fax = mfd;
            
            printer.Print("Document.pdf");
            scanner.Scan();
            fax.Fax("Important memo");
            
            // Or use the concrete class that has all capabilities
            mfd.Print("Report.docx");
            mfd.Scan();
            mfd.Fax("Contract.pdf");
            
            // ============ INTERFACE SEGREGATION PRINCIPLE ============
            Console.WriteLine("\n=== 2. Interface Segregation Principle ===");
            Console.WriteLine("""
                Instead of one large interface:
                    interface IMachine { void Print(); void Scan(); void Fax(); }
                    
                Use smaller, focused interfaces:
                    interface IPrinter { void Print(); }
                    interface IScanner { void Scan(); }
                    interface IFaxMachine { void Fax(); }
                    
                Benefits:
                • Classes only implement interfaces they need
                • No forced implementation of unused methods
                • Better maintainability and flexibility
                """);
            
            // Demonstrate ISP in action
            SimplePrinter simplePrinter = new SimplePrinter();
            AllInOneMachine allInOne = new AllInOneMachine();
            
            simplePrinter.Print("Simple document");  // Can only print
            allInOne.Print("Document");             // Can print, scan, and fax
            allInOne.Scan();
            allInOne.Fax("Document");
        }
        
        static void DemonstrateExplicitImplementation()
        {
            Console.WriteLine("\n============ EXPLICIT INTERFACE IMPLEMENTATION ============\n");
            
            // ============ WHEN TO USE EXPLICIT IMPLEMENTATION ============
            Console.WriteLine("=== 1. Explicit Interface Implementation ===");
            Console.WriteLine("""
                Used when:
                1. A class implements two interfaces with same method signature
                2. You want to "hide" interface methods from the class's public API
                3. You need different implementations for same method from different interfaces
                
                Syntax: returnType InterfaceName.MethodName(parameters) { ... }
                """);
            
            // ============ CONFLICTING METHOD NAMES ============
            Console.WriteLine("\n=== 2. Resolving Name Conflicts ===");
            
            MultiInterfaceClass multi = new MultiInterfaceClass();
            
            // Can only access explicitly implemented methods through interface
            IFirstInterface first = multi;
            ISecondInterface second = multi;
            
            first.DoSomething();  // Calls IFirstInterface implementation
            second.DoSomething(); // Calls ISecondInterface implementation
            
            // multi.DoSomething(); // ERROR: Not accessible directly
            
            // ============ HIDING INTERFACE METHODS ============
            Console.WriteLine("\n=== 3. Hiding Interface Methods ===");
            
            FileHandler handler = new FileHandler();
            
            // Public method with additional functionality
            handler.Save("data.txt", "Hello World");
            
            // Interface method (explicit) with basic functionality
            ISaveable saveable = handler;
            saveable.Save("backup.txt", "Backup data");
            
            // ============ ACCESSING EXPLICIT IMPLEMENTATIONS ============
            Console.WriteLine("\n=== 4. Accessing Explicit Implementations ===");
            
            // Using type casting
            var handler2 = new FileHandler();
            ((ISaveable)handler2).Save("test.txt", "Test data");
        }
        
        static void DemonstrateDefaultInterfaceMethods()
        {
            Console.WriteLine("\n============ DEFAULT INTERFACE METHODS (C# 8.0+) ============\n");
            
            // ============ DEFAULT METHOD BASICS ============
            Console.WriteLine("=== 1. Default Interface Methods ===");
            Console.WriteLine("""
                New in C# 8.0: Interfaces can have default implementations
                
                Benefits:
                • Add new methods to interfaces without breaking existing implementations
                • Provide common functionality that can be overridden
                • Enable traits-like behavior
                
                Limitations:
                • Only accessible through interface reference
                • Cannot contain instance fields
                • Can only call other interface members
                """);
            
            // ============ USING DEFAULT METHODS ============
            Console.WriteLine("\n=== 2. Using Default Methods ===");
            
            IRepository<User> userRepo = new UserRepository();
            IRepository<Product> productRepo = new ProductRepository();
            
            // Call default method
            Console.WriteLine($"User repo is valid: {userRepo.IsValid()}");
            Console.WriteLine($"Product repo is valid: {productRepo.IsValid()}");
            
            // Call overridden default method
            Console.WriteLine($"\nUser count: {userRepo.Count()}");
            Console.WriteLine($"Product count: {productRepo.Count()}");
            
            // ============ VERSIONING WITH DEFAULT METHODS ============
            Console.WriteLine("\n=== 3. Interface Versioning Example ===");
            
            ILegacyService legacy = new ModernService();
            IModernService modern = new ModernService();
            
            legacy.PerformTask();      // Calls default implementation
            modern.PerformTask();      // Calls modern implementation
            modern.PerformNewTask();   // Calls default implementation
        }
        
        static void DemonstrateInterfaceInheritance()
        {
            Console.WriteLine("\n============ INTERFACE INHERITANCE ============\n");
            
            // ============ BASIC INTERFACE INHERITANCE ============
            Console.WriteLine("=== 1. Interface Inheritance ===");
            
            // Create instance of class implementing derived interface
            IAdvancedCalculator calculator = new ScientificCalculator();
            
            // Can call methods from all interfaces in hierarchy
            calculator.Add(5, 3);
            calculator.Subtract(10, 4);
            calculator.SquareRoot(25);
            calculator.Power(2, 8);
            
            // ============ MULTIPLE INTERFACE INHERITANCE ============
            Console.WriteLine("\n=== 2. Multiple Interface Inheritance ===");
            
            // Interface can inherit from multiple interfaces
            IMultiFunctionalDevice device = new OfficeMachine();
            
            device.Print("Report");
            device.Scan();
            device.Email("report@company.com", "Monthly Report");
            device.Fax("123-456-7890", "Contract");
            
            // ============ DIAMOND PROBLEM RESOLUTION ============
            Console.WriteLine("\n=== 3. Diamond Problem with Interfaces ===");
            Console.WriteLine("""
                C# handles the diamond problem (multiple inheritance through interfaces)
                using explicit interface implementation when needed.
                
                interface IA { void Method(); }
                interface IB { void Method(); }
                interface IC : IA, IB { }
                
                Class implementing IC must resolve which Method() to call,
                often using explicit implementation for at least one.
                """);
        }
        
        static void DemonstrateInterfaceVsAbstractClass()
        {
            Console.WriteLine("\n============ INTERFACE VS ABSTRACT CLASS ============\n");
            
            Console.WriteLine("=== Comparison Table ===");
            Console.WriteLine("""
                | Feature                | Interface                      | Abstract Class               |
                |------------------------|--------------------------------|------------------------------|
                | Multiple Inheritance   | Yes (class can implement many) | No (class inherits one only) |
                | Default Implementation | Yes (C# 8.0+)                  | Yes                          |
                | Fields                 | No (until C# 11)               | Yes                          |
                | Constructors           | No                             | Yes                          |
                | Access Modifiers       | All public implicitly          | Any (public, protected, etc) |
                | Versioning             | Better (default methods)       | Can break derived classes    |
                | Purpose                | Define contract/capability     | Provide common base implementation |
                """);
            
            // ============ WHEN TO USE INTERFACE ============
            Console.WriteLine("\n=== When to Use Interface ===");
            Console.WriteLine("""
                1. Multiple unrelated classes need same capability
                2. You need to define a contract for plugins/extensions
                3. You want to enable mocking in unit tests
                4. You need to support multiple inheritance of type
                5. The capability might be added to existing classes
                """);
            
            // ============ WHEN TO USE ABSTRACT CLASS ============
            Console.WriteLine("\n=== When to Use Abstract Class ===");
            Console.WriteLine("""
                1. Related classes share significant common code
                2. You need to define base behavior with some abstract parts
                3. You need to use non-public members in the hierarchy
                4. You need constructors or destructors in base type
                5. You're creating a family of closely related types
                """);
            
            // ============ PRACTICAL EXAMPLE ============
            Console.WriteLine("\n=== Practical Example ===");
            
            // Interface-based approach
            List<INotificationSender> senders = new List<INotificationSender>
            {
                new EmailSender(),
                new SmsSender(),
                new PushNotificationSender()
            };
            
            foreach (var sender in senders)
            {
                sender.SendNotification("Server maintenance scheduled", "admin");
            }
            
            // Abstract class-based approach
            Animal dog = new Dog();
            Animal cat = new Cat();
            
            dog.MakeSound();  // "Woof!"
            cat.MakeSound();  // "Meow!"
            dog.Eat();        // "Eating kibble" (from Animal base class)
            cat.Eat();        // "Eating kibble" (from Animal base class)
        }
        
        static void DemonstrateDependencyInjection()
        {
            Console.WriteLine("\n============ DEPENDENCY INJECTION WITH INTERFACES ============\n");
            
            // ============ WITHOUT DEPENDENCY INJECTION ============
            Console.WriteLine("=== 1. Problem: Tight Coupling ===");
            
            // Tightly coupled - hard to test or change
            var orderService1 = new OrderService();
            orderService1.ProcessOrder(123);
            
            // ============ WITH DEPENDENCY INJECTION ============
            Console.WriteLine("\n=== 2. Solution: Dependency Injection ===");
            
            // Create dependencies
            IOrderRepository repository = new SqlOrderRepository();
            IEmailService emailService = new SmtpEmailService();
            ILogger logger = new ConsoleLogger();
            
            // Inject dependencies through constructor
            var orderService2 = new OrderService(repository, emailService, logger);
            orderService2.ProcessOrder(456);
            
            // ============ TESTING WITH MOCKS ============
            Console.WriteLine("\n=== 3. Testing with Mocks ===");
            Console.WriteLine("""
                // With interfaces, we can easily create test doubles
                public class MockOrderRepository : IOrderRepository
                {
                    public Order GetOrder(int id) => new Order(id, "Test");
                    public void SaveOrder(Order order) { }
                }
                
                public class MockEmailService : IEmailService  
                {
                    public void SendEmail(string to, string subject) { }
                }
                
                // Now we can test OrderService in isolation
                var testService = new OrderService(
                    new MockOrderRepository(),
                    new MockEmailService(),
                    new ConsoleLogger()
                );
                """);
            
            // ============ DEPENDENCY INJECTION CONTAINER ============
            Console.WriteLine("\n=== 4. DI Container Example ===");
            
            // Simple manual DI container
            var container = new DependencyContainer();
            container.Register<ILogger, ConsoleLogger>();
            container.Register<IOrderRepository, SqlOrderRepository>();
            container.Register<IEmailService, SmtpEmailService>();
            container.Register<OrderService, OrderService>();
            
            var orderService3 = container.Resolve<OrderService>();
            orderService3.ProcessOrder(789);
        }
        
        static void DemonstrateRealWorldPatterns()
        {
            Console.WriteLine("\n============ REAL-WORLD INTERFACE PATTERNS ============\n");
            
            // ============ REPOSITORY PATTERN ============
            Console.WriteLine("=== 1. Repository Pattern ===");
            
            IRepository<Customer> customerRepo = new CustomerRepository();
            customerRepo.Add(new Customer(1, "Alice"));
            customerRepo.Add(new Customer(2, "Bob"));
            
            var customer = customerRepo.GetById(1);
            Console.WriteLine($"Retrieved customer: {customer.Name}");
            
            foreach (var c in customerRepo.GetAll())
            {
                Console.WriteLine($"Customer: {c.Name}");
            }
            
            // ============ STRATEGY PATTERN ============
            Console.WriteLine("\n=== 2. Strategy Pattern ===");
            
            var data = new[] { 5, 2, 8, 1, 9 };
            
            ISortStrategy bubbleSort = new BubbleSort();
            ISortStrategy quickSort = new QuickSort();
            
            var sorter = new Sorter(bubbleSort);
            sorter.Sort(data);
            Console.WriteLine("Sorted with bubble sort");
            
            sorter.SetStrategy(quickSort);
            sorter.Sort(data);
            Console.WriteLine("Sorted with quick sort");
            
            // ============ OBSERVER PATTERN ============
            Console.WriteLine("\n=== 3. Observer Pattern ===");
            
            var stock = new Stock("AAPL", 150.00m);
            var display = new StockDisplay();
            
            // Subscribe observers
            stock.Attach(display);
            stock.Attach(new PriceAlert(160.00m, "Price alert!"));
            
            // Change price (notifies all observers)
            stock.Price = 155.00m;
            stock.Price = 165.00m;
            
            // ============ ADAPTER PATTERN ============
            Console.WriteLine("\n=== 4. Adapter Pattern ===");
            
            // Legacy system we need to adapt
            var legacyLogger = new LegacyLogger();
            
            // Adapter makes legacy compatible with modern interface
            ILogger modernLogger = new LegacyLoggerAdapter(legacyLogger);
            modernLogger.Log("Adapted legacy message");
            
            // ============ FACTORY PATTERN ============
            Console.WriteLine("\n=== 5. Factory Pattern ===");
            
            IDocumentFactory factory = new DocumentFactory();
            
            IDocument report = factory.CreateDocument("report");
            report.Generate();
            
            IDocument invoice = factory.CreateDocument("invoice");
            invoice.Generate();
            
            IDocument resume = factory.CreateDocument("resume");
            resume.Generate();
        }
    }
    
    // ============ BASIC INTERFACE EXAMPLES ============
    
    // Simple interface with method, property, and event
    public interface ILogger
    {
        // Method
        void Log(string message);
        
        // Property
        LogLevel LogLevel { get; set; }
        
        // Event
        event EventHandler<string> LogMessageLogged;
    }
    
    public enum LogLevel { Debug, Info, Warning, Error }
    
    // Implementation 1: Console logger
    public class ConsoleLogger : ILogger
    {
        public LogLevel LogLevel { get; set; } = LogLevel.Info;
        public event EventHandler<string> LogMessageLogged;
        
        public void Log(string message)
        {
            if (LogLevel <= LogLevel.Info)
            {
                Console.WriteLine($"[CONSOLE] {DateTime.Now:HH:mm:ss}: {message}");
                LogMessageLogged?.Invoke(this, message);
            }
        }
    }
    
    // Implementation 2: File logger
    public class FileLogger : ILogger
    {
        private readonly string _filePath;
        
        public FileLogger(string filePath)
        {
            _filePath = filePath;
        }
        
        public LogLevel LogLevel { get; set; } = LogLevel.Warning;
        public event EventHandler<string> LogMessageLogged;
        
        public void Log(string message)
        {
            if (LogLevel <= LogLevel.Warning)
            {
                File.AppendAllText(_filePath, $"{DateTime.Now}: {message}\n");
                Console.WriteLine($"[FILE] Logged to {_filePath}: {message}");
                LogMessageLogged?.Invoke(this, message);
            }
        }
    }
    
    // Implementation 3: Database logger
    public class DatabaseLogger : ILogger
    {
        public LogLevel LogLevel { get; set; } = LogLevel.Error;
        public event EventHandler<string> LogMessageLogged;
        
        public void Log(string message)
        {
            // Simulate database logging
            Console.WriteLine($"[DATABASE] Would log to DB: {message}");
            LogMessageLogged?.Invoke(this, message);
        }
    }
    
    // ============ MULTIPLE INTERFACE EXAMPLES ============
    
    // Separate interfaces (Interface Segregation Principle)
    public interface IPrinter { void Print(string document); }
    public interface IScanner { void Scan(); }
    public interface IFaxMachine { void Fax(string document); }
    
    // Class implementing multiple interfaces
    public class MultiFunctionDevice : IPrinter, IScanner, IFaxMachine
    {
        public void Print(string document)
        {
            Console.WriteLine($"Printing: {document}");
        }
        
        public void Scan()
        {
            Console.WriteLine("Scanning document...");
        }
        
        public void Fax(string document)
        {
            Console.WriteLine($"Faxing: {document}");
        }
    }
    
    // Simple printer (only implements IPrinter)
    public class SimplePrinter : IPrinter
    {
        public void Print(string document)
        {
            Console.WriteLine($"Simple printer: {document}");
        }
    }
    
    // All-in-one machine (implements all)
    public class AllInOneMachine : IPrinter, IScanner, IFaxMachine
    {
        public void Print(string document)
        {
            Console.WriteLine($"All-in-one printing: {document}");
        }
        
        public void Scan()
        {
            Console.WriteLine("All-in-one scanning...");
        }
        
        public void Fax(string document)
        {
            Console.WriteLine($"All-in-one faxing: {document}");
        }
    }
    
    // ============ EXPLICIT INTERFACE IMPLEMENTATION ============
    
    // Two interfaces with same method signature
    public interface IFirstInterface { void DoSomething(); }
    public interface ISecondInterface { void DoSomething(); }
    
    // Class implementing both with explicit implementation
    public class MultiInterfaceClass : IFirstInterface, ISecondInterface
    {
        // Explicit implementation for IFirstInterface
        void IFirstInterface.DoSomething()
        {
            Console.WriteLine("IFirstInterface.DoSomething() called");
        }
        
        // Explicit implementation for ISecondInterface
        void ISecondInterface.DoSomething()
        {
            Console.WriteLine("ISecondInterface.DoSomething() called");
        }
    }
    
    // Interface with method to hide
    public interface ISaveable { void Save(string filename, string content); }
    
    // Class with explicit implementation to "hide" interface method
    public class FileHandler : ISaveable
    {
        // Public method with additional functionality
        public void Save(string filename, string content)
        {
            Console.WriteLine($"Saving with validation: {filename}");
            ValidateContent(content);
            File.WriteAllText(filename, content);
        }
        
        // Explicit interface implementation (basic version)
        void ISaveable.Save(string filename, string content)
        {
            Console.WriteLine($"Basic save: {filename}");
            File.WriteAllText(filename, content);
        }
        
        private void ValidateContent(string content)
        {
            if (string.IsNullOrEmpty(content))
                throw new ArgumentException("Content cannot be empty");
        }
    }
    
    // ============ DEFAULT INTERFACE METHODS ============
    
    // Repository interface with default methods
    public interface IRepository<T>
    {
        // Abstract method (must be implemented)
        void Add(T item);
        
        // Default method (C# 8.0+)
        bool IsValid()
        {
            Console.WriteLine("Default IsValid() implementation");
            return true;
        }
        
        // Another default method
        virtual int Count()
        {
            Console.WriteLine("Default Count() implementation");
            return 0;
        }
    }
    
    public class User
    {
        public int Id { get; set; }
        public string Name { get; set; }
        
        public User(int id, string name)
        {
            Id = id;
            Name = name;
        }
    }
    
    public class Product
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public decimal Price { get; set; }
    }
    
    public class UserRepository : IRepository<User>
    {
        private List<User> _users = new List<User>();
        
        public void Add(User user)
        {
            _users.Add(user);
            Console.WriteLine($"Added user: {user.Name}");
        }
        
        // Override default method
        public int Count()
        {
            return _users.Count;
        }
    }
    
    public class ProductRepository : IRepository<Product>
    {
        public void Add(Product product)
        {
            Console.WriteLine($"Added product: {product.Name}");
        }
        
        // Uses default Count() method
    }
    
    // ============ INTERFACE VERSIONING EXAMPLE ============
    
    // Legacy interface
    public interface ILegacyService
    {
        void PerformTask();
    }
    
    // Modern interface extends legacy
    public interface IModernService : ILegacyService
    {
        // New method with default implementation
        void PerformNewTask()
        {
            Console.WriteLine("Default implementation of PerformNewTask");
        }
        
        // Can also override legacy method with default
        new void PerformTask()
        {
            Console.WriteLine("Modern implementation of PerformTask");
        }
    }
    
    public class ModernService : IModernService
    {
        // Must implement the original PerformTask (from ILegacyService)
        public void PerformTask()
        {
            Console.WriteLine("Concrete implementation of PerformTask");
        }
        
        // Can optionally override default methods
    }
    
    // ============ INTERFACE INHERITANCE ============
    
    // Base interface
    public interface ICalculator
    {
        int Add(int a, int b);
        int Subtract(int a, int b);
    }
    
    // Extended interface
    public interface IAdvancedCalculator : ICalculator
    {
        double SquareRoot(double number);
        double Power(double baseNumber, double exponent);
    }
    
    public class ScientificCalculator : IAdvancedCalculator
    {
        public int Add(int a, int b) => a + b;
        public int Subtract(int a, int b) => a - b;
        public double SquareRoot(double number) => Math.Sqrt(number);
        public double Power(double baseNumber, double exponent) => Math.Pow(baseNumber, exponent);
    }
    
    // ============ DEPENDENCY INJECTION EXAMPLES ============
    
    // Service interfaces
    public interface IOrderRepository
    {
        Order GetOrder(int id);
        void SaveOrder(Order order);
    }
    
    public interface IEmailService
    {
        void SendEmail(string to, string subject, string body);
    }
    
    public class Order
    {
        public int Id { get; }
        public decimal Total { get; set; }
        
        public Order(int id) { Id = id; }
    }
    
    // Concrete implementations
    public class SqlOrderRepository : IOrderRepository
    {
        public Order GetOrder(int id)
        {
            Console.WriteLine($"Getting order {id} from SQL database");
            return new Order(id) { Total = 100.00m };
        }
        
        public void SaveOrder(Order order)
        {
            Console.WriteLine($"Saving order {order.Id} to SQL database");
        }
    }
    
    public class SmtpEmailService : IEmailService
    {
        public void SendEmail(string to, string subject, string body)
        {
            Console.WriteLine($"Sending email to {to}: {subject}");
        }
    }
    
    // Service with constructor injection
    public class OrderService
    {
        private readonly IOrderRepository _repository;
        private readonly IEmailService _emailService;
        private readonly ILogger _logger;
        
        // Constructor injection
        public OrderService(
            IOrderRepository repository,
            IEmailService emailService,
            ILogger logger)
        {
            _repository = repository;
            _emailService = emailService;
            _logger = logger;
        }
        
        // Parameterless constructor for demonstration
        public OrderService()
        {
            _repository = new SqlOrderRepository();
            _emailService = new SmtpEmailService();
            _logger = new ConsoleLogger();
        }
        
        public void ProcessOrder(int orderId)
        {
            _logger.Log($"Processing order {orderId}");
            var order = _repository.GetOrder(orderId);
            // Process order...
            _repository.SaveOrder(order);
            _emailService.SendEmail("customer@example.com", "Order Confirmation", "Your order was processed");
            _logger.Log($"Order {orderId} processed successfully");
        }
    }
    
    // Simple DI container
    public class DependencyContainer
    {
        private readonly Dictionary<Type, Type> _registrations = new();
        
        public void Register<TInterface, TImplementation>() where TImplementation : TInterface
        {
            _registrations[typeof(TInterface)] = typeof(TImplementation);
        }
        
        public T Resolve<T>()
        {
            var type = _registrations[typeof(T)];
            return (T)Activator.CreateInstance(type);
        }
    }
    
    // ============ REAL-WORLD PATTERN EXAMPLES ============
    
    // Repository Pattern
    public interface IRepository<T> where T : class
    {
        T GetById(int id);
        IEnumerable<T> GetAll();
        void Add(T entity);
        void Update(T entity);
        void Delete(T entity);
    }
    
    public class Customer
    {
        public int Id { get; }
        public string Name { get; set; }
        
        public Customer(int id, string name)
        {
            Id = id;
            Name = name;
        }
    }
    
    public class CustomerRepository : IRepository<Customer>
    {
        private List<Customer> _customers = new();
        
        public Customer GetById(int id) => _customers.FirstOrDefault(c => c.Id == id);
        public IEnumerable<Customer> GetAll() => _customers;
        public void Add(Customer entity) => _customers.Add(entity);
        public void Update(Customer entity) { /* Update logic */ }
        public void Delete(Customer entity) => _customers.Remove(entity);
    }
    
    // Strategy Pattern
    public interface ISortStrategy
    {
        void Sort(int[] array);
    }
    
    public class BubbleSort : ISortStrategy
    {
        public void Sort(int[] array) => Console.WriteLine("Sorting with bubble sort");
    }
    
    public class QuickSort : ISortStrategy
    {
        public void Sort(int[] array) => Console.WriteLine("Sorting with quick sort");
    }
    
    public class Sorter
    {
        private ISortStrategy _strategy;
        
        public Sorter(ISortStrategy strategy) => _strategy = strategy;
        public void SetStrategy(ISortStrategy strategy) => _strategy = strategy;
        public void Sort(int[] array) => _strategy.Sort(array);
    }
    
    // Observer Pattern
    public interface IObserver { void Update(string symbol, decimal price); }
    public interface ISubject
    {
        void Attach(IObserver observer);
        void Detach(IObserver observer);
        void Notify();
    }
    
    public class Stock : ISubject
    {
        private List<IObserver> _observers = new();
        private string _symbol;
        private decimal _price;
        
        public Stock(string symbol, decimal price)
        {
            _symbol = symbol;
            _price = price;
        }
        
        public decimal Price
        {
            get => _price;
            set
            {
                if (_price != value)
                {
                    _price = value;
                    Notify();
                }
            }
        }
        
        public void Attach(IObserver observer) => _observers.Add(observer);
        public void Detach(IObserver observer) => _observers.Remove(observer);
        public void Notify()
        {
            foreach (var observer in _observers)
                observer.Update(_symbol, _price);
        }
    }
    
    public class StockDisplay : IObserver
    {
        public void Update(string symbol, decimal price)
        {
            Console.WriteLine($"Stock {symbol}: ${price:F2}");
        }
    }
    
    public class PriceAlert : IObserver
    {
        private decimal _threshold;
        private string _message;
        
        public PriceAlert(decimal threshold, string message)
        {
            _threshold = threshold;
            _message = message;
        }
        
        public void Update(string symbol, decimal price)
        {
            if (price >= _threshold)
                Console.WriteLine($"ALERT: {_message} {symbol} at ${price:F2}");
        }
    }
    
    // Adapter Pattern
    public class LegacyLogger
    {
        public void WriteLog(string message)
        {
            Console.WriteLine($"LEGACY: {message}");
        }
    }
    
    public class LegacyLoggerAdapter : ILogger
    {
        private LegacyLogger _legacyLogger;
        
        public LegacyLoggerAdapter(LegacyLogger legacyLogger)
        {
            _legacyLogger = legacyLogger;
        }
        
        public LogLevel LogLevel { get; set; }
        public event EventHandler<string> LogMessageLogged;
        
        public void Log(string message)
        {
            _legacyLogger.WriteLog(message);
            LogMessageLogged?.Invoke(this, message);
        }
    }
    
    // Factory Pattern
    public interface IDocument { void Generate(); }
    public interface IDocumentFactory { IDocument CreateDocument(string type); }
    
    public class Report : IDocument { public void Generate() => Console.WriteLine("Generating report..."); }
    public class Invoice : IDocument { public void Generate() => Console.WriteLine("Generating invoice..."); }
    public class Resume : IDocument { public void Generate() => Console.WriteLine("Generating resume..."); }
    
    public class DocumentFactory : IDocumentFactory
    {
        public IDocument CreateDocument(string type)
        {
            return type.ToLower() switch
            {
                "report" => new Report(),
                "invoice" => new Invoice(),
                "resume" => new Resume(),
                _ => throw new ArgumentException($"Unknown document type: {type}")
            };
        }
    }
    
    // ============ ABSTRACT CLASS VS INTERFACE EXAMPLE ============
    
    // Abstract class example
    public abstract class Animal
    {
        // Abstract method (must be implemented)
        public abstract void MakeSound();
        
        // Concrete method (inherited by all derived classes)
        public virtual void Eat()
        {
            Console.WriteLine("Eating kibble");
        }
        
        // Can have fields
        protected int _age;
        
        // Can have constructor
        protected Animal() { }
    }
    
    public class Dog : Animal
    {
        public override void MakeSound() => Console.WriteLine("Woof!");
    }
    
    public class Cat : Animal
    {
        public override void MakeSound() => Console.WriteLine("Meow!");
        public override void Eat() => Console.WriteLine("Eating fish");
    }
    
    // Interface example for same domain
    public interface INotificationSender
    {
        void SendNotification(string message, string recipient);
    }
    
    public class EmailSender : INotificationSender
    {
        public void SendNotification(string message, string recipient)
        {
            Console.WriteLine($"Email to {recipient}: {message}");
        }
    }
    
    public class SmsSender : INotificationSender
    {
        public void SendNotification(string message, string recipient)
        {
            Console.WriteLine($"SMS to {recipient}: {message}");
        }
    }
    
    public class PushNotificationSender : INotificationSender
    {
        public void SendNotification(string message, string recipient)
        {
            Console.WriteLine($"Push notification to {recipient}: {message}");
        }
    }
}