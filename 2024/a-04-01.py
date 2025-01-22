FieldData = list[list[str]]
Indexlist = list[int]

from helpers import read_data_as_list_list

def make_test_string(data: FieldData, y_indices: Indexlist, x_indices: Indexlist) -> str:
    '''
    Create test string to check if it equals "XMAS"

    Parameters
    ----------
    data: list[list[str]]
      The entire field of data that is checked
    y_indices: list[int]
      The y indices from which to create the test string
    x_indices: list[int]
      The x indices from which to create the test string

    Returns
    -------
    result_string: str
      If any indices are invalid, this will be ''
    '''

    if any([index < 0 for index in y_indices]):
        return ''
    if any([index < 0 for index in x_indices]):
        return ''
    try:
        return ''.join([data[yi][xi] for yi,xi in zip(y_indices, x_indices)])
    except IndexError:
        return ''

def increase(index: int):
    return range(index,index+4)

def decrease(index: int):
    return range(index,index-4,-1)

def constant(index: int):
    return [index for _ in range(4)]

def find_xmas_for_one_tile(
        data: FieldData,
        y: int,
        x: int
        ) -> int:
    '''
    Check how many "XMAS" strings start on tile (y,x).

    Parameters
    ----------
    data: list[list[str]]
      The entire field of data that is checked
    y: int
      The y index for which to create the test string
    x: int
      The x index for which to create the test string


    Returns
    -------
    result: int
      The number of "XMAS" strings starting on (y,x)
    '''

    result = 0

    y_list, x_list = [], []
    # check N -> S
    y_list.append(increase(y))
    x_list.append(constant(x))
    # check NE -> SW
    y_list.append(increase(y))
    x_list.append(decrease(x))
    # check E -> W
    y_list.append(constant(y))
    x_list.append(decrease(x))
    # check SE -> NW
    y_list.append(decrease(y))
    x_list.append(decrease(x))
    # check S -> N
    y_list.append(decrease(y))
    x_list.append(constant(x))
    # check SW -> NE
    y_list.append(decrease(y))
    x_list.append(increase(x))
    # check W -> E
    y_list.append(constant(y))
    x_list.append(increase(x))
    # check NW -> SE
    y_list.append(increase(y))
    x_list.append(increase(x))


    for y_indices, x_indices in zip(y_list, x_list):
        test_string = make_test_string(data, y_indices, x_indices)
        if test_string != 'XMAS':
            continue

        result += 1

    return result

def find_all_xmas(data: FieldData) -> int:
    '''
    Sum up for all tiles how many "XMAS" strings start on tile.

    Parameters
    ----------
    data: list[list[str]]
      The entire field of data that is checked

    Returns
    -------
    total_sum: int
    '''
    n_x, n_y = len(data[0]), len(data)
    total_sum = 0

    for y in range(n_y):
        for x in range(n_x):
            if data[y][x] != 'X':
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
    print(f'The number of "XMAS" is {total_sum}.')
