#include <iostream>
#include <string>

// ============================================================================
// 1. MULTIPLE INHERITANCE & DIAMOND PROBLEM
// ============================================================================

void demonstrate_multiple_inheritance() {
    std::cout << "\n=== MULTIPLE INHERITANCE ===\n";
    
    // Base class A
    class A {
    public:
        int value_a;
        A(int val = 0) : value_a(val) {
            std::cout << "A constructor: " << value_a << "\n";
        }
        
        virtual ~A() {
            std::cout << "A destructor\n";
        }
        
        virtual void display() const {
            std::cout << "Class A: " << value_a << "\n";
        }
        
        void method_a() {
            std::cout << "Method A specific\n";
        }
    };
    
    // Base class B
    class B {
    public:
        int value_b;
        B(int val = 0) : value_b(val) {
            std::cout << "B constructor: " << value_b << "\n";
        }
        
        virtual ~B() {
            std::cout << "B destructor\n";
        }
        
        virtual void display() const {
            std::cout << "Class B: " << value_b << "\n";
        }
        
        void method_b() {
            std::cout << "Method B specific\n";
        }
    };
    
    // Simple multiple inheritance
    class C : public A, public B {
    public:
        int value_c;
        
        C(int a_val, int b_val, int c_val) 
            : A(a_val), B(b_val), value_c(c_val) {
            std::cout << "C constructor: " << value_c << "\n";
        }
        
        ~C() override {
            std::cout << "C destructor\n";
        }
        
        // Can access both A and B members
        void show_all() const {
            std::cout << "C contains: A=" << value_a 
                      << ", B=" << value_b 
                      << ", C=" << value_c << "\n";
        }
        
        // Must resolve ambiguity if both bases have same method
        void display() const override {
            // Call both base implementations
            A::display();
            B::display();
            std::cout << "Class C: " << value_c << "\n";
        }
    };
    
    C c(10, 20, 30);
    c.show_all();
    c.method_a();  // From A
    c.method_b();  // From B
    c.display();   // Calls C's overridden version
    
    // ============================================================================
    // DIAMOND PROBLEM
    // ============================================================================
    
    std::cout << "\n=== DIAMOND PROBLEM ===\n";
    
    class Base {
    public:
        int data;
        Base(int d = 0) : data(d) {
            std::cout << "Base constructor: " << data << "\n";
        }
        
        virtual ~Base() {
            std::cout << "Base destructor\n";
        }
        
        virtual void func() {
            std::cout << "Base::func(): " << data << "\n";
        }
    };
    
    // PROBLEM: Without virtual inheritance
    class Derived1 : public Base {
    public:
        Derived1(int d) : Base(d) {
            std::cout << "Derived1 constructor\n";
        }
    };
    
    class Derived2 : public Base {
    public:
        Derived2(int d) : Base(d) {
            std::cout << "Derived2 constructor\n";
        }
    };
    
    // This creates TWO separate Base subobjects in Final
    class FinalProblem : public Derived1, public Derived2 {
    public:
        FinalProblem(int d1, int d2) : Derived1(d1), Derived2(d2) {
            std::cout << "FinalProblem constructor\n";
        }
        
        void show_problem() {
            // Which 'data' member? Ambiguous!
            // Derived1::data and Derived2::data are DIFFERENT instances
            std::cout << "Derived1::data: " << Derived1::data << "\n";
            std::cout << "Derived2::data: " << Derived2::data << "\n";
            
            // Must specify which Base subobject to call
            Derived1::func();
            Derived2::func();
        }
    };
    
    FinalProblem problem(100, 200);
    problem.show_problem();
    
    // ============================================================================
    // SOLUTION: Virtual Inheritance
    // ============================================================================
    
    std::cout << "\n=== VIRTUAL INHERITANCE SOLUTION ===\n";
    
    class VirtualBase {
    public:
        int shared_data;
        VirtualBase(int d = 0) : shared_data(d) {
            std::cout << "VirtualBase constructor: " << shared_data << "\n";
        }
        
        virtual ~VirtualBase() {
            std::cout << "VirtualBase destructor\n";
        }
        
        virtual void virtual_func() {
            std::cout << "VirtualBase::virtual_func(): " << shared_data << "\n";
        }
    };
    
    // Virtual inheritance - share the same Base instance
    class VirtualDerived1 : virtual public VirtualBase {
    public:
        VirtualDerived1(int d, int d1) : VirtualBase(d) {
            std::cout << "VirtualDerived1 constructor: " << d1 << "\n";
        }
    };
    
    class VirtualDerived2 : virtual public VirtualBase {
    public:
        VirtualDerived2(int d, int d2) : VirtualBase(d) {
            std::cout << "VirtualDerived2 constructor: " << d2 << "\n";
        }
    };
    
    // Now FinalSolution has ONLY ONE VirtualBase subobject
    class FinalSolution : public VirtualDerived1, public VirtualDerived2 {
    public:
        // VirtualBase MUST be initialized by the most derived class
        FinalSolution(int base_val, int d1_val, int d2_val, int final_val)
            : VirtualBase(base_val),      // Initialize shared base
              VirtualDerived1(base_val, d1_val),  // Don't initialize VirtualBase here
              VirtualDerived2(base_val, d2_val) { // Don't initialize VirtualBase here
            std::cout << "FinalSolution constructor: " << final_val << "\n";
        }
        
        void show_solution() {
            // Only ONE shared_data member now
            std::cout << "shared_data: " << shared_data << "\n";
            
            // No ambiguity
            virtual_func();
            
            // Can also access through derived classes (same object)
            VirtualDerived1::virtual_func();
            VirtualDerived2::virtual_func();
        }
    };
    
    FinalSolution solution(42, 1, 2, 3);
    solution.show_solution();
    
    // ============================================================================
    // PRACTICAL EXAMPLE: Input/Output Streams
    // ============================================================================
    
    std::cout << "\n=== PRACTICAL EXAMPLE: IOStream Hierarchy ===\n";
    
    // This is how std::iostream is implemented:
    // class ios_base { ... };
    // class basic_ios : virtual public ios_base { ... };
    // class basic_istream : virtual public basic_ios { ... };
    // class basic_ostream : virtual public basic_ios { ... };
    // class basic_iostream : public basic_istream, public basic_ostream { ... };
    
    // Benefits of virtual inheritance in iostream:
    // 1. Single ios_base object shared by istream and ostream
    // 2. Stream state (good, fail, eof) is shared
    // 3. Formatting flags are shared
}

#include <iostream>
#include <cmath>

// ============================================================================
// 2. FRIEND CLASSES & FUNCTIONS
// ============================================================================

void demonstrate_friends() {
    std::cout << "\n=== FRIEND CLASSES & FUNCTIONS ===\n";
    
    // ============================================================================
    // FRIEND FUNCTIONS
    // ============================================================================
    
    class Vector2D {
    private:
        double x, y;
        
    public:
        Vector2D(double x = 0, double y = 0) : x(x), y(y) {}
        
        // Declare friend functions
        friend Vector2D operator+(const Vector2D& a, const Vector2D& b);
        friend Vector2D operator*(double scalar, const Vector2D& v);
        friend std::ostream& operator<<(std::ostream& os, const Vector2D& v);
        friend bool operator==(const Vector2D& a, const Vector2D& b);
        
        // Non-friend member function
        double magnitude() const {
            return std::sqrt(x * x + y * y);
        }
        
        // Getter functions
        double getX() const { return x; }
        double getY() const { return y; }
    };
    
    // Friend function definitions - can access private members
    Vector2D operator+(const Vector2D& a, const Vector2D& b) {
        return Vector2D(a.x + b.x, a.y + b.y);  // Direct access to private members
    }
    
    Vector2D operator*(double scalar, const Vector2D& v) {
        return Vector2D(scalar * v.x, scalar * v.y);
    }
    
    std::ostream& operator<<(std::ostream& os, const Vector2D& v) {
        os << "(" << v.x << ", " << v.y << ")";
        return os;
    }
    
    bool operator==(const Vector2D& a, const Vector2D& b) {
        return a.x == b.x && a.y == b.y;
    }
    
    Vector2D v1(3, 4), v2(1, 2);
    std::cout << "v1: " << v1 << ", magnitude: " << v1.magnitude() << "\n";
    std::cout << "v2: " << v2 << "\n";
    std::cout << "v1 + v2: " << (v1 + v2) << "\n";
    std::cout << "2 * v1: " << (2.0 * v1) << "\n";
    
    // ============================================================================
    // FRIEND CLASSES
    // ============================================================================
    
    class Matrix;  // Forward declaration
    
    class Vector {
    private:
        double data[3];
        
    public:
        Vector(double x = 0, double y = 0, double z = 0) {
            data[0] = x; data[1] = y; data[2] = z;
        }
        
        // Declare Matrix as friend class
        friend class Matrix;
        
        // Friend specific member function of another class
        friend double Matrix::multiply_row(const Vector& v, int row) const;
        
        void print() const {
            std::cout << "Vector: [" << data[0] << ", " 
                      << data[1] << ", " << data[2] << "]\n";
        }
    };
    
    class Matrix {
    private:
        double data[3][3];
        
    public:
        Matrix() {
            for (int i = 0; i < 3; ++i)
                for (int j = 0; j < 3; ++j)
                    data[i][j] = (i == j) ? 1.0 : 0.0;  // Identity matrix
        }
        
        // Can access Vector's private members
        Vector multiply(const Vector& v) const {
            Vector result;
            for (int i = 0; i < 3; ++i) {
                result.data[i] = 0;
                for (int j = 0; j < 3; ++j) {
                    result.data[i] += data[i][j] * v.data[j];  // Direct access!
                }
            }
            return result;
        }
        
        // Friend function declaration in Vector refers to this
        double multiply_row(const Vector& v, int row) const {
            double sum = 0;
            for (int j = 0; j < 3; ++j) {
                sum += data[row][j] * v.data[j];
            }
            return sum;
        }
        
        void set_value(int i, int j, double value) {
            data[i][j] = value;
        }
    };
    
    Matrix m;
    m.set_value(0, 1, 2.0);  // Add some non-diagonal element
    
    Vector v(1, 2, 3);
    Vector result = m.multiply(v);
    
    std::cout << "\nMatrix-Vector multiplication:\n";
    v.print();
    std::cout << "Result: ";
    result.print();
    
    // ============================================================================
    // WHEN TO USE FRIENDS
    // ============================================================================
    
    std::cout << "\n=== WHEN TO USE FRIENDS ===\n";
    
    // Case 1: Operator overloading for symmetric operations
    class Complex {
    private:
        double real, imag;
        
    public:
        Complex(double r = 0, double i = 0) : real(r), imag(i) {}
        
        // Member function for this * scalar (natural)
        Complex operator*(double scalar) const {
            return Complex(real * scalar, imag * scalar);
        }
        
        // Friend for scalar * this (symmetric)
        friend Complex operator*(double scalar, const Complex& c) {
            return c * scalar;  // Reuse member function
        }
        
        friend std::ostream& operator<<(std::ostream& os, const Complex& c);
    };
    
    std::ostream& operator<<(std::ostream& os, const Complex& c) {
        os << c.real << " + " << c.imag << "i";
        return os;
    }
    
    Complex c(3, 4);
    std::cout << "Complex: " << c << "\n";
    std::cout << "c * 2: " << (c * 2) << "\n";
    std::cout << "2 * c: " << (2 * c) << "\n";  // Needs friend
    
    // Case 2: Factory functions that need access to private constructors
    class Logger {
    private:
        std::string name;
        // Private constructor - only friends can create instances
        Logger(const std::string& name) : name(name) {}
        
    public:
        // Factory function as friend
        friend Logger create_logger(const std::string& name);
        
        void log(const std::string& message) {
            std::cout << "[" << name << "] " << message << "\n";
        }
    };
    
    Logger create_logger(const std::string& name) {
        // Can call private constructor
        return Logger(name);
    }
    
    // Logger logger("test");  // ERROR: constructor is private
    Logger logger = create_logger("System");  // OK: friend factory
    logger.log("System initialized");
    
    // Case 3: Tightly coupled classes (like iterator-container)
    class ContainerIterator;
    
    class Container {
    private:
        int* data;
        size_t size;
        
    public:
        Container(size_t n) : size(n) {
            data = new int[n];
            for (size_t i = 0; i < n; ++i) data[i] = i;
        }
        
        ~Container() { delete[] data; }
        
        // Iterator needs access to private data
        friend class ContainerIterator;
    };
    
    class ContainerIterator {
    private:
        Container& container;
        size_t index;
        
    public:
        ContainerIterator(Container& c, size_t idx = 0) 
            : container(c), index(idx) {}
        
        int& operator*() {
            return container.data[index];  // Direct access
        }
        
        ContainerIterator& operator++() {
            ++index;
            return *this;
        }
        
        bool operator!=(const ContainerIterator& other) const {
            return index != other.index;
        }
    };
    
    // ============================================================================
    // FRIENDSHIP IS NOT TRANSITIVE OR INHERITED
    // ============================================================================
    
    class BaseClass {
    private:
        int secret;
        
    public:
        BaseClass() : secret(42) {}
        
        // Friend declaration
        friend class FriendClass;
    };
    
    class FriendClass {
    public:
        void access_base(BaseClass& b) {
            std::cout << "FriendClass accessing BaseClass secret: " 
                      << b.secret << "\n";
        }
    };
    
    class DerivedFromFriend : public FriendClass {
    public:
        // CANNOT access BaseClass::secret!
        // Friendship is not inherited
        void try_access(BaseClass& b) {
            // std::cout << b.secret;  // ERROR
        }
    };
    
    class AnotherClass {
    public:
        // CANNOT access BaseClass::secret!
        // Friendship is not transitive
        void try_access(BaseClass& b) {
            // std::cout << b.secret;  // ERROR
        }
    };
}


#include <iostream>
#include <vector>
#include <algorithm>

// ============================================================================
// 3. NESTED CLASSES
// ============================================================================

void demonstrate_nested_classes() {
    std::cout << "\n=== NESTED CLASSES ===\n";
    
    // ============================================================================
    // PUBLIC NESTED CLASSES
    // ============================================================================
    
    class LinkedList {
    public:
        // Public nested class - part of the interface
        class Node {
        public:
            int data;
            Node* next;
            
            Node(int value) : data(value), next(nullptr) {}
            
            void print() const {
                std::cout << "Node[" << data << "]";
            }
        };
        
    private:
        Node* head;
        
        // Private nested class - implementation detail
        class IteratorImpl {
            Node* current;
            
        public:
            IteratorImpl(Node* node) : current(node) {}
            
            bool operator!=(const IteratorImpl& other) const {
                return current != other.current;
            }
            
            IteratorImpl& operator++() {
                if (current) current = current->next;
                return *this;
            }
            
            int& operator*() {
                return current->data;
            }
        };
        
    public:
        LinkedList() : head(nullptr) {}
        
        ~LinkedList() {
            while (head) {
                Node* temp = head;
                head = head->next;
                delete temp;
            }
        }
        
        void append(int value) {
            Node* new_node = new Node(value);
            if (!head) {
                head = new_node;
            } else {
                Node* current = head;
                while (current->next) {
                    current = current->next;
                }
                current->next = new_node;
            }
        }
        
        // Public iterator using nested class
        class Iterator {
            IteratorImpl impl;
            
        public:
            Iterator(Node* node) : impl(node) {}
            
            bool operator!=(const Iterator& other) const {
                return impl != other.impl;
            }
            
            Iterator& operator++() {
                ++impl;
                return *this;
            }
            
            int& operator*() {
                return *impl;
            }
        };
        
        Iterator begin() { return Iterator(head); }
        Iterator end() { return Iterator(nullptr); }
        
        // Access to public nested class from outside
        Node* get_head() const { return head; }
    };
    
    LinkedList list;
    list.append(10);
    list.append(20);
    list.append(30);
    
    std::cout << "LinkedList contents: ";
    for (int value : list) {  // Using iterator
        std::cout << value << " ";
    }
    std::cout << "\n";
    
    // Can create Node objects outside LinkedList
    LinkedList::Node external_node(99);
    external_node.print();
    std::cout << "\n";
    
    // ============================================================================
    // PRIVATE NESTED CLASSES
    // ============================================================================
    
    class Tree {
    private:
        // Private nested class - completely hidden
        class TreeNode {
        private:
            int value;
            TreeNode* left;
            TreeNode* right;
            
            // TreeNode can access Tree's private members
            // But Tree CANNOT access TreeNode's private members
            // unless declared as friend
            
        public:
            TreeNode(int val) : value(val), left(nullptr), right(nullptr) {}
            
            // Friend declaration allows Tree to access TreeNode's private members
            friend class Tree;
            
            void print(int depth = 0) const {
                if (right) right->print(depth + 1);
                std::cout << std::string(depth * 2, ' ') << value << "\n";
                if (left) left->print(depth + 1);
            }
        };
        
        TreeNode* root;
        
    public:
        Tree() : root(nullptr) {}
        
        void insert(int value) {
            root = insert_recursive(root, value);
        }
        
        void print() const {
            if (root) {
                root->print();
            } else {
                std::cout << "Empty tree\n";
            }
        }
        
    private:
        // Can access TreeNode's private members because TreeNode declared Tree as friend
        TreeNode* insert_recursive(TreeNode* node, int value) {
            if (!node) {
                return new TreeNode(value);
            }
            
            if (value < node->value) {
                node->left = insert_recursive(node->left, value);
            } else {
                node->right = insert_recursive(node->right, value);
            }
            
            return node;
        }
    };
    
    Tree tree;
    tree.insert(50);
    tree.insert(30);
    tree.insert(70);
    tree.insert(20);
    tree.insert(40);
    tree.insert(60);
    tree.insert(80);
    
    std::cout << "\nBinary Search Tree:\n";
    tree.print();
    
    // ============================================================================
    // NESTED CLASSES WITH TEMPLATES
    // ============================================================================
    
    template<typename T>
    class Graph {
    public:
        class Vertex {
        private:
            T data;
            std::vector<Vertex*> neighbors;
            
        public:
            Vertex(const T& d) : data(d) {}
            
            void add_neighbor(Vertex* neighbor) {
                neighbors.push_back(neighbor);
            }
            
            const T& get_data() const { return data; }
            
            void print() const {
                std::cout << "Vertex " << data << " -> ";
                for (auto* neighbor : neighbors) {
                    std::cout << neighbor->data << " ";
                }
                std::cout << "\n";
            }
        };
        
    private:
        std::vector<Vertex*> vertices;
        
    public:
        ~Graph() {
            for (auto* vertex : vertices) {
                delete vertex;
            }
        }
        
        Vertex* add_vertex(const T& data) {
            Vertex* new_vertex = new Vertex(data);
            vertices.push_back(new_vertex);
            return new_vertex;
        }
        
        void add_edge(Vertex* from, Vertex* to) {
            from->add_neighbor(to);
        }
        
        void print() const {
            for (auto* vertex : vertices) {
                vertex->print();
            }
        }
    };
    
    Graph<std::string> social_network;
    auto* alice = social_network.add_vertex("Alice");
    auto* bob = social_network.add_vertex("Bob");
    auto* charlie = social_network.add_vertex("Charlie");
    
    social_network.add_edge(alice, bob);
    social_network.add_edge(alice, charlie);
    social_network.add_edge(bob, charlie);
    
    std::cout << "\nSocial Network Graph:\n";
    social_network.print();
    
    // ============================================================================
    // LOCAL CLASSES (Nested within functions)
    // ============================================================================
    
    auto create_counter = []() {
        // Local class inside lambda/function
        class Counter {
        private:
            int count;
            
        public:
            Counter() : count(0) {}
            
            int increment() { return ++count; }
            int get() const { return count; }
        };
        
        return Counter();  // Returns instance of local class
    };
    
    auto counter = create_counter();
    std::cout << "\nLocal class counter: " << counter.increment() << "\n";
    std::cout << "Local class counter: " << counter.increment() << "\n";
    
    // ============================================================================
    // ENUMERATION CLASSES INSIDE CLASSES
    // ============================================================================
    
    class NetworkConnection {
    public:
        // Nested enum class - strongly typed
        enum class State {
            DISCONNECTED,
            CONNECTING,
            CONNECTED,
            ERROR
        };
        
        enum class Protocol {
            TCP,
            UDP,
            HTTP,
            HTTPS
        };
        
    private:
        State current_state;
        Protocol protocol;
        
    public:
        NetworkConnection(Protocol p) 
            : current_state(State::DISCONNECTED), protocol(p) {}
        
        void connect() {
            if (current_state == State::DISCONNECTED) {
                current_state = State::CONNECTING;
                std::cout << "Connecting using ";
                
                switch (protocol) {
                    case Protocol::TCP: std::cout << "TCP"; break;
                    case Protocol::UDP: std::cout << "UDP"; break;
                    case Protocol::HTTP: std::cout << "HTTP"; break;
                    case Protocol::HTTPS: std::cout << "HTTPS"; break;
                }
                std::cout << "...\n";
                
                current_state = State::CONNECTED;
            }
        }
        
        State get_state() const { return current_state; }
    };
    
    NetworkConnection conn(NetworkConnection::Protocol::HTTPS);
    conn.connect();
}


#include <iostream>
#include <type_traits>

// ============================================================================
// 4. CRTP (Curiously Recurring Template Pattern)
// ============================================================================

void demonstrate_crtp() {
    std::cout << "\n=== CRTP (Curiously Recurring Template Pattern) ===\n";
    
    // ============================================================================
    // BASIC CRTP PATTERN
    // ============================================================================
    
    template<typename Derived>
    class Base {
    public:
        // Method that uses the derived class
        void interface() {
            static_cast<Derived*>(this)->implementation();
        }
        
        // Can provide default implementation
        void default_implementation() {
            std::cout << "Default implementation in Base\n";
        }
        
        // CRTP allows static polymorphism (compile-time)
        void call_implementation() {
            // Calls derived class method without virtual functions
            static_cast<Derived*>(this)->implementation();
        }
    };
    
    class Derived1 : public Base<Derived1> {
    public:
        void implementation() {
            std::cout << "Derived1 specific implementation\n";
        }
    };
    
    class Derived2 : public Base<Derived2> {
    public:
        void implementation() {
            std::cout << "Derived2 specific implementation\n";
        }
        
        // Can also use default
        void default_implementation() {
            std::cout << "Derived2 overridden default\n";
        }
    };
    
    Derived1 d1;
    Derived2 d2;
    
    d1.interface();  // Calls Derived1::implementation
    d2.interface();  // Calls Derived2::implementation
    
    d1.default_implementation();  // Calls Base::default_implementation
    d2.default_implementation();  // Calls Derived2::default_implementation
    
    // ============================================================================
    // CRTP FOR STATIC POLYMORPHISM (NO VTABLE OVERHEAD)
    // ============================================================================
    
    template<typename T>
    class ShapeCRTP {
    public:
        double area() const {
            // Statically dispatches to derived class
            return static_cast<const T*>(this)->compute_area();
        }
        
        void print_area() const {
            std::cout << "Area: " << area() << "\n";
        }
        
        // Common functionality that uses derived methods
        void scale_and_print(double factor) {
            static_cast<T*>(this)->scale(factor);
            print_area();
        }
    };
    
    class CircleCRTP : public ShapeCRTP<CircleCRTP> {
    private:
        double radius;
        
    public:
        CircleCRTP(double r) : radius(r) {}
        
        double compute_area() const {
            return 3.14159 * radius * radius;
        }
        
        void scale(double factor) {
            radius *= factor;
        }
    };
    
    class SquareCRTP : public ShapeCRTP<SquareCRTP> {
    private:
        double side;
        
    public:
        SquareCRTP(double s) : side(s) {}
        
        double compute_area() const {
            return side * side;
        }
        
        void scale(double factor) {
            side *= factor;
        }
    };
    
    CircleCRTP circle(5.0);
    SquareCRTP square(4.0);
    
    std::cout << "\nCRTP Shapes:\n";
    circle.print_area();  // Static dispatch, no vtable lookup
    square.print_area();
    
    // Can't store in homogeneous container like with virtual functions
    // ShapeCRTP<CircleCRTP>* ptr = &circle; // Type is specific
    
    // ============================================================================
    // CRTP FOR OBJECT COUNTING
    // ============================================================================
    
    template<typename T>
    class ObjectCounter {
    protected:
        // Protected constructor to prevent direct instantiation
        ObjectCounter() {
            ++count;
            ++total_count;
        }
        
        // Protected destructor
        ~ObjectCounter() {
            --count;
        }
        
    public:
        // Static methods to access counts
        static int get_count() { return count; }
        static int get_total_count() { return total_count; }
        
    private:
        static inline int count = 0;
        static inline int total_count = 0;
    };
    
    class Widget : public ObjectCounter<Widget> {
    public:
        Widget() { std::cout << "Widget created\n"; }
        ~Widget() { std::cout << "Widget destroyed\n"; }
    };
    
    class Gadget : public ObjectCounter<Gadget> {
    public:
        Gadget() { std::cout << "Gadget created\n"; }
        ~Gadget() { std::cout << "Gadget destroyed\n"; }
    };
    
    std::cout << "\nObject Counting with CRTP:\n";
    std::cout << "Initial Widget count: " << Widget::get_count() << "\n";
    std::cout << "Initial Gadget count: " << Gadget::get_count() << "\n";
    
    {
        Widget w1, w2;
        Gadget g1;
        
        std::cout << "Widget count: " << Widget::get_count() << "\n";
        std::cout << "Gadget count: " << Gadget::get_count() << "\n";
        std::cout << "Total Widgets ever: " << Widget::get_total_count() << "\n";
    }
    
    std::cout << "After scope - Widget count: " << Widget::get_count() << "\n";
    
    // ============================================================================
    // CRTP FOR MIXIN CLASSES
    // ============================================================================
    
    // Mixin: Adds functionality to derived class
    
    template<typename Derived>
    class Comparable {
    public:
        bool operator==(const Derived& other) const {
            return !(static_cast<const Derived*>(this)->operator<(other)) &&
                   !(other < *static_cast<const Derived*>(this));
        }
        
        bool operator!=(const Derived& other) const {
            return !(*this == other);
        }
        
        bool operator>(const Derived& other) const {
            return other < *static_cast<const Derived*>(this);
        }
        
        bool operator<=(const Derived& other) const {
            return !(other < *static_cast<const Derived*>(this));
        }
        
        bool operator>=(const Derived& other) const {
            return !(static_cast<const Derived*>(this)->operator<(other));
        }
    };
    
    class Person : public Comparable<Person> {
    private:
        std::string name;
        int age;
        
    public:
        Person(std::string n, int a) : name(n), age(a) {}
        
        // Only need to implement operator<
        bool operator<(const Person& other) const {
            if (name != other.name) return name < other.name;
            return age < other.age;
        }
        
        void print() const {
            std::cout << name << " (" << age << ")\n";
        }
    };
    
    Person alice("Alice", 30);
    Person bob("Bob", 25);
    Person alice2("Alice", 30);
    
    std::cout << "\nComparable Mixin:\n";
    std::cout << "alice < bob: " << (alice < bob) << "\n";
    std::cout << "alice == bob: " << (alice == bob) << "\n";
    std::cout << "alice == alice2: " << (alice == alice2) << "\n";
    std::cout << "alice != bob: " << (alice != bob) << "\n";
    std::cout << "alice > bob: " << (alice > bob) << "\n";
    
    // ============================================================================
    // CRTP FOR SINGLETON PATTERN
    // ============================================================================
    
    template<typename T>
    class Singleton {
    protected:
        Singleton() = default;
        
    public:
        // Delete copy operations
        Singleton(const Singleton&) = delete;
        Singleton& operator=(const Singleton&) = delete;
        
        // Get instance
        static T& get_instance() {
            static T instance;  // Meyer's Singleton
            return instance;
        }
    };
    
    class DatabaseManager : public Singleton<DatabaseManager> {
    private:
        friend class Singleton<DatabaseManager>;  // Allow Singleton to construct
        
        DatabaseManager() {
            std::cout << "DatabaseManager initialized\n";
        }
        
    public:
        void connect() {
            std::cout << "Database connected\n";
        }
        
        void query(const std::string& sql) {
            std::cout << "Executing: " << sql << "\n";
        }
    };
    
    std::cout << "\nSingleton with CRTP:\n";
    DatabaseManager::get_instance().connect();
    DatabaseManager::get_instance().query("SELECT * FROM users");
    
    // ============================================================================
    // ADVANCED: CRTP WITH CONCEPTS (C++20)
    // ============================================================================
    
    #if __cplusplus >= 202002L
    template<typename Derived>
    concept HasArea = requires(const Derived& d) {
        { d.compute_area() } -> std::convertible_to<double>;
    };
    
    template<HasArea Derived>
    class ShapeWithConcept : public ShapeCRTP<Derived> {
        // Compile-time check that Derived has compute_area()
    };
    #endif
    
    // ============================================================================
    // LIMITATIONS OF CRTP
    // ============================================================================
    
    // 1. Can't store different CRTP types in same container easily
    // 2. Derived class must know its base template argument
    // 3. More complex error messages
    // 4. No runtime polymorphism
    
    std::cout << "\nCRTP Limitations:\n";
    // ShapeCRTP<CircleCRTP> shapes[] = {circle, square}; // ERROR: different types
}


#include <iostream>
#include <functional>
#include <memory>
#include <vector>
#include <any>

// ============================================================================
// 5. TYPE ERASURE
// ============================================================================

void demonstrate_type_erasure() {
    std::cout << "\n=== TYPE ERASURE ===\n";
    
    // ============================================================================
    // std::function - TYPE ERASURE FOR CALLABLES
    // ============================================================================
    
    std::cout << "\n=== std::function ===\n";
    
    // std::function can store any callable with matching signature
    std::function<int(int, int)> operation;
    
    // Store a lambda
    operation = [](int a, int b) { return a + b; };
    std::cout << "Lambda add: " << operation(10, 20) << "\n";
    
    // Store a function pointer
    int multiply(int a, int b) { return a * b; }
    operation = multiply;
    std::cout << "Function multiply: " << operation(10, 20) << "\n";
    
    // Store a functor
    struct Divider {
        int operator()(int a, int b) const { return a / b; }
    };
    operation = Divider();
    std::cout << "Functor divide: " << operation(20, 5) << "\n";
    
    // Store member function with std::bind
    class Calculator {
    public:
        int power(int base, int exponent) {
            int result = 1;
            for (int i = 0; i < exponent; ++i) result *= base;
            return result;
        }
    };
    
    Calculator calc;
    operation = std::bind(&Calculator::power, &calc, 
                         std::placeholders::_1, std::placeholders::_2);
    std::cout << "Member function power: " << operation(2, 8) << "\n";
    
    // std::function in containers
    std::vector<std::function<double(double)>> transforms;
    transforms.push_back([](double x) { return x * x; });
    transforms.push_back([](double x) { return std::sqrt(x); });
    transforms.push_back([](double x) { return std::sin(x); });
    
    double value = 2.0;
    std::cout << "\nApplying transforms to " << value << ":\n";
    for (const auto& transform : transforms) {
        std::cout << "Result: " << transform(value) << "\n";
    }
    
    // ============================================================================
    // CUSTOM TYPE ERASURE PATTERN
    // ============================================================================
    
    std::cout << "\n=== CUSTOM TYPE ERASURE ===\n";
    
    // Manual type erasure implementation
    class Drawable {
    private:
        // Concept - what operations do we need?
        struct DrawableConcept {
            virtual ~DrawableConcept() = default;
            virtual void draw() const = 0;
            virtual std::unique_ptr<DrawableConcept> clone() const = 0;
        };
        
        // Model - implements concept for specific type
        template<typename T>
        struct DrawableModel : DrawableConcept {
            T data;
            
            DrawableModel(const T& d) : data(d) {}
            DrawableModel(T&& d) : data(std::move(d)) {}
            
            void draw() const override {
                data.draw();  // Requires T has draw() method
            }
            
            std::unique_ptr<DrawableConcept> clone() const override {
                return std::make_unique<DrawableModel<T>>(data);
            }
        };
        
        std::unique_ptr<DrawableConcept> pimpl;
        
    public:
        // Constructor template - accepts any type with draw() method
        template<typename T>
        Drawable(T&& obj) 
            : pimpl(std::make_unique<DrawableModel<std::decay_t<T>>>(
                std::forward<T>(obj))) {}
        
        // Copy operations
        Drawable(const Drawable& other) 
            : pimpl(other.pimpl ? other.pimpl->clone() : nullptr) {}
        
        Drawable& operator=(const Drawable& other) {
            if (this != &other) {
                pimpl = other.pimpl ? other.pimpl->clone() : nullptr;
            }
            return *this;
        }
        
        // Move operations
        Drawable(Drawable&&) = default;
        Drawable& operator=(Drawable&&) = default;
        
        // Interface
        void draw() const {
            if (pimpl) pimpl->draw();
        }
    };
    
    // Types that can be stored in Drawable
    class CircleType {
    public:
        void draw() const {
            std::cout << "Drawing CircleType\n";
        }
    };
    
    class SquareType {
    public:
        void draw() const {
            std::cout << "Drawing SquareType\n";
        }
    };
    
    // Can store different types in same container
    std::vector<Drawable> shapes;
    shapes.push_back(CircleType());
    shapes.push_back(SquareType());
    shapes.push_back([]() {  // Even a lambda with draw()
        struct LambdaDrawable {
            void draw() const {
                std::cout << "Drawing from lambda\n";
            }
        };
        return LambdaDrawable();
    }());
    
    std::cout << "\nDrawing all shapes:\n";
    for (const auto& shape : shapes) {
        shape.draw();
    }
    
    // ============================================================================
    // TYPE ERASURE WITH std::any (C++17)
    // ============================================================================
    
    std::cout << "\n=== std::any TYPE ERASURE ===\n";
    
    class AnyDrawable {
    private:
        std::any storage;
        void (*draw_func)(const std::any&);
        
        template<typename T>
        static void draw_impl(const std::any& obj) {
            if (obj.has_value()) {
                std::any_cast<T>(obj).draw();
            }
        }
        
    public:
        template<typename T>
        AnyDrawable(T&& obj) 
            : storage(std::forward<T>(obj)),
              draw_func(&draw_impl<std::decay_t<T>>) {}
        
        void draw() const {
            if (draw_func) {
                draw_func(storage);
            }
        }
    };
    
    AnyDrawable any_circle(CircleType());
    AnyDrawable any_square(SquareType());
    
    std::cout << "AnyDrawable circle: ";
    any_circle.draw();
    std::cout << "AnyDrawable square: ";
    any_square.draw();
    
    // ============================================================================
    // TYPE ERASURE VS VIRTUAL FUNCTIONS
    // ============================================================================
    
    std::cout << "\n=== TYPE ERASURE vs VIRTUAL FUNCTIONS ===\n";
    
    // Virtual function approach (traditional polymorphism)
    class AnimalVirtual {
    public:
        virtual ~AnimalVirtual() = default;
        virtual void speak() const = 0;
        virtual std::unique_ptr<AnimalVirtual> clone() const = 0;
    };
    
    class DogVirtual : public AnimalVirtual {
    public:
        void speak() const override {
            std::cout << "Woof!\n";
        }
        
        std::unique_ptr<AnimalVirtual> clone() const override {
            return std::make_unique<DogVirtual>(*this);
        }
    };
    
    class CatVirtual : public AnimalVirtual {
    public:
        void speak() const override {
            std::cout << "Meow!\n";
        }
        
        std::unique_ptr<AnimalVirtual> clone() const override {
            return std::make_unique<CatVirtual>(*this);
        }
    };
    
    // Type erasure approach
    class AnimalErased {
    private:
        struct Concept {
            virtual ~Concept() = default;
            virtual void speak() const = 0;
            virtual std::unique_ptr<Concept> clone() const = 0;
        };
        
        template<typename T>
        struct Model : Concept {
            T animal;
            
            Model(const T& a) : animal(a) {}
            
            void speak() const override {
                animal.speak();
            }
            
            std::unique_ptr<Concept> clone() const override {
                return std::make_unique<Model<T>>(animal);
            }
        };
        
        std::unique_ptr<Concept> pimpl;
        
    public:
        template<typename T>
        AnimalErased(T&& animal) 
            : pimpl(std::make_unique<Model<std::decay_t<T>>>(std::forward<T>(animal))) {}
        
        void speak() const {
            pimpl->speak();
        }
    };
    
    // Non-virtual types that can be type-erased
    struct DogSimple {
        void speak() const { std::cout << "Simple Woof!\n"; }
    };
    
    struct CatSimple {
        void speak() const { std::cout << "Simple Meow!\n"; }
    };
    
    struct Robot {
        void speak() const { std::cout << "Beep boop!\n"; }
    };
    
    std::cout << "\nVirtual functions approach:\n";
    std::vector<std::unique_ptr<AnimalVirtual>> virtual_animals;
    virtual_animals.push_back(std::make_unique<DogVirtual>());
    virtual_animals.push_back(std::make_unique<CatVirtual>());
    
    for (const auto& animal : virtual_animals) {
        animal->speak();
    }
    
    std::cout << "\nType erasure approach:\n";
    std::vector<AnimalErased> erased_animals;
    erased_animals.push_back(DogSimple());
    erased_animals.push_back(CatSimple());
    erased_animals.push_back(Robot());  // Can add Robot without inheritance!
    
    for (const auto& animal : erased_animals) {
        animal.speak();
    }
    
    // ============================================================================
    // PERFORMANCE CONSIDERATIONS
    // ============================================================================
    
    std::cout << "\n=== PERFORMANCE CONSIDERATIONS ===\n";
    
    // Virtual functions:
    // - One indirection (vtable lookup)
    // - Good cache locality for same type
    // - Overhead per object (vptr)
    
    // Type erasure (std::function):
    // - Two indirections (function call + type-erased object)
    // - Heap allocation (usually)
    // - More flexible (any callable)
    
    // Small Buffer Optimization (SBO):
    // std::function and some type erasure implementations use SBO
    // - Small objects stored inline (no heap allocation)
    // - Large objects stored on heap
    
    auto small_lambda = []() { return 42; };
    auto large_lambda = [array = std::array<int, 100>{}]() mutable { 
        return array[0]; 
    };
    
    std::function<int()> f1 = small_lambda;  // Likely SBO
    std::function<int()> f2 = large_lambda;  // Likely heap allocation
    
    std::cout << "Small lambda size in std::function: likely inline\n";
    std::cout << "Large lambda size in std::function: likely heap allocated\n";
}

#include <iostream>
#include <memory>
#include <vector>
#include <string>

// ============================================================================
// 6. PIMPL IDIOM (Pointer to Implementation)
// ============================================================================

void demonstrate_pimpl() {
    std::cout << "\n=== PIMPL IDIOM ===\n";
    
    // ============================================================================
    // BASIC PIMPL PATTERN
    // ============================================================================
    
    // widget.h - Public interface
    class Widget {
    public:
        Widget();                           // Constructor
        ~Widget();                          // Destructor (must be in .cpp)
        
        // Rule of Five
        Widget(const Widget& other);        // Copy constructor
        Widget& operator=(const Widget& other); // Copy assignment
        Widget(Widget&& other) noexcept;    // Move constructor
        Widget& operator=(Widget&& other) noexcept; // Move assignment
        
        // Public interface
        void process_data(int value);
        int get_result() const;
        void display() const;
        
    private:
        // Forward declaration of implementation class
        class Impl;
        
        // Pointer to implementation
        std::unique_ptr<Impl> pimpl;
    };
    
    // widget.cpp - Implementation
    class Widget::Impl {
    private:
        int data;
        std::vector<int> processed_data;
        std::string name;
        // Can include private headers here without exposing them in widget.h
        
    public:
        Impl() : data(0), name("WidgetImpl") {
            std::cout << "Widget::Impl constructor\n";
        }
        
        ~Impl() {
            std::cout << "Widget::Impl destructor\n";
        }
        
        void process(int value) {
            data = value;
            processed_data.push_back(value);
            processed_data.push_back(value * 2);
            processed_data.push_back(value * 3);
        }
        
        int get_data() const {
            return data;
        }
        
        const std::vector<int>& get_processed() const {
            return processed_data;
        }
        
        void set_name(const std::string& new_name) {
            name = new_name;
        }
        
        void display() const {
            std::cout << "Widget::Impl: " << name 
                      << ", data=" << data 
                      << ", processed items=" << processed_data.size() << "\n";
        }
    };
    
    // Widget member function implementations
    Widget::Widget() : pimpl(std::make_unique<Impl>()) {
        std::cout << "Widget constructor\n";
    }
    
    Widget::~Widget() = default;  // Must be in .cpp for unique_ptr<Impl>
    
    Widget::Widget(const Widget& other) 
        : pimpl(std::make_unique<Impl>(*other.pimpl)) {
        std::cout << "Widget copy constructor\n";
    }
    
    Widget& Widget::operator=(const Widget& other) {
        if (this != &other) {
            *pimpl = *other.pimpl;
        }
        std::cout << "Widget copy assignment\n";
        return *this;
    }
    
    Widget::Widget(Widget&& other) noexcept = default;
    Widget& Widget::operator=(Widget&& other) noexcept = default;
    
    void Widget::process_data(int value) {
        pimpl->process(value);
    }
    
    int Widget::get_result() const {
        return pimpl->get_data();
    }
    
    void Widget::display() const {
        pimpl->display();
    }
    
    // ============================================================================
    // BENEFITS OF PIMPL
    // ============================================================================
    
    std::cout << "\n=== PIMPL BENEFITS ===\n";
    
    // 1. COMPILATION FIREWALL
    Widget w1;
    w1.process_data(42);
    w1.display();
    
    Widget w2 = w1;  // Copy
    w2.display();
    
    // Changing Widget::Impl doesn't require recompiling Widget's clients
    
    // 2. BINARY COMPATIBILITY
    class LibraryClass {
    private:
        class Impl;
        std::unique_ptr<Impl> pimpl;
        
    public:
        LibraryClass();
        ~LibraryClass();
        
        // Can add new methods without breaking binary compatibility
        void existing_method();
        void new_method();  // Added in version 2.0
    };
    
    // LibraryClass::Impl in .cpp can change without recompiling users
    
    // ============================================================================
    // PIMPL WITH SHARED_PTR
    // ============================================================================
    
    std::cout << "\n=== PIMPL WITH SHARED_PTR ===\n";
    
    class SharedPimpl {
    public:
        SharedPimpl();
        ~SharedPimpl();  // Can be defaulted in header with shared_ptr
        
        // Copy operations work naturally with shared_ptr
        SharedPimpl(const SharedPimpl&) = default;
        SharedPimpl& operator=(const SharedPimpl&) = default;
        
        void do_something();
        
    private:
        struct Impl;
        std::shared_ptr<Impl> pimpl;  // Enables shallow copying
    };
    
    // ============================================================================
    // PIMPL WITH CONST CORRECTNESS
    // ============================================================================
    
    class ConstCorrectWidget {
    public:
        ConstCorrectWidget();
        ~ConstCorrectWidget();
        
        // Const method
        int get_value() const;
        
        // Non-const method
        void set_value(int value);
        
    private:
        class Impl;
        
        // For const methods
        const Impl* get_impl() const { return pimpl.get(); }
        Impl* get_impl() { return pimpl.get(); }
        
        std::unique_ptr<Impl> pimpl;
    };
    
    // ============================================================================
    // ADVANCED PIMPL PATTERNS
    // ============================================================================
    
    // 1. Fast Pimpl (stack allocation for small objects)
    template<typename T, size_t Size, size_t Alignment>
    class FastPimpl {
    private:
        alignas(Alignment) std::byte storage[Size];
        T* ptr() { return reinterpret_cast<T*>(storage); }
        const T* ptr() const { return reinterpret_cast<const T*>(storage); }
        
    public:
        template<typename... Args>
        FastPimpl(Args&&... args) {
            new (storage) T(std::forward<Args>(args)...);
        }
        
        ~FastPimpl() {
            ptr()->~T();
        }
        
        T* operator->() { return ptr(); }
        const T* operator->() const { return ptr(); }
        
        T& operator*() { return *ptr(); }
        const T& operator*() const { return *ptr(); }
    };
    
    // 2. Pimpl with interface inheritance
    class DrawableInterface {
    public:
        virtual ~DrawableInterface() = default;
        virtual void draw() const = 0;
        virtual std::unique_ptr<DrawableInterface> clone() const = 0;
    };
    
    class ShapePimpl {
    private:
        std::unique_ptr<DrawableInterface> pimpl;
        
    public:
        template<typename T>
        ShapePimpl(T shape) 
            : pimpl(std::make_unique<Model<T>>(std::move(shape))) {}
        
        void draw() const {
            pimpl->draw();
        }
        
    private:
        template<typename T>
        class Model : public DrawableInterface {
            T shape;
            
        public:
            Model(T s) : shape(std::move(s)) {}
            
            void draw() const override {
                shape.draw();
            }
            
            std::unique_ptr<DrawableInterface> clone() const override {
                return std::make_unique<Model<T>>(shape);
            }
        };
    };
    
    // ============================================================================
    // WHEN TO USE PIMPL
    // ============================================================================
    
    std::cout << "\n=== WHEN TO USE PIMPL ===\n";
    
    // Use PIMPL when:
    // 1. You need to hide implementation details completely
    // 2. You want to minimize compile-time dependencies
    // 3. You need binary compatibility between library versions
    // 4. You have many private member variables that change frequently
    // 5. You want to reduce header file size
    
    // Don't use PIMPL when:
    // 1. Performance is critical (extra indirection)
    // 2. Class is simple and stable
    // 3. You need inline functions for performance
    // 4. You're implementing templates (PIMPL doesn't work well with templates)
    
    std::cout << "\n=== PIMPL TRADEOFFS ===\n";
    std::cout << "Advantages:\n";
    std::cout << "  - Complete implementation hiding\n";
    std::cout << "  - Reduced compilation dependencies\n";
    std::cout << "  - Better binary compatibility\n";
    std::cout << "  - Faster compilation for client code\n";
    
    std::cout << "\nDisadvantages:\n";
    std::cout << "  - Extra indirection (performance hit)\n";
    std::cout << "  - Heap allocation (usually)\n";
    std::cout << "  - More complex code\n";
    std::cout << "  - Can't use inline functions\n";
    std::cout << "  - Debugging is harder (extra layer)\n";
}

// ============================================================================
// MAIN FUNCTION
// ============================================================================

int main() {
    std::cout << "=== ADVANCED C++ OOP PATTERNS DEMONSTRATION ===\n";
    
    demonstrate_multiple_inheritance();
    demonstrate_friends();
    demonstrate_nested_classes();
    demonstrate_crtp();
    demonstrate_type_erasure();
    demonstrate_pimpl();
    
    std::cout << "\n=== ALL DEMONSTRATIONS COMPLETED ===\n";
    return 0;
}