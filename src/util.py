#!/usr/bin/python

import random
from Crypto.Cipher import AES

''' Some util functions '''

def get_blocks(text, block_size):
    ''' Divide a string into equal sized blocks '''
    return [text[start:start+block_size] for start in xrange(0, len(text), block_size)]

def string_xor(x, y):
    ''' Xor two equal length strings character by character '''
    return ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(x,y)])

def random_string(length):
    ''' Generate a random string of length l'''
    return ''.join([chr(random.randint(0, 255)) for i in xrange(length)])

def ecb_decrypt(text, key):
    ''' Decode an AES-128 ECB cipher '''
    c = AES.new(key, AES.MODE_ECB)
    return c.decrypt(text)

def ecb_encrypt(text, key):
    ''' Encode an AES-128 ECB cipher '''
    text = pkcs_pad(text, len(key))
    c = AES.new(key, AES.MODE_ECB)
    return c.encrypt(text)

def cbc_encrypt(text, key, iv):
    ''' CBC encrypt text with initialization vector iv and key '''
    block_length = len(iv)
    text = pkcs_pad(text, block_length)
    blocks = get_blocks(text, block_length)

    blocks[0] = ecb_encrypt(string_xor(blocks[0], iv), key)

    for i in xrange(1, len(blocks)):
        blocks[i] = ecb_encrypt(string_xor(blocks[i], blocks[i-1]), key)

    return ''.join(blocks)

def cbc_decrypt(text, key, iv):
    ''' CBC decrypt text with initialization vector iv and key '''
    block_length = len(iv)
    blocks = get_blocks(text, block_length)

    decoded_blocks = [0] * len(blocks)

    decoded_blocks[0] = string_xor(ecb_decrypt(blocks[0], key), iv)
    for i in xrange(1, len(blocks)):
        decoded_blocks[i] = string_xor(ecb_decrypt(blocks[i], key), blocks[i-1])

    return ''.join(decoded_blocks)

def pkcs_pad(string, block_size):
    ''' PKCS 7 pad a string '''
    pad_length = 0
    if len(string) % block_size > 0:
        pad_length = block_size - (len(string) % block_size)
    
    pad = chr(pad_length)
    return string + pad_length * pad

def is_valid_padding(string):
    ''' Test for validity of PKCS 7 padding on a string '''
    last = string[-1]
    if last * ord(last) == string[-ord(last):]:
        return True
    return False
