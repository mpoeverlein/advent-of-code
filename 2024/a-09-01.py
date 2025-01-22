from copy import deepcopy

def read_data(input_filename: str) -> list[int]:
    '''
    Read data from input filename and return as list of integers.

    Parameters
    ----------
    input_filename: str

    Returns
    -------
    result: list[int]
    '''
    with open(input_filename, 'r') as f:
        line = f.readline()
    return [int(s) for s in line.strip()]

def uncompress(data_list: list[int]) -> list[dict[str, int], dict[int, str]]:
    '''
    Translate input sequence into data dictionary and inverse data dictionary

    Parameters
    ----------
    data_list: list[int]
      Numbers, alternatingly indicating occupied and empty blocks

    Returns
    -------
    data_dict: dict[str, int]
      keys: blockID, values: location
    inverse_data_dict: dict[int, str]
      keys: location, values: blockID or empty
    '''

    data_dict, inverse_data_dict = {}, {}
    pointer = 0
    id_counter = 0
    for i, value in enumerate(data_list):
        if i%2 == 0:
            data_dict[id_counter] = []
            for j in range(value):
                data_dict[id_counter].append(j+pointer)
                inverse_data_dict[j+pointer] = str(id_counter)
            id_counter += 1

        else:
            for j in range(value):
                inverse_data_dict[j+pointer] = '.'

        pointer += value
    return data_dict, inverse_data_dict

def print_data_dict(data_dict: dict[str, int]) -> str:
    '''
    Create string representing data of data_dict

    Parameters
    ----------
    data_dict: dict[str, int]
      keys: blockID, values: location

    Returns
    -------
    result: str
    '''
    max_length = 0
    for k,v in data_dict.items():
        max_length = max(max_length, max(v))

    result = (max_length+1) * ['.']
    for k,v in data_dict.items():
        for j in v:
            result[j] = str(k)

    return ''.join(result)

def print_inverse_data_dict(inverse_data_dict: dict[str, int]) -> str:
    '''
    Create string representing data of inverse_data_dict

    Parameters
    ----------
    inverse_data_dict: dict[int, str]
      keys: location, values: blockID or empty

    Returns
    -------
    result: str
    '''
    max_length = max(inverse_data_dict.keys()) + 1
    result = max_length * ['.']
    for i in range(max_length):
        result[i] = str(inverse_data_dict[i])

    return ''.join(result)

def move_blocks(inverse_data_dict: dict[str, int]) -> dict[str, int]:
    '''
    Move blocks such that every blocks was tried to be moved forward if empty blocks allow for it.

    Parameters
    ----------
    inverse_data_dict: dict[int, str]
      keys: location, values: blockID or empty

    Returns
    -------
    reordered_data_dict: dict[str, int]
    '''
    reordered_data_dict = deepcopy(inverse_data_dict)
    while True:
        last_full_block = find_right_block(reordered_data_dict)
        first_empty_block = find_empty_block(reordered_data_dict)

        if first_empty_block > last_full_block:
            break

        reordered_data_dict[first_empty_block] = reordered_data_dict[last_full_block]
        reordered_data_dict[last_full_block] = '.'


    return reordered_data_dict

def find_right_block(d):
    '''
    Get location of last non-empty block.
    Parameters
    ----------
    d: dict[int,str]

    Returns
    -------
    k: int
    '''
    for k,v in reversed(d.items()):
        if v != '.':
            return k

def find_empty_block(d: dict[int,str]) -> int:
    '''
    Get location of first empty block.

    Parameters
    ----------
    d: dict[int,str]

    Returns
    -------
    k: int
    '''
    for k,v in d.items():
        if v == '.':
            return k

def filesystem_checksum(reordered_data_dict: dict[int,str]) -> int:
    '''
    Calculate checksum from reordered data.

    Parameters
    ----------
    reordered_data_dict: dict[int,str]

    Returns
    -------
    counter: int
      Checksum value
    '''

    counter = 0
    for k,v in reordered_data_dict.items():
        if v == '.':
            return counter
        counter += k * int(v)

    return counter

if __name__ == '__main__':
    input_filename = 'z-09-02-actual-example.txt'
    input_filename = 'z-09-01-input.txt'
    data_list = read_data(input_filename)
    data_dict, inverse_data_dict = uncompress(data_list)
    result = print_data_dict(data_dict)
    result = print_inverse_data_dict(inverse_data_dict)
    reordered_data_dict = move_blocks(inverse_data_dict)
    checksum = filesystem_checksum(reordered_data_dict)
    print(f'The checksum is {checksum}.')
