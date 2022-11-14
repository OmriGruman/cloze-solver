import json
import re
import numpy as np

from time import time

start = time()
print()

N = 4
BLANK = '__________'


def find_cloze_preceding_words(cloze_text):
    return [match.group().split() for match in re.finditer(fr'(\S+\s){{{N-1}}}(?={BLANK})', cloze_text)]


def count_ngram_ending_freqs(corpus, ngram_beginnings, candidate_words):
    probabilities = np.zeros((len(ngram_beginnings), N-1, len(candidate_words)))

    with open(corpus, 'r', encoding='utf-8') as f:
        window = [""] * N
        for i, line in enumerate(f):
            for word in line.split():
                window = window[1:]
                if word in candidate_words:
                    for n in range(N-1):
                        for b, begin in enumerate(ngram_beginnings):
                            if window[N-1-n-1:] == begin[N-1-n-1:]:
                                probabilities[b][n][candidate_words.index(word)] += 1
                window.append(word)

            if i % 100000 == 0:
                print(f'[{(time() - start):.2f}] {i}')

    return probabilities


def solve_cloze(cloze, candidates, lexicon, corpus):
    print(f'[{(time() - start):.2f}] starting to solve the cloze {cloze} with {candidates} using {lexicon} and {corpus}')

    with open(cloze, 'r', encoding='utf-8') as f:
        cloze_text = f.read()
    with open(candidates, 'r', encoding='utf-8') as f:
        candidate_words = f.read().split()

    ngram_beginnings = find_cloze_preceding_words(cloze_text)
    print(ngram_beginnings)

    probabilities = count_ngram_ending_freqs(corpus, ngram_beginnings, candidate_words)

    for b, begin in enumerate(ngram_beginnings):
        print(f'-------- {begin}')
        for n in range(N-1):
            print(f'---- {begin[N-1-n-1:]}')
            for c, candidate in enumerate(candidate_words):
                print(f'{candidate} = {probabilities[b][n][c]}')

    return list()  # return your solution

# Random chance:
# generate 100 permutations of the candidates
# calculate mean of the accuracy of all permutations


if __name__ == '__main__':
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print(f'[{(time() - start):.2f}] cloze solution:', solution)
