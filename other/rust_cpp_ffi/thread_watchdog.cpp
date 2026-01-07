#include <atomic>
#include <chrono>
#include <iostream>
#include <thread>

using namespace std::chrono;

std::atomic<bool> running{true};
std::atomic<steady_clock::time_point> heartbeat{steady_clock::now()};

void worker()
{
    while (running) {
        std::this_thread::sleep_for(200ms);
        heartbeat.store(steady_clock::now(), std::memory_order_relaxed);
    }
}

void watchdog(milliseconds timeout)
{
    while (running) {
        std::this_thread::sleep_for(timeout / 2);

        if (steady_clock::now() - heartbeat.load(std::memory_order_relaxed) > timeout) {
            std::cerr << "Watchdog: worker thread is unresponsive!\n";
            running = false;
        }
    }
}

int main()
{
    std::thread w(worker), wd(watchdog, 1s);

    std::this_thread::sleep_for(3s);
    std::cout << "Main: stopping heartbeat\n";
    std::this_thread::sleep_for(3s);

    running = false;
    w.join();
    wd.join();
}
