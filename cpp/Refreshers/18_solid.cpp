#include <iostream>
#include <string>
#include <memory>
#include <fstream>

// ============================================================================
// SEPARATE CLASSES EACH WITH SINGLE RESPONSIBILITY
// ============================================================================

// Responsibility 1: Represent employee data
class Employee {
private:
    std::string name;
    double salary;
    std::string department;
    
public:
    Employee(const std::string& n, double s, const std::string& d)
        : name(n), salary(s), department(d) {}
    
    // Getters for data access
    const std::string& getName() const { return name; }
    double getSalary() const { return salary; }
    const std::string& getDepartment() const { return department; }
    
    // Business logic related to employee state
    void setSalary(double newSalary) { salary = newSalary; }
    void setDepartment(const std::string& newDept) { department = newDept; }
    
    // Only methods that directly relate to employee data
    double calculateBonus(double percentage) const {
        return salary * percentage / 100.0;
    }
};

// Responsibility 2: Persistence - save/load employees
class EmployeeRepository {
public:
    void saveToFile(const Employee& emp, const std::string& filename) {
        std::ofstream file(filename, std::ios::app);  // Append mode
        if (file) {
            file << emp.getName() << "," 
                 << emp.getSalary() << "," 
                 << emp.getDepartment() << "\n";
            std::cout << "Employee saved to file: " << filename << "\n";
        }
    }
    
    std::vector<Employee> loadFromFile(const std::string& filename) {
        std::vector<Employee> employees;
        std::ifstream file(filename);
        std::string line;
        
        while (std::getline(file, line)) {
            // Parse CSV line
            size_t pos1 = line.find(',');
            size_t pos2 = line.find(',', pos1 + 1);
            
            if (pos1 != std::string::npos && pos2 != std::string::npos) {
                std::string name = line.substr(0, pos1);
                double salary = std::stod(line.substr(pos1 + 1, pos2 - pos1 - 1));
                std::string dept = line.substr(pos2 + 1);
                
                employees.emplace_back(name, salary, dept);
            }
        }
        return employees;
    }
};

// Responsibility 3: Generate reports
class ReportGenerator {
public:
    void generateEmployeeReport(const Employee& emp) {
        std::cout << "\n=== Employee Report ===\n";
        std::cout << "Name: " << emp.getName() << "\n";
        std::cout << "Salary: $" << emp.getSalary() << "\n";
        std::cout << "Department: " << emp.getDepartment() << "\n";
        std::cout << "Bonus (10%): $" << emp.calculateBonus(10) << "\n";
        std::cout << "======================\n";
    }
    
    void generateDepartmentReport(const std::vector<Employee>& employees) {
        std::map<std::string, double> deptSalaries;
        
        for (const auto& emp : employees) {
            deptSalaries[emp.getDepartment()] += emp.getSalary();
        }
        
        std::cout << "\n=== Department Salary Report ===\n";
        for (const auto& [dept, total] : deptSalaries) {
            std::cout << dept << ": $" << total << "\n";
        }
        std::cout << "================================\n";
    }
};

// Responsibility 4: Handle notifications
class EmailService {
public:
    void sendPromotionEmail(const Employee& emp, double oldSalary) {
        std::cout << "\n=== Promotion Email ===\n";
        std::cout << "To: " << emp.getName() << "@company.com\n";
        std::cout << "Subject: Congratulations on Your Promotion!\n";
        std::cout << "Body: Dear " << emp.getName() << ",\n";
        std::cout << "Congratulations! Your salary has been increased ";
        std::cout << "from $" << oldSalary << " to $" << emp.getSalary() << ".\n";
        std::cout << "Best regards,\nHR Department\n";
        std::cout << "=========================\n";
    }
    
    void sendBirthdayEmail(const Employee& emp) {
        std::cout << "\n=== Birthday Email ===\n";
        std::cout << "To: " << emp.getName() << "@company.com\n";
        std::cout << "Subject: Happy Birthday!\n";
        std::cout << "Body: Happy Birthday " << emp.getName() << "!\n";
        std::cout << "Wishing you a wonderful day!\n";
        std::cout << "=========================\n";
    }
};

// Responsibility 5: Employee management (orchestrates other classes)
class EmployeeService {
private:
    EmployeeRepository repository;
    ReportGenerator reporter;
    EmailService emailService;
    
public:
    void promoteEmployee(Employee& emp, double raisePercentage) {
        double oldSalary = emp.getSalary();
        double newSalary = oldSalary * (1 + raisePercentage / 100.0);
        emp.setSalary(newSalary);
        
        // Use specialized services
        reporter.generateEmployeeReport(emp);
        emailService.sendPromotionEmail(emp, oldSalary);
        repository.saveToFile(emp, "promotions.csv");
        
        std::cout << "\nPromotion completed successfully!\n";
    }
    
    void processBirthdays(const std::vector<Employee>& employees) {
        std::cout << "\nProcessing birthdays...\n";
        for (const auto& emp : employees) {
            emailService.sendBirthdayEmail(emp);
        }
    }
};

void demonstrate_srp_correct() {
    std::cout << "\n=== SINGLE RESPONSIBILITY PRINCIPLE ===\n";
    
    // Create employee
    Employee john("John Doe", 50000, "Engineering");
    Employee jane("Jane Smith", 60000, "Marketing");
    
    // Create services
    EmployeeService empService;
    ReportGenerator reporter;
    EmployeeRepository repository;
    
    // Demonstrate SRP in action
    std::cout << "\n1. Employee operations:\n";
    double bonus = john.calculateBonus(15);
    std::cout << "John's bonus: $" << bonus << "\n";
    
    std::cout << "\n2. Reporting:\n";
    reporter.generateEmployeeReport(john);
    
    std::cout << "\n3. Persistence:\n";
    repository.saveToFile(john, "employees.csv");
    
    std::cout << "\n4. Promotion workflow:\n";
    empService.promoteEmployee(jane, 10);
    
    std::cout << "\n5. Department report:\n";
    std::vector<Employee> employees = {john, jane};
    reporter.generateDepartmentReport(employees);
}

// ============================================================================
// BENEFITS OF SRP
// ============================================================================

/*
Benefits of Single Responsibility Principle:

1. **Easier to Understand**: Each class does one thing
2. **Easier to Maintain**: Changes are isolated
3. **Easier to Test**: Each class can be tested independently
4. **Lower Coupling**: Classes don't depend on unrelated functionality
5. **Better Reusability**: Small, focused classes can be reused more easily

Example: If we need to change:
- Email format → Change only EmailService
- Report format → Change only ReportGenerator  
- Storage method → Change only EmployeeRepository
- Business logic → Change only Employee or EmployeeService
*/



#include <iostream>
#include <memory>
#include <vector>

// ============================================================================
// OCP COMPLIANT DESIGN USING ABSTRACTION
// ============================================================================

// Step 1: Define abstract interface (closed for modification)
class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;  // Pure virtual - must be implemented
    virtual std::string name() const = 0;
};

// Step 2: Concrete implementations (extensions, not modifications)
class Circle : public Shape {
private:
    double radius;
    
public:
    Circle(double r) : radius(r) {}
    
    double area() const override {
        return 3.14159 * radius * radius;
    }
    
    std::string name() const override {
        return "Circle";
    }
};

class Square : public Shape {
private:
    double side;
    
public:
    Square(double s) : side(s) {}
    
    double area() const override {
        return side * side;
    }
    
    std::string name() const override {
        return "Square";
    }
};

class Rectangle : public Shape {
private:
    double width, height;
    
public:
    Rectangle(double w, double h) : width(w), height(h) {}
    
    double area() const override {
        return width * height;
    }
    
    std::string name() const override {
        return "Rectangle";
    }
};

// NEW: Adding new shape doesn't require modifying existing code!
class Triangle : public Shape {
private:
    double base, height;
    
public:
    Triangle(double b, double h) : base(b), height(h) {}
    
    double area() const override {
        return 0.5 * base * height;
    }
    
    std::string name() const override {
        return "Triangle";
    }
};

// Step 3: Calculator that works with any Shape (closed for modification)
class AreaCalculator {
public:
    double calculateTotalArea(const std::vector<std::shared_ptr<Shape>>& shapes) {
        double total = 0;
        
        for (const auto& shape : shapes) {
            total += shape->area();
            std::cout << shape->name() << " area: " << shape->area() << "\n";
        }
        
        return total;
    }
    
    // We can add new methods without breaking existing functionality
    void printShapesInfo(const std::vector<std::shared_ptr<Shape>>& shapes) {
        std::cout << "\n=== Shapes Information ===\n";
        for (const auto& shape : shapes) {
            std::cout << shape->name() << ": Area = " << shape->area() << "\n";
        }
    }
};

// ============================================================================
// ANOTHER EXAMPLE: DISCOUNT STRATEGY PATTERN
// ============================================================================

// Abstract discount strategy
class DiscountStrategy {
public:
    virtual ~DiscountStrategy() = default;
    virtual double calculateDiscount(double amount) const = 0;
    virtual std::string getDescription() const = 0;
};

// Concrete strategies
class RegularCustomerDiscount : public DiscountStrategy {
public:
    double calculateDiscount(double amount) const override {
        return amount * 0.1;  // 10%
    }
    
    std::string getDescription() const override {
        return "Regular Customer (10% discount)";
    }
};

class PremiumCustomerDiscount : public DiscountStrategy {
public:
    double calculateDiscount(double amount) const override {
        return amount * 0.2;  // 20%
    }
    
    std::string getDescription() const override {
        return "Premium Customer (20% discount)";
    }
};

class VipCustomerDiscount : public DiscountStrategy {
public:
    double calculateDiscount(double amount) const override {
        return amount * 0.3;  // 30%
    }
    
    std::string getDescription() const override {
        return "VIP Customer (30% discount)";
    }
};

// NEW: Adding new discount type is easy!
class EmployeeDiscount : public DiscountStrategy {
public:
    double calculateDiscount(double amount) const override {
        return amount * 0.4;  // 40%
    }
    
    std::string getDescription() const override {
        return "Employee (40% discount)";
    }
};

// Calculator that uses strategies (closed for modification)
class OrderProcessor {
public:
    double processOrder(double amount, const DiscountStrategy& strategy) {
        double discount = strategy.calculateDiscount(amount);
        double finalAmount = amount - discount;
        
        std::cout << "\n=== Order Processing ===\n";
        std::cout << "Amount: $" << amount << "\n";
        std::cout << "Discount Type: " << strategy.getDescription() << "\n";
        std::cout << "Discount: $" << discount << "\n";
        std::cout << "Final Amount: $" << finalAmount << "\n";
        
        return finalAmount;
    }
    
    // We can extend functionality without modifying existing code
    void processMultipleOrders(const std::vector<std::pair<double, DiscountStrategy*>>& orders) {
        std::cout << "\n=== Batch Order Processing ===\n";
        double totalDiscount = 0;
        
        for (const auto& [amount, strategy] : orders) {
            double discount = strategy->calculateDiscount(amount);
            totalDiscount += discount;
            std::cout << strategy->getDescription() << " on $" << amount 
                      << ": $" << discount << " discount\n";
        }
        
        std::cout << "Total discount given: $" << totalDiscount << "\n";
    }
};

// ============================================================================
// TEMPLATE METHOD PATTERN FOR OCP
// ============================================================================

// Base class with template method (closed for modification)
class ReportGenerator {
protected:
    // These steps can be overridden by subclasses
    virtual std::string generateHeader() const {
        return "=== Report ===\n";
    }
    
    virtual std::string generateBody() const = 0;  // Must be implemented
    
    virtual std::string generateFooter() const {
        return "==============\n";
    }
    
public:
    // Template method - fixed algorithm
    std::string generateReport() const {
        std::string report;
        report += generateHeader();
        report += generateBody();
        report += generateFooter();
        return report;
    }
    
    virtual ~ReportGenerator() = default;
};

// Extensions (open for extension)
class SalesReport : public ReportGenerator {
protected:
    std::string generateBody() const override {
        return "Sales: $100,000\nProfit: $25,000\n";
    }
    
    std::string generateHeader() const override {
        return "=== SALES REPORT ===\nDate: 2024-01-15\n";
    }
};

class InventoryReport : public ReportGenerator {
protected:
    std::string generateBody() const override {
        return "Items in stock: 1,250\nLow stock items: 15\n";
    }
    
    // Can also add new methods
    std::string generateRecommendations() const {
        return "Recommended actions: Reorder items #101, #205, #309\n";
    }
};

// ============================================================================
// VISITOR PATTERN FOR OCP
// ============================================================================

// Visitor interface
class ShapeVisitor {
public:
    virtual ~ShapeVisitor() = default;
    virtual void visit(const Circle& circle) = 0;
    virtual void visit(const Square& square) = 0;
    virtual void visit(const Rectangle& rectangle) = 0;
    // Adding new shape requires adding new visit method
    // But existing visitors don't need to change if they provide default
};

// Concrete visitors
class AreaVisitor : public ShapeVisitor {
private:
    double totalArea = 0;
    
public:
    void visit(const Circle& circle) override {
        totalArea += circle.area();
    }
    
    void visit(const Square& square) override {
        totalArea += square.area();
    }
    
    void visit(const Rectangle& rectangle) override {
        totalArea += rectangle.area();
    }
    
    double getTotalArea() const { return totalArea; }
};

class PrintVisitor : public ShapeVisitor {
public:
    void visit(const Circle& circle) override {
        std::cout << "Visiting Circle with area: " << circle.area() << "\n";
    }
    
    void visit(const Square& square) override {
        std::cout << "Visiting Square with area: " << square.area() << "\n";
    }
    
    void visit(const Rectangle& rectangle) override {
        std::cout << "Visiting Rectangle with area: " << rectangle.area() << "\n";
    }
};

void demonstrate_ocp_correct() {
    std::cout << "\n=== OPEN/CLOSED PRINCIPLE ===\n";
    
    // 1. Shape example
    std::cout << "\n1. Shape Area Calculation:\n";
    
    std::vector<std::shared_ptr<Shape>> shapes;
    shapes.push_back(std::make_shared<Circle>(5.0));
    shapes.push_back(std::make_shared<Square>(4.0));
    shapes.push_back(std::make_shared<Rectangle>(3.0, 6.0));
    shapes.push_back(std::make_shared<Triangle>(4.0, 3.0));  // New shape!
    
    AreaCalculator calculator;
    double totalArea = calculator.calculateTotalArea(shapes);
    std::cout << "\nTotal area: " << totalArea << "\n";
    
    // 2. Discount example
    std::cout << "\n2. Discount Strategies:\n";
    
    OrderProcessor orderProcessor;
    RegularCustomerDiscount regular;
    PremiumCustomerDiscount premium;
    VipCustomerDiscount vip;
    EmployeeDiscount employee;  // New discount type!
    
    orderProcessor.processOrder(100.0, regular);
    orderProcessor.processOrder(100.0, vip);
    orderProcessor.processOrder(100.0, employee);  // Works without modifying OrderProcessor
    
    // 3. Report generation
    std::cout << "\n3. Report Generation:\n";
    
    SalesReport salesReport;
    InventoryReport inventoryReport;
    
    std::cout << "\nSales Report:\n" << salesReport.generateReport();
    std::cout << "\nInventory Report:\n" << inventoryReport.generateReport();
    
    // 4. Visitor pattern
    std::cout << "\n4. Visitor Pattern:\n";
    
    Circle circle(3);
    Square square(4);
    Rectangle rectangle(3, 5);
    
    AreaVisitor areaVisitor;
    PrintVisitor printVisitor;
    
    // Simulating accept() calls (normally shapes would have accept() method)
    areaVisitor.visit(circle);
    areaVisitor.visit(square);
    areaVisitor.visit(rectangle);
    
    std::cout << "Visitor calculated total area: " << areaVisitor.getTotalArea() << "\n";
}

// ============================================================================
// BENEFITS OF OCP
// ============================================================================

/*
Benefits of Open/Closed Principle:

1. **Stability**: Core functionality doesn't change
2. **Extensibility**: Easy to add new features
3. **Maintainability**: Changes are isolated in new code
4. **Testability**: Existing code doesn't need re-testing
5. **Scalability**: System grows organically

Common patterns for OCP:
1. **Strategy Pattern**: Different algorithms for same interface
2. **Template Method**: Skeleton algorithm with customizable steps
3. **Visitor Pattern**: Operations on object structure
4. **Decorator Pattern**: Add responsibilities dynamically
5. **Abstract Factory**: Create families of related objects

Key Insight:
- Use abstraction (interfaces, abstract classes)
- Depend on abstractions, not concretions
- New functionality = new classes, not modified classes
*/


#include <iostream>
#include <memory>
#include <vector>
#include <cmath>

// ============================================================================
// LSP COMPLIANT DESIGNS
// ============================================================================

// SOLUTION 1: Separate hierarchies for different behaviors
class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;
    virtual std::string getName() const = 0;
};

class Rectangle : public Shape {
protected:
    double width, height;
    
public:
    Rectangle(double w, double h) : width(w), height(h) {}
    
    void setWidth(double w) { width = w; }
    void setHeight(double h) { height = h; }
    
    double getWidth() const { return width; }
    double getHeight() const { return height; }
    
    double area() const override {
        return width * height;
    }
    
    std::string getName() const override {
        return "Rectangle";
    }
};

class Square : public Shape {
private:
    double side;
    
public:
    Square(double s) : side(s) {}
    
    void setSide(double s) { side = s; }
    double getSide() const { return side; }
    
    double area() const override {
        return side * side;
    }
    
    std::string getName() const override {
        return "Square";
    }
};

// Function works with any Shape
void printShapeInfo(const Shape& shape) {
    std::cout << shape.getName() << " area: " << shape.area() << "\n";
}

// SOLUTION 2: Interface segregation (see ISP section)
class IFlyable {
public:
    virtual ~IFlyable() = default;
    virtual void fly() = 0;
    virtual double getAirSpeed() const = 0;
};

class ISwimmable {
public:
    virtual ~ISwimmable() = default;
    virtual void swim() = 0;
    virtual double getSwimSpeed() const = 0;
};

class Bird {
public:
    virtual ~Bird() = default;
    virtual std::string getName() const = 0;
    virtual void makeSound() const = 0;
};

class Sparrow : public Bird, public IFlyable {
public:
    std::string getName() const override {
        return "Sparrow";
    }
    
    void makeSound() const override {
        std::cout << "Chirp chirp!\n";
    }
    
    void fly() override {
        std::cout << "Sparrow is flying gracefully\n";
    }
    
    double getAirSpeed() const override {
        return 15.0;
    }
};

class Penguin : public Bird, public ISwimmable {
public:
    std::string getName() const override {
        return "Penguin";
    }
    
    void makeSound() const override {
        std::cout << "Honk honk!\n";
    }
    
    void swim() override {
        std::cout << "Penguin is swimming swiftly\n";
    }
    
    double getSwimSpeed() const override {
        return 8.0;
    }
};

// Functions work with specific capabilities
void processFlyingBird(IFlyable& flyer) {
    flyer.fly();
    std::cout << "Speed: " << flyer.getAirSpeed() << " km/h\n";
}

void processSwimmingBird(ISwimmable& swimmer) {
    swimmer.swim();
    std::cout << "Speed: " << swimmer.getSwimSpeed() << " km/h\n";
}

// SOLUTION 3: Account hierarchy with proper contracts
class Account {
protected:
    double balance;
    
public:
    Account(double initial) : balance(initial) {}
    virtual ~Account() = default;
    
    double getBalance() const { return balance; }
    
    // Clear contract: can always get balance
    virtual bool canWithdraw(double amount) const {
        return amount > 0 && amount <= balance;
    }
    
    // Returns success/failure, doesn't throw
    virtual bool withdraw(double amount) {
        if (canWithdraw(amount)) {
            balance -= amount;
            return true;
        }
        return false;
    }
    
    virtual void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }
};

class CheckingAccount : public Account {
public:
    CheckingAccount(double initial) : Account(initial) {}
    
    // Can add overdraft protection
    bool canWithdraw(double amount) const override {
        // Allow overdraft up to 500
        return amount > 0 && amount <= (balance + 500);
    }
};

class SavingsAccount : public Account {
private:
    int withdrawalLimit;
    int withdrawalsThisMonth;
    
public:
    SavingsAccount(double initial) 
        : Account(initial), withdrawalLimit(5), withdrawalsThisMonth(0) {}
    
    bool canWithdraw(double amount) const override {
        return amount > 0 && 
               amount <= balance && 
               withdrawalsThisMonth < withdrawalLimit;
    }
    
    bool withdraw(double amount) override {
        if (Account::withdraw(amount)) {
            withdrawalsThisMonth++;
            return true;
        }
        return false;
    }
    
    void resetWithdrawalCount() {
        withdrawalsThisMonth = 0;
    }
};

// Function works with any Account
void processAccount(Account& account) {
    std::cout << "Current balance: $" << account.getBalance() << "\n";
    
    double amount = 100;
    if (account.canWithdraw(amount)) {
        bool success = account.withdraw(amount);
        std::cout << "Withdrawal of $" << amount 
                  << (success ? " succeeded" : " failed") << "\n";
    } else {
        std::cout << "Cannot withdraw $" << amount << "\n";
    }
    
    std::cout << "New balance: $" << account.getBalance() << "\n\n";
}

// SOLUTION 4: Covariant return types (C++ allows this correctly)
class Animal {
public:
    virtual ~Animal() = default;
    virtual Animal* clone() const = 0;
    virtual std::string speak() const = 0;
};

class Dog : public Animal {
public:
    // Covariant return type - allowed in C++
    Dog* clone() const override {
        return new Dog(*this);
    }
    
    std::string speak() const override {
        return "Woof!";
    }
};

class Cat : public Animal {
public:
    Cat* clone() const override {
        return new Cat(*this);
    }
    
    std::string speak() const override {
        return "Meow!";
    }
};

void demonstrate_lsp_correct() {
    std::cout << "\n=== LISKOV SUBSTITUTION PRINCIPLE ===\n";
    
    // Example 1: Shapes
    std::cout << "\n1. Shape Hierarchy (LSP Compliant):\n";
    
    Rectangle rect(5, 10);
    Square square(5);
    
    printShapeInfo(rect);
    printShapeInfo(square);  // Both work as Shapes
    
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Rectangle>(3, 4));
    shapes.push_back(std::make_unique<Square>(5));
    
    std::cout << "\nProcessing shapes collection:\n";
    for (const auto& shape : shapes) {
        printShapeInfo(*shape);
    }
    
    // Example 2: Birds with capabilities
    std::cout << "\n2. Bird Hierarchy with Interfaces:\n";
    
    Sparrow sparrow;
    Penguin penguin;
    
    std::cout << "Sparrow:\n";
    sparrow.makeSound();
    processFlyingBird(sparrow);  // Only works with IFlyable
    
    std::cout << "\nPenguin:\n";
    penguin.makeSound();
    processSwimmingBird(penguin);  // Only works with ISwimmable
    
    // Both are Birds
    std::vector<std::unique_ptr<Bird>> birds;
    birds.push_back(std::make_unique<Sparrow>());
    birds.push_back(std::make_unique<Penguin>());
    
    std::cout << "\nBird sounds:\n";
    for (const auto& bird : birds) {
        std::cout << bird->getName() << " says: ";
        bird->makeSound();
    }
    
    // Example 3: Accounts
    std::cout << "\n3. Account Hierarchy:\n";
    
    CheckingAccount checking(1000);
    SavingsAccount savings(2000);
    
    std::cout << "Checking Account:\n";
    processAccount(checking);
    
    std::cout << "Savings Account:\n";
    processAccount(savings);
    
    // Can process both through Account reference
    std::vector<std::reference_wrapper<Account>> accounts = {checking, savings};
    std::cout << "Processing all accounts:\n";
    for (auto& account : accounts) {
        processAccount(account);
    }
    
    // Example 4: Covariant returns
    std::cout << "\n4. Covariant Return Types:\n";
    
    Dog dog;
    Cat cat;
    
    Animal* animals[] = {&dog, &cat};
    
    for (Animal* animal : animals) {
        Animal* clone = animal->clone();
        std::cout << "Original: " << animal->speak() << "\n";
        std::cout << "Clone: " << clone->speak() << "\n";
        delete clone;
    }
}

// ============================================================================
// LSP RULES AND GUIDELINES
// ============================================================================

/*
Liskov Substitution Principle Rules:

1. **Signature Rule**: Methods must match
   - Same parameter types
   - Same or covariant return types
   - Same or weaker exceptions

2. **Methods Rule**: Methods must behave consistently
   - Cannot strengthen preconditions
   - Cannot weaken postconditions
   - Must preserve invariants

3. **Properties Rule**: Properties must be preserved
   - History constraint: Subclass can't allow states disallowed by superclass
   - Subclass methods must not violate superclass constraints

Common LSP Violations to Avoid:

1. **Type Checking**: if (type == "Square") 
2. **Throwing Unexpected Exceptions**: Base doesn't throw, subclass throws
3. **Changing Return Types**: Base returns int, subclass returns string
4. **Weakening Invariants**: Base ensures X > 0, subclass allows X = 0
5. **Strengthening Preconditions**: Base accepts any int, subclass requires positive
6. **Weakening Postconditions**: Base ensures non-null, subclass allows null
7. **Empty Overrides**: Subclass overrides with empty implementation

Testing for LSP:
1. Write unit tests for base class behavior
2. Run same tests with subclass instances
3. All tests should pass without modification
*/


#include <iostream>
#include <memory>
#include <vector>

// ============================================================================
// ISP COMPLIANT DESIGNS
// ============================================================================

// SOLUTION 1: Segregated worker interfaces
class IOfficeWork {
public:
    virtual ~IOfficeWork() = default;
    virtual void workOnComputer() = 0;
    virtual void attendMeeting() = 0;
    virtual void writeReport() = 0;
};

class IFactoryWork {
public:
    virtual ~IFactoryWork() = default;
    virtual void operateMachine() = 0;
    virtual void assembleProduct() = 0;
    virtual void performQualityCheck() = 0;
};

class IDeliveryWork {
public:
    virtual ~IDeliveryWork() = default;
    virtual void driveVehicle() = 0;
    virtual void loadPackages() = 0;
    virtual void deliverPackages() = 0;
};

class IManagementWork {
public:
    virtual ~IManagementWork() = default;
    virtual void manageTeam() = 0;
    virtual void approveExpenses() = 0;
    virtual void conductInterview() = 0;
};

// Concrete classes implement only what they need
class OfficeWorker : public IOfficeWork {
public:
    void workOnComputer() override {
        std::cout << "Office worker: Working on computer\n";
    }
    
    void attendMeeting() override {
        std::cout << "Office worker: Attending meeting\n";
    }
    
    void writeReport() override {
        std::cout << "Office worker: Writing report\n";
    }
};

class FactoryWorker : public IFactoryWork {
public:
    void operateMachine() override {
        std::cout << "Factory worker: Operating machine\n";
    }
    
    void assembleProduct() override {
        std::cout << "Factory worker: Assembling product\n";
    }
    
    void performQualityCheck() override {
        std::cout << "Factory worker: Performing quality check\n";
    }
};

class DeliveryWorker : public IDeliveryWork {
public:
    void driveVehicle() override {
        std::cout << "Delivery worker: Driving vehicle\n";
    }
    
    void loadPackages() override {
        std::cout << "Delivery worker: Loading packages\n";
    }
    
    void deliverPackages() override {
        std::cout << "Delivery worker: Delivering packages\n";
    }
};

// Workers can implement multiple interfaces
class Supervisor : public IOfficeWork, public IManagementWork {
public:
    // Office work
    void workOnComputer() override {
        std::cout << "Supervisor: Working on computer\n";
    }
    
    void attendMeeting() override {
        std::cout << "Supervisor: Attending meeting\n";
    }
    
    void writeReport() override {
        std::cout << "Supervisor: Writing report\n";
    }
    
    // Management work
    void manageTeam() override {
        std::cout << "Supervisor: Managing team\n";
    }
    
    void approveExpenses() override {
        std::cout << "Supervisor: Approving expenses\n";
    }
    
    void conductInterview() override {
        std::cout << "Supervisor: Conducting interview\n";
    }
};

// SOLUTION 2: Printer interfaces
class IPrinter {
public:
    virtual ~IPrinter() = default;
    virtual void print(const std::string& document) = 0;
};

class IColorPrinter : public IPrinter {
public:
    virtual void printColor(const std::string& document) = 0;
};

class IDuplexPrinter : public IPrinter {
public:
    virtual void printDuplex(const std::string& document) = 0;
};

class IScanner {
public:
    virtual ~IScanner() = default;
    virtual void scan(const std::string& document) = 0;
};

class IAdvancedScanner : public IScanner {
public:
    virtual void scanToEmail(const std::string& document) = 0;
    virtual void scanToCloud(const std::string& document) = 0;
};

class IFaxMachine {
public:
    virtual ~IFaxMachine() = default;
    virtual void fax(const std::string& document) = 0;
    virtual void receiveFax() = 0;
};

class ICopier {
public:
    virtual ~ICopier() = default;
    virtual void copy(const std::string& document) = 0;
};

class IColorCopier : public ICopier {
public:
    virtual void copyColor(const std::string& document) = 0;
};

class IMaintenance {
public:
    virtual ~IMaintenance() = default;
    virtual void calibrate() = 0;
    virtual void cleanPrintHeads() = 0;
    virtual void replaceInk() = 0;
};

// Concrete devices implement only what they support
class SimplePrinter : public IPrinter, public IMaintenance {
public:
    void print(const std::string& document) override {
        std::cout << "Simple printer printing: " << document << "\n";
    }
    
    void calibrate() override {
        std::cout << "Simple printer: Calibrating\n";
    }
    
    void cleanPrintHeads() override {
        // No print heads to clean
    }
    
    void replaceInk() override {
        std::cout << "Simple printer: Replacing ink cartridge\n";
    }
};

class OfficePrinter : public IPrinter, public IScanner, public ICopier, public IMaintenance {
public:
    void print(const std::string& document) override {
        std::cout << "Office printer printing: " << document << "\n";
    }
    
    void scan(const std::string& document) override {
        std::cout << "Office printer scanning: " << document << "\n";
    }
    
    void copy(const std::string& document) override {
        std::cout << "Office printer copying: " << document << "\n";
    }
    
    void calibrate() override {
        std::cout << "Office printer: Calibrating\n";
    }
    
    void cleanPrintHeads() override {
        std::cout << "Office printer: Cleaning print heads\n";
    }
    
    void replaceInk() override {
        std::cout << "Office printer: Replacing ink\n";
    }
};

class AllInOnePrinter : public IColorPrinter, 
                        public IDuplexPrinter,
                        public IAdvancedScanner,
                        public IFaxMachine,
                        public IColorCopier,
                        public IMaintenance {
public:
    // Printing
    void print(const std::string& document) override {
        std::cout << "All-in-one printing: " << document << "\n";
    }
    
    void printColor(const std::string& document) override {
        std::cout << "All-in-one printing color: " << document << "\n";
    }
    
    void printDuplex(const std::string& document) override {
        std::cout << "All-in-one printing duplex: " << document << "\n";
    }
    
    // Scanning
    void scan(const std::string& document) override {
        std::cout << "All-in-one scanning: " << document << "\n";
    }
    
    void scanToEmail(const std::string& document) override {
        std::cout << "All-in-one scanning to email: " << document << "\n";
    }
    
    void scanToCloud(const std::string& document) override {
        std::cout << "All-in-one scanning to cloud: " << document << "\n";
    }
    
    // Fax
    void fax(const std::string& document) override {
        std::cout << "All-in-one faxing: " << document << "\n";
    }
    
    void receiveFax() override {
        std::cout << "All-in-one receiving fax\n";
    }
    
    // Copying
    void copy(const std::string& document) override {
        std::cout << "All-in-one copying: " << document << "\n";
    }
    
    void copyColor(const std::string& document) override {
        std::cout << "All-in-one copying color: " << document << "\n";
    }
    
    // Maintenance
    void calibrate() override {
        std::cout << "All-in-one: Calibrating\n";
    }
    
    void cleanPrintHeads() override {
        std::cout << "All-in-one: Cleaning print heads\n";
    }
    
    void replaceInk() override {
        std::cout << "All-in-one: Replacing ink\n";
    }
};

// SOLUTION 3: Notification system
class IEmailNotifier {
public:
    virtual ~IEmailNotifier() = default;
    virtual void sendEmail(const std::string& to, const std::string& subject, 
                          const std::string& body) = 0;
};

class ISmsNotifier {
public:
    virtual ~ISmsNotifier() = default;
    virtual void sendSms(const std::string& phoneNumber, const std::string& message) = 0;
};

class IPushNotifier {
public:
    virtual ~IPushNotifier() = default;
    virtual void sendPushNotification(const std::string& deviceId, 
                                     const std::string& message) = 0;
};

class IAudioNotifier {
public:
    virtual ~IAudioNotifier() = default;
    virtual void playSound(const std::string& sound) = 0;
};

// Clients use only what they need
class EmailService : public IEmailNotifier {
public:
    void sendEmail(const std::string& to, const std::string& subject, 
                  const std::string& body) override {
        std::cout << "Sending email to: " << to << "\n";
        std::cout << "Subject: " << subject << "\n";
        std::cout << "Body: " << body << "\n";
    }
};

class MobileApp : public IPushNotifier, public IAudioNotifier {
public:
    void sendPushNotification(const std::string& deviceId, 
                             const std::string& message) override {
        std::cout << "Sending push to device: " << deviceId << "\n";
        std::cout << "Message: " << message << "\n";
    }
    
    void playSound(const std::string& sound) override {
        std::cout << "Playing sound: " << sound << "\n";
    }
};

class EmergencySystem : public ISmsNotifier, public IAudioNotifier {
public:
    void sendSms(const std::string& phoneNumber, const std::string& message) override {
        std::cout << "Sending SMS to: " << phoneNumber << "\n";
        std::cout << "Message: " << message << "\n";
    }
    
    void playSound(const std::string& sound) override {
        std::cout << "Playing emergency sound: " << sound << "\n";
    }
};

// Functions depend on specific interfaces, not general ones
void processOfficeWork(IOfficeWork& worker) {
    worker.workOnComputer();
    worker.attendMeeting();
    worker.writeReport();
}

void sendImportantNotification(IEmailNotifier& notifier) {
    notifier.sendEmail("boss@company.com", "Important Update", "Project completed!");
}

void alertUser(IAudioNotifier& notifier) {
    notifier.playSound("alert.wav");
}

void demonstrate_isp_correct() {
    std::cout << "\n=== INTERFACE SEGREGATION PRINCIPLE ===\n";
    
    // Example 1: Workers
    std::cout << "\n1. Worker Interfaces:\n";
    
    OfficeWorker officeWorker;
    FactoryWorker factoryWorker;
    DeliveryWorker deliveryWorker;
    Supervisor supervisor;
    
    std::cout << "\nOffice worker tasks:\n";
    processOfficeWork(officeWorker);
    
    std::cout << "\nSupervisor tasks:\n";
    processOfficeWork(supervisor);
    supervisor.manageTeam();
    
    // Example 2: Printers
    std::cout << "\n2. Printer Interfaces:\n";
    
    SimplePrinter simplePrinter;
    OfficePrinter officePrinter;
    AllInOnePrinter allInOne;
    
    std::cout << "\nSimple printer:\n";
    simplePrinter.print("Simple document");
    simplePrinter.replaceInk();
    
    std::cout << "\nOffice printer:\n";
    officePrinter.print("Office document");
    officePrinter.scan("Scanned document");
    officePrinter.copy("Copied document");
    
    std::cout << "\nAll-in-one printer:\n";
    allInOne.printColor("Color document");
    allInOne.scanToEmail("Document to email");
    allInOne.fax("Fax document");
    allInOne.copyColor("Color copy");
    
    // Example 3: Notifications
    std::cout << "\n3. Notification Interfaces:\n";
    
    EmailService emailService;
    MobileApp mobileApp;
    EmergencySystem emergencySystem;
    
    std::cout << "\nSending email:\n";
    sendImportantNotification(emailService);
    
    std::cout << "\nMobile app alerts:\n";
    mobileApp.sendPushNotification("device123", "You have a new message");
    alertUser(mobileApp);
    
    std::cout << "\nEmergency system:\n";
    emergencySystem.sendSms("+1234567890", "Emergency alert!");
    alertUser(emergencySystem);
    
    // Example 4: Using interfaces in collections
    std::cout << "\n4. Interface Collections:\n";
    
    std::vector<IPrinter*> printers = {&simplePrinter, &officePrinter, &allInOne};
    std::vector<IAudioNotifier*> notifiers = {&mobileApp, &emergencySystem};
    
    std::cout << "\nPrinting with all printers:\n";
    for (auto printer : printers) {
        printer->print("Batch document");
    }
    
    std::cout << "\nAlerting with all notifiers:\n";
    for (auto notifier : notifiers) {
        notifier->playSound("notification.wav");
    }
}

// ============================================================================
// BENEFITS AND GUIDELINES
// ============================================================================

/*
Benefits of Interface Segregation Principle:

1. **Reduced Coupling**: Clients depend only on what they use
2. **Better Cohesion**: Interfaces have single, focused purposes
3. **Easier Maintenance**: Changes affect fewer clients
4. **Improved Testability**: Can mock smaller interfaces
5. **Clearer Contracts**: Interfaces document exact capabilities

How to Apply ISP:

1. **Identify Client Needs**: What does each client actually use?
2. **Split Large Interfaces**: Break "god interfaces" into focused ones
3. **Use Multiple Inheritance**: C++ supports implementing multiple interfaces
4. **Apply YAGNI**: Don't add methods "just in case"
5. **Review Regularly**: Refactor as client needs change

Signs of ISP Violation:

1. **Empty Method Implementations**: throw or do nothing
2. **"NotImplemented" Comments**: Methods that aren't relevant
3. **Client-Specific Methods**: Some clients use only subset of methods
4. **Frequent Interface Changes**: Adding methods for specific clients

Remember: Many small interfaces > One large interface
*/


#include <iostream>
#include <memory>
#include <vector>
#include <functional>

// ============================================================================
// DIP COMPLIANT DESIGNS
// ============================================================================

// ============================================================================
// 1. REPORT GENERATOR EXAMPLE
// ============================================================================

// Abstraction (interface)
class IReportWriter {
public:
    virtual ~IReportWriter() = default;
    virtual void write(const std::string& data) = 0;
};

// High-level module depends on abstraction
class ReportGenerator {
private:
    std::shared_ptr<IReportWriter> writer;
    
public:
    // Dependency injected through constructor (Inversion of Control)
    ReportGenerator(std::shared_ptr<IReportWriter> writer) 
        : writer(std::move(writer)) {}
    
    void generateReport(const std::string& data) {
        std::string report = "=== Report ===\n" + data + "\n==============\n";
        writer->write(report);  // Depends on abstraction, not implementation
        std::cout << "Report generated\n";
    }
    
    // Can change writer at runtime
    void setWriter(std::shared_ptr<IReportWriter> newWriter) {
        writer = std::move(newWriter);
    }
};

// Low-level implementations depend on abstraction
class FileReportWriter : public IReportWriter {
private:
    std::string filename;
    
public:
    FileReportWriter(const std::string& fname) : filename(fname) {}
    
    void write(const std::string& data) override {
        // Simulate file writing
        std::cout << "Writing to file '" << filename << "':\n" << data << "\n";
    }
};

class DatabaseReportWriter : public IReportWriter {
private:
    std::string connectionString;
    
public:
    DatabaseReportWriter(const std::string& connStr) 
        : connectionString(connStr) {}
    
    void write(const std::string& data) override {
        std::cout << "Storing in database '" << connectionString << "':\n" 
                  << data << "\n";
    }
};

class CloudReportWriter : public IReportWriter {
private:
    std::string cloudEndpoint;
    
public:
    CloudReportWriter(const std::string& endpoint) 
        : cloudEndpoint(endpoint) {}
    
    void write(const std::string& data) override {
        std::cout << "Uploading to cloud '" << cloudEndpoint << "':\n" 
                  << data << "\n";
    }
};

// ============================================================================
// 2. PAYMENT PROCESSOR EXAMPLE
// ============================================================================

// Abstraction
class IPaymentGateway {
public:
    virtual ~IPaymentGateway() = default;
    virtual void processPayment(double amount) = 0;
    virtual std::string getName() const = 0;
};

// High-level module
class PaymentProcessor {
private:
    std::shared_ptr<IPaymentGateway> gateway;
    
public:
    PaymentProcessor(std::shared_ptr<IPaymentGateway> gateway)
        : gateway(std::move(gateway)) {}
    
    void processOrder(double amount, const std::string& item) {
        std::cout << "Processing order for: " << item << "\n";
        std::cout << "Amount: $" << amount << "\n";
        std::cout << "Using: " << gateway->getName() << "\n";
        
        gateway->processPayment(amount);
        
        std::cout << "Payment completed successfully!\n";
    }
    
    void setGateway(std::shared_ptr<IPaymentGateway> newGateway) {
        gateway = std::move(newGateway);
    }
};

// Low-level implementations
class PayPalGateway : public IPaymentGateway {
public:
    void processPayment(double amount) override {
        std::cout << "Processing $" << amount << " via PayPal API\n";
        // Actual PayPal integration would go here
    }
    
    std::string getName() const override {
        return "PayPal";
    }
};

class StripeGateway : public IPaymentGateway {
public:
    void processPayment(double amount) override {
        std::cout << "Charging $" << amount << " via Stripe API\n";
        // Actual Stripe integration would go here
    }
    
    std::string getName() const override {
        return "Stripe";
    }
};

class BankTransferGateway : public IPaymentGateway {
public:
    void processPayment(double amount) override {
        std::cout << "Initiating bank transfer of $" << amount << "\n";
        // Actual bank transfer logic would go here
    }
    
    std::string getName() const override {
        return "Bank Transfer";
    }
};

// ============================================================================
// 3. NOTIFICATION SERVICE WITH DEPENDENCY INJECTION
// ============================================================================

// Abstraction
class INotificationChannel {
public:
    virtual ~INotificationChannel() = default;
    virtual void send(const std::string& recipient, 
                      const std::string& message) = 0;
    virtual std::string getChannelType() const = 0;
};

// High-level module
class NotificationService {
private:
    std::vector<std::shared_ptr<INotificationChannel>> channels;
    
public:
    // Constructor injection
    NotificationService(std::initializer_list<std::shared_ptr<INotificationChannel>> initChannels)
        : channels(initChannels) {}
    
    // Method injection
    void addChannel(std::shared_ptr<INotificationChannel> channel) {
        channels.push_back(std::move(channel));
    }
    
    void sendNotification(const std::string& message, 
                          const std::vector<std::string>& recipients) {
        std::cout << "\n=== Sending Notifications ===\n";
        std::cout << "Message: " << message << "\n";
        
        for (const auto& recipient : recipients) {
            std::cout << "\nTo: " << recipient << "\n";
            
            for (const auto& channel : channels) {
                std::cout << "Via " << channel->getChannelType() << ": ";
                channel->send(recipient, message);
            }
        }
    }
};

// Low-level implementations
class EmailChannel : public INotificationChannel {
public:
    void send(const std::string& recipient, const std::string& message) override {
        std::cout << "Email sent to " << recipient << "\n";
        // Actual email sending logic
    }
    
    std::string getChannelType() const override {
        return "Email";
    }
};

class SMSChannel : public INotificationChannel {
public:
    void send(const std::string& recipient, const std::string& message) override {
        std::cout << "SMS sent to " << recipient << "\n";
        // Actual SMS sending logic
    }
    
    std::string getChannelType() const override {
        return "SMS";
    }
};

class PushNotificationChannel : public INotificationChannel {
public:
    void send(const std::string& recipient, const std::string& message) override {
        std::cout << "Push notification sent to device " << recipient << "\n";
        // Actual push notification logic
    }
    
    std::string getChannelType() const override {
        return "Push Notification";
    }
};

// ============================================================================
// 4. DATA ACCESS WITH REPOSITORY PATTERN
// ============================================================================

// Abstraction
class IUserRepository {
public:
    virtual ~IUserRepository() = default;
    virtual void save(const std::string& userData) = 0;
    virtual std::string findById(int id) = 0;
    virtual std::vector<std::string> findAll() = 0;
};

// High-level module (business logic)
class UserService {
private:
    std::shared_ptr<IUserRepository> repository;
    
public:
    UserService(std::shared_ptr<IUserRepository> repo)
        : repository(std::move(repo)) {}
    
    void createUser(const std::string& name, int age) {
        std::string userData = "Name: " + name + ", Age: " + std::to_string(age);
        repository->save(userData);
        std::cout << "User created: " << userData << "\n";
    }
    
    void getUser(int id) {
        std::string user = repository->findById(id);
        std::cout << "Found user: " << user << "\n";
    }
    
    void listAllUsers() {
        auto users = repository->findAll();
        std::cout << "\n=== All Users ===\n";
        for (const auto& user : users) {
            std::cout << user << "\n";
        }
    }
};

// Low-level implementations
class MySQLUserRepository : public IUserRepository {
public:
    void save(const std::string& userData) override {
        std::cout << "[MySQL] Saving user: " << userData << "\n";
        // Actual MySQL insert
    }
    
    std::string findById(int id) override {
        std::string result = "[MySQL] User with id=" + std::to_string(id);
        // Actual MySQL select
        return result;
    }
    
    std::vector<std::string> findAll() override {
        return {"[MySQL] John, 30", "[MySQL] Jane, 25", "[MySQL] Bob, 40"};
    }
};

class PostgreSQLUserRepository : public IUserRepository {
public:
    void save(const std::string& userData) override {
        std::cout << "[PostgreSQL] Saving user: " << userData << "\n";
        // Actual PostgreSQL insert
    }
    
    std::string findById(int id) override {
        std::string result = "[PostgreSQL] User with id=" + std::to_string(id);
        // Actual PostgreSQL select
        return result;
    }
    
    std::vector<std::string> findAll() override {
        return {"[PostgreSQL] Alice, 28", "[PostgreSQL] Charlie, 35"};
    }
};

class InMemoryUserRepository : public IUserRepository {
private:
    std::vector<std::string> users;
    
public:
    void save(const std::string& userData) override {
        users.push_back(userData);
        std::cout << "[InMemory] User saved: " << userData << "\n";
    }
    
    std::string findById(int id) override {
        if (id >= 0 && id < static_cast<int>(users.size())) {
            return "[InMemory] " + users[id];
        }
        return "[InMemory] User not found";
    }
    
    std::vector<std::string> findAll() override {
        std::vector<std::string> result;
        for (const auto& user : users) {
            result.push_back("[InMemory] " + user);
        }
        return result;
    }
};

// ============================================================================
// 5. FACTORY PATTERN FOR DEPENDENCY CREATION
// ============================================================================

class Logger {
public:
    virtual ~Logger() = default;
    virtual void log(const std::string& message) = 0;
};

class FileLogger : public Logger {
public:
    void log(const std::string& message) override {
        std::cout << "[File] " << message << "\n";
    }
};

class ConsoleLogger : public Logger {
public:
    void log(const std::string& message) override {
        std::cout << "[Console] " << message << "\n";
    }
};

class DatabaseLogger : public Logger {
public:
    void log(const std::string& message) override {
        std::cout << "[Database] " << message << "\n";
    }
};

// Factory abstraction
class LoggerFactory {
public:
    virtual ~LoggerFactory() = default;
    virtual std::unique_ptr<Logger> createLogger() = 0;
};

// Concrete factories
class FileLoggerFactory : public LoggerFactory {
public:
    std::unique_ptr<Logger> createLogger() override {
        return std::make_unique<FileLogger>();
    }
};

class ConsoleLoggerFactory : public LoggerFactory {
public:
    std::unique_ptr<Logger> createLogger() override {
        return std::make_unique<ConsoleLogger>();
    }
};

// Application using factory
class Application {
private:
    std::unique_ptr<Logger> logger;
    
public:
    Application(std::unique_ptr<LoggerFactory> factory)
        : logger(factory->createLogger()) {}
    
    void run() {
        logger->log("Application started");
        // Business logic
        logger->log("Processing data...");
        logger->log("Application finished");
    }
};

// ============================================================================
// 6. DEPENDENCY INJECTION CONTAINER (SIMPLIFIED)
// ============================================================================

class IDataSource {
public:
    virtual ~IDataSource() = default;
    virtual std::string fetchData() = 0;
};

class DatabaseDataSource : public IDataSource {
public:
    std::string fetchData() override {
        return "Data from database";
    }
};

class APIDataSource : public IDataSource {
public:
    std::string fetchData() override {
        return "Data from API";
    }
};

// Simple dependency container
class DIContainer {
private:
    std::map<std::string, std::function<std::shared_ptr<void>()>> services;
    
public:
    template<typename Interface, typename Implementation>
    void registerService() {
        services[typeid(Interface).name()] = []() {
            return std::static_pointer_cast<void>(
                std::make_shared<Implementation>());
        };
    }
    
    template<typename Interface>
    std::shared_ptr<Interface> resolve() {
        auto it = services.find(typeid(Interface).name());
        if (it != services.end()) {
            return std::static_pointer_cast<Interface>(it->second());
        }
        return nullptr;
    }
};

// Service using dependency injection
class DataProcessor {
private:
    std::shared_ptr<IDataSource> dataSource;
    
public:
    DataProcessor(std::shared_ptr<IDataSource> source)
        : dataSource(std::move(source)) {}
    
    void process() {
        std::string data = dataSource->fetchData();
        std::cout << "Processing: " << data << "\n";
    }
};

void demonstrate_dip_correct() {
    std::cout << "\n=== DEPENDENCY INVERSION PRINCIPLE ===\n";
    
    // 1. Report Generator
    std::cout << "\n1. Report Generator with Different Writers:\n";
    
    auto fileWriter = std::make_shared<FileReportWriter>("report.txt");
    auto dbWriter = std::make_shared<DatabaseReportWriter>("server=localhost");
    auto cloudWriter = std::make_shared<CloudReportWriter>("https://api.cloud.com");
    
    ReportGenerator reportGen(fileWriter);
    reportGen.generateReport("Sales Data Q1");
    
    reportGen.setWriter(dbWriter);
    reportGen.generateReport("Inventory Report");
    
    reportGen.setWriter(cloudWriter);
    reportGen.generateReport("Analytics Data");
    
    // 2. Payment Processor
    std::cout << "\n2. Payment Processor with Different Gateways:\n";
    
    auto paypal = std::make_shared<PayPalGateway>();
    auto stripe = std::make_shared<StripeGateway>();
    auto bank = std::make_shared<BankTransferGateway>();
    
    PaymentProcessor paymentProcessor(paypal);
    paymentProcessor.processOrder(99.99, "Premium Subscription");
    
    paymentProcessor.setGateway(stripe);
    paymentProcessor.processOrder(49.99, "Basic Subscription");
    
    paymentProcessor.setGateway(bank);
    paymentProcessor.processOrder(199.99, "Enterprise License");
    
    // 3. Notification Service
    std::cout << "\n3. Notification Service with Multiple Channels:\n";
    
    auto email = std::make_shared<EmailChannel>();
    auto sms = std::make_shared<SMSChannel>();
    auto push = std::make_shared<PushNotificationChannel>();
    
    NotificationService notificationService({email, sms});
    notificationService.addChannel(push);
    
    std::vector<std::string> recipients = {"john@example.com", "+1234567890", "device_abc123"};
    notificationService.sendNotification("Your order has shipped!", recipients);
    
    // 4. User Service with Different Repositories
    std::cout << "\n4. User Service with Different Data Sources:\n";
    
    auto mysqlRepo = std::make_shared<MySQLUserRepository>();
    auto postgresRepo = std::make_shared<PostgreSQLUserRepository>();
    auto memoryRepo = std::make_shared<InMemoryUserRepository>();
    
    UserService userService(mysqlRepo);
    userService.createUser("John Doe", 30);
    userService.createUser("Jane Smith", 25);
    userService.getUser(0);
    userService.listAllUsers();
    
    std::cout << "\nSwitching to PostgreSQL repository:\n";
    userService = UserService(postgresRepo);
    userService.createUser("Alice Johnson", 28);
    userService.listAllUsers();
    
    std::cout << "\nSwitching to In-Memory repository:\n";
    userService = UserService(memoryRepo);
    userService.createUser("Bob Wilson", 40);
    userService.listAllUsers();
    
    // 5. Factory Pattern
    std::cout << "\n5. Factory Pattern for Logger Creation:\n";
    
    auto consoleFactory = std::make_unique<ConsoleLoggerFactory>();
    Application app1(std::move(consoleFactory));
    app1.run();
    
    // 6. Dependency Injection Container
    std::cout << "\n6. Dependency Injection Container:\n";
    
    DIContainer container;
    container.registerService<IDataSource, DatabaseDataSource>();
    
    auto dataSource = container.resolve<IDataSource>();
    if (dataSource) {
        DataProcessor processor(dataSource);
        processor.process();
    }
    
    // Switch implementation at container level
    container.registerService<IDataSource, APIDataSource>();
    dataSource = container.resolve<IDataSource>();
    if (dataSource) {
        DataProcessor processor(dataSource);
        processor.process();
    }
}

// ============================================================================
// BENEFITS AND PATTERNS
// ============================================================================

/*
Benefits of Dependency Inversion Principle:

1. **Decoupling**: High-level and low-level modules are independent
2. **Testability**: Easy to mock dependencies for testing
3. **Flexibility**: Can swap implementations without changing code
4. **Maintainability**: Changes are isolated
5. **Reusability**: Modules can be reused in different contexts

Common Patterns for DIP:

1. **Dependency Injection (DI)**: 
   - Constructor Injection (recommended)
   - Setter/Method Injection
   - Interface Injection

2. **Factory Pattern**: Create objects without specifying exact class

3. **Service Locator**: Central registry for dependencies

4. **Inversion of Control (IoC) Containers**: 
   - Automate dependency resolution
   - Manage object lifetimes
   - Configure dependencies externally

Key Concepts:

1. **Abstraction**: Interfaces or abstract classes
2. **Dependency**: Anything your class needs to function
3. **Inversion**: Dependencies flow from high-level to low-level
4. **Injection**: Providing dependencies from outside

Implementation Guidelines:

1. **Depend on abstractions**, not concretions
2. **No `new` in business logic** (except for value objects)
3. **Use constructor injection** for required dependencies
4. **Use setter injection** for optional dependencies
5. **Program to interfaces**, not implementations
*/

int main() {
    std::cout << "=== SOLID PRINCIPLES IN C++ ===\n";
    
    demonstrate_srp_correct();
    demonstrate_ocp_correct();
    demonstrate_lsp_correct();
    demonstrate_isp_correct();
    demonstrate_dip_correct();
    
    std::cout << "\n=== ALL SOLID PRINCIPLES DEMONSTRATED ===\n";
    
    return 0;
}


