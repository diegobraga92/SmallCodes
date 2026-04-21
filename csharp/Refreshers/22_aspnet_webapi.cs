/*
    C# ASP.NET CORE WEB API
    File: 22_aspnet_webapi.cs
    
    Comprehensive guide to ASP.NET Core Web API development.
    Covers controllers, routing, model binding, validation, middleware,
    authentication, authorization, versioning, documentation, and best practices.
*/

using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;
using Microsoft.OpenApi.Models;
using Microsoft.AspNetCore.Diagnostics;
using System.Net;

namespace CSharpRefresher.AspNetWebApi
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# ASP.NET Core Web API ===\n");
            
            DemonstrateProjectStructure();
            DemonstrateControllersAndRouting();
            DemonstrateModelBindingValidation();
            DemonstrateMiddlewarePipeline();
            DemonstrateAuthenticationAuthorization();
            DemonstrateAdvancedFeatures();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateProjectStructure()
        {
            Console.WriteLine("=== 1. Project Structure ===\n");
            
            // 1. Program.cs - Application entry point
            Console.WriteLine("1. Program.cs (Entry Point):");
            Console.WriteLine("""
                Modern .NET 6+ template (minimal APIs):
                
                var builder = WebApplication.CreateBuilder(args);
                
                // Add services
                builder.Services.AddControllers();
                builder.Services.AddEndpointsApiExplorer();
                builder.Services.AddSwaggerGen();
                
                var app = builder.Build();
                
                // Configure pipeline
                if (app.Environment.IsDevelopment())
                {
                    app.UseSwagger();
                    app.UseSwaggerUI();
                }
                
                app.UseHttpsRedirection();
                app.UseAuthorization();
                app.MapControllers();
                
                app.Run();
                
                Traditional Startup.cs (pre-.NET 6):
                public class Startup
                {
                    public Startup(IConfiguration configuration)
                    {
                        Configuration = configuration;
                    }
                    
                    public IConfiguration Configuration { get; }
                    
                    public void ConfigureServices(IServiceCollection services)
                    {
                        // Dependency injection
                    }
                    
                    public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
                    {
                        // Middleware pipeline
                    }
                }
                """);
            
            // 2. appsettings.json configuration
            Console.WriteLine("\n2. Configuration (appsettings.json):");
            Console.WriteLine("""
                Example appsettings.json:
                {
                  "Logging": {
                    "LogLevel": {
                      "Default": "Information",
                      "Microsoft.AspNetCore": "Warning"
                    }
                  },
                  "AllowedHosts": "*",
                  "ConnectionStrings": {
                    "DefaultConnection": "Server=localhost;Database=MyDb;Trusted_Connection=True;"
                  },
                  "Jwt": {
                    "Key": "super-secret-key-at-least-32-chars",
                    "Issuer": "MyApi",
                    "Audience": "MyApiUsers",
                    "ExpireMinutes": 60
                  },
                  "Cors": {
                    "AllowedOrigins": ["http://localhost:3000", "https://myapp.com"]
                  }
                }
                
                Access configuration:
                var connectionString = Configuration.GetConnectionString("DefaultConnection");
                var jwtKey = Configuration["Jwt:Key"];
                
                Environment-specific configs:
                • appsettings.Development.json
                • appsettings.Production.json
                • appsettings.Staging.json
                """);
            
            // 3. Project file structure
            Console.WriteLine("\n3. Project File Structure:");
            Console.WriteLine("""
                Typical structure:
                • Controllers/         - API controllers
                • Models/             - Request/response DTOs
                • Services/           - Business logic
                • Data/               - Data access (DbContext, repositories)
                • Middleware/         - Custom middleware
                • Filters/            - Action filters
                • Validators/         - Fluent validation
                • Extensions/         - Extension methods
                • Properties/         - launchSettings.json
                
                Clean Architecture alternative:
                • Application/        - Use cases, interfaces
                • Domain/             - Business entities, rules
                • Infrastructure/     - Data access, external services
                • WebApi/             - Controllers, DTOs, middleware
                """);
            
            // 4. Launch settings
            Console.WriteLine("\n4. Launch Settings (launchSettings.json):");
            Console.WriteLine("""
                Example launchSettings.json:
                {
                  "profiles": {
                    "MyApi": {
                      "commandName": "Project",
                      "dotnetRunMessages": true,
                      "launchBrowser": true,
                      "launchUrl": "swagger",
                      "applicationUrl": "https://localhost:5001;http://localhost:5000",
                      "environmentVariables": {
                        "ASPNETCORE_ENVIRONMENT": "Development"
                      }
                    },
                    "IIS Express": {
                      "commandName": "IISExpress",
                      "launchBrowser": true,
                      "launchUrl": "swagger",
                      "environmentVariables": {
                        "ASPNETCORE_ENVIRONMENT": "Development"
                      }
                    }
                  }
                }
                
                Environment variables:
                • ASPNETCORE_ENVIRONMENT: Development, Staging, Production
                • ASPNETCORE_URLS: Override default URLs
                • DOTNET_ENVIRONMENT: Alternative to ASPNETCORE_ENVIRONMENT
                """);
        }
        
        static void DemonstrateControllersAndRouting()
        {
            Console.WriteLine("\n=== 2. Controllers and Routing ===\n");
            
            // 1. Basic controller
            Console.WriteLine("1. Basic API Controller:");
            
            [ApiController]
            [Route("api/[controller]")]
            public class UsersController : ControllerBase
            {
                private readonly IUserService _userService;
                private readonly ILogger<UsersController> _logger;
                
                public UsersController(IUserService userService, ILogger<UsersController> logger)
                {
                    _userService = userService;
                    _logger = logger;
                }
                
                // GET api/users
                [HttpGet]
                public async Task<ActionResult<IEnumerable<UserDto>>> GetUsers([FromQuery] UserQueryParameters queryParams)
                {
                    _logger.LogInformation("Getting all users");
                    var users = await _userService.GetUsersAsync(queryParams);
                    return Ok(users);
                }
                
                // GET api/users/{id}
                [HttpGet("{id:int}")]
                public async Task<ActionResult<UserDto>> GetUser(int id)
                {
                    var user = await _userService.GetUserByIdAsync(id);
                    if (user == null)
                    {
                        return NotFound($"User with ID {id} not found");
                    }
                    return Ok(user);
                }
                
                // POST api/users
                [HttpPost]
                public async Task<ActionResult<UserDto>> CreateUser([FromBody] CreateUserDto createDto)
                {
                    if (!ModelState.IsValid)
                    {
                        return BadRequest(ModelState);
                    }
                    
                    var createdUser = await _userService.CreateUserAsync(createDto);
                    return CreatedAtAction(nameof(GetUser), new { id = createdUser.Id }, createdUser);
                }
                
                // PUT api/users/{id}
                [HttpPut("{id:int}")]
                public async Task<ActionResult> UpdateUser(int id, [FromBody] UpdateUserDto updateDto)
                {
                    if (id != updateDto.Id)
                    {
                        return BadRequest("ID mismatch");
                    }
                    
                    await _userService.UpdateUserAsync(updateDto);
                    return NoContent();
                }
                
                // DELETE api/users/{id}
                [HttpDelete("{id:int}")]
                public async Task<ActionResult> DeleteUser(int id)
                {
                    await _userService.DeleteUserAsync(id);
                    return NoContent();
                }
                
                // PATCH api/users/{id}
                [HttpPatch("{id:int}")]
                public async Task<ActionResult> PartialUpdateUser(int id, [FromBody] JsonPatchDocument<UserDto> patchDoc)
                {
                    if (patchDoc == null)
                    {
                        return BadRequest();
                    }
                    
                    await _userService.PartialUpdateUserAsync(id, patchDoc);
                    return NoContent();
                }
            }
            
            Console.WriteLine("""
                Controller best practices:
                • Derive from ControllerBase (not Controller for APIs)
                • Use [ApiController] attribute
                • Use dependency injection in constructor
                • Return ActionResult<T> for type safety
                • Use appropriate HTTP status codes
                • Implement all CRUD operations consistently
                """);
            
            // 2. Routing
            Console.WriteLine("\n2. Routing Configuration:");
            Console.WriteLine("""
                Attribute routing examples:
                [Route("api/v{version:apiVersion}/[controller]")] // Versioned
                [Route("api/[controller]")]
                [Route("[controller]/[action]")] // MVC-style
                
                Route templates:
                • [HttpGet("{id:int}")] - Constraint
                • [HttpGet("{id:min(1)}")] - Minimum value
                • [HttpGet("{name:alpha}")] - Alphabetic only
                • [HttpGet("{id:guid}")] - GUID constraint
                • [HttpGet("{*path}")] - Catch-all
                
                Conventional routing:
                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapControllers();
                    
                    // Custom route
                    endpoints.MapControllerRoute(
                        name: "default",
                        pattern: "{controller=Home}/{action=Index}/{id?}");
                });
                """);
            
            // 3. Action results
            Console.WriteLine("\n3. Action Results:");
            Console.WriteLine("""
                Common return types:
                • Ok(object) - 200 OK with data
                • CreatedAtAction - 201 Created with location header
                • NoContent() - 204 No Content
                • BadRequest() - 400 Bad Request
                • Unauthorized() - 401 Unauthorized
                • Forbid() - 403 Forbidden
                • NotFound() - 404 Not Found
                • Conflict() - 409 Conflict
                • StatusCode(int) - Custom status code
                
                ActionResult<T> benefits:
                • Type-safe return values
                • Can return T or ActionResult
                • Swagger documentation improvements
                • Compile-time checking
                """);
            
            // 4. Minimal APIs (.NET 6+)
            Console.WriteLine("\n4. Minimal APIs (.NET 6+):");
            Console.WriteLine("""
                Example minimal API:
                
                var builder = WebApplication.CreateBuilder(args);
                var app = builder.Build();
                
                app.MapGet("/api/users", async (IUserService service) =>
                    await service.GetUsersAsync());
                
                app.MapGet("/api/users/{id}", async (int id, IUserService service) =>
                {
                    var user = await service.GetUserByIdAsync(id);
                    return user != null ? Results.Ok(user) : Results.NotFound();
                });
                
                app.MapPost("/api/users", async (CreateUserDto dto, IUserService service) =>
                {
                    var user = await service.CreateUserAsync(dto);
                    return Results.Created($"/api/users/{user.Id}", user);
                });
                
                app.MapPut("/api/users/{id}", async (int id, UpdateUserDto dto, IUserService service) =>
                {
                    await service.UpdateUserAsync(dto);
                    return Results.NoContent();
                });
                
                app.MapDelete("/api/users/{id}", async (int id, IUserService service) =>
                {
                    await service.DeleteUserAsync(id);
                    return Results.NoContent();
                });
                
                Benefits:
                • Less boilerplate
                • Improved performance
                • Simpler for small APIs
                
                Limitations:
                • Less structure for complex APIs
                • Harder to organize large codebases
                • Fewer built-in features
                """);
        }
        
        static void DemonstrateModelBindingValidation()
        {
            Console.WriteLine("\n=== 3. Model Binding and Validation ===\n");
            
            // 1. DTO classes
            Console.WriteLine("1. DTO (Data Transfer Object) Classes:");
            
            public class CreateUserDto
            {
                [Required]
                [StringLength(100, MinimumLength = 3)]
                public string Username { get; set; }
                
                [Required]
                [EmailAddress]
                public string Email { get; set; }
                
                [Required]
                [DataType(DataType.Password)]
                [StringLength(100, MinimumLength = 8)]
                [RegularExpression(@"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", 
                    ErrorMessage = "Password must contain uppercase, lowercase, and number")]
                public string Password { get; set; }
                
                [Compare("Password", ErrorMessage = "Passwords do not match")]
                public string ConfirmPassword { get; set; }
                
                [Range(18, 120, ErrorMessage = "Age must be between 18 and 120")]
                public int? Age { get; set; }
                
                [Url]
                public string Website { get; set; }
                
                [Phone]
                public string PhoneNumber { get; set; }
                
                public DateTime? BirthDate { get; set; }
                
                [CreditCard]
                public string CreditCardNumber { get; set; }
            }
            
            public class UserDto
            {
                public int Id { get; set; }
                public string Username { get; set; }
                public string Email { get; set; }
                public DateTime CreatedAt { get; set; }
                public bool IsActive { get; set; }
            }
            
            public class UserQueryParameters
            {
                [FromQuery]
                public string Search { get; set; }
                
                [FromQuery]
                public int Page { get; set; } = 1;
                
                [FromQuery]
                [Range(1, 100)]
                public int PageSize { get; set; } = 20;
                
                [FromQuery]
                public string SortBy { get; set; } = "Id";
                
                [FromQuery]
                public bool SortDesc { get; set; } = false;
                
                [FromQuery]
                public bool? IsActive { get; set; }
            }
            
            Console.WriteLine("""
                Data annotations for validation:
                • [Required] - Field is required
                • [StringLength] - Length constraints
                • [EmailAddress] - Email format validation
                • [Phone] - Phone number validation
                • [Url] - URL format validation
                • [Range] - Numeric range validation
                • [RegularExpression] - Custom regex validation
                • [Compare] - Compare two properties
                • [CreditCard] - Credit card number validation
                • [DataType] - Data type hint
                """);
            
            // 2. Model binding sources
            Console.WriteLine("\n2. Model Binding Sources:");
            Console.WriteLine("""
                Binding source attributes:
                • [FromBody] - Request body (JSON/XML)
                • [FromQuery] - Query string parameters
                • [FromRoute] - Route parameters
                • [FromForm] - Form data (multipart/form-data)
                • [FromHeader] - HTTP headers
                • [FromServices] - Dependency injection
                
                Example:
                public IActionResult Get(
                    [FromQuery] string search,
                    [FromRoute] int id,
                    [FromHeader(Name = "X-API-Key")] string apiKey,
                    [FromBody] UpdateModel model,
                    [FromServices] ILogger logger)
                {
                    // ...
                }
                
                Automatic model binding:
                • Complex types from body by default
                • Simple types from query by default
                • Can be configured globally
                """);
            
            // 3. Fluent validation
            Console.WriteLine("\n3. Fluent Validation:");
            Console.WriteLine("""
                Install FluentValidation.AspNetCore
                
                Validator class:
                public class CreateUserDtoValidator : AbstractValidator<CreateUserDto>
                {
                    public CreateUserDtoValidator()
                    {
                        RuleFor(x => x.Username)
                            .NotEmpty().WithMessage("Username is required")
                            .Length(3, 100).WithMessage("Username must be 3-100 characters")
                            .Matches("^[a-zA-Z0-9_]+$").WithMessage("Username can only contain letters, numbers, and underscores");
                            
                        RuleFor(x => x.Email)
                            .NotEmpty().WithMessage("Email is required")
                            .EmailAddress().WithMessage("Invalid email address");
                            
                        RuleFor(x => x.Password)
                            .NotEmpty().WithMessage("Password is required")
                            .MinimumLength(8).WithMessage("Password must be at least 8 characters")
                            .Matches("[A-Z]").WithMessage("Password must contain at least one uppercase letter")
                            .Matches("[a-z]").WithMessage("Password must contain at least one lowercase letter")
                            .Matches("[0-9]").WithMessage("Password must contain at least one number");
                            
                        RuleFor(x => x.Age)
                            .InclusiveBetween(18, 120).When(x => x.Age.HasValue)
                            .WithMessage("Age must be between 18 and 120");
                            
                        RuleFor(x => x.ConfirmPassword)
                            .Equal(x => x.Password).WithMessage("Passwords must match");
                    }
                }
                
                Register in Startup:
                services.AddControllers()
                    .AddFluentValidation(fv => 
                    {
                        fv.RegisterValidatorsFromAssemblyContaining<Startup>();
                        fv.RunDefaultMvcValidationAfterFluentValidationExecutes = false;
                    });
                
                Benefits over data annotations:
                • Separation of concerns
                • More complex validation rules
                • Better testability
                • Reusable validation logic
                """);
            
            // 4. Custom validation
            Console.WriteLine("\n4. Custom Validation Attributes:");
            
            public class MinimumAgeAttribute : ValidationAttribute
            {
                private readonly int _minimumAge;
                
                public MinimumAgeAttribute(int minimumAge)
                {
                    _minimumAge = minimumAge;
                    ErrorMessage = $"Must be at least {minimumAge} years old";
                }
                
                protected override ValidationResult IsValid(object value, ValidationContext validationContext)
                {
                    if (value is DateTime birthDate)
                    {
                        var age = DateTime.Today.Year - birthDate.Year;
                        if (birthDate.Date > DateTime.Today.AddYears(-age)) age--;
                        
                        if (age >= _minimumAge)
                        {
                            return ValidationResult.Success;
                        }
                    }
                    
                    return new ValidationResult(ErrorMessage);
                }
            }
            
            public class UniqueUsernameAttribute : ValidationAttribute
            {
                protected override ValidationResult IsValid(object value, ValidationContext validationContext)
                {
                    var username = value as string;
                    if (string.IsNullOrEmpty(username))
                    {
                        return ValidationResult.Success; // Let Required handle this
                    }
                    
                    var userService = (IUserService)validationContext.GetService(typeof(IUserService));
                    if (userService == null)
                    {
                        return ValidationResult.Success; // Can't validate without service
                    }
                    
                    var isUnique = userService.IsUsernameUniqueAsync(username).GetAwaiter().GetResult();
                    return isUnique 
                        ? ValidationResult.Success 
                        : new ValidationResult("Username is already taken");
                }
            }
            
            // 5. ModelState and validation responses
            Console.WriteLine("\n5. ModelState and Validation Responses:");
            Console.WriteLine("""
                Automatic validation with [ApiController]:
                • Returns 400 BadRequest automatically
                • ModelState.IsValid is checked automatically
                • Error responses are standardized
                
                Custom validation response:
                if (!ModelState.IsValid)
                {
                    return BadRequest(new ValidationProblemDetails(ModelState)
                    {
                        Title = "Validation failed",
                        Status = StatusCodes.Status400BadRequest,
                        Type = "https://tools.ietf.org/html/rfc7231#section-6.5.1"
                    });
                }
                
                Disable automatic validation:
                [ApiController]
                [Route("api/[controller]")]
                public class MyController : ControllerBase
                {
                    [ApiController]
                    [Route("api/[controller]")]
                    [ApiController]
                    public class MyController : ControllerBase
                    {
                        // Disable for specific action
                        [SkipAutoValidation]
                        public IActionResult MyAction([FromBody] MyModel model)
                        {
                            // Manual validation
                            if (!TryValidateModel(model))
                            {
                                return BadRequest(ModelState);
                            }
                            // ...
                        }
                    }
                }
                
                SuppressModelStateInvalidFilter globally:
                services.Configure<ApiBehaviorOptions>(options =>
                {
                    options.SuppressModelStateInvalidFilter = true;
                });
                """);
        }
        
        static void DemonstrateMiddlewarePipeline()
        {
            Console.WriteLine("\n=== 4. Middleware Pipeline ===\n");
            
            // 1. Built-in middleware
            Console.WriteLine("1. Built-in Middleware:");
            Console.WriteLine("""
                Typical middleware order:
                1. Exception/error handling
                2. HTTPS redirection
                3. Static files
                4. Routing
                5. Authentication
                6. Authorization
                7. Endpoints
                
                Example pipeline configuration:
                app.UseExceptionHandler("/error");
                app.UseHttpsRedirection();
                app.UseStaticFiles();
                app.UseRouting();
                app.UseCors("MyCorsPolicy");
                app.UseAuthentication();
                app.UseAuthorization();
                app.UseResponseCompression();
                app.UseResponseCaching();
                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapControllers();
                });
                """);
            
            // 2. Custom middleware
            Console.WriteLine("\n2. Custom Middleware:");
            
            // Request logging middleware
            public class RequestLoggingMiddleware
            {
                private readonly RequestDelegate _next;
                private readonly ILogger<RequestLoggingMiddleware> _logger;
                
                public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
                {
                    _next = next;
                    _logger = logger;
                }
                
                public async Task InvokeAsync(HttpContext context)
                {
                    var startTime = DateTime.UtcNow;
                    
                    // Log request
                    _logger.LogInformation($"Request: {context.Request.Method} {context.Request.Path}");
                    
                    // Call next middleware
                    await _next(context);
                    
                    // Log response
                    var duration = DateTime.UtcNow - startTime;
                    _logger.LogInformation(
                        $"Response: {context.Response.StatusCode} - {duration.TotalMilliseconds}ms");
                }
            }
            
            // Extension method for easy registration
            public static class RequestLoggingMiddlewareExtensions
            {
                public static IApplicationBuilder UseRequestLogging(this IApplicationBuilder builder)
                {
                    return builder.UseMiddleware<RequestLoggingMiddleware>();
                }
            }
            
            // Usage: app.UseRequestLogging();
            
            // 3. Exception handling middleware
            Console.WriteLine("\n3. Exception Handling Middleware:");
            
            public class GlobalExceptionHandlerMiddleware
            {
                private readonly RequestDelegate _next;
                private readonly ILogger<GlobalExceptionHandlerMiddleware> _logger;
                private readonly IWebHostEnvironment _env;
                
                public GlobalExceptionHandlerMiddleware(
                    RequestDelegate next, 
                    ILogger<GlobalExceptionHandlerMiddleware> logger,
                    IWebHostEnvironment env)
                {
                    _next = next;
                    _logger = logger;
                    _env = env;
                }
                
                public async Task InvokeAsync(HttpContext context)
                {
                    try
                    {
                        await _next(context);
                    }
                    catch (Exception ex)
                    {
                        _logger.LogError(ex, "An unhandled exception occurred");
                        await HandleExceptionAsync(context, ex);
                    }
                }
                
                private async Task HandleExceptionAsync(HttpContext context, Exception exception)
                {
                    context.Response.ContentType = "application/json";
                    
                    var problemDetails = new ProblemDetails
                    {
                        Title = "An error occurred",
                        Status = (int)HttpStatusCode.InternalServerError,
                        Instance = context.Request.Path
                    };
                    
                    if (_env.IsDevelopment())
                    {
                        problemDetails.Detail = exception.ToString();
                        problemDetails.Extensions["stackTrace"] = exception.StackTrace;
                        problemDetails.Extensions["innerException"] = exception.InnerException?.Message;
                    }
                    else
                    {
                        problemDetails.Detail = "An internal server error occurred. Please try again later.";
                    }
                    
                    // Handle specific exceptions
                    switch (exception)
                    {
                        case ValidationException validationEx:
                            context.Response.StatusCode = (int)HttpStatusCode.BadRequest;
                            problemDetails.Status = (int)HttpStatusCode.BadRequest;
                            problemDetails.Title = "Validation failed";
                            problemDetails.Detail = "One or more validation errors occurred.";
                            problemDetails.Extensions["errors"] = validationEx.Errors;
                            break;
                            
                        case NotFoundException notFoundEx:
                            context.Response.StatusCode = (int)HttpStatusCode.NotFound;
                            problemDetails.Status = (int)HttpStatusCode.NotFound;
                            problemDetails.Title = "Resource not found";
                            problemDetails.Detail = notFoundEx.Message;
                            break;
                            
                        case UnauthorizedAccessException:
                            context.Response.StatusCode = (int)HttpStatusCode.Unauthorized;
                            problemDetails.Status = (int)HttpStatusCode.Unauthorized;
                            problemDetails.Title = "Unauthorized";
                            problemDetails.Detail = "You are not authorized to perform this action.";
                            break;
                    }
                    
                    var json = System.Text.Json.JsonSerializer.Serialize(problemDetails);
                    await context.Response.WriteAsync(json);
                }
            }
            
            // 4. Built-in exception handling
            Console.WriteLine("\n4. Built-in Exception Handling:");
            Console.WriteLine("""
                Developer Exception Page (development only):
                app.UseDeveloperExceptionPage();
                
                Custom exception handler:
                app.UseExceptionHandler(appBuilder =>
                {
                    appBuilder.Run(async context =>
                    {
                        var exceptionHandler = context.Features.Get<IExceptionHandlerPathFeature>();
                        var exception = exceptionHandler?.Error;
                        
                        context.Response.StatusCode = 500;
                        context.Response.ContentType = "application/json";
                        
                        var response = new
                        {
                            error = "An unexpected error occurred",
                            message = exception?.Message,
                            stackTrace = app.Environment.IsDevelopment() ? exception?.StackTrace : null
                        };
                        
                        await context.Response.WriteAsJsonAsync(response);
                    });
                });
                
                Status code pages:
                app.UseStatusCodePages(async context =>
                {
                    context.HttpContext.Response.ContentType = "application/json";
                    var response = new
                    {
                        statusCode = context.HttpContext.Response.StatusCode,
                        message = GetStatusCodeMessage(context.HttpContext.Response.StatusCode)
                    };
                    await context.HttpContext.Response.WriteAsJsonAsync(response);
                });
                """);
        }
        
        static void DemonstrateAuthenticationAuthorization()
        {
            Console.WriteLine("\n=== 5. Authentication and Authorization ===\n");
            
            // 1. JWT authentication
            Console.WriteLine("1. JWT Authentication:");
            Console.WriteLine("""
                Configuration in Startup:
                
                services.AddAuthentication(options =>
                {
                    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
                    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
                })
                .AddJwtBearer(options =>
                {
                    options.TokenValidationParameters = new TokenValidationParameters
                    {
                        ValidateIssuer = true,
                        ValidateAudience = true,
                        ValidateLifetime = true,
                        ValidateIssuerSigningKey = true,
                        
                        ValidIssuer = Configuration["Jwt:Issuer"],
                        ValidAudience = Configuration["Jwt:Audience"],
                        IssuerSigningKey = new SymmetricSecurityKey(
                            Encoding.UTF8.GetBytes(Configuration["Jwt:Key"]))
                    };
                    
                    // For SignalR/WebSockets
                    options.Events = new JwtBearerEvents
                    {
                        OnMessageReceived = context =>
                        {
                            var accessToken = context.Request.Query["access_token"];
                            var path = context.HttpContext.Request.Path;
                            if (!string.IsNullOrEmpty(accessToken) && 
                                path.StartsWithSegments("/chat"))
                            {
                                context.Token = accessToken;
                            }
                            return Task.CompletedTask;
                        }
                    };
                });
                
                Generate JWT token:
                public string GenerateJwtToken(User user)
                {
                    var claims = new[]
                    {
                        new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
                        new Claim(JwtRegisteredClaimNames.UniqueName, user.Username),
                        new Claim(JwtRegisteredClaimNames.Email, user.Email),
                        new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
                        new Claim(ClaimTypes.Role, user.Role)
                    };
                    
                    var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_jwtSettings.Key));
                    var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
                    
                    var token = new JwtSecurityToken(
                        issuer: _jwtSettings.Issuer,
                        audience: _jwtSettings.Audience,
                        claims: claims,
                        expires: DateTime.UtcNow.AddMinutes(_jwtSettings.ExpireMinutes),
                        signingCredentials: creds);
                        
                    return new JwtSecurityTokenHandler().WriteToken(token);
                }
                """);
            
            // 2. Authorization
            Console.WriteLine("\n2. Authorization:");
            Console.WriteLine("""
                Policy-based authorization:
                
                services.AddAuthorization(options =>
                {
                    options.AddPolicy("AdminOnly", policy =>
                        policy.RequireRole("Admin"));
                        
                    options.AddPolicy("Over18", policy =>
                        policy.RequireAssertion(context =>
                            context.User.HasClaim(c => 
                                c.Type == "Age" && int.Parse(c.Value) >= 18)));
                            
                    options.AddPolicy("CanEditUser", policy =>
                        policy.RequireAssertion(context =>
                        {
                            var userId = context.User.FindFirstValue(ClaimTypes.NameIdentifier);
                            var routeUserId = context.Resource as string; // From route
                            return userId == routeUserId || context.User.IsInRole("Admin");
                        }));
                });
                
                Usage in controllers:
                [Authorize]
                public class UsersController : ControllerBase
                {
                    [Authorize(Roles = "Admin")]
                    public IActionResult GetAll() { ... }
                    
                    [Authorize(Policy = "Over18")]
                    public IActionResult GetAdultContent() { ... }
                    
                    [Authorize(Policy = "CanEditUser")]
                    public IActionResult EditUser(int id) { ... }
                }
                
                Resource-based authorization:
                public class UserAuthorizationHandler : 
                    AuthorizationHandler<SameUserRequirement, User>
                {
                    protected override Task HandleRequirementAsync(
                        AuthorizationHandlerContext context,
                        SameUserRequirement requirement,
                        User resource)
                    {
                        var userId = context.User.FindFirstValue(ClaimTypes.NameIdentifier);
                        if (userId == resource.Id.ToString())
                        {
                            context.Succeed(requirement);
                        }
                        return Task.CompletedTask;
                    }
                }
                """);
            
            // 3. Identity integration
            Console.WriteLine("\n3. ASP.NET Core Identity:");
            Console.WriteLine("""
                Setup with Entity Framework:
                
                services.AddDbContext<ApplicationDbContext>(options =>
                    options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection")));
                    
                services.AddIdentity<ApplicationUser, IdentityRole>(options =>
                {
                    options.Password.RequireDigit = true;
                    options.Password.RequiredLength = 8;
                    options.Password.RequireNonAlphanumeric = false;
                    options.Password.RequireUppercase = true;
                    options.Password.RequireLowercase = true;
                    
                    options.User.RequireUniqueEmail = true;
                    options.SignIn.RequireConfirmedEmail = true;
                })
                .AddEntityFrameworkStores<ApplicationDbContext>()
                .AddDefaultTokenProviders();
                
                User registration:
                public async Task<IActionResult> Register(RegisterDto model)
                {
                    var user = new ApplicationUser
                    {
                        UserName = model.Username,
                        Email = model.Email
                    };
                    
                    var result = await _userManager.CreateAsync(user, model.Password);
                    if (result.Succeeded)
                    {
                        await _userManager.AddToRoleAsync(user, "User");
                        
                        // Generate email confirmation token
                        var token = await _userManager.GenerateEmailConfirmationTokenAsync(user);
                        var callbackUrl = Url.Action("ConfirmEmail", "Account", 
                            new { userId = user.Id, token }, protocol: HttpContext.Request.Scheme);
                            
                        // Send email
                        await _emailService.SendConfirmationEmailAsync(user.Email, callbackUrl);
                        
                        return Ok(new { message = "Registration successful" });
                    }
                    
                    return BadRequest(result.Errors);
                }
                """);
        }
        
        static void DemonstrateAdvancedFeatures()
        {
            Console.WriteLine("\n=== 6. Advanced Features ===\n");
            
            // 1. API versioning
            Console.WriteLine("1. API Versioning:");
            Console.WriteLine("""
                Install Microsoft.AspNetCore.Mvc.Versioning
                
                Configuration:
                services.AddApiVersioning(options =>
                {
                    options.DefaultApiVersion = new ApiVersion(1, 0);
                    options.AssumeDefaultVersionWhenUnspecified = true;
                    options.ReportApiVersions = true;
                    options.ApiVersionReader = ApiVersionReader.Combine(
                        new QueryStringApiVersionReader("api-version"),
                        new HeaderApiVersionReader("X-API-Version"),
                        new UrlSegmentApiVersionReader());
                });
                
                Usage:
                [ApiVersion("1.0")]
                [ApiVersion("2.0")]
                [Route("api/v{version:apiVersion}/[controller]")]
                public class UsersController : ControllerBase
                {
                    [HttpGet]
                    [MapToApiVersion("1.0")]
                    public IActionResult GetV1() { ... }
                    
                    [HttpGet]
                    [MapToApiVersion("2.0")]
                    public IActionResult GetV2() { ... }
                }
                
                Versioning strategies:
                • URL segment: /api/v1/users
                • Query string: /api/users?api-version=1.0
                • Header: X-API-Version: 1.0
                • Media type: Accept: application/json;version=1.0
                """);
            
            // 2. Swagger/OpenAPI documentation
            Console.WriteLine("\n2. Swagger/OpenAPI Documentation:");
            Console.WriteLine("""
                Install Swashbuckle.AspNetCore
                
                Configuration:
                services.AddSwaggerGen(options =>
                {
                    options.SwaggerDoc("v1", new OpenApiInfo
                    {
                        Title = "My API",
                        Version = "v1",
                        Description = "My API Description",
                        Contact = new OpenApiContact
                        {
                            Name = "Support",
                            Email = "support@example.com"
                        }
                    });
                    
                    // Add JWT authentication to Swagger
                    options.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
                    {
                        Description = "JWT Authorization header using the Bearer scheme",
                        Name = "Authorization",
                        In = ParameterLocation.Header,
                        Type = SecuritySchemeType.Http,
                        Scheme = "bearer"
                    });
                    
                    options.AddSecurityRequirement(new OpenApiSecurityRequirement
                    {
                        {
                            new OpenApiSecurityScheme
                            {
                                Reference = new OpenApiReference
                                {
                                    Type = ReferenceType.SecurityScheme,
                                    Id = "Bearer"
                                }
                            },
                            new string[] {}
                        }
                    });
                    
                    // Include XML comments
                    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
                    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
                    options.IncludeXmlComments(xmlPath);
                    
                    // Support API versioning
                    options.DocInclusionPredicate((version, desc) =>
                    {
                        if (!desc.TryGetMethodInfo(out MethodInfo methodInfo)) return false;
                        var versions = methodInfo.DeclaringType
                            .GetCustomAttributes(true)
                            .OfType<ApiVersionAttribute>()
                            .SelectMany(attr => attr.Versions);
                        return versions.Any(v => $"v{v}" == version);
                    });
                });
                
                Enable in pipeline:
                app.UseSwagger();
                app.UseSwaggerUI(options =>
                {
                    options.SwaggerEndpoint("/swagger/v1/swagger.json", "My API v1");
                    options.RoutePrefix = "swagger";
                });
                """);
            
            // 3. CORS
            Console.WriteLine("\n3. CORS (Cross-Origin Resource Sharing):");
            Console.WriteLine("""
                Configuration:
                services.AddCors(options =>
                {
                    options.AddPolicy("MyCorsPolicy", builder =>
                    {
                        builder.WithOrigins("http://localhost:3000", "https://myapp.com")
                               .AllowAnyHeader()
                               .AllowAnyMethod()
                               .AllowCredentials()
                               .WithExposedHeaders("X-Pagination")
                               .SetPreflightMaxAge(TimeSpan.FromHours(1));
                    });
                    
                    options.AddPolicy("AllowAll", builder =>
                    {
                        builder.AllowAnyOrigin()
                               .AllowAnyHeader()
                               .AllowAnyMethod();
                    });
                });
                
                Usage:
                // Global policy
                app.UseCors("MyCorsPolicy");
                
                // Per controller/action
                [EnableCors("MyCorsPolicy")]
                public class MyController : ControllerBase { ... }
                
                [EnableCors("AllowAll")]
                [HttpGet]
                public IActionResult Get() { ... }
                
                [DisableCors]
                [HttpGet]
                public IActionResult GetNoCors() { ... }
                """);
            
            // 4. Response compression and caching
            Console.WriteLine("\n4. Response Compression and Caching:");
            Console.WriteLine("""
                Response compression:
                services.AddResponseCompression(options =>
                {
                    options.EnableForHttps = true;
                    options.Providers.Add<BrotliCompressionProvider>();
                    options.Providers.Add<GzipCompressionProvider>();
                });
                
                Response caching:
                services.AddResponseCaching(options =>
                {
                    options.MaximumBodySize = 1024 * 1024; // 1MB
                    options.UseCaseSensitivePaths = true;
                });
                
                Usage:
                [HttpGet]
                [ResponseCache(Duration = 60, Location = ResponseCacheLocation.Client)]
                public IActionResult GetCachedData() { ... }
                
                [HttpGet]
                [ResponseCache(VaryByQueryKeys = new[] { "search", "page" }, Duration = 30)]
                public IActionResult GetSearchResults(string search, int page) { ... }
                
                Manual caching in controller:
                [HttpGet("{id}")]
                public async Task<IActionResult> GetUser(int id)
                {
                    var cacheKey = $"user_{id}";
                    if (!_cache.TryGetValue(cacheKey, out UserDto user))
                    {
                        user = await _userService.GetUserAsync(id);
                        var cacheEntryOptions = new MemoryCacheEntryOptions()
                            .SetSlidingExpiration(TimeSpan.FromMinutes(5))
                            .SetAbsoluteExpiration(TimeSpan.FromHours(1));
                        _cache.Set(cacheKey, user, cacheEntryOptions);
                    }
                    return Ok(user);
                }
                """);
            
            // 5. Health checks
            Console.WriteLine("\n5. Health Checks:");
            Console.WriteLine("""
                Configuration:
                services.AddHealthChecks()
                    .AddCheck<DatabaseHealthCheck>("database")
                    .AddCheck<ExternalApiHealthCheck>("external-api")
                    .AddDbContextCheck<ApplicationDbContext>()
                    .AddRedis("localhost:6379")
                    .AddElasticsearch("http://localhost:9200");
                
                Custom health check:
                public class DatabaseHealthCheck : IHealthCheck
                {
                    private readonly ApplicationDbContext _dbContext;
                    
                    public DatabaseHealthCheck(ApplicationDbContext dbContext)
                    {
                        _dbContext = dbContext;
                    }
                    
                    public async Task<HealthCheckResult> CheckHealthAsync(
                        HealthCheckContext context, 
                        CancellationToken cancellationToken = default)
                    {
                        try
                        {
                            await _dbContext.Database.CanConnectAsync(cancellationToken);
                            return HealthCheckResult.Healthy("Database is available");
                        }
                        catch (Exception ex)
                        {
                            return HealthCheckResult.Unhealthy("Database is unavailable", ex);
                        }
                    }
                }
                
                Map health endpoints:
                app.MapHealthChecks("/health", new HealthCheckOptions
                {
                    ResponseWriter = async (context, report) =>
                    {
                        context.Response.ContentType = "application/json";
                        var response = new
                        {
                            status = report.Status.ToString(),
                            checks = report.Entries.Select(e => new
                            {
                                name = e.Key,
                                status = e.Value.Status.ToString(),
                                description = e.Value.Description,
                                duration = e.Value.Duration.TotalMilliseconds
                            })
                        };
                        await context.Response.WriteAsJsonAsync(response);
                    }
                });
                
                app.MapHealthChecks("/health/ready", new HealthCheckOptions
                {
                    Predicate = check => check.Tags.Contains("ready")
                });
                
                app.MapHealthChecks("/health/live", new HealthCheckOptions
                {
                    Predicate = _ => false // No checks for liveness
                });
                """);
            
            // 6. Best practices summary
            Console.WriteLine("\n=== ASP.NET Core Web API Best Practices ===");
            Console.WriteLine("""
                1. Use async/await for all I/O operations
                2. Implement proper error handling and logging
                3. Use DTOs instead of exposing entities directly
                4. Implement validation (FluentValidation recommended)
                5. Use dependency injection properly
                6. Implement proper authentication/authorization
                7. Add API versioning from the start
                8. Document APIs with Swagger/OpenAPI
                9. Implement rate limiting
                10. Use HTTPS in production
                11. Implement CORS properly
                12. Add health checks
                13. Use response compression and caching
                14. Implement proper logging (structured logging)
                15. Use configuration properly (environment variables for secrets)
                16. Implement unit and integration tests
                17. Use middleware for cross-cutting concerns
                18. Follow RESTful conventions
                19. Implement pagination for list endpoints
                20. Use proper HTTP status codes
                
                Performance tips:
                • Use response caching where appropriate
                • Implement database query optimization
                • Use async database operations
                • Minimize payload sizes
                • Use compression
                • Implement CDN for static files
                • Use connection pooling
                
                Security tips:
                • Validate all inputs
                • Use parameterized queries (prevent SQL injection)
                • Implement proper authentication
                • Use HTTPS everywhere
                • Sanitize output
                • Implement rate limiting
                • Keep dependencies updated
                • Use security headers
                """);
        }
    }
    
    // Supporting classes for examples
    public interface IUserService
    {
        Task<IEnumerable<UserDto>> GetUsersAsync(UserQueryParameters queryParams);
        Task<UserDto> GetUserByIdAsync(int id);
        Task<UserDto> CreateUserAsync(CreateUserDto createDto);
        Task UpdateUserAsync(UpdateUserDto updateDto);
        Task DeleteUserAsync(int id);
        Task<bool> IsUsernameUniqueAsync(string username);
    }
    
    public class UpdateUserDto
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string Email { get; set; }
    }
    
    // Exception classes
    public class ValidationException : Exception
    {
        public Dictionary<string, string[]> Errors { get; }
        
        public ValidationException(Dictionary<string, string[]> errors)
            : base("Validation failed")
        {
            Errors = errors;
        }
    }
    
    public class NotFoundException : Exception
    {
        public NotFoundException(string message) : base(message) { }
    }
    
    // Authorization requirement
    public class SameUserRequirement : IAuthorizationRequirement { }
}