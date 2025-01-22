def read_data(input_filename: str) -> list[list[int],list[list[int]]]:
    '''
    Read data from <input_filename> to result_list and element_list.

    Parameters
    ----------
    input_filename: str

    Returns
    -------
    result_list: list[int]
    element_list: list[list[int]]
    '''
    with open(input_filename, 'r') as ff:
        lines = ff.readlines()
    result_list, element_list = [], []
    for line in lines:
        result, elements = line.split(':')
        result_list.append(int(result))
        element_list.append([int(i) for i in elements.split()])

    return [result_list, element_list]

def calculate(elements: list[int], operators: str) -> int:
    '''
    Calculate result of elements with mathematical operators given in operators variable.
    Parameters
    ----------
    elements: list[int]
    operators: str, consists of '+' and '*'

    Returns
    -------
    result: int
    '''

    result = elements[0]
    for element, operator in zip(elements[1:], operators):
        if operator == '+':
            result = result + element
        elif operator == '*':
            result = result * element

    return result

def obtain_calibration_result(results: list[int], elements_list: list[list[int]]) -> int:
    '''
    Find out which equations are possible by testing all possible combinations of addition and multiplication.
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
        for i in range(2**N):
            # create list of all possible combinations of + and *
            operators = f'{i:b}'.zfill(N).replace('0','+').replace('1','*')
            if result == calculate(elements, operators):
                calibration_result += result
                break

    return calibration_result

if __name__ == '__main__':
    f = 'z-07-01-input.txt'
    # f = 'z-07-02-actual-example.txt'
    results, elements_list = read_data(f)
    calibration_result = obtain_calibration_result(results, elements_list)
    print(f'The calibration result is {calibration_result}.')


