#!/usr/bin/env python3

def read_data(input_filename: str) -> list[list[str]]:
    '''
    Read in data from input file and return as two lists: the building_blocks and the target sequences.

    Parameters
    ----------
    input_filename: str

    Returns
    -------
    building_blocks: list[str]
      e.g. br,gb,ubw, etc.
    targets: list[str]
      e.g. bwrgbr,ubwbeg,etc.
    '''
    with open(input_filename, 'r') as f:
        content = ''.join(f.readlines())

    building_blocks, targets = content.split('\n\n')
    building_blocks = building_blocks.split(', ')
    targets = targets.split('\n')

    return building_blocks, targets

def can_be_built(building_blocks: list[str], target: str) -> bool:
    '''
    Check if target sequence can be built from building blocks.

    Parameters
    ----------
    building_blocks: list[str]
      e.g. br,gb,ubw, etc.
    target: str
      e.g. bwrgbr

    Returns
    -------
    is_built: bool
    '''

    test_sequences = {target}
    while len(test_sequences) > 0:
        test_sequence = test_sequences.pop()
        if test_sequence in building_blocks:
            return True
        for building_block in building_blocks:
            if test_sequence.startswith(building_block):
                test_sequences.add(test_sequence[len(building_block):])

    return False

def count_possible(building_blocks: list[str], targets: list[str]) -> int:
    '''
    How many target sequences can be built?

    Parameters
    ----------
    building_blocks: list[str]
      e.g. br,gb,ubw, etc.
    targets: list[str]
      e.g. bwrgbr,ubwbeg,etc.

    Returns
    -------
    n_buildable: int
    '''

    return len([target for target in targets if can_be_built(building_blocks, target)])

if __name__ == '__main__':
    input_filename = 'z-19-01-input.txt'
    # input_filename = 'z-19-02-actual-example.txt'
    building_blocks, targets = read_data(input_filename)
    n_possible = count_possible(building_blocks, targets)
    print(f'{n_possible} designs are possible.')
