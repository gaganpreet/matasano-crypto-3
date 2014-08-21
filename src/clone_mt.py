from mersenne_twister import MersenneTwister

class ClonedMersenneTwister:
    length = 624

    def __init__(self, state, index):
        self.state = state[:]
        self.index = index

    def next(self):
        if self.index == 0:
            self.generate_numbers()

        y = self.state[self.index]
        y = y ^ (y >> 11)
        y = y ^ (y << 7) & 2636928640
        y = y ^ (y << 15) & 4022730752
        y = y ^ (y >> 18)

        self.index = (self.index + 1) % self.length
        return y

    def generate_numbers(self):
        for i in xrange(self.length):
            y = (self.state[i] & 0x80000000) + ((self.state[(i+1) % self.length]) & 0x7fffffff)
            self.state[i] = self.state[(i + 397) % self.length] ^ (y >> 1)
            if y % 2:
                self.state[i] ^= 2567483615

'''
    The following functions are based on http://b10l.com/?p=24
    I worked the basic maths on paper, but was finding a bit hard to get the
    math specifics right.
'''
def untemperA(y):
    return y ^ (y >> 18)

def untemperB(y):
    return y ^ ((y << 15) & 4022730752)

def untemperC(y):
    mask = 2636928640
    a = y << 7
    b = y ^ (a & mask)

    c = b << 7
    d = y ^ (c & mask)

    e = d << 7
    f = y ^ (e & mask)

    g = f << 7
    h = y ^ (g & mask)

    i = h << 7
    k = y ^ (i & mask)

    return k

def untemperD(y):
    a = y >> 11
    b = y ^ a
    c = b >> 11
    return y ^ c

def untemper(n):
    n = untemperA(n)
    n = untemperB(n)
    n = untemperC(n)
    n = untemperD(n)
    return n

def clone_mt(mt):
    state = []
    for i in xrange(624):
        state.append(untemper(mt.next()))
    return ClonedMersenneTwister(state, 0)

if __name__ == '__main__':
    mt = MersenneTwister(0)
    cmt = clone_mt(mt)
    for i in xrange(10):
        print "From cloned: %s, from original: %s" % (mt.next(), cmt.next())
