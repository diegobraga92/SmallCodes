#include <iostream>
#include <vector>
#include <memory>
#include <algorithm>
#include <string>

// Forward declaration
class Subject;

// Observer interface
class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(const Subject& subject) = 0;
    virtual std::string getName() const = 0;
};

// Subject (Observable) base class
class Subject {
public:
    virtual ~Subject() = default;
    
    void attach(std::shared_ptr<Observer> observer) {
        observers_.push_back(observer);
        std::cout << observer->getName() << " attached to subject\n";
    }
    
    void detach(std::shared_ptr<Observer> observer) {
        auto it = std::find_if(observers_.begin(), observers_.end(),
            [&observer](const std::shared_ptr<Observer>& obs) {
                return obs->getName() == observer->getName();
            });
        
        if (it != observers_.end()) {
            std::cout << observer->getName() << " detached from subject\n";
            observers_.erase(it);
        }
    }
    
    void notify() {
        for (const auto& observer : observers_) {
            observer->update(*this);
        }
    }
    
    virtual std::string getState() const = 0;
    virtual void setState(const std::string& state) = 0;

protected:
    std::vector<std::shared_ptr<Observer>> observers_;
};