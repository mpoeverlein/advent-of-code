'''
Since the number of items in the list of stones grows exponentially in the worst case,
the stones are now represented by a dictionary (Stones().data) with
keys: the number on the stone
value: how many stones with this number are there

For every blink, blink() creates a new Stones() object based on the previous iteration.
This approach works because of the cyclical structures in the data, e.g.:
    0 -> 1 -> 2024 -> 20, 24 -> 2, **0**, 2, 4 -> 4096, **1**, 4096, 8192 -> ..., **2024**, ... ->
'''


class Stones:
    def __init__(self, data: dict[int, int]) -> None:
        '''
        Create Stones object with Stones.data stored.

        Parameters
        ----------
        data: dict[int,int]
          keys: all unique values of stones
          values: frequency of each unique value
        '''
        self.data = data

    def __repr__(self) -> str:
        return f'Stones object with stones: {self.data}'

    def __len__(self) -> int:
        return len(self.data)

    def add(self, stone: int, value: int) -> None:
        '''
        Add <value> number of stones to stone id with value <stone>.
        Parameters
        ----------
        stone: int
        value: int
        '''

        if stone in self.data:
            self.data[stone] += value
        else:
            self.data[stone] = value

    def sum(self) -> int:
        '''
        Total sum of all numbers of stones.

        Returns
        -------
        total: int
        '''
        total = 0
        for stone, value in self.data.items():
            total += value
        return total

def read_data(input_filename: str) -> Stones:
    '''
    Read data from input filename and create Stones object.

    Parameter
    ---------
    input_filename: str

    Returns
    -------
    stones: Stones
    '''
    with open(input_filename, 'r') as f:
        line = f.readline()
    stones = Stones(data={0: 0}) # initialize empty Stones object
    for stone in line.split():
        stones.add(int(stone), 1)

    return stones

def blink(stones: Stones) -> Stones:
    '''
    Apply blink rules:
      1. if stone value is 0, make stone value 1
      2. if number of digits in stone value is even, add two stones: one with first part of original stone value, the other with the second part
      3. otherwise, multiply stone value by 2024

    Due to the Stones object, the rules only have to be applied once for each possible stone value.

    Parameters
    ----------
    stones: Stones

    Returns
    -------
    new_stones: Stones
      Stones after blinking
    '''
    new_stones = Stones(data={0: 0})
    for stone, value in stones.data.items():
        N = len(str(stone))
        if stone == 0:
            new_stones.add(1, value)
        elif N % 2 == 0:
            first, second = int(str(stone)[:N//2]), int(str(stone)[N//2:])
            new_stones.add(first, value)
            new_stones.add(second, value)
        else:
            new_stones.add(2024*stone, value)

    return new_stones


if __name__ == '__main__':
    # input_filename = 'z-11-02-actual-example.txt'
    input_filename = 'z-11-01-input.txt'
    stones = read_data(input_filename)
    len_list = []
    for i in range(75): # blink 75 times
        stones = blink(stones)
        len_list.append(len(stones))

    print(f'Number of different stones: {len(stones)}')
    print(f'Number of stones after blinking 75 times: {stones.sum()}')
