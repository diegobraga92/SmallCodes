import cProfile

def work():
    sum(i*i for i in range(1000000))

cProfile.run('work()')