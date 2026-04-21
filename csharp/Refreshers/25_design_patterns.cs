/*
    C# DESIGN PATTERNS
    File: 25_design_patterns.cs
    
    Comprehensive guide to Gang of Four (GoF) design patterns in C#.
    Covers creational, structural, and behavioral patterns with practical examples,
    real-world applications, .NET framework usage, and best practices.
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace CSharpRefresher.DesignPatterns
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Design Patterns ===\n");
            
            DemonstratePatternFundamentals();
            DemonstrateCreationalPatterns();
            DemonstrateStructuralPatterns();
            DemonstrateBehavioralPatterns();
            DemonstrateRealWorldApplications();
            DemonstrateBestPractices();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstratePatternFundamentals()
        {
            Console.WriteLine("=== 1. Pattern Fundamentals ===\n");
            
            // 1. What are design patterns?
            Console.WriteLine("1. What are Design Patterns?");
            Console.WriteLine("""
                Design patterns are reusable solutions to common software design problems.
                They are templates for solving problems that occur repeatedly in software development.
                
                Gang of Four (GoF) patterns (1994):
                • 23 classic patterns categorized into 3 groups
                • Still relevant today, though some have been superseded by language features
                
                Benefits:
                • Proven solutions: Tested and refined by experienced developers
                • Common vocabulary: Improves communication among team members
                • Code quality: Promotes maintainable, flexible, and reusable code
                • Learning tool: Helps developers understand good design principles
                
                When to use patterns:
                • Recognize the problem first, then apply the pattern
                • Don't force patterns where they don't fit
                • Consider simpler alternatives before complex patterns
                • Patterns should emerge from requirements, not be applied arbitrarily
                """);
            
            // 2. Pattern categories
            Console.WriteLine("\n2. Pattern Categories:");
            Console.WriteLine("""
                Creational Patterns (5):
                • Singleton: Ensure a class has only one instance
                • Factory Method: Create objects without specifying exact class
                • Abstract Factory: Create families of related objects
                • Builder: Construct complex objects step by step
                • Prototype: Clone existing objects
                
                Structural Patterns (7):
                • Adapter: Make incompatible interfaces work together
                • Decorator: Add responsibilities to objects dynamically
                • Facade: Provide simplified interface to complex subsystem
                • Composite: Treat individual objects and compositions uniformly
                • Proxy: Control access to another object
                • Bridge: Separate abstraction from implementation
                • Flyweight: Share objects to support large numbers efficiently
                
                Behavioral Patterns (11):
                • Observer: Notify dependents of state changes
                • Strategy: Encapsulate algorithms and make them interchangeable
                • Command: Encapsulate requests as objects
                • Iterator: Sequentially access elements of a collection
                • State: Allow object to alter behavior when its state changes
                • Template Method: Define algorithm skeleton, deferring steps to subclasses
                • Visitor: Add operations to objects without modifying them
                • Chain of Responsibility: Pass requests along a chain of handlers
                • Mediator: Centralize complex communications between objects
                • Memento: Capture and restore object state
                • Interpreter: Define grammar and interpreter for language
                """);
            
            // 3. Pattern principles
            Console.WriteLine("\n3. Underlying Principles:");
            Console.WriteLine("""
                SOLID principles (often implemented via patterns):
                • Single Responsibility: Each class has one reason to change
                • Open/Closed: Open for extension, closed for modification
                • Liskov Substitution: Subtypes should be substitutable for base types
                • Interface Segregation: Many specific interfaces better than one general
                • Dependency Inversion: Depend on abstractions, not concretions
                
                Other important principles:
                • DRY (Don't Repeat Yourself): Avoid code duplication
                • KISS (Keep It Simple, Stupid): Simplicity is key
                • YAGNI (You Ain't Gonna Need It): Don't add functionality until needed
                • Law of Demeter: Talk to friends, not strangers
                • Composition over Inheritance: Favor object composition over class inheritance
                """);
            
            // 4. Anti-patterns
            Console.WriteLine("\n4. Common Anti-patterns:");
            Console.WriteLine("""
                • God Object: Class that does too much (violates SRP)
                • Spaghetti Code: Unstructured, difficult-to-follow code
                • Golden Hammer: Using familiar solution for all problems
                • Premature Optimization: Optimizing before measuring
                • Magic Numbers/Strings: Hard-coded values without explanation
                • Copy-Paste Programming: Duplicating code instead of reusing
                • Bike Shedding: Spending too much time on trivial decisions
                
                Pattern misuse:
                • Pattern Happy: Applying patterns everywhere unnecessarily
                • Pattern Fetish: Choosing complex patterns for simple problems
                • Cargo Cult Programming: Using patterns without understanding why
                """);
        }
        
        static void DemonstrateCreationalPatterns()
        {
            Console.WriteLine("\n=== 2. Creational Patterns ===\n");
            
            // 1. Singleton pattern
            Console.WriteLine("1. Singleton Pattern:");
            Console.WriteLine("""
                Ensures a class has only one instance and provides global access.
                
                Thread-safe implementation (C#):
                public sealed class Singleton
                {
                    private static readonly Lazy<Singleton> _instance = 
                        new Lazy<Singleton>(() => new Singleton());
                    
                    public static Singleton Instance => _instance.Value;
                    
                    private Singleton() { }
                    
                    public void DoWork() { /* ... */ }
                }
                
                Usage:
                var singleton = Singleton.Instance;
                singleton.DoWork();
                
                When to use:
                • Logging, configuration, caching services
                • Database connections, thread pools
                • When exactly one instance is needed globally
                
                Considerations:
                • Hard to test (global state)
                • Can hide dependencies
                • Consider dependency injection instead
                • In .NET Core, use IOptions, ILogger, etc.
                """);
            
            // 2. Factory Method pattern
            Console.WriteLine("\n2. Factory Method Pattern:");
            Console.WriteLine("""
                Defines interface for creating objects, but lets subclasses decide which class.
                
                Example: Document creation
                public abstract class Document
                {
                    public abstract void Open();
                    public abstract void Save();
                }
                
                public class PdfDocument : Document { /* ... */ }
                public class WordDocument : Document { /* ... */ }
                
                public abstract class DocumentCreator
                {
                    public abstract Document CreateDocument();
                    
                    public void ProcessDocument()
                    {
                        var doc = CreateDocument();
                        doc.Open();
                        // Process...
                        doc.Save();
                    }
                }
                
                public class PdfCreator : DocumentCreator
                {
                    public override Document CreateDocument() => new PdfDocument();
                }
                
                public class WordCreator : DocumentCreator
                {
                    public override Document CreateDocument() => new WordDocument();
                }
                
                Usage:
                DocumentCreator creator = new PdfCreator();
                creator.ProcessDocument();
                
                When to use:
                • Class can't anticipate type of objects it must create
                • Class wants subclasses to specify objects it creates
                • Classes delegate responsibility to helper subclasses
                """);
            
            // 3. Abstract Factory pattern
            Console.WriteLine("\n3. Abstract Factory Pattern:");
            Console.WriteLine("""
                Creates families of related objects without specifying concrete classes.
                
                Example: UI framework for different OS
                public interface IButton { void Render(); }
                public interface ITextBox { void Render(); }
                
                public class WindowsButton : IButton { public void Render() => Console.WriteLine("Windows button"); }
                public class WindowsTextBox : ITextBox { public void Render() => Console.WriteLine("Windows textbox"); }
                
                public class MacButton : IButton { public void Render() => Console.WriteLine("Mac button"); }
                public class MacTextBox : ITextBox { public void Render() => Console.WriteLine("Mac textbox"); }
                
                public interface IUIFactory
                {
                    IButton CreateButton();
                    ITextBox CreateTextBox();
                }
                
                public class WindowsFactory : IUIFactory
                {
                    public IButton CreateButton() => new WindowsButton();
                    public ITextBox CreateTextBox() => new WindowsTextBox();
                }
                
                public class MacFactory : IUIFactory
                {
                    public IButton CreateButton() => new MacButton();
                    public ITextBox CreateTextBox() => new MacTextBox();
                }
                
                public class Application
                {
                    private readonly IButton _button;
                    private readonly ITextBox _textBox;
                    
                    public Application(IUIFactory factory)
                    {
                        _button = factory.CreateButton();
                        _textBox = factory.CreateTextBox();
                    }
                    
                    public void RenderUI()
                    {
                        _button.Render();
                        _textBox.Render();
                    }
                }
                
                Usage:
                IUIFactory factory = new WindowsFactory(); // Or MacFactory based on OS
                var app = new Application(factory);
                app.RenderUI();
                
                When to use:
                • System should be independent of how products are created
                • System configured with multiple product families
                • Products from same family must be used together
                • Need to enforce consistency across products
                """);
            
            // 4. Builder pattern
            Console.WriteLine("\n4. Builder Pattern:");
            Console.WriteLine("""
                Constructs complex objects step by step.
                
                Example: Pizza builder
                public class Pizza
                {
                    public string Dough { get; set; }
                    public string Sauce { get; set; }
                    public List<string> Toppings { get; } = new List<string>();
                    public bool Cheese { get; set; }
                    
                    public void Describe()
                    {
                        Console.WriteLine($"Pizza with {Dough} dough, {Sauce} sauce");
                        if (Cheese) Console.WriteLine("  Extra cheese");
                        if (Toppings.Any()) Console.WriteLine($"  Toppings: {string.Join(", ", Toppings)}");
                    }
                }
                
                public interface IPizzaBuilder
                {
                    void BuildDough();
                    void BuildSauce();
                    void BuildToppings();
                    void AddCheese();
                    Pizza GetPizza();
                }
                
                public class MargheritaBuilder : IPizzaBuilder
                {
                    private Pizza _pizza = new Pizza();
                    
                    public void BuildDough() => _pizza.Dough = "thin crust";
                    public void BuildSauce() => _pizza.Sauce = "tomato";
                    public void BuildToppings() => _pizza.Toppings.Add("basil");
                    public void AddCheese() => _pizza.Cheese = true;
                    public Pizza GetPizza() => _pizza;
                }
                
                public class PepperoniBuilder : IPizzaBuilder
                {
                    private Pizza _pizza = new Pizza();
                    
                    public void BuildDough() => _pizza.Dough = "thick crust";
                    public void BuildSauce() => _pizza.Sauce = "spicy tomato";
                    public void BuildToppings() => _pizza.Toppings.AddRange(new[] { "pepperoni", "mushrooms" });
                    public void AddCheese() => _pizza.Cheese = true;
                    public Pizza GetPizza() => _pizza;
                }
                
                public class Cook
                {
                    public Pizza MakePizza(IPizzaBuilder builder)
                    {
                        builder.BuildDough();
                        builder.BuildSauce();
                        builder.AddCheese();
                        builder.BuildToppings();
                        return builder.GetPizza();
                    }
                }
                
                Usage:
                var cook = new Cook();
                var margherita = cook.MakePizza(new MargheritaBuilder());
                margherita.Describe();
                
                Fluent builder variation (common in C#):
                public class PizzaFluentBuilder
                {
                    private Pizza _pizza = new Pizza();
                    
                    public PizzaFluentBuilder WithDough(string dough) { _pizza.Dough = dough; return this; }
                    public PizzaFluentBuilder WithSauce(string sauce) { _pizza.Sauce = sauce; return this; }
                    public PizzaFluentBuilder AddTopping(string topping) { _pizza.Toppings.Add(topping); return this; }
                    public PizzaFluentBuilder WithCheese() { _pizza.Cheese = true; return this; }
                    public Pizza Build() => _pizza;
                }
                
                // Fluent usage
                var pizza = new PizzaFluentBuilder()
                    .WithDough("thin crust")
                    .WithSauce("tomato")
                    .AddTopping("pepperoni")
                    .AddTopping("mushrooms")
                    .WithCheese()
                    .Build();
                
                When to use:
                • Complex object creation with many steps/options
                • Need different representations of same construction process
                • Avoid telescoping constructors (constructors with many parameters)
                • Want to create immutable objects
                """);
            
            // 5. Prototype pattern
            Console.WriteLine("\n5. Prototype Pattern:");
            Console.WriteLine("""
                Create new objects by copying existing objects (prototypes).
                
                In C#, use ICloneable interface or custom clone methods:
                public abstract class Shape : ICloneable
                {
                    public int X { get; set; }
                    public int Y { get; set; }
                    public string Color { get; set; }
                    
                    public abstract void Draw();
                    
                    // Shallow copy implementation
                    public object Clone()
                    {
                        return MemberwiseClone();
                    }
                    
                    // Deep copy method (custom)
                    public abstract Shape DeepClone();
                }
                
                public class Circle : Shape
                {
                    public int Radius { get; set; }
                    
                    public override void Draw()
                    {
                        Console.WriteLine($"Drawing circle at ({X},{Y}) with radius {Radius}");
                    }
                    
                    public override Shape DeepClone()
                    {
                        return new Circle
                        {
                            X = X,
                            Y = Y,
                            Color = Color,
                            Radius = Radius
                        };
                    }
                }
                
                public class Rectangle : Shape
                {
                    public int Width { get; set; }
                    public int Height { get; set; }
                    
                    public override void Draw()
                    {
                        Console.WriteLine($"Drawing rectangle at ({X},{Y}) {Width}x{Height}");
                    }
                    
                    public override Shape DeepClone()
                    {
                        return new Rectangle
                        {
                            X = X,
                            Y = Y,
                            Color = Color,
                            Width = Width,
                            Height = Height
                        };
                    }
                }
                
                // Prototype registry
                public class ShapeRegistry
                {
                    private Dictionary<string, Shape> _prototypes = new Dictionary<string, Shape>();
                    
                    public ShapeRegistry()
                    {
                        _prototypes["circle"] = new Circle { X = 0, Y = 0, Radius = 10, Color = "Red" };
                        _prototypes["rectangle"] = new Rectangle { X = 0, Y = 0, Width = 20, Height = 30, Color = "Blue" };
                    }
                    
                    public Shape CreateShape(string type)
                    {
                        if (_prototypes.TryGetValue(type, out Shape prototype))
                            return prototype.DeepClone();
                        throw new ArgumentException($"Unknown shape type: {type}");
                    }
                }
                
                Usage:
                var registry = new ShapeRegistry();
                var circle1 = registry.CreateShape("circle");
                circle1.X = 100;
                circle1.Draw();
                
                var circle2 = registry.CreateShape("circle");
                circle2.X = 200;
                circle2.Draw(); // Independent copy
                
                When to use:
                • Object creation is expensive (database calls, complex calculations)
                • Want to avoid subclassing for object creation
                • System should be independent of how objects are created
                • Need to create objects dynamically at runtime
                • When classes have few differences (configure via copying)
                """);
        }
        
        static void DemonstrateStructuralPatterns()
        {
            Console.WriteLine("\n=== 3. Structural Patterns ===\n");
            
            // 1. Adapter pattern
            Console.WriteLine("1. Adapter Pattern:");
            Console.WriteLine("""
                Makes incompatible interfaces work together.
                
                Example: Legacy system integration
                // Legacy system (incompatible interface)
                public class LegacyLogger
                {
                    public void LogMessage(string message, int severity)
                    {
                        Console.WriteLine($"[{severity}] {DateTime.Now}: {message}");
                    }
                }
                
                // Modern interface
                public interface ILogger
                {
                    void Log(string message, LogLevel level);
                }
                
                public enum LogLevel { Info, Warning, Error }
                
                // Adapter
                public class LegacyLoggerAdapter : ILogger
                {
                    private readonly LegacyLogger _legacyLogger;
                    
                    public LegacyLoggerAdapter(LegacyLogger legacyLogger)
                    {
                        _legacyLogger = legacyLogger;
                    }
                    
                    public void Log(string message, LogLevel level)
                    {
                        int severity = level switch
                        {
                            LogLevel.Info => 1,
                            LogLevel.Warning => 2,
                            LogLevel.Error => 3,
                            _ => 1
                        };
                        
                        _legacyLogger.LogMessage(message, severity);
                    }
                }
                
                // Object adapter (composition) vs Class adapter (inheritance)
                // C# doesn't support multiple inheritance, so object adapter is common
                
                Usage:
                var legacyLogger = new LegacyLogger();
                ILogger logger = new LegacyLoggerAdapter(legacyLogger);
                logger.Log("System started", LogLevel.Info);
                
                When to use:
                • Integrating legacy code with new system
                • Using third-party libraries with different interfaces
                • Creating reusable classes that cooperate with unrelated classes
                • Need multiple inheritance-like behavior (via interfaces)
                """);
            
            // 2. Decorator pattern
            Console.WriteLine("\n2. Decorator Pattern:");
            Console.WriteLine("""
                Adds responsibilities to objects dynamically.
                
                Example: Stream decorators in .NET
                // Base component
                public interface IDataStream
                {
                    string Read();
                    void Write(string data);
                }
                
                public class FileStream : IDataStream
                {
                    public string Read() => "File data";
                    public void Write(string data) => Console.WriteLine($"Writing to file: {data}");
                }
                
                // Base decorator
                public abstract class DataStreamDecorator : IDataStream
                {
                    protected IDataStream _stream;
                    
                    protected DataStreamDecorator(IDataStream stream)
                    {
                        _stream = stream;
                    }
                    
                    public virtual string Read() => _stream.Read();
                    public virtual void Write(string data) => _stream.Write(data);
                }
                
                // Concrete decorators
                public class EncryptionDecorator : DataStreamDecorator
                {
                    public EncryptionDecorator(IDataStream stream) : base(stream) { }
                    
                    public override string Read()
                    {
                        string encrypted = _stream.Read();
                        return $"Decrypted({encrypted})";
                    }
                    
                    public override void Write(string data)
                    {
                        string encrypted = $"Encrypted({data})";
                        _stream.Write(encrypted);
                    }
                }
                
                public class CompressionDecorator : DataStreamDecorator
                {
                    public CompressionDecorator(IDataStream stream) : base(stream) { }
                    
                    public override string Read()
                    {
                        string compressed = _stream.Read();
                        return $"Decompressed({compressed})";
                    }
                    
                    public override void Write(string data)
                    {
                        string compressed = $"Compressed({data})";
                        _stream.Write(compressed);
                    }
                }
                
                public class LoggingDecorator : DataStreamDecorator
                {
                    public LoggingDecorator(IDataStream stream) : base(stream) { }
                    
                    public override string Read()
                    {
                        Console.WriteLine("Reading data...");
                        return _stream.Read();
                    }
                    
                    public override void Write(string data)
                    {
                        Console.WriteLine($"Writing data: {data}");
                        _stream.Write(data);
                    }
                }
                
                Usage:
                IDataStream stream = new FileStream();
                stream = new LoggingDecorator(stream);
                stream = new CompressionDecorator(stream);
                stream = new EncryptionDecorator(stream);
                
                stream.Write("Hello World"); // Logs, compresses, encrypts, then writes to file
                string data = stream.Read(); // Reads file, decrypts, decompresses, logs
                
                When to use:
                • Add responsibilities to objects dynamically/transparently
                • Responsibilities can be withdrawn
                • Extension by subclassing is impractical
                • .NET examples: Stream decorators (GZipStream, CryptoStream), ASP.NET Middleware
                """);
            
            // 3. Facade pattern
            Console.WriteLine("\n3. Facade Pattern:");
            Console.WriteLine("""
                Provides simplified interface to complex subsystem.
                
                Example: Home theater system
                // Complex subsystem classes
                public class Amplifier
                {
                    public void On() => Console.WriteLine("Amplifier on");
                    public void SetVolume(int level) => Console.WriteLine($"Volume set to {level}");
                    public void Off() => Console.WriteLine("Amplifier off");
                }
                
                public class DvdPlayer
                {
                    public void On() => Console.WriteLine("DVD player on");
                    public void Play(string movie) => Console.WriteLine($"Playing {movie}");
                    public void Stop() => Console.WriteLine("DVD player stopped");
                    public void Off() => Console.WriteLine("DVD player off");
                }
                
                public class Projector
                {
                    public void On() => Console.WriteLine("Projector on");
                    public void SetInput(string input) => Console.WriteLine($"Projector input: {input}");
                    public void Off() => Console.WriteLine("Projector off");
                }
                
                public class Lights
                {
                    public void Dim(int level) => Console.WriteLine($"Lights dimmed to {level}%");
                    public void On() => Console.WriteLine("Lights on");
                }
                
                // Facade
                public class HomeTheaterFacade
                {
                    private readonly Amplifier _amp;
                    private readonly DvdPlayer _dvd;
                    private readonly Projector _projector;
                    private readonly Lights _lights;
                    
                    public HomeTheaterFacade(Amplifier amp, DvdPlayer dvd, Projector projector, Lights lights)
                    {
                        _amp = amp;
                        _dvd = dvd;
                        _projector = projector;
                        _lights = lights;
                    }
                    
                    public void WatchMovie(string movie)
                    {
                        Console.WriteLine("\n=== Getting ready to watch movie ===");
                        _lights.Dim(10);
                        _projector.On();
                        _projector.SetInput("DVD");
                        _amp.On();
                        _amp.SetVolume(5);
                        _dvd.On();
                        _dvd.Play(movie);
                    }
                    
                    public void EndMovie()
                    {
                        Console.WriteLine("\n=== Shutting down home theater ===");
                        _dvd.Stop();
                        _dvd.Off();
                        _amp.Off();
                        _projector.Off();
                        _lights.On();
                    }
                }
                
                Usage:
                var facade = new HomeTheaterFacade(
                    new Amplifier(),
                    new DvdPlayer(),
                    new Projector(),
                    new Lights());
                
                facade.WatchMovie("Inception");
                // Later...
                facade.EndMovie();
                
                When to use:
                • Provide simple interface to complex subsystem
                • Decouple client from subsystem components
                • Layer subsystems - create entry point for each layer
                • Wrap legacy systems with modern interface
                """);
            
            // 4. Composite pattern
            Console.WriteLine("\n4. Composite Pattern:");
            Console.WriteLine("""
                Treat individual objects and compositions uniformly.
                
                Example: File system structure
                // Component
                public abstract class FileSystemComponent
                {
                    public string Name { get; protected set; }
                    public abstract long GetSize();
                    public abstract void Display(string indent = "");
                    
                    public virtual void Add(FileSystemComponent component)
                    {
                        throw new NotImplementedException();
                    }
                    
                    public virtual void Remove(FileSystemComponent component)
                    {
                        throw new NotImplementedException();
                    }
                    
                    public virtual FileSystemComponent GetChild(int index)
                    {
                        throw new NotImplementedException();
                    }
                }
                
                // Leaf
                public class File : FileSystemComponent
                {
                    private long _size;
                    
                    public File(string name, long size)
                    {
                        Name = name;
                        _size = size;
                    }
                    
                    public override long GetSize() => _size;
                    
                    public override void Display(string indent = "")
                    {
                        Console.WriteLine($"{indent}📄 {Name} ({_size} bytes)");
                    }
                }
                
                // Composite
                public class Directory : FileSystemComponent
                {
                    private List<FileSystemComponent> _children = new List<FileSystemComponent>();
                    
                    public Directory(string name)
                    {
                        Name = name;
                    }
                    
                    public override void Add(FileSystemComponent component)
                    {
                        _children.Add(component);
                    }
                    
                    public override void Remove(FileSystemComponent component)
                    {
                        _children.Remove(component);
                    }
                    
                    public override FileSystemComponent GetChild(int index)
                    {
                        return _children[index];
                    }
                    
                    public override long GetSize()
                    {
                        return _children.Sum(child => child.GetSize());
                    }
                    
                    public override void Display(string indent = "")
                    {
                        Console.WriteLine($"{indent}📁 {Name}/ (total: {GetSize()} bytes)");
                        
                        foreach (var child in _children)
                        {
                            child.Display(indent + "  ");
                        }
                    }
                }
                
                Usage:
                var root = new Directory("root");
                var documents = new Directory("documents");
                var photos = new Directory("photos");
                
                root.Add(new File("readme.txt", 1024));
                root.Add(documents);
                root.Add(photos);
                
                documents.Add(new File("report.pdf", 20480));
                documents.Add(new File("budget.xlsx", 15360));
                
                photos.Add(new File("vacation.jpg", 5242880));
                photos.Add(new File("family.jpg", 4194304));
                
                root.Display();
                Console.WriteLine($"Total size: {root.GetSize()} bytes");
                
                When to use:
                • Represent part-whole hierarchies
                • Clients treat individual objects and compositions uniformly
                • GUI components (containers and widgets)
                • Organizational structures (departments and employees)
                • Expressions in compilers (expressions and subexpressions)
                """);
            
            // 5. Proxy pattern
            Console.WriteLine("\n5. Proxy Pattern:");
            Console.WriteLine("""
                Controls access to another object.
                
                Types of proxies:
                • Virtual Proxy: Creates expensive objects on demand
                • Protection Proxy: Controls access based on permissions
                • Remote Proxy: Represents object in different address space
                • Smart Proxy: Adds additional functionality (logging, caching)
                
                Example: Virtual proxy for expensive image loading
                public interface IImage
                {
                    void Display();
                }
                
                public class RealImage : IImage
                {
                    private string _filename;
                    
                    public RealImage(string filename)
                    {
                        _filename = filename;
                        LoadFromDisk();
                    }
                    
                    private void LoadFromDisk()
                    {
                        Console.WriteLine($"Loading {_filename} from disk...");
                        // Simulate expensive operation
                        System.Threading.Thread.Sleep(1000);
                    }
                    
                    public void Display()
                    {
                        Console.WriteLine($"Displaying {_filename}");
                    }
                }
                
                public class ProxyImage : IImage
                {
                    private RealImage _realImage;
                    private string _filename;
                    
                    public ProxyImage(string filename)
                    {
                        _filename = filename;
                    }
                    
                    public void Display()
                    {
                        if (_realImage == null)
                        {
                            _realImage = new RealImage(_filename);
                        }
                        _realImage.Display();
                    }
                }
                
                Example: Protection proxy
                public interface IDatabase
                {
                    void Query(string sql);
                }
                
                public class RealDatabase : IDatabase
                {
                    public void Query(string sql)
                    {
                        Console.WriteLine($"Executing: {sql}");
                    }
                }
                
                public class ProtectedDatabaseProxy : IDatabase
                {
                    private RealDatabase _database = new RealDatabase();
                    private string _userRole;
                    
                    public ProtectedDatabaseProxy(string userRole)
                    {
                        _userRole = userRole;
                    }
                    
                    public void Query(string sql)
                    {
                        if (_userRole == "admin" || !sql.ToUpper().Contains("DELETE"))
                        {
                            _database.Query(sql);
                        }
                        else
                        {
                            Console.WriteLine("Access denied: DELETE queries require admin role");
                        }
                    }
                }
                
                Usage:
                // Virtual proxy
                IImage image = new ProxyImage("photo.jpg");
                // Image not loaded yet
                image.Display(); // Loads and displays
                image.Display(); // Uses cached instance
                
                // Protection proxy
                IDatabase db = new ProtectedDatabaseProxy("user");
                db.Query("SELECT * FROM users"); // Allowed
                db.Query("DELETE FROM users");   // Denied
                
                When to use:
                • Lazy initialization (virtual proxy)
                • Access control (protection proxy)
                • Local representation of remote object (remote proxy)
                • Logging, caching, monitoring (smart proxy)
                • Reference counting, synchronization
                """);
        }
        
        static void DemonstrateBehavioralPatterns()
        {
            Console.WriteLine("\n=== 4. Behavioral Patterns ===\n");
            
            // 1. Observer pattern
            Console.WriteLine("1. Observer Pattern:");
            Console.WriteLine("""
                Defines one-to-many dependency: when subject changes, observers are notified.
                
                Example: Stock market notifications
                // Subject
                public interface IStockSubject
                {
                    void RegisterObserver(IStockObserver observer);
                    void RemoveObserver(IStockObserver observer);
                    void NotifyObservers();
                }
                
                public class Stock : IStockSubject
                {
                    private List<IStockObserver> _observers = new List<IStockObserver>();
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
                                NotifyObservers();
                            }
                        }
                    }
                    
                    public string Symbol => _symbol;
                    
                    public void RegisterObserver(IStockObserver observer)
                    {
                        _observers.Add(observer);
                    }
                    
                    public void RemoveObserver(IStockObserver observer)
                    {
                        _observers.Remove(observer);
                    }
                    
                    public void NotifyObservers()
                    {
                        foreach (var observer in _observers)
                        {
                            observer.Update(this);
                        }
                    }
                }
                
                // Observer
                public interface IStockObserver
                {
                    void Update(Stock stock);
                }
                
                public class Investor : IStockObserver
                {
                    private string _name;
                    
                    public Investor(string name)
                    {
                        _name = name;
                    }
                    
                    public void Update(Stock stock)
                    {
                        Console.WriteLine($"{_name}: {stock.Symbol} price changed to {stock.Price:C}");
                    }
                }
                
                public class StockApp : IStockObserver
                {
                    public void Update(Stock stock)
                    {
                        Console.WriteLine($"📱 Stock App: {stock.Symbol} = {stock.Price:C}");
                    }
                }
                
                Usage:
                var apple = new Stock("AAPL", 150.00m);
                
                var investor1 = new Investor("John");
                var investor2 = new Investor("Sarah");
                var app = new StockApp();
                
                apple.RegisterObserver(investor1);
                apple.RegisterObserver(investor2);
                apple.RegisterObserver(app);
                
                apple.Price = 152.50m; // All observers notified
                apple.Price = 151.75m; // All observers notified
                
                // .NET built-in: IObservable<T> and IObserver<T>
                // Events in C# are implementation of observer pattern
                
                When to use:
                • Change in one object requires changing others (unknown how many)
                • Object should notify others without knowing who they are
                • Loose coupling between subject and observers
                • Event-driven systems
                """);
            
            // 2. Strategy pattern
            Console.WriteLine("\n2. Strategy Pattern:");
            Console.WriteLine("""
                Encapsulates algorithms and makes them interchangeable.
                
                Example: Payment processing
                // Strategy interface
                public interface IPaymentStrategy
                {
                    void Pay(decimal amount);
                }
                
                // Concrete strategies
                public class CreditCardPayment : IPaymentStrategy
                {
                    private string _cardNumber;
                    private string _cvv;
                    
                    public CreditCardPayment(string cardNumber, string cvv)
                    {
                        _cardNumber = cardNumber;
                        _cvv = cvv;
                    }
                    
                    public void Pay(decimal amount)
                    {
                        Console.WriteLine($"Paid {amount:C} using credit card {_cardNumber.Substring(_cardNumber.Length - 4)}");
                    }
                }
                
                public class PayPalPayment : IPaymentStrategy
                {
                    private string _email;
                    
                    public PayPalPayment(string email)
                    {
                        _email = email;
                    }
                    
                    public void Pay(decimal amount)
                    {
                        Console.WriteLine($"Paid {amount:C} using PayPal account {_email}");
                    }
                }
                
                public class BitcoinPayment : IPaymentStrategy
                {
                    private string _walletAddress;
                    
                    public BitcoinPayment(string walletAddress)
                    {
                        _walletAddress = walletAddress;
                    }
                    
                    public void Pay(decimal amount)
                    {
                        Console.WriteLine($"Paid {amount:C} using Bitcoin wallet {_walletAddress.Substring(0, 8)}...");
                    }
                }
                
                // Context
                public class ShoppingCart
                {
                    private IPaymentStrategy _paymentStrategy;
                    private List<decimal> _items = new List<decimal>();
                    
                    public void AddItem(decimal price)
                    {
                        _items.Add(price);
                    }
                    
                    public decimal Total => _items.Sum();
                    
                    public void SetPaymentStrategy(IPaymentStrategy strategy)
                    {
                        _paymentStrategy = strategy;
                    }
                    
                    public void Checkout()
                    {
                        if (_paymentStrategy == null)
                            throw new InvalidOperationException("Payment strategy not set");
                        
                        Console.WriteLine($"Checking out {_items.Count} items, total: {Total:C}");
                        _paymentStrategy.Pay(Total);
                        _items.Clear();
                    }
                }
                
                Usage:
                var cart = new ShoppingCart();
                cart.AddItem(25.99m);
                cart.AddItem(19.99m);
                cart.AddItem(12.49m);
                
                // User selects payment method
                cart.SetPaymentStrategy(new CreditCardPayment("4111111111111111", "123"));
                cart.Checkout();
                
                // Or different strategy
                cart.AddItem(49.99m);
                cart.SetPaymentStrategy(new PayPalPayment("user@example.com"));
                cart.Checkout();
                
                When to use:
                • Multiple related algorithms differ only in behavior
                • Need different variants of algorithm
                • Avoid conditional statements for algorithm selection
                • Hide algorithm implementation details from clients
                """);
            
            // 3. Command pattern
            Console.WriteLine("\n3. Command Pattern:");
            Console.WriteLine("""
                Encapsulates requests as objects.
                
                Example: Text editor with undo/redo
                // Command interface
                public interface ICommand
                {
                    void Execute();
                    void Undo();
                }
                
                // Receiver
                public class TextEditor
                {
                    public string Text { get; private set; } = "";
                    
                    public void AddText(string text)
                    {
                        Text += text;
                    }
                    
                    public void DeleteText(int length)
                    {
                        if (length > Text.Length)
                            length = Text.Length;
                        Text = Text.Substring(0, Text.Length - length);
                    }
                    
                    public void Display()
                    {
                        Console.WriteLine($"Editor: \"{Text}\"");
                    }
                }
                
                // Concrete commands
                public class AddTextCommand : ICommand
                {
                    private TextEditor _editor;
                    private string _text;
                    
                    public AddTextCommand(TextEditor editor, string text)
                    {
                        _editor = editor;
                        _text = text;
                    }
                    
                    public void Execute()
                    {
                        _editor.AddText(_text);
                    }
                    
                    public void Undo()
                    {
                        _editor.DeleteText(_text.Length);
                    }
                }
                
                public class DeleteTextCommand : ICommand
                {
                    private TextEditor _editor;
                    private int _length;
                    private string _deletedText;
                    
                    public DeleteTextCommand(TextEditor editor, int length)
                    {
                        _editor = editor;
                        _length = length;
                    }
                    
                    public void Execute()
                    {
                        var currentText = _editor.Text;
                        _deletedText = currentText.Substring(currentText.Length - _length);
                        _editor.DeleteText(_length);
                    }
                    
                    public void Undo()
                    {
                        _editor.AddText(_deletedText);
                    }
                }
                
                // Invoker
                public class CommandManager
                {
                    private Stack<ICommand> _undoStack = new Stack<ICommand>();
                    private Stack<ICommand> _redoStack = new Stack<ICommand>();
                    
                    public void ExecuteCommand(ICommand command)
                    {
                        command.Execute();
                        _undoStack.Push(command);
                        _redoStack.Clear();
                    }
                    
                    public void Undo()
                    {
                        if (_undoStack.Count > 0)
                        {
                            var command = _undoStack.Pop();
                            command.Undo();
                            _redoStack.Push(command);
                        }
                    }
                    
                    public void Redo()
                    {
                        if (_redoStack.Count > 0)
                        {
                            var command = _redoStack.Pop();
                            command.Execute();
                            _undoStack.Push(command);
                        }
                    }
                }
                
                Usage:
                var editor = new TextEditor();
                var manager = new CommandManager();
                
                manager.ExecuteCommand(new AddTextCommand(editor, "Hello "));
                editor.Display(); // "Hello "
                
                manager.ExecuteCommand(new AddTextCommand(editor, "World!"));
                editor.Display(); // "Hello World!"
                
                manager.Undo();
                editor.Display(); // "Hello "
                
                manager.Redo();
                editor.Display(); // "Hello World!"
                
                manager.ExecuteCommand(new DeleteTextCommand(editor, 6));
                editor.Display(); // "Hello "
                
                manager.Undo();
                editor.Display(); // "Hello World!"
                
                When to use:
                • Parameterize objects with operations
                • Queue requests, schedule execution
                • Support undo/redo functionality
                • Log changes for recovery
                • Transactional behavior
                """);
            
            // 4. State pattern
            Console.WriteLine("\n4. State Pattern:");
            Console.WriteLine("""
                Allows object to change behavior when its internal state changes.
                
                Example: Order processing system
                // State interface
                public interface IOrderState
                {
                    void ProcessOrder(Order order);
                    void ShipOrder(Order order);
                    void DeliverOrder(Order order);
                    void CancelOrder(Order order);
                }
                
                // Context
                public class Order
                {
                    private IOrderState _currentState;
                    public string OrderNumber { get; }
                    
                    public Order(string orderNumber)
                    {
                        OrderNumber = orderNumber;
                        _currentState = new NewState();
                    }
                    
                    public void SetState(IOrderState state)
                    {
                        _currentState = state;
                    }
                    
                    public void Process() => _currentState.ProcessOrder(this);
                    public void Ship() => _currentState.ShipOrder(this);
                    public void Deliver() => _currentState.DeliverOrder(this);
                    public void Cancel() => _currentState.CancelOrder(this);
                    
                    public void DisplayStatus()
                    {
                        Console.WriteLine($"Order {OrderNumber}: {_currentState.GetType().Name}");
                    }
                }
                
                // Concrete states
                public class NewState : IOrderState
                {
                    public void ProcessOrder(Order order)
                    {
                        Console.WriteLine($"Processing order {order.OrderNumber}");
                        order.SetState(new ProcessingState());
                    }
                    
                    public void ShipOrder(Order order)
                    {
                        Console.WriteLine("Cannot ship order that hasn't been processed");
                    }
                    
                    public void DeliverOrder(Order order)
                    {
                        Console.WriteLine("Cannot deliver order that hasn't been shipped");
                    }
                    
                    public void CancelOrder(Order order)
                    {
                        Console.WriteLine($"Cancelling order {order.OrderNumber}");
                        order.SetState(new CancelledState());
                    }
                }
                
                public class ProcessingState : IOrderState
                {
                    public void ProcessOrder(Order order)
                    {
                        Console.WriteLine("Order is already being processed");
                    }
                    
                    public void ShipOrder(Order order)
                    {
                        Console.WriteLine($"Shipping order {order.OrderNumber}");
                        order.SetState(new ShippedState());
                    }
                    
                    public void DeliverOrder(Order order)
                    {
                        Console.WriteLine("Cannot deliver order that hasn't been shipped");
                    }
                    
                    public void CancelOrder(Order order)
                    {
                        Console.WriteLine($"Cancelling order {order.OrderNumber}");
                        order.SetState(new CancelledState());
                    }
                }
                
                public class ShippedState : IOrderState
                {
                    public void ProcessOrder(Order order)
                    {
                        Console.WriteLine("Order already shipped");
                    }
                    
                    public void ShipOrder(Order order)
                    {
                        Console.WriteLine("Order already shipped");
                    }
                    
                    public void DeliverOrder(Order order)
                    {
                        Console.WriteLine($"Delivering order {order.OrderNumber}");
                        order.SetState(new DeliveredState());
                    }
                    
                    public void CancelOrder(Order order)
                    {
                        Console.WriteLine("Cannot cancel shipped order");
                    }
                }
                
                public class DeliveredState : IOrderState
                {
                    public void ProcessOrder(Order order)
                    {
                        Console.WriteLine("Order already delivered");
                    }
                    
                    public void ShipOrder(Order order)
                    {
                        Console.WriteLine("Order already delivered");
                    }
                    
                    public void DeliverOrder(Order order)
                    {
                        Console.WriteLine("Order already delivered");
                    }
                    
                    public void CancelOrder(Order order)
                    {
                        Console.WriteLine("Cannot cancel delivered order");
                    }
                }
                
                public class CancelledState : IOrderState
                {
                    public void ProcessOrder(Order order)
                    {
                        Console.WriteLine("Cannot process cancelled order");
                    }
                    
                    public void ShipOrder(Order order)
                    {
                        Console.WriteLine("Cannot ship cancelled order");
                    }
                    
                    public void DeliverOrder(Order order)
                    {
                        Console.WriteLine("Cannot deliver cancelled order");
                    }
                    
                    public void CancelOrder(Order order)
                    {
                        Console.WriteLine("Order already cancelled");
                    }
                }
                
                Usage:
                var order = new Order("ORD-12345");
                order.DisplayStatus(); // NewState
                
                order.Process();
                order.DisplayStatus(); // ProcessingState
                
                order.Ship();
                order.DisplayStatus(); // ShippedState
                
                order.Deliver();
                order.DisplayStatus(); // DeliveredState
                
                // Try invalid transition
                var order2 = new Order("ORD-67890");
                order2.Ship(); // "Cannot ship order that hasn't been processed"
                
                When to use:
                • Object behavior depends on its state
                • Operations have large conditional statements based on state
                • States and transitions are well-defined
                • Need to add new states without changing existing code
                • State-specific behavior changes at runtime
                """);
            
            // 5. Template Method pattern
            Console.WriteLine("\n5. Template Method Pattern:");
            Console.WriteLine("""
                Defines algorithm skeleton, deferring steps to subclasses.
                
                Example: Data processing pipeline
                public abstract class DataProcessor
                {
                    // Template method - defines algorithm skeleton
                    public void ProcessData()
                    {
                        ReadData();
                        ValidateData();
                        TransformData();
                        SaveData();
                        NotifyCompletion();
                    }
                    
                    // Steps with default implementations
                    protected virtual void ReadData()
                    {
                        Console.WriteLine("Reading data from default source...");
                    }
                    
                    protected abstract void ValidateData();
                    protected abstract void TransformData();
                    
                    protected virtual void SaveData()
                    {
                        Console.WriteLine("Saving data to default destination...");
                    }
                    
                    protected virtual void NotifyCompletion()
                    {
                        Console.WriteLine("Processing completed");
                    }
                }
                
                public class CsvProcessor : DataProcessor
                {
                    protected override void ReadData()
                    {
                        Console.WriteLine("Reading CSV file...");
                    }
                    
                    protected override void ValidateData()
                    {
                        Console.WriteLine("Validating CSV data (checking columns, formats)...");
                    }
                    
                    protected override void TransformData()
                    {
                        Console.WriteLine("Transforming CSV data (parsing, cleaning)...");
                    }
                    
                    protected override void SaveData()
                    {
                        Console.WriteLine("Saving to database...");
                    }
                }
                
                public class JsonProcessor : DataProcessor
                {
                    protected override void ReadData()
                    {
                        Console.WriteLine("Reading JSON file from API...");
                    }
                    
                    protected override void ValidateData()
                    {
                        Console.WriteLine("Validating JSON schema...");
                    }
                    
                    protected override void TransformData()
                    {
                        Console.WriteLine("Transforming JSON structure...");
                    }
                    
                    protected override void SaveData()
                    {
                        Console.WriteLine("Saving to cloud storage...");
                    }
                    
                    protected override void NotifyCompletion()
                    {
                        base.NotifyCompletion();
                        Console.WriteLine("Sending email notification...");
                    }
                }
                
                public class XmlProcessor : DataProcessor
                {
                    protected override void ValidateData()
                    {
                        Console.WriteLine("Validating against XML schema (XSD)...");
                    }
                    
                    protected override void TransformData()
                    {
                        Console.WriteLine("Applying XSLT transformation...");
                    }
                    
                    // Uses default ReadData() and SaveData()
                }
                
                Usage:
                Console.WriteLine("Processing CSV:");
                var csvProcessor = new CsvProcessor();
                csvProcessor.ProcessData();
                
                Console.WriteLine("\nProcessing JSON:");
                var jsonProcessor = new JsonProcessor();
                jsonProcessor.ProcessData();
                
                Console.WriteLine("\nProcessing XML:");
                var xmlProcessor = new XmlProcessor();
                xmlProcessor.ProcessData();
                
                When to use:
                • Implement invariant parts of algorithm once
                • Let subclasses implement variant parts
                • Control subclass extensions (hook methods)
                • Code reuse among similar algorithms
                • Framework design (ASP.NET Page life cycle)
                """);
        }
        
        static void DemonstrateRealWorldApplications()
        {
            Console.WriteLine("\n=== 5. Real-World Applications ===\n");
            
            // 1. .NET Framework patterns
            Console.WriteLine("1. Patterns in .NET Framework:");
            Console.WriteLine("""
                Built-in pattern implementations:
                
                • IEnumerable/IEnumerator: Iterator pattern
                • IDisposable: Template Method (with using statement)
                • Stream decorators: Decorator pattern (GZipStream, CryptoStream)
                • IObservable/IObserver: Observer pattern
                • Lazy<T>: Virtual Proxy pattern
                • HttpClientFactory: Factory and Flyweight patterns
                • Middleware pipeline: Chain of Responsibility
                • ASP.NET MVC Filters: Decorator pattern
                • Entity Framework: Unit of Work, Repository patterns
                • Dependency Injection: Strategy and Factory patterns
                
                Example: ASP.NET Core middleware (Chain of Responsibility)
                public class CustomMiddleware
                {
                    private readonly RequestDelegate _next;
                    
                    public CustomMiddleware(RequestDelegate next)
                    {
                        _next = next;
                    }
                    
                    public async Task InvokeAsync(HttpContext context)
                    {
                        // Process request
                        Console.WriteLine("Before next middleware");
                        
                        await _next(context); // Call next middleware in chain
                        
                        // Process response
                        Console.WriteLine("After next middleware");
                    }
                }
                
                // Registration creates chain
                app.UseMiddleware<CustomMiddleware>();
                app.UseMiddleware<AuthenticationMiddleware>();
                app.UseMiddleware<AuthorizationMiddleware>();
                app.UseMiddleware<EndpointMiddleware>();
                """);
            
            // 2. Modern C# alternatives
            Console.WriteLine("\n2. Modern C# Alternatives to Classic Patterns:");
            Console.WriteLine("""
                Some patterns are less needed with modern language features:
                
                • Strategy Pattern: Replaced by delegates, lambda expressions, Func/Action
                  // Instead of strategy classes
                  public void ProcessData(Func<Data, Result> strategy) { }
                  ProcessData(data => data.Transform()); // Lambda as strategy
                  
                • Template Method: Replaced by default interface methods (C# 8.0+)
                  public interface IDataProcessor
                  {
                      void Process() // Template method
                      {
                          Read();
                          Validate();
                          Transform();
                      }
                      
                      void Read() { /* default */ }
                      abstract void Validate();
                      abstract void Transform();
                  }
                  
                • Singleton: Use dependency injection with singleton lifetime
                  services.AddSingleton<IService, Service>();
                  
                • Factory: Use static factory methods, DI containers
                  public static T Create<T>() where T : new() => new T();
                  
                • Observer: Use events, IObservable<T>, Reactive Extensions (Rx)
                  public event EventHandler<EventArgs> DataChanged;
                  DataChanged?.Invoke(this, EventArgs.Empty);
                  
                • Command: Use lambda expressions, Action/Func delegates
                  var commands = new List<Action>();
                  commands.Add(() => Console.WriteLine("Command 1"));
                  commands.ForEach(cmd => cmd());
                """);
            
            // 3. Microservices patterns
            Console.WriteLine("\n3. Patterns in Microservices Architecture:");
            Console.WriteLine("""
                • Circuit Breaker: Prevent cascade failures
                • Retry Pattern: Handle transient failures
                • Bulkhead: Isolate failures to specific components
                • API Gateway: Facade pattern for multiple services
                • Service Registry: Singleton for service discovery
                • Sidecar: Decorator pattern for cross-cutting concerns
                • Event Sourcing: Command pattern with event storage
                • CQRS: Separation of read and write operations
                • Saga Pattern: Distributed transaction management
                
                Example: Circuit Breaker implementation
                public class CircuitBreaker
                {
                    private CircuitState _state = CircuitState.Closed;
                    private int _failureCount = 0;
                    private DateTime _lastFailureTime;
                    
                    public async Task<T> ExecuteAsync<T>(Func<Task<T>> action)
                    {
                        if (_state == CircuitState.Open)
                        {
                            // Check if timeout has passed
                            if (DateTime.UtcNow - _lastFailureTime > TimeSpan.FromMinutes(1))
                            {
                                _state = CircuitState.HalfOpen;
                            }
                            else
                            {
                                throw new CircuitBreakerOpenException();
                            }
                        }
                        
                        try
                        {
                            var result = await action();
                            _state = CircuitState.Closed;
                            _failureCount = 0;
                            return result;
                        }
                        catch (Exception ex)
                        {
                            _failureCount++;
                            _lastFailureTime = DateTime.UtcNow;
                            
                            if (_failureCount >= 5)
                            {
                                _state = CircuitState.Open;
                            }
                            else if (_state == CircuitState.HalfOpen)
                            {
                                _state = CircuitState.Open;
                            }
                            
                            throw;
                        }
                    }
                    
                    private enum CircuitState { Closed, Open, HalfOpen }
                }
                """);
        }
        
        static void DemonstrateBestPractices()
        {
            Console.WriteLine("\n=== 6. Best Practices ===\n");
            
            // 1. When to use patterns
            Console.WriteLine("1. When to Use Design Patterns:");
            Console.WriteLine("""
                Use patterns when:
                • You recognize the problem the pattern solves
                • Pattern provides clear benefits over simpler solution
                • Pattern improves code maintainability, readability, or flexibility
                • Team understands and agrees on pattern usage
                • Pattern aligns with overall architecture
                
                Don't use patterns when:
                • You're applying pattern just because you know it
                • Simpler solution exists (KISS principle)
                • Pattern adds unnecessary complexity
                • Team doesn't understand the pattern
                • Requirements don't justify pattern overhead
                
                Remember: Patterns are tools, not goals.
                """);
            
            // 2. Pattern implementation guidelines
            Console.WriteLine("\n2. Implementation Guidelines:");
            Console.WriteLine("""
                • Start simple: Implement basic version first, refactor to pattern if needed
                • Use interfaces: Define pattern roles with interfaces for flexibility
                • Follow naming conventions: Use pattern names in class names (XxxStrategy, XxxFactory)
                • Document pattern usage: Add comments explaining why pattern was used
                • Consider performance: Some patterns add overhead (proxy, decorator)
                • Test patterns: Ensure pattern behavior is correct, especially state transitions
                • Keep patterns focused: Each pattern class should have single responsibility
                • Use modern C# features: Replace classic patterns with language features when appropriate
                """);
            
            // 3. Common mistakes
            Console.WriteLine("\n3. Common Mistakes to Avoid:");
            Console.WriteLine("""
                • Over-engineering: Using patterns for simple problems
                • Pattern misuse: Applying wrong pattern for problem
                • Blind copying: Using pattern without understanding
                • Rigid implementation: Not adapting pattern to specific needs
                • Pattern combination: Overlapping patterns causing confusion
                • Ignoring alternatives: Not considering simpler solutions
                • Premature optimization: Adding patterns for "future flexibility"
                • Testing difficulties: Creating hard-to-test pattern implementations
                """);
            
            // 4. Learning resources
            Console.WriteLine("\n4. Learning Resources:");
            Console.WriteLine("""
                Books:
                • "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF)
                • "Head First Design Patterns"
                • "Patterns of Enterprise Application Architecture" (Martin Fowler)
                • "Clean Code" and "Clean Architecture" (Robert C. Martin)
                
                Online Resources:
                • Refactoring Guru: Visual explanations with examples
                • SourceMaking: Detailed pattern explanations
                • .NET Documentation: Pattern implementations in .NET
                • Pluralsight/Udemy courses: Video tutorials
                
                Practice:
                • Implement patterns in small projects
                • Refactor existing code to use patterns
                • Study open-source projects using patterns
                • Participate in code reviews focusing on patterns
                """);
            
            // 5. Evolution of patterns
            Console.WriteLine("\n5. Pattern Evolution:");
            Console.WriteLine("""
                Patterns evolve with technology:
                • New patterns emerge (Microservices patterns, Cloud patterns)
                • Some patterns become built-in language features
                • Patterns combine to solve complex problems
                • Anti-patterns are identified and avoided
                
                Future trends:
                • Functional programming patterns
                • Reactive patterns (Rx, event-driven)
                • Cloud-native patterns
                • AI/ML patterns
                • Blockchain patterns
                
                Continuous learning:
                • Stay updated with new patterns
                • Understand pattern applicability in different contexts
                • Share knowledge with team
                • Adapt patterns to modern technologies
                """);
        }
    }
    
    // Supporting classes for pattern examples
    
    // For Strategy pattern
    public class Data { public string Content { get; set; } }
    public class Result { public bool Success { get; set; } public string Message { get; set; } }
    
    // For Command pattern
    public class CircuitBreakerOpenException : Exception
    {
        public CircuitBreakerOpenException() : base("Circuit breaker is open") { }
    }
    
    // For Observer pattern
    public class EventArgs { }
}
