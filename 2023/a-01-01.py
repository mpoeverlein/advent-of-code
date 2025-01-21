def get_first_digit(line):
    for char in line:
        if char.isdigit():
            return int(char)


with open('z-01-01-input.txt', 'r') as f:
    lines = f.readlines()

calibration_number = 0
for line in lines:
    a = get_first_digit(line)
    b = get_first_digit(line[::-1])
    calibration_number += 10*a + b

print(f'The solution is: {calibration_number}')
