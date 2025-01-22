from copy import deepcopy

def read_data(f: str) -> list[int]:
    with open(f, 'r') as ff:
        line = ff.readline()
    return [int(s) for s in line.strip()]

def uncompress(data_list: list[int]) -> list[dict[str, int], dict[int, str]]:
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
    max_length = 0
    for k,v in data_dict.items():
        max_length = max(max_length, max(v))
    
    result = (max_length+1) * ['.']
    for k,v in data_dict.items():
        for j in v:
            result[j] = str(k)

    return ''.join(result)

def print_inverse_data_dict(inverse_data_dict: dict[str, int]) -> str:
    max_length = max(inverse_data_dict.keys()) + 1
    result = max_length * ['.']
    for i in range(max_length):
        result[i] = str(inverse_data_dict[i])

    return ''.join(result)

def move_blocks(inverse_data_dict):
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
    for k,v in reversed(d.items()):
        if v != '.':
            return k

def find_empty_block(d):
    for k,v in d.items():
        if v == '.':
            return k

def filesystem_checksum(reordered_data_dict) -> int:
    counter = 0
    print(reordered_data_dict)
    for k,v in reordered_data_dict.items():
        if v == '.':
            return counter
        counter += k * int(v)

    return counter

input_filename = 'z-09-02-actual-example.txt'
input_filename = 'z-09-01-input.txt'
data_list = read_data(input_filename)
# print(data_list)
data_dict, inverse_data_dict = uncompress(data_list)
# print(data_dict)
# print(inverse_data_dict)
result = print_data_dict(data_dict)
# print(result)
result = print_inverse_data_dict(inverse_data_dict)
# print(result)
reordered_data_dict = move_blocks(inverse_data_dict)
# print(reordered_data_dict)
# print(print_inverse_data_dict(reordered_data_dict))
print(filesystem_checksum(reordered_data_dict))
