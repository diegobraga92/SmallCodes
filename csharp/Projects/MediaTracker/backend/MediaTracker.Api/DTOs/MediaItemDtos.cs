using System.ComponentModel.DataAnnotations;
using MediaTracker.Api.Models;

namespace MediaTracker.Api.DTOs;

/*
 * These DTOs define the API contract for media item operations.
 *
 * Notice how MediaItemDto flattens the inheritance hierarchy — instead of having
 * separate DTOs for BookDto, GameDto, MovieDto, we have a single DTO with all
 * type-specific fields as nullable. This is simpler for the frontend to consume
 * (one type to handle) but means the frontend receives null fields for properties
 * that don't apply to the current media type.
 *
 * Alternative: We could have separate DTOs per type (BookDto, GameDto, MovieDto)
 * and use a discriminated union. This would be more type-safe but more complex
 * to serialize/deserialize. The flat approach is pragmatic for this scope.
 */

/*
 * Response DTO — sent from server to client when returning media items.
 * Includes all fields from all media types (flattened).
 */
public class MediaItemDto
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string? Description { get; set; }
    public string? Genre { get; set; }
    public MediaStatus Status { get; set; }
    public int? Rating { get; set; }
    public MediaType MediaType { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }

    // Book-specific
    public string? Author { get; set; }
    public int? Pages { get; set; }
    public string? Isbn { get; set; }

    // Game-specific
    public string? Platform { get; set; }
    public string? Developer { get; set; }
    public string? Publisher { get; set; }
    public int? HoursPlayed { get; set; }

    // Movie-specific
    public string? Director { get; set; }
    public int? DurationMinutes { get; set; }
    public int? ReleaseYear { get; set; }
}

/*
 * Create DTO — sent from client to server when creating a new media item.
 * Note: There is NO UserId field here! The UserId is extracted from the JWT
 * token server-side (see MediaController.GetUserId()). This is a security measure
 * — if we accepted UserId from the client, a malicious user could create items
 * belonging to other users.
 */
public class CreateMediaItemDto
{
    [Required]
    [MaxLength(200)]
    public string Title { get; set; } = string.Empty;

    [MaxLength(2000)]
    public string? Description { get; set; }

    [MaxLength(100)]
    public string? Genre { get; set; }

    public MediaStatus Status { get; set; } = MediaStatus.NotStarted;

    [Range(1, 5)]
    public int? Rating { get; set; }

    [Required]
    public MediaType MediaType { get; set; }

    // Book-specific
    [MaxLength(200)]
    public string? Author { get; set; }
    public int? Pages { get; set; }
    [MaxLength(20)]
    public string? Isbn { get; set; }

    // Game-specific
    [MaxLength(100)]
    public string? Platform { get; set; }
    [MaxLength(200)]
    public string? Developer { get; set; }
    [MaxLength(200)]
    public string? Publisher { get; set; }
    public int? HoursPlayed { get; set; }

    // Movie-specific
    [MaxLength(200)]
    public string? Director { get; set; }
    public int? DurationMinutes { get; set; }
    public int? ReleaseYear { get; set; }
}

/*
 * Update DTO — sent from client to server when updating an existing media item.
 * All fields are optional (nullable) because the client may only want to update
 * specific fields. This is called a "partial update" or "patch-style" update.
 *
 * The service layer (MediaService.UpdateAsync) checks each field for null before
 * applying it. If a field is null, it means "don't change this field."
 *
 * Tradeoff: We can't distinguish between "set this field to empty string" and
 * "don't change this field." For this app, that's acceptable. For apps where
 * clearing a field is meaningful, you'd need a different approach (e.g., using
 * a special "null" vs "not provided" pattern).
 */
public class UpdateMediaItemDto
{
    [MaxLength(200)]
    public string? Title { get; set; }

    [MaxLength(2000)]
    public string? Description { get; set; }

    [MaxLength(100)]
    public string? Genre { get; set; }

    public MediaStatus? Status { get; set; }

    [Range(1, 5)]
    public int? Rating { get; set; }

    // Book-specific
    [MaxLength(200)]
    public string? Author { get; set; }
    public int? Pages { get; set; }
    [MaxLength(20)]
    public string? Isbn { get; set; }

    // Game-specific
    [MaxLength(100)]
    public string? Platform { get; set; }
    [MaxLength(200)]
    public string? Developer { get; set; }
    [MaxLength(200)]
    public string? Publisher { get; set; }
    public int? HoursPlayed { get; set; }

    // Movie-specific
    [MaxLength(200)]
    public string? Director { get; set; }
    public int? DurationMinutes { get; set; }
    public int? ReleaseYear { get; set; }
}
