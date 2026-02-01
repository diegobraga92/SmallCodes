package main

import (
    "context"
    "crypto/rand"
    "crypto/subtle"
    "database/sql"
    "encoding/base64"
    "encoding/json"
    "fmt"
    "html/template"
    "io"
    "log"
    "net/http"
    "net/url"
    "regexp"
    "strings"
    "time"

    "github.com/golang-jwt/jwt/v5"
    "github.com/google/uuid"
    "golang.org/x/crypto/bcrypt"
    "golang.org/x/oauth2"
    "golang.org/x/oauth2/github"
)

// =============================================
// 1. PASSWORD HASHING WITH BCRYPT
// =============================================

type PasswordManager struct{}

func (pm *PasswordManager) HashPassword(password string) (string, error) {
    // Cost factor determines the computational complexity
    // Higher cost = more secure but slower (default is 10)
    bytes, err := bcrypt.GenerateFromPassword([]byte(password), 12)
    if err != nil {
        return "", fmt.Errorf("failed to hash password: %w", err)
    }
    return string(bytes), nil
}

func (pm *PasswordManager) ComparePassword(hashedPassword, password string) bool {
    err := bcrypt.CompareHashAndPassword([]byte(hashedPassword), []byte(password))
    return err == nil
}

// Generate secure random salt
func generateSalt(length int) (string, error) {
    salt := make([]byte, length)
    if _, err := rand.Read(salt); err != nil {
        return "", fmt.Errorf("failed to generate salt: %w", err)
    }
    return base64.URLEncoding.EncodeToString(salt), nil
}

// Password strength validation
func validatePasswordStrength(password string) error {
    if len(password) < 8 {
        return fmt.Errorf("password must be at least 8 characters")
    }
    
    hasUpper := regexp.MustCompile(`[A-Z]`).MatchString(password)
    hasLower := regexp.MustCompile(`[a-z]`).MatchString(password)
    hasNumber := regexp.MustCompile(`[0-9]`).MatchString(password)
    hasSpecial := regexp.MustCompile(`[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]`).MatchString(password)
    
    checksPassed := 0
    if hasUpper {
        checksPassed++
    }
    if hasLower {
        checksPassed++
    }
    if hasNumber {
        checksPassed++
    }
    if hasSpecial {
        checksPassed++
    }
    
    if checksPassed < 3 {
        return fmt.Errorf("password must contain at least 3 of: uppercase, lowercase, number, special character")
    }
    
    return nil
}

// =============================================
// 2. JWT FUNDAMENTALS & IMPLEMENTATION
// =============================================

type JWTConfig struct {
    SecretKey     []byte
    AccessExpiry  time.Duration
    RefreshExpiry time.Duration
    Issuer        string
}

type JWTAuth struct {
    config *JWTConfig
}

func NewJWTAuth(secret string) *JWTAuth {
    return &JWTAuth{
        config: &JWTConfig{
            SecretKey:     []byte(secret),
            AccessExpiry:  15 * time.Minute,
            RefreshExpiry: 7 * 24 * time.Hour, // 7 days
            Issuer:        "myapp",
        },
    }
}

type Claims struct {
    UserID    string   `json:"user_id"`
    Email     string   `json:"email"`
    Roles     []string `json:"roles"`
    TokenType string   `json:"token_type"` // "access" or "refresh"
    jwt.RegisteredClaims
}

func (ja *JWTAuth) GenerateAccessToken(userID, email string, roles []string) (string, error) {
    claims := Claims{
        UserID:    userID,
        Email:     email,
        Roles:     roles,
        TokenType: "access",
        RegisteredClaims: jwt.RegisteredClaims{
            ExpiresAt: jwt.NewNumericDate(time.Now().Add(ja.config.AccessExpiry)),
            IssuedAt:  jwt.NewNumericDate(time.Now()),
            NotBefore: jwt.NewNumericDate(time.Now()),
            Issuer:    ja.config.Issuer,
            Subject:   userID,
            ID:        uuid.New().String(),
        },
    }
    
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString(ja.config.SecretKey)
}

func (ja *JWTAuth) GenerateRefreshToken(userID string) (string, error) {
    claims := Claims{
        UserID:    userID,
        TokenType: "refresh",
        RegisteredClaims: jwt.RegisteredClaims{
            ExpiresAt: jwt.NewNumericDate(time.Now().Add(ja.config.RefreshExpiry)),
            IssuedAt:  jwt.NewNumericDate(time.Now()),
            Issuer:    ja.config.Issuer,
            Subject:   userID,
            ID:        uuid.New().String(),
        },
    }
    
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString(ja.config.SecretKey)
}

func (ja *JWTAuth) ValidateToken(tokenString string) (*Claims, error) {
    token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(token *jwt.Token) (interface{}, error) {
        // Validate signing method
        if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
            return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
        }
        return ja.config.SecretKey, nil
    })
    
    if err != nil {
        return nil, fmt.Errorf("token validation failed: %w", err)
    }
    
    if claims, ok := token.Claims.(*Claims); ok && token.Valid {
        return claims, nil
    }
    
    return nil, fmt.Errorf("invalid token claims")
}

func (ja *JWTAuth) RefreshTokenPair(refreshToken string) (string, string, error) {
    claims, err := ja.ValidateToken(refreshToken)
    if err != nil {
        return "", "", fmt.Errorf("invalid refresh token: %w", err)
    }
    
    if claims.TokenType != "refresh" {
        return "", "", fmt.Errorf("not a refresh token")
    }
    
    // Generate new token pair
    accessToken, err := ja.GenerateAccessToken(claims.UserID, claims.Email, claims.Roles)
    if err != nil {
        return "", "", err
    }
    
    newRefreshToken, err := ja.GenerateRefreshToken(claims.UserID)
    if err != nil {
        return "", "", err
    }
    
    return accessToken, newRefreshToken, nil
}

// =============================================
// 3. OAUTH2 BASICS & IMPLEMENTATION
// =============================================

type OAuthProvider struct {
    config *oauth2.Config
    name   string
}

func NewOAuthProvider(providerName, clientID, clientSecret, redirectURL string) *OAuthProvider {
    var endpoint oauth2.Endpoint
    
    switch providerName {
    case "github":
        endpoint = github.Endpoint
    case "google":
        endpoint = oauth2.Endpoint{
            AuthURL:  "https://accounts.google.com/o/oauth2/auth",
            TokenURL: "https://oauth2.googleapis.com/token",
        }
    case "facebook":
        endpoint = oauth2.Endpoint{
            AuthURL:  "https://www.facebook.com/v12.0/dialog/oauth",
            TokenURL: "https://graph.facebook.com/v12.0/oauth/access_token",
        }
    default:
        panic("unsupported provider")
    }
    
    return &OAuthProvider{
        name: providerName,
        config: &oauth2.Config{
            ClientID:     clientID,
            ClientSecret: clientSecret,
            RedirectURL:  redirectURL,
            Scopes:       []string{}, // Provider-specific scopes
            Endpoint:     endpoint,
        },
    }
}

type OAuthUserInfo struct {
    ID        string
    Email     string
    Name      string
    AvatarURL string
    Provider  string
}

func (op *OAuthProvider) HandleLogin(w http.ResponseWriter, r *http.Request) {
    // Generate state parameter for CSRF protection
    state := uuid.New().String()
    
    // Store state in session
    session, _ := sessionStore.Get(r, "oauth_state")
    session.Values["state"] = state
    session.Save(r, w)
    
    // Redirect to OAuth provider
    url := op.config.AuthCodeURL(state, oauth2.AccessTypeOffline)
    http.Redirect(w, r, url, http.StatusFound)
}

func (op *OAuthProvider) HandleCallback(w http.ResponseWriter, r *http.Request) (*OAuthUserInfo, error) {
    // Verify state parameter
    session, _ := sessionStore.Get(r, "oauth_state")
    storedState, ok := session.Values["state"].(string)
    if !ok {
        return nil, fmt.Errorf("invalid session state")
    }
    
    queryState := r.URL.Query().Get("state")
    if subtle.ConstantTimeCompare([]byte(storedState), []byte(queryState)) != 1 {
        return nil, fmt.Errorf("state mismatch")
    }
    
    // Clear state from session
    delete(session.Values, "state")
    session.Save(r, w)
    
    // Exchange code for token
    code := r.URL.Query().Get("code")
    token, err := op.config.Exchange(r.Context(), code)
    if err != nil {
        return nil, fmt.Errorf("failed to exchange token: %w", err)
    }
    
    // Fetch user info from provider
    userInfo, err := op.fetchUserInfo(r.Context(), token)
    if err != nil {
        return nil, fmt.Errorf("failed to fetch user info: %w", err)
    }
    
    return userInfo, nil
}

func (op *OAuthProvider) fetchUserInfo(ctx context.Context, token *oauth2.Token) (*OAuthUserInfo, error) {
    client := op.config.Client(ctx, token)
    
    var userInfo OAuthUserInfo
    userInfo.Provider = op.name
    
    switch op.name {
    case "github":
        resp, err := client.Get("https://api.github.com/user")
        if err != nil {
            return nil, err
        }
        defer resp.Body.Close()
        
        var data struct {
            ID        int    `json:"id"`
            Email     string `json:"email"`
            Name      string `json:"name"`
            AvatarURL string `json:"avatar_url"`
        }
        
        if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
            return nil, err
        }
        
        userInfo.ID = fmt.Sprintf("%d", data.ID)
        userInfo.Email = data.Email
        userInfo.Name = data.Name
        userInfo.AvatarURL = data.AvatarURL
        
    case "google":
        resp, err := client.Get("https://www.googleapis.com/oauth2/v2/userinfo")
        if err != nil {
            return nil, err
        }
        defer resp.Body.Close()
        
        var data struct {
            ID        string `json:"id"`
            Email     string `json:"email"`
            Name      string `json:"name"`
            Picture   string `json:"picture"`
        }
        
        if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
            return nil, err
        }
        
        userInfo.ID = data.ID
        userInfo.Email = data.Email
        userInfo.Name = data.Name
        userInfo.AvatarURL = data.Picture
    }
    
    return &userInfo, nil
}

// =============================================
// 4. HTTPS & TLS CONFIGURATION
// =============================================

type TLSServer struct {
    certFile string
    keyFile  string
}

func (ts *TLSServer) Start(addr string, handler http.Handler) error {
    server := &http.Server{
        Addr:    addr,
        Handler: handler,
        TLSConfig: &tls.Config{
            MinVersion: tls.VersionTLS12,
            CurvePreferences: []tls.CurveID{
                tls.X25519,
                tls.CurveP256,
            },
            CipherSuites: []uint16{
                tls.TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,
                tls.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
                tls.TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,
                tls.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,
                tls.TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,
                tls.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
            },
            PreferServerCipherSuites: true,
        },
        ReadTimeout:  15 * time.Second,
        WriteTimeout: 15 * time.Second,
        IdleTimeout:  60 * time.Second,
    }
    
    return server.ListenAndServeTLS(ts.certFile, ts.keyFile)
}

// Generate self-signed certificate for development
// In production, use Let's Encrypt or commercial CA
func generateSelfSignedCert() {
    /*
    // Using mkcert for local development
    // Install: brew install mkcert (macOS)
    // Run: mkcert -install
    // Then: mkcert localhost 127.0.0.1 ::1
    
    // Or programmatically:
    cert, err := selfsigned.GenerateSelfSignedCert()
    if err != nil {
        log.Fatal(err)
    }
    
    ioutil.WriteFile("cert.pem", cert.Cert, 0644)
    ioutil.WriteFile("key.pem", cert.Key, 0644)
    */
}

// =============================================
// 5. SECURE HEADERS
// =============================================

type SecurityHeaders struct{}

func (sh *SecurityHeaders) Middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Set security headers
        headers := w.Header()
        
        // Prevent MIME type sniffing
        headers.Set("X-Content-Type-Options", "nosniff")
        
        // Prevent clickjacking
        headers.Set("X-Frame-Options", "DENY")
        
        // XSS protection
        headers.Set("X-XSS-Protection", "1; mode=block")
        
        // Strict Transport Security (HSTS)
        headers.Set("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        
        // Content Security Policy
        headers.Set("Content-Security-Policy",
            "default-src 'self'; "+
                "script-src 'self' https://cdn.example.com; "+
                "style-src 'self' https://fonts.googleapis.com; "+
                "img-src 'self' data: https:; "+
                "font-src 'self' https://fonts.gstatic.com; "+
                "connect-src 'self' https://api.example.com; "+
                "frame-ancestors 'none'; "+
                "form-action 'self'")
        
        // Referrer Policy
        headers.Set("Referrer-Policy", "strict-origin-when-cross-origin")
        
        // Permissions Policy (formerly Feature Policy)
        headers.Set("Permissions-Policy",
            "camera=(), microphone=(), geolocation=(), payment=()")
        
        // Cache control for sensitive pages
        if strings.Contains(r.URL.Path, "/admin") || strings.Contains(r.URL.Path, "/account") {
            headers.Set("Cache-Control", "no-store, max-age=0")
        }
        
        next.ServeHTTP(w, r)
    })
}

// CORS middleware
func CORSMiddleware(allowedOrigins []string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            origin := r.Header.Get("Origin")
            
            // Check if origin is allowed
            allowed := false
            for _, allowedOrigin := range allowedOrigins {
                if allowedOrigin == "*" || allowedOrigin == origin {
                    allowed = true
                    break
                }
            }
            
            if allowed {
                w.Header().Set("Access-Control-Allow-Origin", origin)
                w.Header().Set("Access-Control-Allow-Credentials", "true")
                w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH")
                w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
                w.Header().Set("Access-Control-Expose-Headers", "X-Total-Count, Link")
                w.Header().Set("Access-Control-Max-Age", "86400") // 24 hours
            }
            
            if r.Method == "OPTIONS" {
                w.WriteHeader(http.StatusOK)
                return
            }
            
            next.ServeHTTP(w, r)
        })
    }
}

// =============================================
// 6. INPUT VALIDATION & SANITIZATION
// =============================================

type InputValidator struct{}

func (iv *InputValidator) ValidateEmail(email string) (bool, string) {
    // Basic email validation
    emailRegex := regexp.MustCompile(`^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
    if !emailRegex.MatchString(email) {
        return false, "Invalid email format"
    }
    
    // Check for disposable emails
    disposableDomains := []string{
        "tempmail.com", "mailinator.com", "guerrillamail.com",
        "10minutemail.com", "trashmail.com",
    }
    
    parts := strings.Split(email, "@")
    if len(parts) != 2 {
        return false, "Invalid email"
    }
    
    domain := strings.ToLower(parts[1])
    for _, disposable := range disposableDomains {
        if strings.Contains(domain, disposable) {
            return false, "Disposable email addresses are not allowed"
        }
    }
    
    return true, ""
}

func (iv *InputValidator) SanitizeHTML(input string) string {
    // Allow only safe HTML tags and attributes
    policy := bluemonday.NewPolicy()
    
    // Basic tags
    policy.AllowStandardAttributes()
    policy.AllowElements("p", "br", "b", "i", "em", "strong", "a", "ul", "ol", "li")
    
    // Links with safe attributes
    policy.AllowAttrs("href").OnElements("a")
    policy.RequireParseableURLs(true)
    
    // Additional security
    policy.RequireNoFollowOnLinks(true)
    policy.RequireNoReferrerOnLinks(true)
    policy.AddTargetBlankToFullyQualifiedLinks(true)
    
    return policy.Sanitize(input)
}

func (iv *InputValidator) ValidateAndSanitizeInput(input map[string]interface{}) (map[string]interface{}, error) {
    sanitized := make(map[string]interface{})
    
    for key, value := range input {
        switch v := value.(type) {
        case string:
            // Trim whitespace
            trimmed := strings.TrimSpace(v)
            
            // Check for maximum length
            if len(trimmed) > 10000 {
                return nil, fmt.Errorf("%s exceeds maximum length", key)
            }
            
            // Sanitize based on field type
            if strings.Contains(key, "html") || strings.Contains(key, "content") {
                sanitized[key] = iv.SanitizeHTML(trimmed)
            } else {
                // Escape special characters for non-HTML fields
                sanitized[key] = template.HTMLEscapeString(trimmed)
            }
            
        case []interface{}:
            // Recursively sanitize arrays
            sanitizedArray := make([]interface{}, len(v))
            for i, item := range v {
                if str, ok := item.(string); ok {
                    sanitizedArray[i] = template.HTMLEscapeString(str)
                } else {
                    sanitizedArray[i] = item
                }
            }
            sanitized[key] = sanitizedArray
            
        default:
            sanitized[key] = v
        }
    }
    
    return sanitized, nil
}

// =============================================
// 7. COMMON VULNERABILITIES PROTECTION
// =============================================

type SecurityMiddleware struct {
    db *sql.DB
}

// SQL Injection Protection
func (sm *SecurityMiddleware) SafeQuery(query string, args ...interface{}) (*sql.Rows, error) {
    // Always use parameterized queries
    return sm.db.Query(query, args...)
}

// Example vulnerable query (DON'T DO THIS)
func vulnerableQuery(db *sql.DB, userInput string) {
    // ⚠️ VULNERABLE TO SQL INJECTION
    query := fmt.Sprintf("SELECT * FROM users WHERE name = '%s'", userInput)
    db.Query(query)
    
    // ✅ SAFE - Use parameterized queries
    safeQuery := "SELECT * FROM users WHERE name = ?"
    db.Query(safeQuery, userInput)
}

// XSS Protection
func (sm *SecurityMiddleware) XSSProtection(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Validate Content-Type
        contentType := r.Header.Get("Content-Type")
        if r.Method == "POST" || r.Method == "PUT" || r.Method == "PATCH" {
            if !strings.Contains(contentType, "application/json") &&
               !strings.Contains(contentType, "application/x-www-form-urlencoded") &&
               !strings.Contains(contentType, "multipart/form-data") {
                http.Error(w, "Unsupported Content-Type", http.StatusUnsupportedMediaType)
                return
            }
        }
        
        // Sanitize query parameters
        query := r.URL.Query()
        for key, values := range query {
            sanitizedValues := make([]string, len(values))
            for i, value := range values {
                sanitizedValues[i] = template.URLQueryEscaper(value)
            }
            query[key] = sanitizedValues
        }
        r.URL.RawQuery = query.Encode()
        
        next.ServeHTTP(w, r)
    })
}

// CSRF Protection
func (sm *SecurityMiddleware) CSRFProtection(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Skip CSRF for safe methods
        if r.Method == "GET" || r.Method == "HEAD" || r.Method == "OPTIONS" {
            next.ServeHTTP(w, r)
            return
        }
        
        // Check CSRF token
        csrfToken := r.Header.Get("X-CSRF-Token")
        if csrfToken == "" {
            csrfToken = r.FormValue("csrf_token")
        }
        
        session, _ := sessionStore.Get(r, "session")
        storedToken, ok := session.Values["csrf_token"].(string)
        if !ok || csrfToken != storedToken {
            http.Error(w, "Invalid CSRF token", http.StatusForbidden)
            return
        }
        
        next.ServeHTTP(w, r)
    })
}

// Rate limiting protection against brute force
type RateLimiter struct {
    attempts map[string][]time.Time
    mu       sync.RWMutex
}

func NewRateLimiter() *RateLimiter {
    return &RateLimiter{
        attempts: make(map[string][]time.Time),
    }
}

func (rl *RateLimiter) Check(identifier string, maxAttempts int, window time.Duration) bool {
    rl.mu.Lock()
    defer rl.mu.Unlock()
    
    now := time.Now()
    
    // Clean old attempts
    validAttempts := []time.Time{}
    for _, attempt := range rl.attempts[identifier] {
        if now.Sub(attempt) <= window {
            validAttempts = append(validAttempts, attempt)
        }
    }
    
    // Check if exceeded
    if len(validAttempts) >= maxAttempts {
        return false
    }
    
    // Record new attempt
    validAttempts = append(validAttempts, now)
    rl.attempts[identifier] = validAttempts
    
    return true
}

// =============================================
// 8. SESSION MANAGEMENT
// =============================================

type SessionManager struct {
    store sessions.Store
}

func NewSessionManager(secretKey string) *SessionManager {
    return &SessionManager{
        store: sessions.NewCookieStore([]byte(secretKey)),
    }
}

func (sm *SessionManager) CreateSession(w http.ResponseWriter, r *http.Request, userID, email string) error {
    session, _ := sm.store.Get(r, "session")
    
    // Set session values
    session.Values["user_id"] = userID
    session.Values["email"] = email
    session.Values["authenticated"] = true
    session.Values["login_time"] = time.Now().Unix()
    
    // Generate CSRF token
    csrfToken := uuid.New().String()
    session.Values["csrf_token"] = csrfToken
    
    // Set session options
    session.Options = &sessions.Options{
        Path:     "/",
        MaxAge:   86400 * 7, // 7 days
        HttpOnly: true,
        Secure:   true, // Set to true in production (HTTPS only)
        SameSite: http.SameSiteStrictMode,
    }
    
    return session.Save(r, w)
}

func (sm *SessionManager) GetSession(r *http.Request) (map[string]interface{}, error) {
    session, err := sm.store.Get(r, "session")
    if err != nil {
        return nil, err
    }
    
    if auth, ok := session.Values["authenticated"].(bool); !ok || !auth {
        return nil, fmt.Errorf("not authenticated")
    }
    
    return session.Values, nil
}

func (sm *SessionManager) DestroySession(w http.ResponseWriter, r *http.Request) error {
    session, _ := sm.store.Get(r, "session")
    
    // Clear all values
    for key := range session.Values {
        delete(session.Values, key)
    }
    
    // Set MaxAge to -1 to delete the cookie
    session.Options.MaxAge = -1
    
    return session.Save(r, w)
}

func (sm *SessionManager) RegenerateSession(w http.ResponseWriter, r *http.Request) error {
    session, _ := sm.store.Get(r, "session")
    
    // Get current values
    values := session.Values
    
    // Delete old session
    session.Options.MaxAge = -1
    session.Save(r, w)
    
    // Create new session
    newSession, _ := sm.store.New(r, "session")
    newSession.Values = values
    newSession.Options = &sessions.Options{
        Path:     "/",
        MaxAge:   86400 * 7,
        HttpOnly: true,
        Secure:   true,
        SameSite: http.SameSiteStrictMode,
    }
    
    return newSession.Save(r, w)
}

// =============================================
// 9. ROLE-BASED ACCESS CONTROL (RBAC)
// =============================================

type Permission string

const (
    PermissionUserRead   Permission = "user:read"
    PermissionUserWrite  Permission = "user:write"
    PermissionUserDelete Permission = "user:delete"
    PermissionAdminRead  Permission = "admin:read"
    PermissionAdminWrite Permission = "admin:write"
)

type Role struct {
    Name        string
    Permissions []Permission
}

var (
    RoleAdmin = Role{
        Name: "admin",
        Permissions: []Permission{
            PermissionUserRead,
            PermissionUserWrite,
            PermissionUserDelete,
            PermissionAdminRead,
            PermissionAdminWrite,
        },
    }
    
    RoleEditor = Role{
        Name: "editor",
        Permissions: []Permission{
            PermissionUserRead,
            PermissionUserWrite,
        },
    }
    
    RoleViewer = Role{
        Name: "viewer",
        Permissions: []Permission{
            PermissionUserRead,
        },
    }
)

type RBAC struct {
    roles map[string]Role
}

func NewRBAC() *RBAC {
    return &RBAC{
        roles: map[string]Role{
            "admin":  RoleAdmin,
            "editor": RoleEditor,
            "viewer": RoleViewer,
        },
    }
}

func (rbac *RBAC) HasPermission(roleName string, permission Permission) bool {
    role, exists := rbac.roles[roleName]
    if !exists {
        return false
    }
    
    for _, p := range role.Permissions {
        if p == permission {
            return true
        }
    }
    
    return false
}

func (rbac *RBAC) Middleware(requiredPermission Permission) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            // Get user roles from context (set by auth middleware)
            rolesRaw := r.Context().Value("user_roles")
            if rolesRaw == nil {
                http.Error(w, "Unauthorized", http.StatusUnauthorized)
                return
            }
            
            roles, ok := rolesRaw.([]string)
            if !ok {
                http.Error(w, "Unauthorized", http.StatusUnauthorized)
                return
            }
            
            // Check if any role has the required permission
            authorized := false
            for _, role := range roles {
                if rbac.HasPermission(role, requiredPermission) {
                    authorized = true
                    break
                }
            }
            
            if !authorized {
                http.Error(w, "Forbidden", http.StatusForbidden)
                return
            }
            
            next.ServeHTTP(w, r)
        })
    }
}

// =============================================
// 10. SECURE PASSWORD STORAGE SYSTEM
// =============================================

type SecurePasswordStorage struct {
    passwordManager *PasswordManager
    pepper          string // Application-wide secret pepper
}

func NewSecurePasswordStorage(pepper string) *SecurePasswordStorage {
    return &SecurePasswordStorage{
        passwordManager: &PasswordManager{},
        pepper:          pepper,
    }
}

func (sps *SecurePasswordStorage) CreatePasswordHash(password string) (string, error) {
    // Add pepper before hashing
    pepperedPassword := password + sps.pepper
    
    // Hash with bcrypt
    hash, err := sps.passwordManager.HashPassword(pepperedPassword)
    if err != nil {
        return "", fmt.Errorf("failed to hash password: %w", err)
    }
    
    return hash, nil
}

func (sps *SecurePasswordStorage) VerifyPassword(storedHash, password string) bool {
    // Add pepper before verifying
    pepperedPassword := password + sps.pepper
    
    return sps.passwordManager.ComparePassword(storedHash, pepperedPassword)
}

// Password rotation policy
func (sps *SecurePasswordStorage) ShouldRotatePassword(lastChanged time.Time) bool {
    // Require password change every 90 days
    return time.Since(lastChanged) > 90*24*time.Hour
}

// =============================================
// 11. COMPREHENSIVE AUTHENTICATION SYSTEM
// =============================================

type AuthSystem struct {
    jwtAuth      *JWTAuth
    sessionMgr   *SessionManager
    passwordMgr  *SecurePasswordStorage
    rbac         *RBAC
    rateLimiter  *RateLimiter
    oauthConfigs map[string]*OAuthProvider
}

func NewAuthSystem(jwtSecret, sessionSecret, passwordPepper string) *AuthSystem {
    return &AuthSystem{
        jwtAuth:     NewJWTAuth(jwtSecret),
        sessionMgr:  NewSessionManager(sessionSecret),
        passwordMgr: NewSecurePasswordStorage(passwordPepper),
        rbac:        NewRBAC(),
        rateLimiter: NewRateLimiter(),
        oauthConfigs: make(map[string]*OAuthProvider),
    }
}

func (as *AuthSystem) RegisterRoutes(mux *http.ServeMux) {
    mux.HandleFunc("/api/register", as.handleRegister)
    mux.HandleFunc("/api/login", as.handleLogin)
    mux.HandleFunc("/api/logout", as.handleLogout)
    mux.HandleFunc("/api/refresh", as.handleRefreshToken)
    mux.HandleFunc("/api/me", as.handleGetCurrentUser)
    mux.HandleFunc("/api/change-password", as.handleChangePassword)
    
    // OAuth routes
    mux.HandleFunc("/api/oauth/{provider}/login", as.handleOAuthLogin)
    mux.HandleFunc("/api/oauth/{provider}/callback", as.handleOAuthCallback)
}

func (as *AuthSystem) handleRegister(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }
    
    var req struct {
        Email    string `json:"email"`
        Password string `json:"password"`
        Name     string `json:"name"`
    }
    
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid request", http.StatusBadRequest)
        return
    }
    
    // Validate input
    if valid, msg := validator.ValidateEmail(req.Email); !valid {
        http.Error(w, msg, http.StatusBadRequest)
        return
    }
    
    if err := validatePasswordStrength(req.Password); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    
    // Rate limiting by IP
    ip := strings.Split(r.RemoteAddr, ":")[0]
    if !as.rateLimiter.Check("register_"+ip, 5, time.Hour) {
        http.Error(w, "Too many registration attempts", http.StatusTooManyRequests)
        return
    }
    
    // Check if user exists (in database)
    // ...
    
    // Hash password
    passwordHash, err := as.passwordMgr.CreatePasswordHash(req.Password)
    if err != nil {
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }
    
    // Create user in database
    userID := uuid.New().String()
    
    // Generate tokens
    accessToken, err := as.jwtAuth.GenerateAccessToken(userID, req.Email, []string{"user"})
    if err != nil {
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }
    
    refreshToken, err := as.jwtAuth.GenerateRefreshToken(userID)
    if err != nil {
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }
    
    // Set session
    if err := as.sessionMgr.CreateSession(w, r, userID, req.Email); err != nil {
        log.Printf("Session creation error: %v", err)
    }
    
    // Return response
    response := map[string]interface{}{
        "access_token":  accessToken,
        "refresh_token": refreshToken,
        "user": map[string]interface{}{
            "id":    userID,
            "email": req.Email,
            "name":  req.Name,
            "roles": []string{"user"},
        },
    }
    
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}

func (as *AuthSystem) handleLogin(w http.ResponseWriter, r *http.Request) {
    if r.Method != "POST" {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }
    
    var req struct {
        Email    string `json:"email"`
        Password string `json:"password"`
    }
    
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid request", http.StatusBadRequest)
        return
    }
    
    // Rate limiting by email
    if !as.rateLimiter.Check("login_"+req.Email, 5, 15*time.Minute) {
        http.Error(w, "Too many login attempts", http.StatusTooManyRequests)
        return
    }
    
    // Get user from database
    // ...
    
    // Verify password
    // storedHash := getUserPasswordHash(req.Email)
    // if !as.passwordMgr.VerifyPassword(storedHash, req.Password) {
    //     http.Error(w, "Invalid credentials", http.StatusUnauthorized)
    //     return
    // }
    
    // For demo - simulate successful login
    userID := "demo_user_id"
    userEmail := req.Email
    userRoles := []string{"user"}
    
    // Generate tokens
    accessToken, err := as.jwtAuth.GenerateAccessToken(userID, userEmail, userRoles)
    if err != nil {
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }
    
    refreshToken, err := as.jwtAuth.GenerateRefreshToken(userID)
    if err != nil {
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }
    
    // Set session
    if err := as.sessionMgr.CreateSession(w, r, userID, userEmail); err != nil {
        log.Printf("Session creation error: %v", err)
    }
    
    // Return response
    response := map[string]interface{}{
        "access_token":  accessToken,
        "refresh_token": refreshToken,
        "user": map[string]interface{}{
            "id":    userID,
            "email": userEmail,
            "roles": userRoles,
        },
    }
    
    w.Header().Set("Content-Type", "application/json")
    w.Header().Set("Cache-Control", "no-store")
    json.NewEncoder(w).Encode(response)
}

func (as *AuthSystem) AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Try JWT token first
        authHeader := r.Header.Get("Authorization")
        var claims *Claims
        var err error
        
        if strings.HasPrefix(authHeader, "Bearer ") {
            token := strings.TrimPrefix(authHeader, "Bearer ")
            claims, err = as.jwtAuth.ValidateToken(token)
            if err == nil {
                // Add user info to context
                ctx := context.WithValue(r.Context(), "user_id", claims.UserID)
                ctx = context.WithValue(ctx, "user_email", claims.Email)
                ctx = context.WithValue(ctx, "user_roles", claims.Roles)
                r = r.WithContext(ctx)
                next.ServeHTTP(w, r)
                return
            }
        }
        
        // Try session
        session, err := as.sessionMgr.GetSession(r)
        if err == nil {
            userID, _ := session["user_id"].(string)
            email, _ := session["email"].(string)
            
            // Add user info to context
            ctx := context.WithValue(r.Context(), "user_id", userID)
            ctx = context.WithValue(ctx, "user_email", email)
            ctx = context.WithValue(ctx, "user_roles", []string{"user"})
            r = r.WithContext(ctx)
            next.ServeHTTP(w, r)
            return
        }
        
        // Unauthorized
        http.Error(w, "Unauthorized", http.StatusUnauthorized)
    })
}

// =============================================
// 12. SECURE PASSWORD RESET FLOW
// =============================================

type PasswordResetManager struct {
    resetTokens map[string]resetToken // In production, use database
    mu          sync.RWMutex
}

type resetToken struct {
    email     string
    tokenHash string
    expiresAt time.Time
}

func NewPasswordResetManager() *PasswordResetManager {
    return &PasswordResetManager{
        resetTokens: make(map[string]resetToken),
    }
}

func (prm *PasswordResetManager) GenerateResetToken(email string) (string, error) {
    prm.mu.Lock()
    defer prm.mu.Unlock()
    
    // Generate random token
    tokenBytes := make([]byte, 32)
    if _, err := rand.Read(tokenBytes); err != nil {
        return "", err
    }
    token := base64.URLEncoding.EncodeToString(tokenBytes)
    
    // Hash token before storing (like password)
    tokenHash, err := bcrypt.GenerateFromPassword([]byte(token), bcrypt.DefaultCost)
    if err != nil {
        return "", err
    }
    
    // Store with expiration (1 hour)
    prm.resetTokens[email] = resetToken{
        email:     email,
        tokenHash: string(tokenHash),
        expiresAt: time.Now().Add(time.Hour),
    }
    
    return token, nil
}

func (prm *PasswordResetManager) ValidateResetToken(email, token string) bool {
    prm.mu.RLock()
    defer prm.mu.RUnlock()
    
    storedToken, exists := prm.resetTokens[email]
    if !exists {
        return false
    }
    
    // Check expiration
    if time.Now().After(storedToken.expiresAt) {
        delete(prm.resetTokens, email)
        return false
    }
    
    // Verify token
    err := bcrypt.CompareHashAndPassword([]byte(storedToken.tokenHash), []byte(token))
    return err == nil
}

func (prm *PasswordResetManager) ConsumeResetToken(email string) {
    prm.mu.Lock()
    defer prm.mu.Unlock()
    delete(prm.resetTokens, email)
}

// =============================================
// MAIN FUNCTION - DEMO
// =============================================

func main() {
    fmt.Println("=== Go Authentication & Security Demo ===\n")
    
    // 1. Password hashing demo
    fmt.Println("1. Password Hashing with Bcrypt:")
    passwordManager := &PasswordManager{}
    
    password := "SecureP@ssw0rd123"
    hash, err := passwordManager.HashPassword(password)
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("Password: %s\n", password)
    fmt.Printf("Hash: %s\n", hash)
    fmt.Printf("Verification: %v\n\n", passwordManager.ComparePassword(hash, password))
    
    // 2. JWT token demo
    fmt.Println("2. JWT Token Generation:")
    jwtAuth := NewJWTAuth("super-secret-key-change-in-production")
    
    accessToken, err := jwtAuth.GenerateAccessToken("user123", "user@example.com", []string{"user", "admin"})
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("Access Token: %s\n", accessToken[:50] + "...")
    
    claims, err := jwtAuth.ValidateToken(accessToken)
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("Decoded Claims - UserID: %s, Email: %s, Roles: %v\n\n", 
        claims.UserID, claims.Email, claims.Roles)
    
    // 3. Password strength validation
    fmt.Println("3. Password Strength Validation:")
    testPasswords := []string{"weak", "MediumPass", "StrongP@ss1"}
    
    for _, pwd := range testPasswords {
        err := validatePasswordStrength(pwd)
        if err != nil {
            fmt.Printf("'%s' - %v\n", pwd, err)
        } else {
            fmt.Printf("'%s' - OK\n", pwd)
        }
    }
    fmt.Println()
    
    // 4. Input sanitization demo
    fmt.Println("4. Input Sanitization:")
    validator := &InputValidator{}
    
    dirtyInput := `<script>alert("XSS")</script><p>Hello <b>World</b></p>`
    cleanHTML := validator.SanitizeHTML(dirtyInput)
    
    fmt.Printf("Original: %s\n", dirtyInput)
    fmt.Printf("Sanitized: %s\n\n", cleanHTML)
    
    // 5. RBAC demo
    fmt.Println("5. Role-Based Access Control:")
    rbac := NewRBAC()
    
    permissions := []Permission{PermissionUserRead, PermissionAdminWrite}
    for _, perm := range permissions {
        fmt.Printf("Role 'admin' has '%s': %v\n", perm, rbac.HasPermission("admin", perm))
        fmt.Printf("Role 'viewer' has '%s': %v\n", perm, rbac.HasPermission("viewer", perm))
    }
    fmt.Println()
    
    // 6. Secure headers
    fmt.Println("6. Security Headers Configuration:")
    headers := &SecurityHeaders{}
    fmt.Println("Security headers middleware created")
    fmt.Println("- X-Content-Type-Options: nosniff")
    fmt.Println("- X-Frame-Options: DENY")
    fmt.Println("- X-XSS-Protection: 1; mode=block")
    fmt.Println("- Content-Security-Policy: configured")
    fmt.Println("- Strict-Transport-Security: 1 year")
    fmt.Println()
    
    // 7. Rate limiting demo
    fmt.Println("7. Rate Limiting:")
    rateLimiter := NewRateLimiter()
    
    for i := 1; i <= 6; i++ {
        allowed := rateLimiter.Check("test_user", 5, time.Minute)
        fmt.Printf("Attempt %d: %v\n", i, allowed)
    }
    fmt.Println()
    
    // 8. Start demo server
    fmt.Println("=== Starting Secure Demo Server ===")
    
    // Create auth system
    authSystem := NewAuthSystem(
        "jwt-super-secret-key",
        "session-secret-key-32-chars-long",
        "password-pepper-secret",
    )
    
    // Setup routes
    mux := http.NewServeMux()
    authSystem.RegisterRoutes(mux)
    
    // Add security middleware
    handler := &SecurityHeaders{}
    handler = handler.Middleware(mux)
    handler = authSystem.AuthMiddleware(handler)
    
    // Start server
    go func() {
        fmt.Println("Demo server running on http://localhost:8081")
        fmt.Println("Available endpoints:")
        fmt.Println("  POST /api/register")
        fmt.Println("  POST /api/login")
        fmt.Println("  POST /api/logout")
        fmt.Println("  POST /api/refresh")
        fmt.Println("  GET  /api/me (requires auth)")
        fmt.Println("\nPress Ctrl+C to exit")
        
        // For demo purposes, use HTTP. In production, ALWAYS use HTTPS
        http.ListenAndServe(":8081", handler)
    }()
    
    // Keep main running
    select {}
}

// Required imports and stubs for compilation
import (
    "crypto/tls"
    "sync"
    "github.com/gorilla/sessions"
    "github.com/microcosm-cc/bluemonday"
)

var sessionStore sessions.Store = sessions.NewCookieStore([]byte("demo-secret"))
var validator = &InputValidator{}

func init() {
    // Initialize session store
    store := sessions.NewCookieStore([]byte("test-secret-key-32-chars-long"))
    store.Options = &sessions.Options{
        Path:     "/",
        MaxAge:   86400 * 7,
        HttpOnly: true,
        Secure:   false, // false for HTTP demo
        SameSite: http.SameSiteLaxMode,
    }
    sessionStore = store
}