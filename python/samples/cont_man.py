from contextlib import contextmanager

@contextmanager
def opener(name):
    f = open(name)
    try:
        yield f
    finally:
        f.close()

with opener("file.txt") as f:
    print(f.read())

# Using with statement
with open('file.txt', 'r') as file:
    content = file.read()
# File automatically closed

# Creating custom context manager
from contextlib import contextmanager

@contextmanager
def managed_resource(*args):
    # Setup code
    resource = acquire_resource(*args)
    try:
        yield resource
    finally:
        # Cleanup code
        release_resource(resource)