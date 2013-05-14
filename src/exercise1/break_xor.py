####################################
####################################
# wget --header='User-Agent: Mozilla/5.0' 'http://www.gutenberg.org/cache/epub/19033/pg19033.txt' -c -O book.txt
###################################
###################################

from collections import Counter 
import string

character_set = string.letters + string.digits + ',.\'"-)(:!?; /'

def decode_xor_cipher(char_map, encoded_string):
    ''' Brute force a xor cipher '''

    scores = Counter()
    for char in char_map.keys():
        possible = xor_cipher(encoded_string, string_xor(char, encoded_string[0]))
        scores[char] = compare_character_frequency(Counter(possible), char_map)

    least_score = scores.most_common()[-1]
    key, score = least_score[:]
    return xor_cipher(encoded_string, string_xor(key, encoded_string[0])), score, string_xor(key, encoded_string[0])

def repeating_key_xor_cipher(input_string, key):
    pad_length = len(input_string) % len(key)
    repeat_factor = len(input_string) / len(key)

    repeated_key = key * repeat_factor + key[:pad_length]

    return string_xor(input_string, repeated_key)

def compare_character_frequency(possible_map, reference_map):
    ''' A score of the string is computed based on the sum of absolute difference of character
        frequencies between the two maps. Least score is the best score
    '''

    possible_map_string = ''.join(possible_map)
    # Ignore strings which have characters other than reference map
    if len(possible_map_string.strip(character_set)) > 0:
        return 1000


    score = 0
    for char, freq in possible_map.items():
        reference_freq = reference_map[char]
        score += abs(reference_freq - freq)

    return score

def decode_repeating_key_xor(text, reference_map, key_size):
    ''' Main function to decode a repeating key xor '''

    key = ''
    for start in xrange(key_size):
        block = text[start::key_size]
        decoded_string, block_score, block_key = decode_xor_cipher(reference_map, block)
        key += block_key

    return repeating_key_xor_cipher(text, key)

# Utility functions
def string_xor(x, y):
    return ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(x,y)])

def xor_cipher(string, key):
    return string_xor(len(string) * key, string)

def get_char_frequency_from_string(string):
    c = Counter(string)
    for k, v in c.items():
        c[k] = v * 1.0 / len(string)
    return c

def get_char_frequency_from_file(file_name):
    contents = open(file_name).read()
    return get_char_frequency_from_string(contents)

