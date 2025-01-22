#!/usr/bin/env python3

def read_data(input_filename: str) -> list[list[str]]:
    with open(input_filename, 'r') as f:
        content = ''.join(f.readlines())

    building_blocks, target = content.split('\n\n')
    building_blocks = building_blocks.split(', ')
    target = target.split('\n')

    return building_blocks, target

def build_from_blocks(building_blocks: list[str], target: str) -> bool:
    test_sequences = {target}
    while len(test_sequences) > 0:
        # print('test_sequence', test_sequences)
        test_sequence = test_sequences.pop()
        # print('test_sequence', test_sequence)
        if test_sequence in building_blocks:
            return True
        for building_block in building_blocks:
            if test_sequence.startswith(building_block):
                # print(building_block, test_sequence)
                test_sequences.add(test_sequence[len(building_block):])

    return False

def count_possible(building_blocks: list[str], targets: list[str]) -> int:
    counter = 0
    for target in targets:
        if build_from_blocks(building_blocks, target):
            counter += 1
    return counter

if __name__ == '__main__':
    input_filename = 'z-19-01-input.txt'
    # input_filename = 'z-19-02-actual-example.txt'
    building_blocks, targets = read_data(input_filename)
    print(building_blocks)
    # print(build_from_blocks(building_blocks, 'brwrr'))
    print(count_possible(building_blocks, targets))
