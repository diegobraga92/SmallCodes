////////* CONDITIONALS *////////

#include <iostream>
#include <string>

void demonstrate_conditionals() {
    std::cout << "============ CONDITIONALS ============\n" << std::endl;
    
    int score = 85;
    std::string grade;
    
    // ============ BASIC IF-ELSE ============
    std::cout << "=== Basic if-else ===" << std::endl;
    if (score >= 90) {
        grade = "A";
        std::cout << "Excellent!" << std::endl;
    } 
    else if (score >= 80) {  // else if chain
        grade = "B";
        std::cout << "Good job!" << std::endl;
    } 
    else if (score >= 70) {
        grade = "C";
        std::cout << "Average" << std::endl;
    }
    else {  // Final else (optional)
        grade = "F";
        std::cout << "Needs improvement" << std::endl;
    }
    
    std::cout << "Grade: " << grade << std::endl;

    // ============ TERNARY OPERATOR ============
    // Compact if-else for simple assignments
    std::cout << "\n=== Ternary Operator ===" << std::endl;
    std::string result = (score >= 60) ? "Pass" : "Fail";
    std::cout << "Result: " << result << std::endl;
    
    // Nested ternary (use with caution - can be hard to read)
    std::string feedback = (score >= 90) ? "Excellent" :
                          (score >= 80) ? "Good" :
                          (score >= 70) ? "Average" : "Poor";
    std::cout << "Feedback: " << feedback << std::endl;

    // ============ SWITCH STATEMENT ============
    std::cout << "\n=== Switch Statement ===" << std::endl;
    
    char operation = '*';
    double a = 10, b = 5, result_op;
    
    switch (operation) {
        case '+':  // Cases must be constant expressions
            result_op = a + b;
            std::cout << "Addition: " << result_op << std::endl;
            break;  // CRITICAL: without break, execution "falls through"
            
        case '-':
            result_op = a - b;
            std::cout << "Subtraction: " << result_op << std::endl;
            break;
            
        case '*':
            result_op = a * b;
            std::cout << "Multiplication: " << result_op << std::endl;
            break;
            
        case '/':
            if (b != 0) {
                result_op = a / b;
                std::cout << "Division: " << result_op << std::endl;
            } else {
                std::cout << "Division by zero!" << std::endl;
            }
            break;
            
        default:  // Optional: handles all other cases
            std::cout << "Unknown operation!" << std::endl;
            break;
    }

    // ============ SWITCH FALL-THROUGH ============
    std::cout << "\n=== Intentional Fall-through ===" << std::endl;
    
    int month = 2;
    int year = 2024;
    int days = 0;
    
    switch (month) {
        case 1: case 3: case 5: case 7: case 8: case 10: case 12:
            days = 31;
            break;
            
        case 4: case 6: case 9: case 11:
            days = 30;
            break;
            
        case 2:
            // Leap year calculation
            if ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)) {
                days = 29;
            } else {
                days = 28;
            }
            break;
            
        default:
            days = -1;  // Invalid month
    }
    
    std::cout << "Month " << month << " has " << days << " days" << std::endl;

    // ============ INITIALIZATION IN IF (C++17) ============
    std::cout << "\n=== If with Initialization (C++17) ===" << std::endl;
    
    // Old way:
    std::string input = "42";
    int value = std::stoi(input);
    if (value > 0) {
        std::cout << "Positive: " << value << std::endl;
    }
    
    // New way (C++17): initialize variable in if statement
    if (int val = std::stoi(input); val > 0) {
        std::cout << "Still positive: " << val << std::endl;
        // val is only in scope within this if block
    }
    // val is not accessible here - out of scope
    
    // Can also have else if and else
    if (int x = 10; x > 5) {
        std::cout << "x is greater than 5" << std::endl;
    } else if (x < 5) {
        std::cout << "x is less than 5" << std::endl;
    } else {
        std::cout << "x is 5" << std::endl;
    }

    // ============ SWITCH WITH INITIALIZATION (C++17) ============
    std::cout << "\n=== Switch with Initialization (C++17) ===" << std::endl;
    
    switch (int code = std::rand() % 3; code) {
        case 0:
            std::cout << "Code 0 generated" << std::endl;
            break;
        case 1:
            std::cout << "Code 1 generated" << std::endl;
            break;
        default:
            std::cout << "Code " << code << " generated" << std::endl;
    }
    // code is out of scope here
}

int main() {
    demonstrate_conditionals();
    return 0;
}


////////* LOOPS *////////

#include <iostream>
#include <vector>
#include <array>
#include <map>

void demonstrate_loops() {
    std::cout << "============ LOOPS ============\n" << std::endl;
    
    // ============ BASIC FOR LOOP ============
    std::cout << "=== Basic for loop ===" << std::endl;
    
    // Classic for loop: initialization; condition; increment
    for (int i = 0; i < 5; ++i) {  // Prefer ++i over i++ for non-class types
        std::cout << "Iteration " << i << std::endl;
    }
    
    // Multiple variables in initialization
    std::cout << "\nMultiple variables:" << std::endl;
    for (int i = 0, j = 10; i < 5; ++i, j -= 2) {
        std::cout << "i=" << i << ", j=" << j << std::endl;
    }
    
    // ============ WHILE LOOP ============
    std::cout << "\n=== while loop ===" << std::endl;
    
    int count = 0;
    while (count < 5) {  // Condition checked BEFORE each iteration
        std::cout << "Count: " << count << std::endl;
        ++count;  // Don't forget to increment!
    }
    
    // ============ DO-WHILE LOOP ============
    std::cout << "\n=== do-while loop ===" << std::endl;
    
    int input;
    do {  // Condition checked AFTER each iteration
        std::cout << "Enter a positive number: ";
        std::cin >> input;
        if (input <= 0) {
            std::cout << "Invalid input. Try again." << std::endl;
        }
    } while (input <= 0);  // Note the semicolon!
    
    std::cout << "You entered: " << input << std::endl;
    
    // ============ RANGE-BASED FOR LOOP (C++11) ============
    std::cout << "\n=== Range-based for loop ===" << std::endl;
    
    // Array iteration
    int arr[] = {10, 20, 30, 40, 50};
    std::cout << "Array elements: ";
    for (int element : arr) {  // Copy of each element
        std::cout << element << " ";
    }
    std::cout << std::endl;
    
    // Using reference to avoid copying
    std::cout << "Array elements (doubled): ";
    for (int& element : arr) {  // Reference to each element
        element *= 2;
        std::cout << element << " ";
    }
    std::cout << std::endl;
    
    // Using const reference for read-only access
    std::cout << "Array elements (read-only): ";
    for (const int& element : arr) {
        // element *= 2;  // ERROR: can't modify const reference
        std::cout << element << " ";
    }
    std::cout << std::endl;
    
    // ============ LOOPING THROUGH CONTAINERS ============
    std::cout << "\n=== Looping through STL containers ===" << std::endl;
    
    // Vector
    std::vector<int> vec = {1, 2, 3, 4, 5};
    std::cout << "Vector elements: ";
    for (int val : vec) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
    
    // Map (requires C++17 for structured bindings for clean syntax)
    std::map<std::string, int> scores = {{"Alice", 95}, {"Bob", 87}, {"Charlie", 92}};
    
    std::cout << "\nMap elements (C++11 style):" << std::endl;
    for (const auto& pair : scores) {  // auto deduces std::pair<const std::string, int>
        std::cout << pair.first << ": " << pair.second << std::endl;
    }
    
    std::cout << "\nMap elements (C++17 structured bindings):" << std::endl;
    for (const auto& [name, score] : scores) {  // Much cleaner!
        std::cout << name << ": " << score << std::endl;
    }
    
    // ============ LOOP CONTROL STATEMENTS ============
    std::cout << "\n=== Loop control: break, continue ===" << std::endl;
    
    // break - exit loop immediately
    std::cout << "Break example (stops at 3): ";
    for (int i = 0; i < 10; ++i) {
        if (i == 3) break;
        std::cout << i << " ";
    }
    std::cout << std::endl;
    
    // continue - skip to next iteration
    std::cout << "Continue example (skips even numbers): ";
    for (int i = 0; i < 10; ++i) {
        if (i % 2 == 0) continue;  // Skip even numbers
        std::cout << i << " ";
    }
    std::cout << std::endl;
    
    // ============ INFINITE LOOPS ============
    std::cout << "\n=== Infinite loops (and how to exit) ===" << std::endl;
    
    // Three common patterns for infinite loops:
    
    // 1. while(true) - Most common
    int infinite_count = 0;
    while (true) {
        ++infinite_count;
        if (infinite_count >= 3) {
            std::cout << "Breaking from while(true) loop" << std::endl;
            break;
        }
    }
    
    // 2. for(;;) - Also common (no condition means always true)
    for (;;) {
        std::cout << "Breaking from for(;;) loop" << std::endl;
        break;  // Always need a break in for(;;)
    }
    
    // 3. do-while with always true condition
    do {
        std::cout << "Breaking from do-while(true) loop" << std::endl;
        break;
    } while (true);
    
    // ============ NESTED LOOPS ============
    std::cout << "\n=== Nested loops ===" << std::endl;
    
    std::cout << "Multiplication table (1-3):" << std::endl;
    for (int i = 1; i <= 3; ++i) {
        for (int j = 1; j <= 3; ++j) {
            std::cout << i << "×" << j << "=" << i * j << "\t";
        }
        std::cout << std::endl;
    }
    
    // ============ MODERN FEATURES ============
    std::cout << "\n=== Modern C++ loop features ===" << std::endl;
    
    // C++20: init-statement in range-based for
    std::vector<int> data = {1, 2, 3, 4, 5};
    
    for (auto vec = std::vector{1, 2, 3}; int x : vec) {
        std::cout << x << " ";  // vec exists only in loop scope
    }
    std::cout << std::endl;
    
    // Using auto with range-based for
    std::cout << "Using auto: ";
    for (auto x : {10, 20, 30, 40}) {  // auto deduces type
        std::cout << x << " ";
    }
    std::cout << std::endl;
}

int main() {
    demonstrate_loops();
    return 0;
}


////////* GOTO *////////

#include <iostream>
#include <vector>
#include <stdexcept>

void demonstrate_goto() {
    std::cout << "============ goto STATEMENT ============\n" << std::endl;
    
    // ============ BASIC GOTO SYNTAX ============
    std::cout << "=== Basic goto Syntax ===" << std::endl;
    
    int i = 0;
    
start:  // Label (identifier followed by colon)
    std::cout << "i = " << i << std::endl;
    i++;
    
    if (i < 5) {
        goto start;  // Jump to label
    }
    
    std::cout << "Loop finished\n" << std::endl;
    
    // ============ GOTO FOR ERROR HANDLING ============
    std::cout << "=== goto for Error Handling (C-style) ===" << std::endl;
    
    // Example: Resource cleanup on error (old C style)
    int* resource1 = nullptr;
    int* resource2 = nullptr;
    int* resource3 = nullptr;
    
    resource1 = new int(100);
    if (!resource1) {
        goto cleanup;  // Jump to cleanup
    }
    
    resource2 = new int(200);
    if (!resource2) {
        goto cleanup;  // Jump to cleanup
    }
    
    resource3 = new int(300);
    if (!resource3) {
        goto cleanup;  // Jump to cleanup
    }
    
    std::cout << "All resources allocated successfully" << std::endl;
    
    // Use resources...
    
cleanup:
    delete resource3;
    delete resource2;
    delete resource1;
    
    std::cout << "Resources cleaned up\n" << std::endl;
    
    // ============ DANGERS OF goto ============
    std::cout << "=== Dangers of goto ===" << std::endl;
    
    // 1. CANNOT jump over variable initializations
    /*
    {
        int x = 10;
        goto skip;  // ERROR: jumps over initialization
        int y = 20; // y would be uninitialized if we jumped here
    skip:
        std::cout << x << std::endl;
    }
    */
    
    // 2. Spaghetti code - hard to follow control flow
    std::cout << "goto can create 'spaghetti code':" << std::endl;
    
    int counter = 0;
    
    part1:
        counter++;
        if (counter % 2 == 0) goto part3;
        
    part2:
        counter += 2;
        if (counter > 10) goto end;
        goto part1;
        
    part3:
        counter += 3;
        goto part2;
        
    end:
        std::cout << "Final counter: " << counter << " (hard to trace!)\n" << std::endl;
    
    // ============ WHY AVOID goto ============
    std::cout << "=== Why Avoid goto ===" << std::endl;
    
    // Modern alternatives exist:
    
    // 1. Use loops instead of goto for iteration
    std::cout << "Use for/while loops instead:" << std::endl;
    for (int j = 0; j < 5; ++j) {
        std::cout << "j = " << j << std::endl;
    }
    std::cout << "(Much clearer than goto version)\n" << std::endl;
    
    // 2. Use RAII and exceptions for error handling
    std::cout << "Use RAII instead of goto cleanup:" << std::endl;
    
    class Resource {
    private:
        int* data;
        
    public:
        Resource(int value) : data(new int(value)) {
            std::cout << "  Resource " << *data << " allocated" << std::endl;
        }
        
        ~Resource() {
            delete data;
            std::cout << "  Resource " << *data << " freed" << std::endl;
        }
        
        // Disable copy (simplified example)
        Resource(const Resource&) = delete;
        Resource& operator=(const Resource&) = delete;
    };
    
    try {
        Resource r1(100);  // Automatically cleaned up when out of scope
        Resource r2(200);
        Resource r3(300);
        
        // If something fails, exception will unwind stack and destructors run
        throw std::runtime_error("Simulated error");
        
    } catch (const std::exception& e) {
        std::cout << "Exception: " << e.what() << std::endl;
        // All resources automatically cleaned up!
    }
    std::cout << "(Cleanup happens automatically via destructors)\n" << std::endl;
    
    // 3. Use structured programming constructs
    std::cout << "Use break, continue, return:" << std::endl;
    
    bool condition = true;
    while (condition) {
        // Instead of goto, use:
        if (some_condition) break;     // Exit loop
        if (another_condition) continue; // Next iteration
        // Normal processing
    }
    
    // ============ VALID USES OF goto ============
    std::cout << "=== (Rare) Valid Uses of goto ===" << std::endl;
    
    // 1. Breaking out of nested loops
    std::cout << "Breaking out of deeply nested loops:" << std::endl;
    
    for (int x = 0; x < 3; ++x) {
        for (int y = 0; y < 3; ++y) {
            for (int z = 0; z < 3; ++z) {
                if (x == 1 && y == 1 && z == 1) {
                    goto found;  // Clean break from all loops
                }
                std::cout << "(" << x << "," << y << "," << z << ") ";
            }
        }
    }
    std::cout << "\nPoint not found" << std::endl;
    goto end_example;
    
found:
    std::cout << "\nPoint (1,1,1) found!" << std::endl;
    
end_example:
    
    // Alternative: use a flag (more verbose but structured)
    std::cout << "\nAlternative using flag:" << std::endl;
    bool found_flag = false;
    
    for (int x = 0; x < 3 && !found_flag; ++x) {
        for (int y = 0; y < 3 && !found_flag; ++y) {
            for (int z = 0; z < 3 && !found_flag; ++z) {
                if (x == 1 && y == 1 && z == 1) {
                    found_flag = true;
                }
            }
        }
    }
    
    // 2. Low-level system programming or parsers
    // Sometimes used in performance-critical code or state machines
    
    // 3. Generated code (compilers sometimes use goto)
    
    // ============ BEST PRACTICES ============
    std::cout << "\n=== Best Practices ===" << std::endl;
    std::cout << "1. AVOID goto in new C++ code" << std::endl;
    std::cout << "2. Use exceptions and RAII for error handling" << std::endl;
    std::cout << "3. Use structured control flow (loops, functions)" << std::endl;
    std::cout << "4. If you MUST use goto:" << std::endl;
    std::cout << "   - Only jump forward, never backward" << std::endl;
    std::cout << "   - Only use for error cleanup or breaking nested loops" << std::endl;
    std::cout << "   - Document WHY goto was necessary" << std::endl;
    
    // ============ HISTORICAL CONTEXT ============
    std::cout << "\n=== Historical Context ===" << std::endl;
    std::cout << "goto was heavily used in:" << std::endl;
    std::cout << "- Early FORTRAN, BASIC, and assembly programming" << std::endl;
    std::cout << "- Dijkstra's 1968 letter 'Go To Statement Considered Harmful'" << std::endl;
    std::cout << "- Modern consensus: structured programming is better" << std::endl;
}

bool some_condition = false;
bool another_condition = false;

int main() {
    demonstrate_goto();
    return 0;
}