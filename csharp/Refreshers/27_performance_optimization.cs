/*
    C# PERFORMANCE OPTIMIZATION
    File: 27_performance_optimization.cs
    
    Comprehensive guide to performance optimization in C# and .NET applications.
    Covers profiling, memory management, algorithms, data structures, I/O optimization,
    concurrency, caching, database optimization, and real-world performance patterns.
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;
using System.IO;
using System.Threading;
using System.Buffers;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;

namespace CSharpRefresher.PerformanceOptimization
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Performance Optimization ===\n");
            
            DemonstratePerformanceFundamentals();
            DemonstrateProfilingAndMeasurement();
            DemonstrateMemoryOptimization();
            DemonstrateAlgorithmOptimization();
            DemonstrateIOOptimization();
            DemonstrateConcurrencyOptimization();
            DemonstrateCachingStrategies();
            DemonstrateDatabaseOptimization();
            DemonstrateRealWorldOptimizations();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstratePerformanceFundamentals()
        {
            Console.WriteLine("=== 1. Performance Fundamentals ===\n");
            
            // 1. Performance vs scalability
            Console.WriteLine("1. Performance vs Scalability:");
            Console.WriteLine("""
                Performance: How fast a single operation executes
                • Response time, throughput, latency
                • Measured in milliseconds, requests per second
                
                Scalability: How well a system handles increased load
                • Horizontal scaling (adding more machines)
                • Vertical scaling (adding more resources to a machine)
                • Measured in capacity, concurrent users
                
                Trade-offs:
                • Time vs space (CPU vs memory)
                • Read vs write optimization
                • Consistency vs availability (CAP theorem)
                • Development time vs runtime performance
                """);
            
            // 2. Big O notation and algorithm analysis
            Console.WriteLine("\n2. Big O Notation and Algorithm Analysis:");
            Console.WriteLine("""
                Common time complexities:
                • O(1): Constant time - Best
                • O(log n): Logarithmic - Excellent
                • O(n): Linear - Good
                • O(n log n): Linearithmic - Acceptable
                • O(n²): Quadratic - Poor
                • O(2ⁿ): Exponential - Terrible
                • O(n!): Factorial - Unusable for large n
                
                Space complexity:
                // Example: O(1) space
                int SumArray(int[] arr)
                {
                    int sum = 0;
                    for (int i = 0; i < arr.Length; i++)
                    {
                        sum += arr[i];
                    }
                    return sum;
                }
                
                // Example: O(n) space
                int[] CopyAndReverse(int[] arr)
                {
                    int[] result = new int[arr.Length];
                    for (int i = 0; i < arr.Length; i++)
                    {
                        result[arr.Length - 1 - i] = arr[i];
                    }
                    return result;
                }
                
                Amortized analysis:
                // List<T> resizing: O(1) amortized time
                // Doubles capacity when full: O(n) copy, but happens rarely
                """);
            
            // 3. Performance measurement concepts
            Console.WriteLine("\n3. Performance Measurement Concepts:");
            Console.WriteLine("""
                Key metrics:
                • Latency: Time to complete a single operation
                • Throughput: Operations per unit time
                • Resource utilization: CPU, memory, disk, network
                • Response time: Time from request to response
                • Turnaround time: Total time for a task
                • Wait time: Time spent waiting for resources
                
                Measurement principles:
                • Measure in production-like environments
                • Use statistical significance (multiple runs)
                • Account for warm-up (JIT compilation, cache population)
                • Use percentiles (P50, P90, P95, P99, P99.9)
                • Consider both average and worst-case scenarios
                
                Performance testing types:
                • Load testing: Normal expected load
                • Stress testing: Beyond normal capacity
                • Soak testing: Long duration to find memory leaks
                • Spike testing: Sudden load increases
                • Scalability testing: Increasing load to find limits
                """);
        }
        
        static void DemonstrateProfilingAndMeasurement()
        {
            Console.WriteLine("\n=== 2. Profiling and Measurement ===\n");
            
            // 1. Benchmarking with BenchmarkDotNet
            Console.WriteLine("1. Benchmarking with BenchmarkDotNet:");
            Console.WriteLine("""
                // Install-Package BenchmarkDotNet
                
                [MemoryDiagnoser]
                [RankColumn]
                public class StringConcatenationBenchmark
                {
                    private string[] data;
                    
                    [GlobalSetup]
                    public void Setup()
                    {
                        data = Enumerable.Range(1, 1000)
                            .Select(i => $"Item {i}")
                            .ToArray();
                    }
                    
                    [Benchmark(Baseline = true)]
                    public string StringConcatenation()
                    {
                        string result = "";
                        foreach (var item in data)
                        {
                            result += item + ", ";
                        }
                        return result;
                    }
                    
                    [Benchmark]
                    public string StringBuilder()
                    {
                        var sb = new StringBuilder();
                        foreach (var item in data)
                        {
                            sb.Append(item).Append(", ");
                        }
                        return sb.ToString();
                    }
                    
                    [Benchmark]
                    public string StringJoin()
                    {
                        return string.Join(", ", data);
                    }
                }
                
                // Run in Main
                var summary = BenchmarkRunner.Run<StringConcatenationBenchmark>();
                
                Key attributes:
                • [MemoryDiagnoser]: Reports memory allocation
                • [RankColumn]: Ranks methods by performance
                • [Benchmark]: Marks a benchmark method
                • [GlobalSetup]: Runs once before all benchmarks
                • [GlobalCleanup]: Runs once after all benchmarks
                • [IterationSetup]: Runs before each iteration
                • [IterationCleanup]: Runs after each iteration
                """);
            
            // 2. Profiling tools
            Console.WriteLine("\n2. Profiling Tools:");
            Console.WriteLine("""
                Visual Studio Diagnostic Tools:
                • CPU Usage: Hot paths, expensive methods
                • Memory Usage: Allocations, GC pressure
                • Performance Profiler: Instrumentation, sampling
                
                dotnet-counters:
                // Monitor live metrics
                dotnet-counters monitor --process-id 1234
                dotnet-counters monitor --process-id 1234 System.Runtime
                
                dotnet-trace:
                // Collect traces
                dotnet-trace collect --process-id 1234
                dotnet-trace collect --process-id 1234 --profile cpu-sampling
                
                dotnet-dump:
                // Collect and analyze dumps
                dotnet-dump collect --process-id 1234
                dotnet-dump analyze core_20240101.dmp
                
                PerfView:
                • Windows performance analysis tool
                • Low-overhead sampling profiler
                • GC analysis, JIT information
                
                JetBrains dotTrace, dotMemory:
                • Commercial profiling tools
                • Timeline profiling, memory traffic
                • SQL queries, async profiling
                """);
            
            // 3. Performance counters and metrics
            Console.WriteLine("\n3. Performance Counters and Metrics:");
            Console.WriteLine("""
                Key .NET counters:
                • % Time in GC: Percentage of CPU time spent garbage collecting
                • Gen 0/1/2 Collections: GC generation collections
                • Allocated Bytes/sec: Memory allocation rate
                • CPU Usage: Process CPU utilization
                • Working Set: Physical memory used
                • Exception Count: Exceptions thrown per second
                
                Custom metrics with System.Diagnostics:
                public class PerformanceMetrics
                {
                    private readonly Counter _requestsPerSecond;
                    private readonly Counter _averageResponseTime;
                    private readonly Gauge _activeConnections;
                    
                    public PerformanceMetrics()
                    {
                        var meter = new Meter("MyApp.Performance");
                        
                        _requestsPerSecond = meter.CreateCounter<int>(
                            "requests_per_second",
                            description: "Number of requests per second");
                        
                        _averageResponseTime = meter.CreateCounter<double>(
                            "average_response_time_ms",
                            description: "Average response time in milliseconds");
                        
                        _activeConnections = meter.CreateObservableGauge<int>(
                            "active_connections",
                            () => GetActiveConnections(),
                            description: "Number of active connections");
                    }
                    
                    public void RecordRequest(TimeSpan duration)
                    {
                        _requestsPerSecond.Add(1);
                        _averageResponseTime.Add(duration.TotalMilliseconds);
                    }
                }
                
                Application Insights / OpenTelemetry:
                // Distributed tracing, metrics collection
                // Correlation IDs, dependency tracking
                """);
        }
        
        static void DemonstrateMemoryOptimization()
        {
            Console.WriteLine("\n=== 3. Memory Optimization ===\n");
            
            // 1. Garbage collection optimization
            Console.WriteLine("1. Garbage Collection Optimization:");
            Console.WriteLine("""
                GC generations:
                • Gen 0: Short-lived objects (collected frequently)
                • Gen 1: Buffer between Gen 0 and Gen 2
                • Gen 2: Long-lived objects (collected infrequently)
                • LOH (Large Object Heap): Objects > 85KB
                
                GC modes:
                • Workstation GC: Optimized for UI responsiveness
                • Server GC: Optimized for throughput (multiple cores)
                • Concurrent GC: Minimizes pauses (Workstation only)
                • Background GC: Gen 2 collection doesn't block Gen 0/1
                
                GC configuration:
                // In csproj or runtimeconfig.json
                <PropertyGroup>
                  <ServerGarbageCollection>true</ServerGarbageCollection>
                  <ConcurrentGarbageCollection>true</ConcurrentGarbageCollection>
                  <TieredCompilation>true</TieredCompilation>
                </PropertyGroup>
                
                // Or in runtimeconfig.json
                {
                  "runtimeOptions": {
                    "configProperties": {
                      "System.GC.Server": true,
                      "System.GC.Concurrent": true,
                      "System.GC.RetainVM": true
                    }
                  }
                }
                
                Reducing GC pressure:
                • Pool objects (ArrayPool<T>, MemoryPool<T>)
                • Use structs for small, short-lived data
                • Avoid large object allocations (> 85KB)
                • Implement IDisposable for unmanaged resources
                • Use StringBuilder for string concatenation
                • Reuse collections with Clear() instead of new
                """);
            
            // 2. ArrayPool and MemoryPool
            Console.WriteLine("\n2. ArrayPool and MemoryPool:");
            Console.WriteLine("""
                ArrayPool<T> for array pooling:
                public class ArrayPoolExample
                {
                    public void ProcessData(byte[] input)
                    {
                        // Rent array from pool
                        var pool = ArrayPool<byte>.Shared;
                        byte[] buffer = pool.Rent(1024);
                        
                        try
                        {
                            // Use buffer
                            Array.Copy(input, buffer, Math.Min(input.Length, 1024));
                            ProcessBuffer(buffer);
                        }
                        finally
                        {
                            // Return to pool
                            pool.Return(buffer, clearArray: false);
                        }
                    }
                    
                    private void ProcessBuffer(byte[] buffer)
                    {
                        // Process data
                    }
                }
                
                MemoryPool<T> for memory pooling:
                public class MemoryPoolExample
                {
                    public async Task ProcessStreamAsync(Stream stream)
                    {
                        var pool = MemoryPool<byte>.Shared;
                        using (var memory = pool.Rent(4096))
                        {
                            Memory<byte> buffer = memory.Memory;
                            
                            int bytesRead;
                            while ((bytesRead = await stream.ReadAsync(buffer)) > 0)
                            {
                                ProcessChunk(buffer.Slice(0, bytesRead));
                            }
                        }
                    }
                    
                    private void ProcessChunk(Memory<byte> chunk)
                    {
                        // Process memory chunk
                    }
                }
                
                Benefits:
                • Reduces GC pressure
                • Reuses allocated memory
                • Improves performance for frequent allocations
                • Thread-safe (shared pool)
                
                When to use:
                • Frequent allocation of temporary arrays/buffers
                • Network I/O, file I/O buffers
                • Image processing, data transformation
                """);
            
            // 3. Span<T> and Memory<T>
            Console.WriteLine("\n3. Span<T> and Memory<T>:");
            Console.WriteLine("""
                Span<T> for stack allocation:
                public unsafe void ProcessWithSpan(byte[] data)
                {
                    // Stack allocation (no heap allocation)
                    Span<byte> buffer = stackalloc byte[256];
                    
                    // Copy data to span
                    data.AsSpan(0, Math.Min(data.Length, 256)).CopyTo(buffer);
                    
                    // Process span
                    for (int i = 0; i < buffer.Length; i++)
                    {
                        buffer[i] = (byte)(buffer[i] ^ 0xFF); // Invert bits
                    }
                }
                
                Memory<T> for async operations:
                public async Task ProcessAsync(Memory<byte> memory)
                {
                    // Memory<T> can cross async boundaries
                    await ProcessChunkAsync(memory);
                    
                    // Slice without allocation
                    Memory<byte> firstHalf = memory.Slice(0, memory.Length / 2);
                    Memory<byte> secondHalf = memory.Slice(memory.Length / 2);
                    
                    await Task.WhenAll(
                        ProcessChunkAsync(firstHalf),
                        ProcessChunkAsync(secondHalf)
                    );
                }
                
                Benefits:
                • Zero-copy operations
                • Stack allocation possible
                • Unified API for arrays, strings, native memory
                • Performance comparable to unsafe code
                
                Common patterns:
                • Parsing without allocations
                • String manipulation
                • Network protocol handling
                • Image/signal processing
                """);
            
            // 4. Struct vs class optimization
            Console.WriteLine("\n4. Struct vs Class Optimization:");
            Console.WriteLine("""
                When to use structs:
                • Size < 16 bytes (generally)
                • Short-lived, immutable data
                • Value semantics needed
                • Frequent allocation/deallocation
                • Data is copied rather than referenced
                
                When to use classes:
                • Size > 16 bytes
                • Long-lived objects
                • Reference semantics needed
                • Inheritance required
                • Identity matters (reference equality)
                
                Readonly structs:
                public readonly struct Point3D
                {
                    public readonly double X;
                    public readonly double Y;
                    public readonly double Z;
                    
                    public Point3D(double x, double y, double z)
                    {
                        X = x;
                        Y = y;
                        Z = z;
                    }
                    
                    public double DistanceTo(Point3D other)
                    {
                        double dx = X - other.X;
                        double dy = Y - other.Y;
                        double dz = Z - other.Z;
                        return Math.Sqrt(dx * dx + dy * dy + dz * dz);
                    }
                }
                
                Benefits:
                • No heap allocation (stack or inline)
                • Better cache locality
                • No GC pressure
                • Defensive copying prevents mutation
                
                Ref structs (stack-only):
                public ref struct StackOnlyBuffer
                {
                    private Span<byte> _buffer;
                    
                    public StackOnlyBuffer(Span<byte> buffer)
                    {
                        _buffer = buffer;
                    }
                    
                    // Cannot be boxed or used in async methods
                }
                """);
            
            // 5. String optimization
            Console.WriteLine("\n5. String Optimization:");
            Console.WriteLine("""
                String interning:
                // Runtime maintains intern pool
                string s1 = "Hello";
                string s2 = "Hello";
                Console.WriteLine(ReferenceEquals(s1, s2)); // True
                
                string s3 = new string('A', 10);
                string s4 = string.Intern(s3); // Add to intern pool
                
                StringBuilder for concatenation:
                // BAD: O(n²) time, many allocations
                string result = "";
                for (int i = 0; i < 1000; i++)
                {
                    result += "item " + i + ", ";
                }
                
                // GOOD: O(n) time, single allocation
                var sb = new StringBuilder();
                for (int i = 0; i < 1000; i++)
                {
                    sb.Append("item ").Append(i).Append(", ");
                }
                string result = sb.ToString();
                
                String.Create for complex formatting:
                public static string FormatName(string firstName, string lastName)
                {
                    return string.Create(
                        firstName.Length + lastName.Length + 1,
                        (firstName, lastName),
                        (span, state) =>
                        {
                            state.firstName.AsSpan().CopyTo(span);
                            span[state.firstName.Length] = ' ';
                            state.lastName.AsSpan().CopyTo(span.Slice(state.firstName.Length + 1));
                        });
                }
                
                ReadOnlySpan<char> for parsing:
                public static int ParseInt(ReadOnlySpan<char> span)
                {
                    int result = 0;
                    for (int i = 0; i < span.Length; i++)
                    {
                        char c = span[i];
                        if (c >= '0' && c <= '9')
                        {
                            result = result * 10 + (c - '0');
                        }
                    }
                    return result;
                }
                
                // Usage
                string input = "Price: 12345";
                int value = ParseInt(input.AsSpan(7)); // "12345"
                """);
        }
        
        static void DemonstrateAlgorithmOptimization()
        {
            Console.WriteLine("\n=== 4. Algorithm Optimization ===\n");
            
            // 1. Data structure selection
            Console.WriteLine("1. Data Structure Selection:");
            Console.WriteLine("""
                Collection performance characteristics:
                
                List<T>:
                • O(1) indexed access
                • O(1) amortized add (end)
                • O(n) insert/remove (middle)
                • Good for random access, iteration
                
                LinkedList<T>:
                • O(1) insert/remove (known position)
                • O(n) search
                • Good for frequent insertions/deletions
                • Poor cache locality
                
                Dictionary<TKey, TValue>:
                • O(1) average case lookup/insert/delete
                • O(n) worst case (hash collisions)
                • Memory overhead for buckets
                • Good for key-value lookups
                
                HashSet<T>:
                • O(1) average case lookup/insert/delete
                • Unique elements only
                • Good for membership testing
                
                SortedDictionary<TKey, TValue>:
                • O(log n) lookup/insert/delete
                • Maintains sorted order
                • Red-black tree implementation
                
                SortedSet<T>:
                • O(log n) operations
                • Sorted unique elements
                
                Queue<T>, Stack<T>:
                • O(1) enqueue/dequeue, push/pop
                • FIFO/LIFO semantics
                
                Choosing the right collection:
                • Frequent lookups by key: Dictionary/HashSet
                • Frequent iteration: List/Array
                • Frequent insertion/deletion: LinkedList
                • Need sorted data: SortedDictionary/SortedSet
                • Need FIFO/LIFO: Queue/Stack
                """);
            
            // 2. Algorithm optimization patterns
            Console.WriteLine("\n2. Algorithm Optimization Patterns:");
            Console.WriteLine("""
                Memoization (caching):
                public class FibonacciMemoized
                {
                    private readonly Dictionary<int, long> _cache = new();
                    
                    public long Calculate(int n)
                    {
                        if (n <= 1) return n;
                        
                        if (_cache.TryGetValue(n, out var cached))
                            return cached;
                        
                        long result = Calculate(n - 1) + Calculate(n - 2);
                        _cache[n] = result;
                        return result;
                    }
                }
                
                Dynamic programming:
                public class LongestCommonSubsequence
                {
                    public int LcsLength(string x, string y)
                    {
                        int m = x.Length;
                        int n = y.Length;
                        int[,] dp = new int[m + 1, n + 1];
                        
                        for (int i = 1; i <= m; i++)
                        {
                            for (int j = 1; j <= n; j++)
                            {
                                if (x[i - 1] == y[j - 1])
                                {
                                    dp[i, j] = dp[i - 1, j - 1] + 1;
                                }
                                else
                                {
                                    dp[i, j] = Math.Max(dp[i - 1, j], dp[i, j - 1]);
                                }
                            }
                        }
                        
                        return dp[m, n];
                    }
                }
                
                Two-pointer technique:
                public static bool HasPairWithSum(int[] arr, int targetSum)
                {
                    Array.Sort(arr); // O(n log n)
                    
                    int left = 0;
                    int right = arr.Length - 1;
                    
                    while (left < right)
                    {
                        int sum = arr[left] + arr[right];
                        
                        if (sum == targetSum)
                            return true;
                        else if (sum < targetSum)
                            left++;
                        else
                            right--;
                    }
                    
                    return false;
                }
                
                Sliding window:
                public static int MaxSumSubarray(int[] arr, int k)
                {
                    if (arr.Length < k) return 0;
                    
                    // Calculate first window
                    int maxSum = 0;
                    for (int i = 0; i < k; i++)
                    {
                        maxSum += arr[i];
                    }
                    
                    // Slide window
                    int windowSum = maxSum;
                    for (int i = k; i < arr.Length; i++)
                    {
                        windowSum += arr[i] - arr[i - k];
                        maxSum = Math.Max(maxSum, windowSum);
                    }
                    
                    return maxSum;
                }
                """);
            
            // 3. Sorting algorithm selection
            Console.WriteLine("\n3. Sorting Algorithm Selection:");
            Console.WriteLine("""
                Built-in Array.Sort and List.Sort:
                • Uses IntroSort (hybrid of QuickSort, HeapSort, InsertionSort)
                • O(n log n) average case
                • O(n²) worst case (rare)
                • In-place, unstable for value types, stable for reference types
                
                LINQ OrderBy:
                • Stable sort
                • O(n log n) worst case
                • Creates new sequence (not in-place)
                • Uses deferred execution
                
                When to use custom sorting:
                • Special data characteristics (mostly sorted, small range)
                • Need specific algorithm (stable, in-place)
                • Parallel sorting for large datasets
                • External sorting (data doesn't fit in memory)
                
                Counting sort for small integer ranges:
                public static void CountingSort(int[] arr, int maxValue)
                {
                    int[] count = new int[maxValue + 1];
                    
                    // Count occurrences
                    foreach (int value in arr)
                    {
                        count[value]++;
                    }
                    
                    // Reconstruct sorted array
                    int index = 0;
                    for (int value = 0; value <= maxValue; value++)
                    {
                        while (count[value] > 0)
                        {
                            arr[index++] = value;
                            count[value]--;
                        }
                    }
                }
                
                TimSort (Python's default):
                • Hybrid of MergeSort and InsertionSort
                • Stable, adaptive, O(n log n) worst case
                • Good for real-world data (partially ordered)
                """);
            
            // 4. Search algorithm optimization
            Console.WriteLine("\n4. Search Algorithm Optimization:");
            Console.WriteLine("""
                Binary search:
                public static int BinarySearch(int[] arr, int target)
                {
                    int left = 0;
                    int right = arr.Length - 1;
                    
                    while (left <= right)
                    {
                        int mid = left + (right - left) / 2; // Avoid overflow
                        
                        if (arr[mid] == target)
                            return mid;
                        else if (arr[mid] < target)
                            left = mid + 1;
                        else
                            right = mid - 1;
                    }
                    
                    return -1;
                }
                
                Interpolation search (uniformly distributed data):
                public static int InterpolationSearch(int[] arr, int target)
                {
                    int low = 0;
                    int high = arr.Length - 1;
                    
                    while (low <= high && target >= arr[low] && target <= arr[high])
                    {
                        if (low == high)
                        {
                            if (arr[low] == target) return low;
                            return -1;
                        }
                        
                        // Formula for position
                        int pos = low + ((target - arr[low]) * (high - low)) 
                                            / (arr[high] - arr[low]);
                        
                        if (arr[pos] == target)
                            return pos;
                        else if (arr[pos] < target)
                            low = pos + 1;
                        else
                            high = pos - 1;
                    }
                    
                    return -1;
                }
                
                Bloom filters (probabilistic membership):
                // Install-Package Microsoft.AspNetCore.Blazor
                public class BloomFilter
                {
                    private readonly bool[] _bits;
                    private readonly Func<string, int>[] _hashFunctions;
                    
                    public BloomFilter(int size, int hashCount)
                    {
                        _bits = new bool[size];
                        _hashFunctions = new Func<string, int>[hashCount];
                        
                        var rng = new Random();
                        for (int i = 0; i < hashCount; i++)
                        {
                            int seed = rng.Next();
                            _hashFunctions[i] = s => Math.Abs(s.GetHashCode() ^ seed) % size;
                        }
                    }
                    
                    public void Add(string item)
                    {
                        foreach (var hash in _hashFunctions)
                        {
                            _bits[hash(item)] = true;
                        }
                    }
                    
                    public bool MightContain(string item)
                    {
                        foreach (var hash in _hashFunctions)
                        {
                            if (!_bits[hash(item)])
                                return false;
                        }
                        return true;
                    }
                }
                """);
        }
        
        static void DemonstrateIOOptimization()
        {
            Console.WriteLine("\n=== 5. I/O Optimization ===\n");
            
            // 1. File I/O optimization
            Console.WriteLine("1. File I/O Optimization:");
            Console.WriteLine("""
                Buffered streams:
                // BAD: Many small reads
                using (var fs = new FileStream("largefile.bin", FileMode.Open))
                {
                    byte[] buffer = new byte[1];
                    for (int i = 0; i < 1000000; i++)
                    {
                        fs.Read(buffer, 0, 1); // Expensive!
                    }
                }
                
                // GOOD: Buffered reads
                using (var fs = new FileStream("largefile.bin", FileMode.Open))
                using (var bs = new BufferedStream(fs, 81920)) // 80KB buffer
                {
                    byte[] buffer = new byte[4096];
                    int bytesRead;
                    while ((bytesRead = bs.Read(buffer, 0, buffer.Length)) > 0)
                    {
                        ProcessBuffer(buffer, bytesRead);
                    }
                }
                
                Memory-mapped files for large files:
                public static void ProcessLargeFile(string filePath)
                {
                    using (var mmf = MemoryMappedFile.CreateFromFile(filePath))
                    using (var accessor = mmf.CreateViewAccessor())
                    {
                        long fileSize = new FileInfo(filePath).Length;
                        byte[] buffer = new byte[4096];
                        
                        for (long offset = 0; offset < fileSize; offset += buffer.Length)
                        {
                            int bytesToRead = (int)Math.Min(buffer.Length, fileSize - offset);
                            accessor.ReadArray(offset, buffer, 0, bytesToRead);
                            ProcessBuffer(buffer, bytesToRead);
                        }
                    }
                }
                
                Asynchronous file operations:
                public async Task ProcessFileAsync(string filePath)
                {
                    byte[] buffer = new byte[8192];
                    
                    using (var fs = new FileStream(filePath, 
                        FileMode.Open, FileAccess.Read, FileShare.Read, 
                        8192, FileOptions.Asynchronous | FileOptions.SequentialScan))
                    {
                        int bytesRead;
                        while ((bytesRead = await fs.ReadAsync(buffer, 0, buffer.Length)) > 0)
                        {
                            await ProcessBufferAsync(buffer, bytesRead);
                        }
                    }
                }
                
                FileOptions for optimization:
                • FileOptions.Asynchronous: Enable async I/O
                • FileOptions.SequentialScan: Optimize for sequential access
                • FileOptions.RandomAccess: Optimize for random access
                • FileOptions.WriteThrough: Write directly to disk (no OS cache)
                • FileOptions.Encrypted: Encrypt/decrypt on the fly
                """);
            
            // 2. Network I/O optimization
            Console.WriteLine("\n2. Network I/O Optimization:");
            Console.WriteLine("""
                HttpClient pooling and reuse:
                // BAD: Creating new HttpClient for each request
                public async Task<string> GetBadAsync(string url)
                {
                    using (var client = new HttpClient()) // Creates new connection
                    {
                        return await client.GetStringAsync(url);
                    }
                }
                
                // GOOD: Reuse HttpClient (IHttpClientFactory recommended)
                public class GoodHttpClient
                {
                    private static readonly HttpClient _client = new HttpClient();
                    
                    public async Task<string> GetGoodAsync(string url)
                    {
                        return await _client.GetStringAsync(url);
                    }
                }
                
                // BEST: Use IHttpClientFactory (ASP.NET Core)
                services.AddHttpClient<MyService>(client =>
                {
                    client.BaseAddress = new Uri("https://api.example.com");
                    client.Timeout = TimeSpan.FromSeconds(30);
                    client.DefaultRequestHeaders.Add("User-Agent", "MyApp");
                });
                
                Connection pooling:
                // Default in .NET: Connection pooling enabled
                // Max connections per server: Environment dependent
                // Adjust with ServicePointManager
                ServicePointManager.DefaultConnectionLimit = 100;
                
                Compression for network traffic:
                public class CompressedHttpClient
                {
                    private readonly HttpClient _client;
                    
                    public CompressedHttpClient()
                    {
                        var handler = new HttpClientHandler
                        {
                            AutomaticDecompression = DecompressionMethods.GZip | 
                                                    DecompressionMethods.Deflate
                        };
                        
                        _client = new HttpClient(handler);
                        _client.DefaultRequestHeaders.AcceptEncoding.Add(
                            new StringWithQualityHeaderValue("gzip"));
                        _client.DefaultRequestHeaders.AcceptEncoding.Add(
                            new StringWithQualityHeaderValue("deflate"));
                    }
                    
                    public async Task<string> GetCompressedAsync(string url)
                    {
                        var response = await _client.GetAsync(url);
                        return await response.Content.ReadAsStringAsync();
                    }
                }
                
                WebSocket for real-time communication:
                public class WebSocketClient
                {
                    private ClientWebSocket _webSocket;
                    
                    public async Task ConnectAsync(string url)
                    {
                        _webSocket = new ClientWebSocket();
                        await _webSocket.ConnectAsync(new Uri(url), CancellationToken.None);
                        
                        // Start receiving
                        _ = ReceiveLoopAsync();
                    }
                    
                    private async Task ReceiveLoopAsync()
                    {
                        var buffer = new byte[4096];
                        
                        while (_webSocket.State == WebSocketState.Open)
                        {
                            var result = await _webSocket.ReceiveAsync(
                                new ArraySegment<byte>(buffer), CancellationToken.None);
                            
                            if (result.MessageType == WebSocketMessageType.Close)
                            {
                                await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, 
                                    "Closing", CancellationToken.None);
                                break;
                            }
                            
                            ProcessMessage(buffer, result.Count, result.EndOfMessage);
                        }
                    }
                }
                """);
            
            // 3. Database I/O optimization
            Console.WriteLine("\n3. Database I/O Optimization:");
            Console.WriteLine("""
                Connection pooling (ADO.NET):
                // Enabled by default in SqlConnection
                // Pool settings in connection string
                "Server=.;Database=MyDb;Integrated Security=true;" +
                "Pooling=true;Min Pool Size=5;Max Pool Size=100;" +
                "Connection Lifetime=300;Connection Timeout=30"
                
                • Pooling=true: Enable connection pooling
                • Min Pool Size: Minimum connections in pool
                • Max Pool Size: Maximum connections in pool  
                • Connection Lifetime: Max seconds connection stays in pool
                • Connection Timeout: Seconds to wait for connection
                
                Command batching:
                // BAD: Multiple round trips
                foreach (var item in items)
                {
                    cmd.CommandText = $"INSERT INTO Items VALUES ({item.Id}, '{item.Name}')";
                    await cmd.ExecuteNonQueryAsync();
                }
                
                // GOOD: Batch insert
                var sb = new StringBuilder();
                sb.AppendLine("INSERT INTO Items (Id, Name) VALUES");
                
                for (int i = 0; i < items.Count; i++)
                {
                    sb.Append($"({items[i].Id}, '{items[i].Name}')");
                    if (i < items.Count - 1) sb.AppendLine(",");
                }
                
                cmd.CommandText = sb.ToString();
                await cmd.ExecuteNonQueryAsync();
                
                // BETTER: Table-valued parameters (SQL Server)
                DataTable dt = new DataTable();
                dt.Columns.Add("Id", typeof(int));
                dt.Columns.Add("Name", typeof(string));
                
                foreach (var item in items)
                {
                    dt.Rows.Add(item.Id, item.Name);
                }
                
                var param = cmd.Parameters.AddWithValue("@Items", dt);
                param.SqlDbType = SqlDbType.Structured;
                param.TypeName = "dbo.ItemTableType";
                
                cmd.CommandText = "INSERT INTO Items SELECT * FROM @Items";
                await cmd.ExecuteNonQueryAsync();
                
                Bulk operations:
                // SqlBulkCopy for large inserts
                using (var bulkCopy = new SqlBulkCopy(connection))
                {
                    bulkCopy.DestinationTableName = "Items";
                    bulkCopy.BatchSize = 1000;
                    bulkCopy.BulkCopyTimeout = 60;
                    
                    // Map columns
                    bulkCopy.ColumnMappings.Add("Id", "Id");
                    bulkCopy.ColumnMappings.Add("Name", "Name");
                    
                    await bulkCopy.WriteToServerAsync(dataTable);
                }
                
                Query optimization:
                • Use WHERE clauses to filter early
                • SELECT only needed columns (not SELECT *)
                • Use EXISTS instead of COUNT(*) > 0
                • Create appropriate indexes
                • Avoid N+1 queries (use JOIN or Include)
                • Use stored procedures for complex logic
                """);
        }
        
        static void DemonstrateConcurrencyOptimization()
        {
            Console.WriteLine("\n=== 6. Concurrency Optimization ===\n");
            
            // 1. Parallel processing
            Console.WriteLine("1. Parallel Processing:");
            Console.WriteLine("""
                Parallel.For and Parallel.ForEach:
                public void ProcessInParallel(int[] data)
                {
                    // Simple parallel loop
                    Parallel.For(0, data.Length, i =>
                    {
                        data[i] = ProcessItem(data[i]);
                    });
                    
                    // With options
                    var options = new ParallelOptions
                    {
                        MaxDegreeOfParallelism = Environment.ProcessorCount,
                        CancellationToken = CancellationToken.None
                    };
                    
                    Parallel.ForEach(data, options, item =>
                    {
                        ProcessItem(item);
                    });
                }
                
                PLINQ (Parallel LINQ):
                public void ProcessWithPlinq(int[] data)
                {
                    var results = data.AsParallel()
                        .WithDegreeOfParallelism(Environment.ProcessorCount)
                        .WithExecutionMode(ParallelExecutionMode.ForceParallelism)
                        .WithMergeOptions(ParallelMergeOptions.AutoBuffered)
                        .Where(x => x > 0)
                        .Select(x => ProcessItem(x))
                        .ToArray();
                        
                    // Merge options:
                    // • NotBuffered: Results available as soon as produced
                    // • AutoBuffered: Buffer automatically sized
                    // • FullyBuffered: Wait for all results
                }
                
                Task Parallel Library (TPL):
                public async Task ProcessWithTasks(int[] data)
                {
                    var tasks = new Task[data.Length];
                    
                    for (int i = 0; i < data.Length; i++)
                    {
                        int index = i; // Capture local variable
                        tasks[i] = Task.Run(() =>
                        {
                            data[index] = ProcessItem(data[index]);
                        });
                    }
                    
                    await Task.WhenAll(tasks);
                    
                    // Or with batches
                    const int batchSize = 100;
                    for (int i = 0; i < data.Length; i += batchSize)
                    {
                        int start = i;
                        int end = Math.Min(i + batchSize, data.Length);
                        
                        await Task.Run(() =>
                        {
                            for (int j = start; j < end; j++)
                            {
                                data[j] = ProcessItem(data[j]);
                            }
                        });
                    }
                }
                
                Dataflow (TPL Dataflow):
                // Install-Package System.Threading.Tasks.Dataflow
                public async Task ProcessWithDataflow(int[] data)
                {
                    var bufferBlock = new BufferBlock<int>();
                    var transformBlock = new TransformBlock<int, int>(
                        x => ProcessItem(x),
                        new ExecutionDataflowBlockOptions
                        {
                            MaxDegreeOfParallelism = Environment.ProcessorCount,
                            BoundedCapacity = 1000
                        });
                    var actionBlock = new ActionBlock<int>(
                        result => Console.WriteLine($"Result: {result}"));
                    
                    // Link blocks
                    bufferBlock.LinkTo(transformBlock);
                    transformBlock.LinkTo(actionBlock);
                    
                    // Post data
                    foreach (var item in data)
                    {
                        await bufferBlock.SendAsync(item);
                    }
                    
                    bufferBlock.Complete();
                    await actionBlock.Completion;
                }
                """);
            
            // 2. Locking optimization
            Console.WriteLine("\n2. Locking Optimization:");
            Console.WriteLine("""
                Lock granularity:
                // COARSE: Everything locked together
                private readonly object _lock = new object();
                private Dictionary<string, int> _data = new();
                
                public void UpdateCoarse(string key, int value)
                {
                    lock (_lock) // Blocks all access
                    {
                        _data[key] = value;
                        // Other operations...
                    }
                }
                
                // FINE: Separate locks per key
                private readonly Dictionary<string, object> _keyLocks = new();
                private readonly Dictionary<string, int> _data = new();
                
                public void UpdateFine(string key, int value)
                {
                    object keyLock;
                    lock (_keyLocks)
                    {
                        if (!_keyLocks.TryGetValue(key, out keyLock))
                        {
                            keyLock = new object();
                            _keyLocks[key] = keyLock;
                        }
                    }
                    
                    lock (keyLock) // Only blocks this key
                    {
                        _data[key] = value;
                    }
                }
                
                ReaderWriterLockSlim:
                public class ThreadSafeCache
                {
                    private readonly ReaderWriterLockSlim _lock = new();
                    private readonly Dictionary<string, string> _cache = new();
                    
                    public string GetOrAdd(string key, Func<string> valueFactory)
                    {
                        // Try read lock first
                        _lock.EnterUpgradeableReadLock();
                        try
                        {
                            if (_cache.TryGetValue(key, out var value))
                                return value;
                            
                            // Upgrade to write lock
                            _lock.EnterWriteLock();
                            try
                            {
                                // Double-check (another thread might have added)
                                if (!_cache.TryGetValue(key, out value))
                                {
                                    value = valueFactory();
                                    _cache[key] = value;
                                }
                                return value;
                            }
                            finally
                            {
                                _lock.ExitWriteLock();
                            }
                        }
                        finally
                        {
                            _lock.ExitUpgradeableReadLock();
                        }
                    }
                }
                
                SpinLock for very short operations:
                public class SpinLockExample
                {
                    private SpinLock _spinLock = new SpinLock();
                    private int _counter;
                    
                    public void Increment()
                    {
                        bool lockTaken = false;
                        try
                        {
                            _spinLock.Enter(ref lockTaken);
                            _counter++;
                        }
                        finally
                        {
                            if (lockTaken) _spinLock.Exit();
                        }
                    }
                }
                
                Interlocked operations:
                public class AtomicCounter
                {
                    private int _counter;
                    
                    public void Increment()
                    {
                        Interlocked.Increment(ref _counter);
                    }
                    
                    public void Add(int value)
                    {
                        Interlocked.Add(ref _counter, value);
                    }
                    
                    public int Read()
                    {
                        return Interlocked.CompareExchange(ref _counter, 0, 0);
                    }
                    
                    public bool TryUpdate(int expected, int newValue)
                    {
                        return Interlocked.CompareExchange(
                            ref _counter, newValue, expected) == expected;
                    }
                }
                
                Volatile for low-lock code:
                public class VolatileExample
                {
                    private volatile bool _flag;
                    private int _data;
                    
                    public void Writer()
                    {
                        _data = 42;
                        _flag = true; // Write barrier
                    }
                    
                    public void Reader()
                    {
                        if (_flag) // Read barrier
                        {
                            // _data is guaranteed to be 42
                            Console.WriteLine(_data);
                        }
                    }
                }
                """);
            
            // 3. Async/await optimization
            Console.WriteLine("\n3. Async/Await Optimization:");
            Console.WriteLine("""
                ConfigureAwait(false):
                public async Task ProcessAsync()
                {
                    // On UI thread
                    var data = await GetDataAsync();
                    
                    // Continue on thread pool (not UI thread)
                    await ProcessDataAsync(data).ConfigureAwait(false);
                    
                    // Back to UI thread (if needed)
                    UpdateUI(data);
                }
                
                ValueTask for synchronous completion:
                public ValueTask<int> GetCachedValueAsync(int key)
                {
                    if (_cache.TryGetValue(key, out var value))
                    {
                        return new ValueTask<int>(value); // Synchronous
                    }
                    
                    return new ValueTask<int>(LoadValueAsync(key)); // Asynchronous
                }
                
                Cancellation for responsiveness:
                public async Task ProcessWithCancellationAsync(
                    CancellationToken cancellationToken = default)
                {
                    // Pass token to async operations
                    var data = await GetDataAsync(cancellationToken);
                    
                    // Check token periodically
                    for (int i = 0; i < 100; i++)
                    {
                        cancellationToken.ThrowIfCancellationRequested();
                        await ProcessItemAsync(data[i], cancellationToken);
                    }
                }
                
                TaskCompletionSource for custom async operations:
                public Task<int> WaitForEventAsync()
                {
                    var tcs = new TaskCompletionSource<int>();
                    
                    SomeEvent += (sender, args) =>
                    {
                        tcs.TrySetResult(args.Value);
                    };
                    
                    // Timeout support
                    _ = Task.Delay(TimeSpan.FromSeconds(30))
                        .ContinueWith(_ => tcs.TrySetCanceled());
                    
                    return tcs.Task;
                }
                
                Async streams (IAsyncEnumerable<T>):
                public async IAsyncEnumerable<int> GenerateSequenceAsync()
                {
                    for (int i = 0; i < 10; i++)
                    {
                        await Task.Delay(100);
                        yield return i;
                    }
                }
                
                // Consume with await foreach
                await foreach (var item in GenerateSequenceAsync())
                {
                    Console.WriteLine(item);
                }
                """);
        }
        
        static void DemonstrateCachingStrategies()
        {
            Console.WriteLine("\n=== 7. Caching Strategies ===\n");
            
            // 1. Memory caching
            Console.WriteLine("1. Memory Caching:");
            Console.WriteLine("""
                IMemoryCache (ASP.NET Core):
                // In Startup.cs
                services.AddMemoryCache(options =>
                {
                    options.SizeLimit = 1024 * 1024 * 100; // 100MB
                    options.CompactionPercentage = 0.2;
                    options.ExpirationScanFrequency = TimeSpan.FromMinutes(5);
                });
                
                public class DataService
                {
                    private readonly IMemoryCache _cache;
                    
                    public async Task<string> GetDataAsync(string key)
                    {
                        // Try get from cache
                        if (_cache.TryGetValue(key, out string cachedData))
                            return cachedData;
                        
                        // Get from source
                        var data = await FetchDataFromSourceAsync(key);
                        
                        // Cache with options
                        var cacheOptions = new MemoryCacheEntryOptions
                        {
                            AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5),
                            SlidingExpiration = TimeSpan.FromMinutes(1),
                            Size = 1, // Size in units (for SizeLimit)
                            Priority = CacheItemPriority.Normal
                        };
                        
                        // Register callbacks
                        cacheOptions.RegisterPostEvictionCallback(
                            (key, value, reason, state) =>
                            {
                                Console.WriteLine($"Cache evicted: {key}, reason: {reason}");
                            });
                        
                        _cache.Set(key, data, cacheOptions);
                        return data;
                    }
                }
                
                Cache entry options:
                • AbsoluteExpiration: Fixed point in time
                • AbsoluteExpirationRelativeToNow: Time from now
                • SlidingExpiration: Reset on access
                • Size: Relative size for cache eviction
                • Priority: Eviction priority (Low, Normal, High, NeverRemove)
                
                Cache aside pattern:
                public class CacheAsideService
                {
                    public async Task<T> GetOrAddAsync<T>(
                        string key, 
                        Func<Task<T>> valueFactory,
                        TimeSpan expiration)
                    {
                        if (_cache.TryGetValue(key, out T cached))
                            return cached;
                        
                        var value = await valueFactory();
                        
                        _cache.Set(key, value, expiration);
                        return value;
                    }
                }
                """);
            
            // 2. Distributed caching
            Console.WriteLine("\n2. Distributed Caching:");
            Console.WriteLine("""
                Redis caching:
                // Install-Package Microsoft.Extensions.Caching.StackExchangeRedis
                services.AddStackExchangeRedisCache(options =>
                {
                    options.Configuration = "localhost:6379";
                    options.InstanceName = "MyApp";
                });
                
                public class RedisCacheService
                {
                    private readonly IDistributedCache _cache;
                    
                    public async Task<byte[]> GetAsync(string key)
                    {
                        return await _cache.GetAsync(key);
                    }
                    
                    public async Task SetAsync(
                        string key, 
                        byte[] value, 
                        DistributedCacheEntryOptions options)
                    {
                        await _cache.SetAsync(key, value, options);
                    }
                    
                    public async Task RefreshAsync(string key)
                    {
                        await _cache.RefreshAsync(key);
                    }
                    
                    public async Task RemoveAsync(string key)
                    {
                        await _cache.RemoveAsync(key);
                    }
                }
                
                SQL Server distributed cache:
                // Install-Package Microsoft.Extensions.Caching.SqlServer
                services.AddDistributedSqlServerCache(options =>
                {
                    options.ConnectionString = _config.GetConnectionString("DistCache");
                    options.SchemaName = "dbo";
                    options.TableName = "Cache";
                });
                
                Cache synchronization:
                public class SynchronizedCache
                {
                    private readonly ConcurrentDictionary<string, SemaphoreSlim> _locks = new();
                    private readonly IDistributedCache _cache;
                    
                    public async Task<T> GetOrCreateAsync<T>(
                        string key, 
                        Func<Task<T>> factory,
                        DistributedCacheEntryOptions options)
                    {
                        var bytes = await _cache.GetAsync(key);
                        if (bytes != null)
                        {
                            return Deserialize<T>(bytes);
                        }
                        
                        var semaphore = _locks.GetOrAdd(key, _ => new SemaphoreSlim(1, 1));
                        await semaphore.WaitAsync();
                        
                        try
                        {
                            // Double-check
                            bytes = await _cache.GetAsync(key);
                            if (bytes != null)
                            {
                                return Deserialize<T>(bytes);
                            }
                            
                            var value = await factory();
                            bytes = Serialize(value);
                            await _cache.SetAsync(key, bytes, options);
                            
                            return value;
                        }
                        finally
                        {
                            semaphore.Release();
                            _locks.TryRemove(key, out _);
                        }
                    }
                }
                
                Cache invalidation strategies:
                • Time-based expiration (TTL)
                • Write-through: Update cache on write
                • Write-behind: Update cache asynchronously after write
                • Cache stampede prevention: Lock per key
                • Version-based: Cache key includes version
                • Tag-based: Invalidate by tags
                """);
            
            // 3. HTTP caching
            Console.WriteLine("\n3. HTTP Caching:");
            Console.WriteLine("""
                Response caching middleware:
                // In Startup.cs
                services.AddResponseCaching(options =>
                {
                    options.MaximumBodySize = 1024 * 1024; // 1MB
                    options.UseCaseSensitivePaths = false;
                });
                
                app.UseResponseCaching();
                app.Use(async (context, next) =>
                {
                    context.Response.GetTypedHeaders().CacheControl = 
                        new CacheControlHeaderValue
                        {
                            Public = true,
                            MaxAge = TimeSpan.FromSeconds(60),
                            MustRevalidate = true
                        };
                    
                    await next();
                });
                
                Cache-control headers:
                • public: Can be cached by any cache
                • private: Can only be cached by browser
                • no-cache: Must revalidate with server
                • no-store: Don't cache at all
                • max-age: Maximum time to cache (seconds)
                • s-maxage: Maximum time for shared caches
                • must-revalidate: Must check with server when stale
                • proxy-revalidate: Same for proxy caches
                
                ETag for conditional requests:
                public class EtagController : Controller
                {
                    [HttpGet("/api/data/{id}")]
                    public IActionResult GetData(int id)
                    {
                        var data = _repository.GetData(id);
                        var etag = GenerateEtag(data);
                        
                        // Check If-None-Match header
                        if (Request.Headers["If-None-Match"] == etag)
                        {
                            return StatusCode(304); // Not Modified
                        }
                        
                        Response.Headers["ETag"] = etag;
                        return Ok(data);
                    }
                    
                    private string GenerateEtag(object data)
                    {
                        var json = JsonSerializer.Serialize(data);
                        using (var md5 = MD5.Create())
                        {
                            var hash = md5.ComputeHash(Encoding.UTF8.GetBytes(json));
                            return $"\"{Convert.ToBase64String(hash)}\"";
                        }
                    }
                }
                
                CDN caching:
                // CloudFront, Azure CDN, Cloudflare
                // Edge locations worldwide
                // Cache static assets (images, CSS, JS)
                // Dynamic content with appropriate headers
                """);
        }
        
        static void DemonstrateDatabaseOptimization()
        {
            Console.WriteLine("\n=== 8. Database Optimization ===\n");
            
            // 1. Query optimization
            Console.WriteLine("1. Query Optimization:");
            Console.WriteLine("""
                Entity Framework optimization:
                // BAD: N+1 query problem
                var orders = context.Orders.ToList();
                foreach (var order in orders)
                {
                    var customer = context.Customers
                        .FirstOrDefault(c => c.Id == order.CustomerId); // N queries!
                }
                
                // GOOD: Eager loading
                var orders = context.Orders
                    .Include(o => o.Customer)
                    .Include(o => o.OrderItems)
                        .ThenInclude(oi => oi.Product)
                    .ToList();
                
                // GOOD: Projection (SELECT only needed columns)
                var orderSummaries = context.Orders
                    .Where(o => o.Date >= DateTime.Today.AddDays(-30))
                    .Select(o => new OrderSummary
                    {
                        Id = o.Id,
                        CustomerName = o.Customer.Name,
                        Total = o.OrderItems.Sum(oi => oi.Quantity * oi.UnitPrice),
                        ItemCount = o.OrderItems.Count
                    })
                    .ToList();
                
                // GOOD: Raw SQL for complex queries
                var topCustomers = context.Customers
                    .FromSqlRaw(
                        @"SELECT c.* FROM Customers c
                          INNER JOIN (
                              SELECT CustomerId, COUNT(*) as OrderCount
                              FROM Orders
                              GROUP BY CustomerId
                              HAVING COUNT(*) > 10
                          ) o ON c.Id = o.CustomerId")
                    .ToList();
                
                AsNoTracking for read-only queries:
                var customers = context.Customers
                    .AsNoTracking() // No change tracking overhead
                    .Where(c => c.IsActive)
                    .ToList();
                
                Compiled queries:
                private static readonly Func<MyDbContext, int, IQueryable<Order>> 
                    GetOrdersByCustomer = 
                        EF.CompileQuery((MyDbContext context, int customerId) =>
                            context.Orders
                                .Where(o => o.CustomerId == customerId)
                                .Include(o => o.OrderItems));
                
                // Usage (compiled once, cached)
                var orders = GetOrdersByCustomer(context, customerId).ToList();
                
                Batch operations:
                // Entity Framework Core 5+ supports SaveChanges batching
                context.ChangeTracker.AutoDetectChangesEnabled = false;
                
                for (int i = 0; i < 1000; i++)
                {
                    context.Products.Add(new Product { Name = $"Product {i}" });
                }
                
                await context.SaveChangesAsync(); // Single batch
                """);
            
            // 2. Index optimization
            Console.WriteLine("\n2. Index Optimization:");
            Console.WriteLine("""
                Creating indexes:
                // In DbContext.OnModelCreating
                modelBuilder.Entity<Order>()
                    .HasIndex(o => o.CustomerId);
                
                modelBuilder.Entity<Order>()
                    .HasIndex(o => new { o.CustomerId, o.OrderDate })
                    .IsUnique()
                    .HasName("IX_Orders_CustomerId_OrderDate");
                
                modelBuilder.Entity<Product>()
                    .HasIndex(p => p.Name)
                    .HasFilter("[Name] IS NOT NULL")
                    .IncludeProperties(p => new { p.Price, p.Category });
                
                Index types:
                • Clustered: Physically orders data (only one per table)
                • Non-clustered: Separate structure, points to data
                • Unique: No duplicate values
                • Filtered: Only includes rows meeting criteria
                • Covering: Includes all columns needed by query
                • Columnstore: For data warehousing (analytics)
                
                Index maintenance:
                // Rebuild index (offline)
                ALTER INDEX IX_Orders_CustomerId ON Orders REBUILD;
                
                // Reorganize index (online)
                ALTER INDEX IX_Orders_CustomerId ON Orders REORGANIZE;
                
                // Update statistics
                UPDATE STATISTICS Orders IX_Orders_CustomerId;
                
                Monitoring index usage:
                SELECT 
                    OBJECT_NAME(s.object_id) as TableName,
                    i.name as IndexName,
                    s.user_seeks,
                    s.user_scans,
                    s.user_lookups,
                    s.user_updates,
                    s.last_user_seek,
                    s.last_user_scan
                FROM sys.dm_db_index_usage_stats s
                INNER JOIN sys.indexes i ON s.object_id = i.object_id 
                    AND s.index_id = i.index_id
                WHERE OBJECT_NAME(s.object_id) = 'Orders'
                ORDER BY s.user_seeks + s.user_scans DESC;
                """);
            
            // 3. Connection and transaction optimization
            Console.WriteLine("\n3. Connection and Transaction Optimization:");
            Console.WriteLine("""
                Transaction isolation levels:
                // Read uncommitted (dirty reads)
                using (var transaction = context.Database.BeginTransaction(
                    System.Data.IsolationLevel.ReadUncommitted))
                {
                    // Can read uncommitted data
                    // Fastest, least consistent
                }
                
                // Read committed (default)
                using (var transaction = context.Database.BeginTransaction(
                    System.Data.IsolationLevel.ReadCommitted))
                {
                    // Can only read committed data
                    // Prevents dirty reads
                }
                
                // Repeatable read
                using (var transaction = context.Database.BeginTransaction(
                    System.Data.IsolationLevel.RepeatableRead))
                {
                    // Prevents non-repeatable reads
                    // Locks read rows
                }
                
                // Serializable
                using (var transaction = context.Database.BeginTransaction(
                    System.Data.IsolationLevel.Serializable))
                {
                    // Highest isolation
                    // Range locks, prevents phantom reads
                    // Slowest, most consistent
                }
                
                // Snapshot (SQL Server)
                using (var transaction = context.Database.BeginTransaction(
                    System.Data.IsolationLevel.Snapshot))
                {
                    // Uses row versioning
                    // No locks, but maintains versions
                    // Good for read-heavy workloads
                }
                
                Transaction scope:
                // Keep transactions short
                // Acquire locks late, release early
                // Process data outside transaction when possible
                // Use appropriate isolation level
                // Consider optimistic concurrency
                
                Connection resiliency:
                // Enable retry logic
                services.AddDbContext<MyDbContext>(options =>
                    options.UseSqlServer(
                        connectionString,
                        sqlOptions => 
                        {
                            sqlOptions.EnableRetryOnFailure(
                                maxRetryCount: 5,
                                maxRetryDelay: TimeSpan.FromSeconds(30),
                                errorNumbersToAdd: null);
                        }));
                """);
        }
        
        static void DemonstrateRealWorldOptimizations()
        {
            Console.WriteLine("\n=== 9. Real-World Optimizations ===\n");
            
            // 1. Web application optimizations
            Console.WriteLine("1. Web Application Optimizations:");
            Console.WriteLine("""
                ASP.NET Core optimizations:
                // In Startup.cs
                services.AddControllersWithViews(options =>
                {
                    options.SuppressAsyncSuffixInActionNames = true;
                })
                .AddJsonOptions(options =>
                {
                    options.JsonSerializerOptions.PropertyNamingPolicy = null;
                    options.JsonSerializerOptions.WriteIndented = false;
                    options.JsonSerializerOptions.IgnoreNullValues = true;
                });
                
                // Response compression
                services.AddResponseCompression(options =>
                {
                    options.EnableForHttps = true;
                    options.Providers.Add<BrotliCompressionProvider>();
                    options.Providers.Add<GzipCompressionProvider>();
                });
                
                // Kestrel configuration
                webBuilder.ConfigureKestrel(serverOptions =>
                {
                    serverOptions.Limits.MaxRequestBodySize = 52428800; // 50MB
                    serverOptions.Limits.MaxConcurrentConnections = 100;
                    serverOptions.Limits.MaxConcurrentUpgradedConnections = 100;
                    serverOptions.Limits.KeepAliveTimeout = TimeSpan.FromMinutes(2);
                    serverOptions.Limits.RequestHeadersTimeout = TimeSpan.FromSeconds(30);
                });
                
                Static file optimization:
                app.UseStaticFiles(new StaticFileOptions
                {
                    OnPrepareResponse = ctx =>
                    {
                        // Cache static files for 1 year
                        ctx.Context.Response.Headers[HeaderNames.CacheControl] = 
                            "public,max-age=31536000";
                    }
                });
                
                // Serve compressed files
                app.UseStaticFiles(new StaticFileOptions
                {
                    ServeUnknownFileTypes = false,
                    DefaultContentType = "application/octet-stream",
                    OnPrepareResponse = ctx =>
                    {
                        var path = ctx.File.PhysicalPath;
                        if (path.EndsWith(".br"))
                            ctx.Context.Response.Headers[HeaderNames.ContentEncoding] = "br";
                        else if (path.EndsWith(".gz"))
                            ctx.Context.Response.Headers[HeaderNames.ContentEncoding] = "gzip";
                    }
                });
                
                Middleware optimization:
                // Order matters!
                app.UseResponseCompression(); // Early for compression
                app.UseStaticFiles(); // Before routing for static files
                app.UseRouting();
                app.UseResponseCaching(); // After routing, before endpoints
                app.UseEndpoints(endpoints => { /* ... */ });
                
                API optimization:
                • Use pagination for large results
                • Implement filtering, sorting
                • Support partial responses (fields parameter)
                • Use HTTP/2 for multiplexing
                • Implement rate limiting
                • Use OData for complex queries
                """);
            
            // 2. Microservices optimizations
            Console.WriteLine("\n2. Microservices Optimizations:");
            Console.WriteLine("""
                gRPC for service-to-service communication:
                // Protocol buffers, binary serialization
                // HTTP/2, multiplexing, header compression
                // Lower latency, smaller payloads
                
                services.AddGrpc(options =>
                {
                    options.EnableDetailedErrors = true;
                    options.MaxReceiveMessageSize = 4 * 1024 * 1024; // 4MB
                    options.MaxSendMessageSize = 4 * 1024 * 1024;
                });
                
                Message queue optimization:
                public class OptimizedMessageProcessor
                {
                    private readonly IConnection _connection;
                    private readonly IModel _channel;
                    private readonly SemaphoreSlim _semaphore;
                    
                    public OptimizedMessageProcessor(int maxConcurrency)
                    {
                        _semaphore = new SemaphoreSlim(maxConcurrency);
                        
                        // Prefetch count
                        _channel.BasicQos(
                            prefetchSize: 0,
                            prefetchCount: (ushort)maxConcurrency,
                            global: false);
                    }
                    
                    public async Task ProcessMessagesAsync()
                    {
                        var consumer = new AsyncEventingBasicConsumer(_channel);
                        consumer.Received += async (model, ea) =>
                        {
                            await _semaphore.WaitAsync();
                            
                            try
                            {
                                await ProcessMessageAsync(ea.Body.ToArray());
                                _channel.BasicAck(ea.DeliveryTag, multiple: false);
                            }
                            catch (Exception ex)
                            {
                                // Handle error, maybe nack
                                _channel.BasicNack(ea.DeliveryTag, multiple: false, requeue: true);
                            }
                            finally
                            {
                                _semaphore.Release();
                            }
                        };
                        
                        _channel.BasicConsume(
                            queue: "myqueue",
                            autoAck: false,
                            consumer: consumer);
                    }
                }
                
                Circuit breaker pattern:
                // Install-Package Polly
                public class ResilientServiceClient
                {
                    private readonly IAsyncPolicy<HttpResponseMessage> _policy;
                    
                    public ResilientServiceClient()
                    {
                        _policy = Policy
                            .Handle<HttpRequestException>()
                            .OrResult<HttpResponseMessage>(r => !r.IsSuccessStatusCode)
                            .CircuitBreakerAsync(
                                handledEventsAllowedBeforeBreaking: 3,
                                durationOfBreak: TimeSpan.FromSeconds(30),
                                onBreak: (result, timespan, context) =>
                                {
                                    Console.WriteLine("Circuit broken!");
                                },
                                onReset: (context) =>
                                {
                                    Console.WriteLine("Circuit reset!");
                                });
                    }
                    
                    public async Task<string> CallServiceAsync(string url)
                    {
                        return await _policy.ExecuteAsync(async () =>
                        {
                            var response = await _httpClient.GetAsync(url);
                            response.EnsureSuccessStatusCode();
                            return await response.Content.ReadAsStringAsync();
                        });
                    }
                }
                
                Service discovery and load balancing:
                • Consul, Eureka, ZooKeeper
                • Round-robin, least connections, IP hash
                • Health checks, circuit breaking
                • Client-side vs server-side load balancing
                """);
            
            // 3. Real-time application optimizations
            Console.WriteLine("\n3. Real-Time Application Optimizations:");
            Console.WriteLine("""
                SignalR optimization:
                services.AddSignalR(options =>
                {
                    options.EnableDetailedErrors = true;
                    options.MaximumReceiveMessageSize = 32768; // 32KB
                    options.StreamBufferCapacity = 10;
                    
                    // Transport options
                    options.Transports = HttpTransportType.WebSockets | 
                                        HttpTransportType.LongPolling;
                    
                    // Keep-alive
                    options.KeepAliveInterval = TimeSpan.FromSeconds(15);
                })
                .AddMessagePackProtocol() // Binary protocol
                .AddHubOptions<ChatHub>(options =>
                {
                    options.EnableDetailedErrors = false;
                    options.ClientTimeoutInterval = TimeSpan.FromSeconds(30);
                    options.HandshakeTimeout = TimeSpan.FromSeconds(15);
                });
                
                WebSocket optimization:
                app.UseWebSockets(new WebSocketOptions
                {
                    KeepAliveInterval = TimeSpan.FromSeconds(120),
                    ReceiveBufferSize = 4096,
                });
                
                // Custom WebSocket handler
                public class OptimizedWebSocketHandler
                {
                    private const int MaxConcurrentConnections = 1000;
                    private readonly SemaphoreSlim _connectionSemaphore = 
                        new SemaphoreSlim(MaxConcurrentConnections);
                    
                    public async Task HandleWebSocketAsync(HttpContext context)
                    {
                        if (!await _connectionSemaphore.WaitAsync(0))
                        {
                            context.Response.StatusCode = 503; // Service Unavailable
                            return;
                        }
                        
                        try
                        {
                            var webSocket = await context.WebSockets.AcceptWebSocketAsync();
                            await ProcessWebSocketAsync(webSocket);
                        }
                        finally
                        {
                            _connectionSemaphore.Release();
                        }
                    }
                    
                    private async Task ProcessWebSocketAsync(WebSocket webSocket)
                    {
                        var buffer = new byte[4096];
                        
                        while (webSocket.State == WebSocketState.Open)
                        {
                            var result = await webSocket.ReceiveAsync(
                                new ArraySegment<byte>(buffer), 
                                CancellationToken.None);
                            
                            if (result.MessageType == WebSocketMessageType.Close)
                            {
                                await webSocket.CloseAsync(
                                    WebSocketCloseStatus.NormalClosure,
                                    "Closing",
                                    CancellationToken.None);
                                break;
                            }
                            
                            // Process message
                            await ProcessMessageAsync(buffer, result.Count);
                        }
                    }
                }
                
                UDP for high-throughput, low-latency:
                public class UdpServer
                {
                    private readonly UdpClient _udpClient;
                    private readonly byte[] _receiveBuffer = new byte[65507]; // Max UDP size
                    
                    public async Task StartAsync(int port)
                    {
                        _udpClient = new UdpClient(port);
                        
                        while (true)
                        {
                            try
                            {
                                var result = await _udpClient.ReceiveAsync();
                                ProcessPacket(result.Buffer, result.RemoteEndPoint);
                            }
                            catch (SocketException ex)
                            {
                                // Handle error
                            }
                        }
                    }
                    
                    private void ProcessPacket(byte[] data, IPEndPoint remoteEndpoint)
                    {
                        // Process UDP packet
                        // No connection overhead, no guarantees
                    }
                }
                """);
            
            // 4. Monitoring and tuning
            Console.WriteLine("\n4. Monitoring and Tuning:");
            Console.WriteLine("""
                Application performance monitoring (APM):
                • Application Insights
                • New Relic
                • Dynatrace
                • OpenTelemetry
                
                Key metrics to monitor:
                • Response time percentiles
                • Error rate
                • Throughput (requests/sec)
                • Resource utilization (CPU, memory, disk, network)
                • GC collections and pauses
                • Database query performance
                • Cache hit ratio
                
                Performance tuning process:
                1. Measure baseline performance
                2. Identify bottlenecks (CPU, memory, I/O, network)
                3. Hypothesize root cause
                4. Implement optimization
                5. Measure improvement
                6. Repeat if necessary
                
                Common bottlenecks:
                • CPU: Infinite loops, complex algorithms
                • Memory: Memory leaks, excessive allocations
                • I/O: Slow disks, many small reads/writes
                • Network: High latency, low bandwidth
                • Database: Missing indexes, N+1 queries
                • Locking: Contention, deadlocks
                
                Production debugging:
                // DebugDiag, WinDbg, dotnet-dump
                // Memory dumps, CPU sampling
                // Thread stacks, lock contention
                // GC heap analysis
                
                Continuous performance testing:
                • Load tests in CI/CD pipeline
                • Performance gates (fail if regressions)
                • Canary deployments with performance monitoring
                • A/B testing for performance optimizations
                """);
        }
    }
    
    // Supporting classes for examples
    
    public class Order
    {
        public int Id { get; set; }
        public int CustomerId { get; set; }
        public DateTime OrderDate { get; set; }
        public Customer Customer { get; set; }
        public List<OrderItem> OrderItems { get; set; }
    }
    
    public class Customer
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public bool IsActive { get; set; }
    }
    
    public class OrderItem
    {
        public int Id { get; set; }
        public int OrderId { get; set; }
        public int ProductId { get; set; }
        public int Quantity { get; set; }
        public decimal UnitPrice { get; set; }
        public Product Product { get; set; }
    }
    
    public class Product
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public decimal Price { get; set; }
        public string Category { get; set; }
    }
    
    public class OrderSummary
    {
        public int Id { get; set; }
        public string CustomerName { get; set; }
        public decimal Total { get; set; }
        public int ItemCount { get; set; }
    }
    
    public class MyDbContext : DbContext
    {
        public DbSet<Order> Orders { get; set; }
        public DbSet<Customer> Customers { get; set; }
        public DbSet<Product> Products { get; set; }
        public DbSet<OrderItem> OrderItems { get; set; }
        
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            // Index configuration
            modelBuilder.Entity<Order>()
                .HasIndex(o => o.CustomerId);
        }
    }
    
    // Mock methods for examples
    private static int ProcessItem(int item) => item * 2;
    private static void ProcessBuffer(byte[] buffer, int length) { }
    private static Task ProcessBufferAsync(byte[] buffer, int length) => Task.CompletedTask;
    private static Task ProcessChunkAsync(Memory<byte> chunk) => Task.CompletedTask;
    private static Task<string> GetDataAsync(CancellationToken ct) => Task.FromResult("data");
    private static Task ProcessDataAsync(string data) => Task.CompletedTask;
    private static void UpdateUI(string data) { }
    private static Task<int> LoadValueAsync(int key) => Task.FromResult(key * 2);
    private static Task<string> FetchDataFromSourceAsync(string key) => Task.FromResult("data");
    private static int GetActiveConnections() => 0;
    private static Task ProcessItemAsync(object data, CancellationToken ct) => Task.CompletedTask;
    private static void ProcessMessage(byte[] buffer, int count, bool endOfMessage) { }
    private static Task ProcessMessageAsync(byte[] buffer) => Task.CompletedTask;
    private static T Deserialize<T>(byte[] bytes) => default;
    private static byte[] Serialize<T>(T value) => Array.Empty<byte>();
    private static Task ProcessPacket(byte[] data, IPEndPoint endpoint) => Task.CompletedTask;
}