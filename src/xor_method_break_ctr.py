'''
20. Break fixed-nonce CTR mode using stream cipher analysis

At the following URL:

   https://gist.github.com/3336141

Find a similar set of Base64'd plaintext. Do with them exactly
what you did with the first, but solve the problem differently.

Instead of making spot guesses at to known plaintext, treat the
collection of ciphertexts the same way you would repeating-key
XOR.

Obviously, CTR encryption appears different from repeated-key XOR,
but with a fixed nonce they are effectively the same thing.

To exploit this: take your collection of ciphertexts and truncate
them to a common length (the length of the smallest ciphertext will
work).

Solve the resulting concatenation of ciphertexts as if for repeating-
key XOR, with a key size of the length of the ciphertext you XOR'd.
'''

from base64 import b64decode
from implement_ctr import ctr_encrypt
from exercise1 import break_xor

def get_ciphertexts():
    return [ctr_encrypt(b64decode(line)) for line in open('3336141/gistfile1.txt').readlines()]

def main():
    ciphertexts = get_ciphertexts()
    min_length = min([len(s) for s in ciphertexts])

    key_size = min_length
    xor_string = ''.join([s[:key_size] for s in ciphertexts])

    print break_xor.decode_repeating_key_xor(xor_string, 
                                       break_xor.get_char_frequency_from_file('exercise1/book.txt'),
                                       key_size)



if __name__ == '__main__':
    main()
