class SingletonMeta(type):
    """Metaclass for Singleton pattern"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    def __init__(self):
        print("Initializing database...")

db1 = Database()  # Prints "Initializing database..."
db2 = Database()  # No print, returns same instance
print(db1 is db2)  # True