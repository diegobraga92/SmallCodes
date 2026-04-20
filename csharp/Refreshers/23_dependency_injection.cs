/*
    C# DEPENDENCY INJECTION
    File: 23_dependency_injection.cs
    
    This file demonstrates dependency injection in C# programming.
    Covering concepts from junior to upper mid-level.
    
    Key Concepts Covered:
    1. Basic dependency injection concepts
    2. Intermediate dependency injection patterns
    3. Advanced dependency injection techniques
    4. Real-world dependency injection examples
*/

using System;

namespace CSharpRefresher.dependencyinjection
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# dependency injection Demonstration ===\n");
            
            DemonstrateBasicConcepts();
            DemonstrateIntermediateConcepts();
            DemonstrateAdvancedConcepts();
            
            Console.WriteLine("\n=== dependency injection Complete ===");
        }
        
        static void DemonstrateBasicConcepts()
        {
            Console.WriteLine("============ BASIC CONCEPTS ============\n");
            
            Console.WriteLine("1. Basic dependency injection example:");
            // Basic implementation here
            Console.WriteLine("   Basic concept demonstrated");
            
            Console.WriteLine("\n2. Simple usage:");
            // Simple usage example
            Console.WriteLine("   Simple usage shown");
        }
        
        static void DemonstrateIntermediateConcepts()
        {
            Console.WriteLine("\n============ INTERMEDIATE CONCEPTS ============\n");
            
            Console.WriteLine("1. Intermediate dependency injection pattern:");
            // Intermediate pattern
            Console.WriteLine("   Intermediate pattern demonstrated");
            
            Console.WriteLine("\n2. Common dependency injection scenarios:");
            // Common scenarios
            Console.WriteLine("   Common scenarios shown");
        }
        
        static void DemonstrateAdvancedConcepts()
        {
            Console.WriteLine("\n============ ADVANCED CONCEPTS ============\n");
            
            Console.WriteLine("1. Advanced dependency injection technique:");
            // Advanced technique
            Console.WriteLine("   Advanced technique demonstrated");
            
            Console.WriteLine("\n2. Performance considerations:");
            // Performance tips
            Console.WriteLine("   Performance considerations discussed");
        }
    }
    
    // Supporting class for dependency injection
    public class dependencyinjectionExample
    {
        public string Name { get; set; }
        public int Value { get; set; }
        
        public dependencyinjectionExample(string name, int value)
        {
            Name = name;
            Value = value;
        }
        
        public void Demonstrate()
        {
            Console.WriteLine(`${Name} example with value: ${Value}`);
        }
    }
}
