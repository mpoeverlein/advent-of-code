'''
This implementation is quite slow because it works on the string representation of the field.
But it works!
'''

from helpers import read_data_as_list_list

FieldData = list[list[str]]
Trajectory = list[tuple[int]]
empty, blockade = '.', '#'
movement_dictionary = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
rotation_dictionary = {'^': '>', '>': 'v', 'v': '<', '<': '^'}


def print_field(field: FieldData) -> str:
    '''
    Prints data of <field> in between '*****' and returns this output as a string

    Parameters
    ----------
    field: FieldData

    Returns
    -------
    result: str
    '''
    result = '\n'.join([''.join([symbol for symbol in yline]) for yline in field])
    print(80*'*')
    print(result)
    print(80*'*')
    return result

def get_guard_state(field: FieldData) -> tuple[int,str]:
    '''
    Find guard and in which direction it is looking.
    If no guard, returns -1, -1, ''

    Parameters
    ----------
    field: FieldData

    Returns
    -------
    y: int
      y coordinate on field where guard is
    x: int
      x coordinate on field where guard is
    symbol: str
      direction of guard
    '''
    for y, yline in enumerate(field):
        for x, symbol in enumerate(yline):
            if symbol in movement_dictionary:
                return y, x, symbol
    return -1, -1, '' # no guard

def position_in_front_of_guard(field: FieldData, y: int, x: int, direction: str) -> list[str]:
    '''
    Parameters
    ----------
    field: FieldData
    y: int
    x: int
    direction: str

    Returns
    -------
    front_y: int
      y coordinate in front of guard
    front_x: int
      x coordinate in front of guard
    '''
    dy, dx = movement_dictionary[direction]
    return [y+dy, x+dx]

def get_new_direction(direction: str, in_front: str):
    '''
    Parameters
    ----------
    direction: str
      Where guard is currently looking
    in_front: str
      Which tile is in front of guard, i.e. empty or barrier

    Returns
    -------
    new_direction: str
      Where guard should be looking
    '''

    if in_front == empty:
        return direction
    return rotation_dictionary[direction]

def propagate_field(field: FieldData) -> FieldData:
    '''
    Advance field state by one step
    1. find guard and where it is looking
    2. bring guard to next tile
    3. finish if guard is free

    Parameters
    ----------
    field: FieldData

    Returns
    -------
    field: FieldData
    '''
    y, x, direction = get_guard_state(field)
    if direction == '':
        return field
    ys, xs = position_in_front_of_guard(field, y, x, direction)
    try:
        in_front = field[ys][xs]
    except IndexError:
        in_front = empty

    direction = get_new_direction(direction, in_front)
    new_y, new_x = position_in_front_of_guard(field, y, x, direction)

    field[y][x] = empty
    try:
        field[new_y][new_x] = direction
    except IndexError:
        pass

    return field

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

    y, x, symbol = get_guard_state(field)
    guard_trajectory = [(x,y)]
    while True:
        if debug:
            print('Next step started.')
        field = propagate_field(field)
        y, x, symbol = get_guard_state(field)
        if symbol == '': break
        guard_trajectory.append((x,y))

    return guard_trajectory

def add_trajectory_to_field(field: FieldData, trajectory: Trajectory) -> FieldData:
    '''
    Mark where guard has visited in field data

    Parameters
    ----------
    field: FieldData
    trajectory: Trajectory

    Returns
    -------
    field: FieldData
    '''
    for x,y in trajectory:
        field[y][x] = 'X'
    return field

def count_trajectory_length(field_with_X: FieldData) -> int:
    '''
    Count how many unique tiles were visited by guard
    Parameters
    ----------
    field_with_X: FieldData
      In this field, every spot the guard visited is marked by 'X'

    Returns
    -------
    int
    '''
    result = '\n'.join([''.join([symbol for symbol in yline]) for yline in field_with_X])
    return result.count('X')

if __name__ == '__main__':
    input_filename = 'z-06-01-input.txt'
    field = read_data_as_list_list(input_filename, datatype=str, separator='None')
    guard_trajectory = make_trajectory(field)
    field = add_trajectory_to_field(field, guard_trajectory)
    trajectory_length = count_trajectory_length(field)
    print(f'The guard visits {trajectory_length} distinct positions.')
