/*
    C# NAMESPACES AND ASSEMBLIES
    File: 14_namespaces_assemblies.cs
    
    Comprehensive guide to namespaces (logical organization) 
    and assemblies (physical deployment) in C#.
    Covers namespace design, assembly structure, versioning,
    strong naming, and deployment strategies.
*/

using System;
using System.Reflection;
using System.IO;
using System.Collections.Generic;
using System.Runtime.Loader;

namespace CSharpRefresher.NamespacesAssemblies
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Namespaces and Assemblies ===\n");
            
            DemonstrateNamespaces();
            DemonstrateAssemblyBasics();
            DemonstrateAssemblyLoading();
            DemonstrateStrongNaming();
            DemonstratePracticalScenarios();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateNamespaces()
        {
            Console.WriteLine("=== 1. Namespaces ===\n");
            
            // Basic namespace declaration
            namespace Company.Product.Module
            {
                public class Service
                {
                    public void Execute() => Console.WriteLine("Service executed");
                }
            }
            
            // Using directives
            using Company.Product.Module;
            
            // Namespace aliases
            using AliasService = Company.Product.Module.Service;
            var service = new AliasService();
            service.Execute();
            
            // Global namespace qualification
            global::System.Console.WriteLine("Global namespace access");
            
            // Nested namespaces (two ways)
            namespace Outer
            {
                namespace Inner
                {
                    class NestedClass { }
                }
            }
            
            namespace Outer.Inner.Deep
            {
                class DeepClass { }
            }
            
            Console.WriteLine("\nNamespace best practices:");
            Console.WriteLine("""
                1. Use PascalCase for namespace names
                2. Follow Company.Product.Module pattern
                3. Avoid deep nesting (max 3-4 levels)
                4. Keep related types together
                5. Use meaningful, descriptive names
                6. Consider backward compatibility
                7. Avoid namespace collisions
                """);
            
            // Namespace resolution example
            Console.WriteLine("\nNamespace resolution order:");
            Console.WriteLine("1. Current namespace");
            Console.WriteLine("2. Namespaces in using directives");
            Console.WriteLine("3. Outer namespaces (if nested)");
            Console.WriteLine("4. Global namespace");
        }
        
        static void DemonstrateAssemblyBasics()
        {
            Console.WriteLine("\n=== 2. Assembly Basics ===\n");
            
            // Get current assembly info
            var assembly = Assembly.GetExecutingAssembly();
            
            Console.WriteLine($"Assembly Name: {assembly.GetName().Name}");
            Console.WriteLine($"Full Name: {assembly.GetName().FullName}");
            Console.WriteLine($"Version: {assembly.GetName().Version}");
            Console.WriteLine($"Location: {assembly.Location}");
            Console.WriteLine($"Is Fully Trusted: {assembly.IsFullyTrusted}");
            Console.WriteLine($"Entry Point: {assembly.EntryPoint?.Name}");
            
            // Assembly manifest
            Console.WriteLine("\nAssembly Manifest Contents:");
            Console.WriteLine("• Assembly identity (name, version, culture, public key)");
            Console.WriteLine("• List of files in assembly");
            Console.WriteLine("• Referenced assemblies");
            Console.WriteLine("• Permission requests");
            Console.WriteLine("• Exported types");
            
            // Types of assemblies
            Console.WriteLine("\nAssembly Types:");
            Console.WriteLine("• EXE (executable) - has entry point, runs as application");
            Console.WriteLine("• DLL (library) - no entry point, used by other assemblies");
            Console.WriteLine("• NETMODULE - compiled module without assembly manifest");
            
            // Multi-file assemblies (rarely used)
            Console.WriteLine("\nMulti-file Assemblies:");
            Console.WriteLine("""
                Rare feature allowing:
                • Separate modules for different languages
                • Dynamic loading of modules
                • Reduced memory footprint
                • Mostly replaced by single-file deployments
                """);
        }
        
        static void DemonstrateAssemblyLoading()
        {
            Console.WriteLine("\n=== 3. Assembly Loading ===\n");
            
            // Different ways to load assemblies
            Console.WriteLine("Assembly Loading Methods:");
            
            // 1. Load by name (from GAC or application base)
            try
            {
                var sysAssembly = Assembly.Load("System");
                Console.WriteLine($"Loaded System: {sysAssembly.GetName().Version}");
            }
            catch (FileNotFoundException)
            {
                Console.WriteLine("System assembly not found");
            }
            
            // 2. Load from file path
            var currentPath = Assembly.GetExecutingAssembly().Location;
            var fileAssembly = Assembly.LoadFile(currentPath);
            Console.WriteLine($"Loaded from file: {fileAssembly.GetName().Name}");
            
            // 3. Load from byte array
            byte[] assemblyBytes = File.ReadAllBytes(currentPath);
            var byteAssembly = Assembly.Load(assemblyBytes);
            Console.WriteLine($"Loaded from bytes: {byteAssembly.GetName().Name}");
            
            // 4. Reflection-only load
            var reflectionAssembly = Assembly.ReflectionOnlyLoadFrom(currentPath);
            Console.WriteLine($"Reflection-only load: {reflectionAssembly.GetName().Name}");
            
            // Assembly resolution events
            AppDomain.CurrentDomain.AssemblyResolve += (sender, args) =>
            {
                Console.WriteLine($"Resolving assembly: {args.Name}");
                return null; // Continue with default resolution
            };
            
            // Assembly load context (.NET Core)
            var alc = new CustomLoadContext();
            var contextAssembly = alc.LoadFromAssemblyPath(currentPath);
            Console.WriteLine($"Loaded via custom context: {contextAssembly.GetName().Name}");
            
            // Probing paths
            Console.WriteLine("\nAssembly Probing Order:");
            Console.WriteLine("1. Global Assembly Cache (GAC)");
            Console.WriteLine("2. CodeBase hint (if specified)");
            Console.WriteLine("3. Application base directory");
            Console.WriteLine("4. Private bin paths");
            Console.WriteLine("5. Culture-specific subdirectories");
        }
        
        static void DemonstrateStrongNaming()
        {
            Console.WriteLine("\n=== 4. Strong Naming and Signing ===\n");
            
            // Strong name components
            Console.WriteLine("Strong Name Components:");
            Console.WriteLine("• Simple name (e.g., 'MyAssembly')");
            Console.WriteLine("• Version number (e.g., 1.2.3.4)");
            Console.WriteLine("• Culture info (e.g., 'en-US' or neutral)");
            Console.WriteLine("• Public key (for verification)");
            Console.WriteLine("• Digital signature (for integrity)");
            
            // Assembly versioning
            Console.WriteLine("\nAssembly Versioning:");
            Console.WriteLine("""
                Format: Major.Minor.Build.Revision
                • Major: Breaking changes
                • Minor: Backward-compatible features
                • Build: Compilation number (often auto-incremented)
                • Revision: Patch/fix number
                
                Common attributes:
                [assembly: AssemblyVersion("1.0.0.0")]
                [assembly: AssemblyFileVersion("1.0.0.0")]
                [assembly: AssemblyInformationalVersion("1.0.0-alpha")]
                """);
            
            // Delay signing
            Console.WriteLine("\nDelay Signing Process:");
            Console.WriteLine("1. Generate public/private key pair: sn -k key.snk");
            Console.WriteLine("2. Extract public key: sn -p key.snk public.snk");
            Console.WriteLine("3. Add to project: [assembly: AssemblyKeyFile("public.snk")]");
            Console.WriteLine("4. Enable delay signing: [assembly: AssemblyDelaySign(true)]");
            Console.WriteLine("5. After building, sign with private key: sn -R assembly.dll key.snk");
            
            // Global Assembly Cache (GAC)
            Console.WriteLine("\nGlobal Assembly Cache (GAC):");
            Console.WriteLine("""
                Purpose:
                • Shared assembly storage
                • Side-by-side versioning
                • Centralized management
                
                Commands:
                • Install: gacutil -i assembly.dll
                • Uninstall: gacutil -u assembly
                • List: gacutil -l
                
                Note: GAC is Windows-specific, less used in .NET Core
                """);
            
            // Authenticode signing
            Console.WriteLine("\nAuthenticode Code Signing:");
            Console.WriteLine("""
                Purpose:
                • Verify publisher identity
                • Ensure code integrity
                • Required for Windows Store, drivers
                
                Process:
                1. Obtain code signing certificate
                2. Sign assembly: signtool sign /f cert.pfx /p password assembly.dll
                3. Verify signature: signtool verify /v assembly.dll
                """);
        }
        
        static void DemonstratePracticalScenarios()
        {
            Console.WriteLine("\n=== 5. Practical Scenarios ===\n");
            
            // 1. Plugin architecture
            Console.WriteLine("1. Plugin Architecture:");
            
            interface IPlugin
            {
                string Name { get; }
                void Execute();
            }
            
            // Simulate loading plugins from directory
            var pluginDir = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "plugins");
            if (Directory.Exists(pluginDir))
            {
                foreach (var dll in Directory.GetFiles(pluginDir, "*.dll"))
                {
                    try
                    {
                        var pluginAssembly = Assembly.LoadFrom(dll);
                        var pluginTypes = pluginAssembly.GetTypes()
                            .Where(t => typeof(IPlugin).IsAssignableFrom(t) && !t.IsAbstract);
                        
                        foreach (var type in pluginTypes)
                        {
                            var plugin = Activator.CreateInstance(type) as IPlugin;
                            Console.WriteLine($"  Loaded plugin: {plugin.Name}");
                        }
                    }
                    catch (Exception ex)
                    {
                        Console.WriteLine($"  Failed to load {dll}: {ex.Message}");
                    }
                }
            }
            
            // 2. Assembly version binding redirect
            Console.WriteLine("\n2. Version Binding Redirect:");
            Console.WriteLine("""
                app.config/web.config:
                <configuration>
                  <runtime>
                    <assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
                      <dependentAssembly>
                        <assemblyIdentity name="MyLibrary" 
                                          publicKeyToken="..." 
                                          culture="neutral" />
                        <bindingRedirect oldVersion="1.0.0.0-1.5.0.0" 
                                         newVersion="2.0.0.0" />
                      </dependentAssembly>
                    </assemblyBinding>
                  </runtime>
                </configuration>
                """);
            
            // 3. Satellite assemblies for localization
            Console.WriteLine("\n3. Satellite Assemblies (Localization):");
            Console.WriteLine("""
                Structure:
                • Main assembly: MyApp.dll
                • Satellite: MyApp.resources.dll (in en-US/, fr-FR/, etc.)
                • Contain only resources, no code
                
                Loading resources automatically based on CurrentUICulture
                """);
            
            // 4. Single-file deployment
            Console.WriteLine("\n4. Single-File Deployment (.NET Core 3.0+):");
            Console.WriteLine("""
                Publish command:
                dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true
                
                Benefits:
                • Single executable
                • No external dependencies
                • Simplified distribution
                • Improved startup time
                """);
            
            // 5. Assembly trimming
            Console.WriteLine("\n5. Assembly Trimming (.NET Core 3.0+):");
            Console.WriteLine("""
                Reduces deployment size by removing unused code:
                
                Publish command:
                dotnet publish -c Release -r win-x64 /p:PublishTrimmed=true
                
                Considerations:
                • May break reflection-based code
                • Use [DynamicallyAccessedMembers] attribute
                • Test thoroughly after trimming
                """);
            
            Console.WriteLine("\n=== Best Practices ===");
            Console.WriteLine("""
                Namespace Design:
                1. Follow established conventions
                2. Avoid too many using directives
                3. Use aliases for disambiguation
                4. Consider namespace hierarchy for large projects
                
                Assembly Design:
                1. Keep assemblies focused (Single Responsibility)
                2. Consider deployment dependencies
                3. Use strong naming for shared libraries
                4. Implement proper versioning strategy
                5. Consider framework compatibility
                
                Deployment:
                1. Use NuGet for dependency management
                2. Consider framework-dependent vs self-contained
                3. Implement proper error handling for missing assemblies
                4. Use configuration files for binding redirects
                5. Consider using AssemblyLoadContext for dynamic loading
                
                Security:
                1. Sign assemblies for production
                2. Validate assembly integrity
                3. Consider code access security requirements
                4. Keep dependencies updated
                """);
        }
    }
    
    // Custom AssemblyLoadContext for .NET Core
    class CustomLoadContext : AssemblyLoadContext
    {
        public CustomLoadContext() : base(isCollectible: true)
        {
        }
        
        protected override Assembly Load(AssemblyName assemblyName)
        {
            // Custom loading logic
            return null; // Use default loading
        }
    }
    
    // Example namespace hierarchy
    namespace Company
    {
        namespace Product
        {
            namespace Data
            {
                public class Repository { }
            }
            
            namespace Services
            {
                public class Service
                {
                    private readonly Data.Repository _repo;
                    
                    public Service(Data.Repository repo)
                    {
                        _repo = repo;
                    }
                }
            }
            
            namespace Web.Controllers
            {
                public class HomeController
                {
                    private readonly Services.Service _service;
                    
                    public HomeController(Services.Service service)
                    {
                        _service = service;
                    }
                }
            }
        }
    }
}