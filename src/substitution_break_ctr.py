#!/usr/bin/python

import string
from collections import Counter
from base64 import b64decode
from implement_ctr import ctr_encrypt
from operator import itemgetter
import util


# From wikipedia article on trigrams and letter frequencies
allowed_letters = string.letters + ',.\'"-)(:!?; '

unigrams = [' ', 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'd', 'l', 'c', 'u', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', 'j', 'x', 'q', 'z', ]

digrams = ['th', 'he', 'in', 'er', 'an', 're', 'on', 'at', 'en', 'nd', 'st', 'or', 'te', 'es', 'is', 'ha', 'ou', 'it', 'to', 'ed', 'ti', 'ng', 'ar', 'se', 'al', 'nt', 'as', 'le', 've', 'of', 'me', 'hi', 'ea', 'ne', 'de', 'co', 'ro', 'll', 'ri', 'li', 'ra', 'io', 'be', 'el', 'ch', 'ic', 'ce', 'ta', 'ma', 'ur', 'om', 'ho', 'et', 'no', 'ut', 'si', 'ca', 'la', 'il', 'fo', 'us', 'pe', 'ot', 'ec', 'lo', 'di', 'ns', 'ge', 'ly', 'ac', 'wi', 'wh', 'tr', 'ee', 'so', 'un', 'rs', 'wa', 'ow', 'id', 'ad', 'ai', 'ss', 'pr', 'ct', 'we', 'mo', 'ol', 'em', 'nc', 'rt', 'sh', 'po', 'ie', 'ul', 'im', 'ts', 'am', 'ir', 'yo', 'fi', 'os', 'pa', 'ni', 'ld', 'sa', 'ay', 'ke', 'mi', 'na', 'oo', 'su', 'do', 'ig', 'ev', 'gh', 'bl', 'if', 'tu', 'av', 'pl', 'wo', 'ry', 'bu']

trigrams =['the', 'ing', 'and', 'ion', 'ent', 'hat', 'her', 'tio', 'tha', 'for', 'ter', 'ere', 'his', 'you', 'thi', 'ate', 'ver', 'all', 'ati', 'ith', 'rea', 'con', 'wit', 'are', 'ers', 'int', 'nce', 'sta', 'not', 'eve', 'res', 'ist', 'ted', 'ons', 'ess', 'ave', 'ear', 'out', 'ill', 'was', 'our', 'men', 'pro', 'com', 'est', 'ome', 'one', 'ect', 'ive', 'tin', 'hin', 'hav', 'ght', 'but', 'igh', 'ore', 'ain', 'str', 'oul', 'per', 'sti', 'ine', 'uld', 'ste', 'tur', 'man', 'oth', 'oun', 'rom', 'ble', 'nte', 'ove', 'ind', 'han', 'hou', 'whi', 'fro', 'use', 'der', 'ame', 'ide', 'ort', 'und', 'rin', 'cti', 'ant', 'hen', 'end', 'tho', 'art', 'red', 'lin']

class KeyStream:
    ''' A strange extension of string class to manage semi decoded keystream 
        Yes, I rewrote a crude string implementation using lists
    '''

    def __init__(self, length):
        self.string = ['']*length

    def assign(self, start_position, string):
        ''' Assign the string starting at start_position '''
        self.string[start_position:(start_position+len(string))] = string

    def available(self, start_position, string):
        ''' Check if the string can be assigned starting at start_position '''
        for c in xrange(start_position, start_position+len(string)):
            if self.string[c] != '' and self.string[c] != string[c - start_position]:
                return False
        return True

    def __repr__(self):
        return repr(self.__str__())

    def __str__(self):
        s = ''
        for i in self.string:
            s += i
            if i == '':
                s += '\0'
        return s

keystream = KeyStream(0)

def get_ciphertexts():
    return [ctr_encrypt(b64decode(line)) for line in open('substitution_break_ctr.in').readlines()]

def most_occurences(l):
    c = Counter()
    for i in l:
        c[i] += 1
    return c

def repeated_ngrams(ciphertexts, ngram_length):
    ''' Count ngrams of ngram_length from ciphertext at every position
        Result is sorted, stored in an array of dictionaries
        with keys:
            count -> number of occurences
            start -> start index
            content -> ngram which repeated
    '''
    # Maximum length of a ciphertext
    max_length = max([len(i) for i in ciphertexts])

    # Array to store the most repeated n-grams
    most_common = []

    # Count n-grams starting at every possible position
    for end in xrange(ngram_length, max_length):
        counter = Counter()
        for ciphertext in ciphertexts:
            ngram = ciphertext[end - ngram_length:end]
            # A simple check for verification
            if len(ngram) != ngram_length:
                continue
            counter[ngram] += 1

        for ngram, count in counter.most_common():
            if count == 1:
                break
            most_common.append({'count': count, 'start': end - ngram_length, 'content': ngram})
    most_common.sort(key=itemgetter('count'), reverse=True)
    return most_common

def try_ngrams(ciphertexts, length, ngram_frequency):
    ''' Match most repeated ngram with most common possible
        ngrams (from the list declared above), going down to least
        possible occurence
    '''
    global trigrams
    global keystream
    most_common = repeated_ngrams(ciphertexts, length)

    # Start with most occured ngram
    for repeated_ngram in most_common:
        # ngram reference frequency
        for ngram in ngram_frequency:
            possible_keystream = util.string_xor(repeated_ngram['content'], ngram)
            start = repeated_ngram['start']
            s = ''
            # Go through every ciphertext, and apply keystream at that position
            for ciphertext in ciphertexts:
                s += util.string_xor(possible_keystream, ciphertext[start:start+length]) + '-'
            if len(s.strip(allowed_letters)) == 0:
                if keystream.available(start, possible_keystream):
                    keystream.assign(start, possible_keystream)

def print_decoded(ciphertexts, keystream):
    for ciphertext in ciphertexts:
        print repr(util.string_xor(ciphertext, str(keystream)))

def main():
    global keystream
    ciphertexts = get_ciphertexts()

    max_length = max([len(i) for i in ciphertexts])
    keystream = KeyStream(max_length)

    try_ngrams(ciphertexts, 1, unigrams)
    print '-----------------After unigrams------------------'
    print 'Keystream: ', repr(keystream)
    print_decoded(ciphertexts, keystream)

    print '\n'*3
    print 'Looks like unigrams did most of the job, rest seems deciperhable'

if __name__ == '__main__':
    main()
