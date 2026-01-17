/*
    Go Structs & Methods - Comprehensive Example with Detailed Comments
    
    This file demonstrates Go's struct types and methods with practical examples:
    - Struct definitions and instantiation
    - Struct literals and field tags
    - Embedded structs (composition over inheritance)
    - Methods with value and pointer receivers
    - Interfaces and method sets
*/

package main

import (
    "encoding/json"
    "fmt"
    "math"
    "time"
)

func main() {
    fmt.Println("=== GO STRUCTS & METHODS DEMONSTRATION ===")
    fmt.Println()

    /*
        SECTION 1: STRUCT DEFINITIONS
        
        Structs in Go:
        - Collection of named fields
        - Similar to classes in OOP (but no inheritance)
        - Can have methods attached
        - Zero value is struct with zero-valued fields
    */
    
    fmt.Println("=== 1. STRUCT DEFINITIONS ===")
    
    // -----------------------------------------------------------------
    // Basic struct definition
    // -----------------------------------------------------------------
    fmt.Println("\n1. Basic Struct Definition:")
    
    // Define a struct type
    type Person struct {
        FirstName string
        LastName  string
        Age       int
        Height    float64 // in meters
        IsStudent bool
    }
    
    // Zero value of struct
    var zeroPerson Person
    fmt.Printf("   var zeroPerson Person\t\t= %+v\n", zeroPerson)
    fmt.Printf("   zeroPerson.FirstName\t\t\t= \"%s\" (zero value)\n", zeroPerson.FirstName)
    
    // -----------------------------------------------------------------
    // Creating struct instances
    // -----------------------------------------------------------------
    fmt.Println("\n2. Creating Struct Instances:")
    
    // Using var (zero-valued)
    var alice Person
    alice.FirstName = "Alice"
    alice.LastName = "Smith"
    alice.Age = 30
    fmt.Printf("   Created with var: %+v\n", alice)
    
    // Using struct literal (all fields)
    bob := Person{
        FirstName: "Bob",
        LastName:  "Johnson",
        Age:       25,
        Height:    1.75,
        IsStudent: true,
    }
    fmt.Printf("   Literal with field names: %+v\n", bob)
    
    // Struct literal without field names (must be in order, all fields)
    carol := Person{"Carol", "Williams", 35, 1.68, false}
    fmt.Printf("   Literal without names: %+v\n", carol)
    
    // Partial initialization (uninitialized fields get zero values)
    dave := Person{
        FirstName: "Dave",
        Age:       40,
    }
    fmt.Printf("   Partial initialization: %+v\n", dave)
    
    // Using new() - returns pointer
    eve := new(Person)
    eve.FirstName = "Eve"
    eve.Age = 28
    fmt.Printf("   Using new(): %+v (type: %T)\n", eve, eve)
    
    // -----------------------------------------------------------------
    // Accessing and modifying fields
    // -----------------------------------------------------------------
    fmt.Println("\n3. Accessing and Modifying Fields:")
    
    person := Person{"John", "Doe", 45, 1.80, false}
    
    // Access fields
    fmt.Printf("   person.FirstName\t\t= %s\n", person.FirstName)
    fmt.Printf("   person.Age\t\t\t= %d\n", person.Age)
    
    // Modify fields
    person.Age = 46
    person.LastName = "Smith-Doe"
    fmt.Printf("   After modification: %+v\n", person)
    
    // -----------------------------------------------------------------
    // Struct field tags (for JSON, validation, etc.)
    // -----------------------------------------------------------------
    fmt.Println("\n4. Struct Field Tags:")
    
    type User struct {
        ID        int    `json:"id" db:"user_id" validate:"required"`
        Username  string `json:"username" validate:"min=3,max=20"`
        Password  string `json:"-"` // Dash means exclude from JSON
        CreatedAt time.Time `json:"created_at,omitempty"`
        IsAdmin   bool    `json:"is_admin"`
    }
    
    user := User{
        ID:       1,
        Username: "johndoe",
        Password: "secret123",
        CreatedAt: time.Now(),
        IsAdmin:   false,
    }
    
    // Marshal to JSON to demonstrate tags
    jsonBytes, _ := json.MarshalIndent(user, "   ", "  ")
    fmt.Printf("   User as JSON:\n%s\n", string(jsonBytes))
    
    fmt.Printf("   Field tags for Username:\n")
    fmt.Printf("     json: \"username\"\n")
    fmt.Printf("     validate: \"min=3,max=20\"\n")
    
    fmt.Println()

    /*
        SECTION 2: STRUCT LITERALS
        
        Go provides flexible ways to create struct instances.
    */
    
    fmt.Println("=== 2. STRUCT LITERALS ===")
    
    // -----------------------------------------------------------------
    // Anonymous structs
    // -----------------------------------------------------------------
    fmt.Println("\n1. Anonymous Structs:")
    
    // Create struct without defining a type
    anonymous := struct {
        ID   int
        Name string
    }{
        ID:   100,
        Name: "Anonymous",
    }
    
    fmt.Printf("   Anonymous struct: %+v\n", anonymous)
    
    // Useful for one-time use or JSON unmarshaling
    config := struct {
        Host     string `json:"host"`
        Port     int    `json:"port"`
        SSL      bool   `json:"ssl"`
        Timeout  int    `json:"timeout"`
    }{
        Host:    "localhost",
        Port:    8080,
        SSL:     false,
        Timeout: 30,
    }
    
    fmt.Printf("   Config struct: %+v\n", config)
    
    // -----------------------------------------------------------------
    // Struct comparison
    // -----------------------------------------------------------------
    fmt.Println("\n2. Struct Comparison:")
    
    point1 := struct{ X, Y int }{10, 20}
    point2 := struct{ X, Y int }{10, 20}
    point3 := struct{ X, Y int }{5, 20}
    
    fmt.Printf("   point1 == point2? %v\n", point1 == point2) // true
    fmt.Printf("   point1 == point3? %v\n", point1 == point3) // false
    
    // Structs with comparable fields can be compared
    p1 := Person{"Alice", "Smith", 30, 1.65, false}
    p2 := Person{"Alice", "Smith", 30, 1.65, false}
    p3 := Person{"Alice", "Smith", 31, 1.65, false}
    
    fmt.Printf("   p1 == p2? %v\n", p1 == p2) // true
    fmt.Printf("   p1 == p3? %v\n", p1 == p3) // false
    
    // -----------------------------------------------------------------
    // Nested structs
    // -----------------------------------------------------------------
    fmt.Println("\n3. Nested Structs:")
    
    type Address struct {
        Street  string
        City    string
        Country string
        ZipCode string
    }
    
    type Employee struct {
        ID        int
        Name      string
        Position  string
        Salary    float64
        Address   Address // Nested struct
        ManagerID *int    // Pointer field
    }
    
    managerID := 1001
    emp := Employee{
        ID:       5001,
        Name:     "Jane Smith",
        Position: "Software Engineer",
        Salary:   85000.50,
        Address: Address{
            Street:  "123 Main St",
            City:    "San Francisco",
            Country: "USA",
            ZipCode: "94105",
        },
        ManagerID: &managerID,
    }
    
    fmt.Printf("   Employee with nested address:\n")
    fmt.Printf("     Name: %s\n", emp.Name)
    fmt.Printf("     City: %s\n", emp.Address.City)
    fmt.Printf("     Manager ID: %d\n", *emp.ManagerID)
    
    // Deep copy of nested struct
    empCopy := emp
    empCopy.Address.City = "New York" // Doesn't affect original
    fmt.Printf("   Original employee city: %s\n", emp.Address.City)
    fmt.Printf("   Copied employee city: %s\n", empCopy.Address.City)
    
    fmt.Println()

    /*
        SECTION 3: EMBEDDED STRUCTS
        
        Go uses composition over inheritance.
        Embedded structs allow fields and methods to be promoted.
    */
    
    fmt.Println("=== 3. EMBEDDED STRUCTS (Composition) ===")
    
    // -----------------------------------------------------------------
    // Basic embedding
    // -----------------------------------------------------------------
    fmt.Println("\n1. Basic Embedding:")
    
    type Contact struct {
        Email   string
        Phone   string
    }
    
    type Customer struct {
        ID      int
        Name    string
        Contact // Embedded struct (no field name)
    }
    
    customer := Customer{
        ID:   1,
        Name: "Acme Corp",
        Contact: Contact{
            Email: "info@acme.com",
            Phone: "555-1234",
        },
    }
    
    // Fields from embedded struct are "promoted"
    fmt.Printf("   customer.Email\t\t= %s (promoted field)\n", customer.Email)
    fmt.Printf("   customer.Contact.Email\t= %s (also works)\n", customer.Contact.Email)
    
    // -----------------------------------------------------------------
    // Multiple embedding
    // -----------------------------------------------------------------
    fmt.Println("\n2. Multiple Embedding:")
    
    type BaseInfo struct {
        ID        int
        CreatedAt time.Time
        UpdatedAt time.Time
    }
    
    type Product struct {
        BaseInfo           // Embedded
        Name       string
        Price      float64
        CategoryID int
    }
    
    product := Product{
        BaseInfo: BaseInfo{
            ID:        101,
            CreatedAt: time.Now(),
            UpdatedAt: time.Now(),
        },
        Name:       "Laptop",
        Price:      1299.99,
        CategoryID: 5,
    }
    
    fmt.Printf("   Product: %s ($%.2f)\n", product.Name, product.Price)
    fmt.Printf("   Created: %v\n", product.CreatedAt)
    fmt.Printf("   ID from BaseInfo: %d\n", product.ID)
    
    // -----------------------------------------------------------------
    // Embedding with field name (not promoted)
    // -----------------------------------------------------------------
    fmt.Println("\n3. Embedding with Field Name (Not Promoted):")
    
    type Client struct {
        ID           int
        Name         string
        ContactInfo  Contact // Named field, not embedded
    }
    
    client := Client{
        ID:   2,
        Name: "Beta Inc",
        ContactInfo: Contact{
            Email: "beta@example.com",
            Phone: "555-5678",
        },
    }
    
    // Must use field name for named embedding
    // fmt.Printf("client.Email") // Error!
    fmt.Printf("   client.ContactInfo.Email\t= %s\n", client.ContactInfo.Email)
    
    // -----------------------------------------------------------------
    // Field and method promotion
    // -----------------------------------------------------------------
    fmt.Println("\n4. Field and Method Promotion:")
    
    type Animal struct {
        Name string
        Age  int
    }
    
    func (a Animal) Speak() string {
        return "Animal sound"
    }
    
    type Dog struct {
        Animal        // Embed Animal
        Breed   string
    }
    
    // Dog gets promoted fields and methods from Animal
    dog := Dog{
        Animal: Animal{
            Name: "Buddy",
            Age:  3,
        },
        Breed: "Golden Retriever",
    }
    
    fmt.Printf("   Dog name (promoted): %s\n", dog.Name)
    fmt.Printf("   Dog age (promoted): %d\n", dog.Age)
    fmt.Printf("   Dog speak (promoted method): %s\n", dog.Speak())
    
    // -----------------------------------------------------------------
    // Embedding with conflicts
    // -----------------------------------------------------------------
    fmt.Println("\n5. Embedding Conflicts:")
    
    type A struct {
        Value int
    }
    
    type B struct {
        Value string
    }
    
    type C struct {
        A
        B
        Value float64 // Outer struct's own field
    }
    
    c := C{
        A: A{Value: 10},
        B: B{Value: "hello"},
        Value: 3.14,
    }
    
    // Access different levels explicitly
    fmt.Printf("   c.Value\t\t\t= %.2f (outer field wins)\n", c.Value)
    fmt.Printf("   c.A.Value\t\t\t= %d\n", c.A.Value)
    fmt.Printf("   c.B.Value\t\t\t= %s\n", c.B.Value)
    
    fmt.Println()

    /*
        SECTION 4: METHODS ON STRUCTS
        
        Methods in Go are functions with a special receiver argument.
        The receiver appears between 'func' and the method name.
    */
    
    fmt.Println("=== 4. METHODS ON STRUCTS ===")
    
    // -----------------------------------------------------------------
    // Basic method definition
    // -----------------------------------------------------------------
    fmt.Println("\n1. Basic Method Definition:")
    
    type Rectangle struct {
        Width  float64
        Height float64
    }
    
    // Method with value receiver
    func (r Rectangle) Area() float64 {
        return r.Width * r.Height
    }
    
    // Method with value receiver
    func (r Rectangle) Perimeter() float64 {
        return 2 * (r.Width + r.Height)
    }
    
    rect := Rectangle{Width: 5, Height: 3}
    fmt.Printf("   Rectangle: %+v\n", rect)
    fmt.Printf("   rect.Area()\t\t= %.2f\n", rect.Area())
    fmt.Printf("   rect.Perimeter()\t= %.2f\n", rect.Perimeter())
    
    // -----------------------------------------------------------------
    // Method with pointer receiver
    // -----------------------------------------------------------------
    fmt.Println("\n2. Method with Pointer Receiver:")
    
    type Counter struct {
        value int
    }
    
    // Pointer receiver method (can modify struct)
    func (c *Counter) Increment() {
        c.value++
    }
    
    // Value receiver method (cannot modify)
    func (c Counter) GetValue() int {
        return c.value
    }
    
    counter := Counter{value: 10}
    fmt.Printf("   Initial counter: %d\n", counter.GetValue())
    
    counter.Increment() // Go automatically converts to pointer for us
    counter.Increment()
    fmt.Printf("   After 2 increments: %d\n", counter.GetValue())
    
    // Explicit pointer works too
    counterPtr := &counter
    counterPtr.Increment()
    fmt.Printf("   After pointer increment: %d\n", counter.GetValue())
    
    // -----------------------------------------------------------------
    // Methods on non-struct types
    // -----------------------------------------------------------------
    fmt.Println("\n3. Methods on Non-Struct Types:")
    
    // Define a new type based on existing type
    type MyString string
    
    // Add method to custom type
    func (s MyString) Reverse() MyString {
        runes := []rune(s)
        for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
            runes[i], runes[j] = runes[j], runes[i]
        }
        return MyString(runes)
    }
    
    func (s MyString) Uppercase() MyString {
        return MyString(strings.ToUpper(string(s)))
    }
    
    myStr := MyString("Hello, World!")
    fmt.Printf("   Original: %s\n", myStr)
    fmt.Printf("   Reversed: %s\n", myStr.Reverse())
    fmt.Printf("   Uppercase: %s\n", myStr.Uppercase())
    
    // Cannot add methods to built-in types directly
    // But can create alias types as shown above
    
    // -----------------------------------------------------------------
    // Methods with multiple return values
    // -----------------------------------------------------------------
    fmt.Println("\n4. Methods with Multiple Return Values:")
    
    type BankAccount struct {
        AccountNumber string
        Balance       float64
        Owner         string
    }
    
    func (ba *BankAccount) Deposit(amount float64) (newBalance float64, err error) {
        if amount <= 0 {
            return ba.Balance, fmt.Errorf("deposit amount must be positive")
        }
        ba.Balance += amount
        return ba.Balance, nil
    }
    
    func (ba *BankAccount) Withdraw(amount float64) (newBalance float64, err error) {
        if amount <= 0 {
            return ba.Balance, fmt.Errorf("withdrawal amount must be positive")
        }
        if amount > ba.Balance {
            return ba.Balance, fmt.Errorf("insufficient funds")
        }
        ba.Balance -= amount
        return ba.Balance, nil
    }
    
    account := BankAccount{
        AccountNumber: "ACC123456",
        Balance:       1000.00,
        Owner:         "John Doe",
    }
    
    fmt.Printf("   Initial balance: $%.2f\n", account.Balance)
    
    balance, err := account.Deposit(500.00)
    if err != nil {
        fmt.Printf("   Deposit error: %v\n", err)
    } else {
        fmt.Printf("   After deposit: $%.2f\n", balance)
    }
    
    balance, err = account.Withdraw(200.00)
    if err != nil {
        fmt.Printf("   Withdrawal error: %v\n", err)
    } else {
        fmt.Printf("   After withdrawal: $%.2f\n", balance)
    }
    
    // Try invalid withdrawal
    balance, err = account.Withdraw(2000.00)
    if err != nil {
        fmt.Printf("   Expected error: %v\n", err)
    }
    
    fmt.Println()

    /*
        SECTION 5: VALUE VS POINTER RECEIVERS
        
        This is a crucial Go concept. Choosing between value and pointer receivers
        depends on whether you need to modify the receiver or optimize for large structs.
    */
    
    fmt.Println("=== 5. VALUE VS POINTER RECEIVERS ===")
    
    // -----------------------------------------------------------------
    // Value receiver (copy)
    // -----------------------------------------------------------------
    fmt.Println("\n1. Value Receiver (Copy):")
    
    type Point struct {
        X, Y int
    }
    
    // Value receiver - works on copy
    func (p Point) MoveByValue(dx, dy int) Point {
        p.X += dx
        p.Y += dy
        return p // Returns modified copy
    }
    
    // Pointer receiver - modifies original
    func (p *Point) MoveByPointer(dx, dy int) {
        p.X += dx
        p.Y += dy
    }
    
    point := Point{X: 10, Y: 20}
    fmt.Printf("   Original point: %+v\n", point)
    
    // Value receiver doesn't modify original
    movedPoint := point.MoveByValue(5, 5)
    fmt.Printf("   After MoveByValue(5,5):\n")
    fmt.Printf("     Original: %+v (unchanged)\n", point)
    fmt.Printf("     Returned: %+v (modified copy)\n", movedPoint)
    
    // Pointer receiver modifies original
    point.MoveByPointer(5, 5)
    fmt.Printf("   After MoveByPointer(5,5): %+v (original modified)\n", point)
    
    // -----------------------------------------------------------------
    // When to use value receivers
    // -----------------------------------------------------------------
    fmt.Println("\n2. When to Use Value Receivers:")
    
    type ImmutableConfig struct {
        Version string
        Debug   bool
    }
    
    // Value receiver for immutable types
    func (c ImmutableConfig) GetVersion() string {
        return c.Version
    }
    
    // Value receiver for small structs
    func (c ImmutableConfig) IsDebug() bool {
        return c.Debug
    }
    
    config2 := ImmutableConfig{Version: "1.0.0", Debug: true}
    fmt.Printf("   Config version: %s\n", config2.GetVersion())
    fmt.Printf("   Is debug? %v\n", config2.IsDebug())
    
    // -----------------------------------------------------------------
    // When to use pointer receivers
    // -----------------------------------------------------------------
    fmt.Println("\n3. When to Use Pointer Receivers:")
    
    type LargeStruct struct {
        Data [1000]int
    }
    
    // Pointer receiver avoids copying large struct
    func (ls *LargeStruct) Update(index, value int) {
        if index >= 0 && index < len(ls.Data) {
            ls.Data[index] = value
        }
    }
    
    // Value receiver would copy 1000 integers!
    // func (ls LargeStruct) Update(index, value int) { ... } // Inefficient!
    
    large := &LargeStruct{}
    large.Update(0, 42)
    fmt.Printf("   Large struct first element: %d\n", large.Data[0])
    
    // -----------------------------------------------------------------
    // Mixing value and pointer receivers
    // -----------------------------------------------------------------
    fmt.Println("\n4. Mixing Value and Pointer Receivers:")
    
    type ShoppingCart struct {
        Items []string
        Total float64
    }
    
    // Value receiver for read-only operation
    func (c ShoppingCart) ItemCount() int {
        return len(c.Items)
    }
    
    // Pointer receiver for modification
    func (c *ShoppingCart) AddItem(item string, price float64) {
        c.Items = append(c.Items, item)
        c.Total += price
    }
    
    // Pointer receiver for modification
    func (c *ShoppingCart) Clear() {
        c.Items = []string{}
        c.Total = 0
    }
    
    cart := &ShoppingCart{}
    cart.AddItem("Book", 29.99)
    cart.AddItem("Coffee", 5.99)
    
    fmt.Printf("   Cart has %d items\n", cart.ItemCount())
    fmt.Printf("   Cart total: $%.2f\n", cart.Total)
    
    // -----------------------------------------------------------------
    // Method sets and interfaces
    // -----------------------------------------------------------------
    fmt.Println("\n5. Method Sets and Interfaces:")
    
    type Shape interface {
        Area() float64
        Scale(factor float64)
    }
    
    type Circle struct {
        Radius float64
    }
    
    // Value receiver method
    func (c Circle) Area() float64 {
        return math.Pi * c.Radius * c.Radius
    }
    
    // Pointer receiver method
    func (c *Circle) Scale(factor float64) {
        c.Radius *= factor
    }
    
    // IMPORTANT: Method set determines what interfaces a type satisfies
    // - Value type T has methods with both value and pointer receivers
    // - Pointer type *T has methods with both value and pointer receivers
    // - But interface satisfaction differs!
    
    var circle Circle = Circle{Radius: 5}
    var circlePtr *Circle = &Circle{Radius: 10}
    
    // Both can call Area() (value receiver)
    fmt.Printf("   circle.Area() = %.2f\n", circle.Area())
    fmt.Printf("   circlePtr.Area() = %.2f\n", circlePtr.Area())
    
    // Both can call Scale() (pointer receiver)
    circle.Scale(2)      // Go automatically converts to pointer!
    circlePtr.Scale(0.5)
    
    fmt.Printf("   After scaling:\n")
    fmt.Printf("     circle radius = %.2f\n", circle.Radius)
    fmt.Printf("     circlePtr radius = %.2f\n", circlePtr.Radius)
    
    // Interface satisfaction
    var shape Shape
    
    // This works: *Circle satisfies Shape interface
    shape = circlePtr
    fmt.Printf("   shape.Area() = %.2f\n", shape.Area())
    shape.Scale(2)
    
    // This also works! Go converts Circle to *Circle for interface assignment
    shape = &circle
    fmt.Printf("   shape.Area() after conversion = %.2f\n", shape.Area())
    
    // This would NOT work:
    // shape = circle // Error: Circle doesn't implement Scale (need pointer)
    
    // -----------------------------------------------------------------
    // Best practices summary
    // -----------------------------------------------------------------
    fmt.Println("\n6. Best Practices Summary:")
    
    fmt.Println("   Use Pointer Receivers When:")
    fmt.Println("     - Method needs to modify the receiver")
    fmt.Println("     - Struct is large (avoids copying)")
    fmt.Println("     - Consistency with other methods on the type")
    
    fmt.Println("\n   Use Value Receivers When:")
    fmt.Println("     - Method doesn't modify receiver")
    fmt.Println("     - Struct is small (copying is cheap)")
    fmt.Println("     - Working with immutable types")
    fmt.Println("     - Type is a map, func, or chan (reference types)")
    
    fmt.Println("\n   Consistency Rule:")
    fmt.Println("     - If some methods need pointer receivers,")
    fmt.Println("       use pointer receivers for ALL methods on that type")
    
    // -----------------------------------------------------------------
    // Practical example: Complete struct with methods
    // -----------------------------------------------------------------
    fmt.Println("\n7. Practical Complete Example:")
    
    type Employee2 struct {
        ID        int
        FirstName string
        LastName  string
        Salary    float64
        Department string
    }
    
    // Constructor-like function (Go doesn't have constructors)
    func NewEmployee(id int, firstName, lastName, department string, salary float64) *Employee2 {
        return &Employee2{
            ID:         id,
            FirstName:  firstName,
            LastName:   lastName,
            Department: department,
            Salary:     salary,
        }
    }
    
    // Value receiver for read-only
    func (e Employee2) FullName() string {
        return e.FirstName + " " + e.LastName
    }
    
    // Value receiver for calculation
    func (e Employee2) AnnualSalary() float64 {
        return e.Salary * 12
    }
    
    // Pointer receiver for modification
    func (e *Employee2) Raise(percentage float64) {
        if percentage > 0 {
            e.Salary *= (1 + percentage/100)
        }
    }
    
    // Pointer receiver for modification
    func (e *Employee2) Transfer(newDept string) {
        e.Department = newDept
    }
    
    // Create employee
    emp2 := NewEmployee(1001, "Sarah", "Connor", "Engineering", 75000)
    
    fmt.Printf("   Employee: %s\n", emp2.FullName())
    fmt.Printf("   Department: %s\n", emp2.Department)
    fmt.Printf("   Monthly: $%.2f\n", emp2.Salary)
    fmt.Printf("   Annual: $%.2f\n", emp2.AnnualSalary())
    
    emp2.Raise(10) // 10% raise
    emp2.Transfer("Management")
    
    fmt.Printf("   After 10%% raise and transfer:\n")
    fmt.Printf("   Department: %s\n", emp2.Department)
    fmt.Printf("   Monthly: $%.2f\n", emp2.Salary)
    fmt.Printf("   Annual: $%.2f\n", emp2.AnnualSalary())
    
    fmt.Println()
    fmt.Println("=== END OF STRUCTS & METHODS DEMONSTRATION ===")
}

/*
    KEY TAKEAWAYS:
    
    1. STRUCT DEFINITIONS:
       - Define types with named fields
       - Zero value has all fields zero-valued
       - Field tags for metadata (JSON, validation, etc.)
    
    2. STRUCT LITERALS:
       - Multiple ways to instantiate structs
       - Anonymous structs for one-time use
       - Structs are comparable if all fields are comparable
    
    3. EMBEDDED STRUCTS (COMPOSITION):
       - Go's alternative to inheritance
       - Fields and methods are "promoted"
       - Outer struct fields/methods take precedence
       - Use for code reuse and polymorphism
    
    4. METHODS:
       - Functions with receiver arguments
       - Can be defined on any type (not just structs)
       - Can return multiple values (like functions)
       - Receiver appears between 'func' and method name
    
    5. VALUE VS POINTER RECEIVERS:
       - Value receiver: Works on copy, doesn't modify original
       - Pointer receiver: Can modify original, avoids copying large structs
       - Method set determines interface satisfaction
       - Go automatically converts between value and pointer when calling methods
    
    6. BEST PRACTICES:
       - Use pointer receivers for methods that modify the receiver
       - Use value receivers for immutable operations on small structs
       - Be consistent within a type (all pointer or all value receivers)
       - Use embedded structs for composition, not inheritance
       - Define "constructor" functions (NewType) for complex initialization
    
    IMPORTANT CONCEPTS:
    1. Method Sets:
       - Value type T: methods with value receivers
       - Pointer type *T: methods with both value and pointer receivers
    
    2. Interface Satisfaction:
       - *T can satisfy interfaces requiring value or pointer receivers
       - T can only satisfy interfaces requiring value receivers
    
    3. Automatic Conversion:
       - Go automatically converts values to pointers when calling methods
       - But not for interface satisfaction (important distinction!)
    
    COMMON PATTERNS:
    1. Constructor pattern: NewType() function
    2. Builder pattern: Method chaining with pointer receivers
    3. Fluent interface: Methods return receiver for chaining
    4. Option pattern: Functional options for configuration
*/