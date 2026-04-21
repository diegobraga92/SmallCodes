/*
    C# MEMORY MANAGEMENT
    File: 15_memory_management.cs
    
    Comprehensive guide to memory management in C#.
    Covers value vs reference types, stack vs heap, 
    garbage collection, IDisposable pattern, finalizers,
    memory leaks, performance optimization, and best practices.
*/

using System;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.Collections.Generic;

namespace CSharpRefresher.MemoryManagement
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Memory Management ===\n");
            
            DemonstrateMemoryBasics();
            DemonstrateGarbageCollection();
            DemonstrateDisposePattern();
            DemonstrateMemoryLeaks();
            DemonstratePerformanceOptimization();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateMemoryBasics()
        {
            Console.WriteLine("=== 1. Memory Basics ===\n");
            
            // Value types (stored on stack for local variables)
            Console.WriteLine("Value Types (stack-allocated for locals):");
            int x = 10;               // Stack
            double y = 3.14;          // Stack
            DateTime now = DateTime.Now; // Stack (struct)
            Point p = new Point(5, 10); // Stack (custom struct)
            
            // Reference types (always on heap)
            Console.WriteLine("\nReference Types (heap-allocated):");
            string name = "Alice";    // Heap (string is special)
            object obj = new object(); // Heap
            int[] numbers = new int[1000]; // Heap
            List<string> list = new List<string>(); // Heap
            
            // Struct vs Class memory allocation
            struct Point
            {
                public int X, Y;
                public Point(int x, int y) { X = x; Y = y; }
            }
            
            class Person
            {
                public string Name;
                public int Age;
            }
            
            // Memory layout demonstration
            Console.WriteLine("\nMemory Layout:");
            Console.WriteLine("Stack (fast, automatic cleanup):");
            Console.WriteLine("  • Local value type variables");
            Console.WriteLine("  • Method parameters");
            Console.WriteLine("  • Return addresses");
            
            Console.WriteLine("\nHeap (slower, GC-managed):");
            Console.WriteLine("  • All reference type instances");
            Console.WriteLine("  • Large value types (>16 bytes in arrays)");
            Console.WriteLine("  • Boxed value types");
            
            // Boxing and unboxing
            Console.WriteLine("\nBoxing and Unboxing:");
            int value = 42;
            object boxed = value;     // Boxing (heap allocation)
            int unboxed = (int)boxed; // Unboxing (type check + copy)
            
            Console.WriteLine($"Original: {value}, Boxed: {boxed}, Unboxed: {unboxed}");
            
            // Sizeof and Marshal.SizeOf
            Console.WriteLine("\nType Sizes:");
            Console.WriteLine($"sizeof(int): {sizeof(int)} bytes");
            Console.WriteLine($"sizeof(double): {sizeof(double)} bytes");
            Console.WriteLine($"sizeof(DateTime): {sizeof(DateTime)} bytes");
            Console.WriteLine($"Marshal.SizeOf<Point>(): {Marshal.SizeOf<Point>()} bytes");
        }
        
        static void DemonstrateGarbageCollection()
        {
            Console.WriteLine("\n=== 2. Garbage Collection ===\n");
            
            // GC generations
            Console.WriteLine("GC Generations:");
            Console.WriteLine("""
                Generation 0: Youngest objects, collected most frequently
                Generation 1: Buffer between young and old
                Generation 2: Long-lived objects, collected rarely
                Large Object Heap (LOH): Objects > 85KB
                """);
            
            // GC collection types
            Console.WriteLine("\nGC Collection Types:");
            Console.WriteLine("• Ephemeral (Gen 0/1) - Fast, frequent");
            Console.WriteLine("• Full (Gen 0/1/2) - Slow, comprehensive");
            Console.WriteLine("• Background (concurrent) - Non-blocking");
            Console.WriteLine("• Blocking - Pauses application");
            
            // GC methods
            Console.WriteLine("\nGC Methods:");
            var totalMemory = GC.GetTotalMemory(false);
            Console.WriteLine($"Total memory: {totalMemory:N0} bytes");
            
            var maxGen = GC.MaxGeneration;
            Console.WriteLine($"Max generation: {maxGen}");
            
            var collectionCount0 = GC.CollectionCount(0);
            var collectionCount1 = GC.CollectionCount(1);
            var collectionCount2 = GC.CollectionCount(2);
            Console.WriteLine($"Collections: Gen0={collectionCount0}, Gen1={collectionCount1}, Gen2={collectionCount2}");
            
            // GC modes
            Console.WriteLine("\nGC Modes:");
            Console.WriteLine("• Workstation (default) - Optimized for responsiveness");
            Console.WriteLine("• Server - Optimized for throughput");
            Console.WriteLine("• Concurrent - Allows GC during execution");
            Console.WriteLine("• Non-concurrent - Blocks during GC");
            
            // GC notifications (advanced)
            Console.WriteLine("\nGC Notifications (for critical operations):");
            try
            {
                // Register for GC notification (approaching full collection)
                GC.RegisterForFullGCNotification(10, 10);
                Console.WriteLine("Registered for GC notifications");
            }
            catch (InvalidOperationException)
            {
                Console.WriteLine("GC notifications not supported in this configuration");
            }
            
            // GC latency modes
            Console.WriteLine("\nGC Latency Modes:");
            Console.WriteLine("• Batch (default) - Disables concurrent GC");
            Console.WriteLine("• Interactive - Enables concurrent GC");
            Console.WriteLine("• LowLatency - Temporarily suppresses full GC");
            Console.WriteLine("• SustainedLowLatency - Longer-term suppression");
            Console.WriteLine("• NoGCRegion - Specified region with no GC");
            
            // Setting latency mode example
            var oldMode = GCSettings.LatencyMode;
            GCSettings.LatencyMode = GCLatencyMode.LowLatency;
            Console.WriteLine($"Changed latency mode from {oldMode} to {GCSettings.LatencyMode}");
            GCSettings.LatencyMode = oldMode; // Restore
            
            // GC best practices
            Console.WriteLine("\nGC Best Practices:");
            Console.WriteLine("""
                1. Let GC do its job (avoid premature optimization)
                2. Use value types for small, short-lived data
                3. Avoid unnecessary allocations in hot paths
                4. Use object pooling for frequently created objects
                5. Be careful with finalizers (they keep objects alive longer)
                6. Use WeakReference for caches
                7. Consider array pooling for large arrays
                """);
        }
        
        static void DemonstrateDisposePattern()
        {
            Console.WriteLine("\n=== 3. Dispose Pattern ===\n");
            
            // Simple IDisposable implementation
            class SimpleResource : IDisposable
            {
                private bool _disposed = false;
                private IntPtr _handle;
                
                public SimpleResource()
                {
                    _handle = Marshal.AllocHGlobal(1000);
                    Console.WriteLine("Allocated unmanaged resource");
                }
                
                public void DoWork()
                {
                    if (_disposed)
                        throw new ObjectDisposedException(nameof(SimpleResource));
                    Console.WriteLine("Working with resource...");
                }
                
                public void Dispose()
                {
                    Dispose(true);
                    GC.SuppressFinalize(this);
                }
                
                protected virtual void Dispose(bool disposing)
                {
                    if (!_disposed)
                    {
                        if (disposing)
                        {
                            // Dispose managed resources
                        }
                        
                        // Free unmanaged resources
                        if (_handle != IntPtr.Zero)
                        {
                            Marshal.FreeHGlobal(_handle);
                            _handle = IntPtr.Zero;
                            Console.WriteLine("Freed unmanaged resource");
                        }
                        
                        _disposed = true;
                    }
                }
                
                ~SimpleResource()
                {
                    Dispose(false);
                }
            }
            
            // Using statement (automatic disposal)
            Console.WriteLine("Using statement example:");
            using (var resource = new SimpleResource())
            {
                resource.DoWork();
            } // Dispose called automatically
            
            // Using declaration (C# 8.0+)
            Console.WriteLine("\nUsing declaration example (C# 8.0+):");
            using var resource2 = new SimpleResource();
            resource2.DoWork();
            // Dispose called when variable goes out of scope
            
            // Complex disposable pattern
            class ComplexResource : IDisposable
            {
                private bool _disposed = false;
                private List<IDisposable> _managedResources = new();
                private IntPtr _unmanagedResource;
                
                public ComplexResource()
                {
                    _unmanagedResource = Marshal.AllocHGlobal(500);
                    _managedResources.Add(new MemoryStream());
                }
                
                protected virtual void Dispose(bool disposing)
                {
                    if (!_disposed)
                    {
                        if (disposing)
                        {
                            // Dispose managed resources
                            foreach (var resource in _managedResources)
                            {
                                resource?.Dispose();
                            }
                            _managedResources.Clear();
                        }
                        
                        // Free unmanaged resources
                        if (_unmanagedResource != IntPtr.Zero)
                        {
                            Marshal.FreeHGlobal(_unmanagedResource);
                            _unmanagedResource = IntPtr.Zero;
                        }
                        
                        _disposed = true;
                    }
                }
                
                public void Dispose()
                {
                    Dispose(true);
                    GC.SuppressFinalize(this);
                }
                
                ~ComplexResource()
                {
                    Dispose(false);
                }
            }
            
            // IAsyncDisposable (.NET Core 3.0+)
            Console.WriteLine("\nIAsyncDisposable example:");
            class AsyncResource : IAsyncDisposable, IDisposable
            {
                private MemoryStream _stream = new();
                
                public async ValueTask DisposeAsync()
                {
                    await _stream.DisposeAsync();
                    Dispose(false);
                    GC.SuppressFinalize(this);
                }
                
                public void Dispose()
                {
                    _stream.Dispose();
                    Dispose(false);
                    GC.SuppressFinalize(this);
                }
                
                protected virtual void Dispose(bool disposing)
                {
                    // Cleanup logic
                }
            }
        }
        
        static void DemonstrateMemoryLeaks()
        {
            Console.WriteLine("\n=== 4. Memory Leaks ===\n");
            
            // Common memory leak patterns
            
            // 1. Event handlers
            Console.WriteLine("1. Event Handler Leaks:");
            class Publisher
            {
                public event EventHandler SomethingHappened;
                public void DoSomething() => SomethingHappened?.Invoke(this, EventArgs.Empty);
            }
            
            class Subscriber
            {
                private Publisher _publisher;
                
                public Subscriber(Publisher publisher)
                {
                    _publisher = publisher;
                    _publisher.SomethingHappened += OnSomethingHappened;
                }
                
                private void OnSomethingHappened(object sender, EventArgs e)
                {
                    Console.WriteLine("Event received");
                }
                
                public void Unsubscribe()
                {
                    _publisher.SomethingHappened -= OnSomethingHappened;
                }
            }
            
            // Without unsubscribe, subscriber stays alive
            Console.WriteLine("Fix: Always unsubscribe from events");
            
            // 2. Static references
            Console.WriteLine("\n2. Static Reference Leaks:");
            class Cache
            {
                private static List<byte[]> _cache = new();
                
                public static void Add(byte[] data)
                {
                    _cache.Add(data); // Data never becomes unreachable
                }
                
                public static void Clear()
                {
                    _cache.Clear();
                    _cache.TrimExcess();
                }
            }
            
            Console.WriteLine("Fix: Use WeakReference for caches");
            
            // 3. Thread-local storage
            Console.WriteLine("\n3. Thread-Local Storage Leaks:");
            [ThreadStatic]
            static List<string> _threadLocalData;
            
            Console.WriteLine("Fix: Clean up thread-local data when thread ends");
            
            // 4. Unmanaged resources
            Console.WriteLine("\n4. Unmanaged Resource Leaks:");
            class UnmanagedResource
            {
                private IntPtr _handle;
                
                public UnmanagedResource()
                {
                    _handle = Marshal.AllocHGlobal(1000);
                }
                
                // Missing Dispose/finalizer!
                // Memory leak: _handle never freed
            }
            
            Console.WriteLine("Fix: Always implement IDisposable for unmanaged resources");
            
            // 5. Large Object Heap fragmentation
            Console.WriteLine("\n5. LOH Fragmentation:");
            byte[] large1 = new byte[85000]; // Goes to LOH
            byte[] large2 = new byte[85000]; // Goes to LOH
            
            // If large1 is collected, gap remains in LOH
            large1 = null;
            GC.Collect();
            
            byte[] large3 = new byte[86000]; // Might not fit in gap, causes fragmentation
            
            Console.WriteLine("Fix: Pool large objects or use ArrayPool");
            
            // Detecting memory leaks
            Console.WriteLine("\nDetecting Memory Leaks:");
            Console.WriteLine("• Use Performance Profiler (Visual Studio)");
            Console.WriteLine("• Use dotMemory (JetBrains)");
            Console.WriteLine("• Use BenchmarkDotNet for memory diagnostics");
            Console.WriteLine("• Monitor Process.GetCurrentProcess().WorkingSet64");
            Console.WriteLine("• Use GC.GetTotalMemory() for tracking");
            
            // Memory pressure
            Console.WriteLine("\nMemory Pressure:");
            GC.AddMemoryPressure(1000000); // Tell GC about unmanaged memory
            GC.RemoveMemoryPressure(1000000);
        }
        
        static void DemonstratePerformanceOptimization()
        {
            Console.WriteLine("\n=== 5. Performance Optimization ===\n");
            
            // 1. Reduce allocations
            Console.WriteLine("1. Reduce Allocations:");
            
            // Bad: Creates new string each iteration
            string result = "";
            for (int i = 0; i < 100; i++)
            {
                result += i.ToString(); // Creates new string
            }
            
            // Good: Use StringBuilder
            var sb = new System.Text.StringBuilder();
            for (int i = 0; i < 100; i++)
            {
                sb.Append(i);
            }
            result = sb.ToString();
            
            // 2. Array pooling
            Console.WriteLine("\n2. Array Pooling:");
            var pool = System.Buffers.ArrayPool<byte>.Shared;
            byte[] buffer = pool.Rent(1024);
            try
            {
                // Use buffer
                buffer[0] = 1;
            }
            finally
            {
                pool.Return(buffer);
            }
            
            // 3. Span and Memory for zero-copy operations
            Console.WriteLine("\n3. Span<T> and Memory<T>:");
            byte[] data = new byte[100];
            Span<byte> span = data.AsSpan();
            span.Fill(42); // No allocations
            
            // 4. Struct optimizations
            Console.WriteLine("\n4. Struct Optimizations:");
            
            // Consider struct for small, frequently created objects
            struct SmallData
            {
                public int Id;
                public float Value;
                public bool Flag;
            }
            
            // 5. Object pooling
            Console.WriteLine("\n5. Object Pooling:");
            class ObjectPool<T> where T : new()
            {
                private Stack<T> _pool = new();
                
                public T Rent()
                {
                    lock (_pool)
                    {
                        return _pool.Count > 0 ? _pool.Pop() : new T();
                    }
                }
                
                public void Return(T item)
                {
                    lock (_pool)
                    {
                        _pool.Push(item);
                    }
                }
            }
            
            // 6. Lazy initialization
            Console.WriteLine("\n6. Lazy Initialization:");
            class ExpensiveResource
            {
                private Lazy<byte[]> _data = new Lazy<byte[]>(() =>
                {
                    Console.WriteLine("Creating expensive resource...");
                    return new byte[1000000];
                });
                
                public byte[] Data => _data.Value;
            }
            
            // 7. Weak references for caches
            Console.WriteLine("\n7. Weak References:");
            var weakRef = new WeakReference<byte[]>(new byte[1000]);
            if (weakRef.TryGetTarget(out byte[] cachedData))
            {
                // Use cached data if still in memory
            }
            
            // 8. Memory diagnostics
            Console.WriteLine("\n8. Memory Diagnostics:");
            var process = Process.GetCurrentProcess();
            Console.WriteLine($"Working Set: {process.WorkingSet64:N0} bytes");
            Console.WriteLine($"Private Memory: {process.PrivateMemorySize64:N0} bytes");
            Console.WriteLine($"Virtual Memory: {process.VirtualMemorySize64:N0} bytes");
            
            // 9. GC settings for performance
            Console.WriteLine("\n9. GC Performance Settings:");
            Console.WriteLine("""
                App.config settings for optimal performance:
                
                <configuration>
                  <runtime>
                    <gcServer enabled="true" />  <!-- For server apps -->
                    <gcConcurrent enabled="true" /> <!-- Concurrent GC -->
                    <gcAllowVeryLargeObjects enabled="true" /> <!-- >2GB arrays -->
                  </runtime>
                </configuration>
                """);
            
            Console.WriteLine("\n=== Memory Management Best Practices ===");
            Console.WriteLine("""
                1. Understand value vs reference types
                2. Implement IDisposable correctly for unmanaged resources
                3. Avoid finalizers unless absolutely necessary
                4. Use using statements for deterministic cleanup
                5. Be mindful of event handler subscriptions
                6. Use appropriate collections for your data
                7. Consider memory implications of LINQ queries
                8. Profile memory usage before optimizing
                9. Use ArrayPool for large, temporary arrays
                10. Consider Span<T> for performance-critical code
                
                Remember: The best optimization is often reducing allocations,
                not micro-optimizing existing allocations.
                """);
        }
    }
}