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
            
            /*
                OVERVIEW: CHOOSING THE RIGHT SYNCHRONIZATION PRIMITIVE
                ======================================================
                
                • lock/Monitor: General-purpose, simple, suitable for most cases
                    - Use for: Quick critical sections, single-process scenarios
                    - Performance: Fast (uncontended), moderate (contended)
                    - When NOT to use: Cross-process sync, async/await contexts
                
                • SemaphoreSlim: Limits concurrent access to a resource
                    - Use for: Throttling, rate limiting, resource pools
                    - Has async support (WaitAsync)
                    - Lighter weight than Semaphore
                
                • ReaderWriterLockSlim: Optimizes for many readers, few writers
                    - Use for: Read-heavy scenarios (caches, configuration)
                    - More complex and slower than lock when write-heavy
                
                • Mutex: Cross-process synchronization
                    - Use for: Ensuring single application instance, IPC
                    - Slower than lock (kernel object)
                
                • Interlocked: Lock-free atomic operations
                    - Use for: Simple counters, flags, CAS operations
                    - Fastest option for simple operations
                
                • SpinLock: Busy-waiting for short critical sections
                    - Use for: Very short locks (<100ns) on multi-core systems
                    - DON'T use for I/O or long operations (wastes CPU)
            */
            
            // Lock statement
            Console.WriteLine("1. Lock Statement:");
            
            // Lock is syntactic sugar for Monitor.Enter/Exit
            // It's the most common synchronization primitive for protecting shared state
            // within a single process
            object lockObject = new object();
            int sharedCounter = 0;
            
            // Without lock, this would cause race conditions and incorrect results
            Parallel.For(0, 1000, i =>
            {
                // lock ensures only one thread can execute this block at a time
                // Pros: Simple, reliable, automatic cleanup (even on exceptions)
                // Cons: Blocks threads (no async support), single-process only
                lock (lockObject)
                {
                    sharedCounter++; // Critical section: increment must be atomic
                }
                // Lock is released here automatically
            });
            
            Console.WriteLine($"Counter after lock: {sharedCounter}");
            
            // Monitor (lock statement uses Monitor internally)
            Console.WriteLine("\n2. Monitor Class:");
            
            /*
                MONITOR vs LOCK:
                ===============
                
                lock (obj) { ... } is equivalent to:
                
                bool lockTaken = false;
                try {
                    Monitor.Enter(obj, ref lockTaken);
                    // ... critical section ...
                } finally {
                    if (lockTaken) Monitor.Exit(obj);
                }
                
                WHY USE MONITOR DIRECTLY?
                • Monitor.TryEnter: Non-blocking lock attempt with timeout
                • Monitor.Wait/Pulse: Condition variables for complex coordination
                • More control over lock acquisition/release
                
                WHEN TO USE LOCK INSTEAD:
                • 99% of the time - lock is simpler and safer
                • Use Monitor only when you need TryEnter or Wait/Pulse
            */
            
            var monitorCounter = 0;
            Parallel.For(0, 1000, i =>
            {
                bool lockTaken = false;
                try
                {
                    // Monitor.Enter acquires the lock on lockObject
                    // The lockTaken parameter ensures we only Exit if we successfully entered
                    Monitor.Enter(lockObject, ref lockTaken);
                    monitorCounter++; // Protected critical section
                }
                finally
                {
                    // CRITICAL: Always check lockTaken before calling Exit
                    // Calling Exit without Enter causes SynchronizationLockException
                    if (lockTaken)
                        Monitor.Exit(lockObject);
                }
            });
            
            Console.WriteLine($"Counter with Monitor: {monitorCounter}");
            
            // Mutex (cross-process)
            Console.WriteLine("\n3. Mutex (Cross-Process):");
            
            /*
                MUTEX vs LOCK:
                =============
                
                Mutex:
                • Can synchronize across processes (named mutex)
                • Kernel object (slower than lock)
                • Use for: Single-instance applications, cross-process coordination
                
                Lock/Monitor:
                • Within single process only
                • User-mode object (faster)
                • Use for: All other scenarios
                
                PERFORMANCE COMPARISON:
                • lock:  ~25ns (uncontended), ~100ns (contended)
                • Mutex: ~1000ns (always goes through kernel)
                
                PRACTICAL USE CASES:
                • Mutex: Preventing multiple app instances, file access coordination
                • Lock: Everything else (protecting shared state within app)
            */
            
            // Named mutex for cross-process synchronization
            // "Global\\" prefix makes it visible across all sessions (including services)
            // Use "Local\\" prefix for per-session mutexes
            using (var mutex = new Mutex(false, "Global\\MyAppMutex"))
            {
                // WaitOne attempts to acquire the mutex with a timeout
                // Returns true if acquired, false if timeout expired
                // Timeout prevents deadlock if another process holds it indefinitely
                if (mutex.WaitOne(1000)) // Wait up to 1 second
                {
                    try
                    {
                        Console.WriteLine("Acquired mutex, doing work...");
                        // Only one process can execute this code at a time
                        Thread.Sleep(100);
                    }
                    finally
                    {
                        // CRITICAL: Always release mutex in finally block
                        // Forgetting to release causes abandoned mutex
                        mutex.ReleaseMutex();
                        Console.WriteLine("Released mutex");
                    }
                }
                else
                {
                    // Timeout occurred - another process holds the mutex
                    Console.WriteLine("Could not acquire mutex (timeout)");
                }
            }
            
            // Semaphore and SemaphoreSlim
            Console.WriteLine("\n4. Semaphore/SemaphoreSlim:");
            
            /*
                SEMAPHORE vs SEMAPHORESLIM vs LOCK:
                ===================================
                
                SemaphoreSlim (RECOMMENDED):
                • Lightweight, single-process
                • Supports async/await (WaitAsync)
                • Use for: Rate limiting, throttling, resource pools
                • Example: Limit concurrent HTTP requests to API
                
                Semaphore:
                • Heavier (kernel object)
                • Cross-process capable
                • No async support
                • Use for: Cross-process resource limits
                
                Lock:
                • Binary (0 or 1), not countable
                • No async support
                • Use for: Simple mutual exclusion
                
                WHEN TO USE SEMAPHORESLIM:
                • Limiting concurrent operations (e.g., max 5 concurrent downloads)
                • Throttling API calls (e.g., max 10 requests/second)
                • Managing resource pools (e.g., database connections)
                • Any async scenario requiring controlled concurrency
                
                KEY CONCEPT:
                • initialCount=2, maxCount=2: Allows 2 threads/tasks at once
                • When 2 are inside, others wait until one releases
                • Like a bouncer at a club: "Only 2 people allowed inside"
            */
            
            // Create a semaphore that allows 2 concurrent entries
            // initialCount=2: Start with 2 available slots
            // maxCount=2: Maximum of 2 slots total
            using (var semaphore = new SemaphoreSlim(2, 2)) // Allow 2 concurrent
            {
                var tasks = new Task[5]; // Create 5 tasks competing for 2 slots
                for (int i = 0; i < tasks.Length; i++)
                {
                    int id = i;
                    tasks[i] = Task.Run(async () =>
                    {
                        // WaitAsync: Asynchronously wait for an available slot
                        // This is a KEY ADVANTAGE over lock (which can't await)
                        await semaphore.WaitAsync();
                        try
                        {
                            Console.WriteLine($"Task {id} entered semaphore");
                            // Simulate work: Only 2 tasks will be here at once
                            await Task.Delay(200);
                        }
                        finally
                        {
                            // CRITICAL: Always release in finally block
                            // Release() makes one slot available for waiting tasks
                            semaphore.Release();
                            Console.WriteLine($"Task {id} exited semaphore");
                        }
                    });
                }
                
                // Wait for all 5 tasks to complete
                // Even though 5 tasks run, only 2 execute concurrently at any time
                await Task.WhenAll(tasks);
            }
            
            // ReaderWriterLockSlim
            Console.WriteLine("\n5. ReaderWriterLockSlim:");
            
            /*
                READERWRITERLOCKSLIM vs LOCK:
                =============================
                
                ReaderWriterLockSlim:
                • Optimized for scenarios with MANY reads, FEW writes
                • Allows multiple concurrent readers
                • Writers get exclusive access (blocks all readers and other writers)
                • More complex and slower than lock when write-heavy
                
                Lock:
                • Simple, fast, general-purpose
                • Always exclusive (one thread at a time)
                • Better for balanced read/write scenarios
                
                PERFORMANCE CHARACTERISTICS:
                • Read-heavy (90% reads): ReaderWriterLockSlim wins
                • Write-heavy (50%+ writes): lock is faster
                • Overhead: ~3x slower than lock when uncontended
                
                USE CASES:
                ✓ Configuration/settings caches (frequent reads, rare updates)
                ✓ In-memory lookup tables
                ✓ Shared data structures with < 10% write operations
                ✗ Write-heavy scenarios (use lock instead)
                ✗ Simple mutual exclusion (use lock instead)
                
                RULE OF THUMB:
                If your write ratio > 20%, use lock instead.
            */
            
            var rwLock = new ReaderWriterLockSlim();
            var dictionary = new Dictionary<string, string>();
            
            // Multiple readers can execute concurrently
            // This is the KEY ADVANTAGE: no blocking between readers
            Parallel.For(0, 5, i =>
            {
                // EnterReadLock: Multiple threads can hold read lock simultaneously
                // As long as no writer has the lock
                rwLock.EnterReadLock();
                try
                {
                    Console.WriteLine($"Reader {i} reading");
                    // All 5 readers can be here at the same time
                    // No contention between readers
                }
                finally
                {
                    // Always exit in finally block
                    rwLock.ExitReadLock();
                }
            });
            
            // Single writer gets exclusive access
            // EnterWriteLock: Waits for all readers to finish, then gets exclusive lock
            rwLock.EnterWriteLock();
            try
            {
                Console.WriteLine("Writer writing");
                // No readers or other writers can be here
                // This is the EXCLUSIVE section
                dictionary["key"] = "value";
            }
            finally
            {
                // Release write lock, allowing readers/writers to proceed
                rwLock.ExitWriteLock();
            }
            
            // AutoResetEvent and ManualResetEvent
            Console.WriteLine("\n6. AutoResetEvent/ManualResetEvent:");
            
            /*
                AUTORESETEVENT vs MANUALRESETEVENT:
                ===================================
                
                AutoResetEvent (Turnstile):
                • Set(): Releases ONE waiting thread, then auto-resets to non-signaled
                • Like a turnstile: one person passes, gate closes automatically
                • Use for: Producer-consumer, signaling one specific thread
                
                ManualResetEvent (Gate):
                • Set(): Releases ALL waiting threads, stays signaled until Reset()
                • Like a gate: opens for everyone, stays open until manually closed
                • Use for: Broadcasting to multiple threads, initialization complete signals
                
                WHEN TO USE:
                • AutoReset: "Wake up ONE thread to handle this item"
                • ManualReset: "All threads can now proceed"
                
                MODERN ALTERNATIVES:
                • SemaphoreSlim.WaitAsync() for async scenarios
                • TaskCompletionSource for async signaling
                • async/await patterns in general
                
                NOTE: These are older primitives. Prefer SemaphoreSlim or
                TaskCompletionSource in new code for better async support.
            */
            
            // AutoResetEvent starts in non-signaled state (false)
            var autoEvent = new AutoResetEvent(false);
            
            // Background thread will signal the event after 100ms
            Task.Run(() =>
            {
                Thread.Sleep(100);
                Console.WriteLine("Signaling event");
                // Set() signals the event: releases ONE waiting thread
                // Then AUTOMATICALLY resets to non-signaled
                autoEvent.Set();
            });
            
            Console.WriteLine("Waiting for event...");
            // WaitOne() blocks until event is signaled
            // Once signaled, THIS thread proceeds and event auto-resets
            autoEvent.WaitOne();
            Console.WriteLine("Event received");
            
            // If another thread calls WaitOne() now, it would block
            // because AutoResetEvent has already reset itself
            
            // CountdownEvent
            Console.WriteLine("\n7. CountdownEvent:");
            
            /*
                COUNTDOWNEVENT: Wait for N operations to complete
                =================================================
                
                CONCEPT:
                • Initialize with count N
                • Each task calls Signal() when done (decrements count)
                • Wait() blocks until count reaches 0
                • Like waiting for N workers to finish before proceeding
                
                vs TASK.WHENALL:
                • CountdownEvent: Use when you don't have Task objects
                  (e.g., callbacks, events, non-async operations)
                • Task.WhenAll: Use when you have Task objects (preferred for async)
                
                vs BARRIER:
                • CountdownEvent: One-time coordination (waits for completion)
                • Barrier: Multi-phase coordination (synchronizes at multiple points)
                
                USE CASES:
                ✓ Waiting for N callbacks to complete
                ✓ Initialization where multiple components must be ready
                ✓ Aggregating results from parallel workers
                ✗ Async operations with Task (use Task.WhenAll instead)
            */
            
            // Create a countdown initialized to 3
            // Will reach 0 when Signal() is called 3 times
            using (var countdown = new CountdownEvent(3))
            {
                // Start 3 tasks that will each signal when done
                for (int i = 0; i < 3; i++)
                {
                    int id = i;
                    Task.Run(() =>
                    {
                        // Simulate work of varying duration
                        Thread.Sleep(100 * (id + 1));
                        Console.WriteLine($"Task {id} completed");
                        
                        // Signal() decrements the count by 1
                        // When count reaches 0, Wait() unblocks
                        countdown.Signal();
                    });
                }
                
                // Wait() blocks until count reaches 0
                // (i.e., all 3 tasks have called Signal())
                countdown.Wait();
                Console.WriteLine("All tasks completed");
            }
            
            // Barrier
            Console.WriteLine("\n8. Barrier:");
            
            /*
                BARRIER: Multi-phase parallel algorithm coordination
                ====================================================
                
                CONCEPT:
                • Synchronization point for N threads/tasks
                • All must reach the barrier before ANY can proceed
                • Like a checkpoint in a race: everyone waits for the slowest runner
                • Can have multiple phases (barriers in sequence)
                
                vs COUNTDOWNEVENT:
                • Barrier: Reusable, multi-phase (stays open after reaching)
                • CountdownEvent: One-time use (disposed after reaching 0)
                
                vs TASK.WHENALL:
                • Barrier: For iterative parallel algorithms with phases
                • Task.WhenAll: For waiting on completion of independent tasks
                
                USE CASES:
                ✓ Parallel algorithms with phases (e.g., iterative solvers)
                ✓ Game simulation with turn-based logic
                ✓ Parallel data processing pipelines with checkpoints
                ✓ Benchmarking (synchronize start of all threads)
                
                REAL-WORLD EXAMPLE:
                Parallel matrix calculation where each iteration depends on
                previous iteration's results from all workers.
            */
            
            // Create barrier for 3 participants
            // Post-phase action runs when all participants reach barrier
            var barrier = new Barrier(3, b =>
            {
                // This callback executes after all threads signal
                // but before any proceed to next phase
                Console.WriteLine($"Barrier phase {b.CurrentPhaseNumber} completed");
                // Useful for: aggregating results, logging, cleanup
            });
            
            for (int i = 0; i < 3; i++)
            {
                int id = i;
                Task.Run(() =>
                {
                    // Phase 0: All tasks work independently
                    Console.WriteLine($"Task {id} phase 0");
                    
                    // SignalAndWait(): "I'm done with phase 0"
                    // Blocks until all 3 tasks call SignalAndWait()
                    barrier.SignalAndWait();
                    // At this point, all tasks have completed phase 0
                    
                    // Phase 1: All tasks proceed together
                    Console.WriteLine($"Task {id} phase 1");
                    
                    // Another synchronization point
                    barrier.SignalAndWait();
                    // All tasks have now completed phase 1
                });
            }
            
            Thread.Sleep(500); // Allow barrier to complete
            
            // SpinLock and SpinWait
            Console.WriteLine("\n9. SpinLock/SpinWait:");
            
            /*
                SPINLOCK: Busy-waiting lock for very short critical sections
                ============================================================
                
                HOW IT WORKS:
                • Instead of blocking (context switch), thread "spins" in a loop
                • Keeps checking if lock is available (burns CPU cycles)
                • No kernel transition = faster for SHORT locks (<100 nanoseconds)
                
                vs LOCK (Monitor):
                • SpinLock: Busy-waits (uses CPU), faster for very short sections
                • Lock: Blocks thread (context switch), better for longer sections
                
                WHEN TO USE SPINLOCK:
                ✓ Critical section < 100ns on multi-core systems
                ✓ Lock contention is low
                ✓ You've measured and proven it's faster than lock
                
                WHEN NOT TO USE:
                ✗ I/O operations (will waste CPU spinning)
                ✗ Long critical sections (>1 microsecond)
                ✗ Single-core systems (spinning prevents other threads)
                ✗ Any async operations (never use with await)
                ✗ Unknown workload (use lock instead)
                
                DANGER ZONE:
                • Easy to misuse and harm performance
                • Profile before using!
                • 95% of the time, lock is the right choice
                
                RULE OF THUMB:
                If in doubt, use lock. Only use SpinLock after profiling
                shows lock is a bottleneck AND critical section is tiny.
            */
            
            var spinLock = new SpinLock();
            var spinCounter = 0;
            
            Parallel.For(0, 1000, i =>
            {
                bool lockTaken = false;
                // Enter() spins in a loop until lock is acquired
                // This burns CPU but avoids context switch
                spinLock.Enter(ref lockTaken);
                if (lockTaken)
                {
                    try 
                    { 
                        // CRITICAL: Keep this section TINY
                        // spinCounter++ is ~2ns - perfect for SpinLock
                        // If this were > 100ns, lock would be faster
                        spinCounter++; 
                    }
                    finally 
                    { 
                        // ALWAYS release in finally
                        // Not releasing causes permanent lock
                        spinLock.Exit(); 
                    }
                }
            });
            
            Console.WriteLine($"Counter with SpinLock: {spinCounter}");
            
            // Volatile and Memory barriers
            Console.WriteLine("\n10. Volatile and Memory Barriers:");
            
            /*
                VOLATILE: Prevents compiler/CPU reordering of reads/writes
                ==========================================================
                
                Without volatile:
                • Compiler/CPU can reorder instructions for optimization
                • Thread A: write X=1, Y=1
                • Thread B might see: Y=1, X=0 (reordered by CPU)
                
                With volatile:
                • Reads always see latest value
                • Writes are immediately visible to other threads
                • Prevents reordering around volatile operations
                
                WHEN TO USE:
                ✓ Simple flags (bool shutdown = false)
                ✓ Reference types (object instance = new Foo())
                ✗ Complex operations (use lock or Interlocked instead)
                ✗ Composite operations (i++ requires Interlocked)
                
                MEMORY BARRIER:
                • Full fence: no reordering across this point
                • Heavier than volatile, ensures full memory visibility
            */
            
            volatile int volatileValue = 0;
            // volatile ensures other threads see changes immediately
            
            Thread.MemoryBarrier(); // Ensures reads/writes don't get reordered
            // Acts as a fence: no loads/stores move across this line
            
            // Interlocked operations
            Console.WriteLine("\n11. Interlocked Operations:");
            
            /*
                INTERLOCKED: Lock-free atomic operations
                ========================================
                
                WHAT IS IT:
                • CPU-level atomic operations (compare-and-swap, add, etc.)
                • Lock-free: no blocking, no deadlocks
                • Fastest synchronization primitive
                • Hardware support ensures atomicity
                
                vs LOCK:
                • Interlocked: Lock-free, ~5-10ns, simple operations only
                • Lock: Blocking, ~25-100ns, protects complex operations
                
                AVAILABLE OPERATIONS:
                • Increment/Decrement: i++, i--
                • Add: i += n
                • Exchange: swap values
                • CompareExchange: CAS (compare-and-swap)
                • Read: atomic 64-bit reads on 32-bit systems
                
                WHEN TO USE:
                ✓ Simple counters (hits, requests, errors)
                ✓ Flags (state = 1)
                ✓ Lock-free algorithms (if you know what you're doing)
                
                WHEN NOT TO USE:
                ✗ Complex operations (calculations, multiple vars)
                ✗ When lock is simpler and fast enough
                
                PERFORMANCE:
                Interlocked.Increment: ~5ns
                lock { i++; }: ~25ns (uncontended), ~100ns (contended)
            */
            
            int interlockedCounter = 0;
            Parallel.For(0, 1000, i =>
            {
                // Interlocked.Increment: atomic i++
                // Equivalent to: lock(obj) { interlockedCounter++; }
                // But lock-free and faster
                Interlocked.Increment(ref interlockedCounter);
            });
            
            Console.WriteLine($"Interlocked counter: {interlockedCounter}");
            
            // CompareExchange: atomic compare-and-swap
            // The foundation of lock-free programming
            int compareValue = 0;
            
            // CompareExchange(ref location, newValue, expectedValue)
            // Atomically: if (location == expectedValue) { location = newValue; return expectedValue; }
            // Returns: original value of location
            int original = Interlocked.CompareExchange(ref compareValue, 10, 0);
            // If compareValue was 0, it's now 10, and original = 0
            // If compareValue was NOT 0, it's unchanged, and original = old value
            Console.WriteLine($"CompareExchange: original={original}, new={compareValue}");
            
            /*
                WHY COMPAREEXCHANGE IS POWERFUL:
                • Building block for lock-free data structures
                • Optimistic concurrency: "try to update, retry if someone else did first"
                • Pattern: while (!Interlocked.CompareExchange(ref x, newVal, oldVal)) { }
                • Used internally by: ConcurrentDictionary, ConcurrentQueue, etc.
            */
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