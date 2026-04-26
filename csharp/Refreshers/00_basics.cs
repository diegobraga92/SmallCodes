/*
    C# BASICS - Fundamental Concepts
    File: 00_basics.cs
    
    Comprehensive guide to C# fundamentals covering data types, variables,
    operators, and type conversion. This file builds from junior-level basics
    to mid-level understanding of memory, performance, and type system nuances.
    
    Key Concepts Covered:
    1. Value Types vs Reference Types (stack vs heap allocation)
    2. Integer, Floating-point, and Special Types
    3. Variable Declaration and Scope
    4. Operators (arithmetic, comparison, logical, bitwise)
    5. Type Conversion (implicit, explicit, boxing/unboxing)
    6. Nullable Types and Null Safety
    7. Type Inference with var
    8. Constants and Readonly Fields
*/

using System;

namespace CSharpRefresher.Basics
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Basics Demonstration ===\n");
            
            DemonstrateDataTypes();
            DemonstrateVariables();
            DemonstrateOperators();
            DemonstrateTypeConversion();
            
            Console.WriteLine("\n=== Basics Complete ===");
        }
        
        static void DemonstrateDataTypes()
        {
            Console.WriteLine("============ DATA TYPES ============\n");
            
            // ============ VALUE TYPES VS REFERENCE TYPES ============
            Console.WriteLine("=== 1. Value Types vs Reference Types ===");
            Console.WriteLine("""
                C# types are divided into two categories:
                
                Value Types (stored on stack):
                • int, long, float, double, decimal, bool, char, struct, enum
                • Each variable has its own copy of the data
                • Assigned by value (copying the data)
                • Cannot be null (unless nullable)
                • More efficient for small data
                
                Reference Types (stored on heap):
                • string, class, interface, delegate, array, object
                • Variables hold a reference (pointer) to the data
                • Assigned by reference (copying the pointer)
                • Can be null
                • Subject to garbage collection
                """);
            
            // ============ INTEGER TYPES ============
            Console.WriteLine("\n=== 2. Integer Types ===");
            Console.WriteLine("""
                C# provides signed and unsigned integer types of varying sizes:
                
                | Type    | Size   | Range                                    | Use Case              |
                |---------|--------|------------------------------------------|-----------------------|
                | byte    | 8-bit  | 0 to 255                                | Small counters, bytes |
                | sbyte   | 8-bit  | -128 to 127                             | Small signed values   |
                | short   | 16-bit | -32,768 to 32,767                       | Memory-sensitive      |
                | ushort  | 16-bit | 0 to 65,535                             | Unsigned small values |
                | int     | 32-bit | -2.1B to 2.1B                           | Default integer type  |
                | uint    | 32-bit | 0 to 4.29B                              | Positive-only counts  |
                | long    | 64-bit | -9.2E18 to 9.2E18                       | Large values          |
                | ulong   | 64-bit | 0 to 1.84E19                            | Very large unsigned   |
                
                Key points:
                • Prefer 'int' for general-purpose integers (best performance on 32/64-bit CPUs)
                • Use 'long' when values exceed int range (~2.1 billion)
                • Use 'byte' for raw byte data or memory-constrained scenarios
                • Signed types cover negative values, unsigned only positive
                """);
            
            // Integer types
            byte myByte = 255;                 // 0 to 255 (8-bit)
            sbyte mySByte = -128;              // -128 to 127 (8-bit signed)
            short myShort = 32767;             // -32,768 to 32,767 (16-bit)
            ushort myUShort = 65535;           // 0 to 65,535 (16-bit unsigned)
            int myInt = 2147483647;            // -2,147,483,648 to 2,147,483,647 (32-bit)
            uint myUInt = 4294967295;          // 0 to 4,294,967,295 (32-bit unsigned)
            long myLong = 9223372036854775807; // 64-bit
            ulong myULong = 18446744073709551615; // 64-bit unsigned
            
            // ============ FLOATING POINT TYPES ============
            Console.WriteLine("\n=== 3. Floating Point Types ===");
            Console.WriteLine("""
                C# provides three floating-point types with different precision:
                
                | Type    | Size   | Precision | Suffix | Use Case                          |
                |---------|--------|-----------|--------|-----------------------------------|
                | float   | 32-bit | ~7 digits | f      | Graphics, 3D, game development    |
                | double  | 64-bit | ~15 digits| (none) | General-purpose math, science     |
                | decimal | 128-bit| ~28 digits| m      | Financial, monetary calculations  |
                
                Key points:
                • double is the default for floating-point literals (3.14 is double)
                • float requires 'f' suffix: 3.14f
                • decimal requires 'm' suffix: 3.14m
                • decimal avoids floating-point rounding errors (base-10)
                • float/double use base-2 and can have small rounding errors
                • Never use float/double for money - use decimal
                """);
            
            // Floating point types
            float myFloat = 3.14159f;          // 7 digits precision (32-bit) - 'f' suffix required
            double myDouble = 3.14159265358979; // 15-16 digits precision (64-bit)
            decimal myDecimal = 3.14159265358979323846m; // 28-29 digits precision (128-bit) - 'm' suffix required
            
            // ============ OTHER BASIC TYPES ============
            Console.WriteLine("\n=== 4. Other Basic Types ===");
            Console.WriteLine("""
                | Type    | Size   | Description                          |
                |---------|--------|--------------------------------------|
                | char    | 16-bit | Single Unicode character (UTF-16)    |
                | bool    | 8-bit  | true or false                        |
                | string  | Ref    | Immutable sequence of characters     |
                | object  | Ref    | Ultimate base class for all types    |
                | dynamic | Ref    | Type resolved at runtime             |
                
                Key points:
                • char is numeric (can cast to int for ASCII/Unicode value)
                • string is a reference type but behaves like value type (immutable, == compares content)
                • object is the root of the type hierarchy
                • dynamic bypasses compile-time type checking (use sparingly)
                """);
            
            // Other types
            char myChar = 'A';                 // 16-bit Unicode character
            bool myBool = true;                // true or false
            
            // Special types
            string myString = "Hello, C#!";    // Reference type but behaves like value type
            object myObject = new object();    // Base type for all types
            dynamic myDynamic = "I can be anything"; // Type resolved at runtime
            
            Console.WriteLine($"Integer types:");
            Console.WriteLine($"  byte: {myByte} (size: {sizeof(byte)} byte)");
            Console.WriteLine($"  int: {myInt} (size: {sizeof(int)} bytes)");
            Console.WriteLine($"  long: {myLong} (size: {sizeof(long)} bytes)");
            
            Console.WriteLine($"\nFloating point types:");
            Console.WriteLine($"  float: {myFloat} (size: {sizeof(float)} bytes)");
            Console.WriteLine($"  double: {myDouble} (size: {sizeof(double)} bytes)");
            Console.WriteLine($"  decimal: {myDecimal} (size: {sizeof(decimal)} bytes) - for financial calculations");
            
            Console.WriteLine($"\nOther types:");
            Console.WriteLine($"  char: '{myChar}' (as int: {(int)myChar})");
            Console.WriteLine($"  bool: {myBool}");
            Console.WriteLine($"  string: \"{myString}\" (length: {myString.Length})");
            
            // ============ DEFAULT VALUES ============
            Console.WriteLine("\n=== 5. Default Values ===");
            Console.WriteLine("""
                Every type has a default value:
                • Numeric types: 0 (or 0.0 for floating-point)
                • bool: false
                • char: '\\0' (null character)
                • Reference types: null
                • Nullable value types: null
                
                Use 'default' keyword to get the default value of any type:
                    int defaultInt = default;    // 0
                    string defaultStr = default; // null
                """);
            
            int defaultInt = default;          // 0
            bool defaultBool = default;        // false
            string defaultString = default;    // null
            Console.WriteLine($"  default(int): {defaultInt}");
            Console.WriteLine($"  default(bool): {defaultBool}");
            Console.WriteLine($"  default(string): {(defaultString == null ? "null" : defaultString)}");
        }
        
        static void DemonstrateVariables()
        {
            Console.WriteLine("\n============ VARIABLES ============\n");
            
            // Different ways to declare variables
            int explicitType = 42;                     // Explicit type declaration
            var inferredType = 42;                     // Type inference with 'var' (C# 3+)
            const int CONSTANT_VALUE = 100;            // Constant (must be initialized, cannot change)
            readonly int readOnlyField = 200;          // Readonly (can only be set in constructor)
            
            Console.WriteLine($"Explicit type: {explicitType} (type: {explicitType.GetType().Name})");
            Console.WriteLine($"Inferred type: {inferredType} (type: {inferredType.GetType().Name})");
            Console.WriteLine($"Constant: {CONSTANT_VALUE}");
            Console.WriteLine($"Readonly field: {readOnlyField}");
            
            // Multiple declarations
            int x = 1, y = 2, z = 3;
            Console.WriteLine($"\nMultiple variables: x={x}, y={y}, z={z}");
            
            // Variable scope
            {
                int blockScoped = 10;
                Console.WriteLine($"Block-scoped variable: {blockScoped}");
                // blockScoped is only accessible within this block
            }
            // Console.WriteLine(blockScoped); // ERROR: blockScoped is out of scope
            
            // Nullable value types (C# 2+)
            int? nullableInt = null;                   // Can be null
            nullableInt = 42;                          // Can be assigned a value
            Console.WriteLine($"\nNullable int: {nullableInt}");
            Console.WriteLine($"Has value: {nullableInt.HasValue}");
            Console.WriteLine($"Value (or default): {nullableInt ?? 0}"); // Null-coalescing operator
            
            // Implicitly typed arrays
            var implicitArray = new[] { 1, 2, 3, 4, 5 };
            Console.WriteLine($"\nImplicitly typed array: [{string.Join(", ", implicitArray)}]");
            Console.WriteLine($"Type: {implicitArray.GetType().Name}");
        }
        
        static void DemonstrateOperators()
        {
            Console.WriteLine("\n============ OPERATORS ============\n");
            
            int a = 10, b = 3;
            
            Console.WriteLine($"Arithmetic operators (a={a}, b={b}):");
            Console.WriteLine($"  a + b = {a + b}");      // Addition
            Console.WriteLine($"  a - b = {a - b}");      // Subtraction
            Console.WriteLine($"  a * b = {a * b}");      // Multiplication
            Console.WriteLine($"  a / b = {a / b}");      // Integer division
            Console.WriteLine($"  a % b = {a % b}");      // Modulus (remainder)
            Console.WriteLine($"  a++ = {a++}");          // Post-increment
            Console.WriteLine($"  ++a = {++a}");          // Pre-increment
            
            // Reset a
            a = 10;
            
            Console.WriteLine($"\nComparison operators (a={a}, b={b}):");
            Console.WriteLine($"  a == b: {a == b}");     // Equal to
            Console.WriteLine($"  a != b: {a != b}");     // Not equal to
            Console.WriteLine($"  a > b: {a > b}");       // Greater than
            Console.WriteLine($"  a < b: {a < b}");       // Less than
            Console.WriteLine($"  a >= b: {a >= b}");     // Greater than or equal to
            Console.WriteLine($"  a <= b: {a <= b}");     // Less than or equal to
            
            Console.WriteLine($"\nLogical operators:");
            bool p = true, q = false;
            Console.WriteLine($"  p && q: {p && q}");     // AND
            Console.WriteLine($"  p || q: {p || q}");     // OR
            Console.WriteLine($"  !p: {!p}");             // NOT
            Console.WriteLine($"  p ^ q: {p ^ q}");       // XOR (exclusive OR)
            
            Console.WriteLine($"\nBitwise operators (a=5, b=3):");
            int x = 5, y = 3; // Binary: 5=0101, 3=0011
            Console.WriteLine($"  x & y: {x & y}");       // AND (0101 & 0011 = 0001 = 1)
            Console.WriteLine($"  x | y: {x | y}");       // OR (0101 | 0011 = 0111 = 7)
            Console.WriteLine($"  x ^ y: {x ^ y}");       // XOR (0101 ^ 0011 = 0110 = 6)
            Console.WriteLine($"  ~x: {~x}");             // NOT (complement)
            Console.WriteLine($"  x << 1: {x << 1}");     // Left shift (0101 << 1 = 1010 = 10)
            Console.WriteLine($"  x >> 1: {x >> 1}");     // Right shift (0101 >> 1 = 0010 = 2)
            
            Console.WriteLine($"\nAssignment operators:");
            int value = 10;
            Console.WriteLine($"  Initial value: {value}");
            value += 5;  Console.WriteLine($"  value += 5: {value}");  // value = value + 5
            value -= 3;  Console.WriteLine($"  value -= 3: {value}");  // value = value - 3
            value *= 2;  Console.WriteLine($"  value *= 2: {value}");  // value = value * 2
            value /= 4;  Console.WriteLine($"  value /= 4: {value}");  // value = value / 4
            value %= 3;  Console.WriteLine($"  value %= 3: {value}");  // value = value % 3
            
            Console.WriteLine($"\nTernary operator:");
            int age = 20;
            string status = age >= 18 ? "Adult" : "Minor";
            Console.WriteLine($"  Age {age}: {status}");
            
            Console.WriteLine($"\nNull-coalescing operators:");
            string name = null;
            string displayName = name ?? "Anonymous";  // If name is null, use "Anonymous"
            Console.WriteLine($"  name ?? \"Anonymous\": {displayName}");
            
            string maybeNull = null;
            string result = maybeNull?.ToUpper() ?? "DEFAULT"; // Null-conditional + null-coalescing
            Console.WriteLine($"  maybeNull?.ToUpper() ?? \"DEFAULT\": {result}");
        }
        
        static void DemonstrateTypeConversion()
        {
            Console.WriteLine("\n============ TYPE CONVERSION ============\n");
            
            // Implicit conversion (safe, no data loss)
            int smallInt = 100;
            long bigLong = smallInt;  // Implicit: int to long
            Console.WriteLine($"Implicit conversion (int to long): {smallInt} -> {bigLong}");
            
            float smallFloat = 3.14f;
            double bigDouble = smallFloat;  // Implicit: float to double
            Console.WriteLine($"Implicit conversion (float to double): {smallFloat} -> {bigDouble}");
            
            // Explicit conversion (casting, potential data loss)
            double precise = 9.87;
            int truncated = (int)precise;  // Explicit: double to int (truncates)
            Console.WriteLine($"\nExplicit conversion (double to int): {precise} -> {truncated}");
            
            long bigNumber = 300;
            byte smallByte = (byte)bigNumber;  // Explicit: long to byte (may overflow)
            Console.WriteLine($"Explicit conversion (long to byte): {bigNumber} -> {smallByte}");
            
            // Checked context for overflow detection
            try
            {
                checked
                {
                    int maxInt = int.MaxValue;
                    // int overflow = maxInt + 1; // Would throw OverflowException
                }
            }
            catch (OverflowException)
            {
                Console.WriteLine($"Checked context detected overflow!");
            }
            
            // Conversion using Convert class
            string numberString = "123";
            int convertedInt = Convert.ToInt32(numberString);
            Console.WriteLine($"\nConvert.ToInt32(\"123\"): {convertedInt}");
            
            // TryParse for safe conversion
            string invalidString = "abc";
            if (int.TryParse(invalidString, out int parsedValue))
            {
                Console.WriteLine($"Parsed: {parsedValue}");
            }
            else
            {
                Console.WriteLine($"Failed to parse \"{invalidString}\" as int");
            }
            
            // Boxing and unboxing
            int valueType = 42;
            object boxed = valueType;           // Boxing: value type to object
            int unboxed = (int)boxed;           // Unboxing: object to value type
            Console.WriteLine($"\nBoxing/unboxing: {valueType} -> boxed -> {unboxed}");
            
            // Type checking and conversion
            object obj = "Hello";
            if (obj is string)                  // Type check with 'is'
            {
                string str = obj as string;     // Safe cast with 'as' (returns null if fails)
                Console.WriteLine($"Object is string: {str}");
            }
            
            // Pattern matching (C# 7+)
            if (obj is string s)                // Pattern matching with declaration
            {
                Console.WriteLine($"Pattern matched string: {s}");
            }
        }
    }
}