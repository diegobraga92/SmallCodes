/*
    C# ASYNC/AWAIT AND ASYNCHRONOUS PROGRAMMING
    File: 11_async_await.cs
    
    This file demonstrates async/await and asynchronous programming in C#,
    covering concepts from junior to upper mid-level. Asynchronous programming
    enables responsive applications by allowing non-blocking operations,
    particularly important for I/O-bound work and modern application development.
    
    Key Concepts Covered:
    1. Async/Await Syntax and Basics
    2. Task and Task<T> Types
    3. Async Method Return Types
    4. Exception Handling in Async Code
    5. Cancellation with CancellationToken
    6. Async Streams (IAsyncEnumerable)
    7. ValueTask for Performance
    8. Async Patterns and Best Practices
    9. Async with LINQ and Collections
    10. Real-world Async Scenarios
*/

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

namespace CSharpRefresher.AsyncAwait
{
    class Program
    {
        static async Task Main(string[] args)
        {
            Console.WriteLine("=== C# Async/Await Demonstration ===\n");
            
            await DemonstrateAsyncBasics();
            await DemonstrateTaskTypes();
            await DemonstrateAsyncReturnTypes();
            await DemonstrateExceptionHandling();
            await DemonstrateCancellation();
            await DemonstrateAsyncStreams();
            await DemonstrateValueTask();
            await DemonstrateAsyncPatterns();
            await DemonstrateAsyncWithLinq();
            await DemonstrateRealWorldScenarios();
            
            Console.WriteLine("\n=== Async/Await Complete ===");
        }
        
        static async Task DemonstrateAsyncBasics()
        {
            Console.WriteLine("============ ASYNC/AWAIT BASICS ============\n");
            
            // ============ BASIC ASYNC/AWAIT SYNTAX ============
            Console.WriteLine("=== 1. Basic Async/Await Syntax ===");
            
            async Task<string> GetGreetingAsync()
            {
                await Task.Delay(100); // Simulate async work
                return "Hello, Async World!";
            }
            
            async Task ProcessDataAsync()
            {
                Console.WriteLine("Starting async processing...");
                var greeting = await GetGreetingAsync();
                Console.WriteLine($"Result: {greeting}");
                Console.WriteLine("Processing complete.");
            }
            
            await ProcessDataAsync();
            
            // ============ ASYNC METHOD STRUCTURE ============
            Console.WriteLine("\n=== 2. Async Method Structure ===");
            
            async Task<int> CalculateAsync(int x, int y)
            {
                // Async work simulation
                await Task.Delay(50);
                
                // Multiple awaits
                var sum = await Task.FromResult(x + y);
                var product = await Task.Run(() => x * y);
                
                return sum + product;
            }
            
            var result = await CalculateAsync(3, 4);
            Console.WriteLine($"CalculateAsync(3, 4) = {result}");
            
            // ============ AWAIT EXPRESSIONS ============
            Console.WriteLine("\n=== 3. Await Expressions ===");
            
            async Task DemonstrateAwaitExpressions()
            {
                // Await in variable assignment
                var task1 = Task.Delay(100);
                await task1;
                
                // Await in expression
                int value = await Task.Run(() => 42);
                Console.WriteLine($"Value from task: {value}");
                
                // Await in using statement (C# 8.0+)
                await using (var stream = new MemoryStream())
                {
                    await stream.WriteAsync(new byte[] { 1, 2, 3 }, 0, 3);
                    Console.WriteLine("Async using completed");
                }
                
                // Await in foreach (C# 8.0+)
                await foreach (var item in GenerateNumbersAsync())
                {
                    Console.WriteLine($"Async foreach item: {item}");
                }
            }
            
            await DemonstrateAwaitExpressions();
            
            // ============ CONFIGURING AWAIT ============
            Console.WriteLine("\n=== 4. ConfigureAwait ===");
            
            async Task DemonstrateConfigureAwait()
            {
                // ConfigureAwait(false) for performance in library code
                await Task.Delay(100).ConfigureAwait(false);
                
                Console.WriteLine("""
                    ConfigureAwait(false):
                    • Avoids capturing SynchronizationContext
                    • Improves performance in library code
                    • Use in non-UI code to prevent deadlocks
                    • Don't use in UI code that needs context
                    """);
                
                // Example: Library method that doesn't need context
                async Task<string> GetDataFromApiAsync()
                {
                    using var client = new HttpClient();
                    var response = await client.GetAsync("https://api.example.com/data")
                        .ConfigureAwait(false);
                    return await response.Content.ReadAsStringAsync()
                        .ConfigureAwait(false);
                }
            }
            
            await DemonstrateConfigureAwait();
            
            // ============ FIRE AND FORGET ============
            Console.WriteLine("\n=== 5. Fire and Forget (Caution) ===");
            
            async Task FireAndForgetAsync()
            {
                // Don't do this: unobserved exceptions
                // Task.Run(() => SomeMethod()); // Bad
                
                // Better: handle exceptions
                _ = Task.Run(async () =>
                {
                    try
                    {
                        await Task.Delay(100);
                        Console.WriteLine("Fire and forget task completed");
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"Fire and forget error: {ex.Message}");
                    }
                });
                
                Console.WriteLine("Main thread continues immediately");
            }
            
            await FireAndForgetAsync();
            await Task.Delay(150); // Wait for fire-and-forget to complete
        }
        
        static async Task DemonstrateTaskTypes()
        {
            Console.WriteLine("\n============ TASK AND TASK<T> TYPES ============\n");
            
            // ============ TASK VS TASK<T> ============
            Console.WriteLine("=== 1. Task vs Task<T> ===");
            
            // Task - for async operations without return value
            async Task PerformWorkAsync()
            {
                await Task.Delay(100);
                Console.WriteLine("Work completed");
            }
            
            // Task<T> - for async operations with return value
            async Task<int> CalculateValueAsync()
            {
                await Task.Delay(100);
                return 42;
            }
            
            await PerformWorkAsync();
            var value = await CalculateValueAsync();
            Console.WriteLine($"Calculated value: {value}");
            
            // ============ TASK CREATION METHODS ============
            Console.WriteLine("\n=== 2. Task Creation Methods ===");
            
            // Task.Run for CPU-bound work
            var cpuTask = Task.Run(() =>
            {
                Console.WriteLine("CPU-bound work starting...");
                Thread.Sleep(100); // Simulate CPU work
                return Enumerable.Range(1, 1000).Sum();
            });
            
            // Task.FromResult for already-completed tasks
            var completedTask = Task.FromResult("Immediate result");
            
            // Task.Delay for timed delays
            var delayTask = Task.Delay(200);
            
            // Task.WhenAll for multiple tasks
            var task1 = Task.Delay(100);
            var task2 = Task.Delay(150);
            var task3 = Task.Delay(200);
            await Task.WhenAll(task1, task2, task3);
            Console.WriteLine("All tasks completed");
            
            // Task.WhenAny for first completed task
            var tasks = new[] { Task.Delay(300), Task.Delay(100), Task.Delay(200) };
            var firstCompleted = await Task.WhenAny(tasks);
            Console.WriteLine("First task completed");
            
            // ============ TASK CONTINUATION ============
            Console.WriteLine("\n=== 3. Task Continuation ===");
            
            var initialTask = Task.Run(() => 
            {
                Console.WriteLine("Initial task running");
                return 10;
            });
            
            // ContinueWith for explicit continuations
            var continuation = initialTask.ContinueWith(prevTask =>
            {
                Console.WriteLine($"Previous result: {prevTask.Result}");
                return prevTask.Result * 2;
            });
            
            var result = await continuation;
            Console.WriteLine($"Continuation result: {result}");
            
            // Multiple continuations
            var chain = Task.Run(() => 5)
                .ContinueWith(t => t.Result + 3)
                .ContinueWith(t => t.Result * 2)
                .ContinueWith(t => $"Final: {t.Result}");
            
            Console.WriteLine($"Chained result: {await chain}");
            
            // ============ TASK COMPLETION SOURCE ============
            Console.WriteLine("\n=== 4. TaskCompletionSource ===");
            
            var tcs = new TaskCompletionSource<int>();
            
            // Simulate async completion
            _ = Task.Run(async () =>
            {
                await Task.Delay(100);
                tcs.SetResult(42); // Complete with result
                // tcs.SetException(new Exception("Error")); // Complete with error
                // tcs.SetCanceled(); // Complete as canceled
            });
            
            try
            {
                var tcsResult = await tcs.Task;
                Console.WriteLine($"TaskCompletionSource result: {tcsResult}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"TaskCompletionSource error: {ex.Message}");
            }
            
            // ============ TASK STATUS AND PROPERTIES ============
            Console.WriteLine("\n=== 5. Task Status and Properties ===");
            
            var sampleTask = Task.Run(() => Thread.Sleep(100));
            
            Console.WriteLine($"Task status: {sampleTask.Status}");
            Console.WriteLine($"IsCompleted: {sampleTask.IsCompleted}");
            Console.WriteLine($"IsCanceled: {sampleTask.IsCanceled}");
            Console.WriteLine($"IsFaulted: {sampleTask.IsFaulted}");
            
            await sampleTask;
            Console.WriteLine($"After completion - Status: {sampleTask.Status}");
        }
        
        static async Task DemonstrateAsyncReturnTypes()
        {
            Console.WriteLine("\n============ ASYNC RETURN TYPES ============\n");
            
            // ============ VALID ASYNC RETURN TYPES ============
            Console.WriteLine("=== 1. Valid Async Return Types ===");
            
            // Task
            async Task DoWorkAsync()
            {
                await Task.Delay(100);
            }
            
            // Task<T>
            async Task<int> GetNumberAsync()
            {
                await Task.Delay(100);
                return 42;
            }
            
            // ValueTask (C# 7.0+)
            async ValueTask<int> GetNumberValueAsync()
            {
                await Task.Delay(100);
                return 42;
            }
            
            // void (for event handlers - use with caution)
            async void EventHandlerMethod()
            {
                try
                {
                    await Task.Delay(100);
                    Console.WriteLine("Event handler completed");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Event handler error: {ex.Message}");
                }
            }
            
            await DoWorkAsync();
            Console.WriteLine($"GetNumberAsync: {await GetNumberAsync()}");
            Console.WriteLine($"GetNumberValueAsync: {await GetNumberValueAsync()}");
            
            // ============ ASYNC MAIN METHODS ============
            Console.WriteLine("\n=== 2. Async Main Methods (C# 7.1+) ===");
            
            Console.WriteLine("""
                Valid Main signatures:
                • static async Task Main()
                • static async Task<int> Main()
                • static async Task Main(string[] args)
                • static async Task<int> Main(string[] args)
                
                Allows await in Main method directly.
                """);
            
            // ============ IASYNCENUMERABLE<T> (C# 8.0+) ============
            Console.WriteLine("\n=== 3. IAsyncEnumerable<T> (Async Streams) ===");
            
            static async IAsyncEnumerable<int> GenerateNumbersAsync()
            {
                for (int i = 1; i <= 5; i++)
                {
                    await Task.Delay(100);
                    yield return i;
                }
            }
            
            Console.WriteLine("Async stream numbers:");
            await foreach (var number in GenerateNumbersAsync())
            {
                Console.WriteLine($"  {number}");
            }
            
            // ============ CUSTOM AWAITABLE TYPES ============
            Console.WriteLine("\n=== 4. Custom Awaitable Types ===");
            
            class CustomAwaitable
            {
                public CustomAwaiter GetAwaiter() => new CustomAwaiter();
            }
            
            class CustomAwaiter : System.Runtime.CompilerServices.INotifyCompletion
            {
                private bool _isCompleted = false;
                public bool IsCompleted => _isCompleted;
                
                public void OnCompleted(Action continuation)
                {
                    Task.Run(() =>
                    {
                        Thread.Sleep(100);
                        _isCompleted = true;
                        continuation();
                    });
                }
                
                public int GetResult() => 42;
            }
            
            async Task UseCustomAwaitable()
            {
                var result = await new CustomAwaitable();
                Console.WriteLine($"Custom awaitable result: {result}");
            }
            
            await UseCustomAwaitable();
            
            // ============ ASYNC LAMBDAS ============
            Console.WriteLine("\n=== 5. Async Lambdas ===");
            
            Func<Task<int>> asyncLambda = async () =>
            {
                await Task.Delay(100);
                return 42;
            };
            
            EventHandler asyncEventHandler = async (sender, e) =>
            {
                await Task.Delay(100);
                Console.WriteLine("Async event handled");
            };
            
            var lambdaResult = await asyncLambda();
            Console.WriteLine($"Async lambda result: {lambdaResult}");
        }
        
        static async Task DemonstrateExceptionHandling()
        {
            Console.WriteLine("\n============ EXCEPTION HANDLING IN ASYNC CODE ============\n");
            
            // ============ BASIC ASYNC EXCEPTION HANDLING ============
            Console.WriteLine("=== 1. Basic Async Exception Handling ===");
            
            async Task<int> MightFailAsync(bool shouldFail)
            {
                await Task.Delay(100);
                if (shouldFail)
                    throw new InvalidOperationException("Async operation failed!");
                return 42;
            }
            
            try
            {
                var result = await MightFailAsync(true);
                Console.WriteLine($"Result: {result}");
            }
            catch (InvalidOperationException ex)
            {
                Console.WriteLine($"Caught exception: {ex.Message}");
            }
            
            // ============ AGGREGATE EXCEPTIONS ============
            Console.WriteLine("\n=== 2. Aggregate Exceptions ===");
            
            async Task DemonstrateAggregateExceptions()
            {
                var task1 = Task.Run(() => throw new Exception("Task 1 failed"));
                var task2 = Task.Run(() => throw new Exception("Task 2 failed"));
                
                try
                {
                    await Task.WhenAll(task1, task2);
                }
                catch (AggregateException agEx)
                {
                    Console.WriteLine($"AggregateException with {agEx.InnerExceptions.Count} inner exceptions:");
                    foreach (var inner in agEx.InnerExceptions)
                    {
                        Console.WriteLine($"  - {inner.Message}");
                    }
                }
                catch (Exception ex)
                {
                    // WhenAll unwraps AggregateException in async/await
                    Console.WriteLine($"Exception: {ex.Message}");
                }
            }
            
            await DemonstrateAggregateExceptions();
            
            // ============ HANDLING MULTIPLE ASYNC EXCEPTIONS ============
            Console.WriteLine("\n=== 3. Handling Multiple Async Exceptions ===");
            
            async Task HandleMultipleAsyncExceptions()
            {
                var tasks = new List<Task>();
                
                for (int i = 0; i < 3; i++)
                {
                    int id = i;
                    tasks.Add(Task.Run(async () =>
                    {
                        await Task.Delay(100);
                        if (id == 1) throw new Exception($"Task {id} failed");
                        Console.WriteLine($"Task {id} completed");
                    }));
                }
                
                // Wait for all tasks, collect exceptions
                var allTasks = Task.WhenAll(tasks);
                try
                {
                    await allTasks;
                }
                catch
                {
                    // Handle individual task exceptions
                    foreach (var task in tasks)
                    {
                        if (task.IsFaulted)
                        {
                            Console.WriteLine($"Faulted task: {task.Exception.InnerException.Message}");
                        }
                    }
                }
            }
            
            await HandleMultipleAsyncExceptions();
            
            // ============ EXCEPTION FILTERS IN ASYNC CODE ============
            Console.WriteLine("\n=== 4. Exception Filters in Async Code (C# 6.0+) ===");
            
            async Task DemonstrateExceptionFilters()
            {
                try
                {
                    await Task.Run(() => throw new InvalidOperationException("Test error"));
                }
                catch (InvalidOperationException ex) when (ex.Message.Contains("Test"))
                {
                    Console.WriteLine($"Exception filtered and caught: {ex.Message}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"General exception: {ex.Message}");
                }
            }
            
            await DemonstrateExceptionFilters();
            
            // ============ FINALLY IN ASYNC CODE ============
            Console.WriteLine("\n=== 5. Finally in Async Code ===");
            
            async Task DemonstrateFinally()
            {
                Console.WriteLine("Starting async operation...");
                try
                {
                    await Task.Delay(100);
                    Console.WriteLine("Async operation completed");
                }
                finally
                {
                    Console.WriteLine("Finally block executed (cleanup)");
                }
            }
            
            await DemonstrateFinally();
            
            // ============ UNOBSERVED EXCEPTIONS ============
            Console.WriteLine("\n=== 6. Unobserved Exceptions ===");
            
            TaskScheduler.UnobservedTaskException += (sender, e) =>
            {
                Console.WriteLine($"Unobserved task exception: {e.Exception.Message}");
                e.SetObserved(); // Mark as observed to prevent crash
            };
            
            // Fire and forget without await (dangerous)
            _ = Task.Run(() => throw new Exception("This will be unobserved"));
            
            // Force GC to trigger unobserved exception handler
            GC.Collect();
            GC.WaitForPendingFinalizers();
            await Task.Delay(100);
        }
        
        static async Task DemonstrateCancellation()
        {
            Console.WriteLine("\n============ CANCELLATION WITH CANCELLATIONTOKEN ============\n");
            
            // ============ CANCELLATIONTOKEN BASICS ============
            Console.WriteLine("=== 1. CancellationToken Basics ===");
            
            var cts = new CancellationTokenSource();
            var token = cts.Token;
            
            async Task LongRunningOperationAsync(CancellationToken cancellationToken)
            {
                Console.WriteLine("Long operation started");
                
                for (int i = 0; i < 10; i++)
                {
                    // Check for cancellation
                    cancellationToken.ThrowIfCancellationRequested();
                    
                    await Task.Delay(100, cancellationToken);
                    Console.WriteLine($"  Progress: {i + 1}/10");
                }
                
                Console.WriteLine("Long operation completed");
            }
            
            // Start operation and cancel after 300ms
            var operation = LongRunningOperationAsync(token);
            _ = Task.Run(async () =>
            {
                await Task.Delay(300);
                Console.WriteLine("Cancelling operation...");
                cts.Cancel();
            });
            
            try
            {
                await operation;
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Operation was cancelled");
            }
            
            // ============ MULTIPLE CANCELLATION TOKENS ============
            Console.WriteLine("\n=== 2. Multiple Cancellation Tokens ===");
            
            var cts1 = new CancellationTokenSource();
            var cts2 = new CancellationTokenSource();
            
            // Create linked token source
            var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(
                cts1.Token, cts2.Token);
            
            async Task WithLinkedTokensAsync(CancellationToken cancellationToken)
            {
                try
                {
                    while (!cancellationToken.IsCancellationRequested)
                    {
                        Console.WriteLine("Working...");
                        await Task.Delay(100, cancellationToken);
                    }
                }
                catch (OperationCanceledException)
                {
                    Console.WriteLine("Cancelled via linked token");
                }
            }
            
            var linkedTask = WithLinkedTokensAsync(linkedCts.Token);
            await Task.Delay(250);
            cts1.Cancel(); // This will cancel the linked token
            await linkedTask;
            
            // ============ CANCELLATION WITH TIMEOUT ============
            Console.WriteLine("\n=== 3. Cancellation with Timeout ===");
            
            using (var timeoutCts = new CancellationTokenSource(TimeSpan.FromSeconds(0.5)))
            {
                try
                {
                    await Task.Delay(1000, timeoutCts.Token);
                }
                catch (OperationCanceledException)
                {
                    Console.WriteLine("Task cancelled due to timeout");
                }
            }
            
            // ============ CANCELLATION CALLBACKS ============
            Console.WriteLine("\n=== 4. Cancellation Callbacks ===");
            
            var callbackCts = new CancellationTokenSource();
            callbackCts.Token.Register(() =>
            {
                Console.WriteLine("Cancellation requested! Performing cleanup...");
            });
            
            // Start and cancel
            var callbackTask = Task.Delay(1000, callbackCts.Token);
            _ = Task.Run(async () =>
            {
                await Task.Delay(100);
                callbackCts.Cancel();
            });
            
            try { await callbackTask; } catch (OperationCanceledException) { }
            
            // ============ POLLING VS CALLBACKS ============
            Console.WriteLine("\n=== 5. Polling vs Callbacks ===");
            
            async Task DemonstratePollingAsync(CancellationToken cancellationToken)
            {
                // Polling approach
                while (!cancellationToken.IsCancellationRequested)
                {
                    // Do work
                    await Task.Delay(100);
                }
                
                Console.WriteLine("Cancelled via polling");
            }
            
            async Task DemonstrateCallbackAsync(CancellationToken cancellationToken)
            {
                using (cancellationToken.Register(() => 
                    Console.WriteLine("Cancellation callback invoked")))
                {
                    try
                    {
                        await Task.Delay(5000, cancellationToken);
                    }
                    catch (OperationCanceledException)
                    {
                        Console.WriteLine("Operation cancelled");
                    }
                }
            }
            
            var pollCts = new CancellationTokenSource();
            var pollTask = DemonstratePollingAsync(pollCts.Token);
            await Task.Delay(300);
            pollCts.Cancel();
            await pollTask;
            
            // ============ CANCELLATION BEST PRACTICES ============
            Console.WriteLine("\n=== 6. Cancellation Best Practices ===");
            
            Console.WriteLine("""
                Best practices for cancellation:
                
                1. Always accept CancellationToken parameter in async methods
                2. Pass token to all async operations you call
                3. Use ThrowIfCancellationRequested() for polling
                4. Clean up resources in cancellation callbacks
                5. Use timeouts for operations that should complete quickly
                6. Document cancellation behavior in method signatures
                7. Consider using CancellationToken.None for required operations
                """);
        }
        
        static async Task DemonstrateAsyncStreams()
        {
            Console.WriteLine("\n============ ASYNC STREAMS (IASYNCENUMERABLE) ============\n");
            
            // ============ BASIC ASYNC STREAMS ============
            Console.WriteLine("=== 1. Basic Async Streams ===");
            
            static async IAsyncEnumerable<int> GenerateSequenceAsync()
            {
                for (int i = 1; i <= 5; i++)
                {
                    await Task.Delay(100); // Simulate async work
                    yield return i;
                }
            }
            
            Console.WriteLine("Async sequence:");
            await foreach (var number in GenerateSequenceAsync())
            {
                Console.WriteLine($"  Received: {number}");
            }
            
            // ============ ASYNC STREAMS WITH CANCELLATION ============
            Console.WriteLine("\n=== 2. Async Streams with Cancellation ===");
            
            static async IAsyncEnumerable<int> GenerateWithCancellationAsync(
                [System.Runtime.CompilerServices.EnumeratorCancellation] 
                CancellationToken cancellationToken = default)
            {
                for (int i = 1; i <= 10; i++)
                {
                    await Task.Delay(100, cancellationToken);
                    yield return i;
                }
            }
            
            var streamCts = new CancellationTokenSource();
            var streamTask = Task.Run(async () =>
            {
                try
                {
                    await foreach (var item in GenerateWithCancellationAsync()
                        .WithCancellation(streamCts.Token))
                    {
                        Console.WriteLine($"  Item: {item}");
                        if (item == 3) streamCts.Cancel();
                    }
                }
                catch (OperationCanceledException)
                {
                    Console.WriteLine("Async stream cancelled");
                }
            });
            
            await streamTask;
            
            // ============ ASYNC STREAMS WITH LINQ ============
            Console.WriteLine("\n=== 3. Async Streams with LINQ ===");
            
            // Note: System.Linq.Async NuGet package needed for full LINQ support
            static async IAsyncEnumerable<string> GetItemsAsync()
            {
                string[] items = { "Apple", "Banana", "Cherry", "Date", "Elderberry" };
                foreach (var item in items)
                {
                    await Task.Delay(50);
                    yield return item;
                }
            }
            
            Console.WriteLine("Filtered async stream:");
            await foreach (var item in GetItemsAsync())
            {
                if (item.Length > 5)
                    Console.WriteLine($"  Long item: {item}");
            }
            
            // ============ ASYNC STREAMS FOR DATA PAGINATION ============
            Console.WriteLine("\n=== 4. Async Streams for Data Pagination ===");
            
            class DataService
            {
                private int currentPage = 0;
                private const int PageSize = 3;
                private readonly List<string> allData = new List<string>
                {
                    "Item1", "Item2", "Item3", "Item4", "Item5",
                    "Item6", "Item7", "Item8", "Item9", "Item10"
                };
                
                public async IAsyncEnumerable<string> GetDataStreamAsync()
                {
                    while (currentPage * PageSize < allData.Count)
                    {
                        Console.WriteLine($"Fetching page {currentPage + 1}...");
                        await Task.Delay(200); // Simulate network delay
                        
                        var pageData = allData
                            .Skip(currentPage * PageSize)
                            .Take(PageSize);
                        
                        foreach (var item in pageData)
                        {
                            yield return item;
                        }
                        
                        currentPage++;
                    }
                }
            }
            
            var dataService = new DataService();
            Console.WriteLine("Paged data stream:");
            await foreach (var item in dataService.GetDataStreamAsync())
            {
                Console.WriteLine($"  Received: {item}");
            }
            
            // ============ ASYNC STREAMS FOR REAL-TIME DATA ============
            Console.WriteLine("\n=== 5. Async Streams for Real-time Data ===");
            
            class Sensor
            {
                public async IAsyncEnumerable<double> ReadSensorAsync()
                {
                    var random = new Random();
                    while (true)
                    {
                        await Task.Delay(100);
                        yield return random.NextDouble() * 100;
                    }
                }
            }
            
            // Example of consuming real-time stream with cancellation
            var sensor = new Sensor();
            var sensorCts = new CancellationTokenSource();
            
            _ = Task.Run(async () =>
            {
                await foreach (var reading in sensor.ReadSensorAsync()
                    .WithCancellation(sensorCts.Token))
                {
                    Console.WriteLine($"  Sensor reading: {reading:F2}");
                    if (reading > 80) break;
                }
                sensorCts.Cancel();
            });
            
            await Task.Delay(500);
            sensorCts.Cancel();
            
            // ============ ASYNC STREAMS BEST PRACTICES ============
            Console.WriteLine("\n=== 6. Async Streams Best Practices ===");
            
            Console.WriteLine("""
                Async streams best practices:
                
                1. Use for data that arrives asynchronously over time
                2. Always support cancellation
                3. Clean up resources in disposal
                4. Handle exceptions gracefully
                5. Consider backpressure (consumer speed)
                6. Use for pagination of large datasets
                7. Great for real-time data feeds
                8. Consider buffering for bursty data
                """);
        }
        
        static async Task DemonstrateValueTask()
        {
            Console.WriteLine("\n============ VALUETASK FOR PERFORMANCE ============\n");
            
            // ============ VALUETASK VS TASK ============
            Console.WriteLine("=== 1. ValueTask vs Task ===");
            
            private static readonly Dictionary<int, string> cache = new()
            {
                { 1, "One" }, { 2, "Two" }, { 3, "Three" }
            };
            
            // Using ValueTask for potentially synchronous completion
            async ValueTask<string> GetValueAsync(int key)
            {
                // Check cache synchronously
                if (cache.TryGetValue(key, out var value))
                    return value; // Synchronous completion
                
                // If not in cache, do async work
                await Task.Delay(100); // Simulate async lookup
                return $"Value-{key}";
            }
            
            Console.WriteLine("ValueTask performance test:");
            var sw = Stopwatch.StartNew();
            
            for (int i = 0; i < 1000; i++)
            {
                var result = await GetValueAsync(1); // Usually from cache
            }
            
            sw.Stop();
            Console.WriteLine($"  Cached lookups: {sw.ElapsedMilliseconds}ms");
            
            // ============ WHEN TO USE VALUETASK ============
            Console.WriteLine("\n=== 2. When to Use ValueTask ===");
            
            Console.WriteLine("""
                Use ValueTask when:
                • Method often completes synchronously
                • High-performance scenarios
                • Avoiding heap allocations is critical
                • Hot paths called frequently
                
                Use Task when:
                • Method usually completes asynchronously
                • Result needs to be awaited multiple times
                • Interoperating with existing Task-based APIs
                • Debugging and tooling support needed
                """);
            
            // ============ VALUETASK<T> RESTRICTIONS ============
            Console.WriteLine("\n=== 3. ValueTask<T> Restrictions ===");
            
            async ValueTask<int> GetNumberAsync()
            {
                await Task.Delay(100);
                return 42;
            }
            
            var valueTask = GetNumberAsync();
            
            Console.WriteLine("""
                ValueTask restrictions:
                • Can only be awaited once
                • Should not be used with Task.WhenAll/WhenAny
                • Not for long-term storage (convert to Task if needed)
                • .AsTask() converts to regular Task
                """);
            
            // Convert to Task if needed for multiple awaits
            var task = valueTask.AsTask();
            var result1 = await task;
            var result2 = await task; // Can await multiple times
            
            // ============ VALUETASK POOLING ============
            Console.WriteLine("\n=== 4. ValueTask Pooling ===");
            
            // Using IValueTaskSource for advanced pooling (C# 7.0+)
            class PooledValueTaskSource : System.Threading.Tasks.Sources.IValueTaskSource<int>
            {
                private int _result;
                private short _version;
                private System.Threading.Tasks.Sources.ValueTaskSourceStatus _status;
                
                public void SetResult(int result)
                {
                    _result = result;
                    _status = System.Threading.Tasks.Sources.ValueTaskSourceStatus.Succeeded;
                    _version++;
                }
                
                public int GetResult(short token) => _result;
                public System.Threading.Tasks.Sources.ValueTaskSourceStatus GetStatus(short token) => _status;
                public void OnCompleted(System.Action<object> continuation, object state, short token, 
                    System.Threading.Tasks.Sources.ValueTaskSourceOnCompletedFlags flags) { }
            }
            
            Console.WriteLine("IValueTaskSource enables zero-allocation async methods");
            
            // ============ REAL-WORLD VALUETASK EXAMPLE ============
            Console.WriteLine("\n=== 5. Real-world ValueTask Example ===");
            
            class ConnectionPool
            {
                private readonly Queue<object> _availableConnections = new();
                private readonly List<object> _allConnections = new();
                
                public async ValueTask<object> GetConnectionAsync()
                {
                    // Try to get connection synchronously
                    lock (_availableConnections)
                    {
                        if (_availableConnections.Count > 0)
                            return _availableConnections.Dequeue();
                    }
                    
                    // Create new connection asynchronously
                    await Task.Delay(100); // Simulate connection creation
                    var connection = new object();
                    lock (_allConnections) _allConnections.Add(connection);
                    return connection;
                }
                
                public void ReturnConnection(object connection)
                {
                    lock (_availableConnections)
                        _availableConnections.Enqueue(connection);
                }
            }
            
            var pool = new ConnectionPool();
            var conn = await pool.GetConnectionAsync();
            pool.ReturnConnection(conn);
            Console.WriteLine("Connection pool with ValueTask for fast path");
        }
        
        static async Task DemonstrateAsyncPatterns()
        {
            Console.WriteLine("\n============ ASYNC PATTERNS AND BEST PRACTICES ============\n");
            
            // ============ ASYNC FACTORY PATTERN ============
            Console.WriteLine("=== 1. Async Factory Pattern ===");
            
            class DatabaseConnection
            {
                private DatabaseConnection() { }
                
                public static async Task<DatabaseConnection> CreateAsync(string connectionString)
                {
                    var connection = new DatabaseConnection();
                    await connection.InitializeAsync(connectionString);
                    return connection;
                }
                
                private async Task InitializeAsync(string connectionString)
                {
                    Console.WriteLine($"Initializing connection: {connectionString}");
                    await Task.Delay(100);
                }
                
                public async Task QueryAsync(string sql)
                {
                    await Task.Delay(50);
                    Console.WriteLine($"Executed: {sql}");
                }
            }
            
            var db = await DatabaseConnection.CreateAsync("Server=localhost");
            await db.QueryAsync("SELECT * FROM Users");
            
            // ============ ASYNC LAZY INITIALIZATION ============
            Console.WriteLine("\n=== 2. Async Lazy Initialization ===");
            
            class AsyncLazy<T>
            {
                private readonly Func<Task<T>> _factory;
                private Lazy<Task<T>> _lazy;
                
                public AsyncLazy(Func<Task<T>> factory)
                {
                    _factory = factory;
                    _lazy = new Lazy<Task<T>>(_factory);
                }
                
                public Task<T> Value => _lazy.Value;
                
                public void Reset()
                {
                    lock (this)
                    {
                        _lazy = new Lazy<Task<T>>(_factory);
                    }
                }
            }
            
            var lazyConfig = new AsyncLazy<Dictionary<string, string>>(async () =>
            {
                Console.WriteLine("Loading configuration...");
                await Task.Delay(200);
                return new Dictionary<string, string> { { "key", "value" } };
            });
            
            var config = await lazyConfig.Value; // First call loads
            var config2 = await lazyConfig.Value; // Returns cached
            
            // ============ ASYNC DISPOSABLE ============
            Console.WriteLine("\n=== 3. Async Disposable (C# 8.0+) ===");
            
            class AsyncResource : IAsyncDisposable
            {
                public async ValueTask DisposeAsync()
                {
                    Console.WriteLine("Disposing async resource...");
                    await Task.Delay(100); // Simulate async cleanup
                    Console.WriteLine("Async disposal complete");
                }
                
                public async Task UseAsync()
                {
                    Console.WriteLine("Using resource...");
                    await Task.Delay(50);
                }
            }
            
            await using (var resource = new AsyncResource())
            {
                await resource.UseAsync();
            } // Automatically calls DisposeAsync
            
            // ============ ASYNC LOCK PATTERN ============
            Console.WriteLine("\n=== 4. Async Lock Pattern ===");
            
            class AsyncLock
            {
                private readonly SemaphoreSlim _semaphore = new(1, 1);
                
                public async Task<IDisposable> LockAsync()
                {
                    await _semaphore.WaitAsync();
                    return new Releaser(_semaphore);
                }
                
                private class Releaser : IDisposable
                {
                    private readonly SemaphoreSlim _semaphore;
                    public Releaser(SemaphoreSlim semaphore) => _semaphore = semaphore;
                    public void Dispose() => _semaphore.Release();
                }
            }
            
            var asyncLock = new AsyncLock();
            var sharedResource = 0;
            
            async Task IncrementWithLockAsync()
            {
                using (await asyncLock.LockAsync())
                {
                    await Task.Delay(10);
                    sharedResource++;
                    Console.WriteLine($"Shared resource: {sharedResource}");
                }
            }
            
            var lockTasks = Enumerable.Range(1, 5)
                .Select(_ => IncrementWithLockAsync());
            await Task.WhenAll(lockTasks);
            
            // ============ ASYNC PRODUCER-CONSUMER ============
            Console.WriteLine("\n=== 5. Async Producer-Consumer ===");
            
            class AsyncQueue<T>
            {
                private readonly Queue<T> _queue = new();
                private readonly SemaphoreSlim _semaphore = new(0);
                
                public void Enqueue(T item)
                {
                    lock (_queue) _queue.Enqueue(item);
                    _semaphore.Release();
                }
                
                public async Task<T> DequeueAsync(CancellationToken cancellationToken = default)
                {
                    await _semaphore.WaitAsync(cancellationToken);
                    lock (_queue) return _queue.Dequeue();
                }
            }
            
            var queue = new AsyncQueue<int>();
            var producer = Task.Run(async () =>
            {
                for (int i = 1; i <= 3; i++)
                {
                    await Task.Delay(100);
                    queue.Enqueue(i);
                    Console.WriteLine($"Produced: {i}");
                }
            });
            
            var consumer = Task.Run(async () =>
            {
                for (int i = 1; i <= 3; i++)
                {
                    var item = await queue.DequeueAsync();
                    Console.WriteLine($"Consumed: {item}");
                }
            });
            
            await Task.WhenAll(producer, consumer);
            
            // ============ ASYNC BEST PRACTICES ============
            Console.WriteLine("\n=== 6. Async Best Practices ===");
            
            Console.WriteLine("""
                Async/Await Best Practices:
                
                1. Use async/await all the way up/down the call stack
                2. Avoid async void (except event handlers)
                3. Use ConfigureAwait(false) in library code
                4. Name async methods with "Async" suffix
                5. Handle exceptions properly
                6. Use cancellation tokens
                7. Avoid mixing sync and async code
                8. Don't block on async code (.Result, .Wait())
                9. Consider ValueTask for hot paths
                10. Profile and measure performance
                
                Common Pitfalls:
                • Deadlocks from blocking on async code
                • Unobserved exceptions in fire-and-forget
                • Async without await (missing await keyword)
                • Not passing cancellation tokens
                • Excessive parallelism without throttling
                """);
        }
        
        static async Task DemonstrateAsyncWithLinq()
        {
            Console.WriteLine("\n============ ASYNC WITH LINQ ============\n");
            
            // ============ ASYNC LINQ EXTENSIONS ============
            Console.WriteLine("=== 1. Async LINQ Extensions ===");
            
            // Note: Requires System.Linq.Async NuGet package for full support
            static async Task<List<int>> ProcessNumbersAsync(IEnumerable<int> numbers)
            {
                var results = new List<int>();
                
                foreach (var number in numbers)
                {
                    var processed = await ProcessSingleAsync(number);
                    results.Add(processed);
                }
                
                return results;
            }
            
            static async Task<int> ProcessSingleAsync(int number)
            {
                await Task.Delay(10);
                return number * 2;
            }
            
            var numbers = Enumerable.Range(1, 5);
            var processed = await ProcessNumbersAsync(numbers);
            Console.WriteLine($"Processed numbers: {string.Join(", ", processed)}");
            
            // ============ ASYNC SELECT (PROJECTION) ============
            Console.WriteLine("\n=== 2. Async Select (Projection) ===");
            
            async Task<IEnumerable<string>> SelectAsync(IEnumerable<int> source)
            {
                var tasks = source.Select(async x =>
                {
                    await Task.Delay(10);
                    return $"Number: {x}";
                });
                
                return await Task.WhenAll(tasks);
            }
            
            var selected = await SelectAsync(new[] { 1, 2, 3 });
            Console.WriteLine($"Selected: {string.Join(", ", selected)}");
            
            // ============ ASYNC WHERE (FILTERING) ============
            Console.WriteLine("\n=== 3. Async Where (Filtering) ===");
            
            async Task<IEnumerable<int>> WhereAsync(IEnumerable<int> source)
            {
                var tasks = source.Select(async x => 
                    (Value: x, Keep: await ShouldKeepAsync(x)));
                
                var results = await Task.WhenAll(tasks);
                return results.Where(r => r.Keep).Select(r => r.Value);
            }
            
            static async Task<bool> ShouldKeepAsync(int value)
            {
                await Task.Delay(10);
                return value % 2 == 0;
            }
            
            var filtered = await WhereAsync(new[] { 1, 2, 3, 4, 5 });
            Console.WriteLine($"Filtered (evens): {string.Join(", ", filtered)}");
            
            // ============ ASYNC AGGREGATION ============
            Console.WriteLine("\n=== 4. Async Aggregation ===");
            
            async Task<int> SumAsync(IEnumerable<int> source)
            {
                int sum = 0;
                foreach (var item in source)
                {
                    await Task.Delay(10);
                    sum += item;
                }
                return sum;
            }
            
            var sum = await SumAsync(new[] { 1, 2, 3, 4, 5 });
            Console.WriteLine($"Async sum: {sum}");
            
            // ============ PARALLEL ASYNC PROCESSING ============
            Console.WriteLine("\n=== 5. Parallel Async Processing ===");
            
            async Task<List<int>> ProcessInParallelAsync(IEnumerable<int> source, int maxConcurrency)
            {
                var semaphore = new SemaphoreSlim(maxConcurrency);
                var tasks = new List<Task<int>>();
                
                foreach (var item in source)
                {
                    await semaphore.WaitAsync();
                    
                    tasks.Add(Task.Run(async () =>
                    {
                        try
                        {
                            return await ProcessSingleAsync(item);
                        }
                        finally
                        {
                            semaphore.Release();
                        }
                    }));
                }
                
                return (await Task.WhenAll(tasks)).ToList();
            }
            
            var parallelResults = await ProcessInParallelAsync(Enumerable.Range(1, 10), 3);
            Console.WriteLine($"Parallel processed (max 3 at a time): {parallelResults.Count} items");
            
            // ============ ASYNC LINQ BEST PRACTICES ============
            Console.WriteLine("\n=== 6. Async LINQ Best Practices ===");
            
            Console.WriteLine("""
                Async LINQ considerations:
                
                1. Be mindful of degree of parallelism
                2. Consider using SemaphoreSlim for throttling
                3. Watch out for Task.WhenAll memory usage
                4. Handle exceptions in individual tasks
                5. Consider System.Linq.Async for better patterns
                6. Use async streams (IAsyncEnumerable) for large datasets
                7. Avoid mixing sync and async enumerations
                8. Cache results if operations are expensive
                """);
        }
        
        static async Task DemonstrateRealWorldScenarios()
        {
            Console.WriteLine("\n============ REAL-WORLD ASYNC SCENARIOS ============\n");
            
            // ============ WEB API CLIENT ============
            Console.WriteLine("=== 1. Web API Client ===");
            
            class ApiClient
            {
                private readonly HttpClient _client;
                
                public ApiClient(HttpClient client)
                {
                    _client = client;
                }
                
                public async Task<string> GetUserDataAsync(int userId, CancellationToken cancellationToken = default)
                {
                    var response = await _client.GetAsync(
                        $"https://api.example.com/users/{userId}",
                        cancellationToken);
                    
                    response.EnsureSuccessStatusCode();
                    return await response.Content.ReadAsStringAsync();
                }
                
                public async Task<string> GetMultipleUsersAsync(IEnumerable<int> userIds, CancellationToken cancellationToken = default)
                {
                    var tasks = userIds.Select(id => GetUserDataAsync(id, cancellationToken));
                    var results = await Task.WhenAll(tasks);
                    return string.Join(", ", results);
                }
            }
            
            Console.WriteLine("API client with cancellation support");
            
            // ============ DATABASE OPERATIONS ============
            Console.WriteLine("\n=== 2. Database Operations ===");
            
            class UserRepository
            {
                public async Task<User> GetUserAsync(int id, CancellationToken cancellationToken = default)
                {
                    // Simulate database call
                    await Task.Delay(100, cancellationToken);
                    return new User(id, $"User{id}");
                }
                
                public async Task<List<User>> GetUsersAsync(IEnumerable<int> ids, CancellationToken cancellationToken = default)
                {
                    var tasks = ids.Select(id => GetUserAsync(id, cancellationToken));
                    return (await Task.WhenAll(tasks)).ToList();
                }
                
                public async IAsyncEnumerable<User> StreamUsersAsync(CancellationToken cancellationToken = default)
                {
                    for (int i = 1; i <= 5; i++)
                    {
                        await Task.Delay(50, cancellationToken);
                        yield return new User(i, $"StreamedUser{i}");
                    }
                }
            }
            
            var repo = new UserRepository();
            var user = await repo.GetUserAsync(1);
            Console.WriteLine($"User: {user.Name}");
            
            // ============ FILE PROCESSING ============
            Console.WriteLine("\n=== 3. File Processing ===");
            
            async Task ProcessFilesAsync(string directory, CancellationToken cancellationToken = default)
            {
                var files = Directory.GetFiles(directory);
                
                // Process files in parallel with throttling
                var semaphore = new SemaphoreSlim(5); // Max 5 concurrent
                var tasks = files.Select(async file =>
                {
                    await semaphore.WaitAsync(cancellationToken);
                    try
                    {
                        using var stream = new FileStream(file, FileMode.Open, FileAccess.Read, FileShare.Read, 4096, FileOptions.Asynchronous);
                        var buffer = new byte[1024];
                        var bytesRead = await stream.ReadAsync(buffer, 0, buffer.Length, cancellationToken);
                        Console.WriteLine($"Processed {Path.GetFileName(file)}: {bytesRead} bytes");
                    }
                    finally
                    {
                        semaphore.Release();
                    }
                });
                
                await Task.WhenAll(tasks);
            }
            
            Console.WriteLine("Async file processing with concurrency limit");
            
            // ============ REAL-TIME DATA PROCESSING ============
            Console.WriteLine("\n=== 4. Real-time Data Processing ===");
            
            class DataProcessor
            {
                private readonly Channel<DataItem> _channel;
                
                public DataProcessor()
                {
                    _channel = Channel.CreateUnbounded<DataItem>();
                }
                
                public async Task ProduceDataAsync(CancellationToken cancellationToken)
                {
                    var random = new Random();
                    while (!cancellationToken.IsCancellationRequested)
                    {
                        var item = new DataItem(DateTime.Now, random.NextDouble());
                        await _channel.Writer.WriteAsync(item, cancellationToken);
                        await Task.Delay(100, cancellationToken);
                    }
                    _channel.Writer.Complete();
                }
                
                public async Task ConsumeDataAsync(CancellationToken cancellationToken)
                {
                    await foreach (var item in _channel.Reader.ReadAllAsync(cancellationToken))
                    {
                        Console.WriteLine($"Processed: {item.Timestamp:HH:mm:ss} - {item.Value:F2}");
                    }
                }
            }
            
            // ============ ASYNC INITIALIZATION ============
            Console.WriteLine("\n=== 5. Async Initialization ===");
            
            class Application
            {
                private readonly Task _initializationTask;
                
                public Application()
                {
                    _initializationTask = InitializeAsync();
                }
                
                private async Task InitializeAsync()
                {
                    Console.WriteLine("Initializing application...");
                    await Task.Delay(200); // Simulate initialization
                    Console.WriteLine("Application initialized");
                }
                
                public async Task RunAsync()
                {
                    await _initializationTask; // Wait for initialization
                    Console.WriteLine("Running application...");
                }
            }
            
            var app = new Application();
            await app.RunAsync();
            
            // ============ ASYNC TESTING ============
            Console.WriteLine("\n=== 6. Async Testing ===");
            
            Console.WriteLine("""
                Async testing considerations:
                
                1. Use async test methods in xUnit/NUnit
                2. Test cancellation behavior
                3. Test timeout scenarios
                4. Mock async dependencies properly
                5. Use TaskCompletionSource for controlled testing
                6. Test exception propagation
                7. Consider using Microsoft.Reactive.Testing for complex async
                
                Example test pattern:
                [Fact]
                public async Task SomeMethodAsync_WhenCalled_ReturnsExpected()
                {
                    // Arrange
                    var sut = new SomeService();
                    
                    // Act
                    var result = await sut.SomeMethodAsync();
                    
                    // Assert
                    Assert.Equal(expected, result);
                }
                """);
            
            // ============ SUMMARY ============
            Console.WriteLine("\n=== 7. Summary ===");
            
            Console.WriteLine("""
                Async/Await is essential for modern C# development:
                
                Key Takeaways:
                1. Use async/await for I/O-bound operations
                2. Understand Task vs ValueTask trade-offs
                3. Always handle cancellation properly
                4. Use async streams for data sequences
                5. Follow async patterns and best practices
                6. Test async code thoroughly
                7. Profile performance of async operations
                
                Remember:
                • Async != parallel (though they can be combined)
                • Don't block async code (.Result, .Wait())
                • Use ConfigureAwait(false) in library code
                • Name async methods with Async suffix
                • Handle exceptions in async methods
                """);
        }
        
        // Supporting classes
        class User
        {
            public int Id { get; }
            public string Name { get; }
            
            public User(int id, string name)
            {
                Id = id;
                Name = name;
            }
        }
        
        class DataItem
        {
            public DateTime Timestamp { get; }
            public double Value { get; }
            
            public DataItem(DateTime timestamp, double value)
            {
                Timestamp = timestamp;
                Value = value;
            }
        }
    }
}