import json
import re
import numpy as np

from time import time

start = time()

N_PRE = 3
N_POST = 3
BLANK = '__________'
PADDING = '#'


def find_cloze_context(cloze_text):
    cloze_text = ' '.join([PADDING] * N_PRE + [cloze_text] + [PADDING] * N_POST)
    prefixes = [match.group().lower().split() for match in re.finditer(fr'(\S+\s){{{N_PRE}}}(?={BLANK})', cloze_text)]
    suffixes = [match.group().lower().split() for match in re.finditer(fr'(?<={BLANK})(\s\S+){{{N_POST}}}', cloze_text)]

    return prefixes, suffixes


def find_context_in_window(window, context, candidate_words, probabilities):
    context_i, (pre, post) = context
    curr_context = pre + [window[N_PRE]] + post

    for context_size in range(N_PRE + N_POST, -1, -1):
        max_n_pre = min(context_size, N_PRE)
        min_n_pre = max(context_size - N_POST, 0)

        for n_pre in range(max_n_pre, min_n_pre - 1, -1):
            n_post = context_size - n_pre

            start_pos = N_PRE - n_pre
            end_pos = len(window) - (N_POST - n_post)
            sub_window = window[start_pos: end_pos]
            sub_context = curr_context[start_pos: end_pos]

            if sub_context == sub_window:
                probabilities[context_i, n_pre, n_post, candidate_words.index(window[N_PRE])] += 1


def evaluate_sliding_window(window, prefixes, suffixes, candidate_words, probabilities):
    if window[N_PRE] in candidate_words:
        for context in enumerate(zip(prefixes, suffixes)):
            find_context_in_window(window, context, candidate_words, probabilities)


def calc_word_probabilities_by_context(corpus, prefixes, suffixes, candidate_words):
    probabilities = np.zeros((len(prefixes), N_PRE + 1, N_POST + 1, len(candidate_words)))

    with open(corpus, 'r', encoding='utf-8') as f:

        window = [PADDING] * (N_PRE + 1 + N_POST)
        for i, line in enumerate(f):
            for word in line.split():
                window = window[1:] + [word]
                evaluate_sliding_window(window, prefixes, suffixes, candidate_words, probabilities)

            if i % 100000 == 0:
                print(f'[{(time() - start):.2f}] {i}')

        # scan N_POST tokens after the end of the file
        for n_post in range(N_POST):
            window = window[1:] + [PADDING]
            evaluate_sliding_window(window, prefixes, suffixes, candidate_words, probabilities)

    return probabilities


def solve_cloze(cloze, candidates, lexicon, corpus):
    print(f'[{(time() - start):.2f}] starting to solve the cloze {cloze} with {candidates} using {lexicon} and {corpus}')

    with open(cloze, 'r', encoding='utf-8') as f:
        cloze_text = f.read()
    with open(candidates, 'r', encoding='utf-8') as f:
        candidate_words = f.read().split()
        print(candidate_words)

    prefixes, suffixes = find_cloze_context(cloze_text)
    probabilities = calc_word_probabilities_by_context(corpus, prefixes, suffixes, candidate_words)

    for cxt, (pre, post) in enumerate(zip(prefixes, suffixes)):
        print(f'================ {" ".join(pre)} {BLANK} {" ".join(post)}')
        for npre in range(N_PRE + 1):
            for npost in range(N_POST + 1):
                print(f'---- {" ".join(pre[N_PRE - npre:])} {BLANK} {" ".join(post[:npost])}')
                for c, candidate in enumerate(candidate_words):
                    print(f'{candidate} = {probabilities[cxt, npre, npost, c]}')

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
