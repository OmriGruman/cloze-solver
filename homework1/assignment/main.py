import json


def solve_cloze(input, candidates, lexicon, corpus):
    # todo: implement this function
    print(f'starting to solve the cloze {input} with {candidates} using {lexicon} and {corpus}')

    # Go over the input text and locate the blank spaces
    # for every blank space, detect the N-gram before the blank
    # Calc word frequencies for the detected N-gram
    # take the word with the maximum value for the found N-gram from the candidates
    # add to the result list

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

    print('cloze solution:', solution)
