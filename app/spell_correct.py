import re
from collections import Counter, OrderedDict
from time import time


# load the dictionary when server starts
with open('app/assets/en-use-case.txt') as f:
    dictionary = f.read()

# create counter for each word to find popularity
dictionary = Counter(re.findall(r'\w+', dictionary.lower()))
total_words = sum(dictionary.values())

# dictionary with deletes1 and deletes2 for faroo method
faroo_dict = {}

# rules for soundex
rules = ['aeiouyhw', 'bfpv', 'cgjkqsxz', 'dt', 'l', 'mn', 'r']
# for storing soundex code for each known word
soundex_dict = {}

def init_faroo():
    faroo_dict = {word: [word] for word in dictionary.keys()}
    deletes1 = [dw1 for word in faroo_dict for dw1 in deletes(word)]
    deletes2 = [dw2 for dw1 in deletes1 for dw2 in deletes(dw1)]
    deletes_dict = {}
    for word in faroo_dict.copy().items():
        for dw in deletes1 + deletes2:
            if dw in faroo_dict:
                faroo_dict[dw].append(word)
            elif dw in deletes_dict:
                deletes_dict[dw].append(word)
            else:
                deletes_dict[dw] = [word]
    faroo_dict.update(deletes_dict)
                
def init_soundex():
    "Initializes the soundex dictionary of known words"
    for word in dictionary:
        soundex = find_soundex(word)
        if soundex in soundex_dict:
            soundex_dict[soundex].append(word)
        else:
            soundex_dict[soundex] = [word]

def find_soundex(word):
    "Given a word, find it's soundex code"
    if word:
        soundex = word[0]
        for i in range(1, len(word)):
            for j, rule in enumerate(rules):
                if word[i] in rule:
                    soundex += str(j)
                    break
        soundex = ''.join(OrderedDict.fromkeys(soundex).keys())
        soundex = soundex.replace('0', '')
        return soundex
    
def spell_correct(words, method=None):
    words = [word.strip().lower() for word in words if isinstance(word, str)]
    result = {}
    for word in words:
        result[word] = correction(word, method)
    return result

def correction(word, method):
    if method == 'soundex':
        possible_corrections = candidates_soundex(word)
    elif method == 'faroo':
        possible_corrections = candidates_faroo(word)
    else:  # norvig
        possible_corrections = candidates_norvig(word)
    # print([(w, popularity(w)) for w in possible_corrections])
    return max(possible_corrections, key=popularity)

def candidates_norvig(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def candidates_soundex(word):
    soundex = find_soundex(word)
    return (soundex_dict[soundex] if soundex in soundex_dict else [word])

def candidates_faroo(word):
    "All edits that are one delete away from word."
    deletes1 = deletes(word)
    deletes2 = [dw2 for dw1 in deletes1 for dw2 in deletes(dw1)]
    return (orig_known_word([word]) or orig_known_word(deletes1)
            or orig_known_word(deletes2))

# Next four function are taken from http://norvig.com/spell-correct.html
def popularity(word):
    return dictionary[word] / total_words

def known(words): 
    "The subset of `words` that appear in the dictionary."
    return set(w for w in words if w in dictionary)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))
            
def deletes(word):
    "Edits with one delete distance"
    return set([word.replace(c, '', 1) for c in word])

def orig_known_word(words):
    "Original dictionary words for subset of given words that exists in faroo_dict"
    return set(faroo_dict[w] for w in words if w in faroo_dict)

# initialize all dictionaries required for each methods
init_soundex()
#init_faroo()

