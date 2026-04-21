/*
    C# COLLECTIONS
    File: 07_collections.cs
    
    This file demonstrates collections in C# programming.
    Covering concepts from junior to upper mid-level.
*/

using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace CSharpRefresher.Collections
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Collections Demonstration ===\n");
            
            DemonstrateArrays();
            DemonstrateLists();
            DemonstrateDictionaries();
            DemonstrateSets();
            DemonstrateQueuesAndStacks();
            DemonstrateCollectionInterfaces();
            DemonstrateLINQWithCollections();
            
            Console.WriteLine("\n=== Collections Complete ===");
        }
        
        static void DemonstrateArrays()
        {
            Console.WriteLine("============ ARRAYS ============\n");
            
            // Single-dimensional array
            Console.WriteLine("=== Single-dimensional Array ===");
            int[] numbers = new int[5] { 1, 2, 3, 4, 5 };
            Console.WriteLine($"Array length: {numbers.Length}");
            Console.WriteLine($"Elements: {string.Join(", ", numbers)}");
            
            // Multi-dimensional array
            Console.WriteLine("\n=== Multi-dimensional Array ===");
            int[,] matrix = new int[2, 3] { { 1, 2, 3 }, { 4, 5, 6 } };
            Console.WriteLine($"Matrix[1,2]: {matrix[1, 2]}");
            Console.WriteLine($"Total elements: {matrix.Length}");
            
            // Jagged array (array of arrays)
            Console.WriteLine("\n=== Jagged Array ===");
            int[][] jagged = new int[3][];
            jagged[0] = new int[] { 1, 2, 3 };
            jagged[1] = new int[] { 4, 5 };
            jagged[2] = new int[] { 6, 7, 8, 9 };
            
            Console.WriteLine($"jagged[2][3]: {jagged[2][3]}");
            Console.WriteLine($"Total arrays: {jagged.Length}");
            
            // Array methods
            Console.WriteLine("\n=== Array Methods ===");
            Array.Sort(numbers);
            Array.Reverse(numbers);
            int index = Array.IndexOf(numbers, 3);
            Array.Resize(ref numbers, 10);
            
            Console.WriteLine($"Sorted & reversed: {string.Join(", ", numbers)}");
            Console.WriteLine($"Index of 3: {index}");
            Console.WriteLine($"New length: {numbers.Length}");
        }
        
        static void DemonstrateLists()
        {
            Console.WriteLine("\n============ LISTS ============\n");
            
            // List creation
            Console.WriteLine("=== List Creation ===");
            List<string> fruits = new List<string> { "Apple", "Banana", "Cherry" };
            List<int> numbers = new List<int>();
            
            // Adding elements
            Console.WriteLine("\n=== Adding Elements ===");
            fruits.Add("Date");
            fruits.AddRange(new[] { "Elderberry", "Fig" });
            fruits.Insert(1, "Apricot");
            
            Console.WriteLine($"Fruits: {string.Join(", ", fruits)}");
            Console.WriteLine($"Count: {fruits.Count}, Capacity: {fruits.Capacity}");
            
            // Accessing elements
            Console.WriteLine("\n=== Accessing Elements ===");
            Console.WriteLine($"First: {fruits[0]}, Last: {fruits[^1]}");
            Console.WriteLine($"Contains 'Banana': {fruits.Contains("Banana")}");
            Console.WriteLine($"Index of 'Cherry': {fruits.IndexOf("Cherry")}");
            
            // Removing elements
            Console.WriteLine("\n=== Removing Elements ===");
            fruits.Remove("Fig");
            fruits.RemoveAt(0);
            fruits.RemoveAll(f => f.StartsWith("A"));
            fruits.RemoveRange(1, 2);
            
            Console.WriteLine($"After removal: {string.Join(", ", fruits)}");
            
            // List methods
            Console.WriteLine("\n=== List Methods ===");
            numbers.AddRange(new[] { 5, 2, 8, 1, 9 });
            numbers.Sort();
            numbers.Reverse();
            
            Console.WriteLine($"Sorted numbers: {string.Join(", ", numbers)}");
            Console.WriteLine($"Min: {numbers.Min()}, Max: {numbers.Max()}, Sum: {numbers.Sum()}");
            
            // List capacity
            Console.WriteLine("\n=== List Capacity ===");
            List<int> largeList = new List<int>();
            for (int i = 0; i < 100; i++)
            {
                largeList.Add(i);
                if (i % 25 == 0)
                    Console.WriteLine($"Count: {largeList.Count}, Capacity: {largeList.Capacity}");
            }
            
            // Trim excess
            largeList.TrimExcess();
            Console.WriteLine($"After TrimExcess - Capacity: {largeList.Capacity}");
        }
        
        static void DemonstrateDictionaries()
        {
            Console.WriteLine("\n============ DICTIONARIES ============\n");
            
            // Dictionary creation
            Console.WriteLine("=== Dictionary Creation ===");
            Dictionary<string, int> ages = new Dictionary<string, int>
            {
                ["Alice"] = 30,
                ["Bob"] = 25,
                ["Charlie"] = 35
            };
            
            // Alternative syntax
            Dictionary<int, string> products = new Dictionary<int, string>
            {
                { 1, "Laptop" },
                { 2, "Phone" },
                { 3, "Tablet" }
            };
            
            Console.WriteLine($"Alice's age: {ages["Alice"]}");
            Console.WriteLine($"Product 2: {products[2]}");
            
            // Adding and updating
            Console.WriteLine("\n=== Adding and Updating ===");
            ages["David"] = 28; // Add new
            ages["Alice"] = 31; // Update existing
            
            ages.Add("Eve", 27); // Alternative add
            // ages.Add("Eve", 30); // ERROR: Key already exists
            
            Console.WriteLine($"All ages: {string.Join(", ", ages.Select(kv => $"{kv.Key}:{kv.Value}"))}");
            
            // Checking and accessing
            Console.WriteLine("\n=== Checking and Accessing ===");
            bool hasBob = ages.ContainsKey("Bob");
            bool hasAge30 = ages.ContainsValue(30);
            
            Console.WriteLine($"Has key 'Bob': {hasBob}");
            Console.WriteLine($"Has value 30: {hasAge30}");
            
            // Safe access with TryGetValue
            if (ages.TryGetValue("Frank", out int frankAge))
                Console.WriteLine($"Frank's age: {frankAge}");
            else
                Console.WriteLine("Frank not found");
            
            // Removing
            Console.WriteLine("\n=== Removing ===");
            ages.Remove("Charlie");
            ages.Remove("Nonexistent"); // Returns false, no error
            
            Console.WriteLine($"After removal: {string.Join(", ", ages.Select(kv => $"{kv.Key}:{kv.Value}"))}");
            
            // Dictionary iteration
            Console.WriteLine("\n=== Dictionary Iteration ===");
            foreach (var kvp in ages)
            {
                Console.WriteLine($"  {kvp.Key} is {kvp.Value} years old");
            }
            
            foreach (string name in ages.Keys)
            {
                Console.WriteLine($"  Key: {name}");
            }
            
            foreach (int age in ages.Values)
            {
                Console.WriteLine($"  Value: {age}");
            }
        }
        
        static void DemonstrateSets()
        {
            Console.WriteLine("\n============ SETS ============\n");
            
            // HashSet - unordered collection of unique elements
            Console.WriteLine("=== HashSet ===");
            HashSet<int> set1 = new HashSet<int> { 1, 2, 3, 4, 5 };
            HashSet<int> set2 = new HashSet<int> { 4, 5, 6, 7, 8 };
            
            Console.WriteLine($"Set1: {string.Join(", ", set1)}");
            Console.WriteLine($"Set2: {string.Join(", ", set2)}");
            
            // Set operations
            Console.WriteLine("\n=== Set Operations ===");
            HashSet<int> union = new HashSet<int>(set1);
            union.UnionWith(set2);
            Console.WriteLine($"Union: {string.Join(", ", union)}");
            
            HashSet<int> intersection = new HashSet<int>(set1);
            intersection.IntersectWith(set2);
            Console.WriteLine($"Intersection: {string.Join(", ", intersection)}");
            
            HashSet<int> except = new HashSet<int>(set1);
            except.ExceptWith(set2);
            Console.WriteLine($"Set1 except Set2: {string.Join(", ", except)}");
            
            HashSet<int> symmetricExcept = new HashSet<int>(set1);
            symmetricExcept.SymmetricExceptWith(set2);
            Console.WriteLine($"Symmetric difference: {string.Join(", ", symmetricExcept)}");
            
            // Set comparisons
            Console.WriteLine("\n=== Set Comparisons ===");
            Console.WriteLine($"Set1 is subset of union: {set1.IsSubsetOf(union)}");
            Console.WriteLine($"Union is superset of set1: {union.IsSupersetOf(set1)}");
            Console.WriteLine($"Set1 overlaps set2: {set1.Overlaps(set2)}");
            Console.WriteLine($"Set1 equals set2: {set1.SetEquals(set2)}");
            
            // SortedSet - sorted unique elements
            Console.WriteLine("\n=== SortedSet ===");
            SortedSet<string> sortedNames = new SortedSet<string>
            {
                "Charlie", "Alice", "Bob", "David"
            };
            
            Console.WriteLine($"Sorted names: {string.Join(", ", sortedNames)}");
            Console.WriteLine($"Min: {sortedNames.Min}, Max: {sortedNames.Max}");
            
            // Get view between
            foreach (string name in sortedNames.GetViewBetween("B", "D"))
            {
                Console.WriteLine($"  Between B and D: {name}");
            }
        }
        
        static void DemonstrateQueuesAndStacks()
        {
            Console.WriteLine("\n============ QUEUES AND STACKS ============\n");
            
            // Queue - FIFO (First In, First Out)
            Console.WriteLine("=== Queue (FIFO) ===");
            Queue<string> queue = new Queue<string>();
            queue.Enqueue("First");
            queue.Enqueue("Second");
            queue.Enqueue("Third");
            
            Console.WriteLine($"Queue count: {queue.Count}");
            Console.WriteLine($"Peek: {queue.Peek()}"); // First without removing
            
            while (queue.Count > 0)
            {
                Console.WriteLine($"  Dequeue: {queue.Dequeue()}");
            }
            
            // Stack - LIFO (Last In, First Out)
            Console.WriteLine("\n=== Stack (LIFO) ===");
            Stack<string> stack = new Stack<string>();
            stack.Push("First");
            stack.Push("Second");
            stack.Push("Third");
            
            Console.WriteLine($"Stack count: {stack.Count}");
            Console.WriteLine($"Peek: {stack.Peek()}"); // Top without removing
            
            while (stack.Count > 0)
            {
                Console.WriteLine($"  Pop: {stack.Pop()}");
            }
            
            // Concurrent collections (thread-safe)
            Console.WriteLine("\n=== Concurrent Collections ===");
            System.Collections.Concurrent.ConcurrentQueue<int> concurrentQueue = new();
            System.Collections.Concurrent.ConcurrentStack<int> concurrentStack = new();
            System.Collections.Concurrent.ConcurrentDictionary<string, int> concurrentDict = new();
            
            concurrentQueue.Enqueue(1);
            concurrentStack.Push(1);
            concurrentDict["key"] = 1;
            
            Console.WriteLine("Thread-safe collections for concurrent access");
        }
        
        static void DemonstrateCollectionInterfaces()
        {
            Console.WriteLine("\n============ COLLECTION INTERFACES ============\n");
            
            // IEnumerable - basic iteration
            Console.WriteLine("=== IEnumerable<T> ===");
            IEnumerable<int> numbers = new List<int> { 1, 2, 3, 4, 5 };
            
            Console.Write("IEnumerable iteration: ");
            foreach (int num in numbers)
            {
                Console.Write($"{num} ");
            }
            Console.WriteLine();
            
            // ICollection - collection operations
            Console.WriteLine("\n=== ICollection<T> ===");
            ICollection<string> collection = new List<string> { "A", "B", "C" };
            
            Console.WriteLine($"Count: {collection.Count}");
            Console.WriteLine($"IsReadOnly: {collection.IsReadOnly}");
            
            collection.Add("D");
            collection.Remove("A");
            
            Console.WriteLine($"After modifications: {string.Join(", ", collection)}");
            
            // IList - indexed collection
            Console.WriteLine("\n=== IList<T> ===");
            IList<double> list = new List<double> { 1.1, 2.2, 3.3 };
            
            Console.WriteLine($"Index of 2.2: {list.IndexOf(2.2)}");
            list.Insert(1, 1.5);
            list[2] = 2.5;
            
            Console.WriteLine($"After modifications: {string.Join(", ", list)}");
            
            // IDictionary - key-value collection
            Console.WriteLine("\n=== IDictionary<TKey, TValue> ===");
            IDictionary<string, int> dict = new Dictionary<string, int>
            {
                ["One"] = 1,
                ["Two"] = 2
            };
            
            Console.WriteLine($"Keys: {string.Join(", ", dict.Keys)}");
            Console.WriteLine($"Values: {string.Join(", ", dict.Values)}");
            
            // IReadOnly collections
            Console.WriteLine("\n=== IReadOnly Collections ===");
            IReadOnlyList<string> readOnlyList = new List<string> { "Read", "Only" };
            IReadOnlyDictionary<int, string> readOnlyDict = new Dictionary<int, string>
            {
                [1] = "One",
                [2] = "Two"
            };
            
            Console.WriteLine($"ReadOnlyList[0]: {readOnlyList[0]}");
            Console.WriteLine($"ReadOnlyDict[2]: {readOnlyDict[2]}");
            // readOnlyList.Add("New"); // ERROR: Read-only
        }
        
        static void DemonstrateLINQWithCollections()
        {
            Console.WriteLine("\n============ LINQ WITH COLLECTIONS ============\n");
            
            List<Person> people = new List<Person>
            {
                new Person("Alice", 30, "Engineering"),
                new Person("Bob", 25, "Sales"),
                new Person("Charlie", 35, "Engineering"),
                new Person("David", 28, "Marketing"),
                new Person("Eve", 32, "Sales")
            };
            
            // Filtering
            Console.WriteLine("=== Filtering (Where) ===");
            var engineers = people.Where(p => p.Department == "Engineering");
            var youngPeople = people.Where(p => p.Age < 30);
            
            Console.WriteLine($"Engineers: {string.Join(", ", engineers.Select(p => p.Name))}");
            Console.WriteLine($"Young people: {string.Join(", ", youngPeople.Select(p => p.Name))}");
            
            // Projection
            Console.WriteLine("\n=== Projection (Select) ===");
            var names = people.Select(p => p.Name);
            var nameAgePairs = people.Select(p => $"{p.Name} ({p.Age})");
            
            Console.WriteLine($"Names: {string.Join(", ", names)}");
            Console.WriteLine($"Name-Age pairs: {string.Join(", ", nameAgePairs)}");
            
            // Ordering
            Console.WriteLine("\n=== Ordering ===");
            var byAge = people.OrderBy(p => p.Age);
            var byNameDesc = people.OrderByDescending(p => p.Name);
            var byDeptThenAge = people.OrderBy(p => p.Department).ThenBy(p => p.Age);
            
            Console.WriteLine("By age:");
            foreach (var p in byAge) Console.WriteLine($"  {p.Name}: {p.Age}");
            
            // Grouping
            Console.WriteLine("\n=== Grouping ===");
            var byDepartment = people.GroupBy(p => p.Department);
            
            foreach (var group in byDepartment)
            {
                Console.WriteLine($"Department: {group.Key}");
                foreach (var person in group)
                {
                    Console.WriteLine($"  {person.Name} ({person.Age})");
                }
            }
            
            // Aggregation
            Console.WriteLine("\n=== Aggregation ===");
            var totalAge = people.Sum(p => p.Age);
            var averageAge = people.Average(p => p.Age);
            var maxAge = people.Max(p => p.Age);
            var minAge = people.Min(p => p.Age);
            var count = people.Count();
            var countEngineers = people.Count(p => p.Department == "Engineering");
            
            Console.WriteLine($"Total age: {totalAge}");
            Console.WriteLine($"Average age: {averageAge:F1}");
            Console.WriteLine($"Max age: {maxAge}, Min age: {minAge}");
            Console.WriteLine($"Total: {count}, Engineers: {countEngineers}");
            
            // First/Last/Single
            Console.WriteLine("\n=== First/Last/Single ===");
            var first = people.First();
            var firstEngineer = people.First(p => p.Department == "Engineering");
            var last = people.Last();
            var singleAlice = people.Single(p => p.Name == "Alice");
            // var single = people.Single(); // ERROR: More than one element
            
            Console.WriteLine($"First: {first.Name}, Last: {last.Name}");
            Console.WriteLine($"First engineer: {firstEngineer.Name}");
            Console.WriteLine($"Single Alice: {singleAlice.Name}");
            
            // Any/All/Contains
            Console.WriteLine("\n=== Any/All/Contains ===");
            bool anyOver40 = people.Any(p => p.Age > 40);
            bool allOver20 = people.All(p => p.Age > 20);
            bool containsAlice = people.Any(p => p.Name == "Alice");
            
            Console.WriteLine($"Any over 40: {anyOver40}");
            Console.WriteLine($"All over 20: {allOver20}");
            Console.WriteLine($"Contains Alice: {containsAlice}");
            
            // Conversion
            Console.WriteLine("\n=== Conversion ===");
