#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>
#include <functional>
#include <mutex>
#include <condition_variable>

class Watchdog {
public:
    // Constructor: sets timeout in milliseconds and optional callback
    Watchdog(uint64_t timeout_ms, std::function<void()> callback = nullptr)
        : timeout_ms_(timeout_ms)
        , callback_(callback)
        , running_(false)
        , triggered_(false)
    {}
    
    ~Watchdog() {
        stop();
    }
    
    // Start the watchdog
    void start() {
        if (running_) return;
        
        running_ = true;
        triggered_ = false;
        watchdog_thread_ = std::thread(&Watchdog::watchdog_loop, this);
    }
    
    // Stop the watchdog
    void stop() {
        running_ = false;
        cv_.notify_all();
        
        if (watchdog_thread_.joinable()) {
            watchdog_thread_.join();
        }
    }
    
    // Pet the watchdog (reset the timer)
    void pet() {
        std::lock_guard<std::mutex> lock(mutex_);
        last_pet_time_ = std::chrono::steady_clock::now();
        triggered_ = false;
        cv_.notify_all();
    }
    
    // Check if watchdog has triggered
    bool has_triggered() const {
        return triggered_.load();
    }
    
    // Set new timeout value
    void set_timeout(uint64_t timeout_ms) {
        std::lock_guard<std::mutex> lock(mutex_);
        timeout_ms_ = timeout_ms;
    }
    
    // Get remaining time until timeout
    uint64_t get_remaining_time() const {
        std::lock_guard<std::mutex> lock(mutex_);
        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
            now - last_pet_time_);
        
        if (elapsed.count() >= timeout_ms_) {
            return 0;
        }
        
        return timeout_ms_ - elapsed.count();
    }

private:
    void watchdog_loop() {
        std::unique_lock<std::mutex> lock(mutex_);
        
        // Initialize the last pet time
        last_pet_time_ = std::chrono::steady_clock::now();
        
        while (running_) {
            // Wait for timeout or pet signal
            if (cv_.wait_for(lock, std::chrono::milliseconds(timeout_ms_)) == std::cv_status::timeout) {
                // Timeout occurred - check if we should trigger
                auto now = std::chrono::steady_clock::now();
                auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(
                    now - last_pet_time_);
                
                if (elapsed.count() >= timeout_ms_ && running_) {
                    triggered_ = true;
                    
                    // Execute callback if provided
                    if (callback_) {
                        // Execute callback without holding the lock
                        lock.unlock();
                        callback_();
                        lock.lock();
                    }
                    
                    // Wait for next pet or stop
                    cv_.wait(lock, [this]() { 
                        return !running_ || !triggered_; 
                    });
                }
            }
        }
    }
    
    uint64_t timeout_ms_;
    std::function<void()> callback_;
    std::atomic<bool> running_;
    std::atomic<bool> triggered_;
    std::thread watchdog_thread_;
    
    mutable std::mutex mutex_;
    std::condition_variable cv_;
    std::chrono::steady_clock::time_point last_pet_time_;
};