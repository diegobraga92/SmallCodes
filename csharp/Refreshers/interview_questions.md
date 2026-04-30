# C# Technical Interview Questions

A curated list of questions based on the C# refresher series, organized by topic and seniority level. Focused on the topics most likely to appear in a conversational technical interview.

---

## 1. C# TYPE SYSTEM & BASICS

### Junior
1. **What is the difference between a value type and a reference type in C#? Where is each stored?**

   *Key points: Value types (structs, enums, primitives) store data directly on the stack. Reference types (classes, arrays, strings) store a reference on the heap; the reference itself lives on the stack. Value types are copied on assignment; reference types share the same object.*

2. **Explain boxing and unboxing. Why can they be expensive?**

   *Key points: Boxing wraps a value type into an object (heap allocation). Unboxing extracts the value back. Expensive because: heap allocation, memory copy, and type checking overhead. Avoid in performance-critical code (e.g., collections before generics).*

3. **What is the difference between `const` and `readonly`? When would you use each?**

   *Key points: `const` is compile-time constant, implicitly static, must be initialized. `readonly` is runtime constant, can be set in constructor, can be instance-level. Use `const` for truly immutable values (PI), `readonly` for values set at construction.*

4. **What does the `var` keyword do? Is it the same as `dynamic`?**

   *Key points: `var` is implicitly typed at compile time — the type is inferred and fixed. `dynamic` bypasses compile-time type checking, resolved at runtime. `var` is type-safe; `dynamic` is not and can cause runtime exceptions.*

5. **What are nullable value types (e.g., `int?`)? How do you check if a nullable has a value?**

   *Key points: `int?` is syntactic sugar for `Nullable<int>`. Check with `.HasValue` property or compare to `null`. Access value with `.Value` (throws if null) or use `??` operator for default.*

6. **What is the difference between `string` and `StringBuilder`? When would you choose one over the other?**

   *Key points: `string` is immutable — every concatenation creates a new object. `StringBuilder` uses a mutable buffer. Use `string` for fixed/small text, `StringBuilder` for large or repeated concatenations (loops).*

### Mid
7. **Explain the difference between `ref`, `out`, and `in` parameter modifiers. When would you use each?**

   *Key points: `ref` — variable must be initialized before passing, method can read/write. `out` — variable doesn't need initialization, method must assign before returning. `in` — read-only reference, prevents modification. Use `ref` for swapping, `out` for TryParse patterns, `in` for large structs.*

8. **What are tuples in C#? How do named tuples improve code readability?**

   *Key points: Tuples group multiple values without creating a class. Named tuples: `(string Name, int Age) person`. Improves readability over `Item1`, `Item2`. Value types, mutable. Use for temporary groupings.*

9. **What are records (`record` keyword)? How do they differ from classes and structs in terms of equality and immutability?**

   *Key points: Records are reference types with value-based equality. `record class` — reference type, immutable by default (with `init`). `record struct` — value type. Records provide `ToString()`, `Deconstruct`, `With` expressions automatically. Classes use reference equality.*

10. **What is pattern matching in C#? Give examples of type patterns, property patterns, and relational patterns.**

    *Key points: Pattern matching tests expressions against patterns. Type: `if (obj is string s)`. Property: `if (obj is { Name: "John", Age: > 18 })`. Relational: `switch { > 0 and < 10 => ... }`. Reduces if-else chains.*

11. **Explain the difference between `Array.CopyTo()` and `Array.Clone()`. What about deep copy vs shallow copy?**

    *Key points: `Clone()` returns a new array object (shallow copy). `CopyTo()` copies elements into an existing array at a specified index. Both do shallow copy — reference types still point to same objects. Deep copy requires serialization or manual copying.*

---

## 2. OOP: CLASSES, INHERITANCE, POLYMORPHISM & INTERFACES

### Junior
12. **What is the difference between an abstract class and an interface? When would you choose one over the other?**

    *Key points: Abstract class can have implementation, fields, constructors. Interface (pre-C# 8) only declarations. Choose abstract class for shared base logic, interface for contract/capability. C# 8+ interfaces can have default implementations.*

13. **Explain the `virtual` and `override` keywords. What happens if you don't use `override` when hiding a base method?**

    *Key points: `virtual` allows a method to be overridden. `override` replaces the base implementation. Without `override`, you get method hiding (compiler warning) — calling through base type reference invokes base method, not derived.*

14. **What does the `sealed` keyword do when applied to a class? To a method?**

    *Key points: `sealed class` prevents inheritance. `sealed method` prevents further overriding in derived classes. Used for security, performance (devirtualization), or design finality.*

15. **What is constructor chaining? How does the `base` keyword work in constructors?**

    *Key points: Constructor chaining calls one constructor from another using `this()` or `base()`. `base()` calls the parent class constructor. Ensures proper initialization chain. Default `base()` call is implicit if not specified.*

16. **What is the difference between public, private, protected, and internal access modifiers?**

    *Key points: `public` — any code. `private` — same class only. `protected` — same class + derived classes. `internal` — same assembly. `protected internal` — same assembly + derived classes. `private protected` — same class + derived classes in same assembly.*

### Mid
17. **What are default interface methods (C# 8.0+)? Why were they introduced?**

    *Key points: Interfaces can now provide default implementations. Introduced for API backward compatibility — adding a method to an interface without breaking existing implementers. Also enables traits-like patterns.*

18. **What is explicit interface implementation? When would you need it?**

    *Key points: Implementing an interface method without `public` access — only callable through the interface reference. Use when: resolving name conflicts (two interfaces with same method), hiding implementation details, or implementing `IEnumerable` alongside a class-specific `GetEnumerator`.*

19. **Explain the difference between composition and inheritance. Give a real-world example where you'd choose composition over inheritance.**

    *Key points: Inheritance is "is-a" (tight coupling). Composition is "has-a" (loose coupling, more flexible). Example: A `Car` class should compose `Engine`, `Wheels` rather than inherit from `Engine`. Composition allows runtime behavior changes.*

20. **What is the Liskov Substitution Principle? Give an example of a violation in C#.**

    *Key points: Derived classes must be substitutable for their base class without altering correctness. Violation: `Square` inheriting from `Rectangle` — setting width on Square also changes height, breaking Rectangle's expected behavior.*

21. **How does C# handle multiple inheritance? Why doesn't it support it for classes?**

    *Key points: C# doesn't support multiple class inheritance (diamond problem, ambiguity). Instead uses interfaces (multiple interface implementation) and default interface methods. Composition is preferred over multiple inheritance.*

---

## 3. GENERICS

### Junior
22. **What are generics in C#? What problem do they solve?**

    *Key points: Generics allow type-safe data structures without boxing or casting. Solved: code reuse without sacrificing type safety, avoiding `ArrayList` (boxing overhead), compile-time type checking.*

23. **What is a generic constraint? Give examples of `where T : class`, `where T : struct`, `where T : new()`.**

    *Key points: Constraints restrict what types can be used as generic arguments. `where T : class` — reference type only. `where T : struct` — value type only. `where T : new()` — must have parameterless constructor. Combine with `where T : SomeInterface`.*

### Mid
24. **Explain covariance and contravariance in C# generics. When would you use `in` and `out` keywords?**

    *Key points: Covariance (`out`) — you can use a more derived type than specified (e.g., `IEnumerable<Dog>` as `IEnumerable<Animal>`). Contravariance (`in`) — you can use a less derived type (e.g., `Action<Animal>` as `Action<Dog>`). `out` for return types, `in` for input parameters.*

25. **Why can't you use `operator ==` or `operator +` directly on generic type parameters? How do you work around this?**

    *Key points: Operators are static methods, not part of interfaces. The compiler can't guarantee the type supports them. Workaround: use `EqualityComparer<T>.Default`, `IComparable<T>` constraint, or `dynamic` (with performance cost).*

26. **What is the difference between `List<T>` and `ArrayList`? Why should you prefer `List<T>`?**

    *Key points: `List<T>` is generic (type-safe, no boxing). `ArrayList` is non-generic (stores `object`, boxing for value types, casting needed). Prefer `List<T>` for performance and type safety.*

---

## 4. DELEGATES, EVENTS, LAMBDAS & CLOSURES

### Junior
27. **What is a delegate? How is it different from a regular method call?**

    *Key points: A delegate is a type-safe function pointer. Unlike direct method calls, delegates can be passed as parameters, stored, and invoked dynamically. Supports multicast (multiple methods).*

28. **What are the built-in delegate types `Func<T>`, `Action<T>`, and `Predicate<T>`? When would you use each?**

    *Key points: `Func<TResult>` — returns a value (up to 16 params). `Action` — returns void. `Predicate<T>` — returns bool, used for conditions. Use `Func` for transformations, `Action` for side effects, `Predicate` for filtering.*

29. **What is a lambda expression? What is the `=>` syntax?**

    *Key points: Lambda is a concise anonymous function: `(x) => x * 2`. The `=>` is the lambda operator (read as "goes to"). Can be used as a delegate or expression tree. Supports statement bodies with `{}`.*

### Mid
30. **What is a closure in C#? How does capturing a variable in a lambda affect its lifetime?**

    *Key points: A closure captures outer variables into the lambda's scope. Captured variables are hoisted to a compiler-generated class, extending their lifetime beyond the declaring method. Can cause memory leaks if the delegate lives long.*

31. **What is the difference between a delegate and an event? Why can't you invoke an event from outside the declaring class?**

    *Key points: An event is a wrapper around a delegate — only the declaring class can invoke it. Outside code can only subscribe/unsubscribe (`+=`/`-=`). This encapsulation prevents external code from clearing or invoking the invocation list.*

32. **What is a multicast delegate? How do you combine delegates and what is the return value of a multicast delegate?**

    *Key points: A delegate that holds references to multiple methods. Combine with `+=` or `Delegate.Combine()`. Return value is the return of the last method in the invocation list. Use `GetInvocationList()` to get individual results.*

33. **Explain the standard EventHandler pattern in .NET. Why use `EventArgs` or `EventArgs<T>`?**

    *Key points: Pattern: `public event EventHandler<MyEventArgs> MyEvent;` with `protected virtual void OnMyEvent(MyEventArgs e)`. `EventArgs` is the base class for event data. `EventArgs<T>` (C# 9+) simplifies single-value event data. Enables inheritance and consistency.*

---

## 5. LINQ

### Junior
34. **What is LINQ? What are the two syntaxes for writing LINQ queries?**

    *Key points: LINQ (Language Integrated Query) provides query capabilities over data sources. Two syntaxes: Query syntax (SQL-like: `from x in list where x.Age > 18 select x`) and Method syntax (fluent: `list.Where(x => x.Age > 18)`).*

35. **What is the difference between `.Where()` and `.Select()` in LINQ?**

    *Key points: `Where()` filters elements (returns subset of same type). `Select()` transforms elements (projects to new type). `Where` reduces count; `Select` changes shape.*

36. **How do you sort data with LINQ? What is the difference between `OrderBy` and `ThenBy`?**

    *Key points: `OrderBy()` sorts by primary key. `ThenBy()` sorts by secondary key within the same primary group. `OrderByDescending()`/`ThenByDescending()` for descending order. `ThenBy` only works after `OrderBy`.*

### Mid
37. **Explain deferred execution vs immediate execution in LINQ. Which methods trigger immediate execution?**

    *Key points: Deferred execution — query is evaluated when enumerated (e.g., `Where`, `Select`, `OrderBy`). Immediate execution — query runs immediately (e.g., `ToList()`, `ToArray()`, `Count()`, `First()`, `Any()`). Deferred is lazy; immediate is eager.*

38. **What is the difference between `First()`, `FirstOrDefault()`, `Single()`, and `SingleOrDefault()`? When would each throw an exception?**

    *Key points: `First()` — returns first, throws if empty. `FirstOrDefault()` — returns first or default, no throw. `Single()` — expects exactly one, throws if none or >1. `SingleOrDefault()` — expects 0 or 1, throws if >1. Use `First` when order matters, `Single` when uniqueness is expected.*

39. **How does `GroupBy()` work in LINQ? Give an example of grouping and aggregating.**

    *Key points: `GroupBy(keySelector)` returns `IEnumerable<IGrouping<TKey, TElement>>`. Example: `people.GroupBy(p => p.Department).Select(g => new { Dept = g.Key, Count = g.Count() })`. Groups by key, then aggregate per group.*

40. **What is the difference between `IEnumerable<T>` and `IQueryable<T>`? When would you use each with LINQ?**

    *Key points: `IEnumerable<T>` — in-memory LINQ to Objects (client-side). `IQueryable<T>` — builds expression trees, executed on server (e.g., EF Core translates to SQL). Use `IQueryable` for database queries to push filtering to the server.*

41. **What is a join in LINQ? How does `Join()` differ from `GroupJoin()`?**

    *Key points: `Join()` performs inner join — pairs matching elements from two sequences. `GroupJoin()` performs left outer join — groups right-side matches under each left element. `GroupJoin` is useful for hierarchical results (e.g., orders with their items).*

---

## 6. ASYNC/AWAIT & ASYNCHRONOUS PROGRAMMING

### Junior
42. **What is the `async` and `await` keyword? What does `await` do?**

    *Key points: `async` marks a method as asynchronous. `await` suspends the method until the awaited task completes, without blocking the thread. The method resumes on the captured SynchronizationContext (usually the original thread).*

43. **What return types can an async method have? What is the difference between `Task` and `Task<T>`?**

    *Key points: Return types: `Task` (void-returning async), `Task<T>` (returns value), `void` (fire-and-forget, only for event handlers), `ValueTask<T>` (performance optimization). `Task` is awaitable; `Task<T>` also provides a result via `.Result` or `await`.*

44. **How do you handle exceptions in async code? What happens if you don't await a task that throws?**

    *Key points: Use `try/catch` around `await`. Unawaited faulted tasks become "fire-and-forget" — the exception is swallowed unless the task is observed (e.g., stored and awaited later). Unobserved exceptions trigger `TaskScheduler.UnobservedTaskException` event (and in .NET Core+, may be ignored).*

### Mid
45. **What is `ConfigureAwait(false)`? When and why would you use it?**

    *Key points: `ConfigureAwait(false)` tells the awaiter not to capture the current SynchronizationContext. Use in library code to avoid forcing continuations back to the UI/ASP.NET thread. Improves performance and prevents deadlocks in synchronous blocking scenarios.*

46. **What is the difference between `Task.Run()` and `async/await`? When would you use each?**

    *Key points: `Task.Run()` queues work on the thread pool (CPU-bound or I/O-bound offloading). `async/await` is a language feature for asynchronous operations. Use `Task.Run` for CPU-bound work to avoid blocking the UI thread. Use `async/await` for I/O-bound work (no extra thread needed).*

47. **What is `ValueTask<T>` and when should you use it instead of `Task<T>`?**

    *Key points: `ValueTask<T>` is a value type that can avoid heap allocation when the result is synchronously available. Use for high-performance paths where the result is often already computed (e.g., cached data). Avoid if method is awaited multiple times or stored.*

48. **What is `CancellationToken` and how do you use it to cancel async operations?**

    *Key points: `CancellationToken` from `CancellationTokenSource`. Pass to async methods. Check `token.ThrowIfCancellationRequested()` or `token.IsCancellationRequested`. `CancellationTokenSource.CancelAfter(TimeSpan)` for timeout. Cooperative cancellation — the operation must check the token.*

49. **What are async streams (`IAsyncEnumerable<T>`)? Give a use case.**

    *Key points: `IAsyncEnumerable<T>` enables async iteration with `await foreach`. Use case: reading paginated API results, processing large files line-by-line, streaming data from a database. Each element is produced asynchronously.*

50. **What is SynchronizationContext and how does it relate to `await` capturing context?**

    *Key points: `SynchronizationContext` represents a "context" to execute code (UI thread, ASP.NET request context). By default, `await` captures the current context and resumes on it. `ConfigureAwait(false)` skips this capture. Important for UI apps (must resume on UI thread) and library code (should not capture).*

### Senior
51. **Explain the state machine that the compiler generates for async methods. What happens under the hood?**

    *Key points: The compiler transforms async methods into a state machine struct implementing `IAsyncStateMachine`. It tracks state (where execution paused), local variables, and the builder. Each `await` is a state transition. The method returns a `Task` that completes when the state machine reaches final state.*

52. **How would you implement a retry pattern with async/await? What considerations are there for exponential backoff?**

    *Key points: Use a loop with `try/catch`, `await Task.Delay(delay)` between retries. Exponential backoff: `delay *= 2` (or `TimeSpan.FromSeconds(Math.Pow(2, attempt))`). Add jitter (`Random.Next()`) to avoid thundering herd. Consider max retries, circuit breaker, and transient fault detection.*

---

## 7. COLLECTIONS

### Junior
53. **What is the difference between `List<T>`, `Dictionary<TKey, TValue>`, `HashSet<T>`, and `Queue<T>`? When would you use each?**

    *Key points: `List<T>` — ordered, indexable, allows duplicates. `Dictionary<TKey, TValue>` — key-value pairs, fast lookup by key. `HashSet<T>` — unordered, unique elements, fast set operations. `Queue<T>` — FIFO. Use: List for general collections, Dictionary for lookups, HashSet for uniqueness, Queue for processing order.*

54. **What is the difference between an array (`T[]`) and a `List<T>`? When would you choose one over the other?**

    *Key points: Array — fixed size, faster access, lower memory. `List<T>` — dynamic size, more methods (Add, Remove, LINQ). Use array for fixed-size, performance-critical data. Use List for dynamic collections.*

### Mid
55. **What is the difference between `Dictionary<TKey, TValue>` and `ConcurrentDictionary<TKey, TValue>`? When would you use the concurrent version?**

    *Key points: `Dictionary` is not thread-safe — concurrent access causes corruption. `ConcurrentDictionary` is thread-safe with fine-grained locking. Use `ConcurrentDictionary` in multi-threaded scenarios. For single-threaded, `Dictionary` is faster.*

56. **What is the difference between `Stack<T>` and `Queue<T>`? Give a real-world use case for each.**

    *Key points: `Stack<T>` — LIFO (Last In, First Out). Use: undo/redo, expression evaluation, backtracking. `Queue<T>` — FIFO (First In, First Out). Use: task scheduling, message processing, BFS algorithms.*

57. **How does `HashSet<T>` ensure uniqueness? What methods must a type implement to work correctly in a `HashSet<T>`?**

    *Key points: Uses hash codes and equality. Requires `GetHashCode()` (for bucketing) and `Equals()` (for collision resolution). Both must be consistent — equal objects must have equal hash codes. Implement `IEquatable<T>` for better performance.*

---

## 8. MEMORY MANAGEMENT & IDISPOSABLE

### Junior
58. **How does the garbage collector work in .NET? What are the generations (Gen 0, 1, 2)?**

    *Key points: GC automatically manages memory. Generations: Gen 0 — short-lived objects (collected most frequently). Gen 1 — objects that survived Gen 0 (bridge). Gen 2 — long-lived objects (large objects, static data). GC promotes survivors to higher generations.*

59. **What is the `IDisposable` interface? When and how do you use it?**

    *Key points: `IDisposable` provides a mechanism to release unmanaged resources (file handles, network connections, database connections). Implement `Dispose()` method. Call via `using` statement or `try/finally`. Not handled by GC.*

60. **What is the `using` statement? What does it guarantee?**

    *Key points: `using (var resource = new FileStream(...)) { ... }` ensures `Dispose()` is called even if an exception occurs. Compiler translates to `try/finally`. C# 8+ also supports `using var` declarations (disposed at end of scope).*

### Mid
61. **What is the dispose pattern? When would you implement a finalizer alongside `Dispose`?**

    *Key points: Dispose pattern: `Dispose(bool disposing)` with a flag. Finalizer (`~MyClass()`) is a safety net if `Dispose()` wasn't called. Implement finalizer only when holding unmanaged resources directly (rare — prefer `SafeHandle`). Call `GC.SuppressFinalize(this)` in `Dispose()`.*

62. **What is a large object heap (LOH)? What objects go there and why does it matter?**

    *Key points: Objects ≥ 85,000 bytes go to LOH. LOH is not compacted (performance cost), causing fragmentation. Large arrays, strings, buffers. Fragmentation can cause `OutOfMemoryException` even with free space. Use `ArrayPool<T>` for large temporary buffers.*

63. **What causes memory leaks in .NET? Give examples (e.g., event handlers, static references, forgotten subscriptions).**

    *Key points: Common causes: event handlers preventing GC (subscriber keeps publisher alive), static collections growing unbounded, forgotten `IDisposable` (file handles), anonymous methods capturing large objects, `Task` not disposed, `Thread` not terminated.*

64. **What is `GC.Collect()`? Why should you generally avoid calling it explicitly?**

    *Key points: `GC.Collect()` forces immediate garbage collection. Avoid because: it's expensive (freezes threads), promotes objects prematurely, disrupts GC's self-tuning heuristics. Only use in diagnostics or specific scenarios (e.g., after large allocation bursts).*

---

## 9. DEPENDENCY INJECTION

### Mid
65. **What is Dependency Injection? What problem does it solve?**

    *Key points: DI provides dependencies to a class from outside rather than creating them internally. Solves: tight coupling, hard-to-test code, violation of Dependency Inversion Principle. Enables loose coupling, testability, and configuration flexibility.*

66. **Explain the three DI service lifetimes: `Singleton`, `Scoped`, and `Transient`. When would you use each?**

    *Key points: `Singleton` — one instance for entire application (stateless services, configuration). `Scoped` — one instance per request/scope (DbContext, request-scoped services). `Transient` — new instance every injection (lightweight, stateless services). Choose based on state sharing needs.*

67. **What is a captive dependency? How do you detect one?**

    *Key points: A captive dependency is a shorter-lived service injected into a longer-lived one (e.g., `Transient`/`Scoped` into `Singleton`). The shorter-lived service is "captured" and lives longer than intended. Detect with DI container analyzers (e.g., `Microsoft.Extensions.DependencyInjection.Analyzers`).*

68. **How does DI integrate with ASP.NET Core's request pipeline?**

    *Key points: ASP.NET Core has built-in DI. Controllers, middleware, and filters receive dependencies via constructor injection. `IServiceCollection` configures services in `Program.cs`. `HttpContext.RequestServices` provides access to scoped services.*

---

## 10. ASP.NET CORE WEB API

### Mid
69. **What is middleware in ASP.NET Core? How does the pipeline work?**

    *Key points: Middleware are components in the request pipeline. Each middleware can process the request, pass to the next, or short-circuit. Pipeline is configured in `Program.cs` with `Use`, `Run`, `Map`. Order matters — early middleware handles errors, auth, logging.*

70. **What is the difference between attribute routing and conventional routing? Which is preferred for Web APIs?**

    *Key points: Attribute routing uses `[Route("api/[controller]")]` on controllers/actions. Conventional routing uses `app.MapControllerRoute()` with patterns. Attribute routing is preferred for Web APIs — explicit, supports constraints, easier to maintain.*

71. **How does model binding work? How do `[FromBody]`, `[FromQuery]`, `[FromRoute]`, and `[FromHeader]` differ?**

    *Key points: Model binding maps HTTP request data to action parameters. `[FromBody]` — JSON/XML body. `[FromQuery]` — query string. `[FromRoute]` — route parameters. `[FromHeader]` — HTTP headers. Default sources are inferred (complex types from body, primitives from query/route).*

72. **How do you validate incoming request data in ASP.NET Core? What is `[ApiController]` and how does it help?**

    *Key points: Use data annotations (`[Required]`, `[Range]`, `[EmailAddress]`) on models. `[ApiController]` enables automatic 400 response for invalid models, binding source inference, and attribute routing requirement. Also supports `FluentValidation` for complex rules.*

73. **What is the difference between authentication and authorization? How do you implement JWT authentication in ASP.NET Core?**

    *Key points: Authentication verifies identity (who you are). Authorization verifies permissions (what you can do). JWT: `AddAuthentication().AddJwtBearer()` with token validation parameters (issuer, audience, signing key). `[Authorize]` attribute protects endpoints.*

74. **How do you implement global exception handling in ASP.NET Core?**

    *Key points: Options: custom middleware (try/catch around `next`), `UseExceptionHandler()` for developer page or custom endpoint, `IExceptionHandler` (minimal API), or `ProblemDetails` middleware. Log exceptions, return consistent error responses.*

---

## 11. ENTITY FRAMEWORK CORE

### Mid
75. **What is the N+1 query problem in EF Core? How do you avoid it?**

    *Key points: N+1 occurs when loading a parent entity and then iterating over its children, causing one query for the parent + N queries for each child. Fix: use `.Include()` (eager loading) or `.ThenInclude()` to load related data in a single query.*

76. **What is the difference between eager loading, lazy loading, and explicit loading?**

    *Key points: Eager loading — `.Include()` loads related data upfront (single query). Lazy loading — related data loaded on first access (requires proxy, multiple queries). Explicit loading — manually call `.Load()` on a navigation property. Eager is most efficient for known access patterns.*

77. **What is change tracking in EF Core? How does `DbContext` know what changed?**

    *Key points: `DbContext` tracks entity states (Added, Modified, Deleted, Unchanged, Detached). On `SaveChanges()`, it compares current values with original snapshots. `ChangeTracker` provides access to tracked entities. `AsNoTracking()` disables tracking for read-only queries.*

78. **What are migrations in EF Core? How do you create and apply them?**

    *Key points: Migrations are code-generated files that update the database schema. Create: `dotnet ef migrations add InitialCreate`. Apply: `dotnet ef database update`. `DbContext.Database.Migrate()` applies at startup. Supports rollback and scripting.*

79. **What is the difference between `AsNoTracking()` and the default tracking behavior? When would you use `AsNoTracking()`?**

    *Key points: Default tracking — entities are tracked, changes are saved on `SaveChanges()`. `AsNoTracking()` — entities are not tracked (faster, less memory). Use for read-only queries, reporting, or when entities won't be updated.*

80. **How do you handle concurrency conflicts in EF Core?**

    *Key points: Use `[ConcurrencyCheck]` or `[Timestamp]` (row version) attributes. When saving, EF checks if the row version matches. If another user modified it, `DbUpdateConcurrencyException` is thrown. Handle with retry logic or "last write wins" strategy.*

---

## 12. EXCEPTION HANDLING

### Junior
81. **What is the difference between `throw` and `throw ex` in a catch block? Why is one preferred?**

    *Key points: `throw` re-throws the original exception preserving the stack trace. `throw ex` resets the stack trace to the catch point (loses original location). Always use `throw` to preserve debugging information.*

82. **What is the purpose of the `finally` block? Does it always execute?**

    *Key points: `finally` executes regardless of exception or return — used for cleanup (closing files, releasing resources). Almost always executes, except: `StackOverflowException`, `Environment.FailFast()`, or thread abort.*

### Mid
83. **What are exception filters (`when` keyword)? Give an example where they're useful.**

    *Key points: `catch (HttpRequestException ex) when (ex.StatusCode == 429)` — catches only specific conditions without unwinding the stack. Useful for: retry logic, logging without catching, handling specific error codes differently.*

84. **What is the difference between `ArgumentException`, `ArgumentNullException`, and `ArgumentOutOfRangeException`? When would you throw each?**

    *Key points: `ArgumentException` — general invalid argument. `ArgumentNullException` — null where not allowed. `ArgumentOutOfRangeException` — value outside valid range (e.g., index < 0 or >= length). Throw the most specific type for clarity.*

85. **What are best practices for designing custom exceptions? Should they be serializable?**

    *Key points: Extend `Exception` (not `ApplicationException`). End class name with "Exception". Implement three constructors (parameterless, message, message + inner). Mark `[Serializable]` for cross-domain scenarios. Keep them in the root namespace.*

---

## 13. THREADING & CONCURRENCY

### Mid
86. **What is the difference between `Thread`, `ThreadPool`, and `Task`? When would you use each?**

    *Key points: `Thread` — direct OS thread (expensive, manual management). `ThreadPool` — reusable threads (avoids creation overhead). `Task` — higher-level abstraction (uses ThreadPool, supports continuations, cancellation, async/await). Prefer `Task` for most scenarios.*

87. **What is the Task Parallel Library (TPL)? How does `Parallel.ForEach` differ from a regular `foreach`?**

    *Key points: TPL simplifies parallel programming. `Parallel.ForEach` partitions the collection and processes items concurrently on multiple threads. Regular `foreach` is sequential. Use `Parallel.ForEach` for CPU-bound independent work. Not suitable for I/O-bound or shared state.*

88. **What synchronization primitives does .NET provide? Explain `lock`, `Monitor`, `Mutex`, `SemaphoreSlim`, and `ReaderWriterLockSlim`.**

    *Key points: `lock` — simple mutual exclusion (syntactic sugar for `Monitor`). `Monitor` — advanced locking (TryEnter, Pulse/Wait). `Mutex` — cross-process synchronization. `SemaphoreSlim` — limits concurrent access count. `ReaderWriterLockSlim` — multiple readers or single writer.*

89. **What are concurrent collections (`ConcurrentBag<T>`, `ConcurrentQueue<T>`, etc.)? When should you use them instead of locking manually?**

    *Key points: Thread-safe collections optimized for concurrent access. `ConcurrentQueue<T>` — producer-consumer. `ConcurrentBag<T>` — unordered, thread-local storage. `ConcurrentDictionary<TKey, TValue>` — concurrent key-value. Use instead of manual locking for better performance and correctness.*

90. **What is a deadlock? How do you prevent one in C#?**

    *Key points: Deadlock occurs when two threads each hold a lock the other needs. Prevention: consistent lock ordering, use `Monitor.TryEnter` with timeout, avoid nested locks, use `SemaphoreSlim` with async, use `lock` only when necessary.*

---

## 14. SOLID PRINCIPLES

### Mid
91. **Explain each of the SOLID principles. Give a C# example of a violation and the fix for each.**

    *Key points: S — Single Responsibility (one reason to change). O — Open/Closed (open for extension, closed for modification). L — Liskov Substitution (derived must work as base). I — Interface Segregation (small, focused interfaces). D — Dependency Inversion (depend on abstractions, not concretions).*

92. **What is the Dependency Inversion Principle? How does it differ from Dependency Injection?**

    *Key points: DIP: high-level modules should not depend on low-level modules — both should depend on abstractions. DI is a technique to implement DIP (injecting dependencies through constructor/parameter). DIP is the principle; DI is the implementation pattern.*

93. **What is the Interface Segregation Principle? Give an example of a "fat interface" and how you'd refactor it.**

    *Key points: No client should be forced to depend on methods it doesn't use. Fat interface: `IMultiFunctionPrinter` with Print, Scan, Fax, Staple. Refactor into `IPrinter`, `IScanner`, `IFaxer`. Classes implement only what they need.*

---

## 15. DESIGN PATTERNS (COMMON)

### Mid
94. **Implement a thread-safe Singleton in C#. What are the options (static constructor, `Lazy<T>`, double-check locking)?**

    *Key points: Options: static constructor (CLR guarantees single execution), `Lazy<T>` with `LazyThreadSafetyMode.ExecutionAndPublication` (simplest), double-check locking with `volatile` (manual control). `Lazy<T>` is preferred for simplicity and performance.*

95. **What is the Factory Method pattern? When would you use it over a simple constructor?**

    *Key points: Factory Method defines an interface for creating objects, letting subclasses decide which class to instantiate. Use over constructor when: creation logic is complex, you need to return different types based on input, or you want to decouple client code from concrete types.*

96. **What is the Observer pattern? How does C# support it natively with events?**

    *Key points: Observer defines a one-to-many dependency where when one object changes state, all dependents are notified. C# supports it natively with events and delegates — the event is the subject, subscribers are observers. No need to implement the pattern from scratch.*

97. **What is the Strategy pattern? Give a real-world example.**

    *Key points: Strategy defines a family of interchangeable algorithms. Example: `ISortStrategy` with `QuickSort`, `MergeSort`, `BubbleSort` implementations. The context selects a strategy at runtime. In C#, often implemented with delegates/Func instead of interfaces.*

---

## 16. ATTRIBUTES & REFLECTION

### Mid
98. **What are attributes in C#? Give examples of built-in attributes and how to create a custom one.**

    *Key points: Attributes add metadata to code (classes, methods, properties). Built-in: `[Obsolete]`, `[Serializable]`, `[Required]`, `[Route]`. Custom: create a class extending `Attribute`, add `[AttributeUsage]`. Read via reflection at runtime.*

99. **What is reflection? How do you inspect types, methods, and properties at runtime?**

    *Key points: Reflection uses `System.Reflection` to inspect assemblies, types, members at runtime. `typeof(MyClass).GetMethods()`, `Assembly.GetExecutingAssembly()`. Used for: serialization, DI containers, ORMs, dynamic code generation.*

100. **What are the performance implications of using reflection? What alternatives exist (source generators, expression trees)?**

     *Key points: Reflection is slow (runtime type resolution, no JIT optimization). Alternatives: source generators (compile-time code generation, C# 9+), expression trees (compiled delegates), `dynamic` keyword, `UnsafeAccessor` (.NET 7+). Prefer source generators for performance-critical scenarios.*

---

## 17. TESTING

### Mid
101. **What is the difference between a unit test, an integration test, and a functional test?**

     *Key points: Unit test — tests a single unit in isolation (mocked dependencies). Integration test — tests multiple components together (real database, API). Functional test — tests end-to-end from user perspective. Unit tests are fastest; functional tests are most comprehensive.*

102. **What is mocking? How do frameworks like Moq or NSubstitute work?**

     *Key points: Mocking creates fake implementations of dependencies to isolate the unit under test. Frameworks use dynamic proxy generation (Castle.Core) to create implementations at runtime. `mock.Setup(x => x.Method()).Returns(value)`. Enables verifying interactions.*

103. **What is test-driven development (TDD)? What is the Red-Green-Refactor cycle?**

     *Key points: TDD: write failing test first (Red), write minimal code to pass (Green), improve code quality (Refactor). Benefits: better design, test coverage, confidence in refactoring. Cycle: Red → Green → Refactor → repeat.*

104. **How do you test async methods? What should you be careful about?**

     *Key points: Use `await` in test methods (return `Task` or `ValueTask`). Avoid `.Result` or `.Wait()` (can deadlock). Use `ConfigureAwait(false)` in library code. Be careful with timeouts — use `CancellationToken` with realistic delays. Mock async methods with `ReturnsAsync()`.*

---

## 18. SENIOR-LEVEL & SYSTEM DESIGN

### Senior
105. **How would you design a background job processing system in .NET? Consider `IHostedService`, `BackgroundService`, and `Channel<T>`.**

     *Key points: Use `BackgroundService` (extends `IHostedService`) for long-running background tasks. `Channel<T>` provides a thread-safe producer-consumer queue. Pattern: API enqueues jobs to `Channel<T>`, `BackgroundService` dequeues and processes. Consider: retries, error handling, graceful shutdown, persistence for durability.*

106. **How would you architect a high-throughput API in ASP.NET Core? Consider caching, rate limiting, async I/O, connection pooling, and database optimization.**

     *Key points: Use async I/O throughout, implement response caching (in-memory, Redis), rate limiting with `AspNetCoreRateLimit`, connection pooling (default in EF Core/SqlClient), database indexing, pagination, read replicas, CDN for static content, load balancing.*

107. **Explain how you would implement CQRS (Command Query Responsibility Segregation) in a .NET application.**

     *Key points: Separate read and write models. Commands (writes) use MediatR with `IRequest`, Queries (reads) use separate handlers. Often paired with Event Sourcing. Benefits: optimized read/write schemas, scalability, clear separation of concerns. Use `MediatR` library.*

108. **How do you handle distributed transactions across microservices in .NET?**

     *Key points: Avoid distributed transactions (2PC) — use eventual consistency. Patterns: Saga (choreography/orchestration), Outbox pattern (reliable message publishing), Idempotent endpoints, Compensating transactions. Use message brokers (RabbitMQ, Azure Service Bus) for coordination.*

109. **What considerations go into versioning a Web API? Compare URI versioning, query string versioning, and header versioning.**

     *Key points: URI versioning (`/api/v1/orders`) — explicit, easy to route, but clutters URLs. Query string (`?version=1`) — simple but easy to forget. Header versioning (`Accept: application/vnd.myapp.v1+json`) — clean URLs but harder to discover. URI versioning is most common.*

110. **How would you implement real-time communication in .NET (SignalR)? What transport mechanisms does it use?**

     *Key points: SignalR provides real-time web functionality. Transports: WebSocket (primary), Server-Sent Events, Long Polling (fallback). Hubs handle client-server communication. `Groups` for broadcasting to subsets. Scale out with Redis Backplane or Azure SignalR Service.*

---

## 19. BEHAVIORAL & EXPERIENCE

111. **Describe a time you debugged a memory leak in a .NET application. What tools did you use (dotMemory, PerfView, SOS)?**

     *Key points: Common tools: dotMemory/dotMemory Unit (heap analysis), PerfView (ETW traces), SOS (WinDbg debugger extension), Visual Studio Diagnostic Tools. Look for: large object heap fragmentation, event handler leaks, static collections, disposed objects not released.*

112. **How would you approach migrating a legacy .NET Framework application to .NET Core/.NET 8+? What are the biggest challenges?**

     *Key points: Steps: assess dependencies (third-party libs, Windows-specific APIs), use `.NET Portability Analyzer`, update project files to SDK-style, replace `Web.config` with `appsettings.json`, update DI, update EF. Challenges: missing APIs (AppDomain, Remoting), third-party compatibility, configuration migration.*

113. **Tell me about a time you improved the performance of a slow API endpoint. What was the bottleneck and how did you fix it?**

     *Key points: Common bottlenecks: N+1 queries (add `.Include()`), missing indexes (add database indexes), synchronous I/O (make async), large payloads (add pagination, projection), no caching (add response/memory cache), chatty database calls (batch queries).*

114. **How do you stay up to date with new C# and .NET features? What's a recent feature you've adopted?**

     *Key points: Follow: official .NET blog, GitHub dotnet/roslyn, community (Nick Chapsas, David Fowler), conferences (NDC, .NET Conf). Recent features: primary constructors, collection expressions, `InlineArray`, `field` keyword in properties, `TimeProvider` abstraction.*

115. **Describe your experience with code reviews. What do you look for in a C# code review?**

     *Key points: Check: correctness, SOLID principles, async/await usage (no sync-over-async), exception handling, disposal of resources, thread safety, LINQ efficiency (avoid N+1), naming conventions, test coverage, security (SQL injection, XSS).*

---

*Generated from the C# Refreshers series (00–30). Focused on topics most likely to appear in a conversational technical interview for C#/.NET roles.*
