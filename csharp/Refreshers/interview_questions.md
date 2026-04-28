# C# Technical Interview Questions

A curated list of questions based on the C# refresher series, organized by topic and seniority level. Focused on the topics most likely to appear in a conversational technical interview.

---

## 1. C# TYPE SYSTEM & BASICS

### Junior
1. What is the difference between a **value type** and a **reference type** in C#? Where is each stored?
2. Explain **boxing** and **unboxing**. Why can they be expensive?
3. What is the difference between `const` and `readonly`? When would you use each?
4. What does the `var` keyword do? Is it the same as `dynamic`?
5. What are **nullable value types** (e.g., `int?`)? How do you check if a nullable has a value?
6. What is the difference between `string` and `StringBuilder`? When would you choose one over the other?

### Mid
7. Explain the difference between `ref`, `out`, and `in` parameter modifiers. When would you use each?
8. What are **tuples** in C#? How do named tuples improve code readability?
9. What are **records** (`record` keyword)? How do they differ from classes and structs in terms of equality and immutability?
10. What is **pattern matching** in C#? Give examples of type patterns, property patterns, and relational patterns.
11. Explain the difference between `Array.CopyTo()` and `Array.Clone()`. What about deep copy vs shallow copy?

---

## 2. OOP: CLASSES, INHERITANCE, POLYMORPHISM & INTERFACES

### Junior
12. What is the difference between an **abstract class** and an **interface**? When would you choose one over the other?
13. Explain the `virtual` and `override` keywords. What happens if you don't use `override` when hiding a base method?
14. What does the `sealed` keyword do when applied to a class? To a method?
15. What is **constructor chaining**? How does the `base` keyword work in constructors?
16. What is the difference between public, private, protected, and internal access modifiers?

### Mid
17. What are **default interface methods** (C# 8.0+)? Why were they introduced?
18. What is **explicit interface implementation**? When would you need it?
19. Explain the difference between **composition** and **inheritance**. Give a real-world example where you'd choose composition over inheritance.
20. What is the **Liskov Substitution Principle**? Give an example of a violation in C#.
21. How does C# handle **multiple inheritance**? Why doesn't it support it for classes?

---

## 3. GENERICS

### Junior
22. What are **generics** in C#? What problem do they solve?
23. What is a **generic constraint**? Give examples of `where T : class`, `where T : struct`, `where T : new()`.

### Mid
24. Explain **covariance** and **contravariance** in C# generics. When would you use `in` and `out` keywords?
25. Why can't you use `operator ==` or `operator +` directly on generic type parameters? How do you work around this?
26. What is the difference between `List<T>` and `ArrayList`? Why should you prefer `List<T>`?

---

## 4. DELEGATES, EVENTS, LAMBDAS & CLOSURES

### Junior
27. What is a **delegate**? How is it different from a regular method call?
28. What are the built-in delegate types `Func<T>`, `Action<T>`, and `Predicate<T>`? When would you use each?
29. What is a **lambda expression**? What is the `=>` syntax?

### Mid
30. What is a **closure** in C#? How does capturing a variable in a lambda affect its lifetime?
31. What is the difference between a **delegate** and an **event**? Why can't you invoke an event from outside the declaring class?
32. What is a **multicast delegate**? How do you combine delegates and what is the return value of a multicast delegate?
33. Explain the standard **EventHandler pattern** in .NET. Why use `EventArgs` or `EventArgs<T>`?

---

## 5. LINQ

### Junior
34. What is **LINQ**? What are the two syntaxes for writing LINQ queries?
35. What is the difference between `.Where()` and `.Select()` in LINQ?
36. How do you sort data with LINQ? What is the difference between `OrderBy` and `ThenBy`?

### Mid
37. Explain **deferred execution** vs **immediate execution** in LINQ. Which methods trigger immediate execution?
38. What is the difference between `First()`, `FirstOrDefault()`, `Single()`, and `SingleOrDefault()`? When would each throw an exception?
39. How does `GroupBy()` work in LINQ? Give an example of grouping and aggregating.
40. What is the difference between `IEnumerable<T>` and `IQueryable<T>`? When would you use each with LINQ?
41. What is a **join** in LINQ? How does `Join()` differ from `GroupJoin()`?

---

## 6. ASYNC/AWAIT & ASYNCHRONOUS PROGRAMMING

### Junior
42. What is the `async` and `await` keyword? What does `await` do?
43. What return types can an async method have? What is the difference between `Task` and `Task<T>`?
44. How do you handle exceptions in async code? What happens if you don't await a task that throws?

### Mid
45. What is `ConfigureAwait(false)`? When and why would you use it?
46. What is the difference between `Task.Run()` and `async/await`? When would you use each?
47. What is `ValueTask<T>` and when should you use it instead of `Task<T>`?
48. What is `CancellationToken` and how do you use it to cancel async operations?
49. What are **async streams** (`IAsyncEnumerable<T>`)? Give a use case.
50. What is **SynchronizationContext** and how does it relate to `await` capturing context?

### Senior
51. Explain the **state machine** that the compiler generates for async methods. What happens under the hood?
52. How would you implement a **retry pattern** with async/await? What considerations are there for exponential backoff?

---

## 7. COLLECTIONS

### Junior
53. What is the difference between `List<T>`, `Dictionary<TKey, TValue>`, `HashSet<T>`, and `Queue<T>`? When would you use each?
54. What is the difference between an array (`T[]`) and a `List<T>`? When would you choose one over the other?

### Mid
55. What is the difference between `Dictionary<TKey, TValue>` and `ConcurrentDictionary<TKey, TValue>`? When would you use the concurrent version?
56. What is the difference between `Stack<T>` and `Queue<T>`? Give a real-world use case for each.
57. How does `HashSet<T>` ensure uniqueness? What methods must a type implement to work correctly in a `HashSet<T>`?

---

## 8. MEMORY MANAGEMENT & IDISPOSABLE

### Junior
58. How does the **garbage collector** work in .NET? What are the generations (Gen 0, 1, 2)?
59. What is the `IDisposable` interface? When and how do you use it?
60. What is the `using` statement? What does it guarantee?

### Mid
61. What is the **dispose pattern**? When would you implement a finalizer alongside `Dispose`?
62. What is a **large object heap (LOH)**? What objects go there and why does it matter?
63. What causes **memory leaks** in .NET? Give examples (e.g., event handlers, static references, forgotten subscriptions).
64. What is `GC.Collect()`? Why should you generally avoid calling it explicitly?

---

## 9. DEPENDENCY INJECTION

### Mid
65. What is **Dependency Injection**? What problem does it solve?
66. Explain the three DI **service lifetimes**: `Singleton`, `Scoped`, and `Transient`. When would you use each?
67. What is a **captive dependency**? How do you detect one?
68. How does DI integrate with ASP.NET Core's request pipeline?

---

## 10. ASP.NET CORE WEB API

### Mid
69. What is **middleware** in ASP.NET Core? How does the pipeline work?
70. What is the difference between **attribute routing** and **conventional routing**? Which is preferred for Web APIs?
71. How does **model binding** work? How do `[FromBody]`, `[FromQuery]`, `[FromRoute]`, and `[FromHeader]` differ?
72. How do you validate incoming request data in ASP.NET Core? What is `[ApiController]` and how does it help?
73. What is the difference between **authentication** and **authorization**? How do you implement JWT authentication in ASP.NET Core?
74. How do you implement **global exception handling** in ASP.NET Core?

---

## 11. ENTITY FRAMEWORK CORE

### Mid
75. What is the **N+1 query problem** in EF Core? How do you avoid it?
76. What is the difference between **eager loading**, **lazy loading**, and **explicit loading**?
77. What is **change tracking** in EF Core? How does `DbContext` know what changed?
78. What are **migrations** in EF Core? How do you create and apply them?
79. What is the difference between `AsNoTracking()` and the default tracking behavior? When would you use `AsNoTracking()`?
80. How do you handle **concurrency conflicts** in EF Core?

---

## 12. EXCEPTION HANDLING

### Junior
81. What is the difference between `throw` and `throw ex` in a catch block? Why is one preferred?
82. What is the purpose of the `finally` block? Does it always execute?

### Mid
83. What are **exception filters** (`when` keyword)? Give an example where they're useful.
84. What is the difference between `ArgumentException`, `ArgumentNullException`, and `ArgumentOutOfRangeException`? When would you throw each?
85. What are **best practices** for designing custom exceptions? Should they be serializable?

---

## 13. THREADING & CONCURRENCY

### Mid
86. What is the difference between `Thread`, `ThreadPool`, and `Task`? When would you use each?
87. What is the **Task Parallel Library (TPL)**? How does `Parallel.ForEach` differ from a regular `foreach`?
88. What synchronization primitives does .NET provide? Explain `lock`, `Monitor`, `Mutex`, `SemaphoreSlim`, and `ReaderWriterLockSlim`.
89. What are **concurrent collections** (`ConcurrentBag<T>`, `ConcurrentQueue<T>`, etc.)? When should you use them instead of locking manually?
90. What is a **deadlock**? How do you prevent one in C#?

---

## 14. SOLID PRINCIPLES

### Mid
91. Explain each of the **SOLID** principles. Give a C# example of a violation and the fix for each.
92. What is the **Dependency Inversion Principle**? How does it differ from Dependency Injection?
93. What is the **Interface Segregation Principle**? Give an example of a "fat interface" and how you'd refactor it.

---

## 15. DESIGN PATTERNS (COMMON)

### Mid
94. Implement a thread-safe **Singleton** in C#. What are the options (static constructor, `Lazy<T>`, double-check locking)?
95. What is the **Factory Method** pattern? When would you use it over a simple constructor?
96. What is the **Observer** pattern? How does C# support it natively with events?
97. What is the **Strategy** pattern? Give a real-world example.

---

## 16. ATTRIBUTES & REFLECTION

### Mid
98. What are **attributes** in C#? Give examples of built-in attributes and how to create a custom one.
99. What is **reflection**? How do you inspect types, methods, and properties at runtime?
100. What are the **performance implications** of using reflection? What alternatives exist (source generators, expression trees)?

---

## 17. TESTING

### Mid
101. What is the difference between a **unit test**, an **integration test**, and a **functional test**?
102. What is **mocking**? How do frameworks like Moq or NSubstitute work?
103. What is **test-driven development (TDD)**? What is the Red-Green-Refactor cycle?
104. How do you test async methods? What should you be careful about?

---

## 18. SENIOR-LEVEL & SYSTEM DESIGN

### Senior
105. How would you design a **background job processing system** in .NET? Consider `IHostedService`, `BackgroundService`, and `Channel<T>`.
106. How would you architect a **high-throughput API** in ASP.NET Core? Consider caching, rate limiting, async I/O, connection pooling, and database optimization.
107. Explain how you would implement **CQRS** (Command Query Responsibility Segregation) in a .NET application.
108. How do you handle **distributed transactions** across microservices in .NET?
109. What considerations go into **versioning a Web API**? Compare URI versioning, query string versioning, and header versioning.
110. How would you implement **real-time communication** in .NET (SignalR)? What transport mechanisms does it use?

---

## 19. BEHAVIORAL & EXPERIENCE

111. Describe a time you debugged a **memory leak** in a .NET application. What tools did you use (dotMemory, PerfView, SOS)?
112. How would you approach **migrating a legacy .NET Framework application to .NET Core/.NET 8+**? What are the biggest challenges?
113. Tell me about a time you improved the **performance** of a slow API endpoint. What was the bottleneck and how did you fix it?
114. How do you stay up to date with new C# and .NET features? What's a recent feature you've adopted?
115. Describe your experience with **code reviews**. What do you look for in a C# code review?

---

*Generated from the C# Refreshers series (00–30). Focused on topics most likely to appear in a conversational technical interview for C#/.NET roles.*
