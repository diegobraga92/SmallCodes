/*
    C# SERIALIZATION
    File: 18_serialization.cs
    
    Comprehensive guide to serialization and deserialization in C#.
    Covers JSON, XML, binary serialization, data contracts, custom serializers,
    performance considerations, versioning, and real-world patterns.
*/

using System;
using System.IO;
using System.Text;
using System.Xml;
using System.Xml.Serialization;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Formatters.Binary;
using System.Runtime.Serialization.Json;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace CSharpRefresher.Serialization
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Serialization ===\n");
            
            DemonstrateJsonSerialization();
            DemonstrateXmlSerialization();
            DemonstrateBinarySerialization();
            DemonstrateDataContractSerialization();
            DemonstrateCustomSerialization();
            DemonstrateBestPractices();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateJsonSerialization()
        {
            Console.WriteLine("=== 1. JSON Serialization ===\n");
            
            // Sample class for serialization
            public class Person
            {
                public string Name { get; set; }
                public int Age { get; set; }
                public DateTime BirthDate { get; set; }
                public List<string> Hobbies { get; set; }
                public Address Address { get; set; }
                
                [JsonIgnore] // System.Text.Json attribute
                public string Secret { get; set; }
                
                [JsonPropertyName("full_name")] // Rename property in JSON
                public string FullName => $"{Name} (Age: {Age})";
            }
            
            public class Address
            {
                public string Street { get; set; }
                public string City { get; set; }
                public string Country { get; set; }
            }
            
            // Create sample object
            var person = new Person
            {
                Name = "John Doe",
                Age = 30,
                BirthDate = new DateTime(1993, 5, 15),
                Hobbies = new List<string> { "Reading", "Hiking", "Coding" },
                Address = new Address
                {
                    Street = "123 Main St",
                    City = "New York",
                    Country = "USA"
                },
                Secret = "Don't serialize this"
            };
            
            // 1. System.Text.Json (modern, high-performance)
            Console.WriteLine("1. System.Text.Json:");
            
            // Serialize
            string json = System.Text.Json.JsonSerializer.Serialize(person, 
                new JsonSerializerOptions 
                { 
                    WriteIndented = true,
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                });
            Console.WriteLine($"Serialized JSON:\n{json}");
            
            // Deserialize
            Person deserializedPerson = System.Text.Json.JsonSerializer.Deserialize<Person>(json);
            Console.WriteLine($"Deserialized Name: {deserializedPerson.Name}");
            
            // Async serialization
            async Task AsyncJsonExample()
            {
                using (var stream = new MemoryStream())
                {
                    await System.Text.Json.JsonSerializer.SerializeAsync(stream, person);
                    stream.Position = 0;
                    var asyncDeserialized = await System.Text.Json.JsonSerializer.DeserializeAsync<Person>(stream);
                    Console.WriteLine($"Async deserialized Name: {asyncDeserialized.Name}");
                }
            }
            AsyncJsonExample().Wait();
            
            // Custom converters
            Console.WriteLine("\n2. Custom JSON Converters:");
            
            public class DateTimeOffsetConverter : JsonConverter<DateTimeOffset>
            {
                public override DateTimeOffset Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
                {
                    return DateTimeOffset.Parse(reader.GetString());
                }
                
                public override void Write(Utf8JsonWriter writer, DateTimeOffset value, JsonSerializerOptions options)
                {
                    writer.WriteStringValue(value.ToString("yyyy-MM-ddTHH:mm:sszzz"));
                }
            }
            
            var optionsWithConverter = new JsonSerializerOptions
            {
                Converters = { new DateTimeOffsetConverter() },
                WriteIndented = true
            };
            
            // 2. Newtonsoft.Json (Json.NET) - if referenced
            Console.WriteLine("\n3. Newtonsoft.Json (Json.NET) - if referenced:");
            Console.WriteLine("""
                Features not in System.Text.Json:
                • More forgiving parsing
                • LINQ to JSON (JObject, JArray)
                • More customization options
                • Better polymorphic serialization
                
                Common when compatibility with older code is needed.
                """);
            
            // JSON Schema validation
            Console.WriteLine("\n4. JSON Schema Validation:");
            Console.WriteLine("""
                For validating JSON structure:
                • NJsonSchema (NuGet package)
                • Manually validate with JsonDocument
                • Use JsonSchema from Newtonsoft.Json.Schema
                """);
            
            // Performance tips
            Console.WriteLine("\n5. JSON Performance Tips:");
            Console.WriteLine("""
                • Use System.Text.Json for performance
                • Reuse JsonSerializerOptions instances
                • Use source generation (C# 9+)
                • Consider Utf8JsonReader/Utf8JsonWriter for low-level ops
                • Use pooling for MemoryStream/ArrayPool
                """);
            
            // Source generation example (C# 9+)
            Console.WriteLine("\n6. Source Generation (C# 9+):");
            Console.WriteLine("""
                [JsonSerializable(typeof(Person))]
                internal partial class PersonJsonContext : JsonSerializerContext
                {
                }
                
                // Then serialize with context for AOT compilation
                """);
        }
        
        static void DemonstrateXmlSerialization()
        {
            Console.WriteLine("\n=== 2. XML Serialization ===\n");
            
            // Sample class with XML attributes
            [XmlRoot("Person")]
            public class XmlPerson
            {
                [XmlAttribute("id")]
                public int Id { get; set; }
                
                [XmlElement("FullName")]
                public string Name { get; set; }
                
                [XmlIgnore]
                public string Secret { get; set; }
                
                [XmlArray("Hobbies")]
                [XmlArrayItem("Hobby")]
                public List<string> Hobbies { get; set; }
                
                [XmlElement("BirthDate", DataType = "date")]
                public DateTime BirthDate { get; set; }
                
                public XmlPerson()
                {
                    Hobbies = new List<string>();
                }
            }
            
            var person = new XmlPerson
            {
                Id = 1,
                Name = "Jane Smith",
                Secret = "Hidden",
                BirthDate = new DateTime(1990, 8, 20),
                Hobbies = { "Swimming", "Photography" }
            };
            
            // 1. Basic XML serialization
            Console.WriteLine("1. Basic XML Serialization:");
            
            var serializer = new XmlSerializer(typeof(XmlPerson));
            
            using (var writer = new StringWriter())
            {
                serializer.Serialize(writer, person);
                string xml = writer.ToString();
                Console.WriteLine($"Serialized XML:\n{xml}");
                
                // Deserialize
                using (var reader = new StringReader(xml))
                {
                    var deserialized = (XmlPerson)serializer.Deserialize(reader);
                    Console.WriteLine($"Deserialized Name: {deserialized.Name}");
                }
            }
            
            // 2. XML with namespaces
            Console.WriteLine("\n2. XML with Namespaces:");
            
            var ns = new XmlSerializerNamespaces();
            ns.Add("", "http://example.com/namespace");
            
            using (var writer = new StringWriter())
            {
                serializer.Serialize(writer, person, ns);
                Console.WriteLine($"XML with namespace:\n{writer}");
            }
            
            // 3. XML Document (DOM) manipulation
            Console.WriteLine("\n3. XML Document (DOM):");
            
            var xmlDoc = new XmlDocument();
            xmlDoc.LoadXml("<root><person><name>Test</name></person></root>");
            
            // Create element
            var newElement = xmlDoc.CreateElement("age");
            newElement.InnerText = "30";
            xmlDoc.DocumentElement.FirstChild.AppendChild(newElement);
            
            Console.WriteLine($"Modified XML:\n{xmlDoc.OuterXml}");
            
            // 4. XPath queries
            Console.WriteLine("\n4. XPath Queries:");
            
            var nav = xmlDoc.CreateNavigator();
            var node = nav.SelectSingleNode("//person/name");
            Console.WriteLine($"XPath result: {node?.Value}");
            
            // 5. XML Reader/Writer (streaming)
            Console.WriteLine("\n5. XML Reader/Writer (Streaming):");
            
            var settings = new XmlWriterSettings
            {
                Indent = true,
                Encoding = Encoding.UTF8
            };
            
            using (var stream = new MemoryStream())
            using (var xmlWriter = XmlWriter.Create(stream, settings))
            {
                xmlWriter.WriteStartDocument();
                xmlWriter.WriteStartElement("People");
                xmlWriter.WriteStartElement("Person");
                xmlWriter.WriteAttributeString("id", "1");
                xmlWriter.WriteElementString("Name", "Alice");
                xmlWriter.WriteEndElement(); // Person
                xmlWriter.WriteEndElement(); // People
                xmlWriter.WriteEndDocument();
                xmlWriter.Flush();
                
                stream.Position = 0;
                var xml = Encoding.UTF8.GetString(stream.ToArray());
                Console.WriteLine($"Stream-written XML:\n{xml}");
            }
            
            // 6. XML Schema (XSD) validation
            Console.WriteLine("\n6. XML Schema (XSD) Validation:");
            Console.WriteLine("""
                // Create schema
                var schemas = new XmlSchemaSet();
                schemas.Add("", "schema.xsd");
                
                var xmlReaderSettings = new XmlReaderSettings
                {
                    ValidationType = ValidationType.Schema,
                    Schemas = schemas
                };
                xmlReaderSettings.ValidationEventHandler += (s, e) => 
                {
                    Console.WriteLine($"Validation error: {e.Message}");
                };
                """);
            
            // 7. LINQ to XML (modern XML API)
            Console.WriteLine("\n7. LINQ to XML:");
            
            var xdoc = new System.Xml.Linq.XDocument(
                new System.Xml.Linq.XElement("People",
                    new System.Xml.Linq.XElement("Person",
                        new System.Xml.Linq.XAttribute("id", 1),
                        new System.Xml.Linq.XElement("Name", "Bob"),
                        new System.Xml.Linq.XElement("Age", 25)
                    )
                )
            );
            
            Console.WriteLine($"LINQ to XML:\n{xdoc}");
            
            // Query with LINQ
            var names = from p in xdoc.Descendants("Person")
                        select p.Element("Name")?.Value;
            
            Console.WriteLine($"Names: {string.Join(", ", names)}");
        }
        
        static void DemonstrateBinarySerialization()
        {
            Console.WriteLine("\n=== 3. Binary Serialization ===\n");
            
            // Note: BinaryFormatter is deprecated in .NET 5+ due to security concerns
            // Use alternatives like Protocol Buffers, MessagePack, or custom binary
            
            // Sample serializable class
            [Serializable]
            public class BinaryData : ISerializable
            {
                public string Name { get; set; }
                public int Value { get; set; }
                public DateTime Timestamp { get; set; }
                [NonSerialized]
                public string TemporaryData; // Won't be serialized
                
                // Default constructor required
                public BinaryData() { }
                
                // Constructor for deserialization
                protected BinaryData(SerializationInfo info, StreamingContext context)
                {
                    Name = info.GetString("Name");
                    Value = info.GetInt32("Value");
                    Timestamp = info.GetDateTime("Timestamp");
                }
                
                // ISerializable implementation
                public void GetObjectData(SerializationInfo info, StreamingContext context)
                {
                    info.AddValue("Name", Name);
                    info.AddValue("Value", Value);
                    info.AddValue("Timestamp", Timestamp);
                }
            }
            
            var data = new BinaryData
            {
                Name = "Test",
                Value = 42,
                Timestamp = DateTime.UtcNow,
                TemporaryData = "Not serialized"
            };
            
            // 1. BinaryFormatter (deprecated but shown for legacy)
            Console.WriteLine("1. BinaryFormatter (Legacy - Security Warning):");
            Console.WriteLine("""
                WARNING: BinaryFormatter is deprecated due to security vulnerabilities.
                Avoid in new code. Use alternatives:
                • Protocol Buffers (protobuf-net)
                • MessagePack
                • System.Text.Json with binary writer
                • Custom binary serialization
                """);
            
            // 2. Manual binary serialization
            Console.WriteLine("\n2. Manual Binary Serialization:");
            
            using (var stream = new MemoryStream())
            using (var writer = new BinaryWriter(stream, Encoding.UTF8, leaveOpen: true))
            {
                // Write string with length prefix
                writer.Write(data.Name);
                writer.Write(data.Value);
                writer.Write(data.Timestamp.Ticks);
                
                var bytes = stream.ToArray();
                Console.WriteLine($"Manual binary size: {bytes.Length} bytes");
                
                // Deserialize
                stream.Position = 0;
                using (var reader = new BinaryReader(stream, Encoding.UTF8, leaveOpen: true))
                {
                    var name = reader.ReadString();
                    var value = reader.ReadInt32();
                    var ticks = reader.ReadInt64();
                    var timestamp = new DateTime(ticks);
                    
                    Console.WriteLine($"Manual deserialized: {name}, {value}, {timestamp}");
                }
            }
            
            // 3. Protocol Buffers (protobuf-net example)
            Console.WriteLine("\n3. Protocol Buffers (protobuf-net):");
            Console.WriteLine("""
                // Install: NuGet package protobuf-net
                [ProtoContract]
                public class ProtoData
                {
                    [ProtoMember(1)]
                    public string Name { get; set; }
                    
                    [ProtoMember(2)]
                    public int Value { get; set; }
                }
                
                // Serialize
                using (var stream = new MemoryStream())
                {
                    Serializer.Serialize(stream, data);
                }
                
                Advantages:
                • Compact binary format
                • Fast serialization/deserialization
                • Version tolerant
                • Cross-platform
                """);
            
            // 4. MessagePack
            Console.WriteLine("\n4. MessagePack:");
            Console.WriteLine("""
                // Install: NuGet package MessagePack
                [MessagePackObject]
                public class MessagePackData
                {
                    [Key(0)]
                    public string Name { get; set; }
                    
                    [Key(1)]
                    public int Value { get; set; }
                }
                
                // Serialize
                var bytes = MessagePackSerializer.Serialize(data);
                
                Advantages:
                • Extremely fast
                • Very compact
                • Zero-allocation possible
                """);
            
            // 5. MemoryPack (new, high-performance)
            Console.WriteLine("\n5. MemoryPack (High-Performance):");
            Console.WriteLine("""
                // Install: NuGet package MemoryPack
                [MemoryPackable]
                public partial class MemoryPackData
                {
                    public string Name { get; set; }
                    public int Value { get; set; }
                }
                
                // Serialize (zero-allocation)
                var bytes = MemoryPackSerializer.Serialize(data);
                
                Advantages:
                • Fastest C# serializer
                • Zero-allocation
                • AOT compatible
                """);
            
            // 6. Binary security considerations
            Console.WriteLine("\n6. Binary Serialization Security:");
            Console.WriteLine("""
                Security risks with binary serialization:
                • Arbitrary type instantiation
                • Code execution during deserialization
                • Data tampering
                
                Mitigations:
                • Use secure serializers (protobuf, MessagePack)
                • Validate data before deserialization
                • Use digital signatures
                • Limit deserialization to trusted types
                """);
        }
        
        static void DemonstrateDataContractSerialization()
        {
            Console.WriteLine("\n=== 4. Data Contract Serialization ===\n");
            
            // Data contracts are used with WCF and other Microsoft technologies
            
            [DataContract(Namespace = "http://example.com/contracts")]
            public class ContractPerson
            {
                [DataMember(Name = "PersonName", Order = 1, IsRequired = true)]
                public string Name { get; set; }
                
                [DataMember(Order = 2)]
                public int Age { get; set; }
                
                [DataMember(Order = 3, EmitDefaultValue = false)]
                public DateTime? BirthDate { get; set; }
                
                // Not a DataMember - won't be serialized
                public string Secret { get; set; }
                
                [IgnoreDataMember]
                public string InternalCode { get; set; }
            }
            
            var person = new ContractPerson
            {
                Name = "Contract User",
                Age = 35,
                Secret = "Hidden"
            };
            
            // 1. DataContractSerializer (XML)
            Console.WriteLine("1. DataContractSerializer (XML):");
            
            var dcSerializer = new DataContractSerializer(typeof(ContractPerson));
            
            using (var stream = new MemoryStream())
            {
                dcSerializer.WriteObject(stream, person);
                stream.Position = 0;
                
                using (var reader = new StreamReader(stream))
                {
                    string xml = reader.ReadToEnd();
                    Console.WriteLine($"DataContract XML:\n{xml}");
                }
                
                // Deserialize
                stream.Position = 0;
                var deserialized = (ContractPerson)dcSerializer.ReadObject(stream);
                Console.WriteLine($"Deserialized: {deserialized.Name}");
            }
            
            // 2. DataContractJsonSerializer (legacy JSON)
            Console.WriteLine("\n2. DataContractJsonSerializer (Legacy):");
            
            var jsonSerializer = new DataContractJsonSerializer(typeof(ContractPerson));
            
            using (var stream = new MemoryStream())
            {
                jsonSerializer.WriteObject(stream, person);
                stream.Position = 0;
                
                using (var reader = new StreamReader(stream))
                {
                    string json = reader.ReadToEnd();
                    Console.WriteLine($"DataContract JSON:\n{json}");
                }
            }
            
            // 3. Known types for polymorphism
            Console.WriteLine("\n3. Known Types for Polymorphism:");
            
            [DataContract]
            [KnownType(typeof(Employee))]
            [KnownType(typeof(Customer))]
            public abstract class PersonBase
            {
                [DataMember]
                public string Name { get; set; }
            }
            
            [DataContract]
            public class Employee : PersonBase
            {
                [DataMember]
                public string Department { get; set; }
            }
            
            [DataContract]
            public class Customer : PersonBase
            {
                [DataMember]
                public string CustomerId { get; set; }
            }
            
            // 4. Version tolerance
            Console.WriteLine("\n4. Version Tolerance:");
            Console.WriteLine("""
                Data contracts support versioning:
                • New members ignore missing data (deserialization)
                • Missing members get default values (deserialization)
                • Use [DataMember(IsRequired = true)] for required fields
                • Use [DataMember(EmitDefaultValue = false)] to omit defaults
                """);
            
            // 5. WCF considerations
            Console.WriteLine("\n5. WCF Service Considerations:");
            Console.WriteLine("""
                For WCF services:
                • Data contracts define service boundaries
                • Use [ServiceContract] on interfaces
                • Use [OperationContract] on methods
                • Consider streaming for large data
                • Use fault contracts for errors
                """);
        }
        
        static void DemonstrateCustomSerialization()
        {
            Console.WriteLine("\n=== 5. Custom Serialization ===\n");
            
            // 1. ISerializable interface
            Console.WriteLine("1. ISerializable Interface:");
            
            [Serializable]
            public class CustomSerializable : ISerializable
            {
                public string Data { get; set; }
                public int Version { get; set; }
                private string _privateField = "Private";
                
                public CustomSerializable() { }
                
                // Protected constructor for deserialization
                protected CustomSerializable(SerializationInfo info, StreamingContext context)
                {
                    Data = info.GetString("Data");
                    Version = info.GetInt32("Version");
                    _privateField = info.GetString("PrivateField") ?? "default";
                }
                
                public void GetObjectData(SerializationInfo info, StreamingContext context)
                {
                    info.AddValue("Data", Data);
                    info.AddValue("Version", Version);
                    info.AddValue("PrivateField", _privateField);
                    info.AddValue("SerializedAt", DateTime.UtcNow);
                }
            }
            
            // 2. Custom formatters
            Console.WriteLine("\n2. Custom Formatters:");
            
            public class CustomFormatter : IFormatter
            {
                public SerializationBinder Binder { get; set; }
                public StreamingContext Context { get; set; }
                public ISurrogateSelector SurrogateSelector { get; set; }
                
                public object Deserialize(Stream serializationStream)
                {
                    // Implement custom deserialization
                    throw new NotImplementedException();
                }
                
                public void Serialize(Stream serializationStream, object graph)
                {
                    // Implement custom serialization
                    throw new NotImplementedException();
                }
            }
            
            // 3. Surrogate selectors
            Console.WriteLine("\n3. Surrogate Selectors:");
            Console.WriteLine("""
                Surrogates allow serialization of types you don't control:
                
                class CustomSurrogate : ISerializationSurrogate
                {
                    public void GetObjectData(object obj, SerializationInfo info, StreamingContext context)
                    {
                        // Extract data from obj
                    }
                    
                    public object SetObjectData(object obj, SerializationInfo info, StreamingContext context, ISurrogateSelector selector)
                    {
                        // Reconstruct object
                        return obj;
                    }
                }
                
                // Register surrogate
                var selector = new SurrogateSelector();
                selector.AddSurrogate(typeof(ThirdPartyClass), 
                    new StreamingContext(StreamingContextStates.All), 
                    new CustomSurrogate());
                """);
            
            // 4. Serialization callbacks
            Console.WriteLine("\n4. Serialization Callbacks:");
            
            [Serializable]
            public class CallbackExample
            {
                public string Data { get; set; }
                
                [OnSerializing]
                internal void OnSerializingMethod(StreamingContext context)
                {
                    Console.WriteLine("About to serialize");
                }
                
                [OnSerialized]
                internal void OnSerializedMethod(StreamingContext context)
                {
                    Console.WriteLine("Finished serializing");
                }
                
                [OnDeserializing]
                internal void OnDeserializingMethod(StreamingContext context)
                {
                    Console.WriteLine("About to deserialize");
                }
                
                [OnDeserialized]
                internal void OnDeserializedMethod(StreamingContext context)
                {
                    Console.WriteLine("Finished deserializing");
                    // Initialize transient fields here
                }
            }
            
            // 5. Compression with serialization
            Console.WriteLine("\n5. Compression with Serialization:");
            
            async Task CompressedSerializationExample()
            {
                var data = new { Name = "Test", Value = 123 };
                string json = System.Text.Json.JsonSerializer.Serialize(data);
                
                using (var compressed = new MemoryStream())
                using (var gzip = new System.IO.Compression.GZipStream(compressed, 
                       System.IO.Compression.CompressionLevel.Optimal))
                {
                    var bytes = Encoding.UTF8.GetBytes(json);
                    await gzip.WriteAsync(bytes, 0, bytes.Length);
                    await gzip.FlushAsync();
                    
                    Console.WriteLine($"Original: {bytes.Length} bytes, Compressed: {compressed.Length} bytes");
                }
            }
            CompressedSerializationExample().Wait();
            
            // 6. Encryption with serialization
            Console.WriteLine("\n6. Encryption with Serialization:");
            Console.WriteLine("""
                For sensitive data:
                1. Serialize to bytes
                2. Encrypt with AES or other symmetric algorithm
                3. Store/transmit encrypted data
                4. Decrypt before deserialization
                
                Consider:
                • Key management
                • IV (Initialization Vector) generation
                • Authenticated encryption (AEAD)
                • Performance impact
                """);
        }
        
        static void DemonstrateBestPractices()
        {
            Console.WriteLine("\n=== 6. Serialization Best Practices ===\n");
            
            Console.WriteLine("1. Choose the Right Serializer:");
            Console.WriteLine("""
                • JSON (REST APIs, web): System.Text.Json
                • High-performance binary: MessagePack, MemoryPack
                • Cross-platform/gRPC: Protocol Buffers
                • Legacy/WCF: DataContractSerializer
                • Configuration files: XML or JSON
                • Avoid: BinaryFormatter (security)
                """);
            
            Console.WriteLine("\n2. Versioning Strategy:");
            Console.WriteLine("""
                • Add new properties at the end
                • Don't remove properties (mark obsolete instead)
                • Use default values for missing properties
                • Consider [Obsolete] attribute for deprecated members
                • Test forward/backward compatibility
                """);
            
            Console.WriteLine("\n3. Security Considerations:");
            Console.WriteLine("""
                • Validate input before deserialization
                • Limit types that can be deserialized
                • Use secure serializers
                • Consider digital signatures for integrity
                • Sanitize serialized output for injection attacks
                """);
            
            Console.WriteLine("\n4. Performance Optimization:");
            Console.WriteLine("""
                • Reuse serializer instances (JsonSerializerOptions)
                • Use source generation when possible
                • Consider streaming for large data
                • Pool buffers (ArrayPool, MemoryStream)
                • Benchmark different serializers
                """);
            
            Console.WriteLine("\n5. Error Handling:");
            Console.WriteLine("""
                • Catch specific exceptions (JsonException, XmlException)
                • Provide meaningful error messages
                • Log serialization errors
                • Implement retry logic for transient failures
                • Validate data before serialization
                """);
            
            Console.WriteLine("\n6. Cross-Platform Considerations:");
            Console.WriteLine("""
                • Use UTF-8 encoding
                • Be aware of line ending differences
                • Consider time zone handling for DateTime
                • Test on target platforms
                • Use platform-independent formats
                """);
            
            Console.WriteLine("\n7. Testing Serialization:");
            Console.WriteLine("""
                • Test round-trip serialization/deserialization
                • Test with null values
                • Test with default values
                • Test version tolerance
                • Test performance with realistic data sizes
                """);
            
            Console.WriteLine("\n8. Common Patterns:");
            Console.WriteLine("""
                1. DTO (Data Transfer Object) Pattern:
                   - Simple classes for serialization
                   - Separate from business logic
                   - Optimized for serialization
                
                2. Versioned API Pattern:
                   - Different DTOs for different API versions
                   - Mapping between versions
                   - Deprecation strategy
                
                3. Caching Serialized Data:
                   - Serialize once, cache result
                   - Invalidate cache when data changes
                   - Consider compression for cached data
                
                4. Streaming Pattern:
                   - Serialize/deserialize in chunks
                   - Use streaming APIs
                   - Handle backpressure
                
                5. Polymorphic Serialization:
                   - Use discriminator field
                   - Factory pattern for deserialization
                   - Known type registration
                """);
            
            Console.WriteLine("\n=== Real-World Scenarios ===");
            Console.WriteLine("""
                1. Web API Development:
                   • Use System.Text.Json for ASP.NET Core
                   • Configure camelCase naming
                   • Handle circular references
                   • Use [JsonIgnore] for sensitive data
                
                2. Message Queue Systems:
                   • Use compact binary formats (MessagePack)
                   • Include message version
                   • Handle schema evolution
                
                3. Configuration Files:
                   • Use JSON or XML
                   • Support comments (JSON with Newtonsoft.Json)
                   • Environment-specific overrides
                
                4. Caching Layer:
                   • Serialize to Redis/other cache
                   • Use efficient binary format
                   • Include cache version for invalidation
                
                5. File Storage:
                   • Choose format based on use case
                   • Consider human readability vs performance
                   • Include metadata in serialized format
                
                6. Inter-process Communication:
                   • Use shared memory with serialization
                   • Consider performance requirements
                   • Handle version mismatch gracefully
                """);
            
            Console.WriteLine("\n=== Tools and Libraries ===");
            Console.WriteLine("""
                • System.Text.Json (built-in, high-performance)
                • Newtonsoft.Json (feature-rich, legacy compatibility)
                • protobuf-net (Protocol Buffers for .NET)
                • MessagePack-CSharp (extremely fast binary)
                • MemoryPack (fastest, zero-allocation)
                • YamlDotNet (YAML serialization)
                • CSVHelper (CSV serialization)
                • Jil (fast JSON serializer from Stack Overflow)
                
                Choose based on:
                • Performance requirements
                • Feature needs
                • Compatibility requirements
                • Security considerations
                """);
        }
    }
}