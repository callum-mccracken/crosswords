import json
import os

import matplotlib.pyplot as plt
import numpy as np

from PyDictionary import PyDictionary
dictionary=PyDictionary()


def define(word):
    meaning = dictionary.meaning(word)
    if meaning is None:
        print('No definition for', word)
        return 'Dictionary had no definition for this word. Make your own!'
    # meaning is a dict which may have 2 keys, one for verb one for noun
    keys = list(meaning.keys())
    # just take the first one, whichever that is
    first_key_defs = meaning[keys[0]]
    # for some reason, some definitions are missing right brackets
    defn = first_key_defs[0]
    if '(' in defn and ')' not in defn:
        defn += ')'
    # that's a list, take the first definition
    return defn


def main(filename):
    """Make a numpy array out of a black and white image"""
    arr = plt.imread(filename)  # im[x,y] = [r,g,b,a]
    if not np.array_equal(np.unique(arr), [0, 1]):
        raise ValueError('Only black&white images are supported')
    if filename.endswith('.png'):
        # assuming grayscale image, all we need is the r channel
        arr = arr[:,:,0]
    else:
        raise ValueError("image file type not supported")
    print('made array from image')


    """
    Then make a Qxw deck.
    Array convention: 1 = letter entry spot, 0 = blank
    """

    # a deck is a list of words, one per line
    # let an "entry word" be a list of numbers corresponding
    # to squares where a word should go
    entry_words = []

    # go through array looking for chains of 1s
    entry_counter = 1  # letter square labelling will begin at 1
    entry_names_arr = np.zeros_like(arr, dtype=int)
    current_entry_word = []

    def record_entry_word_if_needed():
        nonlocal current_entry_word, entry_words
        if current_entry_word != []:
            entry_words.append(current_entry_word)
            current_entry_word = []

    # go across:
    for i, row in enumerate(arr):
        for j, entry_name in enumerate(row):
            if entry_name == 1:
                if entry_names_arr[i, j] == 0:
                    entry_names_arr[i, j] = entry_counter
                    entry_counter += 1
                current_entry_word.append(entry_names_arr[i, j])
            else:  # must be zero
                record_entry_word_if_needed()
        record_entry_word_if_needed()
    record_entry_word_if_needed()

    # crosswords only ever write words of length > 1
    entry_words = [w for w in entry_words if len(w) > 1]
    # how many across words?
    n_across = len(entry_words)

    # then go down (note all entry_names should be assigned by now):
    for j, column in enumerate(arr.transpose()):
        for i, entry_name in enumerate(column):
            if entry_name == 1:
                current_entry_word.append(entry_names_arr[i, j])
            else:
                record_entry_word_if_needed()
        record_entry_word_if_needed()
    record_entry_word_if_needed()

    # again, only count words that have more than 1 letter
    entry_words = [w for w in entry_words if len(w) > 1]
    print(len(entry_words), 'words to find')

    # write deck file
    deck_text = ''
    for w in entry_words:
        deck_text += ' '.join(map(str, w)) + '\n'
    with open('deck.qxd', 'w') as deckfile:
        deckfile.write(deck_text)
    print('made deck file')

    # then run qxw
    print('running qxw, if this takes more than a minute, just quit')
    os.system(f'qxw -b deck.qxd > qxw_output.txt')
    print('done running qxw')

    # then read qxw output file and map back to entry_names_arr, to get words
    with open('qxw_output.txt', 'r') as qxw_output_file:
        lines = qxw_output_file.readlines()
        """ The file looks like:
        W0 ARA
        # Ara
        W1 CYSTIC
        # cystic...
        """
    # skip lines with proper capitalization
    lines = [l for l in lines if '#' not in l]

    # letters_arr is the array of solution letters
    letters_arr = np.zeros_like(entry_names_arr, dtype=str)
    for i, line in enumerate(lines):
        word = line.split()[1]  # 2nd word = actual word
        entry_names_for_word = entry_words[i]
        for en, letter in zip(entry_names_for_word, word):
            letters_arr[entry_names_arr==en] = letter

    # now find which numbers to write for starting squares
    # (e.g. the first square of 23 down should have a 23 in it)
    # should get black squares dealt with here too, using '#'
    starting_square_nums = []
    
    # do across words first
    across_ews = entry_words[:n_across]
    starters_across = {}
    for i, ew in enumerate(across_ews):
        # the across word that starts with entry_name=ew[0] is across word i+1
        # e.g. maybe word [6, 7, 8] is "3 across" (ew[0]=6, i=2)
        starters_across[ew[0]] = i+1
    for row in entry_names_arr:
        newrow = []
        for entry_name in row:
            if entry_name == 0:
                newrow.append('#')
            else:
                if entry_name in starters_across.keys():
                    newrow.append(str(starters_across[entry_name]))
                else:
                    newrow.append("0")
        starting_square_nums.append(newrow)

    # list of numbers for things like the hint list
    across_numbers = list(starters_across.values())

    # now same for down words

    # use a list that we'll append to here, rather than a dict
    # because we may have words that coincide with across words
    down_numbers = []      
    down_ews = entry_words[n_across:]
    starters_down = {}
    for i, ew in enumerate(down_ews):
        starters_down[ew[0]] = n_across + i+1

    for j, column in enumerate(entry_names_arr.transpose()):
        for i, entry_name in enumerate(column):
            if entry_name == 0:
                assert starting_square_nums[i][j] == '#'
            else:
                if entry_name in starters_down.keys():
                    # if not taken
                    if starting_square_nums[i][j] == '0':
                        n = str(starters_down[entry_name])
                        starting_square_nums[i][j] = n
                        down_numbers.append(n)
                    else:
                        # adapt down words to corner nicely with accross
                        n = starting_square_nums[i][j]
                        down_numbers.append(n)
                else:
                    pass

    # get definitions as starter hints
    across_words = []
    for ew in across_ews:
        word = ''
        for en in ew:
            letter = letters_arr[entry_names_arr==en][0]
            word += letter
        across_words.append(word)
    down_words = []
    for ew in down_ews:
        word = ''
        for en in ew:
            letter = letters_arr[entry_names_arr==en][0]
            word += letter
        down_words.append(word)

    across_hints = [define(w) for w in across_words]
    down_hints = [define(w) for w in down_words]



    # put puzzle data here
    puzzle_dict = {
        "origin": "Bean Lord's Puzzle Vault",
        "version": "http://ipuz.org/v2",
        "kind": ["http://ipuz.org/crossword#1"],
        "copyright": "CC0, feel free to spread this around, " +
                     "like your favourite bean paste",
        "author": "Bean Lord",
        "publisher": "Bean Lord, Inc.",
        "title": "Bean Shaped Words",
        "intro": "This puzzle has no clues but it looks like a bean",
        "difficulty": "Impossible",
        "empty": "0",
        "dimensions": { "width": arr.shape[0], "height": arr.shape[1]},
        "puzzle": starting_square_nums,
        "clues":{
            "Across": [[n,h] for n, h in zip(across_numbers, across_hints)],
            "Down": [[n,h] for n,h in zip(down_numbers, down_hints)],
        },
        "solution": letters_arr.tolist()
    }

    # make .ipuz-writeable string
    # there's a bunch of crappy code here, mostly to deal with single vs
    # double quote errors. If you have time, feel free to clean this up
    ipuz_json_string = ""
    for key_idx, key in enumerate(puzzle_dict.keys()):
        value = puzzle_dict[key]
        if type(value) == str:
            print_value = f'"{value}"'
        elif type(value) == list:
            print_value = ""
            for i, v in enumerate(value):
                if type(v) == str:
                    print_value += f'"{v}"'
                elif type(v) == list:
                    inner_print_value = ""
                    for j, inner_v in enumerate(v):
                        inner_print_value += f'"{inner_v}"'
                        if j != len(v)-1:
                            inner_print_value += ','
                    inner_print_value = "[" + inner_print_value + "]"
                    print_value += inner_print_value
                if i != len(value)-1:
                    print_value += ',\n    '
            print_value = "[\n    " + print_value + "\n  ]"
        elif type(value) == dict:
            print_value = ""
            for i, k in enumerate(value.keys()):
                if type(value[k]) in [str, int]:
                    print_value += f'"{k}": {value[k]}'
                elif type(value[k]) == list:
                    inner_print_value = ""
                    for j, inner_v in enumerate(value[k]):
                        if type(inner_v) == list:
                            ipv = ""
                            for q, v in enumerate(inner_v):
                                ipv += f'"{v}"'
                                if q != len(inner_v)-1:
                                    ipv += ','
                            ipv = '['+ipv+']'
                            inner_print_value += ipv
                        else:
                            inner_print_value += f'{inner_v}'
                        if j != len(value[k])-1:
                            inner_print_value += ',\n      '
                    inner_print_value = "[\n      " + inner_print_value + "\n    ]"
                    print_value += f'"{k}": {inner_print_value}'
                if i != len(value.keys())-1:
                    print_value += ',\n    '
            print_value = "{\n    " + print_value + "\n  }"
        else:
            print_value = repr(value)
        if key_idx != len(puzzle_dict.keys()) - 1:
            ipuz_json_string += f'  "{key}": {print_value},\n'
        else:
            ipuz_json_string += f'  "{key}": {print_value}'
    ipuz_json_string = "{\n" + ipuz_json_string + "\n}"

    # write it out
    with open('BeanWord.ipuz', 'w') as f:
        f.write(ipuz_json_string)
    
if __name__ == "__main__":
    main('bean.png')

