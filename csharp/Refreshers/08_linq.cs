/*
    C# LINQ (Language Integrated Query)
    File: 08_linq.cs
    
    This file demonstrates LINQ (Language Integrated Query) in C# programming,
    covering concepts from junior to upper mid-level. LINQ provides a consistent,
    declarative way to query data from various sources (collections, databases,
    XML, etc.) using a SQL-like syntax or method syntax.
    
    Key Concepts Covered:
    1. LINQ Query Syntax vs Method Syntax
    2. LINQ to Objects (Collections)
    3. Standard Query Operators (Where, Select, OrderBy, GroupBy, Join, etc.)
    4. Deferred Execution and Immediate Execution
    5. LINQ to XML, LINQ to SQL/Entities (concepts)
    6. Performance Considerations and Best Practices
    7. Advanced LINQ Patterns (Custom Operators, Expression Trees)
    8. Real-world LINQ Examples
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Xml.Linq;

namespace CSharpRefresher.Linq
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# LINQ Demonstration ===\n");
            
            DemonstrateBasicLinq();
            DemonstrateQueryVsMethodSyntax();
            DemonstrateStandardQueryOperators();
            DemonstrateDeferredExecution();
            DemonstrateLinqToXml();
            DemonstratePerformanceConsiderations();
            DemonstrateAdvancedPatterns();
            DemonstrateRealWorldExamples();
            
            Console.WriteLine("\n=== LINQ Complete ===");
        }
        
        static void DemonstrateBasicLinq()
        {
            Console.WriteLine("============ BASIC LINQ ============\n");
            
            // ============ WHAT IS LINQ? ============
            Console.WriteLine("=== 1. What is LINQ? ===");
            Console.WriteLine("""
                LINQ (Language Integrated Query) is a set of features that extends
                powerful query capabilities to the C# language syntax. It provides:
                
                • A consistent query experience across different data sources
                • Compile-time type checking and IntelliSense support
                • Two syntax styles: Query syntax (SQL-like) and Method syntax (fluent)
                • Support for objects, databases, XML, and other data sources
                """);
            
            // ============ BASIC LINQ WITH COLLECTIONS ============
            Console.WriteLine("\n=== 2. Basic LINQ with Collections ===");
            
            List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
            
            // Query syntax: Get even numbers
            var evenNumbersQuery = from n in numbers
                                   where n % 2 == 0
                                   select n;
            
            // Method syntax: Get even numbers
            var evenNumbersMethod = numbers.Where(n => n % 2 == 0);
            
            Console.WriteLine($"Numbers: {string.Join(", ", numbers)}");
            Console.WriteLine($"Even numbers (query): {string.Join(", ", evenNumbersQuery)}");
            Console.WriteLine($"Even numbers (method): {string.Join(", ", evenNumbersMethod)}");
            
            // ============ BASIC TRANSFORMATIONS ============
            Console.WriteLine("\n=== 3. Basic Transformations ===");
            
            List<string> fruits = new List<string> { "apple", "banana", "cherry", "date", "elderberry" };
            
            // Select: Transform each element
            var fruitLengths = fruits.Select(f => f.Length);
            Console.WriteLine($"Fruit lengths: {string.Join(", ", fruitLengths)}");
            
            // Select with index
            var fruitsWithIndex = fruits.Select((f, i) => $"{i}: {f}");
            Console.WriteLine($"Fruits with index: {string.Join(", ", fruitsWithIndex)}");
            
            // ============ BASIC FILTERING ============
            Console.WriteLine("\n=== 4. Basic Filtering ===");
            
            var longFruits = fruits.Where(f => f.Length > 5);
            var fruitsStartingWithB = fruits.Where(f => f.StartsWith("b", StringComparison.OrdinalIgnoreCase));
            
            Console.WriteLine($"Fruits longer than 5 chars: {string.Join(", ", longFruits)}");
            Console.WriteLine($"Fruits starting with 'b': {string.Join(", ", fruitsStartingWithB)}");
            
            // ============ BASIC ORDERING ============
            Console.WriteLine("\n=== 5. Basic Ordering ===");
            
            var sortedAlphabetically = fruits.OrderBy(f => f);
            var sortedByLength = fruits.OrderBy(f => f.Length);
            var sortedByLengthDesc = fruits.OrderByDescending(f => f.Length);
            
            Console.WriteLine($"Alphabetical: {string.Join(", ", sortedAlphabetically)}");
            Console.WriteLine($"By length (asc): {string.Join(", ", sortedByLength)}");
            Console.WriteLine($"By length (desc): {string.Join(", ", sortedByLengthDesc)}");
        }
        
        static void DemonstrateQueryVsMethodSyntax()
        {
            Console.WriteLine("\n============ QUERY VS METHOD SYNTAX ============\n");
            
            // Sample data
            List<Product> products = new List<Product>
            {
                new Product(1, "Laptop", 999.99m, "Electronics"),
                new Product(2, "Coffee Mug", 12.99m, "Kitchen"),
                new Product(3, "Desk Chair", 249.99m, "Furniture"),
                new Product(4, "Smartphone", 799.99m, "Electronics"),
                new Product(5, "Notebook", 8.99m, "Stationery"),
                new Product(6, "Monitor", 349.99m, "Electronics"),
                new Product(7, "Pen", 1.99m, "Stationery")
            };
            
            // ============ WHEN TO USE WHICH SYNTAX ============
            Console.WriteLine("=== 1. When to Use Which Syntax ===");
            Console.WriteLine("""
                Query Syntax (SQL-like):
                • More readable for complex queries with multiple joins, groupings
                • Familiar to SQL developers
                • Better for queries that span multiple lines
                
                Method Syntax (Fluent):
                • More concise for simple queries
                • Allows method chaining
                • More flexible (can use any .NET method)
                • Required for some operations (First(), Single(), etc.)
                """);
            
            // ============ SIMPLE QUERY - BOTH SYNTAXES ============
            Console.WriteLine("\n=== 2. Simple Query - Both Syntaxes ===");
            
            // Query syntax: Get expensive electronics
            var expensiveElectronicsQuery = from p in products
                                            where p.Category == "Electronics" && p.Price > 500
                                            select p;
            
            // Method syntax: Same query
            var expensiveElectronicsMethod = products
                .Where(p => p.Category == "Electronics" && p.Price > 500);
            
            Console.WriteLine("Expensive Electronics (> $500):");
            foreach (var p in expensiveElectronicsQuery)
            {
                Console.WriteLine($"  {p.Name}: ${p.Price}");
            }
            
            // ============ COMPLEX QUERY - JOIN EXAMPLE ============
            Console.WriteLine("\n=== 3. Complex Query - Join Example ===");
            
            List<Customer> customers = new List<Customer>
            {
                new Customer(1, "Alice", "alice@example.com"),
                new Customer(2, "Bob", "bob@example.com"),
                new Customer(3, "Charlie", "charlie@example.com")
            };
            
            List<Order> orders = new List<Order>
            {
                new Order(101, 1, 999.99m),
                new Order(102, 2, 12.99m),
                new Order(103, 1, 249.99m),
                new Order(104, 3, 799.99m)
            };
            
            // Query syntax with join (more readable for complex joins)
            var customerOrdersQuery = from c in customers
                                      join o in orders on c.Id equals o.CustomerId
                                      select new { c.Name, o.OrderId, o.Amount };
            
            // Method syntax with join (more concise but less readable for complex joins)
            var customerOrdersMethod = customers.Join(orders,
                c => c.Id,
                o => o.CustomerId,
                (c, o) => new { c.Name, o.OrderId, o.Amount });
            
            Console.WriteLine("Customer Orders (Query Syntax):");
            foreach (var co in customerOrdersQuery)
            {
                Console.WriteLine($"  {co.Name}: Order #{co.OrderId}, Amount: ${co.Amount}");
            }
            
            // ============ MIXING SYNTAXES ============
            Console.WriteLine("\n=== 4. Mixing Syntaxes ===");
            Console.WriteLine("""
                You can mix query and method syntax using the 'into' keyword
                or by calling methods on query results.
                """);
            
            // Query syntax with method call
            var mixedQuery = (from p in products
                             where p.Price > 100
                             select p).OrderByDescending(p => p.Price).Take(3);
            
            Console.WriteLine("Top 3 products over $100 (mixed syntax):");
            foreach (var p in mixedQuery)
            {
                Console.WriteLine($"  {p.Name}: ${p.Price}");
            }
            
            // ============ QUERY CONTINUATION ============
            Console.WriteLine("\n=== 5. Query Continuation (into) ===");
            
            var continuationQuery = from p in products
                                   group p by p.Category into categoryGroup
                                   select new
                                   {
                                       Category = categoryGroup.Key,
                                       Count = categoryGroup.Count(),
                                       TotalValue = categoryGroup.Sum(p => p.Price)
                                   };
            
            Console.WriteLine("Products by Category (with continuation):");
            foreach (var group in continuationQuery)
            {
                Console.WriteLine($"  {group.Category}: {group.Count} items, Total: ${group.TotalValue:F2}");
            }
        }
        
        static void DemonstrateStandardQueryOperators()
        {
            Console.WriteLine("\n============ STANDARD QUERY OPERATORS ============\n");
            
            List<Employee> employees = new List<Employee>
            {
                new Employee(1, "Alice", "Engineering", 75000, new DateTime(2020, 1, 15)),
                new Employee(2, "Bob", "Sales", 65000, new DateTime(2019, 3, 20)),
                new Employee(3, "Charlie", "Engineering", 80000, new DateTime(2021, 6, 10)),
                new Employee(4, "Diana", "Marketing", 55000, new DateTime(2022, 2, 28)),
                new Employee(5, "Eve", "Sales", 70000, new DateTime(2018, 11, 5)),
                new Employee(6, "Frank", "Engineering", 90000, new DateTime(2017, 7, 30)),
                new Employee(7, "Grace", "HR", 60000, new DateTime(2023, 1, 10))
            };
            
            // ============ FILTERING OPERATORS ============
            Console.WriteLine("=== 1. Filtering Operators ===");
            
            // Where - basic filtering
            var engineeringEmployees = employees.Where(e => e.Department == "Engineering");
            Console.WriteLine($"Engineering employees: {engineeringEmployees.Count()}");
            
            // OfType - filter by type (useful with heterogeneous collections)
            object[] mixedObjects = { 1, "hello", 2.5, "world", 3, DateTime.Now };
            var stringsOnly = mixedObjects.OfType<string>();
            Console.WriteLine($"Strings in mixed collection: {string.Join(", ", stringsOnly)}");
            
            // ============ PROJECTION OPERATORS ============
            Console.WriteLine("\n=== 2. Projection Operators ===");
            
            // Select - transform each element
            var employeeNames = employees.Select(e => e.Name);
            Console.WriteLine($"Employee names: {string.Join(", ", employeeNames)}");
            
            // SelectMany - flatten nested collections
            List<Department> departments = new List<Department>
            {
                new Department("Engineering", new List<string> { "Alice", "Charlie", "Frank" }),
                new Department("Sales", new List<string> { "Bob", "Eve" })
            };
            
            var allDepartmentMembers = departments.SelectMany(d => d.Members);
            Console.WriteLine($"All department members: {string.Join(", ", allDepartmentMembers)}");
            
            // ============ PARTITIONING OPERATORS ============
            Console.WriteLine("\n=== 3. Partitioning Operators ===");
            
            // Take, Skip, TakeWhile, SkipWhile
            var first3Employees = employees.Take(3);
            var skipFirst2 = employees.Skip(2);
            var highEarners = employees.TakeWhile(e => e.Salary > 60000);
            
            Console.WriteLine($"First 3 employees: {string.Join(", ", first3Employees.Select(e => e.Name))}");
            Console.WriteLine($"Skip first 2: {string.Join(", ", skipFirst2.Select(e => e.Name))}");
            Console.WriteLine($"High earners (while > 60000): {string.Join(", ", highEarners.Select(e => e.Name))}");
            
            // ============ ORDERING OPERATORS ============
            Console.WriteLine("\n=== 4. Ordering Operators ===");
            
            // OrderBy, ThenBy, OrderByDescending, ThenByDescending
            var orderedEmployees = employees
                .OrderBy(e => e.Department)
                .ThenByDescending(e => e.Salary);
            
            Console.WriteLine("Employees ordered by department, then by salary (desc):");
            foreach (var emp in orderedEmployees)
            {
                Console.WriteLine($"  {emp.Department} - {emp.Name}: ${emp.Salary}");
            }
            
            // Reverse
            var reversedNames = employees.Select(e => e.Name).Reverse();
            Console.WriteLine($"Reversed names: {string.Join(", ", reversedNames)}");
            
            // ============ GROUPING OPERATORS ============
            Console.WriteLine("\n=== 5. Grouping Operators ===");
            
            // GroupBy
            var employeesByDept = employees.GroupBy(e => e.Department);
            
            Console.WriteLine("Employees grouped by department:");
            foreach (var group in employeesByDept)
            {
                Console.WriteLine($"  {group.Key}: {group.Count()} employees");
                foreach (var emp in group)
                {
                    Console.WriteLine($"    - {emp.Name}: ${emp.Salary}");
                }
            }
            
            // GroupBy with result selector
            var deptStats = employees.GroupBy(
                e => e.Department,
                (key, group) => new
                {
                    Department = key,
                    EmployeeCount = group.Count(),
                    AvgSalary = group.Average(e => e.Salary),
                    MaxSalary = group.Max(e => e.Salary),
                    MinSalary = group.Min(e => e.Salary)
                });
            
            Console.WriteLine("\nDepartment statistics:");
            foreach (var stat in deptStats)
            {
                Console.WriteLine($"  {stat.Department}: {stat.EmployeeCount} employees, " +
                    $"Avg: ${stat.AvgSalary:F2}, Max: ${stat.MaxSalary}, Min: ${stat.MinSalary}");
            }
            
            // ============ SET OPERATORS ============
            Console.WriteLine("\n=== 6. Set Operators ===");
            
            List<int> setA = new List<int> { 1, 2, 3, 4, 5 };
            List<int> setB = new List<int> { 4, 5, 6, 7, 8 };
            
            Console.WriteLine($"Set A: {string.Join(", ", setA)}");
            Console.WriteLine($"Set B: {string.Join(", ", setB)}");
            Console.WriteLine($"Union: {string.Join(", ", setA.Union(setB))}");
            Console.WriteLine($"Intersect: {string.Join(", ", setA.Intersect(setB))}");
            Console.WriteLine($"Except (A - B): {string.Join(", ", setA.Except(setB))}");
            Console.WriteLine($"Distinct (from duplicates): {string.Join(", ", new List<int> { 1, 2, 2, 3, 3, 3 }.Distinct())}");
            
            // ============ QUANTIFIER OPERATORS ============
            Console.WriteLine("\n=== 7. Quantifier Operators ===");
            
            bool anyHighEarners = employees.Any(e => e.Salary > 100000);
            bool allHaveSalary = employees.All(e => e.Salary > 0);
            bool containsAlice = employees.Any(e => e.Name == "Alice");
            
            Console.WriteLine($"Any employees earning > $100k? {anyHighEarners}");
            Console.WriteLine($"All employees have salary > $0? {allHaveSalary}");
            Console.WriteLine($"Contains employee named 'Alice'? {containsAlice}");
            
            // ============ AGGREGATION OPERATORS ============
            Console.WriteLine("\n=== 8. Aggregation Operators ===");
            
            var totalSalary = employees.Sum(e => e.Salary);
            var avgSalary = employees.Average(e => e.Salary);
            var minSalary = employees.Min(e => e.Salary);
            var maxSalary = employees.Max(e => e.Salary);
            var employeeCount = employees.Count();
            var engineeringCount = employees.Count(e => e.Department == "Engineering");
            
            Console.WriteLine($"Total salary: ${totalSalary:F2}");
            Console.WriteLine($"Average salary: ${avgSalary:F2}");
            Console.WriteLine($"Minimum salary: ${minSalary}");
            Console.WriteLine($"Maximum salary: ${maxSalary}");
            Console.WriteLine($"Employee count: {employeeCount}");
            Console.WriteLine($"Engineering count: {engineeringCount}");
            
            // Aggregate - custom aggregation
            var salaryRanges = employees.Aggregate(
                new { Min = decimal.MaxValue, Max = decimal.MinValue },
                (acc, emp) => new
                {
                    Min = emp.Salary < acc.Min ? emp.Salary : acc.Min,
                    Max = emp.Salary > acc.Max ? emp.Salary : acc.Max
                });
            
            Console.WriteLine($"Salary range: ${salaryRanges.Min} - ${salaryRanges.Max}");
            
            // ============ ELEMENT OPERATORS ============
            Console.WriteLine("\n=== 9. Element Operators ===");
            
            try
            {
                var firstEmployee = employees.First();
                var firstEngineering = employees.First(e => e.Department == "Engineering");
                var firstOrDefaultHR = employees.FirstOrDefault(e => e.Department == "HR");
                var lastEmployee = employees.Last();
                var singleAlice = employees.Single(e => e.Name == "Alice");
                var elementAt = employees.ElementAt(2);
                
                Console.WriteLine($"First employee: {firstEmployee.Name}");
                Console.WriteLine($"First engineering employee: {firstEngineering.Name}");
                Console.WriteLine($"First or default HR: {(firstOrDefaultHR != null ? firstOrDefaultHR.Name : "null")}");
                Console.WriteLine($"Last employee: {lastEmployee.Name}");
                Console.WriteLine($"Single employee named Alice: {singleAlice.Name}");
                Console.WriteLine($"Element at index 2: {elementAt.Name}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Element operator error: {ex.Message}");
            }
            
            // ============ GENERATION OPERATORS ============
            Console.WriteLine("\n=== 10. Generation Operators ===");
            
            // Range
            var numbers = Enumerable.Range(1, 5);
            Console.WriteLine($"Range 1-5: {string.Join(", ", numbers)}");
            
            // Repeat
            var repeated = Enumerable.Repeat("Hello", 3);
            Console.WriteLine($"Repeat 'Hello' 3 times: {string.Join(", ", repeated)}");
            
            // Empty
            var emptyCollection = Enumerable.Empty<int>();
            Console.WriteLine($"Empty collection count: {emptyCollection.Count()}");
            
            // ============ JOIN OPERATORS ============
            Console.WriteLine("\n=== 11. Join Operators ===");
            
            // Already demonstrated Join earlier, now show GroupJoin
            List<Student> students = new List<Student>
            {
                new Student(1, "Alice"),
                new Student(2, "Bob"),
                new Student(3, "Charlie")
            };
            
            List<Course> courses = new List<Course>
            {
                new Course(101, "Math", 1),
                new Course(102, "Physics", 1),
                new Course(103, "Chemistry", 2),
                new Course(104, "Biology", 3)
            };
            
            // GroupJoin (left outer join)
            var studentsWithCourses = students.GroupJoin(courses,
                student => student.Id,
                course => course.StudentId,
                (student, studentCourses) => new
                {
                    Student = student.Name,
                    Courses = studentCourses.Select(c => c.Name)
                });
            
            Console.WriteLine("Students with their courses:");
            foreach (var sc in studentsWithCourses)
            {
                Console.WriteLine($"  {sc.Student}: {string.Join(", ", sc.Courses.DefaultIfEmpty("No courses"))}");
            }
            
            // ============ CONVERSION OPERATORS ============
            Console.WriteLine("\n=== 12. Conversion Operators ===");
            
            // ToArray, ToList, ToDictionary, ToLookup
            var employeeArray = employees.ToArray();
            var employeeList = employees.ToList();
            var employeeDict = employees.ToDictionary(e => e.Id, e => e.Name);
            var employeeLookup = employees.ToLookup(e => e.Department);
            
            Console.WriteLine($"Array length: {employeeArray.Length}");
            Console.WriteLine($"List count: {employeeList.Count}");
            Console.WriteLine($"Dictionary entries: {employeeDict.Count}");
            Console.WriteLine($"Lookup groups: {employeeLookup.Count}");
            
            // Cast and AsEnumerable
            IEnumerable<Employee> employeeEnumerable = employees.AsEnumerable();
            Console.WriteLine($"AsEnumerable count: {employeeEnumerable.Count()}");
            
            // OfType (already shown) and Cast
            List<object> objects = new List<object> { "hello", 42, "world", 3.14 };
            var castStrings = objects.OfType<string>(); // Only returns strings
            // var allStrings = objects.Cast<string>(); // Would throw on non-strings
            
            Console.WriteLine($"OfType<string> from objects: {string.Join(", ", castStrings)}");
        }
        
        static void DemonstrateDeferredExecution()
        {
            Console.WriteLine("\n============ DEFERRED EXECUTION ============\n");
            
            Console.WriteLine("=== 1. Understanding Deferred Execution ===");
            Console.WriteLine("""
                Deferred Execution (Lazy Evaluation):
                • LINQ queries are not executed when created
                • Execution happens when the result is enumerated (foreach, ToList, etc.)
                • Query is re-evaluated each time it's enumerated
                
                Immediate Execution:
                • Query executes immediately (ToList, ToArray, Count, First, etc.)
                • Results are materialized and stored
                
                Benefits of Deferred Execution:
                • Performance optimization (only process what's needed)
                • Ability to build queries incrementally
                • Re-evaluation with fresh data
                """);
            
            // ============ DEFERRED EXECUTION DEMONSTRATION ============
            Console.WriteLine("\n=== 2. Deferred Execution Demonstration ===");
            
            List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };
            
            // Create a deferred query
            var deferredQuery = numbers.Where(n =>
            {
                Console.WriteLine($"  Processing number: {n}");
                return n % 2 == 0;
            }).Select(n =>
            {
                Console.WriteLine($"  Transforming number: {n}");
                return n * 10;
            });
            
            Console.WriteLine("Query created (not executed yet)");
            Console.WriteLine("Adding number 6 to original list...");
            numbers.Add(6);
            
            Console.WriteLine("\nExecuting query (first iteration):");
            foreach (var result in deferredQuery)
            {
                Console.WriteLine($"  Result: {result}");
            }
            
            Console.WriteLine("\nExecuting query again (second iteration):");
            foreach (var result in deferredQuery)
            {
                Console.WriteLine($"  Result: {result}");
            }
            
            // ============ IMMEDIATE EXECUTION DEMONSTRATION ============
            Console.WriteLine("\n=== 3. Immediate Execution Demonstration ===");
            
            // Materialize the query with ToList()
            var immediateResult = numbers.Where(n =>
            {
                Console.WriteLine($"  Processing number: {n} (immediate)");
                return n % 2 == 0;
            }).Select(n =>
            {
                Console.WriteLine($"  Transforming number: {n} (immediate)");
                return n * 10;
            }).ToList(); // ToList() forces immediate execution
            
            Console.WriteLine("\nQuery executed immediately with ToList()");
            Console.WriteLine($"Results: {string.Join(", ", immediateResult)}");
            
            // Adding more numbers doesn't affect the materialized list
            numbers.Add(8);
            Console.WriteLine($"Added number 8, but materialized list unchanged: {string.Join(", ", immediateResult)}");
            
            // ============ QUERY RE-EVALUATION ============
            Console.WriteLine("\n=== 4. Query Re-evaluation ===");
            
            var sourceData = new List<int> { 10, 20, 30, 40 };
            var query = sourceData.Where(x => x > 15);
            
            Console.WriteLine($"First execution: {string.Join(", ", query)}");
            
            // Modify source data
            sourceData.Add(50);
            sourceData.Remove(10);
            
            Console.WriteLine($"After modifying source: {string.Join(", ", query)}");
            
            // ============ METHODS THAT TRIGGER IMMEDIATE EXECUTION ============
            Console.WriteLine("\n=== 5. Methods That Trigger Immediate Execution ===");
            Console.WriteLine("""
                The following methods cause immediate execution:
                • Aggregation: Count(), Sum(), Average(), Min(), Max()
                • Conversion: ToList(), ToArray(), ToDictionary(), ToLookup()
                • Element: First(), FirstOrDefault(), Single(), Last(), ElementAt()
                • Others: Any(), All(), Contains()
                """);
            
            // Example: Count() triggers execution
            var countQuery = numbers.Where(n => n > 10);
            Console.WriteLine($"Before Count(): Query defined but not executed");
            int count = countQuery.Count(); // Executes here
            Console.WriteLine($"After Count(): Executed, count = {count}");
            
            // ============ DEFERRED EXECUTION PITFALLS ============
            Console.WriteLine("\n=== 6. Deferred Execution Pitfalls ===");
            
            Console.WriteLine("Pitfall 1: Multiple enumerations causing repeated work");
            var expensiveQuery = Enumerable.Range(1, 5).Select(n =>
            {
                Console.WriteLine($"  Expensive operation on {n}");
                return n * n;
            });
            
            Console.WriteLine("First enumeration:");
            foreach (var item in expensiveQuery) { /* Just enumerating */ }
            
            Console.WriteLine("Second enumeration (repeats work):");
            foreach (var item in expensiveQuery) { /* Just enumerating */ }
            
            Console.WriteLine("\nSolution: Materialize with ToList() for multiple uses");
            var materialized = expensiveQuery.ToList();
            
            Console.WriteLine("Pitfall 2: Closure over modified variable");
            var filters = new List<Func<int, bool>>();
            for (int i = 0; i < 3; i++)
            {
                // Captures variable i, not value at iteration time
                filters.Add(x => x > i);
            }
            
            Console.WriteLine($"Filters count: {filters.Count}");
            Console.WriteLine($"All filters use final i value (3): {filters[0](5)}");
            
            Console.WriteLine("\nSolution: Create local variable in loop");
            var fixedFilters = new List<Func<int, bool>>();
            for (int i = 0; i < 3; i++)
            {
                int localI = i; // Local copy
                fixedFilters.Add(x => x > localI);
            }
            
            Console.WriteLine($"Fixed filters: {fixedFilters[0](5)}, {fixedFilters[1](5)}, {fixedFilters[2](5)}");
        }
        
        static void DemonstrateLinqToXml()
        {
            Console.WriteLine("\n============ LINQ TO XML ============\n");
            
            Console.WriteLine("=== 1. LINQ to XML Overview ===");
            Console.WriteLine("""
                LINQ to XML provides an in-memory XML programming interface
                that takes advantage of LINQ query capabilities.
                
                Key classes:
                • XDocument - Represents an XML document
                • XElement - Represents an XML element
                • XAttribute - Represents an XML attribute
                • XNamespace - Represents an XML namespace
                
                Benefits:
                • Simplified XML creation and manipulation
                • Strongly-typed queries using LINQ
                • Functional construction (fluent API)
                """);
            
            // ============ CREATING XML WITH LINQ TO XML ============
            Console.WriteLine("\n=== 2. Creating XML ===");
            
            // Functional construction (fluent API)
            XDocument catalog = new XDocument(
                new XElement("Catalog",
                    new XElement("Product",
                        new XAttribute("Id", 1),
                        new XElement("Name", "Laptop"),
                        new XElement("Price", 999.99),
                        new XElement("Category", "Electronics")
                    ),
                    new XElement("Product",
                        new XAttribute("Id", 2),
                        new XElement("Name", "Coffee Mug"),
                        new XElement("Price", 12.99),
                        new XElement("Category", "Kitchen")
                    ),
                    new XElement("Product",
                        new XAttribute("Id", 3),
                        new XElement("Name", "Desk Chair"),
                        new XElement("Price", 249.99),
                        new XElement("Category", "Furniture")
                    )
                )
            );
            
            Console.WriteLine("Created XML catalog:");
            Console.WriteLine(catalog.ToString());
            
            // ============ QUERYING XML WITH LINQ ============
            Console.WriteLine("\n=== 3. Querying XML ===");
            
            // Query syntax
            var expensiveProducts = from product in catalog.Descendants("Product")
                                    where (decimal)product.Element("Price") > 100
                                    select new
                                    {
                                        Id = (int)product.Attribute("Id"),
                                        Name = (string)product.Element("Name"),
                                        Price = (decimal)product.Element("Price")
                                    };
            
            Console.WriteLine("Expensive products (> $100):");
            foreach (var product in expensiveProducts)
            {
                Console.WriteLine($"  {product.Name} (ID: {product.Id}): ${product.Price}");
            }
            
            // Method syntax with XPath-like navigation
            var electronics = catalog.Descendants("Product")
                .Where(p => (string)p.Element("Category") == "Electronics")
                .Select(p => new
                {
                    Name = (string)p.Element("Name"),
                    Price = (decimal)p.Element("Price")
                });
            
            Console.WriteLine("\nElectronics:");
            foreach (var item in electronics)
            {
                Console.WriteLine($"  {item.Name}: ${item.Price}");
            }
            
            // ============ MODIFYING XML ============
            Console.WriteLine("\n=== 4. Modifying XML ===");
            
            // Add a new product
            catalog.Root.Add(
                new XElement("Product",
                    new XAttribute("Id", 4),
                    new XElement("Name", "Keyboard"),
                    new XElement("Price", 49.99),
                    new XElement("Category", "Electronics")
                )
            );
            
            Console.WriteLine("Added new product:");
            var keyboard = catalog.Descendants("Product")
                .FirstOrDefault(p => (string)p.Element("Name") == "Keyboard");
            Console.WriteLine($"  {keyboard?.Element("Name")?.Value}: ${keyboard?.Element("Price")?.Value}");
            
            // Update existing product
            var laptop = catalog.Descendants("Product")
                .FirstOrDefault(p => (string)p.Element("Name") == "Laptop");
            if (laptop != null)
            {
                laptop.Element("Price").Value = "899.99";
                Console.WriteLine($"Updated laptop price to: ${laptop.Element("Price").Value}");
            }
            
            // ============ XML NAMESPACES ============
            Console.WriteLine("\n=== 5. XML Namespaces ===");
            
            XNamespace ns = "http://example.com/products";
            XDocument catalogWithNs = new XDocument(
                new XElement(ns + "Catalog",
                    new XElement(ns + "Product",
                        new XAttribute("Id", 1),
                        new XElement(ns + "Name", "Smartphone"),
                        new XElement(ns + "Price", 799.99)
                    )
                )
            );
            
            Console.WriteLine("XML with namespace:");
            Console.WriteLine(catalogWithNs.ToString());
            
            // Query with namespace
            var nsProducts = from product in catalogWithNs.Descendants(ns + "Product")
                             select new
                             {
                                 Name = (string)product.Element(ns + "Name"),
                                 Price = (decimal)product.Element(ns + "Price")
                             };
            
            Console.WriteLine("\nProducts with namespace:");
            foreach (var product in nsProducts)
            {
                Console.WriteLine($"  {product.Name}: ${product.Price}");
            }
        }
        
        static void DemonstratePerformanceConsiderations()
        {
            Console.WriteLine("\n============ PERFORMANCE CONSIDERATIONS ============\n");
            
            // ============ N+1 QUERY PROBLEM ============
            Console.WriteLine("=== 1. N+1 Query Problem ===");
            
            List<Order> orders = new List<Order>
            {
                new Order(1, 101, 99.99m),
                new Order(2, 101, 49.99m),
                new Order(3, 102, 149.99m),
                new Order(4, 103, 29.99m)
            };
            
            List<Customer> customers = new List<Customer>
            {
                new Customer(101, "Alice", "alice@example.com"),
                new Customer(102, "Bob", "bob@example.com"),
                new Customer(103, "Charlie", "charlie@example.com")
            };
            
            Console.WriteLine("Inefficient N+1 pattern:");
            // Bad: Query for each order's customer separately
            foreach (var order in orders)
            {
                var customer = customers.FirstOrDefault(c => c.Id == order.CustomerId);
                Console.WriteLine($"  Order {order.OrderId}: {customer?.Name}");
            }
            
            Console.WriteLine("\nEfficient join pattern:");
            // Good: Single query with join
            var orderDetails = from o in orders
                               join c in customers on o.CustomerId equals c.Id
                               select new { o.OrderId, c.Name, o.Amount };
            
            foreach (var detail in orderDetails)
            {
                Console.WriteLine($"  Order {detail.OrderId}: {detail.Name}, Amount: ${detail.Amount}");
            }
            
            // ============ MATERIALIZATION OVERHEAD ============
            Console.WriteLine("\n=== 2. Materialization Overhead ===");
            
            // Create large dataset
            var largeDataset = Enumerable.Range(1, 1000000);
            
            Console.WriteLine("Testing materialization overhead...");
            
            // Measure time for deferred vs immediate
            var sw = System.Diagnostics.Stopwatch.StartNew();
            
            // Deferred: Only processes what's needed
            var deferred = largeDataset.Where(x => x % 2 == 0).Take(10);
            var deferredList = deferred.ToList(); // Processes only until 10 matches found
            
            sw.Stop();
            Console.WriteLine($"Deferred (take 10 even numbers): {sw.ElapsedMilliseconds}ms, Count: {deferredList.Count}");
            
            sw.Restart();
            
            // Immediate: Processes entire dataset
            var immediate = largeDataset.Where(x => x % 2 == 0).ToList(); // Processes all 1M elements
            var immediateFirst10 = immediate.Take(10).ToList();
            
            sw.Stop();
            Console.WriteLine($"Immediate (filter all then take 10): {sw.ElapsedMilliseconds}ms, Count: {immediateFirst10.Count}");
            
            // ============ INDEXED QUERIES ============
            Console.WriteLine("\n=== 3. Indexed Queries ===");
            
            // For large collections, consider using indexed data structures
            Dictionary<int, Customer> customerDict = customers.ToDictionary(c => c.Id, c => c);
            
            Console.WriteLine("Dictionary lookup vs LINQ FirstOrDefault:");
            
            sw.Restart();
            for (int i = 0; i < 10000; i++)
            {
                var cust = customers.FirstOrDefault(c => c.Id == 101); // O(n)
            }
            sw.Stop();
            Console.WriteLine($"  10,000 LINQ FirstOrDefault: {sw.ElapsedMilliseconds}ms");
            
            sw.Restart();
            for (int i = 0; i < 10000; i++)
            {
                var cust = customerDict.TryGetValue(101, out var c) ? c : null; // O(1)
            }
            sw.Stop();
            Console.WriteLine($"  10,000 Dictionary lookups: {sw.ElapsedMilliseconds}ms");
            
            // ============ QUERY COMPLEXITY ============
            Console.WriteLine("\n=== 4. Query Complexity ===");
            
            Console.WriteLine("Complex query with multiple operations:");
            var complexQuery = Enumerable.Range(1, 1000)
                .Where(x => x % 2 == 0)          // O(n)
                .Select(x => x * x)              // O(n)
                .OrderByDescending(x => x)       // O(n log n) - most expensive
                .GroupBy(x => x % 10)            // O(n)
                .Select(g => new { Key = g.Key, Count = g.Count() }) // O(n)
                .ToList();
            
            Console.WriteLine($"Complex query result count: {complexQuery.Count}");
            
            // ============ AS PARALLEL LINQ (PLINQ) ============
            Console.WriteLine("\n=== 5. AsParallel (PLINQ) ===");
            
            Console.WriteLine("""
                Use AsParallel() for CPU-bound operations on large datasets.
                Be careful with overhead and thread safety.
                """);
            
            var numbers = Enumerable.Range(1, 1000000);
            
            sw.Restart();
            var sequential = numbers.Where(x => IsPrime(x)).Take(100).ToList();
            sw.Stop();
            Console.WriteLine($"Sequential prime search: {sw.ElapsedMilliseconds}ms");
            
            sw.Restart();
            var parallel = numbers.AsParallel()
                .Where(x => IsPrime(x))
                .Take(100)
                .ToList();
            sw.Stop();
            Console.WriteLine($"Parallel prime search: {sw.ElapsedMilliseconds}ms");
            
            // ============ MEMORY ALLOCATION ============
            Console.WriteLine("\n=== 6. Memory Allocation ===");
            
            Console.WriteLine("Anonymous types create new objects:");
            var allocations = Enumerable.Range(1, 10000)
                .Select(i => new { Index = i, Value = i * 2 }) // Creates 10,000 objects
                .ToList();
            
            Console.WriteLine($"Created {allocations.Count} anonymous objects");
            
            Console.WriteLine("\nConsider using value tuples or structs for less overhead:");
            var valueTuples = Enumerable.Range(1, 10000)
                .Select(i => (Index: i, Value: i * 2)) // Value tuple (stack allocated)
                .ToList();
            
            Console.WriteLine($"Created {valueTuples.Count} value tuples");
        }
        
        static void DemonstrateAdvancedPatterns()
        {
            Console.WriteLine("\n============ ADVANCED LINQ PATTERNS ============\n");
            
            // ============ CUSTOM LINQ OPERATORS ============
            Console.WriteLine("=== 1. Custom LINQ Operators ===");
            
            Console.WriteLine("Creating custom WhereNot operator:");
            
            var numbers = Enumerable.Range(1, 10);
            var notEven = numbers.WhereNot(n => n % 2 == 0);
            Console.WriteLine($"Numbers not even: {string.Join(", ", notEven)}");
            
            // ============ EXPRESSION TREES ============
            Console.WriteLine("\n=== 2. Expression Trees ===");
            
            Console.WriteLine("""
                Expression trees represent code as data, enabling:
                • Dynamic query construction
                • Translation to other query languages (SQL, etc.)
                • Runtime query optimization
                """);
            
            // Simple expression tree example
            System.Linq.Expressions.Expression<Func<int, bool>> isEvenExpr = x => x % 2 == 0;
            Console.WriteLine($"Expression: {isEvenExpr}");
            Console.WriteLine($"Expression body: {isEvenExpr.Body}");
            Console.WriteLine($"Expression parameters: {string.Join(", ", isNevenExpr.Parameters)}");
            
            // Compile and execute
            var isEvenFunc = isEvenExpr.Compile();
            Console.WriteLine($"Is 5 even? {isEvenFunc(5)}");
            Console.WriteLine($"Is 6 even? {isEvenFunc(6)}");
            
            // ============ DYNAMIC QUERY CONSTRUCTION ============
            Console.WriteLine("\n=== 3. Dynamic Query Construction ===");
            
            var products = new List<Product>
            {
                new Product(1, "Laptop", 999.99m, "Electronics"),
                new Product(2, "Coffee Mug", 12.99m, "Kitchen"),
                new Product(3, "Desk Chair", 249.99m, "Furniture"),
                new Product(4, "Smartphone", 799.99m, "Electronics")
            };
            
            // Build query dynamically based on conditions
            IQueryable<Product> query = products.AsQueryable();
            
            string categoryFilter = "Electronics";
            decimal? minPrice = 500;
            decimal? maxPrice = 1000;
            
            if (!string.IsNullOrEmpty(categoryFilter))
            {
                query = query.Where(p => p.Category == categoryFilter);
            }
            
            if (minPrice.HasValue)
            {
                query = query.Where(p => p.Price >= minPrice.Value);
            }
            
            if (maxPrice.HasValue)
            {
                query = query.Where(p => p.Price <= maxPrice.Value);
            }
            
            var results = query.OrderBy(p => p.Price).ToList();
            
            Console.WriteLine($"Dynamic query results ({results.Count} items):");
            foreach (var p in results)
            {
                Console.WriteLine($"  {p.Name}: ${p.Price} ({p.Category})");
            }
            
            // ============ LAZY EVALUATION WITH YIELD ============
            Console.WriteLine("\n=== 4. Lazy Evaluation with Yield ===");
            
            Console.WriteLine("Custom sequence generator with yield:");
            
            foreach (var number in GenerateFibonacci(10))
            {
                Console.Write($"{number} ");
            }
            Console.WriteLine();
            
            // ============ QUERY COMPOSITION ============
            Console.WriteLine("\n=== 5. Query Composition ===");
            
            // Build queries incrementally
            var baseQuery = products.AsQueryable();
            
            // Add filters based on business logic
            var filteredQuery = baseQuery.Where(p => p.Price > 100);
            
            // Add ordering
            var orderedQuery = filteredQuery.OrderByDescending(p => p.Price);
            
            // Add paging
            var pagedQuery = orderedQuery.Skip(0).Take(2);
            
            Console.WriteLine("Composed query results:");
            foreach (var p in pagedQuery)
            {
                Console.WriteLine($"  {p.Name}: ${p.Price}");
            }
            
            // ============ MONAD PATTERNS ============
            Console.WriteLine("\n=== 6. Monad Patterns (SelectMany) ===");
            
            // Flattening nested collections
            var departments = new List<Department>
            {
                new Department("Engineering", new List<string> { "Alice", "Bob" }),
                new Department("Sales", new List<string> { "Charlie", "Diana" })
            };
            
            // Without SelectMany (nested loops)
            Console.WriteLine("All employees (nested loops):");
            foreach (var dept in departments)
            {
                foreach (var employee in dept.Members)
                {
                    Console.WriteLine($"  {employee} ({dept.Name})");
                }
            }
            
            // With SelectMany (flattened)
            Console.WriteLine("\nAll employees (SelectMany):");
            var allEmployees = departments.SelectMany(dept => 
                dept.Members.Select(employee => $"{employee} ({dept.Name})"));
            
            foreach (var emp in allEmployees)
            {
                Console.WriteLine($"  {emp}");
            }
        }
        
        static void DemonstrateRealWorldExamples()
        {
            Console.WriteLine("\n============ REAL-WORLD LINQ EXAMPLES ============\n");
            
            // ============ DATA ANALYSIS ============
            Console.WriteLine("=== 1. Data Analysis ===");
            
            List<SalesTransaction> transactions = new List<SalesTransaction>
            {
                new SalesTransaction(1, "Alice", "Laptop", 999.99m, new DateTime(2024, 1, 15)),
                new SalesTransaction(2, "Bob", "Mouse", 49.99m, new DateTime(2024, 1, 16)),
                new SalesTransaction(3, "Alice", "Keyboard", 79.99m, new DateTime(2024, 1, 17)),
                new SalesTransaction(4, "Charlie", "Monitor", 349.99m, new DateTime(2024, 2, 1)),
                new SalesTransaction(5, "Bob", "Laptop", 999.99m, new DateTime(2024, 2, 5)),
                new SalesTransaction(6, "Alice", "Monitor", 349.99m, new DateTime(2024, 2, 10))
            };
            
            // Monthly sales report
            var monthlySales = transactions
                .GroupBy(t => new { t.Date.Year, t.Date.Month })
                .Select(g => new
                {
                    Year = g.Key.Year,
                    Month = g.Key.Month,
                    TotalSales = g.Sum(t => t.Amount),
                    TransactionCount = g.Count(),
                    AverageSale = g.Average(t => t.Amount)
                })
                .OrderBy(g => g.Year).ThenBy(g => g.Month);
            
            Console.WriteLine("Monthly Sales Report:");
            foreach (var month in monthlySales)
            {
                Console.WriteLine($"  {month.Year}-{month.Month:D2}: " +
                    $"{month.TransactionCount} transactions, " +
                    $"Total: ${month.TotalSales:F2}, " +
                    $"Avg: ${month.AverageSale:F2}");
            }
            
            // Top customers
            var topCustomers = transactions
                .GroupBy(t => t.SalesPerson)
                .Select(g => new
                {
                    SalesPerson = g.Key,
                    TotalSales = g.Sum(t => t.Amount),
                    TransactionCount = g.Count()
                })
                .OrderByDescending(c => c.TotalSales)
                .Take(3);
            
            Console.WriteLine("\nTop 3 Customers by Sales:");
            foreach (var customer in topCustomers)
            {
                Console.WriteLine($"  {customer.SalesPerson}: " +
                    $"{customer.TransactionCount} transactions, " +
                    $"Total: ${customer.TotalSales:F2}");
            }
            
            // ============ DATA VALIDATION ============
            Console.WriteLine("\n=== 2. Data Validation ===");
            
            List<User> users = new List<User>
            {
                new User(1, "alice@example.com", "Alice", 25),
                new User(2, "bob@example", "Bob", 17), // Invalid email
                new User(3, "charlie@example.com", "", 30), // Empty name
                new User(4, "diana@example.com", "Diana", 15) // Underage
            };
            
            // Find invalid users
            var invalidUsers = users.Where(u =>
                !IsValidEmail(u.Email) ||
                string.IsNullOrWhiteSpace(u.Name) ||
                u.Age < 18);
            
            Console.WriteLine("Invalid Users:");
            foreach (var user in invalidUsers)
            {
                List<string> issues = new List<string>();
                if (!IsValidEmail(user.Email)) issues.Add("Invalid email");
                if (string.IsNullOrWhiteSpace(user.Name)) issues.Add("Empty name");
                if (user.Age < 18) issues.Add("Underage");
                
                Console.WriteLine($"  {user.Name} (ID: {user.Id}): {string.Join(", ", issues)}");
            }
            
            // ============ PAGINATION ============
            Console.WriteLine("\n=== 3. Pagination ===");
            
            var allProducts = Enumerable.Range(1, 100)
                .Select(i => new Product(i, $"Product {i}", i * 10m, "Category " + (i % 5)));
            
            int pageSize = 10;
            int pageNumber = 2; // 0-based or 1-based depends on your convention
            
            var page = allProducts
                .Skip(pageNumber * pageSize)
                .Take(pageSize)
                .ToList();
            
            Console.WriteLine($"Page {pageNumber + 1} (items {pageNumber * pageSize + 1}-{pageNumber * pageSize + page.Count}):");
            foreach (var product in page)
            {
                Console.WriteLine($"  {product.Name}: ${product.Price}");
            }
            
            // Total pages calculation
            int totalItems = allProducts.Count();
            int totalPages = (int)Math.Ceiling((double)totalItems / pageSize);
            Console.WriteLine($"Total pages: {totalPages}");
            
            // ============ SEARCH WITH MULTIPLE CRITERIA ============
            Console.WriteLine("\n=== 4. Search with Multiple Criteria ===");
            
            string searchTerm = "lap";
            decimal? minPrice = 500;
            decimal? maxPrice = 1000;
            string category = "Electronics";
            
            var searchResults = allProducts
                .Where(p => 
                    (string.IsNullOrEmpty(searchTerm) || p.Name.Contains(searchTerm, StringComparison.OrdinalIgnoreCase)) &&
                    (!minPrice.HasValue || p.Price >= minPrice.Value) &&
                    (!maxPrice.HasValue || p.Price <= maxPrice.Value) &&
                    (string.IsNullOrEmpty(category) || p.Category == category))
                .OrderBy(p => p.Price)
                .ToList();
            
            Console.WriteLine($"Search results: {searchResults.Count} products found");
            
            // ============ BATCH PROCESSING ============
            Console.WriteLine("\n=== 5. Batch Processing ===");
            
            var largeDataSet = Enumerable.Range(1, 1000);
            int batchSize = 100;
            
            Console.WriteLine("Processing in batches:");
            for (int i = 0; i < largeDataSet.Count(); i += batchSize)
            {
                var batch = largeDataSet.Skip(i).Take(batchSize).ToList();
                Console.WriteLine($"  Processing batch {i / batchSize + 1}: items {i + 1}-{i + batch.Count}");
                // Process batch here
            }
            
            // ============ DATA TRANSFORMATION PIPELINE ============
            Console.WriteLine("\n=== 6. Data Transformation Pipeline ===");
            
            var rawData = new List<string>
            {
                "Alice,25,Engineer",
                "Bob,30,Designer",
                "Charlie,35,Manager",
                "Invalid Data",
                "Diana,28,Developer"
            };
            
            var processedData = rawData
                .Select(line => line.Split(','))
                .Where(parts => parts.Length == 3)
                .Select(parts => new
                {
                    Name = parts[0],
                    Age = int.TryParse(parts[1], out int age) ? age : 0,
                    JobTitle = parts[2]
                })
                .Where(person => person.Age > 0)
                .OrderBy(person => person.Name)
                .ToList();
            
            Console.WriteLine("Processed data:");
            foreach (var person in processedData)
            {
                Console.WriteLine($"  {person.Name}, {person.Age}, {person.JobTitle}");
            }
        }
        
        // Helper methods
        static bool IsValidEmail(string email)
        {
            return !string.IsNullOrEmpty(email) && email.Contains("@") && email.Contains(".");
        }
        
        static bool IsPrime(int number)
        {
            if (number <= 1) return false;
            if (number == 2) return true;
            if (number % 2 == 0) return false;
            
            var boundary = (int)Math.Floor(Math.Sqrt(number));
            
            for (int i = 3; i <= boundary; i += 2)
            {
                if (number % i == 0) return false;
            }
            
            return true;
        }
        
        static IEnumerable<int> GenerateFibonacci(int count)
        {
            int a = 0, b = 1;
            
            for (int i = 0; i < count; i++)
            {
                yield return a;
                int temp = a;
                a = b;
                b = temp + b;
            }
        }
    }
    
    // Custom LINQ extension method
    public static class LinqExtensions
    {
        public static IEnumerable<TSource> WhereNot<TSource>(
            this IEnumerable<TSource> source,
            Func<TSource, bool> predicate)
        {
            return source.Where(item => !predicate(item));
        }
    }
    
    // Data classes
    public class Product
    {
        public int Id { get; }
        public string Name { get; }
        public decimal Price { get; }
        public string Category { get; }
        
        public Product(int id, string name, decimal price, string category)
        {
            Id = id;
            Name = name;
            Price = price;
            Category = category;
        }
    }
    
    public class Customer
    {
        public int Id { get; }
        public string Name { get; }
        public string Email { get; }
        
        public Customer(int id, string name, string email)
        {
            Id = id;
            Name = name;
            Email = email;
        }
    }
    
    public class Order
    {
        public int OrderId { get; }
        public int CustomerId { get; }
        public decimal Amount { get; }
        
        public Order(int orderId, int customerId, decimal amount)
        {
            OrderId = orderId;
            CustomerId = customerId;
            Amount = amount;
        }
    }
    
    public class Employee
    {
        public int Id { get; }
        public string Name { get; }
        public string Department { get; }
        public decimal Salary { get; }
        public DateTime HireDate { get; }
        
        public Employee(int id, string name, string department, decimal salary, DateTime hireDate)
        {
            Id = id;
            Name = name;
            Department = department;
            Salary = salary;
            HireDate = hireDate;
        }
    }
    
    public class Department
    {
        public string Name { get; }
        public List<string> Members { get; }
        
        public Department(string name, List<string> members)
        {
            Name = name;
            Members = members;
        }
    }
    
    public class Student
    {
        public int Id { get; }
        public string Name { get; }
        
        public Student(int id, string name)
        {
            Id = id;
            Name = name;
        }
    }
    
    public class Course
    {
        public int Id { get; }
        public string Name { get; }
        public int StudentId { get; }
        
        public Course(int id, string name, int studentId)
        {
            Id = id;
            Name = name;
            StudentId = studentId;
        }
    }
    
    public class SalesTransaction
    {
        public int Id { get; }
        public string SalesPerson { get; }
        public string Product { get; }
        public decimal Amount { get; }
        public DateTime Date { get; }
        
        public SalesTransaction(int id, string salesPerson, string product, decimal amount, DateTime date)
        {
            Id = id;
            SalesPerson = salesPerson;
            Product = product;
            Amount = amount;
            Date = date;
        }
    }
    
    public class User
    {
        public int Id { get; }
        public string Email { get; }
        public string Name { get; }
        public int Age { get; }
        
        public User(int id, string email, string name, int age)
        {
            Id = id;
            Email = email;
            Name = name;
            Age = age;
        }
    }
}