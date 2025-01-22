from itertools import product

import importlib
day_07_01 = importlib.import_module('a-07-01')

def calculate(elements, operators):
    result = elements[0]
    for element, operator in zip(elements[1:], operators):
        if operator == '+':
            result = result + element
        elif operator == '*':
            result = result * element
        elif operator == '|':
            result = int( str(result) + str(element) )

    return result

def obtain_calibration_result(results: list[int], elements_list: list[list[int]]) -> int:
    '''
    Find out which equations are possible by testing all possible combinations of addition and multiplication and concatenation.
    Sum up the possible results.

    Parameters
    ----------
    result_list: list[int]
    element_list: list[list[int]]

    Returns
    -------
    calibration_result: int
    '''
    calibration_result = 0

    for result, elements in zip(results, elements_list):
        N = len(elements) - 1
        for operators in product('+*|', repeat=N):
            if result == calculate(elements, operators):
                calibration_result += result
                break

    return calibration_result


if __name__ == '__main__':
    f = 'z-07-01-input.txt'
    # f = 'z-07-02-actual-example.txt'
    results, elements_list = day_07_01.read_data(f)
    calibration_result = obtain_calibration_result(results, elements_list)
    print(f'The calibration result is {calibration_result}.')

