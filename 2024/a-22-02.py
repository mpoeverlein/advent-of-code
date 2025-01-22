def mix(a: int, b: int) -> int: return a ^ b

def prune(a: int, mod: int=16777216) -> int: return a % mod

def step_a(secret_number: int) -> int:
    return prune(mix(secret_number << 6, secret_number))

def step_b(secret_number: int) -> int:
    result = secret_number >> 5
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

def find_first_n_prices(numbers: list[int], final_step: int) -> dict[int,list[int]]:
    prices = {}
    for n in numbers:
        prices.update({n: [n%10]})
        secret_number = n
        for i in range(final_step):
            secret_number = next_secret_number(secret_number)
            prices[n].append(secret_number%10)
    return prices

def make_price_differences(prices: dict[int,list[int]]) -> dict[int,list[int]]:
    return {k: [b-a for a,b in zip(v,v[1:])] for k,v in prices.items()}

def make_quad_sequences_with_prices(price_differences: dict[int,list[int]], prices: dict[int,list[int]]) -> list[dict[tuple[int],int]]:
    sequences = []
    for number, pd in price_differences.items():
        price_list = prices[number]
        quad_sequence = {}
        for a,b,c,d, price in zip(pd,pd[1:],pd[2:],pd[3:], price_list[4:]):
            if (a,b,c,d) in quad_sequence: continue
            quad_sequence[(a,b,c,d)] = price

        sequences.append(quad_sequence)

    return sequences

def get_total_scores(quad_sequences: list[dict[tuple[int],int]]) -> dict[tuple[int],int]:
    scores = {}
    for sequence_dict in quad_sequences:
        for sequence, price in sequence_dict.items():
            if sequence in scores:
                scores[sequence] += price
            else:
                scores[sequence] = price

    return scores

        



if __name__ == '__main__':
    # input_filename = 'z-22-03-another-example.txt'
    # input_filename = 'z-22-02-actual-example.txt'
    input_filename = 'z-22-01-input.txt'
    numbers = read_data(input_filename)
    assert len(numbers) == len(set(numbers)), 'One or more numbers appear more than once! Approach will not work then'
    prices = find_first_n_prices(numbers, 2000)
    price_differences = make_price_differences(prices)
    quad_sequences = make_quad_sequences_with_prices(price_differences, prices)
    scores = get_total_scores(quad_sequences)
    scores = [[k,v] for k,v in scores.items()]
    scores.sort(key=lambda v: v[1])
    print(scores[-1])

