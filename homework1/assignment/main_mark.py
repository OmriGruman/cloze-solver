import json
import re
from timeit import default_timer as timer
from datetime import timedelta

import numpy as np

N = 2
Cloze = "__________"
Space = ' '

# [t.start() for t in re.finditer('hey', s)]
def read_input(input):
    n_gram = []
    with open(input, 'r') as text:
        txt = text.read()
        cloze_loc = [t.start() for t in re.finditer(Cloze, txt)]
        spaces_loc = np.array([t.start() for t in re.finditer(Space, txt)])

        for ind in cloze_loc:
            start_index = spaces_loc[spaces_loc < ind][-N]
            n_gram.append(txt[start_index: ind])

    return cloze_loc[0], n_gram[0]


def solve_single(n_gram, candidates, text):
    txt = text.read()
    lambda_helper = lambda a: len(re.findall(n_gram + a, txt))
    winner = list(map(lambda_helper, candidates))
    return winner

def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    _, n_gram = read_input(input)
    with open(candidates, 'r') as cand:
        candidates = list(map(lambda a: a[:-1],list(cand.readlines())))
    #print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')
    with open(corpus, 'r', encoding="utf8") as text:
        start = timer()
        print(n_gram)
        print(candidates)
        print(solve_single(n_gram, candidates, text))
        end = timer()
        print(timedelta(seconds=end - start))

    return list()  # return your solution


if __name__ == '__main__':

    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print('cloze solution:', solution)
