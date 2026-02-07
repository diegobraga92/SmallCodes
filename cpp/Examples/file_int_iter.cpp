/*
Task Description:

A file contains a sequence of integers, stored one per line.
Implement a class that facilitates iteration over these integers.

A valid integer:
- Is a sequence of one or more digits (no leading zeros unless the value is zero)
- May be optionally preceded by a '+' or '-' sign
- Must represent a number in the range [-1,000,000,000, 1,000,000,000]
- May have spaces before and/or after the integer
- Lines are separated by a line-feed character (ASCII 10)

Lines that do not represent valid integers must be discarded.

Examples of invalid lines:
- 2u1, 23.9, #12, 00, ++1, 2000000000

Interface to implement:

    #include <iosfwd>

    class Solution {
    public:
        Solution(std::istream& s);
        class iterator;

        iterator begin();
        iterator end();
    };

The iterator must be an input iterator (C++03/C++11 style) and
iterate over all valid integers in the input stream.

The iterator is guaranteed to be used only once per file.
*/

#include <iosfwd>
#include <istream>
#include <string>
#include <cctype>
#include <limits>

class Solution {
    std::istream& stream_;

    static bool parseLine(const std::string& line, int& value) {
        size_t i = 0;
        size_t n = line.size();

        // Skip leading spaces
        while (i < n && std::isspace(static_cast<unsigned char>(line[i]))) {
            ++i;
        }

        if (i == n) return false;

        int sign = 1;
        if (line[i] == '+' || line[i] == '-') {
            sign = (line[i] == '-') ? -1 : 1;
            ++i;
        }

        if (i == n || !std::isdigit(static_cast<unsigned char>(line[i]))) {
            return false;
        }

        // Leading zero rules
        if (line[i] == '0' && i + 1 < n && std::isdigit(static_cast<unsigned char>(line[i + 1]))) {
            return false;
        }

        long long num = 0;
        while (i < n && std::isdigit(static_cast<unsigned char>(line[i]))) {
            num = num * 10 + (line[i] - '0');
            if (num > 1000000000LL) return false;
            ++i;
        }

        // Skip trailing spaces
        while (i < n && std::isspace(static_cast<unsigned char>(line[i]))) {
            ++i;
        }

        if (i != n) return false;

        num *= sign;
        if (num < -1000000000LL || num > 1000000000LL) return false;

        value = static_cast<int>(num);
        return true;
    }

public:
    explicit Solution(std::istream& s) : stream_(s) {}

    class iterator {
        std::istream* stream_;
        int current_;
        bool atEnd_;

        void readNext() {
            if (!stream_) {
                atEnd_ = true;
                return;
            }

            std::string line;
            while (std::getline(*stream_, line)) {
                int val;
                if (Solution::parseLine(line, val)) {
                    current_ = val;
                    return;
                }
            }

            atEnd_ = true;
            stream_ = nullptr;
        }

    public:
        iterator() : stream_(nullptr), current_(0), atEnd_(true) {}

        explicit iterator(std::istream& s)
            : stream_(&s), current_(0), atEnd_(false) {
            readNext();
        }

        int operator*() const {
            return current_;
        }

        iterator& operator++() {
            readNext();
            return *this;
        }

        bool operator!=(const iterator& other) const {
            return atEnd_ != other.atEnd_;
        }
    };

    iterator begin() {
        return iterator(stream_);
    }

    iterator end() {
        return iterator();
    }
};
