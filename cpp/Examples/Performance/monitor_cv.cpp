#include <mutex>
#include <condition_variable>

class Monitor {
protected:
    std::mutex mtx_;

    // Helper type: condition variable bound to this monitor
    struct Condition {
        std::condition_variable cv;
    };

    // Wait releases the monitor lock and reacquires it on wakeup
    void wait(Condition& cond, std::unique_lock<std::mutex>& lock) {
        cond.cv.wait(lock);
    }

    // Signal wakes one waiting thread
    void signal(Condition& cond) {
        cond.cv.notify_one();
    }

    // Broadcast wakes all waiting threads
    void broadcast(Condition& cond) {
        cond.cv.notify_all();
    }
};
