def read_data(f) -> list[list[int],list[list[int]]]:
    with open(f, 'r') as ff:
        lines = ff.readlines()
    result_list, element_list = [], []
    for line in lines:
        result, elements = line.split(':')
        result_list.append(int(result))
        element_list.append([int(i) for i in elements.split()])

    return [result_list, element_list]

def calculate(elements, operators):
    result = elements[0]
    for element, operator in zip(elements[1:], operators):
        if operator == '+':
            result = result + element
        elif operator == '*':
            result = result * element

    return result

# def turn_binary_number_to_operator_string(decimal_number):
#     return f'{decimal_number:

f = 'z-07-01-input.txt'
# f = 'z-07-02-actual-example.txt'
results, elements_list = read_data(f)
print(results)

calibration_result = 0

for result, elements in zip(results, elements_list):
    N = len(elements) - 1
    for i in range(2**N):
        operators = f'{i:b}'.zfill(N).replace('0','+').replace('1','*')
        if result == calculate(elements, operators):
            calibration_result += result
            break

print(calibration_result)

