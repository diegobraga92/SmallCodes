/*
    C# ATTRIBUTES AND REFLECTION
    File: 13_attributes_reflection.cs
    
    Comprehensive guide to attributes (metadata) and reflection in C#.
    Covers built-in attributes, custom attributes, reflection API,
    dynamic type inspection, and practical use cases.
*/

using System;
using System.Reflection;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;

namespace CSharpRefresher.AttributesReflection
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Attributes and Reflection ===\n");
            
            DemonstrateBuiltInAttributes();
            DemonstrateCustomAttributes();
            DemonstrateBasicReflection();
            DemonstrateAdvancedReflection();
            DemonstratePracticalUseCases();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateBuiltInAttributes()
        {
            Console.WriteLine("=== 1. Built-in Attributes ===\n");
            
            // Obsolete attribute
            [Obsolete("Use NewMethod instead", error: false)]
            static void OldMethod()
            {
                Console.WriteLine("Old method");
            }
            
            OldMethod(); // Warning: Obsolete
            
            // Conditional attribute (method only called in DEBUG)
            #if DEBUG
            static void DebugMethod()
            {
                Console.WriteLine("Debug only");
            }
            #endif
            
            // Serializable attribute
            [Serializable]
            class SerializableData
            {
                public int Id { get; set; }
                public string Name { get; set; }
            }
            
            // Data annotation attributes
            class User
            {
                [Required]
                [StringLength(50)]
                public string Username { get; set; }
                
                [Range(1, 150)]
                public int Age { get; set; }
                
                [EmailAddress]
                public string Email { get; set; }
            }
            
            // DllImport attribute
            // [DllImport("user32.dll")]
            // static extern bool MessageBeep(uint uType);
            
            Console.WriteLine("Common built-in attributes:");
            Console.WriteLine("• [Obsolete] - Marks deprecated code");
            Console.WriteLine("• [Serializable] - Enables serialization");
            Console.WriteLine("• [Conditional] - Conditional compilation");
            Console.WriteLine("• [DllImport] - External DLL functions");
            Console.WriteLine("• Data annotations for validation");
        }
        
        static void DemonstrateCustomAttributes()
        {
            Console.WriteLine("\n=== 2. Custom Attributes ===\n");
            
            // Define custom attribute
            [AttributeUsage(AttributeTargets.Class | AttributeTargets.Method, 
                           AllowMultiple = false, 
                           Inherited = true)]
            class AuthorAttribute : Attribute
            {
                public string Name { get; }
                public string Version { get; set; } = "1.0";
                
                public AuthorAttribute(string name)
                {
                    Name = name;
                }
            }
            
            // Attribute with parameters
            [AttributeUsage(AttributeTargets.Property)]
            class DisplayAttribute : Attribute
            {
                public string Label { get; }
                public int Order { get; set; }
                
                public DisplayAttribute(string label)
                {
                    Label = label;
                }
            }
            
            // Using custom attributes
            [Author("John Doe", Version = "2.0")]
            class Document
            {
                [Display("Document Title", Order = 1)]
                public string Title { get; set; }
                
                [Display("Creation Date", Order = 2)]
                public DateTime Created { get; set; }
            }
            
            // Reading attributes via reflection
            var docType = typeof(Document);
            var authorAttr = docType.GetCustomAttribute<AuthorAttribute>();
            Console.WriteLine($"Author: {authorAttr?.Name}, Version: {authorAttr?.Version}");
            
            var props = docType.GetProperties();
            foreach (var prop in props)
            {
                var displayAttr = prop.GetCustomAttribute<DisplayAttribute>();
                if (displayAttr != null)
                {
                    Console.WriteLine($"{prop.Name}: {displayAttr.Label} (Order: {displayAttr.Order})");
                }
            }
        }
        
        static void DemonstrateBasicReflection()
        {
            Console.WriteLine("\n=== 3. Basic Reflection ===\n");
            
            class Person
            {
                public string Name { get; set; }
                private int Age { get; set; }
                
                public Person(string name, int age)
                {
                    Name = name;
                    Age = age;
                }
                
                public void SayHello() => Console.WriteLine($"Hello, I'm {Name}");
                private void SecretMethod() => Console.WriteLine("Secret!");
            }
            
            var person = new Person("Alice", 30);
            var type = person.GetType();
            
            // Type information
            Console.WriteLine($"Type: {type.Name}");
            Console.WriteLine($"Full name: {type.FullName}");
            Console.WriteLine($"Namespace: {type.Namespace}");
            Console.WriteLine($"Is class: {type.IsClass}");
            Console.WriteLine($"Base type: {type.BaseType?.Name}");
            
            // Properties
            Console.WriteLine("\nProperties:");
            var properties = type.GetProperties(
                BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            foreach (var prop in properties)
            {
                Console.WriteLine($"  {prop.Name} ({prop.PropertyType.Name}): " +
                                 $"Public: {prop.GetMethod?.IsPublic}, " +
                                 $"Private: {prop.GetMethod?.IsPrivate}");
            }
            
            // Methods
            Console.WriteLine("\nMethods:");
            var methods = type.GetMethods(
                BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            foreach (var method in methods.Where(m => !m.IsSpecialName))
            {
                Console.WriteLine($"  {method.Name} (Public: {method.IsPublic})");
            }
            
            // Constructors
            Console.WriteLine("\nConstructors:");
            var constructors = type.GetConstructors();
            foreach (var ctor in constructors)
            {
                Console.WriteLine($"  {ctor.Name} with {ctor.GetParameters().Length} parameters");
            }
        }
        
        static void DemonstrateAdvancedReflection()
        {
            Console.WriteLine("\n=== 4. Advanced Reflection ===\n");
            
            // Dynamic type creation
            Console.WriteLine("Dynamic type creation:");
            
            // Get assembly info
            var assembly = Assembly.GetExecutingAssembly();
            Console.WriteLine($"Assembly: {assembly.FullName}");
            Console.WriteLine($"Location: {assembly.Location}");
            
            // Get all types in assembly
            var types = assembly.GetTypes();
            Console.WriteLine($"Total types: {types.Length}");
            
            // Create instance dynamically
            class DynamicType
            {
                public string Value { get; set; }
                
                public void Print() => Console.WriteLine($"Value: {Value}");
            }
            
            var dynamicType = typeof(DynamicType);
            var instance = Activator.CreateInstance(dynamicType) as DynamicType;
            instance.Value = "Created dynamically";
            instance.Print();
            
            // Invoke methods dynamically
            var method = dynamicType.GetMethod("Print");
            method.Invoke(instance, null);
            
            // Set properties dynamically
            var property = dynamicType.GetProperty("Value");
            property.SetValue(instance, "Updated dynamically");
            method.Invoke(instance, null);
            
            // Generic type reflection
            Console.WriteLine("\nGeneric type reflection:");
            
            var listType = typeof(List<>);
            Console.WriteLine($"Generic type: {listType}");
            
            var stringListType = listType.MakeGenericType(typeof(string));
            var stringList = Activator.CreateInstance(stringListType);
            var addMethod = stringListType.GetMethod("Add");
            addMethod.Invoke(stringList, new object[] { "Hello" });
            
            Console.WriteLine($"Created List<string> with {((List<string>)stringList).Count} items");
        }
        
        static void DemonstratePracticalUseCases()
        {
            Console.WriteLine("\n=== 5. Practical Use Cases ===\n");
            
            // 1. Plugin system
            Console.WriteLine("1. Plugin System:");
            
            interface IPlugin
            {
                string Name { get; }
                void Execute();
            }
            
            [AttributeUsage(AttributeTargets.Class)]
            class PluginAttribute : Attribute
            {
                public string Category { get; }
                
                public PluginAttribute(string category)
                {
                    Category = category;
                }
            }
            
            [Plugin("Utility")]
            class LoggerPlugin : IPlugin
            {
                public string Name => "Logger";
                public void Execute() => Console.WriteLine("Logging...");
            }
            
            [Plugin("Analysis")]
            class AnalyzerPlugin : IPlugin
            {
                public string Name => "Analyzer";
                public void Execute() => Console.WriteLine("Analyzing...");
            }
            
            // Discover plugins
            var pluginTypes = Assembly.GetExecutingAssembly()
                .GetTypes()
                .Where(t => t.GetCustomAttribute<PluginAttribute>() != null && 
                           typeof(IPlugin).IsAssignableFrom(t));
            
            foreach (var pluginType in pluginTypes)
            {
                var plugin = Activator.CreateInstance(pluginType) as IPlugin;
                var attr = pluginType.GetCustomAttribute<PluginAttribute>();
                Console.WriteLine($"  Plugin: {plugin.Name} (Category: {attr.Category})");
            }
            
            // 2. Object mapper
            Console.WriteLine("\n2. Object Mapper:");
            
            class Source
            {
                public int Id { get; set; }
                public string FullName { get; set; }
            }
            
            class Destination
            {
                public int Identifier { get; set; }
                public string Name { get; set; }
            }
            
            // Simple mapper using reflection
            Destination Map(Source source)
            {
                var dest = new Destination();
                var sourceProps = source.GetType().GetProperties();
                var destProps = dest.GetType().GetProperties();
                
                foreach (var destProp in destProps)
                {
                    var sourceProp = sourceProps.FirstOrDefault(p => 
                        p.Name.Equals(destProp.Name, StringComparison.OrdinalIgnoreCase));
                    
                    if (sourceProp != null && sourceProp.PropertyType == destProp.PropertyType)
                    {
                        var value = sourceProp.GetValue(source);
                        destProp.SetValue(dest, value);
                    }
                }
                
                return dest;
            }
            
            var source = new Source { Id = 1, FullName = "John Doe" };
            var destination = Map(source);
            Console.WriteLine($"  Mapped: Id={source.Id} → Identifier={destination.Identifier}");
            
            // 3. Dependency injection
            Console.WriteLine("\n3. Dependency Injection Container:");
            
            class SimpleContainer
            {
                private Dictionary<Type, Type> _mappings = new();
                
                public void Register<TInterface, TImplementation>() 
                    where TImplementation : TInterface
                {
                    _mappings[typeof(TInterface)] = typeof(TImplementation);
                }
                
                public TInterface Resolve<TInterface>()
                {
                    if (_mappings.TryGetValue(typeof(TInterface), out var implType))
                    {
                        return (TInterface)Activator.CreateInstance(implType);
                    }
                    throw new InvalidOperationException($"No registration for {typeof(TInterface)}");
                }
            }
            
            // 4. Serialization/deserialization
            Console.WriteLine("\n4. Custom Serialization:");
            
            class JsonSerializer
            {
                public string Serialize(object obj)
                {
                    var props = obj.GetType().GetProperties();
                    var dict = new Dictionary<string, object>();
                    
                    foreach (var prop in props)
                    {
                        var value = prop.GetValue(obj);
                        dict[prop.Name] = value;
                    }
                    
                    // Simple JSON representation
                    return string.Join(", ", 
                        dict.Select(kv => $"\"{kv.Key}\": \"{kv.Value}\""));
                }
            }
            
            var serializer = new JsonSerializer();
            var json = serializer.Serialize(new { Name = "Test", Value = 123 });
            Console.WriteLine($"  Serialized: {{{json}}}");
            
            Console.WriteLine("\n=== Best Practices ===");
            Console.WriteLine("""
                1. Use attributes for declarative programming
                2. Cache reflection results (Type, MethodInfo, etc.)
                3. Consider performance impact of reflection
                4. Use nameof() instead of string literals
                5. Validate attributes at compile time when possible
                6. Use Expression Trees for better performance
                7. Consider source generators for compile-time reflection
                
                Performance tips:
                • Reflection is slower than direct calls
                • Cache Type and MethodInfo objects
                • Use Delegate.CreateDelegate for repeated calls
                • Consider dynamic keyword for simple scenarios
                • Use compiled Expression Trees for complex scenarios
                """);
        }
    }
    
    // Helper attributes
    [AttributeUsage(AttributeTargets.Property)]
    class RequiredAttribute : Attribute { }
    
    [AttributeUsage(AttributeTargets.Property)]
    class StringLengthAttribute : Attribute
    {
        public int MaximumLength { get; }
        
        public StringLengthAttribute(int maxLength)
        {
            MaximumLength = maxLength;
        }
    }
    
    [AttributeUsage(AttributeTargets.Property)]
    class RangeAttribute : Attribute
    {
        public int Min { get; }
        public int Max { get; }
        
        public RangeAttribute(int min, int max)
        {
            Min = min;
            Max = max;
        }
    }
    
    [AttributeUsage(AttributeTargets.Property)]
    class EmailAddressAttribute : Attribute { }
}