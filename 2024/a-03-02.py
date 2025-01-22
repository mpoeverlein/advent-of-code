import importlib
day_03_01 = importlib.import_module('a-03-01')
from helpers import read_data_as_list_strings
def read_data() -> list[str]:
    with open('z-03-01-input.txt', 'r') as f:
        lines = f.readlines()

    return lines

def check_switch(test: str) -> tuple[int, str]:
    if test.startswith('do()'):
        return 1, test[4:]
    elif test.startswith("don't()"):
        return 2, test[7:]

    return 3, test

def get_sum_of_multiplications_with_do(data_string: str) -> int:
    '''
    Run check_pattern until whole string is checked.
    This time, the multiplication result is only added if the last "do()" is more recent than the last "dont()"

    Parameters
    ----------
    data_string: str
      The string for which to check for multiplications

    Returns
    -------
    total_sum: int
      The sum of all multiplications
    '''

    operation_enabled = True
    total_sum = 0
    while data_string != '':
        result, data_string = check_switch(data_string)
        if result == 1:
            operation_enabled = True
        elif result == 2:
            operation_enabled = False

        result, data_string = day_03_01.check_pattern(data_string)
        if operation_enabled:
            total_sum += result

    return total_sum

if __name__ == '__main__':
    input_filename = 'z-03-01-input.txt'
    lines = read_data_as_list_strings(input_filename)
    data_string = ''.join(lines)
    total_sum = get_sum_of_multiplications_with_do(data_string)
    print(f'The sum of all relevant multiplications is: {total_sum}.')


