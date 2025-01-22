from copy import deepcopy
'''
This implementation is faster since we instantly teleport the guard to the next position.
It is still quite slow, though.
'''

import importlib
day_06_01 = importlib.import_module('a-06-01')

FieldData = list[list[str]]
Trajectory = list[tuple[int,str]]
empty, blockade = '.', '#'

def next_tiles_in_front_of_guard(field: FieldData, y: int, x: int, direction: str) -> tuple[int,str]:
    match direction:
        case '^': return [(yi, x, field[yi][x]) for yi in range(y-1,-1,-1)]
        case '>': return [(y, xi, field[y][xi]) for xi in range(x+1,len(field[0]))]
        case 'v': return [(yi, x, field[yi][x]) for yi in range(y+1,len(field))]
        case '<': return [(y, xi, field[y][xi]) for xi in range(x-1,-1,-1)]

def propagate_field(field: FieldData) -> FieldData:
    ''' Advance field state by as many steps as possible

    Parameters
    ----------
    field: FieldData

    Returns
    -------
    field: FieldData
    '''
    y, x, direction = day_06_01.get_guard_state(field)
    next_tiles = next_tiles_in_front_of_guard(field, y, x, direction)
    next_tiles_symbols = [item[2] for item in next_tiles]
    if blockade == next_tiles_symbols[0]:
        field[y][x] = day_06_01.get_new_direction(direction, blockade)
        return field, [(y,x,direction)]
    if blockade in next_tiles_symbols:
        block_index = next_tiles_symbols.index(blockade)
        new_y, new_x = next_tiles[block_index-1][:2]
        field[y][x] = empty
        field[new_y][new_x] = day_06_01.get_new_direction(direction, blockade)
        return field, [(y,x,direction)] + [(yi,xi,direction) for yi,xi,symbol in next_tiles[:block_index-1]]
    else:
        field[y][x] = empty
        return field, [(y,x,direction)] + [(yi,xi,direction) for yi,xi,symbol in next_tiles]

def make_trajectory(field: FieldData, debug: bool=False) -> Trajectory:
    '''
    Propagate state of field until guard is gone

    Parameters
    ----------
    field: FieldData
    debug: bool

    Returns
    -------
    guard_trajectory: Trajectory
    '''

    y, x, symbol = day_06_01.get_guard_state(field)
    guard_trajectory = [(y,x,symbol)]
    while True:
        if debug:
            print('Next step started.')
        field, new_trajectory_points = propagate_field(field)
        for trajectory_point in new_trajectory_points:
            guard_trajectory.append(trajectory_point)
        y, x, symbol = day_06_01.get_guard_state(field)
        if symbol == '': break
        guard_trajectory.append((y,x,symbol))

    return guard_trajectory

def find_all_possible_obstacles(original_field: FieldData, guard_trajectory: Trajectory) -> int:
    '''
    for every field visited by the guard, we test if we can trap the guard by placing
    an obstacle on this field

    Parameters
    ----------
    original_field: FieldData
    guard_trajectory: Trajectory
      original trajectory of guard

    Returns
    -------
    int
    '''
    actual_field = deepcopy(original_field)
    initial_y, initial_x, initial_symbol = day_06_01.get_guard_state(actual_field)
    count_obstacles = 0
    unique_guard_positions = []
    for (y,x,symbol) in guard_trajectory:
        if (y,x) not in unique_guard_positions:
            unique_guard_positions.append((y,x))
    for c, (test_y,test_x) in enumerate(unique_guard_positions):
        print(f'Test next position ({test_y,test_x}). Check no. {c} of {len(unique_guard_positions)}.')
        test_field = deepcopy(original_field)
        test_field[test_y][test_x] = '#'

        if (test_y,test_x) == guard_trajectory[0][:2]: # if test tile is where guard starts
            (initial_y, initial_x, initial_symbol) = guard_trajectory[1]
            test_field[initial_y][initial_x] = initial_symbol
        test_trajectory = [(initial_y, initial_x, initial_symbol)]
        while True:
            test_field, test_trajectory_part = propagate_field(test_field)
            y, x, symbol = day_06_01.get_guard_state(test_field)
            if symbol == '':
                break
            if (y,x,symbol) in test_trajectory[1:]: # we're in a loop!
                count_obstacles += 1
                test_field[test_y][test_x] = 'O'
                break

            for trajectory_part in test_trajectory_part:
                test_trajectory.append(trajectory_part)

    return count_obstacles

if __name__ == '__main__':
    input_filename = 'z-06-01-input.txt'
    field = day_06_01.read_data_as_list_list(input_filename, datatype=str, separator='None')
    field = [[s for s in line if s != '\n'] for line in field]
    original_field = deepcopy(field)
    guard_trajectory = make_trajectory(field)
    n_obstacles = find_all_possible_obstacles(original_field, guard_trajectory)
    print(f'There are {n_obstacles} possible unique positions to place obstacles that trap the guard in a circle.')
