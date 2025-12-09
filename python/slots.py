class RegularClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class OptimizedClass:
    __slots__ = ['x', 'y']  # Prevents dict creation
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# OptimizedClass uses less memory
import sys
regular = RegularClass(1, 2)
optimized = OptimizedClass(1, 2)
print(f"Regular size: {sys.getsizeof(regular)}")
print(f"Optimized size: {sys.getsizeof(optimized)}")