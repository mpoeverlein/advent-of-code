import importlib
day_22_01 = importlib.import_module('a-22-01')

def find_first_n_prices(numbers: list[int], final_step: int) -> dict[int,list[int]]:
    '''
    Calculate the first <final_step> prices by starting with the numbers <numbers>.

    Parameters
    ----------
    numbers: list[int]
      The list of starting secret numbers
    final_step: int
      How often to generate next secret number

    Returns
    -------
    prices: dict[int,list[int]]
      keys: the starting secret numbers
      values: the computed number of bananas
    '''
    prices = {}
    for n in numbers:
        prices.update({n: [n%10]})
        secret_number = n
        for i in range(final_step):
            secret_number = day_22_01.next_secret_number(secret_number)
            prices[n].append(secret_number%10)
    return prices

def make_price_differences(prices: dict[int,list[int]]) -> dict[int,list[int]]:
    '''
    Parameters
    ----------
    prices: dict[int,list[int]]
      keys: the starting secret numbers
      values: the computed number of bananas

    Returns
    -------
    price_difference: dict[int,list[int]]
      keys: the starting secret numbers
      values: the difference in subsequent number of bananas
    '''

    return {k: [b-a for a,b in zip(v,v[1:])] for k,v in prices.items()}

def make_quad_sequences_with_prices(price_differences: dict[int,list[int]], prices: dict[int,list[int]]) -> list[dict[tuple[int],int]]:
    '''
    Find out which 4-tuples of price differences generate which price.

    Parameters
    ----------
    prices: dict[int,list[int]]
      keys: the starting secret numbers
      values: the computed number of bananas

    price_difference: dict[int,list[int]]
      keys: the starting secret numbers
      values: the difference in subsequent number of bananas

    Returns
    -------
    sequences: list[dict[tuple[int],int]]
      each sequence has keys: 4-tuple of price difference and values: resulting price
    '''
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
    '''
    Merge all the sequence dictionaries into one total price dictionary

    Parameters
    ----------
    quad_sequences: list[dict[tuple[int],int]]

    Returns
    -------
    scores: dict[tuple[int],int]
    '''
    scores = {}
    for sequence_dict in quad_sequences:
        for sequence, price in sequence_dict.items():
            if sequence in scores:
                scores[sequence] += price
            else:
                scores[sequence] = price

    return scores

def find_highest_scoring_sequence(scores: dict[tuple[int],int]) -> int:
    scores = [[k,v] for k,v in scores.items()]
    scores.sort(key=lambda v: v[1])
    return scores[-1][1]

if __name__ == '__main__':
    # input_filename = 'z-22-03-another-example.txt'
    # input_filename = 'z-22-02-actual-example.txt'
    input_filename = 'z-22-01-input.txt'
    numbers = day_22_01.read_data(input_filename)
    assert len(numbers) == len(set(numbers)), 'One or more numbers appear more than once! Approach will not work then'
    prices = find_first_n_prices(numbers, 2000)
    price_differences = make_price_differences(prices)
    quad_sequences = make_quad_sequences_with_prices(price_differences, prices)
    scores = get_total_scores(quad_sequences)
    high_score = find_highest_scoring_sequence(scores)
    print(f'The highest score is {high_score}.')

