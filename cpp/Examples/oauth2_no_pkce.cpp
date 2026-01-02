#include <string>

class OAuth2ClientPrePKCE {
private:
    std::string clientId;
    std::string clientSecret;  // Problematic for mobile apps!
    
public:
    // STEP 1: Get authorization URL (NO code_challenge)
    std::string getAuthorizationUrl() {
        return "https://auth.server/authorize?" +
               "response_type=code&" +
               "client_id=" + clientId + "&" +
               "redirect_uri=myapp://callback&" +
               "state=" + generateState();
        // MISSING: code_challenge parameter!
    }
    
    // STEP 2: Exchange code for token
    TokenResponse exchangeCode(const std::string& authCode) {
        // Problem: Mobile apps can't securely store client_secret!
        std::string body = 
            "grant_type=authorization_code&" +
            "code=" + authCode + "&" +
            "redirect_uri=myapp://callback&" +
            "client_id=" + clientId + "&" +
            "client_secret=" + clientSecret;  // UNSECURE!
        
        return postToTokenEndpoint(body);
    }
};