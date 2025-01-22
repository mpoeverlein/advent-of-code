#!/usr/bin/env python3

'''
We identify which sequences are always increasing by 1,2 or 3.
'''

from helpers import read_data_as_list_list

def check_increasing(levels: list[int]) -> bool:
    '''
    All numbers must differ by at least one and at most three.

    Parameters
    ----------
    levels: list[int]
      One sequence to check if increasing

    Returns
    -------
    all_increasing: bool

    '''
    difference_list = [b-a for a,b in zip(levels, levels[1:])]
    all_increasing = all([1 <= difference <= 3 for difference in difference_list])
    return all_increasing

def check_all(levels_list: list[list[int]]) -> int:
    '''
    Check how many sequences are safe.

    Parameters
    ----------
    levels_list: list[list[int]]
      All sequence to check if increasing

    Returns
    -------
    n_safe: int
    '''
    n_safe = 0
    for levels in levels_list:
        if check_increasing(levels) or check_increasing(levels[::-1]):
            n_safe += 1
    return n_safe

if __name__ == '__main__':
    input_filename = 'z-02-01-input.txt'
    levels_list = read_data_as_list_list(input_filename, datatype=int)
    n_safe= check_all(levels_list)
    print(f'The number of safe sequences is: {n_safe}.')
