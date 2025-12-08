# Uses python3

# Gets the last digit of the sum between two fibonacci numbers.
# Since both have the same period size (60 for mod 10), adds in this range

def calc_fib_mod(n, to, m):
    period = [0,1, 1 % m]
    i = 2

    while not (period[i] == 1 and period[i-1] == 0):
        i = i+1
        period.append((period[i - 1] + period[i - 2]) % m)

    # Subtracts 1 from i to invert its initial value of 2
    modIndexFrom = n % (i - 1)
    modIndexTo = to % (i - 1)

    # Used a while instead of a straight for because when modIndexTo < modIndexFrom it is expected to do the sum by increasing to 60 (i - 1) and resetting
    sum = 0
    i = modIndexFrom
    if modIndexTo == 59:
        modIndexTo = -1

    while i != modIndexTo + 1:
        sum = (sum + period[i]) % m
        i = i + 1
        if (i >= 60):
            i = 0
        

    return sum

if __name__ == '__main__':
    from_, to = map(int, input().split())
    print(calc_fib_mod(from_, to, 10))