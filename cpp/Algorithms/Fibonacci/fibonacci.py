# Uses python3

fib_array = []

def calc_fib(n):
    fib_array.append(0)
    fib_array.append(1)

    for i in range(2, n+1):
        fib_array.append(fib_array[i - 1] + fib_array[i - 2])

    return fib_array[n]

n = int(input())
print(calc_fib(n))
