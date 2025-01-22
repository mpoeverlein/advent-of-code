from helpers import read_data_as_list_strings

def check_pattern(test: str) -> tuple[int, str]:
    '''
    Parameters
    ----------
    test: str
      The string for which to check for multiplications

    Returns
    -------
    multiplication_result: int
      0 if no multiplication, otherwise a*b for mul(a,b)

    new_test: str
      string for which to repeat check_pattern()

    '''
    if not test.startswith('mul('):
        return 0, test[1:]

    test = test[4:] # removes mul(

    first_number_string = test.split(',')[0]
    try:
        first_number = int(first_number_string)
    except ValueError:
        return 0, test

    test = test[1+len(first_number_string):] # remove number

    second_number_string = test.split(')')[0]
    try:
        second_number = int(second_number_string)
    except ValueError:
        return 0, test

    multiplication_result = first_number * second_number
    new_test = test[len(second_number_string)+1:]
    return multiplication_result, new_test

def get_sum_of_multiplications(data_string: str) -> int:
    '''
    Run check_pattern until whole string is checked.

    Parameters
    ----------
    data_string: str
      The string for which to check for multiplications

    Returns
    -------
    total_sum: int
      The sum of all multiplications
    '''

    total_sum = 0
    while data_string != '':
        result, data_string = check_pattern(data_string)
        total_sum += result
    return total_sum

if __name__ == '__main__':
    input_filename = 'z-03-01-input.txt'
    lines = read_data_as_list_strings(input_filename)
    data_string = ''.join(lines)
    total_sum = get_sum_of_multiplications(data_string)
    print(f'The sum of all multiplications is: {total_sum}.')


