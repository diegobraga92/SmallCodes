class Animal:
    species = "Unknown"  # class attr
    def __init__(self, name): self.name = name
    
class Dog(Animal):
    def speak(self): return "woof"