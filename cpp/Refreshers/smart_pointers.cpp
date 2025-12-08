#include <memory>

struct Foo{
    Foo() {}
    ~Foo() {}
};

int main() {
    auto f = std::make_unique<Foo>(); // Unique Pointers owns the object and implement RAII
    // Cannot be copied, only moved

    auto s1 = std::make_shared<Foo>(); // Shared allow multiple owners
    auto s2 = s1; // Increments
    // Destroys content when all shared pointers go out of scope.
    // Uses atomic counters to know how many owners

    s2.reset(); // Decrements

    std::weak_ptr<Foo> w2 = s1; // Create weak reference
    // Weak does not own, but observes Shared
    // Is used to prevent circular reference when using only Shared Pointers

    return 0;
}

// Circular reference example:
/*
void circular_reference_example() {
    auto node1 = std::make_shared<Foo>("Alice");
    auto node2 = std::make_shared<Node>("Bob");
    
    node1->partner = node2; // Alice points to Bob
    node2->partner = node1; // Bob points to Alice (circular reference!)
    
    // When this function ends, neither node1 nor node2 will be destroyed
    // because they reference each other, creating a memory leak
}
*/

// Fix using Weak Pointer:
/*
class Person {
public:
    std::string name;
    std::weak_ptr<Person> partner; // Use weak_ptr to avoid circular reference
...

    void introducePartner() {
        if (auto sharedPartner = partner.lock()) { // Convert to shared_ptr
            std::cout << name << "'s partner is " << sharedPartner->name << std::endl;
        } else {
            std::cout << name << " has no partner or partner was destroyed" << std::endl;
        }
    }
};
*/