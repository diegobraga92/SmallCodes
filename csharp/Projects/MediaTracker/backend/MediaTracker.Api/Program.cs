using System.Text;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using MediaTracker.Api.Data;
using MediaTracker.Api.Services;

/*
 * Program.cs is the entry point of the application. It uses the "top-level statements"
 * feature (C# 9+) which eliminates the explicit class and Main method boilerplate.
 * The code here is implicitly inside a Main method.
 *
 * The pattern follows the "builder pattern" — WebApplication.CreateBuilder sets up
 * the application, we configure services, then we build and run it.
 */
var builder = WebApplication.CreateBuilder(args);

// ===== SERVICE REGISTRATION =====
// Services registered here are added to the Dependency Injection (DI) container.
// When a controller or service constructor requests a dependency (e.g., IMediaService),
// the DI container provides the registered implementation.

/*
 * AddDbContext registers EF Core's DbContext with scoped lifetime.
 * "Scoped" means one instance per HTTP request — this is the "unit of work" pattern.
 * Each request gets a fresh DbContext, so concurrent requests don't interfere with
 * each other's tracked entities.
 *
 * UseNpgsql configures PostgreSQL as the database provider. The connection string
 * comes from appsettings.json or environment variables (in Docker).
 */
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));

/*
 * ASP.NET Core Identity provides user management: registration, login, password hashing,
 * role management, etc. AddIdentity registers the necessary services.
 *
 * AddEntityFrameworkStores tells Identity to use our AppDbContext for storing user data.
 * This creates the AspNetUsers, AspNetRoles, AspNetUserRoles, etc. tables.
 */
builder.Services.AddIdentity<IdentityUser, IdentityRole>()
    .AddEntityFrameworkStores<AppDbContext>()
    .AddDefaultTokenProviders();

/*
 * JWT Authentication configuration.
 *
 * Authentication = "who are you?" (verifying identity)
 * Authorization = "what can you do?" (checking permissions)
 *
 * We configure the JWT bearer handler to validate tokens on every request.
 * The validation parameters ensure the token:
 * - Was issued by our server (ValidateIssuer)
 * - Is intended for our frontend (ValidateAudience)
 * - Hasn't expired (ValidateLifetime)
 * - Hasn't been tampered with (ValidateIssuerSigningKey)
 */
var jwtSettings = builder.Configuration.GetSection("Jwt");
var jwtKey = Encoding.UTF8.GetBytes(jwtSettings["Key"] ?? throw new InvalidOperationException("JWT Key not configured"));

builder.Services.AddAuthentication(options =>
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
        ValidIssuer = jwtSettings["Issuer"],
        ValidAudience = jwtSettings["Audience"],
        IssuerSigningKey = new SymmetricSecurityKey(jwtKey)
    };
});

builder.Services.AddAuthorization();

/*
 * Register our application services with scoped lifetime.
 * Each service has an interface (contract) and an implementation.
 * The DI container will create an AuthService when IAuthService is requested.
 */
builder.Services.AddScoped<IAuthService, AuthService>();
builder.Services.AddScoped<IMediaService, MediaService>();
builder.Services.AddScoped<IStatsService, StatsService>();

/*
 * AddControllers registers all controllers in the assembly.
 * AddJsonOptions configures JSON serialization — JsonStringEnumConverter makes
 * enums serialize as strings ("NotStarted") instead of integers (0).
 * This is important for API readability and frontend compatibility.
 */
builder.Services.AddControllers()
    .AddJsonOptions(options =>
    {
        options.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter());
    });

// AddOpenApi enables the OpenAPI/Swagger endpoint for API documentation
builder.Services.AddOpenApi();

/*
 * CORS (Cross-Origin Resource Sharing) configuration.
 * In development, the frontend (localhost:5173) and backend (localhost:5000)
 * are on different origins, so the browser blocks cross-origin requests unless
 * the server allows it via CORS headers.
 *
 * AllowAnyOrigin is permissive — fine for development/education but not for production.
 * In production (Docker Compose), Nginx proxies all requests, so CORS isn't needed.
 */
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

// ===== MIDDLEWARE PIPELINE =====
// After builder.Build(), we configure the HTTP request pipeline.
// Middleware runs in the ORDER it's added — this order matters!

var app = builder.Build();

// OpenAPI endpoint only in development
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

/*
 * Middleware order:
 * 1. CORS — must come before authentication
 * 2. Authentication — verifies the JWT token
 * 3. Authorization — checks if the user has permission
 * 4. MapControllers — routes requests to controllers
 *
 * If Authentication came after MapControllers, the controller would run
 * before the token was validated — a security vulnerability.
 */
app.UseCors("AllowFrontend");
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

/*
 * Auto-migrate database on startup.
 * This applies any pending EF Core migrations automatically.
 *
 * Tradeoff: Convenient for development but dangerous for production.
 * In production, you'd use a controlled migration process (e.g., as part of CI/CD)
 * to avoid downtime or data loss from failed migrations.
 */
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.Migrate();
}

app.Run();
