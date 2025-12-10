from multiprocessing import Process
import time

def work():
    s = 0
    for _ in range(10_000_000):
        s += 1
    print("done")

p = Process(target=work)
p.start()
p.join()
