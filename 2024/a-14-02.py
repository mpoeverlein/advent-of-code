'''
when do the robots arrange to a christmas tree?
this script prints the robot configuration at every time step and we will
visually find the answer
'''

import importlib
day_14_01 = importlib.import_module('a-14-01')
Robot = day_14_01.Robot

def make_field_string(robots: list[Robot], dim_x: int, dim_y: int) -> str:
    empty = [[' ' for i in range(dim_x)] for y in range(dim_y)]
    for robot in robots:
        x,y = robot.p
        empty[y][x] = 'O'
    return '\n'.join([''.join(s) for s in empty])

if __name__ == '__main__':
    # input_filename = 'z-14-02-actual-example.txt'
    input_filename = 'z-14-01-input.txt'
    robots = day_14_01.read_data(input_filename)
    time_steps, dim_x, dim_y = 100, 101, 103
    # find christmas tree by visual inspection
    for i in range(1,18_251): # 18,251 is where I found the pattern by visual inspection
        for robot in robots:
            robot.propagate(1, dim_x, dim_y)
        print(i)
        field_string = make_field_string(robots, dim_x, dim_y)
        if 'OOOOOOOOO' in field_string:
            print(field_string)
            break

    print(f'The christmas tree first appears after {i} steps.')

