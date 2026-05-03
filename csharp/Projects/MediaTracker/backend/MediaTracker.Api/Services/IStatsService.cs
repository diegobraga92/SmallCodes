using MediaTracker.Api.DTOs;

namespace MediaTracker.Api.Services;

/*
 * The simplest interface in the project — a single method.
 * This is a good example of the Interface Segregation Principle:
 * a focused interface with one responsibility.
 */
public interface IStatsService
{
    Task<StatsDto> GetStatsAsync(string userId);
}
