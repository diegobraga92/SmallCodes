using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MediaTracker.Api.Models;

/*
 * Enums (short for "enumerations") are a type-safe way to define a set of named
 * constants. Unlike using strings or integers directly, enums prevent invalid values
 * at compile time — you can't accidentally pass "InProgres" (typo) where a MediaStatus
 * is expected. The JSON serializer converts these to/from strings via JsonStringEnumConverter
 * (configured in Program.cs), so the API sends/receives "NotStarted" rather than 0.
 */
public enum MediaStatus
{
    NotStarted,
    InProgress,
    Completed,
    OnHold,
    Dropped
}

public enum MediaType
{
    Book,
    Game,
    Movie
}

/*
 * MediaItem is an abstract class — it cannot be instantiated directly. It defines the
 * common properties shared by all media types (Book, Game, Movie). This is the base
 * of the inheritance hierarchy that EF Core maps using Table Per Hierarchy (TPH).
 *
 * TPH means all types share a single database table ("MediaItems") with a discriminator
 * column ("MediaType") that tells EF Core which subclass each row represents.
 * See AppDbContext.cs for the TPH configuration.
 *
 * Tradeoff: Type-specific properties (Author, Platform, Director, etc.) are stored in
 * separate subclasses but end up as nullable columns in the same table. This is simple
 * but wastes space and prevents NOT NULL constraints on subtype-specific columns.
 */
public abstract class MediaItem
{
    /*
     * [Key] identifies this as the primary key. We use Guid (globally unique identifier)
     * instead of auto-increment int for several reasons:
     *   1. Client-side generation: Guid.NewGuid() creates the ID before saving to DB,
     *      avoiding a round-trip to get the generated ID back.
     *   2. Harder to guess/iterate: Sequential int IDs make it easy to enumerate resources.
     *   3. Distributed-friendly: No central sequence needed — any node can generate IDs.
     *
     * Tradeoff: Guids are 16 bytes vs 4 bytes for int, and can cause index fragmentation
     * in some databases. PostgreSQL handles UUIDs reasonably well.
     */
    [Key]
    public Guid Id { get; set; } = Guid.NewGuid();

    /*
     * Data annotations like [Required] and [MaxLength] serve dual purposes:
     *   1. Model validation — ASP.NET Core automatically validates these before
     *      the controller action runs (returning 400 Bad Request if invalid).
     *   2. EF Core schema generation — migrations use these to create NOT NULL
     *      columns and VARCHAR(200) column types.
     *
     * This is the "data annotations" approach. The alternative is Fluent API in
     * AppDbContext.OnModelCreating(). We use a mix: annotations for simple constraints,
     * Fluent API for complex mappings (like TPH discriminator).
     */
    [Required]
    [MaxLength(200)]
    public string Title { get; set; } = string.Empty;

    [MaxLength(2000)]
    public string? Description { get; set; }

    [MaxLength(100)]
    public string? Genre { get; set; }

    public MediaStatus Status { get; set; } = MediaStatus.NotStarted;

    /*
     * Nullable int (int?) — the ? suffix makes the value type nullable. Rating is
     * optional because not all items have been rated yet. In the database this maps
     * to a nullable INTEGER column.
     */
    [Range(1, 5)]
    public int? Rating { get; set; }

    /*
     * This is the discriminator property used by EF Core's TPH mapping. It tells
     * EF Core which subclass (Book, Game, Movie) each row represents. The value is
     * set automatically when creating a new entity (e.g., new Book { MediaType = MediaType.Book }).
     */
    [Required]
    public MediaType MediaType { get; set; }

    /*
     * UserId links each media item to its owner. This is a foreign key to the
     * AspNetUsers table (from ASP.NET Core Identity). Note: there's no explicit
     * [ForeignKey] attribute here — the relationship is implicit. The UserId is
     * NEVER taken from the client's request body; it's extracted from the JWT token
     * server-side (see MediaController.GetUserId()). This prevents users from
     * creating/modifying items belonging to other users.
     */
    [Required]
    public string UserId { get; set; } = string.Empty;

    /*
     * DateTime.UtcNow stores the current time in Coordinated Universal Time (UTC).
     * Why UTC and not local time? UTC is timezone-agnostic — it doesn't matter where
     * the server is located. When displaying to users, the frontend converts to their
     * local timezone. Storing local time would be ambiguous (e.g., "2:30 PM" could
     * be EST, PST, BST, etc.).
     */
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}
