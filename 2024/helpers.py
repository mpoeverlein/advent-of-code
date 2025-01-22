def read_data_as_list_strings(input_filename: str) -> list[str]:
    '''
    Return contents of <input_filename> as list of list of integers
    Parameters
    ----------
    input_filename: str
      Name of the input file

    Returns
    -------
    lines: list[str]
    '''
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    return lines

def read_data_as_list_list_int(input_filename: str) -> list[list[int]]:
    '''
    Return contents of <input_filename> as list of list of integers
    Parameters
    ----------
    input_filename: str
      Name of the input file

    Returns
    -------
    levels_list: list[list[int]]

    '''
    with open(input_filename, 'r') as f:
        lines = f.readlines()

    levels_list = []
    for line in lines:
        levels_list.append([int(s) for s in line.split()])

    return levels_list

FieldData = list[list]
PositionData = tuple[int]

class Position:
    def __init__(self, y: int, x: int):
        assert type(y) == type(x) == int, 'Position object must be initialized with two integers!'
        self.y, self.x = y, x
        self.position_tuple = (self.y, self.x)
        self.one_d_pos = self.one_d_position()
    def __repr__(self):
        return f'Position: y={self.y},x={self.x}'
    def __eq__(self, a) -> bool:
        return self.position_tuple == a.position_tuple
    def __hash__(self) -> int:
        return hash(self.position_tuple)
    def data(self) -> PositionData:
        return (self.y, self.x)
    def position(self) -> PositionData:
        return (self.y, self.x)
    def one_d_position(self) -> int:
        # linearize 2-ple by indexing over cross-diagonals
        k = self.y + self.x + 1
        return int((k*(k+1))//2 - 1) - self.y

class Field:
    def __init__(self, input_filename, datatype=str):
        self.field = self.read_data(input_filename, datatype=datatype)
        self.Ny, self.Nx = len(self.field), len(self.field[0])
        # create serialized version of data to make looping easier
        y_list, x_list, data_list = [], [], []
        for y in range(self.Ny):
            for x in range(self.Nx):
                y_list.append(y)
                x_list.append(x)
                data_list.append(self.field[y][x])
        self.linearized = [((y,x), d) for y,x,d in zip(y_list, x_list, data_list)]
        self.data_list = data_list
        self.position_list = list(zip(y_list, x_list))

    def __repr__(self) -> str:
        result = '\n'.join([''.join([str(symbol) for symbol in yline]) for yline in self.field])
        return 80 * '*' + '\n' + result + '\n' + 80 * '*' + '\n'

    @staticmethod
    def read_data(filename: str, datatype=str) -> FieldData:
        with open(filename, 'r') as f:
            lines = f.read()
    
        return [[datatype(s) for s in line] for line in lines.split('\n')][:-1] # last one is empty list

    def get_value(self, position: Position) -> int:
        return self.field[position.y][position.x]

    def set_value(self, position: Position, new_value) -> None:
        self.field[position.y][position.x] = new_value

    def in_bounds(self, position: Position) -> bool:
        y,x = position.y, position.x
        return 0 <= y < self.Ny and 0 <= x < self.Nx

    def get_neighbors(self, position: Position) -> list[Position]:
        y,x = position.y, position.x
        y_list, x_list = [y-1,y,y+1,y], [x,x+1,x,x-1]
        neighbors = [Position(i,j) for i,j in zip(y_list,x_list)]
        validated = [n for n in neighbors if self.in_bounds(n)]
        return validated

    def find_trails_one_start(self, trailhead: Position) -> list[list[Position]]:
        trail = [[trailhead]]
        goal_value = 1
        while goal_value < 10:
            # print('GOAL VLAUE', goal_value)
            new_list = []
            for position in trail[-1]:
                for neighbor_position in self.get_neighbors(position):
                    if self.get_value(neighbor_position) == goal_value:
                        new_list.append(neighbor_position)

            new_new_list = []
            for item in new_list:
                if item in new_new_list: continue
                new_new_list.append(item)
            

            print('oldlist', new_list)
            print('newlist', new_new_list)
            if len(new_list) == 0:
                break
            goal_value += 1
            trail.append(new_list)

        return trail

    def find_all_trailheads(self):
        trailheads = []
        for y, line in enumerate(self.field):
            for x, symbol in enumerate(line):
                if symbol == 0:
                    trailheads.append(Position(y,x))
        self.trailheads = trailheads

    def find_all_trails(self) -> list[int]:
        scores = []
        for p in self.trailheads:
            trails = self.find_trails_one_start(p)
            print(trails[-1])
        return [len(self.find_trails_one_start(p)[-1]) for p in self.trailheads]

if __name__ == '__main__':

    input_filename = 'z-10-02-actual-example.txt'
    field = Field(input_filename, datatype=int)
    for (y,x), d in field.linearized:
        p = Position(y,x)
        print(y,x,d,p.one_d_pos)
