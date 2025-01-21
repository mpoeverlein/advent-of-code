#!/usr/bin/env python3

'''
For this task, we read in the two lists, sort them, then compute the absolute difference between
corresponding items in the left and right list.
'''

def read_data(input_filename: str) -> list[list[int]]:
    '''
    Return the left and right list from the file <input_filename>.

    Parameters
    ----------
    input_filename: str
      Name of the input file

    Returns
    -------
    [left, right]: list[list[int]]
      The two lists of integers
    '''
    with open(input_filename, 'r') as f:
        lines = f.readlines()

    left, right = [], []
    for line in lines:
        l, r = line.split()
        left.append(int(l))
        right.append(int(r))

    return [left, right]

def compute_distance(left_list: list[int], right_list: list[int]) -> int:
    '''
    Sort the two lists and return the sum of absolute difference between corresponding items

    Parameters
    ----------
    left_list: list[int]
      The left list
    right_list: list[int]
      The right list

    Returns
    -------
    distance: int
      The sum of absolute differences after sorting
    '''
    left_list.sort()
    right_list.sort()
    distance = sum([abs(l-r) for l,r in zip(left_list, right_list)])
    return distance

def test_compute_distance() -> None:
    left_list, right_list = [3,5,4], [2,6,1]
    expected_result = 5
    obtained_result = compute_distance(left_list, right_list)
    assert expected_result == obtained_result, 'Test for "compute_distance()" failed!'

if __name__ == '__main__':
    test_compute_distance()
    input_filename = 'z-01-01-input.txt'
    left_list, right_list = read_data(input_filename)
    print(compute_distance(left_list, right_list))
