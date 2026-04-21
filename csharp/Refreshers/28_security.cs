/*
    C# SECURITY
    File: 28_security.cs
    
    Comprehensive guide to security in C# and .NET applications.
    Covers authentication, authorization, data protection, cryptography,
    secure coding practices, web security, network security, security testing,
    and real-world security implementation patterns.
*/

using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Security.Claims;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.Net.Security;
using System.IO;
using Microsoft.AspNetCore.Cryptography.KeyDerivation;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.Extensions.DependencyInjection;

namespace CSharpRefresher.Security
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== C# Security ===\n");
            
            DemonstrateSecurityFundamentals();
            DemonstrateAuthenticationAndAuthorization();
            DemonstrateDataProtection();
            DemonstrateSecureCodingPractices();
            DemonstrateCryptography();
            DemonstrateWebSecurity();
            DemonstrateNetworkSecurity();
            DemonstrateSecurityTesting();
            DemonstrateRealWorldScenarios();
            
            Console.WriteLine("\n=== Complete ===");
        }
        
        static void DemonstrateSecurityFundamentals()
        {
            Console.WriteLine("=== 1. Security Fundamentals ===\n");
            
            // 1. CIA Triad
            Console.WriteLine("1. CIA Triad:");
            Console.WriteLine("""
                • Confidentiality: Protecting data from unauthorized access
                  - Encryption, access controls, data masking
                  
                • Integrity: Ensuring data is not tampered with
                  - Hash functions, digital signatures, checksums
                  
                • Availability: Ensuring systems are accessible when needed
                  - Redundancy, load balancing, DDoS protection
                  
                Additional principles:
                • Authentication: Verifying identity
                • Authorization: Determining access rights
                • Non-repudiation: Preventing denial of actions
                • Auditability: Tracking security events
                """);
            
            // 2. Security threats and vulnerabilities
            Console.WriteLine("\n2. Common Security Threats:");
            Console.WriteLine("""
                OWASP Top 10 (2021):
                1. Broken Access Control
                2. Cryptographic Failures
                3. Injection (SQL, NoSQL, Command, etc.)
                4. Insecure Design
                5. Security Misconfiguration
                6. Vulnerable and Outdated Components
                7. Identification and Authentication Failures
                8. Software and Data Integrity Failures
                9. Security Logging and Monitoring Failures
                10. Server-Side Request Forgery (SSRF)
                
                Additional .NET-specific threats:
                • Deserialization vulnerabilities
                • XML External Entity (XXE) attacks
                • Path traversal attacks
                • Insecure random number generation
                • Information disclosure through exceptions
                • Thread safety issues in security contexts
                """);
            
            // 3. Defense in depth
            Console.WriteLine("\n3. Defense in Depth:");
            Console.WriteLine("""
                Multiple layers of security:
                
                Layer 1: Physical Security
                • Data center access controls
                • Hardware security modules (HSM)
                
                Layer 2: Network Security
                • Firewalls, VPNs, network segmentation
                • DDoS protection, intrusion detection
                
                Layer 3: Host Security
                • OS hardening, patch management
                • Antivirus, host-based firewalls
                
                Layer 4: Application Security
                • Secure coding practices
                • Input validation, output encoding
                • Authentication, authorization
                
                Layer 5: Data Security
                • Encryption at rest and in transit
                • Data masking, tokenization
                
                Layer 6: Policies and Procedures
                • Security policies, training
                • Incident response plans
                
                Principle of least privilege:
                • Users/processes have minimum necessary permissions
                • Run services with minimal privileges
                • Use separate accounts for different purposes
                """);
            
            // 4. Security by design
            Console.WriteLine("\n4. Security by Design:");
            Console.WriteLine("""
                Integrating security throughout SDLC:
                
                Requirements Phase:
                • Define security requirements
                • Identify compliance needs (GDPR, HIPAA, PCI-DSS)
                • Threat modeling
                
                Design Phase:
                • Security architecture review
                • Secure design patterns
                • Cryptography decisions
                
                Implementation Phase:
                • Secure coding guidelines
                • Code reviews with security focus
                • Static analysis (SAST)
                
                Testing Phase:
                • Dynamic analysis (DAST)
                • Penetration testing
                • Security scanning
                
                Deployment Phase:
                • Secure configuration
                • Secrets management
                • Infrastructure as code security
                
                Operations Phase:
                • Security monitoring
                • Incident response
                • Patch management
                
                Microsoft Security Development Lifecycle (SDL):
                • Training
                • Requirements
                • Design
                • Implementation
                • Verification
                • Release
                • Response
                """);
        }
        
        static void DemonstrateAuthenticationAndAuthorization()
        {
            Console.WriteLine("\n=== 2. Authentication and Authorization ===\n");
            
            // 1. Authentication fundamentals
            Console.WriteLine("1. Authentication Fundamentals:");
            Console.WriteLine("""
                Authentication factors:
                • Something you know (password, PIN)
                • Something you have (token, smart card, phone)
                • Something you are (biometrics)
                • Somewhere you are (location)
                • Something you do (behavioral patterns)
                
                Multi-factor authentication (MFA):
                // Example: Require 2+ factors
                if (passwordCorrect && tokenValid && biometricMatch)
                {
                    // Grant access
                }
                
                Single Sign-On (SSO):
                // Central authentication service
                // Protocols: SAML, OAuth 2.0, OpenID Connect
                """);
            
            // 2. ASP.NET Core Identity
            Console.WriteLine("\n2. ASP.NET Core Identity:");
            Console.WriteLine("""
                Setup:
                services.AddIdentity<ApplicationUser, IdentityRole>(options =>
                {
                    // Password settings
                    options.Password.RequireDigit = true;
                    options.Password.RequiredLength = 8;
                    options.Password.RequireNonAlphanumeric = true;
                    options.Password.RequireUppercase = true;
                    options.Password.RequireLowercase = true;
                    options.Password.RequiredUniqueChars = 6;
                    
                    // Lockout settings
                    options.Lockout.DefaultLockoutTimeSpan = TimeSpan.FromMinutes(5);
                    options.Lockout.MaxFailedAccessAttempts = 5;
                    options.Lockout.AllowedForNewUsers = true;
                    
                    // User settings
                    options.User.RequireUniqueEmail = true;
                    options.SignIn.RequireConfirmedEmail = true;
                    options.SignIn.RequireConfirmedPhoneNumber = false;
                })
                .AddEntityFrameworkStores<ApplicationDbContext>()
                .AddDefaultTokenProviders();
                
                User registration:
                public async Task<IActionResult> Register(RegisterViewModel model)
                {
                    var user = new ApplicationUser 
                    { 
                        UserName = model.Email, 
                        Email = model.Email 
                    };
                    
                    var result = await _userManager.CreateAsync(user, model.Password);
                    
                    if (result.Succeeded)
                    {
                        // Generate email confirmation token
                        var token = await _userManager.GenerateEmailConfirmationTokenAsync(user);
                        var callbackUrl = Url.Action("ConfirmEmail", "Account", 
                            new { userId = user.Id, token = token }, 
                            protocol: HttpContext.Request.Scheme);
                        
                        // Send email
                        await _emailSender.SendEmailAsync(model.Email, "Confirm your email",
                            $"Please confirm your account by <a href='{callbackUrl}'>clicking here</a>.");
                        
                        return RedirectToAction("RegisterConfirmation");
                    }
                    
                    // Handle errors
                    foreach (var error in result.Errors)
                    {
                        ModelState.AddModelError(string.Empty, error.Description);
                    }
                    
                    return View(model);
                }
                
                Password hashing:
                // Identity uses PBKDF2 with HMAC-SHA256, 128-bit salt, 256-bit subkey, 10,000 iterations
                var hashedPassword = _userManager.PasswordHasher.HashPassword(user, password);
                var result = _userManager.PasswordHasher.VerifyHashedPassword(user, hashedPassword, password);
                """);
            
            // 3. OAuth 2.0 and OpenID Connect
            Console.WriteLine("\n3. OAuth 2.0 and OpenID Connect:");
            Console.WriteLine("""
                OAuth 2.0 flows:
                • Authorization Code: Web apps (with PKCE for mobile/native)
                • Implicit: Legacy (not recommended)
                • Client Credentials: Machine-to-machine
                • Resource Owner Password Credentials: Legacy (not recommended)
                • Device Code: Devices with limited input
                
                OpenID Connect (OIDC):
                // Identity layer on top of OAuth 2.0
                services.AddAuthentication(options =>
                {
                    options.DefaultScheme = CookieAuthenticationDefaults.AuthenticationScheme;
                    options.DefaultChallengeScheme = OpenIdConnectDefaults.AuthenticationScheme;
                })
                .AddCookie()
                .AddOpenIdConnect(options =>
                {
                    options.Authority = "https://login.microsoftonline.com/tenant-id/v2.0";
                    options.ClientId = "client-id";
                    options.ClientSecret = "client-secret";
                    options.ResponseType = "code";
                    options.SaveTokens = true;
                    options.Scope.Add("openid");
                    options.Scope.Add("profile");
                    options.Scope.Add("email");
                    options.Scope.Add("api://api-id/access_as_user");
                    options.TokenValidationParameters = new TokenValidationParameters
                    {
                        NameClaimType = "name",
                        RoleClaimType = "roles"
                    };
                });
                
                JWT (JSON Web Tokens):
                // Creating JWT
                var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("super-secret-key"));
                var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);
                
                var claims = new[]
                {
                    new Claim(JwtRegisteredClaimNames.Sub, "user-id"),
                    new Claim(JwtRegisteredClaimNames.Email, "user@example.com"),
                    new Claim(ClaimTypes.Role, "Admin"),
                    new Claim("custom-claim", "custom-value")
                };
                
                var token = new JwtSecurityToken(
                    issuer: "your-issuer",
                    audience: "your-audience",
                    claims: claims,
                    expires: DateTime.Now.AddHours(1),
                    signingCredentials: credentials);
                
                var tokenString = new JwtSecurityTokenHandler().WriteToken(token);
                
                // Validating JWT
                services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
                    .AddJwtBearer(options =>
                    {
                        options.TokenValidationParameters = new TokenValidationParameters
                        {
                            ValidateIssuer = true,
                            ValidateAudience = true,
                            ValidateLifetime = true,
                            ValidateIssuerSigningKey = true,
                            ValidIssuer = "your-issuer",
                            ValidAudience = "your-audience",
                            IssuerSigningKey = new SymmetricSecurityKey(
                                Encoding.UTF8.GetBytes("super-secret-key"))
                        };
                    });
                """);
            
            // 4. Authorization
            Console.WriteLine("\n4. Authorization:");
            Console.WriteLine("""
                Role-based authorization:
                [Authorize(Roles = "Admin,Manager")]
                public IActionResult AdminOnly()
                {
                    return View();
                }
                
                // Multiple roles
                if (User.IsInRole("Admin") || User.IsInRole("Manager"))
                {
                    // Allow access
                }
                
                Policy-based authorization:
                services.AddAuthorization(options =>
                {
                    options.AddPolicy("RequireAdminRole", 
                        policy => policy.RequireRole("Admin"));
                    
                    options.AddPolicy("Over18", 
                        policy => policy.RequireClaim(ClaimTypes.DateOfBirth));
                    
                    options.AddPolicy("CanEditArticle",
                        policy => policy.Requirements.Add(new CanEditArticleRequirement()));
                    
                    options.AddPolicy("MinimumAge",
                        policy => policy.Requirements.Add(new MinimumAgeRequirement(18)));
                });
                
                [Authorize(Policy = "Over18")]
                public IActionResult AdultContent()
                {
                    return View();
                }
                
                Resource-based authorization:
                public class DocumentAuthorizationHandler : 
                    AuthorizationHandler<SameAuthorRequirement, Document>
                {
                    protected override Task HandleRequirementAsync(
                        AuthorizationHandlerContext context,
                        SameAuthorRequirement requirement,
                        Document resource)
                    {
                        if (context.User.Identity?.Name == resource.Author)
                        {
                            context.Succeed(requirement);
                        }
                        
                        return Task.CompletedTask;
                    }
                }
                
                [Authorize]
                public async Task<IActionResult> Edit(int id)
                {
                    var document = await _documentRepository.GetAsync(id);
                    
                    if (document == null)
                        return NotFound();
                    
                    var authResult = await _authorizationService.AuthorizeAsync(
                        User, document, "EditPolicy");
                    
                    if (!authResult.Succeeded)
                        return Forbid();
                    
                    return View(document);
                }
                
                Claims-based authorization:
                // Adding claims
                var claims = new List<Claim>
                {
                    new Claim(ClaimTypes.Name, "john"),
                    new Claim(ClaimTypes.Email, "john@example.com"),
                    new Claim("EmployeeId", "12345"),
                    new Claim(ClaimTypes.Role, "User"),
                    new Claim(ClaimTypes.Role, "Editor")
                };
                
                var claimsIdentity = new ClaimsIdentity(claims, "Custom");
                var principal = new ClaimsPrincipal(claimsIdentity);
                
                // Checking claims
                var email = User.FindFirst(ClaimTypes.Email)?.Value;
                var hasEmployeeId = User.HasClaim(c => c.Type == "EmployeeId");
                var isEditor = User.HasClaim(ClaimTypes.Role, "Editor");
                """);
            
            // 5. Secure session management
            Console.WriteLine("\n5. Secure Session Management:");
            Console.WriteLine("""
                ASP.NET Core session:
                services.AddSession(options =>
                {
                    options.Cookie.Name = ".App.Session";
                    options.Cookie.HttpOnly = true;
                    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
                    options.Cookie.SameSite = SameSiteMode.Strict;
                    options.IdleTimeout = TimeSpan.FromMinutes(20);
                    options.Cookie.IsEssential = true;
                });
                
                // Store sensitive data in session
                HttpContext.Session.SetString("UserId", userId);
                var userId = HttpContext.Session.GetString("UserId");
                
                Distributed session with Redis:
                services.AddStackExchangeRedisCache(options =>
                {
                    options.Configuration = "localhost:6379";
                    options.InstanceName = "SessionStore";
                });
                
                services.AddSession(options =>
                {
                    options.Cookie.HttpOnly = true;
                    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
                    options.IdleTimeout = TimeSpan.FromMinutes(30);
                });
                
                Preventing session fixation:
                // Regenerate session ID on login
                await HttpContext.SignInAsync(principal);
                
                // Or in Identity
                await _signInManager.SignInAsync(user, isPersistent: false);
                """);
        }
        
        static void DemonstrateDataProtection()
        {
            Console.WriteLine("\n=== 3. Data Protection ===\n");
            
            // 1. Data Protection API (DPAPI)
            Console.WriteLine("1. Data Protection API (DPAPI):");
            Console.WriteLine("""
                Microsoft.AspNetCore.DataProtection:
                
                Setup:
                services.AddDataProtection()
                    .PersistKeysToFileSystem(new DirectoryInfo(@"c:\keys"))
                    .ProtectKeysWithCertificate(certificate)
                    .SetApplicationName("MyApp")
                    .SetDefaultKeyLifetime(TimeSpan.FromDays(90));
                
                // Or with Azure Key Vault
                services.AddDataProtection()
                    .PersistKeysToAzureBlobStorage(connectionString, containerName, blobName)
                    .ProtectKeysWithAzureKeyVault(new Uri(keyIdentifier), credential);
                
                Usage:
                public class DataProtectionService
                {
                    private readonly IDataProtector _protector;
                    
                    public DataProtectionService(IDataProtectionProvider provider)
                    {
                        _protector = provider.CreateProtector("MyApp.Purpose");
                    }
                    
                    public string Protect(string plaintext)
                    {
                        return _protector.Protect(plaintext);
                    }
                    
                    public string Unprotect(string protectedText)
                    {
                        return _protector.Unprotect(protectedText);
                    }
                }
                
                // With time-limited protection
                var timeLimitedProtector = _protector.ToTimeLimitedDataProtector();
                var protectedData = timeLimitedProtector.Protect(
                    "sensitive data", 
                    lifetime: TimeSpan.FromHours(1));
                
                try
                {
                    var unprotectedData = timeLimitedProtector.Unprotect(protectedData);
                }
                catch (CryptographicException ex) when (ex.Message.Contains("expired"))
                {
                    // Handle expired data
                }
                
                Purpose strings:
                // Different purposes get different encryption keys
                var protector1 = provider.CreateProtector("User.Tokens");
                var protector2 = provider.CreateProtector("User.PersonalData");
                var protector3 = provider.CreateProtector("App.Configuration");
                """);
            
            // 2. Encryption at rest
            Console.WriteLine("\n2. Encryption at Rest:");
            Console.WriteLine("""
                File encryption:
                using (var aes = Aes.Create())
                {
                    aes.GenerateKey();
                    aes.GenerateIV();
                    
                    using (var encryptor = aes.CreateEncryptor())
                    using (var fsOutput = new FileStream("encrypted.bin", FileMode.Create))
                    using (var cs = new CryptoStream(fsOutput, encryptor, CryptoStreamMode.Write))
                    using (var sw = new StreamWriter(cs))
                    {
                        sw.Write("sensitive data");
                    }
                    
                    // Save key and IV securely
                    File.WriteAllText("key.bin", Convert.ToBase64String(aes.Key));
                    File.WriteAllText("iv.bin", Convert.ToBase64String(aes.IV));
                }
                
                // Decryption
                var key = Convert.FromBase64String(File.ReadAllText("key.bin"));
                var iv = Convert.FromBase64String(File.ReadAllText("iv.bin"));
                
                using (var aes = Aes.Create())
                {
                    aes.Key = key;
                    aes.IV = iv;
                    
                    using (var decryptor = aes.CreateDecryptor())
                    using (var fsInput = new FileStream("encrypted.bin", FileMode.Open))
                    using (var cs = new CryptoStream(fsInput, decryptor, CryptoStreamMode.Read))
                    using (var sr = new StreamReader(cs))
                    {
                        var plaintext = sr.ReadToEnd();
                    }
                }
                
                Database column encryption:
                // Using Always Encrypted (SQL Server)
                // Column encryption settings in connection string
                "Data Source=server;Initial Catalog=database;Integrated Security=true;Column Encryption Setting=Enabled"
                
                // Entity Framework with Always Encrypted
                modelBuilder.Entity<User>()
                    .Property(u => u.SSN)
                    .HasConversion(
                        v => v, // No conversion needed for string
                        v => v)
                    .HasColumnType("nvarchar(11)")
                    .IsUnicode(false);
                """);
            
            // 3. Secure string handling
            Console.WriteLine("\n3. Secure String Handling:");
            Console.WriteLine("""
                SecureString (legacy, Windows only):
                // Note: SecureString is being deprecated, but here's usage
                using (var secureString = new SecureString())
                {
                    foreach (char c in "password")
                    {
                        secureString.AppendChar(c);
                    }
                    
                    // Use with Windows APIs
                    var credential = new System.Net.NetworkCredential("username", secureString);
                }
                
                // Clear sensitive data from memory
                void ClearSensitiveData(byte[] data)
                {
                    CryptographicOperations.ZeroMemory(data);
                }
                
                void ClearSensitiveData(char[] data)
                {
                    Array.Clear(data, 0, data.Length);
                }
                
                // Example with password
                char[] passwordChars = null;
                try
                {
                    passwordChars = Console.ReadLine().ToCharArray();
                    // Use password...
                }
                finally
                {
                    if (passwordChars != null)
                    {
                        Array.Clear(passwordChars, 0, passwordChars.Length);
                    }
                }
                
                Span<T> for sensitive data:
                // Span allows stack allocation (no heap)
                Span<byte> sensitiveData = stackalloc byte[32];
                RandomNumberGenerator.Fill(sensitiveData);
                
                // Use sensitiveData...
                
                // Clear when done
                sensitiveData.Clear();
                """);
            
            // 4. Data masking and tokenization
            Console.WriteLine("\n4. Data Masking and Tokenization:");
            Console.WriteLine("""
                Data masking:
                public static class DataMasker
                {
                    public static string MaskCreditCard(string cardNumber)
                    {
                        if (string.IsNullOrEmpty(cardNumber) || cardNumber.Length < 12)
                            return cardNumber;
                            
                        return cardNumber.Substring(0, 6) + 
                               new string('*', cardNumber.Length - 10) + 
                               cardNumber.Substring(cardNumber.Length - 4);
                    }
                    
                    public static string MaskEmail(string email)
                    {
                        if (string.IsNullOrEmpty(email) || !email.Contains("@"))
                            return email;
                            
                        var parts = email.Split('@');
                        var username = parts[0];
                        var domain = parts[1];
                        
                        if (username.Length <= 2)
                            return new string('*', username.Length) + "@" + domain;
                        
                        return username.Substring(0, 2) + 
                               new string('*', username.Length - 2) + 
                               "@" + domain;
                    }
                    
                    public static string MaskPhoneNumber(string phone)
                    {
                        if (string.IsNullOrEmpty(phone) || phone.Length < 10)
                            return phone;
                            
                        return new string('*', phone.Length - 4) + 
                               phone.Substring(phone.Length - 4);
                    }
                }
                
                Tokenization:
                public class TokenizationService
                {
                    private readonly Dictionary<string, string> _tokenToValue = new();
                    private readonly Dictionary<string, string> _valueToToken = new();
                    private readonly RandomNumberGenerator _rng = RandomNumberGenerator.Create();
                    
                    public string Tokenize(string sensitiveValue)
                    {
                        if (_valueToToken.TryGetValue(sensitiveValue, out var token))
                            return token;
                        
                        // Generate secure random token
                        byte[] tokenBytes = new byte[32];
                        _rng.GetBytes(tokenBytes);
                        token = Convert.ToBase64String(tokenBytes)
                            .Replace("/", "_")
                            .Replace("+", "-")
                            .Replace("=", "");
                        
                        _tokenToValue[token] = sensitiveValue;
                        _valueToToken[sensitiveValue] = token;
                        
                        return token;
                    }
                    
                    public string Detokenize(string token)
                    {
                        return _tokenToValue.TryGetValue(token, out var value) 
                            ? value 
                            : null;
                    }
                    
                    public void RemoveToken(string token)
                    {
                        if (_tokenToValue.TryGetValue(token, out var value))
                        {
                            _tokenToValue.Remove(token);
                            _valueToToken.Remove(value);
                        }
                    }
                }
                """);
        }
        
        static void DemonstrateSecureCodingPractices()
        {
            Console.WriteLine("\n=== 4. Secure Coding Practices ===\n");
            
            // 1. Input validation
            Console.WriteLine("1. Input Validation:");
            Console.WriteLine("""
                Defense against injection attacks:
                
                SQL Injection prevention:
                // BAD: String concatenation
                string query = "SELECT * FROM Users WHERE Username = '" + username + "'";
                
                // GOOD: Parameterized queries
                using (var command = new SqlCommand(
                    "SELECT * FROM Users WHERE Username = @Username", connection))
                {
                    command.Parameters.AddWithValue("@Username", username);
                }
                
                // Entity Framework uses parameterized queries automatically
                var user = dbContext.Users.FirstOrDefault(u => u.Username == username);
                
                Command Injection prevention:
                // BAD
                Process.Start("cmd.exe", "/c ping " + userInput);
                
                // GOOD: Validate and sanitize
                if (Regex.IsMatch(userInput, @"^[0-9.]+$"))
                {
                    Process.Start("ping", userInput);
                }
                
                // BETTER: Use safe APIs
                var ipAddress = IPAddress.Parse(userInput);
                // Use ipAddress...
                
                HTML/JavaScript Injection (XSS):
                // In Razor, automatically encoded
                <div>@userInput</div> <!-- Auto-encoded -->
                
                // Manual encoding
                var encoded = System.Net.WebUtility.HtmlEncode(userInput);
                
                // For JavaScript
                var jsEncoded = System.Text.Encodings.Web.JavaScriptEncoder.Default.Encode(userInput);
                
                // For URLs
                var urlEncoded = System.Uri.EscapeDataString(userInput);
                
                // For attributes
                var attrEncoded = System.Text.Encodings.Web.HtmlEncoder.Default.Encode(userInput);
                
                Regular expression validation:
                public static class InputValidators
                {
                    // Email validation
                    private static readonly Regex EmailRegex = new Regex(
                        @"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                        RegexOptions.Compiled | RegexOptions.IgnoreCase);
                    
                    // Phone number (US)
                    private static readonly Regex PhoneRegex = new Regex(
                        @"^\+?1?[-.\s]?\(?[2-9][0-9]{2}\)?[-.\s]?[2-9][0-9]{2}[-.\s]?[0-9]{4}$",
                        RegexOptions.Compiled);
                    
                    // Credit card
                    private static readonly Regex CreditCardRegex = new Regex(
                        @"^[0-9]{13,19}$",
                        RegexOptions.Compiled);
                    
                    // ZIP code
                    private static readonly Regex ZipCodeRegex = new Regex(
                        @"^\d{5}(-\d{4})?$",
                        RegexOptions.Compiled);
                    
                    public static bool IsValidEmail(string email) => 
                        !string.IsNullOrEmpty(email) && EmailRegex.IsMatch(email);
                    
                    public static bool IsValidPhone(string phone) => 
                        !string.IsNullOrEmpty(phone) && PhoneRegex.IsMatch(phone);
                }
                
                Whitelist vs blacklist:
                // BAD: Blacklisting (trying to block bad characters)
                if (input.Contains("<") || input.Contains(">") || input.Contains("'") || input.Contains("\""))
                {
                    // Reject
                }
                
                // GOOD: Whitelisting (allowing only known good characters)
                if (Regex.IsMatch(input, @"^[a-zA-Z0-9\s\-\.]+$"))
                {
                    // Accept
                }
                """);
            
            // 2. Output encoding
            Console.WriteLine("\n2. Output Encoding:");
            Console.WriteLine("""
                Context-specific encoding:
                
                HTML Context:
                // Razor auto-encodes
                <p>@Model.UserInput</p>
                
                // Manual encoding
                <p>@Html.Raw("<b>Bold</b>")</p> <!-- DANGEROUS if UserInput -->
                <p>@Html.DisplayFor(m => m.UserInput)</p> <!-- Safe -->
                
                // For untrusted data
                var encoded = Microsoft.AspNetCore.Http.Extensions.UrlEncoder.Default.Encode(userInput);
                
                JavaScript Context:
                // In Razor
                <script>
                    var userData = '@JavaScriptEncoder.Default.Encode(Model.UserData)';
                </script>
                
                // Or using JsonSerializer
                <script>
                    var userData = @Json.Serialize(Model.UserData);
                </script>
                
                URL Context:
                // Building URLs
                var url = $"https://example.com/profile?name={Uri.EscapeDataString(userName)}";
                
                // In Razor
                <a href="/profile/@Uri.EscapeDataString(userName)">Profile</a>
                
                CSS Context:
                // Rarely needed, but available
                var cssEncoded = System.Text.Encodings.Web.CssEncoder.Default.Encode(userInput);
                
                // In Razor with style attribute
                <div style="color: @CssEncoder.Default.Encode(userColor)"></div>
                
                Anti-XSS Library (Microsoft):
                // Install-Package AntiXSS
                using Microsoft.Security.Application;
                
                var safeHtml = Sanitizer.GetSafeHtml(userInput);
                var safeUrl = UrlEncoder.UrlEncode(userInput);
                var safeCss = CssEncode(userInput);
                var safeJs = JavaScriptEncode(userInput);
                """);
            
            // 3. Error handling and logging
            Console.WriteLine("\n3. Error Handling and Logging:");
            Console.WriteLine("""
                Secure exception handling:
                // DON'T expose internal details
                try
                {
                    // Sensitive operation
                }
                catch (SqlException ex)
                {
                    // BAD: Logging sensitive data
                    _logger.LogError($"SQL error: {ex.Message}");
                    
                    // GOOD: Generic message
                    _logger.LogError(ex, "Database error occurred");
                    throw new ApplicationException("An error occurred processing your request");
                }
                
                // Custom exception filter
                public class SecureExceptionFilter : IExceptionFilter
                {
                    public void OnException(ExceptionContext context)
                    {
                        var exception = context.Exception;
                        
                        // Log securely
                        _logger.LogError(exception, "Unhandled exception");
                        
                        // Don't expose stack traces in production
                        if (!context.HttpContext.RequestServices
                            .GetRequiredService<IHostEnvironment>().IsDevelopment())
                        {
                            context.Result = new ObjectResult("An error occurred")
                            {
                                StatusCode = (int)HttpStatusCode.InternalServerError
                            };
                            context.ExceptionHandled = true;
                        }
                    }
                }
                
                Safe logging practices:
                public class SecureLogger
                {
                    private readonly ILogger _logger;
                    
                    public void LogUserAction(string userId, string action)
                    {
                        // Safe: No PII
                        _logger.LogInformation("User {UserId} performed {Action}", 
                            HashUserId(userId), action);
                    }
                    
                    public void LogSensitiveOperation(string operation, string data)
                    {
                        // Mask sensitive data
                        var maskedData = MaskSensitiveData(data);
                        _logger.LogInformation("Operation {Operation} with data: {Data}", 
                            operation, maskedData);
                    }
                    
                    private string HashUserId(string userId)
                    {
                        using (var sha256 = SHA256.Create())
                        {
                            var hash = sha256.ComputeHash(Encoding.UTF8.GetBytes(userId));
                            return Convert.ToBase64String(hash);
                        }
                    }
                    
                    private string MaskSensitiveData(string data)
                    {
                        // Implement masking logic
                        if (data.Length > 8)
                            return data.Substring(0, 4) + new string('*', data.Length - 8) + data.Substring(data.Length - 4);
                        return new string('*', data.Length);
                    }
                }
                
                Global error handling:
                // In Startup.Configure
                app.UseExceptionHandler("/Error");
                app.UseStatusCodePagesWithReExecute("/Error/{0}");
                
                // Error controller
                [AllowAnonymous]
                public class ErrorController : Controller
                {
                    [Route("Error/{statusCode}")]
                    public IActionResult HttpStatusCodeHandler(int statusCode)
                    {
                        var viewModel = new ErrorViewModel
                        {
                            StatusCode = statusCode,
                            Message = statusCode switch
                            {
                                404 => "Page not found",
                                403 => "Access denied",
                                500 => "Internal server error",
                                _ => "An error occurred"
                            }
                        };
                        
                        return View("Error", viewModel);
                    }
                }
                """);
            
            // 4. File and path security
            Console.WriteLine("\n4. File and Path Security:");
            Console.WriteLine("""
                Preventing path traversal:
                // BAD
                var userFile = Request.Form["file"];
                var fullPath = Path.Combine("C:\\uploads", userFile);
                // User could enter "../../../windows/system32/config/sam"
                
                // GOOD: Validate and sanitize
                public static string SafeCombine(string basePath, string userPath)
                {
                    // Get canonical paths
                    var fullPath = Path.GetFullPath(Path.Combine(basePath, userPath));
                    var baseFullPath = Path.GetFullPath(basePath);
                    
                    // Ensure the resulting path is within base directory
                    if (!fullPath.StartsWith(baseFullPath, StringComparison.OrdinalIgnoreCase))
                    {
                        throw new SecurityException("Path traversal attempt detected");
                    }
                    
                    return fullPath;
                }
                
                // Alternative: Use a whitelist
                var allowedFiles = new[] { "report.pdf", "data.csv", "image.jpg" };
                if (!allowedFiles.Contains(userFile, StringComparer.OrdinalIgnoreCase))
                {
                    throw new SecurityException("Invalid file requested");
                }
                
                Safe file uploads:
                public class FileUploadService
                {
                    private static readonly string[] AllowedExtensions = 
                        { ".jpg", ".jpeg", ".png", ".gif", ".pdf", ".doc", ".docx" };
                    private static readonly long MaxFileSize = 10 * 1024 * 1024; // 10MB
                    
                    public async Task<string> SaveUploadedFile(IFormFile file)
                    {
                        // Validate file size
                        if (file.Length > MaxFileSize)
                            throw new ArgumentException("File too large");
                        
                        // Validate extension
                        var extension = Path.GetExtension(file.FileName).ToLowerInvariant();
                        if (string.IsNullOrEmpty(extension) || !AllowedExtensions.Contains(extension))
                            throw new ArgumentException("Invalid file type");
                        
                        // Generate safe filename
                        var safeFileName = Guid.NewGuid().ToString() + extension;
                        var filePath = Path.Combine("uploads", safeFileName);
                        
                        // Save file
                        using (var stream = new FileStream(filePath, FileMode.Create))
                        {
                            await file.CopyToAsync(stream);
                        }
                        
                        return safeFileName;
                    }
                }
                
                File permissions:
                // Set secure file permissions
                public static void SetSecurePermissions(string filePath)
                {
                    var fileInfo = new FileInfo(filePath);
                    
                    // Remove inheritance and set explicit permissions
                    var fileSecurity = fileInfo.GetAccessControl();
                    fileSecurity.SetAccessRuleProtection(true, false);
                    
                    // Set specific permissions
                    var currentUser = WindowsIdentity.GetCurrent().User;
                    fileSecurity.AddAccessRule(new FileSystemAccessRule(
                        currentUser,
                        FileSystemRights.Read | FileSystemRights.Write,
                        AccessControlType.Allow));
                    
                    // Remove everyone else
                    fileSecurity.RemoveAccessRuleAll(new FileSystemAccessRule(
                        new SecurityIdentifier(WellKnownSidType.WorldSid, null),
                        FileSystemRights.FullControl,
                        AccessControlType.Allow));
                    
                    fileInfo.SetAccessControl(fileSecurity);
                }
                """);
            
            // 5. Memory safety
            Console.WriteLine("\n5. Memory Safety:");
            Console.WriteLine("""
                Buffer overflow prevention:
                // Use safe APIs
                char[] buffer = new char[100];
                
                // BAD: Could overflow
                for (int i = 0; i < userInput.Length; i++)
                {
                    buffer[i] = userInput[i]; // Potential overflow
                }
                
                // GOOD: Bounds checking
                var length = Math.Min(userInput.Length, buffer.Length);
                Array.Copy(userInput.ToCharArray(), buffer, length);
                
                // BETTER: Use Span<T>
                Span<char> bufferSpan = stackalloc char[100];
                userInput.AsSpan().CopyTo(bufferSpan);
                
                Secure random numbers:
                // BAD: System.Random is predictable
                var random = new Random();
                int badRandom = random.Next();
                
                // GOOD: Cryptographic random
                using (var rng = RandomNumberGenerator.Create())
                {
                    byte[] randomBytes = new byte[4];
                    rng.GetBytes(randomBytes);
                    int goodRandom = BitConverter.ToInt32(randomBytes, 0);
                }
                
                // Helper method for cryptographic random
                public static int GetCryptographicRandom(int minValue, int maxValue)
                {
                    if (minValue >= maxValue)
                        throw new ArgumentException("minValue must be less than maxValue");
                    
                    var range = (long)maxValue - minValue;
                    if (range > int.MaxValue)
                        throw new ArgumentException("Range too large");
                    
                    byte[] randomBytes = new byte[4];
                    RandomNumberGenerator.Fill(randomBytes);
                    
                    uint randomValue = BitConverter.ToUInt32(randomBytes, 0);
                    return (int)(randomValue % range) + minValue;
                }
                
                Secure disposal:
                public class SecureDisposable : IDisposable
                {
                    private byte[] _sensitiveData;
                    private bool _disposed = false;
                    
                    public SecureDisposable()
                    {
                        _sensitiveData = new byte[1024];
                        // Fill with sensitive data
                    }
                    
                    public void Dispose()
                    {
                        Dispose(true);
                        GC.SuppressFinalize(this);
                    }
                    
                    protected virtual void Dispose(bool disposing)
                    {
                        if (!_disposed)
                        {
                            if (disposing)
                            {
                                // Clear sensitive data
                                if (_sensitiveData != null)
                                {
                                    CryptographicOperations.ZeroMemory(_sensitiveData);
                                    _sensitiveData = null;
                                }
                            }
                            
                            _disposed = true;
                        }
                    }
                    
                    ~SecureDisposable()
                    {
                        Dispose(false);
                    }
                }
                """);
        }
        
        static void DemonstrateCryptography()
        {
            Console.WriteLine("\n=== 5. Cryptography ===\n");
            
            // 1. Hashing
            Console.WriteLine("1. Hashing:");
            Console.WriteLine("""
                Password hashing with PBKDF2:
                public static class PasswordHasher
                {
                    private const int SaltSize = 128 / 8; // 128 bits
                    private const int HashSize = 256 / 8; // 256 bits
                    private const int Iterations = 100000;
                    
                    public static string HashPassword(string password)
                    {
                        // Generate salt
                        byte[] salt = new byte[SaltSize];
                        using (var rng = RandomNumberGenerator.Create())
                        {
                            rng.GetBytes(salt);
                        }
                        
                        // Hash password
                        byte[] hash = KeyDerivation.Pbkdf2(
                            password: password,
                            salt: salt,
                            prf: KeyDerivationPrf.HMACSHA256,
                            iterationCount: Iterations,
                            numBytesRequested: HashSize);
                        
                        // Combine salt and hash
                        byte[] hashBytes = new byte[SaltSize + HashSize];
                        Array.Copy(salt, 0, hashBytes, 0, SaltSize);
                        Array.Copy(hash, 0, hashBytes, SaltSize, HashSize);
                        
                        return Convert.ToBase64String(hashBytes);
                    }
                    
                    public static bool VerifyPassword(string password, string hashedPassword)
                    {
                        // Extract bytes
                        byte[] hashBytes = Convert.FromBase64String(hashedPassword);
                        
                        // Extract salt
                        byte[] salt = new byte[SaltSize];
                        Array.Copy(hashBytes, 0, salt, 0, SaltSize);
                        
                        // Compute hash
                        byte[] hash = KeyDerivation.Pbkdf2(
                            password: password,
                            salt: salt,
                            prf: KeyDerivationPrf.HMACSHA256,
                            iterationCount: Iterations,
                            numBytesRequested: HashSize);
                        
                        // Compare
                        for (int i = 0; i < HashSize; i++)
                        {
                            if (hashBytes[i + SaltSize] != hash[i])
                                return false;
                        }
                        
                        return true;
                    }
                }
                
                File integrity checking:
                public static class FileIntegrity
                {
                    public static string ComputeFileHash(string filePath)
                    {
                        using (var sha256 = SHA256.Create())
                        using (var stream = File.OpenRead(filePath))
                        {
                            byte[] hash = sha256.ComputeHash(stream);
                            return BitConverter.ToString(hash).Replace("-", "").ToLowerInvariant();
                        }
                    }
                    
                    public static bool VerifyFileHash(string filePath, string expectedHash)
                    {
                        var actualHash = ComputeFileHash(filePath);
                        return string.Equals(actualHash, expectedHash, 
                            StringComparison.OrdinalIgnoreCase);
                    }
                }
                
                HMAC for message authentication:
                public static class MessageAuthenticator
                {
                    private static readonly byte[] Key = new byte[64]; // 512-bit key
                    
                    static MessageAuthenticator()
                    {
                        using (var rng = RandomNumberGenerator.Create())
                        {
                            rng.GetBytes(Key);
                        }
                    }
                    
                    public static string CreateHmac(string message)
                    {
                        using (var hmac = new HMACSHA256(Key))
                        {
                            byte[] hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(message));
                            return Convert.ToBase64String(hash);
                        }
                    }
                    
                    public static bool VerifyHmac(string message, string hmacToVerify)
                    {
                        var computedHmac = CreateHmac(message);
                        return CryptographicOperations.FixedTimeEquals(
                            Convert.FromBase64String(computedHmac),
                            Convert.FromBase64String(hmacToVerify));
                    }
                }
                """);
            
            // 2. Symmetric encryption
            Console.WriteLine("\n2. Symmetric Encryption:");
            Console.WriteLine("""
                AES encryption:
                public static class AesEncryption
                {
                    public static (string ciphertext, string iv) Encrypt(string plaintext, byte[] key)
                    {
                        using (var aes = Aes.Create())
                        {
                            aes.Key = key;
                            aes.GenerateIV();
                            
                            using (var encryptor = aes.CreateEncryptor())
                            using (var ms = new MemoryStream())
                            {
                                // Write IV first
                                ms.Write(aes.IV, 0, aes.IV.Length);
                                
                                // Encrypt data
                                using (var cs = new CryptoStream(ms, encryptor, CryptoStreamMode.Write))
                                using (var sw = new StreamWriter(cs))
                                {
                                    sw.Write(plaintext);
                                }
                                
                                var encrypted = ms.ToArray();
                                return (Convert.ToBase64String(encrypted), 
                                        Convert.ToBase64String(aes.IV));
                            }
                        }
                    }
                    
                    public static string Decrypt(string ciphertext, byte[] key, string ivBase64)
                    {
                        var encryptedBytes = Convert.FromBase64String(ciphertext);
                        var iv = Convert.FromBase64String(ivBase64);
                        
                        using (var aes = Aes.Create())
                        {
                            aes.Key = key;
                            aes.IV = iv;
                            
                            using (var decryptor = aes.CreateDecryptor())
                            using (var ms = new MemoryStream(encryptedBytes))
                            {
                                // Skip IV (already known)
                                ms.Position = aes.IV.Length;
                                
                                using (var cs = new CryptoStream(ms, decryptor, CryptoStreamMode.Read))
                                using (var sr = new StreamReader(cs))
                                {
                                    return sr.ReadToEnd();
                                }
                            }
                        }
                    }
                }
                
                Authenticated encryption (AES-GCM):
                public static class AuthenticatedEncryption
                {
                    public static (string ciphertext, string tag, string nonce) 
                        Encrypt(string plaintext, byte[] key)
                    {
                        // Generate 96-bit nonce (12 bytes)
                        byte[] nonce = new byte[12];
                        RandomNumberGenerator.Fill(nonce);
                        
                        // Encrypt
                        byte[] plaintextBytes = Encoding.UTF8.GetBytes(plaintext);
                        byte[] tag = new byte[16]; // 128-bit tag
                        byte[] ciphertext = new byte[plaintextBytes.Length];
                        
                        using (var aesGcm = new AesGcm(key))
                        {
                            aesGcm.Encrypt(nonce, plaintextBytes, ciphertext, tag);
                        }
                        
                        return (Convert.ToBase64String(ciphertext),
                                Convert.ToBase64String(tag),
                                Convert.ToBase64String(nonce));
                    }
                    
                    public static string Decrypt(string ciphertext, byte[] key, 
                        string tagBase64, string nonceBase64)
                    {
                        byte[] ciphertextBytes = Convert.FromBase64String(ciphertext);
                        byte[] tag = Convert.FromBase64String(tagBase64);
                        byte[] nonce = Convert.FromBase64String(nonceBase64);
                        
                        byte[] plaintextBytes = new byte[ciphertextBytes.Length];
                        
                        using (var aesGcm = new AesGcm(key))
                        {
                            aesGcm.Decrypt(nonce, ciphertextBytes, tag, plaintextBytes);
                        }
                        
                        return Encoding.UTF8.GetString(plaintextBytes);
                    }
                }
                """);
            
            // 3. Asymmetric encryption
            Console.WriteLine("\n3. Asymmetric Encryption:");
            Console.WriteLine("""
                RSA encryption:
                public static class RsaEncryption
                {
                    public static (string publicKey, string privateKey) GenerateKeys()
                    {
                        using (var rsa = RSA.Create(2048))
                        {
                            var publicKey = rsa.ExportSubjectPublicKeyInfoPem();
                            var privateKey = rsa.ExportPkcs8PrivateKeyPem();
                            return (publicKey, privateKey);
                        }
                    }
                    
                    public static string Encrypt(string plaintext, string publicKeyPem)
                    {
                        using (var rsa = RSA.Create())
                        {
                            rsa.ImportFromPem(publicKeyPem);
                            
                            byte[] plaintextBytes = Encoding.UTF8.GetBytes(plaintext);
                            byte[] encryptedBytes = rsa.Encrypt(plaintextBytes, RSAEncryptionPadding.OaepSHA256);
                            
                            return Convert.ToBase64String(encryptedBytes);
                        }
                    }
                    
                    public static string Decrypt(string ciphertext, string privateKeyPem)
                    {
                        using (var rsa = RSA.Create())
                        {
                            rsa.ImportFromPem(privateKeyPem);
                            
                            byte[] encryptedBytes = Convert.FromBase64String(ciphertext);
                            byte[] plaintextBytes = rsa.Decrypt(encryptedBytes, RSAEncryptionPadding.OaepSHA256);
                            
                            return Encoding.UTF8.GetString(plaintextBytes);
                        }
                    }
                }
                
                Digital signatures:
                public static class DigitalSigner
                {
                    public static (string signature, string publicKey) Sign(string message)
                    {
                        using (var rsa = RSA.Create(2048))
                        {
                            byte[] messageBytes = Encoding.UTF8.GetBytes(message);
                            byte[] signature = rsa.SignData(messageBytes, 
                                HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
                            
                            var publicKey = rsa.ExportSubjectPublicKeyInfoPem();
                            
                            return (Convert.ToBase64String(signature), publicKey);
                        }
                    }
                    
                    public static bool Verify(string message, string signature, string publicKeyPem)
                    {
                        using (var rsa = RSA.Create())
                        {
                            rsa.ImportFromPem(publicKeyPem);
                            
                            byte[] messageBytes = Encoding.UTF8.GetBytes(message);
                            byte[] signatureBytes = Convert.FromBase64String(signature);
                            
                            return rsa.VerifyData(messageBytes, signatureBytes, 
                                HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
                        }
                    }
                }
                """);
            
            // 4. Key management
            Console.WriteLine("\n4. Key Management:");
            Console.WriteLine("""
                Azure Key Vault integration:
                public class AzureKeyVaultService
                {
                    private readonly SecretClient _secretClient;
                    private readonly KeyClient _keyClient;
                    
                    public AzureKeyVaultService(string vaultUri, TokenCredential credential)
                    {
                        _secretClient = new SecretClient(new Uri(vaultUri), credential);
                        _keyClient = new KeyClient(new Uri(vaultUri), credential);
                    }
                    
                    public async Task<string> GetSecretAsync(string secretName)
                    {
                        var secret = await _secretClient.GetSecretAsync(secretName);
                        return secret.Value.Value;
                    }
                    
                    public async Task SetSecretAsync(string secretName, string secretValue)
                    {
                        await _secretClient.SetSecretAsync(secretName, secretValue);
                    }
                    
                    public async Task<byte[]> EncryptWithKeyVault(string keyName, byte[] plaintext)
                    {
                        var encryptResult = await _keyClient.GetCryptographyClient(keyName)
                            .EncryptAsync(EncryptionAlgorithm.RsaOaep, plaintext);
                        
                        return encryptResult.Ciphertext;
                    }
                    
                    public async Task<byte[]> DecryptWithKeyVault(string keyName, byte[] ciphertext)
                    {
                        var decryptResult = await _keyClient.GetCryptographyClient(keyName)
                            .DecryptAsync(EncryptionAlgorithm.RsaOaep, ciphertext);
                        
                        return decryptResult.Plaintext;
                    }
                }
                
                Key rotation:
                public class KeyRotationService
                {
                    private readonly Dictionary<string, (byte[] Key, DateTime Expiry)> _keys = new();
                    
                    public void RotateKeys()
                    {
                        // Generate new key
                        var newKeyId = Guid.NewGuid().ToString();
                        var newKey = GenerateAesKey();
                        
                        // Add with expiry
                        _keys[newKeyId] = (newKey, DateTime.UtcNow.AddDays(90));
                        
                        // Remove expired keys
                        var expiredKeys = _keys.Where(k => k.Value.Expiry < DateTime.UtcNow)
                                            .Select(k => k.Key)
                                            .ToList();
                        
                        foreach (var keyId in expiredKeys)
                        {
                            _keys.Remove(keyId);
                        }
                    }
                    
                    public string EncryptWithCurrentKey(string plaintext)
                    {
                        var currentKeyId = _keys.OrderByDescending(k => k.Value.Expiry)
                                              .First().Key;
                        var currentKey = _keys[currentKeyId].Key;
                        
                        // Encrypt with key ID in result
                        var encrypted = AesEncryption.Encrypt(plaintext, currentKey);
                        return $"{currentKeyId}:{encrypted}";
                    }
                    
                    public string DecryptWithKeyId(string encryptedData)
                    {
                        var parts = encryptedData.Split(':');
                        if (parts.Length != 2)
                            throw new ArgumentException("Invalid encrypted data format");
                        
                        var keyId = parts[0];
                        var ciphertext = parts[1];
                        
                        if (!_keys.TryGetValue(keyId, out var keyInfo))
                            throw new KeyNotFoundException($"Key {keyId} not found");
                        
                        return AesEncryption.Decrypt(ciphertext, keyInfo.Key);
                    }
                    
                    private byte[] GenerateAesKey()
                    {
                        using (var aes = Aes.Create())
                        {
                            aes.GenerateKey();
                            return aes.Key;
                        }
                    }
                }
                """);
        }
        
        static void DemonstrateWebSecurity()
        {
            Console.WriteLine("\n=== 6. Web Security ===\n");
            
            // 1. HTTPS and TLS
            Console.WriteLine("1. HTTPS and TLS:");
            Console.WriteLine("""
                Enforcing HTTPS:
                // In Startup.Configure
                app.UseHttpsRedirection();
                
                // Or with options
                app.UseHttpsRedirection(options =>
                {
                    options.RedirectStatusCode = StatusCodes.Status307TemporaryRedirect;
                    options.HttpsPort = 443;
                });
                
                // In controllers/actions
                [RequireHttps]
                public class SecureController : Controller
                {
                }
                
                // Or globally
                services.AddMvc(options =>
                {
                    options.Filters.Add(new RequireHttpsAttribute());
                });
                
                HSTS (HTTP Strict Transport Security):
                // In Startup.Configure
                app.UseHsts();
                
                // Or with options
                app.UseHsts(options =>
                {
                    options.Preload = true;
                    options.IncludeSubDomains = true;
                    options.MaxAge = TimeSpan.FromDays(365);
                });
                
                // Note: Only use in production, not in development
                if (!env.IsDevelopment())
                {
                    app.UseHsts();
                }
                
                TLS configuration:
                // In Kestrel configuration
                webBuilder.ConfigureKestrel(serverOptions =>
                {
                    serverOptions.ConfigureHttpsDefaults(httpsOptions =>
                    {
                        httpsOptions.SslProtocols = SslProtocols.Tls12 | SslProtocols.Tls13;
                        
                        // Cipher suites (simplified)
                        // .NET Core 3.0+ uses secure defaults
                    });
                });
                
                Certificate validation:
                // Custom certificate validation
                var handler = new HttpClientHandler
                {
                    ServerCertificateCustomValidationCallback = (message, cert, chain, errors) =>
                    {
                        if (errors == SslPolicyErrors.None)
                            return true;
                        
                        // Custom validation logic
                        if (cert.Subject.Contains("example.com"))
                            return true;
                        
                        return false;
                    }
                };
                
                var client = new HttpClient(handler);
                """);
            
            // 2. CORS
            Console.WriteLine("\n2. CORS (Cross-Origin Resource Sharing):");
            Console.WriteLine("""
                Configuring CORS:
                services.AddCors(options =>
                {
                    options.AddPolicy("AllowSpecificOrigin",
                        builder =>
                        {
                            builder.WithOrigins("https://example.com", "https://api.example.com")
                                   .AllowAnyHeader()
                                   .AllowAnyMethod()
                                   .AllowCredentials()
                                   .SetPreflightMaxAge(TimeSpan.FromSeconds(86400));
                        });
                    
                    options.AddPolicy("AllowAnyOrigin",
                        builder =>
                        {
                            builder.AllowAnyOrigin()
                                   .AllowAnyHeader()
                                   .AllowAnyMethod();
                            // Note: AllowAnyOrigin and AllowCredentials cannot be used together
                        });
                    
                    options.AddPolicy("Restricted",
                        builder =>
                        {
                            builder.WithOrigins("https://trusted.com")
                                   .WithMethods("GET", "POST")
                                   .WithHeaders("Content-Type", "Authorization")
                                   .WithExposedHeaders("X-Custom-Header");
                        });
                });
                
                // Apply globally
                app.UseCors("AllowSpecificOrigin");
                
                // Or per endpoint
                app.UseEndpoints(endpoints =>
                {
                    endpoints.MapGet("/api/data")
                        .RequireCors("AllowSpecificOrigin");
                });
                
                // Or with attribute
                [EnableCors("AllowSpecificOrigin")]
                [ApiController]
                public class ApiController : ControllerBase
                {
                }
                
                // Disable CORS
                [DisableCors]
                public IActionResult NoCors()
                {
                    return Ok();
                }
                """);
            
            // 3. CSRF protection
            Console.WriteLine("\n3. CSRF Protection:");
            Console.WriteLine("""
                Anti-forgery tokens:
                // In Startup.ConfigureServices
                services.AddAntiforgery(options =>
                {
                    options.HeaderName = "X-CSRF-TOKEN";
                    options.Cookie.Name = ".AspNetCore.Antiforgery";
                    options.Cookie.HttpOnly = true;
                    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
                    options.SuppressXFrameOptionsHeader = false;
                });
                
                // In views (Razor)
                @using (Html.BeginForm())
                {
                    @Html.AntiForgeryToken()
                    <!-- form fields -->
                }
                
                // Or manually
                <form method="post">
                    <input name="__RequestVerificationToken" type="hidden" 
                           value="@(ViewContext.HttpContext.GetAntiforgeryToken())" />
                    <!-- form fields -->
                </form>
                
                // In AJAX requests
                <script>
                    function getToken() {
                        return document.querySelector('input[name="__RequestVerificationToken"]').value;
                    }
                    
                    $.ajax({
                        url: '/api/data',
                        type: 'POST',
                        headers: {
                            'X-CSRF-TOKEN': getToken()
                        },
                        data: { /* ... */ }
                    });
                </script>
                
                // Validate in controllers
                [HttpPost]
                [ValidateAntiForgeryToken]
                public IActionResult Update(UpdateModel model)
                {
                    // Token automatically validated
                }
                
                // For API controllers (different approach needed)
                [HttpPost]
                [IgnoreAntiforgeryToken] // Disable for APIs (use tokens instead)
                public IActionResult ApiUpdate(UpdateModel model)
                {
                    // Use JWT or API key for authentication
                }
                """);
            
            // 4. Security headers
            Console.WriteLine("\n4. Security Headers:");
            Console.WriteLine("""
                Adding security headers:
                // Custom middleware
                app.Use(async (context, next) =>
                {
                    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
                    context.Response.Headers.Add("X-Frame-Options", "DENY");
                    context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
                    context.Response.Headers.Add("Referrer-Policy", "strict-origin-when-cross-origin");
                    context.Response.Headers.Add("Permissions-Policy", 
                        "camera=(), microphone=(), geolocation=()");
                    
                    // Content Security Policy (CSP)
                    context.Response.Headers.Add("Content-Security-Policy",
                        "default-src 'self'; " +
                        "script-src 'self' 'unsafe-inline' https://cdn.example.com; " +
                        "style-src 'self' 'unsafe-inline'; " +
                        "img-src 'self' data: https:; " +
                        "font-src 'self'; " +
                        "connect-src 'self'; " +
                        "media-src 'self'; " +
                        "object-src 'none'; " +
                        "frame-src 'none'; " +
                        "base-uri 'self'; " +
                        "form-action 'self'; " +
                        "frame-ancestors 'none'; " +
                        "block-all-mixed-content; " +
                        "upgrade-insecure-requests;");
                    
                    await next();
                });
                
                Using NWebSec (NuGet package):
                // Install-Package NWebsec.AspNetCore.Middleware
                app.UseHsts(options => options.MaxAge(days: 365).IncludeSubdomains());
                app.UseXContentTypeOptions();
                app.UseXDownloadOptions();
                app.UseXfo(options => options.Deny());
                app.UseXXssProtection(options => options.EnabledWithBlockMode());
                app.UseReferrerPolicy(options => options.NoReferrer());
                
                // CSP with NWebSec
                app.UseCsp(options => options
                    .DefaultSources(s => s.Self())
                    .ScriptSources(s => s.Self().CustomSources("https://cdn.example.com"))
                    .StyleSources(s => s.Self().UnsafeInline())
                    .ImageSources(s => s.Self().CustomSources("data:"))
                    .FontSources(s => s.Self())
                );
                """);
            
            // 5. Rate limiting
            Console.WriteLine("\n5. Rate Limiting:");
            Console.WriteLine("""
                ASP.NET Core rate limiting:
                // Install-Package Microsoft.AspNetCore.RateLimiting
                
                services.AddRateLimiter(options =>
                {
                    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(
                        context => RateLimitPartition.GetFixedWindowLimiter(
                            partitionKey: context.Connection.RemoteIpAddress?.ToString(),
                            factory: partition => new FixedWindowRateLimiterOptions
                            {
                                AutoReplenishment = true,
                                PermitLimit = 100,
                                QueueLimit = 0,
                                Window = TimeSpan.FromMinutes(1)
                            }));
                    
                    options.OnRejected = (context, token) =>
                    {
                        context.HttpContext.Response.StatusCode = StatusCodes.Status429TooManyRequests;
                        return new ValueTask();
                    };
                });
                
                // Apply globally
                app.UseRateLimiter();
                
                // Or per endpoint
                app.MapGet("/api/limited", () => "Limited endpoint")
                    .RequireRateLimiting("fixed");
                
                // Multiple policies
                services.AddRateLimiter(options =>
                {
                    options.AddFixedWindowLimiter("fixed", fixedOptions =>
                    {
                        fixedOptions.PermitLimit = 10;
                        fixedOptions.Window = TimeSpan.FromSeconds(10);
                        fixedOptions.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
                        fixedOptions.QueueLimit = 5;
                    });
                    
                    options.AddSlidingWindowLimiter("sliding", slidingOptions =>
                    {
                        slidingOptions.PermitLimit = 20;
                        slidingOptions.Window = TimeSpan.FromSeconds(30);
                        slidingOptions.SegmentsPerWindow = 3;
                        slidingOptions.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
                        slidingOptions.QueueLimit = 5;
                    });
                    
                    options.AddTokenBucketLimiter("token", tokenOptions =>
                    {
                        tokenOptions.TokenLimit = 100;
                        tokenOptions.TokensPerPeriod = 20;
                        tokenOptions.ReplenishmentPeriod = TimeSpan.FromSeconds(10);
                        tokenOptions.AutoReplenishment = true;
                        tokenOptions.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
                        tokenOptions.QueueLimit = 5;
                    });
                    
                    options.AddConcurrencyLimiter("concurrency", concurrencyOptions =>
                    {
                        concurrencyOptions.PermitLimit = 10;
                        concurrencyOptions.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
                        concurrencyOptions.QueueLimit = 5;
                    });
                });
                
                Custom rate limiting:
                public class CustomRateLimiter : IRateLimiterPolicy<HttpContext>
                {
                    public Func<HttpContext, RateLimitPartition> GetPartition(HttpContext context)
                    {
                        var ipAddress = context.Connection.RemoteIpAddress?.ToString();
                        
                        if (string.IsNullOrEmpty(ipAddress))
                            return RateLimitPartition.GetNoLimiter("unknown");
                        
                        // Different limits for different IPs
                        if (ipAddress.StartsWith("192.168."))
                        {
                            return RateLimitPartition.GetFixedWindowLimiter(ipAddress,
                                partition => new FixedWindowLimiterOptions
                                {
                                    PermitLimit = 1000,
                                    Window = TimeSpan.FromMinutes(1)
                                });
                        }
                        else
                        {
                            return RateLimitPartition.GetFixedWindowLimiter(ipAddress,
                                partition => new FixedWindowLimiterOptions
                                {
                                    PermitLimit = 100,
                                    Window = TimeSpan.FromMinutes(1)
                                });
                        }
                    }
                    
                    public RateLimitHeaders GetRateLimitHeaders(HttpContext context)
                    {
                        return new RateLimitHeaders
                        {
                            Limit = "X-RateLimit-Limit",
                            Remaining = "X-RateLimit-Remaining",
                            Reset = "X-RateLimit-Reset"
                        };
                    }
                }
                """);
        }
        
        static void DemonstrateNetworkSecurity()
        {
            Console.WriteLine("\n=== 7. Network Security ===\n");
            
            // 1. Secure network communication
            Console.WriteLine("1. Secure Network Communication:");
            Console.WriteLine("""
                Secure TCP/UDP communication:
                // Using SslStream for TCP
                public async Task SecureTcpClient(string host, int port, string message)
                {
                    using (var client = new TcpClient(host, port))
                    using (var stream = client.GetStream())
                    using (var sslStream = new SslStream(stream, false, 
                        ValidateServerCertificate, null))
                    {
                        await sslStream.AuthenticateAsClientAsync(host);
                        
                        // Send data
                        byte[] messageBytes = Encoding.UTF8.GetBytes(message);
                        await sslStream.WriteAsync(messageBytes, 0, messageBytes.Length);
                        
                        // Read response
                        byte[] buffer = new byte[4096];
                        int bytesRead = await sslStream.ReadAsync(buffer, 0, buffer.Length);
                        string response = Encoding.UTF8.GetString(buffer, 0, bytesRead);
                    }
                }
                
                private bool ValidateServerCertificate(
                    object sender, 
                    X509Certificate certificate, 
                    X509Chain chain, 
                    SslPolicyErrors sslPolicyErrors)
                {
                    // Custom validation logic
                    if (sslPolicyErrors == SslPolicyErrors.None)
                        return true;
                    
                    // Log or handle errors
                    Console.WriteLine($"Certificate error: {sslPolicyErrors}");
                    return false;
                }
                
                Secure UDP with DTLS:
                // Note: .NET doesn't have built-in DTLS support
                // Consider using libraries like BouncyCastle or custom implementation
                
                IP address validation:
                public static bool IsValidIpAddress(string ipAddress)
                {
                    if (IPAddress.TryParse(ipAddress, out var ip))
                    {
                        // Check for private/internal addresses
                        byte[] bytes = ip.GetAddressBytes();
                        
                        // IPv4 private ranges
                        if (ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork)
                        {
                            // 10.0.0.0/8
                            if (bytes[0] == 10)
                                return false;
                            
                            // 172.16.0.0/12
                            if (bytes[0] == 172 && bytes[1] >= 16 && bytes[1] <= 31)
                                return false;
                            
                            // 192.168.0.0/16
                            if (bytes[0] == 192 && bytes[1] == 168)
                                return false;
                            
                            // 127.0.0.0/8 (loopback)
                            if (bytes[0] == 127)
                                return false;
                        }
                        
                        // IPv6 private ranges
                        if (ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetworkV6)
                        {
                            if (ip.IsIPv6LinkLocal || ip.IsIPv6SiteLocal || 
                                ip.IsIPv6Multicast || ip.IsIPv6Teredo)
                                return false;
                        }
                        
                        return true;
                    }
                    
                    return false;
                }
                """);
            
            // 2. Firewall and network isolation
            Console.WriteLine("\n2. Firewall and Network Isolation:");
            Console.WriteLine("""
                Application-level firewall:
                public class ApplicationFirewallMiddleware
                {
                    private readonly RequestDelegate _next;
                    private readonly HashSet<string> _blockedIps = new();
                    private readonly HashSet<string> _allowedUserAgents = new();
                    
                    public ApplicationFirewallMiddleware(RequestDelegate next)
                    {
                        _next = next;
                        
                        // Load blocked IPs from configuration
                        _blockedIps.Add("192.168.1.100");
                        _blockedIps.Add("10.0.0.5");
                        
                        // Allowed user agents
                        _allowedUserAgents.Add("Mozilla/5.0");
                        _allowedUserAgents.Add("Chrome/");
                        _allowedUserAgents.Add("Safari/");
                    }
                    
                    public async Task InvokeAsync(HttpContext context)
                    {
                        var ipAddress = context.Connection.RemoteIpAddress?.ToString();
                        
                        // Check blocked IPs
                        if (!string.IsNullOrEmpty(ipAddress) && _blockedIps.Contains(ipAddress))
                        {
                            context.Response.StatusCode = StatusCodes.Status403Forbidden;
                            await context.Response.WriteAsync("Access denied");
                            return;
                        }
                        
                        // Check user agent
                        var userAgent = context.Request.Headers["User-Agent"].ToString();
                        if (!string.IsNullOrEmpty(userAgent) && 
                            !_allowedUserAgents.Any(ua => userAgent.Contains(ua)))
                        {
                            context.Response.StatusCode = StatusCodes.Status403Forbidden;
                            await context.Response.WriteAsync("Invalid user agent");
                            return;
                        }
                        
                        // Rate limiting per IP
                        var rateLimitKey = $"rate:{ipAddress}";
                        var requestCount = await GetRequestCount(rateLimitKey);
                        
                        if (requestCount > 100) // 100 requests per minute
                        {
                            context.Response.StatusCode = StatusCodes.Status429TooManyRequests;
                            await context.Response.WriteAsync("Too many requests");
                            return;
                        }
                        
                        await _next(context);
                    }
                    
                    private async Task<int> GetRequestCount(string key)
                    {
                        // Implement using Redis, database, or memory cache
                        return 0;
                    }
                }
                
                // Register middleware
                app.UseMiddleware<ApplicationFirewallMiddleware>();
                
                Network segmentation in code:
                public class NetworkSegmentService
                {
                    private readonly Dictionary<string, NetworkSegment> _segments = new();
                    
                    public NetworkSegmentService()
                    {
                        // Define segments
                        _segments["internal"] = new NetworkSegment
                        {
                            AllowedIps = new[] { "192.168.0.0/16", "10.0.0.0/8" },
                            AllowedPorts = new[] { 80, 443, 8080 },
                            RequiresAuthentication = false
                        };
                        
                        _segments["dmz"] = new NetworkSegment
                        {
                            AllowedIps = new[] { "0.0.0.0/0" }, // All IPs
                            AllowedPorts = new[] { 80, 443 },
                            RequiresAuthentication = true
                        };
                        
                        _segments["database"] = new NetworkSegment
                        {
                            AllowedIps = new[] { "192.168.1.0/24" },
                            AllowedPorts = new[] { 1433, 3306, 5432 },
                            RequiresAuthentication = true
                        };
                    }
                    
                    public bool IsAllowed(string segmentName, string ipAddress, int port)
                    {
                        if (!_segments.TryGetValue(segmentName, out var segment))
                            return false;
                        
                        // Check IP
                        if (!segment.AllowedIps.Any(network => IsInNetwork(ipAddress, network)))
                            return false;
                        
                        // Check port
                        if (!segment.AllowedPorts.Contains(port))
                            return false;
                        
                        return true;
                    }
                    
                    private bool IsInNetwork(string ipAddress, string network)
                    {
                        // Implement CIDR notation checking
                        return true; // Simplified
                    }
                }
                
                public class NetworkSegment
                {
                    public string[] AllowedIps { get; set; }
                    public int[] AllowedPorts { get; set; }
                    public bool RequiresAuthentication { get; set; }
                }
                """);
            
            // 3. DNS security
            Console.WriteLine("\n3. DNS Security:");
            Console.WriteLine("""
                DNS over HTTPS (DoH):
                public class DnsOverHttpsClient
                {
                    private readonly HttpClient _httpClient;
                    
                    public DnsOverHttpsClient()
                    {
                        _httpClient = new HttpClient();
                        _httpClient.DefaultRequestHeaders.Add("Accept", "application/dns-json");
                    }
                    
                    public async Task<string[]> ResolveAsync(string domain, string dnsServer = "https://cloudflare-dns.com/dns-query")
                    {
                        var url = $"{dnsServer}?name={Uri.EscapeDataString(domain)}&type=A";
                        
                        var response = await _httpClient.GetAsync(url);
                        response.EnsureSuccessStatusCode();
                        
                        var json = await response.Content.ReadAsStringAsync();
                        // Parse JSON response for DNS records
                        
                        return new[] { "192.168.1.1" }; // Simplified
                    }
                }
                
                DNS cache poisoning protection:
                public class SecureDnsResolver
                {
                    private readonly Dictionary<string, (string[] Ips, DateTime Expiry)> _cache = new();
                    private readonly Random _random = new();
                    
                    public async Task<string[]> SecureResolveAsync(string domain)
                    {
                        // Check cache
                        if (_cache.TryGetValue(domain, out var cached) && cached.Expiry > DateTime.UtcNow)
                        {
                            return cached.Ips;
                        }
                        
                        // Use multiple DNS servers for validation
                        var dnsServers = new[]
                        {
                            "8.8.8.8", // Google
                            "1.1.1.1", // Cloudflare
                            "9.9.9.9"  // Quad9
                        };
                        
                        var results = new List<string[]>();
                        
                        foreach (var server in dnsServers)
                        {
                            try
                            {
                                var ips = await ResolveWithServerAsync(domain, server);
                                results.Add(ips);
                            }
                            catch
                            {
                                // Continue with other servers
                            }
                        }
                        
                        // Validate all results match
                        if (results.Count == 0)
                            throw new Exception("DNS resolution failed");
                        
                        var firstResult = results[0];
                        bool allMatch = results.All(r => r.SequenceEqual(firstResult));
                        
                        if (!allMatch)
                        {
                            // Potential DNS poisoning detected
                            throw new SecurityException("DNS poisoning suspected");
                        }
                        
                        // Cache with TTL
                        _cache[domain] = (firstResult, DateTime.UtcNow.AddMinutes(5));
                        
                        return firstResult;
                    }
                    
                    private async Task<string[]> ResolveWithServerAsync(string domain, string server)
                    {
                        // Implement DNS query
                        return new[] { "192.168.1.1" }; // Simplified
                    }
                }
                """);
            
            // 4. Secure protocols
            Console.WriteLine("\n4. Secure Protocols:");
            Console.WriteLine("""
                Choosing secure protocols:
                // Configure HttpClient to use TLS 1.2 or higher
                var handler = new HttpClientHandler
                {
                    SslProtocols = SslProtocols.Tls12 | SslProtocols.Tls13,
                    ServerCertificateCustomValidationCallback = (message, cert, chain, errors) =>
                    {
                        // Additional validation
                        return errors == SslPolicyErrors.None;
                    }
                };
                
                var client = new HttpClient(handler);
                
                // Or globally for all HttpClient instances
                AppContext.SetSwitch("System.Net.Http.UseSocketsHttpHandler", true);
                ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12 | SecurityProtocolType.Tls13;
                
                SSH/SFTP in .NET:
                // Using SSH.NET library
                // Install-Package SSH.NET
                
                using (var client = new SftpClient("host", "username", "password"))
                {
                    client.Connect();
                    
                    // Upload file
                    using (var fileStream = File.OpenRead("local.txt"))
                    {
                        client.UploadFile(fileStream, "remote.txt");
                    }
                    
                    // Download file
                    using (var fileStream = File.OpenWrite("local.txt"))
                    {
                        client.DownloadFile("remote.txt", fileStream);
                    }
                    
                    client.Disconnect();
                }
                
                // With key authentication
                var privateKey = new PrivateKeyFile("private.key");
                var client = new SftpClient("host", "username", new[] { privateKey });
                
                Secure WebSocket (WSS):
                // Client-side
                var client = new ClientWebSocket();
                client.Options.RemoteCertificateValidationCallback = 
                    (sender, certificate, chain, sslPolicyErrors) =>
                    {
                        return sslPolicyErrors == SslPolicyErrors.None;
                    };
                
                await client.ConnectAsync(new Uri("wss://example.com/ws"), CancellationToken.None);
                
                // Server-side (ASP.NET Core)
                app.UseWebSockets(new WebSocketOptions
                {
                    KeepAliveInterval = TimeSpan.FromSeconds(120),
                    AllowedOrigins = { "https://example.com" }
                });
                
                app.Use(async (context, next) =>
                {
                    if (context.WebSockets.IsWebSocketRequest)
                    {
                        var webSocket = await context.WebSockets.AcceptWebSocketAsync();
                        // Handle WebSocket connection
                    }
                    else
                    {
                        await next();
                    }
                });
                """);
        }
        
        static void DemonstrateSecurityTesting()
        {
            Console.WriteLine("\n=== 8. Security Testing ===\n");
            
            // 1. Static Application Security Testing (SAST)
            Console.WriteLine("1. Static Application Security Testing (SAST):");
            Console.WriteLine("""
                Using Roslyn analyzers:
                // In csproj
                <PropertyGroup>
                  <EnableNETAnalyzers>true</EnableNETAnalyzers>
                  <AnalysisLevel>latest</AnalysisLevel>
                  <AnalysisMode>AllEnabledByDefault</AnalysisMode>
                </PropertyGroup>
                
                <ItemGroup>
                  <PackageReference Include="Microsoft.CodeAnalysis.NetAnalyzers" Version="latest" />
                  <PackageReference Include="SecurityCodeScan" Version="latest" />
                </ItemGroup>
                
                Common security rules:
                • CA3001: Review code for SQL injection vulnerabilities
                • CA3002: Review code for XSS vulnerabilities
                • CA3003: Review code for file path injection vulnerabilities
                • CA3004: Review code for information disclosure vulnerabilities
                • CA3005: Review code for LDAP injection vulnerabilities
                • CA3006: Review code for process command injection vulnerabilities
                • CA3007: Review code for open redirect vulnerabilities
                • CA3008: Review code for XPath injection vulnerabilities
                • CA3009: Review code for XML injection vulnerabilities
                • CA3010: Review code for XAML injection vulnerabilities
                • CA3011: Review code for DLL injection vulnerabilities
                • CA3012: Review code for regex injection vulnerabilities
                
                Custom security rules:
                [DiagnosticAnalyzer(LanguageNames.CSharp)]
                public class SqlInjectionAnalyzer : DiagnosticAnalyzer
                {
                    private const string DiagnosticId = "SEC001";
                    private const string Category = "Security";
                    
                    private static readonly DiagnosticDescriptor Rule = new DiagnosticDescriptor(
                        DiagnosticId,
                        "Potential SQL injection vulnerability",
                        "String concatenation in SQL query detected",
                        Category,
                        DiagnosticSeverity.Warning,
                        isEnabledByDefault: true,
                        description: "Use parameterized queries to prevent SQL injection.");
                    
                    public override ImmutableArray<DiagnosticDescriptor> SupportedDiagnostics => 
                        ImmutableArray.Create(Rule);
                    
                    public override void Initialize(AnalysisContext context)
                    {
                        context.ConfigureGeneratedCodeAnalysis(GeneratedCodeAnalysisFlags.None);
                        context.EnableConcurrentExecution();
                        context.RegisterSyntaxNodeAction(AnalyzeNode, SyntaxKind.InvocationExpression);
                    }
                    
                    private void AnalyzeNode(SyntaxNodeAnalysisContext context)
                    {
                        var invocation = (InvocationExpressionSyntax)context.Node;
                        var methodSymbol = context.SemanticModel.GetSymbolInfo(invocation).Symbol as IMethodSymbol;
                        
                        if (methodSymbol?.Name == "ExecuteSql" && 
                            methodSymbol.ContainingType?.Name == "SqlCommand")
                        {
                            // Check for string concatenation in arguments
                            var arguments = invocation.ArgumentList.Arguments;
                            foreach (var argument in arguments)
                            {
                                if (argument.Expression is BinaryExpressionSyntax binaryExpr &&
                                    binaryExpr.OperatorToken.Kind() == SyntaxKind.PlusToken)
                                {
                                    var diagnostic = Diagnostic.Create(
                                        Rule, argument.Expression.GetLocation());
                                    context.ReportDiagnostic(diagnostic);
                                }
                            }
                        }
                    }
                }
                """);
            
            // 2. Dynamic Application Security Testing (DAST)
            Console.WriteLine("\n2. Dynamic Application Security Testing (DAST):");
            Console.WriteLine("""
                Automated vulnerability scanning:
                // Using OWASP ZAP API
                public class ZapScanner
                {
                    private readonly HttpClient _client;
                    
                    public ZapScanner(string zapUrl, string apiKey)
                    {
                        _client = new HttpClient();
                        _client.BaseAddress = new Uri(zapUrl);
                        _client.DefaultRequestHeaders.Add("X-ZAP-API-Key", apiKey);
                    }
                    
                    public async Task ScanWebsite(string targetUrl)
                    {
                        // Start spider
                        var spiderResponse = await _client.GetAsync(
                            $"/JSON/spider/action/scan/?url={Uri.EscapeDataString(targetUrl)}");
                        
                        // Wait for spider to complete
                        await Task.Delay(TimeSpan.FromSeconds(30));
                        
                        // Start active scan
                        var scanResponse = await _client.GetAsync(
                            $"/JSON/ascan/action/scan/?url={Uri.EscapeDataString(targetUrl)}");
                        
                        // Wait for scan to complete
                        await Task.Delay(TimeSpan.FromSeconds(60));
                        
                        // Get results
                        var resultsResponse = await _client.GetAsync("/JSON/core/view/alerts/");
                        var results = await resultsResponse.Content.ReadAsStringAsync();
                        
                        // Parse and analyze results
                    }
                }
                
                // Using Burp Suite Enterprise Edition API (similar approach)
                
                Custom vulnerability tests:
                public class VulnerabilityTester
                {
                    private readonly HttpClient _httpClient;
                    
                    public async Task TestSqlInjection(string baseUrl)
                    {
                        var testPayloads = new[]
                        {
                            "' OR '1'='1",
                            "'; DROP TABLE Users--",
                            "' UNION SELECT NULL, username, password FROM Users--"
                        };
                        
                        foreach (var payload in testPayloads)
                        {
                            var url = $"{baseUrl}/search?q={Uri.EscapeDataString(payload)}";
                            var response = await _httpClient.GetAsync(url);
                            var content = await response.Content.ReadAsStringAsync();
                            
                            // Check for SQL error messages
                            if (content.Contains("SQL") || content.Contains("syntax") || 
                                content.Contains("database") || content.Contains("query"))
                            {
                                Console.WriteLine($"Potential SQL injection: {payload}");
                            }
                        }
                    }
                    
                    public async Task TestXss(string baseUrl)
                    {
                        var testPayloads = new[]
                        {
                            "<script>alert('XSS')</script>",
                            "\" onmouseover=\"alert('XSS')\"",
                            "<img src=x onerror=alert('XSS')>"
                        };
                        
                        foreach (var payload in testPayloads)
                        {
                            var url = $"{baseUrl}/search?q={Uri.EscapeDataString(payload)}";
                            var response = await _httpClient.GetAsync(url);
                            var content = await response.Content.ReadAsStringAsync();
                            
                            // Check if payload appears unencoded
                            if (content.Contains(payload) && 
                                !content.Contains(HttpUtility.HtmlEncode(payload)))
                            {
                                Console.WriteLine($"Potential XSS: {payload}");
                            }
                        }
                    }
                    
                    public async Task TestDirectoryTraversal(string baseUrl)
                    {
                        var testPayloads = new[]
                        {
                            "../../../etc/passwd",
                            "..\\..\\..\\windows\\system32\\config\\sam",
                            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
                        };
                        
                        foreach (var payload in testPayloads)
                        {
                            var url = $"{baseUrl}/download?file={payload}";
                            var response = await _httpClient.GetAsync(url);
                            
                            // Check for sensitive file contents
                            if (response.IsSuccessStatusCode)
                            {
                                var content = await response.Content.ReadAsStringAsync();
                                if (content.Contains("root:") || content.Contains("Administrator"))
                                {
                                    Console.WriteLine($"Directory traversal: {payload}");
                                }
                            }
                        }
                    }
                }
                """);
            
            // 3. Penetration testing
            Console.WriteLine("\n3. Penetration Testing:");
            Console.WriteLine("""
                Manual penetration testing checklist:
                
                Information Gathering:
                • Enumerate subdomains
                • Identify technologies (Wappalyzer, WhatWeb)
                • Check for exposed files (robots.txt, sitemap.xml)
                • Check DNS records
                
                Configuration Testing:
                • Check for default credentials
                • Test for directory listing
                • Check HTTP methods (OPTIONS, TRACE)
                • Test for verbose error messages
                
                Authentication Testing:
                • Test for weak passwords
                • Test for account enumeration
                • Test for brute force vulnerabilities
                • Test for password reset flaws
                • Test for session management issues
                
                Authorization Testing:
                • Test for IDOR (Insecure Direct Object Reference)
                • Test for privilege escalation
                • Test for horizontal/vertical access control
                
                Input Validation Testing:
                • Test all parameters for injection
                • Test file upload functionality
                • Test for XXE (XML External Entity)
                
                Client-side Testing:
                • Test for DOM-based XSS
                • Test for client-side storage issues
                • Test for JavaScript vulnerabilities
                
                Business Logic Testing:
                • Test for workflow bypasses
                • Test for pricing manipulation
                • Test for race conditions
                
                Automated penetration testing tools:
                // Using Metasploit Framework via API
                // Using Nessus, Qualys, or OpenVAS
                // Using custom scripts with Nmap, Nikto, etc.
                
                Reporting vulnerabilities:
                public class VulnerabilityReport
                {
                    public string Title { get; set; }
                    public string Description { get; set; }
                    public string Impact { get; set; }
                    public string Severity { get; set; } // Critical, High, Medium, Low
                    public string StepsToReproduce { get; set; }
                    public string ProofOfConcept { get; set; }
                    public string Remediation { get; set; }
                    public string References { get; set; }
                    public DateTime DiscoveryDate { get; set; }
                    public string Reporter { get; set; }
                }
                """);
            
            // 4. Security code review
            Console.WriteLine("\n4. Security Code Review:");
            Console.WriteLine("""
                Code review checklist:
                
                Authentication:
                • Are passwords hashed with strong algorithms (PBKDF2, Argon2, bcrypt)?
                • Is multi-factor authentication implemented?
                • Are session tokens properly generated and validated?
                • Is there protection against brute force attacks?
                
                Authorization:
                • Is the principle of least privilege followed?
                • Are access controls enforced server-side?
                • Is there protection against IDOR?
                • Are admin functions properly protected?
                
                Input Validation:
                • Is all user input validated?
                • Are parameterized queries used for database access?
                • Is output properly encoded?
                • Are file uploads properly restricted?
                
                Cryptography:
                • Are strong algorithms used (AES-256, RSA-2048+, SHA-256+)?
                • Are cryptographic keys properly managed?
                • Is random number generation cryptographically secure?
                • Is encryption used for sensitive data?
                
                Error Handling:
                • Do error messages leak sensitive information?
                • Are exceptions properly caught and logged?
                • Is there generic error handling for users?
                
                Session Management:
                • Are session tokens random and unpredictable?
                • Is session timeout properly configured?
                • Are sessions invalidated on logout?
                • Is there protection against session fixation?
                
                Configuration:
                • Are default passwords changed?
                • Is debugging disabled in production?
                • Are security headers set?
                • Are unnecessary services disabled?
                
                Dependencies:
                • Are dependencies up to date?
                • Are vulnerability scans run on dependencies?
                • Are only necessary packages included?
                
                Logging:
                • Are security events logged?
                • Is sensitive data masked in logs?
                • Are logs protected from tampering?
                • Is log rotation implemented?
                
                Tools for code review:
                • Visual Studio Code Analysis
                • SonarQube with security plugins
                • Checkmarx, Fortify, Veracode
                • Semgrep, CodeQL
                • OWASP Dependency Check
                """);
        }
        
        static void DemonstrateRealWorldScenarios()
        {
            Console.WriteLine("\n=== 9. Real-World Security Scenarios ===\n");
            
            // 1. Secure microservices architecture
            Console.WriteLine("1. Secure Microservices Architecture:");
            Console.WriteLine("""
                Service-to-service authentication:
                // Using OAuth 2.0 Client Credentials flow
                public class ServiceAuthentication
                {
                    private readonly HttpClient _httpClient;
                    private readonly string _clientId;
                    private readonly string _clientSecret;
                    private readonly string _tokenEndpoint;
                    
                    public async Task<string> GetAccessTokenAsync()
                    {
                        var request = new HttpRequestMessage(HttpMethod.Post, _tokenEndpoint);
                        var content = new FormUrlEncodedContent(new[]
                        {
                            new KeyValuePair<string, string>("grant_type", "client_credentials"),
                            new KeyValuePair<string, string>("client_id", _clientId),
                            new KeyValuePair<string, string>("client_secret", _clientSecret),
                            new KeyValuePair<string, string>("scope", "api1 api2")
                        });
                        
                        request.Content = content;
                        
                        var response = await _httpClient.SendAsync(request);
                        response.EnsureSuccessStatusCode();
                        
                        var tokenResponse = await response.Content.ReadFromJsonAsync<TokenResponse>();
                        return tokenResponse.AccessToken;
                    }
                    
                    public async Task<HttpResponseMessage> CallServiceAsync(string serviceUrl, string method, object data)
                    {
                        var token = await GetAccessTokenAsync();
                        
                        var request = new HttpRequestMessage(new HttpMethod(method), serviceUrl);
                        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
                        
                        if (data != null)
                        {
                            request.Content = JsonContent.Create(data);
                        }
                        
                        return await _httpClient.SendAsync(request);
                    }
                }
                
                // Or using mutual TLS (mTLS)
                public class MutualTlsClient
                {
                    private readonly HttpClient _httpClient;
                    
                    public MutualTlsClient(string certificatePath, string certificatePassword)
                    {
                        var handler = new HttpClientHandler();
                        handler.ClientCertificates.Add(new X509Certificate2(
                            certificatePath, certificatePassword));
                        
                        _httpClient = new HttpClient(handler);
                    }
                    
                    public async Task<string> CallServiceAsync(string url)
                    {
                        var response = await _httpClient.GetAsync(url);
                        return await response.Content.ReadAsStringAsync();
                    }
                }
                
                API Gateway security:
                public class ApiGatewaySecurityMiddleware
                {
                    private readonly RequestDelegate _next;
                    private readonly IApiKeyValidator _keyValidator;
                    private readonly IJwtValidator _jwtValidator;
                    
                    public async Task InvokeAsync(HttpContext context)
                    {
                        // Check for API key
                        if (context.Request.Headers.TryGetValue("X-API-Key", out var apiKey))
                        {
                            if (!await _keyValidator.ValidateAsync(apiKey))
                            {
                                context.Response.StatusCode = 401;
                                return;
                            }
                        }
                        // Check for JWT
                        else if (context.Request.Headers.TryGetValue("Authorization", out var authHeader))
                        {
                            var token = authHeader.ToString().Replace("Bearer ", "");
                            if (!await _jwtValidator.ValidateAsync(token))
                            {
                                context.Response.StatusCode = 401;
                                return;
                            }
                        }
                        else
                        {
                            context.Response.StatusCode = 401;
                            return;
                        }
                        
                        // Rate limiting
                        var clientId = GetClientId(context);
                        if (!await CheckRateLimitAsync(clientId))
                        {
                            context.Response.StatusCode = 429;
                            return;
                        }
                        
                        // Log request
                        await LogRequestAsync(context);
                        
                        await _next(context);
                    }
                }
                """);
            
            // 2. Secure cloud deployment
            Console.WriteLine("\n2. Secure Cloud Deployment:");
            Console.WriteLine("""
                Azure Security Center recommendations:
                • Enable Azure Defender for servers
                • Enable Just-In-Time (JIT) VM access
                • Enable adaptive application controls
                • Enable file integrity monitoring
                • Enable threat detection for storage
                • Enable encryption for data at rest
                
                AWS Security Hub recommendations:
                • Enable AWS Config
                • Enable CloudTrail
                • Enable GuardDuty
                • Enable Security Hub
                • Enable Inspector
                • Enable Macie for sensitive data
                
                Kubernetes security:
                // Pod security policies
                apiVersion: policy/v1beta1
                kind: PodSecurityPolicy
                metadata:
                  name: restricted
                spec:
                  privileged: false
                  allowPrivilegeEscalation: false
                  requiredDropCapabilities:
                    - ALL
                  volumes:
                    - 'configMap'
                    - 'emptyDir'
                    - 'projected'
                    - 'secret'
                    - 'downwardAPI'
                    - 'persistentVolumeClaim'
                  hostNetwork: false
                  hostIPC: false
                  hostPID: false
                  runAsUser:
                    rule: 'MustRunAsNonRoot'
                  seLinux:
                    rule: 'RunAsAny'
                  supplementalGroups:
                    rule: 'MustRunAs'
                    ranges:
                      - min: 1
                        max: 65535
                  fsGroup:
                    rule: 'MustRunAs'
                    ranges:
                      - min: 1
                        max: 65535
                  readOnlyRootFilesystem: true
                
                // Network policies
                apiVersion: networking.k8s.io/v1
                kind: NetworkPolicy
                metadata:
                  name: default-deny
                spec:
                  podSelector: {}
                  policyTypes:
                  - Ingress
                  - Egress
                
                Secrets management in cloud:
                // Azure Key Vault
                var secretClient = new SecretClient(
                    new Uri("https://myvault.vault.azure.net/"),
                    new DefaultAzureCredential());
                
                var secret = await secretClient.GetSecretAsync("DatabaseConnectionString");
                var connectionString = secret.Value.Value;
                
                // AWS Secrets Manager
                var client = new AmazonSecretsManagerClient();
                var response = await client.GetSecretValueAsync(new GetSecretValueRequest
                {
                    SecretId = "prod/DatabaseConnectionString"
                });
                
                var connectionString = response.SecretString;
                
                // HashiCorp Vault
                var vaultClient = new VaultClient("https://vault.example.com:8200");
                vaultClient.SetToken("vault-token");
                
                var secret = await vaultClient.Secrets.KeyValue.V2.ReadSecretAsync(
                    path: "secret/data/database",
                    mountPoint: "secret");
                
                var connectionString = secret.Data.Data["connectionString"].ToString();
                """);
            
            // 3. Incident response
            Console.WriteLine("\n3. Incident Response:");
            Console.WriteLine("""
                Incident response plan:
                
                Preparation:
                • Establish incident response team
                • Create communication plan
                • Prepare tools and resources
                • Conduct training and drills
                
                Identification:
                • Monitor security alerts
                • Analyze suspicious activity
                • Determine scope and impact
                • Classify incident severity
                
                Containment:
                • Short-term containment (isolate affected systems)
                • Long-term containment (apply patches, remove malware)
                • Evidence collection and preservation
                
                Eradication:
                • Remove malware or unauthorized access
                • Identify and address root cause
                • Validate system cleanliness
                
                Recovery:
                • Restore systems from backups
                • Monitor for recurrence
                • Validate system functionality
                
                Lessons Learned:
                • Document incident details
                • Analyze response effectiveness
                • Update policies and procedures
                • Implement preventive measures
                
                Incident response automation:
                public class IncidentResponseAutomation
                {
                    private readonly ISecurityAlertService _alertService;
                    private readonly ISystemIsolationService _isolationService;
                    private readonly ILogCollectionService _logService;
                    private readonly INotificationService _notificationService;
                    
                    public async Task HandleSecurityIncidentAsync(SecurityAlert alert)
                    {
                        // Step 1: Validate alert
                        if (!await ValidateAlertAsync(alert))
                            return;
                        
                        // Step 2: Isolate affected systems
                        await _isolationService.IsolateSystemAsync(alert.AffectedSystem);
                        
                        // Step 3: Collect evidence
                        var logs = await _logService.CollectLogsAsync(
                            alert.AffectedSystem, 
                            alert.DetectionTime.AddHours(-1), 
                            DateTime.UtcNow);
                        
                        // Step 4: Notify response team
                        await _notificationService.NotifyIncidentResponseTeamAsync(
                            alert.Severity, 
                            alert.Description, 
                            logs);
                        
                        // Step 5: Begin investigation
                        await InvestigateIncidentAsync(alert, logs);
                    }
                    
                    private async Task<bool> ValidateAlertAsync(SecurityAlert alert)
                    {
                        // Check if this is a false positive
                        // Verify with additional data sources
                        // Consult threat intelligence
                        return true; // Simplified
                    }
                    
                    private async Task InvestigateIncidentAsync(SecurityAlert alert, LogCollection logs)
                    {
                        // Automated investigation steps
                        // Analyze logs for patterns
                        // Check for similar incidents
                        // Determine attack vector
                        // Identify compromised accounts
                    }
                }
                
                Forensics and evidence handling:
                public class DigitalForensics
                {
                    public async Task<ForensicEvidence> CollectEvidenceAsync(string systemId)
                    {
                        var evidence = new ForensicEvidence
                        {
                            CollectionTime = DateTime.UtcNow,
                            Collector = Environment.UserName,
                            SystemId = systemId
                        };
                        
                        // Collect memory dump
                        evidence.MemoryDump = await CollectMemoryDumpAsync(systemId);
                        
                        // Collect disk image
                        evidence.DiskImage = await CollectDiskImageAsync(systemId);
                        
                        // Collect network captures
                        evidence.NetworkCaptures = await CollectNetworkCapturesAsync(systemId);
                        
                        // Collect logs
                        evidence.Logs = await CollectLogsAsync(systemId);
                        
                        // Collect registry/configuration
                        evidence.Configuration = await CollectConfigurationAsync(systemId);
                        
                        // Calculate hashes for integrity
                        evidence.Hash = ComputeEvidenceHash(evidence);
                        
                        return evidence;
                    }
                    
                    private string ComputeEvidenceHash(ForensicEvidence evidence)
                    {
                        using (var sha256 = SHA256.Create())
                        {
                            // Create hash of all evidence
                            var bytes = Encoding.UTF8.GetBytes(
                                $"{evidence.CollectionTime}{evidence.SystemId}{evidence.Logs}");
                            return Convert.ToBase64String(sha256.ComputeHash(bytes));
                        }
                    }
                }
                """);
            
            // 4. Compliance and regulations
            Console.WriteLine("\n4. Compliance and Regulations:");
            Console.WriteLine("""
                GDPR compliance:
                public class GdprComplianceService
                {
                    private readonly IDataRepository _repository;
                    
                    // Right to access
                    public async Task<PersonalDataReport> GetPersonalDataAsync(string userId)
                    {
                        var data = await _repository.GetAllUserDataAsync(userId);
                        
                        return new PersonalDataReport
                        {
                            UserId = userId,
                            CollectedData = data,
                            ProcessingPurposes = GetProcessingPurposes(data),
                            ThirdPartyRecipients = GetThirdPartyRecipients(data),
                            RetentionPeriods = GetRetentionPeriods(data)
                        };
                    }
                    
                    // Right to erasure (right to be forgotten)
                    public async Task DeletePersonalDataAsync(string userId)
                    {
                        // Anonymize or delete data
                        await _repository.AnonymizeUserDataAsync(userId);
                        
                        // Notify third parties
                        await NotifyThirdPartiesAsync(userId);
                        
                        // Log deletion
                        await LogDeletionAsync(userId);
                    }
                    
                    // Data portability
                    public async Task<DataPortabilityPackage> ExportPersonalDataAsync(string userId)
                    {
                        var data = await _repository.GetAllUserDataAsync(userId);
                        
                        return new DataPortabilityPackage
                        {
                            UserId = userId,
                            Data = data,
                            Format = "JSON",
                            Timestamp = DateTime.UtcNow
                        };
                    }
                    
                    // Consent management
                    public async Task<bool> HasValidConsentAsync(string userId, string consentType)
                    {
                        var consent = await _repository.GetConsentAsync(userId, consentType);
                        
                        return consent != null && 
                               consent.IsGiven && 
                               consent.IsInformed && 
                               consent.IsSpecific && 
                               consent.IsUnambiguous && 
                               !consent.IsWithdrawn;
                    }
                }
                
                PCI DSS compliance:
                public class PciDssComplianceService
                {
                    // Requirement 3: Protect stored cardholder data
                    public string MaskCardNumber(string cardNumber)
                    {
                        if (string.IsNullOrEmpty(cardNumber) || cardNumber.Length < 12)
                            return cardNumber;
                            
                        return cardNumber.Substring(0, 6) + 
                               new string('*', cardNumber.Length - 10) + 
                               cardNumber.Substring(cardNumber.Length - 4);
                    }
                    
                    // Requirement 4: Encrypt transmission of cardholder data
                    public async Task<string> EncryptCardDataAsync(string cardData)
                    {
                        using (var aes = Aes.Create())
                        {
                            aes.GenerateKey();
                            aes.GenerateIV();
                            
                            using (var encryptor = aes.CreateEncryptor())
                            using (var ms = new MemoryStream())
                            {
                                await ms.WriteAsync(aes.IV, 0, aes.IV.Length);
                                
                                using (var cs = new CryptoStream(ms, encryptor, CryptoStreamMode.Write))
                                using (var sw = new StreamWriter(cs))
                                {
                                    await sw.WriteAsync(cardData);
                                }
                                
                                return Convert.ToBase64String(ms.ToArray());
                            }
                        }
                    }
                    
                    // Requirement 8: Identify and authenticate access
                    public async Task<bool> AuthenticateUserAsync(string userId, string password)
                    {
                        // Multi-factor authentication
                        var passwordValid = await ValidatePasswordAsync(userId, password);
                        var tokenValid = await ValidateTokenAsync(userId);
                        
                        return passwordValid && tokenValid;
                    }
                    
                    // Requirement 10: Track and monitor access
                    public async Task LogCardAccessAsync(string userId, string cardId, string action)
                    {
                        await _auditLogger.LogAsync(new AuditEntry
                        {
                            Timestamp = DateTime.UtcNow,
                            UserId = userId,
                            Action = action,
                            Resource = $"Card/{cardId}",
                            IpAddress = GetClientIpAddress(),
                            Success = true
                        });
                    }
                }
                
                HIPAA compliance:
                public class HipaaComplianceService
                {
                    // Protected Health Information (PHI) handling
                    public string DeidentifyPhi(string phi)
                    {
                        // Remove 18 HIPAA identifiers
                        // 1. Names
                        // 2. Geographic subdivisions smaller than a state
                        // 3. All elements of dates (except year) for ages over 89
                        // 4. Telephone numbers
                        // 5. Vehicle identifiers and serial numbers
                        // 6. Fax numbers
                        // 7. Device identifiers and serial numbers
                        // 8. Email addresses
                        // 9. Web URLs
                        // 10. IP addresses
                        // 11. Social Security numbers
                        // 12. Medical record numbers
                        // 13. Health plan beneficiary numbers
                        // 14. Account numbers
                        // 15. Certificate/license numbers
                        // 16. Vehicle identifiers and serial numbers
                        // 17. Device identifiers and serial numbers
                        // 18. Biometric identifiers
                        
                        // Implementation would use regex patterns to identify and remove/replace
                        return Regex.Replace(phi, 
                            @"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b", // SSN pattern
                            "***-**-****");
                    }
                    
                    // Minimum Necessary Rule
                    public async Task<PhiData> ApplyMinimumNecessaryAsync(PhiData data, string purpose)
                    {
                        var filtered = new PhiData();
                        
                        switch (purpose)
                        {
                            case "Billing":
                                filtered.PatientId = data.PatientId;
                                filtered.ProcedureCodes = data.ProcedureCodes;
                                filtered.Dates = data.Dates;
                                break;
                                
                            case "Treatment":
                                filtered.PatientId = data.PatientId;
                                filtered.MedicalHistory = data.MedicalHistory;
                                filtered.CurrentConditions = data.CurrentConditions;
                                filtered.Medications = data.Medications;
                                break;
                                
                            case "Research":
                                filtered = DeidentifyPhiData(data);
                                break;
                        }
                        
                        return filtered;
                    }
                    
                    // Audit controls
                    public async Task<AuditReport> GenerateAccessReportAsync(string patientId, DateTime start, DateTime end)
                    {
                        var accesses = await _auditLog.GetAccessesAsync(patientId, start, end);
                        
                        return new AuditReport
                        {
                            PatientId = patientId,
                            Period = $"{start:yyyy-MM-dd} to {end:yyyy-MM-dd}",
                            TotalAccesses = accesses.Count,
                            AccessesByUser = accesses.GroupBy(a => a.UserId)
                                .Select(g => new { User = g.Key, Count = g.Count() }),
                            UnusualAccesses = accesses.Where(a => IsUnusualAccess(a))
                        };
                    }
                }
                """);
        }
    }
    
    // Supporting classes for examples
    
    public class ApplicationUser
    {
        public string Id { get; set; }
        public string UserName { get; set; }
        public string Email { get; set; }
    }
    
    public class SecurityAlert
    {
        public string Id { get; set; }
        public string Severity { get; set; }
        public string Description { get; set; }
        public string AffectedSystem { get; set; }
        public DateTime DetectionTime { get; set; }
    }
    
    public class ForensicEvidence
    {
        public DateTime CollectionTime { get; set; }
        public string Collector { get; set; }
        public string SystemId { get; set; }
        public byte[] MemoryDump { get; set; }
        public byte[] DiskImage { get; set; }
        public byte[] NetworkCaptures { get; set; }
        public string Logs { get; set; }
        public string Configuration { get; set; }
        public string Hash { get; set; }
    }
    
    public class PersonalDataReport
    {
        public string UserId { get; set; }
        public object CollectedData { get; set; }
        public string[] ProcessingPurposes { get; set; }
        public string[] ThirdPartyRecipients { get; set; }
        public Dictionary<string, TimeSpan> RetentionPeriods { get; set; }
    }
    
    public class DataPortabilityPackage
    {
        public string UserId { get; set; }
        public object Data { get; set; }
        public string Format { get; set; }
        public DateTime Timestamp { get; set; }
    }
    
    public class PhiData
    {
        public string PatientId { get; set; }
        public string[] ProcedureCodes { get; set; }
        public DateTime[] Dates { get; set; }
        public string MedicalHistory { get; set; }
        public string[] CurrentConditions { get; set; }
        public string[] Medications { get; set; }
    }
    
    public class AuditReport
    {
        public string PatientId { get; set; }
        public string Period { get; set; }
        public int TotalAccesses { get; set; }
        public object AccessesByUser { get; set; }
        public object UnusualAccesses { get; set; }
    }
    
    public class TokenResponse
    {
        public string AccessToken { get; set; }
        public string TokenType { get; set; }
        public int ExpiresIn { get; set; }
        public string Scope { get; set; }
    }
    
    public class UpdateModel
    {
        public string Data { get; set; }
    }
    
    public class RegisterViewModel
    {
        public string Email { get; set; }
        public string Password { get; set; }
    }
    
    public class ErrorViewModel
    {
        public int StatusCode { get; set; }
        public string Message { get; set; }
    }
    
    public class LogCollection
    {
        public string SystemId { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public string LogData { get; set; }
    }
    
    public class AuditEntry
    {
        public DateTime Timestamp { get; set; }
        public string UserId { get; set; }
        public string Action { get; set; }
        public string Resource { get; set; }
        public string IpAddress { get; set; }
        public bool Success { get; set; }
    }
    
    // Mock services for examples
    public interface IDataRepository
    {
        Task<object> GetAllUserDataAsync(string userId);
        Task AnonymizeUserDataAsync(string userId);
        Task<object> GetConsentAsync(string userId, string consentType);
    }
    
    public interface ISecurityAlertService { }
    public interface ISystemIsolationService { }
    public interface ILogCollectionService { }
    public interface INotificationService { }
    public interface IApiKeyValidator { Task<bool> ValidateAsync(string apiKey); }
    public interface IJwtValidator { Task<bool> ValidateAsync(string token); }
    public interface IAuditLogger { Task LogAsync(AuditEntry entry); }
}