#!/usr/bin/python

import struct
from base64 import b64decode
import util

class Counter:
    def __init__(self):
        self.nonce = 0
        self.count = -1

    def next(self):
        self.count += 1
        return self.format()

    def format(self):
        return struct.pack('<Q', self.nonce) + struct.pack('<Q', self.count)

def ctr_encrypt(text, key='YELLOW SUBMARINE', nonce=0):
    ''' CTR encrypt a text using key and nonce '''
    block_size = len(key)
    blocks = util.get_blocks(text, block_size)

    c = Counter()
    encrypted = ''
    for block in blocks:
        keystring = util.ecb_encrypt(c.next(), key)
        encrypted += util.string_xor(keystring, block)

    return encrypted

def ctr_decrypt(text, key='YELLOW SUBMARINE', nonce=0):
    ''' CTR decrypt a text using key and nonce '''
    block_size = len(key)
    blocks = util.get_blocks(text, block_size)

    c = Counter()
    decrypted = ''
    for block in blocks:
        keystring = util.ecb_encrypt(c.next(), key)
        decrypted += util.string_xor(keystring, block)

    return decrypted

if __name__ == '__main__':
    print ctr_decrypt(b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='))
