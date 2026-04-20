/*
    C# GENERICS
    File: 06_generics.cs
    
    This file demonstrates generics in C# programming, covering concepts from
    junior to upper mid-level. Generics enable type-safe, reusable code that
    works with any data type while maintaining compile-time type checking.
    
    Key Concepts Covered:
    1. Generic Classes and Methods
    2. Type Parameters and Constraints
    3. Generic Interfaces and Delegates
    4. Variance: Covariance and Contravariance
    5. Generic Collections (List<T>, Dictionary<TKey, TValue>)
    6. Generic Constraints (where T : ...)
    7. Default Keyword with Generics
    8. Real-world Generic Patterns
*/

using System;
using System.Collections.Generic;

namespace CSharpRefresher.Generics
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Generics Demonstration ===\n");
            
            DemonstrateGenericClasses();
            DemonstrateGenericMethods();
            DemonstrateGenericConstraints();
            DemonstrateGenericInterfaces();
            DemonstrateGenericDelegates();
            DemonstrateVariance();
            DemonstrateGenericCollections();
            DemonstrateRealWorldPatterns();
            
            Console.WriteLine("\n=== Generics Complete ===");
        }
        
        static void DemonstrateGenericClasses()
        {
            Console.WriteLine("============ GENERIC CLASSES ============\n");
            
            // ============ BASIC GENERIC CLASS ============
            Console.WriteLine("=== 1. Basic Generic Class ===");
            Console.WriteLine("""
                Generic classes allow you to define a class that can work with
                any data type while maintaining type safety.
                
                Syntax: class ClassName<T> { ... }
                Where T is a type parameter that can be used throughout the class.
                """);
            
            // Create generic container instances with different types
            Container<int> intContainer = new Container<int>(42);
            Container<string> stringContainer = new Container<string>("Hello");
            Container<DateTime> dateContainer = new Container<DateTime>(DateTime.Now);
            
            Console.WriteLine($"Int container: {intContainer.GetItem()}");
            Console.WriteLine($"String container: {stringContainer.GetItem()}");
            Console.WriteLine($"Date container: {dateContainer.GetItem()}");
            
            // ============ MULTIPLE TYPE PARAMETERS ============
            Console.WriteLine("\n=== 2. Multiple Type Parameters ===");
            
            Pair<int, string> idNamePair = new Pair<int, string>(1, "Alice");
            Pair<string, decimal> productPrice = new Pair<string, decimal>("Laptop", 999.99m);
            
            Console.WriteLine($"Pair 1: {idNamePair.First} -> {idNamePair.Second}");
            Console.WriteLine($"Pair 2: {productPrice.First} -> ${productPrice.Second}");
            
            // ============ GENERIC WITH PROPERTIES AND METHODS ============
            Console.WriteLine("\n=== 3. Generic with Properties and Methods ===");
            
            Repository<Customer> customerRepo = new Repository<Customer>();
            customerRepo.Add(new Customer(1, "Alice"));
            customerRepo.Add(new Customer(2, "Bob"));
            
            Console.WriteLine($"Customer count: {customerRepo.Count}");
            Console.WriteLine($"Customer 1: {customerRepo.GetById(1)?.Name}");
            
            // ============ STATIC MEMBERS IN GENERIC CLASSES ============
            Console.WriteLine("\n=== 4. Static Members in Generic Classes ===");
            Console.WriteLine("""
                Each closed generic type has its own set of static members.
                Example: GenericClass<int> and GenericClass<string> have separate
                static field instances.
                """);
            
            GenericWithStatic<int>.Count = 5;
            GenericWithStatic<string>.Count = 10;
            
            Console.WriteLine($"GenericWithStatic<int>.Count: {GenericWithStatic<int>.Count}");
            Console.WriteLine($"GenericWithStatic<string>.Count: {GenericWithStatic<string>.Count}");
            
            // ============ GENERIC INHERITANCE ============
            Console.WriteLine("\n=== 5. Generic Inheritance ===");
            
            StringList list = new StringList();
            list.Add("Item 1");
            list.Add("Item 2");
            Console.WriteLine($"String list items: {string.Join(", ", list.GetAll())}");
        }
        
        static void DemonstrateGenericMethods()
        {
            Console.WriteLine("\n============ GENERIC METHODS ============\n");
            
            // ============ BASIC GENERIC METHOD ============
            Console.WriteLine("=== 1. Basic Generic Method ===");
            
            Console.WriteLine($"Max of 5 and 10: {MathUtils.Max(5, 10)}");
            Console.WriteLine($"Max of 3.14 and 2.71: {MathUtils.Max(3.14, 2.71)}");
            Console.WriteLine($"Max of 'A' and 'B': {MathUtils.Max('A', 'B')}");
            
            // ============ TYPE INFERENCE ============
            Console.WriteLine("\n=== 2. Type Inference ===");
            Console.WriteLine("""
                The compiler can often infer type parameters from method arguments,
                so you don't need to specify them explicitly.
                """);
            
            // Type inferred from arguments
            var result1 = MathUtils.Max(5, 10);        // T inferred as int
            var result2 = MathUtils.Max("apple", "zebra"); // T inferred as string
            
            Console.WriteLine($"Inferred int max: {result1}");
            Console.WriteLine($"Inferred string max: {result2}");
            
            // ============ GENERIC METHOD IN NON-GENERIC CLASS ============
            Console.WriteLine("\n=== 3. Generic Method in Non-Generic Class ===");
            
            ArrayProcessor processor = new ArrayProcessor();
            int[] numbers = { 1, 2, 3, 4, 5 };
            string[] strings = { "A", "B", "C" };
            
            processor.PrintArray(numbers);
            processor.PrintArray(strings);
            
            // ============ MULTIPLE TYPE PARAMETERS IN METHODS ============
            Console.WriteLine("\n=== 4. Multiple Type Parameters in Methods ===");
            
            var tuple = TupleUtils.CreatePair(42, "Answer");
            Console.WriteLine($"Created tuple: {tuple.Item1} -> {tuple.Item2}");
            
            // ============ GENERIC METHOD OVERLOADING ============
            Console.WriteLine("\n=== 5. Generic Method Overloading ===");
            
            Overloader.Print(42);              // Calls non-generic Print(int)
            Overloader.Print("Hello");         // Calls non-generic Print(string)
            Overloader.Print(3.14);           // Calls generic Print<T>(T value)
            Overloader.Print(true);           // Calls generic Print<T>(T value)
        }
        
        static void DemonstrateGenericConstraints()
        {
            Console.WriteLine("\n============ GENERIC CONSTRAINTS ============\n");
            
            Console.WriteLine("=== Common Generic Constraints ===");
            Console.WriteLine("""
                | Constraint          | Description                          | Example                        |
                |---------------------|--------------------------------------|--------------------------------|
                | where T : class     | T must be a reference type           | where T : class                |
                | where T : struct    | T must be a value type (non-nullable)| where T : struct               |
                | where T : new()     | T must have parameterless constructor| where T : new()                |
                | where T : BaseClass | T must derive from BaseClass         | where T : Stream               |
                | where T : Interface | T must implement Interface           | where T : IComparable<T>       |
                | where T : U         | T must inherit from or be U          | where T : U                    |
                """);
            
            // ============ CLASS CONSTRAINT ============
            Console.WriteLine("\n=== 1. Class Constraint (reference types) ===");
            
            ReferenceContainer<string> stringContainer = new ReferenceContainer<string>("Test");
            // ReferenceContainer<int> intContainer; // ERROR: int is value type
            
            // ============ STRUCT CONSTRAINT ============
            Console.WriteLine("\n=== 2. Struct Constraint (value types) ===");
            
            ValueContainer<int> intContainer = new ValueContainer<int>(42);
            ValueContainer<DateTime> dateContainer = new ValueContainer<DateTime>(DateTime.Now);
            // ValueContainer<string> stringContainer; // ERROR: string is reference type
            
            Console.WriteLine($"Int container: {intContainer.Value}");
            Console.WriteLine($"Date container: {dateContainer.Value}");
            
            // ============ NEW() CONSTRAINT ============
            Console.WriteLine("\n=== 3. new() Constraint ===");
            
            Factory<Product> productFactory = new Factory<Product>();
            Product product = productFactory.Create();
            Console.WriteLine($"Created product: {product.Name}");
            
            // ============ BASE CLASS CONSTRAINT ============
            Console.WriteLine("\n=== 4. Base Class Constraint ===");
            
            Repository<Entity> entityRepo = new Repository<Entity>();
            entityRepo.Add(new User("Alice"));
            entityRepo.Add(new Product("Laptop"));
            
            Console.WriteLine($"Entity count: {entityRepo.Count}");
            
            // ============ INTERFACE CONSTRAINT ============
            Console.WriteLine("\n=== 5. Interface Constraint ===");
            
            SortedList<int> sortedNumbers = new SortedList<int>();
            sortedNumbers.Add(5);
            sortedNumbers.Add(2);
            sortedNumbers.Add(8);
            Console.WriteLine($"Sorted: {string.Join(", ", sortedNumbers.GetSorted())}");
            
            SortedList<string> sortedStrings = new SortedList<string>();
            sortedStrings.Add("Zebra");
            sortedStrings.Add("Apple");
            sortedStrings.Add("Banana");
            Console.WriteLine($"Sorted strings: {string.Join(", ", sortedStrings.GetSorted())}");
            
            // ============ MULTIPLE CONSTRAINTS ============
            Console.WriteLine("\n=== 6. Multiple Constraints ===");
            
            AdvancedRepository<Customer> customerRepo = new AdvancedRepository<Customer>();
            customerRepo.Add(new Customer(1, "Alice"));
            Console.WriteLine($"Customer repository valid: {customerRepo.IsValid()}");
            
            // ============ DEFAULT KEYWORD WITH GENERICS ============
            Console.WriteLine("\n=== 7. Default Keyword with Generics ===");
            Console.WriteLine("""
                The 'default' keyword returns the default value for type T:
                • null for reference types
                • 0 for numeric value types
                • false for bool
                • struct with all fields default for value types
                """);
            
            Console.WriteLine($"default(int) = {default(int)}");
            Console.WriteLine($"default(string) = {(default(string) == null ? "null" : "not null")}");
            Console.WriteLine($"default(DateTime) = {default(DateTime)}");
            
            var utils = new GenericUtils();
            Console.WriteLine($"Default int from generic method: {utils.GetDefault<int>()}");
            Console.WriteLine($"Default string from generic method: {utils.GetDefault<string>() ?? "null"}");
        }
        
        static void DemonstrateGenericInterfaces()
        {
            Console.WriteLine("\n============ GENERIC INTERFACES ============\n");
            
            // ============ BASIC GENERIC INTERFACE ============
            Console.WriteLine("=== 1. Basic Generic Interface ===");
            
            IRepository<Employee> employeeRepo = new EmployeeRepository();
            employeeRepo.Add(new Employee("Alice", "Engineering"));
            employeeRepo.Add(new Employee("Bob", "Sales"));
            
            Console.WriteLine($"Employee count: {employeeRepo.Count()}");
            Console.WriteLine($"First employee: {employeeRepo.Get(0)?.Name}");
            
            // ============ GENERIC INTERFACE IMPLEMENTATION ============
            Console.WriteLine("\n=== 2. Generic Interface Implementation ===");
            
            ICache<string, User> userCache = new MemoryCache<string, User>();
            userCache.Add("alice", new User("Alice"));
            userCache.Add("bob", new User("Bob"));
            
            Console.WriteLine($"Cached user 'alice': {userCache.Get("alice")?.Name}");
            Console.WriteLine($"Cache contains 'bob': {userCache.Contains("bob")}");
            
            // ============ COVARIANT INTERFACE ============
            Console.WriteLine("\n=== 3. Covariant Interface (out T) ===");
            Console.WriteLine("""
                Covariance (out T): Allows using a more derived type than specified.
                Example: IEnumerable<Derived> can be assigned to IEnumerable<Base>
                """);
            
            ICovariant<Dog> dogProvider = new AnimalProvider<Dog>();
            ICovariant<Animal> animalProvider = dogProvider; // Covariant assignment
            
            // ============ CONTRAVARIANT INTERFACE ============
            Console.WriteLine("\n=== 4. Contravariant Interface (in T) ===");
            Console.WriteLine("""
                Contravariance (in T): Allows using a more base type than specified.
                Example: IComparer<Base> can be assigned to IComparer<Derived>
                """);
            
            IContravariant<Animal> animalComparer = new AnimalComparer();
            IContravariant<Dog> dogComparer = animalComparer; // Contravariant assignment
            
            // ============ VARIANT GENERIC DELEGATES ============
            Console.WriteLine("\n=== 5. Variant Generic Delegates ===");
            
            Func<Dog> getDog = () => new Dog();
            Func<Animal> getAnimal = getDog; // Covariant return type
            
            Action<Animal> processAnimal = a => Console.WriteLine($"Processing {a.GetType().Name}");
            Action<Dog> processDog = processAnimal; // Contravariant parameter type
        }
        
        static void DemonstrateGenericDelegates()
        {
            Console.WriteLine("\n============ GENERIC DELEGATES ============\n");
            
            // ============ FUNC DELEGATE ============
            Console.WriteLine("=== 1. Func Delegate ===");
            Console.WriteLine("""
                Func<TResult> - no parameters, returns TResult
                Func<T1, TResult> - one parameter, returns TResult
                Func<T1, T2, TResult> - two parameters, returns TResult
                ... up to 16 parameters
                """);
            
            Func<int, int, int> add = (x, y) => x + y;
            Func<string, int> stringLength = s => s.Length;
            Func<double, double> squareRoot = Math.Sqrt;
            
            Console.WriteLine($"Add(5, 3) = {add(5, 3)}");
            Console.WriteLine($"Length of 'Hello' = {stringLength("Hello")}");
            Console.WriteLine($"Square root of 25 = {squareRoot(25)}");
            
            // ============ ACTION DELEGATE ============
            Console.WriteLine("\n=== 2. Action Delegate ===");
            Console.WriteLine("""
                Action - no parameters, returns void
                Action<T> - one parameter, returns void
                Action<T1, T2> - two parameters, returns void
                ... up to 16 parameters
                """);
            
            Action<string> print = s => Console.WriteLine($"Printed: {s}");
            Action<int, int> printSum = (x, y) => Console.WriteLine($"Sum: {x + y}");
            
            print("Hello World");
            printSum(10, 20);
            
            // ============ PREDICATE DELEGATE ============
            Console.WriteLine("\n=== 3. Predicate Delegate ===");
            Console.WriteLine("""
                Predicate<T> - takes T, returns bool
                Commonly used for filtering collections
                """);
            
            Predicate<int> isEven = n => n % 2 == 0;
            Predicate<string> isLong = s => s.Length > 10;
            
            Console.WriteLine($"Is 5 even? {isEven(5)}");
            Console.WriteLine($"Is 'Hello World' long? {isLong("Hello World")}");
            
            // ============ COMPARISON DELEGATE ============
            Console.WriteLine("\n=== 4. Comparison Delegate ===");
            
            Comparison<string> lengthComparer = (x, y) => x.Length.CompareTo(y.Length);
            string[] words = { "apple", "banana", "cherry", "date" };
            Array.Sort(words, lengthComparer);
            Console.WriteLine($"Sorted by length: {string.Join(", ", words)}");
            
            // ============ CONVERTER DELEGATE ============
            Console.WriteLine("\n=== 5. Converter Delegate ===");
            
            Converter<int, string> intToString = n => n.ToString("X");
            int[] numbers = { 10, 20, 30, 255 };
            string[] hexStrings = Array.ConvertAll(numbers, intToString);
            Console.WriteLine($"Hex values: {string.Join(", ", hexStrings)}");
            
            // ============ CUSTOM GENERIC DELEGATE ============
            Console.WriteLine("\n=== 6. Custom Generic Delegate ===");
            
            Transformer<int, string> transform = n => $"Number: {n}";
            Console.WriteLine($"Transformed: {transform(42)}");
            
            // Generic event handler
            var publisher = new EventPublisher<string>();
            publisher.ValueChanged += (sender, value) => Console.WriteLine($"Value changed to: {value}");
            publisher.Publish("New Value");
        }
        
        static void DemonstrateVariance()
        {
            Console.WriteLine("\n============ VARIANCE ============\n");
            
            // ============ COVARIANCE ============
            Console.WriteLine("=== 1. Covariance (out T) ===");
            Console.WriteLine("""
                Covariance allows you to use a more derived type than originally specified.
                Safe because you can always treat a Derived as its Base.
                
                Example: IEnumerable<Dog> can be assigned to IEnumerable<Animal>
                because you can treat every Dog as an Animal.
                """);
            
            List<Dog> dogs = new List<Dog> { new Dog(), new Dog() };
            IEnumerable<Animal> animals = dogs; // Covariant assignment
            
            foreach (var animal in animals)
            {
                Console.WriteLine($"Animal: {animal.GetType().Name}");
            }
            
            // Covariant interface example
            ICovariant<Dog> dogSource = new AnimalSource<Dog>();
            ICovariant<Animal> animalSource = dogSource; // OK - covariance
            
            // ============ CONTRAVARIANCE ============
            Console.WriteLine("\n=== 2. Contravariance (in T) ===");
            Console.WriteLine("""
                Contravariance allows you to use a more base type than originally specified.
                Safe because you can always accept a Base when expecting a Derived.
                
                Example: IComparer<Animal> can be assigned to IComparer<Dog>
                because a comparer that compares Animals can also compare Dogs.
                """);
            
            IContravariant<Animal> animalProcessor = new AnimalProcessor();
            IContravariant<Dog> dogProcessor = animalProcessor; // Contravariant assignment
            
            // Contravariant delegate example
            Action<Animal> feedAnimal = a => Console.WriteLine($"Feeding {a.GetType().Name}");
            Action<Dog> feedDog = feedAnimal; // OK - contravariance
            feedDog(new Dog());
            
            // ============ INVARIANCE ============
            Console.WriteLine("\n=== 3. Invariance ===");
            Console.WriteLine("""
                Invariant types require exact type matching.
                Most generic types are invariant by default.
                
                Example: List<Dog> cannot be assigned to List<Animal>
                because you could add a Cat to List<Animal>, breaking type safety.
                """);
            
            List<Dog> dogList = new List<Dog>();
            // List<Animal> animalList = dogList; // ERROR - List<T> is invariant
            
            // ============ REAL-WORLD VARIANCE EXAMPLES ============
            Console.WriteLine("\n=== 4. Real-world Variance Examples ===");
            
            // Covariant return types in .NET
            IEnumerable<string> strings = new List<string> { "A", "B", "C" };
            IEnumerable<object> objects = strings; // Covariant
            
            // Contravariant parameters
            IComparer<object> objectComparer = Comparer<object>.Default;
            IComparer<string> stringComparer = objectComparer; // Contravariant
            
            // Func covariance/contravariance
            Func<Dog> getDog = () => new Dog();
            Func<Animal> getAnimal = getDog; // Covariant return
            
            Action<Animal> actOnAnimal = a => { };
            Action<Dog> actOnDog = actOnAnimal; // Contravariant parameter
        }
        
        static void DemonstrateGenericCollections()
        {
            Console.WriteLine("\n============ GENERIC COLLECTIONS ============\n");
            
            // ============ LIST<T> ============
            Console.WriteLine("=== 1. List<T> ===");
            
            List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };
            numbers.Add(6);
            numbers.Insert(0, 0);
            numbers.Remove(3);
            
            Console.WriteLine($"Numbers: {string.Join(", ", numbers)}");
            Console.WriteLine($"Count: {numbers.Count}, Capacity: {numbers.Capacity}");
            
            // ============ DICTIONARY<TKEY, TVALUE> ============
            Console.WriteLine("\n=== 2. Dictionary<TKey, TValue> ===");
            
            Dictionary<string, int> wordCounts = new Dictionary<string, int>
            {
                ["apple"] = 5,
                ["banana"] = 3,
                ["cherry"] = 7
            };
            
            wordCounts["date"] = 4;
            wordCounts["apple"] = 6; // Update existing
            
            Console.WriteLine("Word counts:");
            foreach (var kvp in wordCounts)
            {
                Console.WriteLine($"  {kvp.Key}: {kvp.Value}");
            }
            
            // ============ QUEUE<T> AND STACK<T> ============
            Console.WriteLine("\n=== 3. Queue<T> and Stack<T> ===");
            
            Queue<string> queue = new Queue<string>();
            queue.Enqueue("First");
            queue.Enqueue("Second");
            queue.Enqueue("Third");
            
            Console.WriteLine("Queue (FIFO):");
            while (queue.Count > 0)
            {
                Console.WriteLine($"  Dequeue: {queue.Dequeue()}");
            }
            
            Stack<int> stack = new Stack<int>();
            stack.Push(1);
            stack.Push(2);
            stack.Push(3);
            
            Console.WriteLine("Stack (LIFO):");
            while (stack.Count > 0)
            {
                Console.WriteLine($"  Pop: {stack.Pop()}");
            }
            
            // ============ SORTEDSET<T> AND SORTEDDICTIONARY<TKEY, TVALUE> ============
            Console.WriteLine("\n=== 4. SortedSet<T> and SortedDictionary<TKey, TValue> ===");
            
            SortedSet<string> sortedSet = new SortedSet<string> { "Zebra", "Apple", "Banana", "Cherry" };
            Console.WriteLine($"Sorted set: {string.Join(", ", sortedSet)}");
            
            SortedDictionary<int, string> sortedDict = new SortedDictionary<int, string>
            {
                [3] = "Three",
                [1] = "One",
                [2] = "Two"
            };
            
            Console.WriteLine("Sorted dictionary:");
            foreach (var kvp in sortedDict)
            {
                Console.WriteLine($"  {kvp.Key}: {kvp.Value}");
            }
            
            // ============ LINKEDLIST<T> ============
            Console.WriteLine("\n=== 5. LinkedList<T> ===");
            
            LinkedList<string> linkedList = new LinkedList<string>();
            linkedList.AddLast("First");
            linkedList.AddLast("Third");
            linkedList.AddBefore(linkedList.Last!, "Second");
            
            Console.WriteLine("Linked list:");
            foreach (var item in linkedList)
            {
                Console.WriteLine($"  {item}");
            }
            
            // ============ CONCURRENT COLLECTIONS ============
            Console.WriteLine("\n=== 6. Concurrent Collections ===");
            
            System.Collections.Concurrent.ConcurrentDictionary<string, int> concurrentDict = 
                new System.Collections.Concurrent.ConcurrentDictionary<string, int>();
            
            concurrentDict.TryAdd("key1", 1);
            concurrentDict.TryAdd("key2", 2);
            
            Console.WriteLine("Concurrent dictionary:");
            foreach (var kvp in concurrentDict)
            {
                Console.WriteLine($"  {kvp.Key}: {kvp.Value}");
            }
        }
        
        static void DemonstrateRealWorldPatterns()
        {
            Console.WriteLine("\n============ REAL-WORLD GENERIC PATTERNS ============\n");
            
            // ============ REPOSITORY PATTERN ============
            Console.WriteLine("=== 1. Repository Pattern with Generics ===");
            
            GenericRepository<User> userRepo = new GenericRepository<User>();
            userRepo.Add(new User("Alice"));
            userRepo.Add(new User("Bob"));
            
            Console.WriteLine($"All users: {string.Join(", ", userRepo.GetAll().Select(u => u.Name))}");
            Console.WriteLine($"User count: {userRepo.Count()}");
            
            // ============ FACTORY PATTERN ============
            Console.WriteLine("\n=== 2. Factory Pattern with Generics ===");
            
            var factory = new GenericFactory();
            var car = factory.Create<Car>();
            var bike = factory.Create<Bike>();
            
            car.Drive();
            bike.Ride();
            
            // ============ BUILDER PATTERN ============
            Console.WriteLine("\n=== 3. Builder Pattern with Generics ===");
            
            var queryBuilder = new QueryBuilder<Person>()
                .Where(p => p.Age > 18)
                .OrderBy(p => p.Name)
                .Take(10);
            
            Console.WriteLine($"Built query for {typeof(Person).Name}");
            
            // ============ STRATEGY PATTERN ============
            Console.WriteLine("\n=== 4. Strategy Pattern with Generics ===");
            
            var paymentProcessor = new PaymentProcessor();
            paymentProcessor.ProcessPayment(new CreditCardPayment());
            paymentProcessor.ProcessPayment(new PayPalPayment());
            
            // ============ SPECIFICATION PATTERN ============
            Console.WriteLine("\n=== 5. Specification Pattern with Generics ===");
            
            var adultSpec = new AgeSpecification(18);
            var employedSpec = new EmploymentSpecification();
            var adultAndEmployed = adultSpec.And(employedSpec);
            
            var people = new List<Person>
            {
                new Person("Alice", 25, true),
                new Person("Bob", 16, false),
                new Person("Charlie", 30, true)
            };
            
            Console.WriteLine("Adults who are employed:");
            foreach (var person in people.Where(adultAndEmployed.IsSatisfiedBy))
            {
                Console.WriteLine($"  {person.Name} ({person.Age})");
            }
            
            // ============ UNIT OF WORK PATTERN ============
            Console.WriteLine("\n=== 6. Unit of Work Pattern with Generics ===");
            
            var unitOfWork = new UnitOfWork();
            var userRepository = unitOfWork.GetRepository<User>();
            var productRepository = unitOfWork.GetRepository<Product>();
            
            userRepository.Add(new User("David"));
            productRepository.Add(new Product("Tablet"));
            
            Console.WriteLine($"Users in UoW: {userRepository.Count()}");
            Console.WriteLine($"Products in UoW: {productRepository.Count()}");
            
            // ============ CACHING PATTERN ============
            Console.WriteLine("\n=== 7. Caching Pattern with Generics ===");
            
            var cache = new GenericCache<string, Product>();
            cache.Set("p1", new Product("Laptop"));
            cache.Set("p2", new Product("Phone"));
            
            Console.WriteLine($"Cached product p1: {cache.Get("p1")?.Name}");
            Console.WriteLine($"Cache contains p2: {cache.Contains("p2")}");
        }
    }
    
    // ============ BASIC GENERIC CLASS EXAMPLES ============
    
    // Simple generic container
    public class Container<T>
    {
        private T _item;
        
        public Container(T item)
        {
            _item = item;
        }
        
        public T GetItem() => _item;
        public void SetItem(T newItem) => _item = newItem;
        
        public override string ToString() => $"Container<{typeof(T).Name}>: {_item}";
    }
    
    // Generic class with multiple type parameters
    public class Pair<TFirst, TSecond>
    {
        public TFirst First { get; set; }
        public TSecond Second { get; set; }
        
        public Pair(TFirst first, TSecond second)
        {
            First = first;
            Second = second;
        }
    }
    
    // Generic repository
    public class Repository<T>
    {
        private List<T> _items = new List<T>();
        
        public void Add(T item) => _items.Add(item);
        public void Remove(T item) => _items.Remove(item);
        public T GetById(int id) where T : IEntity => _items.FirstOrDefault(item => (item as IEntity)?.Id == id);
        public int Count => _items.Count;
        public IEnumerable<T> GetAll() => _items;
    }
    
    public interface IEntity
    {
        int Id { get; }
    }
    
    public class Customer : IEntity
    {
        public int Id { get; }
        public string Name { get; set; }
        
        public Customer(int id, string name)
        {
            Id = id;
            Name = name;
        }
    }
    
    // Generic class with static members
    public class GenericWithStatic<T>
    {
        public static int Count { get; set; }
        public static T LastItem { get; set; }
    }
    
    // Generic inheritance
    public class GenericList<T>
    {
        protected List<T> _items = new List<T>();
        
        public void Add(T item) => _items.Add(item);
        public void Remove(T item) => _items.Remove(item);
        public IEnumerable<T> GetAll() => _items;
    }
    
    public class StringList : GenericList<string>
    {
        public void AddRange(params string[] items) => _items.AddRange(items);
    }
    
    // ============ GENERIC METHOD EXAMPLES ============
    
    public static class MathUtils
    {
        // Generic method to find maximum of two values
        public static T Max<T>(T a, T b) where T : IComparable<T>
        {
            return a.CompareTo(b) > 0 ? a : b;
        }
        
        // Generic method with multiple parameters
        public static TResult Combine<T1, T2, TResult>(T1 a, T2 b, Func<T1, T2, TResult> combiner)
        {
            return combiner(a, b);
        }
    }
    
    public class ArrayProcessor
    {
        // Generic method in non-generic class
        public void PrintArray<T>(T[] array)
        {
            Console.WriteLine($"Array of {typeof(T).Name}: [{string.Join(", ", array)}]");
        }
        
        // Generic method with constraints
        public T FindMax<T>(T[] array) where T : IComparable<T>
        {
            if (array.Length == 0) throw new ArgumentException("Array cannot be empty");
            
            T max = array[0];
            for (int i = 1; i < array.Length; i++)
            {
                if (array[i].CompareTo(max) > 0)
                    max = array[i];
            }
            return max;
        }
    }
    
    public static class TupleUtils
    {
        public static (T1, T2) CreatePair<T1, T2>(T1 first, T2 second)
        {
            return (first, second);
        }
    }
    
    public static class Overloader
    {
        // Non-generic methods
        public static void Print(int value) => Console.WriteLine($"Integer: {value}");
        public static void Print(string value) => Console.WriteLine($"String: {value}");
        
        // Generic fallback
        public static void Print<T>(T value) => Console.WriteLine($"Generic <{typeof(T).Name}>: {value}");
    }
    
    // ============ GENERIC CONSTRAINT EXAMPLES ============
    
    // Class constraint (reference types only)
    public class ReferenceContainer<T> where T : class
    {
        private T _value;
        
        public ReferenceContainer(T value)
        {
            _value = value;
        }
        
        public T Value => _value;
    }
    
    // Struct constraint (value types only)
    public class ValueContainer<T> where T : struct
    {
        private T _value;
        
        public ValueContainer(T value)
        {
            _value = value;
        }
        
        public T Value => _value;
    }
    
    // new() constraint
    public class Factory<T> where T : new()
    {
        public T Create()
        {
            return new T();
        }
    }
    
    public class Product
    {
        public string Name { get; set; } = "Unnamed Product";
    }
    
    // Base class constraint
    public class EntityRepository<T> where T : Entity
    {
        private List<T> _entities = new List<T>();
        
        public void Add(T entity) => _entities.Add(entity);
        public int Count => _entities.Count;
    }
    
    public abstract class Entity
    {
        public int Id { get; set; }
    }
    
    public class User : Entity
    {
        public string Name { get; set; }
        
        public User(string name)
        {
            Name = name;
        }
    }
    
    // Interface constraint
    public class SortedList<T> where T : IComparable<T>
    {
        private List<T> _items = new List<T>();
        
        public void Add(T item) => _items.Add(item);
        public List<T> GetSorted() => _items.OrderBy(x => x).ToList();
    }
    
    // Multiple constraints
    public class AdvancedRepository<T> where T : class, IEntity, new()
    {
        private List<T> _items = new List<T>();
        
        public void Add(T item) => _items.Add(item);
        public bool IsValid() => _items.All(item => item.Id > 0);
    }
    
    // Default keyword with generics
    public class GenericUtils
    {
        public T GetDefault<T>() => default(T);
        
        public void Reset<T>(ref T value)
        {
            value = default(T);
        }
    }
    
    // ============ GENERIC INTERFACE EXAMPLES ============
    
    public interface IRepository<T>
    {
        void Add(T item);
        void Remove(T item);
        T Get(int index);
        int Count();
    }
    
    public class Employee
    {
        public string Name { get; set; }
        public string Department { get; set; }
        
        public Employee(string name, string department)
        {
            Name = name;
            Department = department;
        }
    }
    
    public class EmployeeRepository : IRepository<Employee>
    {
        private List<Employee> _employees = new List<Employee>();
        
        public void Add(Employee item) => _employees.Add(item);
        public void Remove(Employee item) => _employees.Remove(item);
        public Employee Get(int index) => _employees[index];
        public int Count() => _employees.Count;
    }
    
    public interface ICache<TKey, TValue>
    {
        void Add(TKey key, TValue value);
        bool Contains(TKey key);
        TValue Get(TKey key);
        void Remove(TKey key);
    }
    
    public class MemoryCache<TKey, TValue> : ICache<TKey, TValue>
    {
        private Dictionary<TKey, TValue> _cache = new Dictionary<TKey, TValue>();
        
        public void Add(TKey key, TValue value) => _cache[key] = value;
        public bool Contains(TKey key) => _cache.ContainsKey(key);
        public TValue Get(TKey key) => _cache[key];
        public void Remove(TKey key) => _cache.Remove(key);
    }
    
    // Covariant interface
    public interface ICovariant<out T>
    {
        T GetItem();
    }
    
    public class AnimalProvider<T> : ICovariant<T> where T : new()
    {
        public T GetItem() => new T();
    }
    
    // Contravariant interface
    public interface IContravariant<in T>
    {
        void Process(T item);
    }
    
    public class AnimalComparer : IContravariant<Animal>
    {
        public void Process(Animal item)
        {
            Console.WriteLine($"Processing animal: {item.GetType().Name}");
        }
    }
    
    // ============ GENERIC DELEGATE EXAMPLES ============
    
    // Custom generic delegate
    public delegate TResult Transformer<in T, out TResult>(T input);
    
    // Generic event handler
    public class EventPublisher<T>
    {
        public event EventHandler<T> ValueChanged;
        
        public void Publish(T value)
        {
            ValueChanged?.Invoke(this, value);
        }
    }
    
    // ============ VARIANCE EXAMPLES ============
    
    public class Animal { }
    public class Dog : Animal { }
    public class Cat : Animal { }
    
    // Covariant interface implementation
    public class AnimalSource<T> : ICovariant<T> where T : new()
    {
        public T GetItem() => new T();
    }
    
    // Contravariant interface implementation
    public class AnimalProcessor : IContravariant<Animal>
    {
        public void Process(Animal item)
        {
            Console.WriteLine($"Processing {item.GetType().Name}");
        }
    }
    
    // ============ REAL-WORLD PATTERN EXAMPLES ============
    
    // Generic Repository Pattern
    public class GenericRepository<T> where T : class
    {
        private List<T> _items = new List<T>();
        
        public void Add(T item) => _items.Add(item);
        public void Remove(T item) => _items.Remove(item);
        public T GetById(int id) where T : IEntity => _items.FirstOrDefault(item => (item as IEntity)?.Id == id);
        public IEnumerable<T> GetAll() => _items;
        public int Count() => _items.Count;
    }
    
    // Generic Factory Pattern
    public class GenericFactory
    {
        public T Create<T>() where T : new()
        {
            return new T();
        }
    }
    
    public class Car
    {
        public void Drive() => Console.WriteLine("Car is driving");
    }
    
    public class Bike
    {
        public void Ride() => Console.WriteLine("Bike is riding");
    }
    
    // Generic Builder Pattern
    public class QueryBuilder<T>
    {
        public QueryBuilder<T> Where(Predicate<T> predicate)
        {
            Console.WriteLine($"Added WHERE clause for {typeof(T).Name}");
            return this;
        }
        
        public QueryBuilder<T> OrderBy<TKey>(Func<T, TKey> keySelector)
        {
            Console.WriteLine($"Added ORDER BY clause for {typeof(T).Name}");
            return this;
        }
        
        public QueryBuilder<T> Take(int count)
        {
            Console.WriteLine($"Added TAKE {count} clause");
            return this;
        }
    }
    
    public class Person
    {
        public string Name { get; }
        public int Age { get; }
        public bool IsEmployed { get; }
        
        public Person(string name, int age, bool isEmployed)
        {
            Name = name;
            Age = age;
            IsEmployed = isEmployed;
        }
    }
    
    // Generic Specification Pattern
    public interface ISpecification<T>
    {
        bool IsSatisfiedBy(T item);
        ISpecification<T> And(ISpecification<T> other);
        ISpecification<T> Or(ISpecification<T> other);
        ISpecification<T> Not();
    }
    
    public abstract class Specification<T> : ISpecification<T>
    {
        public abstract bool IsSatisfiedBy(T item);
        
        public ISpecification<T> And(ISpecification<T> other)
        {
            return new AndSpecification<T>(this, other);
        }
        
        public ISpecification<T> Or(ISpecification<T> other)
        {
            return new OrSpecification<T>(this, other);
        }
        
        public ISpecification<T> Not()
        {
            return new NotSpecification<T>(this);
        }
    }
    
    public class AgeSpecification : Specification<Person>
    {
        private readonly int _minAge;
        
        public AgeSpecification(int minAge)
        {
            _minAge = minAge;
        }
        
        public override bool IsSatisfiedBy(Person person)
        {
            return person.Age >= _minAge;
        }
    }
    
    public class EmploymentSpecification : Specification<Person>
    {
        public override bool IsSatisfiedBy(Person person)
        {
            return person.IsEmployed;
        }
    }
    
    public class AndSpecification<T> : Specification<T>
    {
        private readonly ISpecification<T> _left;
        private readonly ISpecification<T> _right;
        
        public AndSpecification(ISpecification<T> left, ISpecification<T> right)
        {
            _left = left;
            _right = right;
        }
        
        public override bool IsSatisfiedBy(T item)
        {
            return _left.IsSatisfiedBy(item) && _right.IsSatisfiedBy(item);
        }
    }
    
    public class OrSpecification<T> : Specification<T>
    {
        private readonly ISpecification<T> _left;
        private readonly ISpecification<T> _right;
        
        public OrSpecification(ISpecification<T> left, ISpecification<T> right)
        {
            _left = left;
            _right = right;
        }
        
        public override bool IsSatisfiedBy(T item)
        {
            return _left.IsSatisfiedBy(item) || _right.IsSatisfiedBy(item);
        }
    }
    
    public class NotSpecification<T> : Specification<T>
    {
        private readonly ISpecification<T> _specification;
        
        public NotSpecification(ISpecification<T> specification)
        {
            _specification = specification;
        }
        
        public override bool IsSatisfiedBy(T item)
        {
            return !_specification.IsSatisfiedBy(item);
        }
    }
    
    // Generic Strategy Pattern
    public interface IPaymentStrategy<T> where T : IPayment
    {
        void Process(T payment);
    }
    
    public interface IPayment { }
    
    public class CreditCardPayment : IPayment { }
    public class PayPalPayment : IPayment { }
    
    public class PaymentProcessor
    {
        public void ProcessPayment<T>(T payment) where T : IPayment
        {
            Console.WriteLine($"Processing {typeof(T).Name} payment");
        }
    }
    
    // Generic Unit of Work Pattern
    public interface IUnitOfWork
    {
        IRepository<T> GetRepository<T>() where T : class;
        void SaveChanges();
    }
    
    public class UnitOfWork : IUnitOfWork
    {
        private Dictionary<Type, object> _repositories = new Dictionary<Type, object>();
        
        public IRepository<T> GetRepository<T>() where T : class
        {
            if (!_repositories.ContainsKey(typeof(T)))
            {
                _repositories[typeof(T)] = new Repository<T>();
            }
            return (IRepository<T>)_repositories[typeof(T)];
        }
        
        public void SaveChanges()
        {
            Console.WriteLine("Changes saved to database");
        }
    }
    
    // Generic Caching Pattern
    public class GenericCache<TKey, TValue>
    {
        private Dictionary<TKey, TValue> _cache = new Dictionary<TKey, TValue>();
        
        public void Set(TKey key, TValue value) => _cache[key] = value;
        public TValue Get(TKey key) => _cache.TryGetValue(key, out var value) ? value : default;
        public bool Contains(TKey key) => _cache.ContainsKey(key);
        public void Remove(TKey key) => _cache.Remove(key);
        public void Clear() => _cache.Clear();
    }
}