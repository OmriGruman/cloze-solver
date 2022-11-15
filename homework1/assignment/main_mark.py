import json
import re
from collections import defaultdict
from timeit import default_timer as timer
from datetime import timedelta
import numpy as np

N = 4
Cloze = "__________"
Space = ' '


def omri():
    pass


def ans_to_finale(ans):
    res = [] #{candidate : gram[i]}
    for threshhold in range(0.9,0,-0.1):
        for i,gram, dic in enumerate(ans.items()):
            for cand, value in dic.items():
                res[i] = cand
                if (value * len(dic.values()) / sum(dic.values()) > 1):
                    print(cand + ' : ' + str(value / sum(dic.values())))

def tеxt_to_ngram_nested_dict(filename,n_grams, candidates,n):

    res = np.zeros((len(candidates), len(candidates))) #[[0 for _ in range(len(candidates))] for _ in range(len(candidates))]

    with open(filename, 'r', encoding='utf-8') as fin:
        print('reading the text file...')
        for i, line in enumerate(fin.readlines()):
            splited_line = line.split()
            for ind in range(len(splited_line)-n):
                curr = ''
                for j in range(n-1):
                    curr += splited_line[ind+j]+' '
                curr = curr[:-1]
                if(curr in n_grams and splited_line[ind+n-1] in candidates):
                    res[n_grams.index(curr)][candidates.index(splited_line[ind+n-1])] += 1
            if i % 100000 == 0:
                print(i)

    return res
# [t.start() for t in re.finditer('hey', s)]

def full_nested_dict(filename, input, candidates):
    res = np.zeros((len(candidates), len(candidates), N-1)) #[[[0 for _ in range(N-1)] for _ in range(len(candidates))] for _ in range(len(candidates))]
    n = N
    while n > 1:
        n_grams = read_input(input,n)
        ans = tеxt_to_ngram_nested_dict(filename, n_grams, candidates, n)
        for i_gram in range(len(ans)):
            for i_cand in range(len(ans[i_gram])):
                res[i_gram][i_cand][n-2] = ans[i_gram][i_cand]
        n -= 1
    return res

def read_input(input,n):
    n_gram = []
    with open(input, 'r') as text:
        txt = text.read().replace('\n',' ')
        cloze_loc = [t.start() for t in re.finditer(Cloze, txt)]
        spaces_loc = np.array([t.start() for t in re.finditer(Space, txt)])

        for ind in cloze_loc:
            start_index = spaces_loc[spaces_loc < ind][-n]
            n_gram.append(txt[start_index+1: ind-1])

    return n_gram


def solve_single(n_gram, candidates, text):
    txt = text.read()
    lambda_helper = lambda a: len(re.findall(n_gram + a, txt))
    winner = list(map(lambda_helper, candidates))
    return winner

def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')


    with open(candidates, 'r') as cand:
        candidates = list(map(lambda a: a[:-1], list(cand.readlines())))

    start = timer()

    ans = full_nested_dict(corpus, input, candidates)
    n_grams = read_input(input, N)
    for i_gram in range(len(ans)):
        print('--------' + n_grams[i_gram] + ' :')
        for i_cand in range(len(ans[i_gram])):
            for n in range(len(ans[i_gram][i_cand])):

                if sum(ans[i_gram,:,n]) != 0 and ans[i_gram][i_cand][n] * len(ans[i_gram,:,n]!=0) / sum(ans[i_gram,:,n]) >= 2:
                    print('---' + candidates[i_cand] + ' : ' +str(n+2) + ' : ' + str(ans[i_gram][i_cand][n]/sum(ans[i_gram,:,n])))
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
