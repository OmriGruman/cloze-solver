import json
import re
from collections import defaultdict
from time import time
start = time()

N = 2
BLANK = '__________'


def read_files(cloze, candidates, corpus):
    with open(cloze, 'r', encoding='utf-8') as f:
        cloze_text = f.read()
    with open(candidates, 'r', encoding='utf-8') as f:
        candidate_words = f.read().split()
    with open(corpus, 'r', encoding='utf-8') as f:
        corpus_text = f.read()
    return cloze_text, candidate_words, corpus_text


def find_cloze_preceding_words(cloze_text):
    return [match.group() for match in re.finditer(fr'(\S+\s){{{N-1}}}(?={BLANK})', cloze_text)]


def count_ngram_ending_freqs(text, ngram_begin, candidate_words):
    ending_freqs = defaultdict(int)
    print(f"[{(time() - start):.2f}] LOOKING FOR {ngram_begin}")
    for match in re.finditer(fr'(?<={ngram_begin})\S+', text):
        if match.group() in candidate_words:
            ending_freqs[match.group()] += 1

    return ending_freqs


def solve_cloze(cloze, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {cloze} with {candidates} using {lexicon} and {corpus}')

    cloze_text, candidate_words, corpus_text = read_files(cloze, candidates, corpus)
    ngram_beginnings = find_cloze_preceding_words(cloze_text)

    ngram_frequencies = {
        ngram_begin: count_ngram_ending_freqs(corpus_text, ngram_begin, candidate_words)
        for ngram_begin in ngram_beginnings
    }
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
