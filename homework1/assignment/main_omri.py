import json
import re
from collections import defaultdict
from time import time
start = time()

N = 2
BLANK = '__________'


def read_files(cloze, candidates, corpus):
    print("Read cloze..")
    with open(cloze, 'r', encoding='utf-8') as f:
        cloze_text = f.read()
    print("Read candidates..")
    with open(candidates, 'r', encoding='utf-8') as f:
        candidate_words = f.read().split()
    print("Read corpus..")
    with open(corpus, 'r', encoding='utf-8') as f:
        corpus_text = f.read()
    return cloze_text, candidate_words, corpus_text


def find_cloze_preceding_words(cloze_text):
    return [match.group() for match in re.finditer(fr'(\S+\s){{{N-1}}}(?={BLANK})', cloze_text)]


def count_ngram_ending_freqs(text, ngram_beginnings, candidate_words):
    ending_freqs = {begin: defaultdict(int) for begin in ngram_beginnings}

    for match in re.finditer(fr'(\S+\s){{{N-1}}}(?=\S+)', text):
        match = match.group()
        beginning = match[:match.rfind(' ')+1]
        ending = match[match.rfind(' ')+1:]
        if beginning in ngram_beginnings and ending in candidate_words:
            ending_freqs[beginning][ending] += 1

    return ending_freqs


def solve_cloze(cloze, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {cloze} with {candidates} using {lexicon} and {corpus}')

    cloze_text, candidate_words, corpus_text = read_files(cloze, candidates, corpus)
    ngram_beginnings = find_cloze_preceding_words(cloze_text)
    print(ngram_beginnings)
    ngram_frequencies = count_ngram_ending_freqs(corpus_text, ngram_beginnings, candidate_words)
    print(ngram_frequencies)

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
