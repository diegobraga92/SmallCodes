#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <memory>

// Basic exception throwing and catching
void basicExceptionExample() {
    try {
        std::cout << "Entering try block...\n";
        
        // Simulating an error condition
        int value = -1;
        if (value < 0) {
            // Throw a standard exception
            throw std::runtime_error("Negative value encountered!");
        }
        
        std::cout << "This line won't execute if exception is thrown\n";
    }
    catch (const std::runtime_error& e) {
        // Catch specific exception type
        std::cout << "Caught runtime_error: " << e.what() << "\n";
    }
    catch (const std::exception& e) {
        // Catch all exceptions derived from std::exception
        std::cout << "Caught standard exception: " << e.what() << "\n";
    }
    catch (...) {
        // Catch-all handler for any exception type
        std::cout << "Caught unknown exception type\n";
    }
    
    std::cout << "Program continues after exception handling\n";
}

// Multiple exception types
void multipleExceptionTypes() {
    std::cout << "\n=== Multiple Exception Types ===\n";
    
    try {
        int operation = 2; // Try changing this value
        
        if (operation == 1) {
            throw std::logic_error("Logic error: Invalid operation");
        }
        else if (operation == 2) {
            throw std::out_of_range("Out of range: Index too large");
        }
        else if (operation == 3) {
            throw std::bad_alloc(); // Memory allocation failure
        }
        else {
            throw 42; // Throwing non-standard type (int)
        }
    }
    catch (const std::logic_error& e) {
        std::cout << "Logic error handled: " << e.what() << "\n";
    }
    catch (const std::out_of_range& e) {
        std::cout << "Range error handled: " << e.what() << "\n";
    }
    catch (const std::exception& e) {
        std::cout << "General exception: " << e.what() << "\n";
    }
    catch (int errorCode) {
        std::cout << "Caught integer error code: " << errorCode << "\n";
    }
}

// Nested try-catch blocks
void nestedExceptionHandling() {
    std::cout << "\n=== Nested Exception Handling ===\n";
    
    try {
        std::cout << "Outer try block\n";
        
        try {
            std::cout << "Inner try block\n";
            throw std::runtime_error("Error from inner block");
            
            std::cout << "This won't execute\n";
        }
        catch (const std::runtime_error& e) {
            std::cout << "Inner catch: " << e.what() << "\n";
            // Re-throw to outer handler
            throw;
        }
        
        std::cout << "This also won't execute\n";
    }
    catch (const std::exception& e) {
        std::cout << "Outer catch (re-thrown): " << e.what() << "\n";
    }
}

int main() {
    basicExceptionExample();
    multipleExceptionTypes();
    nestedExceptionHandling();
    
    return 0;
}

#include <iostream>
#include <stdexcept>
#include <string>
#include <sstream>

// Base custom exception class
class DatabaseException : public std::runtime_error {
private:
    int errorCode;
    std::string sqlState;
    
public:
    DatabaseException(const std::string& message, int code, const std::string& state = "")
        : std::runtime_error(message), errorCode(code), sqlState(state) {}
    
    int getErrorCode() const { return errorCode; }
    std::string getSqlState() const { return sqlState; }
    
    virtual std::string getFullMessage() const {
        std::ostringstream oss;
        oss << "Database Error [" << errorCode << "]: " << what();
        if (!sqlState.empty()) {
            oss << " (SQL State: " << sqlState << ")";
        }
        return oss.str();
    }
};

// Derived exception classes
class ConnectionException : public DatabaseException {
public:
    ConnectionException(const std::string& message, int code = 1000)
        : DatabaseException(message, code, "08000") {} // Connection exception SQL state
        
    std::string getFullMessage() const override {
        return "Connection Failed: " + std::string(what());
    }
};

class QueryException : public DatabaseException {
private:
    std::string query;
    
public:
    QueryException(const std::string& message, const std::string& sql, int code = 2000)
        : DatabaseException(message, code, "42000"), query(sql) {} // Syntax error SQL state
        
    std::string getQuery() const { return query; }
    
    std::string getFullMessage() const override {
        std::ostringstream oss;
        oss << "Query Error in SQL: " << query << "\n";
        oss << "Reason: " << what();
        return oss.str();
    }
};

class DataIntegrityException : public DatabaseException {
public:
    DataIntegrityException(const std::string& message, int code = 3000)
        : DatabaseException(message, code, "23000") {} // Integrity constraint violation
        
    std::string getFullMessage() const override {
        return "Data Integrity Violation: " + std::string(what());
    }
};

// Using custom exceptions
class DatabaseConnection {
private:
    bool connected = false;
    
public:
    void connect() {
        if (!connected) {
            // Simulate connection failure
            throw ConnectionException("Could not connect to database server", 1001);
        }
    }
    
    void executeQuery(const std::string& query) {
        if (query.empty()) {
            throw QueryException("Empty query string", query, 2001);
        }
        
        if (query.find("DROP TABLE") != std::string::npos) {
            throw DataIntegrityException("DROP TABLE not allowed", 3001);
        }
        
        // Simulate successful query
        std::cout << "Executing: " << query << "\n";
    }
    
    void disconnect() {
        if (!connected) {
            throw std::logic_error("Not connected");
        }
    }
};

void customExceptionDemo() {
    std::cout << "\n=== Custom Exception Demo ===\n";
    
    DatabaseConnection db;
    
    try {
        std::cout << "Attempting to connect...\n";
        db.connect();
    }
    catch (const ConnectionException& e) {
        std::cout << "Connection error: " << e.getFullMessage() << "\n";
        std::cout << "Error code: " << e.getErrorCode() << "\n";
    }
    
    try {
        std::cout << "\nAttempting to execute query...\n";
        db.executeQuery("DROP TABLE users");
    }
    catch (const DataIntegrityException& e) {
        std::cout << "Data integrity error: " << e.getFullMessage() << "\n";
        std::cout << "SQL State: " << e.getSqlState() << "\n";
    }
    catch (const QueryException& e) {
        std::cout << "Query error: " << e.getFullMessage() << "\n";
    }
    catch (const DatabaseException& e) {
        std::cout << "Database error: " << e.getFullMessage() << "\n";
    }
}

int main() {
    customExceptionDemo();
    return 0;
}


//// STACK UNWINDING

#include <iostream>
#include <stdexcept>
#include <memory>
#include <vector>

// Resource management class to demonstrate RAII
class Resource {
private:
    int id;
    std::string name;
    
public:
    Resource(int id, const std::string& name) : id(id), name(name) {
        std::cout << "Resource " << id << " (" << name << ") constructed\n";
    }
    
    ~Resource() {
        std::cout << "Resource " << id << " (" << name << ") destroyed\n";
    }
    
    void use() {
        std::cout << "Using resource " << id << "\n";
    }
};

// Class that might throw during construction
class UnstableObject {
private:
    int value;
    
public:
    UnstableObject(int val) : value(val) {
        std::cout << "UnstableObject constructing with value " << val << "\n";
        
        if (val < 0) {
            throw std::runtime_error("Negative value not allowed");
        }
        
        if (val > 100) {
            throw std::out_of_range("Value too large");
        }
        
        std::cout << "UnstableObject constructed successfully\n";
    }
    
    ~UnstableObject() {
        std::cout << "UnstableObject destroyed\n";
    }
};

// Function demonstrating stack unwinding
void functionA();
void functionB();
void functionC();

void functionC() {
    std::cout << "\n=== Entering functionC ===\n";
    
    // Stack-allocated objects (RAII)
    Resource res1(1, "Local Resource in functionC");
    Resource res2(2, "Another Resource in functionC");
    
    std::cout << "Throwing exception from functionC...\n";
    throw std::runtime_error("Exception from deep in the call stack");
    
    std::cout << "This won't execute\n";
}

void functionB() {
    std::cout << "\n=== Entering functionB ===\n";
    
    Resource res(3, "Resource in functionB");
    
    // Smart pointer (also follows RAII)
    auto uniqueRes = std::make_unique<Resource>(4, "Unique Resource");
    
    functionC();
    
    std::cout << "This won't execute if functionC throws\n";
}

void functionA() {
    std::cout << "\n=== Entering functionA ===\n";
    
    Resource res(5, "Resource in functionA");
    
    try {
        functionB();
    }
    catch (const std::exception& e) {
        std::cout << "Caught exception in functionA: " << e.what() << "\n";
        // Continue unwinding
        throw;
    }
    
    std::cout << "This might not execute\n";
}

// Example with constructor exception
void constructorExceptionExample() {
    std::cout << "\n=== Constructor Exception Example ===\n";
    
    try {
        std::cout << "Creating objects...\n";
        
        Resource r1(10, "First");
        
        // This constructor will throw
        UnstableObject unstable(-5);
        
        // This never gets constructed
        Resource r2(11, "Second");
        
        std::cout << "All objects created successfully\n";
    }
    catch (const std::exception& e) {
        std::cout << "Caught exception: " << e.what() << "\n";
    }
}

// Vector example - what happens when push_back throws?
void vectorExceptionSafety() {
    std::cout << "\n=== Vector Exception Safety ===\n";
    
    std::vector<UnstableObject> objects;
    
    try {
        std::cout << "Adding stable object...\n";
        objects.emplace_back(50);  // This succeeds
        
        std::cout << "Adding unstable object...\n";
        objects.emplace_back(-10); // This throws
        
        std::cout << "Adding another object...\n";
        objects.emplace_back(30);  // This won't execute
    }
    catch (const std::exception& e) {
        std::cout << "Caught exception: " << e.what() << "\n";
        std::cout << "Vector size: " << objects.size() << "\n";
    }
}

int main() {
    std::cout << "=== Stack Unwinding Demonstration ===\n";
    
    try {
        functionA();
    }
    catch (const std::exception& e) {
        std::cout << "\nCaught exception in main: " << e.what() << "\n";
    }
    
    constructorExceptionExample();
    vectorExceptionSafety();
    
    return 0;
}


//// EXCEPTION SAFETY GUARANTEES

#include <iostream>
#include <stdexcept>
#include <vector>
#include <memory>
#include <algorithm>

// 1. NO-THROW GUARANTEE: Function never throws exceptions
class NoThrowClass {
private:
    int value;
    
public:
    // Destructors should provide no-throw guarantee
    ~NoThrowClass() noexcept {
        // Simple cleanup that can't fail
    }
    
    // Swap operations should be noexcept
    void swap(NoThrowClass& other) noexcept {
        using std::swap;
        swap(value, other.value);
    }
    
    // Simple getter - no-throw guarantee
    int getValue() const noexcept {
        return value;
    }
};

// 2. STRONG GUARANTEE: Operations succeed or leave state unchanged
class Transaction {
private:
    std::vector<int> data;
    std::vector<int> backup;
    
    void saveBackup() {
        backup = data;  // Can throw, but we handle it
    }
    
    void restoreFromBackup() {
        data = backup;  // Can throw
    }
    
public:
    // Strong guarantee: either succeeds or leaves object unchanged
    void addItemWithStrongGuarantee(int item) {
        saveBackup();  // Save current state
        
        try {
            data.push_back(item);  // Might throw bad_alloc
            
            // More operations that might fail
            if (item < 0) {
                throw std::runtime_error("Negative item");
            }
        }
        catch (...) {
            // Rollback on any exception
            restoreFromBackup();
            throw;  // Re-throw the exception
        }
        
        // Success - discard backup
        backup.clear();
    }
    
    // Alternative using copy-and-swap idiom (strong guarantee)
    void addItemCopyAndSwap(int item) {
        std::vector<int> newData = data;  // Copy current state
        newData.push_back(item);           // Modify the copy
        
        if (item < 0) {
            throw std::runtime_error("Negative item");
        }
        
        // Commit: swap old and new (no-throw guarantee for swap)
        data.swap(newData);
    }
};

// 3. BASIC GUARANTEE: No resource leaks, object remains in valid state
class BasicGuaranteeDatabase {
private:
    std::unique_ptr<int[]> buffer;
    size_t size;
    size_t capacity;
    
public:
    BasicGuaranteeDatabase(size_t initialCapacity = 10) 
        : buffer(std::make_unique<int[]>(initialCapacity))
        , size(0)
        , capacity(initialCapacity) {}
    
    // Basic guarantee: might leave object in different but valid state
    void addItemBasicGuarantee(int item) {
        if (size >= capacity) {
            // Need to resize - this operation can fail
            size_t newCapacity = capacity * 2;
            auto newBuffer = std::make_unique<int[]>(newCapacity);
            
            // Copy existing data (might throw)
            for (size_t i = 0; i < size; ++i) {
                newBuffer[i] = buffer[i];
            }
            
            // Commit changes (no-throw operations)
            buffer.swap(newBuffer);
            capacity = newCapacity;
        }
        
        // Add new item
        buffer[size] = item;
        ++size;  // Only update size after successful assignment
    }
    
    size_t getSize() const noexcept { return size; }
    size_t getCapacity() const noexcept { return capacity; }
};

// Example demonstrating different guarantees
class BankAccount {
private:
    double balance;
    std::vector<std::string> transactionLog;
    
public:
    BankAccount(double initialBalance) : balance(initialBalance) {}
    
    // Strong guarantee version
    void depositStrong(double amount) {
        if (amount <= 0) {
            throw std::invalid_argument("Deposit amount must be positive");
        }
        
        double oldBalance = balance;
        std::vector<std::string> oldLog = transactionLog;
        
        try {
            balance += amount;
            transactionLog.push_back("Deposited: $" + std::to_string(amount));
            
            // Simulate a failure point
            if (amount > 10000) {
                throw std::runtime_error("Large deposit requires verification");
            }
        }
        catch (...) {
            // Rollback on any exception
            balance = oldBalance;
            transactionLog = oldLog;
            throw;
        }
    }
    
    // Basic guarantee version (simpler, faster)
    void depositBasic(double amount) {
        if (amount <= 0) {
            throw std::invalid_argument("Deposit amount must be positive");
        }
        
        // Update balance first
        balance += amount;
        
        // Then log (might fail, but balance already updated)
        transactionLog.push_back("Deposited: $" + std::to_string(amount));
        
        // If logging fails, balance is correct but log is incomplete
        // Still a valid state (basic guarantee)
    }
    
    // No-throw getter
    double getBalance() const noexcept {
        return balance;
    }
    
    // Basic guarantee: might throw, but won't leak
    void printTransactions() const {
        std::cout << "Transaction History:\n";
        for (const auto& entry : transactionLog) {
            std::cout << "  " << entry << "\n";
        }
    }
};

void demonstrateExceptionGuarantees() {
    std::cout << "=== Exception Safety Guarantees ===\n\n";
    
    // 1. No-throw guarantee example
    std::cout << "1. NO-THROW GUARANTEE:\n";
    NoThrowClass obj1;
    std::cout << "No-throw getter: " << obj1.getValue() << "\n\n";
    
    // 2. Strong guarantee example
    std::cout << "2. STRONG GUARANTEE:\n";
    Transaction trans;
    
    try {
        trans.addItemWithStrongGuarantee(10);
        std::cout << "Added item 10 successfully\n";
        
        trans.addItemWithStrongGuarantee(-5);  // This will throw
        std::cout << "This won't execute\n";
    }
    catch (const std::exception& e) {
        std::cout << "Caught: " << e.what() << "\n";
        std::cout << "State unchanged (strong guarantee)\n";
    }
    
    // 3. Basic guarantee example
    std::cout << "\n3. BASIC GUARANTEE:\n";
    BasicGuaranteeDatabase db(2);
    
    try {
        db.addItemBasicGuarantee(1);
        db.addItemBasicGuarantee(2);
        db.addItemBasicGuarantee(3);  // Triggers resize
        
        std::cout << "Database size: " << db.getSize() << "\n";
        std::cout << "Database capacity: " << db.getCapacity() << "\n";
    }
    catch (const std::bad_alloc& e) {
        std::cout << "Memory allocation failed\n";
        std::cout << "Database is still valid (basic guarantee)\n";
    }
    
    // Bank account example
    std::cout << "\n4. BANK ACCOUNT EXAMPLE:\n";
    BankAccount account(1000.0);
    
    try {
        account.depositStrong(500.0);
        std::cout << "Strong deposit successful. Balance: $" << account.getBalance() << "\n";
        
        // This will trigger rollback
        account.depositStrong(15000.0);
    }
    catch (const std::exception& e) {
        std::cout << "Deposit failed: " << e.what() << "\n";
        std::cout << "Balance unchanged (strong guarantee): $" << account.getBalance() << "\n";
    }
}

int main() {
    demonstrateExceptionGuarantees();
    return 0;
}


//// WHEN NOT TO USE EXCEPTIONS

#include <iostream>
#include <stdexcept>
#include <optional>
#include <variant>
#include <expected>
#include <functional>
#include <chrono>
#include <fstream>
#include <system_error>

// 1. REAL-TIME SYSTEMS: Exceptions have unpredictable timing
class RealTimeController {
private:
    bool errorOccurred = false;
    std::string lastError;
    
public:
    // DON'T use exceptions for real-time error handling
    void processDataBad(int data) {
        if (data < 0) {
            throw std::runtime_error("Negative data"); // BAD: unpredictable
        }
        // Process data...
    }
    
    // DO use error codes or flags
    bool processDataGood(int data) {
        if (data < 0) {
            errorOccurred = true;
            lastError = "Negative data";
            return false;
        }
        
        // Process data...
        errorOccurred = false;
        return true;
    }
    
    bool hasError() const { return errorOccurred; }
    std::string getLastError() const { return lastError; }
};

// 2. DESTRUCTORS: Should not throw (C++ standard forbids throwing from destructor)
class ResourceHolder {
private:
    int* resource;
    
public:
    ResourceHolder() : resource(new int(42)) {}
    
    // BAD: Destructor throwing
    ~ResourceHolder() {
        // If delete throws, program terminates
        delete resource;
        
        // Never do this:
        // if (someCondition) {
        //     throw std::runtime_error("Error in destructor"); // TERMINATES PROGRAM
        // }
    }
    
    // GOOD: Separate cleanup function
    bool cleanup() noexcept {
        try {
            delete resource;
            resource = nullptr;
            return true;
        }
        catch (...) {
            // Log error but don't throw
            std::cerr << "Warning: Failed to cleanup resource\n";
            return false;
        }
    }
};

// 3. HIGH-FREQUENCY FUNCTIONS: Exception overhead in tight loops
void highFrequencyProcessing() {
    std::cout << "\n=== High Frequency Processing ===\n";
    
    // BAD: Using exceptions for normal control flow
    auto findValueBad = [](const std::vector<int>& vec, int target) {
        try {
            for (size_t i = 0; i < vec.size(); ++i) {
                if (vec[i] == target) {
                    throw i; // Using exception for normal flow
                }
            }
            throw -1;
        }
        catch (size_t index) {
            return static_cast<int>(index);
        }
        catch (int) {
            return -1;
        }
    };
    
    // GOOD: Using standard control flow
    auto findValueGood = [](const std::vector<int>& vec, int target) {
        for (size_t i = 0; i < vec.size(); ++i) {
            if (vec[i] == target) {
                return static_cast<int>(i);
            }
        }
        return -1;
    };
    
    // Performance comparison
    std::vector<int> data(1000);
    for (int i = 0; i < 1000; ++i) data[i] = i;
    
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000; ++i) {
        findValueGood(data, 999);
    }
    auto end = std::chrono::high_resolution_clock::now();
    std::cout << "Good version: " 
              << std::chrono::duration_cast<std::chrono::microseconds>(end - start).count()
              << " microseconds\n";
}

// 4. CROSS-LANGUAGE BOUNDARIES: Exceptions don't propagate through C interfaces
extern "C" {
    // C interface - can't use exceptions
    typedef struct {
        int error_code;
        char error_message[256];
    } ErrorInfo;
    
    int c_style_function(int input, ErrorInfo* error) {
        if (input < 0) {
            if (error) {
                error->error_code = 1;
                snprintf(error->error_message, sizeof(error->error_message),
                        "Negative input: %d", input);
            }
            return -1; // Error indicator
        }
        return input * 2; // Success
    }
}

// C++ wrapper for C interface
class CInterfaceWrapper {
public:
    // BAD: Trying to throw through C interface
    // int callWithException(int input) {
    //     ErrorInfo error;
    //     int result = c_style_function(input, &error);
    //     if (result == -1) {
    //         throw std::runtime_error(error.error_message); // Won't work across DLLs
    //     }
    //     return result;
    // }
    
    // GOOD: Using std::optional or similar
    std::optional<int> callWithOptional(int input) {
        ErrorInfo error = {};
        int result = c_style_function(input, &error);
        
        if (result == -1) {
            return std::nullopt; // Clear error indication
        }
        return result;
    }
    
    // GOOD: Using std::expected (C++23) or similar pattern
    struct Result {
        int value;
        std::string error;
    };
    
    Result callWithResult(int input) {
        ErrorInfo error = {};
        int result = c_style_function(input, &error);
        
        if (result == -1) {
            return {0, error.error_message};
        }
        return {result, ""};
    }
};

// 5. RECOVERABLE VS UNRECOVERABLE ERRORS
void errorHandlingStrategies() {
    std::cout << "\n=== Error Type Analysis ===\n";
    
    // UNRECOVERABLE ERRORS (Don't use exceptions)
    auto handleUnrecoverable = [](const std::string& message) {
        // BAD: Using exception for programming errors
        // throw std::logic_error(message);
        
        // GOOD: Assert or terminate
        std::cerr << "FATAL: " << message << "\n";
        std::abort(); // Or std::terminate()
    };
    
    // RECOVERABLE ERRORS (Good for exceptions)
    auto openFile = [](const std::string& filename) -> std::ifstream {
        std::ifstream file(filename);
        if (!file) {
            // GOOD: File not found is an exceptional condition
            throw std::runtime_error("Cannot open file: " + filename);
        }
        return file;
    };
    
    // EXPECTED FAILURES (Don't use exceptions)
    auto parseInteger = [](const std::string& str) -> std::optional<int> {
        try {
            return std::stoi(str);
        }
        catch (...) {
            // BAD: Using exception for expected failure
            // return -1 or throw?
            
            // GOOD: Using std::optional for expected failures
            return std::nullopt;
        }
    };
}

// 6. ALTERNATIVES TO EXCEPTIONS
void demonstrateAlternatives() {
    std::cout << "\n=== Alternatives to Exceptions ===\n";
    
    // 1. std::optional (C++17)
    std::cout << "1. std::optional:\n";
    auto divideOptional = [](double a, double b) -> std::optional<double> {
        if (b == 0) {
            return std::nullopt;
        }
        return a / b;
    };
    
    auto result1 = divideOptional(10, 2);
    if (result1) {
        std::cout << "10 / 2 = " << *result1 << "\n";
    } else {
        std::cout << "Division failed\n";
    }
    
    // 2. std::variant (C++17)
    std::cout << "\n2. std::variant:\n";
    using ParseResult = std::variant<int, std::string>;
    
    auto parseInput = [](const std::string& input) -> ParseResult {
        try {
            return std::stoi(input);
        }
        catch (...) {
            return "Invalid number: " + input;
        }
    };
    
    ParseResult res = parseInput("123");
    if (std::holds_alternative<int>(res)) {
        std::cout << "Parsed: " << std::get<int>(res) << "\n";
    } else {
        std::cout << "Error: " << std::get<std::string>(res) << "\n";
    }
    
    // 3. std::expected (C++23) or similar
    std::cout << "\n3. Expected-like pattern:\n";
    template<typename T, typename E>
    class Expected {
    private:
        union {
            T value;
            E error;
        };
        bool hasValue;
        
    public:
        Expected(const T& v) : value(v), hasValue(true) {}
        Expected(const E& e) : error(e), hasValue(false) {}
        
        ~Expected() {
            if (hasValue) {
                value.~T();
            } else {
                error.~E();
            }
        }
        
        explicit operator bool() const { return hasValue; }
        T& getValue() { return value; }
        E& getError() { return error; }
    };
    
    // 4. Error codes with enums
    std::cout << "\n4. Error codes:\n";
    enum class FileError {
        Success,
        NotFound,
        PermissionDenied,
        DiskFull,
        InvalidFormat
    };
    
    struct FileResult {
        FileError error;
        std::string content;
    };
    
    auto readFile = [](const std::string& path) -> FileResult {
        std::ifstream file(path);
        if (!file) {
            return {FileError::NotFound, ""};
        }
        
        std::string content;
        if (!std::getline(file, content)) {
            return {FileError::InvalidFormat, ""};
        }
        
        return {FileError::Success, content};
    };
    
    auto fileResult = readFile("nonexistent.txt");
    if (fileResult.error == FileError::Success) {
        std::cout << "File content: " << fileResult.content << "\n";
    } else {
        std::cout << "File error code: " << static_cast<int>(fileResult.error) << "\n";
    }
}

// 7. WHEN TO USE EXCEPTIONS (Summary)
void exceptionGuidelines() {
    std::cout << "\n=== Exception Usage Guidelines ===\n\n";
    
    std::cout << "USE EXCEPTIONS FOR:\n";
    std::cout << "1. Errors that can't be handled locally\n";
    std::cout << "2. Constructor failures\n";
    std::cout << "3. Resource acquisition failures\n";
    std::cout << "4. API contract violations\n";
    std::cout << "5. Out-of-memory conditions\n\n";
    
    std::cout << "AVOID EXCEPTIONS FOR:\n";
    std::cout << "1. Normal control flow\n";
    std::cout << "2. High-frequency error checking\n";
    std::cout << "3. Destructor error handling\n";
    std::cout << "4. Real-time systems\n";
    std::cout << "5. Expected failure cases\n";
    std::cout << "6. Cross-language boundaries\n";
    std::cout << "7. Programming errors (use asserts)\n";
}

int main() {
    RealTimeController rtc;
    if (!rtc.processDataGood(-5)) {
        std::cout << "Error: " << rtc.getLastError() << "\n";
    }
    
    highFrequencyProcessing();
    errorHandlingStrategies();
    demonstrateAlternatives();
    exceptionGuidelines();
    
    return 0;
}


