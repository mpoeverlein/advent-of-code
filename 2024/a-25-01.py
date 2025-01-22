def read_data(input_filename: str) -> list[list[tuple[int]],int]:
    with open(input_filename, 'r') as f:
        lines = ''.join(f.readlines())
    datasets = lines.split('\n\n')
    keys, locks = [], []
    for data in datasets:
        if data.startswith('.'):
            locks.append(translate(data))
        else:
            keys.append(translate(data))

    height = len(datasets[0].split('\n'))-2
    return keys, locks, height

def translate(data: str) -> tuple[int]:
    lines = data.split('\n')
    lines = [l for l in lines if l != '']
    Nx = len(lines[0])
    height_list = []
    for i in range(Nx):
        column = ''.join([line[i] for line in lines])
        height_list.append(column.count('#')-1) # subtract zero to follow convention of example
    return tuple(height_list)

def fit(key: tuple[int], lock: tuple[int], height: int) -> bool:
    return all([k+l <= height for k,l in zip(key, lock)])

def count_fits(keys: list[tuple[int]], locks: list[tuple[int]], height: int) -> int:
    counter = 0
    for key in keys:
        for lock in locks:
            if fit(key, lock, height):
                counter += 1
    return counter

if __name__ == '__main__':
    input_filename = 'z-25-01-input.txt'
    # input_filename = 'z-25-02-actual-example.txt'
    keys, locks, height = read_data(input_filename)
    print(height)
    print(keys, locks)
    print(count_fits(keys, locks, height))

