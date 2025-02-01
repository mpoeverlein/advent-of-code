#!/usr/bin/env python3

'''
Since the actual input data has so many possible arrangements, it is impossible to list them all individually.
Instead, we keep only track of the number of possibilities.
This is done by taking the target string and checking if any of the building blocks fit.
If a block fits, the remainder of the test string is added to the data.
This can be done recursively until only the empty string remains.
Example:
    blocks: r, wr, b, g, bwu, rb, gb, br

    target: gbbr
    -> 'bbr': 1 (possibility for g), 'br': 1 (possibility for gb)
    -> 'br': 2 (possibilities for gb (line above) and g,b)
    -> 'r': 2 (possibilities for gb,r and g,b,r)
    -> '': 2
'''

import importlib
day_19_01 = importlib.import_module('a-19-01')

def make_possibilities_tree(building_blocks: list[str], target: str) -> int:
    '''
    Given a target design and a list of building blocks, find the number of possible arrangements.

    Parameters
    ----------
    building_blocks: list[str]
      e.g. br,gb,ubw, etc.
    targets: list[str]
      e.g. bwrgbr,ubwbeg,etc.

    Returns
    -------
    n_arrangements: int
    '''
    len_max = max([len(b) for b in building_blocks])
    building_blocks_dict = {i: [] for i in range(1,len_max+1)}
    for b in building_blocks:
        building_blocks_dict[len(b)].append(b)

    if target == '': return 0
    data_dict = reduce_string(building_blocks_dict, target, len_max)
    if len(data_dict) == 0: return 0
    while any(key != '' for key in data_dict):
        test_rest = list(data_dict.keys())[0]
        if test_rest == '': # don't pop the empty string!
            test_rest = list(data_dict.keys())[1]
        n_possibilities = data_dict.pop(test_rest)
        test_dict = reduce_string(building_blocks_dict, test_rest, len_max)
        if len(test_dict) == 0: continue # no possibilities!
        for k,v in test_dict.items():
            if k in data_dict:
                data_dict[k] += n_possibilities
            else:
                data_dict[k] = n_possibilities

    if len(data_dict) == 0: return 0
    return data_dict['']

def reduce_string(building_blocks_dict: dict[int,list[str]], target: str, len_max: int) -> dict[str,int]:
    '''
    Given an input string <target>, check which building blocks come next and return dictionary of remainders strings as keys and number of possible arrangement as values.

    Parameters
    ----------
    building_blocks_dict: dict[int,list[str]]
      keys: length of building blocks
      values: all building blocks of certain length
    target: str
      e.g. gbbrwu
    len_max: int
      How long is the longest building block?

    Returns
    -------
    data_dict: dict[str,int]
      keys: remaining string
      values: number of possible arrangements
    '''
    data_dict = {}
    for i in range(1,min(len_max,len(target))+1):
        test_string = target[:i]
        rest_string = target[i:]
        for b in building_blocks_dict[i]:
            if b != test_string:
                continue
            if rest_string in data_dict:
                data_dict[rest_string] += 1
            else:
                data_dict[rest_string] = 1
    return data_dict

def count_possibilities(building_blocks: list[str], targets: list[str]) -> int:
    '''
    The target designs can be built in how many ways?

    Parameters
    ----------
    building_blocks: list[str]
      e.g. br,gb,ubw, etc.
    targets: list[str]
      e.g. bwrgbr,ubwbeg,etc.

    Returns
    -------
    n_possibilities: int
    '''
    return sum([make_possibilities_tree(building_blocks, target) for target in targets])

if __name__ == '__main__':
    input_filename = 'z-19-01-input.txt'
    # input_filename = 'z-19-02-actual-example.txt'
    building_blocks, targets = day_19_01.read_data(input_filename)
    counter = count_possibilities(building_blocks, targets)
    print(f'The number of possible arrangements is {counter}.')

