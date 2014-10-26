#!/usr/bin/env python

from collections import defaultdict
import itertools
import re
import subprocess
import unicodedata

language = 'fr'
words_without_vowels = defaultdict(list)

mapping = {
    0: ['s', 'c'],
    1: ['t', 'd'],
    2: ['n'],
    3: ['m'],
    4: ['r'],
    5: ['l'],
    6: ['j', 'g'],
    7: ['k', 'q', 'c'],
    8: ['f', 'v'],
    9: ['p', 'b'],
}

print("Extracting words...")

words = subprocess.check_output(['aspell', '-d', language, 'dump', 'master']).splitlines()
words = [word.decode('utf-8') for word in words]

for word in words:
    word = word.strip()
    word_without_accents = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('ascii')
    word_without_accents = re.sub(r'(.)\1+', r'\1', word_without_accents)
    word_without_accends = word_without_accents.rstrip('s')
    word_without_vowels = ''.join([l for l in word_without_accents if l not in ['a', 'e', 'i', 'o', 'u', 'y', 'h']])
    words_without_vowels[word_without_vowels].append(word)

print("%d words extracted" % len(words))


def find_in(wl, number, mapping):
    permutations = itertools.product(*[mapping[int(x)] for x in number])
    matches = {}

    for permutation in permutations:
        permutation_str = ''.join(permutation)

        if permutation_str in wl:
            matches[permutation_str] = wl[permutation_str]

    return matches

while True:
    nb = raw_input('Enter a number to translate (C-c to quit): ')
    matches = find_in(words_without_vowels, nb, mapping)

    for permutation, words in matches.items():
        print(permutation)

        for word in words:
            print(word.encode('utf-8'))

        print('')
