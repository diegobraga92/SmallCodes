/*
    C# DEPENDENCY INJECTION
    File: 23_dependency_injection.cs
    
    Comprehensive guide to Dependency Injection (DI) in C# and .NET Core.
    Covers DI principles, service lifetimes, registration patterns,
    constructor injection, advanced scenarios, third-party containers,
    and integration with ASP.NET Core.
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

namespace CSharpRefresher.DependencyInjection
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Dependency Injection ===\n");
            
            DemonstrateDiPrinciples();
            DemonstrateServiceLifetimes();
            DemonstrateRegistrationPatterns();
            DemonstrateInjectionTypes();
            DemonstrateAdvancedScenarios();
            DemonstrateAspNetCoreIntegration();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateDiPrinciples()
        {
            Console.WriteLine("=== 1. Dependency Injection Principles ===\n");
            
            // 1. What is Dependency Injection?
            Console.WriteLine("1. What is Dependency Injection?");
            Console.WriteLine("""
                DI is a design pattern that implements Inversion of Control (IoC) for resolving dependencies.
                
                Key principles:
                • Inversion of Control: Framework calls your code, not vice versa
                • Dependency Inversion Principle (DIP): Depend on abstractions, not concretions
                • Separation of Concerns: Business logic separated from infrastructure
                • Testability: Easy to mock dependencies for unit testing
                
                Without DI (tight coupling):
                public class OrderService
                {
                    private readonly EmailService _emailService;
                    
                    public OrderService()
                    {
                        _emailService = new EmailService(); // Direct dependency
                    }
                }
                
                With DI (loose coupling):
                public class OrderService
                {
                    private readonly IEmailService _emailService;
                    
                    public OrderService(IEmailService emailService) // Injected dependency
                    {
                        _emailService = emailService;
                    }
                }
                """);
            
            // 2. Benefits of DI
            Console.WriteLine("\n2. Benefits of Dependency Injection:");
            Console.WriteLine("""
                • Loose coupling: Components depend on abstractions, not concrete implementations
                • Testability: Easy to mock dependencies for unit testing
                • Maintainability: Changing implementations doesn't require modifying consumers
                • Reusability: Components can be reused in different contexts
                • Configuration flexibility: Dependencies can be configured at runtime
                • Lifecycle management: Automatic disposal and resource management
                • Parallel development: Teams can work on different components independently
                """);
            
            // 3. DI Containers
            Console.WriteLine("\n3. DI Containers (IoC Containers):");
            Console.WriteLine("""
                A DI container manages object creation and lifetime.
                
                Built-in .NET Core container:
                • Microsoft.Extensions.DependencyInjection
                • Lightweight, fast, integrated with ASP.NET Core
                • Sufficient for most applications
                
                Third-party containers:
                • Autofac: Feature-rich, modular registration
                • StructureMap: Convention-based registration
                • Ninject: Kernel-based, flexible binding
                • Unity: Microsoft's container (legacy)
                • Simple Injector: Fast, verification features
                
                When to use third-party containers:
                • Need advanced features (property injection, decorators)
                • Complex modular applications
                • Convention-based registration
                • Interception/AOP requirements
                """);
            
            // 4. Common anti-patterns
            Console.WriteLine("\n4. Common DI Anti-patterns:");
            Console.WriteLine("""
                1. Service Locator (anti-pattern):
                   // DON'T DO THIS
                   public class OrderService
                   {
                       public void ProcessOrder()
                       {
                           var emailService = ServiceLocator.GetService<IEmailService>();
                           // ...
                       }
                   }
                   
                   Problems:
                   • Hidden dependencies
                   • Hard to test
                   • Runtime errors instead of compile-time
                   
                2. Constructor over-injection:
                   // Too many dependencies
                   public class OrderService
                   {
                       public OrderService(
                           IEmailService email,
                           ILogger logger,
                           IDatabase db,
                           ICache cache,
                           IValidator validator,
                           IConfig config,
                           IAuditor auditor) // Too many!
                       { }
                   }
                   
                   Solution: Refactor into smaller classes
                   
                3. Captive dependencies:
                   // Singleton depending on Scoped/Transient
                   services.AddSingleton<ISingletonService>(sp =>
                       new SingletonService(sp.GetRequiredService<ITransientService>()));
                   
                   Problem: Transient captured by Singleton lives as long as Singleton
                """);
        }
        
        static void DemonstrateServiceLifetimes()
        {
            Console.WriteLine("\n=== 2. Service Lifetimes ===\n");
            
            // 1. Transient lifetime
            Console.WriteLine("1. Transient Lifetime:");
            Console.WriteLine("""
                Registration: services.AddTransient<IService, Service>();
                
                Characteristics:
                • New instance created every time it's requested
                • Suitable for lightweight, stateless services
                • No thread-safety concerns (each request gets own instance)
                • Higher memory/GC pressure if overused
                
                Example use cases:
                • Validators
                • Mappers (AutoMapper, etc.)
                • ViewModels
                • Request-specific calculations
                """);
            
            // 2. Scoped lifetime
            Console.WriteLine("\n2. Scoped Lifetime:");
            Console.WriteLine("""
                Registration: services.AddScoped<IService, Service>();
                
                Characteristics:
                • Single instance per scope (e.g., per HTTP request in ASP.NET Core)
                • Created at beginning of scope, disposed at end
                • Thread-safe within scope
                • Common for database contexts (Entity Framework)
                
                Example use cases:
                • DbContext (Entity Framework)
                • Unit of Work pattern
                • Request-specific services
                • Repository instances
                
                Creating scope manually:
                using (var scope = serviceProvider.CreateScope())
                {
                    var service = scope.ServiceProvider.GetRequiredService<IScopedService>();
                    // Use service
                } // Service disposed when scope ends
                """);
            
            // 3. Singleton lifetime
            Console.WriteLine("\n3. Singleton Lifetime:");
            Console.WriteLine("""
                Registration: services.AddSingleton<IService, Service>();
                
                Characteristics:
                • Single instance for application lifetime
                • Created on first request
                • Must be thread-safe
                • Disposed when application shuts down
                
                Example use cases:
                • Configuration services
                • Caching services
                • Logging services (ILogger is singleton-safe)
                • Connection pools
                • Background service hosts
                
                Thread safety considerations:
                public class CacheService : ICacheService
                {
                    private readonly ConcurrentDictionary<string, object> _cache;
                    private readonly object _lock = new object();
                    
                    public void Add(string key, object value)
                    {
                        // Use thread-safe collections or locking
                        _cache[key] = value;
                    }
                }
                """);
            
            // 4. Lifetime comparisons and guidelines
            Console.WriteLine("\n4. Lifetime Guidelines:");
            Console.WriteLine("""
                Choosing the right lifetime:
                
                Use Transient when:
                • Service is stateless
                • Service is lightweight to create
                • Each consumer needs its own instance
                • Service implements IDisposable with lightweight resources
                
                Use Scoped when:
                • Service needs to maintain state within a logical operation
                • Service uses resources that should be cleaned up after operation
                • Service is Entity Framework DbContext
                • Multiple consumers in same scope should share instance
                
                Use Singleton when:
                • Service is stateless and thread-safe
                • Service is expensive to create (configuration, connections)
                • Service needs to maintain application-wide state (cache)
                • Service should exist for application lifetime
                
                General rules:
                • Prefer shorter lifetimes (Transient > Scoped > Singleton)
                • Singleton should not depend on Scoped or Transient
                • Be cautious with IDisposable in Singleton
                • Consider using factories for complex lifetime requirements
                """);
            
            // 5. Lifetime validation and common issues
            Console.WriteLine("\n5. Lifetime Validation:");
            Console.WriteLine("""
                Common lifetime issues:
                
                1. Captive dependency:
                   // Singleton captures Scoped dependency
                   services.AddSingleton<ISingleton>(sp => 
                       new Singleton(sp.GetRequiredService<IScoped>())); // BAD
                   
                2. Scoped service resolved from Singleton:
                   public class SingletonService
                   {
                       public SingletonService(IServiceProvider provider)
                       {
                           // This creates a captive dependency
                           using var scope = provider.CreateScope();
                           var scoped = scope.ServiceProvider.GetRequiredService<IScoped>();
                       }
                   }
                   
                3. Multiple Dispose() calls:
                   // If registered multiple times with different lifetimes
                   services.AddScoped<IDisposableService, DisposableService>();
                   services.AddSingleton<IDisposableService, DisposableService>(); // BAD
                   
                Enable validation in development:
                public void ConfigureServices(IServiceCollection services)
                {
                    services.AddControllers()
                        .AddControllersAsServices(); // Helps with validation
                    
                    // Build and validate
                    var serviceProvider = services.BuildServiceProvider(validateScopes: true);
                    // In ASP.NET Core, this happens automatically in Development
                }
                """);
        }
        
        static void DemonstrateRegistrationPatterns()
        {
            Console.WriteLine("\n=== 3. Registration Patterns ===\n");
            
            // 1. Basic registration
            Console.WriteLine("1. Basic Registration Methods:");
            
            // Example service interfaces and implementations
            public interface IEmailService { }
            public class SmtpEmailService : IEmailService { }
            public class SendGridEmailService : IEmailService { }
            
            public interface ILoggerService { }
            public class FileLoggerService : ILoggerService { }
            public class DatabaseLoggerService : ILoggerService { }
            
            Console.WriteLine("""
                // Register interface with implementation
                services.AddTransient<IEmailService, SmtpEmailService>();
                
                // Register concrete type (less common)
                services.AddTransient<SmtpEmailService>();
                
                // Register instance (pre-created object)
                var emailService = new SmtpEmailService();
                services.AddSingleton<IEmailService>(emailService);
                
                // Register with factory method
                services.AddScoped<IEmailService>(sp =>
                {
                    var config = sp.GetRequiredService<IConfiguration>();
                    var logger = sp.GetRequiredService<ILogger<SmtpEmailService>>();
                    return new SmtpEmailService(config, logger);
                });
                
                // Register multiple implementations
                services.AddTransient<IEmailService, SmtpEmailService>();
                services.AddTransient<IEmailService, SendGridEmailService>();
                // Resolved as IEnumerable<IEmailService>
                """);
            
            // 2. Multiple implementations and named services
            Console.WriteLine("\n2. Multiple Implementations:");
            Console.WriteLine("""
                Strategy pattern with multiple implementations:
                
                // Define strategy interface
                public interface IPaymentProcessor
                {
                    bool CanProcess(string paymentType);
                    Task<PaymentResult> ProcessAsync(PaymentRequest request);
                }
                
                // Implementations
                public class CreditCardProcessor : IPaymentProcessor { }
                public class PayPalProcessor : IPaymentProcessor { }
                public class BitcoinProcessor : IPaymentProcessor { }
                
                // Registration
                services.AddTransient<IPaymentProcessor, CreditCardProcessor>();
                services.AddTransient<IPaymentProcessor, PayPalProcessor>();
                services.AddTransient<IPaymentProcessor, BitcoinProcessor>();
                
                // Consumer
                public class PaymentService
                {
                    private readonly IEnumerable<IPaymentProcessor> _processors;
                    
                    public PaymentService(IEnumerable<IPaymentProcessor> processors)
                    {
                        _processors = processors;
                    }
                    
                    public async Task<PaymentResult> ProcessAsync(PaymentRequest request)
                    {
                        var processor = _processors.FirstOrDefault(p => p.CanProcess(request.Type));
                        if (processor == null)
                            throw new InvalidOperationException($"No processor for {request.Type}");
                        
                        return await processor.ProcessAsync(request);
                    }
                }
                
                Named services pattern (using factory):
                services.AddTransient<CreditCardProcessor>();
                services.AddTransient<PayPalProcessor>();
                services.AddTransient<BitcoinProcessor>();
                
                services.AddTransient<IPaymentProcessorFactory, PaymentProcessorFactory>();
                """);
            
            // 3. Open generics registration
            Console.WriteLine("\n3. Open Generics Registration:");
            Console.WriteLine("""
                // Generic repository pattern
                public interface IRepository<T> where T : class
                {
                    Task<T> GetByIdAsync(int id);
                    Task AddAsync(T entity);
                }
                
                public class EfRepository<T> : IRepository<T> where T : class
                {
                    private readonly DbContext _context;
                    
                    public EfRepository(T context)
                    {
                        _context = context;
                    }
                    
                    // Implementation...
                }
                
                // Single registration for all types
                services.AddScoped(typeof(IRepository<>), typeof(EfRepository<>));
                
                // Usage - automatically resolved for any T
                public class UserService
                {
                    private readonly IRepository<User> _userRepository;
                    
                    public UserService(IRepository<User> userRepository)
                    {
                        _userRepository = userRepository; // Resolves to EfRepository<User>
                    }
                }
                
                // Also works with multiple generic parameters
                public interface ICache<TKey, TValue> { }
                public class MemoryCache<TKey, TValue> : ICache<TKey, TValue> { }
                
                services.AddSingleton(typeof(ICache<,>), typeof(MemoryCache<,>));
                """);
            
            // 4. Decorator pattern registration
            Console.WriteLine("\n4. Decorator Pattern:");
            Console.WriteLine("""
                // Base service
                public interface IDataService
                {
                    Task<Data> GetDataAsync(int id);
                }
                
                public class DataService : IDataService
                {
                    public async Task<Data> GetDataAsync(int id) { /* ... */ }
                }
                
                // Decorator 1: Caching
                public class CachingDataService : IDataService
                {
                    private readonly IDataService _inner;
                    private readonly ICache _cache;
                    
                    public CachingDataService(IDataService inner, ICache cache)
                    {
                        _inner = inner;
                        _cache = cache;
                    }
                    
                    public async Task<Data> GetDataAsync(int id)
                    {
                        var cacheKey = $"data_{id}";
                        if (_cache.TryGet(cacheKey, out Data cached))
                            return cached;
                            
                        var data = await _inner.GetDataAsync(id);
                        _cache.Set(cacheKey, data, TimeSpan.FromMinutes(5));
                        return data;
                    }
                }
                
                // Decorator 2: Logging
                public class LoggingDataService : IDataService
                {
                    private readonly IDataService _inner;
                    private readonly ILogger _logger;
                    
                    public LoggingDataService(IDataService inner, ILogger logger)
                    {
                        _inner = inner;
                        _logger = logger;
                    }
                    
                    public async Task<Data> GetDataAsync(int id)
                    {
                        _logger.LogInformation($"Getting data for id: {id}");
                        try
                        {
                            var result = await _inner.GetDataAsync(id);
                            _logger.LogInformation($"Successfully got data for id: {id}");
                            return result;
                        }
                        catch (Exception ex)
                        {
                            _logger.LogError(ex, $"Error getting data for id: {id}");
                            throw;
                        }
                    }
                }
                
                // Manual decorator registration
                services.AddScoped<IDataService>(sp =>
                {
                    var logger = sp.GetRequiredService<ILogger<LoggingDataService>>();
                    var cache = sp.GetRequiredService<ICache>();
                    
                    // Create chain: Logging -> Caching -> DataService
                    var dataService = new DataService();
                    var cachingService = new CachingDataService(dataService, cache);
                    var loggingService = new LoggingDataService(cachingService, logger);
                    
                    return loggingService;
                });
                
                // With third-party containers (Autofac), decorators are easier
                """);
            
            // 5. Conditional registration
            Console.WriteLine("\n5. Conditional Registration:");
            Console.WriteLine("""
                // Based on configuration
                var emailProvider = Configuration["Email:Provider"];
                
                if (emailProvider == "SendGrid")
                {
                    services.AddTransient<IEmailService, SendGridEmailService>();
                }
                else if (emailProvider == "SMTP")
                {
                    services.AddTransient<IEmailService, SmtpEmailService>();
                }
                else
                {
                    services.AddTransient<IEmailService, MockEmailService>();
                }
                
                // Based on environment
                if (env.IsDevelopment())
                {
                    services.AddTransient<IEmailService, MockEmailService>();
                    services.AddTransient<IPaymentService, MockPaymentService>();
                }
                else
                {
                    services.AddTransient<IEmailService, SmtpEmailService>();
                    services.AddTransient<IPaymentService, RealPaymentService>();
                }
                
                // Feature flags
                var featureFlags = Configuration.GetSection("Features").Get<FeatureFlags>();
                
                if (featureFlags.EnableCaching)
                {
                    services.AddSingleton<ICacheService, RedisCacheService>();
                }
                else
                {
                    services.AddSingleton<ICacheService, NullCacheService>();
                }
                
                // TryAdd registration (don't replace existing)
                services.TryAddSingleton<ICacheService, MemoryCacheService>();
                services.TryAddSingleton<ICacheService, RedisCacheService>(); // Won't replace
                
                // TryAddScoped, TryAddTransient also available
                """);
        }
        
        static void DemonstrateInjectionTypes()
        {
            Console.WriteLine("\n=== 4. Injection Types ===\n");
            
            // 1. Constructor injection (recommended)
            Console.WriteLine("1. Constructor Injection (Recommended):");
            Console.WriteLine("""
                public class OrderService
                {
                    private readonly IEmailService _emailService;
                    private readonly ILogger<OrderService> _logger;
                    private readonly IPaymentService _paymentService;
                    
                    // Dependencies clearly declared in constructor
                    public OrderService(
                        IEmailService emailService,
                        ILogger<OrderService> logger,
                        IPaymentService paymentService)
                    {
                        _emailService = emailService ?? throw new ArgumentNullException(nameof(emailService));
                        _logger = logger ?? throw new ArgumentNullException(nameof(logger));
                        _paymentService = paymentService ?? throw new ArgumentNullException(nameof(paymentService));
                    }
                    
                    public async Task ProcessOrderAsync(Order order)
                    {
                        _logger.LogInformation("Processing order {OrderId}", order.Id);
                        await _paymentService.ProcessPaymentAsync(order);
                        await _emailService.SendOrderConfirmationAsync(order);
                    }
                }
                
                Benefits:
                • Dependencies are explicit and required
                • Class is immutable (readonly fields)
                • Easy to test (pass mock dependencies)
                • Compile-time checking
                
                Best practices:
                • Use readonly fields for injected dependencies
                • Validate null arguments
                • Keep constructor simple (no logic)
                • Consider maximum 3-4 dependencies (refactor if more)
                """);
            
            // 2. Property injection (use sparingly)
            Console.WriteLine("\n2. Property Injection:");
            Console.WriteLine("""
                // Mark property with [FromServices] or use third-party containers
                public class ReportService
                {
                    // Optional dependency
                    [FromServices] // ASP.NET Core attribute
                    public IFormatter Formatter { get; set; }
                    
                    // Required dependency (set via constructor)
                    private readonly IDataService _dataService;
                    
                    public ReportService(IDataService dataService)
                    {
                        _dataService = dataService;
                    }
                    
                    public Report GenerateReport()
                    {
                        // Formatter may be null if not injected
                        if (Formatter == null)
                            throw new InvalidOperationException("Formatter not set");
                            
                        var data = _dataService.GetData();
                        return Formatter.Format(data);
                    }
                }
                
                Use cases:
                • Optional dependencies (plugins, extensions)
                • Framework components (ASP.NET MVC filters)
                • Circular dependency workarounds (avoid if possible)
                • Legacy code integration
                
                Drawbacks:
                • Dependencies not explicit in constructor
                • Can be null at runtime
                • Harder to test (need to set properties)
                • Breaks immutability
                
                With third-party containers (Autofac example):
                builder.RegisterType<ReportService>()
                    .PropertiesAutowired(); // Auto-wires properties
                """);
            
            // 3. Method injection
            Console.WriteLine("\n3. Method Injection:");
            Console.WriteLine("""
                // Inject dependency directly into method
                public class OrderProcessor
                {
                    public async Task ProcessAsync(
                        Order order, 
                        [FromServices] IEmailService emailService) // Method injection
                    {
                        // Process order...
                        await emailService.SendConfirmationAsync(order);
                    }
                }
                
                // More common pattern: Pass dependency as parameter
                public class DataTransformer
                {
                    public Data Transform(Data input, ITransformer transformer)
                    {
                        return transformer.Transform(input);
                    }
                }
                
                Use cases:
                • Single-use dependencies
                • Strategy pattern implementations
                • Factory methods
                • Extension methods
                
                ASP.NET Core minimal APIs:
                app.MapPost("/orders", async (Order order, IEmailService emailService) =>
                {
                    // emailService injected into method
                    await emailService.SendConfirmationAsync(order);
                    return Results.Ok();
                });
                
                Benefits:
                • Clear which methods need which dependencies
                • Can use different implementations per call
                • No need to store dependencies in fields
                
                Drawbacks:
                • Method signature becomes complex
                • Caller needs to provide dependencies
                • Can't be used with constructor-only DI containers
                """);
            
            // 4. IServiceProvider injection (service locator pattern - use cautiously)
            Console.WriteLine("\n4. IServiceProvider Injection (Service Locator):");
            Console.WriteLine("""
                // Sometimes necessary for factories or complex scenarios
                public class ServiceFactory
                {
                    private readonly IServiceProvider _serviceProvider;
                    
                    public ServiceFactory(IServiceProvider serviceProvider)
                    {
                        _serviceProvider = serviceProvider;
                    }
                    
                    public IReportService CreateReportService(string reportType)
                    {
                        return reportType switch
                        {
                            "pdf" => _serviceProvider.GetRequiredService<PdfReportService>(),
                            "excel" => _serviceProvider.GetRequiredService<ExcelReportService>(),
                            _ => throw new ArgumentException($"Unknown report type: {reportType}")
                        };
                    }
                }
                
                Valid use cases:
                • Abstract factories
                • Resolving named services
                • Lazy resolution
                • Resolving IEnumerable<T> of services
                • Complex object graphs
                
                Anti-pattern examples:
                // DON'T: Service locator in business logic
                public class OrderService
                {
                    private readonly IServiceProvider _serviceProvider;
                    
                    public void ProcessOrder()
                    {
                        // Hidden dependency
                        var emailService = _serviceProvider.GetRequiredService<IEmailService>();
                        emailService.Send(...);
                    }
                }
                
                Best practices:
                • Keep IServiceProvider usage in composition root or factories
                • Avoid in business logic classes
                • Consider using typed factories instead
                • Document why IServiceProvider is needed
                """);
        }
        
        static void DemonstrateAdvancedScenarios()
        {
            Console.WriteLine("\n=== 5. Advanced Scenarios ===\n");
            
            // 1. Factories and Func<T>
            Console.WriteLine("1. Factories and Func<T>:");
            Console.WriteLine("""
                // Func<T> factory
                services.AddTransient<IService, Service>();
                services.AddTransient<Func<IService>>(sp => 
                    () => sp.GetRequiredService<IService>());
                
                // Usage
                public class Consumer
                {
                    private readonly Func<IService> _serviceFactory;
                    
                    public Consumer(Func<IService> serviceFactory)
                    {
                        _serviceFactory = serviceFactory;
                    }
                    
                    public void DoWork()
                    {
                        // Create new instance each time
                        using var service = _serviceFactory();
                        service.DoSomething();
                    }
                }
                
                // Typed factory interface
                public interface IServiceFactory
                {
                    IService CreateService();
                    void ReleaseService(IService service);
                }
                
                public class ServiceFactory : IServiceFactory
                {
                    private readonly IServiceProvider _serviceProvider;
                    
                    public ServiceFactory(IServiceProvider serviceProvider)
                    {
                        _serviceProvider = serviceProvider;
                    }
                    
                    public IService CreateService()
                    {
                        return _serviceProvider.GetRequiredService<IService>();
                    }
                    
                    public void ReleaseService(IService service)
                    {
                        // Handle disposal if needed
                        if (service is IDisposable disposable)
                            disposable.Dispose();
                    }
                }
                
                // Register factory
                services.AddSingleton<IServiceFactory, ServiceFactory>();
                """);
            
            // 2. Lazy<T> resolution
            Console.WriteLine("\n2. Lazy<T> Resolution:");
            Console.WriteLine("""
                // Automatic Lazy<T> support
                services.AddTransient<IService, ExpensiveService>();
                
                // Consumer can request Lazy<IService>
                public class Consumer
                {
                    private readonly Lazy<IService> _lazyService;
                    
                    public Consumer(Lazy<IService> lazyService)
                    {
                        _lazyService = lazyService;
                    }
                    
                    public void DoWork()
                    {
                        // Service only created when Value is accessed
                        if (SomeCondition)
                        {
                            var service = _lazyService.Value;
                            service.DoSomething();
                        }
                    }
                }
                
                // Manual Lazy registration
                services.AddSingleton<Lazy<IService>>(sp =>
                    new Lazy<IService>(() => sp.GetRequiredService<IService>()));
                
                Use cases:
                • Expensive to create services
                • Services that might not be needed
                • Circular dependency resolution
                • Optional features
                """);
            
            // 3. Option pattern and configuration
            Console.WriteLine("\n4. Options Pattern:");
            Console.WriteLine("""
                // Configuration class
                public class EmailSettings
                {
                    public string SmtpServer { get; set; }
                    public int Port { get; set; }
                    public string Username { get; set; }
                    public string Password { get; set; }
                }
                
                // appsettings.json
                {
                  "EmailSettings": {
                    "SmtpServer": "smtp.gmail.com",
                    "Port": 587,
                    "Username": "user@example.com"
                  }
                }
                
                // Registration
                services.Configure<EmailSettings>(Configuration.GetSection("EmailSettings"));
                
                // Usage with IOptions<T>
                public class EmailService : IEmailService
                {
                    private readonly EmailSettings _settings;
                    
                    public EmailService(IOptions<EmailSettings> options)
                    {
                        _settings = options.Value;
                    }
                    
                    public void SendEmail()
                    {
                        // Use _settings.SmtpServer, etc.
                    }
                }
                
                // IOptionsSnapshot for scoped (updated per request)
                public class ScopedService
                {
                    public ScopedService(IOptionsSnapshot<EmailSettings> options)
                    {
                        // Gets current configuration (can change between requests)
                        var settings = options.Value;
                    }
                }
                
                // IOptionsMonitor for singleton (gets updates)
                public class SingletonService : IDisposable
                {
                    private readonly IDisposable _changeToken;
                    private EmailSettings _settings;
                    
                    public SingletonService(IOptionsMonitor<EmailSettings> options)
                    {
                        _settings = options.CurrentValue;
                        // Listen for changes
                        _changeToken = options.OnChange(newSettings =>
                        {
                            _settings = newSettings;
                        });
                    }
                    
                    public void Dispose()
                    {
                        _changeToken?.Dispose();
                    }
                }
                
                // Named options
                services.Configure<EmailSettings>("Primary", Configuration.GetSection("Email:Primary"));
                services.Configure<EmailSettings>("Secondary", Configuration.GetSection("Email:Secondary"));
                
                // Resolve named options
                var primaryOptions = serviceProvider.GetRequiredService<IOptionsMonitor<EmailSettings>>()
                    .Get("Primary");
                """);
            
            // 4. Validation with DI
            Console.WriteLine("\n5. Validation in DI:");
            Console.WriteLine("""
                // Validate on startup
                public void ConfigureServices(IServiceCollection services)
                {
                    // Build service provider with validation
                    var serviceProvider = services.BuildServiceProvider(
                        new ServiceProviderOptions
                        {
                            ValidateScopes = true,
                            ValidateOnBuild = true
                        });
                        
                    // This will throw if:
                    // • Unresolvable dependencies exist
                    // • Captive dependencies detected
                    // • Scoped services resolved from root
                }
                
                // Manual validation
                var errors = services.BuildServiceProvider(
                    validateScopes: true)
                    .GetValidationErrors();
                
                foreach (var error in errors)
                {
                    Console.WriteLine($"DI Error: {error}");
                }
                
                // ASP.NET Core automatic validation
                // In Development environment, ASP.NET Core validates scopes automatically
                
                // Using hosted service for startup validation
                public class StartupValidationService : IHostedService
                {
                    private readonly IServiceProvider _serviceProvider;
                    
                    public StartupValidationService(IServiceProvider serviceProvider)
                    {
                        _serviceProvider = serviceProvider;
                    }
                    
                    public Task StartAsync(CancellationToken cancellationToken)
                    {
                        // Try to resolve key services to validate DI
                        try
                        {
                            _serviceProvider.GetRequiredService<ICriticalService>();
                            _serviceProvider.GetRequiredService<IAnotherService>();
                        }
                        catch (Exception ex)
                        {
                            throw new InvalidOperationException(
                                "DI validation failed on startup", ex);
                        }
                        
                        return Task.CompletedTask;
                    }
                    
                    public Task StopAsync(CancellationToken cancellationToken)
                        => Task.CompletedTask;
                }
                
                services.AddHostedService<StartupValidationService>();
                """);
        }
        
        static void DemonstrateAspNetCoreIntegration()
        {
            Console.WriteLine("\n=== 6. ASP.NET Core Integration ===\n");
            
            // 1. ASP.NET Core startup configuration
            Console.WriteLine("1. ASP.NET Core Startup Configuration:");
            Console.WriteLine("""
                // Program.cs (.NET 6+ minimal API)
                var builder = WebApplication.CreateBuilder(args);
                
                // Add services to DI container
                builder.Services.AddControllers();
                builder.Services.AddEndpointsApiExplorer();
                builder.Services.AddSwaggerGen();
                
                // Custom services
                builder.Services.AddScoped<IUserService, UserService>();
                builder.Services.AddScoped<IEmailService, EmailService>();
                builder.Services.AddSingleton<ICacheService, RedisCacheService>();
                
                // Configuration
                builder.Services.Configure<AppSettings>(builder.Configuration);
                
                var app = builder.Build();
                
                // Traditional Startup.cs (pre-.NET 6)
                public class Startup
                {
                    public Startup(IConfiguration configuration)
                    {
                        Configuration = configuration;
                    }
                    
                    public IConfiguration Configuration { get; }
                    
                    public void ConfigureServices(IServiceCollection services)
                    {
                        // DI configuration here
                        services.AddControllers();
                        services.AddScoped<IUserService, UserService>();
                        // ...
                    }
                    
                    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
                    {
                        // Middleware pipeline
                        if (env.IsDevelopment())
                        {
                            app.UseDeveloperExceptionPage();
                        }
                        
                        app.UseRouting();
                        app.UseAuthorization();
                        app.UseEndpoints(endpoints =>
                        {
                            endpoints.MapControllers();
                        });
                    }
                }
                """);
            
            // 2. Controller activation and constructor injection
            Console.WriteLine("\n2. Controller DI Integration:");
            Console.WriteLine("""
                // Controllers support constructor injection automatically
                [ApiController]
                [Route("api/[controller]")]
                public class UsersController : ControllerBase
                {
                    private readonly IUserService _userService;
                    private readonly ILogger<UsersController> _logger;
                    private readonly IEmailService _emailService;
                    
                    // Dependencies injected automatically
                    public UsersController(
                        IUserService userService,
                        ILogger<UsersController> logger,
                        IEmailService emailService)
                    {
                        _userService = userService;
                        _logger = logger;
                        _emailService = emailService;
                    }
                    
                    [HttpGet("{id}")]
                    public async Task<ActionResult<User>> GetUser(int id)
                    {
                        _logger.LogInformation("Getting user {UserId}", id);
                        var user = await _userService.GetUserAsync(id);
                        if (user == null)
                            return NotFound();
                            
                        return Ok(user);
                    }
                }
                
                // Action method injection
                [HttpGet("profile")]
                public IActionResult GetProfile([FromServices] IProfileService profileService)
                {
                    // profileService injected into method
                    var profile = profileService.GetProfile();
                    return Ok(profile);
                }
                
                // View injection (Razor Pages)
                @inject IEmailService EmailService
                
                <div>
                    @if (EmailService.IsConfigured)
                    {
                        <span>Email service is ready</span>
                    }
                </div>
                """);
            
            // 3. Middleware DI
            Console.WriteLine("\n3. Middleware Dependency Injection:");
            Console.WriteLine("""
                // Middleware with constructor injection
                public class CustomMiddleware
                {
                    private readonly RequestDelegate _next;
                    private readonly ILogger<CustomMiddleware> _logger;
                    private readonly IConfiguration _configuration;
                    
                    // Dependencies injected via constructor
                    public CustomMiddleware(
                        RequestDelegate next,
                        ILogger<CustomMiddleware> logger,
                        IConfiguration configuration)
                    {
                        _next = next;
                        _logger = logger;
                        _configuration = configuration;
                    }
                    
                    public async Task InvokeAsync(HttpContext context)
                    {
                        _logger.LogInformation("Middleware executing");
                        
                        // Add scoped services to Invoke method
                        var scopedService = context.RequestServices.GetRequiredService<IScopedService>();
                        
                        await _next(context);
                    }
                }
                
                // Extension method for registration
                public static class CustomMiddlewareExtensions
                {
                    public static IApplicationBuilder UseCustomMiddleware(this IApplicationBuilder builder)
                    {
                        return builder.UseMiddleware<CustomMiddleware>();
                    }
                }
                
                // Usage in Startup.Configure
                app.UseCustomMiddleware();
                
                // Factory-based middleware (better performance)
                public class FactoryActivatedMiddleware : IMiddleware
                {
                    private readonly ILogger<FactoryActivatedMiddleware> _logger;
                    
                    public FactoryActivatedMiddleware(ILogger<FactoryActivatedMiddleware> logger)
                    {
                        _logger = logger;
                    }
                    
                    public async Task InvokeAsync(HttpContext context, RequestDelegate next)
                    {
                        _logger.LogInformation("Factory middleware executing");
                        await next(context);
                    }
                }
                
                // Registration
                services.AddSingleton<FactoryActivatedMiddleware>();
                
                // Usage
                app.UseMiddleware<FactoryActivatedMiddleware>();
                """);
            
            // 4. Hosted services and background jobs
            Console.WriteLine("""
                4. Hosted Services (Background Jobs):
                
                // IHostedService implementation
                public class BackgroundEmailService : IHostedService, IDisposable
                {
                    private readonly IServiceProvider _serviceProvider;
                    private readonly ILogger<BackgroundEmailService> _logger;
                    private Timer _timer;
                    
                    // Constructor injection
                    public BackgroundEmailService(
                        IServiceProvider serviceProvider,
                        ILogger<BackgroundEmailService> logger)
                    {
                        _serviceProvider = serviceProvider;
                        _logger = logger;
                    }
                    
                    public Task StartAsync(CancellationToken cancellationToken)
                    {
                        _logger.LogInformation("Background email service starting");
                        _timer = new Timer(DoWork, null, TimeSpan.Zero, TimeSpan.FromMinutes(5));
                        return Task.CompletedTask;
                    }
                    
                    private void DoWork(object state)
                    {
                        // Create scope for scoped services
                        using var scope = _serviceProvider.CreateScope();
                        var emailService = scope.ServiceProvider.GetRequiredService<IEmailService>();
                        var dbContext = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
                        
                        // Process emails...
                    }
                    
                    public Task StopAsync(CancellationToken cancellationToken)
                    {
                        _logger.LogInformation("Background email service stopping");
                        _timer?.Change(Timeout.Infinite, 0);
                        return Task.CompletedTask;
                    }
                    
                    public void Dispose()
                    {
                        _timer?.Dispose();
                    }
                }
                
                // Registration
                services.AddHostedService<BackgroundEmailService>();
                
                // BackgroundService abstract class (recommended)
                public class QueuedHostedService : BackgroundService
                {
                    private readonly IBackgroundTaskQueue _taskQueue;
                    private readonly IServiceProvider _serviceProvider;
                    private readonly ILogger<QueuedHostedService> _logger;
                    
                    public QueuedHostedService(
                        IBackgroundTaskQueue taskQueue,
                        IServiceProvider serviceProvider,
                        ILogger<QueuedHostedService> logger)
                    {
                        _taskQueue = taskQueue;
                        _serviceProvider = serviceProvider;
                        _logger = logger;
                    }
                    
                    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
                    {
                        _logger.LogInformation("Queued hosted service starting");
                        
                        while (!stoppingToken.IsCancellationRequested)
                        {
                            var workItem = await _taskQueue.DequeueAsync(stoppingToken);
                            
                            try
                            {
                                using var scope = _serviceProvider.CreateScope();
                                await workItem(scope.ServiceProvider, stoppingToken);
                            }
                            catch (Exception ex)
                            {
                                _logger.LogError(ex, "Error processing work item");
                            }
                        }
                    }
                }
                """);
            
            // 5. Testing with DI
            Console.WriteLine("\n5. Testing with Dependency Injection:");
            Console.WriteLine("""
                // Unit test with mocked dependencies
                [Test]
                public void OrderService_ProcessOrder_SendsEmail()
                {
                    // Arrange
                    var mockEmailService = new Mock<IEmailService>();
                    var mockLogger = new Mock<ILogger<OrderService>>();
                    var mockPaymentService = new Mock<IPaymentService>();
                    
                    var orderService = new OrderService(
                        mockEmailService.Object,
                        mockLogger.Object,
                        mockPaymentService.Object);
                    
                    var order = new Order { Id = 1, Total = 100.00m };
                    
                    // Act
                    orderService.ProcessOrder(order);
                    
                    // Assert
                    mockEmailService.Verify(
                        e => e.SendOrderConfirmationAsync(order),
                        Times.Once);
                }
                
                // Integration test with real DI container
                public class IntegrationTests : IClassFixture<WebApplicationFactory<Startup>>
                {
                    private readonly WebApplicationFactory<Startup> _factory;
                    
                    public IntegrationTests(WebApplicationFactory<Startup> factory)
                    {
                        _factory = factory;
                    }
                    
                    [Fact]
                    public async Task Get_Endpoint_ReturnsSuccess()
                    {
                        // Create client with custom service overrides
                        var client = _factory.WithWebHostBuilder(builder =>
                        {
                            builder.ConfigureTestServices(services =>
                            {
                                // Replace real services with test doubles
                                services.AddScoped<IEmailService, MockEmailService>();
                                services.AddScoped<IPaymentService, MockPaymentService>();
                            });
                        }).CreateClient();
                        
                        // Act
                        var response = await client.GetAsync("/api/users/1");
                        
                        // Assert
                        response.EnsureSuccessStatusCode();
                    }
                }
                
                // Testing service registration
                [Fact]
                public void ServiceCollection_RegistersAllRequiredServices()
                {
                    // Arrange
                    var services = new ServiceCollection();
                    var startup = new Startup(Configuration);
                    
                    // Act
                    startup.ConfigureServices(services);
                    
                    // Assert
                    var serviceProvider = services.BuildServiceProvider();
                    
                    // Verify key services can be resolved
                    Assert.NotNull(serviceProvider.GetService<IUserService>());
                    Assert.NotNull(serviceProvider.GetService<IEmailService>());
                    Assert.NotNull(serviceProvider.GetService<ILoggerFactory>());
                    
                    // Verify lifetime
                    var userServiceDescriptor = services.First(s => s.ServiceType == typeof(IUserService));
                    Assert.Equal(ServiceLifetime.Scoped, userServiceDescriptor.Lifetime);
                }
                """);
            
            // 6. Best practices summary
            Console.WriteLine("\n=== Dependency Injection Best Practices ===");
            Console.WriteLine("""
                1. Use constructor injection as primary method
                2. Prefer interfaces over concrete classes
                3. Keep constructors simple (no business logic)
                4. Avoid service locator pattern in business logic
                5. Choose appropriate lifetimes (Transient < Scoped < Singleton)
                6. Validate DI configuration in development
                7. Use options pattern for configuration
                8. Consider using third-party containers for advanced scenarios
                9. Implement IDisposable properly for disposable dependencies
                10. Test DI configuration in integration tests
                
                Performance tips:
                • Use Singleton for stateless, thread-safe services
                • Avoid capturing Scoped/Transient in Singleton
                • Use AddSingleton() for already-created instances
                • Consider using compiled lambdas for complex object graphs
                
                Common pitfalls to avoid:
                • Circular dependencies (refactor design)
                • Captive dependencies (Singleton holding Scoped)
                • Over-injection (too many dependencies - refactor)
                • Property injection for required dependencies
                • Resolving from root container in background services
                
                Migration guidance:
                • Start with built-in container for new projects
                • Consider third-party containers for complex existing systems
                • Gradually refactor towards constructor injection
                • Use adapter pattern for legacy code integration
                """);
        }
    }
    
    // Supporting interfaces and classes for examples
    public interface IEmailService
    {
        Task SendOrderConfirmationAsync(Order order);
        Task SendEmailAsync(string to, string subject, string body);
    }
    
    public interface IPaymentService
    {
        Task<PaymentResult> ProcessPaymentAsync(Order order);
    }
    
    public interface IDataService
    {
        Task<Data> GetDataAsync(int id);
    }
    
    public interface ICache
    {
        bool TryGet<T>(string key, out T value);
        void Set<T>(string key, T value, TimeSpan expiration);
    }
    
    public interface IBackgroundTaskQueue
    {
        Task<Func<IServiceProvider, CancellationToken, Task>> DequeueAsync(CancellationToken cancellationToken);
        void QueueBackgroundWorkItem(Func<IServiceProvider, CancellationToken, Task> workItem);
    }
    
    // Supporting classes
    public class Order { public int Id { get; set; } public decimal Total { get; set; } }
    public class Data { public int Id { get; set; } public string Content { get; set; } }
    public class PaymentResult { public bool Success { get; set; } public string TransactionId { get; set; } }
    public class User { public int Id { get; set; } public string Name { get; set; } }
    
    // Example implementations
    public class SmtpEmailService : IEmailService
    {
        private readonly ILogger<SmtpEmailService> _logger;
        
        public SmtpEmailService(ILogger<SmtpEmailService> logger)
        {
            _logger = logger;
        }
        
        public Task SendOrderConfirmationAsync(Order order)
        {
            _logger.LogInformation("Sending order confirmation for order {OrderId}", order.Id);
            return Task.CompletedTask;
        }
        
        public Task SendEmailAsync(string to, string subject, string body)
        {
            _logger.LogInformation("Sending email to {To} with subject {Subject}", to, subject);
            return Task.CompletedTask;
        }
    }
    
    public class UserService : IUserService
    {
        private readonly IRepository<User> _userRepository;
        private readonly ILogger<UserService> _logger;
        
        public UserService(IRepository<User> userRepository, ILogger<UserService> logger)
        {
            _userRepository = userRepository;
            _logger = logger;
        }
        
        public async Task<User> GetUserAsync(int id)
        {
            _logger.LogInformation("Getting user {UserId}", id);
            return await _userRepository.GetByIdAsync(id);
        }
    }
    
    public interface IUserService
    {
        Task<User> GetUserAsync(int id);
    }
    
    public interface IRepository<T>
    {
        Task<T> GetByIdAsync(int id);
        Task AddAsync(T entity);
    }
    
    public class EfRepository<T> : IRepository<T> where T : class
    {
        private readonly DbContext _context;
        
        public EfRepository(DbContext context)
        {
            _context = context;
        }
        
        public async Task<T> GetByIdAsync(int id)
        {
            return await _context.Set<T>().FindAsync(id);
        }
        
        public async Task AddAsync(T entity)
        {
            await _context.Set<T>().AddAsync(entity);
            await _context.SaveChangesAsync();
        }
    }
    
    // Mock DbContext for example
    public class DbContext : IDisposable
    {
        public void Dispose() { }
        public DbSet<T> Set<T>() where T : class => new DbSet<T>();
    }
    
    public class DbSet<T> where T : class
    {
        public Task<T> FindAsync(params object[] keyValues) => Task.FromResult(default(T));
        public Task AddAsync(T entity, CancellationToken cancellationToken = default) => Task.CompletedTask;
    }
}
