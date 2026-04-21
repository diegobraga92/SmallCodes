/*
    C# ENTITY FRAMEWORK CORE
    File: 21_entity_framework.cs
    
    Comprehensive guide to Entity Framework Core in C#.
    Covers DbContext, entities, migrations, LINQ queries, relationships,
    change tracking, performance optimization, and best practices.
*/

using System;
using System.Linq;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

namespace CSharpRefresher.EntityFramework
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Entity Framework Core ===\n");
            
            DemonstrateDbContextAndEntities();
            DemonstrateMigrations();
            DemonstrateQueriesAndLinq();
            DemonstrateRelationships();
            DemonstrateChangeTracking();
            DemonstratePerformanceAndBestPractices();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateDbContextAndEntities()
        {
            Console.WriteLine("=== 1. DbContext and Entities ===\n");
            
            // 1. Entity classes
            Console.WriteLine("1. Entity Classes:");
            
            // Example entity with data annotations
            [Table("Users")]
            public class User
            {
                [Key]
                [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
                public int Id { get; set; }
                
                [Required]
                [MaxLength(100)]
                public string Username { get; set; }
                
                [EmailAddress]
                [MaxLength(200)]
                public string Email { get; set; }
                
                [NotMapped] // This property won't be mapped to database
                public string DisplayName => $"{Username} ({Email})";
                
                public DateTime CreatedAt { get; set; }
                public bool IsActive { get; set; }
                
                // Navigation properties (relationships)
                public virtual ICollection<Order> Orders { get; set; }
                public virtual UserProfile Profile { get; set; }
                
                // Constructor
                public User()
                {
                    Orders = new HashSet<Order>();
                    CreatedAt = DateTime.UtcNow;
                }
            }
            
            [Table("UserProfiles")]
            public class UserProfile
            {
                [Key, ForeignKey("User")]
                public int UserId { get; set; }
                
                [MaxLength(500)]
                public string Bio { get; set; }
                
                [MaxLength(100)]
                public string Location { get; set; }
                
                public DateTime? BirthDate { get; set; }
                
                // Navigation property
                public virtual User User { get; set; }
            }
            
            [Table("Orders")]
            public class Order
            {
                public int Id { get; set; }
                public string OrderNumber { get; set; }
                public decimal TotalAmount { get; set; }
                public DateTime OrderDate { get; set; }
                public OrderStatus Status { get; set; }
                
                // Foreign key
                public int UserId { get; set; }
                
                // Navigation property
                public virtual User User { get; set; }
                
                // Complex property (owned entity)
                public Address ShippingAddress { get; set; }
                
                // Value conversion example
                public Dictionary<string, string> Metadata { get; set; }
            }
            
            // Owned entity type
            [Owned]
            public class Address
            {
                public string Street { get; set; }
                public string City { get; set; }
                public string Country { get; set; }
                public string PostalCode { get; set; }
            }
            
            // Enum for order status
            public enum OrderStatus
            {
                Pending,
                Processing,
                Shipped,
                Delivered,
                Cancelled
            }
            
            Console.WriteLine("""
                Entity class features:
                • Data annotations for configuration
                • Navigation properties for relationships
                • Foreign key properties
                • Owned entity types (value objects)
                • Value converters for complex types
                • NotMapped for computed properties
                """);
            
            // 2. DbContext
            Console.WriteLine("\n2. DbContext:");
            
            public class AppDbContext : DbContext
            {
                // DbSets represent database tables
                public DbSet<User> Users { get; set; }
                public DbSet<UserProfile> UserProfiles { get; set; }
                public DbSet<Order> Orders { get; set; }
                
                // Constructor with options
                public AppDbContext(DbContextOptions<AppDbContext> options) 
                    : base(options)
                {
                }
                
                // Parameterless constructor for design-time
                protected AppDbContext()
                {
                }
                
                // OnConfiguring (alternative to dependency injection)
                protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
                {
                    if (!optionsBuilder.IsConfigured)
                    {
                        // Development connection string
                        optionsBuilder.UseSqlServer(
                            "Server=localhost;Database=EfDemo;Integrated Security=True;",
                            options => options.EnableRetryOnFailure(3));
                        
                        // Enable logging
                        optionsBuilder.LogTo(Console.WriteLine, LogLevel.Information);
                        optionsBuilder.EnableSensitiveDataLogging(); // For development only
                    }
                }
                
                // OnModelCreating for fluent configuration
                protected override void OnModelCreating(ModelBuilder modelBuilder)
                {
                    base.OnModelCreating(modelBuilder);
                    
                    // Fluent API configuration
                    modelBuilder.Entity<User>(entity =>
                    {
                        // Table name (already set via annotation)
                        entity.ToTable("Users");
                        
                        // Primary key
                        entity.HasKey(e => e.Id);
                        
                        // Properties configuration
                        entity.Property(e => e.Username)
                            .IsRequired()
                            .HasMaxLength(100);
                            
                        entity.Property(e => e.Email)
                            .HasMaxLength(200);
                            
                        entity.Property(e => e.CreatedAt)
                            .HasDefaultValueSql("GETUTCDATE()");
                            
                        entity.Property(e => e.IsActive)
                            .HasDefaultValue(true);
                            
                        // Indexes
                        entity.HasIndex(e => e.Username)
                            .IsUnique();
                            
                        entity.HasIndex(e => e.Email)
                            .IsUnique();
                            
                        // Query filters (global filters)
                        entity.HasQueryFilter(e => e.IsActive);
                    });
                    
                    modelBuilder.Entity<UserProfile>(entity =>
                    {
                        entity.HasKey(e => e.UserId);
                        
                        // One-to-one relationship
                        entity.HasOne(e => e.User)
                            .WithOne(e => e.Profile)
                            .HasForeignKey<UserProfile>(e => e.UserId)
                            .OnDelete(DeleteBehavior.Cascade);
                    });
                    
                    modelBuilder.Entity<Order>(entity =>
                    {
                        entity.HasKey(e => e.Id);
                        
                        entity.Property(e => e.OrderNumber)
                            .IsRequired()
                            .HasMaxLength(50);
                            
                        entity.Property(e => e.TotalAmount)
                            .HasPrecision(18, 2);
                            
                        entity.Property(e => e.OrderDate)
                            .HasDefaultValueSql("GETUTCDATE()");
                            
                        // Configure owned entity
                        entity.OwnsOne(e => e.ShippingAddress, address =>
                        {
                            address.Property(a => a.Street).HasMaxLength(200);
                            address.Property(a => a.City).HasMaxLength(100);
                            address.Property(a => a.Country).HasMaxLength(100);
                            address.Property(a => a.PostalCode).HasMaxLength(20);
                        });
                        
                        // Configure value converter for dictionary
                        entity.Property(e => e.Metadata)
                            .HasConversion(
                                v => System.Text.Json.JsonSerializer.Serialize(v, null),
                                v => System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, string>>(v, null));
                            
                        // Configure enum as string
                        entity.Property(e => e.Status)
                            .HasConversion<string>()
                            .HasMaxLength(20);
                            
                        // One-to-many relationship
                        entity.HasOne(e => e.User)
                            .WithMany(e => e.Orders)
                            .HasForeignKey(e => e.UserId)
                            .OnDelete(DeleteBehavior.Restrict);
                            
                        // Index
                        entity.HasIndex(e => e.OrderNumber)
                            .IsUnique();
                            
                        entity.HasIndex(e => e.OrderDate);
                    });
                    
                    // Seed data
                    modelBuilder.Entity<User>().HasData(
                        new User { Id = 1, Username = "admin", Email = "admin@example.com", IsActive = true },
                        new User { Id = 2, Username = "user1", Email = "user1@example.com", IsActive = true }
                    );
                }
            }
            
            Console.WriteLine("""
                DbContext responsibilities:
                • DbSet properties for entity collections
                • Connection and configuration
                • Fluent API configuration in OnModelCreating
                • Change tracking
                • Database operations
                • Transaction management
                """);
            
            // 3. DbContext lifetime and dependency injection
            Console.WriteLine("\n3. DbContext Lifetime and DI:");
            
            Console.WriteLine("""
                In Startup.cs (ASP.NET Core):
                
                services.AddDbContext<AppDbContext>(options =>
                    options.UseSqlServer(Configuration.GetConnectionString("DefaultConnection"))
                           .UseLoggerFactory(LoggerFactory.Create(builder => builder.AddConsole()))
                           .EnableSensitiveDataLogging() // Development only
                );
                
                // For scoped lifetime (recommended):
                services.AddDbContext<AppDbContext>(options => ...);
                
                // For pooled lifetime (high-performance):
                services.AddDbContextPool<AppDbContext>(options => ..., poolSize: 128);
                
                // For multiple DbContexts:
                services.AddDbContext<AppDbContext>(...);
                services.AddDbContext<OtherDbContext>(...);
                """);
            
            // 4. Database providers
            Console.WriteLine("\n4. Database Providers:");
            Console.WriteLine("""
                Supported providers:
                • SQL Server: UseSqlServer()
                • PostgreSQL: UseNpgsql()
                • MySQL: UseMySQL() or UseMySql()
                • SQLite: UseSqlite()
                • Cosmos DB: UseCosmos()
                • In-memory: UseInMemoryDatabase() (testing only)
                
                Provider-specific features:
                • SQL Server: Temporal tables, JSON support, full-text search
                • PostgreSQL: JSONB, array types, spatial data
                • SQLite: File-based, good for mobile/local apps
                """);
        }
        
        static void DemonstrateMigrations()
        {
            Console.WriteLine("\n=== 2. Migrations ===\n");
            
            // 1. Migration commands
            Console.WriteLine("1. Migration Commands:");
            Console.WriteLine("""
                Package Manager Console commands:
                • Add-Migration InitialCreate
                • Remove-Migration
                • Update-Database
                • Script-Migration
                
                .NET CLI commands:
                • dotnet ef migrations add InitialCreate
                • dotnet ef migrations remove
                • dotnet ef database update
                • dotnet ef migrations script
                
                Generate SQL script:
                dotnet ef migrations script --output migration.sql
                """);
            
            // 2. Migration files
            Console.WriteLine("\n2. Migration Files:");
            Console.WriteLine("""
                Migration contains:
                • Up() method: Applies migration
                • Down() method: Reverts migration
                • Snapshot: Current model state
                
                Example migration:
                public partial class AddUserProfile : Migration
                {
                    protected override void Up(MigrationBuilder migrationBuilder)
                    {
                        migrationBuilder.CreateTable(
                            name: "UserProfiles",
                            columns: table => new
                            {
                                UserId = table.Column<int>(type: "int", nullable: false),
                                Bio = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: true),
                                Location = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true)
                            },
                            constraints: table =>
                            {
                                table.PrimaryKey("PK_UserProfiles", x => x.UserId);
                                table.ForeignKey(
                                    name: "FK_UserProfiles_Users_UserId",
                                    column: x => x.UserId,
                                    principalTable: "Users",
                                    principalColumn: "Id",
                                    onDelete: ReferentialAction.Cascade);
                            });
                    }
                    
                    protected override void Down(MigrationBuilder migrationBuilder)
                    {
                        migrationBuilder.DropTable(name: "UserProfiles");
                    }
                }
                """);
            
            // 3. Custom migration operations
            Console.WriteLine("\n3. Custom Migration Operations:");
            Console.WriteLine("""
                Custom SQL in migrations:
                migrationBuilder.Sql("UPDATE Users SET IsActive = 1 WHERE IsActive IS NULL");
                
                Raw SQL for complex operations:
                migrationBuilder.Sql(@"
                    CREATE PROCEDURE GetActiveUsers
                    AS
                    BEGIN
                        SELECT * FROM Users WHERE IsActive = 1
                    END
                ");
                
                Seeding data in migrations:
                migrationBuilder.InsertData(
                    table: "Users",
                    columns: new[] { "Username", "Email", "IsActive" },
                    values: new object[] { "admin", "admin@example.com", true });
                """);
            
            // 4. Migration strategies
            Console.WriteLine("\n4. Migration Strategies:");
            Console.WriteLine("""
                1. Generate scripts for DBA review:
                   dotnet ef migrations script --idempotent
                   
                2. Automatic migrations (not recommended for production):
                   context.Database.Migrate();
                   
                3. Deployment strategies:
                   • Apply migrations on app startup (simple apps)
                   • Use EF tooling in CI/CD pipeline
                   • Use DbUp or other migration tools
                   • Manual script application for production
                   
                4. Handling multiple DbContexts:
                   • Separate migrations for each context
                   • Use different migration folders
                   • Consider bounded contexts in DDD
                """);
            
            // 5. Data seeding
            Console.WriteLine("\n5. Data Seeding:");
            Console.WriteLine("""
                Model configuration seeding (HasData):
                modelBuilder.Entity<User>().HasData(
                    new User { Id = 1, Username = "admin" },
                    new User { Id = 2, Username = "user1" }
                );
                
                Limitations:
                • Primary key values must be specified
                • Relationships are tricky
                • Good for static/reference data
                
                Custom seeding class:
                public class DataSeeder
                {
                    public static void Seed(AppDbContext context)
                    {
                        if (!context.Users.Any())
                        {
                            context.Users.AddRange(
                                new User { Username = "admin" },
                                new User { Username = "user1" }
                            );
                            context.SaveChanges();
                        }
                    }
                }
                
                In Program.cs:
                using (var scope = app.Services.CreateScope())
                {
                    var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
                    DataSeeder.Seed(context);
                }
                """);
        }
        
        static void DemonstrateQueriesAndLinq()
        {
            Console.WriteLine("\n=== 3. Queries and LINQ ===\n");
            
            // 1. Basic queries
            Console.WriteLine("1. Basic LINQ Queries:");
            
            async Task BasicQueriesExample()
            {
                using var context = new AppDbContext();
                
                // Query all active users
                var users = await context.Users
                    .Where(u => u.IsActive)
                    .ToListAsync();
                
                // Single entity by ID
                var user = await context.Users
                    .FindAsync(1); // Primary key lookup
                    
                // First or default
                var admin = await context.Users
                    .FirstOrDefaultAsync(u => u.Username == "admin");
                    
                // Count
                int activeCount = await context.Users
                    .CountAsync(u => u.IsActive);
                    
                // Any (exists)
                bool hasAdmins = await context.Users
                    .AnyAsync(u => u.Username.Contains("admin"));
                    
                // Select specific columns (projection)
                var userNames = await context.Users
                    .Where(u => u.IsActive)
                    .Select(u => new { u.Id, u.Username })
                    .ToListAsync();
                    
                // Ordering
                var orderedUsers = await context.Users
                    .OrderBy(u => u.Username)
                    .ThenByDescending(u => u.CreatedAt)
                    .ToListAsync();
                    
                // Pagination
                var page = await context.Users
                    .Where(u => u.IsActive)
                    .OrderBy(u => u.Id)
                    .Skip(10) // Page 2 if page size is 10
                    .Take(10)
                    .ToListAsync();
            }
            Console.WriteLine("""
                Basic query patterns:
                • Where() for filtering
                • Select() for projection
                • OrderBy()/ThenBy() for sorting
                • Skip()/Take() for pagination
                • Count()/Any()/All() for aggregates
                • First()/Single()/Find() for single items
                """);
            
            // 2. Eager loading (Include)
            Console.WriteLine("\n2. Eager Loading (Include):");
            
            async Task EagerLoadingExample()
            {
                using var context = new AppDbContext();
                
                // Include related entities
                var usersWithOrders = await context.Users
                    .Include(u => u.Orders) // One-to-many
                    .Include(u => u.Profile) // One-to-one
                    .Where(u => u.IsActive)
                    .ToListAsync();
                
                // ThenInclude for nested relationships
                var usersWithOrderDetails = await context.Users
                    .Include(u => u.Orders)
                        .ThenInclude(o => o.ShippingAddress) // Owned entity
                    .ToListAsync();
                
                // Multiple includes
                var usersWithAll = await context.Users
                    .Include(u => u.Orders)
                    .Include(u => u.Profile)
                    .ToListAsync();
                
                // Filtered include (EF Core 5.0+)
                var usersWithRecentOrders = await context.Users
                    .Include(u => u.Orders
                        .Where(o => o.OrderDate > DateTime.UtcNow.AddDays(-30))
                        .OrderByDescending(o => o.OrderDate)
                        .Take(5))
                    .ToListAsync();
            }
            
            // 3. Explicit loading
            Console.WriteLine("\n3. Explicit Loading:");
            
            async Task ExplicitLoadingExample()
            {
                using var context = new AppDbContext();
                
                // Load entity first
                var user = await context.Users.FindAsync(1);
                
                // Explicitly load related data
                await context.Entry(user)
                    .Collection(u => u.Orders)
                    .LoadAsync();
                    
                // Load with query
                await context.Entry(user)
                    .Collection(u => u.Orders)
                    .Query()
                    .Where(o => o.Status == OrderStatus.Pending)
                    .LoadAsync();
                    
                // Load reference (one-to-one)
                await context.Entry(user)
                    .Reference(u => u.Profile)
                    .LoadAsync();
                    
                // Check if loaded
                bool isLoaded = context.Entry(user)
                    .Collection(u => u.Orders)
                    .IsLoaded;
            }
            
            // 4. Lazy loading
            Console.WriteLine("\n4. Lazy Loading:");
            Console.WriteLine("""
                Enable lazy loading:
                1. Install Microsoft.EntityFrameworkCore.Proxies
                2. Configure DbContext:
                   optionsBuilder.UseLazyLoadingProxies();
                
                3. Make navigation properties virtual:
                   public virtual ICollection<Order> Orders { get; set; }
                   public virtual UserProfile Profile { get; set; }
                
                Usage:
                var user = context.Users.Find(1);
                var orders = user.Orders; // Automatically loaded
                
                Considerations:
                • N+1 query problem
                • Performance implications
                • Use carefully, prefer eager loading
                """);
            
            // 5. Raw SQL queries
            Console.WriteLine("\n5. Raw SQL Queries:");
            
            async Task RawSqlExample()
            {
                using var context = new AppDbContext();
                
                // FromSqlRaw for entities
                var users = await context.Users
                    .FromSqlRaw("SELECT * FROM Users WHERE IsActive = 1")
                    .ToListAsync();
                
                // With parameters
                var specificUser = await context.Users
                    .FromSqlInterpolated($"SELECT * FROM Users WHERE Id = {1}")
                    .FirstOrDefaultAsync();
                
                // Stored procedures
                var activeUsers = await context.Users
                    .FromSqlRaw("EXEC GetActiveUsers")
                    .ToListAsync();
                
                // Non-entity SQL (ExecuteSqlRaw)
                int rowsAffected = await context.Database
                    .ExecuteSqlRawAsync("UPDATE Users SET IsActive = 0 WHERE LastLogin < {0}", 
                        DateTime.UtcNow.AddMonths(-6));
                
                // Views (treat as DbSet)
                // context.Set<UserView>().FromSqlRaw("SELECT * FROM vw_ActiveUsers");
            }
            
            // 6. Complex queries
            Console.WriteLine("\n6. Complex LINQ Queries:");
            
            async Task ComplexQueriesExample()
            {
                using var context = new AppDbContext();
                
                // Group by
                var ordersByStatus = await context.Orders
                    .GroupBy(o => o.Status)
                    .Select(g => new
                    {
                        Status = g.Key,
                        Count = g.Count(),
                        Total = g.Sum(o => o.TotalAmount)
                    })
                    .ToListAsync();
                
                // Join
                var userOrders = await context.Users
                    .Join(context.Orders,
                        user => user.Id,
                        order => order.UserId,
                        (user, order) => new { user.Username, order.OrderNumber, order.TotalAmount })
                    .ToListAsync();
                
                // Subquery
                var usersWithOrders = await context.Users
                    .Where(u => context.Orders.Any(o => o.UserId == u.Id && o.TotalAmount > 100))
                    .ToListAsync();
                
                // Case/when equivalent
                var orderSummary = await context.Orders
                    .Select(o => new
                    {
                        o.OrderNumber,
                        SizeCategory = o.TotalAmount > 1000 ? "Large" :
                                      o.TotalAmount > 100 ? "Medium" : "Small"
                    })
                    .ToListAsync();
            }
        }
        
        static void DemonstrateRelationships()
        {
            Console.WriteLine("\n=== 4. Relationships ===\n");
            
            // 1. Relationship types
            Console.WriteLine("1. Relationship Types:");
            Console.WriteLine("""
                One-to-Many (most common):
                • User has many Orders
                • Order belongs to one User
                • Navigation: User.Orders (collection), Order.User (reference)
                • Foreign key: Order.UserId
                
                One-to-One:
                • User has one Profile
                • Profile belongs to one User
                • Navigation: User.Profile, Profile.User
                • Foreign key: Profile.UserId (also primary key)
                
                Many-to-Many (EF Core 5.0+):
                • Product has many Categories
                • Category has many Products
                • Join entity: ProductCategory
                • Navigation: Product.Categories, Category.Products
                
                Owned Entities (Value Objects):
                • Order has ShippingAddress
                • Address is owned by Order
                • No separate identity
                • Stored in same table as Order
                """);
            
            // 2. Configuring relationships
            Console.WriteLine("\n2. Configuring Relationships:");
            Console.WriteLine("""
                Fluent API configuration:
                
                // One-to-Many
                modelBuilder.Entity<Order>()
                    .HasOne(o => o.User)
                    .WithMany(u => u.Orders)
                    .HasForeignKey(o => o.UserId)
                    .OnDelete(DeleteBehavior.Cascade);
                
                // One-to-One
                modelBuilder.Entity<UserProfile>()
                    .HasOne(p => p.User)
                    .WithOne(u => u.Profile)
                    .HasForeignKey<UserProfile>(p => p.UserId);
                
                // Many-to-Many (implicit join table)
                modelBuilder.Entity<Product>()
                    .HasMany(p => p.Categories)
                    .WithMany(c => c.Products)
                    .UsingEntity<Dictionary<string, object>>(
                        "ProductCategory",
                        j => j.HasOne<Category>().WithMany().HasForeignKey("CategoryId"),
                        j => j.HasOne<Product>().WithMany().HasForeignKey("ProductId"),
                        j => j.HasKey("ProductId", "CategoryId"));
                
                // Many-to-Many (explicit join entity)
                modelBuilder.Entity<ProductCategory>()
                    .HasKey(pc => new { pc.ProductId, pc.CategoryId });
                    
                modelBuilder.Entity<ProductCategory>()
                    .HasOne(pc => pc.Product)
                    .WithMany(p => p.ProductCategories)
                    .HasForeignKey(pc => pc.ProductId);
                    
                modelBuilder.Entity<ProductCategory>()
                    .HasOne(pc => pc.Category)
                    .WithMany(c => c.ProductCategories)
                    .HasForeignKey(pc => pc.CategoryId);
                """);
            
            // 3. Cascade delete behavior
            Console.WriteLine("\n3. Cascade Delete Behavior:");
            Console.WriteLine("""
                DeleteBehavior options:
                • Cascade: Delete related entities
                • Restrict: Prevent delete if related entities exist
                • SetNull: Set foreign key to null
                • ClientSetNull: Similar to SetNull, handled by EF
                • ClientCascade: Cascade delete handled by EF
                • NoAction: Database takes no action (default for optional relationships)
                
                Considerations:
                • Use Cascade for composition (Order->OrderItems)
                • Use Restrict or SetNull for aggregation (User->Orders)
                • Consider database constraints
                """);
            
            // 4. Relationship loading patterns
            Console.WriteLine("\n4. Relationship Loading Patterns:");
            Console.WriteLine("""
                Eager Loading (Include):
                • Load related data in same query
                • Good for known needed relationships
                • Can cause large result sets
                
                Explicit Loading:
                • Load relationships on demand
                • More control over what loads
                • Extra database round-trips
                
                Lazy Loading:
                • Automatic loading on access
                • Convenient but can cause N+1
                • Requires virtual properties
                
                Select Loading (Projection):
                • Load only needed data
                • Most efficient for read operations
                • Doesn't load full entity graphs
                """);
        }
        
        static void DemonstrateChangeTracking()
        {
            Console.WriteLine("\n=== 5. Change Tracking ===\n");
            
            // 1. Change tracking states
            Console.WriteLine("1. Entity States:");
            Console.WriteLine("""
                EntityState enumeration:
                • Detached: Not tracked by context
                • Unchanged: Tracked but not modified
                • Added: Will be inserted on SaveChanges
                • Modified: Will be updated on SaveChanges
                • Deleted: Will be deleted on SaveChanges
                
                State transitions:
                • Add(): Entity becomes Added
                • Attach(): Entity becomes Unchanged
                • Remove(): Entity becomes Deleted
                • Property modification: Entity becomes Modified
                """);
            
            // 2. Tracking modifications
            Console.WriteLine("\n2. Tracking Modifications:");
            
            async Task ChangeTrackingExample()
            {
                using var context = new AppDbContext();
                
                // Add new entity
                var newUser = new User { Username = "newuser", Email = "new@example.com" };
                context.Users.Add(newUser); // State: Added
                
                // Update existing entity
                var user = await context.Users.FindAsync(1);
                user.Username = "updated"; // State: Modified (automatic)
                
                // Mark as modified explicitly
                var anotherUser = new User { Id = 2, Username = "explicit" };
                context.Entry(anotherUser).State = EntityState.Modified;
                
                // Delete entity
                var userToDelete = await context.Users.FindAsync(3);
                context.Users.Remove(userToDelete); // State: Deleted
                
                // Attach detached entity
                var detachedUser = new User { Id = 4, Username = "detached" };
                context.Users.Attach(detachedUser); // State: Unchanged
                
                // Check state
                var state = context.Entry(user).State; // EntityState.Modified
                
                // Save changes
                int changes = await context.SaveChangesAsync();
                Console.WriteLine($"Saved {changes} changes");
            }
            
            // 3. Change tracking queries
            Console.WriteLine("\n3. Change Tracking Queries:");
            
            async Task ChangeQueriesExample()
            {
                using var context = new AppDbContext();
                
                var user = await context.Users.FindAsync(1);
                user.Username = "changed";
                
                // Get all modified entities
                var modifiedEntries = context.ChangeTracker
                    .Entries()
                    .Where(e => e.State == EntityState.Modified)
                    .ToList();
                
                // Get original values
                var entry = context.Entry(user);
                var originalName = entry.OriginalValues["Username"];
                var currentName = entry.CurrentValues["Username"];
                
                // Check if property modified
                bool isUsernameModified = entry.Property(u => u.Username).IsModified;
                
                // Get modified properties
                var modifiedProps = entry.Properties
                    .Where(p => p.IsModified)
                    .Select(p => p.Metadata.Name)
                    .ToList();
                
                // Revert changes
                entry.State = EntityState.Unchanged;
                // or entry.Reload();
            }
            
            // 4. Disconnected scenarios
            Console.WriteLine("\n4. Disconnected Scenarios:");
            
            async Task DisconnectedExample()
            {
                // Simulate getting entity from API/outside context
                var updatedUser = new User { Id = 1, Username = "updated", Email = "new@example.com" };
                
                using var context = new AppDbContext();
                
                // Approach 1: Attach and mark as modified
                context.Users.Attach(updatedUser);
                context.Entry(updatedUser).State = EntityState.Modified;
                
                // Approach 2: Update existing entity
                var existingUser = await context.Users.FindAsync(1);
                context.Entry(existingUser).CurrentValues.SetValues(updatedUser);
                
                // Approach 3: Update specific properties
                context.Entry(existingUser).Property(u => u.Username).IsModified = true;
                context.Entry(existingUser).Property(u => u.Email).IsModified = true;
                
                // Handle concurrency
                try
                {
                    await context.SaveChangesAsync();
                }
                catch (DbUpdateConcurrencyException ex)
                {
                    // Handle concurrent modification
                    var entry = ex.Entries[0];
                    var databaseValues = await entry.GetDatabaseValuesAsync();
                    
                    // Choose resolution strategy
                    // 1. Client wins
                    entry.OriginalValues.SetValues(databaseValues);
                    
                    // 2. Database wins  
                    // entry.CurrentValues.SetValues(databaseValues);
                    
                    // 3. Merge
                    // entry.CurrentValues[name] = Merge(original, current, database);
                    
                    await context.SaveChangesAsync();
                }
            }
            
            // 5. AsNoTracking
            Console.WriteLine("\n5. AsNoTracking (Read-only Queries):");
            
            async Task NoTrackingExample()
            {
                using var context = new AppDbContext();
                
                // Read-only query (no change tracking overhead)
                var users = await context.Users
                    .AsNoTracking()
                    .Where(u => u.IsActive)
                    .ToListAsync();
                
                // AsNoTrackingWithIdentityResolution (EF Core 5.0+)
                // For read-only scenarios with relationships
                var usersWithOrders = await context.Users
                    .AsNoTrackingWithIdentityResolution()
                    .Include(u => u.Orders)
                    .ToListAsync();
                
                // Configure default tracking behavior
                // context.ChangeTracker.QueryTrackingBehavior = QueryTrackingBehavior.NoTracking;
            }
        }
        
        static void DemonstratePerformanceAndBestPractices()
        {
            Console.WriteLine("\n=== 6. Performance and Best Practices ===\n");
            
            Console.WriteLine("1. Query Performance:");
            Console.WriteLine("""
                Common performance issues:
                • N+1 queries (lazy loading in loops)
                • Selecting too much data
                • Missing indexes
                • Client-side evaluation
                
                Solutions:
                • Use Include() for needed relationships
                • Project only needed columns (Select())
                • Add appropriate database indexes
                • Use AsNoTracking() for read-only
                • Enable query logging to identify issues
                """);
            
            Console.WriteLine("\n2. Bulk Operations:");
            Console.WriteLine("""
                For bulk inserts/updates:
                
                // Bad: Individual inserts
                foreach (var item in items)
                {
                    context.Items.Add(item);
                    await context.SaveChangesAsync(); // Each item hits database
                }
                
                // Better: Batch inserts
                context.Items.AddRange(items);
                await context.SaveChangesAsync(); // Single round-trip
                
                // Best: Bulk extensions
                // Use EF Core BulkExtensions, EFCore.BulkExtensions, etc.
                await context.BulkInsertAsync(items);
                
                For bulk updates:
                // Use ExecuteSqlRaw for large updates
                await context.Database.ExecuteSqlRawAsync(
                    "UPDATE Items SET Status = {0} WHERE CategoryId = {1}",
                    newStatus, categoryId);
                """);
            
            Console.WriteLine("\n3. Connection Management:");
            Console.WriteLine("""
                • Use dependency injection for DbContext
                • Keep DbContext lifetime short (scoped)
                • Use DbContext pooling for high-throughput
                • Close connections properly (using statement)
                • Configure connection pool size
                • Enable MARS (MultipleActiveResultSets) if needed
                """);
            
            Console.WriteLine("\n4. Monitoring and Logging:");
            Console.WriteLine("""
                Enable detailed logging:
                optionsBuilder.LogTo(Console.WriteLine, LogLevel.Information);
                
                Use MiniProfiler for query analysis:
                services.AddMiniProfiler().AddEntityFramework();
                
                Monitor slow queries:
                • SQL Server: Query Store, Extended Events
                • PostgreSQL: pg_stat_statements
                • Application: Application Insights, OpenTelemetry
                """);
            
            Console.WriteLine("\n5. Testing:");
            Console.WriteLine("""
                Unit testing:
                • Mock DbContext using interfaces
                • Use InMemory database for simple tests
                • Consider using SQLite in-memory for relational tests
                
                Integration testing:
                • Use test containers for real database
                • Reset database state between tests
                • Use transaction rollback for isolation
                """);
            
            Console.WriteLine("\n6. Common Pitfalls:");
            Console.WriteLine("""
                1. Long-lived DbContext:
                   • Accumulates change tracking
                   • Memory leaks
                   • Stale data
                   
                2. Client-side evaluation:
                   // Warning: client-side evaluation
                   var result = context.Users
                       .Where(u => u.Username.StartsWith("A"))
                       .ToList() // Forces client evaluation
                       .Where(u => SomeComplexMethod(u));
                       
                3. Missing indexes on foreign keys
                4. Not using async/await for I/O
                5. Ignoring transaction boundaries
                6. Not handling concurrency conflicts
                7. Overusing lazy loading
                """);
            
            Console.WriteLine("\n=== EF Core vs EF6 ===");
            Console.WriteLine("""
                EF Core advantages:
                • Cross-platform (.NET Core)
                • Better performance
                • Simpler codebase
                • More flexible mapping
                • Open source
                
                EF6 advantages:
                • More mature
                • More features (some)
                • Better tooling (some areas)
                • Stable API
                
                Migration from EF6:
                • Not direct upgrade
                • Manual migration needed
                • Consider hybrid approach
                """);
            
            Console.WriteLine("\n=== Tools and Extensions ===");
            Console.WriteLine("""
                • EF Core Power Tools: Reverse engineering, diagrams
                • EFCore.BulkExtensions: Bulk operations
                • Z.EntityFramework.Plus: Batch operations, caching
                • Microsoft.EntityFrameworkCore.Cosmos: Cosmos DB provider
                • Pomelo.EntityFrameworkCore.MySql: MySQL provider
                • Npgsql.EntityFrameworkCore.PostgreSQL: PostgreSQL provider
                """);
        }
    }
}