using System.Security.Claims;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using MediaTracker.Api.DTOs;
using MediaTracker.Api.Models;
using MediaTracker.Api.Services;

namespace MediaTracker.Api.Controllers;

/*
 * [Authorize] at the class level means ALL endpoints in this controller require
 * a valid JWT token. If the token is missing or invalid, the client gets a 401
 * Unauthorized response before the action even runs.
 *
 * This is more secure than putting [Authorize] on each individual method — you
 * can't forget to add it to a new endpoint.
 */
[ApiController]
[Route("api/[controller]")]
[Authorize]
public class MediaController : ControllerBase
{
    private readonly IMediaService _mediaService;

    public MediaController(IMediaService mediaService)
    {
        _mediaService = mediaService;
    }

    /*
     * Extracts the user ID from the JWT token's claims.
     *
     * When a user authenticates, the JWT contains claims — key-value pairs of
     * information about the user. ClaimTypes.NameIdentifier stores the user's
     * ID (from AspNetUsers.Id). This is set in AuthService.GenerateJwtTokenAsync().
     *
     * This is the KEY security pattern: the user ID comes from the TOKEN, not
     * from the request body. A malicious client cannot impersonate another user
     * by sending a different UserId in the request.
     */
    private string GetUserId() =>
        User.FindFirstValue(ClaimTypes.NameIdentifier) ?? string.Empty;

    /*
     * GET /api/media?type=Book&search=harry&sortBy=title&sortOrder=asc
     *
     * [FromQuery] binds query string parameters to method parameters.
     * All parameters are optional (nullable) — the service handles defaults.
     *
     * Returns 200 OK with the list of media items (empty array if none).
     */
    [HttpGet]
    public async Task<IActionResult> GetAll(
        [FromQuery] MediaType? type = null,
        [FromQuery] string? search = null,
        [FromQuery] string? sortBy = null,
        [FromQuery] string? sortOrder = null)
    {
        var items = await _mediaService.GetAllAsync(GetUserId(), type, search, sortBy, sortOrder);
        return Ok(items);
    }

    /*
     * GET /api/media/{id}
     *
     * {id:guid} is a route constraint — it ensures the parameter is a valid GUID.
     * If the route doesn't match (e.g., "abc" instead of a GUID), ASP.NET Core
     * returns 404 before the action runs.
     *
     * Returns 404 with a message if the item doesn't exist OR belongs to another user.
     * We don't distinguish between "not found" and "not yours" for security reasons.
     */
    [HttpGet("{id:guid}")]
    public async Task<IActionResult> GetById(Guid id)
    {
        var item = await _mediaService.GetByIdAsync(id, GetUserId());
        if (item == null)
            return NotFound(new { message = "Media item not found." });

        return Ok(item);
    }

    /*
     * POST /api/media
     *
     * Returns 201 Created with the newly created item and a Location header
     * pointing to GetById (e.g., Location: /api/media/guid-here).
     * This follows REST conventions for resource creation.
     */
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateMediaItemDto dto)
    {
        var item = await _mediaService.CreateAsync(dto, GetUserId());
        return CreatedAtAction(nameof(GetById), new { id = item.Id }, item);
    }

    /*
     * PUT /api/media/{id}
     *
     * PUT typically means "replace the entire resource." However, our UpdateMediaItemDto
     * has all optional fields, making this behave more like PATCH (partial update).
     * In a strict REST API, we'd use PATCH for partial updates, but PUT is simpler
     * for this educational project.
     */
    [HttpPut("{id:guid}")]
    public async Task<IActionResult> Update(Guid id, [FromBody] UpdateMediaItemDto dto)
    {
        var item = await _mediaService.UpdateAsync(id, dto, GetUserId());
        if (item == null)
            return NotFound(new { message = "Media item not found." });

        return Ok(item);
    }

    /*
     * DELETE /api/media/{id}
     *
     * Returns 204 No Content on success — no body needed, the resource is gone.
     * Returns 404 if the item doesn't exist or doesn't belong to the user.
     */
    [HttpDelete("{id:guid}")]
    public async Task<IActionResult> Delete(Guid id)
    {
        var deleted = await _mediaService.DeleteAsync(id, GetUserId());
        if (!deleted)
            return NotFound(new { message = "Media item not found." });

        return NoContent();
    }
}
