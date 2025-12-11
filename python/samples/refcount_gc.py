import sys
import gc

# Reference counting
a = [1, 2, 3]
print(sys.getrefcount(a))  # Reference count

# Circular reference example
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

# Create circular reference
node1 = Node(1)
node2 = Node(2)
node1.next = node2
node2.next = node1  # Circular reference!

# Force garbage collection
collected = gc.collect()
print(f"Collected {collected} objects")