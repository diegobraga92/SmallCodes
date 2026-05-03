using MediaTracker.Api.DTOs;

namespace MediaTracker.Api.Services;

/*
 * Interfaces define a contract — any class that implements IAuthService MUST
 * provide RegisterAsync and LoginAsync methods with these exact signatures.
 *
 * Why use interfaces?
 * 1. DEPENDENCY INVERSION: Controllers depend on abstractions (interfaces), not
 *    concrete implementations. This makes it easy to swap implementations (e.g.,
 *    for testing, you can create a mock IAuthService).
 * 2. TESTABILITY: You can unit-test controllers with mock services.
 * 3. DECOUPLING: Changes to the implementation don't affect the controller.
 *
 * This is the "I" in SOLID principles — Interface Segregation.
 * Each interface should be focused on a specific responsibility.
 */
public interface IAuthService
{
    Task<AuthResponseDto> RegisterAsync(RegisterDto registerDto);
    Task<AuthResponseDto> LoginAsync(LoginDto loginDto);
}
