/*
    C# UNIT TESTING WITH XUNIT
    File: 24_testing_xunit.cs
    
    Comprehensive guide to unit testing in C# using xUnit.net.
    Covers test fundamentals, assertions, test organization, mocking,
    test-driven development, integration testing, and best practices.
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Xunit;
using Moq;
using FluentAssertions;

namespace CSharpRefresher.TestingXunit
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Unit Testing with xUnit ===\n");
            
            DemonstrateTestFundamentals();
            DemonstrateAssertionsAndFluentAssertions();
            DemonstrateTestOrganization();
            DemonstrateMockingAndIsolation();
            DemonstrateTestDrivenDevelopment();
            DemonstrateIntegrationTesting();
            DemonstrateBestPractices();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateTestFundamentals()
        {
            Console.WriteLine("=== 1. Test Fundamentals ===\n");
            
            // 1. What is unit testing?
            Console.WriteLine("1. What is Unit Testing?");
            Console.WriteLine("""
                Unit testing is testing individual units of code in isolation.
                
                Characteristics of good unit tests:
                • Fast: Run in milliseconds
                • Isolated: Don't depend on external systems
                • Repeatable: Same result every time
                • Self-verifying: Pass/fail without manual inspection
                • Timely: Written at the same time as production code
                
                Benefits:
                • Catch bugs early
                • Documentation of behavior
                • Enables refactoring
                • Improves design (testable code is better designed)
                """);
            
            // 2. xUnit.net basics
            Console.WriteLine("\n2. xUnit.net Basics:");
            Console.WriteLine("""
                xUnit.net is a modern testing framework for .NET.
                
                Key features:
                • [Fact] attribute for parameterless tests
                • [Theory] attribute for parameterized tests
                • [InlineData] for providing test data
                • [MemberData] for complex test data
                • [ClassData] for class-based test data
                • Extensible via custom attributes
                
                Comparison with other frameworks:
                • NUnit: [Test], [TestCase], Setup/Teardown methods
                • MSTest: [TestMethod], [TestClass], test context
                • xUnit: More modern, cleaner design
                """);
            
            // 3. Basic test structure
            Console.WriteLine("\n3. Basic Test Structure:");
            
            // Example class to test
            public class Calculator
            {
                public int Add(int a, int b) => a + b;
                public int Subtract(int a, int b) => a - b;
                public int Multiply(int a, int b) => a * b;
                public int Divide(int a, int b)
                {
                    if (b == 0) throw new DivideByZeroException();
                    return a / b;
                }
            }
            
            Console.WriteLine("""
                // Simple test class
                public class CalculatorTests
                {
                    [Fact]
                    public void Add_TwoNumbers_ReturnsSum()
                    {
                        // Arrange
                        var calculator = new Calculator();
                        int a = 5;
                        int b = 3;
                        
                        // Act
                        int result = calculator.Add(a, b);
                        
                        // Assert
                        Assert.Equal(8, result);
                    }
                }
                
                Test lifecycle:
                • Test class constructor runs before each test
                • Dispose() runs after each test if IDisposable
                • No [SetUp]/[TearDown] methods (use constructor/Dispose)
                """);
        }
        
        static void DemonstrateAssertionsAndFluentAssertions()
        {
            Console.WriteLine("\n=== 2. Assertions and Fluent Assertions ===\n");
            
            // 1. xUnit assertions
            Console.WriteLine("1. xUnit Built-in Assertions:");
            Console.WriteLine("""
                Common assertions:
                
                // Equality
                Assert.Equal(expected, actual);
                Assert.NotEqual(unexpected, actual);
                
                // Boolean
                Assert.True(condition);
                Assert.False(condition);
                
                // Null
                Assert.Null(obj);
                Assert.NotNull(obj);
                
                // Collections
                Assert.Contains(expected, collection);
                Assert.DoesNotContain(unexpected, collection);
                Assert.Empty(collection);
                Assert.NotEmpty(collection);
                
                // Types
                Assert.IsType<T>(obj);
                Assert.IsNotType<T>(obj);
                Assert.IsAssignableFrom<T>(obj);
                
                // Exceptions
                var exception = Assert.Throws<DivideByZeroException>(() => 
                    calculator.Divide(1, 0));
                Assert.Equal("Attempted to divide by zero.", exception.Message);
                
                // Async exceptions
                await Assert.ThrowsAsync<DivideByZeroException>(() => 
                    calculator.DivideAsync(1, 0));
                
                // Ranges
                Assert.InRange(value, low, high);
                Assert.NotInRange(value, low, high);
                
                // Events
                var raisedEvent = Assert.Raises<EventArgs>(
                    handler => obj.Event += handler,
                    handler => obj.Event -= handler,
                    () => obj.DoSomething());
                """);
            
            // 2. Fluent Assertions library
            Console.WriteLine("\n2. Fluent Assertions:");
            Console.WriteLine("""
                Install FluentAssertions package for more expressive tests.
                
                Basic usage:
                actual.Should().Be(expected);
                actual.Should().NotBe(unexpected);
                actual.Should().BeGreaterThan(min);
                actual.Should().BeLessThanOrEqualTo(max);
                
                String assertions:
                "Hello".Should().StartWith("He").And.EndWith("lo");
                "".Should().BeNullOrEmpty();
                "text".Should().Contain("ex");
                
                Collection assertions:
                collection.Should().HaveCount(3);
                collection.Should().Contain(item);
                collection.Should().BeEquivalentTo(expectedCollection);
                collection.Should().BeInAscendingOrder();
                
                Object assertions:
                person.Should().BeEquivalentTo(expectedPerson);
                person.Should().NotBeSameAs(otherPerson);
                person.Address.Should().NotBeNull();
                
                Exception assertions:
                action.Should().Throw<InvalidOperationException>()
                    .WithMessage("Expected message")
                    .WithInnerException<ArgumentException>();
                
                Async assertions:
                await func.Should().ThrowAsync<InvalidOperationException>();
                
                Date/time assertions:
                date.Should().BeAfter(startDate).And.BeBefore(endDate);
                date.Should().BeCloseTo(expected, TimeSpan.FromSeconds(1));
                """);
            
            // 3. Custom assertions
            Console.WriteLine("\n3. Custom Assertions:");
            Console.WriteLine("""
                Create domain-specific assertions:
                
                public static class CustomerAssertions
                {
                    public static void ShouldBeValid(this Customer customer)
                    {
                        Assert.NotNull(customer);
                        Assert.False(string.IsNullOrEmpty(customer.Name));
                        Assert.Matches(@"^[^@]+@[^@]+\.[^@]+$", customer.Email);
                        Assert.InRange(customer.Age, 18, 120);
                    }
                    
                    public static void ShouldHaveOrder(this Customer customer, 
                        string orderNumber)
                    {
                        Assert.Contains(customer.Orders, 
                            o => o.OrderNumber == orderNumber);
                    }
                }
                
                Usage:
                customer.ShouldBeValid();
                customer.ShouldHaveOrder("ORD-123");
                """);
        }
        
        static void DemonstrateTestOrganization()
        {
            Console.WriteLine("\n=== 3. Test Organization ===\n");
            
            // 1. Test class organization
            Console.WriteLine("1. Test Class Organization:");
            Console.WriteLine("""
                Common patterns:
                
                1. One test class per production class:
                   • Calculator → CalculatorTests
                   • OrderService → OrderServiceTests
                   
                2. One test class per feature:
                   • AuthenticationTests (covers multiple classes)
                   • PaymentProcessingTests
                   
                3. Nested test classes for complex classes:
                   public class OrderServiceTests
                   {
                       public class ProcessOrder : OrderServiceTests
                       {
                           [Fact] public void ValidOrder_Success() { }
                           [Fact] public void InvalidOrder_Throws() { }
                       }
                       
                       public class CancelOrder : OrderServiceTests
                       {
                           [Fact] public void ExistingOrder_Cancels() { }
                       }
                   }
                   
                Naming conventions:
                • ClassNameTests for test classes
                • MethodName_Scenario_ExpectedBehavior for test methods
                • Use underscores for readability
                """);
            
            // 2. Test data and theories
            Console.WriteLine("\n2. Test Data and Theories:");
            Console.WriteLine("""
                Parameterized tests with [Theory]:
                
                [Theory]
                [InlineData(2, 3, 5)]
                [InlineData(0, 0, 0)]
                [InlineData(-1, 1, 0)]
                public void Add_VariousNumbers_ReturnsCorrectSum(int a, int b, int expected)
                {
                    var calculator = new Calculator();
                    var result = calculator.Add(a, b);
                    Assert.Equal(expected, result);
                }
                
                Complex test data with [MemberData]:
                
                public static IEnumerable<object[]> TestData =>
                    new List<object[]>
                    {
                        new object[] { 1, 2, 3 },
                        new object[] { 0, 0, 0 },
                        new object[] { -1, -1, -2 }
                    };
                
                [Theory]
                [MemberData(nameof(TestData))]
                public void Add_MemberData_ReturnsCorrectSum(int a, int b, int expected)
                {
                    var calculator = new Calculator();
                    var result = calculator.Add(a, b);
                    Assert.Equal(expected, result);
                }
                
                Class-based test data:
                
                public class CalculatorTestData : IEnumerable<object[]>
                {
                    public IEnumerator<object[]> GetEnumerator()
                    {
                        yield return new object[] { 1, 2, 3 };
                        yield return new object[] { 0, 0, 0 };
                    }
                    
                    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
                }
                
                [Theory]
                [ClassData(typeof(CalculatorTestData))]
                public void Add_ClassData_ReturnsCorrectSum(int a, int b, int expected)
                {
                    // ...
                }
                """);
            
            // 3. Test fixtures and shared context
            Console.WriteLine("\n3. Test Fixtures and Shared Context:");
            Console.WriteLine("""
                Using constructors and IDisposable:
                
                public class DatabaseTests : IDisposable
                {
                    private readonly DatabaseConnection _connection;
                    
                    public DatabaseTests()
                    {
                        // Setup runs before each test
                        _connection = new DatabaseConnection();
                        _connection.Open();
                    }
                    
                    public void Dispose()
                    {
                        // Cleanup runs after each test
                        _connection?.Close();
                        _connection?.Dispose();
                    }
                    
                    [Fact]
                    public void Test1() { /* uses _connection */ }
                    
                    [Fact]
                    public void Test2() { /* uses _connection */ }
                }
                
                Collection fixtures for shared expensive setup:
                
                [CollectionDefinition("DatabaseCollection")]
                public class DatabaseCollection : ICollectionFixture<DatabaseFixture> { }
                
                public class DatabaseFixture : IDisposable
                {
                    public DatabaseConnection Connection { get; }
                    
                    public DatabaseFixture()
                    {
                        Connection = new DatabaseConnection();
                        Connection.Open();
                    }
                    
                    public void Dispose() => Connection?.Close();
                }
                
                [Collection("DatabaseCollection")]
                public class DatabaseTests1
                {
                    private readonly DatabaseFixture _fixture;
                    
                    public DatabaseTests1(DatabaseFixture fixture)
                    {
                        _fixture = fixture;
                    }
                    
                    [Fact]
                    public void Test1() { /* uses _fixture.Connection */ }
                }
                
                [Collection("DatabaseCollection")]
                public class DatabaseTests2
                {
                    private readonly DatabaseFixture _fixture;
                    
                    public DatabaseTests2(DatabaseFixture fixture)
                    {
                        _fixture = fixture;
                    }
                    
                    [Fact]
                    public void Test2() { /* uses _fixture.Connection */ }
                }
                """);
        }
        
        static void DemonstrateMockingAndIsolation()
        {
            Console.WriteLine("\n=== 4. Mocking and Isolation ===\n");
            
            // 1. Mocking with Moq
            Console.WriteLine("1. Mocking with Moq:");
            Console.WriteLine("""
                Install Moq package for creating test doubles.
                
                Basic mocking:
                
                public interface IEmailService
                {
                    void SendEmail(string to, string subject, string body);
                    Task SendEmailAsync(string to, string subject, string body);
                }
                
                // Create mock
                var mockEmailService = new Mock<IEmailService>();
                
                // Setup method calls
                mockEmailService.Setup(es => es.SendEmail(
                    "test@example.com", 
                    "Subject", 
                    "Body"))
                    .Verifiable();
                
                // Setup async methods
                mockEmailService.Setup(es => es.SendEmailAsync(
                    It.IsAny<string>(), 
                    It.IsAny<string>(), 
                    It.IsAny<string>()))
                    .Returns(Task.CompletedTask);
                
                // Setup properties
                mockEmailService.SetupProperty(es => es.IsEnabled, true);
                
                // Get mock object
                IEmailService emailService = mockEmailService.Object;
                
                // Verify calls
                mockEmailService.Verify(es => es.SendEmail(
                    "test@example.com", 
                    "Subject", 
                    "Body"), 
                    Times.Once);
                
                mockEmailService.VerifyAll(); // Verifies all setups marked .Verifiable()
                """);
            
            // 2. Argument matching
            Console.WriteLine("\n2. Argument Matching:");
            Console.WriteLine("""
                Flexible argument matching:
                
                // Match any value
                mock.Setup(m => m.Method(It.IsAny<string>()))
                    .Returns("result");
                
                // Match specific value
                mock.Setup(m => m.Method("exact"))
                    .Returns("exact result");
                
                // Match using predicate
                mock.Setup(m => m.Method(It.Is<string>(s => s.Length > 5)))
                    .Returns("long string");
                
                // Match using regex
                mock.Setup(m => m.Method(It.IsRegex(@"^\d+$")))
                    .Returns("numbers");
                
                // Match using reference equality
                var expectedObject = new object();
                mock.Setup(m => m.Method(expectedObject))
                    .Returns("same object");
                
                // Out parameters
                string output;
                mock.Setup(m => m.TryGetValue(It.IsAny<string>(), out output))
                    .Returns(true)
                    .Callback((string key, out string val) => 
                    {
                        val = "mocked value";
                    });
                
                // Ref parameters
                mock.Setup(m => m.Update(ref It.Ref<int>.IsAny))
                    .Callback((ref int value) => value *= 2);
                """);
            
            // 3. Callbacks and verification
            Console.WriteLine("\n3. Callbacks and Verification:");
            Console.WriteLine("""
                Tracking calls with callbacks:
                
                var callCount = 0;
                var capturedEmails = new List<string>();
                
                mockEmailService.Setup(es => es.SendEmail(
                    It.IsAny<string>(), 
                    It.IsAny<string>(), 
                    It.IsAny<string>()))
                    .Callback<string, string, string>((to, subject, body) =>
                    {
                        callCount++;
                        capturedEmails.Add(to);
                        Console.WriteLine($"Email sent to {to}");
                    })
                    .Verifiable();
                
                Advanced verification:
                
                // Verify specific number of calls
                mockEmailService.Verify(es => es.SendEmail(
                    It.IsAny<string>(), 
                    It.IsAny<string>(), 
                    It.IsAny<string>()), 
                    Times.Exactly(3));
                
                // Verify no calls
                mockEmailService.Verify(es => es.SendEmail(
                    It.IsAny<string>(), 
                    It.IsAny<string>(), 
                    It.IsAny<string>()), 
                    Times.Never);
                
                // Verify with custom message
                mockEmailService.Verify(es => es.SendEmail(
                    "expected@example.com", 
                    It.IsAny<string>(), 
                    It.IsAny<string>()), 
                    Times.Once,
                    "Email should have been sent to expected@example.com");
                
                // Verify order of calls
                var mock1 = new Mock<IService1>();
                var mock2 = new Mock<IService2>();
                
                var sequence = new MockSequence();
                mock1.InSequence(sequence).Setup(m => m.Method1());
                mock2.InSequence(sequence).Setup(m => m.Method2());
                """);
            
            // 4. Test doubles patterns
            Console.WriteLine("\n4. Test Doubles Patterns:");
            Console.WriteLine("""
                Different types of test doubles:
                
                1. Dummy: Object passed but never used
                   var dummy = new Mock<IUnusedService>().Object;
                   
                2. Fake: Working implementation with simplified behavior
                   public class FakeUserRepository : IUserRepository
                   {
                       private readonly List<User> _users = new();
                       
                       public Task<User> GetByIdAsync(int id) =>
                           Task.FromResult(_users.FirstOrDefault(u => u.Id == id));
                           
                       public Task AddAsync(User user)
                       {
                           _users.Add(user);
                           return Task.CompletedTask;
                       }
                   }
                   
                3. Stub: Provides predetermined responses
                   var stub = new Mock<IConfiguration>();
                   stub.Setup(c => c.GetValue<string>("ApiKey"))
                       .Returns("test-key");
                       
                4. Mock: Verifies interactions (behavior verification)
                   var mock = new Mock<IEmailService>();
                   // Setup expectations
                   mock.Setup(e => e.SendEmail(...));
                   // Verify after test
                   mock.Verify(e => e.SendEmail(...), Times.Once);
                   
                5. Spy: Records interactions for later verification
                   public class EmailSpy : IEmailService
                   {
                       public List<Email> SentEmails { get; } = new();
                       
                       public void SendEmail(string to, string subject, string body)
                       {
                           SentEmails.Add(new Email(to, subject, body));
                       }
                   }
                """);
        }
        
        static void DemonstrateTestDrivenDevelopment()
        {
            Console.WriteLine("\n=== 5. Test-Driven Development (TDD) ===\n");
            
            // 1. TDD workflow
            Console.WriteLine("1. TDD Workflow (Red-Green-Refactor):");
            Console.WriteLine("""
                Three laws of TDD:
                1. You may not write production code until you have written a failing test
                2. You may not write more of a test than is sufficient to fail
                3. You may not write more production code than is sufficient to pass the test
                
                TDD cycle:
                
                1. RED: Write a failing test
                   [Fact]
                   public void Add_EmptyString_ReturnsZero()
                   {
                       var calculator = new StringCalculator();
                       int result = calculator.Add("");
                       Assert.Equal(0, result);
                   }
                   
                2. GREEN: Make the test pass (simplest solution)
                   public class StringCalculator
                   {
                       public int Add(string numbers) => 0;
                   }
                   
                3. REFACTOR: Improve code while keeping tests green
                   // Clean up implementation, remove duplication, etc.
                   
                4. Repeat with next test case
                   [Fact]
                   public void Add_SingleNumber_ReturnsNumber()
                   {
                       var calculator = new StringCalculator();
                       int result = calculator.Add("5");
                       Assert.Equal(5, result);
                   }
                """);
            
            // 2. Example: String calculator
            Console.WriteLine("\n2. TDD Example: String Calculator:");
            Console.WriteLine("""
                Implementing StringCalculator step by step:
                
                Step 1: Empty string returns 0
                [Fact] public void Add_EmptyString_ReturnsZero()
                => Assert.Equal(0, new StringCalculator().Add(""));
                
                Step 2: Single number returns that number
                [Fact] public void Add_SingleNumber_ReturnsNumber()
                => Assert.Equal(5, new StringCalculator().Add("5"));
                
                Step 3: Two numbers comma delimited returns sum
                [Fact] public void Add_TwoNumbers_ReturnsSum()
                => Assert.Equal(8, new StringCalculator().Add("3,5"));
                
                Step 4: Handle unknown amount of numbers
                [Fact] public void Add_MultipleNumbers_ReturnsSum()
                => Assert.Equal(15, new StringCalculator().Add("1,2,3,4,5"));
                
                Step 5: Handle new lines as delimiters
                [Fact] public void Add_NewLineDelimiter_ReturnsSum()
                => Assert.Equal(6, new StringCalculator().Add("1\n2,3"));
                
                Step 6: Support custom delimiters
                [Fact] public void Add_CustomDelimiter_ReturnsSum()
                => Assert.Equal(3, new StringCalculator().Add("//;\n1;2"));
                
                Step 7: Negative numbers throw exception
                [Fact] public void Add_NegativeNumber_ThrowsException()
                => Assert.Throws<ArgumentException>(() => 
                    new StringCalculator().Add("1,-2,3"));
                
                Final implementation handles all requirements.
                """);
            
            // 3. Benefits and challenges
            Console.WriteLine("\n3. TDD Benefits and Challenges:");
            Console.WriteLine("""
                Benefits:
                • Comprehensive test coverage
                • Better design (testable code emerges)
                • Living documentation
                • Confidence to refactor
                • Fewer bugs in production
                
                Challenges:
                • Learning curve
                • Slower initial development
                • Over-testing trivial code
                • Maintaining test suite
                • Testing legacy code
                
                When to use TDD:
                • Complex business logic
                • Critical code paths
                • Algorithms and calculations
                • API boundaries
                
                When not to use TDD:
                • Prototyping and exploration
                • Simple CRUD operations
                • Generated code
                • UI code (use integration tests instead)
                """);
        }
        
        static void DemonstrateIntegrationTesting()
        {
            Console.WriteLine("\n=== 6. Integration Testing ===\n");
            
            // 1. What are integration tests?
            Console.WriteLine("1. What are Integration Tests?");
            Console.WriteLine("""
                Integration tests verify that multiple components work together.
                
                Characteristics:
                • Test interactions between components
                • May use real dependencies (databases, APIs)
                • Slower than unit tests
                • Fewer in number than unit tests
                
                Test pyramid:
                • Unit tests: Many, fast, isolated (base)
                • Integration tests: Fewer, slower (middle)
                • End-to-end tests: Fewest, slowest (top)
                
                Common integration test scenarios:
                • Database operations
                • File system interactions
                • External API calls
                • Message queue processing
                • Authentication/authorization flows
                """);
            
            // 2. ASP.NET Core integration testing
            Console.WriteLine("\n2. ASP.NET Core Integration Testing:");
            Console.WriteLine("""
                Using WebApplicationFactory:
                
                public class IntegrationTests : IClassFixture<WebApplicationFactory<Startup>>
                {
                    private readonly WebApplicationFactory<Startup> _factory;
                    
                    public IntegrationTests(WebApplicationFactory<Startup> factory)
                    {
                        _factory = factory;
                    }
                    
                    [Fact]
                    public async Task Get_EndpointReturnsSuccess()
                    {
                        // Arrange
                        var client = _factory.CreateClient();
                        
                        // Act
                        var response = await client.GetAsync("/api/users");
                        
                        // Assert
                        response.EnsureSuccessStatusCode();
                        Assert.Equal("application/json", 
                            response.Content.Headers.ContentType?.MediaType);
                    }
                    
                    [Fact]
                    public async Task Post_ValidUser_CreatesUser()
                    {
                        // Arrange
                        var client = _factory.CreateClient();
                        var user = new { Name = "Test", Email = "test@example.com" };
                        var content = new StringContent(
                            JsonSerializer.Serialize(user),
                            Encoding.UTF8,
                            "application/json");
                        
                        // Act
                        var response = await client.PostAsync("/api/users", content);
                        
                        // Assert
                        response.EnsureSuccessStatusCode();
                        Assert.Equal(HttpStatusCode.Created, response.StatusCode);
                        
                        var location = response.Headers.Location?.ToString();
                        Assert.StartsWith("/api/users/", location);
                    }
                }
                
                Customizing the factory:
                
                public class CustomWebApplicationFactory : WebApplicationFactory<Startup>
                {
                    protected override void ConfigureWebHost(IWebHostBuilder builder)
                    {
                        builder.ConfigureTestServices(services =>
                        {
                            // Replace real services with test doubles
                            services.RemoveAll<IDatabaseService>();
                            services.AddSingleton<IDatabaseService, TestDatabaseService>();
                            
                            // Configure test database
                            services.RemoveAll<DbContextOptions<AppDbContext>>();
                            services.AddDbContext<AppDbContext>(options =>
                                options.UseInMemoryDatabase("TestDb"));
                        });
                    }
                }
                """);
            
            // 3. Database integration testing
            Console.WriteLine("\n3. Database Integration Testing:");
            Console.WriteLine("""
                Strategies for testing with databases:
                
                1. In-memory database (EF Core):
                   services.AddDbContext<AppDbContext>(options =>
                       options.UseInMemoryDatabase("TestDb"));
                   
                   Pros: Fast, isolated
                   Cons: Not exactly like real database, missing features
                   
                2. SQLite in-memory:
                   services.AddDbContext<AppDbContext>(options =>
                       options.UseSqlite("DataSource=:memory:"));
                   
                   Pros: More realistic SQL behavior
                   Cons: Slower than in-memory, still differences
                   
                3. Test containers (Docker):
                   // Using Testcontainers library
                   var container = new TestcontainersBuilder<PostgreSqlTestcontainer>()
                       .WithDatabase(new PostgreSqlTestcontainerConfiguration
                       {
                           Database = "testdb",
                           Username = "test",
                           Password = "test"
                       })
                       .Build();
                   
                   await container.StartAsync();
                   
                   services.AddDbContext<AppDbContext>(options =>
                       options.UseNpgsql(container.ConnectionString));
                   
                   Pros: Real database, accurate testing
                   Cons: Slow, requires Docker
                   
                4. Transaction rollback:
                   [Fact]
                   public async Task CreateUser_SavesToDatabase()
                   {
                       using var scope = _factory.Services.CreateScope();
                       var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
                       
                       // Start transaction
                       await context.Database.BeginTransactionAsync();
                       
                       try
                       {
                           // Act
                           context.Users.Add(new User { Name = "Test" });
                           await context.SaveChangesAsync();
                           
                           // Assert
                           var user = await context.Users.FirstAsync();
                           Assert.Equal("Test", user.Name);
                       }
                       finally
                       {
                           // Rollback - database unchanged for next test
                           await context.Database.RollbackTransactionAsync();
                       }
                   }
                """);
        }
        
        static void DemonstrateBestPractices()
        {
            Console.WriteLine("\n=== 7. Testing Best Practices ===\n");
            
            // 1. Test naming and structure
            Console.WriteLine("1. Test Naming and Structure:");
            Console.WriteLine("""
                Good test names:
                • MethodName_Scenario_ExpectedBehavior
                • Add_NegativeNumber_ThrowsException
                • ProcessOrder_ValidOrder_ReturnsOrderId
                • CalculateTax_IncomeBelowThreshold_ReturnsZero
                
                Arrange-Act-Assert pattern:
                
                [Fact]
                public void CalculateDiscount_QualifyingCustomer_AppliesDiscount()
                {
                    // Arrange
                    var customer = new Customer { IsPreferred = true };
                    var order = new Order { Total = 100.00m };
                    var calculator = new DiscountCalculator();
                    
                    // Act
                    decimal discount = calculator.CalculateDiscount(customer, order);
                    
                    // Assert
                    Assert.Equal(10.00m, discount);
                }
                
                One assertion per test (guideline, not rule):
                • Tests should verify one behavior
                • Multiple related assertions are OK
                • Avoid testing multiple unrelated things
                """);
            
            // 2. Test maintainability
            Console.WriteLine("\n2. Test Maintainability:");
            Console.WriteLine("""
                DRY (Don't Repeat Yourself) in tests:
                • Use factory methods for test data
                • Create test builders for complex objects
                • Extract common setup into helper methods
                • Use test data attributes ([InlineData], [MemberData])
                
                Example test builder:
                
                public class OrderBuilder
                {
                    private Order _order = new Order();
                    
                    public OrderBuilder WithCustomer(string name)
                    {
                        _order.Customer = new Customer { Name = name };
                        return this;
                    }
                    
                    public OrderBuilder WithItem(string sku, decimal price)
                    {
                        _order.Items.Add(new OrderItem { Sku = sku, Price = price });
                        return this;
                    }
                    
                    public Order Build() => _order;
                }
                
                Usage:
                var order = new OrderBuilder()
                    .WithCustomer("John")
                    .WithItem("SKU123", 25.00m)
                    .WithItem("SKU456", 35.00m)
                    .Build();
                """);
            
            // 3. Common pitfalls
            Console.WriteLine("\n3. Common Testing Pitfalls:");
            Console.WriteLine("""
                1. Testing implementation details:
                   // BAD: Tests internal state
                   Assert.Equal(3, calculator._internalCounter);
                   
                   // GOOD: Tests public behavior
                   Assert.Equal(8, calculator.Add(3, 5));
                   
                2. Fragile tests (break when implementation changes):
                   // BAD: Tests exact exception message
                   Assert.Equal("Specific error message", exception.Message);
                   
                   // GOOD: Tests exception type
                   Assert.IsType<InvalidOperationException>(exception);
                   
                3. Slow tests (external dependencies):
                   // BAD: Hits real API
                   var result = await _realApiClient.GetDataAsync();
                   
                   // GOOD: Uses mock
                   _mockApi.Setup(a => a.GetDataAsync())
                       .ReturnsAsync(testData);
                   
                4. Non-deterministic tests (randomness, dates):
                   // BAD: Uses current time
                   var now = DateTime.Now;
                   
                   // GOOD: Uses fixed time
                   var fixedTime = new DateTime(2023, 1, 1);
                   
                5. Over-mocking (tests become mock configuration):
                   // BAD: Too many mock setups
                   _mockA.Setup(...);
                   _mockB.Setup(...);
                   _mockC.Setup(...);
                   
                   // GOOD: Use real objects when possible
                   var realService = new SimpleService();
                """);
            
            // 4. Testing in CI/CD
            Console.WriteLine("\n4. Testing in CI/CD Pipeline:");
            Console.WriteLine("""
                Typical test pipeline:
                
                1. Unit tests (fast, run on every commit):
                   dotnet test --filter "Category=Unit"
                   
                2. Integration tests (slower, run on PR):
                   dotnet test --filter "Category=Integration"
                   
                3. Code coverage:
                   dotnet test --collect:"XPlat Code Coverage"
                   
                4. Test reporting:
                   • Generate TRX reports: dotnet test --logger trx
                   • Use coverlet for coverage: coverlet ./bin/Debug/net6.0/tests.dll
                   • Integrate with SonarQube, Azure DevOps, GitHub Actions
                   
                GitHub Actions example:
                
                name: Run Tests
                on: [push, pull_request]
                jobs:
                  test:
                    runs-on: ubuntu-latest
                    steps:
                    - uses: actions/checkout@v2
                    - name: Setup .NET
                      uses: actions/setup-dotnet@v1
                    - name: Restore dependencies
                      run: dotnet restore
                    - name: Build
                      run: dotnet build --no-restore
                    - name: Run unit tests
                      run: dotnet test --no-build --verbosity normal
                    - name: Run integration tests
                      run: dotnet test --filter "Category=Integration" --no-build
                """);
            
            // 5. Summary
            Console.WriteLine("\n=== Testing Philosophy ===");
            Console.WriteLine("""
                Good tests should be:
                • Fast: Run in milliseconds
                • Isolated: Don't depend on external systems
                • Repeatable: Same result every time
                • Self-verifying: Pass/fail without manual inspection
                • Timely: Written with production code
                
                Test categories:
                • Unit tests: Test individual components in isolation
                • Integration tests: Test interactions between components
                • System tests: Test complete system
                • Acceptance tests: Test from user perspective
                
                Testing mindset:
                • Tests are documentation
                • Tests are safety nets
                • Tests drive design
                • Write tests first when possible
                • Maintain tests like production code
                
                Remember:
                • "Tests are the immune system of your codebase"
                • "If it's not tested, it's broken"
                • "Test behavior, not implementation"
                • "Write tests that fail for the right reason"
                """);
        }
    }
    
    // Supporting classes for examples
    public class Customer
    {
        public string Name { get; set; }
        public string Email { get; set; }
        public int Age { get; set; }
        public bool IsPreferred { get; set; }
        public List<Order> Orders { get; set; } = new();
        public Address Address { get; set; }
    }
    
    public class Address
    {
        public string Street { get; set; }
        public string City { get; set; }
    }
    
    public class Order
    {
        public int Id { get; set; }
        public string OrderNumber { get; set; }
        public decimal Total { get; set; }
        public Customer Customer { get; set; }
        public List<OrderItem> Items { get; set; } = new();
    }
    
    public class OrderItem
    {
        public string Sku { get; set; }
        public decimal Price { get; set; }
    }
    
    // Interfaces for mocking examples
    public interface IEmailService
    {
        void SendEmail(string to, string subject, string body);
        Task SendEmailAsync(string to, string subject, string body);
        bool IsEnabled { get; set; }
    }
    
    public interface IUserRepository
    {
        Task<User> GetByIdAsync(int id);
        Task AddAsync(User user);
    }
    
    public interface IConfiguration
    {
        T GetValue<T>(string key);
    }
    
    public class User
    {
        public int Id { get; set; }
        public string Name { get; set; }
    }
    
    // Example service for testing
    public class DiscountCalculator
    {
        public decimal CalculateDiscount(Customer customer, Order order)
        {
            if (customer.IsPreferred)
            {
                return order.Total * 0.10m; // 10% discount
            }
            return 0;
        }
    }
    
    // TDD example: StringCalculator
    public class StringCalculator
    {
        public int Add(string numbers)
        {
            if (string.IsNullOrEmpty(numbers))
                return 0;
                
            var delimiters = new List<char> { ',', '\n' };
            
            // Check for custom delimiter
            if (numbers.StartsWith("//"))
            {
                var newLineIndex = numbers.IndexOf('\n');
                var customDelimiter = numbers[2];
                delimiters.Add(customDelimiter);
                numbers = numbers.Substring(newLineIndex + 1);
            }
            
            var numberStrings = numbers.Split(delimiters.ToArray());
            var sum = 0;
            var negatives = new List<int>();
            
            foreach (var numStr in numberStrings)
            {
                if (int.TryParse(numStr, out int num))
                {
                    if (num < 0)
                        negatives.Add(num);
                    else if (num <= 1000)
                        sum += num;
                }
            }
            
            if (negatives.Any())
                throw new ArgumentException($"Negatives not allowed: {string.Join(",", negatives)}");
                
            return sum;
        }
    }
}
