import time
import sys
import random
from mersenne_twister import MersenneTwister

def rng():
    time.sleep(random.randint(42, 1024))
    mt = MersenneTwister(int(time.time()))
    time.sleep(random.randint(42, 1024))
    return mt.next()

def update_progress(done, total):
    sys.stdout.write('\b'*4)
    progress = str(int(100.0*done/total))
    text = (3 - len(progress)) * ' ' + progress +  '%'
    sys.stdout.write(text)
    sys.stdout.flush()

def crack_seed(r):
    now = int(time.time())
    start = (now - 2000)
    end = now

    for i in xrange(start, end+1):
        update_progress(i - start, end-start)
        if MersenneTwister(i).next() == r:
            print
            return i
    print
    return "FAILED"

if __name__ == '__main__':
    print 'Sleeping now, will take a while!'
    r = rng()
    print 'Starting to crack now!'
    print crack_seed(r)
