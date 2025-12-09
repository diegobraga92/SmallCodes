from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def f(x): return x*x
with ThreadPoolExecutor() as ex:
    print(ex.map(f, range(5)))