#include <iostream>

class Singleton {
public:
    static Singleton& getInstance() {
        static Singleton instance;
        return instance;
    }
    
    // Delete copy constructor and assignment operator
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
    
    void doSomething() {
        std::cout << "Singleton doing something\n";
    }
    
private:
    Singleton() = default;
    ~Singleton() = default;
};