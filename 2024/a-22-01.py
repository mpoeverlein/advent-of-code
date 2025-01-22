def mix(a: int, b: int) -> int: return a ^ b

def prune(a: int, mod: int=16777216) -> int: return a % mod

def step_a(secret_number: int) -> int:
    return prune(mix(secret_number * 64, secret_number))

def step_b(secret_number: int) -> int:
    result = int(secret_number / 32)
    secret_number = mix(secret_number, result)
    return prune(secret_number)

def step_c(secret_number: int) -> int:
    secret_number = mix(secret_number * 2048, secret_number)
    return prune(secret_number)

def next_secret_number(secret_number: int) -> int:
    return step_c(step_b(step_a(secret_number)))

def read_data(input_filename: str) -> list[int]:
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    return [int(line) for line in lines]

if __name__ == '__main__':
    input_filename = 'z-22-01-input.txt'
    numbers = read_data(input_filename)
    # numbers = [1, 10, 100, 2024,]
    result = []
    for n in numbers:
        secret_number = n
        for i in range(2000):
            secret_number = next_secret_number(secret_number)
        print(n, secret_number)
        result.append(secret_number)

    print(sum(result))

