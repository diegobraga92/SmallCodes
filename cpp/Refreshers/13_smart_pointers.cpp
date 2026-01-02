////////* Ownership Models *////////

#include <memory>
#include <vector>
#include <iostream>

class Owner {
private:
    std::unique_ptr<int> data;  // Exclusive ownership
    
public:
    Owner() : data(std::make_unique<int>(42)) {}
    
    // Transfer ownership
    std::unique_ptr<int> release() {
        return std::move(data);
    }
    
    // Share ownership
    std::shared_ptr<int> share() {
        // Convert unique_ptr to shared_ptr
        return std::shared_ptr<int>(std::move(data));
    }
};

// RAW POINTERS - No ownership
void process(const int* ptr) {
    if (ptr) std::cout << "Processing: " << *ptr << "\n";
}

// UNIQUE OWNERSHIP - One owner
void unique_ownership() {
    std::unique_ptr<int> owner = std::make_unique<int>(100);
    process(owner.get());  // Pass raw pointer, no ownership transfer
}

// SHARED OWNERSHIP - Multiple owners
void shared_ownership() {
    std::shared_ptr<int> shared = std::make_shared<int>(200);
    std::shared_ptr<int> shared2 = shared;  // Both own the resource
}

// OBSERVER - No ownership
void observer_pattern() {
    std::shared_ptr<int> resource = std::make_shared<int>(300);
    std::weak_ptr<int> observer = resource;
    
    if (auto res = observer.lock()) {
        // Can use resource if it still exists
    }
}

////////* Custom Deleters *////////

#include <memory>
#include <iostream>
#include <cstdio>

void custom_deleters() {
    // Lambda as deleter
    auto arrayDeleter = [](int* ptr) {
        std::cout << "Deleting array\n";
        delete[] ptr;
    };
    
    std::unique_ptr<int[], decltype(arrayDeleter)> 
        array(new int[10], arrayDeleter);
    
    // Function as deleter
    struct FileCloser {
        void operator()(FILE* f) const {
            if (f) {
                std::cout << "Closing file\n";
                fclose(f);
            }
        }
    };
    
    std::unique_ptr<FILE, FileCloser> 
        file(fopen("example.txt", "w"));
    
    // Shared_ptr with custom deleter (type erased)
    auto sharedWithDeleter = std::shared_ptr<int>(
        new int[100],
        [](int* p) {
            std::cout << "Custom deleter for shared_ptr\n";
            delete[] p;
        }
    );
    
    // Deleter with state
    class LoggingDeleter {
        std::string id;
    public:
        LoggingDeleter(const std::string& name) : id(name) {}
        
        template<typename T>
        void operator()(T* ptr) const {
            std::cout << "Deleter " << id << " called\n";
            delete ptr;
        }
    };
    
    std::unique_ptr<double, LoggingDeleter> 
        logged(new double(3.14), LoggingDeleter("MyDeleter"));
}

////////* Cyclic References *////////

#include <memory>
#include <iostream>

class Node {
public:
    std::shared_ptr<Node> partner;
    std::string name;
    
    Node(const std::string& n) : name(n) {
        std::cout << name << " created\n";
    }
    
    ~Node() {
        std::cout << name << " destroyed\n";
    }
};

void cyclic_reference() {
    // CYCLIC REFERENCE PROBLEM
    {
        auto alice = std::make_shared<Node>("Alice");
        auto bob = std::make_shared<Node>("Bob");
        
        alice->partner = bob;    // Bob ref count: 2
        bob->partner = alice;    // Alice ref count: 2
        
        // Both have ref count 2
        // When leaving scope:
        // - alice ref count goes to 1 (still referenced by bob)
        // - bob ref count goes to 1 (still referenced by alice)
        // MEMORY LEAK! Neither destroyed
    }
    std::cout << "Scope ended - memory leaked!\n\n";
    
    // SOLUTION: Use weak_ptr to break cycles
    class SafeNode {
    public:
        std::weak_ptr<SafeNode> partner;  // Weak reference!
        std::string name;
        
        SafeNode(const std::string& n) : name(n) {
            std::cout << "Safe " << name << " created\n";
        }
        
        ~SafeNode() {
            std::cout << "Safe " << name << " destroyed\n";
        }
    };
    
    {
        auto safeAlice = std::make_shared<SafeNode>("Alice");
        auto safeBob = std::make_shared<SafeNode>("Bob");
        
        safeAlice->partner = safeBob;  // Doesn't increase ref count
        safeBob->partner = safeAlice;   // Doesn't increase ref count
        
        // Both have ref count 1
        // When leaving scope, both destroyed properly
    }
    std::cout << "Scope ended - no memory leak!\n";
}


#include <iostream>
#include <memory>
#include <vector>
#include <functional>
#include <cstdio>
#include <string>
#include <thread>
#include <chrono>
#include <mutex>

// ============================================================================
// 1. BASIC SMART POINTER TYPES & OWNERSHIP MODELS
// ============================================================================

class Resource {
private:
    std::string name;
    int id;
    static int nextId;
    
public:
    Resource(const std::string& n) : name(n), id(++nextId) {
        std::cout << "[" << id << "] Resource '" << name << "' constructed\n";
    }
    
    ~Resource() {
        std::cout << "[" << id << "] Resource '" << name << "' destroyed\n";
    }
    
    void use() const {
        std::cout << "[" << id << "] Using resource '" << name << "'\n";
    }
    
    void rename(const std::string& newName) {
        std::cout << "[" << id << "] Renaming '" << name << "' to '" << newName << "'\n";
        name = newName;
    }
    
    std::string getName() const { return name; }
    int getId() const { return id; }
};

int Resource::nextId = 0;

// ============================================================================
// 2. UNIQUE_PTR - EXCLUSIVE OWNERSHIP
// ============================================================================

void demonstrate_unique_ptr() {
    std::cout << "\n=== UNIQUE_PTR DEMONSTRATION ===\n";
    
    // 2.1 Creating unique_ptr instances
    std::unique_ptr<Resource> resource1 = std::make_unique<Resource>("UniqueResource1");
    std::unique_ptr<Resource> resource2(new Resource("UniqueResource2"));
    
    // 2.2 Accessing the managed object
    resource1->use();
    (*resource2).use();
    
    // 2.3 Checking if pointer owns an object
    if (resource1) {
        std::cout << "resource1 owns an object\n";
    }
    
    // 2.4 Releasing ownership
    Resource* rawPtr = resource1.release(); // resource1 becomes empty
    std::cout << "Released raw pointer: " << rawPtr->getName() << "\n";
    
    // Must manually delete raw pointer since unique_ptr no longer owns it
    delete rawPtr;
    
    // 2.5 Resetting with new object
    resource1.reset(new Resource("UniqueResource3"));
    
    // 2.6 Transferring ownership (unique_ptr cannot be copied, only moved)
    std::unique_ptr<Resource> resource3 = std::move(resource1); // resource1 becomes empty
    std::cout << "After move, resource1 is " << (resource1 ? "not empty" : "empty") << "\n";
    
    // 2.7 Returning unique_ptr from function (transfer ownership)
    auto createResource = [](const std::string& name) -> std::unique_ptr<Resource> {
        return std::make_unique<Resource>(name);
    };
    
    auto resource4 = createResource("CreatedInFunction");
    
    // 2.8 unique_ptr with arrays
    std::unique_ptr<Resource[]> resourceArray(new Resource[3]{
        Resource("Array1"), Resource("Array2"), Resource("Array3")
    });
    
    for (int i = 0; i < 3; ++i) {
        resourceArray[i].use();
    }
    // Automatically calls delete[] when out of scope
}

// ============================================================================
// 3. SHARED_PTR - SHARED OWNERSHIP WITH REFERENCE COUNTING
// ============================================================================

class Node {
public:
    std::string name;
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> previous; // Use weak_ptr to avoid cycles
    
    Node(const std::string& n) : name(n) {
        std::cout << "Node '" << name << "' created\n";
    }
    
    ~Node() {
        std::cout << "Node '" << name << "' destroyed\n";
    }
    
    void linkTo(std::shared_ptr<Node> node) {
        next = node;
        if (node) {
            node->previous = shared_from_this(); // Need enable_shared_from_this
        }
    }
};

// Class that can safely create shared_ptr to itself
class SharedNode : public std::enable_shared_from_this<SharedNode> {
public:
    std::string name;
    std::shared_ptr<SharedNode> next;
    std::weak_ptr<SharedNode> previous;
    
    SharedNode(const std::string& n) : name(n) {
        std::cout << "SharedNode '" << name << "' created\n";
    }
    
    ~SharedNode() {
        std::cout << "SharedNode '" << name << "' destroyed\n";
    }
    
    void linkTo(std::shared_ptr<SharedNode> node) {
        next = node;
        if (node) {
            node->previous = shared_from_this(); // Safe!
        }
    }
};

void demonstrate_shared_ptr() {
    std::cout << "\n=== SHARED_PTR DEMONSTRATION ===\n";
    
    // 3.1 Creating shared_ptr instances
    std::shared_ptr<Resource> shared1 = std::make_shared<Resource>("SharedResource1");
    
    // 3.2 Reference counting
    {
        std::cout << "shared1 use_count: " << shared1.use_count() << "\n";
        
        std::shared_ptr<Resource> shared2 = shared1; // Copy increases ref count
        std::cout << "After copy, use_count: " << shared1.use_count() << "\n";
        
        std::shared_ptr<Resource> shared3 = shared1;
        std::cout << "After another copy, use_count: " << shared1.use_count() << "\n";
        
        // All share the same object
        shared1->rename("RenamedByShared1");
        shared2->use(); // Shows renamed resource
        
        // shared2 and shared3 go out of scope, ref count decreases
    }
    std::cout << "After inner scope, use_count: " << shared1.use_count() << "\n";
    
    // 3.3 make_shared efficiency (single allocation for object and control block)
    auto shared4 = std::make_shared<Resource>("MakeSharedEfficient");
    
    // 3.4 Custom deleters with shared_ptr (type-erased, more flexible than unique_ptr)
    auto customDeleter = [](Resource* r) {
        std::cout << "Custom deleter called for " << r->getName() << "\n";
        delete r;
    };
    
    std::shared_ptr<Resource> shared5(new Resource("WithCustomDeleter"), customDeleter);
    
    // 3.5 Aliasing constructor - share ownership but point to different object
    struct Data {
        int value;
        std::string info;
    };
    
    auto sharedData = std::make_shared<Data>(Data{42, "Main Data"});
    std::shared_ptr<std::string> aliased(&sharedData->info, sharedData);
    // aliased shares ownership with sharedData but points to info member
    
    std::cout << "sharedData use_count: " << sharedData.use_count() << "\n";
    std::cout << "aliased use_count: " << aliased.use_count() << "\n";
    
    // 3.6 enable_shared_from_this
    auto node1 = std::make_shared<SharedNode>("Node1");
    auto node2 = std::make_shared<SharedNode>("Node2");
    
    node1->linkTo(node2);
    node2->linkTo(node1);
    
    std::cout << "Node1 use_count: " << node1.use_count() << "\n";
    std::cout << "Node2 use_count: " << node2.use_count() << "\n";
    
    // No memory leak despite circular references due to weak_ptr usage
}

// ============================================================================
// 4. WEAK_PTR - NON-OWNING OBSERVERS
// ============================================================================

void demonstrate_weak_ptr() {
    std::cout << "\n=== WEAK_PTR DEMONSTRATION ===\n";
    
    // 4.1 Creating weak_ptr from shared_ptr
    std::shared_ptr<Resource> shared = std::make_shared<Resource>("ObservedResource");
    std::weak_ptr<Resource> weak = shared;
    
    std::cout << "shared use_count: " << shared.use_count() << "\n";
    std::cout << "weak use_count: " << weak.use_count() << "\n";
    
    // 4.2 Locking weak_ptr to get shared_ptr
    if (auto locked = weak.lock()) {
        std::cout << "Successfully locked weak_ptr, object: " << locked->getName() << "\n";
        std::cout << "Now shared use_count: " << shared.use_count() << "\n";
    }
    
    // 4.3 Checking if weak_ptr is expired
    {
        auto tempShared = std::make_shared<Resource>("Temporary");
        std::weak_ptr<Resource> tempWeak = tempShared;
        
        std::cout << "Before destruction, expired: " << (tempWeak.expired() ? "yes" : "no") << "\n";
    } // tempShared destroyed here
    
    std::cout << "After destruction, expired: " << (weak.expired() ? "yes" : "no") << "\n";
    
    // 4.4 Cache pattern with weak_ptr
    class ResourceCache {
    private:
        std::unordered_map<int, std::weak_ptr<Resource>> cache;
        std::mutex cacheMutex;
        
    public:
        std::shared_ptr<Resource> getResource(int id, const std::string& name) {
            std::lock_guard<std::mutex> lock(cacheMutex);
            
            auto it = cache.find(id);
            if (it != cache.end()) {
                if (auto cached = it->second.lock()) {
                    std::cout << "Cache hit for id " << id << "\n";
                    return cached;
                }
                // Entry expired, remove it
                cache.erase(it);
            }
            
            // Cache miss, create new resource
            std::cout << "Cache miss for id " << id << ", creating new\n";
            auto resource = std::make_shared<Resource>(name);
            cache[id] = resource;
            return resource;
        }
        
        size_t cleanupExpired() {
            std::lock_guard<std::mutex> lock(cacheMutex);
            size_t count = 0;
            for (auto it = cache.begin(); it != cache.end(); ) {
                if (it->second.expired()) {
                    it = cache.erase(it);
                    ++count;
                } else {
                    ++it;
                }
            }
            return count;
        }
    };
    
    ResourceCache cache;
    auto cached1 = cache.getResource(1, "Cached1");
    auto cached2 = cache.getResource(1, "Cached1Again"); // Should be cache hit
    
    // 4.5 Observer pattern with weak_ptr
    class Subject; // Forward declaration
    
    class Observer {
    public:
        virtual ~Observer() = default;
        virtual void update(const Subject&) = 0;
    };
    
    class Subject {
    private:
        std::vector<std::weak_ptr<Observer>> observers;
        
    public:
        void attach(std::weak_ptr<Observer> obs) {
            observers.push_back(obs);
        }
        
        void notify() {
            for (auto it = observers.begin(); it != observers.end(); ) {
                if (auto obs = it->lock()) {
                    obs->update(*this);
                    ++it;
                } else {
                    // Observer destroyed, remove from list
                    it = observers.erase(it);
                }
            }
        }
    };
}

// ============================================================================
// 5. CUSTOM DELETERS & RESOURCE MANAGEMENT
// ============================================================================

void demonstrate_custom_deleters() {
    std::cout << "\n=== CUSTOM DELETERS DEMONSTRATION ===\n";
    
    // 5.1 File handling with custom deleters
    auto fileDeleter = [](FILE* f) {
        if (f) {
            std::cout << "Closing file\n";
            fclose(f);
        }
    };
    
    std::unique_ptr<FILE, decltype(fileDeleter)> 
        filePtr(fopen("test.txt", "w"), fileDeleter);
    
    if (filePtr) {
        fprintf(filePtr.get(), "Hello from smart pointer!\n");
        // File automatically closed when filePtr goes out of scope
    }
    
    // 5.2 Array deleter for unique_ptr
    auto arrayDeleter = [](int* arr) {
        std::cout << "Deleting array of integers\n";
        delete[] arr;
    };
    
    std::unique_ptr<int[], decltype(arrayDeleter)> 
        intArray(new int[10]{1,2,3,4,5,6,7,8,9,10}, arrayDeleter);
    
    // 5.3 Shared_ptr with stateful deleter
    class LoggingDeleter {
        std::string loggerName;
    public:
        LoggingDeleter(const std::string& name) : loggerName(name) {}
        
        void operator()(Resource* r) const {
            std::cout << "[" << loggerName << "] Deleting resource "
                      << r->getId() << ": " << r->getName() << "\n";
            delete r;
        }
    };
    
    std::shared_ptr<Resource> loggedResource(
        new Resource("LoggedResource"),
        LoggingDeleter("ResourceLogger")
    );
    
    // 5.4 Memory pool deleter
    class MemoryPool {
    private:
        std::vector<void*> allocated;
        
    public:
        void* allocate(size_t size) {
            void* ptr = malloc(size);
            allocated.push_back(ptr);
            std::cout << "Allocated " << size << " bytes at " << ptr << "\n";
            return ptr;
        }
        
        void deallocate(void* ptr) {
            auto it = std::find(allocated.begin(), allocated.end(), ptr);
            if (it != allocated.end()) {
                std::cout << "Deallocating " << ptr << "\n";
                free(ptr);
                allocated.erase(it);
            }
        }
        
        ~MemoryPool() {
            for (void* ptr : allocated) {
                free(ptr);
            }
        }
    };
    
    MemoryPool pool;
    auto poolDeleter = [&pool](Resource* r) {
        std::cout << "Returning resource to pool: " << r->getName() << "\n";
        pool.deallocate(r);
    };
    
    std::unique_ptr<Resource, decltype(poolDeleter)> 
        pooledResource(static_cast<Resource*>(pool.allocate(sizeof(Resource))), 
                      poolDeleter);
    
    // Use placement new to construct object in pooled memory
    new(pooledResource.get()) Resource("PooledResource");
    
    // Manually call destructor before deleter runs
    pooledResource->~Resource();
}

// ============================================================================
// 6. ADVANCED PATTERNS & USE CASES
// ============================================================================

void demonstrate_advanced_patterns() {
    std::cout << "\n=== ADVANCED PATTERNS ===\n";
    
    // 6.1 Pimpl Idiom with unique_ptr
    class PimplExample {
    private:
        class Impl;
        std::unique_ptr<Impl> pImpl;
        
    public:
        PimplExample();
        ~PimplExample(); // Required in .cpp file where Impl is defined
        PimplExample(PimplExample&&) = default;
        PimplExample& operator=(PimplExample&&) = default;
        
        // Must disable copying since unique_ptr is not copyable
        PimplExample(const PimplExample&) = delete;
        PimplExample& operator=(const PimplExample&) = delete;
        
        void doSomething();
    };
    
    // 6.2 Factory pattern returning unique_ptr
    class Product {
    public:
        virtual ~Product() = default;
        virtual void use() = 0;
    };
    
    class ConcreteProduct : public Product {
    public:
        void use() override {
            std::cout << "Using ConcreteProduct\n";
        }
    };
    
    class ProductFactory {
    public:
        static std::unique_ptr<Product> createProduct() {
            return std::make_unique<ConcreteProduct>();
        }
    };
    
    auto product = ProductFactory::createProduct();
    product->use();
    
    // 6.3 Strategy pattern with shared_ptr
    class Strategy {
    public:
        virtual ~Strategy() = default;
        virtual void execute() = 0;
    };
    
    class FastStrategy : public Strategy {
    public:
        void execute() override {
            std::cout << "Executing fast strategy\n";
        }
    };
    
    class SafeStrategy : public Strategy {
    public:
        void execute() override {
            std::cout << "Executing safe strategy\n";
        }
    };
    
    class Context {
        std::shared_ptr<Strategy> strategy;
    public:
        void setStrategy(std::shared_ptr<Strategy> s) {
            strategy = s;
        }
        
        void executeStrategy() {
            if (strategy) {
                strategy->execute();
            }
        }
    };
    
    Context context;
    context.setStrategy(std::make_shared<FastStrategy>());
    context.executeStrategy();
    
    // 6.4 Thread-safe resource sharing
    class ThreadSafeResource {
    private:
        std::shared_ptr<Resource> resource;
        mutable std::mutex mutex;
        
    public:
        ThreadSafeResource(const std::string& name) 
            : resource(std::make_shared<Resource>(name)) {}
        
        std::shared_ptr<Resource> getResource() {
            std::lock_guard<std::mutex> lock(mutex);
            return resource;
        }
        
        void updateResource(const std::string& newName) {
            std::lock_guard<std::mutex> lock(mutex);
            if (resource) {
                resource->rename(newName);
            }
        }
    };
    
    // 6.5 Polymorphic containers with shared_ptr
    std::vector<std::shared_ptr<Product>> products;
    products.push_back(std::make_shared<ConcreteProduct>());
    
    for (const auto& product : products) {
        product->use();
    }
}

// ============================================================================
// 7. MEMORY LEAK DETECTION & DEBUGGING
// ============================================================================

// Custom allocator that tracks allocations
class DebugAllocator {
    static std::map<void*, std::pair<size_t, std::string>> allocations;
    static std::mutex allocMutex;
    
public:
    static void* allocate(size_t size, const std::string& info = "") {
        void* ptr = malloc(size);
        
        std::lock_guard<std::mutex> lock(allocMutex);
        allocations[ptr] = {size, info};
        std::cout << "[ALLOC] " << ptr << " size: " << size 
                  << " info: " << info << "\n";
        
        return ptr;
    }
    
    static void deallocate(void* ptr) {
        std::lock_guard<std::mutex> lock(allocMutex);
        auto it = allocations.find(ptr);
        if (it != allocations.end()) {
            std::cout << "[FREE] " << ptr << " size: " << it->second.first
                      << " info: " << it->second.second << "\n";
            allocations.erase(it);
        }
        free(ptr);
    }
    
    static void reportLeaks() {
        std::lock_guard<std::mutex> lock(allocMutex);
        if (!allocations.empty()) {
            std::cout << "\n=== MEMORY LEAK DETECTED ===\n";
            for (const auto& [ptr, info] : allocations) {
                std::cout << "Leaked: " << ptr << " size: " << info.first
                          << " info: " << info.second << "\n";
            }
        }
    }
};

std::map<void*, std::pair<size_t, std::string>> DebugAllocator::allocations;
std::mutex DebugAllocator::allocMutex;

void demonstrate_debugging() {
    std::cout << "\n=== DEBUGGING & LEAK DETECTION ===\n";
    
    // Custom debug deleter that uses DebugAllocator
    auto debugDeleter = [](Resource* r) {
        std::cout << "Debug deleting: " << r->getName() << "\n";
        DebugAllocator::deallocate(r);
    };
    
    // This will be detected as leak
    Resource* leaked = static_cast<Resource*>(
        DebugAllocator::allocate(sizeof(Resource), "Potential leak")
    );
    new(leaked) Resource("WillBeLeaked");
    
    // This will be properly cleaned up
    std::unique_ptr<Resource, decltype(debugDeleter)> 
        debugResource(static_cast<Resource*>(
            DebugAllocator::allocate(sizeof(Resource), "DebugResource")
        ), debugDeleter);
    new(debugResource.get()) Resource("DebugResource");
    
    // Manually call destructor for unique_ptr with custom deleter
    debugResource->~Resource();
    
    // Don't clean up leaked resource to demonstrate leak detection
    // In real code, you'd want to properly delete it
    // leaked->~Resource();
    // DebugAllocator::deallocate(leaked);
}

// ============================================================================
// MAIN FUNCTION DEMONSTRATING ALL CONCEPTS
// ============================================================================

int main() {
    std::cout << "=== COMPREHENSIVE SMART POINTERS DEMONSTRATION ===\n";
    
    // Demonstrate all concepts
    demonstrate_unique_ptr();
    demonstrate_shared_ptr();
    demonstrate_weak_ptr();
    demonstrate_custom_deleters();
    demonstrate_advanced_patterns();
    demonstrate_debugging();
    
    // Check for memory leaks at program end
    DebugAllocator::reportLeaks();
    
    std::cout << "\n=== PROGRAM COMPLETED SUCCESSFULLY ===\n";
    return 0;
}

// Implementation of PimplExample (must be in same translation unit or linked)
class PimplExample::Impl {
public:
    int data;
    std::string info;
    
    Impl() : data(42), info("Pimpl Implementation") {
        std::cout << "Pimpl::Impl constructed\n";
    }
    
    ~Impl() {
        std::cout << "Pimpl::Impl destroyed\n";
    }
};

PimplExample::PimplExample() : pImpl(std::make_unique<Impl>()) {}
PimplExample::~PimplExample() = default; // Required for unique_ptr with incomplete type

void PimplExample::doSomething() {
    std::cout << "Pimpl data: " << pImpl->data << ", info: " << pImpl->info << "\n";
}