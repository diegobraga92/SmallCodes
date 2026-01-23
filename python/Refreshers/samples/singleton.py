# SINGLETON:
# Method 1: Using meta.py

# Method 2: Using decorator
def singleton(cls):
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
@singleton
class Config:
    def __init__(self):
        self.settings = {}

# Method 3: Using __new__
class SingletonClass:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance