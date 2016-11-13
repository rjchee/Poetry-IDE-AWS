import json

def rhyming_part(phonemes):
    for i in range(len(phonemes) - 1, 0, -1):
        if phonemes[i][-1] in '12':
            return ' '.join(phoneme.rstrip('012') for phoneme in phonemes[i:])
    return ' '.join(phonemes)

output = {'list': [], 'words': []}
word_map = {}
rhyming_parts = {}
with open('cmudict-0.7b.txt', 'r', encoding='latin1') as f:
#with open('test.txt', 'r') as f:
    for i in range(3):
        f.readline()
    for line in f:
        data = line.strip().split()
        word = data[0].rstrip('()0123456789').lower()
        if word not in word_map:
            word_map[word] = len(word_map)
            output['list'].append(word)
            output['words'].append(list())
        stats = {}
        phonemes = stats['p'] = data[1:]
        stresses = stats['s'] = list(c != '0' for phoneme in phonemes for c in phoneme if c in '012')
        stats['c'] = len(stresses)

        rhyme_part = rhyming_part(phonemes)
        if rhyme_part not in rhyming_parts:
            rhyming_parts[rhyme_part] = []
        rhyming_parts[rhyme_part].append(word_map[word])
        output['words'][word_map[word]].append(stats)

rhymes = {}
for phonemes, words in rhyming_parts.items():
    for word in words:
        if word not in rhymes:
            rhymes[word] = set()
        for other in words:
            if other != word:
                rhymes[word].add(other)
output['rhymes'] = {k: list(v) for k, v in rhymes.items()}
"""
import pprint
pp = pprint.PrettyPrinter()
pp.pprint(output)
#"""
json.dump(output, open('dictionary.json', 'w'))
