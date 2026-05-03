using System.ComponentModel.DataAnnotations;

namespace MediaTracker.Api.Models;

/*
 * Book extends MediaItem, inheriting all common properties (Id, Title, Status, etc.)
 * and adding book-specific fields. This is called "inheritance" — Book IS-A MediaItem.
 *
 * In the database (TPH strategy), these properties are stored as nullable columns
 * in the MediaItems table. They'll be NULL for rows that are Games or Movies.
 *
 * Tradeoff: We can't enforce "Author is required for books" at the database level
 * because the column is shared across all types. This validation must happen in
 * application code (e.g., in the service layer or via a custom validation attribute).
 */
public class Book : MediaItem
{
    [MaxLength(200)]
    public string? Author { get; set; }

    public int? Pages { get; set; }

    [MaxLength(20)]
    public string? Isbn { get; set; }
}
