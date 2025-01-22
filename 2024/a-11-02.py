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
        self.data = data
    def __repr__(self) -> str:
        return f'Stones object with stones: {self.data}'
    def __len__(self) -> int:
        return len(self.data)

    def add(self, stone: int, value: int) -> None:
        if stone in self.data:
            self.data[stone] += value
        else:
            self.data[stone] = value

    def sum(self) -> int:
        total = 0
        for stone, value in self.data.items():
            total += value
        return total

def read_data(input_filename: str) -> Stones:
    with open(input_filename, 'r') as f:
        line = f.readline()
    stones = Stones(data={0: 0}) # initialize empty Stones object
    for stone in line.split():
        stones.add(int(stone), 1)

    return stones

def blink(stones: Stones) -> Stones:
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
    print(stones)
    len_list = []
    for i in range(75): # blink 75 times
        stones = blink(stones)
        # print(i, len(stones), stones)
        len_list.append(len(stones))

    print(f'Number of different stones: {len(stones)}')
    print(f'Number of stones after blinking 75 times: {stones.sum()}')
