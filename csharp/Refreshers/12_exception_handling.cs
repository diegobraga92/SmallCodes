/*
    C# EXCEPTION HANDLING
    File: 12_exception_handling.cs
    
    Comprehensive guide to exception handling in C#.
    Covers try-catch-finally, custom exceptions, exception filters,
    best practices, and performance considerations.
*/

using System;
using System.IO;

namespace CSharpRefresher.ExceptionHandling
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Exception Handling ===\n");
            
            DemonstrateBasicHandling();
            DemonstrateExceptionTypes();
            DemonstrateCustomExceptions();
            DemonstrateExceptionFilters();
            DemonstrateBestPractices();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateBasicHandling()
        {
            Console.WriteLine("=== 1. Basic Try-Catch-Finally ===\n");
            
            // Simple try-catch
            try
            {
                int zero = 0;
                int result = 10 / zero;
            }
            catch (DivideByZeroException ex)
            {
                Console.WriteLine($"Caught: {ex.Message}");
            }
            
            // Multiple catch blocks
            try
            {
                string nullStr = null;
                Console.WriteLine(nullStr.Length);
            }
            catch (NullReferenceException ex)
            {
                Console.WriteLine($"Null ref: {ex.Message}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"General: {ex.Message}");
            }
            
            // Finally block
            FileStream file = null;
            try
            {
                file = File.Open("test.txt", FileMode.Open);
            }
            catch (FileNotFoundException)
            {
                Console.WriteLine("File not found");
            }
            finally
            {
                file?.Close();
                Console.WriteLine("Finally executed");
            }
        }
        
        static void DemonstrateExceptionTypes()
        {
            Console.WriteLine("\n=== 2. Exception Types ===\n");
            
            Console.WriteLine("""
                Common Exception Types:
                • System.Exception (base)
                • ArgumentException/ArgumentNullException
                • InvalidOperationException
                • NullReferenceException
                • IndexOutOfRangeException
                • DivideByZeroException
                • IOException/FileNotFoundException
                """);
            
            // Checked vs unchecked
            int max = int.MaxValue;
            
            unchecked
            {
                int overflow = max + 1;
                Console.WriteLine($"Unchecked overflow: {overflow}");
            }
            
            try
            {
                checked
                {
                    int overflow = max + 1;
                }
            }
            catch (OverflowException ex)
            {
                Console.WriteLine($"Checked overflow: {ex.Message}");
            }
            
            // Exception properties
            try
            {
                throw new InvalidOperationException("Test")
                {
                    Source = "Demo",
                    HelpLink = "https://example.com"
                };
            }
            catch (InvalidOperationException ex)
            {
                Console.WriteLine($"Message: {ex.Message}");
                Console.WriteLine($"Source: {ex.Source}");
                Console.WriteLine($"StackTrace: {ex.StackTrace?.Substring(0, 50)}...");
            }
        }
        
        static void DemonstrateCustomExceptions()
        {
            Console.WriteLine("\n=== 3. Custom Exceptions ===\n");
            
            // Basic custom exception
            class ValidationException : Exception
            {
                public string FieldName { get; }
                public object InvalidValue { get; }
                
                public ValidationException(string field, object value)
                    : base($"Validation failed: {field} = {value}")
                {
                    FieldName = field;
                    InvalidValue = value;
                }
            }
            
            // Using custom exception
            void ValidateAge(int age)
            {
                if (age < 0) throw new ValidationException("Age", age);
            }
            
            try
            {
                ValidateAge(-5);
            }
            catch (ValidationException ex)
            {
                Console.WriteLine($"Custom exception: {ex.Message}");
                Console.WriteLine($"Field: {ex.FieldName}, Value: {ex.InvalidValue}");
            }
            
            // Serializable custom exception
            [Serializable]
            class SerializableException : Exception
            {
                public int ErrorCode { get; }
                
                public SerializableException(string message, int code) 
                    : base(message)
                {
                    ErrorCode = code;
                }
            }
        }
        
        static void DemonstrateExceptionFilters()
        {
            Console.WriteLine("\n=== 4. Exception Filters (C# 6.0+) ===\n");
            
            // Basic filter
            try
            {
                throw new InvalidOperationException("Error code: 500");
            }
            catch (InvalidOperationException ex) when (ex.Message.Contains("500"))
            {
                Console.WriteLine("Caught 500 error");
            }
            catch (InvalidOperationException ex) when (ex.Message.Contains("404"))
            {
                Console.WriteLine("Caught 404 error");
            }
            
            // Filter with logging
            bool LogException(Exception ex)
            {
                Console.WriteLine($"Logging: {ex.Message}");
                return true;
            }
            
            try
            {
                throw new ArgumentException("Test");
            }
            catch (Exception ex) when (LogException(ex))
            {
                Console.WriteLine("Exception logged and caught");
            }
            
            // Filter for retry logic
            int attempt = 0;
            while (true)
            {
                try
                {
                    attempt++;
                    if (attempt < 3)
                        throw new TimeoutException($"Attempt {attempt}");
                    
                    Console.WriteLine("Success");
                    break;
                }
                catch (TimeoutException) when (attempt < 3)
                {
                    Console.WriteLine($"Retrying... ({attempt})");
                }
            }
        }
        
        static void DemonstrateBestPractices()
        {
            Console.WriteLine("\n=== 5. Best Practices ===\n");
            
            Console.WriteLine("""
                DO:
                • Catch specific exceptions first
                • Use finally blocks for cleanup
                • Throw meaningful exceptions
                • Use using statements for IDisposable
                • Log exceptions appropriately
                
                DON'T:
                • Catch general Exception unless at top level
                • Use exceptions for control flow
                • Swallow exceptions silently
                • Include sensitive data in error messages
                • Rethrow with "throw ex;" (use "throw;")
                
                Patterns:
                • Use Try-pattern for expected failures
                • Create custom exceptions for domain errors
                • Use exception filters for conditional handling
                • Implement global exception handlers
                """);
            
            // Example: Try-pattern vs exceptions
            class Parser
            {
                // Exception-based
                public int ParseInt(string input)
                {
                    if (!int.TryParse(input, out int result))
                        throw new FormatException($"Invalid: {input}");
                    return result;
                }
                
                // Try-pattern
                public bool TryParseInt(string input, out int result)
                {
                    return int.TryParse(input, out result);
                }
            }
            
            // Global exception handling
            AppDomain.CurrentDomain.UnhandledException += (sender, e) =>
            {
                Console.WriteLine($"Unhandled: {e.ExceptionObject}");
            };
            
            TaskScheduler.UnobservedTaskException += (sender, e) =>
            {
                Console.WriteLine($"Unobserved task: {e.Exception.Message}");
                e.SetObserved();
            };
            
            Console.WriteLine("\n=== Key Takeaways ===");
            Console.WriteLine("""
                1. Exceptions are for exceptional conditions
                2. Design clear error handling strategies
                3. Balance performance and robustness
                4. Test exception scenarios thoroughly
                5. Monitor exceptions in production
                """);
        }
    }
}