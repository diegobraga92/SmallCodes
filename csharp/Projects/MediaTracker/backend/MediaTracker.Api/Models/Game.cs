using System.ComponentModel.DataAnnotations;

namespace MediaTracker.Api.Models;

/*
 * Game extends MediaItem with game-specific properties. Same TPH inheritance
 * pattern as Book and Movie — all share the MediaItems table.
 *
 * Note: HoursPlayed is an int? (nullable int). In a real gaming context, you might
 * want more precision (e.g., 12.5 hours), but int is simpler for this educational
 * project. The tradeoff is loss of precision.
 */
public class Game : MediaItem
{
    [MaxLength(100)]
    public string? Platform { get; set; }

    [MaxLength(200)]
    public string? Developer { get; set; }

    [MaxLength(200)]
    public string? Publisher { get; set; }

    public int? HoursPlayed { get; set; }
}
