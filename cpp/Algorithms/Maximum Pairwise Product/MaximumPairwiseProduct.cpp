/*
    Given an array, finds which 2 elements multiplied will give the largest number.

    The easiest way to do this is by iterating the array twice and getting the two largest values, this way it will take 2n to run it.

    Long long is used instead of int due to requirements.
*/

#include <iostream>
#include <vector>
#include <algorithm>

long long MaxPairwiseProduct(const std::vector<long long>& numbers) {
    long long n = numbers.size();

    long long firstIndex = 0;
    long long secondValue = -1;

    for(long long i = 0; i < n; i++){
        if(numbers[i] > numbers[firstIndex]){
            firstIndex = i;
        }
    }

    for(long long i = 0; i < n; i++){
        if(i != firstIndex && numbers[i] > secondValue){
            secondValue = numbers[i];
        }
    }

    return numbers[firstIndex] * secondValue;
}

int main() {
    long long n;
    std::cin >> n;
    std::vector<long long> numbers(n);
    for (long long i = 0; i < n; ++i) {
        std::cin >> numbers[i];
    }

    std::cout << MaxPairwiseProduct(numbers) << "\n";
    return 0;
}
