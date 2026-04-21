/*
    C# INHERITANCE AND POLYMORPHISM
    File: 04_inheritance_polymorphism.cs
    
    This file demonstrates inheritance and polymorphism in C# programming,
    covering concepts from junior to upper mid-level. Inheritance allows
    classes to derive from other classes, while polymorphism enables
    objects to be treated as instances of their base class.
    
    Key Concepts Covered:
    1. Basic Inheritance (Single Inheritance)
    2. Method Overriding (virtual/override)
    3. Abstract Classes and Methods
    4. Sealed Classes and Methods
    5. Polymorphism and Type Casting
    6. Constructors in Inheritance Chains
    7. Base Keyword and Protected Access
    8. Interfaces vs Abstract Classes
    9. Composition vs Inheritance
    10. Real-world Inheritance Patterns
*/

using System;
using System.Collections.Generic;

namespace CSharpRefresher.InheritancePolymorphism
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Inheritance and Polymorphism Demonstration ===\n");
            
            DemonstrateBasicInheritance();
            DemonstrateMethodOverriding();
            DemonstrateAbstractClasses();
            DemonstrateSealedClasses();
            DemonstratePolymorphism();
            DemonstrateConstructorsInInheritance();
            DemonstrateBaseAndProtected();
            DemonstrateInterfacesVsAbstractClasses();
            DemonstrateCompositionVsInheritance();
            DemonstrateRealWorldPatterns();
            
            Console.WriteLine("\n=== Inheritance and Polymorphism Complete ===");
        }
        
        static void DemonstrateBasicInheritance()
        {
            Console.WriteLine("============ BASIC INHERITANCE ============\n");
            
            // ============ SINGLE INHERITANCE ============
            Console.WriteLine("=== 1. Single Inheritance ===");
            
            // Base class
            class Vehicle
            {
                public string Make { get; set; }
                public string Model { get; set; }
                public int Year { get; set; }
                
                public Vehicle(string make, string model, int year)
                {
                    Make = make;
                    Model = model;
                    Year = year;
                }
                
                public virtual void Start()
                {
                    Console.WriteLine($"{Make} {Model} starting...");
                }
                
                public void DisplayInfo()
                {
                    Console.WriteLine($"{Year} {Make} {Model}");
                }
            }
            
            // Derived class
            class Car : Vehicle
            {
                public int Doors { get; set; }
                
                public Car(string make, string model, int year, int doors) 
                    : base(make, model, year)
                {
                    Doors = doors;
                }
                
                public void DisplayCarInfo()
                {
                    DisplayInfo(); // Inherited method
                    Console.WriteLine($"Doors: {Doors}");
                }
            }
            
            // Usage
            Vehicle vehicle = new Vehicle("Generic", "Vehicle", 2020);
            Car car = new Car("Toyota", "Camry", 2023, 4);
            
            vehicle.DisplayInfo();
            car.DisplayCarInfo();
            car.Start(); // Inherited from Vehicle
            
            // ============ INHERITANCE HIERARCHY ============
            Console.WriteLine("\n=== 2. Inheritance Hierarchy ===");
            
            class Truck : Vehicle
            {
                public double LoadCapacity { get; set; }
                
                public Truck(string make, string model, int year, double loadCapacity)
                    : base(make, model, year)
                {
                    LoadCapacity = loadCapacity;
                }
                
                public void LoadCargo()
                {
                    Console.WriteLine($"Loading {LoadCapacity} tons of cargo");
                }
            }
            
            class ElectricCar : Car
            {
                public int BatteryRange { get; set; }
                
                public ElectricCar(string make, string model, int year, int doors, int batteryRange)
                    : base(make, model, year, doors)
                {
                    BatteryRange = batteryRange;
                }
                
                public void Charge()
                {
                    Console.WriteLine($"Charging battery for {BatteryRange} km range");
                }
            }
            
            // Create hierarchy
            Truck truck = new Truck("Ford", "F-150", 2024, 2.5);
            ElectricCar tesla = new ElectricCar("Tesla", "Model 3", 2024, 4, 500);
            
            truck.LoadCargo();
            tesla.Charge();
            tesla.DisplayCarInfo(); // From Car class
        }
        
        static void DemonstrateMethodOverriding()
        {
            Console.WriteLine("\n============ METHOD OVERRIDING ============\n");
            
            // ============ VIRTUAL AND OVERRIDE ============
            Console.WriteLine("=== 1. Virtual and Override Keywords ===");
            
            class Animal
            {
                public string Name { get; set; }
                
                public Animal(string name)
                {
                    Name = name;
                }
                
                // Virtual method - can be overridden
                public virtual void MakeSound()
                {
                    Console.WriteLine($"{Name} makes a generic animal sound");
                }
                
                // Non-virtual method - cannot be overridden (but can be hidden with 'new')
                public void Eat()
                {
                    Console.WriteLine($"{Name} is eating");
                }
            }
            
            class Dog : Animal
            {
                public Dog(string name) : base(name) { }
                
                // Override virtual method
                public override void MakeSound()
                {
                    Console.WriteLine($"{Name} barks: Woof! Woof!");
                }
                
                // Hide base method with 'new' keyword (not recommended generally)
                public new void Eat()
                {
                    Console.WriteLine($"{Name} eats bones");
                    base.Eat(); // Can still call base implementation
                }
            }
            
            class Cat : Animal
            {
                public Cat(string name) : base(name) { }
                
                public override void MakeSound()
                {
                    Console.WriteLine($"{Name} meows: Meow!");
                }
            }
            
            // Demonstrate overriding
            Animal genericAnimal = new Animal("Generic");
            Dog dog = new Dog("Buddy");
            Cat cat = new Cat("Whiskers");
            
            genericAnimal.MakeSound();
            dog.MakeSound();
            cat.MakeSound();
            
            Console.WriteLine("\n=== 2. Base Method Calling ===");
            dog.Eat(); // Calls Dog.Eat()
            ((Animal)dog).Eat(); // Calls Animal.Eat() due to hiding, not overriding
            
            // ============ METHOD HIDING WARNING ============
            Console.WriteLine("\n=== 3. Method Hiding (Warning) ===");
            
            Animal animalDog = new Dog("Rex");
            animalDog.MakeSound(); // Calls Dog.MakeSound() (polymorphism works)
            animalDog.Eat(); // Calls Animal.Eat() (hiding, not polymorphism)
        }
        
        static void DemonstrateAbstractClasses()
        {
            Console.WriteLine("\n============ ABSTRACT CLASSES ============\n");
            
            // ============ ABSTRACT CLASSES AND METHODS ============
            Console.WriteLine("=== 1. Abstract Classes ===");
            
            abstract class Shape
            {
                public string Name { get; }
                
                protected Shape(string name)
                {
                    Name = name;
                }
                
                // Abstract method - must be implemented by derived classes
                public abstract double CalculateArea();
                
                // Abstract property
                public abstract int Sides { get; }
                
                // Concrete method in abstract class
                public void DisplayInfo()
                {
                    Console.WriteLine($"Shape: {Name}");
                    Console.WriteLine($"Sides: {Sides}");
                    Console.WriteLine($"Area: {CalculateArea():F2}");
                }
                
                // Virtual method with default implementation
                public virtual void Draw()
                {
                    Console.WriteLine($"Drawing {Name}");
                }
            }
            
            class Circle : Shape
            {
                public double Radius { get; }
                
                public Circle(double radius) : base("Circle")
                {
                    Radius = radius;
                }
                
                // Must implement abstract methods
                public override double CalculateArea()
                {
                    return Math.PI * Radius * Radius;
                }
                
                public override int Sides => 0; // Circle has 0 sides
                
                // Can override virtual methods
                public override void Draw()
                {
                    Console.WriteLine($"Drawing circle with radius {Radius}");
                }
            }
            
            class Rectangle : Shape
            {
                public double Width { get; }
                public double Height { get; }
                
                public Rectangle(double width, double height) : base("Rectangle")
                {
                    Width = width;
                    Height = height;
                }
                
                public override double CalculateArea()
                {
                    return Width * Height;
                }
                
                public override int Sides => 4;
                
                // Additional method specific to Rectangle
                public double CalculateDiagonal()
                {
                    return Math.Sqrt(Width * Width + Height * Height);
                }
            }
            
            // Cannot instantiate abstract class
            // Shape shape = new Shape(); // Error
            
            // Can instantiate concrete derived classes
            Circle circle = new Circle(5.0);
            Rectangle rectangle = new Rectangle(4.0, 6.0);
            
            circle.DisplayInfo();
            rectangle.DisplayInfo();
            Console.WriteLine($"Rectangle diagonal: {rectangle.CalculateDiagonal():F2}");
            
            // ============ ABSTRACT CLASS AS BASE ============
            Console.WriteLine("\n=== 2. Abstract Class as Base ===");
            
            abstract class DatabaseConnection
            {
                public string ConnectionString { get; }
                
                protected DatabaseConnection(string connectionString)
                {
                    ConnectionString = connectionString;
                }
                
                public abstract void Open();
                public abstract void Close();
                public abstract void ExecuteQuery(string query);
                
                // Template method pattern
                public void RunTransaction(Action<DatabaseConnection> transaction)
                {
                    Open();
                    try
                    {
                        transaction(this);
                        Console.WriteLine("Transaction completed successfully");
                    }
                    finally
                    {
                        Close();
                    }
                }
            }
            
            class SqlConnection : DatabaseConnection
            {
                public SqlConnection(string connectionString) : base(connectionString) { }
                
                public override void Open()
                {
                    Console.WriteLine($"Opening SQL connection: {ConnectionString}");
                }
                
                public override void Close()
                {
                    Console.WriteLine("Closing SQL connection");
                }
                
                public override void ExecuteQuery(string query)
                {
                    Console.WriteLine($"Executing SQL query: {query}");
                }
            }
            
            SqlConnection sql = new SqlConnection("Server=localhost;Database=Test;");
            sql.RunTransaction(db => 
            {
                db.ExecuteQuery("BEGIN TRANSACTION");
                db.ExecuteQuery("INSERT INTO Users VALUES ('Alice')");
                db.ExecuteQuery("COMMIT");
            });
        }
        
        static void DemonstrateSealedClasses()
        {
            Console.WriteLine("\n============ SEALED CLASSES AND METHODS ============\n");
            
            // ============ SEALED CLASSES ============
            Console.WriteLine("=== 1. Sealed Classes ===");
            
            class BaseClass
            {
                public virtual void Method1() => Console.WriteLine("Base.Method1");
                public virtual void Method2() => Console.WriteLine("Base.Method2");
            }
            
            class DerivedClass : BaseClass
            {
                public sealed override void Method1() => Console.WriteLine("Derived.Method1 (sealed)");
                public override void Method2() => Console.WriteLine("Derived.Method2");
            }
            
            // Sealed class - cannot be inherited from
            sealed class SealedClass : DerivedClass
            {
                // Cannot override Method1 - it's sealed in DerivedClass
                // public override void Method1() => Console.WriteLine("Sealed.Method1"); // Error
                
                public override void Method2() => Console.WriteLine("Sealed.Method2");
            }
            
            // class FurtherDerived : SealedClass { } // Error: cannot derive from sealed class
            
            SealedClass sealedObj = new SealedClass();
            sealedObj.Method1(); // Calls Derived.Method1
            sealedObj.Method2(); // Calls Sealed.Method2
            
            // ============ SEALED METHODS ============
            Console.WriteLine("\n=== 2. Sealed Methods ===");
            
            class Payment
            {
                public virtual void Process()
                {
                    Console.WriteLine("Processing generic payment");
                }
            }
            
            class CreditCardPayment : Payment
            {
                public sealed override void Process()
                {
                    Console.WriteLine("Processing credit card payment");
                    ValidateCard();
                    ChargeCard();
                }
                
                private void ValidateCard() => Console.WriteLine("Validating card");
                private void ChargeCard() => Console.WriteLine("Charging card");
            }
            
            // Sealing a method prevents further overriding
            // Useful when you want to lock down implementation in a hierarchy
            
            Console.WriteLine("Sealed methods prevent further overriding in derived classes");
        }
        
        static void DemonstratePolymorphism()
        {
            Console.WriteLine("\n============ POLYMORPHISM ============\n");
            
            // ============ POLYMORPHISM BASICS ============
            Console.WriteLine("=== 1. Polymorphism Basics ===");
            
            class Employee
            {
                public string Name { get; }
                public decimal Salary { get; protected set; }
                
                public Employee(string name, decimal salary)
                {
                    Name = name;
                    Salary = salary;
                }
                
                public virtual void Work()
                {
                    Console.WriteLine($"{Name} is working");
                }
                
                public virtual decimal CalculateBonus()
                {
                    return Salary * 0.1m; // 10% bonus
                }
                
                public void DisplayInfo()
                {
                    Console.WriteLine($"{Name}: Salary=${Salary}, Bonus=${CalculateBonus():F2}");
                }
            }
            
            class Manager : Employee
            {
                public int TeamSize { get; }
                
                public Manager(string name, decimal salary, int teamSize) 
                    : base(name, salary)
                {
                    TeamSize = teamSize;
                }
                
                public override void Work()
                {
                    Console.WriteLine($"{Name} is managing a team of {TeamSize} people");
                }
                
                public override decimal CalculateBonus()
                {
                    return Salary * 0.2m + TeamSize * 1000; // 20% + per team member
                }
            }
            
            class Developer : Employee
            {
                public string ProgrammingLanguage { get; }
                
                public Developer(string name, decimal salary, string language) 
                    : base(name, salary)
                {
                    ProgrammingLanguage = language;
                }
                
                public override void Work()
                {
                    Console.WriteLine($"{Name} is coding in {ProgrammingLanguage}");
                }
                
                public override decimal CalculateBonus()
                {
                    return Salary * 0.15m + (ProgrammingLanguage == "C#" ? 5000 : 2000);
                }
            }
            
            // Polymorphism in action
            List<Employee> employees = new List<Employee>
            {
                new Employee("Generic", 50000),
                new Manager("Alice", 80000, 5),
                new Developer("Bob", 70000, "C#"),
                new Developer("Charlie", 65000, "Java")
            };
            
            Console.WriteLine("Employees working:");
            foreach (var emp in employees)
            {
                emp.Work(); // Calls appropriate overridden method
            }
            
            Console.WriteLine("\nEmployee bonuses:");
            foreach (var emp in employees)
            {
                emp.DisplayInfo(); // Uses polymorphic CalculateBonus()
            }
            
            // ============ TYPE CHECKING AND CASTING ============
            Console.WriteLine("\n=== 2. Type Checking and Casting ===");
            
            foreach (var emp in employees)
            {
                // is operator - type checking
                if (emp is Manager manager)
                {
                    Console.WriteLine($"{manager.Name} is a manager with team size {manager.TeamSize}");
                }
                
                // as operator - safe casting
                Developer developer = emp as Developer;
                if (developer != null)
                {
                    Console.WriteLine($"{developer.Name} codes in {developer.ProgrammingLanguage}");
                }
                
                // GetType() and typeof()
                Type empType = emp.GetType();
                Type managerType = typeof(Manager);
                
                if (empType == managerType)
                {
                    Console.WriteLine($"Type match: {emp.Name} is a Manager");
                }
            }
            
            // Explicit casting
            try
            {
                Employee emp = employees[1]; // Manager
                Manager m = (Manager)emp; // Explicit cast
                Console.WriteLine($"Successfully cast to Manager: {m.TeamSize}");
                
                // Invalid cast exception
                Developer d = (Developer)emp; // Throws InvalidCastException
            }
            catch (InvalidCastException ex)
            {
                Console.WriteLine($"Invalid cast: {ex.Message}");
            }
        }
        
        static void DemonstrateConstructorsInInheritance()
        {
            Console.WriteLine("\n============ CONSTRUCTORS IN INHERITANCE ============\n");
            
            // ============ CONSTRUCTOR CHAINING ============
            Console.WriteLine("=== 1. Constructor Chaining ===");
            
            class Person
            {
                public string FirstName { get; }
                public string LastName { get; }
                public int Age { get; }
                
                // Base constructor
                public Person(string firstName, string lastName, int age)
                {
                    FirstName = firstName;
                    LastName = lastName;
                    Age = age;
                    Console.WriteLine($"Person constructor: {FirstName} {LastName}, Age: {Age}");
                }
                
                // Constructor chaining with 'this'
                public Person(string firstName, string lastName) 
                    : this(firstName, lastName, 0) // Calls 3-parameter constructor
                {
                    Console.WriteLine($"Person 2-param constructor called");
                }
            }
            
            class Student : Person
            {
                public string StudentId { get; }
                public string Major { get; }
                
                // Must call base constructor
                public Student(string firstName, string lastName, int age, string studentId, string major)
                    : base(firstName, lastName, age) // Calls base constructor
                {
                    StudentId = studentId;
                    Major = major;
                    Console.WriteLine($"Student constructor: ID={StudentId}, Major={Major}");
                }
                
                // Constructor with default age
                public Student(string firstName, string lastName, string studentId, string major)
                    : this(firstName, lastName, 18, studentId, major) // Calls other Student constructor
                {
                    Console.WriteLine("Student default-age constructor");
                }
            }
            
            class GraduateStudent : Student
            {
                public string ThesisTopic { get; }
                
                public GraduateStudent(string firstName, string lastName, int age, 
                    string studentId, string major, string thesisTopic)
                    : base(firstName, lastName, age, studentId, major)
                {
                    ThesisTopic = thesisTopic;
                    Console.WriteLine($"GraduateStudent constructor: Thesis={ThesisTopic}");
                }
            }
            
            Console.WriteLine("Creating GraduateStudent:");
            GraduateStudent grad = new GraduateStudent("Alice", "Smith", 25, 
                "S12345", "Computer Science", "Machine Learning");
            
            // ============ STATIC CONSTRUCTORS ============
            Console.WriteLine("\n=== 2. Static Constructors in Inheritance ===");
            
            class BaseWithStatic
            {
                static BaseWithStatic()
                {
                    Console.WriteLine("Base static constructor");
                }
                
                public BaseWithStatic()
                {
                    Console.WriteLine("Base instance constructor");
                }
            }
            
            class DerivedWithStatic : BaseWithStatic
            {
                static DerivedWithStatic()
                {
                    Console.WriteLine("Derived static constructor");
                }
                
                public DerivedWithStatic()
                {
                    Console.WriteLine("Derived instance constructor");
                }
            }
            
            Console.WriteLine("First instance of DerivedWithStatic:");
            new DerivedWithStatic();
            
            Console.WriteLine("\nSecond instance of DerivedWithStatic:");
            new DerivedWithStatic();
        }
        
        static void DemonstrateBaseAndProtected()
        {
            Console.WriteLine("\n============ BASE KEYWORD AND PROTECTED ACCESS ============\n");
            
            // ============ BASE KEYWORD ============
            Console.WriteLine("=== 1. Base Keyword ===");
            
            class Device
            {
                protected string SerialNumber;
                protected bool IsPoweredOn;
                
                public Device(string serialNumber)
                {
                    SerialNumber = serialNumber;
                    IsPoweredOn = false;
                }
                
                public virtual void PowerOn()
                {
                    IsPoweredOn = true;
                    Console.WriteLine($"Device {SerialNumber} powered on");
                }
                
                protected void Log(string message)
                {
                    Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] {message}");
                }
            }
            
            class SmartDevice : Device
            {
                private string FirmwareVersion;
                
                public SmartDevice(string serialNumber, string firmwareVersion) 
                    : base(serialNumber) // Call base constructor
                {
                    FirmwareVersion = firmwareVersion;
                }
                
                public override void PowerOn()
                {
                    // Call base implementation
                    base.PowerOn();
                    
                    // Additional functionality
                    Log($"Starting firmware {FirmwareVersion}");
                    InitializeComponents();
                    Console.WriteLine($"Smart device {SerialNumber} ready");
                }
                
                private void InitializeComponents()
                {
                    Log("Initializing components");
                }
                
                // Can access protected members
                public void DisplayInfo()
                {
                    Console.WriteLine($"Serial: {SerialNumber}, Firmware: {FirmwareVersion}, Powered: {IsPoweredOn}");
                }
            }
            
            SmartDevice device = new SmartDevice("SN12345", "v2.1.0");
            device.PowerOn();
            device.DisplayInfo();
            
            // ============ PROTECTED ACCESS MODIFIER ============
            Console.WriteLine("\n=== 2. Protected Access Modifier ===");
            
            class BankAccount
            {
                protected decimal balance;
                private string accountNumber;
                
                public BankAccount(string accountNumber, decimal initialBalance)
                {
                    this.accountNumber = accountNumber;
                    balance = initialBalance;
                }
                
                public decimal GetBalance() => balance;
                
                protected virtual void UpdateBalance(decimal amount)
                {
                    balance += amount;
                    Console.WriteLine($"Balance updated by {amount:C}. New balance: {balance:C}");
                }
            }
            
            class SavingsAccount : BankAccount
            {
                private decimal interestRate;
                
                public SavingsAccount(string accountNumber, decimal initialBalance, decimal interestRate)
                    : base(accountNumber, initialBalance)
                {
                    this.interestRate = interestRate;
                }
                
                public void AddInterest()
                {
                    decimal interest = balance * interestRate;
                    // Can access protected balance and UpdateBalance
                    UpdateBalance(interest);
                    Console.WriteLine($"Added interest: {interest:C}");
                }
                
                // Cannot access private accountNumber
                // public string GetAccountNumber() => accountNumber; // Error
                
                protected override void UpdateBalance(decimal amount)
                {
                    base.UpdateBalance(amount);
                    LogTransaction(amount);
                }
                
                private void LogTransaction(decimal amount)
                {
                    Console.WriteLine($"Logged transaction: {amount:C}");
                }
            }
            
            SavingsAccount savings = new SavingsAccount("SAV123", 1000m, 0.05m);
            savings.AddInterest();
            Console.WriteLine($"Savings balance: {savings.GetBalance():C}");
        }
        
        static void DemonstrateInterfacesVsAbstractClasses()
        {
            Console.WriteLine("\n============ INTERFACES VS ABSTRACT CLASSES ============\n");
            
            // ============ COMPARISON ============
            Console.WriteLine("=== 1. Comparison Table ===");
            Console.WriteLine("""
                Abstract Classes:
                • Can have implementation (concrete methods)
                • Can have fields, properties, methods, constructors
                • Single inheritance only
                • Can have access modifiers (public, protected, etc.)
                • Good for "is-a" relationships with shared implementation
                
                Interfaces:
                • No implementation (until C# 8.0 default methods)
                • Can only have methods, properties, events, indexers
                • Multiple inheritance allowed
                • Members are public by default
                • Good for "can-do" relationships (capabilities)
                """);
            
            // ============ WHEN TO USE WHICH ============
            Console.WriteLine("\n=== 2. When to Use Which ===");
            
            // Example: Abstract class for shared implementation
            abstract class DataExporter
            {
                protected string data;
                
                public DataExporter(string data)
                {
                    this.data = data;
                }
                
                // Shared implementation
                public void ValidateData()
                {
                    if (string.IsNullOrEmpty(data))
                        throw new ArgumentException("Data cannot be empty");
                    Console.WriteLine("Data validated");
                }
                
                // Template method pattern
                public void Export()
                {
                    ValidateData();
                    TransformData();
                    WriteOutput();
                    Console.WriteLine("Export completed");
                }
                
                protected abstract void TransformData();
                protected abstract void WriteOutput();
            }
            
            class CsvExporter : DataExporter
            {
                public CsvExporter(string data) : base(data) { }
                
                protected override void TransformData()
                {
                    Console.WriteLine("Transforming data to CSV format");
                }
                
                protected override void WriteOutput()
                {
                    Console.WriteLine("Writing CSV to file");
                }
            }
            
            // Example: Interface for capabilities
            interface ILoggable
            {
                void Log(string message);
            }
            
            interface IAuditable
            {
                DateTime Created { get; }
                string CreatedBy { get; }
            }
            
            interface IValidatable
            {
                bool Validate();
            }
            
            // Class can implement multiple interfaces
            class Document : ILoggable, IAuditable, IValidatable
            {
                public string Content { get; set; }
                public DateTime Created { get; } = DateTime.Now;
                public string CreatedBy { get; } = "System";
                
                public void Log(string message)
                {
                    Console.WriteLine($"[Document] {message}");
                }
                
                public bool Validate()
                {
                    return !string.IsNullOrEmpty(Content);
                }
            }
            
            // ============ DEFAULT INTERFACE METHODS (C# 8.0+) ============
            Console.WriteLine("\n=== 3. Default Interface Methods (C# 8.0+) ===");
            
            interface IRepository<T>
            {
                // Abstract method
                void Add(T item);
                
                // Default method with implementation
                void AddRange(IEnumerable<T> items)
                {
                    foreach (var item in items)
                    {
                        Add(item);
                    }
                    Console.WriteLine($"Added {items.Count()} items");
                }
                
                // Static method
                static int GetDefaultPageSize() => 10;
            }
            
            class ProductRepository : IRepository<string>
            {
                private List<string> items = new List<string>();
                
                public void Add(string item)
                {
                    items.Add(item);
                    Console.WriteLine($"Added: {item}");
                }
                
                // Can override default method
                public void AddRange(IEnumerable<string> items)
                {
                    Console.WriteLine("Custom AddRange implementation");
                    this.items.AddRange(items);
                }
            }
            
            ProductRepository repo = new ProductRepository();
            repo.Add("Product 1");
            repo.AddRange(new[] { "Product 2", "Product 3" });
            Console.WriteLine($"Default page size: {IRepository<string>.GetDefaultPageSize()}");
        }
        
        static void DemonstrateCompositionVsInheritance()
        {
            Console.WriteLine("\n============ COMPOSITION VS INHERITANCE ============\n");
            
            // ============ COMPOSITION EXAMPLE ============
            Console.WriteLine("=== 1. Composition (Has-a Relationship) ===");
            
            // Small, focused classes
            class Engine
            {
                public void Start() => Console.WriteLine("Engine started");
                public void Stop() => Console.WriteLine("Engine stopped");
            }
            
            class Transmission
            {
                public void ShiftGear(int gear) => Console.WriteLine($"Shifted to gear {gear}");
            }
            
            class Stereo
            {
                public void PlayMusic(string song) => Console.WriteLine($"Playing: {song}");
            }
            
            // Car composed of these parts
            class CarComposition
            {
                private Engine engine = new Engine();
                private Transmission transmission = new Transmission();
                private Stereo stereo = new Stereo();
                
                public void Drive()
                {
                    engine.Start();
                    transmission.ShiftGear(1);
                    Console.WriteLine("Car is driving");
                }
                
                public void Entertainment(string song)
                {
                    stereo.PlayMusic(song);
                }
                
                // Can swap components
                public void UpgradeStereo(Stereo newStereo)
                {
                    stereo = newStereo;
                    Console.WriteLine("Stereo upgraded");
                }
            }
            
            // ============ INHERITANCE EXAMPLE ============
            Console.WriteLine("\n=== 2. Inheritance (Is-a Relationship) ===");
            
            class VehicleInheritance
            {
                public virtual void Move() => Console.WriteLine("Vehicle moving");
            }
            
            class CarInheritance : VehicleInheritance
            {
                public override void Move()
                {
                    base.Move();
                    Console.WriteLine("Car driving on road");
                }
            }
            
            class AirplaneInheritance : VehicleInheritance
            {
                public override void Move()
                {
                    base.Move();
                    Console.WriteLine("Airplane flying");
                }
            }
            
            // ============ FAVOR COMPOSITION OVER INHERITANCE ============
            Console.WriteLine("\n=== 3. Favor Composition Over Inheritance ===");
            
            // Problem with deep inheritance hierarchies
            class AnimalProblem
            {
                public void Eat() => Console.WriteLine("Eating");
            }
            
            class MammalProblem : AnimalProblem
            {
                public void Breathe() => Console.WriteLine("Breathing air");
            }
            
            class DogProblem : MammalProblem
            {
                public void Bark() => Console.WriteLine("Barking");
            }
            
            // What if we need a Dog that doesn't breathe air?
            // Inheritance forces certain behaviors
            
            // Solution with composition
            interface IEatingBehavior { void Eat(); }
            interface IBreathingBehavior { void Breathe(); }
            interface ISoundBehavior { void MakeSound(); }
            
            class EatingBehavior : IEatingBehavior
            {
                public void Eat() => Console.WriteLine("Eating");
            }
            
            class AirBreathing : IBreathingBehavior
            {
                public void Breathe() => Console.WriteLine("Breathing air");
            }
            
            class WaterBreathing : IBreathingBehavior
            {
                public void Breathe() => Console.WriteLine("Breathing water");
            }
            
            class BarkingSound : ISoundBehavior
            {
                public void MakeSound() => Console.WriteLine("Barking");
            }
            
            class AnimalComposition
            {
                private IEatingBehavior eating;
                private IBreathingBehavior breathing;
                private ISoundBehavior sound;
                
                public AnimalComposition(IEatingBehavior eating, IBreathingBehavior breathing, ISoundBehavior sound)
                {
                    this.eating = eating;
                    this.breathing = breathing;
                    this.sound = sound;
                }
                
                public void Live()
                {
                    breathing.Breathe();
                    eating.Eat();
                    sound.MakeSound();
                }
            }
            
            // Create different animals by composition
            AnimalComposition landDog = new AnimalComposition(
                new EatingBehavior(), new AirBreathing(), new BarkingSound());
            
            Console.WriteLine("Land dog:");
            landDog.Live();
            
            // Can easily create a "water dog" without changing hierarchy
            // Not realistic biologically, but demonstrates flexibility
        }
        
        static void DemonstrateRealWorldPatterns()
        {
            Console.WriteLine("\n============ REAL-WORLD INHERITANCE PATTERNS ============\n");
            
            // ============ STRATEGY PATTERN ============
            Console.WriteLine("=== 1. Strategy Pattern ===");
            
            interface IPaymentStrategy
            {
                void ProcessPayment(decimal amount);
            }
            
            class CreditCardPayment : IPaymentStrategy
            {
                public void ProcessPayment(decimal amount)
                {
                    Console.WriteLine($"Processing credit card payment of {amount:C}");
                }
            }
            
            class PayPalPayment : IPaymentStrategy
            {
                public void ProcessPayment(decimal amount)
                {
                    Console.WriteLine($"Processing PayPal payment of {amount:C}");
                }
            }
            
            class PaymentProcessor
            {
                private IPaymentStrategy strategy;
                
                public void SetPaymentStrategy(IPaymentStrategy strategy)
                {
                    this.strategy = strategy;
                }
                
                public void Process(decimal amount)
                {
                    strategy?.ProcessPayment(amount);
                }
            }
            
            PaymentProcessor processor = new PaymentProcessor();
            processor.SetPaymentStrategy(new CreditCardPayment());
            processor.Process(100m);
            processor.SetPaymentStrategy(new PayPalPayment());
            processor.Process(50m);
            
            // ============ TEMPLATE METHOD PATTERN ============
            Console.WriteLine("\n=== 2. Template Method Pattern ===");
            
            abstract class DataProcessor
            {
                // Template method - defines algorithm skeleton
                public void Process()
                {
                    LoadData();
                    TransformData();
                    ValidateData();
                    SaveData();
                    LogResult();
                }
                
                protected virtual void LoadData()
                {
                    Console.WriteLine("Loading data from default source");
                }
                
                protected abstract void TransformData();
                
                protected virtual void ValidateData()
                {
                    Console.WriteLine("Validating data with default rules");
                }
                
                protected abstract void SaveData();
                
                protected virtual void LogResult()
                {
                    Console.WriteLine("Processing completed");
                }
            }
            
            class CustomerDataProcessor : DataProcessor
            {
                protected override void LoadData()
                {
                    Console.WriteLine("Loading customer data from database");
                }
                
                protected override void TransformData()
                {
                    Console.WriteLine("Transforming customer data: cleaning and formatting");
                }
                
                protected override void SaveData()
                {
                    Console.WriteLine("Saving customer data to CRM system");
                }
            }
            
            CustomerDataProcessor customerProcessor = new CustomerDataProcessor();
            customerProcessor.Process();
            
            // ============ DECORATOR PATTERN ============
            Console.WriteLine("\n=== 3. Decorator Pattern ===");
            
            interface IMessage
            {
                void Send(string message);
            }
            
            class BasicMessage : IMessage
            {
                public void Send(string message)
                {
                    Console.WriteLine($"Sending message: {message}");
                }
            }
            
            abstract class MessageDecorator : IMessage
            {
                protected IMessage decoratedMessage;
                
                public MessageDecorator(IMessage message)
                {
                    decoratedMessage = message;
                }
                
                public virtual void Send(string message)
                {
                    decoratedMessage.Send(message);
                }
            }
            
            class EncryptedMessage : MessageDecorator
            {
                public EncryptedMessage(IMessage message) : base(message) { }
                
                public override void Send(string message)
                {
                    string encrypted = $"ENCRYPTED({message})";
                    base.Send(encrypted);
                }
            }
            
            class TimestampedMessage : MessageDecorator
            {
                public TimestampedMessage(IMessage message) : base(message) { }
                
                public override void Send(string message)
                {
                    string timestamped = $"[{DateTime.Now:HH:mm:ss}] {message}";
                    base.Send(timestamped);
                }
            }
            
            IMessage message = new BasicMessage();
            message.Send("Hello"); // Basic
            
            message = new EncryptedMessage(message);
            message.Send("Hello"); // Encrypted
            
            message = new TimestampedMessage(new EncryptedMessage(new BasicMessage()));
            message.Send("Hello"); // Timestamped and encrypted
            
            // ============ FACTORY METHOD PATTERN ============
            Console.WriteLine("\n=== 4. Factory Method Pattern ===");
            
            abstract class DocumentCreator
            {
                public void CreateAndSave()
                {
                    Document doc = CreateDocument();
                    doc.AddContent("Sample content");
                    doc.Save();
                }
                
                protected abstract Document CreateDocument();
            }
            
            abstract class Document
            {
                public abstract void AddContent(string content);
                public abstract void Save();
            }
            
            class PdfDocument : Document
            {
                public override void AddContent(string content)
                {
                    Console.WriteLine($"Adding content to PDF: {content}");
                }
                
                public override void Save()
                {
                    Console.WriteLine("Saving PDF document");
                }
            }
            
            class WordDocument : Document
            {
                public override void AddContent(string content)
                {
                    Console.WriteLine($"Adding content to Word: {content}");
                }
                
                public override void Save()
                {
                    Console.WriteLine("Saving Word document");
                }
            }
            
            class PdfCreator : DocumentCreator
            {
                protected override Document CreateDocument() => new PdfDocument();
            }
            
            class WordCreator : DocumentCreator
            {
                protected override Document CreateDocument() => new WordDocument();
            }
            
            DocumentCreator pdfFactory = new PdfCreator();
            pdfFactory.CreateAndSave();
            
            DocumentCreator wordFactory = new WordCreator();
            wordFactory.CreateAndSave();
            
            Console.WriteLine("\n=== Summary ===");
            Console.WriteLine("""
                Inheritance and polymorphism are fundamental OOP concepts in C#:
                
                1. Use inheritance for "is-a" relationships with shared implementation
                2. Use interfaces for "can-do" relationships and multiple capabilities
                3. Prefer composition over inheritance for flexibility
                4. Use abstract classes when you need shared implementation
                5. Use sealed classes/methods to prevent further inheritance when appropriate
                6. Understand constructor chaining and the 'base' keyword
                7. Master polymorphism for writing flexible, maintainable code
                
                Design patterns often combine inheritance, polymorphism, and interfaces
                to create robust, extensible software architectures.
                """);
        }
    }
}