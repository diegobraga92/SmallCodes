using Microsoft.EntityFrameworkCore;
using MediaTracker.Api.Data;
using MediaTracker.Api.DTOs;
using MediaTracker.Api.Models;

namespace MediaTracker.Api.Services;

/*
 * StatsService computes aggregate statistics for a user's media collection.
 * It demonstrates several EF Core aggregate methods: CountAsync, AnyAsync, AverageAsync.
 *
 * Performance note: This service makes 10 separate database queries (one per CountAsync call).
 * For a small app this is fine, but for large datasets you'd want a single query using
 * GROUP BY or a raw SQL query for efficiency.
 */
public class StatsService : IStatsService
{
    private readonly AppDbContext _context;

    public StatsService(AppDbContext context)
    {
        _context = context;
    }

    public async Task<StatsDto> GetStatsAsync(string userId)
    {
        /*
         * Start with a filtered query — only the current user's items.
         * This query is reused (via deferred execution) for each CountAsync call.
         * Each CountAsync sends a separate SQL query like:
         *   SELECT COUNT(*) FROM "MediaItems" WHERE "UserId" = @userId
         *
         * Tradeoff: 10 separate queries. A more efficient approach would be a single
         * query with GROUP BY, but this is simpler and more readable.
         */
        var query = _context.MediaItems.Where(m => m.UserId == userId);

        var totalItems = await query.CountAsync();
        var totalBooks = await query.CountAsync(m => m.MediaType == MediaType.Book);
        var totalGames = await query.CountAsync(m => m.MediaType == MediaType.Game);
        var totalMovies = await query.CountAsync(m => m.MediaType == MediaType.Movie);
        var notStarted = await query.CountAsync(m => m.Status == MediaStatus.NotStarted);
        var inProgress = await query.CountAsync(m => m.Status == MediaStatus.InProgress);
        var completed = await query.CountAsync(m => m.Status == MediaStatus.Completed);
        var onHold = await query.CountAsync(m => m.Status == MediaStatus.OnHold);
        var dropped = await query.CountAsync(m => m.Status == MediaStatus.Dropped);

        /*
         * Average rating — only computed if at least one item has a rating.
         * AnyAsync checks if there are any items with ratings.
         * AverageAsync computes the average of the rating values.
         *
         * The null-forgiving operator (m.Rating!.Value) is safe here because we
         * already checked AnyAsync(m => m.Rating.HasValue).
         */
        double? averageRating = null;
        if (await query.AnyAsync(m => m.Rating.HasValue))
        {
            averageRating = Math.Round(
                await query.Where(m => m.Rating.HasValue).AverageAsync(m => m.Rating!.Value), 1);
        }

        return new StatsDto
        {
            TotalItems = totalItems,
            TotalBooks = totalBooks,
            TotalGames = totalGames,
            TotalMovies = totalMovies,
            NotStarted = notStarted,
            InProgress = inProgress,
            Completed = completed,
            OnHold = onHold,
            Dropped = dropped,
            AverageRating = averageRating
        };
    }
}
