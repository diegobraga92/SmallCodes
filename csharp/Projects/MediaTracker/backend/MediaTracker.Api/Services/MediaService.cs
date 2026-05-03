using Microsoft.EntityFrameworkCore;
using MediaTracker.Api.Data;
using MediaTracker.Api.DTOs;
using MediaTracker.Api.Models;

namespace MediaTracker.Api.Services;

/*
 * MediaService contains all the business logic for media item CRUD operations.
 * It depends on AppDbContext (EF Core) for data access.
 *
 * This is the "Repository pattern" in practice — the service acts as an abstraction
 * layer between the controllers and the database. Controllers never touch the DbContext
 * directly.
 */
public class MediaService : IMediaService
{
    private readonly AppDbContext _context;

    public MediaService(AppDbContext context)
    {
        _context = context;
    }

    /*
     * GetAllAsync demonstrates LINQ (Language Integrated Query) — C#'s query syntax
     * that works against any data source (databases, collections, XML, etc.).
     *
     * Key LINQ concepts:
     * - .Where() filters records (like SQL WHERE)
     * - .OrderBy() / .OrderByDescending() sorts (like SQL ORDER BY)
     * - .ToListAsync() executes the query and returns results
     *
     * IMPORTANT: LINQ uses "deferred execution" — the query is NOT sent to the database
     * until .ToListAsync() is called. Before that, we're just building an expression tree
     * that EF Core translates to SQL. This allows us to chain multiple .Where() and
     * .OrderBy() calls without hitting the DB multiple times.
     */
    public async Task<IEnumerable<MediaItemDto>> GetAllAsync(
        string userId,
        MediaType? mediaType = null,
        string? search = null,
        string? sortBy = null,
        string? sortOrder = null)
    {
        /*
         * Start building the query. At this point, no SQL has been sent to the database.
         * .AsQueryable() ensures we can chain further LINQ operations.
         */
        var query = _context.MediaItems
            .Where(m => m.UserId == userId)  // Security: only the user's own items
            .AsQueryable();

        // Optional filter by media type (Book, Game, Movie)
        if (mediaType.HasValue)
        {
            query = query.Where(m => m.MediaType == mediaType.Value);
        }

        /*
         * Optional search — uses LIKE in SQL (via .Contains()).
         * We convert both sides to lowercase for case-insensitive search.
         * PostgreSQL is case-sensitive by default for text comparisons.
         *
         * Tradeoff: This uses LOWER() in SQL, which prevents index usage.
         * For a small app this is fine. For large datasets, you'd use PostgreSQL's
         * full-text search or a dedicated search engine like Elasticsearch.
         */
        if (!string.IsNullOrWhiteSpace(search))
        {
            var searchLower = search.ToLower();
            query = query.Where(m =>
                m.Title.ToLower().Contains(searchLower) ||
                (m.Description != null && m.Description.ToLower().Contains(searchLower)) ||
                (m.Genre != null && m.Genre.ToLower().Contains(searchLower)));
        }

        /*
         * Apply sorting using a switch expression (C# 8+ feature).
         * Switch expressions are more concise than traditional switch statements.
         * Default sort is by UpdatedAt descending (most recently updated first).
         */
        query = (sortBy?.ToLower()) switch
        {
            "title" => sortOrder?.ToLower() == "desc"
                ? query.OrderByDescending(m => m.Title)
                : query.OrderBy(m => m.Title),
            "rating" => sortOrder?.ToLower() == "desc"
                ? query.OrderByDescending(m => m.Rating)
                : query.OrderBy(m => m.Rating),
            "status" => sortOrder?.ToLower() == "desc"
                ? query.OrderByDescending(m => m.Status)
                : query.OrderBy(m => m.Status),
            "createdat" => sortOrder?.ToLower() == "desc"
                ? query.OrderByDescending(m => m.CreatedAt)
                : query.OrderBy(m => m.CreatedAt),
            _ => query.OrderByDescending(m => m.UpdatedAt) // default: newest updated first
        };

        /*
         * ToListAsync() EXECUTES the query against the database.
         * Before this line, no SQL was sent. After this line, we have the results in memory.
         * Then we map each entity to a DTO using LINQ's .Select().
         */
        var items = await query.ToListAsync();
        return items.Select(MapToDto);
    }

    public async Task<MediaItemDto?> GetByIdAsync(Guid id, string userId)
    {
        /*
         * FirstOrDefaultAsync returns the first match or null if none found.
         * We filter by both id AND userId — this prevents users from accessing
         * other users' items even if they know the GUID.
         */
        var item = await _context.MediaItems
            .FirstOrDefaultAsync(m => m.Id == id && m.UserId == userId);

        return item == null ? null : MapToDto(item);
    }

    /*
     * CreateAsync uses a switch expression to instantiate the correct subclass
     * based on MediaType. This is where the TPH inheritance comes to life —
     * we create a Book, Game, or Movie, and EF Core saves it to the MediaItems
     * table with the appropriate discriminator value.
     */
    public async Task<MediaItemDto> CreateAsync(CreateMediaItemDto dto, string userId)
    {
        /*
         * Switch expression pattern matching — a concise way to handle different types.
         * Each case creates the appropriate subclass and copies the DTO properties.
         *
         * Note: UserId is set from the parameter (which came from the JWT token),
         * NOT from the DTO. The DTO doesn't even have a UserId field.
         */
        MediaItem item = dto.MediaType switch
        {
            MediaType.Book => new Book
            {
                Title = dto.Title,
                Description = dto.Description,
                Genre = dto.Genre,
                Status = dto.Status,
                Rating = dto.Rating,
                MediaType = MediaType.Book,
                UserId = userId,
                Author = dto.Author,
                Pages = dto.Pages,
                Isbn = dto.Isbn
            },
            MediaType.Game => new Game
            {
                Title = dto.Title,
                Description = dto.Description,
                Genre = dto.Genre,
                Status = dto.Status,
                Rating = dto.Rating,
                MediaType = MediaType.Game,
                UserId = userId,
                Platform = dto.Platform,
                Developer = dto.Developer,
                Publisher = dto.Publisher,
                HoursPlayed = dto.HoursPlayed
            },
            MediaType.Movie => new Movie
            {
                Title = dto.Title,
                Description = dto.Description,
                Genre = dto.Genre,
                Status = dto.Status,
                Rating = dto.Rating,
                MediaType = MediaType.Movie,
                UserId = userId,
                Director = dto.Director,
                DurationMinutes = dto.DurationMinutes,
                ReleaseYear = dto.ReleaseYear
            },
            _ => throw new ArgumentException($"Invalid media type: {dto.MediaType}")
        };

        _context.MediaItems.Add(item);
        await _context.SaveChangesAsync();

        return MapToDto(item);
    }

    /*
     * UpdateAsync uses pattern matching (switch on type) to update type-specific
     * properties. The "is" keyword checks the runtime type of the entity.
     *
     * Only non-null DTO fields are applied — this is the "partial update" pattern.
     */
    public async Task<MediaItemDto?> UpdateAsync(Guid id, UpdateMediaItemDto dto, string userId)
    {
        var item = await _context.MediaItems
            .FirstOrDefaultAsync(m => m.Id == id && m.UserId == userId);

        if (item == null) return null;

        // Update common properties (only if provided — null means "don't change")
        if (dto.Title != null) item.Title = dto.Title;
        if (dto.Description != null) item.Description = dto.Description;
        if (dto.Genre != null) item.Genre = dto.Genre;
        if (dto.Status.HasValue) item.Status = dto.Status.Value;
        if (dto.Rating.HasValue) item.Rating = dto.Rating.Value;
        item.UpdatedAt = DateTime.UtcNow;

        /*
         * Pattern matching with "case Book book" checks if the item is a Book
         * AND creates a typed variable "book" in one step. This is called
         * "pattern matching with declaration" — a C# 7+ feature.
         */
        switch (item)
        {
            case Book book:
                if (dto.Author != null) book.Author = dto.Author;
                if (dto.Pages.HasValue) book.Pages = dto.Pages;
                if (dto.Isbn != null) book.Isbn = dto.Isbn;
                break;
            case Game game:
                if (dto.Platform != null) game.Platform = dto.Platform;
                if (dto.Developer != null) game.Developer = dto.Developer;
                if (dto.Publisher != null) game.Publisher = dto.Publisher;
                if (dto.HoursPlayed.HasValue) game.HoursPlayed = dto.HoursPlayed;
                break;
            case Movie movie:
                if (dto.Director != null) movie.Director = dto.Director;
                if (dto.DurationMinutes.HasValue) movie.DurationMinutes = dto.DurationMinutes;
                if (dto.ReleaseYear.HasValue) movie.ReleaseYear = dto.ReleaseYear;
                break;
        }

        await _context.SaveChangesAsync();
        return MapToDto(item);
    }

    public async Task<bool> DeleteAsync(Guid id, string userId)
    {
        var item = await _context.MediaItems
            .FirstOrDefaultAsync(m => m.Id == id && m.UserId == userId);

        if (item == null) return false;

        _context.MediaItems.Remove(item);
        await _context.SaveChangesAsync();
        return true;
    }

    /*
     * Maps a domain model (MediaItem or subclass) to a response DTO (MediaItemDto).
     * This is a private helper method — it's not part of the interface.
     *
     * The mapping uses pattern matching to copy type-specific properties.
     * This is where the TPH hierarchy is "flattened" into a single DTO.
     */
    private static MediaItemDto MapToDto(MediaItem item)
    {
        var dto = new MediaItemDto
        {
            Id = item.Id,
            Title = item.Title,
            Description = item.Description,
            Genre = item.Genre,
            Status = item.Status,
            Rating = item.Rating,
            MediaType = item.MediaType,
            CreatedAt = item.CreatedAt,
            UpdatedAt = item.UpdatedAt
        };

        switch (item)
        {
            case Book book:
                dto.Author = book.Author;
                dto.Pages = book.Pages;
                dto.Isbn = book.Isbn;
                break;
            case Game game:
                dto.Platform = game.Platform;
                dto.Developer = game.Developer;
                dto.Publisher = game.Publisher;
                dto.HoursPlayed = game.HoursPlayed;
                break;
            case Movie movie:
                dto.Director = movie.Director;
                dto.DurationMinutes = movie.DurationMinutes;
                dto.ReleaseYear = movie.ReleaseYear;
                break;
        }

        return dto;
    }
}
