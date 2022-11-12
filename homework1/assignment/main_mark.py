import json
import re
from collections import defaultdict
from timeit import default_timer as timer
from datetime import timedelta

import numpy as np

N = 2
Cloze = "__________"
Space = ' '

def tеxt_to_ngram_nested_dict(filename,n_grams, candidates):
    res = defaultdict(lambda: defaultdict(int))

    with open(filename, 'r', encoding='utf-8') as fin:
        print('reading the text file...')
        for i, line in enumerate(fin.readlines()):
            splited_line = line.split()
            for ind in range(len(splited_line)-N):
                curr = ''
                for j in range(N-1):
                    curr += splited_line[ind+j]+' '
                curr = curr[:-1]
                if(curr in n_grams and splited_line[ind+N-1] in candidates):
                    res[curr][splited_line[ind+N-1]]+=1
            if i % 100000 == 0:
                print(i)

    return res
# [t.start() for t in re.finditer('hey', s)]
def read_input(input):
    n_gram = []
    with open(input, 'r') as text:
        txt = text.read().replace('\n',' ')
        cloze_loc = [t.start() for t in re.finditer(Cloze, txt)]
        spaces_loc = np.array([t.start() for t in re.finditer(Space, txt)])

        for ind in cloze_loc:
            start_index = spaces_loc[spaces_loc < ind][-N]
            n_gram.append(txt[start_index+1: ind-1])

    return cloze_loc, n_gram


def solve_single(n_gram, candidates, text):
    txt = text.read()
    lambda_helper = lambda a: len(re.findall(n_gram + a, txt))
    winner = list(map(lambda_helper, candidates))
    return winner

def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    _, n_grams = read_input(input)

    with open(candidates, 'r') as cand:
        candidates = list(map(lambda a: a[:-1],list(cand.readlines())))

    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')

    start = timer()

    ans = tеxt_to_ngram_nested_dict(corpus, n_grams, candidates)
    for gram, dic in ans.items():
        print(gram + ' :')
        print([cand + ' : ' + str(value) for cand, value in dic.items()])
    end = timer()
    print(timedelta(seconds=end - start))
    x=1
    return list()  # return your solution


if __name__ == '__main__':

    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    solution = solve_cloze(config['input_filename'],
                           config['candidates_filename'],
                           config['lexicon_filename'],
                           config['corpus'])

    print('cloze solution:', solution)
