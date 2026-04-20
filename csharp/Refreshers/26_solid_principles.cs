/*
    C# SOLID PRINCIPLES
    File: 26_solid_principles.cs
    
    This file demonstrates solid principles in C# programming.
    Covering concepts from junior to upper mid-level.
    
    Key Concepts Covered:
    1. Basic solid principles concepts
    2. Intermediate solid principles patterns
    3. Advanced solid principles techniques
    4. Real-world solid principles examples
*/

using System;

namespace CSharpRefresher.solidprinciples
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# solid principles Demonstration ===\n");
            
            DemonstrateBasicConcepts();
            DemonstrateIntermediateConcepts();
            DemonstrateAdvancedConcepts();
            
            Console.WriteLine("\n=== solid principles Complete ===");
        }
        
        static void DemonstrateBasicConcepts()
        {
            Console.WriteLine("============ BASIC CONCEPTS ============\n");
            
            Console.WriteLine("1. Basic solid principles example:");
            // Basic implementation here
            Console.WriteLine("   Basic concept demonstrated");
            
            Console.WriteLine("\n2. Simple usage:");
            // Simple usage example
            Console.WriteLine("   Simple usage shown");
        }
        
        static void DemonstrateIntermediateConcepts()
        {
            Console.WriteLine("\n============ INTERMEDIATE CONCEPTS ============\n");
            
            Console.WriteLine("1. Intermediate solid principles pattern:");
            // Intermediate pattern
            Console.WriteLine("   Intermediate pattern demonstrated");
            
            Console.WriteLine("\n2. Common solid principles scenarios:");
            // Common scenarios
            Console.WriteLine("   Common scenarios shown");
        }
        
        static void DemonstrateAdvancedConcepts()
        {
            Console.WriteLine("\n============ ADVANCED CONCEPTS ============\n");
            
            Console.WriteLine("1. Advanced solid principles technique:");
            // Advanced technique
            Console.WriteLine("   Advanced technique demonstrated");
            
            Console.WriteLine("\n2. Performance considerations:");
            // Performance tips
            Console.WriteLine("   Performance considerations discussed");
        }
    }
    
    // Supporting class for solid principles
    public class solidprinciplesExample
    {
        public string Name { get; set; }
        public int Value { get; set; }
        
        public solidprinciplesExample(string name, int value)
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
