def read_data(input_filename: str) -> list[int]:
    with open(input_filename, 'r') as f:
        line = f.readline()
    return [int(s) for s in line.split()]

def blink(stones: list[int]) -> list[int]:
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
    print(stones)
    for _ in range(25):
        stones = blink(stones)

    print(len(stones))
