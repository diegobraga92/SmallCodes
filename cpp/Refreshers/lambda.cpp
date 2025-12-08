#include <algorithm>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> values = {3, 7, 8, 5, 2};

    auto it = std::find_if(values.begin(), values.end(),
                           [](int n) { return n % 2 == 0; });

    if (it != values.end())
        std::cout << "First even number: " << *it << '\n';
}
