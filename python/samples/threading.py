import threading
import time

def worker():
    print("start")
    time.sleep(1)
    print("done")

t = threading.Thread(target=worker)
t.start()
t.join()
