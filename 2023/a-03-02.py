with open('z-03-01-input.txt', 'r') as f:
    lines = f.readlines()

def is_gear(char):
    return char == '*'

def get_gear_coordinates(lines):
    gear_coordinates = []
    for row, line in enumerate(lines):
        line = line.rstrip()
        for col, char in enumerate(line):
            if is_gear(char):
                gear_coordinates.append([row, col])
    return gear_coordinates

def get_adjacent_coordinates(row, col):
    c_list = []
    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            c_list.append([i,j])
    c_list.remove([row, col])
    return c_list

def make_allowed_list(lines, symbol_coordinates):
    n_rows = range(len(lines))
    n_cols = range(len(lines[0].rstrip()))
    allowed_list = [[False for i in n_cols]
                    for j in n_rows]
    for row, col in symbol_coordinates:
        index_list = get_adjacent_coordinates(row, col)
        for row, col in index_list:
            allowed_list[row][col] = True
    return allowed_list

def get_number(coord_list, lines):
    s = ''
    for row, col in coord_list:
        s += lines[row][col]
    return int(s)

def get_allowed_number(coord_list, allowed_list, lines):
    for row, col in coord_list:
        if allowed_list[row][col]:
            return get_number(coord_list, lines)
    return 0

def get_new_number_length(s):
    number_string = ''
    for char in s:
        if char.isdigit():
            number_string += char
        else:
            break
    return len(number_string)

def get_number_coordinates(lines):
    coordinates = []
    for line_index, line in enumerate(lines):
        line = line.rstrip()
        char_index = 0
        while char_index < len(line):
            char = line[char_index]
            if not char.isdigit():
                char_index += 1
                continue
            number_length = get_new_number_length(line[char_index:])
            this_coordinate = []
            for i in range(number_length):
                this_coordinate.append([line_index, char_index+i])
            coordinates.append(this_coordinate)
            char_index += number_length
    return coordinates

def find_surrounding_numbers(gear, number_coordinates, lines):
    row_gear, col_gear = gear
    number_list = []
    for coord in number_coordinates:
        for row, col in coord:
            if abs(row-row_gear) < 2 and abs(col-col_gear) < 2:
                number_list.append(get_number(coord, lines))
                break
    if len(number_list) == 2:
        return number_list[0] * number_list[1]
    return 0


gear_coordinates = get_gear_coordinates(lines)
number_coordinates = get_number_coordinates(lines)
counter = 0
for gear in gear_coordinates:
    counter += find_surrounding_numbers(gear, number_coordinates, lines)

print(f'The solution is: {counter}')
