#!/usr/bin/python

import math
import random
from base64 import b64decode
from util import random_string, cbc_encrypt, cbc_decrypt, is_valid_padding

class RandomAES:
    def __init__(self, block_size=16):
        self.key = random_string(block_size)
        self.block_size = block_size
        self.line = None

    def random_line(self, file_name='cbc_padding_oracle.in'):
        ''' Choose a random line from file and b64decode it '''
        if not self.line:
            with open(file_name) as f:
                lines = f.readlines()
                self.line = b64decode(random.choice(lines))
        return self.line

    def encrypt(self, iv='\0'*16):
        return cbc_encrypt(self.random_line(), self.key, iv), iv

    def decrypt(self, text, iv='\0'*16):
        return is_valid_padding(cbc_decrypt(text, self.key, iv))

def decryptor(block_size):
    ''' Main function to decrypt using padding oracle attack '''
    random_aes = RandomAES(16)

    cipher_text, iv = random_aes.encrypt()

    total_blocks = int(math.ceil(len(cipher_text)/block_size))
    string = ''
    for block_number in xrange(total_blocks):
        string += decrypt_block(cipher_text, iv, block_number, block_size, random_aes.decrypt)
    return string
        
def decrypt_block(cipher_text, iv, block_number, block_size, oracle):
    '''
        C[i] = E(P[i] ^ C[i-1])

        D[i] = D(C[i]) ^ C[i-1]
        D[i] = D(E(P[i] ^ C[i-1])) ^ C[i-1]

        D(E(t)) = t
        So,

        D[i] = (P[i] ^ C[i-1]) ^ C[i-1]
        If we modify C[i-1]
        D'[i] = (P[i] ^ C[i-1]) ^ C'[i-1]

        We get a character which gives a valid PKCS 7 padding:
        i.e. D'[i] = '\x01' for last character
        '\x01' = (P[i] ^ C[i-1]) ^ C'[i-1]

        To get P[i] we xor the three knowns together

    '''

    # start and end of block to be decoded
    block_start = block_number * block_size
    block_end = block_start + block_size

    # The first encoded block is xored with the IV, rest are xored with the previous block
    if block_start != 0:
        previous_block = cipher_text[block_start - block_size:block_start]
    else:
        previous_block = iv

    # The modified block which will be replaced (iv/previous block)
    modified_block = bytearray('\0' * block_size)

    # temp variable where the decoded block will be stored
    decoded_block = bytearray('\0' * block_size)

    # start from the last character in the block
    for i in xrange(block_size - 1, -1, -1):
        # padding character that should be matched
        pad_char = block_size - i

        passed_iv = iv
        for c in xrange(256):
            modified_block[i] = c
            if block_start == 0:
                passed_iv = str(modified_block)
                modified_cipher_text = cipher_text[:block_end]
            else:
                modified_cipher_text = cipher_text[:(block_start-16)] + modified_block + cipher_text[block_start:block_end]

            # Found a match
            if oracle(str(modified_cipher_text), passed_iv):
                decoded_block[i] = c ^ pad_char ^ ord(previous_block[i])
                for j in xrange(i, block_size):
                    # Change all following characters to decrypt to next pad character
                    modified_block[j] = (pad_char + 1) ^ decoded_block[j] ^ ord(previous_block[j])
                break
        else:
            print "Something went wrong! Boo!"

    return str(decoded_block)


if __name__ == '__main__':
    print repr(decryptor(16))
