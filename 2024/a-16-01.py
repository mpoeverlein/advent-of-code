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
    '''
    The Trajectory object stores a goal position, the cost to get there, and a representation of the trajectory using arrows.
    '''

    def __init__(self, pos: Position, trajectory_string: str, cost: int) -> None:
        '''
        Parameters
        ----------
        pos: Position
          goal position
        trajectory_string: str
          consists of ^>v<
        cost: int
          the cost of the trajectory
        '''
        self.position = pos
        self.trajectory_string = trajectory_string
        self.cost = cost
        if len(trajectory_string) > 0:
            self.direction = trajectory_string[-1]
        else:
            self.direction = east

    def __repr__(self) -> str:
        return f'Trajectory to {self.position}, cost: {self.cost}, directions: {self.trajectory_string}'

    def __len__(self) -> int:
        return len(self.trajectory_string)

class Maze(Field):
    '''
    Maze object stores information of where Start, End, and barriers are.
    '''
    def __init__(self, input_filename: str) -> None:
        '''
        Parameters
        ----------
        input_filename: str
          The name of the file containing the maze
        '''
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

    def add_field(self, y: int, x: int, s: str) -> None:
        '''
        Add information about field at position (y,x) containing symbol s
        Parameters
        ----------
        y,x: int, int
          position on grid
        s: symbol
          #,.,S,E
        '''
        match s:
            case '#':
                barrier = Position(y,x)
                self.barriers.append(barrier)
                print(len(self.is_free))
                print(barrier.one_d_pos)
                self.is_free[barrier.one_d_pos] = False
            case 'S':
                self.start = Position(y,x)
                self.free_fields.append(Position(y,x))
            case 'E':
                self.end = Position(y,x)
                self.free_fields.append(Position(y,x))
            case '.':
                self.free_fields.append(Position(y,x))

    def make_move_tree(self, move_depth: int=100) -> None:
        '''
        Create self.trajectories, a list of all trajectories leading to the goal.
        The approach is the following: generate all possible trajectories of length n based on the
        trajectories of length n-1. Store all trajectories leading to the goal.
        The approach is relatively quick due to self.clean_trajectories.

        Parameters
        ----------
        move_depth: int
          Check all trajectories for how many moves?
        '''
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
            trajectories.append(new_trajectory)

        for i in range(1, move_depth):
            print(i, len(trajectories))
            this_round_trajectories = []
            for traj in trajectories:
                if traj.position.data() == self.end.data():
                    goal_trajectories.append(traj)
                    print('FOUND ONE!!!')
                    continue
                new_moves = self.add_moves(traj)
                if len(new_moves) == 1 and new_moves[0] == traj:
                    continue
                for n in new_moves:
                    this_round_trajectories.append(n)

            trajectories = this_round_trajectories[:]

            if i % 5 == 0:
                trajectories = self.clean_trajectories(trajectories)

        self.trajectories = goal_trajectories

    def clean_trajectories(self, trajectories) -> list[Trajectory]:
        '''
        From trajectories for a given current position and current position,
        keep only the trajectory with the lowest cost.

        Parameters
        ----------
        trajectories: list[Trajectory]

        Returns
        -------
        cleaned_trajectories: list[Trajectory]
        '''

        new_trajs = []
        new_traj_dict = {} # keys are: (pos_y, pos_x, direction)
        for traj in trajectories:
            test_key = (traj.position.y, traj.position.x, traj.direction)
            if test_key in new_traj_dict:
                if traj.cost < new_traj_dict[test_key].cost:
                    new_traj_dict[test_key] = traj
            else:
                new_traj_dict[test_key] = traj
        return list(new_traj_dict.values())

    def find_minimum_trajectory(self) -> Trajectory:
        '''
        Return the trajectory with the lowest cost.

        Returns
        -------
        min_trajectories: Trajectory
        '''
        return min(self.trajectories, key=lambda t: t.cost)

    def add_moves(self, current: Trajectory) -> list[Trajectory]:
        '''
        For a given trajectory, find all trajectories that are generated by adding one additional move.

        Parameters
        ----------
        current: Trajectory
          input trajectory

        Returns
        -------
        result: list[Trajectory]
        '''
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
        '''
        Parameters
        ----------
        current: Trajectory
          trajectory to test for

        direction: str
          in which direction the next move is supposed to go (^>v<)

        Returns
        -------
        next_position: PositionData
          (y,x) of next step, returns (-1,-1) is trajectory is invalid, e.g., due to barrier on the same tile.

        '''
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


if __name__ == '__main__':
    # maze = Maze('z-16-02-actual-example.txt')
    # maze = Maze('z-16-03-another-example.txt')
    maze = Maze('z-16-01-input.txt')
    maze.make_move_tree(move_depth=550)
    trajectory_cost = maze.find_minimum_trajectory().cost
    print(f'The trajectory with the lowest cost has a cost of {trajectory_cost}.')

