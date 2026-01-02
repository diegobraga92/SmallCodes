// API.h - Public header for library users
#pragma once
#include <memory>

// Forward declaration to hide implementation details
class APIImpl;

class MyAPI {
public:
    // Constructor/Destructor - crucial for ABI stability
    MyAPI();
    ~MyAPI();
    
    // Copy operations - explicitly define or delete
    MyAPI(const MyAPI&) = delete;
    MyAPI& operator=(const MyAPI&) = delete;
    
    // Move operations for modern C++
    MyAPI(MyAPI&&) noexcept;
    MyAPI& operator=(MyAPI&&) noexcept;
    
    // Public API - keep stable once released
    // 1. Never change function signatures
    // 2. Only add new functions at the end
    // 3. Don't remove existing functions (deprecate instead)
    
    // Version 1.0 functions
    void processData(const std::string& input);
    int calculateValue(int x, int y) const;
    
    // Version 1.1 - ADDED, never modified existing
    std::string getResult() const;
    
    // Version 1.2 - ADDED with default parameter
    // Default parameters added only at the end
    void configure(bool enableFeature = true, int timeout = 1000);
    
    // Deprecation example
    [[deprecated("Use newProcessData() instead")]]
    void oldProcessData(const std::string& input);
    
private:
    // PIMPL - Pointer to Implementation
    // This hides implementation details and ensures ABI stability
    std::unique_ptr<APIImpl> pImpl;
};

// APIImpl.cpp - Implementation file
class APIImpl {
public:
    void processData(const std::string& input) {
        // Actual implementation
        data = input;
        transformData();
    }
    
    int calculateValue(int x, int y) const {
        return x * y + offset;
    }
    
    std::string getResult() const {
        return processedData;
    }
    
    void configure(bool enableFeature, int timeout) {
        featureEnabled = enableFeature;
        this->timeout = timeout;
    }
    
private:
    std::string data;
    std::string processedData;
    bool featureEnabled = false;
    int timeout = 1000;
    int offset = 42;
    
    void transformData() {
        processedData = "Processed: " + data;
    }
};

// MyAPI implementation using PIMPL
MyAPI::MyAPI() : pImpl(std::make_unique<APIImpl>()) {}

MyAPI::~MyAPI() = default; // Required for unique_ptr with incomplete type

MyAPI::MyAPI(MyAPI&&) noexcept = default;
MyAPI& MyAPI::operator=(MyAPI&&) noexcept = default;

void MyAPI::processData(const std::string& input) {
    pImpl->processData(input);
}

int MyAPI::calculateValue(int x, int y) const {
    return pImpl->calculateValue(x, y);
}

std::string MyAPI::getResult() const {
    return pImpl->getResult();
}

void MyAPI::configure(bool enableFeature, int timeout) {
    pImpl->configure(enableFeature, timeout);
}

void MyAPI::oldProcessData(const std::string& input) {
    // Legacy implementation
    processData(input); // Forward to new implementation
}



// VersionInfo.h - Semantic versioning utilities
#pragma once
#include <string>
#include <cstdint>

struct Version {
    uint32_t major;
    uint32_t minor;
    uint32_t patch;
    std::string prerelease;
    std::string build;
    
    // Semantic versioning comparison
    bool operator==(const Version& other) const {
        return major == other.major &&
               minor == other.minor &&
               patch == other.patch &&
               prerelease == other.prerelease;
    }
    
    bool operator<(const Version& other) const {
        if (major != other.major) return major < other.major;
        if (minor != other.minor) return minor < other.minor;
        if (patch != other.patch) return patch < other.patch;
        return prerelease < other.prerelease; // Pre-release comparison
    }
    
    std::string toString() const {
        std::string result = std::to_string(major) + "." +
                            std::to_string(minor) + "." +
                            std::to_string(patch);
        if (!prerelease.empty()) {
            result += "-" + prerelease;
        }
        if (!build.empty()) {
            result += "+" + build;
        }
        return result;
    }
    
    // API compatibility checks
    bool isBackwardCompatibleWith(const Version& other) const {
        // Same major version means backward compatible
        return major == other.major && *this >= other;
    }
    
    bool isSourceCompatibleWith(const Version& other) const {
        // Same major version, minor >= other.minor
        return major == other.major && 
               (minor > other.minor || (minor == other.minor && patch >= other.patch));
    }
};

class APIVersion {
public:
    // Current API version
    static constexpr Version CURRENT_VERSION = {2, 1, 3, "beta", "build123"};
    
    // Minimum supported version
    static constexpr Version MIN_SUPPORTED = {1, 0, 0};
    
    // Check if client version is compatible
    static bool isCompatible(const Version& clientVersion) {
        // Major version must match exactly for ABI compatibility
        if (clientVersion.major != CURRENT_VERSION.major) {
            return false;
        }
        
        // Client must not be newer than current
        if (clientVersion > CURRENT_VERSION) {
            return false;
        }
        
        // Client must be at least minimum supported
        return clientVersion >= MIN_SUPPORTED;
    }
    
    // Get API features based on version
    static bool supportsFeature(const std::string& feature, const Version& version) {
        // Feature availability matrix
        static const std::unordered_map<std::string, Version> featureMatrix = {
            {"async_processing", {2, 0, 0}},
            {"encryption", {1, 5, 0}},
            {"compression", {1, 2, 0}},
            {"multithreading", {2, 1, 0}}
        };
        
        auto it = featureMatrix.find(feature);
        if (it != featureMatrix.end()) {
            return version >= it->second;
        }
        return false;
    }
    
    // Version negotiation
    static Version negotiateVersion(const Version& requested) {
        Version result = CURRENT_VERSION;
        
        // Downgrade to requested major version if supported
        if (requested.major < CURRENT_VERSION.major) {
            // Find latest patch in requested major version
            if (requested.major == 1) {
                result = {1, 5, 2}; // Latest v1.x release
            }
        } else if (requested.major == CURRENT_VERSION.major) {
            // Same major version, use requested or current (whichever is lower)
            result = (requested < CURRENT_VERSION) ? requested : CURRENT_VERSION;
        }
        
        return result;
    }
};

// Usage example
void demonstrateVersioning() {
    Version v1 = {1, 0, 0};
    Version v2 = {2, 0, 0};
    
    std::cout << "v1: " << v1.toString() << std::endl;
    std::cout << "v2: " << v2.toString() << std::endl;
    
    if (v1 < v2) {
        std::cout << "v1 is older than v2" << std::endl;
    }
    
    if (APIVersion::isCompatible(v1)) {
        std::cout << "v1 is compatible with current API" << std::endl;
    }
    
    if (APIVersion::supportsFeature("encryption", v1)) {
        std::cout << "v1 supports encryption" << std::endl;
    }
}


// GoodStyle.hpp - Demonstrating good C++ coding style
#pragma once

#include <string>
#include <vector>
#include <memory>
#include <functional>
#include <algorithm>
#include <cstdint>

// ===================== NAMING CONVENTIONS =====================

// PascalCase for types (classes, structs, enums, type aliases)
class NetworkConnection {
    // ...
};

struct UserPreferences {
    // ...
};

enum class ConnectionState {
    Disconnected,
    Connecting,
    Connected,
    Error
};

using UserId = uint64_t;          // PascalCase for type aliases
using Callback = std::function<void()>;

// camelCase for functions and methods
class DataProcessor {
public:
    void processData() {          // camelCase for methods
        loadConfiguration();      // camelCase for private methods
        validateInput();
        transformData();
        storeResults();
    }
    
    int calculateValue() const {  // camelCase for getters that compute
        return cachedValue * multiplier;
    }
    
    // snake_case is also acceptable (common in C++ standard library)
    void process_data() {         // snake_case alternative
        load_configuration();
    }
    
private:
    void loadConfiguration() { /* ... */ }
    void load_configuration() { /* ... */ }
};

// camelCase for variables (member and local)
class UserManager {
private:
    std::string userName;         // camelCase for member variables
    int connectionTimeout = 5000; // camelCase with meaningful names
    bool isAuthenticated = false; // Boolean prefix: is, has, can, should
    
public:
    void authenticateUser(const std::string& username, const std::string& password) {
        // camelCase for local variables
        bool isValid = validateCredentials(username, password);
        int retryCount = 0;
        
        while (!isValid && retryCount < maxRetryCount) {
            // Avoid single-letter variables except in loops
            for (size_t i = 0; i < attempts.size(); ++i) {
                // i, j, k acceptable for loop indices
                processAttempt(attempts[i]);
            }
            retryCount++;
        }
    }
    
private:
    bool validateCredentials(const std::string& user, const std::string& pass) {
        // Use descriptive parameter names
        return !user.empty() && !pass.empty();
    }
};

// UPPER_CASE for constants (global and class constants)
constexpr int MAX_CONNECTIONS = 100;          // Global constant
constexpr double PI = 3.141592653589793;

class PhysicsEngine {
public:
    static constexpr double GRAVITY = 9.81;   // Class constant
    static constexpr int MAX_ITERATIONS = 1000;
    
private:
    static constexpr float FRICTION_COEFFICIENT = 0.85f;
};

// kConstant alternative (Google style)
constexpr int kDefaultPort = 8080;
constexpr int kMaxRetryAttempts = 3;

// ===================== AVOIDING ABBREVIATIONS =====================

// GOOD: Clear, unambiguous names
class ConfigurationManager {      // NOT: ConfigMgr
public:
    void loadUserPreferences() {  // NOT: loadUsrPrefs
        // ...
    }
    
    int calculateAverageValue() { // NOT: calcAvgVal
        return totalValue / count;
    }
    
private:
    std::string temporaryDirectory; // NOT: tempDir
    bool hasConfigurationChanged;   // NOT: configChanged
};

// ACCEPTABLE: Standard abbreviations
class XMLParser {                 // XML is standard
    void parseHTML() {            // HTML is standard
        // ...
    }
    
    void saveToCSV() {            // CSV is standard
        // ...
    }
    
    void encodeURL() {            // URL is standard
        // ...
    }
    
    void calculateCPUUsage() {    // CPU is standard
        // ...
    }
    
    void sendHTTPRequest() {      // HTTP is standard
        // ...
    }
};

// ===================== CONSISTENT FORMATTING =====================

class FormattedClass {
public:
    // Consistent indentation (4 spaces recommended)
    void properlyFormattedMethod(int parameter1, 
                                 const std::string& parameter2,
                                 bool flag = true) {
        
        // Braces on same line for control structures
        if (condition) {
            executeAction();
        } else {
            handleAlternative();
        }
        
        // Spaces around operators
        int result = (value1 + value2) * factor;
        
        // Spaces after commas
        std::vector<int> numbers = {1, 2, 3, 4, 5};
        
        // Limit line length (80-120 characters)
        // This is a very long comment that explains something complex
        // about the implementation details of this particular method
        // and why certain design decisions were made.
    }
    
private:
    // Group related members together
    // Configuration
    int timeout = 5000;
    int maxRetries = 3;
    
    // State
    bool isInitialized = false;
    ConnectionState state = ConnectionState::Disconnected;
    
    // Resources
    std::unique_ptr<NetworkConnection> connection;
    std::vector<UserSession> activeSessions;
};

// ===================== MEANINGFUL COMMENTS =====================

/**
 * @class DatabaseConnection
 * @brief Manages connections to the database with connection pooling
 * 
 * This class provides thread-safe database connection management
 * with automatic connection pooling and health checking.
 * 
 * @note All public methods are thread-safe unless otherwise noted
 */
class DatabaseConnection {
public:
    /**
     * @brief Establishes a connection to the database
     * @param connectionString The connection string in format: 
     *                         "host=localhost;port=5432;database=test"
     * @param maxConnections Maximum number of connections in pool
     * @throws DatabaseException if connection cannot be established
     * 
     * @details The connection pool is initialized lazily on first use.
     * Each thread gets its own connection from the pool.
     */
    void initialize(const std::string& connectionString, 
                    int maxConnections = 10);
    
    /**
     * @brief Executes a SQL query
     * @param query The SQL query to execute
     * @param parameters Query parameters (optional)
     * @return QueryResult containing the results
     * 
     * @warning This method is not thread-safe when called from multiple
     *          threads with the same connection. Use separate connections
     *          or add synchronization.
     */
    QueryResult executeQuery(const std::string& query,
                            const std::vector<Parameter>& parameters = {});
    
private:
    // Cache size in megabytes - tunable based on available memory
    static constexpr size_t CACHE_SIZE_MB = 256;
    
    // Connection pool mutex - protects pool access
    std::mutex poolMutex;
    
    // TODO: Implement connection health checking
    // FIXME: Memory leak detected when connection fails
    // NOTE: This assumes UTF-8 encoding for all strings
};

// ===================== FUNCTION DESIGN =====================

// Good: Small, focused functions with single responsibility
class OrderProcessor {
public:
    // GOOD: Clear name, single responsibility
    double calculateTotalPrice(const Order& order) {
        double subtotal = calculateSubtotal(order.items);
        double tax = calculateTax(subtotal, order.taxRate);
        double shipping = calculateShippingCost(order.destination);
        return subtotal + tax + shipping;
    }
    
private:
    // GOOD: Helper functions for each calculation
    double calculateSubtotal(const std::vector<Item>& items) {
        return std::accumulate(items.begin(), items.end(), 0.0,
            [](double sum, const Item& item) {
                return sum + item.price * item.quantity;
            });
    }
    
    double calculateTax(double amount, double taxRate) {
        return amount * taxRate;
    }
    
    double calculateShippingCost(const Address& destination) {
        if (destination.country == "Local") {
            return STANDARD_SHIPPING;
        } else {
            return INTERNATIONAL_SHIPPING;
        }
    }
    
    // BAD: Too many responsibilities
    double processOrderBad(const Order& order) {
        // Calculates price
        double total = 0;
        for (const auto& item : order.items) {
            total += item.price * item.quantity;
        }
        
        // Applies discount
        if (order.customer.isPremium) {
            total *= 0.9;
        }
        
        // Validates address
        if (!isValidAddress(order.destination)) {
            throw InvalidAddressException();
        }
        
        // Too much in one function!
        return total;
    }
};

// ===================== MODERN C++ FEATURES =====================

class ModernStyle {
public:
    // Use auto when type is obvious from context
    auto processItems(const std::vector<Item>& items) {
        auto processed = std::vector<ProcessedItem>();
        processed.reserve(items.size());
        
        // Range-based for loops
        for (const auto& item : items) {
            processed.push_back(processItem(item));
        }
        
        return processed;  // Return type deduction
    }
    
    // Use constexpr for compile-time evaluation
    constexpr size_t calculateBufferSize(size_t elementCount) {
        return elementCount * sizeof(Element) + HEADER_SIZE;
    }
    
    // Use noexcept when appropriate
    void clear() noexcept {
        data.clear();
        size = 0;
    }
    
private:
    // Use smart pointers for ownership
    std::unique_ptr<Resource> resource;
    std::shared_ptr<Logger> logger;
    
    // Use std::array for fixed-size arrays
    std::array<int, 100> buffer;
    
    // Use std::optional for optional values
    std::optional<std::string> cachedValue;
};



// SecureCoding.hpp - Security best practices in C++
#pragma once

#include <array>
#include <vector>
#include <string>
#include <memory>
#include <limits>
#include <stdexcept>
#include <cstring>
#include <cstdint>

// ===================== BUFFER OVERFLOW PREVENTION =====================

class SecureBuffer {
public:
    // SAFE: Use std::vector or std::array instead of raw arrays
    void processDataSafe(const std::vector<uint8_t>& input) {
        std::vector<uint8_t> buffer(input.size() + HEADER_SIZE);
        
        // Bounds-checked access
        for (size_t i = 0; i < input.size(); ++i) {
            buffer[i + HEADER_SIZE] = input[i];  // Automatic bounds checking
        }
        
        // Use at() for explicit bounds checking
        try {
            buffer.at(buffer.size() - 1) = 0xFF;
        } catch (const std::out_of_range& e) {
            handleError("Buffer overflow prevented");
        }
    }
    
    // UNSAFE: Raw arrays without bounds checking
    void processDataUnsafe(const uint8_t* input, size_t size) {
        uint8_t buffer[256];  // Fixed-size buffer - DANGEROUS
        
        // Potential buffer overflow
        for (size_t i = 0; i < size; ++i) {
            buffer[i] = input[i];  // NO bounds checking!
        }
    }
    
    // SAFE ALTERNATIVE: Use std::array with bounds checking
    void processDataFixedSize(const std::array<uint8_t, 256>& input) {
        std::array<uint8_t, 512> buffer{};  // Zero-initialized
        
        // Compile-time size checking
        static_assert(buffer.size() >= input.size(), 
                     "Buffer too small for input");
        
        std::copy(input.begin(), input.end(), buffer.begin());
    }
    
    // SAFE: String handling with std::string
    void handleStringsSafely(const std::string& input) {
        std::string output;
        output.reserve(input.size() * 2);  // Prevent reallocations
        
        // Safe string operations
        output = "Prefix: " + input + " :Suffix";
        
        // Access with bounds checking
        if (!output.empty()) {
            char first = output.at(0);  // Throws if out of bounds
            char last = output.back();  // Bounds-checked
        }
    }
    
    // UNSAFE: C-style strings
    void handleStringsUnsafe(const char* input) {
        char buffer[100];
        
        // DANGEROUS: No bounds checking
        strcpy(buffer, input);  // Potential buffer overflow!
        
        // Still dangerous
        strncpy(buffer, input, sizeof(buffer));  
        // strncpy doesn't null-terminate if input is too long
        buffer[sizeof(buffer) - 1] = '\0';  // Manual termination needed
    }
    
    // SAFE ALTERNATIVE: Use strncpy_s or custom safe functions
    void copyStringSafely(const char* src, char* dest, size_t destSize) {
        if (destSize == 0) return;
        
        size_t i;
        for (i = 0; i < destSize - 1 && src[i] != '\0'; ++i) {
            dest[i] = src[i];
        }
        dest[i] = '\0';  // Always null-terminate
    }

private:
    static constexpr size_t HEADER_SIZE = 16;
};

// ===================== INTEGER OVERFLOW PREVENTION =====================

class SafeIntegerOperations {
public:
    // UNSAFE: Direct operations can overflow
    int unsafeAdd(int a, int b) {
        return a + b;  // Potential overflow
    }
    
    // SAFE: Check before operation
    int safeAdd(int a, int b) {
        // Check for positive overflow
        if (a > 0 && b > std::numeric_limits<int>::max() - a) {
            throw std::overflow_error("Integer overflow in addition");
        }
        
        // Check for negative overflow
        if (a < 0 && b < std::numeric_limits<int>::min() - a) {
            throw std::overflow_error("Integer underflow in addition");
        }
        
        return a + b;
    }
    
    // SAFE: Use wider types
    int64_t safeMultiply(int32_t a, int32_t b) {
        // Perform in wider type
        int64_t result = static_cast<int64_t>(a) * static_cast<int64_t>(b);
        
        // Check if result fits in int32_t
        if (result < std::numeric_limits<int32_t>::min() || 
            result > std::numeric_limits<int32_t>::max()) {
            throw std::overflow_error("Multiplication overflow");
        }
        
        return static_cast<int32_t>(result);
    }
    
    // SAFE: Use unsigned integers with well-defined overflow
    uint32_t safeRotateLeft(uint32_t value, uint32_t shift) {
        shift %= 32;  // Ensure shift is in range
        return (value << shift) | (value >> (32 - shift));
    }
    
    // SAFE: Size calculations with overflow check
    size_t calculateAllocationSize(size_t count, size_t elementSize) {
        // Check for overflow in multiplication
        if (elementSize != 0 && count > std::numeric_limits<size_t>::max() / elementSize) {
            throw std::bad_alloc();
        }
        
        size_t total = count * elementSize;
        
        // Add overhead with overflow check
        constexpr size_t OVERHEAD = sizeof(void*) * 2;
        if (total > std::numeric_limits<size_t>::max() - OVERHEAD) {
            throw std::bad_alloc();
        }
        
        return total + OVERHEAD;
    }
    
    // SAFE: Array indexing with bounds checking
    template<typename T>
    T& safeArrayAccess(std::vector<T>& vec, ptrdiff_t index) {
        if (index < 0 || static_cast<size_t>(index) >= vec.size()) {
            throw std::out_of_range("Array index out of bounds");
        }
        return vec[static_cast<size_t>(index)];
    }
};

// ===================== SECURE MEMORY HANDLING =====================

class SecureMemory {
public:
    // SAFE: Use smart pointers for automatic cleanup
    void safeMemoryManagement() {
        auto data = std::make_unique<uint8_t[]>(1024);
        // Memory automatically freed when 'data' goes out of scope
        // Even if exception is thrown
        
        fillData(data.get(), 1024);
        processData(data.get(), 1024);
        
        // No need to manually delete
    }
    
    // UNSAFE: Manual memory management
    void unsafeMemoryManagement() {
        uint8_t* data = new uint8_t[1024];
        
        try {
            fillData(data, 1024);
            processData(data, 1024);
        } catch (...) {
            delete[] data;  // Must remember to delete in all paths
            throw;
        }
        
        delete[] data;  // Easy to forget
    }
    
    // SAFE: Zero memory after use (for sensitive data)
    class SecureBuffer {
    public:
        SecureBuffer(size_t size) : data(new uint8_t[size]), size(size) {
            std::fill(data.get(), data.get() + size, 0);
        }
        
        ~SecureBuffer() {
            // Zero memory before freeing
            if (data) {
                secureZeroMemory(data.get(), size);
            }
        }
        
        // Delete copy operations to prevent accidental copies
        SecureBuffer(const SecureBuffer&) = delete;
        SecureBuffer& operator=(const SecureBuffer&) = delete;
        
        // Allow move operations
        SecureBuffer(SecureBuffer&&) = default;
        SecureBuffer& operator=(SecureBuffer&&) = default;
        
    private:
        std::unique_ptr<uint8_t[]> data;
        size_t size;
        
        static void secureZeroMemory(void* ptr, size_t size) {
            volatile uint8_t* p = static_cast<volatile uint8_t*>(ptr);
            while (size--) {
                *p++ = 0;
            }
        }
    };
    
    // SAFE: Input validation
    void processUserInput(const std::string& input) {
        // Validate input length
        constexpr size_t MAX_INPUT_SIZE = 1024;
        if (input.size() > MAX_INPUT_SIZE) {
            throw std::invalid_argument("Input too long");
        }
        
        // Validate content (example: no control characters)
        for (char c : input) {
            if (std::iscntrl(static_cast<unsigned char>(c))) {
                throw std::invalid_argument("Input contains control characters");
            }
        }
        
        // Validate format
        if (!isValidFormat(input)) {
            throw std::invalid_argument("Invalid input format");
        }
        
        // Process validated input
        safeProcess(input);
    }
    
private:
    void fillData(uint8_t* data, size_t size) {
        std::fill(data, data + size, 0xAA);
    }
    
    void processData(uint8_t* data, size_t size) {
        // Process data
    }
    
    bool isValidFormat(const std::string& input) {
        // Implementation-specific validation
        return !input.empty();
    }
    
    void safeProcess(const std::string& input) {
        // Process safe input
    }
};

// ===================== SECURE RANDOM NUMBERS =====================

#include <random>

class SecureRandom {
public:
    // UNSAFE: rand() is predictable and not cryptographically secure
    int unsafeRandom(int min, int max) {
        return min + (std::rand() % (max - min + 1));  // NOT SECURE
    }
    
    // SAFE: Use <random> with proper distributions
    int safeRandom(int min, int max) {
        std::random_device rd;  // Hardware entropy source
        std::mt19937_64 gen(rd());  // Mersenne Twister engine
        std::uniform_int_distribution<int> dist(min, max);
        
        return dist(gen);
    }
    
    // CRYPTOGRAPHICALLY SECURE: For security-sensitive applications
    class CryptographicRandom {
    public:
        CryptographicRandom() {
            // Seed with system entropy
            std::random_device rd;
            std::seed_seq seed{rd(), rd(), rd(), rd()};
            gen.seed(seed);
        }
        
        void generateSecureBytes(uint8_t* buffer, size_t size) {
            std::uniform_int_distribution<uint16_t> dist(0, 255);
            
            for (size_t i = 0; i < size; ++i) {
                buffer[i] = static_cast<uint8_t>(dist(gen));
            }
        }
        
        uint64_t generateSecureNumber() {
            std::uniform_int_distribution<uint64_t> dist;
            return dist(gen);
        }
        
    private:
        std::mt19937_64 gen;  // Consider using a cryptographic RNG for production
    };
};

// ===================== SECURE STRING HANDLING =====================

class SecureStringHandling {
public:
    // SAFE: Prevent format string vulnerabilities
    void safeFormatting() {
        std::string userInput = getUserInput();
        
        // BAD: User input in format string
        // printf(userInput.c_str());  // FORMAT STRING VULNERABILITY!
        
        // GOOD: Use fixed format strings
        std::cout << "User entered: " << userInput << std::endl;
        
        // GOOD: Use type-safe formatting
        std::cout << std::format("User entered: {}", userInput) << std::endl;
    }
    
    // SAFE: SQL injection prevention
    class DatabaseQuery {
    public:
        // UNSAFE: String concatenation
        std::string unsafeQuery(const std::string& username) {
            return "SELECT * FROM users WHERE username = '" + username + "'";
            // SQL INJECTION if username contains '
        }
        
        // SAFE: Parameterized queries
        class SafeQuery {
        public:
            SafeQuery(const std::string& query) : baseQuery(query) {}
            
            void bind(const std::string& paramName, const std::string& value) {
                // Properly escape values
                std::string escaped = escapeString(value);
                parameters[paramName] = escaped;
            }
            
            std::string build() const {
                std::string result = baseQuery;
                for (const auto& [name, value] : parameters) {
                    replaceAll(result, ":" + name, value);
                }
                return result;
            }
            
        private:
            std::string baseQuery;
            std::unordered_map<std::string, std::string> parameters;
            
            std::string escapeString(const std::string& input) {
                std::string result;
                result.reserve(input.size() * 2);
                
                for (char c : input) {
                    switch (c) {
                        case '\'': result += "''"; break;
                        case '\\': result += "\\\\"; break;
                        default: result += c;
                    }
                }
                
                return "'" + result + "'";
            }
            
            void replaceAll(std::string& str, const std::string& from, 
                           const std::string& to) {
                size_t start_pos = 0;
                while ((start_pos = str.find(from, start_pos)) != std::string::npos) {
                    str.replace(start_pos, from.length(), to);
                    start_pos += to.length();
                }
            }
        };
    };
    
private:
    std::string getUserInput() {
        return "test input";
    }
};

// ===================== SECURE FILE HANDLING =====================

#include <fstream>
#include <filesystem>

class SecureFileHandling {
public:
    // SAFE: Validate file paths
    std::string safeOpenFile(const std::string& userPath) {
        namespace fs = std::filesystem;
        
        // Resolve path to prevent directory traversal
        fs::path requestedPath(userPath);
        fs::path baseDir("/var/data");
        fs::path fullPath = baseDir / requestedPath;
        
        // Canonicalize and check for directory traversal
        try {
            fs::path canonicalPath = fs::canonical(fullPath);
            
            // Ensure path is within base directory
            if (!isSubdirectory(canonicalPath, baseDir)) {
                throw std::invalid_argument("Path traversal attempt detected");
            }
            
            return canonicalPath.string();
        } catch (const fs::filesystem_error& e) {
            throw std::invalid_argument("Invalid file path");
        }
    }
    
    // SAFE: File operations with limits
    std::vector<uint8_t> readFileWithLimits(const std::string& path) {
        constexpr size_t MAX_FILE_SIZE = 10 * 1024 * 1024;  // 10 MB
        
        std::ifstream file(path, std::ios::binary | std::ios::ate);
        if (!file) {
            throw std::runtime_error("Cannot open file");
        }
        
        std::streamsize size = file.tellg();
        file.seekg(0, std::ios::beg);
        
        // Check file size limit
        if (size > MAX_FILE_SIZE) {
            throw std::runtime_error("File too large");
        }
        
        std::vector<uint8_t> buffer(size);
        if (!file.read(reinterpret_cast<char*>(buffer.data()), size)) {
            throw std::runtime_error("Error reading file");
        }
        
        return buffer;
    }
    
private:
    bool isSubdirectory(const std::filesystem::path& path, 
                       const std::filesystem::path& base) {
        auto rel = std::filesystem::relative(path, base);
        return !rel.empty() && rel.native()[0] != '.';
    }
};


// DependencyInjection.hpp - Dependency injection patterns in C++
#pragma once

#include <memory>
#include <functional>
#include <string>
#include <vector>
#include <unordered_map>
#include <iostream>

// ===================== WITHOUT DEPENDENCY INJECTION =====================

// Problem: Hard-coded dependencies
class HardcodedDatabase {
    // ...
};

class UserServiceWithoutDI {
private:
    HardcodedDatabase database;  // Hard-coded dependency
    std::string loggerType;      // Configuration hard-coded
    
public:
    UserServiceWithoutDI() 
        : loggerType("FileLogger") {  // Can't change without recompiling
        // Direct instantiation of dependencies
        database.connect("localhost:3306");
    }
    
    void createUser(const std::string& username) {
        // Can't test without actual database
        database.execute("INSERT INTO users VALUES ('" + username + "')");
        
        if (loggerType == "FileLogger") {
            // Can't test logging independently
            std::cout << "User created: " << username << std::endl;
        }
    }
};

// ===================== CONSTRUCTOR INJECTION =====================

// Define interfaces/abstract classes
class IDatabase {
public:
    virtual ~IDatabase() = default;
    virtual void connect(const std::string& connectionString) = 0;
    virtual void execute(const std::string& query) = 0;
    virtual std::vector<std::string> query(const std::string& query) = 0;
};

class ILogger {
public:
    virtual ~ILogger() = default;
    virtual void log(const std::string& message) = 0;
    virtual void error(const std::string& message) = 0;
};

// Concrete implementations
class MySQLDatabase : public IDatabase {
public:
    void connect(const std::string& connectionString) override {
        std::cout << "Connecting to MySQL: " << connectionString << std::endl;
    }
    
    void execute(const std::string& query) override {
        std::cout << "Executing MySQL query: " << query << std::endl;
    }
    
    std::vector<std::string> query(const std::string& query) override {
        std::cout << "Querying MySQL: " << query << std::endl;
        return {"result1", "result2"};
    }
};

class PostgresDatabase : public IDatabase {
public:
    void connect(const std::string& connectionString) override {
        std::cout << "Connecting to Postgres: " << connectionString << std::endl;
    }
    
    void execute(const std::string& query) override {
        std::cout << "Executing Postgres query: " << query << std::endl;
    }
    
    std::vector<std::string> query(const std::string& query) override {
        std::cout << "Querying Postgres: " << query << std::endl;
        return {"result1", "result2"};
    }
};

class FileLogger : public ILogger {
public:
    void log(const std::string& message) override {
        std::cout << "[LOG] " << message << std::endl;
    }
    
    void error(const std::string& message) override {
        std::cerr << "[ERROR] " << message << std::endl;
    }
};

class ConsoleLogger : public ILogger {
public:
    void log(const std::string& message) override {
        std::cout << ">> " << message << std::endl;
    }
    
    void error(const std::string& message) override {
        std::cerr << "!! ERROR: " << message << std::endl;
    }
};

// Service with constructor injection
class UserService {
private:
    std::shared_ptr<IDatabase> database;
    std::shared_ptr<ILogger> logger;
    
public:
    // Constructor injection: dependencies passed explicitly
    UserService(std::shared_ptr<IDatabase> db, 
                std::shared_ptr<ILogger> log)
        : database(std::move(db))
        , logger(std::move(log)) {
        
        if (!database) {
            throw std::invalid_argument("Database cannot be null");
        }
        if (!logger) {
            throw std::invalid_argument("Logger cannot be null");
        }
    }
    
    void createUser(const std::string& username) {
        logger->log("Creating user: " + username);
        
        try {
            database->execute("INSERT INTO users VALUES ('" + username + "')");
            logger->log("User created successfully: " + username);
        } catch (const std::exception& e) {
            logger->error("Failed to create user: " + std::string(e.what()));
            throw;
        }
    }
    
    std::vector<std::string> getUsers() {
        logger->log("Fetching all users");
        return database->query("SELECT username FROM users");
    }
    
    // Can change dependencies at runtime
    void setDatabase(std::shared_ptr<IDatabase> newDb) {
        database = std::move(newDb);
    }
    
    void setLogger(std::shared_ptr<ILogger> newLogger) {
        logger = std::move(newLogger);
    }
};

// ===================== SETTER INJECTION =====================

class OrderService {
private:
    std::shared_ptr<IDatabase> database;
    std::shared_ptr<ILogger> logger;
    std::shared_ptr<IPaymentProcessor> paymentProcessor;
    
public:
    OrderService() = default;
    
    // Setter injection (optional dependencies)
    void setDatabase(std::shared_ptr<IDatabase> db) {
        database = std::move(db);
    }
    
    void setLogger(std::shared_ptr<ILogger> log) {
        logger = std::move(log);
    }
    
    void setPaymentProcessor(std::shared_ptr<IPaymentProcessor> processor) {
        paymentProcessor = std::move(processor);
    }
    
    void validate() const {
        if (!database) {
            throw std::runtime_error("Database not configured");
        }
        if (!logger) {
            throw std::runtime_error("Logger not configured");
        }
        // paymentProcessor is optional
    }
    
    void processOrder(const Order& order) {
        validate();
        
        logger->log("Processing order: " + order.id);
        database->execute("INSERT INTO orders ...");
        
        if (paymentProcessor) {
            paymentProcessor->processPayment(order.total);
        } else {
            logger->log("No payment processor configured");
        }
    }
};

// ===================== INTERFACE INJECTION =====================

class IConfigurable {
public:
    virtual ~IConfigurable() = default;
    virtual void configure(const std::string& key, const std::string& value) = 0;
    virtual std::string getConfiguration(const std::string& key) const = 0;
};

class ConfigurableService : public IConfigurable {
private:
    std::unordered_map<std::string, std::string> config;
    
public:
    void configure(const std::string& key, const std::string& value) override {
        config[key] = value;
    }
    
    std::string getConfiguration(const std::string& key) const override {
        auto it = config.find(key);
        return it != config.end() ? it->second : "";
    }
    
    void initialize() {
        std::string dbType = getConfiguration("database.type");
        std::string logLevel = getConfiguration("logging.level");
        // Use configuration
    }
};

// ===================== FACTORY PATTERN WITH DI =====================

class ServiceFactory {
public:
    virtual ~ServiceFactory() = default;
    
    virtual std::shared_ptr<IDatabase> createDatabase() = 0;
    virtual std::shared_ptr<ILogger> createLogger() = 0;
    virtual std::shared_ptr<IEmailService> createEmailService() = 0;
    
    // Template method for creating complete service
    std::unique_ptr<UserService> createUserService() {
        return std::make_unique<UserService>(
            createDatabase(),
            createLogger()
        );
    }
};

class ProductionFactory : public ServiceFactory {
public:
    std::shared_ptr<IDatabase> createDatabase() override {
        auto db = std::make_shared<MySQLDatabase>();
        db->connect("prod-db.example.com:3306");
        return db;
    }
    
    std::shared_ptr<ILogger> createLogger() override {
        return std::make_shared<FileLogger>();
    }
    
    std::shared_ptr<IEmailService> createEmailService() override {
        return std::make_shared<SMTPEmailService>();
    }
};

class DevelopmentFactory : public ServiceFactory {
public:
    std::shared_ptr<IDatabase> createDatabase() override {
        auto db = std::make_shared<PostgresDatabase>();
        db->connect("localhost:5432");
        return db;
    }
    
    std::shared_ptr<ILogger> createLogger() override {
        return std::make_shared<ConsoleLogger>();
    }
    
    std::shared_ptr<IEmailService> createEmailService() override {
        return std::make_shared<MockEmailService>();
    }
};

// ===================== DEPENDENCY INJECTION CONTAINER =====================

class DIContainer {
private:
    std::unordered_map<std::type_index, std::function<std::shared_ptr<void>()>> creators;
    std::unordered_map<std::type_index, std::shared_ptr<void>> singletons;
    
public:
    template<typename Interface, typename Implementation>
    void registerType(bool singleton = false) {
        auto creator = [this, singleton]() -> std::shared_ptr<void> {
            if (singleton) {
                auto it = singletons.find(typeid(Interface));
                if (it != singletons.end()) {
                    return it->second;
                }
                
                auto instance = std::static_pointer_cast<void>(
                    std::make_shared<Implementation>());
                singletons[typeid(Interface)] = instance;
                return instance;
            }
            
            return std::static_pointer_cast<void>(
                std::make_shared<Implementation>());
        };
        
        creators[typeid(Interface)] = creator;
    }
    
    template<typename Interface, typename Implementation, typename... Args>
    void registerFactory(std::function<std::shared_ptr<Implementation>(Args...)> factory) {
        auto creator = [factory]() -> std::shared_ptr<void> {
            return std::static_pointer_cast<void>(factory());
        };
        
        creators[typeid(Interface)] = creator;
    }
    
    template<typename T>
    std::shared_ptr<T> resolve() {
        auto it = creators.find(typeid(T));
        if (it == creators.end()) {
            throw std::runtime_error("Type not registered: " + 
                                    std::string(typeid(T).name()));
        }
        
        auto instance = it->second();
        return std::static_pointer_cast<T>(instance);
    }
    
    template<typename T, typename... Dependencies>
    std::shared_ptr<T> resolveWithDependencies() {
        // Recursively resolve dependencies
        return std::make_shared<T>(resolve<Dependencies>()...);
    }
};

// Usage of DI Container
void demonstrateDIContainer() {
    DIContainer container;
    
    // Register types
    container.registerType<IDatabase, MySQLDatabase>(true);  // Singleton
    container.registerType<ILogger, FileLogger>(false);      // Transient
    
    // Register with factory
    container.registerFactory<IEmailService, SMTPEmailService>(
        []() {
            auto service = std::make_shared<SMTPEmailService>();
            service->configure("smtp.gmail.com", 587);
            return service;
        }
    );
    
    // Resolve dependencies
    auto database = container.resolve<IDatabase>();
    auto logger = container.resolve<ILogger>();
    
    // Create service with dependencies
    auto userService = std::make_shared<UserService>(database, logger);
    
    // Or use auto-resolution
    auto autoUserService = container.resolveWithDependencies<UserService, 
                                                           IDatabase, 
                                                           ILogger>();
}

// ===================== TESTING WITH DEPENDENCY INJECTION =====================

// Mock implementations for testing
class MockDatabase : public IDatabase {
public:
    // Track calls for verification
    std::vector<std::string> executedQueries;
    bool shouldThrow = false;
    
    void connect(const std::string&) override {
        // Do nothing in test
    }
    
    void execute(const std::string& query) override {
        if (shouldThrow) {
            throw std::runtime_error("Mock database error");
        }
        executedQueries.push_back(query);
    }
    
    std::vector<std::string> query(const std::string& query) override {
        executedQueries.push_back(query);
        return {"mock_user1", "mock_user2"};
    }
};

class MockLogger : public ILogger {
public:
    std::vector<std::string> logMessages;
    std::vector<std::string> errorMessages;
    
    void log(const std::string& message) override {
        logMessages.push_back(message);
    }
    
    void error(const std::string& message) override {
        errorMessages.push_back(message);
    }
};

// Unit tests become much easier
void testUserService() {
    // Arrange
    auto mockDb = std::make_shared<MockDatabase>();
    auto mockLogger = std::make_shared<MockLogger>();
    
    UserService service(mockDb, mockLogger);
    
    // Act
    service.createUser("testuser");
    
    // Assert
    assert(!mockDb->executedQueries.empty());
    assert(mockDb->executedQueries[0].find("testuser") != std::string::npos);
    assert(!mockLogger->logMessages.empty());
    
    // Test error case
    mockDb->shouldThrow = true;
    try {
        service.createUser("failuser");
        assert(false); // Should not reach here
    } catch (...) {
        assert(!mockLogger->errorMessages.empty());
    }
}

// ===================== REAL-WORLD EXAMPLE =====================

class IEmailService {
public:
    virtual ~IEmailService() = default;
    virtual void sendEmail(const std::string& to, 
                          const std::string& subject, 
                          const std::string& body) = 0;
};

class NotificationService {
private:
    std::shared_ptr<IEmailService> emailService;
    std::shared_ptr<ILogger> logger;
    
public:
    NotificationService(std::shared_ptr<IEmailService> email, 
                       std::shared_ptr<ILogger> log)
        : emailService(std::move(email))
        , logger(std::move(log)) {}
    
    void sendWelcomeEmail(const std::string& userEmail, 
                         const std::string& userName) {
        logger->log("Sending welcome email to: " + userEmail);
        
        std::string subject = "Welcome to Our Service!";
        std::string body = "Hello " + userName + ",\n\nWelcome!";
        
        emailService->sendEmail(userEmail, subject, body);
        logger->log("Welcome email sent successfully");
    }
};

// Configuration-based factory
class EnvironmentAwareFactory {
private:
    std::string environment;
    
public:
    explicit EnvironmentAwareFactory(const std::string& env) 
        : environment(env) {}
    
    std::shared_ptr<IDatabase> createDatabase() {
        if (environment == "production") {
            auto db = std::make_shared<MySQLDatabase>();
            db->connect("prod-cluster.example.com:3306");
            return db;
        } else if (environment == "staging") {
            auto db = std::make_shared<PostgresDatabase>();
            db->connect("staging-db.example.com:5432");
            return db;
        } else {
            // Development/testing
            return std::make_shared<MockDatabase>();
        }
    }
    
    std::shared_ptr<ILogger> createLogger() {
        if (environment == "production") {
            return std::make_shared<FileLogger>();
        } else {
            return std::make_shared<ConsoleLogger>();
        }
    }
    
    std::shared_ptr<IEmailService> createEmailService() {
        if (environment == "production") {
            auto service = std::make_shared<SMTPEmailService>();
            service->configure("smtp.sendgrid.net", 587);
            return service;
        } else {
            // Don't send real emails in non-production
            return std::make_shared<MockEmailService>();
        }
    }
    
    std::unique_ptr<NotificationService> createNotificationService() {
        return std::make_unique<NotificationService>(
            createEmailService(),
            createLogger()
        );
    }
};

int main() {
    // Different configurations for different environments
    EnvironmentAwareFactory prodFactory("production");
    EnvironmentAwareFactory devFactory("development");
    
    // Production setup
    auto prodNotificationService = prodFactory.createNotificationService();
    prodNotificationService->sendWelcomeEmail("user@example.com", "John Doe");
    
    // Development setup (won't send real emails)
    auto devNotificationService = devFactory.createNotificationService();
    devNotificationService->sendWelcomeEmail("test@test.com", "Test User");
    
    return 0;
}


// Testability.hpp - Writing testable C++ code
#pragma once

#include <memory>
#include <functional>
#include <vector>
#include <string>
#include <chrono>
#include <random>
#include <algorithm>

// ===================== PURE FUNCTIONS =====================

// Pure function: Same input always produces same output, no side effects
class PureFunctions {
public:
    // GOOD: Pure function - easily testable
    static int add(int a, int b) {
        return a + b;
    }
    
    static double calculateTax(double amount, double taxRate) {
        return amount * taxRate;
    }
    
    static std::string toUpperCase(const std::string& str) {
        std::string result = str;
        std::transform(result.begin(), result.end(), result.begin(), ::toupper);
        return result;
    }
    
    // BAD: Impure function - depends on external state
    int getCurrentYear() {
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        std::tm* tm = std::localtime(&time);
        return tm->tm_year + 1900;  // Depends on system time
    }
    
    // BETTER: Make time dependency explicit
    int getYearFromTime(std::time_t time) {
        std::tm* tm = std::localtime(&time);
        return tm->tm_year + 1900;
    }
};

// ===================== SMALL, FOCUSED INTERFACES =====================

// BAD: Large, complex interface
class IMonolithicService {
public:
    virtual ~IMonolithicService() = default;
    
    // User management
    virtual void createUser(const std::string& username, const std::string& password) = 0;
    virtual void deleteUser(const std::string& username) = 0;
    virtual void updateUser(const std::string& username, const std::string& newPassword) = 0;
    
    // Order management
    virtual void createOrder(const std::string& userId, const std::vector<std::string>& items) = 0;
    virtual void cancelOrder(const std::string& orderId) = 0;
    virtual void processOrder(const std::string& orderId) = 0;
    
    // Payment processing
    virtual void processPayment(const std::string& orderId, double amount) = 0;
    virtual void refundPayment(const std::string& paymentId) = 0;
    
    // Email notifications
    virtual void sendWelcomeEmail(const std::string& email) = 0;
    virtual void sendOrderConfirmation(const std::string& email, const std::string& orderId) = 0;
    virtual void sendPasswordReset(const std::string& email) = 0;
};

// GOOD: Small, focused interfaces (Single Responsibility Principle)
class IUserRepository {
public:
    virtual ~IUserRepository() = default;
    virtual void create(const User& user) = 0;
    virtual std::optional<User> findById(const std::string& id) = 0;
    virtual void update(const User& user) = 0;
    virtual void remove(const std::string& id) = 0;
};

class IOrderProcessor {
public:
    virtual ~IOrderProcessor() = default;
    virtual Order createOrder(const std::string& userId, const std::vector<Item>& items) = 0;
    virtual void cancelOrder(const std::string& orderId) = 0;
    virtual Receipt processOrder(const std::string& orderId) = 0;
};

class IPaymentGateway {
public:
    virtual ~IPaymentGateway() = default;
    virtual PaymentResult charge(const std::string& orderId, double amount) = 0;
    virtual PaymentResult refund(const std::string& paymentId) = 0;
};

class IEmailService {
public:
    virtual ~IEmailService() = default;
    virtual void send(const Email& email) = 0;
};

// ===================== DEPENDENCY INJECTION FOR TESTING =====================

class OrderService {
private:
    std::shared_ptr<IOrderRepository> orderRepository;
    std::shared_ptr<IPaymentGateway> paymentGateway;
    std::shared_ptr<IEmailService> emailService;
    std::shared_ptr<ILogger> logger;
    
public:
    // Constructor injection for testability
    OrderService(std::shared_ptr<IOrderRepository> repo,
                 std::shared_ptr<IPaymentGateway> gateway,
                 std::shared_ptr<IEmailService> email,
                 std::shared_ptr<ILogger> log)
        : orderRepository(std::move(repo))
        , paymentGateway(std::move(gateway))
        , emailService(std::move(email))
        , logger(std::move(log)) {}
    
    Receipt processOrder(const std::string& orderId) {
        logger->info("Processing order: " + orderId);
        
        // Get order from repository
        auto order = orderRepository->findById(orderId);
        if (!order) {
            logger->error("Order not found: " + orderId);
            throw OrderNotFoundException(orderId);
        }
        
        // Process payment
        auto paymentResult = paymentGateway->charge(orderId, order->total);
        if (!paymentResult.success) {
            logger->error("Payment failed for order: " + orderId);
            throw PaymentFailedException(paymentResult.error);
        }
        
        // Update order status
        order->status = OrderStatus::PAID;
        orderRepository->update(*order);
        
        // Send confirmation email
        Email email;
        email.to = order->customerEmail;
        email.subject = "Order Confirmation";
        email.body = "Your order #" + orderId + " has been confirmed.";
        emailService->send(email);
        
        logger->info("Order processed successfully: " + orderId);
        
        return createReceipt(*order, paymentResult);
    }
    
private:
    Receipt createReceipt(const Order& order, const PaymentResult& payment) {
        return Receipt{order.id, order.total, payment.transactionId};
    }
};

// ===================== MOCK OBJECTS FOR TESTING =====================

class MockOrderRepository : public IOrderRepository {
public:
    std::unordered_map<std::string, Order> orders;
    std::vector<std::string> findByIdCalls;
    std::vector<Order> updateCalls;
    
    std::optional<Order> findById(const std::string& id) override {
        findByIdCalls.push_back(id);
        auto it = orders.find(id);
        if (it != orders.end()) {
            return it->second;
        }
        return std::nullopt;
    }
    
    void update(const Order& order) override {
        updateCalls.push_back(order);
        orders[order.id] = order;
    }
    
    // Other methods...
};

class MockPaymentGateway : public IPaymentGateway {
public:
    bool shouldSucceed = true;
    std::string errorMessage = "Mock payment error";
    std::vector<std::pair<std::string, double>> chargeCalls;
    
    PaymentResult charge(const std::string& orderId, double amount) override {
        chargeCalls.emplace_back(orderId, amount);
        
        if (shouldSucceed) {
            return PaymentResult{true, "TXN_" + std::to_string(rand()), ""};
        } else {
            return PaymentResult{false, "", errorMessage};
        }
    }
};

class MockEmailService : public IEmailService {
public:
    std::vector<Email> sentEmails;
    
    void send(const Email& email) override {
        sentEmails.push_back(email);
    }
};

class MockLogger : public ILogger {
public:
    std::vector<std::string> infoMessages;
    std::vector<std::string> errorMessages;
    
    void info(const std::string& message) override {
        infoMessages.push_back(message);
    }
    
    void error(const std::string& message) override {
        errorMessages.push_back(message);
    }
};

// ===================== UNIT TESTS =====================

void testOrderServiceSuccess() {
    // Arrange
    auto mockRepo = std::make_shared<MockOrderRepository>();
    auto mockGateway = std::make_shared<MockPaymentGateway>();
    auto mockEmail = std::make_shared<MockEmailService>();
    auto mockLogger = std::make_shared<MockLogger>();
    
    OrderService service(mockRepo, mockGateway, mockEmail, mockLogger);
    
    // Setup test data
    Order testOrder{"ORD123", 100.0, "customer@example.com", OrderStatus::PENDING};
    mockRepo->orders["ORD123"] = testOrder;
    
    // Act
    auto receipt = service.processOrder("ORD123");
    
    // Assert
    assert(receipt.orderId == "ORD123");
    assert(receipt.amount == 100.0);
    assert(!receipt.transactionId.empty());
    
    assert(mockRepo->findByIdCalls.size() == 1);
    assert(mockRepo->findByIdCalls[0] == "ORD123");
    
    assert(mockGateway->chargeCalls.size() == 1);
    assert(mockGateway->chargeCalls[0].first == "ORD123");
    assert(mockGateway->chargeCalls[0].second == 100.0);
    
    assert(mockEmail->sentEmails.size() == 1);
    assert(mockEmail->sentEmails[0].to == "customer@example.com");
    
    assert(mockLogger->infoMessages.size() == 2);
    assert(mockLogger->errorMessages.empty());
    
    // Verify order was updated
    assert(mockRepo->updateCalls.size() == 1);
    assert(mockRepo->updateCalls[0].status == OrderStatus::PAID);
}

void testOrderServicePaymentFailure() {
    // Arrange
    auto mockRepo = std::make_shared<MockOrderRepository>();
    auto mockGateway = std::make_shared<MockPaymentGateway>();
    auto mockEmail = std::make_shared<MockEmailService>();
    auto mockLogger = std::make_shared<MockLogger>();
    
    OrderService service(mockRepo, mockGateway, mockEmail, mockLogger);
    
    Order testOrder{"ORD456", 200.0, "customer@example.com", OrderStatus::PENDING};
    mockRepo->orders["ORD456"] = testOrder;
    
    mockGateway->shouldSucceed = false;
    mockGateway->errorMessage = "Insufficient funds";
    
    // Act & Assert
    try {
        service.processOrder("ORD456");
        assert(false); // Should throw
    } catch (const PaymentFailedException& e) {
        assert(e.what() == std::string("Insufficient funds"));
    }
    
    // Verify email was NOT sent
    assert(mockEmail->sentEmails.empty());
    
    // Verify error was logged
    assert(!mockLogger->errorMessages.empty());
}

// ===================== TESTABLE DESIGN PATTERNS =====================

// Strategy pattern for testability
class IDiscountStrategy {
public:
    virtual ~IDiscountStrategy() = default;
    virtual double calculateDiscount(const Order& order) = 0;
};

class NoDiscount : public IDiscountStrategy {
public:
    double calculateDiscount(const Order& order) override {
        return 0.0;
    }
};

class PercentageDiscount : public IDiscountStrategy {
private:
    double percentage;
    
public:
    explicit PercentageDiscount(double pct) : percentage(pct) {}
    
    double calculateDiscount(const Order& order) override {
        return order.subtotal * percentage / 100.0;
    }
};

class FixedAmountDiscount : public IDiscountStrategy {
private:
    double amount;
    
public:
    explicit FixedAmountDiscount(double amt) : amount(amt) {}
    
    double calculateDiscount(const Order& order) override {
        return std::min(amount, order.subtotal);
    }
};

class PricingService {
private:
    std::shared_ptr<IDiscountStrategy> discountStrategy;
    
public:
    explicit PricingService(std::shared_ptr<IDiscountStrategy> strategy)
        : discountStrategy(std::move(strategy)) {}
    
    double calculateTotal(const Order& order) {
        double discount = discountStrategy->calculateDiscount(order);
        double subtotal = order.subtotal - discount;
        double tax = subtotal * order.taxRate;
        return subtotal + tax;
    }
};

// Factory for creating test strategies
class TestDiscountStrategy : public IDiscountStrategy {
public:
    double nextDiscount = 0.0;
    
    double calculateDiscount(const Order& order) override {
        return nextDiscount;
    }
};

void testPricingService() {
    // Arrange
    auto mockStrategy = std::make_shared<TestDiscountStrategy>();
    PricingService service(mockStrategy);
    
    Order order{100.0, 0.1}; // $100 subtotal, 10% tax
    
    // Test with no discount
    mockStrategy->nextDiscount = 0.0;
    assert(service.calculateTotal(order) == 110.0); // 100 + 10 tax
    
    // Test with $20 discount
    mockStrategy->nextDiscount = 20.0;
    assert(service.calculateTotal(order) == 88.0); // (100-20) + 8 tax
}

// ===================== TEST DOUBLES =====================

// Fake: Working implementation with simplified behavior
class FakeUserRepository : public IUserRepository {
private:
    std::unordered_map<std::string, User> users;
    
public:
    void create(const User& user) override {
        users[user.id] = user;
    }
    
    std::optional<User> findById(const std::string& id) override {
        auto it = users.find(id);
        if (it != users.end()) {
            return it->second;
        }
        return std::nullopt;
    }
    
    void update(const User& user) override {
        users[user.id] = user;
    }
    
    void remove(const std::string& id) override {
        users.erase(id);
    }
};

// Stub: Returns predefined values
class StubPaymentGateway : public IPaymentGateway {
public:
    PaymentResult nextResult;
    
    PaymentResult charge(const std::string&, double) override {
        return nextResult;
    }
    
    PaymentResult refund(const std::string&) override {
        return nextResult;
    }
};

// Spy: Records interactions
class SpyEmailService : public IEmailService {
public:
    std::vector<Email> emailsSent;
    int sendCount = 0;
    
    void send(const Email& email) override {
        emailsSent.push_back(email);
        sendCount++;
    }
};

// ===================== TEST DATA BUILDERS =====================

class OrderBuilder {
private:
    std::string id = "TEST_" + std::to_string(rand());
    double subtotal = 100.0;
    double taxRate = 0.1;
    std::string customerEmail = "test@example.com";
    OrderStatus status = OrderStatus::PENDING;
    
public:
    OrderBuilder& withId(const std::string& newId) {
        id = newId;
        return *this;
    }
    
    OrderBuilder& withSubtotal(double newSubtotal) {
        subtotal = newSubtotal;
        return *this;
    }
    
    OrderBuilder& withTaxRate(double newTaxRate) {
        taxRate = newTaxRate;
        return *this;
    }
    
    OrderBuilder& withEmail(const std::string& newEmail) {
        customerEmail = newEmail;
        return *this;
    }
    
    OrderBuilder& withStatus(OrderStatus newStatus) {
        status = newStatus;
        return *this;
    }
    
    Order build() const {
        return Order{id, subtotal, taxRate, customerEmail, status};
    }
};

// Usage in tests
void testWithBuilder() {
    // Create complex test objects easily
    Order order = OrderBuilder()
        .withId("SPECIFIC_ID")
        .withSubtotal(250.0)
        .withTaxRate(0.08)
        .withEmail("specific@test.com")
        .withStatus(OrderStatus::PROCESSING)
        .build();
    
    assert(order.id == "SPECIFIC_ID");
    assert(order.subtotal == 250.0);
    // ... more assertions
}

// ===================== PROPERTY-BASED TESTING =====================

// Generate random test data
class TestDataGenerator {
public:
    static Order generateRandomOrder() {
        static std::mt19937 gen(std::random_device{}());
        std::uniform_real_distribution<double> amountDist(1.0, 1000.0);
        std::uniform_real_distribution<double> taxDist(0.0, 0.2);
        
        return Order{
            "ORD_" + std::to_string(gen()),
            amountDist(gen),
            taxDist(gen),
            "user" + std::to_string(gen()) + "@example.com",
            OrderStatus::PENDING
        };
    }
    
    static std::vector<Order> generateOrders(int count) {
        std::vector<Order> orders;
        orders.reserve(count);
        for (int i = 0; i < count; ++i) {
            orders.push_back(generateRandomOrder());
        }
        return orders;
    }
};

// Property-based test
void testDiscountMonotonicity() {
    auto strategy = std::make_shared<PercentageDiscount>(10.0);
    PricingService service(strategy);
    
    // Generate many random orders
    auto orders = TestDataGenerator::generateOrders(1000);
    
    for (const auto& order : orders) {
        double total = service.calculateTotal(order);
        
        // Property: Total should be <= subtotal * (1 + taxRate)
        double maxPossible = order.subtotal * (1 + order.taxRate);
        assert(total <= maxPossible + 1e-6);
        
        // Property: Total should be >= 0
        assert(total >= 0);
        
        // Property: If subtotal increases, total should not decrease
        // (would need to compare multiple orders)
    }
}

// ===================== INTEGRATION TESTING =====================

class IntegrationTestBase {
protected:
    std::shared_ptr<RealDatabase> database;
    std::shared_ptr<RealEmailService> emailService;
    std::shared_ptr<FileLogger> logger;
    
    void setUp() {
        // Set up real dependencies for integration tests
        database = std::make_shared<RealDatabase>();
        database->connect("test-db.example.com");
        
        emailService = std::make_shared<RealEmailService>();
        emailService->configure("test-smtp.example.com");
        
        logger = std::make_shared<FileLogger>("/tmp/test.log");
    }
    
    void tearDown() {
        // Clean up test data
        database->execute("DELETE FROM orders WHERE test_flag = true");
        database->disconnect();
    }
};

void integrationTestOrderProcessing() {
    IntegrationTestBase test;
    test.setUp();
    
    try {
        // Create service with real dependencies
        auto repo = std::make_shared<DatabaseOrderRepository>(test.database);
        auto gateway = std::make_shared<RealPaymentGateway>();
        OrderService service(repo, gateway, test.emailService, test.logger);
        
        // Create test order in database
        test.database->execute(
            "INSERT INTO orders (id, subtotal, status, test_flag) "
            "VALUES ('INT_TEST_1', 100.0, 'PENDING', true)"
        );
        
        // Test the real integration
        auto receipt = service.processOrder("INT_TEST_1");
        
        // Verify in database
        auto result = test.database->query(
            "SELECT status FROM orders WHERE id = 'INT_TEST_1'"
        );
        assert(result[0]["status"] == "PAID");
        
        // Verify email was sent (check email service logs)
        
    } catch (...) {
        test.tearDown();
        throw;
    }
    
    test.tearDown();
}


// CleanArchitecture.hpp - Implementing Clean Architecture in C++
#pragma once

#include <memory>
#include <string>
#include <vector>
#include <functional>
#include <map>
#include <optional>

// ===================== DOMAIN LAYER (Enterprise Business Rules) =====================

// Entities - Core business objects
class User {
private:
    std::string id;
    std::string email;
    std::string name;
    bool isActive;
    
public:
    User(std::string id, std::string email, std::string name)
        : id(std::move(id))
        , email(std::move(email))
        , name(std::move(name))
        , isActive(true) {}
    
    // Business logic methods
    bool isValid() const {
        return !id.empty() && 
               !email.empty() && 
               email.find('@') != std::string::npos;
    }
    
    void deactivate() {
        isActive = false;
    }
    
    void changeEmail(const std::string& newEmail) {
        if (newEmail.find('@') == std::string::npos) {
            throw std::invalid_argument("Invalid email address");
        }
        email = newEmail;
    }
    
    // Getters
    std::string getId() const { return id; }
    std::string getEmail() const { return email; }
    std::string getName() const { return name; }
    bool getIsActive() const { return isActive; }
};

class Product {
private:
    std::string id;
    std::string name;
    double price;
    int stockQuantity;
    
public:
    Product(std::string id, std::string name, double price, int stock)
        : id(std::move(id))
        , name(std::move(name))
        , price(price)
        , stockQuantity(stock) {}
    
    // Business logic
    bool isAvailable() const {
        return stockQuantity > 0;
    }
    
    void reduceStock(int quantity) {
        if (quantity <= 0) {
            throw std::invalid_argument("Quantity must be positive");
        }
        if (quantity > stockQuantity) {
            throw std::runtime_error("Insufficient stock");
        }
        stockQuantity -= quantity;
    }
    
    void increaseStock(int quantity) {
        if (quantity <= 0) {
            throw std::invalid_argument("Quantity must be positive");
        }
        stockQuantity += quantity;
    }
    
    double calculateTotal(int quantity) const {
        if (quantity <= 0) {
            throw std::invalid_argument("Quantity must be positive");
        }
        return price * quantity;
    }
    
    // Getters
    std::string getId() const { return id; }
    std::string getName() const { return name; }
    double getPrice() const { return price; }
    int getStockQuantity() const { return stockQuantity; }
};

// Value Objects - Immutable objects without identity
class Money {
private:
    double amount;
    std::string currency;
    
public:
    Money(double amount, std::string currency)
        : amount(amount)
        , currency(std::move(currency)) {
        if (amount < 0) {
            throw std::invalid_argument("Amount cannot be negative");
        }
    }
    
    // Value objects are equal if all fields are equal
    bool operator==(const Money& other) const {
        return amount == other.amount && currency == other.currency;
    }
    
    bool operator!=(const Money& other) const {
        return !(*this == other);
    }
    
    // Operations return new instances (immutability)
    Money add(const Money& other) const {
        if (currency != other.currency) {
            throw std::runtime_error("Cannot add different currencies");
        }
        return Money(amount + other.amount, currency);
    }
    
    Money multiply(double factor) const {
        return Money(amount * factor, currency);
    }
    
    // Getters
    double getAmount() const { return amount; }
    const std::string& getCurrency() const { return currency; }
};

// Domain Events
class DomainEvent {
public:
    virtual ~DomainEvent() = default;
    virtual std::string getName() const = 0;
    virtual std::time_t getTimestamp() const = 0;
};

class UserRegisteredEvent : public DomainEvent {
private:
    User user;
    std::time_t timestamp;
    
public:
    explicit UserRegisteredEvent(User user)
        : user(std::move(user))
        , timestamp(std::time(nullptr)) {}
    
    std::string getName() const override {
        return "UserRegistered";
    }
    
    std::time_t getTimestamp() const override {
        return timestamp;
    }
    
    const User& getUser() const {
        return user;
    }
};

class ProductOutOfStockEvent : public DomainEvent {
private:
    Product product;
    std::time_t timestamp;
    
public:
    explicit ProductOutOfStockEvent(Product product)
        : product(std::move(product))
        , timestamp(std::time(nullptr)) {}
    
    std::string getName() const override {
        return "ProductOutOfStock";
    }
    
    std::time_t getTimestamp() const override {
        return timestamp;
    }
    
    const Product& getProduct() const {
        return product;
    }
};

// Domain Services - Stateless services that operate on multiple entities
class OrderPricingService {
public:
    Money calculateTotal(const std::vector<std::pair<Product, int>>& items, 
                        const std::string& currency) const {
        double total = 0.0;
        
        for (const auto& [product, quantity] : items) {
            total += product.getPrice() * quantity;
        }
        
        // Apply business rules
        if (items.size() > 5) {
            total *= 0.9; // 10% discount for bulk orders
        }
        
        return Money(total, currency);
    }
};

// Repository Interfaces (in domain layer)
class IUserRepository {
public:
    virtual ~IUserRepository() = default;
    
    virtual std::optional<User> findById(const std::string& id) = 0;
    virtual std::optional<User> findByEmail(const std::string& email) = 0;
    virtual void save(const User& user) = 0;
    virtual void update(const User& user) = 0;
    virtual void deleteById(const std::string& id) = 0;
};

class IProductRepository {
public:
    virtual ~IProductRepository() = default;
    
    virtual std::optional<Product> findById(const std::string& id) = 0;
    virtual std::vector<Product> findAll() = 0;
    virtual std::vector<Product> findAvailable() = 0;
    virtual void save(const Product& product) = 0;
    virtual void update(const Product& product) = 0;
};

// ===================== APPLICATION LAYER (Application Business Rules) =====================

// Use Cases/Interactors
class RegisterUserUseCase {
private:
    std::shared_ptr<IUserRepository> userRepository;
    std::shared_ptr<IEventDispatcher> eventDispatcher;
    
public:
    RegisterUserUseCase(std::shared_ptr<IUserRepository> repo,
                       std::shared_ptr<IEventDispatcher> dispatcher)
        : userRepository(std::move(repo))
        , eventDispatcher(std::move(dispatcher)) {}
    
    struct Input {
        std::string email;
        std::string name;
        std::string password;
    };
    
    struct Output {
        std::string userId;
        std::string email;
        std::string name;
    };
    
    Output execute(const Input& input) {
        // Validate input
        if (input.email.empty() || input.name.empty() || input.password.empty()) {
            throw std::invalid_argument("All fields are required");
        }
        
        // Check if user already exists
        auto existingUser = userRepository->findByEmail(input.email);
        if (existingUser) {
            throw std::runtime_error("User with this email already exists");
        }
        
        // Create user entity
        std::string userId = generateUserId();
        User user(userId, input.email, input.name);
        
        if (!user.isValid()) {
            throw std::runtime_error("Invalid user data");
        }
        
        // Save user
        userRepository->save(user);
        
        // Dispatch domain event
        eventDispatcher->dispatch(std::make_unique<UserRegisteredEvent>(user));
        
        // Return output
        return Output{userId, user.getEmail(), user.getName()};
    }
    
private:
    std::string generateUserId() {
        // Implementation for generating unique ID
        return "USER_" + std::to_string(std::time(nullptr));
    }
};

class PlaceOrderUseCase {
private:
    std::shared_ptr<IProductRepository> productRepository;
    std::shared_ptr<IOrderRepository> orderRepository;
    std::shared_ptr<OrderPricingService> pricingService;
    std::shared_ptr<IEventDispatcher> eventDispatcher;
    
public:
    struct OrderItem {
        std::string productId;
        int quantity;
    };
    
    struct Input {
        std::string userId;
        std::vector<OrderItem> items;
        std::string currency = "USD";
    };
    
    struct Output {
        std::string orderId;
        double totalAmount;
        std::string currency;
    };
    
    Output execute(const Input& input) {
        // Validate input
        if (input.userId.empty() || input.items.empty()) {
            throw std::invalid_argument("Invalid order data");
        }
        
        // Load products
        std::vector<std::pair<Product, int>> orderProducts;
        double total = 0.0;
        
        for (const auto& item : input.items) {
            auto product = productRepository->findById(item.productId);
            if (!product) {
                throw std::runtime_error("Product not found: " + item.productId);
            }
            
            if (!product->isAvailable()) {
                // Dispatch domain event
                eventDispatcher->dispatch(
                    std::make_unique<ProductOutOfStockEvent>(*product));
                throw std::runtime_error("Product out of stock: " + product->getName());
            }
            
            if (item.quantity > product->getStockQuantity()) {
                throw std::runtime_error("Insufficient stock for: " + product->getName());
            }
            
            orderProducts.emplace_back(*product, item.quantity);
            total += product->getPrice() * item.quantity;
        }
        
        // Calculate total using domain service
        Money totalMoney = pricingService->calculateTotal(orderProducts, input.currency);
        
        // Create order
        std::string orderId = generateOrderId();
        Order order(orderId, input.userId, orderProducts, totalMoney);
        
        // Reduce stock for each product
        for (const auto& [product, quantity] : orderProducts) {
            Product updatedProduct = product;
            updatedProduct.reduceStock(quantity);
            productRepository->update(updatedProduct);
        }
        
        // Save order
        orderRepository->save(order);
        
        return Output{orderId, totalMoney.getAmount(), totalMoney.getCurrency()};
    }
    
private:
    std::string generateOrderId() {
        return "ORD_" + std::to_string(std::time(nullptr));
    }
};

// Application Services
class UserApplicationService {
private:
    std::shared_ptr<RegisterUserUseCase> registerUserUseCase;
    // Other use cases...
    
public:
    explicit UserApplicationService(std::shared_ptr<RegisterUserUseCase> useCase)
        : registerUserUseCase(std::move(useCase)) {}
    
    struct RegisterUserCommand {
        std::string email;
        std::string name;
        std::string password;
    };
    
    struct UserDto {
        std::string id;
        std::string email;
        std::string name;
        bool isActive;
    };
    
    UserDto registerUser(const RegisterUserCommand& command) {
        auto input = RegisterUserUseCase::Input{
            command.email, command.name, command.password};
        
        auto output = registerUserUseCase->execute(input);
        
        return UserDto{output.userId, output.email, output.name, true};
    }
};

// DTOs (Data Transfer Objects)
struct ProductDto {
    std::string id;
    std::string name;
    double price;
    bool isAvailable;
    int stockQuantity;
};

struct OrderDto {
    std::string id;
    std::string userId;
    std::vector<ProductDto> products;
    double totalAmount;
    std::string currency;
    std::string status;
};

// ===================== INTERFACE LAYER (Adapters) =====================

// Controllers/Presenters
class UserController {
private:
    std::shared_ptr<UserApplicationService> userService;
    
public:
    explicit UserController(std::shared_ptr<UserApplicationService> service)
        : userService(std::move(service)) {}
    
    struct RegisterRequest {
        std::string email;
        std::string name;
        std::string password;
    };
    
    struct RegisterResponse {
        std::string userId;
        std::string email;
        std::string name;
        std::string message;
    };
    
    RegisterResponse registerUser(const RegisterRequest& request) {
        try {
            auto command = UserApplicationService::RegisterUserCommand{
                request.email, request.name, request.password};
            
            auto userDto = userService->registerUser(command);
            
            return RegisterResponse{
                userDto.id,
                userDto.email,
                userDto.name,
                "User registered successfully"
            };
        } catch (const std::exception& e) {
            return RegisterResponse{"", "", "", "Error: " + std::string(e.what())};
        }
    }
};

// REST API Adapter
class RestUserController {
private:
    std::shared_ptr<UserController> userController;
    
public:
    explicit RestUserController(std::shared_ptr<UserController> controller)
        : userController(std::move(controller)) {}
    
    // Simulating HTTP request handling
    std::string handlePost(const std::string& path, const std::string& body) {
        if (path == "/api/users/register") {
            // Parse JSON body (simplified)
            auto request = parseRegisterRequest(body);
            auto response = userController->registerUser(request);
            
            // Return JSON response
            return formatJsonResponse(response);
        }
        
        return "{\"error\": \"Not found\"}";
    }
    
private:
    UserController::RegisterRequest parseRegisterRequest(const std::string& json) {
        // Simplified JSON parsing
        // In real implementation, use a JSON library
        return UserController::RegisterRequest{
            "parsed@email.com", "Parsed Name", "password123"};
    }
    
    std::string formatJsonResponse(const UserController::RegisterResponse& response) {
        if (response.userId.empty()) {
            return "{\"error\": \"" + response.message + "\"}";
        }
        
        return "{\"userId\": \"" + response.userId + "\", "
               "\"email\": \"" + response.email + "\", "
               "\"name\": \"" + response.name + "\", "
               "\"message\": \"" + response.message + "\"}";
    }
};

// Console Adapter (for CLI)
class ConsoleUserInterface {
private:
    std::shared_ptr<UserController> userController;
    
public:
    explicit ConsoleUserInterface(std::shared_ptr<UserController> controller)
        : userController(std::move(controller)) {}
    
    void run() {
        std::cout << "=== User Registration ===\n";
        
        std::string email, name, password;
        
        std::cout << "Email: ";
        std::cin >> email;
        
        std::cout << "Name: ";
        std::cin.ignore();
        std::getline(std::cin, name);
        
        std::cout << "Password: ";
        std::cin >> password;
        
        auto request = UserController::RegisterRequest{email, name, password};
        auto response = userController->registerUser(request);
        
        std::cout << "\nResult: " << response.message << "\n";
        if (!response.userId.empty()) {
            std::cout << "User ID: " << response.userId << "\n";
            std::cout << "Email: " << response.email << "\n";
            std::cout << "Name: " << response.name << "\n";
        }
    }
};

// ===================== INFRASTRUCTURE LAYER =====================

// Repository Implementations
class DatabaseUserRepository : public IUserRepository {
private:
    std::shared_ptr<DatabaseConnection> db;
    
public:
    explicit DatabaseUserRepository(std::shared_ptr<DatabaseConnection> connection)
        : db(std::move(connection)) {}
    
    std::optional<User> findById(const std::string& id) override {
        auto result = db->query("SELECT * FROM users WHERE id = ?", {id});
        if (result.empty()) {
            return std::nullopt;
        }
        
        return User{
            result[0]["id"],
            result[0]["email"],
            result[0]["name"]
        };
    }
    
    std::optional<User> findByEmail(const std::string& email) override {
        auto result = db->query("SELECT * FROM users WHERE email = ?", {email});
        if (result.empty()) {
            return std::nullopt;
        }
        
        return User{
            result[0]["id"],
            result[0]["email"],
            result[0]["name"]
        };
    }
    
    void save(const User& user) override {
        db->execute(
            "INSERT INTO users (id, email, name, is_active) VALUES (?, ?, ?, ?)",
            {user.getId(), user.getEmail(), user.getName(), user.getIsActive()}
        );
    }
    
    void update(const User& user) override {
        db->execute(
            "UPDATE users SET email = ?, name = ?, is_active = ? WHERE id = ?",
            {user.getEmail(), user.getName(), user.getIsActive(), user.getId()}
        );
    }
    
    void deleteById(const std::string& id) override {
        db->execute("DELETE FROM users WHERE id = ?", {id});
    }
};

class InMemoryProductRepository : public IProductRepository {
private:
    std::map<std::string, Product> products;
    
public:
    std::optional<Product> findById(const std::string& id) override {
        auto it = products.find(id);
        if (it != products.end()) {
            return it->second;
        }
        return std::nullopt;
    }
    
    std::vector<Product> findAll() override {
        std::vector<Product> result;
        for (const auto& [id, product] : products) {
            result.push_back(product);
        }
        return result;
    }
    
    std::vector<Product> findAvailable() override {
        std::vector<Product> result;
        for (const auto& [id, product] : products) {
            if (product.isAvailable()) {
                result.push_back(product);
            }
        }
        return result;
    }
    
    void save(const Product& product) override {
        products[product.getId()] = product;
    }
    
    void update(const Product& product) override {
        products[product.getId()] = product;
    }
};

// Event Dispatcher Implementation
class SimpleEventDispatcher : public IEventDispatcher {
private:
    std::map<std::string, std::vector<std::function<void(const DomainEvent&)>>> handlers;
    
public:
    void registerHandler(const std::string& eventName,
                        std::function<void(const DomainEvent&)> handler) override {
        handlers[eventName].push_back(std::move(handler));
    }
    
    void dispatch(std::unique_ptr<DomainEvent> event) override {
        auto eventName = event->getName();
        auto it = handlers.find(eventName);
        
        if (it != handlers.end()) {
            for (const auto& handler : it->second) {
                handler(*event);
            }
        }
        
        // Also log all events
        std::cout << "[Event] " << eventName << " dispatched at " 
                  << std::ctime(&event->getTimestamp());
    }
};

// Database Connection
class DatabaseConnection {
public:
    struct QueryResult {
        std::vector<std::map<std::string, std::string>> rows;
    };
    
    void connect(const std::string& connectionString) {
        // Real implementation would connect to database
        std::cout << "Connecting to database: " << connectionString << std::endl;
    }
    
    QueryResult query(const std::string& sql, 
                     const std::vector<std::string>& params = {}) {
        // Simplified implementation
        std::cout << "Executing query: " << sql << std::endl;
        return QueryResult{};
    }
    
    void execute(const std::string& sql, 
                const std::vector<std::string>& params = {}) {
        std::cout << "Executing: " << sql << std::endl;
    }
    
    void disconnect() {
        std::cout << "Disconnecting from database" << std::endl;
    }
};

// ===================== DEPENDENCY INJECTION CONFIGURATION =====================

class ApplicationCompositionRoot {
public:
    static std::shared_ptr<RestUserController> createRestController() {
        // Create infrastructure components
        auto db = std::make_shared<DatabaseConnection>();
        db->connect("host=localhost;dbname=mydb");
        
        auto eventDispatcher = std::make_shared<SimpleEventDispatcher>();
        
        // Create repositories
        auto userRepo = std::make_shared<DatabaseUserRepository>(db);
        auto productRepo = std::make_shared<InMemoryProductRepository>();
        
        // Create domain services
        auto pricingService = std::make_shared<OrderPricingService>();
        
        // Create use cases
        auto registerUseCase = std::make_shared<RegisterUserUseCase>(
            userRepo, eventDispatcher);
        
        // Create application services
        auto userAppService = std::make_shared<UserApplicationService>(
            registerUseCase);
        
        // Create controllers
        auto userController = std::make_shared<UserController>(userAppService);
        
        // Create adapters
        return std::make_shared<RestUserController>(userController);
    }
    
    static std::shared_ptr<ConsoleUserInterface> createConsoleInterface() {
        // Similar composition for console interface
        // Reusing same infrastructure components
        auto db = std::make_shared<DatabaseConnection>();
        db->connect("host=localhost;dbname=mydb");
        
        auto eventDispatcher = std::make_shared<SimpleEventDispatcher>();
        auto userRepo = std::make_shared<DatabaseUserRepository>(db);
        
        auto registerUseCase = std::make_shared<RegisterUserUseCase>(
            userRepo, eventDispatcher);
        
        auto userAppService = std::make_shared<UserApplicationService>(
            registerUseCase);
        
        auto userController = std::make_shared<UserController>(userAppService);
        
        return std::make_shared<ConsoleUserInterface>(userController);
    }
};

// ===================== TESTING WITH CLEAN ARCHITECTURE =====================

// Test doubles for repositories
class MockUserRepository : public IUserRepository {
public:
    std::optional<User> nextUser;
    std::vector<User> savedUsers;
    
    std::optional<User> findById(const std::string& id) override {
        return nextUser;
    }
    
    std::optional<User> findByEmail(const std::string& email) override {
        return nextUser;
    }
    
    void save(const User& user) override {
        savedUsers.push_back(user);
    }
    
    void update(const User& user) override {
        // Implementation
    }
    
    void deleteById(const std::string& id) override {
        // Implementation
    }
};

// Unit test for use case
void testRegisterUserUseCase() {
    // Arrange
    auto mockRepo = std::make_shared<MockUserRepository>();
    auto mockDispatcher = std::make_shared<SimpleEventDispatcher>();
    
    RegisterUserUseCase useCase(mockRepo, mockDispatcher);
    
    // Configure mock
    mockRepo->nextUser = std::nullopt; // No existing user
    
    // Act
    auto input = RegisterUserUseCase::Input{
        "test@example.com", "Test User", "password123"};
    
    auto output = useCase.execute(input);
    
    // Assert
    assert(!output.userId.empty());
    assert(output.email == "test@example.com");
    assert(output.name == "Test User");
    assert(mockRepo->savedUsers.size() == 1);
    assert(mockRepo->savedUsers[0].getEmail() == "test@example.com");
}

// Integration test
void testUserRegistrationFlow() {
    // Create real infrastructure for integration test
    auto db = std::make_shared<DatabaseConnection>();
    db->connect(":memory:"); // In-memory database for testing
    
    // Create and initialize test database
    db->execute("CREATE TABLE users (id TEXT, email TEXT, name TEXT, is_active BOOLEAN)");
    
    auto eventDispatcher = std::make_shared<SimpleEventDispatcher>();
    auto userRepo = std::make_shared<DatabaseUserRepository>(db);
    
    // Register event handler for testing
    bool eventHandled = false;
    eventDispatcher->registerHandler("UserRegistered", 
        [&eventHandled](const DomainEvent& event) {
            eventHandled = true;
            std::cout << "Test event handler called!" << std::endl;
        });
    
    // Execute use case
    RegisterUserUseCase useCase(userRepo, eventDispatcher);
    
    auto input = RegisterUserUseCase::Input{
        "integration@test.com", "Integration Test", "password"};
    
    auto output = useCase.execute(input);
    
    // Verify in database
    auto result = db->query("SELECT * FROM users WHERE email = ?", 
                           {"integration@test.com"});
    
    assert(!result.rows.empty());
    assert(eventHandled);
}

// ===================== MAIN APPLICATION =====================

int main(int argc, char* argv[]) {
    try {
        // Compose application based on configuration
        std::shared_ptr<RestUserController> controller;
        
        if (argc > 1 && std::string(argv[1]) == "--console") {
            auto console = ApplicationCompositionRoot::createConsoleInterface();
            console->run();
        } else {
            controller = ApplicationCompositionRoot::createRestController();
            
            // Simulate HTTP request (in real app, this would be from web framework)
            std::string response = controller->handlePost(
                "/api/users/register",
                "{\"email\": \"user@example.com\", \"name\": \"John Doe\", \"password\": \"secret\"}"
            );
            
            std::cout << "HTTP Response: " << response << std::endl;
        }
        
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Application error: " << e.what() << std::endl;
        return 1;
    }
}


// LargeScaleRefactoring.hpp - Strategies for large-scale refactoring in C++
#pragma once

#include <memory>
#include <string>
#include <vector>
#include <map>
#include <functional>
#include <iostream>
#include <chrono>

// ===================== BEFORE REFACTORING (LEGACY CODE) =====================

// Problem: Monolithic class with multiple responsibilities
class LegacyOrderProcessor {
private:
    std::map<std::string, double> inventory;
    std::map<std::string, std::string> customerDatabase;
    std::vector<std::string> orderLog;
    
public:
    LegacyOrderProcessor() {
        // Initialize with hardcoded data
        inventory["ITEM001"] = 99.99;
        inventory["ITEM002"] = 49.99;
        inventory["ITEM003"] = 19.99;
        
        customerDatabase["CUST001"] = "John Doe";
        customerDatabase["CUST002"] = "Jane Smith";
    }
    
    // Too many responsibilities in one method
    std::string processOrder(const std::string& customerId, 
                            const std::string& itemId, 
                            int quantity) {
        
        // 1. Validate customer
        auto custIt = customerDatabase.find(customerId);
        if (custIt == customerDatabase.end()) {
            return "Error: Customer not found";
        }
        
        // 2. Validate item
        auto itemIt = inventory.find(itemId);
        if (itemIt == inventory.end()) {
            return "Error: Item not found";
        }
        
        // 3. Calculate price
        double unitPrice = itemIt->second;
        double totalPrice = unitPrice * quantity;
        
        // 4. Apply discount
        if (quantity > 10) {
            totalPrice *= 0.9; // 10% discount for bulk
        }
        
        // 5. Calculate tax
        double tax = totalPrice * 0.08;
        double finalPrice = totalPrice + tax;
        
        // 6. Generate invoice
        std::string invoice = "INVOICE\n";
        invoice += "Customer: " + custIt->second + "\n";
        invoice += "Item: " + itemId + "\n";
        invoice += "Quantity: " + std::to_string(quantity) + "\n";
        invoice += "Unit Price: $" + std::to_string(unitPrice) + "\n";
        invoice += "Total: $" + std::to_string(finalPrice) + "\n";
        
        // 7. Log order
        orderLog.push_back("Order processed: " + customerId + " - " + itemId);
        
        // 8. Update inventory (missing)
        // 9. Send notification (missing)
        
        return invoice;
    }
    
    // Another method with similar issues
    double calculateShipping(const std::string& customerId, 
                           const std::string& itemId, 
                           int quantity) {
        // Mixed concerns: shipping calculation + customer lookup
        auto custIt = customerDatabase.find(customerId);
        if (custIt == customerDatabase.end()) {
            return -1.0;
        }
        
        auto itemIt = inventory.find(itemId);
        if (itemIt == inventory.end()) {
            return -1.0;
        }
        
        double weight = quantity * 0.5; // Assume 0.5kg per item
        double distance = getCustomerDistance(customerId); // Hidden dependency
        
        return weight * distance * 0.1;
    }
    
private:
    double getCustomerDistance(const std::string& customerId) {
        // Hardcoded distances
        if (customerId == "CUST001") return 10.0;
        if (customerId == "CUST002") return 25.0;
        return 50.0;
    }
};

// ===================== REFACTORING STRATEGY 1: EXTRACT METHOD =====================

class Step1_ExtractedMethods {
private:
    std::map<std::string, double> inventory;
    std::map<std::string, std::string> customerDatabase;
    std::vector<std::string> orderLog;
    
public:
    std::string processOrder(const std::string& customerId, 
                            const std::string& itemId, 
                            int quantity) {
        
        // Extract validation
        std::string validationError = validateOrder(customerId, itemId, quantity);
        if (!validationError.empty()) {
            return validationError;
        }
        
        // Extract price calculation
        double unitPrice = getItemPrice(itemId);
        double totalPrice = calculatePrice(unitPrice, quantity);
        
        // Extract tax calculation
        double tax = calculateTax(totalPrice);
        double finalPrice = totalPrice + tax;
        
        // Extract invoice generation
        std::string invoice = generateInvoice(customerId, itemId, quantity, 
                                             unitPrice, finalPrice);
        
        // Extract logging
        logOrder(customerId, itemId);
        
        return invoice;
    }
    
private:
    // Extracted methods (still in same class)
    std::string validateOrder(const std::string& customerId,
                             const std::string& itemId,
                             int quantity) {
        if (customerDatabase.find(customerId) == customerDatabase.end()) {
            return "Error: Customer not found";
        }
        if (inventory.find(itemId) == inventory.end()) {
            return "Error: Item not found";
        }
        if (quantity <= 0) {
            return "Error: Invalid quantity";
        }
        return "";
    }
    
    double getItemPrice(const std::string& itemId) {
        return inventory[itemId];
    }
    
    double calculatePrice(double unitPrice, int quantity) {
        double total = unitPrice * quantity;
        if (quantity > 10) {
            total *= 0.9; // 10% discount for bulk
        }
        return total;
    }
    
    double calculateTax(double amount) {
        return amount * 0.08;
    }
    
    std::string generateInvoice(const std::string& customerId,
                               const std::string& itemId,
                               int quantity,
                               double unitPrice,
                               double finalPrice) {
        std::string invoice = "INVOICE\n";
        invoice += "Customer: " + customerDatabase[customerId] + "\n";
        invoice += "Item: " + itemId + "\n";
        invoice += "Quantity: " + std::to_string(quantity) + "\n";
        invoice += "Unit Price: $" + std::to_string(unitPrice) + "\n";
        invoice += "Total: $" + std::to_string(finalPrice) + "\n";
        return invoice;
    }
    
    void logOrder(const std::string& customerId, const std::string& itemId) {
        orderLog.push_back("Order processed: " + customerId + " - " + itemId);
    }
};

// ===================== REFACTORING STRATEGY 2: EXTRACT CLASS =====================

// Start extracting classes for different responsibilities
class CustomerRepository {
private:
    std::map<std::string, std::string> customers;
    
public:
    CustomerRepository() {
        customers["CUST001"] = "John Doe";
        customers["CUST002"] = "Jane Smith";
    }
    
    bool customerExists(const std::string& customerId) const {
        return customers.find(customerId) != customers.end();
    }
    
    std::string getCustomerName(const std::string& customerId) const {
        auto it = customers.find(customerId);
        return it != customers.end() ? it->second : "";
    }
    
    double getCustomerDistance(const std::string& customerId) const {
        // Could be moved to a separate CustomerService
        if (customerId == "CUST001") return 10.0;
        if (customerId == "CUST002") return 25.0;
        return 50.0;
    }
};

class InventoryRepository {
private:
    std::map<std::string, double> items;
    
public:
    InventoryRepository() {
        items["ITEM001"] = 99.99;
        items["ITEM002"] = 49.99;
        items["ITEM003"] = 19.99;
    }
    
    bool itemExists(const std::string& itemId) const {
        return items.find(itemId) != items.end();
    }
    
    double getItemPrice(const std::string& itemId) const {
        auto it = items.find(itemId);
        return it != items.end() ? it->second : 0.0;
    }
};

class PricingService {
public:
    double calculatePrice(double unitPrice, int quantity) const {
        double total = unitPrice * quantity;
        if (quantity > 10) {
            total *= 0.9; // 10% discount for bulk
        }
        return total;
    }
    
    double calculateTax(double amount) const {
        return amount * 0.08;
    }
};

class Step2_ExtractedClasses {
private:
    CustomerRepository customerRepo;
    InventoryRepository inventoryRepo;
    PricingService pricingService;
    std::vector<std::string> orderLog;
    
public:
    std::string processOrder(const std::string& customerId, 
                            const std::string& itemId, 
                            int quantity) {
        
        // Validate using repositories
        if (!customerRepo.customerExists(customerId)) {
            return "Error: Customer not found";
        }
        if (!inventoryRepo.itemExists(itemId)) {
            return "Error: Item not found";
        }
        if (quantity <= 0) {
            return "Error: Invalid quantity";
        }
        
        // Calculate using services
        double unitPrice = inventoryRepo.getItemPrice(itemId);
        double totalPrice = pricingService.calculatePrice(unitPrice, quantity);
        double tax = pricingService.calculateTax(totalPrice);
        double finalPrice = totalPrice + tax;
        
        // Generate invoice
        std::string invoice = generateInvoice(customerId, itemId, quantity, 
                                             unitPrice, finalPrice);
        
        // Log order
        logOrder(customerId, itemId);
        
        return invoice;
    }
    
private:
    std::string generateInvoice(const std::string& customerId,
                               const std::string& itemId,
                               int quantity,
                               double unitPrice,
                               double finalPrice) {
        std::string invoice = "INVOICE\n";
        invoice += "Customer: " + customerRepo.getCustomerName(customerId) + "\n";
        invoice += "Item: " + itemId + "\n";
        invoice += "Quantity: " + std::to_string(quantity) + "\n";
        invoice += "Unit Price: $" + std::to_string(unitPrice) + "\n";
        invoice += "Total: $" + std::to_string(finalPrice) + "\n";
        return invoice;
    }
    
    void logOrder(const std::string& customerId, const std::string& itemId) {
        orderLog.push_back("Order processed: " + customerId + " - " + itemId);
    }
};

// ===================== REFACTORING STRATEGY 3: INTRODUCE INTERFACES =====================

// Define interfaces for dependency inversion
class ICustomerRepository {
public:
    virtual ~ICustomerRepository() = default;
    virtual bool customerExists(const std::string& customerId) const = 0;
    virtual std::string getCustomerName(const std::string& customerId) const = 0;
    virtual double getCustomerDistance(const std::string& customerId) const = 0;
};

class IInventoryRepository {
public:
    virtual ~IInventoryRepository() = default;
    virtual bool itemExists(const std::string& itemId) const = 0;
    virtual double getItemPrice(const std::string& itemId) const = 0;
    virtual void updateStock(const std::string& itemId, int quantity) = 0;
};

class IPricingService {
public:
    virtual ~IPricingService() = default;
    virtual double calculatePrice(double unitPrice, int quantity) const = 0;
    virtual double calculateTax(double amount) const = 0;
    virtual double calculateShipping(double weight, double distance) const = 0;
};

class ILogger {
public:
    virtual ~ILogger() = default;
    virtual void log(const std::string& message) = 0;
};

// Concrete implementations
class DatabaseCustomerRepository : public ICustomerRepository {
public:
    bool customerExists(const std::string& customerId) const override {
        // Real database implementation
        return true;
    }
    
    std::string getCustomerName(const std::string& customerId) const override {
        return "John Doe (from DB)";
    }
    
    double getCustomerDistance(const std::string& customerId) const override {
        return 15.0; // From database
    }
};

class FileInventoryRepository : public IInventoryRepository {
public:
    bool itemExists(const std::string& itemId) const override {
        // Read from file
        return true;
    }
    
    double getItemPrice(const std::string& itemId) const override {
        return 99.99; // From file
    }
    
    void updateStock(const std::string& itemId, int quantity) override {
        // Update file
    }
};

class ConsoleLogger : public ILogger {
public:
    void log(const std::string& message) override {
        std::cout << "[LOG] " << message << std::endl;
    }
};

// ===================== REFACTORING STRATEGY 4: APPLICATION SERVICE =====================

class OrderProcessingService {
private:
    std::shared_ptr<ICustomerRepository> customerRepo;
    std::shared_ptr<IInventoryRepository> inventoryRepo;
    std::shared_ptr<IPricingService> pricingService;
    std::shared_ptr<ILogger> logger;
    
public:
    // Dependency injection
    OrderProcessingService(std::shared_ptr<ICustomerRepository> custRepo,
                          std::shared_ptr<IInventoryRepository> invRepo,
                          std::shared_ptr<IPricingService> priceService,
                          std::shared_ptr<ILogger> log)
        : customerRepo(std::move(custRepo))
        , inventoryRepo(std::move(invRepo))
        , pricingService(std::move(priceService))
        , logger(std::move(log)) {}
    
    struct OrderResult {
        bool success;
        std::string invoice;
        std::string errorMessage;
        double totalAmount;
    };
    
    OrderResult processOrder(const std::string& customerId,
                            const std::string& itemId,
                            int quantity) {
        // Validate
        auto validation = validateOrder(customerId, itemId, quantity);
        if (!validation.success) {
            logger->log("Order validation failed: " + validation.errorMessage);
            return validation;
        }
        
        try {
            // Calculate price
            double unitPrice = inventoryRepo->getItemPrice(itemId);
            double subtotal = pricingService->calculatePrice(unitPrice, quantity);
            double tax = pricingService->calculateTax(subtotal);
            double total = subtotal + tax;
            
            // Generate invoice
            std::string invoice = generateInvoice(customerId, itemId, quantity,
                                                 unitPrice, total);
            
            // Update inventory
            inventoryRepo->updateStock(itemId, -quantity);
            
            // Log success
            logger->log("Order processed successfully: " + customerId);
            
            return {true, invoice, "", total};
            
        } catch (const std::exception& e) {
            logger->log("Order processing error: " + std::string(e.what()));
            return {false, "", e.what(), 0.0};
        }
    }
    
    double calculateShipping(const std::string& customerId,
                           const std::string& itemId,
                           int quantity) {
        if (!customerRepo->customerExists(customerId) ||
            !inventoryRepo->itemExists(itemId)) {
            return -1.0;
        }
        
        double weight = quantity * 0.5;
        double distance = customerRepo->getCustomerDistance(customerId);
        
        return pricingService->calculateShipping(weight, distance);
    }
    
private:
    OrderResult validateOrder(const std::string& customerId,
                             const std::string& itemId,
                             int quantity) {
        if (!customerRepo->customerExists(customerId)) {
            return {false, "", "Customer not found", 0.0};
        }
        if (!inventoryRepo->itemExists(itemId)) {
            return {false, "", "Item not found", 0.0};
        }
        if (quantity <= 0) {
            return {false, "", "Invalid quantity", 0.0};
        }
        return {true, "", "", 0.0};
    }
    
    std::string generateInvoice(const std::string& customerId,
                               const std::string& itemId,
                               int quantity,
                               double unitPrice,
                               double totalPrice) {
        std::stringstream invoice;
        invoice << "INVOICE\n";
        invoice << "Customer: " << customerRepo->getCustomerName(customerId) << "\n";
        invoice << "Item: " << itemId << "\n";
        invoice << "Quantity: " << quantity << "\n";
        invoice << "Unit Price: $" << std::fixed << std::setprecision(2) << unitPrice << "\n";
        invoice << "Total: $" << std::fixed << std::setprecision(2) << totalPrice << "\n";
        return invoice.str();
    }
};

// ===================== REFACTORING STRATEGY 5: STRATEGY PATTERN =====================

// Extract varying algorithms
class IDiscountStrategy {
public:
    virtual ~IDiscountStrategy() = default;
    virtual double applyDiscount(double amount, int quantity) const = 0;
};

class BulkDiscountStrategy : public IDiscountStrategy {
public:
    double applyDiscount(double amount, int quantity) const override {
        if (quantity > 10) {
            return amount * 0.9; // 10% off for bulk
        }
        return amount;
    }
};

class SeasonalDiscountStrategy : public IDiscountStrategy {
public:
    double applyDiscount(double amount, int quantity) const override {
        // Check if it's holiday season
        auto now = std::chrono::system_clock::now();
        std::time_t time = std::chrono::system_clock::to_time_t(now);
        std::tm* tm = std::localtime(&time);
        
        if (tm->tm_mon == 11) { // December
            return amount * 0.8; // 20% off in December
        }
        return amount;
    }
};

class NoDiscountStrategy : public IDiscountStrategy {
public:
    double applyDiscount(double amount, int quantity) const override {
        return amount;
    }
};

class ConfigurablePricingService : public IPricingService {
private:
    std::shared_ptr<IDiscountStrategy> discountStrategy;
    double taxRate;
    
public:
    ConfigurablePricingService(std::shared_ptr<IDiscountStrategy> strategy,
                              double taxRate = 0.08)
        : discountStrategy(std::move(strategy))
        , taxRate(taxRate) {}
    
    double calculatePrice(double unitPrice, int quantity) const override {
        double total = unitPrice * quantity;
        return discountStrategy->applyDiscount(total, quantity);
    }
    
    double calculateTax(double amount) const override {
        return amount * taxRate;
    }
    
    double calculateShipping(double weight, double distance) const override {
        return weight * distance * 0.1;
    }
};

// ===================== REFACTORING STRATEGY 6: OBSERVER PATTERN =====================

// For cross-cutting concerns like logging, notifications, etc.
class IOrderObserver {
public:
    virtual ~IOrderObserver() = default;
    virtual void onOrderProcessed(const std::string& customerId,
                                 const std::string& itemId,
                                 double amount) = 0;
    virtual void onOrderFailed(const std::string& customerId,
                              const std::string& itemId,
                              const std::string& error) = 0;
};

class OrderLogger : public IOrderObserver {
public:
    void onOrderProcessed(const std::string& customerId,
                         const std::string& itemId,
                         double amount) override {
        std::cout << "[SUCCESS] Order: " << customerId << " - " 
                  << itemId << " - $" << amount << std::endl;
    }
    
    void onOrderFailed(const std::string& customerId,
                      const std::string& itemId,
                      const std::string& error) override {
        std::cerr << "[FAILED] Order: " << customerId << " - " 
                  << itemId << " - Error: " << error << std::endl;
    }
};

class InventoryUpdater : public IOrderObserver {
public:
    void onOrderProcessed(const std::string& customerId,
                         const std::string& itemId,
                         double amount) override {
        // Update inventory in real-time
        std::cout << "Updating inventory for item: " << itemId << std::endl;
    }
    
    void onOrderFailed(const std::string& customerId,
                      const std::string& itemId,
                      const std::string& error) override {
        // Nothing to do on failure
    }
};

class NotificationService : public IOrderObserver {
public:
    void onOrderProcessed(const std::string& customerId,
                         const std::string& itemId,
                         double amount) override {
        // Send email/SMS notification
        std::cout << "Sending confirmation to customer: " << customerId << std::endl;
    }
    
    void onOrderFailed(const std::string& customerId,
                      const std::string& itemId,
                      const std::string& error) override {
        // Send failure notification
        std::cout << "Notifying customer of failure: " << customerId << std::endl;
    }
};

// ===================== REFACTORING STRATEGY 7: FINAL REFACTORED VERSION =====================

class RefactoredOrderService {
private:
    std::shared_ptr<ICustomerRepository> customerRepo;
    std::shared_ptr<IInventoryRepository> inventoryRepo;
    std::shared_ptr<IPricingService> pricingService;
    std::vector<std::shared_ptr<IOrderObserver>> observers;
    
public:
    RefactoredOrderService(std::shared_ptr<ICustomerRepository> custRepo,
                          std::shared_ptr<IInventoryRepository> invRepo,
                          std::shared_ptr<IPricingService> priceService)
        : customerRepo(std::move(custRepo))
        , inventoryRepo(std::move(invRepo))
        , pricingService(std::move(priceService)) {}
    
    void addObserver(std::shared_ptr<IOrderObserver> observer) {
        observers.push_back(std::move(observer));
    }
    
    struct OrderRequest {
        std::string customerId;
        std::string itemId;
        int quantity;
    };
    
    struct OrderResponse {
        bool success;
        std::string orderId;
        std::string invoice;
        std::string errorMessage;
        double totalAmount;
    };
    
    OrderResponse processOrder(const OrderRequest& request) {
        // Validate
        auto validation = validateRequest(request);
        if (!validation.success) {
            notifyObserversFailure(request, validation.errorMessage);
            return validation;
        }
        
        try {
            // Process order
            auto result = executeOrder(request);
            
            // Notify success
            notifyObserversSuccess(request, result.totalAmount);
            
            return result;
            
        } catch (const std::exception& e) {
            std::string error = e.what();
            notifyObserversFailure(request, error);
            return {false, "", "", error, 0.0};
        }
    }
    
private:
    OrderResponse validateRequest(const OrderRequest& request) {
        if (!customerRepo->customerExists(request.customerId)) {
            return {false, "", "", "Customer not found", 0.0};
        }
        if (!inventoryRepo->itemExists(request.itemId)) {
            return {false, "", "", "Item not found", 0.0};
        }
        if (request.quantity <= 0) {
            return {false, "", "", "Invalid quantity", 0.0};
        }
        return {true, "", "", "", 0.0};
    }
    
    OrderResponse executeOrder(const OrderRequest& request) {
        // Generate order ID
        std::string orderId = generateOrderId();
        
        // Calculate prices
        double unitPrice = inventoryRepo->getItemPrice(request.itemId);
        double subtotal = pricingService->calculatePrice(unitPrice, request.quantity);
        double tax = pricingService->calculateTax(subtotal);
        double total = subtotal + tax;
        
        // Generate invoice
        std::string invoice = generateInvoice(orderId, request, unitPrice, total);
        
        // Update inventory
        inventoryRepo->updateStock(request.itemId, -request.quantity);
        
        return {true, orderId, invoice, "", total};
    }
    
    std::string generateOrderId() {
        static int counter = 0;
        return "ORD_" + std::to_string(++counter) + "_" + 
               std::to_string(std::time(nullptr));
    }
    
    std::string generateInvoice(const std::string& orderId,
                               const OrderRequest& request,
                               double unitPrice,
                               double totalPrice) {
        std::stringstream invoice;
        invoice << "=================================\n";
        invoice << "ORDER INVOICE: " << orderId << "\n";
        invoice << "=================================\n";
        invoice << "Customer: " << customerRepo->getCustomerName(request.customerId) << "\n";
        invoice << "Item: " << request.itemId << "\n";
        invoice << "Quantity: " << request.quantity << "\n";
        invoice << "Unit Price: $" << std::fixed << std::setprecision(2) << unitPrice << "\n";
        invoice << "Total: $" << std::fixed << std::setprecision(2) << totalPrice << "\n";
        invoice << "=================================\n";
        return invoice.str();
    }
    
    void notifyObserversSuccess(const OrderRequest& request, double amount) {
        for (const auto& observer : observers) {
            observer->onOrderProcessed(request.customerId, request.itemId, amount);
        }
    }
    
    void notifyObserversFailure(const OrderRequest& request, const std::string& error) {
        for (const auto& observer : observers) {
            observer->onOrderFailed(request.customerId, request.itemId, error);
        }
    }
};

// ===================== MIGRATION STRATEGY =====================

// Step 1: Create compatibility layer
class MigrationAdapter : public LegacyOrderProcessor {
private:
    std::shared_ptr<RefactoredOrderService> newService;
    
public:
    explicit MigrationAdapter(std::shared_ptr<RefactoredOrderService> service)
        : newService(std::move(service)) {}
    
    // Override legacy method to use new service
    std::string processOrder(const std::string& customerId, 
                            const std::string& itemId, 
                            int quantity) override {
        
        RefactoredOrderService::OrderRequest request{
            customerId, itemId, quantity};
        
        auto response = newService->processOrder(request);
        
        if (response.success) {
            return response.invoice;
        } else {
            return "Error: " + response.errorMessage;
        }
    }
};

// Step 2: Gradual migration
void gradualMigrationExample() {
    // Create new services
    auto customerRepo = std::make_shared<DatabaseCustomerRepository>();
    auto inventoryRepo = std::make_shared<FileInventoryRepository>();
    auto discountStrategy = std::make_shared<BulkDiscountStrategy>();
    auto pricingService = std::make_shared<ConfigurablePricingService>(discountStrategy);
    
    auto orderService = std::make_shared<RefactoredOrderService>(
        customerRepo, inventoryRepo, pricingService);
    
    // Add observers
    orderService->addObserver(std::make_shared<OrderLogger>());
    orderService->addObserver(std::make_shared<InventoryUpdater>());
    orderService->addObserver(std::make_shared<NotificationService>());
    
    // Create adapter for backward compatibility
    auto adapter = std::make_shared<MigrationAdapter>(orderService);
    
    // Phase 1: Use adapter for existing code
    std::string result = adapter->processOrder("CUST001", "ITEM001", 5);
    std::cout << "Legacy interface result:\n" << result << std::endl;
    
    // Phase 2: Gradually migrate to new interface
    RefactoredOrderService::OrderRequest newRequest{
        "CUST002", "ITEM002", 3};
    
    auto newResult = orderService->processOrder(newRequest);
    if (newResult.success) {
        std::cout << "\nNew interface result:\n" << newResult.invoice << std::endl;
    }
    
    // Phase 3: Eventually remove legacy code
    // Delete LegacyOrderProcessor and MigrationAdapter
}

// ===================== TESTING THE REFACTORED CODE =====================

// Mock implementations for testing
class MockCustomerRepository : public ICustomerRepository {
public:
    bool shouldExist = true;
    std::string customerName = "Test Customer";
    double customerDistance = 10.0;
    
    bool customerExists(const std::string&) const override {
        return shouldExist;
    }
    
    std::string getCustomerName(const std::string&) const override {
        return customerName;
    }
    
    double getCustomerDistance(const std::string&) const override {
        return customerDistance;
    }
};

class MockInventoryRepository : public IInventoryRepository {
public:
    bool shouldExist = true;
    double itemPrice = 100.0;
    
    bool itemExists(const std::string&) const override {
        return shouldExist;
    }
    
    double getItemPrice(const std::string&) const override {
        return itemPrice;
    }
    
    void updateStock(const std::string&, int) override {
        // Track calls if needed
    }
};

void testRefactoredOrderService() {
    // Arrange
    auto mockCustomerRepo = std::make_shared<MockCustomerRepository>();
    auto mockInventoryRepo = std::make_shared<MockInventoryRepository>();
    auto mockPricingService = std::make_shared<ConfigurablePricingService>(
        std::make_shared<NoDiscountStrategy>());
    
    RefactoredOrderService service(mockCustomerRepo, mockInventoryRepo, mockPricingService);
    
    // Add test observer
    class TestObserver : public IOrderObserver {
    public:
        bool successCalled = false;
        bool failureCalled = false;
        
        void onOrderProcessed(const std::string&, const std::string&, double) override {
            successCalled = true;
        }
        
        void onOrderFailed(const std::string&, const std::string&, const std::string&) override {
            failureCalled = true;
        }
    };
    
    auto testObserver = std::make_shared<TestObserver>();
    service.addObserver(testObserver);
    
    // Test successful order
    RefactoredOrderService::OrderRequest request{
        "CUST001", "ITEM001", 2};
    
    auto response = service.processOrder(request);
    
    assert(response.success);
    assert(!response.orderId.empty());
    assert(response.invoice.find("ORDER INVOICE") != std::string::npos);
    assert(testObserver->successCalled);
    assert(!testObserver->failureCalled);
    
    // Test failed order (customer doesn't exist)
    mockCustomerRepo->shouldExist = false;
    testObserver->successCalled = false;
    testObserver->failureCalled = false;
    
    auto failedResponse = service.processOrder(request);
    
    assert(!failedResponse.success);
    assert(failedResponse.errorMessage.find("Customer") != std::string::npos);
    assert(!testObserver->successCalled);
    assert(testObserver->failureCalled);
}

// ===================== BENEFITS OF REFACTORING =====================

/*
Benefits achieved through refactoring:

1. Single Responsibility Principle:
   - Each class has one clear responsibility
   - CustomerRepository handles customer data
   - InventoryRepository handles product data
   - PricingService handles price calculations
   - OrderService orchestrates the process

2. Open/Closed Principle:
   - New discount strategies can be added without modifying existing code
   - New observers can be added without changing OrderService
   - New repository implementations can be swapped

3. Liskov Substitution Principle:
   - Mock repositories can substitute real ones for testing
   - Different discount strategies are interchangeable

4. Interface Segregation Principle:
   - Small, focused interfaces
   - Clients only depend on methods they use

5. Dependency Inversion Principle:
   - High-level modules depend on abstractions
   - Dependency injection enables easy testing and configuration

6. Testability:
   - Each component can be tested in isolation
   - Mock dependencies enable unit testing
   - Clear separation of concerns

7. Maintainability:
   - Smaller, focused classes are easier to understand
   - Changes are isolated to specific components
   - Code is self-documenting through clear naming

8. Extensibility:
   - New features can be added with minimal changes
   - Observers allow cross-cutting concerns to be added easily
   - Strategies allow algorithms to be swapped at runtime
*/

int main() {
    std::cout << "=== Large-Scale Refactoring Example ===\n\n";
    
    // Demonstrate legacy code
    std::cout << "1. Legacy Code:\n";
    LegacyOrderProcessor legacy;
    std::string legacyResult = legacy.processOrder("CUST001", "ITEM001", 5);
    std::cout << legacyResult << "\n";
    
    // Demonstrate refactored code
    std::cout << "\n2. Refactored Code:\n";
    gradualMigrationExample();
    
    // Run tests
    std::cout << "\n3. Testing Refactored Code:\n";
    testRefactoredOrderService();
    std::cout << "All tests passed!\n";
    
    return 0;
}




