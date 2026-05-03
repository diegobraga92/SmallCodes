using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using MediaTracker.Api.Models;

namespace MediaTracker.Api.Data;

/*
 * AppDbContext is the bridge between our C# code and the PostgreSQL database.
 * It's the "D" in "Dependency Injection" — registered in Program.cs and injected
 * into services via constructor parameters.
 *
 * It extends IdentityDbContext (not plain DbContext) because we're using ASP.NET
 * Core Identity for authentication. IdentityDbContext adds DbSets for users, roles,
 * claims, etc. (AspNetUsers, AspNetRoles, AspNetUserRoles, ...).
 *
 * If we weren't using Identity, we'd extend plain DbContext instead.
 */
public class AppDbContext : IdentityDbContext
{
    /*
     * The constructor takes DbContextOptions which is configured in Program.cs
     * with the PostgreSQL connection string. The options are passed to the base
     * class via ": base(options)".
     */
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    /*
     * DbSet<MediaItem> represents the MediaItems table. EF Core uses this to
     * perform CRUD operations. The "= null!" is a null-forgiving operator —
     * it tells the compiler "trust me, this won't be null at runtime" because
     * EF Core sets it via reflection. Without it, the nullable reference type
     * warning would appear.
     */
    public DbSet<MediaItem> MediaItems { get; set; } = null!;

    /*
     * OnModelCreating is called by EF Core when the model is being built.
     * This is where we configure the database schema using the Fluent API.
     *
     * Fluent API vs Data Annotations: Both achieve similar goals, but Fluent API
     * is more powerful for complex mappings (like TPH inheritance) and keeps
     * the model classes cleaner. Data annotations are simpler for basic constraints
     * (like [Required], [MaxLength]) directly on properties.
     */
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Must call base.OnModelCreating() to let Identity configure its tables
        base.OnModelCreating(modelBuilder);

        /*
         * TPH (Table Per Hierarchy) configuration:
         *
         * HasDiscriminator tells EF Core to use the MediaType property as the
         * discriminator column. When querying MediaItems, EF Core reads this
         * column and instantiates the correct subclass (Book, Game, or Movie).
         *
         * Alternative strategies:
         * - TPT (Table Per Type): Separate tables for each subclass, joined via FK.
         *   More normalized but requires JOINs for every query.
         * - TPC (Table Per Concrete): Each subclass gets its own table with all columns
         *   (including inherited ones). No shared table, no JOINs, but duplicated columns.
         *
         * We chose TPH because it's the simplest — one table, one query, no joins.
         * The tradeoff is nullable columns for subtype-specific properties.
         */
        modelBuilder.Entity<MediaItem>(entity =>
        {
            entity.ToTable("MediaItems");
            entity.HasDiscriminator(m => m.MediaType)
                  .HasValue<Book>(MediaType.Book)
                  .HasValue<Game>(MediaType.Game)
                  .HasValue<Movie>(MediaType.Movie);

            /*
             * Fluent API configuration for columns. These duplicate some of the
             * data annotations on the model classes. In a real project, you'd
             * typically pick one approach and stick with it. We use both here
             * to demonstrate both techniques.
             */
            entity.Property(m => m.Title).IsRequired().HasMaxLength(200);
            entity.Property(m => m.Description).HasMaxLength(2000);
            entity.Property(m => m.Genre).HasMaxLength(100);
            entity.Property(m => m.UserId).IsRequired();
        });

        /*
         * Subtype-specific configurations. These configure columns that only
         * exist on the specific subclass. EF Core knows to only apply these
         * to rows where the discriminator matches.
         */
        modelBuilder.Entity<Book>(entity =>
        {
            entity.Property(b => b.Author).HasMaxLength(200);
            entity.Property(b => b.Isbn).HasMaxLength(20);
        });

        modelBuilder.Entity<Game>(entity =>
        {
            entity.Property(g => g.Platform).HasMaxLength(100);
            entity.Property(g => g.Developer).HasMaxLength(200);
            entity.Property(g => g.Publisher).HasMaxLength(200);
        });

        modelBuilder.Entity<Movie>(entity =>
        {
            entity.Property(m => m.Director).HasMaxLength(200);
        });
    }
}
