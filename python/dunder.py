class Typed:
    def __init__(self, name):
        self.name = name
    def __get__(self, obj, objtype):
        return obj.__dict__[self.name]
    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError
        obj.__dict__[self.name] = value
class A:
    x = Typed('x')
a = A(); a.x = 5; print(a.x)



class ValidatedAttribute:
    """Descriptor for validated attributes"""
    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __set__(self, instance, value):
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"{self.name} must be >= {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"{self.name} must be <= {self.max_val}")
        instance.__dict__[self.name] = value
    
    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)


class Product:
    price = ValidatedAttribute(min_val=0, max_val=1000)
    
    def __init__(self, price):
        self.price = price

try:
    p = Product(1500)  # Raises ValueError
except ValueError as e:
    print(e)