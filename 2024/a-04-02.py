Field = list[list[str]]
Indexlist = list[int]

import importlib
day_04_01 = importlib.import_module('a-04-01')
from helpers import read_data_as_list_list

def increase(index: int):
    return range(index-1,index+2)

def decrease(index: int):
    return range(index+1,index-2,-1)

def find_xmas_for_one_tile(
        data: Field,
        y: Indexlist,
        x: Indexlist
        ) -> int:

    # check NE -> SW
    test_string = day_04_01.make_test_string(data, increase(y), decrease(x))
    check_ne_sw = test_string in ['MAS', 'SAM']
    # check NW -> SE
    test_string = day_04_01.make_test_string(data, increase(y), increase(x))
    check_nw_se = test_string in ['MAS', 'SAM']

    return 1 if check_ne_sw and check_nw_se else 0

def find_all_xmas(data: Field) -> int:
    # iterate over all letters 
    # if letter is 'A', then check in NE-SW and NW-SE directions if there is 'MAS'
    n_x, n_y = len(data[0]), len(data)
    total_sum = 0

    for y in range(n_y):
        for x in range(n_x):
            if data[y][x] != 'A':
                continue

            total_sum += find_xmas_for_one_tile(data, y, x)

    return total_sum



test_string = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX'''

if __name__ == '__main__':
    input_filename = 'z-04-01-input.txt'
    data = read_data_as_list_list(input_filename, datatype=str, separator='None')
    total_sum = find_all_xmas(data)
    print(f'The number of X-"MAS" is {total_sum}.')
