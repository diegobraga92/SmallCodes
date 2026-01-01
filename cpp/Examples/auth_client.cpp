// SecureStorage.h
#pragma once
#include <string>
#include <vector>
#include <memory>

// Platform-specific secure storage
#ifdef _WIN32
#include <windows.h>
#include <dpapi.h>
#include <wincrypt.h>
#elif __linux__
#include <gnutls/gnutls.h>
#include <libsecret/secret.h>
#endif

class SecureStorage {
public:
    static SecureStorage& GetInstance();
    
    bool StoreToken(const std::string& key, const std::string& token);
    std::string RetrieveToken(const std::string& key);
    bool DeleteToken(const std::string& key);
    void ClearAllTokens();
    
    // Key generation/management
    std::string GenerateRandomBytes(size_t length);
    std::string DeriveKeyFromPassword(const std::string& password, 
                                     const std::string& salt);
    
private:
    SecureStorage();
    ~SecureStorage();
    
#ifdef _WIN32
    bool ProtectData(const std::vector<byte>& data, 
                    std::vector<byte>& encrypted);
    bool UnprotectData(const std::vector<byte>& encrypted,
                      std::vector<byte>& data);
    HCRYPTPROV hCryptProv{0};
#elif __linux__
    SecretService* secretService{nullptr};
#endif
    
    std::string GetStoragePath() const;
};

// SecureHttpClient.h
#pragma once
#include <string>
#include <map>
#include <functional>
#include <memory>
#include <curl/curl.h>
#include <openssl/ssl.h>

struct HttpRequest {
    std::string url;
    std::string method = "GET";
    std::map<std::string, std::string> headers;
    std::string body;
    int timeout = 30;
    bool verifySSL = true;
    std::string clientCertPath;
    std::string clientKeyPath;
    std::string caBundlePath;
};

struct HttpResponse {
    int statusCode{0};
    std::string body;
    std::map<std::string, std::string> headers;
    std::string error;
    long responseTime{0};
};

class SecureHttpClient {
public:
    SecureHttpClient();
    ~SecureHttpClient();
    
    // Authentication methods
    HttpResponse Login(const std::string& username, 
                      const std::string& password);
    HttpResponse RefreshToken(const std::string& refreshToken);
    HttpResponse Logout();
    
    // Authenticated requests
    HttpResponse Get(const std::string& url, 
                    const std::map<std::string, std::string>& headers = {});
    HttpResponse Post(const std::string& url, const std::string& body,
                     const std::map<std::string, std::string>& headers = {});
    
    // Token management
    void SetAccessToken(const std::string& token);
    void ClearTokens();
    
    // SSL/TLS configuration
    bool SetCertificateAuthority(const std::string& caPath);
    bool SetClientCertificate(const std::string& certPath, 
                             const std::string& keyPath);
    
    // Certificate pinning
    void EnableCertificatePinning(const std::string& expectedFingerprint);
    
private:
    CURL* curlHandle{nullptr};
    std::string accessToken;
    std::string refreshToken;
    std::string apiBaseUrl = "https://api.example.com";
    
    // SSL/TLS settings
    std::string caBundlePath;
    std::string clientCertPath;
    std::string clientKeyPath;
    std::string pinnedCertFingerprint;
    
    HttpResponse ExecuteRequest(const HttpRequest& request);
    static size_t WriteCallback(void* contents, size_t size, 
                               size_t nmemb, void* userp);
    static size_t HeaderCallback(char* buffer, size_t size,
                                size_t nitems, void* userdata);
    
    // Security helpers
    std::string EncryptSensitiveData(const std::string& data);
    bool ValidateServerCertificate(CURL* curl);
    
    // Token auto-refresh
    bool IsTokenExpired() const;
    bool RefreshAccessToken();
};

// JwtHandler.h
#pragma once
#include <string>
#include <map>
#include <chrono>
#include <jwt-cpp/jwt.h>

struct JwtClaims {
    std::string subject;
    std::string issuer;
    std::chrono::system_clock::time_point expiration;
    std::chrono::system_clock::time_point issuedAt;
    std::map<std::string, std::string> customClaims;
};

class JwtHandler {
public:
    JwtHandler();
    
    // Token parsing and validation
    bool ParseToken(const std::string& token);
    bool ValidateToken(const std::string& token, 
                      const std::string& expectedIssuer = "");
    
    // Claim accessors
    std::string GetSubject() const;
    std::string GetIssuer() const;
    bool IsExpired() const;
    std::chrono::system_clock::time_point GetExpiration() const;
    std::map<std::string, std::string> GetAllClaims() const;
    
    // Utility
    static std::string Base64UrlEncode(const std::string& data);
    static std::string Base64UrlDecode(const std::string& data);
    
    // For local verification (if using symmetric key)
    void SetVerificationKey(const std::string& key);
    
private:
    JwtClaims claims;
    std::string verificationKey;
    bool parsed{false};
    
    bool VerifySignature(const std::string& token);
    void ExtractClaims(const jwt::decoded_jwt<jwt::traits::kazuho_picojson>& decoded);
};

// AuthManager.h
#pragma once
#include "SecureHttpClient.h"
#include "JwtHandler.h"
#include "SecureStorage.h"
#include <memory>
#include <functional>

enum class AuthState {
    NOT_AUTHENTICATED,
    AUTHENTICATING,
    AUTHENTICATED,
    TOKEN_EXPIRED,
    ERROR
};

class AuthManager {
public:
    using AuthCallback = std::function<void(AuthState, const std::string&)>;
    
    static AuthManager& GetInstance();
    
    // Authentication methods
    void Login(const std::string& username, const std::string& password,
               AuthCallback callback = nullptr);
    void Logout();
    void RefreshTokenAsync(AuthCallback callback = nullptr);
    
    // State management
    AuthState GetState() const { return currentState; }
    bool IsAuthenticated() const { return currentState == AuthState::AUTHENTICATED; }
    std::string GetUsername() const { return username; }
    
    // Token management
    std::string GetAccessToken() const;
    bool ValidateCurrentToken() const;
    
    // Auto-refresh thread
    void StartAutoRefresh(int checkIntervalSeconds = 300);
    void StopAutoRefresh();
    
    // Configuration
    void SetApiEndpoint(const std::string& endpoint);
    void SetSessionTimeout(int seconds) { sessionTimeout = seconds; }
    
private:
    AuthManager();
    ~AuthManager();
    
    AuthState currentState{AuthState::NOT_AUTHENTICATED};
    std::string username;
    std::string accessToken;
    std::string refreshToken;
    
    std::unique_ptr<SecureHttpClient> httpClient;
    std::unique_ptr<JwtHandler> jwtHandler;
    std::unique_ptr<SecureStorage> secureStorage;
    
    // Auto-refresh thread
    std::thread refreshThread;
    std::atomic<bool> stopRefreshThread{false};
    int sessionTimeout{3600}; // 1 hour
    
    void LoadStoredCredentials();
    void SaveCredentials();
    void ClearStoredCredentials();
    
    void HandleLoginResponse(const HttpResponse& response, AuthCallback callback);
    void HandleRefreshResponse(const HttpResponse& response, AuthCallback callback);
    
    // Thread functions
    void AutoRefreshWorker(int checkInterval);
};

// Example client usage
int main() {
    AuthManager& auth = AuthManager::GetInstance();
    auth.SetApiEndpoint("https://api.yourservice.com");
    
    // Login
    auth.Login("username", "password", 
        [](AuthState state, const std::string& message) {
            if (state == AuthState::AUTHENTICATED) {
                // Fetch user data
                SecureHttpClient client;
                auto response = client.Get("/api/data/user");
                
                if (response.statusCode == 200) {
                    // Process secure data
                    ProcessUserData(response.body);
                }
            }
        });
    
    // Start auto-refresh
    auth.StartAutoRefresh();
    
    // Main application loop...
    
    return 0;
}