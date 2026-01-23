try:
    1/0
except ZeroDivisionError:
    print("div by zero")
finally:
    print("cleanup")