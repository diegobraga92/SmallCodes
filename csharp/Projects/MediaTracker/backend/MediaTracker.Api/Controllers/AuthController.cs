using Microsoft.AspNetCore.Mvc;
using MediaTracker.Api.DTOs;
using MediaTracker.Api.Services;

namespace MediaTracker.Api.Controllers;

/*
 * Controllers handle HTTP concerns — routing, request/response formatting, status codes.
 * They should be "thin" — no business logic, just orchestration.
 *
 * [ApiController] enables automatic model validation (returns 400 if DTO validation fails),
 * automatic 400 responses for invalid data, and other API-specific behaviors.
 *
 * [Route("api/[controller]")] maps to "api/auth" — [controller] is a placeholder that
 * gets replaced with the class name minus "Controller" suffix.
 *
 * Note: AuthController does NOT have [Authorize] because login and register must be
 * accessible without authentication. The individual endpoints are public by default.
 */
[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    /*
     * Constructor injection — the IAuthService is provided by the DI container.
     * The service is registered in Program.cs with AddScoped, meaning a new instance
     * is created per HTTP request.
     *
     * The field is readonly because it should never be reassigned after construction.
     * This is a best practice for injected dependencies.
     */
    private readonly IAuthService _authService;

    public AuthController(IAuthService authService)
    {
        _authService = authService;
    }

    /*
     * POST /api/auth/register
     *
     * [FromBody] tells ASP.NET Core to deserialize the request body JSON into a RegisterDto.
     * The [Required] and [EmailAddress] attributes on RegisterDto are validated automatically.
     *
     * CreatedAtAction returns HTTP 201 Created with a Location header pointing to... well,
     * there's no "get user by ID" endpoint, so we use nameof(Register) as a convention.
     * In a real API, you'd return a proper resource URL.
     *
     * The try/catch pattern here converts service-layer exceptions into HTTP responses.
     * ApplicationException → 400 Bad Request (user error, like duplicate email).
     */
    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterDto registerDto)
    {
        try
        {
            var response = await _authService.RegisterAsync(registerDto);
            return CreatedAtAction(nameof(Register), new { id = response.UserId }, response);
        }
        catch (ApplicationException ex)
        {
            return BadRequest(new { message = ex.Message });
        }
    }

    /*
     * POST /api/auth/login
     *
     * UnauthorizedAccessException → 401 Unauthorized (invalid credentials).
     * Note: We return 401, not 404, even if the user doesn't exist. This is intentional —
     * saying "user not found" would let attackers enumerate valid email addresses.
     * "Invalid email or password" is deliberately vague.
     */
    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginDto loginDto)
    {
        try
        {
            var response = await _authService.LoginAsync(loginDto);
            return Ok(response);
        }
        catch (UnauthorizedAccessException ex)
        {
            return Unauthorized(new { message = ex.Message });
        }
    }
}
