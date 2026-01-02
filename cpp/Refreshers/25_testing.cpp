//// UNIT TESTING

// math_operations.h
#pragma once

class MathOperations {
public:
    static int add(int a, int b);
    static int multiply(int a, int b);
    static double divide(double a, double b);
    static bool isPrime(int n);
    static int factorial(int n);
};

// math_operations.cpp
#include "math_operations.h"
#include <stdexcept>
#include <cmath>

int MathOperations::add(int a, int b) {
    return a + b;
}

int MathOperations::multiply(int a, int b) {
    return a * b;
}

double MathOperations::divide(double a, double b) {
    if (b == 0.0) {
        throw std::invalid_argument("Division by zero");
    }
    return a / b;
}

bool MathOperations::isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}

int MathOperations::factorial(int n) {
    if (n < 0) throw std::invalid_argument("Negative factorial");
    if (n == 0) return 1;
    return n * factorial(n - 1);
}

// math_operations_test.cpp
#include <gtest/gtest.h>
#include "math_operations.h"

// Basic assertion tests
TEST(MathOperationsTest, Addition) {
    // ASSERT_* macros terminate test on failure
    ASSERT_EQ(MathOperations::add(2, 3), 5);
    ASSERT_EQ(MathOperations::add(-1, 1), 0);
    ASSERT_EQ(MathOperations::add(0, 0), 0);
}

TEST(MathOperationsTest, Multiplication) {
    // EXPECT_* macros continue test after failure
    EXPECT_EQ(MathOperations::multiply(2, 3), 6);
    EXPECT_EQ(MathOperations::multiply(-2, 3), -6);
    EXPECT_EQ(MathOperations::multiply(0, 100), 0);
}

TEST(MathOperationsTest, Division) {
    EXPECT_DOUBLE_EQ(MathOperations::divide(10.0, 2.0), 5.0);
    EXPECT_NEAR(MathOperations::divide(1.0, 3.0), 0.333333, 1e-6);
    
    // Test exception throwing
    EXPECT_THROW(MathOperations::divide(5.0, 0.0), std::invalid_argument);
    EXPECT_NO_THROW(MathOperations::divide(5.0, 1.0));
}

// Parameterized tests
class PrimeTest : public testing::TestWithParam<std::tuple<int, bool>> {};

TEST_P(PrimeTest, ChecksPrimality) {
    auto [input, expected] = GetParam();
    EXPECT_EQ(MathOperations::isPrime(input), expected);
}

INSTANTIATE_TEST_SUITE_P(
    PrimeNumbers,
    PrimeTest,
    testing::Values(
        std::make_tuple(2, true),
        std::make_tuple(3, true),
        std::make_tuple(4, false),
        std::make_tuple(17, true),
        std::make_tuple(25, false),
        std::make_tuple(97, true),
        std::make_tuple(1, false),
        std::make_tuple(0, false),
        std::make_tuple(-5, false)
    )
);

// Type-parameterized tests
template<typename T>
class TypedMathTest : public testing::Test {
protected:
    T value;
};

using NumericTypes = testing::Types<int, long, float, double>;
TYPED_TEST_SUITE(TypedMathTest, NumericTypes);

TYPED_TEST(TypedMathTest, AdditionCommutative) {
    TypeParam a = 5;
    TypeParam b = 3;
    // Note: MathOperations only works with int/double, so we'd need a template version
    // This shows the pattern for type-parameterized tests
}

// Test Fixture
class StackTest : public testing::Test {
protected:
    // SetUp() is called before each test
    void SetUp() override {
        stack.push(10);
        stack.push(20);
        stack.push(30);
    }
    
    // TearDown() is called after each test
    void TearDown() override {
        // Cleanup if needed
    }
    
    // Helper functions
    int sumStack() {
        int total = 0;
        while (!stack.empty()) {
            total += stack.top();
            stack.pop();
        }
        return total;
    }
    
    std::stack<int> stack;
};

TEST_F(StackTest, InitialSize) {
    EXPECT_EQ(stack.size(), 3);
}

TEST_F(StackTest, TopElement) {
    EXPECT_EQ(stack.top(), 30);
    stack.pop();
    EXPECT_EQ(stack.top(), 20);
}

TEST_F(StackTest, Summation) {
    EXPECT_EQ(sumStack(), 60); // 10 + 20 + 30
    EXPECT_TRUE(stack.empty());
}

// Death tests (for testing fatal errors)
TEST(MathOperationsDeathTest, FactorialNegative) {
    // Test that factorial throws on negative input
    EXPECT_DEATH({
        MathOperations::factorial(-5);
    }, "Negative factorial");
}

// Main function for Google Test
int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    // Optional: Add custom test listeners
    testing::TestEventListeners& listeners = 
        testing::UnitTest::GetInstance()->listeners();
    
    // Add a custom printer (optional)
    // listeners.Append(new CustomTestListener());
    
    return RUN_ALL_TESTS();
}


// catch2_example.cpp
#define CATCH_CONFIG_MAIN  // Generates main()
#include <catch2/catch_all.hpp>
#include "math_operations.h"

// Basic tests
TEST_CASE("Math operations", "[math][basic]") {
    SECTION("Addition") {
        REQUIRE(MathOperations::add(2, 3) == 5);
        REQUIRE(MathOperations::add(-1, 1) == 0);
        REQUIRE(MathOperations::add(0, 0) == 0);
    }
    
    SECTION("Multiplication") {
        REQUIRE(MathOperations::multiply(2, 3) == 6);
        REQUIRE(MathOperations::multiply(-2, 3) == -6);
        REQUIRE(MathOperations::multiply(0, 100) == 0);
    }
}

// BDD-style tests
SCENARIO("Division operations", "[math][division]") {
    GIVEN("Two numbers a and b") {
        double a = 10.0;
        double b = 2.0;
        
        WHEN("b is not zero") {
            THEN("division should succeed") {
                REQUIRE(MathOperations::divide(a, b) == 5.0);
                REQUIRE_NOTHROW(MathOperations::divide(a, b));
            }
        }
        
        WHEN("b is zero") {
            b = 0.0;
            THEN("division should throw") {
                REQUIRE_THROWS_AS(MathOperations::divide(a, b), 
                                 std::invalid_argument);
                REQUIRE_THROWS_WITH(MathOperations::divide(a, b), 
                                   "Division by zero");
            }
        }
    }
}

// Parameterized tests with generators
TEST_CASE("Prime number detection", "[math][prime]") {
    auto [input, expected] = GENERATE(
        table<int, bool>({
            {2, true},
            {3, true},
            {4, false},
            {17, true},
            {25, false},
            {97, true},
            {1, false},
            {0, false},
            {-5, false}
        })
    );
    
    CAPTURE(input);  // Shows input value in failure messages
    REQUIRE(MathOperations::isPrime(input) == expected);
}

// Approximate comparisons
TEST_CASE("Floating point division", "[math][float]") {
    double result = MathOperations::divide(1.0, 3.0);
    REQUIRE(result == Approx(0.333333).epsilon(1e-6));
    REQUIRE(result == Approx(0.333333).margin(0.000001));
}

// Test fixtures in Catch2
class DatabaseFixture {
protected:
    DatabaseFixture() {
        // Setup - called before each test
        db.connect("test.db");
        db.createTable("users");
    }
    
    ~DatabaseFixture() {
        // Teardown - called after each test
        db.dropTable("users");
        db.disconnect();
    }
    
    struct MockDatabase {
        void connect(const std::string&) { /* ... */ }
        void createTable(const std::string&) { /* ... */ }
        void dropTable(const std::string&) { /* ... */ }
        void disconnect() { /* ... */ }
        int query(const std::string&) { return 42; }
    };
    
    MockDatabase db;
};

TEST_CASE_METHOD(DatabaseFixture, "Database operations", "[database]") {
    SECTION("Query execution") {
        REQUIRE(db.query("SELECT * FROM users") == 42);
    }
    
    SECTION("Multiple queries") {
        REQUIRE(db.query("SELECT COUNT(*) FROM users") == 42);
        REQUIRE(db.query("SELECT name FROM users") == 42);
    }
}

// Benchmarking with Catch2
TEST_CASE("Benchmark factorial", "[!benchmark]") {
    BENCHMARK("Factorial of 10") {
        return MathOperations::factorial(10);
    };
    
    BENCHMARK("Factorial of 20") {
        return MathOperations::factorial(20);
    };
}

// Matchers (Catch2 v3)
#ifdef CATCH_CONFIG_ENABLE_ALL_STRINGMAKERS
#include <catch2/matchers/catch_matchers_all.hpp>

TEST_CASE("String matchers", "[matchers]") {
    using namespace Catch::Matchers;
    
    std::string str = "Hello World";
    
    REQUIRE_THAT(str, StartsWith("Hello"));
    REQUIRE_THAT(str, EndsWith("World"));
    REQUIRE_THAT(str, Contains("lo Wo"));
    REQUIRE_THAT(str, Equals("Hello World"));
    REQUIRE_THAT(str, Matches("^Hello.*World$"));
}
#endif



//// MOCKING

// payment_processor.h - System to test
#pragma once
#include <string>
#include <memory>

// Interfaces for dependency injection
class IPaymentGateway {
public:
    virtual ~IPaymentGateway() = default;
    virtual bool processPayment(const std::string& cardNumber, 
                               double amount, 
                               const std::string& currency) = 0;
    virtual std::string getLastTransactionId() const = 0;
};

class ILogger {
public:
    virtual ~ILogger() = default;
    virtual void logInfo(const std::string& message) = 0;
    virtual void logError(const std::string& message) = 0;
    virtual void logDebug(const std::string& message) = 0;
};

class IDatabase {
public:
    virtual ~IDatabase() = default;
    virtual bool saveTransaction(const std::string& id, 
                                double amount, 
                                const std::string& status) = 0;
    virtual std::string getTransactionStatus(const std::string& id) = 0;
};

// Class under test using dependency injection
class PaymentProcessor {
private:
    std::shared_ptr<IPaymentGateway> paymentGateway;
    std::shared_ptr<ILogger> logger;
    std::shared_ptr<IDatabase> database;
    
public:
    PaymentProcessor(std::shared_ptr<IPaymentGateway> gateway,
                    std::shared_ptr<ILogger> log,
                    std::shared_ptr<IDatabase> db)
        : paymentGateway(gateway), logger(log), database(db) {}
    
    bool processOrder(const std::string& orderId, 
                     const std::string& cardNumber, 
                     double amount, 
                     const std::string& currency) {
        
        logger->logInfo("Processing order: " + orderId);
        
        try {
            // Process payment
            bool paymentSuccess = paymentGateway->processPayment(cardNumber, amount, currency);
            
            if (!paymentSuccess) {
                logger->logError("Payment failed for order: " + orderId);
                database->saveTransaction(orderId, amount, "FAILED");
                return false;
            }
            
            std::string transactionId = paymentGateway->getLastTransactionId();
            logger->logDebug("Payment successful. Transaction ID: " + transactionId);
            
            // Save transaction
            bool saveSuccess = database->saveTransaction(orderId, amount, "SUCCESS");
            
            if (!saveSuccess) {
                logger->logError("Failed to save transaction for order: " + orderId);
                return false;
            }
            
            logger->logInfo("Order processed successfully: " + orderId);
            return true;
            
        } catch (const std::exception& e) {
            logger->logError("Exception processing order " + orderId + ": " + e.what());
            return false;
        }
    }
    
    std::string checkOrderStatus(const std::string& orderId) {
        return database->getTransactionStatus(orderId);
    }
};

// Google Mock Tests
#include <gmock/gmock.h>
#include <gtest/gtest.h>

// Mock classes using Google Mock
class MockPaymentGateway : public IPaymentGateway {
public:
    MOCK_METHOD(bool, processPayment, 
                (const std::string& cardNumber, double amount, const std::string& currency), 
                (override));
    MOCK_METHOD(std::string, getLastTransactionId, (), (const, override));
};

class MockLogger : public ILogger {
public:
    MOCK_METHOD(void, logInfo, (const std::string& message), (override));
    MOCK_METHOD(void, logError, (const std::string& message), (override));
    MOCK_METHOD(void, logDebug, (const std::string& message), (override));
};

class MockDatabase : public IDatabase {
public:
    MOCK_METHOD(bool, saveTransaction, 
                (const std::string& id, double amount, const std::string& status), 
                (override));
    MOCK_METHOD(std::string, getTransactionStatus, (const std::string& id), (override));
};

// Test fixture
class PaymentProcessorTest : public testing::Test {
protected:
    void SetUp() override {
        mockGateway = std::make_shared<MockPaymentGateway>();
        mockLogger = std::make_shared<MockLogger>();
        mockDatabase = std::make_shared<MockDatabase>();
        
        processor = std::make_unique<PaymentProcessor>(mockGateway, mockLogger, mockDatabase);
    }
    
    void TearDown() override {
        // Verify all expectations were met
        testing::Mock::VerifyAndClearExpectations(mockGateway.get());
        testing::Mock::VerifyAndClearExpectations(mockLogger.get());
        testing::Mock::VerifyAndClearExpectations(mockDatabase.get());
    }
    
    std::shared_ptr<MockPaymentGateway> mockGateway;
    std::shared_ptr<MockLogger> mockLogger;
    std::shared_ptr<MockDatabase> mockDatabase;
    std::unique_ptr<PaymentProcessor> processor;
};

// Test cases
TEST_F(PaymentProcessorTest, SuccessfulPayment) {
    const std::string orderId = "ORD123";
    const std::string cardNumber = "4111111111111111";
    const double amount = 100.0;
    const std::string currency = "USD";
    const std::string transactionId = "TXN456";
    
    // Set expectations using Google Mock
    EXPECT_CALL(*mockLogger, logInfo("Processing order: ORD123"));
    
    // Expect payment gateway to be called with specific arguments
    EXPECT_CALL(*mockGateway, 
                processPayment(cardNumber, amount, currency))
        .WillOnce(testing::Return(true));
    
    EXPECT_CALL(*mockGateway, getLastTransactionId())
        .WillOnce(testing::Return(transactionId));
    
    EXPECT_CALL(*mockLogger, 
                logDebug("Payment successful. Transaction ID: TXN456"));
    
    EXPECT_CALL(*mockDatabase,
                saveTransaction(orderId, amount, "SUCCESS"))
        .WillOnce(testing::Return(true));
    
    EXPECT_CALL(*mockLogger,
                logInfo("Order processed successfully: ORD123"));
    
    // Execute the test
    bool result = processor->processOrder(orderId, cardNumber, amount, currency);
    
    // Verify result
    EXPECT_TRUE(result);
}

TEST_F(PaymentProcessorTest, FailedPayment) {
    EXPECT_CALL(*mockLogger, logInfo(testing::_));
    
    EXPECT_CALL(*mockGateway, processPayment(testing::_, testing::_, testing::_))
        .WillOnce(testing::Return(false));
    
    EXPECT_CALL(*mockLogger, logError(testing::Contains("Payment failed")));
    
    EXPECT_CALL(*mockDatabase, saveTransaction(testing::_, testing::_, "FAILED"))
        .WillOnce(testing::Return(true));
    
    EXPECT_CALL(*mockGateway, getLastTransactionId()).Times(0); // Never called
    
    bool result = processor->processOrder("ORD456", "5555555555554444", 50.0, "USD");
    EXPECT_FALSE(result);
}

TEST_F(PaymentProcessorTest, DatabaseSaveFailure) {
    EXPECT_CALL(*mockLogger, logInfo(testing::_));
    
    EXPECT_CALL(*mockGateway, processPayment(testing::_, testing::_, testing::_))
        .WillOnce(testing::Return(true));
    
    EXPECT_CALL(*mockGateway, getLastTransactionId())
        .WillOnce(testing::Return("TXN789"));
    
    EXPECT_CALL(*mockLogger, logDebug(testing::_));
    
    EXPECT_CALL(*mockDatabase, saveTransaction(testing::_, testing::_, "SUCCESS"))
        .WillOnce(testing::Return(false)); // Database fails
    
    EXPECT_CALL(*mockLogger, logError(testing::Contains("Failed to save transaction")));
    
    bool result = processor->processOrder("ORD789", "378282246310005", 75.0, "USD");
    EXPECT_FALSE(result);
}

TEST_F(PaymentProcessorTest, CheckOrderStatus) {
    const std::string orderId = "ORD999";
    const std::string expectedStatus = "PROCESSING";
    
    // Expect database to be called with specific order ID
    EXPECT_CALL(*mockDatabase, getTransactionStatus(orderId))
        .WillOnce(testing::Return(expectedStatus));
    
    std::string status = processor->checkOrderStatus(orderId);
    EXPECT_EQ(status, expectedStatus);
}

// Advanced mocking: Using matchers and actions
TEST_F(PaymentProcessorTest, PaymentWithMatchers) {
    using testing::_;
    using testing::AnyNumber;
    using testing::Ge;
    using testing::HasSubstr;
    using testing::Return;
    
    // Use matchers for more flexible expectations
    EXPECT_CALL(*mockGateway, processPayment(
        testing::MatchesRegex("\\d{16}"),  // Any 16-digit card
        Ge(0.0),                           // Amount >= 0
        testing::AnyOf("USD", "EUR", "GBP") // Specific currencies
    )).WillOnce(Return(true));
    
    EXPECT_CALL(*mockGateway, getLastTransactionId())
        .WillOnce(Return("MOCK_TXN"));
    
    EXPECT_CALL(*mockDatabase, saveTransaction(_, _, _))
        .WillOnce(Return(true));
    
    // Expect logInfo to be called at least once
    EXPECT_CALL(*mockLogger, logInfo(_)).Times(AnyNumber());
    
    // Expect specific error message pattern
    EXPECT_CALL(*mockLogger, logError(HasSubstr("failed")))
        .Times(0); // Should not be called in success case
    
    bool result = processor->processOrder("TEST123", "4012888888881881", 99.99, "USD");
    EXPECT_TRUE(result);
}

// Mocking with sequences and ordering
TEST_F(PaymentProcessorTest, VerifyCallOrder) {
    testing::Sequence seq;
    
    // Verify call order
    EXPECT_CALL(*mockLogger, logInfo("Processing order: ORD111"))
        .InSequence(seq);
    
    EXPECT_CALL(*mockGateway, processPayment(_, _, _))
        .InSequence(seq)
        .WillOnce(Return(true));
    
    EXPECT_CALL(*mockGateway, getLastTransactionId())
        .InSequence(seq)
        .WillOnce(Return("TXN111"));
    
    EXPECT_CALL(*mockLogger, logDebug(_))
        .InSequence(seq);
    
    EXPECT_CALL(*mockDatabase, saveTransaction(_, _, _))
        .InSequence(seq)
        .WillOnce(Return(true));
    
    EXPECT_CALL(*mockLogger, logInfo("Order processed successfully: ORD111"))
        .InSequence(seq);
    
    processor->processOrder("ORD111", "4222222222222", 25.0, "USD");
}

// Mocking exceptions
TEST_F(PaymentProcessorTest, GatewayThrowsException) {
    EXPECT_CALL(*mockLogger, logInfo(_));
    
    EXPECT_CALL(*mockGateway, processPayment(_, _, _))
        .WillOnce(testing::Throw(std::runtime_error("Network error")));
    
    EXPECT_CALL(*mockLogger, logError(testing::Contains("Exception processing order")));
    
    EXPECT_CALL(*mockDatabase, saveTransaction(_, _, _)).Times(0);
    
    bool result = processor->processOrder("ORD222", "5105105105105100", 150.0, "USD");
    EXPECT_FALSE(result);
}

// Manual mocks (without Google Mock)
class ManualMockPaymentGateway : public IPaymentGateway {
public:
    bool processPaymentCalled = false;
    std::string lastCardNumber;
    double lastAmount;
    std::string lastCurrency;
    bool processPaymentResult = true;
    std::string transactionId = "MOCK_TXN";
    
    bool processPayment(const std::string& cardNumber, 
                       double amount, 
                       const std::string& currency) override {
        processPaymentCalled = true;
        lastCardNumber = cardNumber;
        lastAmount = amount;
        lastCurrency = currency;
        return processPaymentResult;
    }
    
    std::string getLastTransactionId() const override {
        return transactionId;
    }
};

TEST(ManualMockTest, SimpleMocking) {
    auto mockGateway = std::make_shared<ManualMockPaymentGateway>();
    auto mockLogger = std::make_shared<MockLogger>(); // Still using GMock for logger
    auto mockDatabase = std::make_shared<MockDatabase>();
    
    PaymentProcessor processor(mockGateway, mockLogger, mockDatabase);
    
    // Setup expectations
    EXPECT_CALL(*mockLogger, logInfo(_)).Times(testing::AtLeast(1));
    EXPECT_CALL(*mockDatabase, saveTransaction(_, _, "SUCCESS"))
        .WillOnce(testing::Return(true));
    
    // Execute
    bool result = processor.processOrder("TEST", "1234567812345678", 99.99, "USD");
    
    // Verify manual mock
    EXPECT_TRUE(result);
    EXPECT_TRUE(mockGateway->processPaymentCalled);
    EXPECT_EQ(mockGateway->lastCardNumber, "1234567812345678");
    EXPECT_EQ(mockGateway->lastAmount, 99.99);
    EXPECT_EQ(mockGateway->lastCurrency, "USD");
}


//// PROPERTY-BASED TESTING WITH HYPOTHESIS

// hypothesis_example.cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <cassert>
#include <rapidcheck.h>  // Hypothesis-like library for C++
#include "math_operations.h"

// Basic property-based test
void testAdditionCommutative() {
    rc::check("Addition is commutative", [](int a, int b) {
        // For all integers a and b, a + b == b + a
        RC_ASSERT(MathOperations::add(a, b) == MathOperations::add(b, a));
    });
}

void testAdditionAssociative() {
    rc::check("Addition is associative", [](int a, int b, int c) {
        // (a + b) + c == a + (b + c)
        int left = MathOperations::add(MathOperations::add(a, b), c);
        int right = MathOperations::add(a, MathOperations::add(b, c));
        RC_ASSERT(left == right);
    });
}

void testMultiplicationDistributive() {
    rc::check("Multiplication distributes over addition", 
             [](int a, int b, int c) {
        // a * (b + c) == (a * b) + (a * c)
        int left = MathOperations::multiply(a, MathOperations::add(b, c));
        int right = MathOperations::add(MathOperations::multiply(a, b),
                                       MathOperations::multiply(a, c));
        RC_ASSERT(left == right);
    });
}

void testDivisionProperty() {
    rc::check("Division property: (a * b) / b == a (when b != 0)",
             [](double a, double b) {
        RC_PRE(b != 0.0);  // Precondition
        
        double product = a * b;
        double result = MathOperations::divide(product, b);
        
        // Use relative tolerance for floating point
        RC_ASSERT(std::abs(result - a) < 1e-9);
    });
}

// Custom generator for prime numbers
bool isPrime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}

// Property: Product of two primes > 1 has at least 3 divisors
void testPrimeMultiplication() {
    rc::check("Product of primes has at least 3 divisors",
             []() {
        // Generate primes using custom generator
        auto primeGen = rc::gen::suchThat<int>(rc::gen::inRange(2, 1000), 
                                             [](int n) { return isPrime(n); });
        
        int p1 = *primeGen;
        int p2 = *primeGen;
        
        int product = p1 * p2;
        
        // Count divisors
        int divisorCount = 0;
        for (int i = 1; i <= product; ++i) {
            if (product % i == 0) {
                ++divisorCount;
            }
        }
        
        RC_ASSERT(divisorCount >= 3);  // At least 1, p1, p2, and product itself
        RC_ASSERT(product % p1 == 0);
        RC_ASSERT(product % p2 == 0);
    });
}

// Stateful property testing
struct Counter {
    int value = 0;
    
    void increment() { ++value; }
    void decrement() { --value; }
    void reset() { value = 0; }
};

void testCounterProperties() {
    rc::state::check(
        "Counter maintains invariant",
        // Initial state
        []() { return Counter(); },
        
        // Command generator
        [](const Counter& counter) {
            return rc::state::gen::oneOf(
                rc::state::gen::exec("increment", [](Counter& c) { c.increment(); }),
                rc::state::gen::exec("decrement", [](Counter& c) { c.decrement(); }),
                rc::state::gen::exec("reset", [](Counter& c) { c.reset(); })
            );
        },
        
        // Invariant: value should never go below -100 or above 100 in our tests
        [](const Counter& counter) {
            RC_ASSERT(counter.value >= -100);
            RC_ASSERT(counter.value <= 100);
        }
    );
}

// Testing sorting algorithms
void testSortingProperties() {
    rc::check("Sorting is idempotent", [](std::vector<int> vec) {
        auto sorted1 = vec;
        std::sort(sorted1.begin(), sorted1.end());
        
        auto sorted2 = sorted1;
        std::sort(sorted2.begin(), sorted2.end());
        
        RC_ASSERT(sorted1 == sorted2);
    });
    
    rc::check("Sorted vector is sorted", [](std::vector<int> vec) {
        auto sorted = vec;
        std::sort(sorted.begin(), sorted.end());
        
        for (size_t i = 1; i < sorted.size(); ++i) {
            RC_ASSERT(sorted[i-1] <= sorted[i]);
        }
    });
    
    rc::check("Sorting preserves elements", [](std::vector<int> vec) {
        auto sorted = vec;
        std::sort(sorted.begin(), sorted.end());
        
        // Count frequencies
        std::unordered_map<int, int> originalCount, sortedCount;
        for (int x : vec) originalCount[x]++;
        for (int x : sorted) sortedCount[x]++;
        
        RC_ASSERT(originalCount == sortedCount);
    });
}

// Custom data structure testing
template<typename T>
class Stack {
private:
    std::vector<T> data;
    
public:
    void push(const T& item) { data.push_back(item); }
    
    T pop() {
        if (empty()) throw std::runtime_error("Empty stack");
        T item = data.back();
        data.pop_back();
        return item;
    }
    
    const T& top() const {
        if (empty()) throw std::runtime_error("Empty stack");
        return data.back();
    }
    
    bool empty() const { return data.empty(); }
    size_t size() const { return data.size(); }
};

void testStackProperties() {
    rc::check("Push then pop returns original item", 
             [](int item) {
        Stack<int> stack;
        stack.push(item);
        RC_ASSERT(stack.pop() == item);
    });
    
    rc::check("Push increases size, pop decreases", 
             [](const std::vector<int>& items) {
        Stack<int> stack;
        size_t expectedSize = 0;
        
        for (int item : items) {
            stack.push(item);
            ++expectedSize;
            RC_ASSERT(stack.size() == expectedSize);
        }
        
        for (size_t i = 0; i < items.size(); ++i) {
            RC_ASSERT(!stack.empty());
            stack.pop();
            --expectedSize;
            RC_ASSERT(stack.size() == expectedSize);
        }
        
        RC_ASSERT(stack.empty());
    });
    
    rc::check("LIFO property", [](const std::vector<int>& items) {
        RC_PRE(items.size() >= 2);  // Need at least 2 items
        
        Stack<int> stack;
        for (int item : items) {
            stack.push(item);
        }
        
        // Last in, first out
        for (auto it = items.rbegin(); it != items.rend(); ++it) {
            RC_ASSERT(stack.pop() == *it);
        }
    });
}

// Shrinking demonstration
void testShrinkingExample() {
    rc::check("Division by zero detection",
             [](int a, int b) {
        // This will fail when b == 0
        int result = a / b;
        RC_ASSERT(result * b == a);  // This holds for integers when no remainder
    });
    // RapidCheck will find b = 0 and shrink to minimal counterexample
}

// Running property-based tests
int main() {
    std::cout << "Running property-based tests...\n";
    
    try {
        testAdditionCommutative();
        std::cout << "✓ Addition commutative property passed\n";
        
        testAdditionAssociative();
        std::cout << "✓ Addition associative property passed\n";
        
        testMultiplicationDistributive();
        std::cout << "✓ Multiplication distributive property passed\n";
        
        testDivisionProperty();
        std::cout << "✓ Division property passed\n";
        
        testPrimeMultiplication();
        std::cout << "✓ Prime multiplication property passed\n";
        
        testCounterProperties();
        std::cout << "✓ Counter properties passed\n";
        
        testSortingProperties();
        std::cout << "✓ Sorting properties passed\n";
        
        testStackProperties();
        std::cout << "✓ Stack properties passed\n";
        
        // testShrinkingExample();  // Uncomment to see shrinking in action
        
        std::cout << "\nAll property-based tests passed!\n";
        
    } catch (const rc::detail::CaseResult& result) {
        std::cerr << "\nProperty test failed!\n";
        std::cerr << "Counterexample found after " << result.numSuccess << " successes\n";
        
        if (!result.description.empty()) {
            std::cerr << "Description: " << result.description << "\n";
        }
        
        // RapidCheck automatically shrinks to minimal counterexample
        return 1;
    }
    
    return 0;
}


//// FUZZING

// fuzzing_example.cpp
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

// Target function to fuzz
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    // This is the entry point for libFuzzer
    
    if (size < 1) return 0;  // Reject empty inputs
    
    // Parse input (simple example)
    int value = 0;
    if (data[0] == 'A') {
        if (size > 1 && data[1] == 'B') {
            if (size > 2 && data[2] == 'C') {
                // Trigger a crash (for demonstration)
                if (size > 3 && data[3] == 'D') {
                    // Simulate a bug: null pointer dereference
                    int* ptr = nullptr;
                    *ptr = 42;  // CRASH!
                }
            }
        }
    }
    
    // Test string operations
    std::string input(reinterpret_cast<const char*>(data), size);
    
    // Look for specific patterns that might cause issues
    if (input.find("CRASH") != std::string::npos) {
        // Another crash scenario
        volatile int* crash_ptr = nullptr;
        *crash_ptr = 0xDEADBEEF;
    }
    
    // Test buffer operations
    if (size > 10) {
        // Potential buffer overflow
        char buffer[10];
        memcpy(buffer, data, size);  // Dangerous if size > 10
    }
    
    // Test integer overflow
    if (size >= sizeof(int)) {
        int num = *reinterpret_cast<const int*>(data);
        int result = num * 2;  // Could overflow
        
        // Check for specific problematic value
        if (num == 0x40000000) {
            // Trigger assertion failure
            assert(result > 0);
        }
    }
    
    return 0;  // Return 0 indicates successful execution
}

// Custom fuzzer with coverage guidance
class CustomFuzzer {
private:
    std::vector<uint8_t> corpus;
    size_t mutations = 1000;
    
    // Mutation strategies
    void bitFlip(uint8_t* data, size_t size) {
        if (size == 0) return;
        size_t pos = rand() % size;
        data[pos] ^= 1 << (rand() % 8);
    }
    
    void byteChange(uint8_t* data, size_t size) {
        if (size == 0) return;
        size_t pos = rand() % size;
        data[pos] = rand() % 256;
    }
    
    void insertByte(uint8_t*& data, size_t& size) {
        size_t pos = rand() % (size + 1);
        uint8_t* newData = new uint8_t[size + 1];
        
        memcpy(newData, data, pos);
        newData[pos] = rand() % 256;
        memcpy(newData + pos + 1, data + pos, size - pos);
        
        delete[] data;
        data = newData;
        size++;
    }
    
    void deleteByte(uint8_t*& data, size_t& size) {
        if (size <= 1) return;
        
        size_t pos = rand() % size;
        uint8_t* newData = new uint8_t[size - 1];
        
        memcpy(newData, data, pos);
        memcpy(newData + pos, data + pos + 1, size - pos - 1);
        
        delete[] data;
        data = newData;
        size--;
    }
    
public:
    void runFuzzing(const std::string& initialInput) {
        std::cout << "Starting custom fuzzer...\n";
        
        // Add initial input to corpus
        corpus.insert(corpus.end(), 
                     initialInput.begin(), 
                     initialInput.end());
        
        for (size_t i = 0; i < mutations; ++i) {
            // Create a mutation of the corpus
            size_t size = corpus.size();
            uint8_t* data = new uint8_t[size];
            memcpy(data, corpus.data(), size);
            
            // Apply random mutation
            int mutationType = rand() % 4;
            switch (mutationType) {
                case 0: bitFlip(data, size); break;
                case 1: byteChange(data, size); break;
                case 2: insertByte(data, size); break;
                case 3: deleteByte(data, size); break;
            }
            
            // Execute with mutated input
            try {
                LLVMFuzzerTestOneInput(data, size);
                
                // If execution was interesting (found new paths), 
                // add to corpus
                if (rand() % 10 == 0) {  // Simulated coverage feedback
                    corpus.assign(data, data + size);
                }
            }
            catch (...) {
                std::cout << "Exception caught with input of size " << size << "\n";
            }
            
            delete[] data;
            
            if (i % 100 == 0) {
                std::cout << "Processed " << i << " mutations\n";
            }
        }
        
        std::cout << "Fuzzing completed. Corpus size: " << corpus.size() << "\n";
    }
};

// Example function to fuzz
int parseInteger(const char* str, size_t len) {
    if (len == 0) return 0;
    
    int result = 0;
    bool negative = false;
    size_t i = 0;
    
    if (str[0] == '-') {
        negative = true;
        i = 1;
    }
    
    for (; i < len; ++i) {
        if (str[i] < '0' || str[i] > '9') {
            return 0;  // Invalid character
        }
        
        // Check for overflow
        if (result > INT_MAX / 10) {
            return negative ? INT_MIN : INT_MAX;
        }
        
        result = result * 10 + (str[i] - '0');
    }
    
    return negative ? -result : result;
}

// Fuzzer for parseInteger
extern "C" int LLVMFuzzerTestOneInput_parseInteger(const uint8_t* data, size_t size) {
    if (size > 20) return 0;  // Limit input size
    
    // Ensure null termination for C string
    char* str = new char[size + 1];
    memcpy(str, data, size);
    str[size] = '\0';
    
    int result = parseInteger(str, size);
    
    // Check some properties
    if (size > 0 && data[0] != '-') {
        // Non-negative string should give non-negative result
        assert(result >= 0);
    }
    
    delete[] str;
    return 0;
}

// Memory sanitizer example
void memorySanitizerTest(const uint8_t* data, size_t size) {
    if (size < 4) return;
    
    int* array = new int[4];
    
    // Potential use of uninitialized memory
    if (data[0] > 128) {
        array[0] = 42;  // Initialize only sometimes
    }
    
    // Use potentially uninitialized value
    int value = array[0];  // MemorySanitizer would catch this
    
    delete[] array;
}

// Address sanitizer example
void addressSanitizerTest(const uint8_t* data, size_t size) {
    if (size < 10) return;
    
    char buffer[10];
    
    // Potential buffer overflow
    if (data[0] == 'O') {
        if (data[1] == 'V') {
            if (data[2] == 'E') {
                if (data[3] == 'R') {
                    // Trigger buffer overflow
                    memcpy(buffer, data, size);  // AddressSanitizer would catch this
                }
            }
        }
    }
    
    // Potential use-after-free
    if (data[0] == 'U') {
        int* ptr = new int(42);
        delete ptr;
        
        if (data[1] == 'A') {
            if (data[2] == 'F') {
                *ptr = 99;  // Use after free
            }
        }
    }
}

// Main function to demonstrate fuzzing
int main() {
    std::cout << "Fuzzing Examples\n";
    std::cout << "================\n\n";
    
    // Example of using libFuzzer (would normally be compiled separately)
    // $ clang++ -fsanitize=fuzzer,address fuzzing_example.cpp -o fuzzer
    // $ ./fuzzer corpus/
    
    // Custom fuzzer demonstration
    CustomFuzzer fuzzer;
    fuzzer.runFuzzing("TEST123");
    
    return 0;
}


//// INTEGRATION TESTING


// integration_testing.cpp
#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <thread>
#include <chrono>
#include <cstdlib>
#include <cassert>
#include <sstream>
#include <fstream>
#include <random>

// System components for integration testing
class Database {
private:
    std::vector<std::pair<std::string, std::string>> data;
    
public:
    bool connect(const std::string& connectionString) {
        std::cout << "Database connecting to: " << connectionString << "\n";
        return connectionString.find("test.db") != std::string::npos;
    }
    
    bool execute(const std::string& query) {
        std::cout << "Executing query: " << query << "\n";
        
        // Simulate query parsing
        if (query.find("INSERT") != std::string::npos) {
            // Extract key-value pair (simplified)
            size_t valuesPos = query.find("VALUES");
            if (valuesPos != std::string::npos) {
                std::string values = query.substr(valuesPos + 7);
                size_t commaPos = values.find(',');
                if (commaPos != std::string::npos) {
                    std::string key = values.substr(1, commaPos - 2);  // Remove quotes
                    std::string value = values.substr(commaPos + 2, 
                                                     values.length() - commaPos - 3);
                    data.emplace_back(key, value);
                }
            }
        }
        else if (query.find("SELECT") != std::string::npos) {
            return !data.empty();
        }
        
        return true;
    }
    
    void disconnect() {
        std::cout << "Database disconnected\n";
    }
    
    size_t getRecordCount() const {
        return data.size();
    }
};

class Cache {
private:
    std::unordered_map<std::string, std::string> cache;
    
public:
    void set(const std::string& key, const std::string& value) {
        cache[key] = value;
        std::cout << "Cache set: " << key << " = " << value << "\n";
    }
    
    std::string get(const std::string& key) {
        auto it = cache.find(key);
        if (it != cache.end()) {
            std::cout << "Cache hit: " << key << "\n";
            return it->second;
        }
        std::cout << "Cache miss: " << key << "\n";
        return "";
    }
    
    void clear() {
        cache.clear();
        std::cout << "Cache cleared\n";
    }
    
    size_t size() const {
        return cache.size();
    }
};

class ExternalService {
public:
    bool sendNotification(const std::string& recipient, 
                         const std::string& message) {
        std::cout << "Sending notification to " << recipient 
                  << ": " << message << "\n";
        
        // Simulate network failure sometimes
        static std::mt19937 rng(std::random_device{}());
        if (rng() % 10 == 0) {  // 10% failure rate
            std::cout << "Notification service unavailable\n";
            return false;
        }
        
        return true;
    }
    
    double getExchangeRate(const std::string& from, 
                          const std::string& to) {
        std::cout << "Getting exchange rate from " << from 
                  << " to " << to << "\n";
        
        // Simulate API call
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
        
        if (from == "USD" && to == "EUR") {
            return 0.85;
        } else if (from == "EUR" && to == "USD") {
            return 1.18;
        }
        
        return 1.0;
    }
};

// Integrated system
class ECommerceSystem {
private:
    Database db;
    Cache cache;
    ExternalService externalService;
    bool initialized = false;
    
public:
    bool initialize() {
        std::cout << "\n=== Initializing ECommerce System ===\n";
        
        if (!db.connect("test.db")) {
            std::cerr << "Failed to connect to database\n";
            return false;
        }
        
        cache.clear();
        initialized = true;
        
        std::cout << "System initialized successfully\n";
        return true;
    }
    
    bool addProduct(const std::string& id, 
                   const std::string& name, 
                   double price, 
                   int stock) {
        if (!initialized) {
            std::cerr << "System not initialized\n";
            return false;
        }
        
        std::cout << "\n=== Adding Product ===\n";
        
        // Check cache first
        if (!cache.get(id).empty()) {
            std::cout << "Product already in cache\n";
            return false;
        }
        
        // Add to database
        std::stringstream query;
        query << "INSERT INTO products VALUES ('" << id << "', '" 
              << name << "', " << price << ", " << stock << ")";
        
        if (!db.execute(query.str())) {
            std::cerr << "Failed to add product to database\n";
            return false;
        }
        
        // Update cache
        std::stringstream cacheValue;
        cacheValue << name << "|" << price << "|" << stock;
        cache.set(id, cacheValue.str());
        
        // Send notification (async in real system)
        externalService.sendNotification("admin", 
                                        "Product added: " + name);
        
        std::cout << "Product added successfully: " << name << "\n";
        return true;
    }
    
    std::string getProductInfo(const std::string& id) {
        if (!initialized) {
            return "System not initialized";
        }
        
        std::cout << "\n=== Getting Product Info ===\n";
        
        // Try cache first
        std::string cached = cache.get(id);
        if (!cached.empty()) {
            return "From cache: " + cached;
        }
        
        // Query database
        std::string query = "SELECT * FROM products WHERE id = '" + id + "'";
        if (!db.execute(query)) {
            return "Product not found";
        }
        
        // In reality, would parse the result
        return "From database: Product " + id;
    }
    
    bool processOrder(const std::string& orderId, 
                     const std::string& productId, 
                     int quantity, 
                     const std::string& currency = "USD") {
        if (!initialized) {
            std::cerr << "System not initialized\n";
            return false;
        }
        
        std::cout << "\n=== Processing Order ===\n";
        
        // 1. Check product availability (simplified)
        std::string productInfo = cache.get(productId);
        if (productInfo.empty()) {
            std::cerr << "Product not found: " << productId << "\n";
            return false;
        }
        
        // 2. Convert currency if needed
        double price = 100.0;  // Simplified
        if (currency != "USD") {
            double rate = externalService.getExchangeRate("USD", currency);
            price *= rate;
        }
        
        // 3. Create order record
        std::stringstream query;
        query << "INSERT INTO orders VALUES ('" << orderId << "', '" 
              << productId << "', " << quantity << ", " << price << ")";
        
        if (!db.execute(query.str())) {
            std::cerr << "Failed to create order record\n";
            return false;
        }
        
        // 4. Update cache
        cache.set("order_" + orderId, "PROCESSED");
        
        // 5. Send notification
        externalService.sendNotification("customer", 
                                        "Order " + orderId + " processed");
        
        std::cout << "Order processed successfully: " << orderId << "\n";
        return true;
    }
    
    void shutdown() {
        std::cout << "\n=== Shutting Down System ===\n";
        db.disconnect();
        cache.clear();
        initialized = false;
        std::cout << "System shut down\n";
    }
    
    size_t getDatabaseRecordCount() const {
        // Would need real implementation
        return db.getRecordCount();
    }
};

// Integration test suite
class IntegrationTestSuite {
protected:
    ECommerceSystem system;
    
public:
    void runAllTests() {
        std::cout << "=======================================\n";
        std::cout << "   E-COMMERCE SYSTEM INTEGRATION TESTS\n";
        std::cout << "=======================================\n\n";
        
        testInitialization();
        testProductManagement();
        testOrderProcessing();
        testErrorConditions();
        testPerformance();
        testShutdown();
        
        std::cout << "\n=======================================\n";
        std::cout << "   ALL INTEGRATION TESTS COMPLETED\n";
        std::cout << "=======================================\n";
    }
    
    void testInitialization() {
        std::cout << "TEST: System Initialization\n";
        std::cout << "---------------------------\n";
        
        assert(!system.initialize());  // First init should fail without proper DB
        // Note: In real test, we'd mock or setup test database
        
        std::cout << "✓ Initialization test completed\n\n";
    }
    
    void testProductManagement() {
        std::cout << "TEST: Product Management\n";
        std::cout << "------------------------\n";
        
        // Test adding product
        bool added = system.addProduct("P001", "Laptop", 999.99, 10);
        assert(added);
        
        // Test retrieving product
        std::string info = system.getProductInfo("P001");
        assert(info.find("Laptop") != std::string::npos);
        
        // Test adding duplicate
        added = system.addProduct("P001", "Laptop", 999.99, 10);
        assert(!added);  // Should fail
        
        std::cout << "✓ Product management test completed\n\n";
    }
    
    void testOrderProcessing() {
        std::cout << "TEST: Order Processing\n";
        std::cout << "---------------------\n";
        
        // Setup product first
        system.addProduct("P002", "Phone", 499.99, 5);
        
        // Test successful order
        bool processed = system.processOrder("ORD001", "P002", 1);
        assert(processed);
        
        // Test with different currency
        processed = system.processOrder("ORD002", "P002", 1, "EUR");
        assert(processed);
        
        // Test invalid product
        processed = system.processOrder("ORD003", "INVALID", 1);
        assert(!processed);
        
        std::cout << "✓ Order processing test completed\n\n";
    }
    
    void testErrorConditions() {
        std::cout << "TEST: Error Conditions\n";
        std::cout << "---------------------\n";
        
        // Test without initialization
        ECommerceSystem uninitializedSystem;
        bool result = uninitializedSystem.addProduct("P003", "Tablet", 299.99, 3);
        assert(!result);
        
        // Test external service failure (simulated)
        // In real test, we'd mock the external service to fail
        
        std::cout << "✓ Error condition test completed\n\n";
    }
    
    void testPerformance() {
        std::cout << "TEST: Performance\n";
        std::cout << "-----------------\n";
        
        auto start = std::chrono::high_resolution_clock::now();
        
        // Simulate load
        for (int i = 0; i < 10; ++i) {
            std::string id = "PERF" + std::to_string(i);
            system.addProduct(id, "Product " + std::to_string(i), 
                             100.0 + i, i * 5);
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        std::cout << "Performance: Added 10 products in " 
                  << duration.count() << "ms\n";
        
        assert(duration.count() < 1000);  // Should complete in under 1 second
        
        std::cout << "✓ Performance test completed\n\n";
    }
    
    void testShutdown() {
        std::cout << "TEST: System Shutdown\n";
        std::cout << "---------------------\n";
        
        system.shutdown();
        
        // Verify system is in clean state
        // (In real test, check all resources are released)
        
        std::cout << "✓ Shutdown test completed\n\n";
    }
};

// API Integration Test
class APIIntegrationTest {
public:
    void testRESTAPI() {
        std::cout << "TEST: REST API Integration\n";
        std::cout << "--------------------------\n";
        
        // Simulate HTTP requests (in real test, use libcurl or similar)
        
        // Test GET request
        std::cout << "GET /api/products/P001\n";
        std::string response = simulateHTTPRequest("GET", "/api/products/P001");
        assert(!response.empty());
        
        // Test POST request
        std::cout << "POST /api/orders\n";
        std::string orderData = R"({"productId": "P001", "quantity": 2})";
        response = simulateHTTPRequest("POST", "/api/orders", orderData);
        assert(response.find("orderId") != std::string::npos);
        
        // Test error response
        std::cout << "GET /api/products/INVALID\n";
        response = simulateHTTPRequest("GET", "/api/products/INVALID");
        assert(response.find("404") != std::string::npos);
        
        std::cout << "✓ REST API test completed\n\n";
    }
    
    void testDatabaseIntegration() {
        std::cout << "TEST: Database Integration\n";
        std::cout << "--------------------------\n";
        
        // Setup test database
        system("sqlite3 test_integration.db \"CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT);\"");
        
        // Test connection
        Database db;
        bool connected = db.connect("test_integration.db");
        assert(connected);
        
        // Test queries
        bool executed = db.execute("INSERT INTO test VALUES (1, 'Integration Test')");
        assert(executed);
        
        // Cleanup
        system("rm -f test_integration.db");
        
        std::cout << "✓ Database integration test completed\n\n";
    }
    
private:
    std::string simulateHTTPRequest(const std::string& method, 
                                   const std::string& endpoint,
                                   const std::string& body = "") {
        // In real test, this would make actual HTTP requests
        // For this example, we simulate responses
        
        if (endpoint == "/api/products/P001") {
            return R"({"id": "P001", "name": "Laptop", "price": 999.99})";
        } else if (endpoint == "/api/orders" && method == "POST") {
            return R"({"orderId": "ORD_123", "status": "PROCESSED"})";
        } else if (endpoint.find("INVALID") != std::string::npos) {
            return R"({"error": "404 Not Found"})";
        }
        
        return R"({"error": "Unknown endpoint"})";
    }
};

// End-to-end test
void runEndToEndTest() {
    std::cout << "END-TO-END TEST: Complete User Journey\n";
    std::cout << "======================================\n\n";
    
    ECommerceSystem system;
    
    // 1. Initialize system
    std::cout << "1. Initializing system...\n";
    // (Would require actual database setup)
    
    // 2. Add products
    std::cout << "2. Adding products to catalog...\n";
    system.addProduct("E2E001", "Wireless Headphones", 199.99, 50);
    system.addProduct("E2E002", "Smart Watch", 299.99, 30);
    
    // 3. Customer browses products
    std::cout << "3. Customer browsing products...\n";
    std::string headphoneInfo = system.getProductInfo("E2E001");
    std::cout << "   Product info: " << headphoneInfo << "\n";
    
    // 4. Customer places order
    std::cout << "4. Customer placing order...\n";
    bool orderSuccess = system.processOrder("E2E_ORD_001", "E2E001", 2);
    std::cout << "   Order result: " << (orderSuccess ? "SUCCESS" : "FAILED") << "\n";
    
    // 5. System cleanup
    std::cout << "5. Cleaning up...\n";
    system.shutdown();
    
    std::cout << "\n✓ End-to-end test completed\n\n";
}

int main() {
    std::cout << "=======================================\n";
    std::cout << "   INTEGRATION TESTING DEMONSTRATION\n";
    std::cout << "=======================================\n\n";
    
    // Run integration test suite
    IntegrationTestSuite testSuite;
    testSuite.runAllTests();
    
    // Run API integration tests
    APIIntegrationTest apiTest;
    apiTest.testRESTAPI();
    apiTest.testDatabaseIntegration();
    
    // Run end-to-end test
    runEndToEndTest();
    
    return 0;
}


//// PERFORMANCE TESTING

// performance_testing.cpp
#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <algorithm>
#include <numeric>
#include <memory>
#include <map>
#include <unordered_map>
#include <benchmark/benchmark.h>  // Google Benchmark

// Microbenchmark examples using Google Benchmark
static void BM_VectorPushBack(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> v;
        for (int i = 0; i < state.range(0); ++i) {
            v.push_back(i);
        }
    }
    state.SetComplexityN(state.range(0));
}
BENCHMARK(BM_VectorPushBack)
    ->Range(8, 8<<10)  // Test from 8 to 8192 elements
    ->Complexity(benchmark::oN);

static void BM_StringCreation(benchmark::State& state) {
    for (auto _ : state) {
        std::string empty_string;
    }
}
BENCHMARK(BM_StringCreation);

static void BM_StringCopy(benchmark::State& state) {
    std::string x = "hello";
    for (auto _ : state) {
        std::string copy(x);
    }
}
BENCHMARK(BM_StringCopy);

// Compare different data structures
static void BM_MapInsert(benchmark::State& state) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 1000000);
    
    for (auto _ : state) {
        std::map<int, int> m;
        for (int i = 0; i < state.range(0); ++i) {
            m.insert({dis(gen), i});
        }
    }
}
BENCHMARK(BM_MapInsert)->Range(8, 8<<10);

static void BM_UnorderedMapInsert(benchmark::State& state) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 1000000);
    
    for (auto _ : state) {
        std::unordered_map<int, int> um;
        for (int i = 0; i < state.range(0); ++i) {
            um.insert({dis(gen), i});
        }
    }
}
BENCHMARK(BM_UnorderedMapInsert)->Range(8, 8<<10);

// Algorithm performance comparison
static void BM_STDSort(benchmark::State& state) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::vector<int> v(state.range(0));
    
    for (auto _ : state) {
        state.PauseTiming();
        std::generate(v.begin(), v.end(), [&]() { return gen() % 10000; });
        state.ResumeTiming();
        
        std::sort(v.begin(), v.end());
    }
}
BENCHMARK(BM_STDSort)->Range(8, 8<<12);

static void BM_STDStableSort(benchmark::State& state) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::vector<int> v(state.range(0));
    
    for (auto _ : state) {
        state.PauseTiming();
        std::generate(v.begin(), v.end(), [&]() { return gen() % 10000; });
        state.ResumeTiming();
        
        std::stable_sort(v.begin(), v.end());
    }
}
BENCHMARK(BM_STDStableSort)->Range(8, 8<<12);

// Memory allocation benchmarks
static void BM_NewDelete(benchmark::State& state) {
    const size_t size = state.range(0);
    
    for (auto _ : state) {
        char* p = new char[size];
        benchmark::DoNotOptimize(p);
        delete[] p;
    }
}
BENCHMARK(BM_NewDelete)->Range(8, 8<<10);

static void BM_MakeUnique(benchmark::State& state) {
    const size_t size = state.range(0);
    
    for (auto _ : state) {
        auto p = std::make_unique<char[]>(size);
        benchmark::DoNotOptimize(p);
    }
}
BENCHMARK(BM_MakeUnique)->Range(8, 8<<10);

// Cache performance testing
static void BM_CacheFriendly(benchmark::State& state) {
    const int size = state.range(0);
    std::vector<int> matrix(size * size);
    
    // Initialize matrix
    std::iota(matrix.begin(), matrix.end(), 0);
    
    for (auto _ : state) {
        int sum = 0;
        // Row-major traversal (cache-friendly)
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                sum += matrix[i * size + j];
            }
        }
        benchmark::DoNotOptimize(sum);
    }
}
BENCHMARK(BM_CacheFriendly)->Range(64, 512);

static void BM_CacheUnfriendly(benchmark::State& state) {
    const int size = state.range(0);
    std::vector<int> matrix(size * size);
    
    // Initialize matrix
    std::iota(matrix.begin(), matrix.end(), 0);
    
    for (auto _ : state) {
        int sum = 0;
        // Column-major traversal (cache-unfriendly)
        for (int j = 0; j < size; ++j) {
            for (int i = 0; i < size; ++i) {
                sum += matrix[i * size + j];
            }
        }
        benchmark::DoNotOptimize(sum);
    }
}
BENCHMARK(BM_CacheUnfriendly)->Range(64, 512);

// Custom performance test framework
class PerformanceTest {
public:
    struct TestResult {
        std::string name;
        double average_time_ms;
        double min_time_ms;
        double max_time_ms;
        double throughput;  // operations per second
    };
    
    virtual void setup() {}
    virtual void run() = 0;
    virtual void teardown() {}
    
    TestResult execute(int iterations = 1000, int warmup = 100) {
        // Warmup runs
        for (int i = 0; i < warmup; ++i) {
            run();
        }
        
        // Actual measurement
        std::vector<double> times;
        times.reserve(iterations);
        
        for (int i = 0; i < iterations; ++i) {
            auto start = std::chrono::high_resolution_clock::now();
            run();
            auto end = std::chrono::high_resolution_clock::now();
            
            double duration = std::chrono::duration<double, std::milli>(end - start).count();
            times.push_back(duration);
        }
        
        // Calculate statistics
        double sum = std::accumulate(times.begin(), times.end(), 0.0);
        double avg = sum / iterations;
        double min = *std::min_element(times.begin(), times.end());
        double max = *std::max_element(times.begin(), times.end());
        double throughput = 1000.0 / avg;  // operations per second
        
        return {typeid(*this).name(), avg, min, max, throughput};
    }
};

// Example performance test
class VectorPerformanceTest : public PerformanceTest {
private:
    std::vector<int> data;
    int result;
    
public:
    void setup() override {
        // Initialize with 1M elements
        data.resize(1000000);
        std::iota(data.begin(), data.end(), 0);
        result = 0;
    }
    
    void run() override {
        // Sum all elements
        result = std::accumulate(data.begin(), data.end(), 0);
        benchmark::DoNotOptimize(result);
    }
    
    void teardown() override {
        data.clear();
    }
};

class LinkedListPerformanceTest : public PerformanceTest {
private:
    struct Node {
        int value;
        Node* next;
    };
    
    Node* head;
    int result;
    
public:
    void setup() override {
        // Create linked list with 1M elements
        head = nullptr;
        for (int i = 0; i < 1000000; ++i) {
            Node* newNode = new Node{i, head};
            head = newNode;
        }
        result = 0;
    }
    
    void run() override {
        // Sum all elements
        Node* current = head;
        int sum = 0;
        while (current) {
            sum += current->value;
            current = current->next;
        }
        result = sum;
        benchmark::DoNotOptimize(result);
    }
    
    void teardown() override {
        // Clean up linked list
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }
};

// Memory bandwidth test
class MemoryBandwidthTest {
public:
    static double testReadBandwidth(size_t size) {
        std::vector<char> buffer(size, 1);
        volatile char sink;  // Prevent optimization
        
        auto start = std::chrono::high_resolution_clock::now();
        
        // Read entire buffer
        for (size_t i = 0; i < size; ++i) {
            sink = buffer[i];
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        
        double time_ms = std::chrono::duration<double, std::milli>(end - start).count();
        double bandwidth_mb_s = (size / (1024.0 * 1024.0)) / (time_ms / 1000.0);
        
        return bandwidth_mb_s;
    }
    
    static double testWriteBandwidth(size_t size) {
        std::vector<char> buffer(size);
        
        auto start = std::chrono::high_resolution_clock::now();
        
        // Write to entire buffer
        for (size_t i = 0; i < size; ++i) {
            buffer[i] = static_cast<char>(i);
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        
        double time_ms = std::chrono::duration<double, std::milli>(end - start).count();
        double bandwidth_mb_s = (size / (1024.0 * 1024.0)) / (time_ms / 1000.0);
        
        return bandwidth_mb_s;
    }
};

// Throughput testing
class ThroughputTest {
public:
    static void testHashThroughput() {
        const int operations = 1000000;
        std::unordered_map<int, int> map;
        
        auto start = std::chrono::high_resolution_clock::now();
        
        // Insert operations
        for (int i = 0; i < operations; ++i) {
            map[i] = i * 2;
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        
        double time_ms = std::chrono::duration<double, std::milli>(end - start).count();
        double throughput = operations / (time_ms / 1000.0);
        
        std::cout << "Hash map throughput: " << throughput << " ops/sec\n";
    }
};

// Latency testing
class LatencyTest {
public:
    static void testFunctionCallLatency() {
        const int iterations = 1000000;
        volatile int result = 0;
        
        auto noop = []() {};
        auto addOne = [](int x) { return x + 1; };
        
        // Test no-op latency
        auto start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < iterations; ++i) {
            noop();
        }
        auto end = std::chrono::high_resolution_clock::now();
        
        double time_ms = std::chrono::duration<double, std::milli>(end - start).count();
        double avg_latency_ns = (time_ms * 1000000.0) / iterations;
        
        std::cout << "No-op function call latency: " << avg_latency_ns << " ns\n";
        
        // Test actual function latency
        start = std::chrono::high_resolution_clock::now();
        for (int i = 0; i < iterations; ++i) {
            result = addOne(i);
        }
        end = std::chrono::high_resolution_clock::now();
        
        time_ms = std::chrono::duration<double, std::milli>(end - start).count();
        avg_latency_ns = (time_ms * 1000000.0) / iterations;
        
        std::cout << "Add-one function call latency: " << avg_latency_ns << " ns\n";
    }
};

// Run performance comparisons
void runPerformanceComparisons() {
    std::cout << "========================================\n";
    std::cout << "   PERFORMANCE TESTING DEMONSTRATION\n";
    std::cout << "========================================\n\n";
    
    // Compare vector vs linked list
    std::cout << "Comparing Vector vs Linked List Performance:\n";
    std::cout << "--------------------------------------------\n";
    
    VectorPerformanceTest vectorTest;
    vectorTest.setup();
    auto vectorResult = vectorTest.execute(100, 10);
    vectorTest.teardown();
    
    LinkedListPerformanceTest listTest;
    listTest.setup();
    auto listResult = listTest.execute(100, 10);
    listTest.teardown();
    
    std::cout << "Vector - Avg time: " << vectorResult.average_time_ms 
              << "ms, Throughput: " << vectorResult.throughput << " ops/sec\n";
    std::cout << "LinkedList - Avg time: " << listResult.average_time_ms 
              << "ms, Throughput: " << listResult.throughput << " ops/sec\n";
    
    double speedup = listResult.average_time_ms / vectorResult.average_time_ms;
    std::cout << "Vector is " << speedup << "x faster than LinkedList\n\n";
    
    // Memory bandwidth tests
    std::cout << "Memory Bandwidth Tests:\n";
    std::cout << "-----------------------\n";
    
    for (size_t size : {1 << 20, 10 << 20, 100 << 20}) {  // 1MB, 10MB, 100MB
        double read_bw = MemoryBandwidthTest::testReadBandwidth(size);
        double write_bw = MemoryBandwidthTest::testWriteBandwidth(size);
        
        std::cout << size / (1024 * 1024) << "MB - Read: " << read_bw 
                  << " MB/s, Write: " << write_bw << " MB/s\n";
    }
    std::cout << "\n";
    
    // Throughput tests
    std::cout << "Throughput Tests:\n";
    std::cout << "-----------------\n";
    ThroughputTest::testHashThroughput();
    std::cout << "\n";
    
    // Latency tests
    std::cout << "Latency Tests:\n";
    std::cout << "--------------\n";
    LatencyTest::testFunctionCallLatency();
}

int main(int argc, char** argv) {
    // Run custom performance tests
    runPerformanceComparisons();
    
    // Run Google Benchmark tests
    std::cout << "\nRunning Google Benchmark tests...\n";
    ::benchmark::Initialize(&argc, argv);
    if (::benchmark::ReportUnrecognizedArguments(argc, argv)) return 1;
    ::benchmark::RunSpecifiedBenchmarks();
    ::benchmark::Shutdown();
    
    return 0;
}



//// TESTING IN MULTITHREADED CODE

// deterministic_multithreading.cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>
#include <future>
#include <chrono>
#include <random>
#include <algorithm>
#include <condition_variable>
#include <queue>
#include <barrier>
#include <latch>
#include <semaphore>
#include <memory>
#include <cassert>

// Non-deterministic counter (problematic for testing)
class NonDeterministicCounter {
private:
    int value = 0;
    
public:
    void increment() {
        // This is NOT thread-safe
        int temp = value;
        std::this_thread::sleep_for(std::chrono::microseconds(1));
        value = temp + 1;
    }
    
    int get() const { return value; }
};

// Thread-safe counter using mutex
class MutexCounter {
private:
    int value = 0;
    std::mutex mtx;
    
public:
    void increment() {
        std::lock_guard<std::mutex> lock(mtx);
        value++;
    }
    
    int get() const {
        std::lock_guard<std::mutex> lock(mtx);
        return value;
    }
};

// Thread-safe counter using atomic
class AtomicCounter {
private:
    std::atomic<int> value{0};
    
public:
    void increment() {
        value.fetch_add(1, std::memory_order_relaxed);
    }
    
    int get() const {
        return value.load(std::memory_order_relaxed);
    }
};

// Test helper for deterministic thread scheduling
class DeterministicScheduler {
private:
    std::vector<std::function<void()>> tasks;
    std::vector<std::thread> threads;
    std::barrier<> sync_barrier;
    std::atomic<bool> start_flag{false};
    
public:
    DeterministicScheduler(size_t num_threads) 
        : sync_barrier(num_threads + 1) {  // +1 for main thread
        tasks.resize(num_threads);
    }
    
    void setTask(size_t thread_id, std::function<void()> task) {
        if (thread_id < tasks.size()) {
            tasks[thread_id] = std::move(task);
        }
    }
    
    void run() {
        // Create threads
        for (size_t i = 0; i < tasks.size(); ++i) {
            threads.emplace_back([this, i]() {
                sync_barrier.arrive_and_wait();  // Wait for all threads to be ready
                
                // Execute task
                if (tasks[i]) {
                    tasks[i]();
                }
                
                sync_barrier.arrive_and_wait();  // Wait for all threads to complete
            });
        }
        
        // Start all threads simultaneously
        sync_barrier.arrive_and_wait();
        
        // Wait for all threads to complete
        sync_barrier.arrive_and_wait();
        
        // Join threads
        for (auto& thread : threads) {
            thread.join();
        }
        
        threads.clear();
    }
};

// Deterministic test for counter
void testCounterDeterministic() {
    std::cout << "Testing counters deterministically...\n";
    
    const int NUM_THREADS = 4;
    const int INCREMENTS_PER_THREAD = 1000;
    
    // Test MutexCounter
    {
        MutexCounter counter;
        DeterministicScheduler scheduler(NUM_THREADS);
        
        for (int i = 0; i < NUM_THREADS; ++i) {
            scheduler.setTask(i, [&counter, INCREMENTS_PER_THREAD]() {
                for (int j = 0; j < INCREMENTS_PER_THREAD; ++j) {
                    counter.increment();
                }
            });
        }
        
        scheduler.run();
        
        int expected = NUM_THREADS * INCREMENTS_PER_THREAD;
        int actual = counter.get();
        
        std::cout << "MutexCounter: expected=" << expected 
                  << ", actual=" << actual 
                  << " -> " << (expected == actual ? "PASS" : "FAIL") << "\n";
        assert(expected == actual);
    }
    
    // Test AtomicCounter
    {
        AtomicCounter counter;
        DeterministicScheduler scheduler(NUM_THREADS);
        
        for (int i = 0; i < NUM_THREADS; ++i) {
            scheduler.setTask(i, [&counter, INCREMENTS_PER_THREAD]() {
                for (int j = 0; j < INCREMENTS_PER_THREAD; ++j) {
                    counter.increment();
                }
            });
        }
        
        scheduler.run();
        
        int expected = NUM_THREADS * INCREMENTS_PER_THREAD;
        int actual = counter.get();
        
        std::cout << "AtomicCounter: expected=" << expected 
                  << ", actual=" << actual 
                  << " -> " << (expected == actual ? "PASS" : "FAIL") << "\n";
        assert(expected == actual);
    }
    
    // Test NonDeterministicCounter (should fail)
    {
        NonDeterministicCounter counter;
        DeterministicScheduler scheduler(NUM_THREADS);
        
        for (int i = 0; i < NUM_THREADS; ++i) {
            scheduler.setTask(i, [&counter, INCREMENTS_PER_THREAD]() {
                for (int j = 0; j < INCREMENTS_PER_THREAD; ++j) {
                    counter.increment();
                }
            });
        }
        
        scheduler.run();
        
        int expected = NUM_THREADS * INCREMENTS_PER_THREAD;
        int actual = counter.get();
        
        std::cout << "NonDeterministicCounter: expected=" << expected 
                  << ", actual=" << actual 
                  << " -> " << (expected == actual ? "PASS" : "FAIL") << "\n";
        // This will likely fail due to race condition
    }
}

// Producer-consumer with deterministic testing
class ProducerConsumer {
private:
    std::queue<int> queue;
    std::mutex mtx;
    std::condition_variable cv;
    bool done = false;
    const size_t max_size;
    
public:
    ProducerConsumer(size_t max_size) : max_size(max_size) {}
    
    void produce(int value) {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this]() { return queue.size() < max_size || done; });
        
        if (!done) {
            queue.push(value);
            cv.notify_all();
        }
    }
    
    std::optional<int> consume() {
        std::unique_lock<std::mutex> lock(mtx);
        cv.wait(lock, [this]() { return !queue.empty() || done; });
        
        if (!queue.empty()) {
            int value = queue.front();
            queue.pop();
            cv.notify_all();
            return value;
        }
        
        return std::nullopt;
    }
    
    void finish() {
        std::lock_guard<std::mutex> lock(mtx);
        done = true;
        cv.notify_all();
    }
    
    size_t size() const {
        std::lock_guard<std::mutex> lock(mtx);
        return queue.size();
    }
};

void testProducerConsumerDeterministic() {
    std::cout << "\nTesting Producer-Consumer deterministically...\n";
    
    const int NUM_PRODUCERS = 2;
    const int NUM_CONSUMERS = 2;
    const int ITEMS_PER_PRODUCER = 50;
    
    ProducerConsumer pc(10);
    std::vector<int> consumed_items;
    std::mutex consumed_mtx;
    
    DeterministicScheduler scheduler(NUM_PRODUCERS + NUM_CONSUMERS);
    
    // Setup producers
    for (int i = 0; i < NUM_PRODUCERS; ++i) {
        scheduler.setTask(i, [&pc, ITEMS_PER_PRODUCER, i]() {
            for (int j = 0; j < ITEMS_PER_PRODUCER; ++j) {
                pc.produce(i * 1000 + j);
            }
        });
    }
    
    // Setup consumers
    for (int i = 0; i < NUM_CONSUMERS; ++i) {
        scheduler.setTask(NUM_PRODUCERS + i, [&pc, &consumed_items, &consumed_mtx]() {
            while (true) {
                auto item = pc.consume();
                if (!item) break;
                
                std::lock_guard<std::mutex> lock(consumed_mtx);
                consumed_items.push_back(*item);
            }
        });
    }
    
    // Run producers and consumers
    scheduler.run();
    
    // Signal completion and let consumers finish
    pc.finish();
    
    // Verify all items were produced and consumed
    int expected_total = NUM_PRODUCERS * ITEMS_PER_PRODUCER;
    int actual_total = consumed_items.size();
    
    std::cout << "Produced items: " << expected_total << "\n";
    std::cout << "Consumed items: " << actual_total << "\n";
    std::cout << "Queue size at end: " << pc.size() << "\n";
    
    assert(expected_total == actual_total);
    assert(pc.size() == 0);
    
    // Verify no duplicates
    std::sort(consumed_items.begin(), consumed_items.end());
    auto last = std::unique(consumed_items.begin(), consumed_items.end());
    assert(last == consumed_items.end());
    
    std::cout << "Producer-Consumer test: PASS\n";
}

// Transactional memory test
class BankAccount {
private:
    std::atomic<int> balance{0};
    
public:
    void deposit(int amount) {
        balance.fetch_add(amount, std::memory_order_release);
    }
    
    bool withdraw(int amount) {
        int current = balance.load(std::memory_order_acquire);
        
        // Retry loop for atomic compare-and-swap
        while (current >= amount) {
            if (balance.compare_exchange_weak(
                current, 
                current - amount,
                std::memory_order_release,
                std::memory_order_acquire)) {
                return true;
            }
        }
        return false;
    }
    
    int getBalance() const {
        return balance.load(std::memory_order_acquire);
    }
    
    bool transfer(BankAccount& to, int amount) {
        // This needs to be atomic - both withdraw and deposit
        if (withdraw(amount)) {
            to.deposit(amount);
            return true;
        }
        return false;
    }
};

void testBankAccountDeterministic() {
    std::cout << "\nTesting Bank Account transfers deterministically...\n";
    
    const int NUM_THREADS = 4;
    const int TRANSFERS_PER_THREAD = 100;
    const int INITIAL_BALANCE = 1000;
    
    BankAccount accounts[NUM_THREADS];
    
    // Initialize accounts
    for (int i = 0; i < NUM_THREADS; ++i) {
        accounts[i].deposit(INITIAL_BALANCE);
    }
    
    DeterministicScheduler scheduler(NUM_THREADS);
    
    for (int i = 0; i < NUM_THREADS; ++i) {
        scheduler.setTask(i, [&accounts, i, NUM_THREADS, TRANSFERS_PER_THREAD]() {
            std::random_device rd;
            std::mt19937 gen(rd());
            std::uniform_int_distribution<> amount_dist(1, 100);
            std::uniform_int_distribution<> target_dist(0, NUM_THREADS - 1);
            
            for (int j = 0; j < TRANSFERS_PER_THREAD; ++j) {
                int amount = amount_dist(gen);
                int target = target_dist(gen);
                
                if (target != i) {
                    accounts[i].transfer(accounts[target], amount);
                }
            }
        });
    }
    
    scheduler.run();
    
    // Verify conservation of money
    int total_balance = 0;
    for (int i = 0; i < NUM_THREADS; ++i) {
        total_balance += accounts[i].getBalance();
    }
    
    int expected_total = NUM_THREADS * INITIAL_BALANCE;
    
    std::cout << "Expected total balance: " << expected_total << "\n";
    std::cout << "Actual total balance: " << total_balance << "\n";
    std::cout << "Conservation of money: " 
              << (expected_total == total_balance ? "PASS" : "FAIL") << "\n";
    
    assert(expected_total == total_balance);
    
    // Verify no negative balances
    for (int i = 0; i < NUM_THREADS; ++i) {
        assert(accounts[i].getBalance() >= 0);
    }
    
    std::cout << "All accounts non-negative: PASS\n";
}

// Deadlock detection test
class Philosopher {
private:
    std::mutex& left_fork;
    std::mutex& right_fork;
    int id;
    
public:
    Philosopher(std::mutex& left, std::mutex& right, int id)
        : left_fork(left), right_fork(right), id(id) {}
    
    void dine() {
        while (true) {
            think();
            eat();
        }
    }
    
    void think() {
        std::cout << "Philosopher " << id << " is thinking\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    void eat() {
        // Potential deadlock: all philosophers pick up left fork first
        std::lock_guard<std::mutex> left_lock(left_fork);
        std::this_thread::sleep_for(std::chrono::milliseconds(50));  // Increase deadlock probability
        
        std::lock_guard<std::mutex> right_lock(right_fork);
        
        std::cout << "Philosopher " << id << " is eating\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
    
    // Deadlock-free version using std::lock
    void eat_safely() {
        std::unique_lock<std::mutex> left_lock(left_fork, std::defer_lock);
        std::unique_lock<std::mutex> right_lock(right_fork, std::defer_lock);
        
        std::lock(left_lock, right_lock);  // Atomic lock acquisition
        
        std::cout << "Philosopher " << id << " is eating safely\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }
};

void testDeadlockDetection() {
    std::cout << "\nTesting deadlock scenarios...\n";
    
    const int NUM_PHILOSOPHERS = 5;
    std::vector<std::mutex> forks(NUM_PHILOSOPHERS);
    std::vector<Philosopher> philosophers;
    std::vector<std::thread> threads;
    
    // Create philosophers
    for (int i = 0; i < NUM_PHILOSOPHERS; ++i) {
        philosophers.emplace_back(forks[i], forks[(i + 1) % NUM_PHILOSOPHERS], i);
    }
    
    // Start philosophers (this will likely deadlock)
    bool use_safe_version = true;  // Change to false to see deadlock
    
    if (!use_safe_version) {
        std::cout << "Starting unsafe dining (may deadlock)...\n";
        for (int i = 0; i < NUM_PHILOSOPHERS; ++i) {
            threads.emplace_back([&philosophers, i]() {
                philosophers[i].dine();
            });
        }
    } else {
        std::cout << "Starting safe dining...\n";
        for (int i = 0; i < NUM_PHILOSOPHERS; ++i) {
            threads.emplace_back([&philosophers, i]() {
                while (true) {
                    philosophers[i].think();
                    philosophers[i].eat_safely();
                }
            });
        }
    }
    
    // Run for a limited time
    std::this_thread::sleep_for(std::chrono::seconds(3));
    
    // Interrupt and join
    for (auto& thread : threads) {
        thread.detach();  // Can't join because they might be deadlocked
    }
    
    std::cout << "Test completed (if you see this, no deadlock occurred)\n";
}

// Race condition detection with ThreadSanitizer
void testDataRace() {
    std::cout << "\nTesting for data races...\n";
    
    int shared_data = 0;
    std::atomic<bool> ready{false};
    
    auto writer = [&shared_data, &ready]() {
        // This creates a data race
        shared_data = 42;
        ready.store(true, std::memory_order_release);
    };
    
    auto reader = [&shared_data, &ready]() {
        while (!ready.load(std::memory_order_acquire)) {
            std::this_thread::yield();
        }
        // This reads the potentially uninitialized value
        std::cout << "Reader sees: " << shared_data << "\n";
    };
    
    // ThreadSanitizer would catch this race
    std::thread t1(writer);
    std::thread t2(reader);
    
    t1.join();
    t2.join();
}

// Deterministic test runner
int main() {
    std::cout << "===========================================\n";
    std::cout << "   DETERMINISTIC MULTITHREADED TESTING\n";
    std::cout << "===========================================\n\n";
    
    // Run deterministic tests
    testCounterDeterministic();
    testProducerConsumerDeterministic();
    testBankAccountDeterministic();
    
    // Note: The following tests are non-deterministic by nature
    // They're included to show what to avoid in deterministic testing
    
    // Uncomment to see non-deterministic behavior
    // testDeadlockDetection();
    // testDataRace();
    
    std::cout << "\n===========================================\n";
    std::cout << "   ALL TESTS COMPLETED\n";
    std::cout << "===========================================\n";
    
    return 0;
}