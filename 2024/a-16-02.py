from helpers import Position, Field
PositionData = tuple[int]

north, east, south, west = '^', '>', 'v', '<'
directions = [north, east, south, west]
move_dictionary = {
        north: [west, north, east],
        east: [north, east, south],
        south: [east, south, west],
        west: [south, west, north]
        }

class Trajectory:
    def __init__(self, pos: Position, trajectory_string: str, cost: int) -> None:
        self.position = pos
        self.trajectory_string = trajectory_string
        self.cost = cost
        if len(trajectory_string) > 0:
            self.direction = trajectory_string[-1]
            self.points_visited = set([self.position.one_d_pos])
        else:
            self.direction = east
            self.points_visited = set([self.position.one_d_pos])

    def inherit_points_visited(self, previous) -> None:
        self.points_visited |= previous.points_visited

    def __repr__(self) -> str:
        return f'Trajectory to {self.position}, cost: {self.cost}, directions: {self.trajectory_string}'

    def __len__(self) -> int:
        return len(self.trajectory_string)

    def make_trajectory_to_points(self, start: Position) -> list[Position]:
        trajectory_points = [start]
        current = start
        for direction in self.trajectory_string:
            current_y, current_x = trajectory_points[-1].position_tuple
            match direction:
                case '^': dx = 0; dy = -1
                case '>': dx = 1; dy = 0
                case 'v': dx = 0; dy = 1
                case '<': dx = -1; dy = 0
            current_y, current_x = current_y+dy, current_x+dx
            trajectory_points.append(Position(current_y, current_x))

        return trajectory_points



class Maze(Field):
    def __init__(self, input_filename: str) -> None:
        with open(input_filename, 'r') as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]
        self.Ny, self.Nx = len(lines), len(lines[0])
        k = self.Ny + self.Nx
        n_rows = int(k * (k+1) / 2)
        self.barriers, self.free_fields, self.is_free = [], [], [True for i in range(n_rows)]
        for y, line in enumerate(lines):
            for x, s in enumerate(line):
                self.add_field(y,x,s)
        self.trajectory = []
        self.barriers_tuples = [a.position_tuple for a in self.barriers]
        self.barriers_one_d = [a.one_d_pos for a in self.barriers]
        self.free_one_d = [a.one_d_pos for a in self.free_fields]
        self.goal_cost = None

    def add_field(self, y: int, x: int, s: str) -> None:
        match s:
            case '#':
                barrier = Position(y,x)
                self.barriers.append(barrier)
                self.is_free[barrier.one_d_pos] = False
            case 'S':
                self.start = Position(y,x)
                self.free_fields.append(Position(y,x))
            case 'E':
                self.end = Position(y,x)
                self.free_fields.append(Position(y,x))
            case '.':
                self.free_fields.append(Position(y,x))

    def test_trajectory(self) -> None:
        self.trajectory.append(TrajectoryPoint(2,5,east))

    def make_move_tree(self, move_depth=100) -> None:
        trajectory_string = ''
        current = Trajectory(self.start, '', 0)
        goal_trajectories = []
        trajectories = []
        for direction in directions:
            new_position_data = self.validate_trajectory(current, direction)
            if new_position_data == (-1,-1):
                continue

            additional_cost = 1 if direction == current.direction else 1001
            new_trajectory = Trajectory(Position(*new_position_data), current.trajectory_string+direction, current.cost+additional_cost)
            new_trajectory.inherit_points_visited(current)
            # print(new_trajectory.points_visited)
            # exit()
            trajectories.append(new_trajectory)

        # TODO: somewhere in here should go an "inherit_points_visited"
        for i in range(1, move_depth):
            print(i, len(trajectories))
            this_round_trajectories = []
            for traj in trajectories:
                # print(traj)
                # print(traj.points_visited)
                if traj.position.data() == self.end.data():
                    goal_trajectories.append(traj)
                    print('FOUND ONE!!!')
                    continue
                new_moves = self.add_moves(traj)
                if len(new_moves) == 1 and new_moves[0] == traj:
                    continue
                for n in new_moves:
                    n.inherit_points_visited(traj)
                    this_round_trajectories.append(n)

            trajectories = this_round_trajectories[:]

            # this has to be modified for find all possible pathways of same minimum cost!
            # if i % 5 == 0:
            trajectories = self.clean_trajectories(trajectories)

        print('FINAL traj', goal_trajectories)
        self.trajectories = goal_trajectories

    def clean_trajectories(self, trajectories: list[Trajectory]) -> list[Trajectory]:
        new_traj_dict = {} # keys are: (pos_y, pos_x, direction)
        for traj in trajectories:
            if self.goal_cost:
                if traj.cost > self.goal_cost:
                    continue
            test_key = (traj.position.y, traj.position.x, traj.direction)
            if test_key in new_traj_dict:
                key_cost = new_traj_dict[test_key].cost
                if traj.cost < key_cost:
                    new_traj_dict[test_key] = traj
                elif traj.cost == key_cost:
                    # new_traj_dict[test_key].append(traj)
                    # print('INHERITED', new_traj_dict[test_key], traj)
                    # print('INHERITED', new_traj_dict[test_key].points_visited, traj.points_visited)
                    new_traj_dict[test_key].inherit_points_visited(traj)
                    # print('INHERITED', new_traj_dict[test_key].points_visited, traj.points_visited)


            else:
                new_traj_dict[test_key] = traj

        return list(new_traj_dict.values())
        # new_traj_list = []
        # for k,v in new_traj_dict.items():
        #     for item in v:
        #         new_traj_list.append(item)
        # return new_traj_list


    def find_finish_trajectories(self) -> None:
        trajectories = [t for t in self.trajectories if t.position.data() == self.end.data()]
        self.trajectories = trajectories

    def find_minimum_trajectory(self) -> Trajectory:
        print(self.trajectories)
        return min(self.trajectories, key=lambda t: t.cost)

    def find_all_trajectories_with_minimum_cost(self) -> None:
        # min_cost = min(self.trajectories, key=lambda t: t.cost)
        min_cost = min([t.cost for t in self.trajectories])
        print('MIN COST', min_cost)
        self.minimum_trajectories = [t for t in self.trajectories if t.cost == min_cost]
        print('MINIMUM TRAJ', self.minimum_trajectories)

    def how_many_seats_on_minimum_paths(self) -> int:
        return len(self.find_minimum_trajectory().points_visited)
        print("HELLL")
        seats = set()
        for trajectory in self.minimum_trajectories:
            seat_points = trajectory.make_trajectory_to_points(self.start)
            print('SEAT POINTS', seat_points)
            for point in seat_points:
                seats.add(point.one_d_pos)
        return len(seats)


    def add_moves(self, current: Trajectory) -> list[Trajectory]:
        current_direction = current.direction
        result = []
        for direction in move_dictionary[current_direction]:
            new_position_data = self.validate_trajectory(current, direction)
            if new_position_data == (-1,-1):
                continue

            additional_cost = 1 if direction == current_direction else 1001
            result.append(Trajectory(Position(*new_position_data), current.trajectory_string+direction, current.cost+additional_cost))

        if len(result) == 0:
            return [current]

        return result

    def validate_trajectory(self, current: Trajectory, direction: str) -> PositionData:
        if current.position == self.end:
            return (-1,-1)
        current_y, current_x = current.position.data()
        match direction:
            case '^': dx = 0; dy = -1
            case '>': dx = 1; dy = 0
            case 'v': dx = 0; dy = 1
            case '<': dx = -1; dy = 0
        current_y, current_x = current_y+dy, current_x+dx
        current_pos = Position(current_y, current_x)
        if self.in_bounds(current_pos) and self.is_free[current_pos.one_d_pos]:
            return (current_y, current_x)
        else:
            return (-1, -1)

    def __repr__(self) -> str:
        result = [['.' for x in range(self.Nx)] for y in range(self.Ny)]
        for b in self.barriers:
            result[b.y][b.x] = '#'
        result[self.start.y][self.start.x] = 'S'
        result[self.end.y][self.end.x] = 'E'
        for t in self.trajectory:
            result[t.y][t.x] = t.direction

        return '\n'.join([''.join(i) for i in result])

    def get_neighbors(self, position: Position) -> dict[str,Position]:
        y,x = position.y, position.x
        y_list, x_list = [y-1,y,y+1,y], [x,x+1,x,x-1]
        neighbors = {direction: Position(i,j) for direction,i,j in zip(directions,y_list,x_list)}
        validated = {n:v for n,v in neighbors.items() if self.in_bounds(v)}
        validated = {n:v for n,v in validated.items() if v not in self.barriers}
        return validated

    @staticmethod
    def get_rotation_cost(d1: str, d2: str, turn_cost: int=1000) -> int:
        i1, i2 = directions.index(d1), directions.index(d2)
        # print(d1, d2, turn_cost *  min(abs(i1-i2), abs((i1+2)%4 - (i2+2)%4)))
        return turn_cost *  min(abs(i1-i2), abs((i1+2)%4 - (i2+2)%4))

    def count_cost(self) -> dict[tuple[int], int]:
        ''' cost to move forward: 1, cost to turn left/right: 1000 '''
        cost_dictionary = {(self.start.y, self.start.x): 0}
        number_of_checks_dictionary = {(self.start.y, self.start.x): 11}
        start_tile = TrajectoryPoint(self.start.y, self.start.x, east)
        tiles_to_check = [] # this list contains 2-ples with first item TrajectoryPoint() of initial and
        # second item TrajectoryPoint() of where to go next
        for direction, neighbor in self.get_neighbors(start_tile.position).items():
            tiles_to_check.append((start_tile,
                                   TrajectoryPoint(neighbor.y, neighbor.x, direction)))
        while len(tiles_to_check) > 0:
            print(tiles_to_check)
            current, next_tile = tiles_to_check.pop()

            next_cost = cost_dictionary[current.position_tuple] + 1
            next_cost += self.get_rotation_cost(current.direction, next_tile.direction)
            if next_tile.position_tuple not in cost_dictionary:
                cost_dictionary[next_tile.position_tuple] = next_cost
            else:
                cost_dictionary[next_tile.position_tuple] = min(cost_dictionary[next_tile.position_tuple], next_cost)
            if next_tile.position_tuple not in number_of_checks_dictionary:
                number_of_checks_dictionary[next_tile.position_tuple] = 0

            number_of_checks_dictionary[next_tile.position_tuple] += 1

            for direction, neighbor in self.get_neighbors(next_tile.position).items():
                if neighbor.position_tuple not in number_of_checks_dictionary:
                    number_of_checks_dictionary[neighbor.position_tuple] = 0
                if number_of_checks_dictionary[neighbor.position_tuple] > 10: continue
                tiles_to_check.append((next_tile,
                                   TrajectoryPoint(neighbor.y, neighbor.x, direction)))

        return cost_dictionary





if __name__ == '__main__':
    # maze = Maze('z-16-02-actual-example.txt')
    # maze = Maze('z-16-03-another-example.txt')
    maze = Maze('z-16-01-input.txt')
    maze.goal_cost = 102504 # solution of the first part of the puzzle. all trajectories above this value can be discarded
    maze.make_move_tree(move_depth=620)
    # maze.make_move_tree(move_depth=70)
    maze.find_finish_trajectories()
    maze.find_all_trajectories_with_minimum_cost()
    print(maze.how_many_seats_on_minimum_paths())
    # 505 is too low
