using MediaTracker.Api.DTOs;

namespace MediaTracker.Api.Services;

/*
 * IMediaService defines the contract for media item operations.
 * Note that every method takes a userId parameter — this is the security boundary.
 * The userId comes from the JWT token (set by the controller), not from the client.
 *
 * The methods return DTOs (MediaItemDto), not domain models (MediaItem). This ensures
 * the service layer handles the mapping, and the controller never sees domain models.
 */
public interface IMediaService
{
    /*
     * Returns all media items for a user, with optional filtering, searching, and sorting.
     * The parameters are all nullable — if not provided, sensible defaults are used.
     */
    Task<IEnumerable<MediaItemDto>> GetAllAsync(
        string userId,
        MediaTracker.Api.Models.MediaType? mediaType = null,
        string? search = null,
        string? sortBy = null,
        string? sortOrder = null);

    /*
     * Returns a single item, or null if not found or not owned by the user.
     * The controller converts null to 404 Not Found.
     */
    Task<MediaItemDto?> GetByIdAsync(Guid id, string userId);

    Task<MediaItemDto> CreateAsync(CreateMediaItemDto dto, string userId);

    /*
     * Returns null if the item doesn't exist or doesn't belong to the user.
     * This prevents users from discovering other users' items by ID.
     */
    Task<MediaItemDto?> UpdateAsync(Guid id, UpdateMediaItemDto dto, string userId);

    /*
     * Returns true if deleted, false if not found.
     */
    Task<bool> DeleteAsync(Guid id, string userId);
}
