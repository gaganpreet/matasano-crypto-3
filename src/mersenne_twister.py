class MersenneTwister:
    length = 624
    def __init__(self, seed=0):
        self.state = [0]*self.length
        self.index = 0

        self.state[0] = seed
        for i in xrange(1, self.length):
            t = 1812433253 * (self.state[i-1] ^ (self.state[i-1] >> 30)) + i
            self.state[i] = t & (2**32 -1)

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
            y = (self.state[i] & 0x80000000) + ((self.state[(i+1)%self.length]) & 0x7fffffff)
            self.state[i] = self.state[(i + 397) % self.length] ^ (y >> 1)
            if y % 2:
                self.state[i] ^= 2567483615

if __name__ == '__main__':
    mt = MersenneTwister(0)
    for i in xrange(10):
        print i, mt.next()
