/*
    C# DELEGATES AND EVENTS
    File: 09_delegates_events.cs
    
    This file demonstrates delegates and events in C# programming,
    covering concepts from junior to upper mid-level. Delegates are
    type-safe function pointers, and events provide a way to implement
    the observer pattern with built-in language support.
    
    Key Concepts Covered:
    1. Delegate Declaration and Instantiation
    2. Multicast Delegates and Method Chaining
    3. Anonymous Methods and Lambda Expressions
    4. Built-in Delegate Types (Func, Action, Predicate)
    5. Event Declaration and Subscription
    6. Event Accessors (add/remove)
    7. Custom EventArgs and Event Patterns
    8. EventHandler<T> Delegate
    9. Weak Event Patterns
    10. Real-world Event-driven Patterns
*/

using System;
using System.Collections.Generic;

namespace CSharpRefresher.DelegatesEvents
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Delegates and Events Demonstration ===\n");
            
            DemonstrateBasicDelegates();
            DemonstrateMulticastDelegates();
            DemonstrateBuiltInDelegates();
            DemonstrateBasicEvents();
            DemonstrateEventPatterns();
            DemonstrateEventHandlerGeneric();
            DemonstrateWeakEvents();
            DemonstrateRealWorldPatterns();
            
            Console.WriteLine("\n=== Delegates and Events Complete ===");
        }
        
        static void DemonstrateBasicDelegates()
        {
            Console.WriteLine("============ BASIC DELEGATES ============\n");
            
            // ============ DELEGATE DECLARATION ============
            Console.WriteLine("=== 1. Delegate Declaration ===");
            
            // Delegate declaration (defines a signature)
            delegate int MathOperation(int x, int y);
            delegate void LogMessage(string message);
            delegate bool FilterPredicate(int number);
            
            // Methods matching delegate signatures
            int Add(int a, int b) => a + b;
            int Multiply(int a, int b) => a * b;
            void ConsoleLog(string msg) => Console.WriteLine($"[LOG] {msg}");
            bool IsEven(int n) => n % 2 == 0;
            bool IsPositive(int n) => n > 0;
            
            // ============ DELEGATE INSTANTIATION ============
            Console.WriteLine("\n=== 2. Delegate Instantiation ===");
            
            // Create delegate instances
            MathOperation addDelegate = new MathOperation(Add);
            MathOperation multiplyDelegate = Multiply; // Shorthand syntax
            
            // Invoke delegates
            int sum = addDelegate(5, 3);
            int product = multiplyDelegate(5, 3);
            
            Console.WriteLine($"Add(5, 3) = {sum}");
            Console.WriteLine($"Multiply(5, 3) = {product}");
            
            // Delegate as parameter
            int Calculate(MathOperation operation, int x, int y) => operation(x, y);
            Console.WriteLine($"Calculate(Add, 10, 20) = {Calculate(Add, 10, 20)}");
            Console.WriteLine($"Calculate(Multiply, 10, 20) = {Calculate(Multiply, 10, 20)}");
            
            // ============ DELEGATES AS FIRST-CLASS CITIZENS ============
            Console.WriteLine("\n=== 3. Delegates as First-Class Citizens ===");
            
            // Store delegates in collections
            List<MathOperation> operations = new List<MathOperation> { Add, Multiply };
            
            foreach (var op in operations)
            {
                Console.WriteLine($"Operation(6, 7) = {op(6, 7)}");
            }
            
            // Return delegate from method
            MathOperation GetOperation(string operationType)
            {
                return operationType.ToLower() switch
                {
                    "add" => Add,
                    "multiply" => Multiply,
                    _ => throw new ArgumentException("Invalid operation")
                };
            }
            
            MathOperation selectedOp = GetOperation("add");
            Console.WriteLine($"Selected operation: {selectedOp(8, 9)}");
            
            // ============ DELEGATE INVOCATION PATTERNS ============
            Console.WriteLine("\n=== 4. Delegate Invocation Patterns ===");
            
            // Traditional invocation
            int result1 = addDelegate.Invoke(15, 25);
            Console.WriteLine($"Invoke result: {result1}");
            
            // Null-conditional invocation
            MathOperation? nullableDelegate = null;
            int? result2 = nullableDelegate?.Invoke(1, 2); // Returns null, doesn't throw
            Console.WriteLine($"Null-conditional result: {result2}");
            
            // Safe invocation pattern
            if (addDelegate != null)
            {
                int result3 = addDelegate(30, 40);
                Console.WriteLine($"Safe invocation result: {result3}");
            }
        }
        
        static void DemonstrateMulticastDelegates()
        {
            Console.WriteLine("\n============ MULTICAST DELEGATES ============\n");
            
            // ============ MULTICAST DELEGATE BASICS ============
            Console.WriteLine("=== 1. Multicast Delegate Basics ===");
            
            delegate void NotificationHandler(string recipient, string message);
            
            void EmailNotify(string recipient, string message) 
                => Console.WriteLine($"Email to {recipient}: {message}");
            void SMSNotify(string recipient, string message) 
                => Console.WriteLine($"SMS to {recipient}: {message}");
            void PushNotify(string recipient, string message) 
                => Console.WriteLine($"Push to {recipient}: {message}");
            
            // Create multicast delegate
            NotificationHandler notify = EmailNotify;
            notify += SMSNotify;  // Add another method
            notify += PushNotify; // Add another method
            
            Console.WriteLine("Multicast delegate invocation:");
            notify("alice@example.com", "Hello!");
            
            // ============ DELEGATE COMBINATION ============
            Console.WriteLine("\n=== 2. Delegate Combination ===");
            
            NotificationHandler emailOnly = EmailNotify;
            NotificationHandler smsOnly = SMSNotify;
            
            // Combine delegates
            NotificationHandler combined = emailOnly + smsOnly;
            Console.WriteLine("Combined delegate:");
            combined("bob@example.com", "Combined notification");
            
            // Remove delegate
            combined -= emailOnly;
            Console.WriteLine("\nAfter removing email:");
            combined("bob@example.com", "SMS only");
            
            // ============ DELEGATE INVOCATION LIST ============
            Console.WriteLine("\n=== 3. Delegate Invocation List ===");
            
            Console.WriteLine($"Notification delegate method count: {notify.GetInvocationList().Length}");
            
            // Manual invocation with control
            foreach (NotificationHandler handler in notify.GetInvocationList())
            {
                try
                {
                    handler("charlie@example.com", "Individual invocation");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Handler failed: {ex.Message}");
                }
            }
            
            // ============ MULTICAST RETURN VALUES ============
            Console.WriteLine("\n=== 4. Multicast Return Values ===");
            
            delegate int NumberProcessor(int x);
            
            int Double(int x) => x * 2;
            int Square(int x) => x * x;
            int Increment(int x) => x + 1;
            
            NumberProcessor processor = Double;
            processor += Square;
            processor += Increment;
            
            // Only returns last result
            int lastResult = processor(5);
            Console.WriteLine($"Multicast returns last result only: {lastResult}");
            
            // Get all results
            int input = 5;
            foreach (NumberProcessor p in processor.GetInvocationList())
            {
                Console.WriteLine($"Processor result: {p(input)}");
            }
            
            // ============ EXCEPTION HANDLING ============
            Console.WriteLine("\n=== 5. Exception Handling in Multicast ===");
            
            delegate void RiskyOperation();
            
            void SafeMethod() => Console.WriteLine("Safe method executed");
            void RiskyMethod() => throw new InvalidOperationException("Something went wrong!");
            void AnotherSafeMethod() => Console.WriteLine("Another safe method executed");
            
            RiskyOperation riskyOp = SafeMethod;
            riskyOp += RiskyMethod;
            riskyOp += AnotherSafeMethod;
            
            try
            {
                riskyOp(); // Stops at first exception
            }
            catch (InvalidOperationException ex)
            {
                Console.WriteLine($"Caught exception: {ex.Message}");
                Console.WriteLine("Note: AnotherSafeMethod was never called!");
            }
            
            // Safe pattern
            foreach (RiskyOperation op in riskyOp.GetInvocationList())
            {
                try
                {
                    op();
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Operation failed: {ex.Message}");
                }
            }
        }
        
        static void DemonstrateBuiltInDelegates()
        {
            Console.WriteLine("\n============ BUILT-IN DELEGATES ============\n");
            
            // ============ ACTION DELEGATE ============
            Console.WriteLine("=== 1. Action Delegate (void return) ===");
            
            // Action - no parameters, void return
            Action simpleAction = () => Console.WriteLine("Simple action");
            simpleAction();
            
            // Action with parameters
            Action<string, int> parameterAction = (name, age) => 
                Console.WriteLine($"{name} is {age} years old");
            parameterAction("Alice", 30);
            
            // Action with up to 16 parameters
            Action<int, int, int, int> multiParamAction = (a, b, c, d) =>
                Console.WriteLine($"Sum: {a + b + c + d}");
            multiParamAction(1, 2, 3, 4);
            
            // ============ FUNC DELEGATE ============
            Console.WriteLine("\n=== 2. Func Delegate (with return value) ===");
            
            // Func with return value
            Func<int> getNumber = () => 42;
            Console.WriteLine($"GetNumber: {getNumber()}");
            
            // Func with parameters and return
            Func<int, int, int> addFunc = (x, y) => x + y;
            Func<int, int, int> multiplyFunc = (x, y) => x * y;
            
            Console.WriteLine($"Add: {addFunc(5, 3)}");
            Console.WriteLine($"Multiply: {multiplyFunc(5, 3)}");
            
            // Func with multiple parameters
            Func<string, int, bool, string> complexFunc = (name, count, flag) =>
                flag ? $"{name} has {count} items" : "No items";
            
            Console.WriteLine($"Complex func: {complexFunc("Alice", 5, true)}");
            
            // ============ PREDICATE DELEGATE ============
            Console.WriteLine("\n=== 3. Predicate Delegate (bool return) ===");
            
            // Predicate - always returns bool
            Predicate<int> isEven = x => x % 2 == 0;
            Predicate<string> isLong = s => s.Length > 5;
            
            List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
            List<string> words = new List<string> { "apple", "banana", "cherry", "date", "elderberry" };
            
            // Use with List methods
            int firstEven = numbers.Find(isEven);
            List<int> allEven = numbers.FindAll(isEven);
            bool anyLong = words.Exists(isLong);
            
            Console.WriteLine($"First even: {firstEven}");
            Console.WriteLine($"All even: {string.Join(", ", allEven)}");
            Console.WriteLine($"Any long words: {anyLong}");
            
            // ============ COMPARISON DELEGATE ============
            Console.WriteLine("\n=== 4. Comparison Delegate ===");
            
            // Comparison<T> - compares two objects
            Comparison<string> lengthComparison = (s1, s2) => s1.Length.CompareTo(s2.Length);
            
            List<string> fruits = new List<string> { "apple", "banana", "cherry", "date", "elderberry" };
            fruits.Sort(lengthComparison);
            Console.WriteLine($"Sorted by length: {string.Join(", ", fruits)}");
            
            // ============ CONVERTER DELEGATE ============
            Console.WriteLine("\n=== 5. Converter Delegate ===");
            
            // Converter<TInput, TOutput> - converts one type to another
            Converter<int, string> intToString = x => $"Number: {x}";
            
            List<int> ints = new List<int> { 1, 2, 3, 4, 5 };
            List<string> strings = ints.ConvertAll(intToString);
            Console.WriteLine($"Converted: {string.Join(", ", strings)}");
            
            // ============ REAL-WORLD USAGE ============
            Console.WriteLine("\n=== 6. Real-world Usage ===");
            
            // LINQ extensively uses Func delegates
            var evenNumbers = numbers.Where(x => x % 2 == 0); // Func<int, bool>
            var squared = numbers.Select(x => x * x);         // Func<int, int>
            
            Console.WriteLine($"Even numbers: {string.Join(", ", evenNumbers)}");
            Console.WriteLine($"Squared: {string.Join(", ", squared)}");
            
            // Task uses Action and Func
            Action backgroundWork = () => Console.WriteLine("Working in background");
            Func<int> computeResult = () => { Console.WriteLine("Computing"); return 100; };
        }
        
        static void DemonstrateBasicEvents()
        {
            Console.WriteLine("\n============ BASIC EVENTS ============\n");
            
            // ============ EVENT DECLARATION ============
            Console.WriteLine("=== 1. Event Declaration ===");
            
            class Button
            {
                // Event declaration
                public event EventHandler Clicked;
                
                // Method to raise the event
                public void OnClick()
                {
                    Console.WriteLine("Button clicked, raising event...");
                    Clicked?.Invoke(this, EventArgs.Empty);
                }
            }
            
            class Thermostat
            {
                private double temperature;
                
                // Event with custom delegate
                public delegate void TemperatureChangedHandler(double newTemperature);
                public event TemperatureChangedHandler TemperatureChanged;
                
                public double Temperature
                {
                    get => temperature;
                    set
                    {
                        if (temperature != value)
                        {
                            temperature = value;
                            TemperatureChanged?.Invoke(temperature);
                        }
                    }
                }
            }
            
            // ============ EVENT SUBSCRIPTION ============
            Console.WriteLine("\n=== 2. Event Subscription ===");
            
            Button button = new Button();
            
            // Subscribe with method
            void Button_Clicked(object sender, EventArgs e)
            {
                Console.WriteLine("Button was clicked!");
            }
            
            button.Clicked += Button_Clicked;
            
            // Subscribe with lambda
            button.Clicked += (sender, e) => 
                Console.WriteLine("Lambda handler: Button clicked!");
            
            // Subscribe with anonymous method
            button.Clicked += delegate (object sender, EventArgs e)
            {
                Console.WriteLine("Anonymous method: Button clicked!");
            };
            
            // Raise event
            button.OnClick();
            
            // ============ EVENT UNSUSCRIPTION ============
            Console.WriteLine("\n=== 3. Event Unsubscription ===");
            
            // Store reference for unsubscription
            EventHandler storedHandler = (sender, e) => 
                Console.WriteLine("Stored handler");
            
            button.Clicked += storedHandler;
            Console.WriteLine("After adding stored handler:");
            button.OnClick();
            
            // Unsubscribe
            button.Clicked -= storedHandler;
            Console.WriteLine("\nAfter removing stored handler:");
            button.OnClick();
            
            // Cannot unsubscribe anonymous methods/lambdas without reference
            // button.Clicked -= (sender, e) => Console.WriteLine("Can't remove this");
            
            // ============ THERMOSTAT EXAMPLE ============
            Console.WriteLine("\n=== 4. Thermostat Example ===");
            
            Thermostat thermostat = new Thermostat();
            
            thermostat.TemperatureChanged += temp => 
                Console.WriteLine($"Temperature changed to: {temp}°C");
            
            thermostat.TemperatureChanged += temp =>
            {
                if (temp > 30) Console.WriteLine("Warning: Too hot!");
                else if (temp < 10) Console.WriteLine("Warning: Too cold!");
            };
            
            Console.WriteLine("Changing thermostat temperature:");
            thermostat.Temperature = 20;
            thermostat.Temperature = 35;
            thermostat.Temperature = 5;
            
            // ============ EVENT ACCESSORS ============
            Console.WriteLine("\n=== 5. Event Accessors (add/remove) ===");
            
            class EventSource
            {
                private EventHandler myEvent;
                
                public event EventHandler MyEvent
                {
                    add
                    {
                        Console.WriteLine($"Adding handler: {value.Method.Name}");
                        myEvent += value;
                    }
                    remove
                    {
                        Console.WriteLine($"Removing handler: {value.Method.Name}");
                        myEvent -= value;
                    }
                }
                
                public void RaiseEvent()
                {
                    myEvent?.Invoke(this, EventArgs.Empty);
                }
            }
            
            EventSource source = new EventSource();
            source.MyEvent += (s, e) => Console.WriteLine("Handler 1");
            source.MyEvent += (s, e) => Console.WriteLine("Handler 2");
            
            Console.WriteLine("Raising custom event:");
            source.RaiseEvent();
            
            source.MyEvent -= (s, e) => Console.WriteLine("Handler 1");
            Console.WriteLine("\nAfter removing handler:");
            source.RaiseEvent();
        }
        
        static void DemonstrateEventPatterns()
        {
            Console.WriteLine("\n============ EVENT PATTERNS ============\n");
            
            // ============ STANDARD EVENT PATTERN ============
            Console.WriteLine("=== 1. Standard Event Pattern ===");
            
            // Custom EventArgs
            class OrderEventArgs : EventArgs
            {
                public string OrderId { get; }
                public decimal Amount { get; }
                public DateTime OrderDate { get; }
                
                public OrderEventArgs(string orderId, decimal amount, DateTime orderDate)
                {
                    OrderId = orderId;
                    Amount = amount;
                    OrderDate = orderDate;
                }
            }
            
            class OrderProcessor
            {
                // Event with custom EventArgs
                public event EventHandler<OrderEventArgs> OrderProcessed;
                
                public void ProcessOrder(string orderId, decimal amount)
                {
                    Console.WriteLine($"Processing order {orderId} for ${amount}");
                    
                    // Simulate processing
                    Thread.Sleep(100);
                    
                    // Raise event
                    OnOrderProcessed(new OrderEventArgs(orderId, amount, DateTime.Now));
                }
                
                protected virtual void OnOrderProcessed(OrderEventArgs e)
                {
                    OrderProcessed?.Invoke(this, e);
                }
            }
            
            OrderProcessor processor = new OrderProcessor();
            processor.OrderProcessed += (sender, e) =>
            {
                Console.WriteLine($"Order processed: {e.OrderId}, Amount: ${e.Amount}, Date: {e.OrderDate:g}");
            };
            
            Console.WriteLine("Processing orders:");
            processor.ProcessOrder("ORD001", 99.99m);
            processor.ProcessOrder("ORD002", 149.99m);
            
            // ============ EVENT HANDLER DELEGATE ============
            Console.WriteLine("\n=== 2. EventHandler<T> Delegate ===");
            
            class TemperatureEventArgs : EventArgs
            {
                public double OldTemperature { get; }
                public double NewTemperature { get; }
                
                public TemperatureEventArgs(double oldTemp, double newTemp)
                {
                    OldTemperature = oldTemp;
                    NewTemperature = newTemp;
                }
            }
            
            class SmartThermostat
            {
                private double temperature;
                
                public event EventHandler<TemperatureEventArgs> TemperatureChanged;
                
                public double Temperature
                {
                    get => temperature;
                    set
                    {
                        if (temperature != value)
                        {
                            double oldTemp = temperature;
                            temperature = value;
                            OnTemperatureChanged(oldTemp, temperature);
                        }
                    }
                }
                
                protected virtual void OnTemperatureChanged(double oldTemp, double newTemp)
                {
                    TemperatureChanged?.Invoke(this, new TemperatureEventArgs(oldTemp, newTemp));
                }
            }
            
            SmartThermostat smartThermo = new SmartThermostat();
            smartThermo.TemperatureChanged += (sender, e) =>
            {
                Console.WriteLine($"Temperature changed from {e.OldTemperature}°C to {e.NewTemperature}°C");
                Console.WriteLine($"Change: {e.NewTemperature - e.OldTemperature:+#;-#;0}°C");
            };
            
            smartThermo.Temperature = 20;
            smartThermo.Temperature = 25;
            smartThermo.Temperature = 18;
            
            // ============ CANCELLABLE EVENTS ============
            Console.WriteLine("\n=== 3. Cancellable Events ===");
            
            class CancellableEventArgs : EventArgs
            {
                public bool Cancel { get; set; }
                public string Reason { get; set; }
                
                public CancellableEventArgs()
                {
                    Cancel = false;
                    Reason = string.Empty;
                }
            }
            
            class DocumentEditor
            {
                public event EventHandler<CancellableEventArgs> BeforeSave;
                
                public void SaveDocument(string content)
                {
                    var args = new CancellableEventArgs();
                    BeforeSave?.Invoke(this, args);
                    
                    if (args.Cancel)
                    {
                        Console.WriteLine($"Save cancelled: {args.Reason}");
                        return;
                    }
                    
                    Console.WriteLine($"Saving document: {content}");
                }
            }
            
            DocumentEditor editor = new DocumentEditor();
            editor.BeforeSave += (sender, e) =>
            {
                // Validate before saving
                if (string.IsNullOrEmpty(e.Reason))
                {
                    e.Cancel = true;
                    e.Reason = "Document must have a reason for save";
                }
            };
            
            Console.WriteLine("Trying to save document:");
            editor.SaveDocument("Important notes");
            
            // ============ EVENT CHAINING ============
            Console.WriteLine("\n=== 4. Event Chaining ===");
            
            class Sensor
            {
                public event EventHandler<int> ReadingChanged;
                
                public void SimulateReading(int value)
                {
                    Console.WriteLine($"Sensor reading: {value}");
                    ReadingChanged?.Invoke(this, value);
                }
            }
            
            class DataLogger
            {
                public event EventHandler<string> LogEntryAdded;
                
                public void LogSensorReading(object sender, int reading)
                {
                    string logEntry = $"[{DateTime.Now:HH:mm:ss}] Sensor reading: {reading}";
                    Console.WriteLine($"Logging: {logEntry}");
                    LogEntryAdded?.Invoke(this, logEntry);
                }
            }
            
            class AlertSystem
            {
                public void CheckForAlert(object sender, string logEntry)
                {
                    if (logEntry.Contains("Sensor reading: 100"))
                    {
                        Console.WriteLine("ALERT: Critical sensor reading detected!");
                    }
                }
            }
            
            Sensor sensor = new Sensor();
            DataLogger logger = new DataLogger();
            AlertSystem alerts = new AlertSystem();
            
            // Chain events
            sensor.ReadingChanged += logger.LogSensorReading;
            logger.LogEntryAdded += alerts.CheckForAlert;
            
            Console.WriteLine("Sensor event chain:");
            sensor.SimulateReading(50);
            sensor.SimulateReading(75);
            sensor.SimulateReading(100); // Should trigger alert
        }
        
        static void DemonstrateEventHandlerGeneric()
        {
            Console.WriteLine("\n============ EVENTHANDLER<T> GENERIC ============\n");
            
            // ============ EVENTHANDLER<T> ADVANTAGES ============
            Console.WriteLine("=== 1. EventHandler<T> Advantages ===");
            Console.WriteLine("""
                EventHandler<TEventArgs> provides:
                • Type safety with custom EventArgs
                • No need for custom delegate declarations
                • Standard pattern used throughout .NET
                • Better tooling support
                """);
            
            // ============ PRACTICAL EXAMPLE ============
            Console.WriteLine("\n=== 2. Practical Example ===");
            
            class FileOperationEventArgs : EventArgs
            {
                public string FilePath { get; }
                public long FileSize { get; }
                public DateTime Timestamp { get; }
                
                public FileOperationEventArgs(string filePath, long fileSize)
                {
                    FilePath = filePath;
                    FileSize = fileSize;
                    Timestamp = DateTime.Now;
                }
            }
            
            class FileWatcher
            {
                public event EventHandler<FileOperationEventArgs> FileCreated;
                public event EventHandler<FileOperationEventArgs> FileModified;
                public event EventHandler<FileOperationEventArgs> FileDeleted;
                
                public void SimulateFileCreate(string path, long size)
                {
                    Console.WriteLine($"File created: {path}");
                    FileCreated?.Invoke(this, new FileOperationEventArgs(path, size));
                }
                
                public void SimulateFileModify(string path, long size)
                {
                    Console.WriteLine($"File modified: {path}");
                    FileModified?.Invoke(this, new FileOperationEventArgs(path, size));
                }
                
                public void SimulateFileDelete(string path)
                {
                    Console.WriteLine($"File deleted: {path}");
                    FileDeleted?.Invoke(this, new FileOperationEventArgs(path, 0));
                }
            }
            
            FileWatcher watcher = new FileWatcher();
            
            // Subscribe to events
            watcher.FileCreated += (sender, e) =>
                Console.WriteLine($"Created: {e.FilePath} ({e.FileSize} bytes) at {e.Timestamp:HH:mm:ss}");
            
            watcher.FileModified += (sender, e) =>
                Console.WriteLine($"Modified: {e.FilePath} ({e.FileSize} bytes) at {e.Timestamp:HH:mm:ss}");
            
            watcher.FileDeleted += (sender, e) =>
                Console.WriteLine($"Deleted: {e.FilePath} at {e.Timestamp:HH:mm:ss}");
            
            Console.WriteLine("File operations:");
            watcher.SimulateFileCreate("document.txt", 1024);
            watcher.SimulateFileModify("document.txt", 2048);
            watcher.SimulateFileDelete("document.txt");
            
            // ============ NULLABLE REFERENCE TYPES ============
            Console.WriteLine("\n=== 3. Nullable Reference Types ===");
            
            class ModernEventArgs : EventArgs
            {
                public string? OptionalMessage { get; }
                public int RequiredValue { get; }
                
                public ModernEventArgs(int requiredValue, string? optionalMessage = null)
                {
                    RequiredValue = requiredValue;
                    OptionalMessage = optionalMessage;
                }
            }
            
            class ModernEventSource
            {
                public event EventHandler<ModernEventArgs>? ModernEvent; // Nullable event
                
                public void DoWork()
                {
                    // Check for null subscribers
                    if (ModernEvent != null)
                    {
                        ModernEvent(this, new ModernEventArgs(42, "Hello"));
                    }
                    
                    // Or use null-conditional
                    ModernEvent?.Invoke(this, new ModernEventArgs(100));
                }
            }
            
            // ============ ASYNC EVENT HANDLERS ============
            Console.WriteLine("\n=== 4. Async Event Handlers ===");
            
            class AsyncEventSource
            {
                public event EventHandler<EventArgs>? AsyncEvent;
                
                public async Task RaiseEventAsync()
                {
                    var handlers = AsyncEvent?.GetInvocationList();
                    if (handlers == null) return;
                    
                    foreach (EventHandler<EventArgs> handler in handlers)
                    {
                        // Fire and forget or await as needed
                        Task.Run(() => handler(this, EventArgs.Empty));
                    }
                    
                    await Task.Delay(100); // Simulate async work
                }
            }
            
            Console.WriteLine("Note: Events are synchronous by default. For async,");
            Console.WriteLine("consider using async method calls within handlers.");
        }
        
        static void DemonstrateWeakEvents()
        {
            Console.WriteLine("\n============ WEAK EVENT PATTERNS ============\n");
            
            // ============ MEMORY LEAK PROBLEM ============
            Console.WriteLine("=== 1. Memory Leak Problem ===");
            
            class Publisher
            {
                public event EventHandler? Event;
                
                public void RaiseEvent()
                {
                    Event?.Invoke(this, EventArgs.Empty);
                }
            }
            
            class Subscriber
            {
                private string name;
                
                public Subscriber(string name)
                {
                    this.name = name;
                }
                
                public void HandleEvent(object? sender, EventArgs e)
                {
                    Console.WriteLine($"{name} received event");
                }
            }
            
            Console.WriteLine("Creating publisher and subscriber...");
            var publisher = new Publisher();
            
            // This creates a strong reference, causing memory leak if not unsubscribed
            var subscriber = new Subscriber("Subscriber1");
            publisher.Event += subscriber.HandleEvent;
            
            Console.WriteLine("Raising event with subscriber...");
            publisher.RaiseEvent();
            
            // Even if we null the subscriber, it won't be GC'd due to event reference
            subscriber = null;
            GC.Collect();
            GC.WaitForPendingFinalizers();
            
            Console.WriteLine("Event still has reference to handler");
            publisher.RaiseEvent();
            
            // ============ WEAK EVENT PATTERN ============
            Console.WriteLine("\n=== 2. Weak Event Pattern ===");
            
            class WeakEventPublisher
            {
                private List<WeakReference<EventHandler>> weakHandlers = new List<WeakReference<EventHandler>>();
                
                public event EventHandler WeakEvent
                {
                    add
                    {
                        weakHandlers.Add(new WeakReference<EventHandler>(value));
                    }
                    remove
                    {
                        // Complex removal - simplified for example
                        for (int i = weakHandlers.Count - 1; i >= 0; i--)
                        {
                            if (weakHandlers[i].TryGetTarget(out var handler) && handler == value)
                            {
                                weakHandlers.RemoveAt(i);
                            }
                        }
                    }
                }
                
                public void RaiseWeakEvent()
                {
                    // Clean up dead references
                    for (int i = weakHandlers.Count - 1; i >= 0; i--)
                    {
                        if (!weakHandlers[i].TryGetTarget(out _))
                        {
                            weakHandlers.RemoveAt(i);
                        }
                    }
                    
                    // Invoke remaining handlers
                    foreach (var weakRef in weakHandlers)
                    {
                        if (weakRef.TryGetTarget(out var handler))
                        {
                            handler(this, EventArgs.Empty);
                        }
                    }
                }
            }
            
            // ============ WEAK EVENT MANAGER ============
            Console.WriteLine("\n=== 3. WeakEventManager (.NET) ===");
            
            Console.WriteLine("""
                In WPF/.NET, use WeakEventManager:
                
                // In publisher
                WeakEventManager<MyPublisher, EventArgs>
                    .AddHandler(this, nameof(MyEvent), handler);
                
                // In subscriber
                WeakEventManager<MyPublisher, EventArgs>
                    .RemoveHandler(source, nameof(MyEvent), handler);
                
                This pattern prevents memory leaks in UI applications
                where objects have different lifetimes.
                """);
            
            // ============ MANUAL WEAK REFERENCE ============
            Console.WriteLine("\n=== 4. Manual Weak Reference ===");
            
            class ManualWeakEvent
            {
                private WeakReference<EventHandler>? weakHandler;
                
                public event EventHandler ManualEvent
                {
                    add
                    {
                        weakHandler = new WeakReference<EventHandler>(value);
                    }
                    remove
                    {
                        if (weakHandler != null && weakHandler.TryGetTarget(out var handler) && handler == value)
                        {
                            weakHandler = null;
                        }
                    }
                }
                
                public void RaiseManualEvent()
                {
                    if (weakHandler != null && weakHandler.TryGetTarget(out var handler))
                    {
                        handler(this, EventArgs.Empty);
                    }
                    else
                    {
                        Console.WriteLine("Handler was garbage collected");
                    }
                }
            }
            
            ManualWeakEvent manualEvent = new ManualWeakEvent();
            var tempSubscriber = new Subscriber("TempSubscriber");
            manualEvent.ManualEvent += tempSubscriber.HandleEvent;
            
            Console.WriteLine("First raise:");
            manualEvent.RaiseManualEvent();
            
            Console.WriteLine("After nulling subscriber and GC:");
            tempSubscriber = null;
            GC.Collect();
            GC.WaitForPendingFinalizers();
            
            manualEvent.RaiseManualEvent();
        }
        
        static void DemonstrateRealWorldPatterns()
        {
            Console.WriteLine("\n============ REAL-WORLD PATTERNS ============\n");
            
            // ============ OBSERVER PATTERN ============
            Console.WriteLine("=== 1. Observer Pattern ===");
            
            interface IObserver<T>
            {
                void OnNext(T value);
            }
            
            class Observable<T>
            {
                private List<IObserver<T>> observers = new List<IObserver<T>>();
                
                public IDisposable Subscribe(IObserver<T> observer)
                {
                    observers.Add(observer);
                    return new Unsubscriber(() => observers.Remove(observer));
                }
                
                public void Notify(T value)
                {
                    foreach (var observer in observers)
                    {
                        observer.OnNext(value);
                    }
                }
                
                private class Unsubscriber : IDisposable
                {
                    private Action unsubscribeAction;
                    
                    public Unsubscriber(Action unsubscribeAction)
                    {
                        this.unsubscribeAction = unsubscribeAction;
                    }
                    
                    public void Dispose()
                    {
                        unsubscribeAction?.Invoke();
                    }
                }
            }
            
            class StockObserver : IObserver<decimal>
            {
                private string name;
                
                public StockObserver(string name)
                {
                    this.name = name;
                }
                
                public void OnNext(decimal price)
                {
                    Console.WriteLine($"{name}: Stock price changed to ${price:F2}");
                }
            }
            
            Observable<decimal> stockPrice = new Observable<decimal>();
            var observer1 = new StockObserver("Trader1");
            var observer2 = new StockObserver("Trader2");
            
            using (var subscription1 = stockPrice.Subscribe(observer1))
            using (var subscription2 = stockPrice.Subscribe(observer2))
            {
                Console.WriteLine("Stock price changes:");
                stockPrice.Notify(100.50m);
                stockPrice.Notify(102.75m);
                
                // subscription1.Dispose() automatically called
            }
            
            Console.WriteLine("After unsubscription:");
            stockPrice.Notify(105.00m); // No observers left
            
            // ============ MEDIATOR PATTERN ============
            Console.WriteLine("\n=== 2. Mediator Pattern ===");
            
            class ChatMediator
            {
                public event EventHandler<string> MessageReceived;
                
                public void SendMessage(string sender, string message)
                {
                    Console.WriteLine($"{sender} sends: {message}");
                    MessageReceived?.Invoke(this, $"[{sender}] {message}");
                }
            }
            
            class ChatUser
            {
                private string name;
                
                public ChatUser(string name)
                {
                    this.name = name;
                }
                
                public void ReceiveMessage(object sender, string message)
                {
                    Console.WriteLine($"{name} receives: {message}");
                }
                
                public void SendMessage(ChatMediator mediator, string message)
                {
                    mediator.SendMessage(name, message);
                }
            }
            
            ChatMediator chat = new ChatMediator();
            ChatUser alice = new ChatUser("Alice");
            ChatUser bob = new ChatUser("Bob");
            ChatUser charlie = new ChatUser("Charlie");
            
            chat.MessageReceived += alice.ReceiveMessage;
            chat.MessageReceived += bob.ReceiveMessage;
            chat.MessageReceived += charlie.ReceiveMessage;
            
            Console.WriteLine("Chat session:");
            alice.SendMessage(chat, "Hello everyone!");
            bob.SendMessage(chat, "Hi Alice!");
            charlie.SendMessage(chat, "Good morning!");
            
            // ============ COMMAND PATTERN ============
            Console.WriteLine("\n=== 3. Command Pattern ===");
            
            interface ICommand
            {
                void Execute();
                void Undo();
            }
            
            class CommandInvoker
            {
                public event EventHandler<ICommand> CommandExecuted;
                public event EventHandler<ICommand> CommandUndone;
                
                private Stack<ICommand> history = new Stack<ICommand>();
                
                public void ExecuteCommand(ICommand command)
                {
                    command.Execute();
                    history.Push(command);
                    CommandExecuted?.Invoke(this, command);
                }
                
                public void UndoLastCommand()
                {
                    if (history.Count > 0)
                    {
                        var command = history.Pop();
                        command.Undo();
                        CommandUndone?.Invoke(this, command);
                    }
                }
            }
            
            class TextEditorCommand : ICommand
            {
                private string originalText;
                private string newText;
                private Action<string> setText;
                
                public TextEditorCommand(string originalText, string newText, Action<string> setText)
                {
                    this.originalText = originalText;
                    this.newText = newText;
                    this.setText = setText;
                }
                
                public void Execute()
                {
                    setText(newText);
                    Console.WriteLine($"Executed: Changed text to '{newText}'");
                }
                
                public void Undo()
                {
                    setText(originalText);
                    Console.WriteLine($"Undone: Restored text to '{originalText}'");
                }
            }
            
            string currentText = "Hello";
            CommandInvoker invoker = new CommandInvoker();
            
            invoker.CommandExecuted += (sender, cmd) => 
                Console.WriteLine($"Command executed event raised");
            invoker.CommandUndone += (sender, cmd) => 
                Console.WriteLine($"Command undone event raised");
            
            Console.WriteLine("Text editing:");
            invoker.ExecuteCommand(new TextEditorCommand(currentText, "Hello World", 
                text => currentText = text));
            Console.WriteLine($"Current text: {currentText}");
            
            invoker.ExecuteCommand(new TextEditorCommand(currentText, "Hello World!", 
                text => currentText = text));
            Console.WriteLine($"Current text: {currentText}");
            
            invoker.UndoLastCommand();
            Console.WriteLine($"After undo: {currentText}");
            
            invoker.UndoLastCommand();
            Console.WriteLine($"After second undo: {currentText}");
            
            // ============ SUMMARY ============
            Console.WriteLine("\n=== 4. Summary ===");
            Console.WriteLine("""
                Delegates and Events are fundamental to C#:
                
                Key Points:
                1. Delegates are type-safe function pointers
                2. Events provide publish-subscribe mechanism
                3. Use built-in delegates (Action, Func, Predicate) when possible
                4. Follow standard event patterns with EventArgs
                5. Be mindful of memory leaks with event subscriptions
                6. Consider weak events for long-lived publishers
                7. Events enable many design patterns (Observer, Mediator, etc.)
                
                Best Practices:
                • Use EventHandler<T> for custom events
                • Always check for null before raising events
                • Provide protected OnEventName methods
                • Consider thread safety for multi-threaded scenarios
                • Use weak event patterns for UI and long-lived objects
                • Document event behavior and threading model
                """);
        }
    }
}