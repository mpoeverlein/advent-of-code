digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', '1', '2', '3', '4', '5', '6', '7', '8', '9']
digit_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]
digit_dict = {k: v for k,v in zip(digits, digit_list)}

def get_first_digit(line):
    for i, char in enumerate(line):
        for digit in digits:
            if line[i:i+len(digit)] == digit:
                return digit_dict[digit]

def get_last_digit(line):
    for i in range(len(line), -1, -1):
        for digit in digits:
            if line[i:i+len(digit)] == digit:
                return digit_dict[digit]

with open('z-01-01-input.txt', 'r') as f:
    lines = f.readlines()

calibration_number = 0
for line in lines:
    a = get_first_digit(line)
    b = get_last_digit(line)
    calibration_number += 10*a + b

print(f'The solution is: {calibration_number}')
