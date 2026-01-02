#include <iostream>
#include <string>

// ============================================================================
// 1. CLASSES vs STRUCTS
// ============================================================================

void classes_vs_structs() {
    std::cout << "\n=== CLASSES vs STRUCTS ===\n";
    
    // In C++, the ONLY difference between class and struct is:
    // - class members are private by default
    // - struct members are public by default
    
    struct PointStruct {
        // Public by default
        double x;
        double y;
        
        // Can have member functions
        void print() const {
            std::cout << "PointStruct(" << x << ", " << y << ")\n";
        }
    };
    
    class PointClass {
        // Private by default
        double x;
        double y;
        
    public:
        // Need explicit public section
        void set(double x_val, double y_val) {
            x = x_val;
            y = y_val;
        }
        
        void print() const {
            std::cout << "PointClass(" << x << ", " << y << ")\n";
        }
    };
    
    // Using struct
    PointStruct ps;
    ps.x = 10.5;  // Direct access - struct members public by default
    ps.y = 20.5;
    ps.print();
    
    // Using class
    PointClass pc;
    // pc.x = 10.5;  // ERROR: private member
    pc.set(10.5, 20.5);  // Must use public interface
    pc.print();
    
    // Common conventions:
    // - Use struct for passive data structures (POD - Plain Old Data)
    // - Use class for active objects with behavior and invariants
}

// ============================================================================
// 2. MEMBER FUNCTIONS & ACCESS SPECIFIERS
// ============================================================================

class BankAccount {
private:  // Only accessible within class
    std::string account_number;
    double balance;
    mutable int access_count;  // mutable: can be modified in const methods
    
protected:  // Accessible within class and derived classes
    std::string bank_name;
    
public:  // Accessible from anywhere
    // Constructor
    BankAccount(const std::string& acc_num, double initial_balance)
        : account_number(acc_num), balance(initial_balance), access_count(0) {
        std::cout << "BankAccount created: " << account_number << "\n";
    }
    
    // Regular member function
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            std::cout << "Deposited: $" << amount << "\n";
        }
    }
    
    // Const member function - can't modify non-mutable members
    double get_balance() const {
        access_count++;  // OK: mutable member
        // balance++;  // ERROR: can't modify non-mutable member in const function
        return balance;
    }
    
    // Static member function - belongs to class, not object
    static void display_bank_info() {
        std::cout << "Welcome to Our Bank!\n";
        // Cannot access non-static members: balance, account_number, etc.
    }
    
    // Friend function declaration (external function that can access private members)
    friend void audit_account(const BankAccount& account);
    
    // Inline member function (defined inside class)
    std::string get_account_number() const { return account_number; }
    
    // Member function defined outside class (see below)
    void withdraw(double amount);
};

// Member function definition outside class
void BankAccount::withdraw(double amount) {
    if (amount > 0 && amount <= balance) {
        balance -= amount;
        std::cout << "Withdrew: $" << amount << "\n";
    } else {
        std::cout << "Insufficient funds or invalid amount\n";
    }
}

// Friend function definition
void audit_account(const BankAccount& account) {
    // Can access private members because declared as friend
    std::cout << "Audit - Account: " << account.account_number 
              << ", Balance: $" << account.balance 
              << ", Accessed " << account.access_count << " times\n";
}

// ============================================================================
// 3. CONSTRUCTORS & DESTRUCTORS
// ============================================================================

class SmartArray {
private:
    int* data;
    size_t size;
    
public:
    // 3.1 Default Constructor
    SmartArray() : data(nullptr), size(0) {
        std::cout << "Default constructor called\n";
    }
    
    // 3.2 Parameterized Constructor
    SmartArray(size_t n) : size(n) {
        std::cout << "Parameterized constructor called, size: " << n << "\n";
        data = new int[n]();  // Zero-initialized
    }
    
    // 3.3 Copy Constructor (deep copy)
    SmartArray(const SmartArray& other) : size(other.size) {
        std::cout << "Copy constructor called\n";
        data = new int[size];
        std::copy(other.data, other.data + size, data);
    }
    
    // 3.4 Move Constructor (C++11) - transfers ownership
    SmartArray(SmartArray&& other) noexcept 
        : data(other.data), size(other.size) {
        std::cout << "Move constructor called\n";
        other.data = nullptr;  // Leave source in valid but empty state
        other.size = 0;
    }
    
    // 3.5 Explicit Constructor - prevents implicit conversion
    explicit SmartArray(int initial_value) : size(1) {
        std::cout << "Explicit constructor called with value: " << initial_value << "\n";
        data = new int[1];
        data[0] = initial_value;
    }
    
    // 3.6 Delegating Constructor (C++11) - one constructor calls another
    SmartArray(size_t n, int value) : SmartArray(n) {  // Delegates to parameterized constructor
        std::cout << "Delegating constructor called\n";
        std::fill(data, data + size, value);
    }
    
    // 3.7 Destructor
    ~SmartArray() {
        std::cout << "Destructor called";
        if (data) {
            std::cout << ", freeing " << size << " elements\n";
            delete[] data;
        } else {
            std::cout << ", no data to free\n";
        }
    }
    
    // 3.8 Copy Assignment Operator
    SmartArray& operator=(const SmartArray& other) {
        std::cout << "Copy assignment operator called\n";
        if (this != &other) {  // Self-assignment check
            delete[] data;  // Free existing resources
            
            size = other.size;
            data = new int[size];
            std::copy(other.data, other.data + size, data);
        }
        return *this;
    }
    
    // 3.9 Move Assignment Operator (C++11)
    SmartArray& operator=(SmartArray&& other) noexcept {
        std::cout << "Move assignment operator called\n";
        if (this != &other) {
            delete[] data;
            
            data = other.data;
            size = other.size;
            
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
    
    void print() const {
        std::cout << "Array[";
        for (size_t i = 0; i < size; ++i) {
            std::cout << data[i];
            if (i < size - 1) std::cout << ", ";
        }
        std::cout << "]\n";
    }
};

void demonstrate_constructors() {
    std::cout << "\n=== CONSTRUCTORS & DESTRUCTORS ===\n";
    
    // Default constructor
    SmartArray arr1;
    
    // Parameterized constructor
    SmartArray arr2(5);
    
    // Copy constructor
    SmartArray arr3 = arr2;  // Calls copy constructor
    SmartArray arr4(arr2);   // Alternative syntax
    
    // Move constructor
    SmartArray arr5 = std::move(arr2);  // arr2 is now empty
    
    // Explicit constructor prevents implicit conversion
    SmartArray arr6(42);           // OK: direct initialization
    // SmartArray arr7 = 42;       // ERROR: explicit constructor prevents this
    
    // Delegating constructor
    SmartArray arr8(3, 99);        // Creates array of 3 elements all set to 99
    
    // Copy assignment
    arr1 = arr3;                   // Calls copy assignment operator
    
    // Move assignment
    arr4 = std::move(arr3);        // arr3 is now empty
    
    // Temporary objects
    {
        SmartArray temp(2);
        // temp destroyed at end of scope
    }
    
    std::cout << "End of function - destructors will be called in reverse order\n";
}

// ============================================================================
// 4. ENCAPSULATION & ACCESS CONTROL
// ============================================================================

class TemperatureController {
private:
    double temperature;  // Private data - hidden implementation
    
    // Private helper method - not part of public interface
    bool is_safe_temperature(double temp) const {
        return temp >= -50.0 && temp <= 150.0;
    }
    
public:
    // Public interface - what users can interact with
    TemperatureController() : temperature(20.0) {}
    
    // Getter - provides read-only access
    double get_temperature() const {
        return temperature;
    }
    
    // Setter - validates input before modifying private data
    bool set_temperature(double new_temp) {
        if (is_safe_temperature(new_temp)) {
            temperature = new_temp;
            std::cout << "Temperature set to: " << temperature << "°C\n";
            return true;
        }
        std::cout << "Error: Temperature " << new_temp << "°C is out of safe range\n";
        return false;
    }
    
    // Public method that uses private helper
    void increase_temperature(double delta) {
        set_temperature(temperature + delta);
    }
};

// ============================================================================
// 5. THIS POINTER
// ============================================================================

class Employee {
private:
    std::string name;
    int id;
    double salary;
    
public:
    Employee(const std::string& name, int id, double salary) {
        // Using 'this' to distinguish parameter names from member names
        this->name = name;    // this->name refers to member variable
                              // name refers to parameter
        this->id = id;
        this->salary = salary;
    }
    
    // Alternative: member initializer list (preferred)
    Employee(int id, const std::string& name, double salary) 
        : name(name), id(id), salary(salary) {  // No 'this' needed
    }
    
    // Return reference to self for method chaining
    Employee& set_name(const std::string& new_name) {
        name = new_name;
        return *this;  // Return reference to current object
    }
    
    Employee& set_salary(double new_salary) {
        salary = new_salary;
        return *this;
    }
    
    // Const method returning pointer to const object
    const Employee* get_this_ptr() const {
        return this;  // 'this' is Employee* in non-const methods
                      // const Employee* in const methods
    }
    
    void print() const {
        std::cout << "Employee: " << name 
                  << " (ID: " << id 
                  << ", Salary: $" << salary << ")\n";
    }
    
    // Static method cannot use 'this'
    static void display_company_info() {
        // this->name;  // ERROR: static methods have no 'this' pointer
        std::cout << "XYZ Corporation\n";
    }
};

// ============================================================================
// 6. INHERITANCE
// ============================================================================

class Vehicle {
protected:  // Accessible in derived classes, not from outside
    std::string make;
    std::string model;
    int year;
    
private:    // Not accessible in derived classes
    std::string vin;  // Vehicle Identification Number
    
public:
    Vehicle(const std::string& make, const std::string& model, int year)
        : make(make), model(model), year(year) {
        std::cout << "Vehicle constructor: " << make << " " << model << "\n";
    }
    
    virtual ~Vehicle() {
        std::cout << "Vehicle destructor: " << make << " " << model << "\n";
    }
    
    void display_info() const {
        std::cout << year << " " << make << " " << model << "\n";
    }
    
    virtual void start_engine() const {
        std::cout << "Vehicle engine started\n";
    }
    
    void set_vin(const std::string& vin_num) {
        vin = vin_num;
    }
    
    std::string get_vin() const {
        return vin;
    }
};

// Public inheritance - most common
// Public members of base become public in derived
// Protected members of base become protected in derived
class Car : public Vehicle {
private:
    int doors;
    std::string fuel_type;
    
public:
    Car(const std::string& make, const std::string& model, int year,
        int doors, const std::string& fuel_type)
        : Vehicle(make, model, year),  // Initialize base class
          doors(doors), fuel_type(fuel_type) {
        std::cout << "Car constructor: " << doors << "-door " << fuel_type << " car\n";
    }
    
    ~Car() override {
        std::cout << "Car destructor\n";
    }
    
    // Override base class method
    void start_engine() const override {
        std::cout << "Car engine started with key/button\n";
    }
    
    // New functionality specific to Car
    void open_trunk() const {
        std::cout << "Car trunk opened\n";
    }
    
    void display_car_info() const {
        // Can access protected members of base class
        std::cout << year << " " << make << " " << model 
                  << " (" << doors << " doors, " << fuel_type << ")\n";
        // Cannot access private members of base class
        // std::cout << vin;  // ERROR: private in Vehicle
    }
};

// Protected inheritance - rarely used
// Public and protected members of base become protected in derived
class ProtectedCar : protected Vehicle {
public:
    ProtectedCar() : Vehicle("Toyota", "Camry", 2020) {}
    
    // Vehicle's public members are now protected in ProtectedCar
    void show() {
        display_info();  // OK: inside derived class
        // But from outside: ProtectedCar pc; pc.display_info(); // ERROR
    }
};

// Private inheritance - implementation inheritance, not interface
// Public and protected members of base become private in derived
class PrivateCar : private Vehicle {
public:
    PrivateCar() : Vehicle("Honda", "Accord", 2021) {}
    
    // Expose specific base class methods if needed
    using Vehicle::display_info;  // Make display_info public again
};

// Multiple inheritance
class ElectricVehicle {
public:
    void charge_battery() {
        std::cout << "Battery charging...\n";
    }
};

class HybridCar : public Car, public ElectricVehicle {
public:
    HybridCar() : Car("Toyota", "Prius", 2022, 4, "Hybrid") {}
    
    void start_engine() const override {
        std::cout << "Hybrid car started (electric mode first)\n";
    }
};

// Virtual inheritance - solves diamond problem
class PoweredDevice {
public:
    int power;
    
    PoweredDevice(int p) : power(p) {
        std::cout << "PoweredDevice constructor: " << p << "W\n";
    }
};

class Scanner : virtual public PoweredDevice {  // Virtual inheritance
public:
    Scanner(int resolution, int power) 
        : PoweredDevice(power) {
        std::cout << "Scanner constructor\n";
    }
};

class Printer : virtual public PoweredDevice {  // Virtual inheritance
public:
    Printer(int pages_per_minute, int power)
        : PoweredDevice(power) {
        std::cout << "Printer constructor\n";
    }
};

class Copier : public Scanner, public Printer {
public:
    // PoweredDevice initialized only once by Copier
    Copier(int res, int ppm, int power)
        : PoweredDevice(power),  // Initialize shared base
          Scanner(res, 0),       // Don't initialize PoweredDevice here
          Printer(ppm, 0) {      // Don't initialize PoweredDevice here
        std::cout << "Copier constructor\n";
    }
};

// ============================================================================
// 7. POLYMORPHISM
// ============================================================================

class Shape {
protected:
    double x, y;
    
public:
    Shape(double x, double y) : x(x), y(y) {}
    
    // Virtual destructor - CRUCIAL for polymorphic classes
    virtual ~Shape() {
        std::cout << "Shape destructor\n";
    }
    
    // Virtual function - can be overridden by derived classes
    virtual double area() const {
        std::cout << "Shape area called - default implementation\n";
        return 0.0;
    }
    
    // Pure virtual function - makes class abstract
    virtual void draw() const = 0;  // Must be overridden by derived classes
    
    // Non-virtual function - static binding (compile-time)
    void move(double dx, double dy) {
        x += dx;
        y += dy;
        std::cout << "Shape moved to (" << x << ", " << y << ")\n";
    }
    
    // Virtual function with default implementation
    virtual void scale(double factor) {
        std::cout << "Scaling shape by factor " << factor << "\n";
    }
    
    // final function - cannot be overridden in further derived classes
    virtual void display_type() const final {
        std::cout << "This is a Shape\n";
    }
};

class Circle : public Shape {
private:
    double radius;
    
public:
    Circle(double x, double y, double r) : Shape(x, y), radius(r) {}
    
    ~Circle() override {
        std::cout << "Circle destructor\n";
    }
    
    // Override virtual function
    double area() const override {
        return 3.14159 * radius * radius;
    }
    
    // Must implement pure virtual function
    void draw() const override {
        std::cout << "Drawing Circle at (" << x << ", " << y 
                  << ") with radius " << radius << "\n";
    }
    
    // Override virtual function with default implementation
    void scale(double factor) override {
        Shape::scale(factor);  // Call base class implementation
        radius *= factor;
        std::cout << "Circle radius scaled to: " << radius << "\n";
    }
    
    // Cannot override display_type() - it's final in Shape
    // void display_type() const override { }  // ERROR
};

class Rectangle : public Shape {
private:
    double width, height;
    
public:
    Rectangle(double x, double y, double w, double h) 
        : Shape(x, y), width(w), height(h) {}
    
    ~Rectangle() override {
        std::cout << "Rectangle destructor\n";
    }
    
    // override keyword ensures we're actually overriding a virtual function
    double area() const override {
        return width * height;
    }
    
    void draw() const override {
        std::cout << "Drawing Rectangle at (" << x << ", " << y 
                  << ") with width " << width << " and height " << height << "\n";
    }
    
    // final class - cannot be inherited from
    virtual void special_method() final {
        std::cout << "Final method in Rectangle\n";
    }
};

// class Square : public Rectangle {  // ERROR if Rectangle's special_method is final
// };

void demonstrate_polymorphism() {
    std::cout << "\n=== POLYMORPHISM & VIRTUAL FUNCTIONS ===\n";
    
    // Cannot instantiate abstract class
    // Shape s(0, 0);  // ERROR: Shape has pure virtual function
    
    // Base class pointer to derived class object
    Shape* shape1 = new Circle(10, 20, 5);
    Shape* shape2 = new Rectangle(30, 40, 8, 6);
    
    // Polymorphic calls - runtime binding
    shape1->draw();           // Calls Circle::draw()
    std::cout << "Area: " << shape1->area() << "\n";  // Calls Circle::area()
    
    shape2->draw();           // Calls Rectangle::draw()
    std::cout << "Area: " << shape2->area() << "\n";  // Calls Rectangle::area()
    
    // Non-virtual function - always calls Shape::move()
    shape1->move(5, 5);       // Calls Shape::move()
    
    // Array/vector of base class pointers
    std::vector<Shape*> shapes;
    shapes.push_back(new Circle(0, 0, 3));
    shapes.push_back(new Rectangle(5, 5, 4, 6));
    shapes.push_back(new Circle(10, 10, 2));
    
    for (Shape* shape : shapes) {
        shape->draw();
        std::cout << "Area: " << shape->area() << "\n";
    }
    
    // Clean up
    for (Shape* shape : shapes) {
        delete shape;  // Calls appropriate destructor (virtual destructor needed!)
    }
    
    delete shape1;
    delete shape2;
    
    // VTABLE & VPTR explanation in comments:
    // 1. Each polymorphic class has a vtable (virtual table)
    // 2. Each object has a vptr (virtual pointer) pointing to its class's vtable
    // 3. vtable contains function pointers to virtual functions
    // 4. When calling virtual function, runtime looks up function in vtable via vptr
}

// ============================================================================
// 8. ABSTRACT CLASSES & INTERFACES
// ============================================================================

// Interface (C++ doesn't have explicit interface keyword, use abstract class)
class Drawable {
public:
    virtual ~Drawable() = default;
    virtual void draw() const = 0;  // Pure virtual function
};

class Clickable {
public:
    virtual ~Clickable() = default;
    virtual void onClick() = 0;     // Pure virtual function
    virtual void onHover() {        // Optional implementation
        std::cout << "Default hover behavior\n";
    }
};

// Multiple interface implementation
class Button : public Drawable, public Clickable {
private:
    std::string label;
    int x, y;
    
public:
    Button(const std::string& label, int x, int y) 
        : label(label), x(x), y(y) {}
    
    // Implement Drawable interface
    void draw() const override {
        std::cout << "Drawing Button: \"" << label 
                  << "\" at (" << x << ", " << y << ")\n";
    }
    
    // Implement Clickable interface
    void onClick() override {
        std::cout << "Button \"" << label << "\" clicked!\n";
    }
    
    // Override optional method
    void onHover() override {
        std::cout << "Button \"" << label << "\" is being hovered over\n";
    }
};

// Abstract base class with some implementation
class Animal {
protected:
    std::string name;
    int age;
    
public:
    Animal(const std::string& name, int age) : name(name), age(age) {}
    virtual ~Animal() = default;
    
    // Pure virtual functions - must be implemented by derived classes
    virtual void make_sound() const = 0;
    virtual void move() const = 0;
    
    // Concrete (non-abstract) methods
    void eat() const {
        std::cout << name << " is eating\n";
    }
    
    void sleep() const {
        std::cout << name << " is sleeping\n";
    }
    
    // Virtual function with default implementation
    virtual void display_info() const {
        std::cout << name << " (age: " << age << ")\n";
    }
};

class Dog : public Animal {
public:
    Dog(const std::string& name, int age) : Animal(name, age) {}
    
    void make_sound() const override {
        std::cout << name << " says: Woof!\n";
    }
    
    void move() const override {
        std::cout << name << " is running\n";
    }
    
    void display_info() const override {
        Animal::display_info();  // Call base implementation
        std::cout << "Type: Dog\n";
    }
    
    // Dog-specific method
    void fetch() const {
        std::cout << name << " is fetching the ball\n";
    }
};

class Bird : public Animal {
private:
    double wingspan;
    
public:
    Bird(const std::string& name, int age, double wingspan) 
        : Animal(name, age), wingspan(wingspan) {}
    
    void make_sound() const override {
        std::cout << name << " says: Chirp!\n";
    }
    
    void move() const override {
        std::cout << name << " is flying\n";
    }
    
    void display_info() const override {
        Animal::display_info();
        std::cout << "Type: Bird, Wingspan: " << wingspan << "m\n";
    }
};

// ============================================================================
// 9. RAII (Resource Acquisition Is Initialization)
// ============================================================================

class FileRAII {
private:
    FILE* file;
    std::string filename;
    
public:
    // Constructor acquires resource
    FileRAII(const std::string& filename, const std::string& mode) 
        : filename(filename) {
        file = fopen(filename.c_str(), mode.c_str());
        if (!file) {
            throw std::runtime_error("Failed to open file: " + filename);
        }
        std::cout << "File \"" << filename << "\" opened successfully\n";
    }
    
    // Destructor releases resource
    ~FileRAII() {
        if (file) {
            fclose(file);
            std::cout << "File \"" << filename << "\" closed automatically\n";
        }
    }
    
    // Delete copy operations to prevent double free
    FileRAII(const FileRAII&) = delete;
    FileRAII& operator=(const FileRAII&) = delete;
    
    // Allow move operations
    FileRAII(FileRAII&& other) noexcept 
        : file(other.file), filename(std::move(other.filename)) {
        other.file = nullptr;
        std::cout << "File handle moved\n";
    }
    
    FileRAII& operator=(FileRAII&& other) noexcept {
        if (this != &other) {
            if (file) fclose(file);
            file = other.file;
            filename = std::move(other.filename);
            other.file = nullptr;
        }
        return *this;
    }
    
    // Resource usage methods
    void write(const std::string& data) {
        if (file) {
            fputs(data.c_str(), file);
            fputs("\n", file);
        }
    }
    
    std::string read_line() {
        if (!file) return "";
        
        char buffer[256];
        if (fgets(buffer, sizeof(buffer), file)) {
            return std::string(buffer);
        }
        return "";
    }
};

class DatabaseConnection {
private:
    void* connection;  // Simulated database connection
    
public:
    DatabaseConnection() {
        std::cout << "Database connection established\n";
        connection = malloc(100);  // Simulate resource allocation
    }
    
    ~DatabaseConnection() {
        if (connection) {
            free(connection);  // Always freed
            std::cout << "Database connection released\n";
        }
    }
    
    // RAII ensures resource cleanup even with exceptions
    void execute_query(const std::string& query) {
        if (!connection) throw std::runtime_error("No connection");
        
        std::cout << "Executing query: " << query << "\n";
        // Simulate potential exception
        if (query.find("ERROR") != std::string::npos) {
            throw std::runtime_error("Query failed");
        }
    }
};

class LockRAII {
private:
    std::mutex& mtx;
    
public:
    explicit LockRAII(std::mutex& m) : mtx(m) {
        mtx.lock();
        std::cout << "Mutex locked\n";
    }
    
    ~LockRAII() {
        mtx.unlock();
        std::cout << "Mutex unlocked\n";
    }
    
    // Delete copy operations
    LockRAII(const LockRAII&) = delete;
    LockRAII& operator=(const LockRAII&) = delete;
};

void demonstrate_raii() {
    std::cout << "\n=== RAII PATTERN ===\n";
    
    // Example 1: File handling with RAII
    {
        FileRAII file("test.txt", "w");
        file.write("Hello, RAII!");
        file.write("This file will close automatically");
        // File automatically closed when 'file' goes out of scope
    } // Destructor called here
    
    // Example 2: Database connection with exception safety
    try {
        DatabaseConnection db;
        db.execute_query("SELECT * FROM users");
        db.execute_query("INSERT ERROR HERE");  // This will throw
        // Connection still properly closed even with exception
    }
    catch (const std::exception& e) {
        std::cout << "Caught exception: " << e.what() << "\n";
        // Database connection was already cleaned up by destructor!
    }
    
    // Example 3: Mutex locking with RAII
    std::mutex mtx;
    
    {
        LockRAII lock(mtx);  // Lock acquired
        std::cout << "Critical section - doing work\n";
        // Mutex automatically unlocked when lock goes out of scope
    } // Lock released here
    
    // Example 4: Standard library RAII examples
    {
        std::vector<int> vec{1, 2, 3, 4, 5};  // Memory automatically managed
        std::unique_ptr<int> ptr = std::make_unique<int>(42);  // Automatic deletion
        std::lock_guard<std::mutex> lock(mtx);  // Automatic unlocking
        // All resources automatically cleaned up
    }
}

// ============================================================================
// COMPREHENSIVE EXAMPLE
// ============================================================================

class EmployeeDatabase {
private:
    class EmployeeNode {
    public:
        std::string name;
        int id;
        double salary;
        EmployeeNode* next;
        
        EmployeeNode(const std::string& name, int id, double salary)
            : name(name), id(id), salary(salary), next(nullptr) {}
    };
    
    EmployeeNode* head;
    mutable std::mutex db_mutex;  // For thread safety
    
public:
    EmployeeDatabase() : head(nullptr) {
        std::cout << "Employee Database created\n";
    }
    
    ~EmployeeDatabase() {
        std::lock_guard<std::mutex> lock(db_mutex);  // RAII lock
        EmployeeNode* current = head;
        while (current) {
            EmployeeNode* next = current->next;
            delete current;
            current = next;
        }
        std::cout << "Employee Database destroyed\n";
    }
    
    // Add employee with RAII exception safety
    void add_employee(const std::string& name, int id, double salary) {
        std::lock_guard<std::mutex> lock(db_mutex);  // RAII lock
        EmployeeNode* new_node = new EmployeeNode(name, id, salary);
        
        try {
            // Simulate complex operation that might throw
            if (salary < 0) {
                throw std::invalid_argument("Salary cannot be negative");
            }
            
            new_node->next = head;
            head = new_node;
            
            std::cout << "Added employee: " << name << " (ID: " << id << ")\n";
        }
        catch (...) {
            delete new_node;  // Clean up if exception occurs
            throw;
        }
    }
    
    // Const method for displaying employees
    void display_employees() const {
        std::lock_guard<std::mutex> lock(db_mutex);  // RAII lock
        
        std::cout << "\n=== Employee List ===\n";
        EmployeeNode* current = head;
        while (current) {
            std::cout << "ID: " << current->id 
                      << ", Name: " << current->name 
                      << ", Salary: $" << current->salary << "\n";
            current = current->next;
        }
    }
    
    // Method chaining using 'this' pointer
    EmployeeDatabase& set_head(EmployeeNode* new_head) {
        head = new_head;
        return *this;  // Enable chaining
    }
    
    EmployeeDatabase& sort_by_salary() {
        // Implementation omitted for brevity
        return *this;
    }
};

int main() {
    std::cout << "=== COMPREHENSIVE C++ OOP DEMONSTRATION ===\n";
    
    classes_vs_structs();
    
    // BankAccount example
    BankAccount account("123456789", 1000.0);
    account.deposit(500.0);
    account.withdraw(200.0);
    std::cout << "Balance: $" << account.get_balance() << "\n";
    audit_account(account);
    
    demonstrate_constructors();
    
    // TemperatureController - encapsulation
    TemperatureController thermostat;
    thermostat.set_temperature(22.5);
    thermostat.increase_temperature(5.0);
    // thermostat.temperature = 1000;  // ERROR: private member
    
    // Employee - this pointer
    Employee emp("John Doe", 1001, 75000.0);
    emp.set_name("John Smith").set_salary(80000.0);  // Method chaining
    emp.print();
    
    // Inheritance
    Car myCar("Toyota", "Camry", 2022, 4, "Gasoline");
    myCar.display_info();
    myCar.start_engine();
    myCar.open_trunk();
    
    // Polymorphism
    demonstrate_polymorphism();
    
    // Interfaces
    Button btn("Submit", 100, 50);
    btn.draw();
    btn.onClick();
    btn.onHover();
    
    // Abstract classes
    Dog dog("Buddy", 3);
    Bird bird("Tweety", 2, 0.3);
    
    Animal* animals[] = {&dog, &bird};
    for (Animal* animal : animals) {
        animal->display_info();
        animal->make_sound();
        animal->move();
        animal->eat();
    }
    
    // RAII
    demonstrate_raii();
    
    // Comprehensive example
    EmployeeDatabase db;
    db.add_employee("Alice", 1001, 60000)
      .add_employee("Bob", 1002, 75000)
      .add_employee("Charlie", 1003, 80000);
    db.display_employees();
    
    std::cout << "\n=== ALL DEMONSTRATIONS COMPLETED ===\n";
    return 0;
}