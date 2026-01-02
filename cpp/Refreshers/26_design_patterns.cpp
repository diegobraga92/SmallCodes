#include <iostream>
#include <memory>
#include <unordered_map>
#include <functional>
#include <string>

// ========== SIMPLE FACTORY ==========
class Document {
public:
    virtual void open() = 0;
    virtual void save() = 0;
    virtual ~Document() = default;
    
    // Modern C++: Use type traits
    using DocumentType = std::string;
    virtual DocumentType type() const = 0;
};

class PdfDocument : public Document {
public:
    void open() override {
        std::cout << "Opening PDF document\n";
        // PDF-specific opening logic
    }
    
    void save() override {
        std::cout << "Saving PDF document\n";
        // PDF-specific saving logic
    }
    
    DocumentType type() const override {
        return "application/pdf";
    }
    
    // PDF-specific functionality
    void setEncryption(const std::string& password) {
        std::cout << "Setting PDF encryption with password\n";
    }
};

class WordDocument : public Document {
public:
    void open() override {
        std::cout << "Opening Word document\n";
        // Word-specific opening logic
    }
    
    void save() override {
        std::cout << "Saving Word document\n";
        // Word-specific saving logic
    }
    
    DocumentType type() const override {
        return "application/msword";
    }
    
    // Word-specific functionality
    void trackChanges(bool enable) {
        std::cout << (enable ? "Enabling" : "Disabling") << " track changes\n";
    }
};

// Simple Factory using enum
enum class DocumentType { PDF, WORD };

class DocumentFactory {
public:
    static std::unique_ptr<Document> create(DocumentType type) {
        switch (type) {
            case DocumentType::PDF:
                return std::make_unique<PdfDocument>();
            case DocumentType::WORD:
                return std::make_unique<WordDocument>();
            default:
                throw std::invalid_argument("Unknown document type");
        }
    }
};

// ========== FACTORY METHOD ==========
class Application {
protected:
    virtual std::unique_ptr<Document> createDocument() = 0;
    
public:
    void newDocument() {
        std::cout << "Creating new document...\n";
        auto doc = createDocument();
        doc->open();
        // Add to document list, etc.
    }
    
    virtual ~Application() = default;
};

class PdfApplication : public Application {
protected:
    std::unique_ptr<Document> createDocument() override {
        return std::make_unique<PdfDocument>();
    }
};

class WordApplication : public Application {
protected:
    std::unique_ptr<Document> createDocument() override {
        return std::make_unique<WordDocument>();
    }
};

// ========== ABSTRACT FACTORY ==========
// Related object families
class Theme {
public:
    virtual ~Theme() = default;
    virtual std::string backgroundColor() const = 0;
    virtual std::string textColor() const = 0;
};

class Button {
public:
    virtual ~Button() = default;
    virtual void render() const = 0;
    virtual void onClick() = 0;
};

class LightTheme : public Theme {
public:
    std::string backgroundColor() const override {
        return "#FFFFFF";
    }
    
    std::string textColor() const override {
        return "#000000";
    }
};

class DarkTheme : public Theme {
public:
    std::string backgroundColor() const override {
        return "#121212";
    }
    
    std::string textColor() const override {
        return "#E0E0E0";
    }
};

class LightButton : public Button {
public:
    void render() const override {
        std::cout << "Rendering light button\n";
    }
    
    void onClick() override {
        std::cout << "Light button clicked\n";
    }
};

class DarkButton : public Button {
public:
    void render() const override {
        std::cout << "Rendering dark button\n";
    }
    
    void onClick() override {
        std::cout << "Dark button clicked\n";
    }
};

// Abstract Factory interface
class UIFactory {
public:
    virtual ~UIFactory() = default;
    virtual std::unique_ptr<Theme> createTheme() = 0;
    virtual std::unique_ptr<Button> createButton() = 0;
};

class LightUIFactory : public UIFactory {
public:
    std::unique_ptr<Theme> createTheme() override {
        return std::make_unique<LightTheme>();
    }
    
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<LightButton>();
    }
};

class DarkUIFactory : public UIFactory {
public:
    std::unique_ptr<Theme> createTheme() override {
        return std::make_unique<DarkTheme>();
    }
    
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<DarkButton>();
    }
};

// ========== MODERN C++ FACTORY (Type-safe) ==========
class ModernFactory {
private:
    // Registry of creators using std::function
    std::unordered_map<std::string, std::function<std::unique_ptr<Document>()>> creators;
    
public:
    // Register a creator function
    template<typename T>
    void registerType(const std::string& typeName) {
        creators[typeName] = []() {
            return std::make_unique<T>();
        };
    }
    
    // Create object by type name
    std::unique_ptr<Document> create(const std::string& typeName) {
        auto it = creators.find(typeName);
        if (it != creators.end()) {
            return it->second();
        }
        throw std::runtime_error("Unknown type: " + typeName);
    }
};

// ========== VARIANT FACTORY (C++17) ==========
#include <variant>
#include <type_traits>

template<typename... Types>
class VariantFactory {
public:
    using VariantType = std::variant<Types...>;
    
    template<typename T>
    static VariantType create() {
        static_assert((std::is_same_v<T, Types> || ...), 
                     "Type not registered in factory");
        return T{};
    }
    
    template<typename T, typename... Args>
    static VariantType createWithArgs(Args&&... args) {
        static_assert((std::is_same_v<T, Types> || ...), 
                     "Type not registered in factory");
        return T{std::forward<Args>(args)...};
    }
};

void factoryExample() {
    std::cout << "=== Factory Pattern Examples ===\n\n";
    
    // 1. Simple Factory
    std::cout << "1. Simple Factory:\n";
    auto pdfDoc = DocumentFactory::create(DocumentType::PDF);
    pdfDoc->open();
    
    // 2. Factory Method
    std::cout << "\n2. Factory Method:\n";
    PdfApplication pdfApp;
    pdfApp.newDocument();
    
    // 3. Abstract Factory
    std::cout << "\n3. Abstract Factory:\n";
    std::unique_ptr<UIFactory> factory = std::make_unique<DarkUIFactory>();
    auto theme = factory->createTheme();
    auto button = factory->createButton();
    
    std::cout << "Theme colors: BG=" << theme->backgroundColor() 
              << ", Text=" << theme->textColor() << "\n";
    button->render();
    
    // 4. Modern Factory with Registry
    std::cout << "\n4. Modern Factory with Registry:\n";
    ModernFactory registry;
    registry.registerType<PdfDocument>("pdf");
    registry.registerType<WordDocument>("doc");
    
    auto doc1 = registry.create("pdf");
    auto doc2 = registry.create("doc");
    doc1->open();
    doc2->open();
    
    // 5. Variant Factory (C++17)
    std::cout << "\n5. Variant Factory (C++17):\n";
    using DocumentVariant = std::variant<PdfDocument, WordDocument>;
    
    auto createDocument = [](const std::string& type) -> DocumentVariant {
        if (type == "pdf") {
            return PdfDocument{};
        } else if (type == "word") {
            return WordDocument{};
        }
        throw std::runtime_error("Unknown type");
    };
    
    auto docVariant = createDocument("pdf");
    std::visit([](auto&& doc) {
        doc.open();
    }, docVariant);
}

#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <sstream>

// ========== FLUENT BUILDER ==========
class Pizza {
private:
    std::string size;
    std::vector<std::string> toppings;
    std::string crust;
    bool extraCheese;
    
    // Private constructor - use Builder
    Pizza() : extraCheese(false) {}
    
public:
    // Modern C++: Make it movable
    Pizza(Pizza&&) = default;
    Pizza& operator=(Pizza&&) = default;
    
    // Delete copy operations (or implement properly)
    Pizza(const Pizza&) = delete;
    Pizza& operator=(const Pizza&) = delete;
    
    void display() const {
        std::cout << "Pizza Details:\n";
        std::cout << "  Size: " << size << "\n";
        std::cout << "  Crust: " << crust << "\n";
        std::cout << "  Extra Cheese: " << (extraCheese ? "Yes" : "No") << "\n";
        std::cout << "  Toppings (" << toppings.size() << "): ";
        for (const auto& t : toppings) {
            std::cout << t << " ";
        }
        std::cout << "\n";
    }
    
    // Builder as friend
    friend class PizzaBuilder;
    friend class PizzaDirector;
};

class PizzaBuilder {
protected:
    std::unique_ptr<Pizza> pizza;
    
public:
    PizzaBuilder() : pizza(std::make_unique<Pizza>()) {}
    
    virtual ~PizzaBuilder() = default;
    
    // Fluent interface
    PizzaBuilder& setSize(const std::string& size) {
        pizza->size = size;
        return *this;
    }
    
    PizzaBuilder& addTopping(const std::string& topping) {
        pizza->toppings.push_back(topping);
        return *this;
    }
    
    PizzaBuilder& setCrust(const std::string& crust) {
        pizza->crust = crust;
        return *this;
    }
    
    PizzaBuilder& addExtraCheese() {
        pizza->extraCheese = true;
        return *this;
    }
    
    // Build method with move semantics
    std::unique_ptr<Pizza> build() {
        return std::move(pizza);
    }
};

// ========== STEP BUILDER ==========
class Computer {
private:
    std::string cpu;
    int ramGB;
    int storageGB;
    std::string gpu;
    bool hasSSD;
    
    Computer() : ramGB(0), storageGB(0), hasSSD(false) {}
    
public:
    void display() const {
        std::cout << "Computer Configuration:\n";
        std::cout << "  CPU: " << cpu << "\n";
        std::cout << "  RAM: " << ramGB << "GB\n";
        std::cout << "  Storage: " << storageGB << "GB "
                  << (hasSSD ? "SSD" : "HDD") << "\n";
        std::cout << "  GPU: " << gpu << "\n";
    }
    
    // Step Builder using inner classes
    class CpuBuilder;
    class RamBuilder;
    class StorageBuilder;
    class FinalBuilder;
    
    friend class CpuBuilder;
    friend class RamBuilder;
    friend class StorageBuilder;
    friend class FinalBuilder;
};

class Computer::CpuBuilder {
private:
    std::unique_ptr<Computer> computer;
    
public:
    CpuBuilder() : computer(std::make_unique<Computer>()) {}
    
    RamBuilder& setCPU(const std::string& cpu) {
        computer->cpu = cpu;
        // Transfer ownership to next builder
        static RamBuilder next(std::move(computer));
        return next;
    }
};

class Computer::RamBuilder {
private:
    std::unique_ptr<Computer> computer;
    
public:
    RamBuilder(std::unique_ptr<Computer> comp) : computer(std::move(comp)) {}
    
    StorageBuilder& setRAM(int ramGB) {
        computer->ramGB = ramGB;
        return StorageBuilder(std::move(computer));
    }
};

class Computer::StorageBuilder {
private:
    std::unique_ptr<Computer> computer;
    
public:
    StorageBuilder(std::unique_ptr<Computer> comp) : computer(std::move(comp)) {}
    
    FinalBuilder& setStorage(int storageGB, bool ssd = true) {
        computer->storageGB = storageGB;
        computer->hasSSD = ssd;
        return FinalBuilder(std::move(computer));
    }
};

class Computer::FinalBuilder {
private:
    std::unique_ptr<Computer> computer;
    
public:
    FinalBuilder(std::unique_ptr<Computer> comp) : computer(std::move(comp)) {}
    
    FinalBuilder& setGPU(const std::string& gpu) {
        computer->gpu = gpu;
        return *this;
    }
    
    std::unique_ptr<Computer> build() {
        return std::move(computer);
    }
};

// ========== DIRECTOR PATTERN with Builder ==========
class PizzaDirector {
public:
    // Pre-defined configurations
    static std::unique_ptr<Pizza> createMargherita(PizzaBuilder& builder) {
        return builder.setSize("Medium")
                      .setCrust("Thin")
                      .addTopping("Tomato")
                      .addTopping("Mozzarella")
                      .addTopping("Basil")
                      .build();
    }
    
    static std::unique_ptr<Pizza> createPepperoni(PizzaBuilder& builder) {
        return builder.setSize("Large")
                      .setCrust("Pan")
                      .addTopping("Tomato")
                      .addTopping("Mozzarella")
                      .addTopping("Pepperoni")
                      .addExtraCheese()
                      .build();
    }
};

// ========== GENERIC BUILDER (Modern C++) ==========
template<typename T>
class GenericBuilder {
private:
    T object;
    
public:
    GenericBuilder() = default;
    
    template<typename... Args>
    GenericBuilder(Args&&... args) : object(std::forward<Args>(args)...) {}
    
    template<typename Member, typename Value>
    GenericBuilder& set(Member T::* member, Value&& value) {
        object.*member = std::forward<Value>(value);
        return *this;
    }
    
    T build() && {  // Rvalue-ref qualified
        return std::move(object);
    }
    
    T& buildRef() & {
        return object;
    }
};

// Example class for GenericBuilder
struct Car {
    std::string make;
    std::string model;
    int year;
    double price;
    
    void display() const {
        std::cout << make << " " << model << " (" << year 
                  << ") - $" << price << "\n";
    }
};

void builderExample() {
    std::cout << "\n=== Builder Pattern Examples ===\n\n";
    
    // 1. Fluent Builder
    std::cout << "1. Fluent Builder:\n";
    PizzaBuilder pizzaBuilder;
    auto customPizza = pizzaBuilder.setSize("Large")
                                   .setCrust("Stuffed")
                                   .addTopping("Pepperoni")
                                   .addTopping("Mushrooms")
                                   .addTopping("Onions")
                                   .addExtraCheese()
                                   .build();
    customPizza->display();
    
    // 2. Step Builder
    std::cout << "\n2. Step Builder:\n";
    auto gamingPC = Computer::CpuBuilder()
                    .setCPU("Intel i9")
                    .setRAM(32)
                    .setStorage(1000, true)
                    .setGPU("RTX 4080")
                    .build();
    gamingPC->display();
    
    // 3. Director with Builder
    std::cout << "\n3. Director with Builder:\n";
    PizzaBuilder builder;
    auto margherita = PizzaDirector::createMargherita(builder);
    margherita->display();
    
    // 4. Generic Builder
    std::cout << "\n4. Generic Builder:\n";
    auto car = GenericBuilder<Car>()
                .set(&Car::make, "Tesla")
                .set(&Car::model, "Model 3")
                .set(&Car::year, 2023)
                .set(&Car::price, 45990.0)
                .build();
    car.display();
}

#include <iostream>
#include <mutex>
#include <memory>
#include <atomic>
#include <string>
#include <unordered_map>

// ========== MEYERS' SINGLETON (Thread-safe in C++11+) ==========
class Logger {
private:
    Logger() {
        std::cout << "Logger instance created\n";
    }
    
    ~Logger() {
        std::cout << "Logger instance destroyed\n";
    }
    
    // Delete copy operations
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;
    
public:
    static Logger& getInstance() {
        // C++11 guarantees thread-safe static initialization
        static Logger instance;
        return instance;
    }
    
    void log(const std::string& message) {
        std::cout << "[LOG] " << message << "\n";
    }
    
    // Modern C++: Enable move operations if needed
    Logger(Logger&&) = delete;
    Logger& operator=(Logger&&) = delete;
};

// ========== DOUBLE-CHECKED LOCKING (Modern C++17) ==========
class Configuration {
private:
    std::unordered_map<std::string, std::string> settings;
    mutable std::mutex mutex;
    
    Configuration() {
        // Load configuration from file
        settings["theme"] = "dark";
        settings["language"] = "en";
        std::cout << "Configuration loaded\n";
    }
    
    ~Configuration() = default;
    
public:
    // Delete copy operations
    Configuration(const Configuration&) = delete;
    Configuration& operator=(const Configuration&) = delete;
    
    static Configuration& getInstance() {
        // C++17: thread-safe with double-checked locking pattern
        static Configuration* instance = nullptr;
        static std::once_flag onceFlag;
        
        std::call_once(onceFlag, []() {
            instance = new Configuration();
        });
        
        return *instance;
    }
    
    std::string getSetting(const std::string& key) const {
        std::lock_guard<std::mutex> lock(mutex);
        auto it = settings.find(key);
        return it != settings.end() ? it->second : "";
    }
    
    void setSetting(const std::string& key, const std::string& value) {
        std::lock_guard<std::mutex> lock(mutex);
        settings[key] = value;
    }
};

// ========== SINGLETON WITH DEPENDENCY INJECTION ==========
class Database {
public:
    virtual ~Database() = default;
    virtual void connect() = 0;
    virtual void disconnect() = 0;
};

class PostgresDatabase : public Database {
public:
    void connect() override {
        std::cout << "Connecting to PostgreSQL\n";
    }
    
    void disconnect() override {
        std::cout << "Disconnecting from PostgreSQL\n";
    }
};

class DatabaseManager {
private:
    static std::unique_ptr<Database> instance;
    static std::once_flag initFlag;
    
public:
    template<typename T, typename... Args>
    static void initialize(Args&&... args) {
        std::call_once(initFlag, [&]() {
            instance = std::make_unique<T>(std::forward<Args>(args)...);
        });
    }
    
    static Database& getInstance() {
        if (!instance) {
            throw std::runtime_error("Database not initialized");
        }
        return *instance;
    }
    
    // For testing: reset the singleton
    static void reset() {
        instance.reset();
        initFlag = std::once_flag();
    }
};

std::unique_ptr<Database> DatabaseManager::instance = nullptr;
std::once_flag DatabaseManager::initFlag;

// ========== MONOSTATE PATTERN (Alternative to Singleton) ==========
class MonostateSettings {
private:
    static std::string theme;
    static std::string language;
    static std::mutex mutex;
    
public:
    std::string getTheme() const {
        std::lock_guard<std::mutex> lock(mutex);
        return theme;
    }
    
    void setTheme(const std::string& newTheme) {
        std::lock_guard<std::mutex> lock(mutex);
        theme = newTheme;
    }
    
    std::string getLanguage() const {
        std::lock_guard<std::mutex> lock(mutex);
        return language;
    }
    
    void setLanguage(const std::string& newLanguage) {
        std::lock_guard<std::mutex> lock(mutex);
        language = newLanguage;
    }
};

// Initialize static members
std::string MonostateSettings::theme = "light";
std::string MonostateSettings::language = "en";
std::mutex MonostateSettings::mutex;

// ========== SINGLETON WITH CRTP (Curiously Recurring Template Pattern) ==========
template<typename Derived>
class Singleton {
protected:
    Singleton() = default;
    ~Singleton() = default;
    
    // Delete copy operations
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
    
public:
    static Derived& getInstance() {
        static Derived instance;
        return instance;
    }
};

class CacheManager : public Singleton<CacheManager> {
private:
    std::unordered_map<std::string, std::string> cache;
    mutable std::mutex mutex;
    
    // Private constructor - only Singleton can create
    CacheManager() {
        std::cout << "CacheManager created\n";
    }
    
    friend class Singleton<CacheManager>;
    
public:
    void put(const std::string& key, const std::string& value) {
        std::lock_guard<std::mutex> lock(mutex);
        cache[key] = value;
    }
    
    std::string get(const std::string& key) const {
        std::lock_guard<std::mutex> lock(mutex);
        auto it = cache.find(key);
        return it != cache.end() ? it->second : "";
    }
    
    size_t size() const {
        std::lock_guard<std::mutex> lock(mutex);
        return cache.size();
    }
};

// ========== SINGLETON REGISTRY (Multiple singletons) ==========
class SingletonRegistry {
private:
    static std::unordered_map<std::string, std::shared_ptr<void>> instances;
    static std::mutex mutex;
    
    template<typename T>
    static std::shared_ptr<T> createInstance() {
        return std::make_shared<T>();
    }
    
public:
    template<typename T>
    static std::shared_ptr<T> getInstance(const std::string& key) {
        std::lock_guard<std::mutex> lock(mutex);
        
        auto it = instances.find(key);
        if (it == instances.end()) {
            auto instance = createInstance<T>();
            instances[key] = instance;
            return instance;
        }
        
        return std::static_pointer_cast<T>(it->second);
    }
    
    static void clear() {
        std::lock_guard<std::mutex> lock(mutex);
        instances.clear();
    }
};

std::unordered_map<std::string, std::shared_ptr<void>> SingletonRegistry::instances;
std::mutex SingletonRegistry::mutex;

void singletonExample() {
    std::cout << "\n=== Singleton Pattern Examples ===\n\n";
    
    // 1. Meyers' Singleton
    std::cout << "1. Meyers' Singleton:\n";
    auto& logger = Logger::getInstance();
    logger.log("Application started");
    
    // Same instance
    auto& sameLogger = Logger::getInstance();
    sameLogger.log("Still the same instance");
    
    // 2. Double-checked locking
    std::cout << "\n2. Double-checked Locking:\n";
    auto& config = Configuration::getInstance();
    std::cout << "Theme: " << config.getSetting("theme") << "\n";
    config.setSetting("theme", "light");
    std::cout << "Updated theme: " << config.getSetting("theme") << "\n";
    
    // 3. Singleton with Dependency Injection
    std::cout << "\n3. Singleton with Dependency Injection:\n";
    DatabaseManager::initialize<PostgresDatabase>();
    auto& db = DatabaseManager::getInstance();
    db.connect();
    
    // 4. Monostate Pattern (Alternative)
    std::cout << "\n4. Monostate Pattern:\n";
    MonostateSettings settings1;
    MonostateSettings settings2;
    
    settings1.setTheme("dark");
    std::cout << "Settings2 theme: " << settings2.getTheme() << "\n";  // Outputs "dark"
    
    // 5. CRTP Singleton
    std::cout << "\n5. CRTP Singleton:\n";
    auto& cache = CacheManager::getInstance();
    cache.put("user:1", "John Doe");
    cache.put("user:2", "Jane Smith");
    std::cout << "Cache size: " << cache.size() << "\n";
    std::cout << "User 1: " << cache.get("user:1") << "\n";
    
    // 6. Singleton Registry
    std::cout << "\n6. Singleton Registry:\n";
    auto instance1 = SingletonRegistry::getInstance<std::string>("config");
    *instance1 = "Configuration data";
    
    auto instance2 = SingletonRegistry::getInstance<std::string>("config");
    std::cout << "Same instance: " << (*instance1 == *instance2) << "\n";
    std::cout << "Config value: " << *instance2 << "\n";
}

#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <functional>
#include <unordered_map>

// ========== CONSTRUCTOR INJECTION ==========
class ILogger {
public:
    virtual ~ILogger() = default;
    virtual void log(const std::string& message) = 0;
};

class ConsoleLogger : public ILogger {
public:
    void log(const std::string& message) override {
        std::cout << "[CONSOLE] " << message << "\n";
    }
};

class FileLogger : public ILogger {
public:
    void log(const std::string& message) override {
        std::cout << "[FILE] " << message << " (saved to file)\n";
    }
};

class UserService {
private:
    std::unique_ptr<ILogger> logger;
    
public:
    // Constructor injection
    explicit UserService(std::unique_ptr<ILogger> logger) 
        : logger(std::move(logger)) {}
    
    void createUser(const std::string& username) {
        logger->log("Creating user: " + username);
        // User creation logic
        logger->log("User created successfully");
    }
};

// ========== SETTER INJECTION ==========
class EmailService {
public:
    virtual ~EmailService() = default;
    virtual void send(const std::string& to, const std::string& subject) = 0;
};

class SmtpEmailService : public EmailService {
public:
    void send(const std::string& to, const std::string& subject) override {
        std::cout << "SMTP: Sending email to " << to 
                  << " with subject: " << subject << "\n";
    }
};

class NewsletterService {
private:
    std::unique_ptr<EmailService> emailService;
    
public:
    // Setter injection
    void setEmailService(std::unique_ptr<EmailService> service) {
        emailService = std::move(service);
    }
    
    void sendNewsletter(const std::vector<std::string>& recipients) {
        if (!emailService) {
            throw std::runtime_error("Email service not set");
        }
        
        for (const auto& recipient : recipients) {
            emailService->send(recipient, "Monthly Newsletter");
        }
    }
};

// ========== INTERFACE INJECTION ==========
class Configurable {
public:
    virtual ~Configurable() = default;
    virtual void configure(const std::string& config) = 0;
};

class DatabaseConfig {
private:
    std::string connectionString;
    
public:
    void setConnectionString(const std::string& connStr) {
        connectionString = connStr;
    }
    
    std::string getConnectionString() const {
        return connectionString;
    }
};

class DatabaseClient : public Configurable {
private:
    std::string connectionString;
    
public:
    void configure(const std::string& config) override {
        connectionString = config;
        std::cout << "Database configured with: " << config << "\n";
    }
    
    void connect() {
        std::cout << "Connecting to database: " << connectionString << "\n";
    }
};

// ========== MODERN C++ DI CONTAINER ==========
class DIContainer {
private:
    struct Creator {
        std::function<std::shared_ptr<void>()> create;
        bool isSingleton;
    };
    
    std::unordered_map<std::string, Creator> creators;
    std::unordered_map<std::string, std::shared_ptr<void>> instances;
    
public:
    // Register type
    template<typename Interface, typename Implementation, typename... Args>
    void registerType(const std::string& name, bool singleton = false) {
        creators[name] = {
            [this, singleton]() -> std::shared_ptr<void> {
                if (singleton) {
                    auto it = instances.find(name);
                    if (it != instances.end()) {
                        return it->second;
                    }
                    auto instance = std::make_shared<Implementation>();
                    instances[name] = instance;
                    return instance;
                }
                return std::make_shared<Implementation>();
            },
            singleton
        };
    }
    
    // Register with factory function
    template<typename Interface>
    void registerFactory(const std::string& name, 
                        std::function<std::shared_ptr<Interface>()> factory,
                        bool singleton = false) {
        creators[name] = {
            [factory, singleton, this, name]() -> std::shared_ptr<void> {
                if (singleton) {
                    auto it = instances.find(name);
                    if (it != instances.end()) {
                        return it->second;
                    }
                    auto instance = factory();
                    instances[name] = instance;
                    return instance;
                }
                return factory();
            },
            singleton
        };
    }
    
    // Resolve dependency
    template<typename T>
    std::shared_ptr<T> resolve(const std::string& name) {
        auto it = creators.find(name);
        if (it == creators.end()) {
            throw std::runtime_error("Dependency not registered: " + name);
        }
        
        auto instance = it->second.create();
        return std::static_pointer_cast<T>(instance);
    }
};

// ========== TEMPLATE-BASED DI ==========
template<typename Logger, typename Database, typename Cache>
class OrderService {
private:
    Logger& logger;
    Database& database;
    Cache& cache;
    
public:
    OrderService(Logger& logger, Database& database, Cache& cache)
        : logger(logger), database(database), cache(cache) {}
    
    void placeOrder(const std::string& orderId) {
        logger.log("Placing order: " + orderId);
        database.save(orderId);
        cache.set(orderId, "processing");
        logger.log("Order placed successfully");
    }
};

// ========== DI WITH VARIADIC TEMPLATES ==========
class DIFactory {
private:
    template<typename T, typename... Dependencies>
    static std::unique_ptr<T> createImpl(Dependencies&&... deps) {
        return std::make_unique<T>(std::forward<Dependencies>(deps)...);
    }
    
public:
    template<typename T, typename... Dependencies>
    static std::unique_ptr<T> create() {
        // Recursively create dependencies
        return createImpl<T>(create<Dependencies>()...);
    }
    
    template<typename T>
    static std::unique_ptr<T> create() {
        return std::make_unique<T>();
    }
};

void dependencyInjectionExample() {
    std::cout << "\n=== Dependency Injection Examples ===\n\n";
    
    // 1. Constructor Injection
    std::cout << "1. Constructor Injection:\n";
    auto logger = std::make_unique<FileLogger>();
    UserService userService(std::move(logger));
    userService.createUser("john_doe");
    
    // 2. Setter Injection
    std::cout << "\n2. Setter Injection:\n";
    NewsletterService newsletterService;
    newsletterService.setEmailService(std::make_unique<SmtpEmailService>());
    
    std::vector<std::string> recipients = {"user1@example.com", "user2@example.com"};
    newsletterService.sendNewsletter(recipients);
    
    // 3. Interface Injection
    std::cout << "\n3. Interface Injection:\n";
    DatabaseClient dbClient;
    dbClient.configure("host=localhost;port=5432;database=mydb");
    dbClient.connect();
    
    // 4. DI Container
    std::cout << "\n4. DI Container:\n";
    DIContainer container;
    
    // Register types
    container.registerType<ILogger, ConsoleLogger>("logger");
    container.registerType<EmailService, SmtpEmailService>("email", true);
    
    // Resolve dependencies
    auto resolvedLogger = container.resolve<ILogger>("logger");
    resolvedLogger->log("This is a test message");
    
    auto emailService1 = container.resolve<EmailService>("email");
    auto emailService2 = container.resolve<EmailService>("email");
    emailService1->send("test@example.com", "Hello");
    
    // Should be same instance (singleton)
    std::cout << "Same instance? " 
              << (emailService1.get() == emailService2.get() ? "Yes" : "No") 
              << "\n";
    
    // 5. Template-based DI
    std::cout << "\n5. Template-based DI:\n";
    ConsoleLogger templateLogger;
    struct MockDatabase {
        void save(const std::string& id) {
            std::cout << "Saving order " << id << " to database\n";
        }
    };
    
    struct MockCache {
        void set(const std::string& key, const std::string& value) {
            std::cout << "Caching " << key << " = " << value << "\n";
        }
    };
    
    MockDatabase mockDb;
    MockCache mockCache;
    
    OrderService<ConsoleLogger, MockDatabase, MockCache> 
        orderService(templateLogger, mockDb, mockCache);
    orderService.placeOrder("ORD12345");
}

#include <iostream>
#include <memory>
#include <string>
#include <cmath>

// ========== OBJECT ADAPTER ==========
// Legacy interface (incompatible)
class LegacyRectangle {
private:
    double x1, y1, x2, y2;
    
public:
    LegacyRectangle(double x1, double y1, double x2, double y2)
        : x1(x1), y1(y1), x2(x2), y2(y2) {}
    
    void oldDraw() const {
        std::cout << "LegacyRectangle: draw() at [(" 
                  << x1 << "," << y1 << "), (" 
                  << x2 << "," << y2 << ")]\n";
    }
    
    double getX1() const { return x1; }
    double getY1() const { return y1; }
    double getX2() const { return x2; }
    double getY2() const { return y2; }
};

// Modern interface
class Shape {
public:
    virtual ~Shape() = default;
    virtual void draw() const = 0;
    virtual void resize(double factor) = 0;
    virtual double area() const = 0;
};

// Object Adapter
class RectangleAdapter : public Shape {
private:
    std::unique_ptr<LegacyRectangle> legacyRect;
    
public:
    RectangleAdapter(double x, double y, double w, double h)
        : legacyRect(std::make_unique<LegacyRectangle>(x, y, x + w, y + h)) {}
    
    void draw() const override {
        legacyRect->oldDraw();
    }
    
    void resize(double factor) override {
        double x1 = legacyRect->getX1();
        double y1 = legacyRect->getY1();
        double x2 = legacyRect->getX2();
        double y2 = legacyRect->getY2();
        
        double centerX = (x1 + x2) / 2;
        double centerY = (y1 + y2) / 2;
        double newWidth = (x2 - x1) * factor;
        double newHeight = (y2 - y1) * factor;
        
        legacyRect = std::make_unique<LegacyRectangle>(
            centerX - newWidth / 2,
            centerY - newHeight / 2,
            centerX + newWidth / 2,
            centerY + newHeight / 2
        );
    }
    
    double area() const override {
        double width = legacyRect->getX2() - legacyRect->getX1();
        double height = legacyRect->getY2() - legacyRect->getY1();
        return width * height;
    }
};

// ========== CLASS ADAPTER (Multiple Inheritance) ==========
class ModernCircle {
public:
    virtual ~ModernCircle() = default;
    virtual void render() = 0;
    virtual void scale(double factor) = 0;
    virtual double getRadius() const = 0;
};

class LegacyCircle {
private:
    double x, y, r;
    
public:
    LegacyCircle(double x, double y, double r) : x(x), y(y), r(r) {}
    
    void display() const {
        std::cout << "LegacyCircle: display() at (" 
                  << x << "," << y << ") radius " << r << "\n";
    }
    
    void setRadius(double radius) { r = radius; }
    double getX() const { return x; }
    double getY() const { return y; }
    double getRadius() const { return r; }
};

// Class Adapter (using multiple inheritance)
class CircleAdapter : public ModernCircle, private LegacyCircle {
public:
    CircleAdapter(double x, double y, double r) : LegacyCircle(x, y, r) {}
    
    void render() override {
        display();  // Adapts LegacyCircle::display to ModernCircle::render
    }
    
    void scale(double factor) override {
        setRadius(getRadius() * factor);
    }
    
    double getRadius() const override {
        return LegacyCircle::getRadius();
    }
    
    // Additional adapter methods
    double area() const {
        return M_PI * getRadius() * getRadius();
    }
};

// ========== ADAPTER FOR FUNCTIONAL INTERFACES ==========
// Legacy C-style function
using LegacyCallback = void(*)(int, const char*);

// Modern C++ interface
class EventHandler {
public:
    virtual ~EventHandler() = default;
    virtual void handleEvent(int id, const std::string& data) = 0;
};

// Function adapter
class CallbackAdapter : public EventHandler {
private:
    LegacyCallback callback;
    
public:
    explicit CallbackAdapter(LegacyCallback cb) : callback(cb) {
        if (!cb) {
            throw std::invalid_argument("Callback cannot be null");
        }
    }
    
    void handleEvent(int id, const std::string& data) override {
        // Adapt modern interface to legacy callback
        callback(id, data.c_str());
    }
};

// ========== GENERIC ADAPTER (Modern C++) ==========
template<typename Legacy, typename Modern>
class GenericAdapter : public Modern {
private:
    std::unique_ptr<Legacy> legacy;
    
    // Conversion functions
    static auto convertToLegacy(const typename Modern::ParamType& param) {
        // This would be specialized for each type
        return param;
    }
    
    static auto convertFromLegacy(const typename Legacy::ResultType& result) {
        return result;
    }
    
public:
    template<typename... Args>
    GenericAdapter(Args&&... args) 
        : legacy(std::make_unique<Legacy>(std::forward<Args>(args)...)) {}
    
    typename Modern::ResultType modernMethod(
        const typename Modern::ParamType& param) override {
        
        auto legacyParam = convertToLegacy(param);
        auto legacyResult = legacy->legacyMethod(legacyParam);
        return convertFromLegacy(legacyResult);
    }
};

// ========== ADAPTER WITH LAMBDA ==========
class ModernAPI {
public:
    using Handler = std::function<void(const std::string&)>;
    
    void setHandler(Handler handler) {
        this->handler = std::move(handler);
    }
    
    void trigger(const std::string& event) {
        if (handler) {
            handler(event);
        }
    }
    
private:
    Handler handler;
};

// Legacy API with C-style callback
using LegacyHandler = void(*)(const char*);

class LegacySystem {
private:
    LegacyHandler handler = nullptr;
    
public:
    void registerHandler(LegacyHandler h) {
        handler = h;
    }
    
    void fireEvent(const char* event) {
        if (handler) {
            handler(event);
        }
    }
};

// Lambda adapter
class LambdaAdapter {
private:
    ModernAPI& modern;
    LegacySystem& legacy;
    
public:
    LambdaAdapter(ModernAPI& modern, LegacySystem& legacy) 
        : modern(modern), legacy(legacy) {
        
        // Adapt modern lambda to legacy callback
        modern.setHandler([this](const std::string& event) {
            std::cout << "Modern handler: " << event << "\n";
            // Forward to legacy system
            legacy.fireEvent(event.c_str());
        });
        
        // Adapt legacy callback to modern lambda
        legacy.registerHandler([](const char* event) {
            std::cout << "Legacy handler: " << event << "\n";
        });
    }
};

void adapterExample() {
    std::cout << "\n=== Adapter Pattern Examples ===\n\n";
    
    // 1. Object Adapter
    std::cout << "1. Object Adapter (Legacy Rectangle to Modern Shape):\n";
    RectangleAdapter rect(10, 10, 50, 30);
    rect.draw();
    std::cout << "Area: " << rect.area() << "\n";
    rect.resize(1.5);
    rect.draw();
    std::cout << "New area: " << rect.area() << "\n";
    
    // 2. Class Adapter
    std::cout << "\n2. Class Adapter (Legacy Circle to Modern Circle):\n";
    CircleAdapter circle(100, 100, 25);
    circle.render();
    std::cout << "Radius: " << circle.getRadius() << "\n";
    circle.scale(2.0);
    circle.render();
    std::cout << "New radius: " << circle.getRadius() << "\n";
    std::cout << "Area: " << circle.area() << "\n";
    
    // 3. Callback Adapter
    std::cout << "\n3. Callback Adapter (C-style to C++):\n";
    auto legacyCallback = [](int id, const char* msg) {
        std::cout << "Legacy callback: id=" << id << ", msg=" << msg << "\n";
    };
    
    CallbackAdapter adapter(legacyCallback);
    adapter.handleEvent(42, "Hello from modern C++");
    
    // 4. Lambda Adapter
    std::cout << "\n4. Lambda Adapter (Bidirectional):\n";
    ModernAPI modernAPI;
    LegacySystem legacySystem;
    LambdaAdapter lambdaAdapter(modernAPI, legacySystem);
    
    // Test both directions
    modernAPI.trigger("Modern event");
    legacySystem.fireEvent("Legacy event");
}

#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <functional>

// ========== BASIC DECORATOR ==========
class Beverage {
public:
    virtual ~Beverage() = default;
    virtual std::string getDescription() const = 0;
    virtual double cost() const = 0;
    
    // Modern C++: clone method for prototype pattern
    virtual std::unique_ptr<Beverage> clone() const = 0;
};

class Espresso : public Beverage {
public:
    std::string getDescription() const override {
        return "Espresso";
    }
    
    double cost() const override {
        return 1.99;
    }
    
    std::unique_ptr<Beverage> clone() const override {
        return std::make_unique<Espresso>(*this);
    }
};

// Decorator base class
class CondimentDecorator : public Beverage {
protected:
    std::unique_ptr<Beverage> beverage;
    
public:
    explicit CondimentDecorator(std::unique_ptr<Beverage> bev)
        : beverage(std::move(bev)) {}
    
    std::string getDescription() const override = 0;
    double cost() const override = 0;
    
    // Forward clone to decorated object
    std::unique_ptr<Beverage> clone() const override {
        auto clonedBeverage = beverage->clone();
        return std::make_unique<std::decay_t<decltype(*this)>>(
            std::move(clonedBeverage));
    }
};

class Milk : public CondimentDecorator {
public:
    explicit Milk(std::unique_ptr<Beverage> bev)
        : CondimentDecorator(std::move(bev)) {}
    
    std::string getDescription() const override {
        return beverage->getDescription() + ", Milk";
    }
    
    double cost() const override {
        return beverage->cost() + 0.20;
    }
};

class Mocha : public CondimentDecorator {
public:
    explicit Mocha(std::unique_ptr<Beverage> bev)
        : CondimentDecorator(std::move(bev)) {}
    
    std::string getDescription() const override {
        return beverage->getDescription() + ", Mocha";
    }
    
    double cost() const override {
        return beverage->cost() + 0.30;
    }
};

class Whip : public CondimentDecorator {
public:
    explicit Whip(std::unique_ptr<Beverage> bev)
        : CondimentDecorator(std::move(bev)) {}
    
    std::string getDescription() const override {
        return beverage->getDescription() + ", Whip";
    }
    
    double cost() const override {
        return beverage->cost() + 0.15;
    }
};

// ========== STREAM DECORATOR ==========
class OutputStream {
public:
    virtual ~OutputStream() = default;
    virtual void write(const std::string& data) = 0;
    virtual void flush() = 0;
};

class FileStream : public OutputStream {
private:
    std::string filename;
    
public:
    explicit FileStream(const std::string& filename) : filename(filename) {
        std::cout << "Opening file: " << filename << "\n";
    }
    
    void write(const std::string& data) override {
        std::cout << "Writing to file: " << data << "\n";
    }
    
    void flush() override {
        std::cout << "Flushing file\n";
    }
};

// Stream Decorator base
class StreamDecorator : public OutputStream {
protected:
    std::unique_ptr<OutputStream> stream;
    
public:
    explicit StreamDecorator(std::unique_ptr<OutputStream> stream)
        : stream(std::move(stream)) {}
    
    void write(const std::string& data) override {
        stream->write(data);
    }
    
    void flush() override {
        stream->flush();
    }
};

class BufferedStream : public StreamDecorator {
private:
    std::string buffer;
    size_t bufferSize;
    
public:
    BufferedStream(std::unique_ptr<OutputStream> stream, size_t size = 1024)
        : StreamDecorator(std::move(stream)), bufferSize(size) {}
    
    void write(const std::string& data) override {
        buffer += data;
        if (buffer.size() >= bufferSize) {
            flush();
        }
    }
    
    void flush() override {
        if (!buffer.empty()) {
            stream->write(buffer);
            buffer.clear();
        }
        StreamDecorator::flush();
    }
};

class CompressedStream : public StreamDecorator {
public:
    explicit CompressedStream(std::unique_ptr<OutputStream> stream)
        : StreamDecorator(std::move(stream)) {}
    
    void write(const std::string& data) override {
        // Simulate compression
        std::string compressed = "COMPRESSED[" + data + "]";
        stream->write(compressed);
    }
};

class EncryptedStream : public StreamDecorator {
private:
    int key;
    
public:
    EncryptedStream(std::unique_ptr<OutputStream> stream, int key = 42)
        : StreamDecorator(std::move(stream)), key(key) {}
    
    void write(const std::string& data) override {
        // Simple XOR encryption
        std::string encrypted = data;
        for (char& c : encrypted) {
            c ^= key;
        }
        stream->write(encrypted);
    }
};

// ========== MODERN C++ DECORATOR WITH MIXINS ==========
template<typename Base>
class Decorator : public Base {
public:
    template<typename... Args>
    Decorator(Args&&... args) : Base(std::forward<Args>(args)...) {}
};

// Mixin decorators
template<typename Base>
class LoggingDecorator : public Base {
public:
    template<typename... Args>
    LoggingDecorator(Args&&... args) : Base(std::forward<Args>(args)...) {}
    
    void operation() {
        std::cout << "Logging: Before operation\n";
        Base::operation();
        std::cout << "Logging: After operation\n";
    }
};

template<typename Base>
class TimingDecorator : public Base {
public:
    template<typename... Args>
    TimingDecorator(Args&&... args) : Base(std::forward<Args>(args)...) {}
    
    void operation() {
        auto start = std::chrono::high_resolution_clock::now();
        Base::operation();
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "Operation took " << duration.count() << " microseconds\n";
    }
};

// Base component
class SimpleService {
public:
    void operation() {
        std::cout << "Performing simple service operation\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
};

// ========== FUNCTION DECORATOR (C++17) ==========
template<typename Func>
class FunctionDecorator {
private:
    Func func;
    
public:
    explicit FunctionDecorator(Func f) : func(std::move(f)) {}
    
    template<typename... Args>
    auto operator()(Args&&... args) {
        std::cout << "Before function call\n";
        auto result = func(std::forward<Args>(args)...);
        std::cout << "After function call\n";
        return result;
    }
};

// Helper function to create decorators
template<typename Func>
auto makeDecorator(Func f) {
    return FunctionDecorator<Func>(std::move(f));
}

// ========== DECORATOR WITH LAMBDA ==========
class LambdaDecorator {
public:
    using Handler = std::function<void()>;
    
    static Handler addLogging(Handler handler) {
        return [handler]() {
            std::cout << "Logging: Starting\n";
            handler();
            std::cout << "Logging: Finished\n";
        };
    }
    
    static Handler addTiming(Handler handler) {
        return [handler]() {
            auto start = std::chrono::high_resolution_clock::now();
            handler();
            auto end = std::chrono::high_resolution_clock::now();
            auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
            std::cout << "Execution time: " << duration.count() << "ms\n";
        };
    }
};

void decoratorExample() {
    std::cout << "\n=== Decorator Pattern Examples ===\n\n";
    
    // 1. Beverage Decorator
    std::cout << "1. Beverage Decorator:\n";
    auto beverage = std::make_unique<Espresso>();
    std::cout << beverage->getDescription() 
              << " $" << beverage->cost() << "\n";
    
    // Add decorators
    beverage = std::make_unique<Milk>(std::move(beverage));
    beverage = std::make_unique<Mocha>(std::move(beverage));
    beverage = std::make_unique<Whip>(std::move(beverage));
    
    std::cout << beverage->getDescription() 
              << " $" << beverage->cost() << "\n";
    
    // Clone decorated beverage
    auto clonedBeverage = beverage->clone();
    std::cout << "Cloned: " << clonedBeverage->getDescription() 
              << " $" << clonedBeverage->cost() << "\n";
    
    // 2. Stream Decorator
    std::cout << "\n2. Stream Decorator:\n";
    auto stream = std::make_unique<FileStream>("data.txt");
    stream = std::make_unique<BufferedStream>(std::move(stream), 512);
    stream = std::make_unique<CompressedStream>(std::move(stream));
    stream = std::make_unique<EncryptedStream>(std::move(stream), 123);
    
    stream->write("Hello, Decorator Pattern!");
    stream->flush();
    
    // 3. Mixin Decorator
    std::cout << "\n3. Mixin Decorator:\n";
    using LoggedTimedService = LoggingDecorator<TimingDecorator<SimpleService>>;
    LoggedTimedService service;
    service.operation();
    
    // 4. Function Decorator
    std::cout << "\n4. Function Decorator:\n";
    auto add = [](int a, int b) {
        std::cout << "Adding " << a << " + " << b << "\n";
        return a + b;
    };
    
    auto decoratedAdd = makeDecorator(add);
    int result = decoratedAdd(10, 20);
    std::cout << "Result: " << result << "\n";
    
    // 5. Lambda Decorator
    std::cout << "\n5. Lambda Decorator:\n";
    auto task = []() {
        std::cout << "Doing some work...\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    };
    
    auto decoratedTask = LambdaDecorator::addLogging(
        LambdaDecorator::addTiming(task)
    );
    decoratedTask();
}

#include <iostream>
#include <memory>
#include <string>
#include <vector>

// ========== COMPLEX SUBSYSTEMS ==========
class CPU {
public:
    void freeze() {
        std::cout << "CPU: Freezing processor\n";
    }
    
    void jump(long position) {
        std::cout << "CPU: Jumping to position " << position << "\n";
    }
    
    void execute() {
        std::cout << "CPU: Executing instructions\n";
    }
    
    void reset() {
        std::cout << "CPU: Resetting\n";
    }
};

class Memory {
private:
    std::vector<char> ram;
    
public:
    Memory() : ram(1024 * 1024) {}  // 1MB RAM
    
    void load(long position, const std::vector<char>& data) {
        std::cout << "Memory: Loading " << data.size() 
                  << " bytes at position " << position << "\n";
        std::copy(data.begin(), data.end(), ram.begin() + position);
    }
    
    char read(long position) const {
        return ram[position];
    }
};

class HardDrive {
public:
    std::vector<char> read(long lba, int size) {
        std::cout << "HardDrive: Reading " << size 
                  << " bytes from LBA " << lba << "\n";
        // Simulate reading data
        return std::vector<char>(size, 0xFF);
    }
    
    void write(long lba, const std::vector<char>& data) {
        std::cout << "HardDrive: Writing " << data.size() 
                  << " bytes to LBA " << lba << "\n";
    }
};

class GraphicsCard {
public:
    void initialize() {
        std::cout << "GraphicsCard: Initializing\n";
    }
    
    void setMode(int width, int height) {
        std::cout << "GraphicsCard: Setting mode to " 
                  << width << "x" << height << "\n";
    }
    
    void render(const std::string& frame) {
        std::cout << "GraphicsCard: Rendering frame: " << frame << "\n";
    }
};

class AudioCard {
public:
    void initialize() {
        std::cout << "AudioCard: Initializing\n";
    }
    
    void play(const std::string& sound) {
        std::cout << "AudioCard: Playing sound: " << sound << "\n";
    }
};

// ========== COMPUTER FACADE ==========
class ComputerFacade {
private:
    CPU cpu;
    Memory memory;
    HardDrive hardDrive;
    GraphicsCard graphicsCard;
    AudioCard audioCard;
    
    const long BOOT_ADDRESS = 0x7C00;
    const long BOOT_SECTOR = 0;
    const int SECTOR_SIZE = 512;
    
public:
    void start() {
        std::cout << "\n=== Starting Computer ===\n";
        
        // Power-on self-test (POST)
        cpu.freeze();
        
        // Load BIOS
        auto bios = hardDrive.read(BOOT_SECTOR, SECTOR_SIZE);
        memory.load(BOOT_ADDRESS, bios);
        
        // Initialize hardware
        graphicsCard.initialize();
        audioCard.initialize();
        
        // Jump to BIOS
        cpu.jump(BOOT_ADDRESS);
        cpu.execute();
        
        std::cout << "Computer started successfully!\n";
    }
    
    void shutdown() {
        std::cout << "\n=== Shutting Down Computer ===\n";
        cpu.reset();
        std::cout << "Computer shut down\n";
    }
    
    void playGame(const std::string& gameName) {
        std::cout << "\n=== Playing Game: " << gameName << " ===\n";
        
        // Set graphics mode
        graphicsCard.setMode(1920, 1080);
        
        // Load game assets
        auto gameData = hardDrive.read(1000, 1024 * 1024);  // 1MB game data
        memory.load(0x100000, gameData);  // Load at 1MB offset
        
        // Play game
        for (int i = 0; i < 3; ++i) {
            std::string frame = "Frame " + std::to_string(i) + " of " + gameName;
            graphicsCard.render(frame);
            audioCard.play("Game sound effect");
        }
        
        std::cout << "Game finished\n";
    }
    
    void browseWeb(const std::string& url) {
        std::cout << "\n=== Browsing Web: " << url << " ===\n";
        
        // Set graphics mode for browser
        graphicsCard.setMode(1366, 768);
        
        // Load web page
        auto webData = hardDrive.read(5000, 500 * 1024);  // 500KB web page
        memory.load(0x200000, webData);  // Load at 2MB offset
        
        // Render page
        graphicsCard.render("Web page: " + url);
        audioCard.play("Page load sound");
        
        std::cout << "Web browsing complete\n";
    }
};

// ========== HOME AUTOMATION FACADE ==========
class Light {
private:
    std::string location;
    bool isOn;
    
public:
    explicit Light(const std::string& loc) : location(loc), isOn(false) {}
    
    void on() {
        isOn = true;
        std::cout << location << " light is ON\n";
    }
    
    void off() {
        isOn = false;
        std::cout << location << " light is OFF\n";
    }
    
    bool status() const {
        return isOn;
    }
};

class Thermostat {
private:
    int temperature;
    
public:
    Thermostat() : temperature(22) {}  // Default 22°C
    
    void setTemperature(int temp) {
        temperature = temp;
        std::cout << "Thermostat set to " << temp << "°C\n";
    }
    
    int getTemperature() const {
        return temperature;
    }
};

class SecuritySystem {
public:
    void arm() {
        std::cout << "Security system ARMED\n";
    }
    
    void disarm() {
        std::cout << "Security system DISARMED\n";
    }
    
    void monitor() {
        std::cout << "Security system monitoring...\n";
    }
};

class EntertainmentSystem {
private:
    bool isOn;
    int volume;
    
public:
    EntertainmentSystem() : isOn(false), volume(50) {}
    
    void on() {
        isOn = true;
        std::cout << "Entertainment system ON\n";
    }
    
    void off() {
        isOn = false;
        std::cout << "Entertainment system OFF\n";
    }
    
    void setVolume(int level) {
        volume = level;
        std::cout << "Volume set to " << level << "\n";
    }
    
    void playMovie(const std::string& title) {
        if (isOn) {
            std::cout << "Playing movie: " << title << "\n";
        }
    }
};

class HomeAutomationFacade {
private:
    Light livingRoomLight;
    Light kitchenLight;
    Light bedroomLight;
    Thermostat thermostat;
    SecuritySystem security;
    EntertainmentSystem entertainment;
    
public:
    HomeAutomationFacade() 
        : livingRoomLight("Living Room"),
          kitchenLight("Kitchen"),
          bedroomLight("Bedroom") {}
    
    // Common scenarios
    void arriveHome() {
        std::cout << "\n=== Arriving Home ===\n";
        security.disarm();
        livingRoomLight.on();
        thermostat.setTemperature(21);
        entertainment.on();
        entertainment.setVolume(30);
        entertainment.playMovie("Welcome home movie");
    }
    
    void leaveHome() {
        std::cout << "\n=== Leaving Home ===\n";
        livingRoomLight.off();
        kitchenLight.off();
        bedroomLight.off();
        thermostat.setTemperature(18);  // Energy saving
        security.arm();
        entertainment.off();
    }
    
    void movieNight() {
        std::cout << "\n=== Movie Night ===\n";
        livingRoomLight.off();
        thermostat.setTemperature(20);
        entertainment.on();
        entertainment.setVolume(60);
        entertainment.playMovie("New Blockbuster");
    }
    
    void sleepMode() {
        std::cout << "\n=== Sleep Mode ===\n";
        livingRoomLight.off();
        kitchenLight.off();
        bedroomLight.on();
        thermostat.setTemperature(19);
        security.arm();
        entertainment.off();
    }
    
    void morningWakeup() {
        std::cout << "\n=== Morning Wakeup ===\n";
        bedroomLight.on();
        livingRoomLight.on();
        thermostat.setTemperature(22);
        security.disarm();
        entertainment.on();
        entertainment.setVolume(20);
    }
};

// ========== API GATEWAY FACADE (Modern Microservices) ==========
class UserService {
public:
    std::string getUserInfo(int userId) {
        return "User " + std::to_string(userId) + " info";
    }
};

class OrderService {
public:
    std::string getOrderInfo(int orderId) {
        return "Order " + std::to_string(orderId) + " details";
    }
};

class PaymentService {
public:
    std::string processPayment(int userId, double amount) {
        return "Processed payment of $" + std::to_string(amount) 
               + " for user " + std::to_string(userId);
    }
};

class InventoryService {
public:
    std::string checkStock(int productId) {
        return "Stock for product " + std::to_string(productId) + ": 100 units";
    }
};

class ApiGatewayFacade {
private:
    UserService userService;
    OrderService orderService;
    PaymentService paymentService;
    InventoryService inventoryService;
    
public:
    // Unified API endpoints
    std::string getUserDashboard(int userId) {
        std::cout << "\n=== User Dashboard for ID: " << userId << " ===\n";
        
        std::string dashboard;
        dashboard += userService.getUserInfo(userId) + "\n";
        dashboard += "Recent orders:\n";
        dashboard += orderService.getOrderInfo(1001) + "\n";
        dashboard += orderService.getOrderInfo(1002) + "\n";
        dashboard += "Payment status: " + paymentService.processPayment(userId, 99.99) + "\n";
        
        return dashboard;
    }
    
    std::string getProductDetails(int productId) {
        std::cout << "\n=== Product Details for ID: " << productId << " ===\n";
        
        std::string details;
        details += "Product ID: " + std::to_string(productId) + "\n";
        details += inventoryService.checkStock(productId) + "\n";
        details += "Price: $49.99\n";
        details += "Rating: 4.5/5\n";
        
        return details;
    }
    
    std::string checkout(int userId, int productId, int quantity) {
        std::cout << "\n=== Checkout Process ===\n";
        
        std::string receipt;
        receipt += "Checkout Receipt\n";
        receipt += "================\n";
        receipt += "User: " + userService.getUserInfo(userId) + "\n";
        receipt += "Product: " + inventoryService.checkStock(productId) + "\n";
        receipt += "Quantity: " + std::to_string(quantity) + "\n";
        receipt += "Total: $" + std::to_string(quantity * 49.99) + "\n";
        receipt += paymentService.processPayment(userId, quantity * 49.99) + "\n";
        receipt += "Order confirmed: " + orderService.getOrderInfo(1003) + "\n";
        
        return receipt;
    }
};

void facadeExample() {
    std::cout << "\n=== Facade Pattern Examples ===\n\n";
    
    // 1. Computer Facade
    std::cout << "1. Computer Facade:\n";
    ComputerFacade computer;
    computer.start();
    computer.playGame("Awesome Game");
    computer.browseWeb("https://example.com");
    computer.shutdown();
    
    // 2. Home Automation Facade
    std::cout << "\n2. Home Automation Facade:\n";
    HomeAutomationFacade home;
    home.arriveHome();
    home.movieNight();
    home.sleepMode();
    home.morningWakeup();
    home.leaveHome();
    
    // 3. API Gateway Facade
    std::cout << "\n3. API Gateway Facade (Microservices):\n";
    ApiGatewayFacade apiGateway;
    
    std::cout << apiGateway.getUserDashboard(123) << "\n";
    std::cout << apiGateway.getProductDetails(456) << "\n";
    std::cout << apiGateway.checkout(123, 456, 2) << "\n";
}

#include <iostream>
#include <memory>
#include <string>
#include <vector>

// ========== COMPLEX SUBSYSTEMS ==========
class CPU {
public:
    void freeze() {
        std::cout << "CPU: Freezing processor\n";
    }
    
    void jump(long position) {
        std::cout << "CPU: Jumping to position " << position << "\n";
    }
    
    void execute() {
        std::cout << "CPU: Executing instructions\n";
    }
    
    void reset() {
        std::cout << "CPU: Resetting\n";
    }
};

class Memory {
private:
    std::vector<char> ram;
    
public:
    Memory() : ram(1024 * 1024) {}  // 1MB RAM
    
    void load(long position, const std::vector<char>& data) {
        std::cout << "Memory: Loading " << data.size() 
                  << " bytes at position " << position << "\n";
        std::copy(data.begin(), data.end(), ram.begin() + position);
    }
    
    char read(long position) const {
        return ram[position];
    }
};

class HardDrive {
public:
    std::vector<char> read(long lba, int size) {
        std::cout << "HardDrive: Reading " << size 
                  << " bytes from LBA " << lba << "\n";
        // Simulate reading data
        return std::vector<char>(size, 0xFF);
    }
    
    void write(long lba, const std::vector<char>& data) {
        std::cout << "HardDrive: Writing " << data.size() 
                  << " bytes to LBA " << lba << "\n";
    }
};

class GraphicsCard {
public:
    void initialize() {
        std::cout << "GraphicsCard: Initializing\n";
    }
    
    void setMode(int width, int height) {
        std::cout << "GraphicsCard: Setting mode to " 
                  << width << "x" << height << "\n";
    }
    
    void render(const std::string& frame) {
        std::cout << "GraphicsCard: Rendering frame: " << frame << "\n";
    }
};

class AudioCard {
public:
    void initialize() {
        std::cout << "AudioCard: Initializing\n";
    }
    
    void play(const std::string& sound) {
        std::cout << "AudioCard: Playing sound: " << sound << "\n";
    }
};

// ========== COMPUTER FACADE ==========
class ComputerFacade {
private:
    CPU cpu;
    Memory memory;
    HardDrive hardDrive;
    GraphicsCard graphicsCard;
    AudioCard audioCard;
    
    const long BOOT_ADDRESS = 0x7C00;
    const long BOOT_SECTOR = 0;
    const int SECTOR_SIZE = 512;
    
public:
    void start() {
        std::cout << "\n=== Starting Computer ===\n";
        
        // Power-on self-test (POST)
        cpu.freeze();
        
        // Load BIOS
        auto bios = hardDrive.read(BOOT_SECTOR, SECTOR_SIZE);
        memory.load(BOOT_ADDRESS, bios);
        
        // Initialize hardware
        graphicsCard.initialize();
        audioCard.initialize();
        
        // Jump to BIOS
        cpu.jump(BOOT_ADDRESS);
        cpu.execute();
        
        std::cout << "Computer started successfully!\n";
    }
    
    void shutdown() {
        std::cout << "\n=== Shutting Down Computer ===\n";
        cpu.reset();
        std::cout << "Computer shut down\n";
    }
    
    void playGame(const std::string& gameName) {
        std::cout << "\n=== Playing Game: " << gameName << " ===\n";
        
        // Set graphics mode
        graphicsCard.setMode(1920, 1080);
        
        // Load game assets
        auto gameData = hardDrive.read(1000, 1024 * 1024);  // 1MB game data
        memory.load(0x100000, gameData);  // Load at 1MB offset
        
        // Play game
        for (int i = 0; i < 3; ++i) {
            std::string frame = "Frame " + std::to_string(i) + " of " + gameName;
            graphicsCard.render(frame);
            audioCard.play("Game sound effect");
        }
        
        std::cout << "Game finished\n";
    }
    
    void browseWeb(const std::string& url) {
        std::cout << "\n=== Browsing Web: " << url << " ===\n";
        
        // Set graphics mode for browser
        graphicsCard.setMode(1366, 768);
        
        // Load web page
        auto webData = hardDrive.read(5000, 500 * 1024);  // 500KB web page
        memory.load(0x200000, webData);  // Load at 2MB offset
        
        // Render page
        graphicsCard.render("Web page: " + url);
        audioCard.play("Page load sound");
        
        std::cout << "Web browsing complete\n";
    }
};

// ========== HOME AUTOMATION FACADE ==========
class Light {
private:
    std::string location;
    bool isOn;
    
public:
    explicit Light(const std::string& loc) : location(loc), isOn(false) {}
    
    void on() {
        isOn = true;
        std::cout << location << " light is ON\n";
    }
    
    void off() {
        isOn = false;
        std::cout << location << " light is OFF\n";
    }
    
    bool status() const {
        return isOn;
    }
};

class Thermostat {
private:
    int temperature;
    
public:
    Thermostat() : temperature(22) {}  // Default 22°C
    
    void setTemperature(int temp) {
        temperature = temp;
        std::cout << "Thermostat set to " << temp << "°C\n";
    }
    
    int getTemperature() const {
        return temperature;
    }
};

class SecuritySystem {
public:
    void arm() {
        std::cout << "Security system ARMED\n";
    }
    
    void disarm() {
        std::cout << "Security system DISARMED\n";
    }
    
    void monitor() {
        std::cout << "Security system monitoring...\n";
    }
};

class EntertainmentSystem {
private:
    bool isOn;
    int volume;
    
public:
    EntertainmentSystem() : isOn(false), volume(50) {}
    
    void on() {
        isOn = true;
        std::cout << "Entertainment system ON\n";
    }
    
    void off() {
        isOn = false;
        std::cout << "Entertainment system OFF\n";
    }
    
    void setVolume(int level) {
        volume = level;
        std::cout << "Volume set to " << level << "\n";
    }
    
    void playMovie(const std::string& title) {
        if (isOn) {
            std::cout << "Playing movie: " << title << "\n";
        }
    }
};

class HomeAutomationFacade {
private:
    Light livingRoomLight;
    Light kitchenLight;
    Light bedroomLight;
    Thermostat thermostat;
    SecuritySystem security;
    EntertainmentSystem entertainment;
    
public:
    HomeAutomationFacade() 
        : livingRoomLight("Living Room"),
          kitchenLight("Kitchen"),
          bedroomLight("Bedroom") {}
    
    // Common scenarios
    void arriveHome() {
        std::cout << "\n=== Arriving Home ===\n";
        security.disarm();
        livingRoomLight.on();
        thermostat.setTemperature(21);
        entertainment.on();
        entertainment.setVolume(30);
        entertainment.playMovie("Welcome home movie");
    }
    
    void leaveHome() {
        std::cout << "\n=== Leaving Home ===\n";
        livingRoomLight.off();
        kitchenLight.off();
        bedroomLight.off();
        thermostat.setTemperature(18);  // Energy saving
        security.arm();
        entertainment.off();
    }
    
    void movieNight() {
        std::cout << "\n=== Movie Night ===\n";
        livingRoomLight.off();
        thermostat.setTemperature(20);
        entertainment.on();
        entertainment.setVolume(60);
        entertainment.playMovie("New Blockbuster");
    }
    
    void sleepMode() {
        std::cout << "\n=== Sleep Mode ===\n";
        livingRoomLight.off();
        kitchenLight.off();
        bedroomLight.on();
        thermostat.setTemperature(19);
        security.arm();
        entertainment.off();
    }
    
    void morningWakeup() {
        std::cout << "\n=== Morning Wakeup ===\n";
        bedroomLight.on();
        livingRoomLight.on();
        thermostat.setTemperature(22);
        security.disarm();
        entertainment.on();
        entertainment.setVolume(20);
    }
};

// ========== API GATEWAY FACADE (Modern Microservices) ==========
class UserService {
public:
    std::string getUserInfo(int userId) {
        return "User " + std::to_string(userId) + " info";
    }
};

class OrderService {
public:
    std::string getOrderInfo(int orderId) {
        return "Order " + std::to_string(orderId) + " details";
    }
};

class PaymentService {
public:
    std::string processPayment(int userId, double amount) {
        return "Processed payment of $" + std::to_string(amount) 
               + " for user " + std::to_string(userId);
    }
};

class InventoryService {
public:
    std::string checkStock(int productId) {
        return "Stock for product " + std::to_string(productId) + ": 100 units";
    }
};

class ApiGatewayFacade {
private:
    UserService userService;
    OrderService orderService;
    PaymentService paymentService;
    InventoryService inventoryService;
    
public:
    // Unified API endpoints
    std::string getUserDashboard(int userId) {
        std::cout << "\n=== User Dashboard for ID: " << userId << " ===\n";
        
        std::string dashboard;
        dashboard += userService.getUserInfo(userId) + "\n";
        dashboard += "Recent orders:\n";
        dashboard += orderService.getOrderInfo(1001) + "\n";
        dashboard += orderService.getOrderInfo(1002) + "\n";
        dashboard += "Payment status: " + paymentService.processPayment(userId, 99.99) + "\n";
        
        return dashboard;
    }
    
    std::string getProductDetails(int productId) {
        std::cout << "\n=== Product Details for ID: " << productId << " ===\n";
        
        std::string details;
        details += "Product ID: " + std::to_string(productId) + "\n";
        details += inventoryService.checkStock(productId) + "\n";
        details += "Price: $49.99\n";
        details += "Rating: 4.5/5\n";
        
        return details;
    }
    
    std::string checkout(int userId, int productId, int quantity) {
        std::cout << "\n=== Checkout Process ===\n";
        
        std::string receipt;
        receipt += "Checkout Receipt\n";
        receipt += "================\n";
        receipt += "User: " + userService.getUserInfo(userId) + "\n";
        receipt += "Product: " + inventoryService.checkStock(productId) + "\n";
        receipt += "Quantity: " + std::to_string(quantity) + "\n";
        receipt += "Total: $" + std::to_string(quantity * 49.99) + "\n";
        receipt += paymentService.processPayment(userId, quantity * 49.99) + "\n";
        receipt += "Order confirmed: " + orderService.getOrderInfo(1003) + "\n";
        
        return receipt;
    }
};

void facadeExample() {
    std::cout << "\n=== Facade Pattern Examples ===\n\n";
    
    // 1. Computer Facade
    std::cout << "1. Computer Facade:\n";
    ComputerFacade computer;
    computer.start();
    computer.playGame("Awesome Game");
    computer.browseWeb("https://example.com");
    computer.shutdown();
    
    // 2. Home Automation Facade
    std::cout << "\n2. Home Automation Facade:\n";
    HomeAutomationFacade home;
    home.arriveHome();
    home.movieNight();
    home.sleepMode();
    home.morningWakeup();
    home.leaveHome();
    
    // 3. API Gateway Facade
    std::cout << "\n3. API Gateway Facade (Microservices):\n";
    ApiGatewayFacade apiGateway;
    
    std::cout << apiGateway.getUserDashboard(123) << "\n";
    std::cout << apiGateway.getProductDetails(456) << "\n";
    std::cout << apiGateway.checkout(123, 456, 2) << "\n";
}


#include <iostream>
#include <memory>
#include <string>
#include <unordered_map>
#include <chrono>
#include <thread>
#include <mutex>

// ========== VIRTUAL PROXY (Lazy Initialization) ==========
class Image {
public:
    virtual ~Image() = default;
    virtual void display() = 0;
    virtual int getWidth() const = 0;
    virtual int getHeight() const = 0;
};

class RealImage : public Image {
private:
    std::string filename;
    int width;
    int height;
    
    void loadFromDisk() {
        std::cout << "Loading image from disk: " << filename << "\n";
        // Simulate expensive loading
        std::this_thread::sleep_for(std::chrono::seconds(1));
        
        // Simulate reading image dimensions
        width = 1920;
        height = 1080;
        std::cout << "Image loaded: " << width << "x" << height << "\n";
    }
    
public:
    explicit RealImage(const std::string& filename) 
        : filename(filename), width(0), height(0) {
        loadFromDisk();
    }
    
    void display() override {
        std::cout << "Displaying image: " << filename 
                  << " (" << width << "x" << height << ")\n";
    }
    
    int getWidth() const override {
        return width;
    }
    
    int getHeight() const override {
        return height;
    }
};

class ImageProxy : public Image {
private:
    std::string filename;
    mutable std::unique_ptr<RealImage> realImage;
    mutable std::once_flag loadFlag;
    
    void ensureLoaded() const {
        std::call_once(loadFlag, [this]() {
            realImage = std::make_unique<RealImage>(filename);
        });
    }
    
public:
    explicit ImageProxy(const std::string& filename) : filename(filename) {}
    
    void display() override {
        ensureLoaded();
        realImage->display();
    }
    
    int getWidth() const override {
        ensureLoaded();
        return realImage->getWidth();
    }
    
    int getHeight() const override {
        ensureLoaded();
        return realImage->getHeight();
    }
    
    // Additional proxy functionality
    std::string getFilename() const {
        return filename;
    }
    
    bool isLoaded() const {
        return realImage != nullptr;
    }
};

// ========== PROTECTION PROXY ==========
class Document {
public:
    virtual ~Document() = default;
    virtual void view() = 0;
    virtual void edit() = 0;
    virtual void save() = 0;
};

class RealDocument : public Document {
private:
    std::string content;
    std::string filename;
    
public:
    RealDocument(const std::string& filename) : filename(filename) {
        // Load document content
        content = "Initial content for " + filename;
    }
    
    void view() override {
        std::cout << "Viewing document: " << filename << "\n";
        std::cout << "Content: " << content << "\n";
    }
    
    void edit() override {
        std::cout << "Editing document: " << filename << "\n";
        content += " [edited]";
    }
    
    void save() override {
        std::cout << "Saving document: " << filename << "\n";
        // Save to disk
    }
    
    std::string getContent() const {
        return content;
    }
};

class User {
private:
    std::string username;
    std::vector<std::string> permissions;
    
public:
    User(const std::string& name, const std::vector<std::string>& perms)
        : username(name), permissions(perms) {}
    
    bool hasPermission(const std::string& perm) const {
        return std::find(permissions.begin(), permissions.end(), perm) 
               != permissions.end();
    }
    
    std::string getName() const {
        return username;
    }
};

class ProtectedDocument : public Document {
private:
    std::unique_ptr<RealDocument> realDocument;
    User* user;
    
public:
    ProtectedDocument(const std::string& filename, User* user)
        : realDocument(std::make_unique<RealDocument>(filename)), user(user) {}
    
    void view() override {
        if (user->hasPermission("view")) {
            realDocument->view();
        } else {
            std::cout << "Access denied: User " << user->getName() 
                      << " cannot view this document\n";
        }
    }
    
    void edit() override {
        if (user->hasPermission("edit")) {
            realDocument->edit();
        } else {
            std::cout << "Access denied: User " << user->getName() 
                      << " cannot edit this document\n";
        }
    }
    
    void save() override {
        if (user->hasPermission("save")) {
            realDocument->save();
        } else {
            std::cout << "Access denied: User " << user->getName() 
                      << " cannot save this document\n";
        }
    }
};

// ========== SMART POINTER PROXY (Modern C++) ==========
template<typename T>
class SmartPointerProxy {
private:
    T* ptr;
    std::function<void(T*)> deleter;
    
public:
    explicit SmartPointerProxy(T* p = nullptr, 
                               std::function<void(T*)> d = [](T* p) { delete p; })
        : ptr(p), deleter(std::move(d)) {}
    
    ~SmartPointerProxy() {
        deleter(ptr);
    }
    
    // Delete copy operations
    SmartPointerProxy(const SmartPointerProxy&) = delete;
    SmartPointerProxy& operator=(const SmartPointerProxy&) = delete;
    
    // Move operations
    SmartPointerProxy(SmartPointerProxy&& other) noexcept 
        : ptr(other.ptr), deleter(std::move(other.deleter)) {
        other.ptr = nullptr;
    }
    
    SmartPointerProxy& operator=(SmartPointerProxy&& other) noexcept {
        if (this != &other) {
            deleter(ptr);
            ptr = other.ptr;
            deleter = std::move(other.deleter);
            other.ptr = nullptr;
        }
        return *this;
    }
    
    // Proxy behavior
    T* operator->() {
        // Additional logic before access
        std::cout << "Accessing pointer with custom deleter\n";
        return ptr;
    }
    
    T& operator*() {
        std::cout << "Dereferencing pointer\n";
        return *ptr;
    }
    
    explicit operator bool() const {
        return ptr != nullptr;
    }
    
    // Additional proxy methods
    void reset(T* p = nullptr) {
        deleter(ptr);
        ptr = p;
    }
    
    T* get() const {
        return ptr;
    }
};

// ========== CACHE PROXY ==========
class ExpensiveOperation {
public:
    virtual ~ExpensiveOperation() = default;
    virtual int compute(int input) = 0;
};

class RealExpensiveOperation : public ExpensiveOperation {
public:
    int compute(int input) override {
        // Simulate expensive computation
        std::cout << "Performing expensive computation for input: " << input << "\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
        
        // Some computation
        return input * input;
    }
};

class CacheProxy : public ExpensiveOperation {
private:
    std::unique_ptr<RealExpensiveOperation> realOperation;
    mutable std::unordered_map<int, int> cache;
    mutable std::mutex cacheMutex;
    
public:
    CacheProxy() : realOperation(std::make_unique<RealExpensiveOperation>()) {}
    
    int compute(int input) override {
        // Check cache first
        {
            std::lock_guard<std::mutex> lock(cacheMutex);
            auto it = cache.find(input);
            if (it != cache.end()) {
                std::cout << "Cache hit for input: " << input << "\n";
                return it->second;
            }
        }
        
        // Compute and cache
        int result = realOperation->compute(input);
        
        {
            std::lock_guard<std::mutex> lock(cacheMutex);
            cache[input] = result;
            std::cout << "Cached result for input: " << input << "\n";
        }
        
        return result;
    }
    
    void clearCache() {
        std::lock_guard<std::mutex> lock(cacheMutex);
        cache.clear();
        std::cout << "Cache cleared\n";
    }
    
    size_t cacheSize() const {
        std::lock_guard<std::mutex> lock(cacheMutex);
        return cache.size();
    }
};

// ========== REMOTE PROXY (Simulation) ==========
class RemoteService {
public:
    virtual ~RemoteService() = default;
    virtual std::string fetchData(const std::string& query) = 0;
};

class RealRemoteService : public RemoteService {
public:
    std::string fetchData(const std::string& query) override {
        // Simulate network latency
        std::cout << "Making remote call for query: " << query << "\n";
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
        
        // Simulate response
        return "Remote data for: " + query;
    }
};

class RemoteProxy : public RemoteService {
private:
    std::unique_ptr<RealRemoteService> remoteService;
    mutable std::unordered_map<std::string, std::string> localCache;
    mutable std::mutex cacheMutex;
    
public:
    RemoteProxy() : remoteService(std::make_unique<RealRemoteService>()) {}
    
    std::string fetchData(const std::string& query) override {
        // Check local cache first
        {
            std::lock_guard<std::mutex> lock(cacheMutex);
            auto it = localCache.find(query);
            if (it != localCache.end()) {
                std::cout << "Local cache hit for: " << query << "\n";
                return it->second;
            }
        }
        
        // Make remote call
        std::string data = remoteService->fetchData(query);
        
        // Cache locally
        {
            std::lock_guard<std::mutex> lock(cacheMutex);
            localCache[query] = data;
        }
        
        return data;
    }
    
    // Additional proxy methods
    void preloadData(const std::vector<std::string>& queries) {
        std::cout << "Preloading data for " << queries.size() << " queries\n";
        for (const auto& query : queries) {
            fetchData(query);  // Will cache results
        }
    }
    
    void clearCache() {
        std::lock_guard<std::mutex> lock(cacheMutex);
        localCache.clear();
        std::cout << "Local cache cleared\n";
    }
};

// ========== LOGGING PROXY ==========
template<typename Subject>
class LoggingProxy {
private:
    Subject subject;
    
public:
    template<typename... Args>
    explicit LoggingProxy(Args&&... args) 
        : subject(std::forward<Args>(args)...) {}
    
    // Proxy methods with logging
    void operation() {
        std::cout << "[LOG] Before operation\n";
        auto start = std::chrono::high_resolution_clock::now();
        
        subject.operation();
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
        std::cout << "[LOG] After operation (took " << duration.count() << " μs)\n";
    }
    
    int calculate(int x, int y) {
        std::cout << "[LOG] Calculating " << x << " + " << y << "\n";
        int result = subject.calculate(x, y);
        std::cout << "[LOG] Result: " << result << "\n";
        return result;
    }
    
    // Forward other methods
    template<typename... Args>
    auto forward(Args&&... args) -> decltype(subject(std::forward<Args>(args)...)) {
        return subject(std::forward<Args>(args)...);
    }
};

class Calculator {
public:
    void operation() {
        std::cout << "Performing calculator operation\n";
    }
    
    int calculate(int x, int y) {
        return x + y;
    }
};

void proxyExample() {
    std::cout << "\n=== Proxy Pattern Examples ===\n\n";
    
    // 1. Virtual Proxy (Lazy Loading)
    std::cout << "1. Virtual Proxy (Lazy Loading):\n";
    ImageProxy image("large_photo.jpg");
    
    std::cout << "Image created (not loaded yet)\n";
    std::cout << "Is loaded? " << (image.isLoaded() ? "Yes" : "No") << "\n";
    
    // Load on first access
    std::cout << "Getting image width...\n";
    std::cout << "Width: " << image.getWidth() << "\n";
    std::cout << "Is loaded? " << (image.isLoaded() ? "Yes" : "No") << "\n";
    
    image.display();
    
    // 2. Protection Proxy
    std::cout << "\n2. Protection Proxy:\n";
    User admin("admin", {"view", "edit", "save"});
    User guest("guest", {"view"});
    User anonymous("anonymous", {});
    
    ProtectedDocument doc1("report.pdf", &admin);
    ProtectedDocument doc2("report.pdf", &guest);
    ProtectedDocument doc3("report.pdf", &anonymous);
    
    std::cout << "\nAdmin access:\n";
    doc1.view();
    doc1.edit();
    doc1.save();
    
    std::cout << "\nGuest access:\n";
    doc2.view();
    doc2.edit();  // Should be denied
    doc2.save();  // Should be denied
    
    std::cout << "\nAnonymous access:\n";
    doc3.view();  // Should be denied
    doc3.edit();  // Should be denied
    doc3.save();  // Should be denied
    
    // 3. Smart Pointer Proxy
    std::cout << "\n3. Smart Pointer Proxy:\n";
    {
        SmartPointerProxy<std::string> smartPtr(new std::string("Hello Proxy"));
        std::cout << "String: " << *smartPtr << "\n";
        std::cout << "Length: " << smartPtr->length() << "\n";
    } // Custom deleter called here
    
    // 4. Cache Proxy
    std::cout << "\n4. Cache Proxy:\n";
    CacheProxy cacheProxy;
    
    std::cout << "First computation (should be slow):\n";
    int result1 = cacheProxy.compute(5);
    std::cout << "Result: " << result1 << "\n";
    
    std::cout << "\nSecond computation (should be fast - cached):\n";
    int result2 = cacheProxy.compute(5);
    std::cout << "Result: " << result2 << "\n";
    
    std::cout << "\nDifferent input (should be slow):\n";
    int result3 = cacheProxy.compute(10);
    std::cout << "Result: " << result3 << "\n";
    
    std::cout << "Cache size: " << cacheProxy.cacheSize() << "\n";
    cacheProxy.clearCache();
    
    // 5. Remote Proxy
    std::cout << "\n5. Remote Proxy:\n";
    RemoteProxy remoteProxy;
    
    std::cout << "First fetch (should be slow):\n";
    std::string data1 = remoteProxy.fetchData("user/profile");
    std::cout << "Data: " << data1 << "\n";
    
    std::cout << "\nSecond fetch (should be fast - cached):\n";
    std::string data2 = remoteProxy.fetchData("user/profile");
    std::cout << "Data: " << data2 << "\n";
    
    // 6. Logging Proxy
    std::cout << "\n6. Logging Proxy:\n";
    LoggingProxy<Calculator> loggingCalculator;
    loggingCalculator.operation();
    int sum = loggingCalculator.calculate(10, 20);
    std::cout << "Final sum: " << sum << "\n";
}



#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>

// ========== BASIC COMPOSITE ==========
class FileSystemComponent {
public:
    virtual ~FileSystemComponent() = default;
    virtual void display(int depth = 0) const = 0;
    virtual size_t getSize() const = 0;
    virtual void add(std::unique_ptr<FileSystemComponent>) {
        throw std::runtime_error("Cannot add to leaf");
    }
    virtual void remove(FileSystemComponent*) {
        throw std::runtime_error("Cannot remove from leaf");
    }
    virtual FileSystemComponent* getChild(int) {
        return nullptr;
    }
    
    // Modern C++: Visitor support
    virtual void accept(class Visitor&) = 0;
};

// Leaf: File
class File : public FileSystemComponent {
private:
    std::string name;
    size_t size;
    
public:
    File(const std::string& name, size_t size) : name(name), size(size) {}
    
    void display(int depth = 0) const override {
        std::string indent(depth * 2, ' ');
        std::cout << indent << "📄 " << name << " (" << size << " bytes)\n";
    }
    
    size_t getSize() const override {
        return size;
    }
    
    void accept(Visitor& visitor) override;
    
    std::string getName() const {
        return name;
    }
};

// Composite: Directory
class Directory : public FileSystemComponent {
private:
    std::string name;
    std::vector<std::unique_ptr<FileSystemComponent>> children;
    
public:
    explicit Directory(const std::string& name) : name(name) {}
    
    void display(int depth = 0) const override {
        std::string indent(depth * 2, ' ');
        std::cout << indent << "📁 " << name << "\n";
        
        for (const auto& child : children) {
            child->display(depth + 1);
        }
    }
    
    size_t getSize() const override {
        size_t total = 0;
        for (const auto& child : children) {
            total += child->getSize();
        }
        return total;
    }
    
    void add(std::unique_ptr<FileSystemComponent> component) override {
        children.push_back(std::move(component));
    }
    
    void remove(FileSystemComponent* component) override {
        auto it = std::remove_if(children.begin(), children.end(),
            [component](const std::unique_ptr<FileSystemComponent>& child) {
                return child.get() == component;
            });
        children.erase(it, children.end());
    }
    
    FileSystemComponent* getChild(int index) override {
        if (index >= 0 && index < children.size()) {
            return children[index].get();
        }
        return nullptr;
    }
    
    void accept(Visitor& visitor) override;
    
    const std::vector<std::unique_ptr<FileSystemComponent>>& getChildren() const {
        return children;
    }
    
    std::string getName() const {
        return name;
    }
};

// ========== VISITOR PATTERN for Composite ==========
class Visitor {
public:
    virtual ~Visitor() = default;
    virtual void visitFile(File* file) = 0;
    virtual void visitDirectory(Directory* dir) = 0;
};

void File::accept(Visitor& visitor) {
    visitor.visitFile(this);
}

void Directory::accept(Visitor& visitor) {
    visitor.visitDirectory(this);
    
    for (auto& child : children) {
        child->accept(visitor);
    }
}

class SizeVisitor : public Visitor {
private:
    size_t totalSize;
    
public:
    SizeVisitor() : totalSize(0) {}
    
    void visitFile(File* file) override {
        totalSize += file->getSize();
    }
    
    void visitDirectory(Directory* dir) override {
        // Directory size already accounted for in file visits
    }
    
    size_t getTotalSize() const {
        return totalSize;
    }
};

class SearchVisitor : public Visitor {
private:
    std::string searchTerm;
    std::vector<FileSystemComponent*> results;
    
public:
    explicit SearchVisitor(const std::string& term) : searchTerm(term) {}
    
    void visitFile(File* file) override {
        if (file->getName().find(searchTerm) != std::string::npos) {
            results.push_back(file);
        }
    }
    
    void visitDirectory(Directory* dir) override {
        if (dir->getName().find(searchTerm) != std::string::npos) {
            results.push_back(dir);
        }
    }
    
    const std::vector<FileSystemComponent*>& getResults() const {
        return results;
    }
};

// ========== UI COMPONENT COMPOSITE ==========
class UIComponent {
public:
    virtual ~UIComponent() = default;
    virtual void render() const = 0;
    virtual void add(std::unique_ptr<UIComponent>) {
        throw std::runtime_error("Cannot add to leaf component");
    }
    virtual void remove(UIComponent*) {
        throw std::runtime_error("Cannot remove from leaf component");
    }
    
    // Modern C++: Composite operations with algorithms
    virtual void forEach(std::function<void(UIComponent&)>) = 0;
};

class Button : public UIComponent {
private:
    std::string label;
    
public:
    explicit Button(const std::string& label) : label(label) {}
    
    void render() const override {
        std::cout << "[Button: " << label << "]\n";
    }
    
    void forEach(std::function<void(UIComponent&)> func) override {
        func(*this);
    }
    
    void click() {
        std::cout << "Button '" << label << "' clicked!\n";
    }
};

class Panel : public UIComponent {
private:
    std::string title;
    std::vector<std::unique_ptr<UIComponent>> children;
    
public:
    explicit Panel(const std::string& title) : title(title) {}
    
    void render() const override {
        std::cout << "┌─ Panel: " << title << " ─┐\n";
        for (const auto& child : children) {
            std::cout << "│ ";
            child->render();
        }
        std::cout << "└" << std::string(title.length() + 12, '─') << "┘\n";
    }
    
    void add(std::unique_ptr<UIComponent> component) override {
        children.push_back(std::move(component));
    }
    
    void remove(UIComponent* component) override {
        auto it = std::remove_if(children.begin(), children.end(),
            [component](const std::unique_ptr<UIComponent>& child) {
                return child.get() == component;
            });
        children.erase(it, children.end());
    }
    
    void forEach(std::function<void(UIComponent&)> func) override {
        func(*this);
        for (auto& child : children) {
            child->forEach(func);
        }
    }
    
    size_t count() const {
        return children.size();
    }
};

// ========== EXPRESSION TREE COMPOSITE ==========
class Expression {
public:
    virtual ~Expression() = default;
    virtual double evaluate() const = 0;
    virtual std::string toString() const = 0;
    virtual std::unique_ptr<Expression> clone() const = 0;
    
    // Composite operations
    virtual void add(std::unique_ptr<Expression>) {
        throw std::runtime_error("Cannot add to leaf expression");
    }
};

class Number : public Expression {
private:
    double value;
    
public:
    explicit Number(double value) : value(value) {}
    
    double evaluate() const override {
        return value;
    }
    
    std::string toString() const override {
        return std::to_string(value);
    }
    
    std::unique_ptr<Expression> clone() const override {
        return std::make_unique<Number>(*this);
    }
};

class BinaryOperation : public Expression {
private:
    char op;
    std::unique_ptr<Expression> left;
    std::unique_ptr<Expression> right;
    
public:
    BinaryOperation(char op, std::unique_ptr<Expression> left, 
                   std::unique_ptr<Expression> right)
        : op(op), left(std::move(left)), right(std::move(right)) {}
    
    double evaluate() const override {
        double l = left->evaluate();
        double r = right->evaluate();
        
        switch (op) {
            case '+': return l + r;
            case '-': return l - r;
            case '*': return l * r;
            case '/': 
                if (r == 0) throw std::runtime_error("Division by zero");
                return l / r;
            default: throw std::runtime_error("Unknown operator");
        }
    }
    
    std::string toString() const override {
        return "(" + left->toString() + " " + op + " " + right->toString() + ")";
    }
    
    std::unique_ptr<Expression> clone() const override {
        return std::make_unique<BinaryOperation>(
            op, left->clone(), right->clone());
    }
    
    void add(std::unique_ptr<Expression> expr) override {
        // In a more complex system, you might add to left or right
        throw std::runtime_error("Binary operation cannot accept additional operands");
    }
};

// ========== MENU COMPOSITE ==========
class MenuItem {
public:
    virtual ~MenuItem() = default;
    virtual void display(int depth = 0) const = 0;
    virtual void execute() = 0;
    virtual void add(std::unique_ptr<MenuItem>) {
        throw std::runtime_error("Cannot add to menu item");
    }
};

class Command : public MenuItem {
private:
    std::string name;
    std::function<void()> action;
    
public:
    Command(const std::string& name, std::function<void()> action)
        : name(name), action(std::move(action)) {}
    
    void display(int depth = 0) const override {
        std::string indent(depth * 2, ' ');
        std::cout << indent << "• " << name << "\n";
    }
    
    void execute() override {
        std::cout << "Executing command: " << name << "\n";
        if (action) {
            action();
        }
    }
};

class SubMenu : public MenuItem {
private:
    std::string name;
    std::vector<std::unique_ptr<MenuItem>> items;
    
public:
    explicit SubMenu(const std::string& name) : name(name) {}
    
    void display(int depth = 0) const override {
        std::string indent(depth * 2, ' ');
        std::cout << indent << "▼ " << name << "\n";
        
        for (const auto& item : items) {
            item->display(depth + 1);
        }
    }
    
    void execute() override {
        std::cout << "Opening submenu: " << name << "\n";
        // In a real GUI, this would show the submenu
        for (const auto& item : items) {
            item->display(1);
        }
    }
    
    void add(std::unique_ptr<MenuItem> item) override {
        items.push_back(std::move(item));
    }
    
    MenuItem* findItem(const std::string& name) {
        for (auto& item : items) {
            if (auto command = dynamic_cast<Command*>(item.get())) {
                // Would need getName() method
                continue;
            } else if (auto submenu = dynamic_cast<SubMenu*>(item.get())) {
                auto found = submenu->findItem(name);
                if (found) return found;
            }
        }
        return nullptr;
    }
};

void compositeExample() {
    std::cout << "\n=== Composite Pattern Examples ===\n\n";
    
    // 1. File System Composite
    std::cout << "1. File System Composite:\n";
    auto root = std::make_unique<Directory>("root");
    auto home = std::make_unique<Directory>("home");
    auto documents = std::make_unique<Directory>("documents");
    
    home->add(std::make_unique<File>(".bashrc", 1024));
    home->add(std::make_unique<File>(".profile", 512));
    
    documents->add(std::make_unique<File>("report.docx", 20480));
    documents->add(std::make_unique<File>("presentation.pptx", 40960));
    
    home->add(std::move(documents));
    root->add(std::move(home));
    root->add(std::make_unique<File>("readme.txt", 1024));
    
    root->display();
    std::cout << "Total size: " << root->getSize() << " bytes\n";
    
    // Visitor pattern with composite
    SizeVisitor sizeVisitor;
    root->accept(sizeVisitor);
    std::cout << "Size via visitor: " << sizeVisitor.getTotalSize() << " bytes\n";
    
    SearchVisitor searchVisitor("report");
    root->accept(searchVisitor);
    std::cout << "Search results: " << searchVisitor.getResults().size() << " found\n";
    
    // 2. UI Component Composite
    std::cout << "\n2. UI Component Composite:\n";
    auto mainPanel = std::make_unique<Panel>("Main Window");
    
    auto toolbar = std::make_unique<Panel>("Toolbar");
    toolbar->add(std::make_unique<Button>("New"));
    toolbar->add(std::make_unique<Button>("Open"));
    toolbar->add(std::make_unique<Button>("Save"));
    
    auto contentPanel = std::make_unique<Panel>("Content");
    contentPanel->add(std::make_unique<Button>("Edit"));
    contentPanel->add(std::make_unique<Button>("Delete"));
    
    auto sidebar = std::make_unique<Panel>("Sidebar");
    sidebar->add(std::make_unique<Button>("Settings"));
    sidebar->add(std::make_unique<Button>("Help"));
    
    mainPanel->add(std::move(toolbar));
    mainPanel->add(std::move(contentPanel));
    mainPanel->add(std::move(sidebar));
    
    mainPanel->render();
    
    // Count all components
    size_t componentCount = 0;
    mainPanel->forEach([&componentCount](UIComponent&) {
        componentCount++;
    });
    std::cout << "Total components: " << componentCount << "\n";
    
    // 3. Expression Tree Composite
    std::cout << "\n3. Expression Tree Composite:\n";
    // Build expression: (5 + 3) * (10 - 2) / 4
    auto expr = std::make_unique<BinaryOperation>('/',
        std::make_unique<BinaryOperation>('*',
            std::make_unique<BinaryOperation>('+',
                std::make_unique<Number>(5),
                std::make_unique<Number>(3)
            ),
            std::make_unique<BinaryOperation>('-',
                std::make_unique<Number>(10),
                std::make_unique<Number>(2)
            )
        ),
        std::make_unique<Number>(4)
    );
    
    std::cout << "Expression: " << expr->toString() << "\n";
    std::cout << "Result: " << expr->evaluate() << "\n";
    
    // Clone expression
    auto clonedExpr = expr->clone();
    std::cout << "Cloned expression: " << clonedExpr->toString() << "\n";
    std::cout << "Cloned result: " << clonedExpr->evaluate() << "\n";
    
    // 4. Menu Composite
    std::cout << "\n4. Menu Composite:\n";
    auto fileMenu = std::make_unique<SubMenu>("File");
    fileMenu->add(std::make_unique<Command>("New", []() {
        std::cout << "Creating new file...\n";
    }));
    fileMenu->add(std::make_unique<Command>("Open", []() {
        std::cout << "Opening file...\n";
    }));
    fileMenu->add(std::make_unique<Command>("Save", []() {
        std::cout << "Saving file...\n";
    }));
    
    auto editMenu = std::make_unique<SubMenu>("Edit");
    editMenu->add(std::make_unique<Command>("Cut", []() {
        std::cout << "Cutting selection...\n";
    }));
    editMenu->add(std::make_unique<Command>("Copy", []() {
        std::cout << "Copying selection...\n";
    }));
    editMenu->add(std::make_unique<Command>("Paste", []() {
        std::cout << "Pasting clipboard...\n";
    }));
    
    auto helpMenu = std::make_unique<SubMenu>("Help");
    helpMenu->add(std::make_unique<Command>("About", []() {
        std::cout << "About this application...\n";
    }));
    
    auto mainMenu = std::make_unique<SubMenu>("Main Menu");
    mainMenu->add(std::move(fileMenu));
    mainMenu->add(std::move(editMenu));
    mainMenu->add(std::move(helpMenu));
    
    mainMenu->display();
    std::cout << "\nExecuting menu commands:\n";
    
    // Simulate executing some commands
    auto executeCommand = [](MenuItem& item) {
        if (auto cmd = dynamic_cast<Command*>(&item)) {
            cmd->execute();
        }
    };
    
    // In a real application, you'd navigate the menu structure
    std::cout << "\n(Simulating user interaction)\n";
}


#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <functional>
#include <mutex>

// ========== CLASSIC OBSERVER ==========
class IObserver {
public:
    virtual ~IObserver() = default;
    virtual void update(const std::string& message) = 0;
    virtual std::string getName() const = 0;
};

class ISubject {
public:
    virtual ~ISubject() = default;
    virtual void attach(std::shared_ptr<IObserver> observer) = 0;
    virtual void detach(std::shared_ptr<IObserver> observer) = 0;
    virtual void notify(const std::string& message) = 0;
};

class NewsAgency : public ISubject {
private:
    std::string name;
    std::vector<std::shared_ptr<IObserver>> observers;
    std::mutex mutex;
    
public:
    explicit NewsAgency(const std::string& name) : name(name) {}
    
    void attach(std::shared_ptr<IObserver> observer) override {
        std::lock_guard<std::mutex> lock(mutex);
        observers.push_back(observer);
        std::cout << observer->getName() << " subscribed to " << name << "\n";
    }
    
    void detach(std::shared_ptr<IObserver> observer) override {
        std::lock_guard<std::mutex> lock(mutex);
        auto it = std::remove_if(observers.begin(), observers.end(),
            [observer](const std::shared_ptr<IObserver>& obs) {
                return obs == observer;
            });
        observers.erase(it, observers.end());
        std::cout << observer->getName() << " unsubscribed from " << name << "\n";
    }
    
    void notify(const std::string& message) override {
        std::lock_guard<std::mutex> lock(mutex);
        std::cout << "\n" << name << " broadcasting: " << message << "\n";
        for (const auto& observer : observers) {
            observer->update(message);
        }
    }
    
    void publishNews(const std::string& headline) {
        notify("BREAKING: " + headline);
    }
};

class NewsChannel : public IObserver {
private:
    std::string channelName;
    
public:
    explicit NewsChannel(const std::string& name) : channelName(name) {}
    
    void update(const std::string& message) override {
        std::cout << channelName << " received: " << message << "\n";
    }
    
    std::string getName() const override {
        return channelName;
    }
};

// ========== MODERN C++ OBSERVER (Signals and Slots) ==========
template<typename... Args>
class Signal {
private:
    using Slot = std::function<void(Args...)>;
    std::vector<Slot> slots;
    std::mutex mutex;
    
public:
    // Connect a slot
    void connect(Slot slot) {
        std::lock_guard<std::mutex> lock(mutex);
        slots.push_back(std::move(slot));
    }
    
    // Disconnect all slots
    void disconnectAll() {
        std::lock_guard<std::mutex> lock(mutex);
        slots.clear();
    }
    
    // Emit signal
    void emit(Args... args) {
        std::vector<Slot> localSlots;
        {
            std::lock_guard<std::mutex> lock(mutex);
            localSlots = slots;
        }
        
        for (const auto& slot : localSlots) {
            slot(args...);
        }
    }
    
    // Number of connected slots
    size_t count() const {
        std::lock_guard<std::mutex> lock(mutex);
        return slots.size();
    }
};

// Example usage
class Button {
public:
    Signal<> clicked;
    Signal<const std::string&> textChanged;
    
    void press() {
        std::cout << "Button pressed\n";
        clicked.emit();
    }
    
    void setText(const std::string& text) {
        std::cout << "Button text changed to: " << text << "\n";
        textChanged.emit(text);
    }
};

// ========== REACTIVE OBSERVER (C++17) ==========
template<typename T>
class Observable {
private:
    T value;
    Signal<const T&, const T&> valueChanged;
    
public:
    Observable() = default;
    explicit Observable(const T& initial) : value(initial) {}
    
    // Get current value
    const T& get() const {
        return value;
    }
    
    // Set new value and notify observers
    void set(const T& newValue) {
        if (value != newValue) {
            T oldValue = value;
            value = newValue;
            valueChanged.emit(oldValue, newValue);
        }
    }
    
    // Subscribe to value changes
    void subscribe(std::function<void(const T&, const T&)> callback) {
        valueChanged.connect(std::move(callback));
    }
    
    // Operator overload for intuitive usage
    Observable& operator=(const T& newValue) {
        set(newValue);
        return *this;
    }
    
    operator T() const {
        return value;
    }
};

// ========== EVENT BUS (Advanced Observer) ==========
class Event {
public:
    virtual ~Event() = default;
    virtual std::string getType() const = 0;
};

template<typename T>
class TypedEvent : public Event {
private:
    T data;
    
public:
    explicit TypedEvent(const T& data) : data(data) {}
    
    std::string getType() const override {
        return typeid(T).name();
    }
    
    const T& getData() const {
        return data;
    }
};

class EventBus {
private:
    using EventHandler = std::function<void(const Event&)>;
    std::unordered_map<std::string, std::vector<EventHandler>> handlers;
    std::mutex mutex;
    
public:
    // Subscribe to event type
    template<typename EventType>
    void subscribe(std::function<void(const EventType&)> handler) {
        std::lock_guard<std::mutex> lock(mutex);
        std::string typeName = typeid(EventType).name();
        
        // Convert typed handler to generic handler
        handlers[typeName].push_back([handler](const Event& event) {
            if (auto typedEvent = dynamic_cast<const TypedEvent<
                typename std::remove_const<
                typename std::remove_reference<EventType>::type>::type>*>(&event)) {
                handler(typedEvent->getData());
            }
        });
    }
    
    // Publish event
    template<typename EventType>
    void publish(const EventType& event) {
        std::string typeName = typeid(EventType).name();
        std::vector<EventHandler> localHandlers;
        
        {
            std::lock_guard<std::mutex> lock(mutex);
            auto it = handlers.find(typeName);
            if (it != handlers.end()) {
                localHandlers = it->second;
            }
        }
        
        for (const auto& handler : localHandlers) {
            handler(event);
        }
    }
    
    // Unsubscribe all
    void clear() {
        std::lock_guard<std::mutex> lock(mutex);
        handlers.clear();
    }
};

// ========== OBSERVER WITH PRIORITIES ==========
class PriorityObserver {
private:
    struct ObserverEntry {
        std::shared_ptr<IObserver> observer;
        int priority;
        
        bool operator<(const ObserverEntry& other) const {
            return priority > other.priority;  // Higher priority first
        }
    };
    
    std::vector<ObserverEntry> observers;
    std::mutex mutex;
    
public:
    void attach(std::shared_ptr<IObserver> observer, int priority = 0) {
        std::lock_guard<std::mutex> lock(mutex);
        observers.push_back({observer, priority});
        std::sort(observers.begin(), observers.end());
    }
    
    void detach(std::shared_ptr<IObserver> observer) {
        std::lock_guard<std::mutex> lock(mutex);
        auto it = std::remove_if(observers.begin(), observers.end(),
            [observer](const ObserverEntry& entry) {
                return entry.observer == observer;
            });
        observers.erase(it, observers.end());
    }
    
    void notify(const std::string& message) {
        std::vector<ObserverEntry> localObservers;
        {
            std::lock_guard<std::mutex> lock(mutex);
            localObservers = observers;
        }
        
        for (const auto& entry : localObservers) {
            entry.observer->update(message);
        }
    }
};

// ========== OBSERVER WITH UNSUBSCRIBE TOKENS ==========
class Subscription {
public:
    virtual ~Subscription() = default;
    virtual void unsubscribe() = 0;
};

template<typename... Args>
class ObservableWithTokens {
private:
    using Callback = std::function<void(Args...)>;
    
    struct CallbackEntry {
        Callback callback;
        std::shared_ptr<bool> isValid;
    };
    
    std::vector<CallbackEntry> callbacks;
    std::mutex mutex;
    
public:
    class Token : public Subscription {
    private:
        std::weak_ptr<bool> isValid;
        
    public:
        explicit Token(std::weak_ptr<bool> isValid) : isValid(isValid) {}
        
        void unsubscribe() override {
            if (auto valid = isValid.lock()) {
                *valid = false;
            }
        }
    };
    
    std::unique_ptr<Subscription> subscribe(Callback callback) {
        std::lock_guard<std::mutex> lock(mutex);
        auto isValid = std::make_shared<bool>(true);
        callbacks.push_back({std::move(callback), isValid});
        
        return std::make_unique<Token>(isValid);
    }
    
    void notify(Args... args) {
        std::vector<CallbackEntry> localCallbacks;
        {
            std::lock_guard<std::mutex> lock(mutex);
            localCallbacks = callbacks;
        }
        
        // Clean up invalid callbacks
        auto it = std::remove_if(localCallbacks.begin(), localCallbacks.end(),
            [](const CallbackEntry& entry) {
                return !*(entry.isValid);
            });
        localCallbacks.erase(it, localCallbacks.end());
        
        // Update main list
        {
            std::lock_guard<std::mutex> lock(mutex);
            callbacks = localCallbacks;
        }
        
        // Notify valid callbacks
        for (const auto& entry : localCallbacks) {
            if (*(entry.isValid)) {
                entry.callback(args...);
            }
        }
    }
    
    size_t subscriberCount() const {
        std::lock_guard<std::mutex> lock(mutex);
        return callbacks.size();
    }
};

void observerExample() {
    std::cout << "\n=== Observer Pattern Examples ===\n\n";
    
    // 1. Classic Observer
    std::cout << "1. Classic Observer (News Agency):\n";
    auto cnn = std::make_shared<NewsAgency>("CNN");
    
    auto bbc = std::make_shared<NewsChannel>("BBC News");
    auto fox = std::make_shared<NewsChannel>("Fox News");
    auto aljazeera = std::make_shared<NewsChannel>("Al Jazeera");
    
    cnn->attach(bbc);
    cnn->attach(fox);
    cnn->attach(aljazeera);
    
    cnn->publishNews("Stock market reaches all-time high");
    cnn->detach(fox);
    cnn->publishNews("New scientific discovery announced");
    
    // 2. Modern Signal/Slot
    std::cout << "\n2. Modern Signal/Slot Pattern:\n";
    Button button;
    
    // Connect slots
    button.clicked.connect([]() {
        std::cout << "Slot 1: Button was clicked!\n";
    });
    
    button.clicked.connect([]() {
        std::cout << "Slot 2: Handling click event\n";
    });
    
    button.textChanged.connect([](const std::string& text) {
        std::cout << "Text changed to: " << text << "\n";
    });
    
    // Emit signals
    button.press();
    button.setText("Submit");
    button.press();
    
    std::cout << "Connected slots: " << button.clicked.count() << "\n";
    
    // 3. Reactive Observable
    std::cout << "\n3. Reactive Observable (C++17):\n";
    Observable<int> counter(0);
    
    counter.subscribe([](const int& oldVal, const int& newVal) {
        std::cout << "Counter changed from " << oldVal << " to " << newVal << "\n";
    });
    
    counter = 10;  // Will trigger notification
    counter = 20;  // Will trigger notification
    counter = 20;  // Will NOT trigger (same value)
    
    // Use like regular variable
    int current = counter;
    std::cout << "Current value: " << current << "\n";
    
    // 4. Event Bus
    std::cout << "\n4. Event Bus Pattern:\n";
    EventBus bus;
    
    // Subscribe to specific event types
    bus.subscribe<std::string>([](const std::string& message) {
        std::cout << "String event: " << message << "\n";
    });
    
    bus.subscribe<int>([](int value) {
        std::cout << "Integer event: " << value << "\n";
    });
    
    // Publish events
    bus.publish(TypedEvent<std::string>("Hello Event Bus!"));
    bus.publish(TypedEvent<int>(42));
    
    // 5. Observer with Unsubscribe Tokens
    std::cout << "\n5. Observer with Unsubscribe Tokens:\n";
    ObservableWithTokens<std::string> observable;
    
    auto token1 = observable.subscribe([](const std::string& msg) {
        std::cout << "Observer 1: " << msg << "\n";
    });
    
    auto token2 = observable.subscribe([](const std::string& msg) {
        std::cout << "Observer 2: " << msg << "\n";
    });
    
    observable.notify("First notification");
    
    // Unsubscribe one observer
    token1->unsubscribe();
    observable.notify("Second notification");
    
    std::cout << "Remaining subscribers: " << observable.subscriberCount() << "\n";
}


#include <iostream>
#include <memory>
#include <vector>
#include <algorithm>
#include <functional>
#include <cmath>

// ========== CLASSIC STRATEGY ==========
class SortStrategy {
public:
    virtual ~SortStrategy() = default;
    virtual void sort(std::vector<int>& data) const = 0;
    virtual std::string getName() const = 0;
};

class BubbleSort : public SortStrategy {
public:
    void sort(std::vector<int>& data) const override {
        std::cout << "Using Bubble Sort\n";
        for (size_t i = 0; i < data.size(); ++i) {
            for (size_t j = 0; j < data.size() - i - 1; ++j) {
                if (data[j] > data[j + 1]) {
                    std::swap(data[j], data[j + 1]);
                }
            }
        }
    }
    
    std::string getName() const override {
        return "Bubble Sort";
    }
};

class QuickSort : public SortStrategy {
private:
    void quickSort(std::vector<int>& data, int low, int high) const {
        if (low < high) {
            int pi = partition(data, low, high);
            quickSort(data, low, pi - 1);
            quickSort(data, pi + 1, high);
        }
    }
    
    int partition(std::vector<int>& data, int low, int high) const {
        int pivot = data[high];
        int i = low - 1;
        
        for (int j = low; j <= high - 1; ++j) {
            if (data[j] < pivot) {
                ++i;
                std::swap(data[i], data[j]);
            }
        }
        std::swap(data[i + 1], data[high]);
        return i + 1;
    }
    
public:
    void sort(std::vector<int>& data) const override {
        std::cout << "Using Quick Sort\n";
        if (!data.empty()) {
            quickSort(data, 0, data.size() - 1);
        }
    }
    
    std::string getName() const override {
        return "Quick Sort";
    }
};

class MergeSort : public SortStrategy {
private:
    void merge(std::vector<int>& data, int left, int mid, int right) const {
        int n1 = mid - left + 1;
        int n2 = right - mid;
        
        std::vector<int> L(n1), R(n2);
        
        for (int i = 0; i < n1; ++i)
            L[i] = data[left + i];
        for (int j = 0; j < n2; ++j)
            R[j] = data[mid + 1 + j];
        
        int i = 0, j = 0, k = left;
        
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) {
                data[k] = L[i];
                ++i;
            } else {
                data[k] = R[j];
                ++j;
            }
            ++k;
        }
        
        while (i < n1) {
            data[k] = L[i];
            ++i;
            ++k;
        }
        
        while (j < n2) {
            data[k] = R[j];
            ++j;
            ++k;
        }
    }
    
    void mergeSort(std::vector<int>& data, int left, int right) const {
        if (left < right) {
            int mid = left + (right - left) / 2;
            mergeSort(data, left, mid);
            mergeSort(data, mid + 1, right);
            merge(data, left, mid, right);
        }
    }
    
public:
    void sort(std::vector<int>& data) const override {
        std::cout << "Using Merge Sort\n";
        if (!data.empty()) {
            mergeSort(data, 0, data.size() - 1);
        }
    }
    
    std::string getName() const override {
        return "Merge Sort";
    }
};

class Sorter {
private:
    std::unique_ptr<SortStrategy> strategy;
    
public:
    void setStrategy(std::unique_ptr<SortStrategy> newStrategy) {
        strategy = std::move(newStrategy);
    }
    
    void sortData(std::vector<int>& data) const {
        if (strategy) {
            auto dataCopy = data;  // Don't modify original
            strategy->sort(dataCopy);
            data = dataCopy;
        } else {
            std::cout << "No strategy set!\n";
        }
    }
    
    void sortInPlace(std::vector<int>& data) const {
        if (strategy) {
            strategy->sort(data);
        } else {
            std::cout << "No strategy set!\n";
        }
    }
};

// ========== PAYMENT STRATEGY ==========
class PaymentStrategy {
public:
    virtual ~PaymentStrategy() = default;
    virtual void pay(double amount) const = 0;
    virtual std::string getName() const = 0;
};

class CreditCardPayment : public PaymentStrategy {
private:
    std::string cardNumber;
    std::string cvv;
    
public:
    CreditCardPayment(const std::string& card, const std::string& cvv)
        : cardNumber(card), cvv(cvv) {}
    
    void pay(double amount) const override {
        std::cout << "Processing credit card payment of $" << amount << "\n";
        std::cout << "Card: " << maskCardNumber(cardNumber) << "\n";
        // Process payment...
    }
    
    std::string getName() const override {
        return "Credit Card";
    }
    
private:
    std::string maskCardNumber(const std::string& card) const {
        if (card.length() > 4) {
            return std::string(card.length() - 4, '*') + card.substr(card.length() - 4);
        }
        return card;
    }
};

class PayPalPayment : public PaymentStrategy {
private:
    std::string email;
    
public:
    explicit PayPalPayment(const std::string& email) : email(email) {}
    
    void pay(double amount) const override {
        std::cout << "Processing PayPal payment of $" << amount << "\n";
        std::cout << "Email: " << email << "\n";
        // Process PayPal payment...
    }
    
    std::string getName() const override {
        return "PayPal";
    }
};

class CryptoPayment : public PaymentStrategy {
private:
    std::string walletAddress;
    
public:
    explicit CryptoPayment(const std::string& wallet) : walletAddress(wallet) {}
    
    void pay(double amount) const override {
        std::cout << "Processing cryptocurrency payment of $" << amount << "\n";
        std::cout << "Wallet: " << walletAddress << "\n";
        // Process crypto payment...
    }
    
    std::string getName() const override {
        return "Cryptocurrency";
    }
};

class ShoppingCart {
private:
    std::vector<double> items;
    std::unique_ptr<PaymentStrategy> paymentStrategy;
    
public:
    void addItem(double price) {
        items.push_back(price);
    }
    
    double getTotal() const {
        return std::accumulate(items.begin(), items.end(), 0.0);
    }
    
    void setPaymentStrategy(std::unique_ptr<PaymentStrategy> strategy) {
        paymentStrategy = std::move(strategy);
    }
    
    void checkout() const {
        double total = getTotal();
        std::cout << "\nChecking out...\n";
        std::cout << "Total: $" << total << "\n";
        
        if (paymentStrategy) {
            std::cout << "Using: " << paymentStrategy->getName() << "\n";
            paymentStrategy->pay(total);
        } else {
            std::cout << "No payment method selected!\n";
        }
    }
};

// ========== COMPRESSION STRATEGY ==========
class CompressionStrategy {
public:
    virtual ~CompressionStrategy() = default;
    virtual std::string compress(const std::string& data) const = 0;
    virtual std::string decompress(const std::string& data) const = 0;
    virtual std::string getName() const = 0;
    virtual double getCompressionRatio(const std::string& data) const {
        std::string compressed = compress(data);
        if (data.empty()) return 1.0;
        return static_cast<double>(compressed.size()) / data.size();
    }
};

class ZipCompression : public CompressionStrategy {
public:
    std::string compress(const std::string& data) const override {
        std::cout << "Compressing with ZIP\n";
        // Simple simulation - real ZIP would be more complex
        return "ZIP[" + data + "]";
    }
    
    std::string decompress(const std::string& data) const override {
        std::cout << "Decompressing ZIP\n";
        if (data.find("ZIP[") == 0 && data.back() == ']') {
            return data.substr(4, data.length() - 5);
        }
        return data;
    }
    
    std::string getName() const override {
        return "ZIP";
    }
};

class GzipCompression : public CompressionStrategy {
public:
    std::string compress(const std::string& data) const override {
        std::cout << "Compressing with GZIP\n";
        // Simple simulation
        return "GZIP[" + data + "]";
    }
    
    std::string decompress(const std::string& data) const override {
        std::cout << "Decompressing GZIP\n";
        if (data.find("GZIP[") == 0 && data.back() == ']') {
            return data.substr(5, data.length() - 6);
        }
        return data;
    }
    
    std::string getName() const override {
        return "GZIP";
    }
};

class Bzip2Compression : public CompressionStrategy {
public:
    std::string compress(const std::string& data) const override {
        std::cout << "Compressing with BZIP2\n";
        // Simple simulation
        return "BZIP2[" + data + "]";
    }
    
    std::string decompress(const std::string& data) const override {
        std::cout << "Decompressing BZIP2\n";
        if (data.find("BZIP2[") == 0 && data.back() == ']') {
            return data.substr(6, data.length() - 7);
        }
        return data;
    }
    
    std::string getName() const override {
        return "BZIP2";
    }
};

class FileCompressor {
private:
    std::unique_ptr<CompressionStrategy> strategy;
    
public:
    void setStrategy(std::unique_ptr<CompressionStrategy> newStrategy) {
        strategy = std::move(newStrategy);
    }
    
    std::string compressFile(const std::string& filename, const std::string& content) const {
        if (!strategy) {
            throw std::runtime_error("No compression strategy set");
        }
        
        std::cout << "Compressing file: " << filename << "\n";
        std::string compressed = strategy->compress(content);
        
        double ratio = strategy->getCompressionRatio(content);
        std::cout << "Compression ratio: " << ratio 
                  << " (" << strategy->getName() << ")\n";
        
        return compressed;
    }
    
    std::string decompressFile(const std::string& filename, const std::string& compressed) const {
        if (!strategy) {
            throw std::runtime_error("No compression strategy set");
        }
        
        std::cout << "Decompressing file: " << filename << "\n";
        return strategy->decompress(compressed);
    }
};

// ========== STRATEGY WITH FUNCTION OBJECTS (Modern C++) ==========
template<typename T>
class SortingContext {
private:
    std::function<void(std::vector<T>&)> sortFunction;
    std::string strategyName;
    
public:
    template<typename Strategy>
    void setStrategy(Strategy&& strategy) {
        sortFunction = std::forward<Strategy>(strategy);
        strategyName = typeid(Strategy).name();
    }
    
    void setStrategy(std::function<void(std::vector<T>&)> func, const std::string& name = "") {
        sortFunction = std::move(func);
        strategyName = name.empty() ? "Custom Strategy" : name;
    }
    
    void sort(std::vector<T>& data) const {
        if (sortFunction) {
            std::cout << "Using strategy: " << strategyName << "\n";
            sortFunction(data);
        } else {
            std::cout << "No strategy set!\n";
        }
    }
};

// Lambda strategies
auto lambdaBubbleSort = [](std::vector<int>& data) {
    std::cout << "Lambda Bubble Sort\n";
    for (size_t i = 0; i < data.size(); ++i) {
        for (size_t j = 0; j < data.size() - i - 1; ++j) {
            if (data[j] > data[j + 1]) {
                std::swap(data[j], data[j + 1]);
            }
        }
    }
};

auto lambdaStdSort = [](std::vector<int>& data) {
    std::cout << "Using std::sort\n";
    std::sort(data.begin(), data.end());
};

// ========== STRATEGY WITH TEMPLATES ==========
template<typename SortPolicy>
class GenericSorter {
public:
    void sort(std::vector<int>& data) const {
        SortPolicy::sort(data);
    }
};

struct StdSortPolicy {
    static void sort(std::vector<int>& data) {
        std::cout << "Template Policy: std::sort\n";
        std::sort(data.begin(), data.end());
    }
};

struct StableSortPolicy {
    static void sort(std::vector<int>& data) {
        std::cout << "Template Policy: std::stable_sort\n";
        std::stable_sort(data.begin(), data.end());
    }
};

void strategyExample() {
    std::cout << "\n=== Strategy Pattern Examples ===\n\n";
    
    // 1. Sorting Strategies
    std::cout << "1. Sorting Strategies:\n";
    std::vector<int> data = {64, 34, 25, 12, 22, 11, 90};
    
    Sorter sorter;
    std::cout << "Original: ";
    for (int n : data) std::cout << n << " ";
    std::cout << "\n";
    
    sorter.setStrategy(std::make_unique<BubbleSort>());
    auto data1 = data;
    sorter.sortInPlace(data1);
    std::cout << "Sorted: ";
    for (int n : data1) std::cout << n << " ";
    std::cout << "\n";
    
    sorter.setStrategy(std::make_unique<QuickSort>());
    auto data2 = data;
    sorter.sortInPlace(data2);
    std::cout << "Sorted: ";
    for (int n : data2) std::cout << n << " ";
    std::cout << "\n";
    
    // 2. Payment Strategies
    std::cout << "\n2. Payment Strategies:\n";
    ShoppingCart cart;
    cart.addItem(25.99);
    cart.addItem(19.99);
    cart.addItem(5.99);
    
    // Credit Card
    cart.setPaymentStrategy(
        std::make_unique<CreditCardPayment>("4111111111111111", "123"));
    cart.checkout();
    
    // PayPal
    cart.setPaymentStrategy(
        std::make_unique<PayPalPayment>("user@example.com"));
    cart.checkout();
    
    // Crypto
    cart.setPaymentStrategy(
        std::make_unique<CryptoPayment>("0xABC123DEF456"));
    cart.checkout();
    
    // 3. Compression Strategies
    std::cout << "\n3. Compression Strategies:\n";
    FileCompressor compressor;
    std::string originalData = "This is some sample data that needs compression";
    
    compressor.setStrategy(std::make_unique<ZipCompression>());
    std::string compressed = compressor.compressFile("data.txt", originalData);
    std::string decompressed = compressor.decompressFile("data.txt", compressed);
    std::cout << "Original: " << originalData << "\n";
    std::cout << "Decompressed: " << decompressed << "\n";
    std::cout << (originalData == decompressed ? "✓ Match" : "✗ Mismatch") << "\n";
    
    // 4. Lambda Strategies
    std::cout << "\n4. Lambda Strategies:\n";
    SortingContext<int> context;
    std::vector<int> numbers = {5, 2, 8, 1, 9};
    
    context.setStrategy(lambdaBubbleSort, "Bubble Sort Lambda");
    auto nums1 = numbers;
    context.sort(nums1);
    std::cout << "Result: ";
    for (int n : nums1) std::cout << n << " ";
    std::cout << "\n";
    
    context.setStrategy(lambdaStdSort, "std::sort Lambda");
    auto nums2 = numbers;
    context.sort(nums2);
    std::cout << "Result: ";
    for (int n : nums2) std::cout << n << " ";
    std::cout << "\n";
    
    // Inline lambda
    context.setStrategy([](std::vector<int>& data) {
        std::cout << "Reverse sort\n";
        std::sort(data.rbegin(), data.rend());
    }, "Reverse Sort");
    
    auto nums3 = numbers;
    context.sort(nums3);
    std::cout << "Result: ";
    for (int n : nums3) std::cout << n << " ";
    std::cout << "\n";
    
    // 5. Template Strategy
    std::cout << "\n5. Template Strategy:\n";
    GenericSorter<StdSortPolicy> stdSorter;
    GenericSorter<StableSortPolicy> stableSorter;
    
    auto nums4 = numbers;
    stdSorter.sort(nums4);
    std::cout << "std::sort result: ";
    for (int n : nums4) std::cout << n << " ";
    std::cout << "\n";
    
    auto nums5 = numbers;
    stableSorter.sort(nums5);
    std::cout << "stable_sort result: ";
    for (int n : nums5) std::cout << n << " ";
    std::cout << "\n";
}


#include <iostream>
#include <memory>
#include <vector>
#include <stack>
#include <queue>
#include <functional>
#include <chrono>
#include <thread>

// ========== BASIC COMMAND ==========
class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
    virtual std::string getDescription() const = 0;
};

// Receiver
class TextEditor {
private:
    std::string text;
    int cursorPosition;
    
public:
    TextEditor() : text(""), cursorPosition(0) {}
    
    void insert(const std::string& str) {
        text.insert(cursorPosition, str);
        cursorPosition += str.length();
        std::cout << "Inserted: \"" << str << "\"\n";
    }
    
    void deleteChars(int count) {
        if (count > cursorPosition) count = cursorPosition;
        if (count > 0) {
            text.erase(cursorPosition - count, count);
            cursorPosition -= count;
            std::cout << "Deleted " << count << " characters\n";
        }
    }
    
    void moveCursor(int offset) {
        int newPosition = cursorPosition + offset;
        if (newPosition >= 0 && newPosition <= text.length()) {
            cursorPosition = newPosition;
            std::cout << "Cursor moved to position " << cursorPosition << "\n";
        }
    }
    
    void setText(const std::string& newText) {
        text = newText;
        cursorPosition = text.length();
    }
    
    std::string getText() const {
        return text;
    }
    
    int getCursorPosition() const {
        return cursorPosition;
    }
    
    void display() const {
        std::cout << "Text: \"" << text << "\"\n";
        std::cout << "Cursor: " << std::string(cursorPosition, ' ') << "^\n";
    }
};

// Concrete Commands
class InsertCommand : public Command {
private:
    TextEditor& editor;
    std::string textToInsert;
    bool executed;
    
public:
    InsertCommand(TextEditor& editor, const std::string& text)
        : editor(editor), textToInsert(text), executed(false) {}
    
    void execute() override {
        editor.insert(textToInsert);
        executed = true;
    }
    
    void undo() override {
        if (executed) {
            editor.deleteChars(textToInsert.length());
            executed = false;
        }
    }
    
    std::string getDescription() const override {
        return "Insert: \"" + textToInsert + "\"";
    }
};

class DeleteCommand : public Command {
private:
    TextEditor& editor;
    int count;
    std::string deletedText;
    bool executed;
    
public:
    DeleteCommand(TextEditor& editor, int count)
        : editor(editor), count(count), executed(false) {}
    
    void execute() override {
        int pos = editor.getCursorPosition();
        std::string text = editor.getText();
        if (pos >= count) {
            deletedText = text.substr(pos - count, count);
            editor.deleteChars(count);
            executed = true;
        }
    }
    
    void undo() override {
        if (executed) {
            editor.moveCursor(-editor.getCursorPosition());
            editor.insert(deletedText);
            editor.moveCursor(editor.getText().length() - editor.getCursorPosition());
            executed = false;
        }
    }
    
    std::string getDescription() const override {
        return "Delete " + std::to_string(count) + " characters";
    }
};

class MoveCursorCommand : public Command {
private:
    TextEditor& editor;
    int offset;
    int previousPosition;
    bool executed;
    
public:
    MoveCursorCommand(TextEditor& editor, int offset)
        : editor(editor), offset(offset), executed(false) {}
    
    void execute() override {
        previousPosition = editor.getCursorPosition();
        editor.moveCursor(offset);
        executed = true;
    }
    
    void undo() override {
        if (executed) {
            int current = editor.getCursorPosition();
            editor.moveCursor(previousPosition - current);
            executed = false;
        }
    }
    
    std::string getDescription() const override {
        return "Move cursor by " + std::to_string(offset);
    }
};

// Invoker
class CommandManager {
private:
    std::stack<std::unique_ptr<Command>> undoStack;
    std::stack<std::unique_ptr<Command>> redoStack;
    
public:
    void executeCommand(std::unique_ptr<Command> command) {
        command->execute();
        undoStack.push(std::move(command));
        
        // Clear redo stack when new command is executed
        while (!redoStack.empty()) {
            redoStack.pop();
        }
    }
    
    void undo() {
        if (!undoStack.empty()) {
            auto command = std::move(undoStack.top());
            undoStack.pop();
            command->undo();
            redoStack.push(std::move(command));
        } else {
            std::cout << "Nothing to undo\n";
        }
    }
    
    void redo() {
        if (!redoStack.empty()) {
            auto command = std::move(redoStack.top());
            redoStack.pop();
            command->execute();
            undoStack.push(std::move(command));
        } else {
            std::cout << "Nothing to redo\n";
        }
    }
    
    void showHistory() const {
        std::cout << "\nCommand History:\n";
        std::cout << "Undo stack (" << undoStack.size() << " commands):\n";
        
        std::stack<std::unique_ptr<Command>> temp = undoStack;
        int i = 1;
        while (!temp.empty()) {
            std::cout << "  " << i++ << ". " << temp.top()->getDescription() << "\n";
            temp.pop();
        }
    }
};

// ========== MACRO COMMAND ==========
class MacroCommand : public Command {
private:
    std::vector<std::unique_ptr<Command>> commands;
    std::string name;
    
public:
    explicit MacroCommand(const std::string& name) : name(name) {}
    
    void addCommand(std::unique_ptr<Command> command) {
        commands.push_back(std::move(command));
    }
    
    void execute() override {
        std::cout << "Executing macro: " << name << "\n";
        for (auto& command : commands) {
            command->execute();
        }
    }
    
    void undo() override {
        std::cout << "Undoing macro: " << name << "\n";
        for (auto it = commands.rbegin(); it != commands.rend(); ++it) {
            (*it)->undo();
        }
    }
    
    std::string getDescription() const override {
        return "Macro: " + name + " (" + std::to_string(commands.size()) + " commands)";
    }
};

// ========== ASYNC COMMAND ==========
class AsyncCommand : public Command {
private:
    std::function<void()> action;
    std::function<void()> undoAction;
    std::string description;
    
public:
    AsyncCommand(std::function<void()> action, 
                 std::function<void()> undoAction,
                 const std::string& desc)
        : action(std::move(action)), 
          undoAction(std::move(undoAction)), 
          description(desc) {}
    
    void execute() override {
        std::cout << "Starting async command: " << description << "\n";
        std::thread([this]() {
            if (action) {
                action();
            }
            std::cout << "Async command completed: " << description << "\n";
        }).detach();
    }
    
    void undo() override {
        if (undoAction) {
            undoAction();
        }
    }
    
    std::string getDescription() const override {
        return "Async: " + description;
    }
};

// ========== TRANSACTIONAL COMMAND ==========
class Database {
private:
    std::vector<std::string> records;
    
public:
    void addRecord(const std::string& record) {
        records.push_back(record);
        std::cout << "Added record: " << record << "\n";
    }
    
    void removeRecord(const std::string& record) {
        auto it = std::find(records.begin(), records.end(), record);
        if (it != records.end()) {
            records.erase(it);
            std::cout << "Removed record: " << record << "\n";
        }
    }
    
    void displayRecords() const {
        std::cout << "Database records (" << records.size() << "):\n";
        for (const auto& record : records) {
            std::cout << "  - " << record << "\n";
        }
    }
};

class TransactionalCommand : public Command {
protected:
    Database& database;
    bool executed;
    
public:
    TransactionalCommand(Database& db) : database(db), executed(false) {}
    
    virtual ~TransactionalCommand() = default;
    
    bool commit() {
        try {
            execute();
            executed = true;
            return true;
        } catch (const std::exception& e) {
            std::cout << "Transaction failed: " << e.what() << "\n";
            rollback();
            return false;
        }
    }
    
    void rollback() {
        if (executed) {
            undo();
            executed = false;
        }
    }
};

class AddRecordCommand : public TransactionalCommand {
private:
    std::string record;
    
public:
    AddRecordCommand(Database& db, const std::string& record)
        : TransactionalCommand(db), record(record) {}
    
    void execute() override {
        database.addRecord(record);
    }
    
    void undo() override {
        database.removeRecord(record);
    }
    
    std::string getDescription() const override {
        return "Add record: " + record;
    }
};

// ========== COMMAND QUEUE (for Undo/Redo) ==========
class CommandQueue {
private:
    std::queue<std::unique_ptr<Command>> queue;
    std::mutex mutex;
    std::condition_variable cv;
    bool running;
    std::thread worker;
    
    void processCommands() {
        while (running) {
            std::unique_ptr<Command> command;
            
            {
                std::unique_lock<std::mutex> lock(mutex);
                cv.wait(lock, [this]() { 
                    return !queue.empty() || !running; 
                });
                
                if (!running && queue.empty()) break;
                
                if (!queue.empty()) {
                    command = std::move(queue.front());
                    queue.pop();
                }
            }
            
            if (command) {
                command->execute();
            }
        }
    }
    
public:
    CommandQueue() : running(true) {
        worker = std::thread(&CommandQueue::processCommands, this);
    }
    
    ~CommandQueue() {
        {
            std::lock_guard<std::mutex> lock(mutex);
            running = false;
        }
        cv.notify_all();
        if (worker.joinable()) {
            worker.join();
        }
    }
    
    void enqueue(std::unique_ptr<Command> command) {
        std::lock_guard<std::mutex> lock(mutex);
        queue.push(std::move(command));
        cv.notify_one();
    }
    
    size_t size() const {
        std::lock_guard<std::mutex> lock(mutex);
        return queue.size();
    }
};

// ========== COMMAND WITH PARAMETERS ==========
template<typename... Args>
class ParameterizedCommand : public Command {
private:
    std::function<void(Args...)> executeFunc;
    std::function<void(Args...)> undoFunc;
    std::tuple<Args...> parameters;
    std::string description;
    bool executed;
    
public:
    ParameterizedCommand(std::function<void(Args...)> exec,
                        std::function<void(Args...)> undo,
                        const std::string& desc,
                        Args... args)
        : executeFunc(std::move(exec)),
          undoFunc(std::move(undo)),
          parameters(std::make_tuple(args...)),
          description(desc),
          executed(false) {}
    
    void execute() override {
        std::cout << "Executing: " << description << "\n";
        std::apply(executeFunc, parameters);
        executed = true;
    }
    
    void undo() override {
        if (executed && undoFunc) {
            std::cout << "Undoing: " << description << "\n";
            std::apply(undoFunc, parameters);
            executed = false;
        }
    }
    
    std::string getDescription() const override {
        return description;
    }
};

// Helper function to create parameterized commands
template<typename... Args>
std::unique_ptr<Command> makeCommand(std::function<void(Args...)> exec,
                                     std::function<void(Args...)> undo,
                                     const std::string& desc,
                                     Args... args) {
    return std::make_unique<ParameterizedCommand<Args...>>(
        std::move(exec), std::move(undo), desc, args...);
}

void commandExample() {
    std::cout << "\n=== Command Pattern Examples ===\n\n";
    
    // 1. Text Editor with Undo/Redo
    std::cout << "1. Text Editor with Undo/Redo:\n";
    TextEditor editor;
    CommandManager manager;
    
    // Execute some commands
    manager.executeCommand(std::make_unique<InsertCommand>(editor, "Hello"));
    manager.executeCommand(std::make_unique<InsertCommand>(editor, " World"));
    manager.executeCommand(std::make_unique<MoveCursorCommand>(editor, -6));
    manager.executeCommand(std::make_unique<InsertCommand>(editor, "Beautiful "));
    
    editor.display();
    manager.showHistory();
    
    // Undo
    std::cout << "\nUndoing last command:\n";
    manager.undo();
    editor.display();
    
    // Redo
    std::cout << "\nRedoing:\n";
    manager.redo();
    editor.display();
    
    // Undo multiple times
    std::cout << "\nUndoing all commands:\n";
    manager.undo();
    manager.undo();
    manager.undo();
    editor.display();
    
    // 2. Macro Command
    std::cout << "\n2. Macro Command:\n";
    auto macro = std::make_unique<MacroCommand>("Format Text");
    macro->addCommand(std::make_unique<InsertCommand>(editor, "\n"));
    macro->addCommand(std::make_unique<InsertCommand>(editor, "=== Section ===\n"));
    macro->addCommand(std::make_unique<InsertCommand>(editor, "Content here...\n"));
    
    manager.executeCommand(std::move(macro));
    editor.display();
    
    // Undo macro
    std::cout << "\nUndoing macro:\n";
    manager.undo();
    editor.display();
    
    // 3. Async Command
    std::cout << "\n3. Async Command:\n";
    auto asyncCmd = std::make_unique<AsyncCommand>(
        []() {
            std::cout << "Async task started...\n";
            std::this_thread::sleep_for(std::chrono::seconds(1));
            std::cout << "Async task completed\n";
        },
        []() {
            std::cout << "Undoing async task\n";
        },
        "Background Processing"
    );
    
    asyncCmd->execute();
    std::this_thread::sleep_for(std::chrono::milliseconds(100)); // Let async start
    
    // 4. Transactional Commands
    std::cout << "\n4. Transactional Commands:\n";
    Database db;
    
    auto tx1 = std::make_unique<AddRecordCommand>(db, "Record 1");
    auto tx2 = std::make_unique<AddRecordCommand>(db, "Record 2");
    auto tx3 = std::make_unique<AddRecordCommand>(db, "Record 3");
    
    if (static_cast<TransactionalCommand*>(tx1.get())->commit()) {
        std::cout << "Transaction 1 committed\n";
    }
    
    if (static_cast<TransactionalCommand*>(tx2.get())->commit()) {
        std::cout << "Transaction 2 committed\n";
    }
    
    db.displayRecords();
    
    // Rollback transaction 2
    std::cout << "\nRolling back transaction 2:\n";
    static_cast<TransactionalCommand*>(tx2.get())->rollback();
    db.displayRecords();
    
    // 5. Command Queue
    std::cout << "\n5. Command Queue (Processing):\n";
    CommandQueue cmdQueue;
    
    for (int i = 0; i < 5; ++i) {
        cmdQueue.enqueue(std::make_unique<AsyncCommand>(
            [i]() {
                std::cout << "Processing task " << i << "...\n";
                std::this_thread::sleep_for(std::chrono::milliseconds(100));
                std::cout << "Task " << i << " completed\n";
            },
            []() {},
            "Task " + std::to_string(i)
        ));
    }
    
    std::cout << "Queue size: " << cmdQueue.size() << "\n";
    std::this_thread::sleep_for(std::chrono::seconds(1)); // Let queue process
    
    // 6. Parameterized Command
    std::cout << "\n6. Parameterized Command:\n";
    auto paramCmd = makeCommand<int, std::string>(
        [](int id, const std::string& name) {
            std::cout << "Creating user: ID=" << id << ", Name=" << name << "\n";
        },
        [](int id, const std::string& name) {
            std::cout << "Deleting user: ID=" << id << ", Name=" << name << "\n";
        },
        "Create User",
        1001, "John Doe"
    );
    
    paramCmd->execute();
    paramCmd->undo();
}


#include <iostream>
#include <memory>
#include <vector>
#include <string>
#include <variant>
#include <type_traits>

// ========== CLASSIC VISITOR ==========
class Circle;
class Square;
class Triangle;

class ShapeVisitor {
public:
    virtual ~ShapeVisitor() = default;
    virtual void visit(Circle& circle) = 0;
    virtual void visit(Square& square) = 0;
    virtual void visit(Triangle& triangle) = 0;
};

class Shape {
public:
    virtual ~Shape() = default;
    virtual void accept(ShapeVisitor& visitor) = 0;
    virtual std::string getName() const = 0;
};

class Circle : public Shape {
private:
    double radius;
    
public:
    explicit Circle(double radius) : radius(radius) {}
    
    void accept(ShapeVisitor& visitor) override {
        visitor.visit(*this);
    }
    
    std::string getName() const override {
        return "Circle";
    }
    
    double getRadius() const {
        return radius;
    }
    
    double getArea() const {
        return 3.14159 * radius * radius;
    }
};

class Square : public Shape {
private:
    double side;
    
public:
    explicit Square(double side) : side(side) {}
    
    void accept(ShapeVisitor& visitor) override {
        visitor.visit(*this);
    }
    
    std::string getName() const override {
        return "Square";
    }
    
    double getSide() const {
        return side;
    }
    
    double getArea() const {
        return side * side;
    }
};

class Triangle : public Shape {
private:
    double base;
    double height;
    
public:
    Triangle(double base, double height) : base(base), height(height) {}
    
    void accept(ShapeVisitor& visitor) override {
        visitor.visit(*this);
    }
    
    std::string getName() const override {
        return "Triangle";
    }
    
    double getBase() const {
        return base;
    }
    
    double getHeight() const {
        return height;
    }
    
    double getArea() const {
        return 0.5 * base * height;
    }
};

// Concrete Visitors
class AreaCalculator : public ShapeVisitor {
private:
    double totalArea;
    
public:
    AreaCalculator() : totalArea(0) {}
    
    void visit(Circle& circle) override {
        double area = circle.getArea();
        std::cout << "Circle area: " << area << "\n";
        totalArea += area;
    }
    
    void visit(Square& square) override {
        double area = square.getArea();
        std::cout << "Square area: " << area << "\n";
        totalArea += area;
    }
    
    void visit(Triangle& triangle) override {
        double area = triangle.getArea();
        std::cout << "Triangle area: " << area << "\n";
        totalArea += area;
    }
    
    double getTotalArea() const {
        return totalArea;
    }
};

class PerimeterCalculator : public ShapeVisitor {
private:
    double totalPerimeter;
    
public:
    PerimeterCalculator() : totalPerimeter(0) {}
    
    void visit(Circle& circle) override {
        double perimeter = 2 * 3.14159 * circle.getRadius();
        std::cout << "Circle perimeter: " << perimeter << "\n";
        totalPerimeter += perimeter;
    }
    
    void visit(Square& square) override {
        double perimeter = 4 * square.getSide();
        std::cout << "Square perimeter: " << perimeter << "\n";
        totalPerimeter += perimeter;
    }
    
    void visit(Triangle& triangle) override {
        // For simplicity, assume isosceles triangle
        double side = std::sqrt(triangle.getBase() * triangle.getBase() / 4 + 
                               triangle.getHeight() * triangle.getHeight());
        double perimeter = triangle.getBase() + 2 * side;
        std::cout << "Triangle perimeter: " << perimeter << "\n";
        totalPerimeter += perimeter;
    }
    
    double getTotalPerimeter() const {
        return totalPerimeter;
    }
};

class ShapePrinter : public ShapeVisitor {
public:
    void visit(Circle& circle) override {
        std::cout << "Visiting Circle with radius " << circle.getRadius() << "\n";
    }
    
    void visit(Square& square) override {
        std::cout << "Visiting Square with side " << square.getSide() << "\n";
    }
    
    void visit(Triangle& triangle) override {
        std::cout << "Visiting Triangle with base " << triangle.getBase() 
                  << " and height " << triangle.getHeight() << "\n";
    }
};

// ========== VISITOR WITH RETURN VALUES ==========
template<typename ReturnType>
class GenericVisitor {
public:
    virtual ~GenericVisitor() = default;
    virtual ReturnType visit(Circle& circle) = 0;
    virtual ReturnType visit(Square& square) = 0;
    virtual ReturnType visit(Triangle& triangle) = 0;
};

class JSONExportVisitor : public GenericVisitor<std::string> {
public:
    std::string visit(Circle& circle) override {
        return "{ \"type\": \"circle\", \"radius\": " + 
               std::to_string(circle.getRadius()) + ", \"area\": " +
               std::to_string(circle.getArea()) + " }";
    }
    
    std::string visit(Square& square) override {
        return "{ \"type\": \"square\", \"side\": " + 
               std::to_string(square.getSide()) + ", \"area\": " +
               std::to_string(square.getArea()) + " }";
    }
    
    std::string visit(Triangle& triangle) override {
        return "{ \"type\": \"triangle\", \"base\": " + 
               std::to_string(triangle.getBase()) + ", \"height\": " +
               std::to_string(triangle.getHeight()) + ", \"area\": " +
               std::to_string(triangle.getArea()) + " }";
    }
};

// ========== MODERN C++ VISITOR WITH STD::VARIANT ==========
using ShapeVariant = std::variant<Circle, Square, Triangle>;

// Visitor for std::variant
class VariantVisitor {
public:
    void operator()(Circle& circle) {
        std::cout << "Variant visiting Circle: radius=" << circle.getRadius() << "\n";
    }
    
    void operator()(Square& square) {
        std::cout << "Variant visiting Square: side=" << square.getSide() << "\n";
    }
    
    void operator()(Triangle& triangle) {
        std::cout << "Variant visiting Triangle: base=" << triangle.getBase() 
                  << ", height=" << triangle.getHeight() << "\n";
    }
};

// Generic variant visitor with return type
template<typename... Ts>
struct VariantVisitorTemplate : Ts... {
    using Ts::operator()...;
};

template<typename... Ts>
VariantVisitorTemplate(Ts...) -> VariantVisitorTemplate<Ts...>;

// ========== VISITOR FOR ABSTRACT SYNTAX TREE (AST) ==========
class NumberExpr;
class BinaryExpr;
class VariableExpr;

class ExprVisitor {
public:
    virtual ~ExprVisitor() = default;
    virtual void visit(NumberExpr& expr) = 0;
    virtual void visit(BinaryExpr& expr) = 0;
    virtual void visit(VariableExpr& expr) = 0;
};

class Expr {
public:
    virtual ~Expr() = default;
    virtual void accept(ExprVisitor& visitor) = 0;
};

class NumberExpr : public Expr {
private:
    double value;
    
public:
    explicit NumberExpr(double value) : value(value) {}
    
    void accept(ExprVisitor& visitor) override {
        visitor.visit(*this);
    }
    
    double getValue() const {
        return value;
    }
};

class BinaryExpr : public Expr {
public:
    enum class Op { ADD, SUB, MUL, DIV };
    
private:
    Op op;
    std::unique_ptr<Expr> left;
    std::unique_ptr<Expr> right;
    
public:
    BinaryExpr(Op op, std::unique_ptr<Expr> left, std::unique_ptr<Expr> right)
        : op(op), left(std::move(left)), right(std::move(right)) {}
    
    void accept(ExprVisitor& visitor) override {
        visitor.visit(*this);
    }
    
    Op getOp() const {
        return op;
    }
    
    Expr* getLeft() const {
        return left.get();
    }
    
    Expr* getRight() const {
        return right.get();
    }
    
    std::string opToString() const {
        switch (op) {
            case Op::ADD: return "+";
            case Op::SUB: return "-";
            case Op::MUL: return "*";
            case Op::DIV: return "/";
            default: return "?";
        }
    }
};

class VariableExpr : public Expr {
private:
    std::string name;
    
public:
    explicit VariableExpr(const std::string& name) : name(name) {}
    
    void accept(ExprVisitor& visitor) override {
        visitor.visit(*this);
    }
    
    std::string getName() const {
        return name;
    }
};

class EvalVisitor : public ExprVisitor {
private:
    std::unordered_map<std::string, double> variables;
    double result;
    
public:
    EvalVisitor() : result(0) {}
    
    void setVariable(const std::string& name, double value) {
        variables[name] = value;
    }
    
    void visit(NumberExpr& expr) override {
        result = expr.getValue();
    }
    
    void visit(BinaryExpr& expr) override {
        // Evaluate left
        EvalVisitor leftVisitor = *this;
        expr.getLeft()->accept(leftVisitor);
        double leftResult = leftVisitor.getResult();
        
        // Evaluate right
        EvalVisitor rightVisitor = *this;
        expr.getRight()->accept(rightVisitor);
        double rightResult = rightVisitor.getResult();
        
        // Apply operation
        switch (expr.getOp()) {
            case BinaryExpr::Op::ADD:
                result = leftResult + rightResult;
                break;
            case BinaryExpr::Op::SUB:
                result = leftResult - rightResult;
                break;
            case BinaryExpr::Op::MUL:
                result = leftResult * rightResult;
                break;
            case BinaryExpr::Op::DIV:
                if (rightResult == 0) throw std::runtime_error("Division by zero");
                result = leftResult / rightResult;
                break;
        }
    }
    
    void visit(VariableExpr& expr) override {
        auto it = variables.find(expr.getName());
        if (it != variables.end()) {
            result = it->second;
        } else {
            throw std::runtime_error("Undefined variable: " + expr.getName());
        }
    }
    
    double getResult() const {
        return result;
    }
};

class PrintVisitor : public ExprVisitor {
private:
    std::string output;
    
public:
    void visit(NumberExpr& expr) override {
        output = std::to_string(expr.getValue());
    }
    
    void visit(BinaryExpr& expr) override {
        PrintVisitor leftVisitor, rightVisitor;
        expr.getLeft()->accept(leftVisitor);
        expr.getRight()->accept(rightVisitor);
        
        output = "(" + leftVisitor.getOutput() + " " + 
                 expr.opToString() + " " + 
                 rightVisitor.getOutput() + ")";
    }
    
    void visit(VariableExpr& expr) override {
        output = expr.getName();
    }
    
    std::string getOutput() const {
        return output;
    }
};

// ========== VISITOR WITH DOUBLE DISPATCH ==========
class DocumentElement;
class ParagraphElement;
class ImageElement;
class TableElement;

class DocumentVisitor {
public:
    virtual ~DocumentVisitor() = default;
    virtual void visit(ParagraphElement& element) = 0;
    virtual void visit(ImageElement& element) = 0;
    virtual void visit(TableElement& element) = 0;
};

class DocumentElement {
public:
    virtual ~DocumentElement() = default;
    virtual void accept(DocumentVisitor& visitor) = 0;
    virtual void render() = 0;
};

class ParagraphElement : public DocumentElement {
private:
    std::string text;
    
public:
    explicit ParagraphElement(const std::string& text) : text(text) {}
    
    void accept(DocumentVisitor& visitor) override {
        visitor.visit(*this);
    }
    
    void render() override {
        std::cout << "Paragraph: " << text << "\n";
    }
    
    std::string getText() const {
        return text;
    }
    
    void setText(const std::string& newText) {
        text = newText;
    }
};

class ImageElement : public DocumentElement {
private:
    std::string src;
    int width, height;
    
public:
    ImageElement(const std::string& src, int width, int height)
        : src(src), width(width), height(height) {}
    
    void accept(DocumentVisitor& visitor) override {
        visitor.visit(*this);
    }
    
    void render() override {
        std::cout << "Image: " << src << " (" << width << "x" << height << ")\n";
    }
    
    std::string getSrc() const {
        return src;
    }
    
    std::pair<int, int> getDimensions() const {
        return {width, height};
    }
};

class TableElement : public DocumentElement {
private:
    int rows, cols;
    
public:
    TableElement(int rows, int cols) : rows(rows), cols(cols) {}
    
    void accept(DocumentVisitor& visitor) override {
        visitor.visit(*this);
    }
    
    void render() override {
        std::cout << "Table: " << rows << "x" << cols << "\n";
    }
    
    std::pair<int, int> getSize() const {
        return {rows, cols};
    }
};

class WordExportVisitor : public DocumentVisitor {
public:
    void visit(ParagraphElement& element) override {
        std::cout << "Exporting paragraph to Word: \"" 
                  << element.getText() << "\"\n";
    }
    
    void visit(ImageElement& element) override {
        auto [width, height] = element.getDimensions();
        std::cout << "Exporting image to Word: " << element.getSrc() 
                  << " (" << width << "x" << height << ")\n";
    }
    
    void visit(TableElement& element) override {
        auto [rows, cols] = element.getSize();
        std::cout << "Exporting table to Word: " << rows << "x" << cols << "\n";
    }
};

class HTMLExportVisitor : public DocumentVisitor {
public:
    void visit(ParagraphElement& element) override {
        std::cout << "<p>" << element.getText() << "</p>\n";
    }
    
    void visit(ImageElement& element) override {
        auto [width, height] = element.getDimensions();
        std::cout << "<img src=\"" << element.getSrc() 
                  << "\" width=\"" << width 
                  << "\" height=\"" << height << "\">\n";
    }
    
    void visit(TableElement& element) override {
        auto [rows, cols] = element.getSize();
        std::cout << "<table>\n";
        for (int i = 0; i < rows; ++i) {
            std::cout << "  <tr>\n";
            for (int j = 0; j < cols; ++j) {
                std::cout << "    <td>Cell " << i << "," << j << "</td>\n";
            }
            std::cout << "  </tr>\n";
        }
        std::cout << "</table>\n";
    }
};

void visitorExample() {
    std::cout << "\n=== Visitor Pattern Examples ===\n\n";
    
    // 1. Classic Visitor Pattern
    std::cout << "1. Classic Visitor Pattern (Shapes):\n";
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(5.0));
    shapes.push_back(std::make_unique<Square>(4.0));
    shapes.push_back(std::make_unique<Triangle>(3.0, 6.0));
    
    AreaCalculator areaVisitor;
    PerimeterCalculator perimeterVisitor;
    ShapePrinter printer;
    
    for (const auto& shape : shapes) {
        shape->accept(areaVisitor);
    }
    std::cout << "Total area: " << areaVisitor.getTotalArea() << "\n";
    
    std::cout << "\n";
    for (const auto& shape : shapes) {
        shape->accept(perimeterVisitor);
    }
    std::cout << "Total perimeter: " << perimeterVisitor.getTotalPerimeter() << "\n";
    
    std::cout << "\nPrinting shapes:\n";
    for (const auto& shape : shapes) {
        shape->accept(printer);
    }
    
    // 2. Visitor with Return Values
    std::cout << "\n2. Visitor with Return Values (JSON Export):\n";
    JSONExportVisitor jsonVisitor;
    
    for (const auto& shape : shapes) {
        // Note: Need dynamic_cast or redesign for return values
        if (auto circle = dynamic_cast<Circle*>(shape.get())) {
            std::cout << jsonVisitor.visit(*circle) << "\n";
        } else if (auto square = dynamic_cast<Square*>(shape.get())) {
            std::cout << jsonVisitor.visit(*square) << "\n";
        } else if (auto triangle = dynamic_cast<Triangle*>(shape.get())) {
            std::cout << jsonVisitor.visit(*triangle) << "\n";
        }
    }
    
    // 3. Modern Visitor with std::variant
    std::cout << "\n3. Modern Visitor with std::variant:\n";
    std::vector<ShapeVariant> variantShapes;
    variantShapes.emplace_back(Circle(2.0));
    variantShapes.emplace_back(Square(3.0));
    variantShapes.emplace_back(Triangle(4.0, 5.0));
    
    VariantVisitor variantVisitor;
    for (auto& shape : variantShapes) {
        std::visit(variantVisitor, shape);
    }
    
    // Using template visitor with lambdas
    std::cout << "\nUsing template visitor with lambdas:\n";
    auto areaCalc = VariantVisitorTemplate{
        [](Circle& c) { return c.getArea(); },
        [](Square& s) { return s.getArea(); },
        [](Triangle& t) { return t.getArea(); }
    };
    
    double totalVariantArea = 0;
    for (auto& shape : variantShapes) {
        double area = std::visit(areaCalc, shape);
        totalVariantArea += area;
        std::cout << "Area: " << area << "\n";
    }
    std::cout << "Total variant area: " << totalVariantArea << "\n";
    
    // 4. AST Visitor
    std::cout << "\n4. AST Visitor (Expression Evaluation):\n";
    // Build expression: (x + 5) * (y - 3)
    auto expr = std::make_unique<BinaryExpr>(
        BinaryExpr::Op::MUL,
        std::make_unique<BinaryExpr>(
            BinaryExpr::Op::ADD,
            std::make_unique<VariableExpr>("x"),
            std::make_unique<NumberExpr>(5.0)
        ),
        std::make_unique<BinaryExpr>(
            BinaryExpr::Op::SUB,
            std::make_unique<VariableExpr>("y"),
            std::make_unique<NumberExpr>(3.0)
        )
    );
    
    // Print expression
    PrintVisitor printVisitor;
    expr->accept(printVisitor);
    std::cout << "Expression: " << printVisitor.getOutput() << "\n";
    
    // Evaluate expression
    EvalVisitor evalVisitor;
    evalVisitor.setVariable("x", 10.0);
    evalVisitor.setVariable("y", 8.0);
    
    try {
        expr->accept(evalVisitor);
        std::cout << "Result (x=10, y=8): " << evalVisitor.getResult() << "\n";
        
        // Change variable values
        evalVisitor.setVariable("x", 2.0);
        evalVisitor.setVariable("y", 5.0);
        
        // Need new visitor for new evaluation
        EvalVisitor evalVisitor2;
        evalVisitor2.setVariable("x", 2.0);
        evalVisitor2.setVariable("y", 5.0);
        expr->accept(evalVisitor2);
        std::cout << "Result (x=2, y=5): " << evalVisitor2.getResult() << "\n";
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << "\n";
    }
    
    // 5. Document Visitor
    std::cout << "\n5. Document Visitor (Export Formats):\n";
    std::vector<std::unique_ptr<DocumentElement>> document;
    document.push_back(std::make_unique<ParagraphElement>("Welcome to our document"));
    document.push_back(std::make_unique<ImageElement>("photo.jpg", 800, 600));
    document.push_back(std::make_unique<TableElement>(3, 4));
    document.push_back(std::make_unique<ParagraphElement>("Conclusion paragraph"));
    
    // Export to Word
    std::cout << "\nExporting to Word format:\n";
    WordExportVisitor wordExporter;
    for (const auto& element : document) {
        element->accept(wordExporter);
    }
    
    // Export to HTML
    std::cout << "\nExporting to HTML format:\n";
    HTMLExportVisitor htmlExporter;
    for (const auto& element : document) {
        element->accept(htmlExporter);
    }
    
    // Render directly
    std::cout << "\nRendering directly:\n";
    for (const auto& element : document) {
        element->render();
    }
}

#include <iostream>
#include <memory>
#include <string>
#include <map>
#include <functional>

// ========== CLASSIC STATE PATTERN ==========
class TrafficLightState {
public:
    virtual ~TrafficLightState() = default;
    virtual void handle() = 0;
    virtual std::string getName() const = 0;
    virtual TrafficLightState* getNextState() = 0;
};

class RedState : public TrafficLightState {
public:
    void handle() override {
        std::cout << "Traffic Light: RED - STOP!\n";
    }
    
    std::string getName() const override {
        return "RED";
    }
    
    TrafficLightState* getNextState() override;
};

class YellowState : public TrafficLightState {
public:
    void handle() override {
        std::cout << "Traffic Light: YELLOW - PREPARE TO STOP/GO\n";
    }
    
    std::string getName() const override {
        return "YELLOW";
    }
    
    TrafficLightState* getNextState() override;
};

class GreenState : public TrafficLightState {
public:
    void handle() override {
        std::cout << "Traffic Light: GREEN - GO!\n";
    }
    
    std::string getName() const override {
        return "GREEN";
    }
    
    TrafficLightState* getNextState() override;
};

// Context
class TrafficLight {
private:
    std::unique_ptr<TrafficLightState> currentState;
    
public:
    TrafficLight();
    
    void setState(std::unique_ptr<TrafficLightState> newState) {
        std::cout << "Changing state from " 
                  << (currentState ? currentState->getName() : "NONE")
                  << " to " << newState->getName() << "\n";
        currentState = std::move(newState);
    }
    
    void request() {
        if (currentState) {
            currentState->handle();
        }
    }
    
    void change() {
        if (currentState) {
            setState(std::unique_ptr<TrafficLightState>(currentState->getNextState()));
        }
    }
    
    std::string getCurrentState() const {
        return currentState ? currentState->getName() : "NONE";
    }
};

// Forward declarations resolution
TrafficLightState* RedState::getNextState() {
    return new GreenState();
}

TrafficLightState* YellowState::getNextState() {
    return new RedState();
}

TrafficLightState* GreenState::getNextState() {
    return new YellowState();
}

TrafficLight::TrafficLight() {
    // Start with red light
    currentState = std::make_unique<RedState>();
}

// ========== STATE PATTERN WITH ENUMS ==========
class VendingMachine;

class VendingState {
public:
    virtual ~VendingState() = default;
    virtual void insertMoney(VendingMachine& machine, int amount) = 0;
    virtual void selectProduct(VendingMachine& machine, int productId) = 0;
    virtual void dispenseProduct(VendingMachine& machine) = 0;
    virtual void cancel(VendingMachine& machine) = 0;
    virtual std::string getName() const = 0;
};

class VendingMachine {
private:
    std::unique_ptr<VendingState> currentState;
    int balance;
    int selectedProduct;
    std::map<int, std::pair<std::string, int>> products; // id -> (name, price)
    
public:
    VendingMachine();
    
    void setState(std::unique_ptr<VendingState> newState) {
        currentState = std::move(newState);
        std::cout << "State changed to: " << currentState->getName() << "\n";
    }
    
    void insertMoney(int amount) {
        currentState->insertMoney(*this, amount);
    }
    
    void selectProduct(int productId) {
        currentState->selectProduct(*this, productId);
    }
    
    void dispenseProduct() {
        currentState->dispenseProduct(*this);
    }
    
    void cancel() {
        currentState->cancel(*this);
    }
    
    // Getters and setters
    int getBalance() const { return balance; }
    void setBalance(int amount) { balance = amount; }
    
    int getSelectedProduct() const { return selectedProduct; }
    void setSelectedProduct(int id) { selectedProduct = id; }
    
    void addProduct(int id, const std::string& name, int price) {
        products[id] = {name, price};
    }
    
    std::pair<std::string, int> getProduct(int id) const {
        auto it = products.find(id);
        if (it != products.end()) {
            return it->second;
        }
        return {"", 0};
    }
    
    void displayProducts() const {
        std::cout << "\nAvailable Products:\n";
        for (const auto& [id, product] : products) {
            std::cout << "  " << id << ". " << product.first 
                      << " - $" << product.second << "\n";
        }
    }
};

class NoMoneyState : public VendingState {
public:
    void insertMoney(VendingMachine& machine, int amount) override {
        std::cout << "Inserted $" << amount << "\n";
        machine.setBalance(amount);
        machine.setState(std::make_unique<HasMoneyState>());
    }
    
    void selectProduct(VendingMachine& machine, int productId) override {
        std::cout << "Please insert money first\n";
    }
    
    void dispenseProduct(VendingMachine& machine) override {
        std::cout << "Please insert money and select a product\n";
    }
    
    void cancel(VendingMachine& machine) override {
        std::cout << "No transaction to cancel\n";
    }
    
    std::string getName() const override {
        return "NoMoneyState";
    }
};

class HasMoneyState : public VendingState {
public:
    void insertMoney(VendingMachine& machine, int amount) override {
        std::cout << "Added $" << amount << " to balance\n";
        machine.setBalance(machine.getBalance() + amount);
    }
    
    void selectProduct(VendingMachine& machine, int productId) override {
        auto product = machine.getProduct(productId);
        if (product.first.empty()) {
            std::cout << "Invalid product selection\n";
            return;
        }
        
        if (machine.getBalance() >= product.second) {
            machine.setSelectedProduct(productId);
            machine.setState(std::make_unique<ProductSelectedState>());
            std::cout << "Selected: " << product.first << "\n";
        } else {
            std::cout << "Insufficient funds. Need $" << product.second 
                      << ", have $" << machine.getBalance() << "\n";
        }
    }
    
    void dispenseProduct(VendingMachine& machine) override {
        std::cout << "Please select a product first\n";
    }
    
    void cancel(VendingMachine& machine) override {
        std::cout << "Transaction cancelled. Refunding $" 
                  << machine.getBalance() << "\n";
        machine.setBalance(0);
        machine.setState(std::make_unique<NoMoneyState>());
    }
    
    std::string getName() const override {
        return "HasMoneyState";
    }
};

class ProductSelectedState : public VendingState {
public:
    void insertMoney(VendingMachine& machine, int amount) override {
        std::cout << "Cannot insert money after product selection\n";
    }
    
    void selectProduct(VendingMachine& machine, int productId) override {
        std::cout << "Product already selected\n";
    }
    
    void dispenseProduct(VendingMachine& machine) override {
        auto product = machine.getProduct(machine.getSelectedProduct());
        int price = product.second;
        int balance = machine.getBalance();
        
        if (balance >= price) {
            std::cout << "Dispensing: " << product.first << "\n";
            machine.setBalance(balance - price);
            
            if (machine.getBalance() > 0) {
                std::cout << "Returning change: $" << machine.getBalance() << "\n";
                machine.setBalance(0);
            }
            
            machine.setState(std::make_unique<NoMoneyState>());
        } else {
            std::cout << "Insufficient funds\n";
        }
    }
    
    void cancel(VendingMachine& machine) override {
        std::cout << "Transaction cancelled. Refunding $" 
                  << machine.getBalance() << "\n";
        machine.setBalance(0);
        machine.setSelectedProduct(-1);
        machine.setState(std::make_unique<NoMoneyState>());
    }
    
    std::string getName() const override {
        return "ProductSelectedState";
    }
};

VendingMachine::VendingMachine() 
    : balance(0), selectedProduct(-1) {
    currentState = std::make_unique<NoMoneyState>();
    
    // Add some products
    addProduct(1, "Cola", 150);
    addProduct(2, "Chips", 100);
    addProduct(3, "Candy", 75);
    addProduct(4, "Water", 125);
}

// ========== MODERN STATE PATTERN WITH STD::VARIANT ==========
struct ConnectingState {
    int retryCount;
    
    void enter() {
        std::cout << "Entering ConnectingState (retry: " << retryCount << ")\n";
    }
    
    void exit() {
        std::cout << "Exiting ConnectingState\n";
    }
};

struct ConnectedState {
    std::string connectionId;
    
    void enter() {
        std::cout << "Entering ConnectedState (id: " << connectionId << ")\n";
    }
    
    void exit() {
        std::cout << "Exiting ConnectedState\n";
    }
};

struct DisconnectedState {
    std::string reason;
    
    void enter() {
        std::cout << "Entering DisconnectedState (reason: " << reason << ")\n";
    }
    
    void exit() {
        std::cout << "Exiting DisconnectedState\n";
    }
};

using NetworkState = std::variant<ConnectingState, ConnectedState, DisconnectedState>;

class NetworkConnection {
private:
    NetworkState currentState;
    
    template<typename NewState, typename... Args>
    void transitionTo(Args&&... args) {
        std::visit([](auto& state) { state.exit(); }, currentState);
        
        NewState newState{std::forward<Args>(args)...};
        newState.enter();
        
        currentState = std::move(newState);
    }
    
public:
    NetworkConnection() {
        currentState = DisconnectedState{"Initial"};
        std::visit([](auto& state) { state.enter(); }, currentState);
    }
    
    void connect() {
        std::visit([this](auto& state) {
            using T = std::decay_t<decltype(state)>;
            
            if constexpr (std::is_same_v<T, DisconnectedState>) {
                std::cout << "Initiating connection...\n";
                transitionTo<ConnectingState>(0);
            } else if constexpr (std::is_same_v<T, ConnectingState>) {
                std::cout << "Already connecting...\n";
            } else if constexpr (std::is_same_v<T, ConnectedState>) {
                std::cout << "Already connected\n";
            }
        }, currentState);
    }
    
    void connectionEstablished(const std::string& connectionId) {
        std::visit([this, &connectionId](auto& state) {
            using T = std::decay_t<decltype(state)>;
            
            if constexpr (std::is_same_v<T, ConnectingState>) {
                std::cout << "Connection established: " << connectionId << "\n";
                transitionTo<ConnectedState>(connectionId);
            }
        }, currentState);
    }
    
    void disconnect(const std::string& reason = "User request") {
        std::visit([this, &reason](auto& state) {
            using T = std::decay_t<decltype(state)>;
            
            if constexpr (std::is_same_v<T, ConnectedState>) {
                std::cout << "Disconnecting...\n";
                transitionTo<DisconnectedState>(reason);
            } else if constexpr (std::is_same_v<T, ConnectingState>) {
                std::cout << "Cancelling connection attempt...\n";
                transitionTo<DisconnectedState>("Connection cancelled");
            }
        }, currentState);
    }
    
    void sendData(const std::string& data) {
        std::visit([&data](auto& state) {
            using T = std::decay_t<decltype(state)>;
            
            if constexpr (std::is_same_v<T, ConnectedState>) {
                std::cout << "Sending data over connection " 
                          << state.connectionId << ": " << data << "\n";
            } else {
                std::cout << "Cannot send data - not connected\n";
            }
        }, currentState);
    }
    
    std::string getStateName() const {
        return std::visit([](auto& state) -> std::string {
            using T = std::decay_t<decltype(state)>;
            
            if constexpr (std::is_same_v<T, ConnectingState>) {
                return "Connecting";
            } else if constexpr (std::is_same_v<T, ConnectedState>) {
                return "Connected";
            } else if constexpr (std::is_same_v<T, DisconnectedState>) {
                return "Disconnected";
            }
        }, currentState);
    }
};

// ========== STATE PATTERN WITH FUNCTIONAL APPROACH ==========
class Order {
public:
    enum class State { NEW, PROCESSING, SHIPPED, DELIVERED, CANCELLED };
    
    using StateHandler = std::function<void(Order&)>;
    
private:
    State currentState;
    std::string orderId;
    std::map<State, StateHandler> stateHandlers;
    
public:
    Order(const std::string& id) : orderId(id), currentState(State::NEW) {
        // Define state handlers
        stateHandlers[State::NEW] = [](Order& order) {
            std::cout << "Order " << order.orderId << " is NEW\n";
        };
        
        stateHandlers[State::PROCESSING] = [](Order& order) {
            std::cout << "Order " << order.orderId << " is PROCESSING\n";
        };
        
        stateHandlers[State::SHIPPED] = [](Order& order) {
            std::cout << "Order " << order.orderId << " has been SHIPPED\n";
        };
        
        stateHandlers[State::DELIVERED] = [](Order& order) {
            std::cout << "Order " << order.orderId << " has been DELIVERED\n";
        };
        
        stateHandlers[State::CANCELLED] = [](Order& order) {
            std::cout << "Order " << order.orderId << " has been CANCELLED\n";
        };
        
        // Execute initial state handler
        executeCurrentState();
    }
    
    void setState(State newState) {
        if (isValidTransition(currentState, newState)) {
            currentState = newState;
            executeCurrentState();
        } else {
            std::cout << "Invalid state transition from " 
                      << stateToString(currentState) << " to "
                      << stateToString(newState) << "\n";
        }
    }
    
    void process() {
        switch (currentState) {
            case State::NEW:
                setState(State::PROCESSING);
                break;
            case State::PROCESSING:
                setState(State::SHIPPED);
                break;
            case State::SHIPPED:
                setState(State::DELIVERED);
                break;
            default:
                std::cout << "Cannot process order in state: " 
                          << stateToString(currentState) << "\n";
        }
    }
    
    void cancel() {
        if (currentState == State::NEW || currentState == State::PROCESSING) {
            setState(State::CANCELLED);
        } else {
            std::cout << "Cannot cancel order in state: " 
                      << stateToString(currentState) << "\n";
        }
    }
    
    std::string getState() const {
        return stateToString(currentState);
    }
    
private:
    void executeCurrentState() {
        auto it = stateHandlers.find(currentState);
        if (it != stateHandlers.end()) {
            it->second(*this);
        }
    }
    
    static bool isValidTransition(State from, State to) {
        static std::map<State, std::vector<State>> validTransitions = {
            {State::NEW, {State::PROCESSING, State::CANCELLED}},
            {State::PROCESSING, {State::SHIPPED, State::CANCELLED}},
            {State::SHIPPED, {State::DELIVERED}},
            {State::DELIVERED, {}},
            {State::CANCELLED, {}}
        };
        
        const auto& transitions = validTransitions[from];
        return std::find(transitions.begin(), transitions.end(), to) 
               != transitions.end();
    }
    
    static std::string stateToString(State state) {
        switch (state) {
            case State::NEW: return "NEW";
            case State::PROCESSING: return "PROCESSING";
            case State::SHIPPED: return "SHIPPED";
            case State::DELIVERED: return "DELIVERED";
            case State::CANCELLED: return "CANCELLED";
            default: return "UNKNOWN";
        }
    }
};

void stateExample() {
    std::cout << "\n=== State Pattern Examples ===\n\n";
    
    // 1. Traffic Light State
    std::cout << "1. Traffic Light State Machine:\n";
    TrafficLight trafficLight;
    
    for (int i = 0; i < 6; ++i) {
        std::cout << "\nCycle " << i + 1 << ":\n";
        trafficLight.request();
        trafficLight.change();
    }
    
    // 2. Vending Machine State
    std::cout << "\n2. Vending Machine State Machine:\n";
    VendingMachine vendingMachine;
    vendingMachine.displayProducts();
    
    // Test scenarios
    std::cout << "\nScenario 1: Normal purchase\n";
    vendingMachine.insertMoney(200);      // Insert $2.00
    vendingMachine.selectProduct(1);      // Select Cola ($1.50)
    vendingMachine.dispenseProduct();     // Dispense
    
    std::cout << "\nScenario 2: Insufficient funds\n";
    vendingMachine.insertMoney(50);       // Insert $0.50
    vendingMachine.selectProduct(2);      // Try to buy Chips ($1.00)
    vendingMachine.insertMoney(75);       // Add more money
    vendingMachine.selectProduct(2);      // Now it works
    vendingMachine.dispenseProduct();     // Dispense
    
    std::cout << "\nScenario 3: Cancellation\n";
    vendingMachine.insertMoney(100);
    vendingMachine.cancel();
    
    // 3. Modern State with std::variant
    std::cout << "\n3. Modern State with std::variant (Network Connection):\n";
    NetworkConnection connection;
    
    std::cout << "Current state: " << connection.getStateName() << "\n";
    
    connection.connect();
    connection.connectionEstablished("conn-12345");
    connection.sendData("Hello Server!");
    connection.disconnect("Test complete");
    
    // Try to send data while disconnected
    connection.sendData("This should fail");
    
    // 4. Functional State Pattern
    std::cout << "\n4. Functional State Pattern (Order Processing):\n";
    Order order("ORD-001");
    
    order.process();  // NEW -> PROCESSING
    order.process();  // PROCESSING -> SHIPPED
    order.process();  // SHIPPED -> DELIVERED
    order.process();  // Should fail
    
    std::cout << "\nNew order with cancellation:\n";
    Order order2("ORD-002");
    order2.cancel();  // NEW -> CANCELLED
    order2.process(); // Should fail
    
    std::cout << "\nInvalid transition test:\n";
    Order order3("ORD-003");
    order3.process();  // NEW -> PROCESSING
    order3.process();  // PROCESSING -> SHIPPED
    order3.cancel();   // Should fail - cannot cancel shipped order
}


#include <iostream>
#include <memory>
#include <fstream>
#include <mutex>
#include <vector>
#include <stdexcept>

// ========== BASIC RAII CLASSES ==========

// 1. File RAII wrapper
class File {
private:
    std::FILE* file;
    
public:
    // Constructor acquires resource
    explicit File(const char* filename, const char* mode = "r") {
        file = std::fopen(filename, mode);
        if (!file) {
            throw std::runtime_error("Failed to open file");
        }
        std::cout << "File opened: " << filename << "\n";
    }
    
    // Destructor releases resource
    ~File() {
        if (file) {
            std::fclose(file);
            std::cout << "File closed\n";
        }
    }
    
    // Delete copy operations
    File(const File&) = delete;
    File& operator=(const File&) = delete;
    
    // Allow move operations
    File(File&& other) noexcept : file(other.file) {
        other.file = nullptr;
    }
    
    File& operator=(File&& other) noexcept {
        if (this != &other) {
            if (file) std::fclose(file);
            file = other.file;
            other.file = nullptr;
        }
        return *this;
    }
    
    // Resource usage
    void write(const std::string& data) {
        if (file) {
            std::fprintf(file, "%s", data.c_str());
        }
    }
    
    std::string readAll() {
        if (!file) return "";
        
        std::fseek(file, 0, SEEK_END);
        long size = std::ftell(file);
        std::fseek(file, 0, SEEK_SET);
        
        std::string content(size, '\0');
        std::fread(&content[0], 1, size, file);
        return content;
    }
};

// 2. Mutex RAII wrapper (similar to std::lock_guard)
class ScopedLock {
private:
    std::mutex& mutex;
    
public:
    explicit ScopedLock(std::mutex& m) : mutex(m) {
        mutex.lock();
        std::cout << "Mutex locked\n";
    }
    
    ~ScopedLock() {
        mutex.unlock();
        std::cout << "Mutex unlocked\n";
    }
    
    // Delete copy operations
    ScopedLock(const ScopedLock&) = delete;
    ScopedLock& operator=(const ScopedLock&) = delete;
};

// ========== RAII FOR DYNAMIC ARRAYS ==========
template<typename T>
class DynamicArray {
private:
    T* data;
    size_t size;
    
public:
    explicit DynamicArray(size_t n) : size(n) {
        data = new T[n];
        std::cout << "Allocated array of " << n << " elements\n";
    }
    
    ~DynamicArray() {
        delete[] data;
        std::cout << "Deallocated array\n";
    }
    
    // Delete copy operations
    DynamicArray(const DynamicArray&) = delete;
    DynamicArray& operator=(const DynamicArray&) = delete;
    
    // Move operations
    DynamicArray(DynamicArray&& other) noexcept 
        : data(other.data), size(other.size) {
        other.data = nullptr;
        other.size = 0;
    }
    
    DynamicArray& operator=(DynamicArray&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
    
    T& operator[](size_t index) {
        if (index >= size) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }
    
    const T& operator[](size_t index) const {
        if (index >= size) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }
    
    size_t getSize() const {
        return size;
    }
};

// ========== RAII FOR NETWORK CONNECTIONS ==========
class NetworkConnection {
private:
    int socket;
    bool connected;
    
public:
    NetworkConnection(const std::string& host, int port) 
        : socket(-1), connected(false) {
        // Simulate connection
        std::cout << "Connecting to " << host << ":" << port << "\n";
        socket = 42;  // Simulated socket
        connected = true;
        std::cout << "Connected successfully\n";
    }
    
    ~NetworkConnection() {
        if (connected) {
            std::cout << "Closing network connection\n";
            // Simulate close
            socket = -1;
            connected = false;
        }
    }
    
    // Delete copy operations
    NetworkConnection(const NetworkConnection&) = delete;
    NetworkConnection& operator=(const NetworkConnection&) = delete;
    
    // Move operations
    NetworkConnection(NetworkConnection&& other) noexcept 
        : socket(other.socket), connected(other.connected) {
        other.socket = -1;
        other.connected = false;
    }
    
    NetworkConnection& operator=(NetworkConnection&& other) noexcept {
        if (this != &other) {
            if (connected) {
                // Close current connection
            }
            socket = other.socket;
            connected = other.connected;
            other.socket = -1;
            other.connected = false;
        }
        return *this;
    }
    
    void send(const std::string& data) {
        if (connected) {
            std::cout << "Sending data: " << data << "\n";
        } else {
            throw std::runtime_error("Not connected");
        }
    }
    
    std::string receive() {
        if (connected) {
            return "Simulated response";
        }
        throw std::runtime_error("Not connected");
    }
};

// ========== RAII WITH CUSTOM DELETER ==========
template<typename T, typename Deleter>
class UniqueResource {
private:
    T resource;
    Deleter deleter;
    bool owns;
    
public:
    UniqueResource(T res, Deleter del) 
        : resource(res), deleter(del), owns(true) {}
    
    ~UniqueResource() {
        if (owns) {
            deleter(resource);
        }
    }
    
    // Delete copy operations
    UniqueResource(const UniqueResource&) = delete;
    UniqueResource& operator=(const UniqueResource&) = delete;
    
    // Move operations
    UniqueResource(UniqueResource&& other) noexcept 
        : resource(other.resource), deleter(std::move(other.deleter)), owns(other.owns) {
        other.owns = false;
    }
    
    UniqueResource& operator=(UniqueResource&& other) noexcept {
        if (this != &other) {
            if (owns) {
                deleter(resource);
            }
            resource = other.resource;
            deleter = std::move(other.deleter);
            owns = other.owns;
            other.owns = false;
        }
        return *this;
    }
    
    T get() const {
        return resource;
    }
    
    T release() {
        owns = false;
        return resource;
    }
    
    void reset(T newResource = T()) {
        if (owns) {
            deleter(resource);
        }
        resource = newResource;
        owns = true;
    }
};

// ========== RAII FOR TRANSACTIONS ==========
class DatabaseTransaction {
private:
    bool committed;
    
public:
    DatabaseTransaction() : committed(false) {
        std::cout << "Transaction started\n";
    }
    
    ~DatabaseTransaction() {
        if (!committed) {
            std::cout << "Rolling back transaction\n";
            rollback();
        }
    }
    
    void commit() {
        std::cout << "Committing transaction\n";
        committed = true;
    }
    
private:
    void rollback() {
        std::cout << "Performing rollback operations\n";
    }
    
    // Delete copy operations
    DatabaseTransaction(const DatabaseTransaction&) = delete;
    DatabaseTransaction& operator=(const DatabaseTransaction&) = delete;
};

// ========== SCOPE GUARD (Modern RAII) ==========
class ScopeGuard {
private:
    std::function<void()> cleanup;
    
public:
    explicit ScopeGuard(std::function<void()> cleanupFunc) 
        : cleanup(std::move(cleanupFunc)) {}
    
    ~ScopeGuard() {
        if (cleanup) {
            cleanup();
        }
    }
    
    // Delete copy operations
    ScopeGuard(const ScopeGuard&) = delete;
    ScopeGuard& operator=(const ScopeGuard&) = delete;
    
    // Allow move
    ScopeGuard(ScopeGuard&& other) noexcept 
        : cleanup(std::move(other.cleanup)) {
        other.cleanup = nullptr;
    }
    
    ScopeGuard& operator=(ScopeGuard&& other) noexcept {
        if (this != &other) {
            cleanup = std::move(other.cleanup);
            other.cleanup = nullptr;
        }
        return *this;
    }
    
    void dismiss() {
        cleanup = nullptr;
    }
};

// Helper function to create scope guards
template<typename Func>
ScopeGuard makeScopeGuard(Func cleanup) {
    return ScopeGuard(cleanup);
}

void raiiExample() {
    std::cout << "\n=== RAII Idiom Examples ===\n\n";
    
    // 1. File RAII
    std::cout << "1. File RAII:\n";
    try {
        File output("test.txt", "w");
        output.write("Hello, RAII!\n");
        // File automatically closed when output goes out of scope
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << "\n";
    }
    
    // 2. Mutex RAII
    std::cout << "\n2. Mutex RAII:\n";
    std::mutex mtx;
    {
        ScopedLock lock(mtx);
        std::cout << "Critical section\n";
        // Mutex automatically unlocked when lock goes out of scope
    }
    
    // 3. Dynamic Array RAII
    std::cout << "\n3. Dynamic Array RAII:\n";
    {
        DynamicArray<int> arr(10);
        for (size_t i = 0; i < arr.getSize(); ++i) {
            arr[i] = static_cast<int>(i * 2);
        }
        // Array automatically deleted when arr goes out of scope
    }
    
    // 4. Network Connection RAII
    std::cout << "\n4. Network Connection RAII:\n";
    {
        NetworkConnection conn("localhost", 8080);
        conn.send("GET / HTTP/1.1");
        auto response = conn.receive();
        std::cout << "Response: " << response << "\n";
        // Connection automatically closed when conn goes out of scope
    }
    
    // 5. Unique Resource with Custom Deleter
    std::cout << "\n5. Unique Resource with Custom Deleter:\n";
    {
        auto deleter = [](int* p) {
            std::cout << "Custom delete: " << *p << "\n";
            delete p;
        };
        
        UniqueResource<int*, decltype(deleter)> resource(new int(42), deleter);
        std::cout << "Resource value: " << *resource.get() << "\n";
        // Automatically deleted with custom deleter
    }
    
    // 6. Database Transaction RAII
    std::cout << "\n6. Database Transaction RAII:\n";
    try {
        DatabaseTransaction transaction;
        // Do some database operations
        // throw std::runtime_error("Simulated error");
        transaction.commit();  // If not called, auto-rollback in destructor
    } catch (const std::exception& e) {
        std::cout << "Exception: " << e.what() << "\n";
    }
    
    // 7. Scope Guard
    std::cout << "\n7. Scope Guard:\n";
    {
        auto guard = makeScopeGuard([]() {
            std::cout << "Scope guard cleanup\n";
        });
        
        std::cout << "Doing work...\n";
        // guard.dismiss();  // Uncomment to prevent cleanup
    } // Cleanup happens here
    
    // 8. RAII with exception safety
    std::cout << "\n8. RAII with Exception Safety:\n";
    try {
        File file1("file1.txt", "w");
        File file2("file2.txt", "w");
        File file3("file3.txt", "w");
        
        file1.write("Data 1\n");
        file2.write("Data 2\n");
        throw std::runtime_error("Something went wrong!");
        file3.write("Data 3\n");  // Never reached
        
        // All files properly closed even with exception
    } catch (const std::exception& e) {
        std::cout << "Caught exception: " << e.what() << "\n";
    }
}



#include <iostream>
#include <memory>
#include <vector>
#include <string>

// ========== BASIC PIMPL ==========
// Header: widget.h
class Widget {
public:
    Widget();
    ~Widget();
    
    // Copy operations
    Widget(const Widget& other);
    Widget& operator=(const Widget& other);
    
    // Move operations
    Widget(Widget&& other) noexcept;
    Widget& operator=(Widget&& other) noexcept;
    
    void doSomething();
    int getValue() const;
    
private:
    class Impl;  // Forward declaration
    std::unique_ptr<Impl> pImpl;
};

// Implementation: widget.cpp
class Widget::Impl {
private:
    int value;
    std::string name;
    std::vector<int> data;
    
public:
    Impl() : value(0), name("Default") {
        data = {1, 2, 3, 4, 5};
    }
    
    Impl(const Impl& other) 
        : value(other.value), name(other.name), data(other.data) {}
    
    Impl(Impl&& other) noexcept
        : value(other.value), name(std::move(other.name)), 
          data(std::move(other.data)) {
        other.value = 0;
    }
    
    void doSomething() {
        std::cout << "Widget::Impl::doSomething() called\n";
        std::cout << "Name: " << name << ", Value: " << value << "\n";
        std::cout << "Data: ";
        for (int n : data) std::cout << n << " ";
        std::cout << "\n";
    }
    
    int getValue() const {
        return value;
    }
    
    void setValue(int newValue) {
        value = newValue;
    }
    
    void setName(const std::string& newName) {
        name = newName;
    }
};

// Widget implementation
Widget::Widget() : pImpl(std::make_unique<Impl>()) {}

Widget::~Widget() = default;  // Must be in .cpp for unique_ptr<Impl>

Widget::Widget(const Widget& other) 
    : pImpl(other.pImpl ? std::make_unique<Impl>(*other.pImpl) : nullptr) {}

Widget& Widget::operator=(const Widget& other) {
    if (this != &other) {
        if (other.pImpl) {
            pImpl = std::make_unique<Impl>(*other.pImpl);
        } else {
            pImpl.reset();
        }
    }
    return *this;
}

Widget::Widget(Widget&& other) noexcept = default;
Widget& Widget::operator=(Widget&& other) noexcept = default;

void Widget::doSomething() {
    pImpl->doSomething();
}

int Widget::getValue() const {
    return pImpl->getValue();
}

// ========== PIMPL WITH SHARED IMPLEMENTATION ==========
class SharedWidget {
public:
    SharedWidget();
    ~SharedWidget();
    
    // SharedWidget is copyable and movable
    SharedWidget(const SharedWidget&) = default;
    SharedWidget& operator=(const SharedWidget&) = default;
    SharedWidget(SharedWidget&&) = default;
    SharedWidget& operator=(SharedWidget&&) = default;
    
    void operation();
    void setData(const std::string& data);
    std::string getData() const;
    
private:
    struct SharedImpl;
    std::shared_ptr<SharedImpl> pImpl;
};

struct SharedWidget::SharedImpl {
    std::string data;
    std::vector<int> cache;
    int counter;
    
    SharedImpl() : counter(0) {
        cache.resize(100);
    }
    
    void performOperation() {
        std::cout << "SharedImpl::performOperation()\n";
        std::cout << "Data: " << data << ", Counter: " << counter << "\n";
        ++counter;
    }
};

SharedWidget::SharedWidget() 
    : pImpl(std::make_shared<SharedImpl>()) {}

SharedWidget::~SharedWidget() = default;

void SharedWidget::operation() {
    pImpl->performOperation();
}

void SharedWidget::setData(const std::string& data) {
    pImpl->data = data;
}

std::string SharedWidget::getData() const {
    return pImpl->data;
}

// ========== PIMPL WITH TEMPLATES ==========
template<typename T>
class PimplContainer {
public:
    PimplContainer();
    ~PimplContainer();
    
    // Rule of Five
    PimplContainer(const PimplContainer& other);
    PimplContainer& operator=(const PimplContainer& other);
    PimplContainer(PimplContainer&& other) noexcept;
    PimplContainer& operator=(PimplContainer&& other) noexcept;
    
    void add(const T& value);
    void remove(const T& value);
    bool contains(const T& value) const;
    size_t size() const;
    
private:
    class Impl;
    std::unique_ptr<Impl> pImpl;
};

template<typename T>
class PimplContainer<T>::Impl {
private:
    std::vector<T> data;
    
public:
    void add(const T& value) {
        data.push_back(value);
    }
    
    void remove(const T& value) {
        auto it = std::remove(data.begin(), data.end(), value);
        data.erase(it, data.end());
    }
    
    bool contains(const T& value) const {
        return std::find(data.begin(), data.end(), value) != data.end();
    }
    
    size_t size() const {
        return data.size();
    }
    
    std::vector<T> getData() const {
        return data;
    }
};

template<typename T>
PimplContainer<T>::PimplContainer() : pImpl(std::make_unique<Impl>()) {}

template<typename T>
PimplContainer<T>::~PimplContainer() = default;

template<typename T>
PimplContainer<T>::PimplContainer(const PimplContainer& other)
    : pImpl(other.pImpl ? std::make_unique<Impl>(*other.pImpl) : nullptr) {}

template<typename T>
PimplContainer<T>& PimplContainer<T>::operator=(const PimplContainer& other) {
    if (this != &other) {
        pImpl = other.pImpl ? std::make_unique<Impl>(*other.pImpl) : nullptr;
    }
    return *this;
}

template<typename T>
PimplContainer<T>::PimplContainer(PimplContainer&& other) noexcept = default;

template<typename T>
PimplContainer<T>& PimplContainer<T>::operator=(PimplContainer&& other) noexcept = default;

template<typename T>
void PimplContainer<T>::add(const T& value) {
    pImpl->add(value);
}

template<typename T>
void PimplContainer<T>::remove(const T& value) {
    pImpl->remove(value);
}

template<typename T>
bool PimplContainer<T>::contains(const T& value) const {
    return pImpl->contains(value);
}

template<typename T>
size_t PimplContainer<T>::size() const {
    return pImpl->size();
}

// ========== PIMPL WITH INTERFACE ==========
class Drawable {
public:
    virtual ~Drawable() = default;
    virtual void draw() const = 0;
    virtual void resize(double factor) = 0;
};

class Circle : public Drawable {
public:
    Circle(double radius);
    ~Circle() override;
    
    // Delete copy operations (or implement properly)
    Circle(const Circle&) = delete;
    Circle& operator=(const Circle&) = delete;
    
    // Allow move
    Circle(Circle&&) noexcept;
    Circle& operator=(Circle&&) noexcept;
    
    void draw() const override;
    void resize(double factor) override;
    double getArea() const;
    
private:
    class Impl;
    std::unique_ptr<Impl> pImpl;
};

class Circle::Impl {
private:
    double radius;
    
public:
    Impl(double r) : radius(r) {}
    
    void draw() const {
        std::cout << "Drawing circle with radius " << radius << "\n";
    }
    
    void resize(double factor) {
        radius *= factor;
        std::cout << "Circle resized to radius " << radius << "\n";
    }
    
    double getArea() const {
        return 3.14159 * radius * radius;
    }
    
    double getRadius() const {
        return radius;
    }
};

Circle::Circle(double radius) : pImpl(std::make_unique<Impl>(radius)) {}
Circle::~Circle() = default;

Circle::Circle(Circle&& other) noexcept = default;
Circle& Circle::operator=(Circle&& other) noexcept = default;

void Circle::draw() const {
    pImpl->draw();
}

void Circle::resize(double factor) {
    pImpl->resize(factor);
}

double Circle::getArea() const {
    return pImpl->getArea();
}

// ========== PIMPL WITH COMPLEX DEPENDENCIES ==========
class DatabaseConnection {
public:
    DatabaseConnection(const std::string& connectionString);
    ~DatabaseConnection();
    
    // Rule of Five
    DatabaseConnection(const DatabaseConnection&) = delete;
    DatabaseConnection& operator=(const DatabaseConnection&) = delete;
    DatabaseConnection(DatabaseConnection&&) noexcept;
    DatabaseConnection& operator=(DatabaseConnection&&) noexcept;
    
    void connect();
    void disconnect();
    void executeQuery(const std::string& query);
    std::vector<std::string> fetchResults();
    
private:
    class Impl;
    std::unique_ptr<Impl> pImpl;
};

// Simulated database implementation
class DatabaseConnection::Impl {
private:
    std::string connectionString;
    bool connected;
    std::vector<std::string> results;
    
    // Simulated complex dependencies
    struct DatabaseHandle {
        int id;
        std::string version;
    };
    
    std::unique_ptr<DatabaseHandle> dbHandle;
    
public:
    Impl(const std::string& connStr) 
        : connectionString(connStr), connected(false) {}
    
    ~Impl() {
        if (connected) {
            disconnect();
        }
    }
    
    void connect() {
        if (!connected) {
            std::cout << "Connecting to: " << connectionString << "\n";
            dbHandle = std::make_unique<DatabaseHandle>();
            dbHandle->id = 42;
            dbHandle->version = "1.0";
            connected = true;
            std::cout << "Connected successfully\n";
        }
    }
    
    void disconnect() {
        if (connected) {
            std::cout << "Disconnecting from database\n";
            dbHandle.reset();
            connected = false;
        }
    }
    
    void executeQuery(const std::string& query) {
        if (!connected) {
            throw std::runtime_error("Not connected to database");
        }
        
        std::cout << "Executing query: " << query << "\n";
        results.clear();
        
        // Simulate query results
        results.push_back("Result 1 for: " + query);
        results.push_back("Result 2 for: " + query);
        results.push_back("Result 3 for: " + query);
    }
    
    std::vector<std::string> fetchResults() {
        return results;
    }
};

DatabaseConnection::DatabaseConnection(const std::string& connectionString)
    : pImpl(std::make_unique<Impl>(connectionString)) {}

DatabaseConnection::~DatabaseConnection() = default;

DatabaseConnection::DatabaseConnection(DatabaseConnection&& other) noexcept = default;
DatabaseConnection& DatabaseConnection::operator=(DatabaseConnection&& other) noexcept = default;

void DatabaseConnection::connect() {
    pImpl->connect();
}

void DatabaseConnection::disconnect() {
    pImpl->disconnect();
}

void DatabaseConnection::executeQuery(const std::string& query) {
    pImpl->executeQuery(query);
}

std::vector<std::string> DatabaseConnection::fetchResults() {
    return pImpl->fetchResults();
}

void pimplExample() {
    std::cout << "\n=== PIMPL Idiom Examples ===\n\n";
    
    // 1. Basic PIMPL
    std::cout << "1. Basic PIMPL (Widget):\n";
    Widget w1;
    w1.doSomething();
    
    // Copy constructor works
    Widget w2 = w1;
    w2.doSomething();
    
    // Move constructor
    Widget w3 = std::move(w1);
    w3.doSomething();
    
    // 2. Shared PIMPL
    std::cout << "\n2. Shared PIMPL (SharedWidget):\n";
    SharedWidget sw1;
    sw1.setData("First instance");
    sw1.operation();
    
    SharedWidget sw2 = sw1;  // Shares implementation
    sw2.setData("Second instance");
    sw2.operation();
    
    sw1.operation();  // Counter increased by both
    
    // 3. Template PIMPL
    std::cout << "\n3. Template PIMPL (PimplContainer):\n";
    PimplContainer<int> container;
    container.add(1);
    container.add(2);
    container.add(3);
    
    std::cout << "Container size: " << container.size() << "\n";
    std::cout << "Contains 2? " << (container.contains(2) ? "Yes" : "No") << "\n";
    std::cout << "Contains 5? " << (container.contains(5) ? "Yes" : "No") << "\n";
    
    container.remove(2);
    std::cout << "After removal, size: " << container.size() << "\n";
    
    // 4. PIMPL with Interface
    std::cout << "\n4. PIMPL with Interface (Circle):\n";
    Circle circle(5.0);
    circle.draw();
    std::cout << "Area: " << circle.getArea() << "\n";
    
    circle.resize(2.0);
    circle.draw();
    std::cout << "New area: " << circle.getArea() << "\n";
    
    // Move circle
    Circle movedCircle = std::move(circle);
    movedCircle.draw();
    
    // 5. PIMPL with Complex Dependencies
    std::cout << "\n5. PIMPL with Complex Dependencies (DatabaseConnection):\n";
    DatabaseConnection db("host=localhost;port=5432;database=test");
    
    db.connect();
    db.executeQuery("SELECT * FROM users");
    
    auto results = db.fetchResults();
    std::cout << "Query results:\n";
    for (const auto& result : results) {
        std::cout << "  - " << result << "\n";
    }
    
    db.disconnect();
    
    // Move database connection
    DatabaseConnection movedDb = std::move(db);
    // movedDb can still be used
}



#include <iostream>
#include <memory>
#include <vector>
#include <cmath>

// ========== BASIC NVI PATTERN ==========
class Shape {
public:
    virtual ~Shape() = default;
    
    // Non-virtual public interface
    double getArea() const {
        // Common pre-processing
        std::cout << "Calculating area...\n";
        
        // Delegate to virtual implementation
        double area = doGetArea();
        
        // Common post-processing
        std::cout << "Area calculated: " << area << "\n";
        return area;
    }
    
    void draw() const {
        // Common pre-processing
        std::cout << "Preparing to draw...\n";
        
        // Delegate to virtual implementation
        doDraw();
        
        // Common post-processing
        std::cout << "Drawing completed\n";
    }
    
    void scale(double factor) {
        // Input validation
        if (factor <= 0) {
            throw std::invalid_argument("Scale factor must be positive");
        }
        
        // Common pre-processing
        std::cout << "Scaling by factor " << factor << "...\n";
        
        // Delegate to virtual implementation
        doScale(factor);
        
        // Common post-processing
        std::cout << "Scaling completed\n";
    }
    
protected:
    // Protected virtual methods for derived classes to override
    virtual double doGetArea() const = 0;
    virtual void doDraw() const = 0;
    virtual void doScale(double factor) = 0;
    
    // Helper method for derived classes
    void log(const std::string& message) const {
        std::cout << "[Shape] " << message << "\n";
    }
};

class Circle : public Shape {
private:
    double radius;
    
protected:
    double doGetArea() const override {
        return 3.14159 * radius * radius;
    }
    
    void doDraw() const override {
        std::cout << "Drawing circle with radius " << radius << "\n";
    }
    
    void doScale(double factor) override {
        radius *= factor;
        log("Circle radius scaled to " + std::to_string(radius));
    }
    
public:
    explicit Circle(double r) : radius(r) {
        if (r <= 0) {
            throw std::invalid_argument("Radius must be positive");
        }
    }
    
    double getRadius() const {
        return radius;
    }
};

class Rectangle : public Shape {
private:
    double width;
    double height;
    
protected:
    double doGetArea() const override {
        return width * height;
    }
    
    void doDraw() const override {
        std::cout << "Drawing rectangle " << width << "x" << height << "\n";
    }
    
    void doScale(double factor) override {
        width *= factor;
        height *= factor;
        log("Rectangle scaled to " + std::to_string(width) + 
            "x" + std::to_string(height));
    }
    
public:
    Rectangle(double w, double h) : width(w), height(h) {
        if (w <= 0 || h <= 0) {
            throw std::invalid_argument("Dimensions must be positive");
        }
    }
    
    double getWidth() const {
        return width;
    }
    
    double getHeight() const {
        return height;
    }
};

// ========== NVI WITH TEMPLATE METHOD ==========
class DataProcessor {
public:
    virtual ~DataProcessor() = default;
    
    // Template method defining algorithm skeleton
    void process(const std::vector<int>& data) {
        std::cout << "\n=== Starting Data Processing ===\n";
        
        // Step 1: Validate input
        if (!validateInput(data)) {
            throw std::invalid_argument("Invalid input data");
        }
        
        // Step 2: Pre-process data
        auto processedData = preProcess(data);
        
        // Step 3: Core processing (delegated to subclass)
        auto result = doProcess(processedData);
        
        // Step 4: Post-process result
        auto finalResult = postProcess(result);
        
        // Step 5: Log completion
        logResult(finalResult);
        
        std::cout << "=== Processing Complete ===\n";
    }
    
    // Hook methods with default implementations
    virtual bool validateInput(const std::vector<int>& data) {
        std::cout << "Default validation: checking if data is not empty\n";
        return !data.empty();
    }
    
    virtual std::vector<int> preProcess(const std::vector<int>& data) {
        std::cout << "Default pre-processing: copying data\n";
        return data;
    }
    
    // Pure virtual method - must be implemented by derived classes
    virtual std::vector<int> doProcess(const std::vector<int>& data) = 0;
    
    virtual std::vector<int> postProcess(const std::vector<int>& result) {
        std::cout << "Default post-processing: no changes\n";
        return result;
    }
    
    virtual void logResult(const std::vector<int>& result) {
        std::cout << "Processing completed. Result size: " 
                  << result.size() << "\n";
    }
};

class SumProcessor : public DataProcessor {
protected:
    std::vector<int> doProcess(const std::vector<int>& data) override {
        std::cout << "SumProcessor: Calculating sum\n";
        int sum = 0;
        for (int val : data) {
            sum += val;
        }
        return {sum};
    }
    
    void logResult(const std::vector<int>& result) override {
        std::cout << "Sum: " << result[0] << "\n";
    }
};

class SortProcessor : public DataProcessor {
protected:
    std::vector<int> doProcess(const std::vector<int>& data) override {
        std::cout << "SortProcessor: Sorting data\n";
        std::vector<int> sorted = data;
        std::sort(sorted.begin(), sorted.end());
        return sorted;
    }
    
    bool validateInput(const std::vector<int>& data) override {
        std::cout << "SortProcessor validation: checking data size > 1\n";
        return data.size() > 1;
    }
};

// ========== NVI FOR RESOURCE MANAGEMENT ==========
class Resource {
public:
    virtual ~Resource() = default;
    
    // Non-virtual interface for resource usage
    void use() {
        // Common pre-processing
        if (!isAvailable()) {
            throw std::runtime_error("Resource not available");
        }
        
        std::cout << "Acquiring resource...\n";
        
        // Delegate to virtual implementation
        doUse();
        
        // Common post-processing
        std::cout << "Resource usage completed\n";
        updateUsageStatistics();
    }
    
    void release() {
        // Common pre-processing
        std::cout << "Releasing resource...\n";
        
        // Delegate to virtual implementation
        doRelease();
        
        // Common post-processing
        std::cout << "Resource released\n";
        updateReleaseStatistics();
    }
    
    // Non-virtual query methods
    bool isAvailable() const {
        return doIsAvailable();
    }
    
    int getUsageCount() const {
        return usageCount;
    }
    
protected:
    // Protected virtual implementations
    virtual void doUse() = 0;
    virtual void doRelease() = 0;
    virtual bool doIsAvailable() const = 0;
    
    // Protected helper methods
    void incrementUsage() {
        ++usageCount;
    }
    
    void decrementUsage() {
        if (usageCount > 0) --usageCount;
    }
    
private:
    int usageCount = 0;
    
    void updateUsageStatistics() {
        std::cout << "Usage statistics updated\n";
    }
    
    void updateReleaseStatistics() {
        std::cout << "Release statistics updated\n";
    }
};

class DatabaseConnection : public Resource {
private:
    bool connected;
    int connectionId;
    
protected:
    void doUse() override {
        if (!connected) {
            connect();
        }
        std::cout << "Using database connection " << connectionId << "\n";
        incrementUsage();
    }
    
    void doRelease() override {
        if (connected) {
            disconnect();
        }
        decrementUsage();
    }
    
    bool doIsAvailable() const override {
        return true;  // Always available for this example
    }
    
    void connect() {
        // Simulate connection
        connectionId = rand() % 1000;
        connected = true;
        std::cout << "Connected to database with ID: " << connectionId << "\n";
    }
    
    void disconnect() {
        std::cout << "Disconnecting from database " << connectionId << "\n";
        connected = false;
    }
    
public:
    DatabaseConnection() : connected(false), connectionId(-1) {}
};

// ========== NVI WITH MULTIPLE ALGORITHM STEPS ==========
class EncryptionAlgorithm {
public:
    virtual ~EncryptionAlgorithm() = default;
    
    // Non-virtual template method
    std::string encrypt(const std::string& plaintext, const std::string& key) {
        std::cout << "\n=== Encryption Process ===\n";
        
        // Step 1: Validate inputs
        validateInputs(plaintext, key);
        
        // Step 2: Prepare data
        auto preparedData = prepareData(plaintext);
        
        // Step 3: Generate subkeys
        auto subkeys = generateSubkeys(key);
        
        // Step 4: Core encryption (algorithm-specific)
        auto encrypted = doEncrypt(preparedData, subkeys);
        
        // Step 5: Format output
        auto formatted = formatOutput(encrypted);
        
        // Step 6: Log
        logEncryption(plaintext, formatted);
        
        return formatted;
    }
    
    std::string decrypt(const std::string& ciphertext, const std::string& key) {
        std::cout << "\n=== Decryption Process ===\n";
        
        validateInputs(ciphertext, key);
        auto subkeys = generateSubkeys(key);
        auto decrypted = doDecrypt(ciphertext, subkeys);
        logDecryption(ciphertext, decrypted);
        
        return decrypted;
    }
    
protected:
    // Hook methods with default implementations
    virtual void validateInputs(const std::string& data, const std::string& key) {
        if (data.empty()) {
            throw std::invalid_argument("Data cannot be empty");
        }
        if (key.empty()) {
            throw std::invalid_argument("Key cannot be empty");
        }
        std::cout << "Input validation passed\n";
    }
    
    virtual std::string prepareData(const std::string& data) {
        std::cout << "Preparing data...\n";
        return data;  // Default: no preparation
    }
    
    virtual std::vector<int> generateSubkeys(const std::string& key) {
        std::cout << "Generating subkeys from key\n";
        // Simple key expansion
        std::vector<int> subkeys;
        for (char c : key) {
            subkeys.push_back(static_cast<int>(c));
        }
        return subkeys;
    }
    
    virtual std::string formatOutput(const std::string& data) {
        return data;  // Default: no formatting
    }
    
    virtual void logEncryption(const std::string& plaintext, 
                              const std::string& ciphertext) {
        std::cout << "Encryption complete:\n";
        std::cout << "  Plaintext: " << plaintext << "\n";
        std::cout << "  Ciphertext: " << ciphertext << "\n";
    }
    
    virtual void logDecryption(const std::string& ciphertext,
                              const std::string& plaintext) {
        std::cout << "Decryption complete:\n";
        std::cout << "  Ciphertext: " << ciphertext << "\n";
        std::cout << "  Plaintext: " << plaintext << "\n";
    }
    
    // Pure virtual methods for specific algorithms
    virtual std::string doEncrypt(const std::string& data, 
                                 const std::vector<int>& subkeys) = 0;
    virtual std::string doDecrypt(const std::string& data,
                                 const std::vector<int>& subkeys) = 0;
};

class CaesarCipher : public EncryptionAlgorithm {
protected:
    std::string doEncrypt(const std::string& data, 
                         const std::vector<int>& subkeys) override {
        std::cout << "Applying Caesar cipher encryption\n";
        int shift = subkeys.empty() ? 3 : subkeys[0] % 26;
        
        std::string result;
        for (char c : data) {
            if (std::isalpha(c)) {
                char base = std::isupper(c) ? 'A' : 'a';
                result += static_cast<char>((c - base + shift) % 26 + base);
            } else {
                result += c;
            }
        }
        return result;
    }
    
    std::string doDecrypt(const std::string& data,
                         const std::vector<int>& subkeys) override {
        std::cout << "Applying Caesar cipher decryption\n";
        int shift = subkeys.empty() ? 3 : subkeys[0] % 26;
        
        std::string result;
        for (char c : data) {
            if (std::isalpha(c)) {
                char base = std::isupper(c) ? 'A' : 'a';
                result += static_cast<char>((c - base - shift + 26) % 26 + base);
            } else {
                result += c;
            }
        }
        return result;
    }
    
    std::string formatOutput(const std::string& data) override {
        return "CAESAR[" + data + "]";
    }
};

class XORCipher : public EncryptionAlgorithm {
protected:
    std::string doEncrypt(const std::string& data,
                         const std::vector<int>& subkeys) override {
        std::cout << "Applying XOR cipher encryption\n";
        std::string result = data;
        for (size_t i = 0; i < result.length(); ++i) {
            int key = subkeys.empty() ? 42 : subkeys[i % subkeys.size()];
            result[i] ^= static_cast<char>(key);
        }
        return result;
    }
    
    std::string doDecrypt(const std::string& data,
                         const std::vector<int>& subkeys) override {
        // XOR encryption is symmetric
        return doEncrypt(data, subkeys);
    }
    
    std::string prepareData(const std::string& data) override {
        std::cout << "XOR cipher: Encoding data to base64 (simulated)\n";
        return "ENCODED[" + data + "]";
    }
};

void nviExample() {
    std::cout << "\n=== NVI (Non-virtual Interface) Idiom Examples ===\n\n";
    
    // 1. Basic NVI Pattern
    std::cout << "1. Basic NVI Pattern (Shapes):\n";
    Circle circle(5.0);
    Rectangle rect(4.0, 6.0);
    
    std::cout << "\nCircle operations:\n";
    circle.draw();
    std::cout << "Area: " << circle.getArea() << "\n";
    circle.scale(2.0);
    std::cout << "New area: " << circle.getArea() << "\n";
    
    std::cout << "\nRectangle operations:\n";
    rect.draw();
    std::cout << "Area: " << rect.getArea() << "\n";
    
    // 2. NVI with Template Method
    std::cout << "\n2. NVI with Template Method (DataProcessor):\n";
    std::vector<int> data = {5, 2, 8, 1, 9};
    
    SumProcessor sumProcessor;
    auto sumResult = sumProcessor.process(data);
    
    SortProcessor sortProcessor;
    auto sortResult = sortProcessor.process(data);
    
    // 3. NVI for Resource Management
    std::cout << "\n3. NVI for Resource Management:\n";
    DatabaseConnection dbConn;
    
    try {
        dbConn.use();
        dbConn.use();
        std::cout << "Usage count: " << dbConn.getUsageCount() << "\n";
        dbConn.release();
        std::cout << "Usage count: " << dbConn.getUsageCount() << "\n";
    } catch (const std::exception& e) {
        std::cout << "Error: " << e.what() << "\n";
    }
    
    // 4. NVI with Encryption Algorithms
    std::cout << "\n4. NVI with Encryption Algorithms:\n";
    
    CaesarCipher caesar;
    std::string plaintext = "Hello, World!";
    std::string key = "secret";
    
    std::string encrypted = caesar.encrypt(plaintext, key);
    std::string decrypted = caesar.decrypt(encrypted, key);
    
    std::cout << "\nOriginal: " << plaintext << "\n";
    std::cout << "Encrypted: " << encrypted << "\n";
    std::cout << "Decrypted: " << decrypted << "\n";
    
    XORCipher xorCipher;
    std::string xorEncrypted = xorCipher.encrypt(plaintext, key);
    std::string xorDecrypted = xorCipher.decrypt(xorEncrypted, key);
    
    std::cout << "\nXOR Original: " << plaintext << "\n";
    std::cout << "XOR Encrypted: " << xorEncrypted << "\n";
    std::cout << "XOR Decrypted: " << xorDecrypted << "\n";
    
    // Test error handling
    std::cout << "\n5. Error Handling in NVI:\n";
    try {
        Circle invalidCircle(0);  // Should throw
    } catch (const std::exception& e) {
        std::cout << "Caught exception: " << e.what() << "\n";
    }
    
    try {
        DataProcessor* processor = new SumProcessor();
        std::vector<int> emptyData;
        processor->process(emptyData);  // Should throw in validation
        delete processor;
    } catch (const std::exception& e) {
        std::cout << "Caught exception: " << e.what() << "\n";
    }
}



#include <iostream>
#include <memory>
#include <vector>
#include <algorithm>
#include <cstring>

// ========== BASIC COPY-AND-SWAP ==========
class String {
private:
    char* data;
    size_t length;
    
    // Helper function for deep copy
    void copyFrom(const String& other) {
        length = other.length;
        data = new char[length + 1];
        std::memcpy(data, other.data, length + 1);
    }
    
    // Helper function for cleanup
    void free() {
        delete[] data;
        data = nullptr;
        length = 0;
    }
    
public:
    // Constructor
    String(const char* str = "") {
        length = std::strlen(str);
        data = new char[length + 1];
        std::memcpy(data, str, length + 1);
        std::cout << "Constructed: \"" << data << "\"\n";
    }
    
    // Destructor
    ~String() {
        free();
        std::cout << "Destroyed\n";
    }
    
    // Copy constructor (using copy-and-swap)
    String(const String& other) : data(nullptr), length(0) {
        std::cout << "Copy constructing from: \"" << other.data << "\"\n";
        copyFrom(other);
    }
    
    // Copy assignment operator (using copy-and-swap)
    String& operator=(String other) {  // Note: parameter by value
        std::cout << "Copy assigning from: \"" << other.data << "\"\n";
        swap(other);
        return *this;
    }
    
    // Move constructor (can also use copy-and-swap)
    String(String&& other) noexcept : data(other.data), length(other.length) {
        std::cout << "Move constructing from: \"" << other.data << "\"\n";
        other.data = nullptr;
        other.length = 0;
    }
    
    // Move assignment operator (using copy-and-swap)
    String& operator=(String&& other) noexcept {
        std::cout << "Move assigning from: \"" << other.data << "\"\n";
        swap(other);
        return *this;
    }
    
    // Swap function
    void swap(String& other) noexcept {
        std::swap(data, other.data);
        std::swap(length, other.length);
        std::cout << "Swapped\n";
    }
    
    // Accessors
    const char* c_str() const {
        return data ? data : "";
    }
    
    size_t size() const {
        return length;
    }
    
    // Friend swap for ADL (Argument Dependent Lookup)
    friend void swap(String& first, String& second) noexcept {
        first.swap(second);
    }
    
    // For demonstration
    void print() const {
        std::cout << "String: \"" << (data ? data : "(null)") << "\" (length: " << length << ")\n";
    }
};

// ========== COPY-AND-SWAP WITH RESOURCE ARRAY ==========
template<typename T>
class Vector {
private:
    T* data;
    size_t size_;
    size_t capacity_;
    
    void copyFrom(const Vector& other) {
        size_ = other.size_;
        capacity_ = other.capacity_;
        data = new T[capacity_];
        
        for (size_t i = 0; i < size_; ++i) {
            data[i] = other.data[i];
        }
    }
    
    void free() {
        delete[] data;
        data = nullptr;
        size_ = 0;
        capacity_ = 0;
    }
    
    void resizeIfNeeded() {
        if (size_ >= capacity_) {
            size_t newCapacity = capacity_ == 0 ? 1 : capacity_ * 2;
            T* newData = new T[newCapacity];
            
            for (size_t i = 0; i < size_; ++i) {
                newData[i] = std::move(data[i]);
            }
            
            delete[] data;
            data = newData;
            capacity_ = newCapacity;
        }
    }
    
public:
    // Constructors
    Vector() : data(nullptr), size_(0), capacity_(0) {}
    
    explicit Vector(size_t size) : size_(size), capacity_(size) {
        data = new T[capacity_];
        std::cout << "Vector constructed with size " << size << "\n";
    }
    
    Vector(std::initializer_list<T> init) : size_(init.size()), capacity_(init.size()) {
        data = new T[capacity_];
        size_t i = 0;
        for (const auto& item : init) {
            data[i++] = item;
        }
        std::cout << "Vector constructed from initializer list\n";
    }
    
    // Destructor
    ~Vector() {
        free();
        std::cout << "Vector destroyed\n";
    }
    
    // Copy constructor
    Vector(const Vector& other) : data(nullptr), size_(0), capacity_(0) {
        std::cout << "Vector copy constructor\n";
        copyFrom(other);
    }
    
    // Copy assignment operator (copy-and-swap)
    Vector& operator=(Vector other) {
        std::cout << "Vector copy assignment\n";
        swap(other);
        return *this;
    }
    
    // Move constructor
    Vector(Vector&& other) noexcept 
        : data(other.data), size_(other.size_), capacity_(other.capacity_) {
        std::cout << "Vector move constructor\n";
        other.data = nullptr;
        other.size_ = 0;
        other.capacity_ = 0;
    }
    
    // Move assignment operator (copy-and-swap)
    Vector& operator=(Vector&& other) noexcept {
        std::cout << "Vector move assignment\n";
        swap(other);
        return *this;
    }
    
    // Swap function
    void swap(Vector& other) noexcept {
        std::swap(data, other.data);
        std::swap(size_, other.size_);
        std::swap(capacity_, other.capacity_);
    }
    
    // Friend swap for ADL
    friend void swap(Vector& first, Vector& second) noexcept {
        first.swap(second);
    }
    
    // Element access
    T& operator[](size_t index) {
        if (index >= size_) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }
    
    const T& operator[](size_t index) const {
        if (index >= size_) {
            throw std::out_of_range("Index out of bounds");
        }
        return data[index];
    }
    
    // Capacity
    size_t size() const { return size_; }
    size_t capacity() const { return capacity_; }
    bool empty() const { return size_ == 0; }
    
    // Modifiers
    void push_back(const T& value) {
        resizeIfNeeded();
        data[size_++] = value;
    }
    
    void push_back(T&& value) {
        resizeIfNeeded();
        data[size_++] = std::move(value);
    }
    
    void pop_back() {
        if (size_ > 0) {
            --size_;
        }
    }
    
    void clear() {
        free();
    }
    
    void reserve(size_t newCapacity) {
        if (newCapacity > capacity_) {
            T* newData = new T[newCapacity];
            for (size_t i = 0; i < size_; ++i) {
                newData[i] = std::move(data[i]);
            }
            delete[] data;
            data = newData;
            capacity_ = newCapacity;
        }
    }
    
    // For demonstration
    void print() const {
        std::cout << "Vector [size=" << size_ << ", capacity=" << capacity_ << "]: ";
        for (size_t i = 0; i < size_; ++i) {
            std::cout << data[i] << " ";
        }
        std::cout << "\n";
    }
};

// ========== COPY-AND-SWAP WITH SMART POINTERS ==========
class ManagedResource {
private:
    class Impl;
    std::unique_ptr<Impl> pImpl;
    
public:
    ManagedResource();
    ~ManagedResource();
    
    // Copy operations using copy-and-swap
    ManagedResource(const ManagedResource& other);
    ManagedResource& operator=(ManagedResource other);
    
    // Move operations
    ManagedResource(ManagedResource&& other) noexcept;
    ManagedResource& operator=(ManagedResource&& other) noexcept;
    
    // Swap
    void swap(ManagedResource& other) noexcept;
    
    // Operations
    void use();
    void setValue(int value);
    int getValue() const;
    
private:
    class Impl {
    public:
        int value;
        std::vector<int> data;
        
        Impl() : value(0) {
            data.resize(10);
            std::cout << "ManagedResource::Impl constructed\n";
        }
        
        Impl(const Impl& other) : value(other.value), data(other.data) {
            std::cout << "ManagedResource::Impl copy constructed\n";
        }
        
        Impl(Impl&& other) noexcept 
            : value(other.value), data(std::move(other.data)) {
            other.value = 0;
            std::cout << "ManagedResource::Impl move constructed\n";
        }
    };
};

ManagedResource::ManagedResource() 
    : pImpl(std::make_unique<Impl>()) {}

ManagedResource::~ManagedResource() = default;

ManagedResource::ManagedResource(const ManagedResource& other)
    : pImpl(other.pImpl ? std::make_unique<Impl>(*other.pImpl) : nullptr) {
    std::cout << "ManagedResource copy constructor\n";
}

ManagedResource& ManagedResource::operator=(ManagedResource other) {
    std::cout << "ManagedResource copy assignment\n";
    swap(other);
    return *this;
}

ManagedResource::ManagedResource(ManagedResource&& other) noexcept 
    : pImpl(std::move(other.pImpl)) {
    std::cout << "ManagedResource move constructor\n";
}

ManagedResource& ManagedResource::operator=(ManagedResource&& other) noexcept {
    std::cout << "ManagedResource move assignment\n";
    swap(other);
    return *this;
}

void ManagedResource::swap(ManagedResource& other) noexcept {
    pImpl.swap(other.pImpl);
}

void ManagedResource::use() {
    if (pImpl) {
        std::cout << "Using ManagedResource, value = " << pImpl->value << "\n";
    }
}

void ManagedResource::setValue(int value) {
    if (pImpl) {
        pImpl->value = value;
    }
}

int ManagedResource::getValue() const {
    return pImpl ? pImpl->value : -1;
}

// ========== COPY-AND-SWAP FOR EXCEPTION SAFETY ==========
class Transaction {
private:
    std::vector<std::string> operations;
    bool committed;
    
    // Private copy implementation
    void copyFrom(const Transaction& other) {
        operations = other.operations;
        committed = other.committed;
    }
    
public:
    Transaction() : committed(false) {
        std::cout << "Transaction created\n";
    }
    
    ~Transaction() {
        if (!committed) {
            rollback();
        }
    }
    
    // Copy constructor
    Transaction(const Transaction& other) : committed(false) {
        std::cout << "Transaction copy constructor\n";
        copyFrom(other);
    }
    
    // Copy assignment with copy-and-swap
    Transaction& operator=(Transaction other) {
        std::cout << "Transaction copy assignment\n";
        swap(other);
        return *this;
    }
    
    // Move constructor
    Transaction(Transaction&& other) noexcept 
        : operations(std::move(other.operations)), committed(other.committed) {
        std::cout << "Transaction move constructor\n";
        other.committed = true;  // Prevent rollback in moved-from object
    }
    
    // Move assignment with copy-and-swap
    Transaction& operator=(Transaction&& other) noexcept {
        std::cout << "Transaction move assignment\n";
        swap(other);
        other.committed = true;  // Prevent rollback
        return *this;
    }
    
    // Swap
    void swap(Transaction& other) noexcept {
        std::swap(operations, other.operations);
        std::swap(committed, other.committed);
    }
    
    // Operations
    void addOperation(const std::string& op) {
        operations.push_back(op);
        std::cout << "Added operation: " << op << "\n";
    }
    
    void commit() {
        std::cout << "Committing transaction with " 
                  << operations.size() << " operations\n";
        // Simulate commit
        for (const auto& op : operations) {
            std::cout << "  Executing: " << op << "\n";
        }
        committed = true;
    }
    
    void rollback() {
        std::cout << "Rolling back " << operations.size() 
                  << " operations\n";
        operations.clear();
    }
    
    size_t operationCount() const {
        return operations.size();
    }
};

void copyAndSwapExample() {
    std::cout << "\n=== Copy-and-Swap Idiom Examples ===\n\n";
    
    // 1. Basic String with Copy-and-Swap
    std::cout << "1. Basic String with Copy-and-Swap:\n";
    String s1("Hello");
    String s2("World");
    
    std::cout << "\nOriginal strings:\n";
    s1.print();
    s2.print();
    
    std::cout << "\nCopy assignment (s1 = s2):\n";
    s1 = s2;
    s1.print();
    s2.print();
    
    std::cout << "\nMove assignment (s1 = std::move(s2)):\n";
    s1 = std::move(s2);
    s1.print();
    s2.print();
    
    std::cout << "\nSelf-assignment test (s1 = s1):\n";
    s1 = s1;  // Should handle self-assignment correctly
    s1.print();
    
    // 2. Vector with Copy-and-Swap
    std::cout << "\n2. Vector with Copy-and-Swap:\n";
    Vector<int> v1 = {1, 2, 3, 4, 5};
    Vector<int> v2 = {10, 20, 30};
    
    std::cout << "\nOriginal vectors:\n";
    v1.print();
    v2.print();
    
    std::cout << "\nCopy assignment (v1 = v2):\n";
    v1 = v2;
    v1.print();
    v2.print();
    
    std::cout << "\nMove assignment (v1 = std::move(v2)):\n";
    v1 = std::move(v2);
    v1.print();
    v2.print();
    
    // 3. Managed Resource with Smart Pointers
    std::cout << "\n3. Managed Resource with Smart Pointers:\n";
    ManagedResource r1;
    ManagedResource r2;
    
    r1.setValue(42);
    r2.setValue(100);
    
    std::cout << "\nOriginal resources:\n";
    std::cout << "r1 value: " << r1.getValue() << "\n";
    std::cout << "r2 value: " << r2.getValue() << "\n";
    
    std::cout << "\nCopy assignment (r1 = r2):\n";
    r1 = r2;
    std::cout << "r1 value: " << r1.getValue() << "\n";
    std::cout << "r2 value: " << r2.getValue() << "\n";
    
    std::cout << "\nMove assignment (r1 = std::move(r2)):\n";
    r1 = std::move(r2);
    std::cout << "r1 value: " << r1.getValue() << "\n";
    std::cout << "r2 value: " << r2.getValue() << "\n";
    
    // 4. Transaction with Exception Safety
    std::cout << "\n4. Transaction with Exception Safety:\n";
    Transaction t1;
    t1.addOperation("UPDATE users SET name='John' WHERE id=1");
    t1.addOperation("INSERT INTO logs VALUES ('user_updated')");
    
    Transaction t2;
    t2.addOperation("DELETE FROM temp WHERE expired=1");
    
    std::cout << "\nOriginal transactions:\n";
    std::cout << "t1 operations: " << t1.operationCount() << "\n";
    std::cout << "t2 operations: " << t2.operationCount() << "\n";
    
    std::cout << "\nCopy assignment (t1 = t2):\n";
    t1 = t2;
    std::cout << "t1 operations: " << t1.operationCount() << "\n";
    std::cout << "t2 operations: " << t2.operationCount() << "\n";
    
    std::cout << "\nCommit t1:\n";
    t1.commit();
    
    std::cout << "\nMove t2 to new transaction:\n";
    Transaction t3 = std::move(t2);
    std::cout << "t2 operations: " << t2.operationCount() << "\n";
    std::cout << "t3 operations: " << t3.operationCount() << "\n";
    
    // 5. Exception Safety Demonstration
    std::cout << "\n5. Exception Safety Demonstration:\n";
    try {
        Vector<String> strings;
        strings.push_back(String("First"));
        strings.push_back(String("Second"));
        
        // This might throw, but Vector is exception-safe
        strings.push_back(String("Very long string that might cause allocation failure"));
        
    } catch (const std::bad_alloc& e) {
        std::cout << "Caught bad_alloc: " << e.what() << "\n";
        // Resources are properly cleaned up
    }
    
    // 6. ADL Swap Demonstration
    std::cout << "\n6. ADL Swap Demonstration:\n";
    String a("Apple");
    String b("Banana");
    
    std::cout << "Before swap:\n";
    a.print();
    b.print();
    
    using std::swap;
    swap(a, b);  // Uses ADL to find String::swap
    
    std::cout << "After swap:\n";
    a.print();
    b.print();
}





