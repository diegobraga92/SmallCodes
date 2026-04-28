# C# Technical Interview: Key Concepts & Terms

> A comprehensive reference compiled from `csharp/Refreshers/00` through `30`.
> Use this to prepare for conversational technical interviews at junior to mid-level.

---

## 1. C# Language Fundamentals

### Data Types & Type System
- **Value Types vs Reference Types** — stack vs heap allocation
- **Primitive Types**: `int`, `long`, `float`, `double`, `decimal`, `bool`, `char`, `byte`, `short`
- **`decimal`** — 128-bit, base-10, for financial calculations (avoids floating-point rounding errors)
- **`var`** — type inference (compile-time, strongly typed)
- **`dynamic`** — type resolved at runtime (bypasses compile-time checks)
- **Nullable value types** (`int?`, `HasValue`, `??` null-coalescing)
- **Default values** for all types (`default` keyword)
- **Boxing/Unboxing** — value type → `object` (heap allocation, performance cost)

### Type Conversion
- **Implicit conversion** (safe, no data loss)
- **Explicit conversion / casting** (potential data loss)
- **`Convert` class** (`Convert.ToInt32()`)
- **`TryParse` pattern** (`int.TryParse(string, out int)`) — safe parsing
- **`is` operator** — type checking
- **`as` operator** — safe casting (returns null on failure)
- **Pattern matching** (`obj is string s`)

### Variables & Constants
- **`const`** — compile-time constant
- **`readonly`** — runtime constant (set in constructor)
- **`static readonly`** — often preferred over `const` for complex types

### Operators
- **Null-conditional** (`?.`) — safe member access
- **Null-coalescing** (`??`) — default on null
- **Null-coalescing assignment** (`??=`) — C# 8+
- **Ternary** (`?:`)
- **`is` and `as`** operators
- **`switch` expression** (C# 8+) — concise, returns a value
- **`with` expression** (for records, C# 9+)

---

## 2. Control Flow

### Conditionals
- **`if-else`** — complex/range conditions
- **`switch` statement** — discrete value matching (classic)
- **`switch` expression** — returns a value (C# 8+)
- **Pattern matching in switch** — type patterns, property patterns, relational patterns (C# 9+)

### Loops
- **`for`** — known iterations, index needed
- **`foreach`** — iterating collections (preferred, cleaner)
- **`while`** — unknown iterations, condition first
- **`do-while`** — executes at least once
- **`yield return`** — iterator methods (lazy generation)

### Jump Statements
- **`break`** — exit loop/switch
- **`continue`** — skip to next iteration
- **`return`** — exit method
- **`throw`** — raise exception
- **`goto`** — (avoid in practice)
- **`yield return` / `yield break`** — iterator blocks

---

## 3. Methods & Functions

### Declaration & Parameters
- **Method signature** — name + parameter types + return type
- **Value parameters** (default — copied)
- **`ref` parameters** — pass by reference (modify caller's variable)
- **`out` parameters** — pass by reference (must be assigned in method)
- **`in` parameters** — read-only reference (C# 7.2+)
- **`params`** — variable number of arguments
- **Optional/default parameters**
- **Named arguments** — `Method(name: value, age: other)`

### Return Types
- **`void`** — no return
- **Value types**, **Reference types**
- **Tuples** (`(int sum, double avg)`) — C# 7+, multiple return values
- **Nullable return types** (`int?`)
- **Generics** (`T Method<T>()`)
- **`async Task` / `async Task<T>`**

### Overloading & Special Methods
- **Method overloading** — same name, different parameters
- **Extension methods** — `static` method in `static` class, `this` keyword on first parameter
- **Local functions** — methods inside methods (C# 7+)
- **Expression-bodied members** (`=>`) — concise syntax (C# 6+)
- **Operator overloading** — `public static MyType operator +(MyType a, MyType b)`

---

## 4. Object-Oriented Programming

### Classes & Objects
- **Constructor** — parameterized, default, static, private (singleton)
- **Constructor chaining** — `this()` and `base()` calls
- **Object initializer** — `new Person { Name = "A", Age = 30 }`
- **Destructor / Finalizer** (`~ClassName()`)
- **`this` keyword** — reference to current instance
- **`base` keyword** — access base class members
- **Partial classes** — split across files (`partial` keyword)

### Properties
- **Auto-implemented properties** (`{ get; set; }`)
- **Full properties** with backing field
- **Read-only property** (`{ get; }` or `{ get; private set; }`)
- **Computed properties** (expression body)
- **Init-only setters** (`{ get; init; }`) — C# 9+, set only during initialization
- **Indexers** — `this[int index] { get; set; }`

### Access Modifiers
- **`public`** — anyone
- **`private`** — same class only
- **`protected`** — derived classes
- **`internal`** — same assembly
- **`protected internal`** — derived or same assembly
- **`private protected`** — C# 7.2+, derived within same assembly

### Static Members
- **Static class** — cannot be instantiated, contains only static members
- **Static constructor** — called once, before any static member access
- **Static fields, methods, properties**
- **Static using** (`using static System.Math;`) — C# 6+

### Inheritance
- **Single inheritance** — C# classes inherit only one base class
- **`sealed` class** — cannot be inherited
- **`abstract` class** — cannot be instantiated, may have abstract members
- **Method hiding** (`new` keyword) — hides base method, not polymorphism
- **Virtual/Override** — `virtual` in base, `override` in derived (polymorphism)
- **`sealed` method** — prevents further overriding

### Polymorphism
- **Runtime polymorphism** — via virtual/override
- **Compile-time polymorphism** — via method overloading
- **Type checking** — `is`, `as`, `GetType()`, `typeof()`
- **Covariant return types** (C# 9+)

### Abstract Classes vs Interfaces
- **Abstract class** — shared implementation + abstract members, single inheritance
- **Interface** — contract only, multiple implementation
- **Default interface methods** (C# 8+) — interfaces can have implementation

### Records (C# 9+)
- **`record`** — reference type with value equality
- **`record struct`** — value type record (C# 10+)
- **Positional records** (`record Person(string Name, int Age)`)
- **`with` expression** — non-destructive mutation
- **Value equality** — by properties, not reference

### Structs
- **Value type**, stack-allocated (when local)
- **`readonly struct`** (C# 7.2+)
- **`ref struct`** — stack-only, cannot be boxed (C# 7.2+)
- **When to use struct** — small (<16 bytes), short-lived, value semantics

---

## 5. Interfaces, Generics, Collections

### Interfaces
- **Multiple interface implementation**
- **Explicit interface implementation** (`void IInterface.Method()`)
- **Generic interfaces** (`IComparable<T>`, `IEnumerable<T>`)
- **Covariance** (`out T`) — `IEnumerable<Dog>` → `IEnumerable<Animal>`
- **Contravariance** (`in T`) — `IComparer<Animal>` → `IComparer<Dog>`
- **Default interface methods** (C# 8+)

### Generics
- **Type parameters** (`<T>`)
- **Constraints** — `where T : class`, `struct`, `new()`, `BaseClass`, `Interface`
- **Generic methods** in non-generic classes
- **Generic interfaces, delegates**
- **Variance** — covariance, contravariance, invariance
- **`default` keyword** with generics
- **Static members** in generic classes (separate per closed type)

### Collections
- **`List<T>`** — dynamic array (fast index, slow insert/remove middle)
- **`Dictionary<TKey, TValue>`** — hash table, O(1) average lookup
- **`HashSet<T>`** — unique elements, O(1) membership test
- **`Queue<T>`** — FIFO
- **`Stack<T>`** — LIFO
- **`LinkedList<T>`** — fast insert/remove (known position), O(n) search
- **`SortedDictionary<TKey, TValue>`** — sorted by key (red-black tree)
- **`SortedSet<T>`** — sorted unique elements
- **Array** — fixed size, single/multi-dimensional, jagged
- **`IEnumerable<T>`** — basic iteration
- **`ICollection<T>`** — add/remove/count
- **`IList<T>`** — indexed access
- **`IReadOnlyList<T>` / `IReadOnlyDictionary<TKey, TValue>`**

---

## 6. LINQ (Language Integrated Query)

### Query Operators
- **`Where`** — filtering
- **`Select`** — projection
- **`SelectMany`** — flatten nested collections
- **`OrderBy` / `OrderByDescending` / `ThenBy`** — sorting
- **`GroupBy`** — grouping
- **`Join` / `GroupJoin`** — joining collections
- **`Distinct`** — unique elements
- **`Union`, `Intersect`, `Except`** — set operations
- **`Skip` / `Take`** — pagination
- **`First` / `FirstOrDefault` / `Last` / `Single`** — element operators
- **`Any` / `All` / `Contains`** — quantifiers
- **`Count` / `Sum` / `Average` / `Min` / `Max`** — aggregation
- **`Aggregate`** — custom accumulation
- **`OfType` / `Cast`** — type filtering
- **`ToArray` / `ToList` / `ToDictionary` / `ToLookup`** — conversion

### Key Concepts
- **Query syntax** (SQL-like) vs **Method syntax** (fluent)
- **Deferred execution** — query runs on enumeration
- **Immediate execution** — `ToList()`, `Count()`, `First()` trigger execution
- **Expression trees** — `Expression<Func<T, bool>>` for LINQ-to-SQL/EF translation
- **PLINQ** — `AsParallel()` for parallel query execution
- **Custom LINQ operators** via extension methods

---

## 7. Delegates, Events, Lambdas

### Delegates
- **Delegate declaration** — type-safe function pointer
- **Multicast delegates** — `+=`, `-=` chaining
- **Built-in delegates**: `Action`, `Func<T>`, `Predicate<T>`, `Comparison<T>`, `Converter<TInput, TOutput>`
- **Delegate covariance/contravariance**
- **`Invoke`** vs null-conditional invocation `?.Invoke()`

### Events
- **`event` keyword** — wrapper around delegate (publish-subscribe)
- **`EventHandler` / `EventHandler<TEventArgs>`** — standard pattern
- **Custom EventArgs** — inherit from `EventArgs`
- **Event accessors** (`add`/`remove`)
- **Weak Event pattern** — memory leak prevention
- **Memory leak risk** — event subscriptions keep objects alive

### Lambda Expressions
- **Expression lambda** — single expression (`x => x * x`)
- **Statement lambda** — block body (`x => { ... }`)
- **Captured variables / Closures** — lambda captures outer scope
- **Static lambda** (C# 9+) — `static (x) => x * x`, no capture
- **Discards** — `_` for unused parameters
- **`async` lambda** — `async (x) => await DoAsync(x)`

---

## 8. Async/Await & Concurrency

### Async/Await Basics
- **`async Task` / `async Task<T>`** — return types
- **`await`** — non-blocking wait
- **`ValueTask<T>`** — avoids allocation when result is synchronous (hot path)
- **`ConfigureAwait(false)`** — avoid capturing SynchronizationContext (library code)
- **`Task.Run()`** — CPU-bound work offloading
- **`Task.Delay()`** — async timer
- **`Task.WhenAll()`** — wait for all tasks
- **`Task.WhenAny()`** — wait for first task
- **`TaskCompletionSource<T>`** — manual task creation
- **`IAsyncEnumerable<T>`** — async streams (C# 8+)
- **`await foreach`** — consume async streams

### Async Pitfalls
- **Async void** — only for event handlers, exceptions crash process
- **Deadlock** — blocking on async with `.Result` or `.Wait()`
- **Fire-and-forget** — unobserved exceptions
- **N+1 async calls** — sequential awaits instead of concurrent

### Threading & Concurrency (System.Threading)
- **`Thread`** — direct thread management (low-level)
- **`ThreadPool`** — managed thread pool
- **`Task`** — higher-level abstraction (preferred)
- **Synchronization primitives**: `lock`, `Monitor`, `Mutex`, `SemaphoreSlim`, `ReaderWriterLockSlim`, `SpinLock`, `Barrier`, `CountdownEvent`, `AutoResetEvent/ManualResetEvent`
- **`Interlocked`** — lock-free atomic operations (`Increment`, `CompareExchange`)
- **`volatile`** — prevents compiler/CPU reordering
- **`ConcurrentDictionary<TKey, TValue>`**, `ConcurrentQueue<T>`, `ConcurrentStack<T>`, `ConcurrentBag<T>`, `BlockingCollection<T>`
- **`Parallel.For` / `Parallel.ForEach`** — data parallelism
- **`PLINQ`** — `AsParallel()`
- **`CancellationToken` / `CancellationTokenSource`** — cooperative cancellation

---

## 9. Memory Management & Performance

### Garbage Collection
- **Generations**: Gen 0 (short-lived), Gen 1 (buffer), Gen 2 (long-lived), LOH (>85KB)
- **GC modes**: Workstation, Server, Concurrent, Background
- **`IDisposable`** / `using` statement — deterministic cleanup
- **`IAsyncDisposable`** — `await using` (C# 8+)
- **`GC.Collect()`** — force collection, avoid in production
- **`GC.AddMemoryPressure()`** / `RemoveMemoryPressure()`
- **`WeakReference<T>`** — caching without preventing GC
- **`object pooling`** — `ArrayPool<T>`, `MemoryPool<T>`

### Performance Optimization
- **`Span<T>` / `ReadOnlySpan<T>`** — stack allocation, zero-copy slicing
- **`Memory<T>` / `ReadOnlyMemory<T>`** — async-safe Span
- **`StringBuilder`** — efficient string concatenation
- **String interning** — runtime reuse of identical strings
- **`ArrayPool<T>.Shared`** — rent/return temporary arrays
- **`ref struct`** — stack-only, no boxing
- **`in` parameters** — pass large structs by read-only reference
- **Boxing avoidance** — avoid casting value types to `object`
- **Constant vs ReadOnly** — `const` is compile-time, `readonly` is runtime
- **Big O notation** — algorithm complexity awareness
- **`BenchmarkDotNet`** — performance measurement

---

## 10. Exception Handling

### Structure & Types
- **`try` / `catch` / `finally`**
- **Exception filters** (`catch (ExType ex) when (condition)`) — C# 6+
- **`throw` vs `throw ex`** — preserve stack trace vs reset it
- **Common exception types**: `ArgumentNullException`, `InvalidOperationException`, `NullReferenceException`, `IndexOutOfRangeException`, `DivideByZeroException`, `IOException`, `FileNotFoundException`, `UnauthorizedAccessException`
- **Custom exception** — inherit from `Exception`, add serialization support

### Best Practices
- **Catch specific exceptions first**, general last
- **Try-Parse pattern** — avoid exceptions for expected failures
- **`using` statement** — auto-dispose (compiler generates try/finally)
- **Never swallow exceptions** silently
- **`AggregateException`** — from `Task.WhenAll()` failures

---

## 11. Attributes & Reflection

### Attributes
- **Built-in attributes**: `[Obsolete]`, `[Serializable]`, `[Conditional]`, `[DllImport]`, `[CallerMemberName]`, `[CallerLineNumber]`, `[CallerFilePath]`
- **Custom attributes** — inherit from `Attribute`
- **`[AttributeUsage]`** — restrict target types
- **Positional vs Named parameters** in attributes

### Reflection
- **`Type`** — `typeof()`, `GetType()`
- **`Assembly`** — loaded types, dynamic instantiation
- **`Activator.CreateInstance()`** — dynamic object creation
- **`PropertyInfo` / `MethodInfo` / `FieldInfo`** — member metadata
- **`GetCustomAttribute<T>()`** — reading attributes
- **`GetProperties()`, `GetMethods()`** — member discovery
- **`Invoke()`** — dynamic method call
- **`Expression Trees`** — compile-time code as data

---

## 12. Serialization

- **`System.Text.Json`** (modern, high-performance) — `JsonSerializer`, `Utf8JsonReader`, `Utf8JsonWriter`
- **`Newtonsoft.Json`** (Json.NET) — feature-rich, legacy
- **`XmlSerializer`** — XML serialization
- **`DataContractSerializer`** — WCF-style
- **`ISerializable`** — custom binary serialization
- **`[Serializable]` / `[NonSerialized]`**
- **`[JsonIgnore]` / `[JsonPropertyName]`**
- **Serialization callbacks**: `[OnSerializing]`, `[OnSerialized]`, `[OnDeserializing]`, `[OnDeserialized]`
- **Protocol Buffers (protobuf-net)** — compact binary
- **MessagePack** — ultra-fast binary

---

## 13. ADO.NET & Entity Framework

### ADO.NET
- **`SqlConnection`** / **`DbConnection`** — connection management
- **Connection pooling** — enabled by default, configured in connection string
- **`SqlCommand` / `DbCommand`** — parameterized queries (prevent SQL injection)
- **`SqlDataReader` / `DbDataReader`** — forward-only, read-only, low memory
- **`ExecuteScalar()`** — single value result
- **`ExecuteNonQuery()`** — INSERT/UPDATE/DELETE
- **Transactions**: `SqlTransaction`, `IsolationLevel` (ReadCommitted, Serializable, Snapshot, etc.)
- **`Dapper`** — micro-ORM (extension methods on `IDbConnection`)

### Entity Framework Core
- **`DbContext`** — unit of work + repository pattern
- **`DbSet<T>`** — entity collections (table mapping)
- **Migrations** — `Add-Migration`, `Update-Database`
- **Relationships**: One-to-Many, One-to-One, Many-to-Many
- **Eager loading** (`Include` / `ThenInclude`), **Explicit loading**, **Lazy loading**
- **`AsNoTracking()`** — read-only queries (performance)
- **`FromSqlRaw()`** — raw SQL when needed
- **Change tracking** — `Added`, `Modified`, `Deleted`, `Unchanged`, `Detached`
- **Concurrency handling** — `DbUpdateConcurrencyException`
- **Global query filters** — multi-tenancy, soft delete

---

## 14. ASP.NET Core Web API

### Controllers & Routing
- **`[ApiController]`** — automatic validation, binding, status codes
- **`[Route]`** / `[HttpGet]`, `[HttpPost]`, `[HttpPut]`, `[HttpDelete]`, `[HttpPatch]`
- **`ActionResult<T>`** — typed responses
- **Model binding** — `[FromBody]`, `[FromQuery]`, `[FromRoute]`, `[FromForm]`, `[FromHeader]`
- **Model validation** — data annotations (`[Required]`, `[StringLength]`, `[EmailAddress]`, `[Range]`) or FluentValidation
- **`ProblemDetails`** — RFC 7807 error responses
- **Minimal APIs** (.NET 6+) — `app.MapGet()`, `app.MapPost()`

### Middleware
- **Pipeline order**: Exception → HSTS → HTTPS → Static Files → Routing → CORS → Auth → Authorization → Endpoints
- **Custom middleware** — `RequestDelegate _next`, `InvokeAsync(HttpContext)`
- **Exception handling** — `UseExceptionHandler()`, custom middleware
- **`Swagger` / OpenAPI** — `AddSwaggerGen()`, `UseSwagger()` with `UseSwaggerUI()`
- **CORS** — `AddCors()`, `UseCors()`
- **Authentication** — JWT Bearer, OAuth 2.0, OpenID Connect, ASP.NET Core Identity
- **Authorization** — `[Authorize]`, policies, claims, roles
- **Rate limiting** (.NET 7+)

### Configuration
- **`appsettings.json`** / environment-specific configs
- **Options pattern** — `IOptions<T>`, `IOptionsSnapshot<T>`, `IOptionsMonitor<T>`
- **User Secrets** — development secrets (`dotnet user-secrets`)
- **Feature flags** — `Microsoft.FeatureManagement`

---

## 15. Dependency Injection

### Core Concepts
- **Inversion of Control (IoC)** — framework calls your code
- **Dependency Inversion Principle** — depend on abstractions, not concretions
- **Constructor injection** (preferred), **Property injection**, **Method injection**

### Service Lifetimes
- **Transient** — new instance every request (lightweight, stateless)
- **Scoped** — one instance per HTTP request/scope
- **Singleton** — one instance for application lifetime (thread-safe)
- **Captive dependency** — anti-pattern: singleton holding scoped/transient

### Registration Patterns
- **`AddTransient<TInterface, TImpl>()`**
- **`AddScoped<TInterface, TImpl>()`**
- **`AddSingleton<TInterface, TImpl>()`**
- **Factory registration**: `AddScoped(sp => new Service())`
- **Generic registration**: `typeof(IRepository<>), typeof(EfRepository<>)`
- **Decorator pattern** with DI
- **Built-in container** (`Microsoft.Extensions.DependencyInjection`) vs **third-party** (Autofac, SimpleInjector)

---

## 16. SOLID Principles

| Principle | Meaning | Key Point |
|-----------|---------|-----------|
| **S**ingle Responsibility | One class, one reason to change | Separation of concerns |
| **O**pen/Closed | Open for extension, closed for modification | Use abstraction, not modification |
| **L**iskov Substitution | Subtypes must be substitutable for base types | Don't break contracts |
| **I**nterface Segregation | Many specific interfaces > one general | Client-specific interfaces |
| **D**ependency Inversion | Depend on abstractions, not concretions | Inject interfaces, not implementations |

**Common violations to recognize:**
- **God Class** (SRP) — too many responsibilities
- **Switch statements** for type checking (OCP) — replace with polymorphism
- **Rectangle-Square problem** (LSP) — inheritance that breaks contracts
- **Fat interfaces** (ISP) — `NotImplementedException`
- **`new` keyword for dependencies** (DIP) — tight coupling

---

## 17. Design Patterns

### Creational
- **Singleton** — single instance (use DI container instead)
- **Factory Method** — abstract object creation
- **Abstract Factory** — families of related objects
- **Builder** — step-by-step complex object construction (fluent API)
- **Prototype** — clone existing objects

### Structural
- **Adapter** — make incompatible interfaces work together
- **Decorator** — add responsibilities dynamically (e.g., middleware)
- **Facade** — simplified interface to complex subsystem
- **Composite** — treat individual objects and compositions uniformly
- **Proxy** — control access (lazy init, caching, protection)

### Behavioral
- **Observer** — publish-subscribe (C# events are this pattern)
- **Strategy** — interchangeable algorithms (replace with lambdas/Func)
- **Command** — encapsulate requests (undo/redo)
- **State** — object behavior changes with internal state
- **Template Method** — algorithm skeleton, subclasses fill in steps
- **Chain of Responsibility** — pass request along handler chain (like middleware)

---

## 18. Modern & Advanced C# Features

### C# 6+
- Expression-bodied members
- Null-conditional operator (`?.`)
- String interpolation (`$"Hello {name}"`)
- `nameof` operator
- Exception filters (`when`)

### C# 7+
- Pattern matching (`is T x`, switch patterns)
- Tuples and deconstruction
- Local functions
- `out` variable declarations
- `ref` returns and locals
- `in` parameters
- `ref struct`

### C# 8+
- Nullable reference types
- Default interface methods
- Async streams (`IAsyncEnumerable<T>`, `await foreach`)
- Indices and ranges (`^1`, `.. `)
- `using` declaration
- Switch expressions

### C# 9+
- Records (`record`)
- Init-only setters (`{ get; init; }`)
- Top-level statements
- `with` expressions
- Pattern matching enhancements — relational, logical, list patterns
- Covariant return types
- Static lambdas

### C# 10+
- `record struct`
- Global usings (`global using`)
- File-scoped namespaces
- Constant interpolated strings
- Extended property patterns

### C# 11+
- Required members (`required` keyword)
- Raw string literals (""")
- Generic attributes
- List patterns
- `Span<byte>` improvements
- UTF-8 string literals
- File-local types (`file` keyword)

### C# 12+
- Primary constructors (non-record classes)
- Collection expressions (`[1, 2, 3]`)
- `params` spans
- `nameof` access for parameters
- Inline arrays

---

## 19. Memory & Threading Performance Terms

- **Stack vs Heap** — value types typically on stack, reference types on heap
- **Boxing** — value type → `object` (performance hit, avoid)
- **`Span<T>` / `Memory<T>`** — ref structs for zero-copy memory access
- **`ref struct`** — stack-only, no boxing, no async capture
- **`ArrayPool<T>`** — reduce allocations
- **`StringBuilder`** — reduce string concatenation allocations
- **`ValueTask<T>`** — avoid Task allocations for sync paths
- **`lock` / `Monitor`** — mutual exclusion
- **`Interlocked`** — atomic operations without locks
- **`volatile`** — prevent reordering between threads
- **`ReaderWriterLockSlim`** — multiple readers, exclusive writer
- **`SpinLock`** — busy-waiting (short critical sections only)
- **`ConcurrentDictionary` / `ConcurrentQueue`** — thread-safe collections

---

## 20. Testing (xUnit)

- **[Fact]** — parameterless test
- **[Theory]** / **[InlineData]**, **[MemberData]**, **[ClassData]** — parameterized tests
- **AAA pattern** — Arrange, Act, Assert
- **Mocking** — Moq, NSubstitute (isolate dependencies)
- **FluentAssertions** — readable assertions
- **WebApplicationFactory** — integration testing
- **`IDisposable`** — test cleanup
- **Test doubles**: Dummy, Fake, Stub, Mock, Spy

---

## Quick Reference: .NET Built-in Patterns

| Pattern | .NET Implementation |
|---------|-------------------|
| Observer | Events (`event EventHandler`) |
| Iterator | `IEnumerable<T>` / `IEnumerator<T>` |
| Strategy | `Func<T>`, `Action<T>`, lambdas |
| Decorator | Stream decorators (`GZipStream`, `CryptoStream`) |
| Facade | `HttpClient` wrapping complex HTTP |
| Adapter | ADO.NET providers (`DbProviderFactory`) |
| Template Method | ASP.NET Middleware, Stream |
| Factory | `HttpClientFactory`, `DbProviderFactory` |
| Singleton | DI container (`AddSingleton()`) |

---

## Interview Quick-Tips

1. **Value vs Reference types**: "Value types store data directly, reference types store a pointer to the heap."
2. **`string` is special**: Reference type but immutable, value-like equality (`==` compares content).
3. **`async/await` is not parallel**: It's cooperative multitasking for I/O; use `Task.Run()` or `Parallel.For` for CPU-bound work.
4. **`ConfigureAwait(false)`**: Prevents deadlocks in library code; don't use in UI code.
5. **LINQ is lazy**: Queries don't execute until enumerated (deferred execution).
6. **SOLID is foundational**: Especially Dependency Inversion (interfaces) and Single Responsibility.
7. **`record` vs `class`**: Records are for data with value equality; classes for identity.
8. **`lock` vs `SemaphoreSlim`**: Lock for mutual exclusion; Semaphore for limiting concurrency.
9. **`IEnumerable` vs `IQueryable`**: IEnumerable is in-memory; IQueryable translates to SQL (LINQ-to-SQL).
10. **`throw` vs `throw ex`**: `throw` preserves stack trace; `throw ex` resets it (lose call stack).
