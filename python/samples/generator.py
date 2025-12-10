def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

g = fib()

[next(g) for _ in range(6)]