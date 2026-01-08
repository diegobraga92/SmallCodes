#include <thread>
#include <mutex>
#include <iostream>
#include <chrono>

std::mutex m1;
std::mutex m2;

void threadA() {
    std::lock_guard<std::mutex> lock1(m1);
    std::this_thread::sleep_for(std::chrono::milliseconds(100)); // force interleaving
    std::lock_guard<std::mutex> lock2(m2);

    std::cout << "Thread A finished\n";
}

void threadB() {
    std::lock_guard<std::mutex> lock1(m2);
    std::this_thread::sleep_for(std::chrono::milliseconds(100)); // force interleaving
    std::lock_guard<std::mutex> lock2(m1);

    std::cout << "Thread B finished\n";
}

int main() {
    std::thread t1(threadA);
    std::thread t2(threadB);

    t1.join();
    t2.join();
}

/* FIX 1:

void threadA() {
    std::lock_guard<std::mutex> lock1(m1);
    std::lock_guard<std::mutex> lock2(m2);

    std::cout << "Thread A finished\n";
}

void threadB() {
    std::lock_guard<std::mutex> lock1(m1); // SAME ORDER
    std::lock_guard<std::mutex> lock2(m2);

    std::cout << "Thread B finished\n";
}



FIX 2:

void threadA() {
    std::lock(m1, m2);
    std::lock_guard<std::mutex> lock1(m1, std::adopt_lock);
    std::lock_guard<std::mutex> lock2(m2, std::adopt_lock);

    std::cout << "Thread A finished\n";
}

void threadB() {
    std::lock(m1, m2);
    std::lock_guard<std::mutex> lock1(m1, std::adopt_lock);
    std::lock_guard<std::mutex> lock2(m2, std::adopt_lock);

    std::cout << "Thread B finished\n";
}

*/