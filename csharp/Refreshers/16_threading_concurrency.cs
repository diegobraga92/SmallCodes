/*
    C# THREADING AND CONCURRENCY
    File: 16_threading_concurrency.cs
    
    Comprehensive guide to threading, parallelism, and concurrency in C#.
    Covers threads, tasks, async/await, synchronization primitives,
    concurrent collections, parallelism patterns, and best practices.
*/

using System;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;
using System.Diagnostics;

namespace CSharpRefresher.ThreadingConcurrency
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Threading and Concurrency ===\n");
            
            DemonstrateThreadBasics();
            DemonstrateTaskParallelism();
            DemonstrateAsyncAwaitPatterns();
            DemonstrateSynchronization();
            DemonstrateConcurrentCollections();
            DemonstrateParallelProgramming();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateThreadBasics()
        {
            Console.WriteLine("=== 1. Thread Basics ===\n");
            
            // Creating and starting threads
            Console.WriteLine("1. Creating Threads:");
            
            void ThreadWork()
            {
                Console.WriteLine($"Thread {Thread.CurrentThread.ManagedThreadId} is working");
                Thread.Sleep(1000);
                Console.WriteLine($"Thread {Thread.CurrentThread.ManagedThreadId} completed");
            }
            
            var thread1 = new Thread(ThreadWork);
            var thread2 = new Thread(ThreadWork);
            
            thread1.Start();
            thread2.Start();
            
            thread1.Join();
            thread2.Join();
            
            // Thread parameters
            Console.WriteLine("\n2. Thread with Parameters:");
            
            void ParameterizedWork(object data)
            {
                int count = (int)data;
                for (int i = 0; i < count; i++)
                {
                    Console.WriteLine($"Processing item {i} on thread {Thread.CurrentThread.ManagedThreadId}");
                }
            }
            
            var paramThread = new Thread(ParameterizedWork);
            paramThread.Start(3);
            paramThread.Join();
            
            // Thread properties
            Console.WriteLine("\n3. Thread Properties:");
            var currentThread = Thread.CurrentThread;
            Console.WriteLine($"Current Thread ID: {currentThread.ManagedThreadId}");
            Console.WriteLine($"Thread Name: {currentThread.Name ?? "(unnamed)"}");
            Console.WriteLine($"Thread State: {currentThread.ThreadState}");
            Console.WriteLine($"Is Background: {currentThread.IsBackground}");
            Console.WriteLine($"Priority: {currentThread.Priority}");
            
            // Thread pool
            Console.WriteLine("\n4. Thread Pool:");
            Console.WriteLine($"ThreadPool Threads: {ThreadPool.ThreadCount}");
            Console.WriteLine($"Completed Work Items: {ThreadPool.CompletedWorkItemCount}");
            Console.WriteLine($"Pending Work Items: {ThreadPool.PendingWorkItemCount}");
            
            ThreadPool.QueueUserWorkItem(state =>
            {
                Console.WriteLine($"ThreadPool thread {Thread.CurrentThread.ManagedThreadId} executing");
            });
            
            // Background vs foreground threads
            Console.WriteLine("\n5. Background vs Foreground Threads:");
            var foregroundThread = new Thread(() =>
            {
                Console.WriteLine("Foreground thread running");
                Thread.Sleep(2000);
                Console.WriteLine("Foreground thread completed");
            });
            
            var backgroundThread = new Thread(() =>
            {
                Console.WriteLine("Background thread running");
                Thread.Sleep(2000);
                Console.WriteLine("Background thread completed");
            })
            { IsBackground = true };
            
            foregroundThread.Start();
            backgroundThread.Start();
            
            // Foreground thread keeps app alive, background doesn't
            Console.WriteLine("Main thread exiting - background thread may not complete");
            
            // Thread exceptions
            Console.WriteLine("\n6. Thread Exception Handling:");
            var exceptionThread = new Thread(() =>
            {
                try
                {
                    throw new InvalidOperationException("Thread exception");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Caught in thread: {ex.Message}");
                }
            });
            
            exceptionThread.Start();
            exceptionThread.Join();
            
            // Thread-local storage
            Console.WriteLine("\n7. Thread-Local Storage:");
            
            ThreadLocal<int> threadLocalValue = new ThreadLocal<int>(() => 42);
            
            var t1 = new Thread(() =>
            {
                threadLocalValue.Value = 100;
                Console.WriteLine($"Thread 1 value: {threadLocalValue.Value}");
            });
            
            var t2 = new Thread(() =>
            {
                threadLocalValue.Value = 200;
                Console.WriteLine($"Thread 2 value: {threadLocalValue.Value}");
            });
            
            t1.Start();
            t2.Start();
            t1.Join();
            t2.Join();
            
            Console.WriteLine($"Main thread value: {threadLocalValue.Value}");
        }
        
        static void DemonstrateTaskParallelism()
        {
            Console.WriteLine("\n=== 2. Task Parallelism ===\n");
            
            // Creating and starting tasks
            Console.WriteLine("1. Task Creation:");
            
            var task1 = Task.Run(() =>
            {
                Console.WriteLine($"Task {Task.CurrentId} running");
                return 42;
            });
            
            var task2 = new Task<int>(() =>
            {
                Console.WriteLine($"Task {Task.CurrentId} running");
                return 100;
            });
            task2.Start();
            
            task1.Wait();
            task2.Wait();
            Console.WriteLine($"Results: {task1.Result}, {task2.Result}");
            
            // Task continuation
            Console.WriteLine("\n2. Task Continuation:");
            
            Task.Run(() => "Hello")
                .ContinueWith(t => t.Result + " World")
                .ContinueWith(t => t.Result + "!")
                .ContinueWith(t => Console.WriteLine($"Result: {t.Result}"))
                .Wait();
            
            // Task with different continuation options
            var parentTask = Task.Run(() =>
            {
                Console.WriteLine("Parent task");
                throw new Exception("Parent failed");
            });
            
            var successContinuation = parentTask.ContinueWith(t =>
                Console.WriteLine("Success continuation (won't run)"),
                TaskContinuationOptions.OnlyOnRanToCompletion);
            
            var faultedContinuation = parentTask.ContinueWith(t =>
                Console.WriteLine($"Faulted: {t.Exception?.Message}"),
                TaskContinuationOptions.OnlyOnFaulted);
            
            try { faultedContinuation.Wait(); } catch { }
            
            // Task cancellation
            Console.WriteLine("\n3. Task Cancellation:");
            
            var cts = new CancellationTokenSource();
            var token = cts.Token;
            
            var cancellableTask = Task.Run(() =>
            {
                for (int i = 0; i < 10; i++)
                {
                    if (token.IsCancellationRequested)
                    {
                        Console.WriteLine("Cancellation requested");
                        token.ThrowIfCancellationRequested();
                    }
                    Thread.Sleep(100);
                    Console.WriteLine($"Working... {i}");
                }
            }, token);
            
            cts.CancelAfter(300);
            
            try
            {
                cancellableTask.Wait();
            }
            catch (AggregateException ex)
            {
                Console.WriteLine($"Task cancelled: {ex.InnerException?.GetType().Name}");
            }
            
            // Task status
            Console.WriteLine("\n4. Task Status:");
            var statusTask = Task.Run(() => Thread.Sleep(100));
            Console.WriteLine($"Status before start: {statusTask.Status}");
            Thread.Sleep(50);
            Console.WriteLine($"Status during execution: {statusTask.Status}");
            statusTask.Wait();
            Console.WriteLine($"Status after completion: {statusTask.Status}");
            
            // Task factory
            Console.WriteLine("\n5. Task Factory:");
            var factory = new TaskFactory(TaskCreationOptions.LongRunning, 
                                         TaskContinuationOptions.ExecuteSynchronously);
            
            var factoryTask = factory.StartNew(() =>
            {
                Console.WriteLine($"Factory task {Task.CurrentId} (LongRunning)");
            });
            
            factoryTask.Wait();
            
            // Task completion source (manual task completion)
            Console.WriteLine("\n6. TaskCompletionSource:");
            var tcs = new TaskCompletionSource<int>();
            
            var manualTask = tcs.Task;
            Task.Run(() =>
            {
                Thread.Sleep(500);
                tcs.SetResult(999);
            });
            
            Console.WriteLine($"Manual task result: {manualTask.Result}");
            
            // Task.WaitAll and Task.WaitAny
            Console.WriteLine("\n7. Task.WaitAll / Task.WaitAny:");
            
            var tasks = new Task[3];
            for (int i = 0; i < tasks.Length; i++)
            {
                int id = i;
                tasks[i] = Task.Run(() =>
                {
                    Thread.Sleep(100 * (id + 1));
                    Console.WriteLine($"Task {id} completed");
                });
            }
            
            Task.WaitAll(tasks);
            Console.WriteLine("All tasks completed");
            
            // Task.FromResult for cached/completed tasks
            Console.WriteLine("\n8. Task.FromResult:");
            var completedTask = Task.FromResult("Pre-computed result");
            Console.WriteLine($"Completed task result: {completedTask.Result}");
        }
        
        static void DemonstrateAsyncAwaitPatterns()
        {
            Console.WriteLine("\n=== 3. Async/Await Patterns ===\n");
            
            // Basic async method
            async Task<string> DownloadDataAsync()
            {
                Console.WriteLine("Starting download...");
                await Task.Delay(1000); // Simulate network delay
                Console.WriteLine("Download completed");
                return "Sample data";
            }
            
            Console.WriteLine("1. Basic Async/Await:");
            var dataTask = DownloadDataAsync();
            Console.WriteLine("Main thread continues while downloading...");
            var data = dataTask.Result; // Blocking wait (for demo)
            Console.WriteLine($"Received: {data}");
            
            // Async method with cancellation
            async Task<string> DownloadWithCancellationAsync(CancellationToken token)
            {
                for (int i = 0; i < 10; i++)
                {
                    token.ThrowIfCancellationRequested();
                    await Task.Delay(100);
                }
                return "Data";
            }
            
            Console.WriteLine("\n2. Async with Cancellation:");
            var cts = new CancellationTokenSource();
            cts.CancelAfter(300);
            
            try
            {
                var result = await DownloadWithCancellationAsync(cts.Token);
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Download cancelled");
            }
            
            // Async streams (C# 8.0+)
            async IAsyncEnumerable<int> GenerateNumbersAsync()
            {
                for (int i = 1; i <= 5; i++)
                {
                    await Task.Delay(100);
                    yield return i;
                }
            }
            
            Console.WriteLine("\n3. Async Streams (C# 8.0+):");
            await foreach (var number in GenerateNumbersAsync())
            {
                Console.WriteLine($"Received: {number}");
            }
            
            // ValueTask for performance
            async ValueTask<int> ComputeValueAsync(bool useCache)
            {
                if (useCache)
                    return 42; // Synchronous completion
                
                await Task.Delay(100); // Asynchronous path
                return 100;
            }
            
            Console.WriteLine("\n4. ValueTask for Performance:");
            var fastResult = await ComputeValueAsync(true); // No allocation
            var slowResult = await ComputeValueAsync(false); // Allocates Task
            Console.WriteLine($"Results: {fastResult}, {slowResult}");
            
            // ConfigureAwait
            Console.WriteLine("\n5. ConfigureAwait:");
            
            async Task ConfigureAwaitExample()
            {
                // In library code, use ConfigureAwait(false) to avoid deadlocks
                await Task.Delay(100).ConfigureAwait(false);
                // Not on original context (UI thread) anymore
                Console.WriteLine("Continuing on thread pool thread");
                
                // If you need UI context, don't use ConfigureAwait(false)
                // await Task.Delay(100); // Will return to UI context
            }
            
            await ConfigureAwaitExample();
            
            // Async void (avoid when possible)
            Console.WriteLine("\n6. Async Void (Caution):");
            
            async void AsyncVoidMethod()
            {
                try
                {
                    await Task.Delay(100);
                    throw new Exception("Async void exception");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Caught in async void: {ex.Message}");
                }
            }
            
            AsyncVoidMethod();
            await Task.Delay(200); // Give time for async void to complete
            
            // Task.WhenAll and Task.WhenAny
            Console.WriteLine("\n7. Task.WhenAll / Task.WhenAny:");
            
            async Task<int> AsyncOperation(int id, int delay)
            {
                await Task.Delay(delay);
                Console.WriteLine($"Operation {id} completed");
                return id * 10;
            }
            
            var whenAllTask = Task.WhenAll(
                AsyncOperation(1, 300),
                AsyncOperation(2, 100),
                AsyncOperation(3, 200)
            );
            
            var results = await whenAllTask;
            Console.WriteLine($"WhenAll results: [{string.Join(", ", results)}]");
            
            var whenAnyTask = Task.WhenAny(
                Task.Delay(300),
                Task.Delay(100),
                Task.Delay(200)
            );
            
            var completed = await whenAnyTask;
            Console.WriteLine($"WhenAny: First task completed");
        }
        
        static void DemonstrateSynchronization()
        {
            Console.WriteLine("\n=== 4. Synchronization Primitives ===\n");
            
            // Lock statement
            Console.WriteLine("1. Lock Statement:");
            
            object lockObject = new object();
            int sharedCounter = 0;
            
            Parallel.For(0, 1000, i =>
            {
                lock (lockObject)
                {
                    sharedCounter++;
                }
            });
            
            Console.WriteLine($"Counter after lock: {sharedCounter}");
            
            // Monitor (lock statement uses Monitor internally)
            Console.WriteLine("\n2. Monitor Class:");
            
            var monitorCounter = 0;
            Parallel.For(0, 1000, i =>
            {
                bool lockTaken = false;
                try
                {
                    Monitor.Enter(lockObject, ref lockTaken);
                    monitorCounter++;
                }
                finally
                {
                    if (lockTaken)
                        Monitor.Exit(lockObject);
                }
            });
            
            Console.WriteLine($"Counter with Monitor: {monitorCounter}");
            
            // Mutex (cross-process)
            Console.WriteLine("\n3. Mutex (Cross-Process):");
            
            using (var mutex = new Mutex(false, "Global\\MyAppMutex"))
            {
                if (mutex.WaitOne(1000))
                {
                    try
                    {
                        Console.WriteLine("Acquired mutex, doing work...");
                        Thread.Sleep(100);
                    }
                    finally
                    {
                        mutex.ReleaseMutex();
                        Console.WriteLine("Released mutex");
                    }
                }
            }
            
            // Semaphore and SemaphoreSlim
            Console.WriteLine("\n4. Semaphore/SemaphoreSlim:");
            
            using (var semaphore = new SemaphoreSlim(2, 2)) // Allow 2 concurrent
            {
                var tasks = new Task[5];
                for (int i = 0; i < tasks.Length; i++)
                {
                    int id = i;
                    tasks[i] = Task.Run(async () =>
                    {
                        await semaphore.WaitAsync();
                        try
                        {
                            Console.WriteLine($"Task {id} entered semaphore");
                            await Task.Delay(200);
                        }
                        finally
                        {
                            semaphore.Release();
                            Console.WriteLine($"Task {id} exited semaphore");
                        }
                    });
                }
                
                await Task.WhenAll(tasks);
            }
            
            // ReaderWriterLockSlim
            Console.WriteLine("\n5. ReaderWriterLockSlim:");
            
            var rwLock = new ReaderWriterLockSlim();
            var dictionary = new Dictionary<string, string>();
            
            // Multiple readers
            Parallel.For(0, 5, i =>
            {
                rwLock.EnterReadLock();
                try
                {
                    Console.WriteLine($"Reader {i} reading");
                }
                finally
                {
                    rwLock.ExitReadLock();
                }
            });
            
            // Single writer
            rwLock.EnterWriteLock();
            try
            {
                Console.WriteLine("Writer writing");
                dictionary["key"] = "value";
            }
            finally
            {
                rwLock.ExitWriteLock();
            }
            
            // AutoResetEvent and ManualResetEvent
            Console.WriteLine("\n6. AutoResetEvent/ManualResetEvent:");
            
            var autoEvent = new AutoResetEvent(false);
            
            Task.Run(() =>
            {
                Thread.Sleep(100);
                Console.WriteLine("Signaling event");
                autoEvent.Set();
            });
            
            Console.WriteLine("Waiting for event...");
            autoEvent.WaitOne();
            Console.WriteLine("Event received");
            
            // CountdownEvent
            Console.WriteLine("\n7. CountdownEvent:");
            
            using (var countdown = new CountdownEvent(3))
            {
                for (int i = 0; i < 3; i++)
                {
                    int id = i;
                    Task.Run(() =>
                    {
                        Thread.Sleep(100 * (id + 1));
                        Console.WriteLine($"Task {id} completed");
                        countdown.Signal();
                    });
                }
                
                countdown.Wait();
                Console.WriteLine("All tasks completed");
            }
            
            // Barrier
            Console.WriteLine("\n8. Barrier:");
            
            var barrier = new Barrier(3, b =>
            {
                Console.WriteLine($"Barrier phase {b.CurrentPhaseNumber} completed");
            });
            
            for (int i = 0; i < 3; i++)
            {
                int id = i;
                Task.Run(() =>
                {
                    Console.WriteLine($"Task {id} phase 0");
                    barrier.SignalAndWait();
                    
                    Console.WriteLine($"Task {id} phase 1");
                    barrier.SignalAndWait();
                });
            }
            
            Thread.Sleep(500); // Allow barrier to complete
            
            // SpinLock and SpinWait
            Console.WriteLine("\n9. SpinLock/SpinWait:");
            
            var spinLock = new SpinLock();
            var spinCounter = 0;
            
            Parallel.For(0, 1000, i =>
            {
                bool lockTaken = false;
                spinLock.Enter(ref lockTaken);
                if (lockTaken)
                {
                    try { spinCounter++; }
                    finally { spinLock.Exit(); }
                }
            });
            
            Console.WriteLine($"Counter with SpinLock: {spinCounter}");
            
            // Volatile and Memory barriers
            Console.WriteLine("\n10. Volatile and Memory Barriers:");
            
            volatile int volatileValue = 0;
            Thread.MemoryBarrier(); // Ensures reads/writes don't get reordered
            
            // Interlocked operations
            Console.WriteLine("\n11. Interlocked Operations:");
            
            int interlockedCounter = 0;
            Parallel.For(0, 1000, i =>
            {
                Interlocked.Increment(ref interlockedCounter);
            });
            
            Console.WriteLine($"Interlocked counter: {interlockedCounter}");
            
            // Compare exchange example
            int compareValue = 0;
            int original = Interlocked.CompareExchange(ref compareValue, 10, 0);
            Console.WriteLine($"CompareExchange: original={original}, new={compareValue}");
        }
        
        static void DemonstrateConcurrentCollections()
        {
            Console.WriteLine("\n=== 5. Concurrent Collections ===\n");
            
            // ConcurrentDictionary
            Console.WriteLine("1. ConcurrentDictionary:");
            var concurrentDict = new ConcurrentDictionary<string, int>();
            
            Parallel.For(0, 1000, i =>
            {
                concurrentDict.AddOrUpdate("key",
                    key => 1,
                    (key, oldValue) => oldValue + 1);
            });
            
            Console.WriteLine($"Dictionary value: {concurrentDict["key"]}");
            
            // ConcurrentQueue
            Console.WriteLine("\n2. ConcurrentQueue:");
            var concurrentQueue = new ConcurrentQueue<int>();
            
            Parallel.For(0, 100, i => concurrentQueue.Enqueue(i));
            
            int count = 0;
            while (concurrentQueue.TryDequeue(out int item))
            {
                count++;
            }
            Console.WriteLine($"Dequeued {count} items");
            
            // ConcurrentStack
            Console.WriteLine("\n3. ConcurrentStack:");
            var concurrentStack = new ConcurrentStack<int>();
            
            Parallel.For(0, 100, i => concurrentStack.Push(i));
            
            var items = new int[100];
            concurrentStack.TryPopRange(items);
            Console.WriteLine($"Popped {items.Length} items");
            
            // ConcurrentBag
            Console.WriteLine("\n4. ConcurrentBag:");
            var concurrentBag = new ConcurrentBag<int>();
            
            Parallel.For(0, 100, i => concurrentBag.Add(i));
            
            int bagCount = 0;
            while (concurrentBag.TryTake(out int item))
            {
                bagCount++;
            }
            Console.WriteLine($"Took {bagCount} items from bag");
            
            // BlockingCollection (bounded/unbounded)
            Console.WriteLine("\n5. BlockingCollection:");
            
            using (var blockingCollection = new BlockingCollection<int>(boundedCapacity: 10))
            {
                // Producer
                var producer = Task.Run(() =>
                {
                    for (int i = 0; i < 20; i++)
                    {
                        blockingCollection.Add(i);
                        Console.WriteLine($"Produced: {i}");
                        Thread.Sleep(50);
                    }
                    blockingCollection.CompleteAdding();
                });
                
                // Consumer
                var consumer = Task.Run(() =>
                {
                    foreach (var item in blockingCollection.GetConsumingEnumerable())
                    {
                        Console.WriteLine($"Consumed: {item}");
                        Thread.Sleep(100);
                    }
                });
                
                Task.WaitAll(producer, consumer);
                Console.WriteLine("Producer/Consumer completed");
            }
            
            // Producer/Consumer with multiple producers/consumers
            Console.WriteLine("\n6. Multiple Producers/Consumers:");
            
            using (var bc = new BlockingCollection<int>())
            {
                // Multiple producers
                var producers = Enumerable.Range(0, 3)
                    .Select(i => Task.Run(() =>
                    {
                        for (int j = 0; j < 5; j++)
                        {
                            bc.Add(i * 100 + j);
                        }
                    })).ToArray();
                
                // Multiple consumers
                var consumers = Enumerable.Range(0, 2)
                    .Select(i => Task.Run(() =>
                    {
                        foreach (var item in bc.GetConsumingEnumerable())
                        {
                            Console.WriteLine($"Consumer {i} got: {item}");
                        }
                    })).ToArray();
                
                Task.WaitAll(producers);
                bc.CompleteAdding();
                Task.WaitAll(consumers);
            }
        }
        
        static void DemonstrateParallelProgramming()
        {
            Console.WriteLine("\n=== 6. Parallel Programming ===\n");
            
            // Parallel.For
            Console.WriteLine("1. Parallel.For:");
            var forResults = new int[10];
            
            Parallel.For(0, 10, i =>
            {
                forResults[i] = i * i;
                Console.WriteLine($"Parallel.For iteration {i} on thread {Thread.CurrentThread.ManagedThreadId}");
            });
            
            Console.WriteLine($"Results: [{string.Join(", ", forResults)}]");
            
            // Parallel.ForEach
            Console.WriteLine("\n2. Parallel.ForEach:");
            var data = Enumerable.Range(1, 10).ToList();
            var foreachResults = new int[10];
            
            Parallel.ForEach(data, (item, state, index) =>
            {
                foreachResults[index] = item * 2;
                Console.WriteLine($"Processing {item} on thread {Thread.CurrentThread.ManagedThreadId}");
            });
            
            Console.WriteLine($"Results: [{string.Join(", ", foreachResults)}]");
            
            // Parallel LINQ (PLINQ)
            Console.WriteLine("\n3. Parallel LINQ (PLINQ):");
            
            var numbers = Enumerable.Range(1, 1000000);
            
            var plinqResult = numbers.AsParallel()
                .Where(n => n % 2 == 0)
                .Select(n => n * n)
                .OrderBy(n => n) // Ordering forces merging
                .Take(10)
                .ToList();
            
            Console.WriteLine($"PLINQ results: [{string.Join(", ", plinqResult)}]");
            
            // PLINQ options
            Console.WriteLine("\n4. PLINQ Options:");
            
            var parallelOptions = new ParallelOptions
            {
                MaxDegreeOfParallelism = Environment.ProcessorCount / 2,
                CancellationToken = CancellationToken.None
            };
            
            var customPlinq = numbers.AsParallel()
                .WithDegreeOfParallelism(2)
                .WithExecutionMode(ParallelExecutionMode.ForceParallelism)
                .WithMergeOptions(ParallelMergeOptions.NotBuffered)
                .Where(n => n % 3 == 0)
                .Take(5)
                .ToList();
            
            Console.WriteLine($"Custom PLINQ: [{string.Join(", ", customPlinq)}]");
            
            // Parallel.Invoke
            Console.WriteLine("\n5. Parallel.Invoke:");
            
            Parallel.Invoke(
                () => Console.WriteLine("Action 1"),
                () => Console.WriteLine("Action 2"),
                () => Console.WriteLine("Action 3")
            );
            
            // Task Parallel Library (TPL) Dataflow (if available)
            Console.WriteLine("\n6. TPL Dataflow Concepts:");
            Console.WriteLine("""
                For complex pipelines, consider TPL Dataflow:
                • TransformBlock: Processes input and produces output
                • ActionBlock: Executes action for each input
                • BufferBlock: Buffers data between blocks
                • BroadcastBlock: Broadcasts to multiple targets
                • JoinBlock: Joins multiple sources
                
                Install: System.Threading.Tasks.Dataflow NuGet package
                """);
            
            // Cancellation and exception handling in parallel loops
            Console.WriteLine("\n7. Cancellation in Parallel Loops:");
            
            var parallelCts = new CancellationTokenSource();
            parallelCts.CancelAfter(100);
            
            try
            {
                Parallel.For(0, 100, new ParallelOptions
                {
                    CancellationToken = parallelCts.Token
                }, i =>
                {
                    Thread.Sleep(10);
                    Console.WriteLine($"Iteration {i}");
                });
            }
            catch (OperationCanceledException)
            {
                Console.WriteLine("Parallel loop cancelled");
            }
            
            // Thread affinity and UI threads
            Console.WriteLine("\n8. Thread Affinity Considerations:");
            Console.WriteLine("""
                Important for UI applications:
                • UI controls require specific thread (UI thread)
                • Use Dispatcher.Invoke (WPF) or Control.Invoke (WinForms)
                • In async methods, await returns to original context
                • Use ConfigureAwait(false) in library code
                • Use TaskScheduler.FromCurrentSynchronizationContext()
                """);
            
            Console.WriteLine("\n=== Concurrency Best Practices ===");
            Console.WriteLine("""
                1. Prefer async/await over raw threads for I/O operations
                2. Use Task.Run for CPU-bound work
                3. Avoid async void methods (except event handlers)
                4. Use ConfigureAwait(false) in library code
                5. Understand synchronization primitives and their costs
                6. Use concurrent collections for shared data
                7. Be careful with thread-local storage
                8. Monitor thread pool usage
                9. Consider cancellation support for long operations
                10. Test concurrency scenarios thoroughly
                11. Use profiling tools to find bottlenecks
                12. Understand memory barriers and volatile semantics
                
                Remember: Concurrency bugs are often subtle and hard to reproduce.
                Write thread-safe code from the start, not as an afterthought.
                """);
        }
    }
}