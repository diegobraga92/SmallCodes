def f(a, b=2, *args, **kwargs):
    return a + b + sum(args) + sum(kwargs.values())

def outer():
    x = 0
    def inner():
        nonlocal x
        x += 1
        return x
    return inner


def greet(name="World"):  # Default parameter
    """Docstring: Returns greeting"""  # Documentation
    return f"Hello, {name}"

# *args and **kwargs
def flexible_func(*args, **kwargs):
    """Accepts any number of positional/keyword args"""
    print(f"Positional: {args}")
    print(f"Keyword: {kwargs}")


# Anonymous functions
add = lambda x, y: x + y
print(add(2, 3))  # 5

# Common use with sorted()
people = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
sorted_people = sorted(people, key=lambda x: x["age"])