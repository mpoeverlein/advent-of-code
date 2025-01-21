with open('z-02-01-input.txt', 'r') as f:
    lines = f.readlines()

def get_max(line, color):
    line = line.split(':')[1]
    draw_list = []
    for draw in line.split(';'):
        for cubes in draw.split(','):
            if color in cubes:
                draw_list.append(int(cubes.split()[0]))

    return max(draw_list)

def get_game_id(line, r, g, b):
    game_id = int(line.split(':')[0].split()[-1])
    if (get_max(line, 'red') > r) or \
       (get_max(line, 'green') > g) or \
       (get_max(line, 'blue') > b):
           return 0

    return game_id

counter = 0
for line in lines:
    counter += get_game_id(line, 12, 13, 14)

print(f'The solution is: {counter}')
