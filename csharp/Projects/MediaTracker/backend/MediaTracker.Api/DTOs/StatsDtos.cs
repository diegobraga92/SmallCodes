namespace MediaTracker.Api.DTOs;

/*
 * StatsDto is a read-only response DTO — it's only sent from server to client.
 * There's no corresponding "CreateStatsDto" because stats are computed, not created.
 *
 * This is a good example of the CQRS (Command Query Responsibility Segregation)
 * principle at a small scale: commands (create, update, delete) use different DTOs
 * than queries (get stats). They have different shapes and different validation rules.
 */
public class StatsDto
{
    public int TotalItems { get; set; }
    public int TotalBooks { get; set; }
    public int TotalGames { get; set; }
    public int TotalMovies { get; set; }
    public int NotStarted { get; set; }
    public int InProgress { get; set; }
    public int Completed { get; set; }
    public int OnHold { get; set; }
    public int Dropped { get; set; }

    /*
     * double? (nullable double) because if no items have ratings, the average
     * is undefined (null), not 0. Returning 0 would be misleading — it would
     * look like all items have a 0 rating.
     */
    public double? AverageRating { get; set; }
}
