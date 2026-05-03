using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.AspNetCore.Identity;
using Microsoft.IdentityModel.Tokens;
using MediaTracker.Api.DTOs;

namespace MediaTracker.Api.Services;

/*
 * AuthService handles user registration and login. It uses ASP.NET Core Identity
 * for user management and JWT for token generation.
 *
 * Identity handles password hashing automatically (using PBKDF2 by default).
 * We never store or even see the plaintext password — Identity's UserManager
 * takes care of hashing and verification.
 */
public class AuthService : IAuthService
{
    /*
     * UserManager<IdentityUser> is provided by ASP.NET Core Identity.
     * It provides methods for creating users, finding users, checking passwords, etc.
     * All the complex security stuff (password hashing, salting, account lockout)
     * is handled by Identity internally.
     */
    private readonly UserManager<IdentityUser> _userManager;
    private readonly IConfiguration _configuration;

    public AuthService(UserManager<IdentityUser> userManager, IConfiguration configuration)
    {
        _userManager = userManager;
        _configuration = configuration;
    }

    public async Task<AuthResponseDto> RegisterAsync(RegisterDto registerDto)
    {
        /*
         * IdentityUser is the built-in user entity from ASP.NET Core Identity.
         * It has properties like UserName, Email, Id, PasswordHash (auto-managed).
         * We create a new instance and let Identity handle the rest.
         */
        var user = new IdentityUser
        {
            UserName = registerDto.Username,
            Email = registerDto.Email
        };

        /*
         * CreateAsync hashes the password and saves the user to the AspNetUsers table.
         * The password is NEVER stored in plaintext — Identity uses PBKDF2 with a
         * random salt by default.
         *
         * If registration fails (e.g., duplicate email, password too weak), the
         * result.Errors will contain the reasons.
         */
        var result = await _userManager.CreateAsync(user, registerDto.Password);

        if (!result.Succeeded)
        {
            var errors = string.Join(", ", result.Errors.Select(e => e.Description));
            throw new ApplicationException($"Registration failed: {errors}");
        }

        return await GenerateAuthResponseAsync(user);
    }

    public async Task<AuthResponseDto> LoginAsync(LoginDto loginDto)
    {
        /*
         * FindByEmailAsync looks up the user by email.
         * CheckPasswordAsync verifies the password against the stored hash.
         *
         * We use a single error message ("Invalid email or password") regardless
         * of whether the email exists or the password is wrong. This prevents
         * attackers from enumerating valid email addresses.
         */
        var user = await _userManager.FindByEmailAsync(loginDto.Email);

        if (user == null || !await _userManager.CheckPasswordAsync(user, loginDto.Password))
        {
            throw new UnauthorizedAccessException("Invalid email or password.");
        }

        return await GenerateAuthResponseAsync(user);
    }

    private async Task<AuthResponseDto> GenerateAuthResponseAsync(IdentityUser user)
    {
        var token = await GenerateJwtTokenAsync(user);

        return new AuthResponseDto
        {
            Token = token,
            UserId = user.Id,
            Email = user.Email ?? string.Empty,
            Username = user.UserName ?? string.Empty
        };
    }

    /*
     * JWT (JSON Web Token) generation.
     *
     * A JWT is a self-contained token that consists of three parts:
     * 1. HEADER: Algorithm info (HMAC-SHA256 in our case)
     * 2. PAYLOAD: Claims (user ID, email, roles, etc.)
     * 3. SIGNATURE: Cryptographic signature to verify the token hasn't been tampered with
     *
     * The token is signed with a secret key (SymmetricSecurityKey) using HMAC-SHA256.
     * The server can verify the token without a database lookup because it has the
     * secret key. This is what makes JWT "stateless."
     *
     * Tradeoff: JWTs can't be revoked before expiry. If a token is compromised,
     * it's valid until it expires. For this educational project, 7-day expiry is
     * acceptable. Production apps often use short-lived tokens (15 min) with
     * refresh tokens for revocation capability.
     */
    private async Task<string> GenerateJwtTokenAsync(IdentityUser user)
    {
        var jwtSettings = _configuration.GetSection("Jwt");
        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(jwtSettings["Key"] ?? throw new InvalidOperationException("JWT Key not configured")));

        /*
         * Claims are key-value pairs embedded in the JWT payload.
         * When the client sends this token back, the server reads these claims
         * to identify the user without querying the database.
         *
         * ClaimTypes.NameIdentifier stores the user ID — this is what
         * MediaController.GetUserId() reads from the token.
         */
        var claims = new List<Claim>
        {
            new(ClaimTypes.NameIdentifier, user.Id),
            new(ClaimTypes.Email, user.Email ?? string.Empty),
            new(ClaimTypes.Name, user.UserName ?? string.Empty)
        };

        /*
         * If the user has roles, add them as claims. This allows role-based
         * authorization via the [Authorize(Roles = "Admin")] attribute.
         * Currently no roles are assigned, but the infrastructure is in place.
         */
        var roles = await _userManager.GetRolesAsync(user);
        claims.AddRange(roles.Select(role => new Claim(ClaimTypes.Role, role)));

        var expirationDays = jwtSettings.GetValue<int>("ExpirationDays", 7);

        var token = new JwtSecurityToken(
            issuer: jwtSettings["Issuer"],      // Who created the token
            audience: jwtSettings["Audience"],   // Who the token is intended for
            claims: claims,
            expires: DateTime.UtcNow.AddDays(expirationDays),  // Token expiry
            signingCredentials: new SigningCredentials(key, SecurityAlgorithms.HmacSha256)
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
