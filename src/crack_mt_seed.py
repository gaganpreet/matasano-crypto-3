import time
import random
from mersenne_twister import MersenneTwister

def rng():
    time.sleep(random.randint(42, 1024))
    mt = MersenneTwister(int(time.time()))
    time.sleep(random.randint(42, 1024))
    return mt.next()

def crack_seed(r):
    now = int(time.time())
    start = int(now - 5000)
    end = int(now + 5000)

    for i in xrange(start, end):
        if MersenneTwister(i).next() == r:
            return i

if __name__ == '__main__':
    r = rng()
    print crack_seed(r)
