import re
from collections import Counter, OrderedDict
from time import time


# load the dictionary when server starts
with open('app/assets/en-use-case.txt') as f:
    dictionary = f.read()

# create counter for each word to find popularity
dictionary = Counter(re.findall(r'\w+', dictionary.lower()))
total_words = sum(dictionary.values())

# rules for soundex
rules = ['aeiouyhw', 'bfpv', 'cgjkqsxz', 'dt', 'l', 'mn', 'r']

def find_soundex(word):
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

# create soudex code for each word
soundex_dict = {}
for word in dictionary:
    soundex = find_soundex(word)
    if soundex in soundex_dict:
        soundex_dict[soundex].append(word)
    else:
        soundex_dict[soundex] = [word]
    
def spell_correct(words):
    words = [word.strip() for word in words if isinstance(word, str)]
    result = {}
    for word in words:
        result[word] = correction(word)
    print(result)
    return result

def correction(word):
    possible_corrections = candidates_soundex(word)
    print([(w, popularity(w)) for w in possible_corrections])
    return max(possible_corrections, key=popularity)

def popularity(word):
    return dictionary[word] / total_words

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
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

def candidates_soundex(word):
    soundex = find_soundex(word)
    print(soundex)
    return (soundex_dict[soundex] if soundex in soundex_dict else [word])
