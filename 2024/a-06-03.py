from copy import deepcopy

Field = list[list[str]]
Trajectory = list[tuple[int,str]]
empty, blockade = '.', '#'

def my_find(lst, item):
    try:
        return lst.index(item)
    except ValueError:
        return -1

class directions:
    N, E, S, W = '^', '>', 'v', '<'
    directions = [N, E, S, W]

def read_data(filename) -> Field:
    with open(filename, 'r') as f:
        lines = f.read()

    return [[s for s in line] for line in lines.split('\n')][:-1] # last one is empty list

def print_field(field: Field) -> str:
    print('HELLO')
    result = '\n'.join([''.join([symbol for symbol in yline]) for yline in field])
    print(80*'*')
    print(result)
    print(80*'*')
    return result

def get_guard_state(field: Field) -> tuple[int,str]:
    for y, yline in enumerate(field):
        for x, symbol in enumerate(yline):
            if symbol in directions.directions:
                return y, x, symbol
    return -1, -1, '' # no guard


def get_new_direction(direction: str, in_front: str):
    if in_front == empty:
        return direction
    current_index = directions.directions.index(direction)
    return directions.directions[(current_index+1) % len(directions.directions)]

def propagate_field(field: Field) -> list[Field,Trajectory]:
    # find guard
    y, x, direction = get_guard_state(field)
    partial_trajectory = []
    new_y, new_x = y,x
    field[y][x] = empty
    match direction:
        case directions.N:
            ray = [field[i][x] for i in range(y-1,-1,-1)]
            dy = my_find(ray,'#')
            if dy == -1:
                return field, [(i,x,direction) for i in range(y-1,-1,-1)]
            new_y, new_x = y-dy, x
            for i in range(y-1,new_y-1,-1):
                # print(i)
                # print('LAST FIELD IN TRAJ')
                # print(field[i][x])
                partial_trajectory.append((i,x,direction))

        case directions.E:
            ray = [field[y][i] for i in range(x+1,len(field[y]),1)]
            dx = my_find(ray,'#')
            if dx == -1:
                return field, [(y,i,direction) for i in range(x+1,len(field[y]),1)]
            new_y, new_x = y, x+dx
            for i in range(x+1,new_x+1,1):
                partial_trajectory.append((y,i,direction))

        case directions.S:
            ray = [field[i][x] for i in range(y+1,len(field),1)]
            dy = my_find(ray,'#')
            if dy == -1:
                return field, [(i,x,direction) for i in range(y+1,len(field),1)]
            new_y, new_x = y+dy, x
            for i in range(y+1,new_y+1,1):
                partial_trajectory.append((i,x,direction))

        case directions.W:
            ray = [field[y][i] for i in range(x-1,-1,-1)]
            dx = my_find(ray,'#')
            if dx == -1:
                return field, [(y,i,direction) for i in range(x-1,-1,-1)]
            new_y, new_x = y, x-dx
            for i in range(x-1,new_x-1,-1):
                partial_trajectory.append((y,i,direction))

    field[new_y][new_x] = direction
    # print(field, partial_trajectory)
    return [field, partial_trajectory]

def make_trajectory(field: Field) -> Trajectory:
    print_field(field)
    y, x, symbol = get_guard_state(field)
    guard_trajectory = [(y,x,symbol)]
    while True:
        field, partial_trajectory = propagate_field(field)
        print_field(field)
        y, x, symbol = get_guard_state(field)
        for item in partial_trajectory:
            print(item)
            guard_trajectory.append(item)
        if symbol == '': break
        # guard_trajectory.append((y,x,symbol))
        # marched, now turn
        field[y][x] = get_new_direction(symbol, '#')


    return guard_trajectory

def add_trajectory_to_field(field: Field, trajectory: Trajectory) -> Field:
    for y,x,symbol in trajectory:
        field[y][x] = symbol
    return field

def count_trajectory_length(field_with_X: Field):
    result = print_field(field_with_X)
    return result.count('X')

def get_unique_positions(guard_trajectory: Trajectory) -> Trajectory:
    return set(p for p in guard_trajectory)

def find_all_possible_obstacles(original_field: Field, guard_trajectory: Trajectory) -> int:
    '''
    for every field visited by the guard, we test if we can trap the guard by placing
    an obstacle on this field
    '''
    initial_y, initial_x, initial_symbol = get_guard_state(original_field)
    count_obstacles = 0
    print(guard_trajectory[:2])
    unique_guard_positions = []
    for (y,x,symbol) in guard_trajectory:
        if (y,x) not in unique_guard_positions:
            unique_guard_positions.append((y,x))
    for (test_y,test_x) in unique_guard_positions:
        test_field = deepcopy(original_field)
        test_field[test_y][test_x] = '#'

        if (test_y,test_x) == guard_trajectory[0][:2]:
            (initial_y, initial_x, initial_symbol) = guard_trajectory[1]
            test_field[initial_y][initial_x] = initial_symbol
        test_trajectory = [(initial_y, initial_x, initial_symbol)]
        print('##### TEST #####')
        print(test_y,test_x)
        in_a_loop = False
        while True:
            test_field, partial_trajectory = propagate_field(test_field)
            y, x, symbol = get_guard_state(test_field)
            for item in partial_trajectory:
                if item in test_trajectory[1:]:
                    count_obstacles += 1
                    test_field[test_y][test_x] = 'O'
                    print_field(test_field)
                    in_a_loop = True
                    break

                test_trajectory.append(item)
            if symbol == '':
                break

            test_field[y][x] = get_new_direction(symbol, '#')
            # print_field(test_field)
            if in_a_loop:
                break

    return count_obstacles

# input_filename = 'z-06-02-actual-example.txt'
input_filename = 'z-06-01-input.txt'
field = read_data(input_filename)
original_field = deepcopy(field)
print_field(field)
# print_field(propagate_field(field))
guard_trajectory = make_trajectory(field)
print(guard_trajectory)
field = add_trajectory_to_field(field, guard_trajectory)
print_field(field)
print('ORIGINAL FIELD')
print_field(original_field)
# exit()
# print(count_trajectory_length(field))
print(find_all_possible_obstacles(original_field, guard_trajectory))
