'''
Although the number of items grows exponentially in the worst case, the following simple approach works for 25 repetitions.
'''

def read_data(input_filename: str) -> list[int]:
    '''
    Read data from input file.

    Parameters
    ----------
    input_filename: str
      Name of the input file from which to read data

    Returns
    -------
    numbers_list: list[int]
    '''
    with open(input_filename, 'r') as f:
        line = f.readline()
    return [int(s) for s in line.split()]

def blink(stones: list[int]) -> list[int]:
    '''
    Apply blink rules:
      1. if stone value is 0, make stone value 1
      2. if number of digits in stone value is even, add two stones: one with first part of original stone value, the other with the second part
      3. otherwise, multiply stone value by 2024

    Parameters
    ----------
    stones: list[int]

    Returns
    -------
    new_stones: list[int]
      Stones list after blinking
    '''

    new_stones = []
    for stone in stones:
        N = len(str(stone))
        if stone == 0:
            new_stones.append(1)
        elif N % 2 == 0:
            new_stones.append(int( str(stone)[:N//2] ))
            new_stones.append(int( str(stone)[N//2:] ))
        else:
            new_stones.append(2024*stone)

    return new_stones


if __name__ == '__main__':
    input_filename = 'z-11-02-actual-example.txt'
    input_filename = 'z-11-01-input.txt'
    stones = read_data(input_filename)
    for _ in range(25):
        stones = blink(stones)

    print(f'After 25 blinks, there are {len(stones)} stones.')
