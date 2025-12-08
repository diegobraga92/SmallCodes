#include <thread>
#include <mutex>
#include <condition_variable>
#include <atomic>

std::mutex m;
std::condition_variable cv;
std::atomic<int> access_count{0};

void incr(int& i) {
    for (auto j = 0; j <= 10000; j++) {
        {
            std::lock_guard<std::mutex> lock(m);
            ++i;
            cv.notify_one();
        }
    }
}

void consumer() {
    while (true) {
        std::unique_lock<std::mutex> lock(m);

        cv.wait(lock, [] {});
        break;
    }
}

void main() {
    int i = 0;
    std::thread t1(incr, i);
    std::thread t2(incr, i);

    t1.join();
    t2.join();
}