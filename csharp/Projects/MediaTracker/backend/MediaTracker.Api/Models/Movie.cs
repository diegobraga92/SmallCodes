using System.ComponentModel.DataAnnotations;

namespace MediaTracker.Api.Models;

/*
 * Movie extends MediaItem with movie-specific properties. Same TPH inheritance
 * pattern as Book and Game.
 *
 * ReleaseYear is stored as a standalone int rather than using DateTime. Why?
 * A movie's release year is a simple number — we don't need the day or month.
 * Using DateTime would imply precision we don't have (most movies just have a year)
 * and would complicate input forms. This is a good example of choosing the right
 * data type for the domain, not just the most "powerful" one.
 */
public class Movie : MediaItem
{
    [MaxLength(200)]
    public string? Director { get; set; }

    public int? DurationMinutes { get; set; }

    public int? ReleaseYear { get; set; }
}
