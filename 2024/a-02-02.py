#!/usr/bin/env python3

''' Test which sequences are safe if exactly one number is removed. '''

import importlib
day_02_01 = importlib.import_module('a-02-01')
check_increasing = day_02_01.check_increasing
from helpers import read_data_as_list_list_int

def check_with_one_removed(levels: list[int]) -> bool:
    if check_increasing(levels) or check_increasing(levels[::-1]):
        return True
    for i in range(len(levels)):
         tmp_levels = levels[:]
         tmp_levels.pop(i)
         if check_increasing(tmp_levels) or check_increasing(tmp_levels[::-1]):
             return True

    return False

def check_all(levels_list: list[list[int]]) -> int:
    n_safe = 0
    for levels in levels_list:
        if check_with_one_removed(levels):
            n_safe += 1
    return n_safe

if __name__ == '__main__':
    input_filename = 'z-02-01-input.txt'
    levels_list = read_data_as_list_list_int(input_filename)
    n_safe = check_all(levels_list)
    print(f'The number of (potentially) safe sequences is: {n_safe}.')

