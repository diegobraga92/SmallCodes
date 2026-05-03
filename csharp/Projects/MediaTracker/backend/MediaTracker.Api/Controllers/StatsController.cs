using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using MediaTracker.Api.Services;

namespace MediaTracker.Api.Controllers;

/*
 * StatsController demonstrates the simplest possible controller pattern:
 * one endpoint, one service call, one response. It's a good example of
 * the "thin controller" principle — the controller does almost nothing
 * except delegate to the service.
 */
[ApiController]
[Route("api/[controller]")]
[Authorize]
public class StatsController : ControllerBase
{
    private readonly IStatsService _statsService;

    public StatsController(IStatsService statsService)
    {
        _statsService = statsService;
    }

    /*
     * Same GetUserId pattern as MediaController — extracts user ID from JWT claims.
     * This is duplicated across controllers. In a larger project, you'd extract this
     * into a base class or a custom attribute to avoid repetition.
     */
    private string GetUserId() =>
        User.FindFirstValue(ClaimTypes.NameIdentifier) ?? string.Empty;

    /*
     * GET /api/stats
     *
     * Returns computed statistics for the authenticated user.
     * No parameters needed — the user ID is extracted from the token.
     */
    [HttpGet]
    public async Task<IActionResult> GetStats()
    {
        var stats = await _statsService.GetStatsAsync(GetUserId());
        return Ok(stats);
    }
}
