# Uses python3
import sys

fib_array = []

def calc_fib_last_digit(n):
    fib_array.append(0)
    fib_array.append(1)

    for i in range(2, n+1):
        fib_array.append((fib_array[i - 1] + fib_array[i - 2]) % 10)

    return fib_array[n]

if __name__ == '__main__':
    n = int(input())
    print(calc_fib_last_digit(n))
