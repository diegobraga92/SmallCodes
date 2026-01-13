class Singleton {
public:
    // Access point to the single instance
    static Singleton& instance() {
        // Since C++11:
        //  - Initialization of function-local static variables is thread-safe
        //  - Exactly one thread performs the initialization
        //  - Other threads block until initialization completes
        static Singleton instance;
        return instance;
    }

    // Delete copy/move to enforce single instance
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
    Singleton(Singleton&&) = delete;
    Singleton& operator=(Singleton&&) = delete;

private:
    Singleton() {
        // Constructor is private to prevent direct construction
    }

    ~Singleton() {
        // Destructor is private to prevent deletion by users
        // It WILL be called automatically at program shutdown
    }
};

// Initialization of a function-local static variable is performed exactly once, even in the presence of multiple threads.
// If another static object accesses Singleton::instance() in its destructor → undefined behavior