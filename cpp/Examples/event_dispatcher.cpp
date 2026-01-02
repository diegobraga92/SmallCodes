#include <functional>
#include <vector>
#include <memory>

template<typename EventType>
class SimpleEventDispatcher {
private:
    using Handler = std::function<void(const EventType&)>;
    std::vector<Handler> handlers_;
    
public:
    // Subscribe to events
    void subscribe(Handler handler) {
        handlers_.push_back(std::move(handler));
    }
    
    // Dispatch event to all subscribers
    void dispatch(const EventType& event) {
        for (const auto& handler : handlers_) {
            handler(event);
        }
    }
    
    // Get number of subscribers
    size_t subscriber_count() const {
        return handlers_.size();
    }
    
    // Clear all subscribers
    void clear() {
        handlers_.clear();
    }
};