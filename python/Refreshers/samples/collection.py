from collections import Counter
Counter("banana")


from collections.abc import MutableSequence

class CustomList(MutableSequence):
    """Custom list implementation"""
    def __init__(self, data=None):
        self._data = list(data) if data else []
    
    def __getitem__(self, index):
        return self._data[index]
    
    def __setitem__(self, index, value):
        self._data[index] = value
    
    def __delitem__(self, index):
        del self._data[index]
    
    def __len__(self):
        return len(self._data)
    
    def insert(self, index, value):
        self._data.insert(index, value)
    
    def __repr__(self):
        return f"CustomList({self._data})"

# Usage
clist = CustomList([1, 2, 3])
clist.append(4)  # Works because we inherit from MutableSequence


from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            # Update existing key
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        # Evict if over capacity
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove first (least recently used)