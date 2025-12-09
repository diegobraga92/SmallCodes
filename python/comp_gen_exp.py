evens = [x for x in range(10) if x % 2 == 0]
squares_gen = (x*x for x in range(5))

# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# Generator expression (lazy evaluation)
squares_gen = (x**2 for x in range(10))
next(squares_gen)  # 0

# Dictionary comprehension
square_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}