#!/usr/bin/env python3

'''
For this task, we read in the two lists and count how often an item of the left list appears in the right list.
The score is the sum of each item in the left list times its frequency in the right list.
'''

import importlib
day_01_01 = importlib.import_module('a-01-01')

def make_frequency_dictionary(right_list: list[int]) -> dict[int, int]:
    '''
    Count frequency of each item in <right_list>.

    Parameters
    ----------
    right_list: list[int]
      The input list

    Returns
    -------
    frequency_dictionary: dict[int,int]
      Dictionary with keys: numbers appearing <right_list> and values their frequency

    '''

    frequency_dictionary = {}
    for r in right_list:
        if r in frequency_dictionary:
            frequency_dictionary[r] += 1
        else:
            frequency_dictionary[r] = 1
    return frequency_dictionary

def make_similarity_score(left_list: list[int], frequency_dictionary: dict[int, int]) -> int:
    '''
    Multiplies items in <left_list> by values in <frequency_dictionary>

    Parameters
    ----------
    left_list: list[int]

    frequency_dictionary: dict[int,int]

    Returns
    -------
    similarity_score: int

    '''
    similarity_score = 0
    for l in left_list:
        if l not in frequency_dictionary:
            continue
        similarity_score += l * frequency_dictionary[l]
    return similarity_score

def test_make_frequency_dictionary():
    right_list = [0, 0, 1, 2, 3, 3, 2]
    expected_result = {0: 2, 1: 1, 2: 2, 3: 2}
    obtained_result = make_frequency_dictionary(right_list)
    assert expected_result == obtained_result, 'Test for "make_frequency_dictionary()" failed!'

if __name__ == '__main__':
    test_make_frequency_dictionary()
    input_filename = 'z-01-01-input.txt'
    left_list, right_list = day_01_01.read_data(input_filename)
    frequency_dictionary = make_frequency_dictionary(right_list)
    similarity_score = make_similarity_score(left_list, frequency_dictionary)
    print(f'The similarity score is: {similarity_score}.')
