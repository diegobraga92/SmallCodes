using System.ComponentModel.DataAnnotations;

namespace MediaTracker.Api.DTOs;

/*
 * DTO stands for Data Transfer Object. These are simple objects that carry data
 * between the client and the API. They are separate from the domain models
 * (like IdentityUser) for several important reasons:
 *
 * 1. SECURITY: We never expose internal user data (like password hashes) to the client.
 * 2. API CONTRACT: DTOs define exactly what the API accepts and returns. Changes to
 *    internal models don't automatically change the API surface.
 * 3. VALIDATION: Data annotations on DTOs provide automatic request validation via
 *    ASP.NET Core's model binding. If validation fails, the client gets a 400 response
 *    with details before the controller action even runs.
 *
 * Tradeoff: DTOs create duplication — we define similar fields in multiple places.
 * This is intentional and considered a best practice for API design.
 */

/*
 * RegisterDto defines what the client must send to create a new account.
 * The [Required], [EmailAddress], [MinLength], [MaxLength] attributes are
 * validation rules that ASP.NET Core checks automatically.
 */
public class RegisterDto
{
    [Required]
    [EmailAddress]  // Validates that the string is a valid email format
    public string Email { get; set; } = string.Empty;

    [Required]
    [MinLength(6)]  // Minimum password length (Identity also has its own password policy)
    public string Password { get; set; } = string.Empty;

    [Required]
    [MinLength(3)]
    [MaxLength(50)]
    public string Username { get; set; } = string.Empty;
}

public class LoginDto
{
    [Required]
    public string Email { get; set; } = string.Empty;

    [Required]
    public string Password { get; set; } = string.Empty;
}

/*
 * AuthResponseDto is what the server returns after successful login or registration.
 * Note: We NEVER return the password — only the JWT token and user identifiers.
 * The token is what the client uses to authenticate subsequent requests.
 */
public class AuthResponseDto
{
    /*
     * JWT token string. The client stores this (in localStorage) and sends it
     * with every authenticated request via the Authorization header.
     * See frontend/src/services/api.ts for how this is attached.
     */
    public string Token { get; set; } = string.Empty;

    public string UserId { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string Username { get; set; } = string.Empty;
}
