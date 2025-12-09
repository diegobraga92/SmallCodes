import functools
def timer(fn):
    @functools.wraps(fn)
    def wrapper(*a, **kw):
        import time
        t0 = time.time()
        res = fn(*a, **kw)
        print("elapsed", time.time()-t0)
        return res
    return wrapper

@timer
def work(n):
    sum(range(n))

work(1000000)

def timer_decorator(func):
    """Measures function execution time"""
    import time
    
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.2f} seconds")
        return result
    return wrapper

@timer_decorator
def expensive_operation():
    import time
    time.sleep(1)
    return "Done"