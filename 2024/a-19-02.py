#!/usr/bin/env python3

def read_data(input_filename: str) -> list[list[str]]:
    with open(input_filename, 'r') as f:
        content = ''.join(f.readlines())

    building_blocks, target = content.split('\n\n')
    building_blocks = building_blocks.split(', ')
    target = target.split('\n')

    return building_blocks, target

def print_possibilities(possibilities) -> None:
    print(','.join(['_'.join(p) for p in possibilities]))



def find_all_possibilities_for_blocks(building_blocks: list[str], target: str) -> int:
    ''' this function uses sets in which each item is a tuple of the structure:
        (building_block, building_block, ..., rest of string)
    '''
    if target == '': return 0
    test_sequences = {(target,)}
    possibilities: set = set()
    while len(test_sequences) > 0:
        test_sequence_tuple = test_sequences.pop()
        test_sequence = test_sequence_tuple[-1]
        if test_sequence in building_blocks:
            possibilities.add(test_sequence_tuple)
        for building_block in building_blocks:
            if test_sequence == building_block:
                continue
            if test_sequence.startswith(building_block):
                new_tuple = (*(test_sequence_tuple[:-1]), building_block, test_sequence[len(building_block):])
                test_sequences.add(new_tuple)

    return len(possibilities)

def make_possibilities_dictionary(building_blocks: list[str]) -> dict[str,int]:
    possibilities_dictionary = {}
    for b in building_blocks:
        possibilities_dictionary[b] = find_all_possibilities_for_blocks(building_blocks, b)
    return possibilities_dictionary


def find_all_possibilities_for_target(building_blocks: list[str], target: str, possibilities_dictionary: dict[str,int]) -> int:
    ''' this function uses sets in which each item is a tuple of the structure:
        (building_block, building_block, ..., rest of string)
    '''
    # print('TTARGET', target)
    if target == '': return 0
    if target in possibilities_dictionary:
        # print('FOUND')
        return possibilities_dictionary[target]
    # jelse:
    #     return 0

    # if target[-1] in possibilities_dictionary:
    #     return find_all_possibilities_for_target(building_blocks, target[:-1], possibilities_dictionary)


    possibilities = 0
    for pivot_index in range(1,len(target)):
        # print('SEQ', target[:pivot_index], target[pivot_index:])
        if pivot_index > 1 and target[pivot_index] in possibilities_dictionary:
            continue
        a = find_all_possibilities_for_target(building_blocks, target[:pivot_index], possibilities_dictionary)

        if a == 0:
            continue

        b = find_all_possibilities_for_target(building_blocks, target[pivot_index:], possibilities_dictionary)

        # print('tar', target)
        possibilities += a*b


    return possibilities

def count_possibilities(building_blocks: list[str], targets: list[str]) -> int:
    counter = 0
    for target in targets:
        counter += find_all_possibilities_for_target(building_blocks, target, possibilities_dictionary)
        break
    return counter

if __name__ == '__main__':
    # input_filename = 'z-19-01-input.txt'
    input_filename = 'z-19-02-actual-example.txt'
    building_blocks, targets = read_data(input_filename)
    possibilities_dictionary = make_possibilities_dictionary(building_blocks)
    print(possibilities_dictionary)
    # exit()
    # print(building_blocks)
    # print(build_from_blocks(building_blocks, 'brwrr'))
    # print(count_possibilities(building_blocks, targets))
    print(find_all_possibilities_for_target(building_blocks, 'w', possibilities_dictionary))
    print(find_all_possibilities_for_target(building_blocks, 'rr', possibilities_dictionary))
    print(find_all_possibilities_for_target(building_blocks, 'wr', possibilities_dictionary))
    print(find_all_possibilities_for_target(building_blocks, 'r', possibilities_dictionary))
    print('FINAL', find_all_possibilities_for_target(building_blocks, 'wrr', possibilities_dictionary))
    # print('FINAL', find_all_possibilities_for_target(building_blocks, 'rwrr', possibilities_dictionary))
    # print('FINAL', find_all_possibilities_for_target(building_blocks, 'rwrr', possibilities_dictionary))
    # print('FINAL', find_all_possibilities_for_target(building_blocks, 'rw', possibilities_dictionary))
    print('FINAL', find_all_possibilities_for_target(building_blocks, 'brwrr', possibilities_dictionary))
    for test in ['b', 'rwrr', 'br', 'wrr', 'brw', 'rr', 'brwr', 'r']:
        print(test, '====', find_all_possibilities_for_target(building_blocks, test, possibilities_dictionary))

