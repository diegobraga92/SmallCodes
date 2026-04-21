/*
    C# ADVANCED FEATURES
    File: 30_advanced_features.cs
    
    Comprehensive guide to advanced C# features and techniques.
    Covers modern C# language features, advanced patterns, performance optimizations,
    interoperability, source generators, and cutting-edge .NET capabilities.
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Reflection;
using System.Reflection.Emit;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Numerics;
using System.Threading.Channels;
using System.Buffers;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

namespace CSharpRefresher.AdvancedFeatures
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Advanced Features ===\n");
            
            DemonstrateModernLanguageFeatures();
            DemonstrateAdvancedPatterns();
            DemonstrateHighPerformanceTechniques();
            DemonstrateInteroperability();
            DemonstrateMetaProgramming();
            DemonstrateCuttingEdgeFeatures();
            DemonstrateRealWorldAdvancedScenarios();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateModernLanguageFeatures()
        {
            Console.WriteLine("=== 1. Modern Language Features ===\n");
            
            // 1. Pattern Matching
            Console.WriteLine("1. Pattern Matching:");
            Console.WriteLine("""
                Type patterns:
                object obj = "Hello";
                if (obj is string s)
                {
                    Console.WriteLine($"String length: {s.Length}");
                }
                
                Property patterns:
                var person = new Person { Name = "Alice", Age = 30 };
                if (person is { Age: >= 18, Name: not null })
                {
                    Console.WriteLine($"{person.Name} is an adult");
                }
                
                Switch expressions:
                string category = person.Age switch
                {
                    < 13 => "Child",
                    >= 13 and < 20 => "Teenager",
                    >= 20 and < 65 => "Adult",
                    >= 65 => "Senior",
                    _ => "Unknown"
                };
                
                Tuple patterns:
                var point = (x: 5, y: 10);
                var quadrant = point switch
                {
                    ( > 0, > 0) => "Quadrant I",
                    ( < 0, > 0) => "Quadrant II",
                    ( < 0, < 0) => "Quadrant III",
                    ( > 0, < 0) => "Quadrant IV",
                    _ => "On axis"
                };
                
                List patterns (C# 11+):
                int[] numbers = { 1, 2, 3 };
                if (numbers is [1, 2, 3])
                {
                    Console.WriteLine("Array matches pattern");
                }
                
                if (numbers is [var first, .. var rest])
                {
                    Console.WriteLine($"First: {first}, Rest count: {rest.Length}");
                }
                """);
            
            // 2. Records
            Console.WriteLine("\n2. Records:");
            Console.WriteLine("""
                Positional records:
                public record Person(string FirstName, string LastName, int Age);
                
                // Usage
                var person1 = new Person("John", "Doe", 30);
                var person2 = person1 with { Age = 31 }; // Non-destructive mutation
                
                // Value equality
                var person3 = new Person("John", "Doe", 30);
                Console.WriteLine(person1 == person3); // True
                
                // Deconstruction
                var (firstName, lastName, age) = person1;
                
                Record structs (C# 10+):
                public readonly record struct Point(int X, int Y);
                
                // With explicit members
                public record Product
                {
                    public string Name { get; init; }
                    public decimal Price { get; init; }
                    public string Category { get; init; }
                    
                    public Product(string name, decimal price, string category)
                    {
                        Name = name;
                        Price = price;
                        Category = category;
                    }
                };
                """);
            
            // 3. Init-only properties and required members
            Console.WriteLine("\n3. Init-only and Required Members:");
            Console.WriteLine("""
                Init-only properties:
                public class Configuration
                {
                    public string ServerUrl { get; init; }
                    public int Timeout { get; init; }
                    public bool EnableLogging { get; init; }
                }
                
                // Can only be set during initialization
                var config = new Configuration
                {
                    ServerUrl = "https://api.example.com",
                    Timeout = 30,
                    EnableLogging = true
                };
                
                // config.ServerUrl = "new"; // Compile error!
                
                Required members (C# 11+):
                public class User
                {
                    public required string Username { get; init; }
                    public required string Email { get; init; }
                    public DateTime CreatedAt { get; init; } = DateTime.UtcNow;
                }
                
                // Must initialize required properties
                var user = new User
                {
                    Username = "johndoe",
                    Email = "john@example.com"
                };
                
                // var badUser = new User(); // Compile error!
                
                SetsRequiredMembers attribute:
                [SetsRequiredMembers]
                public User(string username, string email)
                {
                    Username = username;
                    Email = email;
                }
                """);
            
            // 4. Nullable reference types
            Console.WriteLine("\n4. Nullable Reference Types:");
            Console.WriteLine("""
                Enable nullable context:
                #nullable enable
                
                public class Customer
                {
                    public string Name { get; } // Non-nullable
                    public string? MiddleName { get; } // Nullable
                    
                    public Customer(string name, string? middleName)
                    {
                        Name = name ?? throw new ArgumentNullException(nameof(name));
                        MiddleName = middleName;
                    }
                    
                    public string GetFullName()
                    {
                        // Warning: MiddleName may be null
                        return MiddleName == null ? Name : $"{Name} {MiddleName}";
                        
                        // Better: Use null-forgiving operator if you know it's safe
                        return $"{Name} {MiddleName!}";
                    }
                }
                
                Null-forgiving operator (!):
                string definitelyNotNull = GetPossiblyNullString()!;
                
                // Use when you know better than the compiler
                string? possiblyNull = GetString();
                string notNull = possiblyNull!; // I promise it's not null
                
                Null parameter checking:
                public void Process(string input)
                {
                    ArgumentNullException.ThrowIfNull(input);
                    // Safe to use input
                }
                
                // Or with attributes
                public void Process([NotNull] string? input)
                {
                    // Compiler knows input is not null after this point
                }
                """);
            
            // 5. Top-level statements and global using
            Console.WriteLine("\n5. Top-level Statements and Global Using:");
            Console.WriteLine("""
                Top-level statements (simplified Program.cs):
                // No namespace, no class, no Main method
                Console.WriteLine("Hello, World!");
                
                // Can have methods
                SayHello("Alice");
                
                void SayHello(string name) => Console.WriteLine($"Hello, {name}!");
                
                // Returns become exit code
                return 0;
                
                Global usings (GlobalUsings.cs):
                // GlobalUsings.cs
                global using System;
                global using System.Collections.Generic;
                global using System.Linq;
                global using System.Threading.Tasks;
                
                // Now available in all files without explicit using
                """);
        }
        
        static void DemonstrateAdvancedPatterns()
        {
            Console.WriteLine("\n=== 2. Advanced Patterns ===\n");
            
            // 1. Generic math and interfaces
            Console.WriteLine("1. Generic Math and Interfaces:");
            Console.WriteLine("""
                // .NET 7+ generic math
                public static T Add<T>(T left, T right) where T : INumber<T>
                {
                    return left + right;
                }
                
                public static T Average<T>(T[] values) where T : INumber<T>
                {
                    if (values.Length == 0) return T.Zero;
                    
                    T sum = T.Zero;
                    foreach (var value in values)
                    {
                        sum += value;
                    }
                    
                    return sum / T.CreateChecked(values.Length);
                }
                
                // Usage
                int[] ints = { 1, 2, 3, 4, 5 };
                double[] doubles = { 1.5, 2.5, 3.5 };
                
                Console.WriteLine(Average(ints)); // 3
                Console.WriteLine(Average(doubles)); // 2.5
                
                // Generic comparison
                public static T Max<T>(T a, T b) where T : IComparable<T>
                {
                    return a.CompareTo(b) >= 0 ? a : b;
                }
                
                // Generic parsing
                public static T ParseOrDefault<T>(string input) where T : IParsable<T>
                {
                    return T.TryParse(input, null, out var result) ? result : default!;
                }
                """);
            
            // 2. Advanced LINQ and functional programming
            Console.WriteLine("\n2. Advanced LINQ and Functional Programming:");
            Console.WriteLine("""
                Chunk (C# 11+):
                int[] numbers = { 1, 2, 3, 4, 5, 6, 7, 8 };
                var chunks = numbers.Chunk(3);
                // Returns: [1,2,3], [4,5,6], [7,8]
                
                TryGetNonEnumeratedCount:
                var list = new List<int> { 1, 2, 3 };
                if (list.TryGetNonEnumeratedCount(out int count))
                {
                    // Got count without enumeration
                }
                
                Zip with three sequences:
                var names = new[] { "Alice", "Bob", "Charlie" };
                var ages = new[] { 25, 30, 35 };
                var cities = new[] { "NYC", "LA", "Chicago" };
                
                var people = names.Zip(ages, cities)
                    .Select(x => new { Name = x.First, Age = x.Second, City = x.Third });
                
                Aggregate with seed and result selector:
                var sentence = "the quick brown fox jumps over the lazy dog";
                var wordCount = sentence.Split(' ')
                    .Aggregate(
                        seed: 0,
                        func: (count, word) => count + 1,
                        resultSelector: count => $"Word count: {count}");
                
                Custom LINQ operators:
                public static IEnumerable<T> WhereNotNull<T>(this IEnumerable<T?> source)
                    where T : class
                {
                    foreach (var item in source)
                    {
                        if (item != null) yield return item;
                    }
                }
                
                public static IEnumerable<T> DistinctBy<T, TKey>(
                    this IEnumerable<T> source,
                    Func<T, TKey> keySelector)
                {
                    var seen = new HashSet<TKey>();
                    foreach (var item in source)
                    {
                        if (seen.Add(keySelector(item)))
                        {
                            yield return item;
                        }
                    }
                }
                """);
            
            // 3. Advanced async patterns
            Console.WriteLine("\n3. Advanced Async Patterns:");
            Console.WriteLine("""
                ValueTask for performance:
                public async ValueTask<int> CalculateAsync()
                {
                    if (_cachedResult.HasValue)
                    {
                        return _cachedResult.Value; // Synchronous completion
                    }
                    
                    return await ComputeExpensiveResultAsync(); // Asynchronous
                }
                
                IAsyncEnumerable and await foreach:
                public async IAsyncEnumerable<int> GenerateNumbersAsync()
                {
                    for (int i = 0; i < 10; i++)
                    {
                        await Task.Delay(100);
                        yield return i;
                    }
                }
                
                // Usage
                await foreach (var number in GenerateNumbersAsync())
                {
                    Console.WriteLine(number);
                }
                
                Async LINQ with System.Linq.Async:
                // Install-Package System.Linq.Async
                var results = await GenerateNumbersAsync()
                    .Where(x => x % 2 == 0)
                    .SelectAwait(async x => await ProcessAsync(x))
                    .ToListAsync();
                
                CancellationToken with timeout:
                using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(5));
                try
                {
                    await LongRunningOperationAsync(cts.Token);
                }
                catch (OperationCanceledException)
                {
                    Console.WriteLine("Operation timed out");
                }
                
                ConfigureAwait options:
                await SomeAsyncMethod().ConfigureAwait(ConfigureAwaitOptions.SuppressThrowing);
                await SomeAsyncMethod().ConfigureAwait(ConfigureAwaitOptions.ForceYielding);
                """);
            
            // 4. Channels for producer-consumer
            Console.WriteLine("\n4. Channels for Producer-Consumer:");
            Console.WriteLine("""
                // System.Threading.Channels
                var channel = Channel.CreateUnbounded<int>();
                
                // Producer
                async Task ProduceAsync(ChannelWriter<int> writer)
                {
                    for (int i = 0; i < 10; i++)
                    {
                        await writer.WriteAsync(i);
                        await Task.Delay(100);
                    }
                    writer.Complete();
                }
                
                // Consumer
                async Task ConsumeAsync(ChannelReader<int> reader)
                {
                    await foreach (var item in reader.ReadAllAsync())
                    {
                        Console.WriteLine($"Received: {item}");
                        await ProcessItemAsync(item);
                    }
                }
                
                // Bounded channel with options
                var boundedChannel = Channel.CreateBounded<int>(new BoundedChannelOptions(100)
                {
                    FullMode = BoundedChannelFullMode.Wait,
                    SingleWriter = false,
                    SingleReader = false,
                    AllowSynchronousContinuations = true
                });
                
                // Multiple producers, single consumer pattern
                var mpscChannel = Channel.CreateUnbounded<int>(
                    new UnboundedChannelOptions { SingleReader = true });
                """);
        }
        
        static void DemonstrateHighPerformanceTechniques()
        {
            Console.WriteLine("\n=== 3. High-Performance Techniques ===\n");
            
            // 1. Span and Memory
            Console.WriteLine("1. Span<T> and Memory<T>:");
            Console.WriteLine("""
                Span for stack allocation:
                Span<int> stackSpan = stackalloc int[100];
                for (int i = 0; i < stackSpan.Length; i++)
                {
                    stackSpan[i] = i;
                }
                
                Processing arrays without allocation:
                int[] array = { 1, 2, 3, 4, 5 };
                Span<int> slice = array.AsSpan(1, 3); // [2, 3, 4]
                
                // Modify in-place
                slice.Reverse(); // array is now [1, 4, 3, 2, 5]
                
                String processing without allocations:
                string text = "Hello, World!";
                ReadOnlySpan<char> span = text.AsSpan();
                
                // Find without substring allocations
                int index = span.IndexOf(',');
                if (index != -1)
                {
                    var hello = span[..index]; // "Hello"
                    var world = span[(index + 2)..]; // "World!"
                }
                
                Memory for async operations:
                async Task ProcessDataAsync(Memory<byte> buffer)
                {
                    // Can be used in async contexts (unlike Span)
                    await File.ReadAllBytesAsync("data.bin", buffer);
                    ProcessBuffer(buffer.Span);
                }
                
                MemoryMarshal for advanced operations:
                byte[] bytes = { 1, 0, 0, 0, 2, 0, 0, 0 };
                Span<int> ints = MemoryMarshal.Cast<byte, int>(bytes);
                // ints[0] = 1, ints[1] = 2 (little-endian)
                """);
            
            // 2. ArrayPool and MemoryPool
            Console.WriteLine("\n2. ArrayPool and MemoryPool:");
            Console.WriteLine("""
                Using ArrayPool to reduce GC pressure:
                const int BufferSize = 4096;
                var pool = ArrayPool<byte>.Shared;
                
                byte[] buffer = pool.Rent(BufferSize);
                try
                {
                    // Use buffer
                    int bytesRead = stream.Read(buffer, 0, BufferSize);
                    ProcessBuffer(buffer.AsSpan(0, bytesRead));
                }
                finally
                {
                    pool.Return(buffer, clearArray: false); // Don't clear for perf
                }
                
                Custom array pool with cleanup:
                public class CustomArrayPool<T> : ArrayPool<T>
                {
                    private readonly ArrayPool<T> _pool = ArrayPool<T>.Create();
                    
                    public override T[] Rent(int minimumLength)
                    {
                        var array = _pool.Rent(minimumLength);
                        // Custom logic
                        return array;
                    }
                    
                    public override void Return(T[] array, bool clearArray = false)
                    {
                        // Custom cleanup
                        _pool.Return(array, clearArray);
                    }
                }
                
                MemoryPool for IMemoryOwner:
                using (IMemoryOwner<byte> owner = MemoryPool<byte>.Shared.Rent(1024))
                {
                    Memory<byte> memory = owner.Memory;
                    // Use memory
                    await ProcessAsync(memory);
                } // Automatically returned to pool
                """);
            
            // 3. Structs and ref returns
            Console.WriteLine("\n3. Structs and Ref Returns:");
            Console.WriteLine("""
                Ref returns and ref locals:
                public ref int Find(int[] array, int value)
                {
                    for (int i = 0; i < array.Length; i++)
                    {
                        if (array[i] == value)
                        {
                            return ref array[i]; // Return reference, not value
                        }
                    }
                    throw new InvalidOperationException("Value not found");
                }
                
                // Usage
                int[] numbers = { 1, 2, 3, 4, 5 };
                ref int found = ref Find(numbers, 3);
                found = 99; // Modifies array directly
                // numbers is now [1, 2, 99, 4, 5]
                
                Ref structs (stack-only):
                public ref struct StackOnlyStruct
                {
                    public int Value;
                    
                    public void Increment() => Value++;
                    
                    // Cannot implement interfaces (except IDisposable)
                    // Cannot be boxed
                    // Cannot be used in async methods
                    // Cannot be captured by lambda
                }
                
                Readonly ref structs:
                public readonly ref struct ImmutablePoint
                {
                    public readonly int X;
                    public readonly int Y;
                    
                    public ImmutablePoint(int x, int y)
                    {
                        X = x;
                        Y = y;
                    }
                    
                    // Methods must be readonly
                    public readonly double Distance() => Math.Sqrt(X * X + Y * Y);
                }
                
                In parameters for readonly references:
                public double Calculate(in Vector3 vector)
                {
                    // vector is passed by reference but cannot be modified
                    return Math.Sqrt(vector.X * vector.X + 
                                    vector.Y * vector.Y + 
                                    vector.Z * vector.Z);
                }
                """);
            
            // 4. SIMD with Vector and HardwareIntrinsics
            Console.WriteLine("\n4. SIMD with Vector<T> and HardwareIntrinsics:");
            Console.WriteLine("""
                Vector<T> for hardware acceleration:
                float[] a = new float[100];
                float[] b = new float[100];
                float[] result = new float[100];
                
                int vectorSize = Vector<float>.Count;
                for (int i = 0; i < a.Length; i += vectorSize)
                {
                    var va = new Vector<float>(a, i);
                    var vb = new Vector<float>(b, i);
                    var vresult = va + vb; // SIMD addition
                    vresult.CopyTo(result, i);
                }
                
                Hardware intrinsics for specific instructions:
                #if NET5_0_OR_GREATER
                using System.Runtime.Intrinsics;
                using System.Runtime.Intrinsics.X86;
                
                if (Avx2.IsSupported)
                {
                    var v1 = Vector256.Create(1.0f);
                    var v2 = Vector256.Create(2.0f);
                    var result = Avx.Add(v1, v2);
                }
                
                if (Sse42.IsSupported)
                {
                    // Use SSE4.2 instructions
                }
                #endif
                
                BitOperations for fast bit manipulation:
                uint value = 0b00010000;
                int leadingZeroCount = System.Numerics.BitOperations.LeadingZeroCount(value);
                int trailingZeroCount = System.Numerics.BitOperations.TrailingZeroCount(value);
                int popCount = System.Numerics.BitOperations.PopCount(value);
                
                uint reversed = System.Numerics.BitOperations.ReverseEndianness(value);
                """);
        }
        
        static void DemonstrateInteroperability()
        {
            Console.WriteLine("\n=== 4. Interoperability ===\n");
            
            // 1. P/Invoke and native interoperability
            Console.WriteLine("1. P/Invoke and Native Interoperability:");
            Console.WriteLine("""
                Basic P/Invoke:
                [DllImport("kernel32.dll", CharSet = CharSet.Unicode)]
                static extern bool GetComputerName(StringBuilder buffer, ref uint size);
                
                [DllImport("user32.dll")]
                static extern IntPtr GetForegroundWindow();
                
                [DllImport("user32.dll", CharSet = CharSet.Unicode)]
                static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
                
                Modern P/Invoke with LibraryImport:
                [LibraryImport("kernel32.dll", StringMarshalling = StringMarshalling.Utf16)]
                [return: MarshalAs(UnmanagedType.Bool)]
                private static partial bool GetComputerName(
                    [MarshalAs(UnmanagedType.LPWStr)] StringBuilder buffer,
                    ref uint size);
                
                Struct marshalling:
                [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
                public struct SystemInfo
                {
                    public ushort ProcessorArchitecture;
                    public uint PageSize;
                    public IntPtr MinimumApplicationAddress;
                    public IntPtr MaximumApplicationAddress;
                    public IntPtr ActiveProcessorMask;
                    public uint NumberOfProcessors;
                    public uint ProcessorType;
                    public uint AllocationGranularity;
                    public ushort ProcessorLevel;
                    public ushort ProcessorRevision;
                }
                
                [DllImport("kernel32.dll")]
                static extern void GetSystemInfo(ref SystemInfo systemInfo);
                
                Callback functions:
                public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);
                
                [DllImport("user32.dll")]
                [return: MarshalAs(UnmanagedType.Bool)]
                static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);
                
                // Usage
                bool Callback(IntPtr hWnd, IntPtr lParam)
                {
                    Console.WriteLine($"Window handle: {hWnd}");
                    return true;
                }
                
                EnumWindows(Callback, IntPtr.Zero);
                
                Memory marshalling with Span:
                [DllImport("NativeLib.dll")]
                private static extern unsafe int ProcessData(byte* data, int length);
                
                public static int ProcessData(Span<byte> data)
                {
                    unsafe
                    {
                        fixed (byte* ptr = data)
                        {
                            return ProcessData(ptr, data.Length);
                        }
                    }
                }
                """);
            
            // 2. COM interoperability
            Console.WriteLine("\n2. COM Interoperability:");
            Console.WriteLine("""
                COM interface with ComImport:
                [ComImport]
                [Guid("00000000-0000-0000-C000-000000000046")]
                [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
                public interface IUnknown
                {
                    [PreserveSig]
                    int QueryInterface(ref Guid riid, out IntPtr ppvObject);
                    
                    [PreserveSig]
                    uint AddRef();
                    
                    [PreserveSig]
                    uint Release();
                }
                
                CoCreateInstance for COM objects:
                [DllImport("ole32.dll")]
                static extern int CoCreateInstance(
                    [MarshalAs(UnmanagedType.LPStruct)] Guid rclsid,
                    IntPtr pUnkOuter,
                    uint dwClsContext,
                    [MarshalAs(UnmanagedType.LPStruct)] Guid riid,
                    out IntPtr ppv);
                
                // Usage
                Guid clsid = new Guid("...");
                Guid iid = new Guid("...");
                IntPtr comObject;
                int hr = CoCreateInstance(clsid, IntPtr.Zero, 1, iid, out comObject);
                
                COM events with ComSourceInterfaces:
                [ComVisible(true)]
                [ClassInterface(ClassInterfaceType.None)]
                [ComSourceInterfaces(typeof(IMyEvents))]
                public class MyComClass : IMyClass
                {
                    public event Action<string> OnMessage;
                    
                    public void SendMessage(string message)
                    {
                        OnMessage?.Invoke(message);
                    }
                }
                
                Late binding with Type.GetTypeFromProgID:
                Type excelType = Type.GetTypeFromProgID("Excel.Application");
                dynamic excel = Activator.CreateInstance(excelType);
                excel.Visible = true;
                excel.Workbooks.Add();
                """);
            
            // 3. Function pointers and UnmanagedCallersOnly
            Console.WriteLine("\n3. Function Pointers and UnmanagedCallersOnly:");
            Console.WriteLine("""
                Function pointers (C# 9+):
                public unsafe delegate* unmanaged[Cdecl]<int, int, int> AddFunction;
                
                // From native library
                [DllImport("NativeLib.dll")]
                public static extern unsafe delegate* unmanaged[Cdecl]<int, int, int> GetAddFunction();
                
                // Usage
                unsafe
                {
                    AddFunction = GetAddFunction();
                    int result = AddFunction(5, 3); // 8
                }
                
                UnmanagedCallersOnly for native callbacks:
                [UnmanagedCallersOnly(CallConvs = new[] { typeof(CallConvCdecl) })]
                public static int NativeCallback(int a, int b)
                {
                    return a + b;
                }
                
                // Can be passed to native code as function pointer
                // No garbage collection overhead
                // Cannot be called from managed code directly
                
                Managed-to-unmanaged stub:
                public class CallbackWrapper
                {
                    [UnmanagedCallersOnly]
                    public static int StaticCallback(int a, int b)
                    {
                        // Can't capture instance state
                        return a + b;
                    }
                    
                    // Instance method wrapper
                    private int InstanceCallback(int a, int b) => a + b;
                    
                    public delegate* unmanaged[Cdecl]<int, int, int> GetCallback()
                    {
                        var handle = GCHandle.Alloc(this);
                        var callback = (delegate* unmanaged[Cdecl]<int, int, int>)
                            Marshal.GetFunctionPointerForDelegate(
                                (Func<int, int, int>)InstanceCallback);
                        return callback;
                    }
                }
                """);
        }
        
        static void DemonstrateMetaProgramming()
        {
            Console.WriteLine("\n=== 5. Meta-Programming ===\n");
            
            // 1. Reflection and Reflection.Emit
            Console.WriteLine("1. Reflection and Reflection.Emit:");
            Console.WriteLine("""
                Dynamic type creation with Reflection.Emit:
                public static Type CreateDynamicType()
                {
                    var assemblyName = new AssemblyName("DynamicAssembly");
                    var assemblyBuilder = AssemblyBuilder.DefineDynamicAssembly(
                        assemblyName, AssemblyBuilderAccess.Run);
                    
                    var moduleBuilder = assemblyBuilder.DefineDynamicModule("MainModule");
                    var typeBuilder = moduleBuilder.DefineType(
                        "DynamicType",
                        TypeAttributes.Public | TypeAttributes.Class);
                    
                    // Add field
                    var fieldBuilder = typeBuilder.DefineField(
                        "_value",
                        typeof(int),
                        FieldAttributes.Private);
                    
                    // Add property
                    var propertyBuilder = typeBuilder.DefineProperty(
                        "Value",
                        PropertyAttributes.HasDefault,
                        typeof(int),
                        Type.EmptyTypes);
                    
                    // Add get method
                    var getMethodBuilder = typeBuilder.DefineMethod(
                        "get_Value",
                        MethodAttributes.Public | MethodAttributes.SpecialName | 
                        MethodAttributes.HideBySig,
                        typeof(int),
                        Type.EmptyTypes);
                    
                    var getIL = getMethodBuilder.GetILGenerator();
                    getIL.Emit(OpCodes.Ldarg_0);
                    getIL.Emit(OpCodes.Ldfld, fieldBuilder);
                    getIL.Emit(OpCodes.Ret);
                    
                    // Add set method
                    var setMethodBuilder = typeBuilder.DefineMethod(
                        "set_Value",
                        MethodAttributes.Public | MethodAttributes.SpecialName | 
                        MethodAttributes.HideBySig,
                        null,
                        new[] { typeof(int) });
                    
                    var setIL = setMethodBuilder.GetILGenerator();
                    setIL.Emit(OpCodes.Ldarg_0);
                    setIL.Emit(OpCodes.Ldarg_1);
                    setIL.Emit(OpCodes.Stfld, fieldBuilder);
                    setIL.Emit(OpCodes.Ret);
                    
                    propertyBuilder.SetGetMethod(getMethodBuilder);
                    propertyBuilder.SetSetMethod(setMethodBuilder);
                    
                    return typeBuilder.CreateType();
                }
                
                Dynamic method invocation:
                var method = typeof(Math).GetMethod("Max", new[] { typeof(int), typeof(int) });
                var result = method.Invoke(null, new object[] { 5, 10 });
                // result = 10
                
                Faster invocation with MethodInfo.CreateDelegate:
                var maxFunc = (Func<int, int, int>)method.CreateDelegate(
                    typeof(Func<int, int, int>));
                var fastResult = maxFunc(5, 10); // No reflection overhead
                
                Expression trees for dynamic code:
                var paramA = Expression.Parameter(typeof(int), "a");
                var paramB = Expression.Parameter(typeof(int), "b");
                var add = Expression.Add(paramA, paramB);
                var lambda = Expression.Lambda<Func<int, int, int>>(add, paramA, paramB);
                var compiled = lambda.Compile();
                var result = compiled(5, 3); // 8
                """);
            
            // 2. Source Generators
            Console.WriteLine("\n2. Source Generators:");
            Console.WriteLine("""
                Basic source generator structure:
                [Generator]
                public class MySourceGenerator : ISourceGenerator
                {
                    public void Initialize(GeneratorInitializationContext context)
                    {
                        // Register for syntax notifications
                        context.RegisterForSyntaxNotifications(() => 
                            new MySyntaxReceiver());
                    }
                    
                    public void Execute(GeneratorExecutionContext context)
                    {
                        // Generate source code
                        string source = @"
                namespace Generated
                {
                    public class GeneratedClass
                    {
                        public static void SayHello()
                        {
                            System.Console.WriteLine(""Hello from generator!"");
                        }
                    }
                }";
                        
                        context.AddSource("GeneratedClass.g.cs", source);
                    }
                }
                
                Syntax receiver for finding types:
                class MySyntaxReceiver : ISyntaxReceiver
                {
                    public List<ClassDeclarationSyntax> Classes { get; } = new();
                    
                    public void OnVisitSyntaxNode(SyntaxNode syntaxNode)
                    {
                        if (syntaxNode is ClassDeclarationSyntax classDecl)
                        {
                            Classes.Add(classDecl);
                        }
                    }
                }
                
                Generating partial classes:
                // Find classes with [AutoGenerate] attribute
                foreach (var classDecl in syntaxReceiver.Classes)
                {
                    var attributes = classDecl.AttributeLists
                        .SelectMany(al => al.Attributes);
                    
                    if (attributes.Any(a => a.Name.ToString() == "AutoGenerate"))
                    {
                        var className = classDecl.Identifier.Text;
                        var source = GeneratePartialClass(className);
                        context.AddSource($"{className}.generated.cs", source);
                    }
                }
                
                Incremental source generators (C# 10+):
                [Generator]
                public class IncrementalGenerator : IIncrementalGenerator
                {
                    public void Initialize(IncrementalGeneratorInitializationContext context)
                    {
                        var classDeclarations = context.SyntaxProvider
                            .CreateSyntaxProvider(
                                predicate: (node, _) => node is ClassDeclarationSyntax,
                                transform: (ctx, _) => (ClassDeclarationSyntax)ctx.Node)
                            .Where(c => c != null);
                        
                        context.RegisterSourceOutput(classDeclarations,
                            (spc, classDecl) =>
                            {
                                var source = GenerateSource(classDecl);
                                spc.AddSource($"{classDecl.Identifier.Text}.g.cs", source);
                            });
                    }
                }
                """);
            
            // 3. Code analysis and Roslyn
            Console.WriteLine("\n3. Code Analysis and Roslyn:");
            Console.WriteLine("""
                Creating analyzers and code fixes:
                [DiagnosticAnalyzer(LanguageNames.CSharp)]
                public class MyAnalyzer : DiagnosticAnalyzer
                {
                    private static readonly DiagnosticDescriptor Rule = 
                        new DiagnosticDescriptor(
                            id: "MY0001",
                            title: "Type name contains lowercase letters",
                            messageFormat: "Type name '{0}' contains lowercase letters",
                            category: "Naming",
                            defaultSeverity: DiagnosticSeverity.Warning,
                            isEnabledByDefault: true);
                    
                    public override ImmutableArray<DiagnosticDescriptor> 
                        SupportedDiagnostics => ImmutableArray.Create(Rule);
                    
                    public override void Initialize(AnalysisContext context)
                    {
                        context.RegisterSymbolAction(AnalyzeSymbol, SymbolKind.NamedType);
                    }
                    
                    private void AnalyzeSymbol(SymbolAnalysisContext context)
                    {
                        var namedTypeSymbol = (INamedTypeSymbol)context.Symbol;
                        if (namedTypeSymbol.Name.Any(char.IsLower))
                        {
                            var diagnostic = Diagnostic.Create(
                                Rule,
                                namedTypeSymbol.Locations[0],
                                namedTypeSymbol.Name);
                            context.ReportDiagnostic(diagnostic);
                        }
                    }
                }
                
                Code fix provider:
                [ExportCodeFixProvider(LanguageNames.CSharp, Name = nameof(MyCodeFixProvider))]
                public class MyCodeFixProvider : CodeFixProvider
                {
                    public override ImmutableArray<string> FixableDiagnosticIds => 
                        ImmutableArray.Create("MY0001");
                    
                    public override async Task RegisterCodeFixesAsync(CodeFixContext context)
                    {
                        var root = await context.Document.GetSyntaxRootAsync();
                        var diagnostic = context.Diagnostics.First();
                        var diagnosticSpan = diagnostic.Location.SourceSpan;
                        
                        var declaration = root.FindToken(diagnosticSpan.Start)
                            .Parent.AncestorsAndSelf()
                            .OfType<TypeDeclarationSyntax>()
                            .First();
                        
                        context.RegisterCodeFix(
                            CodeAction.Create(
                                title: "Convert to uppercase",
                                createChangedDocument: ct => 
                                    MakeUppercaseAsync(context.Document, declaration, ct),
                                equivalenceKey: "Convert to uppercase"),
                            diagnostic);
                    }
                    
                    private async Task<Document> MakeUppercaseAsync(
                        Document document,
                        TypeDeclarationSyntax typeDecl,
                        CancellationToken cancellationToken)
                    {
                        var oldName = typeDecl.Identifier.Text;
                        var newName = oldName.ToUpperInvariant();
                        
                        var root = await document.GetSyntaxRootAsync(cancellationToken);
                        var newRoot = root.ReplaceNode(
                            typeDecl,
                            typeDecl.WithIdentifier(SyntaxFactory.Identifier(newName)));
                        
                        return document.WithSyntaxRoot(newRoot);
                    }
                }
                """);
        }
        
        static void DemonstrateCuttingEdgeFeatures()
        {
            Console.WriteLine("\n=== 6. Cutting-Edge Features ===\n");
            
            // 1. Native AOT compilation
            Console.WriteLine("1. Native AOT Compilation:");
            Console.WriteLine("""
                Publish as Native AOT:
                // csproj settings
                <PropertyGroup>
                  <PublishAot>true</PublishAot>
                  <SelfContained>true</SelfContained>
                  <RuntimeIdentifier>win-x64</RuntimeIdentifier>
                </PropertyGroup>
                
                // Command line
                dotnet publish -c Release -r win-x64
                
                AOT limitations and workarounds:
                // Reflection is limited
                // Use source generators instead
                // Use [DynamicallyAccessedMembers] attribute
                
                DynamicallyAccessedMembers attribute:
                public class MyClass
                {
                    // Tell the AOT compiler about required members
                    [DynamicallyAccessedMembers(DynamicallyAccessedMemberTypes.PublicProperties)]
                    public Type Type { get; set; }
                    
                    public void Process()
                    {
                        // AOT compiler knows to preserve property metadata
                        var properties = Type.GetProperties();
                    }
                }
                
                Trimming warnings and configuration:
                // .csproj
                <PropertyGroup>
                  <IsTrimmable>true</IsTrimmable>
                  <TrimMode>full</TrimMode>
                  <SuppressTrimAnalysisWarnings>false</SuppressTrimAnalysisWarnings>
                </PropertyGroup>
                
                // Linker configuration file (linker.xml)
                <linker>
                  <assembly fullname="MyAssembly">
                    <type fullname="MyClass" preserve="all" />
                  </assembly>
                </linker>
                """);
            
            // 2. Generic attributes
            Console.WriteLine("\n2. Generic Attributes (C# 11+):");
            Console.WriteLine("""
                Generic attribute definition:
                public class ValidateAttribute<T> : Attribute
                    where T : IValidator
                {
                    public Type ValidatorType => typeof(T);
                }
                
                // Usage
                [Validate<EmailValidator>]
                public string Email { get; set; }
                
                [Validate<RangeValidator<int>>(Min = 0, Max = 100)]
                public int Percentage { get; set; }
                
                Generic attribute with parameters:
                public class CacheAttribute<TKey, TValue> : Attribute
                {
                    public TimeSpan Duration { get; set; }
                    public string CacheRegion { get; set; }
                }
                
                [Cache<string, User>(Duration = "00:05:00", CacheRegion = "Users")]
                public User GetUser(string id) { ... }
                """);
            
            // 3. Raw string literals
            Console.WriteLine("\n3. Raw String Literals (C# 11+):");
            Console.WriteLine("""
                Raw string literals:
                string json = """
                {
                  "name": "John",
                  "age": 30,
                  "address": {
                    "street": "123 Main St",
                    "city": "Anytown"
                  }
                }
                """;
                
                // No escaping needed
                string xml = """
                <root>
                  <element attribute="value">Content & more</element>
                </root>
                """;
                
                Indentation handling:
                string code = """
                public class MyClass
                {
                    public void Method()
                    {
                        Console.WriteLine("Hello");
                    }
                }
                """;
                
                // The closing """ determines the indentation level
                
                Interpolated raw strings:
                string name = "John";
                string greeting = $"""
                Hello, {name}!
                Today is {DateTime.Now:yyyy-MM-dd}.
                """;
                
                Multi-line interpolation:
                string template = $$"""
                {
                  "name": "{{name}}",
                  "timestamp": "{{DateTime.UtcNow:o}}"
                }
                """;
                """);
            
            // 4. Required members and contracts
            Console.WriteLine("\n4. Required Members and Contracts:");
            Console.WriteLine("""
                Required members in constructors:
                public class Person
                {
                    public required string FirstName { get; init; }
                    public required string LastName { get; init; }
                    public DateTime DateOfBirth { get; init; }
                    
                    // Compiler knows constructor sets required members
                    [SetsRequiredMembers]
                    public Person(string firstName, string lastName)
                    {
                        FirstName = firstName;
                        LastName = lastName;
                        DateOfBirth = DateTime.UtcNow;
                    }
                }
                
                Contract-based programming:
                public class Calculator
                {
                    public int Divide(int dividend, int divisor)
                    {
                        // Precondition
                        if (divisor == 0)
                            throw new ArgumentException("Divisor cannot be zero", nameof(divisor));
                        
                        var result = dividend / divisor;
                        
                        // Postcondition
                        Debug.Assert(result * divisor == dividend, 
                            "Division result verification failed");
                        
                        return result;
                    }
                }
                
                Code contracts (System.Diagnostics.Contracts):
                public class Account
                {
                    private decimal _balance;
                    
                    public decimal Balance
                    {
                        get => _balance;
                        set
                        {
                            Contract.Requires(value >= 0, "Balance cannot be negative");
                            _balance = value;
                        }
                    }
                    
                    [ContractInvariantMethod]
                    private void ObjectInvariant()
                    {
                        Contract.Invariant(_balance >= 0);
                    }
                }
                """);
        }
        
        static void DemonstrateRealWorldAdvancedScenarios()
        {
            Console.WriteLine("\n=== 7. Real-World Advanced Scenarios ===\n");
            
            // 1. High-performance parsing
            Console.WriteLine("1. High-Performance Parsing:");
            Console.WriteLine("""
                Zero-allocation JSON parsing with Utf8JsonReader:
                public static int ParseJson(ReadOnlySpan<byte> json)
                {
                    var reader = new Utf8JsonReader(json);
                    int sum = 0;
                    
                    while (reader.Read())
                    {
                        if (reader.TokenType == JsonTokenType.Number)
                        {
                            sum += reader.GetInt32();
                        }
                    }
                    
                    return sum;
                }
                
                Custom text parsing with Span:
                public static int ParseCustomFormat(ReadOnlySpan<char> input)
                {
                    int result = 0;
                    int index = 0;
                    
                    while (index < input.Length)
                    {
                        char c = input[index];
                        
                        if (char.IsDigit(c))
                        {
                            int number = 0;
                            while (index < input.Length && char.IsDigit(input[index]))
                            {
                                number = number * 10 + (input[index] - '0');
                                index++;
                            }
                            result += number;
                        }
                        else
                        {
                            index++;
                        }
                    }
                    
                    return result;
                }
                
                SIMD-accelerated parsing:
                public static unsafe int CountCommas(ReadOnlySpan<byte> data)
                {
                    int count = 0;
                    int vectorSize = Vector<byte>.Count;
                    
                    fixed (byte* ptr = data)
                    {
                        int i = 0;
                        for (; i <= data.Length - vectorSize; i += vectorSize)
                        {
                            var vector = new Vector<byte>(ptr + i);
                            var commaVector = new Vector<byte>((byte)',');
                            var matches = Vector.Equals(vector, commaVector);
                            
                            // Count matches in vector
                            for (int j = 0; j < vectorSize; j++)
                            {
                                if (matches[j] != 0) count++;
                            }
                        }
                        
                        // Handle remaining elements
                        for (; i < data.Length; i++)
                        {
                            if (ptr[i] == (byte)',') count++;
                        }
                    }
                    
                    return count;
                }
                """);
            
            // 2. Custom allocators and memory management
            Console.WriteLine("\n2. Custom Allocators and Memory Management:");
            Console.WriteLine("""
                Pooled array allocator:
                public class PooledArrayAllocator<T>
                {
                    private readonly Stack<T[]> _pool = new();
                    private readonly int _size;
                    
                    public PooledArrayAllocator(int size)
                    {
                        _size = size;
                    }
                    
                    public T[] Rent()
                    {
                        lock (_pool)
                        {
                            return _pool.Count > 0 ? _pool.Pop() : new T[_size];
                        }
                    }
                    
                    public void Return(T[] array)
                    {
                        if (array.Length != _size)
                            throw new ArgumentException("Wrong array size");
                        
                        // Clear if needed
                        Array.Clear(array, 0, array.Length);
                        
                        lock (_pool)
                        {
                            _pool.Push(array);
                        }
                    }
                }
                
                Native memory allocator:
                public sealed class NativeMemoryAllocator : MemoryManager<byte>
                {
                    private readonly IntPtr _pointer;
                    private readonly int _length;
                    private readonly bool _ownsMemory;
                    
                    public NativeMemoryAllocator(int length)
                    {
                        _length = length;
                        _pointer = Marshal.AllocHGlobal(length);
                        _ownsMemory = true;
                    }
                    
                    public override Span<byte> GetSpan()
                    {
                        unsafe
                        {
                            return new Span<byte>(_pointer.ToPointer(), _length);
                        }
                    }
                    
                    public override MemoryHandle Pin(int elementIndex = 0)
                    {
                        unsafe
                        {
                            return new MemoryHandle(
                                (byte*)_pointer.ToPointer() + elementIndex,
                                default,
                                this);
                        }
                    }
                    
                    public override void Unpin() { }
                    
                    protected override void Dispose(bool disposing)
                    {
                        if (_ownsMemory)
                        {
                            Marshal.FreeHGlobal(_pointer);
                        }
                    }
                }
                
                Arena allocator for short-lived objects:
                public class ArenaAllocator : IDisposable
                {
                    private readonly List<IntPtr> _blocks = new();
                    private readonly int _blockSize;
                    private IntPtr _currentBlock;
                    private int _currentOffset;
                    
                    public ArenaAllocator(int blockSize = 4096)
                    {
                        _blockSize = blockSize;
                        AllocateBlock();
                    }
                    
                    public IntPtr Allocate(int size)
                    {
                        if (_currentOffset + size > _blockSize)
                        {
                            AllocateBlock();
                        }
                        
                        var ptr = _currentBlock + _currentOffset;
                        _currentOffset += size;
                        return ptr;
                    }
                    
                    private void AllocateBlock()
                    {
                        _currentBlock = Marshal.AllocHGlobal(_blockSize);
                        _blocks.Add(_currentBlock);
                        _currentOffset = 0;
                    }
                    
                    public void Dispose()
                    {
                        foreach (var block in _blocks)
                        {
                            Marshal.FreeHGlobal(block);
                        }
                        _blocks.Clear();
                    }
                }
                """);
            
            // 3. Advanced concurrency patterns
            Console.WriteLine("\n3. Advanced Concurrency Patterns:");
            Console.WriteLine("""
                Actor model with Channels:
                public class Actor<T>
                {
                    private readonly Channel<T> _inbox = Channel.CreateUnbounded<T>();
                    private readonly Func<T, Task> _handler;
                    
                    public Actor(Func<T, Task> handler)
                    {
                        _handler = handler;
                        Task.Run(RunAsync);
                    }
                    
                    public async Task SendAsync(T message)
                    {
                        await _inbox.Writer.WriteAsync(message);
                    }
                    
                    private async Task RunAsync()
                    {
                        await foreach (var message in _inbox.Reader.ReadAllAsync())
                        {
                            try
                            {
                                await _handler(message);
                            }
                            catch (Exception ex)
                            {
                                // Handle error
                            }
                        }
                    }
                }
                
                Lock-free data structures:
                public class LockFreeStack<T>
                {
                    private sealed class Node
                    {
                        public readonly T Value;
                        public Node Next;
                        
                        public Node(T value)
                        {
                            Value = value;
                        }
                    }
                    
                    private Node _head;
                    
                    public void Push(T value)
                    {
                        var newNode = new Node(value);
                        
                        do
                        {
                            newNode.Next = _head;
                        }
                        while (Interlocked.CompareExchange(ref _head, newNode, newNode.Next) != newNode.Next);
                    }
                    
                    public bool TryPop(out T value)
                    {
                        Node oldHead;
                        
                        do
                        {
                            oldHead = _head;
                            if (oldHead == null)
                            {
                                value = default;
                                return false;
                            }
                        }
                        while (Interlocked.CompareExchange(ref _head, oldHead.Next, oldHead) != oldHead);
                        
                        value = oldHead.Value;
                        return true;
                    }
                }
                
                Concurrent priority queue:
                public class ConcurrentPriorityQueue<T>
                {
                    private readonly SortedDictionary<int, ConcurrentQueue<T>> _queues = new();
                    private readonly object _lock = new();
                    private int _count;
                    
                    public void Enqueue(int priority, T item)
                    {
                        lock (_lock)
                        {
                            if (!_queues.TryGetValue(priority, out var queue))
                            {
                                queue = new ConcurrentQueue<T>();
                                _queues[priority] = queue;
                            }
                            queue.Enqueue(item);
                            _count++;
                            Monitor.Pulse(_lock);
                        }
                    }
                    
                    public bool TryDequeue(out T item, out int priority)
                    {
                        lock (_lock)
                        {
                            while (_count == 0)
                            {
                                Monitor.Wait(_lock);
                            }
                            
                            var highestPriority = _queues.Keys.Min();
                            var queue = _queues[highestPriority];
                            
                            if (queue.TryDequeue(out item))
                            {
                                priority = highestPriority;
                                _count--;
                                
                                if (queue.IsEmpty)
                                {
                                    _queues.Remove(highestPriority);
                                }
                                
                                return true;
                            }
                            
                            priority = -1;
                            return false;
                        }
                    }
                }
                """);
            
            // 4. Real-time systems and performance monitoring
            Console.WriteLine("\n4. Real-Time Systems and Performance Monitoring:");
            Console.WriteLine("""
                High-resolution timing:
                public class HighResTimer
                {
                    private readonly long _frequency;
                    
                    public HighResTimer()
                    {
                        _frequency = Stopwatch.Frequency;
                    }
                    
                    public long GetTimestamp() => Stopwatch.GetTimestamp();
                    
                    public double GetElapsedSeconds(long start, long end)
                    {
                        return (end - start) / (double)_frequency;
                    }
                    
                    public void Measure(Action action, out long ticks, out double seconds)
                    {
                        var start = GetTimestamp();
                        action();
                        var end = GetTimestamp();
                        
                        ticks = end - start;
                        seconds = GetElapsedSeconds(start, end);
                    }
                }
                
                Performance counters:
                public class PerformanceMonitor : IDisposable
                {
                    private readonly PerformanceCounter _cpuCounter;
                    private readonly PerformanceCounter _memoryCounter;
                    private readonly Timer _timer;
                    
                    public event Action<float> CpuUsageUpdated;
                    public event Action<float> MemoryUsageUpdated;
                    
                    public PerformanceMonitor()
                    {
                        _cpuCounter = new PerformanceCounter(
                            "Processor", "% Processor Time", "_Total");
                        _memoryCounter = new PerformanceCounter(
                            "Memory", "Available MBytes");
                        
                        _timer = new Timer(UpdateCounters, null, 1000, 1000);
                    }
                    
                    private void UpdateCounters(object state)
                    {
                        var cpuUsage = _cpuCounter.NextValue();
                        var availableMemory = _memoryCounter.NextValue();
                        
                        CpuUsageUpdated?.Invoke(cpuUsage);
                        MemoryUsageUpdated?.Invoke(availableMemory);
                    }
                    
                    public void Dispose()
                    {
                        _timer?.Dispose();
                        _cpuCounter?.Dispose();
                        _memoryCounter?.Dispose();
                    }
                }
                
                GC latency mode for real-time:
                public class RealTimeComponent : IDisposable
                {
                    private GCLatencyMode _originalMode;
                    
                    public RealTimeComponent()
                    {
                        // Request low-latency GC
                        _originalMode = GCSettings.LatencyMode;
                        GCSettings.LatencyMode = GCLatencyMode.LowLatency;
                    }
                    
                    public void Process()
                    {
                        // Critical real-time processing
                        // GC will be less intrusive
                    }
                    
                    public void Dispose()
                    {
                        // Restore original GC mode
                        GCSettings.LatencyMode = _originalMode;
                        
                        // Force full GC if needed
                        if (_originalMode != GCLatencyMode.LowLatency)
                        {
                            GC.Collect();
                        }
                    }
                }
                """);
        }
    }
    
    // Supporting classes and interfaces for examples
    
    public class Person
    {
        public string Name { get; set; }
        public int Age { get; set; }
    }
    
    public record PersonRecord(string FirstName, string LastName, int Age);
    
    public readonly record struct Point(int X, int Y);
    
    public interface IValidator { }
    public class EmailValidator : IValidator { }
    public class RangeValidator<T> : IValidator where T : IComparable<T>
    {
        public T Min { get; set; }
        public T Max { get; set; }
    }
    
    public interface IMyEvents { }
    public interface IMyClass { }
    
    public struct Vector3
    {
        public float X { get; }
        public float Y { get; }
        public float Z { get; }
        
        public Vector3(float x, float y, float z)
        {
            X = x;
            Y = y;
            Z = z;
        }
    }
    
    public class User
    {
        public string Id { get; set; }
        public string Name { get; set; }
    }
    
    // Mock methods for examples
    public static class ExampleMethods
    {
        public static string GetPossiblyNullString() => "test";
        public static string GetString() => "test";
        public static Task<int> ComputeExpensiveResultAsync() => Task.FromResult(42);
        public static Task ProcessItemAsync(int item) => Task.CompletedTask;
        public static Task ProcessAsync(Memory<byte> memory) => Task.CompletedTask;
        public static Task LongRunningOperationAsync(CancellationToken ct) => Task.CompletedTask;
        public static Task SomeAsyncMethod() => Task.CompletedTask;
        public static Task<int> ProcessAsync(int x) => Task.FromResult(x * 2);
        public static void ProcessBuffer(Span<byte> buffer) { }
        public static int ProcessData(byte* data, int length) => 0;
    }
    
    // AutoGenerate attribute for source generator example
    [AttributeUsage(AttributeTargets.Class)]
    public class AutoGenerateAttribute : Attribute { }
}
