/*
    C# SOLID PRINCIPLES
    File: 26_solid_principles.cs
    
    Comprehensive guide to SOLID principles in object-oriented design.
    Covers Single Responsibility, Open/Closed, Liskov Substitution,
    Interface Segregation, and Dependency Inversion principles with
    practical C# examples, code smells, refactoring techniques,
    and real-world applications.
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace CSharpRefresher.SolidPrinciples
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# SOLID Principles ===\n");
            
            DemonstrateSingleResponsibility();
            DemonstrateOpenClosed();
            DemonstrateLiskovSubstitution();
            DemonstrateInterfaceSegregation();
            DemonstrateDependencyInversion();
            DemonstrateRealWorldApplications();
            DemonstrateCodeSmellsAndRefactoring();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateSingleResponsibility()
        {
            Console.WriteLine("=== 1. Single Responsibility Principle (SRP) ===\n");
            
            // 1. Definition and importance
            Console.WriteLine("1. Definition:");
            Console.WriteLine("""
                "A class should have only one reason to change."
                - Robert C. Martin
                
                Meaning: Each class should have only one responsibility or job.
                If a class has multiple responsibilities, changes to one responsibility
                may affect the others, increasing coupling and reducing maintainability.
                
                Key benefits:
                • Easier to understand: Classes are focused on single tasks
                • Easier to maintain: Changes are isolated
                • Easier to test: Fewer dependencies and side effects
                • Reduced coupling: Classes don't depend on unrelated functionality
                • Better organization: Logical grouping of related functionality
                """);
            
            // 2. Violation example
            Console.WriteLine("\n2. SRP Violation (Anti-pattern):");
            Console.WriteLine("""
                // Bad: Employee class handles too many responsibilities
                public class Employee
                {
                    public int Id { get; set; }
                    public string Name { get; set; }
                    public decimal Salary { get; set; }
                    public string Department { get; set; }
                    
                    // Responsibility 1: Business logic
                    public decimal CalculateBonus()
                    {
                        return Salary * 0.10m;
                    }
                    
                    // Responsibility 2: Data persistence
                    public void SaveToDatabase()
                    {
                        Console.WriteLine($"Saving employee {Id} to database...");
                        // Database connection and SQL execution
                    }
                    
                    // Responsibility 3: Reporting
                    public void GenerateReport()
                    {
                        Console.WriteLine($"Generating report for {Name}...");
                        // Complex report generation logic
                    }
                    
                    // Responsibility 4: Email notification
                    public void SendSalaryEmail()
                    {
                        Console.WriteLine($"Sending salary email to {Name}...");
                        // Email configuration and sending logic
                    }
                }
                
                Problems with this design:
                • Changes to database schema affect business logic
                • Changes to email service affect report generation
                • Testing is difficult (need database, email server)
                • Cannot reuse database logic without business logic
                • Violates separation of concerns
                """);
            
            // 3. Refactored solution
            Console.WriteLine("\n3. SRP-Compliant Solution:");
            Console.WriteLine("""
                // Separate classes for each responsibility
                
                // Domain model (business logic only)
                public class Employee
                {
                    public int Id { get; set; }
                    public string Name { get; set; }
                    public decimal Salary { get; set; }
                    public string Department { get; set; }
                    
                    public decimal CalculateBonus()
                    {
                        return Salary * 0.10m;
                    }
                }
                
                // Data persistence layer
                public class EmployeeRepository
                {
                    public void Save(Employee employee)
                    {
                        Console.WriteLine($"Saving employee {employee.Id} to database...");
                        // Database operations only
                    }
                    
                    public Employee GetById(int id)
                    {
                        Console.WriteLine($"Getting employee {id} from database...");
                        return new Employee { Id = id, Name = "John", Salary = 50000 };
                    }
                }
                
                // Reporting service
                public class ReportGenerator
                {
                    public void GenerateEmployeeReport(Employee employee)
                    {
                        Console.WriteLine($"Generating report for {employee.Name}...");
                        // Report generation logic
                    }
                }
                
                // Email service
                public class EmailService
                {
                    public void SendSalaryEmail(Employee employee)
                    {
                        Console.WriteLine($"Sending salary email to {employee.Name}...");
                        // Email sending logic
                    }
                }
                
                // Usage
                var employee = new Employee { Id = 1, Name = "John", Salary = 50000 };
                var repository = new EmployeeRepository();
                var reportGenerator = new ReportGenerator();
                var emailService = new EmailService();
                
                repository.Save(employee);
                reportGenerator.GenerateEmployeeReport(employee);
                emailService.SendSalaryEmail(employee);
                
                Benefits:
                • Each class has single, focused responsibility
                • Changes are isolated (database changes don't affect email)
                • Easier to test (mock dependencies)
                • Code is reusable (EmailService can be used elsewhere)
                • Better organization and maintainability
                """);
            
            // 4. Identifying responsibilities
            Console.WriteLine("\n4. Identifying Responsibilities:");
            Console.WriteLine("""
                How to identify if a class violates SRP:
                
                1. Ask "What does this class do?" If answer includes "and", it might violate SRP
                2. Look for groups of methods that could be extracted
                3. Check if class imports unrelated namespaces
                4. Count reasons to change (database, UI, business rules, etc.)
                5. Look for private methods that could be public in another class
                
                Common responsibility categories:
                • Data model/entity (properties only)
                • Business logic (calculations, validations)
                • Data access (database operations)
                • Presentation/UI (formatting, display)
                • External communication (APIs, email, messaging)
                • Infrastructure (logging, configuration, caching)
                
                Practical approach:
                • Start with simple classes
                • Extract responsibilities as they grow
                • Use composition over inheritance
                • Apply "extract class" refactoring
                • Consider domain-driven design boundaries
                """);
            
            // 5. Real-world examples
            Console.WriteLine("\n5. Real-World SRP Examples:");
            Console.WriteLine("""
                In ASP.NET Core:
                • Controllers: Handle HTTP requests only (not business logic)
                • Services: Contain business logic
                • Repositories: Handle data access
                • Models: Represent data structures
                
                In Entity Framework:
                • DbContext: Database operations only
                • Entities: Domain models with properties
                • ViewModels: Presentation-specific models
                • DTOs: Data transfer objects
                
                Common patterns that follow SRP:
                • Repository Pattern: Separates data access from business logic
                • Service Layer: Separates business logic from presentation
                • Strategy Pattern: Each strategy has single responsibility
                • Command Pattern: Each command handles specific operation
                
                Testing benefits:
                // Easy to test business logic without database
                [Test]
                public void CalculateBonus_ReturnsCorrectValue()
                {
                    var employee = new Employee { Salary = 50000 };
                    var bonus = employee.CalculateBonus();
                    Assert.Equal(5000, bonus);
                }
                
                // Easy to mock dependencies
                var mockRepository = new Mock<IEmployeeRepository>();
                var service = new EmployeeService(mockRepository.Object);
                // Test service logic without real database
                """);
        }
        
        static void DemonstrateOpenClosed()
        {
            Console.WriteLine("\n=== 2. Open/Closed Principle (OCP) ===\n");
            
            // 1. Definition and importance
            Console.WriteLine("1. Definition:");
            Console.WriteLine("""
                "Software entities (classes, modules, functions, etc.) should be open for extension, 
                but closed for modification."
                - Bertrand Meyer
                
                Meaning: You should be able to extend a class's behavior without modifying its source code.
                This is typically achieved through abstraction (interfaces, abstract classes) and polymorphism.
                
                Key benefits:
                • Stability: Existing code doesn't change, reducing bugs
                • Flexibility: New functionality added without breaking existing code
                • Testability: Existing tests continue to pass
                • Maintainability: Changes are isolated to new code
                • Scalability: Easy to add new features over time
                """);
            
            // 2. Violation example
            Console.WriteLine("\n2. OCP Violation (Anti-pattern):");
            Console.WriteLine("""
                // Bad: Adding new report types requires modifying existing code
                public class ReportGenerator
                {
                    public void GenerateReport(string reportType)
                    {
                        if (reportType == "PDF")
                        {
                            GeneratePdfReport();
                        }
                        else if (reportType == "Excel")
                        {
                            GenerateExcelReport();
                        }
                        else if (reportType == "CSV")
                        {
                            GenerateCsvReport();
                        }
                        // Adding new report type requires modifying this method
                        else
                        {
                            throw new ArgumentException($"Unknown report type: {reportType}");
                        }
                    }
                    
                    private void GeneratePdfReport() { /* PDF generation */ }
                    private void GenerateExcelReport() { /* Excel generation */ }
                    private void GenerateCsvReport() { /* CSV generation */ }
                }
                
                Problems:
                • Violates OCP: Must modify existing code to add new report types
                • Violates SRP: Class knows about all report types
                • Testing: Adding new type requires retesting all existing code
                • Risk: Changes could break existing functionality
                • Maintenance: Class grows with each new report type
                """);
            
            // 3. Refactored solution
            Console.WriteLine("\n3. OCP-Compliant Solution:");
            Console.WriteLine("""
                // Strategy pattern implementation
                public interface IReportGenerator
                {
                    void Generate();
                }
                
                public class PdfReportGenerator : IReportGenerator
                {
                    public void Generate()
                    {
                        Console.WriteLine("Generating PDF report...");
                        // PDF-specific logic
                    }
                }
                
                public class ExcelReportGenerator : IReportGenerator
                {
                    public void Generate()
                    {
                        Console.WriteLine("Generating Excel report...");
                        // Excel-specific logic
                    }
                }
                
                public class CsvReportGenerator : IReportGenerator
                {
                    public void Generate()
                    {
                        Console.WriteLine("Generating CSV report...");
                        // CSV-specific logic
                    }
                }
                
                // New report type can be added without modifying existing code
                public class HtmlReportGenerator : IReportGenerator
                {
                    public void Generate()
                    {
                        Console.WriteLine("Generating HTML report...");
                        // HTML-specific logic
                    }
                }
                
                // Report service that's closed for modification
                public class ReportService
                {
                    private readonly IReportGenerator _generator;
                    
                    public ReportService(IReportGenerator generator)
                    {
                        _generator = generator;
                    }
                    
                    public void GenerateReport()
                    {
                        _generator.Generate();
                    }
                }
                
                // Factory for creating generators (optional)
                public class ReportGeneratorFactory
                {
                    public IReportGenerator CreateGenerator(string reportType)
                    {
                        return reportType switch
                        {
                            "PDF" => new PdfReportGenerator(),
                            "Excel" => new ExcelReportGenerator(),
                            "CSV" => new CsvReportGenerator(),
                            "HTML" => new HtmlReportGenerator(), // New type added easily
                            _ => throw new ArgumentException($"Unknown report type: {reportType}")
                        };
                    }
                }
                
                Usage:
                var factory = new ReportGeneratorFactory();
                var generator = factory.CreateGenerator("HTML"); // New type
                var service = new ReportService(generator);
                service.GenerateReport();
                
                Benefits:
                • Open for extension: Add new report types without modifying existing code
                • Closed for modification: ReportService doesn't change
                • Testable: Each generator can be tested independently
                • Flexible: Easy to swap implementations
                • Maintainable: Changes isolated to new classes
                """);
            
            // 4. Extension methods approach
            Console.WriteLine("\n4. Extension Methods (C# Feature):");
            Console.WriteLine("""
                // Extension methods allow extending existing types without modification
                public static class StringExtensions
                {
                    public static string ToTitleCase(this string input)
                    {
                        if (string.IsNullOrEmpty(input))
                            return input;
                            
                        return char.ToUpper(input[0]) + input.Substring(1).ToLower();
                    }
                    
                    public static bool IsValidEmail(this string input)
                    {
                        return input.Contains("@") && input.Contains(".");
                    }
                    
                    public static string Truncate(this string input, int maxLength)
                    {
                        if (input.Length <= maxLength)
                            return input;
                        return input.Substring(0, maxLength) + "...";
                    }
                }
                
                Usage:
                string name = "john doe";
                string titleCase = name.ToTitleCase(); // "John Doe"
                bool isValid = "test@example.com".IsValidEmail(); // true
                string truncated = "This is a long text".Truncate(10); // "This is a..."
                
                Benefits:
                • Extend sealed/third-party classes
                • Add functionality without inheritance
                • Keep original class clean and focused
                • Organize related extension methods
                
                Limitations:
                • Can't override existing methods
                • Limited to public members of extended type
                • Can lead to "extension method pollution"
                • Not suitable for complex behavior changes
                """);
            
            // 5. Real-world patterns
            Console.WriteLine("\n5. OCP Implementation Patterns:");
            Console.WriteLine("""
                Common patterns that follow OCP:
                
                1. Strategy Pattern: Encapsulate algorithms in interchangeable classes
                   Example: Payment processors (CreditCard, PayPal, Bitcoin)
                   
                2. Template Method Pattern: Define algorithm skeleton in base class
                   Example: Data importers (CSV, XML, JSON importers)
                   
                3. Decorator Pattern: Add responsibilities dynamically
                   Example: Stream decorators (Compression, Encryption, Buffering)
                   
                4. Observer Pattern: Notify objects of state changes
                   Example: Event-driven systems, publish-subscribe
                   
                5. Factory Method Pattern: Delegate object creation to subclasses
                   Example: Document creators (PDF, Word, Excel)
                   
                .NET Framework examples:
                • IEnumerable<T>: Can be extended with LINQ extension methods
                • Stream: Extended by FileStream, MemoryStream, GZipStream, etc.
                • ILogger<T>: Extended by various logging providers
                • HttpClient: Extended by delegating handlers
                
                Testing benefits:
                // Easy to test new functionality without affecting existing tests
                [Test]
                public void HtmlReportGenerator_GeneratesHtmlReport()
                {
                    var generator = new HtmlReportGenerator();
                    // Test only the new generator
                    Assert.DoesNotThrow(() => generator.Generate());
                }
                
                // Existing tests continue to pass
                [Test]
                public void PdfReportGenerator_GeneratesPdfReport()
                {
                    var generator = new PdfReportGenerator();
                    // This test doesn't need to change
                    Assert.DoesNotThrow(() => generator.Generate());
                }
                """);
        }
        
        static void DemonstrateLiskovSubstitution()
        {
            Console.WriteLine("\n=== 3. Liskov Substitution Principle (LSP) ===\n");
            
            // 1. Definition and importance
            Console.WriteLine("1. Definition:");
            Console.WriteLine("""
                "Objects of a superclass should be replaceable with objects of its subclasses 
                without breaking the application."
                - Barbara Liskov
                
                Formal definition: If S is a subtype of T, then objects of type T may be 
                replaced with objects of type S without altering any of the desirable 
                properties of the program.
                
                Key benefits:
                • Predictability: Subclasses behave as expected
                • Reliability: No surprises when substituting types
                • Reusability: Code works with base class and all subclasses
                • Testability: Can test with base class interface
                • Maintainability: Easy to add new subclasses
                """);
            
            // 2. Violation example (classic Rectangle-Square problem)
            Console.WriteLine("\n2. LSP Violation (Rectangle-Square Problem):");
            Console.WriteLine("""
                // Bad: Square inherits from Rectangle, but violates LSP
                public class Rectangle
                {
                    public virtual int Width { get; set; }
                    public virtual int Height { get; set; }
                    
                    public int Area => Width * Height;
                    
                    public virtual void SetDimensions(int width, int height)
                    {
                        Width = width;
                        Height = height;
                    }
                }
                
                public class Square : Rectangle
                {
                    public override int Width
                    {
                        get => base.Width;
                        set
                        {
                            base.Width = value;
                            base.Height = value; // Violation: Changes both dimensions
                        }
                    }
                    
                    public override int Height
                    {
                        get => base.Height;
                        set
                        {
                            base.Height = value;
                            base.Width = value; // Violation: Changes both dimensions
                        }
                    }
                    
                    public override void SetDimensions(int width, int height)
                    {
                        if (width != height)
                            throw new ArgumentException("Square must have equal sides");
                            
                        base.SetDimensions(width, height);
                    }
                }
                
                // Client code that expects Rectangle behavior
                public class AreaCalculator
                {
                    public int CalculateArea(Rectangle rectangle)
                    {
                        rectangle.SetDimensions(5, 4);
                        return rectangle.Area; // Expects 20
                    }
                }
                
                Problem:
                var rectangle = new Rectangle();
                var area1 = new AreaCalculator().CalculateArea(rectangle); // 20
                
                var square = new Square(); // Substituting Rectangle with Square
                var area2 = new AreaCalculator().CalculateArea(square); // Throws exception or returns 25
                
                LSP Violations:
                • Square modifies both dimensions when setting one
                • Square throws exception for valid Rectangle input (5, 4)
                • Square has stronger preconditions than Rectangle
                • Client code breaks when substituting Rectangle with Square
                """);
            
            // 3. Refactored solution
            Console.WriteLine("\n3. LSP-Compliant Solution:");
            Console.WriteLine("""
                // Solution 1: Common interface instead of inheritance
                public interface IShape
                {
                    int Area { get; }
                }
                
                public class Rectangle : IShape
                {
                    public int Width { get; set; }
                    public int Height { get; set; }
                    public int Area => Width * Height;
                    
                    public void SetDimensions(int width, int height)
                    {
                        Width = width;
                        Height = height;
                    }
                }
                
                public class Square : IShape
                {
                    public int Side { get; set; }
                    public int Area => Side * Side;
                    
                    public void SetSide(int side)
                    {
                        Side = side;
                    }
                }
                
                // Solution 2: Immutable approach
                public abstract class Shape
                {
                    public abstract int Area { get; }
                }
                
                public class ImmutableRectangle : Shape
                {
                    public int Width { get; }
                    public int Height { get; }
                    
                    public ImmutableRectangle(int width, int height)
                    {
                        Width = width;
                        Height = height;
                    }
                    
                    public override int Area => Width * Height;
                }
                
                public class ImmutableSquare : Shape
                {
                    public int Side { get; }
                    
                    public ImmutableSquare(int side)
                    {
                        Side = side;
                    }
                    
                    public override int Area => Side * Side;
                }
                
                // Client code works with abstraction
                public class AreaCalculator
                {
                    public int CalculateArea(Shape shape)
                    {
                        return shape.Area; // Works with any Shape
                    }
                }
                
                Usage:
                var rectangle = new ImmutableRectangle(5, 4);
                var square = new ImmutableSquare(5);
                
                var calculator = new AreaCalculator();
                var area1 = calculator.CalculateArea(rectangle); // 20
                var area2 = calculator.CalculateArea(square);    // 25
                
                Benefits:
                • No surprises: Each shape behaves predictably
                • No exceptions: Valid for all shapes
                • Easy substitution: Calculator works with any Shape
                • Clear interfaces: Each shape has appropriate properties/methods
                """);
            
            // 4. Common LSP violations and solutions
            Console.WriteLine("\n4. Common LSP Violations and Solutions:");
            Console.WriteLine("""
                Violation 1: Throwing NotImplementedException
                // Bad
                public abstract class Bird
                {
                    public abstract void Fly();
                }
                
                public class Penguin : Bird
                {
                    public override void Fly()
                    {
                        throw new NotImplementedException("Penguins can't fly");
                    }
                }
                
                // Solution: Separate interfaces
                public interface IBird { }
                public interface IFlyingBird : IBird { void Fly(); }
                public interface ISwimmingBird : IBird { void Swim(); }
                
                public class Eagle : IFlyingBird { public void Fly() { } }
                public class Penguin : ISwimmingBird { public void Swim() { } }
                
                Violation 2: Stronger preconditions
                // Bad: Subclass has stricter requirements
                public class BankAccount
                {
                    public virtual void Withdraw(decimal amount)
                    {
                        if (amount <= 0) throw new ArgumentException("Amount must be positive");
                        // Withdraw logic
                    }
                }
                
                public class SavingsAccount : BankAccount
                {
                    public override void Withdraw(decimal amount)
                    {
                        if (amount > 1000) throw new ArgumentException("Maximum withdrawal is 1000");
                        base.Withdraw(amount);
                    }
                }
                
                // Solution: Don't inherit, use composition
                public class AccountWithdrawalLimit
                {
                    private BankAccount _account;
                    private decimal _limit;
                    
                    public void Withdraw(decimal amount)
                    {
                        if (amount > _limit) throw new ArgumentException($"Maximum withdrawal is {_limit}");
                        _account.Withdraw(amount);
                    }
                }
                
                Violation 3: Returning different types
                // Bad: Subclass returns more specific type
                public class Animal { }
                public class Dog : Animal { }
                
                public class AnimalFactory
                {
                    public virtual Animal Create() => new Animal();
                }
                
                public class DogFactory : AnimalFactory
                {
                    public override Dog Create() => new Dog(); // Covariant return (C# 9+ allows this)
                }
                
                // C# 9+ supports covariant returns, which is LSP-compliant
                """);
            
            // 5. Design by Contract
            Console.WriteLine("\n5. Design by Contract (DbC):");
            Console.WriteLine("""
                LSP is closely related to Design by Contract:
                
                Preconditions: Subclass cannot strengthen preconditions
                • What must be true before method execution
                • Example: Parameter validation
                
                Postconditions: Subclass cannot weaken postconditions
                • What must be true after method execution
                • Example: Return value guarantees
                
                Invariants: Subclass must preserve invariants
                • What must always be true
                • Example: Object state consistency
                
                Example with contracts:
                public abstract class Account
                {
                    protected decimal _balance;
                    
                    // Precondition: amount > 0
                    // Postcondition: _balance reduced by amount
                    // Invariant: _balance >= 0
                    public virtual void Withdraw(decimal amount)
                    {
                        if (amount <= 0)
                            throw new ArgumentException("Amount must be positive", nameof(amount));
                            
                        if (_balance < amount)
                            throw new InvalidOperationException("Insufficient funds");
                            
                        _balance -= amount;
                        
                        // Postcondition check
                        if (_balance < 0)
                            throw new InvalidOperationException("Balance invariant violated");
                    }
                }
                
                public class CheckingAccount : Account
                {
                    // OK: Same or weaker precondition (amount > 0 && amount <= 1000)
                    // OK: Same or stronger postcondition
                    public override void Withdraw(decimal amount)
                    {
                        if (amount > 1000)
                            throw new ArgumentException("Maximum withdrawal is 1000", nameof(amount));
                            
                        base.Withdraw(amount); // Preserves base class contract
                    }
                }
                
                LSP Compliance Checklist:
                • Subclass doesn't throw new exceptions for valid base class input
                • Subclass preserves all invariants of base class
                • Subclass methods accept at least the same input parameters
                • Subclass methods return at most the same output types
                • Subclass doesn't modify behavior in unexpected ways
                • Subclass can be used anywhere base class is expected
                """);
        }
        
        static void DemonstrateInterfaceSegregation()
        {
            Console.WriteLine("\n=== 4. Interface Segregation Principle (ISP) ===\n");
            
            // 1. Definition and importance
            Console.WriteLine("1. Definition:");
            Console.WriteLine("""
                "Clients should not be forced to depend on interfaces they do not use."
                - Robert C. Martin
                
                Meaning: Many client-specific interfaces are better than one general-purpose interface.
                Split large interfaces into smaller, more specific ones so that clients only need
                to know about the methods they actually use.
                
                Key benefits:
                • Decoupling: Clients depend only on what they need
                • Maintainability: Changes affect only relevant clients
                • Testability: Easier to mock smaller interfaces
                • Reusability: Interfaces can be combined as needed
                • Clarity: Clearer intent and responsibility
                """);
            
            // 2. Violation example (fat interface)
            Console.WriteLine("\n2. ISP Violation (Fat Interface):");
            Console.WriteLine("""
                // Bad: One interface trying to do everything
                public interface IWorker
                {
                    void Work();
                    void Eat();
                    void Sleep();
                    void Code();
                    void Design();
                    void Test();
                    void Deploy();
                    void Manage();
                }
                
                // Implementations forced to provide empty implementations
                public class Developer : IWorker
                {
                    public void Work() { /* Work implementation */ }
                    public void Eat() { /* Eat implementation */ }
                    public void Sleep() { /* Sleep implementation */ }
                    public void Code() { /* Code implementation */ }
                    public void Design() { /* Not a designer */ }
                    public void Test() { /* Sometimes tests */ }
                    public void Deploy() { /* Not responsible for deployment */ }
                    public void Manage() { /* Not a manager */ }
                }
                
                public class Manager : IWorker
                {
                    public void Work() { /* Work implementation */ }
                    public void Eat() { /* Eat implementation */ }
                    public void Sleep() { /* Sleep implementation */ }
                    public void Code() { /* Doesn't code */ }
                    public void Design() { /* Doesn't design */ }
                    public void Test() { /* Doesn't test */ }
                    public void Deploy() { /* Sometimes deploys */ }
                    public void Manage() { /* Manage implementation */ }
                }
                
                Problems:
                • Developers must implement methods they don't use
                • Empty implementations or throw NotImplementedException
                • Interface changes affect all implementations
                • Hard to understand what each implementation actually does
                • Violates SRP (interface has multiple responsibilities)
                • Testing is difficult (many methods to mock)
                """);
            
            // 3. Refactored solution
            Console.WriteLine("\n3. ISP-Compliant Solution:");
            Console.WriteLine("""
                // Segregated interfaces
                public interface IPerson
                {
                    void Eat();
                    void Sleep();
                }
                
                public interface IEmployee : IPerson
                {
                    void Work();
                }
                
                public interface IDeveloper
                {
                    void Code();
                    void Test();
                }
                
                public interface IDesigner
                {
                    void Design();
                }
                
                public interface IDevOps
                {
                    void Deploy();
                }
                
                public interface IManager
                {
                    void Manage();
                }
                
                // Implement only needed interfaces
                public class Developer : IEmployee, IDeveloper
                {
                    public void Eat() { Console.WriteLine("Developer eating"); }
                    public void Sleep() { Console.WriteLine("Developer sleeping"); }
                    public void Work() { Console.WriteLine("Developer working"); }
                    public void Code() { Console.WriteLine("Developer coding"); }
                    public void Test() { Console.WriteLine("Developer testing"); }
                }
                
                public class Manager : IEmployee, IManager
                {
                    public void Eat() { Console.WriteLine("Manager eating"); }
                    public void Sleep() { Console.WriteLine("Manager sleeping"); }
                    public void Work() { Console.WriteLine("Manager working"); }
                    public void Manage() { Console.WriteLine("Manager managing"); }
                }
                
                public class FullStackDeveloper : IEmployee, IDeveloper, IDesigner, IDevOps
                {
                    public void Eat() { Console.WriteLine("Full-stack eating"); }
                    public void Sleep() { Console.WriteLine("Full-stack sleeping"); }
                    public void Work() { Console.WriteLine("Full-stack working"); }
                    public void Code() { Console.WriteLine("Full-stack coding"); }
                    public void Test() { Console.WriteLine("Full-stack testing"); }
                    public void Design() { Console.WriteLine("Full-stack designing"); }
                    public void Deploy() { Console.WriteLine("Full-stack deploying"); }
                }
                
                // Clients depend only on what they need
                public class CodingTeam
                {
                    private readonly List<IDeveloper> _developers;
                    
                    public CodingTeam(List<IDeveloper> developers)
                    {
                        _developers = developers;
                    }
                    
                    public void StartCoding()
                    {
                        foreach (var developer in _developers)
                        {
                            developer.Code();
                        }
                    }
                }
                
                public class ManagementTeam
                {
                    private readonly List<IManager> _managers;
                    
                    public ManagementTeam(List<IManager> managers)
                    {
                        _managers = managers;
                    }
                    
                    public void StartManaging()
                    {
                        foreach (var manager in _managers)
                        {
                            manager.Manage();
                        }
                    }
                }
                
                Benefits:
                • No empty implementations
                • Clear role definitions
                • Easy to add new roles
                • Clients depend only on needed interfaces
                • Easy to test (mock specific interfaces)
                • Flexible combinations (FullStackDeveloper)
                """);
            
            // 4. Real-world examples
            Console.WriteLine("\n4. Real-World ISP Examples:");
            Console.WriteLine("""
                .NET Framework examples:
                
                1. IEnumerable<T> vs ICollection<T> vs IList<T>
                   • IEnumerable<T>: Basic iteration
                   • ICollection<T>: Add/remove/count
                   • IList<T>: Index-based access
                   
                2. IDisposable: Single responsibility (dispose resources)
                
                3. IComparable<T> vs IEquatable<T>
                   • IComparable<T>: Compare for ordering
                   • IEquatable<T>: Compare for equality
                   
                4. Stream hierarchy:
                   • Stream: Basic read/write
                   • FileStream: File operations
                   • MemoryStream: Memory operations
                   • NetworkStream: Network operations
                   
                ASP.NET Core examples:
                
                1. ILogger vs ILogger<T>
                   • ILogger: General logging
                   • ILogger<T>: Typed logger
                   
                2. Middleware interfaces:
                   • IMiddleware: Basic middleware
                   • IAuthorizationMiddleware: Authorization-specific
                   
                3. Hosted services:
                   • IHostedService: Basic hosted service
                   • BackgroundService: Abstract base class
                   
                Entity Framework examples:
                
                1. DbContext vs DbSet<T>
                   • DbContext: Database operations
                   • DbSet<T>: Entity-specific operations
                   
                2. IQueryable<T> vs IEnumerable<T>
                   • IQueryable<T>: Query composition
                   • IEnumerable<T>: In-memory iteration
                """);
            
            // 5. Interface design guidelines
            Console.WriteLine("\n5. Interface Design Guidelines:");
            Console.WriteLine("""
                When to create new interfaces:
                1. When interface has multiple unrelated methods
                2. When implementations leave methods empty
                3. When clients use only subset of methods
                4. When interface changes frequently for different reasons
                5. When testing requires mocking many unused methods
                
                Interface size guidelines:
                • 3-5 methods is often ideal
                • More than 10 methods is probably too large
                • Single method interfaces are often useful (Strategy pattern)
                • Consider cohesion: methods should be related
                
                Naming conventions:
                • Use adjective for capability (IComparable, IDisposable)
                • Use noun for role (IProvider, IRepository)
                • Use "I" prefix (standard C# convention)
                • Be specific about responsibility
                
                Composition over inheritance:
                // Instead of large interface hierarchy
                public interface IAdvancedWorker : IWorker, IDeveloper, IManager { }
                
                // Use composition
                public class TeamLead
                {
                    private readonly IWorker _worker;
                    private readonly IDeveloper _developer;
                    private readonly IManager _manager;
                    
                    public TeamLead(IWorker worker, IDeveloper developer, IManager manager)
                    {
                        _worker = worker;
                        _developer = developer;
                        _manager = manager;
                    }
                    
                    public void LeadTeam()
                    {
                        _worker.Work();
                        _developer.Code();
                        _manager.Manage();
                    }
                }
                
                Testing benefits:
                // Easy to mock
                var mockDeveloper = new Mock<IDeveloper>();
                mockDeveloper.Setup(d => d.Code()).Verifiable();
                
                var team = new CodingTeam(new List<IDeveloper> { mockDeveloper.Object });
                team.StartCoding();
                
                mockDeveloper.Verify(d => d.Code(), Times.Once);
                """);
        }
        
        static void DemonstrateDependencyInjection()
        {
            Console.WriteLine("\n=== 5. Dependency Inversion Principle (DIP) ===\n");
            
            // 1. Definition and importance
            Console.WriteLine("1. Definition:");
            Console.WriteLine("""
                "High-level modules should not depend on low-level modules. Both should depend on abstractions.
                Abstractions should not depend on details. Details should depend on abstractions."
                - Robert C. Martin
                
                Meaning: Depend on interfaces (abstractions) rather than concrete implementations.
                This inverts the traditional dependency direction.
                
                Key benefits:
                • Decoupling: Reduces tight coupling between components
                • Testability: Easy to substitute implementations for testing
                • Flexibility: Easy to change implementations
                • Maintainability: Changes are isolated
                • Reusability: Components can be used in different contexts
                """);
            
            // 2. Violation example
            Console.WriteLine("\n2. DIP Violation (Tight Coupling):");
            Console.WriteLine("""
                // Bad: High-level module depends on low-level details
                public class OrderService
                {
                    private readonly SqlServerDatabase _database;
                    private readonly SmtpEmailService _emailService;
                    private readonly FileLogger _logger;
                    
                    public OrderService()
                    {
                        // Direct dependency on concrete implementations
                        _database = new SqlServerDatabase();
                        _emailService = new SmtpEmailService();
                        _logger = new FileLogger();
                    }
                    
                    public void ProcessOrder(Order order)
                    {
                        _logger.Log("Processing order...");
                        _database.Save(order);
                        _emailService.SendConfirmation(order);
                        _logger.Log("Order processed");
                    }
                }
                
                public class SqlServerDatabase
                {
                    public void Save(Order order) { /* SQL Server specific */ }
                }
                
                public class SmtpEmailService
                {
                    public void SendConfirmation(Order order) { /* SMTP specific */ }
                }
                
                public class FileLogger
                {
                    public void Log(string message) { /* File logging */ }
                }
                
                Problems:
                • OrderService tightly coupled to specific implementations
                • Hard to test (need real database, email server, file system)
                • Hard to change (switch to MySQL requires code changes)
                • Violates SRP (OrderService knows about database, email, logging)
                • Cannot reuse OrderService with different implementations
                """);
            
            // 3. Refactored solution
            Console.WriteLine("\n3. DIP-Compliant Solution:");
            Console.WriteLine("""
                // Define abstractions (interfaces)
                public interface IOrderRepository
                {
                    void Save(Order order);
                }
                
                public interface IEmailService
                {
                    void SendConfirmation(Order order);
                }
                
                public interface ILogger
                {
                    void Log(string message);
                }
                
                // High-level module depends on abstractions
                public class OrderService
                {
                    private readonly IOrderRepository _repository;
                    private readonly IEmailService _emailService;
                    private readonly ILogger _logger;
                    
                    // Constructor injection (dependency injection)
                    public OrderService(
                        IOrderRepository repository,
                        IEmailService emailService,
                        ILogger logger)
                    {
                        _repository = repository;
                        _emailService = emailService;
                        _logger = logger;
                    }
                    
                    public void ProcessOrder(Order order)
                    {
                        _logger.Log("Processing order...");
                        _repository.Save(order);
                        _emailService.SendConfirmation(order);
                        _logger.Log("Order processed");
                    }
                }
                
                // Low-level modules implement abstractions
                public class SqlServerOrderRepository : IOrderRepository
                {
                    public void Save(Order order)
                    {
                        Console.WriteLine("Saving order to SQL Server...");
                        // SQL Server implementation
                    }
                }
                
                public class MySqlOrderRepository : IOrderRepository
                {
                    public void Save(Order order)
                    {
                        Console.WriteLine("Saving order to MySQL...");
                        // MySQL implementation
                    }
                }
                
                public class SmtpEmailService : IEmailService
                {
                    public void SendConfirmation(Order order)
                    {
                        Console.WriteLine("Sending email via SMTP...");
                        // SMTP implementation
                    }
                }
                
                public class SendGridEmailService : IEmailService
                {
                    public void SendConfirmation(Order order)
                    {
                        Console.WriteLine("Sending email via SendGrid...");
                        // SendGrid implementation
                    }
                }
                
                public class FileLogger : ILogger
                {
                    public void Log(string message)
                    {
                        Console.WriteLine($"File Log: {message}");
                        // File logging implementation
                    }
                }
                
                public class ConsoleLogger : ILogger
                {
                    public void Log(string message)
                    {
                        Console.WriteLine($"Console Log: {message}");
                        // Console logging
                    }
                }
                
                // Composition root (where dependencies are wired up)
                public class Program
                {
                    public static void Main()
                    {
                        // Configure dependencies (usually in DI container)
                        IOrderRepository repository = new SqlServerOrderRepository();
                        IEmailService emailService = new SendGridEmailService();
                        ILogger logger = new ConsoleLogger();
                        
                        // Inject dependencies
                        var orderService = new OrderService(repository, emailService, logger);
                        
                        // Use the service
                        var order = new Order();
                        orderService.ProcessOrder(order);
                    }
                }
                
                Benefits:
                • OrderService depends on abstractions, not concrete implementations
                • Easy to test (mock dependencies)
                • Easy to switch implementations
                • Components are reusable
                • Follows Open/Closed Principle
                """);
            
            // 4. Dependency Injection patterns
            Console.WriteLine("\n4. Dependency Injection Patterns:");
            Console.WriteLine("""
                Three types of dependency injection:
                
                1. Constructor Injection (recommended):
                public class OrderService
                {
                    private readonly IRepository _repository;
                    
                    public OrderService(IRepository repository)
                    {
                        _repository = repository; // Injected via constructor
                    }
                }
                
                2. Property Injection:
                public class OrderService
                {
                    public IRepository Repository { get; set; } // Injected via property
                }
                
                3. Method Injection:
                public class OrderService
                {
                    public void ProcessOrder(Order order, IRepository repository)
                    {
                        // repository injected via method parameter
                    }
                }
                
                Dependency Injection Containers (IoC Containers):
                
                // Manual dependency injection
                var repository = new SqlRepository();
                var service = new OrderService(repository);
                
                // Using DI container (e.g., Microsoft.Extensions.DependencyInjection)
                var services = new ServiceCollection();
                services.AddSingleton<IRepository, SqlRepository>();
                services.AddSingleton<IOrderService, OrderService>();
                
                var serviceProvider = services.BuildServiceProvider();
                var orderService = serviceProvider.GetRequiredService<IOrderService>();
                
                Common .NET DI containers:
                • Microsoft.Extensions.DependencyInjection (built-in, lightweight)
                • Autofac (feature-rich, modular)
                • Ninject (kernel-based, flexible)
                • Simple Injector (fast, verification)
                • Unity (Microsoft legacy)
                """);
            
            // 5. Real-world applications
            Console.WriteLine("\n5. Real-World DIP Applications:");
            Console.WriteLine("""
                ASP.NET Core architecture:
                
                // Startup.cs or Program.cs
                public void ConfigureServices(IServiceCollection services)
                {
                    // Register abstractions with implementations
                    services.AddScoped<IProductRepository, ProductRepository>();
                    services.AddScoped<IOrderService, OrderService>();
                    services.AddSingleton<ILogger, Logger>();
                    
                    // Framework handles dependency injection
                }
                
                // Controller depends on abstractions
                [ApiController]
                public class OrdersController : ControllerBase
                {
                    private readonly IOrderService _orderService;
                    
                    public OrdersController(IOrderService orderService) // Injected by framework
                    {
                        _orderService = orderService;
                    }
                    
                    [HttpPost]
                    public IActionResult CreateOrder(Order order)
                    {
                        _orderService.ProcessOrder(order);
                        return Ok();
                    }
                }
                
                Testing with DIP:
                
                [Test]
                public void OrderService_ProcessOrder_SavesToRepository()
                {
                    // Arrange
                    var mockRepository = new Mock<IOrderRepository>();
                    var mockEmail = new Mock<IEmailService>();
                    var mockLogger = new Mock<ILogger>();
                    
                    var orderService = new OrderService(
                        mockRepository.Object,
                        mockEmail.Object,
                        mockLogger.Object);
                    
                    var order = new Order();
                    
                    // Act
                    orderService.ProcessOrder(order);
                    
                    // Assert
                    mockRepository.Verify(r => r.Save(order), Times.Once);
                }
                
                Design patterns that use DIP:
                
                1. Strategy Pattern: Context depends on Strategy interface
                2. Factory Pattern: Client depends on Factory interface
                3. Repository Pattern: Business logic depends on Repository interface
                4. Unit of Work Pattern: Services depend on IUnitOfWork interface
                5. Observer Pattern: Subject depends on Observer interface
                
                Architectural patterns:
                
                • Clean Architecture: Inner circles depend on abstractions
                • Hexagonal Architecture: Core depends on ports (interfaces)
                • Onion Architecture: Core depends on abstractions, not infrastructure
                • Layered Architecture: Upper layers depend on abstractions of lower layers
                
                Practical implementation steps:
                
                1. Identify dependencies in your classes
                2. Extract interfaces for those dependencies
                3. Modify classes to depend on interfaces
                4. Move concrete implementations to separate classes
                5. Use dependency injection to wire everything together
                6. Configure dependencies in composition root
                7. Test with mock implementations
                """);
        }
        
        static void DemonstrateRealWorldApplications()
        {
            Console.WriteLine("\n=== 6. SOLID in Real-World Applications ===\n");
            
            // 1. Combined example
            Console.WriteLine("1. Combined SOLID Example:");
            Console.WriteLine("""
                // E-commerce order processing system
                
                // SRP: Separate interfaces for each responsibility
                public interface IOrderRepository
                {
                    Task SaveAsync(Order order);
                }
                
                public interface IPaymentProcessor
                {
                    Task<PaymentResult> ProcessAsync(PaymentRequest request);
                }
                
                public interface IInventoryService
                {
                    Task<bool> ReserveItemsAsync(Order order);
                }
                
                public interface INotificationService
                {
                    Task SendOrderConfirmationAsync(Order order);
                }
                
                // OCP: Open for extension with new processors
                public abstract class PaymentProcessorBase : IPaymentProcessor
                {
                    public abstract bool CanProcess(PaymentType type);
                    public abstract Task<PaymentResult> ProcessAsync(PaymentRequest request);
                }
                
                public class CreditCardProcessor : PaymentProcessorBase { /* ... */ }
                public class PayPalProcessor : PaymentProcessorBase { /* ... */ }
                public class BitcoinProcessor : PaymentProcessorBase { /* ... */ }
                
                // LSP: All processors can be substituted
                public class PaymentService
                {
                    private readonly IEnumerable<PaymentProcessorBase> _processors;
                    
                    public PaymentService(IEnumerable<PaymentProcessorBase> processors)
                    {
                        _processors = processors;
                    }
                    
                    public async Task<PaymentResult> ProcessAsync(PaymentRequest request)
                    {
                        var processor = _processors.FirstOrDefault(p => p.CanProcess(request.Type));
                        if (processor == null)
                            throw new InvalidOperationException($"No processor for {request.Type}");
                        
                        return await processor.ProcessAsync(request);
                    }
                }
                
                // ISP: Segregated interfaces
                public interface IOrderValidator
                {
                    Task<ValidationResult> ValidateAsync(Order order);
                }
                
                public interface IOrderCalculator
                {
                    Task<decimal> CalculateTotalAsync(Order order);
                }
                
                public interface IOrderProcessor
                {
                    Task<OrderResult> ProcessAsync(Order order);
                }
                
                // DIP: High-level service depends on abstractions
                public class OrderService : IOrderProcessor
                {
                    private readonly IOrderRepository _repository;
                    private readonly IPaymentProcessor _paymentProcessor;
                    private readonly IInventoryService _inventoryService;
                    private readonly INotificationService _notificationService;
                    private readonly IOrderValidator _validator;
                    private readonly IOrderCalculator _calculator;
                    
                    public OrderService(
                        IOrderRepository repository,
                        IPaymentProcessor paymentProcessor,
                        IInventoryService inventoryService,
                        INotificationService notificationService,
                        IOrderValidator validator,
                        IOrderCalculator calculator)
                    {
                        _repository = repository;
                        _paymentProcessor = paymentProcessor;
                        _inventoryService = inventoryService;
                        _notificationService = notificationService;
                        _validator = validator;
                        _calculator = calculator;
                    }
                    
                    public async Task<OrderResult> ProcessAsync(Order order)
                    {
                        // Validate order (SRP: validation separated)
                        var validation = await _validator.ValidateAsync(order);
                        if (!validation.IsValid)
                            return OrderResult.Failure(validation.Errors);
                        
                        // Calculate total (SRP: calculation separated)
                        order.Total = await _calculator.CalculateTotalAsync(order);
                        
                        // Reserve inventory
                        var reserved = await _inventoryService.ReserveItemsAsync(order);
                        if (!reserved)
                            return OrderResult.Failure("Items not available");
                        
                        // Process payment (OCP: extensible processors)
                        var paymentRequest = new PaymentRequest(order);
                        var paymentResult = await _paymentProcessor.ProcessAsync(paymentRequest);
                        if (!paymentResult.Success)
                            return OrderResult.Failure("Payment failed");
                        
                        // Save order (SRP: persistence separated)
                        await _repository.SaveAsync(order);
                        
                        // Send notification (SRP: notification separated)
                        await _notificationService.SendOrderConfirmationAsync(order);
                        
                        return OrderResult.Success(order);
                    }
                }
                
                // Testing is easy with SOLID principles
                [Test]
                public async Task OrderService_ProcessOrder_ValidOrder_Success()
                {
                    // Arrange
                    var mockRepo = new Mock<IOrderRepository>();
                    var mockPayment = new Mock<IPaymentProcessor>();
                    var mockInventory = new Mock<IInventoryService>();
                    var mockNotification = new Mock<INotificationService>();
                    var mockValidator = new Mock<IOrderValidator>();
                    var mockCalculator = new Mock<IOrderCalculator>();
                    
                    mockValidator.Setup(v => v.ValidateAsync(It.IsAny<Order>()))
                        .ReturnsAsync(ValidationResult.Success());
                    mockInventory.Setup(i => i.ReserveItemsAsync(It.IsAny<Order>()))
                        .ReturnsAsync(true);
                    mockPayment.Setup(p => p.ProcessAsync(It.IsAny<PaymentRequest>()))
                        .ReturnsAsync(PaymentResult.Success());
                    mockCalculator.Setup(c => c.CalculateTotalAsync(It.IsAny<Order>()))
                        .ReturnsAsync(100.00m);
                    
                    var service = new OrderService(
                        mockRepo.Object,
                        mockPayment.Object,
                        mockInventory.Object,
                        mockNotification.Object,
                        mockValidator.Object,
                        mockCalculator.Object);
                    
                    var order = new Order();
                    
                    // Act
                    var result = await service.ProcessAsync(order);
                    
                    // Assert
                    Assert.True(result.Success);
                    mockRepo.Verify(r => r.SaveAsync(order), Times.Once);
                    mockNotification.Verify(n => n.SendOrderConfirmationAsync(order), Times.Once);
                }
                """);
            
            // 2. Legacy code refactoring
            Console.WriteLine("\n2. Legacy Code Refactoring to SOLID:");
            Console.WriteLine("""
                Common refactoring steps:
                
                Step 1: Identify violations
                • Look for large classes (SRP violation)
                • Look for switch/if statements for type checking (OCP violation)
                • Look for NotImplementedException (LSP violation)
                • Look for large interfaces (ISP violation)
                • Look for "new" keyword for dependencies (DIP violation)
                
                Step 2: Apply SRP first
                • Extract methods into separate classes
                • Identify distinct responsibilities
                • Create focused classes for each responsibility
                
                Step 3: Apply OCP
                • Replace conditionals with polymorphism
                • Use strategy pattern
                • Create abstractions for variable behavior
                
                Step 4: Apply LSP
                • Ensure subclasses can substitute base classes
                • Fix contract violations
                • Use composition over inheritance when appropriate
                
                Step 5: Apply ISP
                • Split large interfaces
                • Create role-specific interfaces
                • Use interface inheritance for related interfaces
                
                Step 6: Apply DIP
                • Introduce dependency injection
                • Create abstractions for dependencies
                • Move instantiation to composition root
                
                Example: Monolithic class to SOLID
                
                // Before: God class
                public class OrderManager
                {
                    public void ProcessOrder(Order order)
                    {
                        // 200 lines of mixed responsibilities
                        Validate(order);
                        CalculateTotal(order);
                        CheckInventory(order);
                        ProcessPayment(order);
                        SaveToDatabase(order);
                        SendEmail(order);
                        GenerateInvoice(order);
                        UpdateReports(order);
                    }
                }
                
                // After: SOLID refactoring
                public class OrderService
                {
                    private readonly IOrderValidator _validator;
                    private readonly IOrderCalculator _calculator;
                    private readonly IInventoryService _inventory;
                    private readonly IPaymentProcessor _payment;
                    private readonly IOrderRepository _repository;
                    private readonly INotificationService _notification;
                    private readonly IInvoiceService _invoice;
                    private readonly IReportService _report;
                    
                    public OrderService(/* dependencies injected */) { }
                    
                    public void ProcessOrder(Order order)
                    {
                        _validator.Validate(order);
                        _calculator.CalculateTotal(order);
                        _inventory.CheckInventory(order);
                        _payment.ProcessPayment(order);
                        _repository.Save(order);
                        _notification.SendEmail(order);
                        _invoice.GenerateInvoice(order);
                        _report.UpdateReports(order);
                    }
                }
                """);
            
            // 3. SOLID in modern architectures
            Console.WriteLine("\n3. SOLID in Modern Architectures:");
            Console.WriteLine("""
                Microservices:
                • SRP: Each microservice has single bounded context
                • OCP: Services can be extended without modification
                • LSP: Service clients can substitute implementations
                • ISP: Service interfaces are specific to clients
                • DIP: Services depend on contracts, not implementations
                
                Domain-Driven Design (DDD):
                • SRP: Aggregates have single responsibility
                • OCP: Domain events allow extension
                • LSP: Value objects can be substituted
                • ISP: Repository interfaces are specific
                • DIP: Application layer depends on domain abstractions
                
                Clean Architecture:
                • SRP: Each layer has specific responsibility
                • OCP: Use cases can be extended
                • LSP: Entities follow substitution
                • ISP: Gateway interfaces are segregated
                • DIP: Dependencies point inward
                
                CQRS (Command Query Responsibility Segregation):
                • SRP: Separate models for commands and queries
                • OCP: Handlers can be added without modification
                • LSP: Handler interfaces allow substitution
                • ISP: Separate interfaces for commands and queries
                • DIP: Handlers depend on abstractions
                
                Event-Driven Architecture:
                • SRP: Each handler processes specific event
                • OCP: New events can be added
                • LSP: Event handlers can be substituted
                • ISP: Event interfaces are specific
                • DIP: Publishers depend on event abstractions
                """);
        }
        
        static void DemonstrateCodeSmellsAndRefactoring()
        {
            Console.WriteLine("\n=== 7. Code Smells and Refactoring ===\n");
            
            // 1. SOLID violations as code smells
            Console.WriteLine("1. SOLID Violations as Code Smells:");
            Console.WriteLine("""
                SRP Violations (God Class):
                • Class with 500+ lines of code
                • Class imports many unrelated namespaces
                • Class has methods doing different things
                • Class changes frequently for different reasons
                • Difficult to describe class purpose in one sentence
                
                OCP Violations (Switch Statements):
                • Long switch/if-else chains
                • Frequent modifications to add new cases
                • Similar code duplicated in multiple places
                • Type checking with is/as operators
                • Violates "don't call us, we'll call you"
                
                LSP Violations (Inheritance Abuse):
                • Subclasses throwing NotImplementedException
                • Subclasses with empty method implementations
                • Subclasses strengthening preconditions
                • Subclasses weakening postconditions
                • "Is-a" relationship doesn't hold in practice
                
                ISP Violations (Fat Interfaces):
                • Interfaces with 10+ methods
                • Implementations with empty methods
                • Clients using only subset of interface
                • Interface changes affect unrelated clients
                • "I can't implement just part of this"
                
                DIP Violations (Tight Coupling):
                • "new" keyword for dependencies
                • Static method calls (DateTime.Now, Console.WriteLine)
                • Direct instantiation of concrete classes
                • Hard-coded configuration values
                • Difficult to test in isolation
                """);
            
            // 2. Refactoring techniques
            Console.WriteLine("\n2. Refactoring Techniques for SOLID:");
            Console.WriteLine("""
                For SRP violations:
                • Extract Class: Move related methods to new class
                • Extract Method: Break large methods into smaller ones
                • Move Method: Move method to more appropriate class
                • Replace Method with Method Object: For complex methods
                
                For OCP violations:
                • Replace Conditional with Polymorphism
                • Extract Interface: Create abstraction for variable behavior
                • Strategy Pattern: Encapsulate algorithms
                • Template Method Pattern: Define algorithm skeleton
                
                For LSP violations:
                • Replace Inheritance with Delegation
                • Extract Interface: Use interface instead of inheritance
                • Compose instead of Inherit
                • Fix Contract Violations
                
                For ISP violations:
                • Extract Interface: Split large interface
                • Interface Segregation: Create role-specific interfaces
                • Adapter Pattern: Adapt existing interface to client needs
                
                For DIP violations:
                • Extract Interface: Create abstraction for dependency
                • Introduce Parameter: Pass dependency as parameter
                • Constructor Injection: Inject dependencies via constructor
                • Factory Pattern: Abstract object creation
                """);
            
            // 3. SOLID metrics and tools
            Console.WriteLine("\n3. SOLID Metrics and Tools:");
            Console.WriteLine("""
                Code metrics for SOLID:
                • Lines of Code (LOC): >500 suggests SRP violation
                • Cyclomatic Complexity: High complexity suggests OCP violation
                • Depth of Inheritance: >3 suggests LSP issues
                • Class Coupling: High coupling suggests DIP violation
                • Maintainability Index: Low index suggests SOLID violations
                
                Static analysis tools:
                • SonarQube: Detects code smells and SOLID violations
                • ReSharper: Suggests refactorings for SOLID
                • Roslyn Analyzers: Custom rules for SOLID
                • NDepend: Metrics and dependency analysis
                • Code Climate: Maintainability analysis
                
                Refactoring tools:
                • Visual Studio Refactoring: Built-in refactorings
                • ReSharper: Advanced refactoring support
                • Rider: JetBrains IDE with refactoring
                • CodeRush: DevExpress refactoring tool
                
                Testing tools:
                • xUnit/NUnit/MSTest: Unit testing frameworks
                • Moq/NSubstitute: Mocking frameworks
                • AutoFixture: Test data generation
                • FluentAssertions: Readable assertions
                
                Continuous Integration:
                • Run tests on every commit
                • Analyze code metrics
                • Enforce coding standards
                • Monitor technical debt
                """);
            
            // 4. Balancing SOLID with pragmatism
            Console.WriteLine("\n4. Balancing SOLID with Pragmatism:");
            Console.WriteLine("""
                When to apply SOLID:
                • Core business logic
                • Frequently changing code
                • Code with many dependencies
                • Code that needs testing
                • Shared libraries and frameworks
                
                When to be pragmatic:
                • Simple data transfer objects (DTOs)
                • Generated code
                • Proof of concepts
                • Throwaway code
                • Performance-critical sections
                
                Over-engineering risks:
                • Too many small classes
                • Complex dependency graphs
                • Performance overhead
                • Learning curve for team
                • Analysis paralysis
                
                Under-engineering risks:
                • Difficult to maintain
                • High bug rate
                • Slow development over time
                • Difficult to test
                • Technical debt accumulation
                
                Finding the balance:
                • Start simple, refactor when needed
                • Apply SOLID incrementally
                • Consider team experience level
                • Consider project longevity
                • Consider maintenance requirements
                
                Remember: SOLID is means to an end, not the end itself.
                The goal is maintainable, testable, flexible code—not SOLID for SOLID's sake.
                """);
            
            // 5. Continuous improvement
            Console.WriteLine("\n5. Continuous Improvement with SOLID:");
            Console.WriteLine("""
                Learning path:
                1. Understand each principle individually
                2. Recognize violations in your code
                3. Apply refactorings to fix violations
                4. Practice with code katas and exercises
                5. Review code with SOLID in mind
                6. Teach SOLID to others
                
                Team adoption:
                • Code reviews focusing on SOLID
                • Pair programming with SOLID focus
                • Refactoring sessions
                • SOLID workshops and training
                • Incorporate SOLID into definition of done
                
                Measurement and feedback:
                • Track code metrics over time
                • Monitor bug rates and maintenance costs
                • Gather team feedback on maintainability
                • Measure test coverage and ease of testing
                • Review velocity and productivity
                
                Resources for learning:
                • Books: "Clean Code", "Clean Architecture"
                • Online courses: Pluralsight, Udemy
                • Blogs: Martin Fowler, Uncle Bob
                • Communities: Stack Overflow, Reddit
                • Practice: Refactor existing code
                
                Final advice:
                • SOLID principles work together
                • Start with one principle at a time
                • Refactor legacy code gradually
                • Write tests before refactoring
                • SOLID leads to better software over time
                """);
        }
    }
    
    // Supporting classes for examples
    public class Order
    {
        public int Id { get; set; }
        public decimal Total { get; set; }
        public List<OrderItem> Items { get; set; } = new List<OrderItem>();
    }
    
    public class OrderItem
    {
        public int ProductId { get; set; }
        public int Quantity { get; set; }
        public decimal Price { get; set; }
    }
    
    public class PaymentRequest
    {
        public Order Order { get; }
        public PaymentType Type { get; set; }
        
        public PaymentRequest(Order order)
        {
            Order = order;
        }
    }
    
    public class PaymentResult
    {
        public bool Success { get; set; }
        public string TransactionId { get; set; }
        
        public static PaymentResult SuccessResult(string transactionId = null) =>
            new PaymentResult { Success = true, TransactionId = transactionId };
    }
    
    public class OrderResult
    {
        public bool Success { get; set; }
        public List<string> Errors { get; set; } = new List<string>();
        public Order Order { get; set; }
        
        public static OrderResult SuccessResult(Order order) =>
            new OrderResult { Success = true, Order = order };
            
        public static OrderResult Failure(params string[] errors) =>
            new OrderResult { Success = false, Errors = errors.ToList() };
    }
    
    public class ValidationResult
    {
        public bool IsValid { get; set; }
        public List<string> Errors { get; set; } = new List<string>();
        
        public static ValidationResult Success() =>
            new ValidationResult { IsValid = true };
            
        public static ValidationResult Failure(params string[] errors) =>
            new ValidationResult { IsValid = false, Errors = errors.ToList() };
    }
    
    public enum PaymentType
    {
        CreditCard,
        PayPal,
        Bitcoin
    }
}
