#include <fstream>
#include <future>
#include <iostream>
#include <string_view>
#include <thread>

struct FileStats {
    size_t charCount = 0;
};

FileStats countChar(std::string_view path) {
    std::ifstream infile{std::string(path)};
    if (!infile) {return {0};}

    size_t count = 0;
    char c;
    while (infile.get(c)) ++count;

    return {count};
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        return 1;
    }

    std::string_view in_file = argv[1];
    std::string_view out_file = argv[2];

    std::future<FileStats> f = std::async(countChar, in_file);

    auto stats = f.get();

    std::thread t([stats, out_file]() {
        std::ofstream outfile{std::string(out_file)};
        if (!outfile) return;

        outfile << "File processed. Char count: " << stats.charCount;
    });

    t.join();

    return 0;
}