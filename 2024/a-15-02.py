direction_dict = {'^': (-1, 0), '>': (0,1), 'v': (1,0), '<': (0,-1)}

class Position:
    def __init__(self, y: int, x: int):
        self.y, self.x = y, x
        self.position = (y,x)

    def __eq__(self, a) -> bool:
        return (self.position == a.position)

    def __repr__(self) -> str:
        return f'Position ({self.y}, {self.x})'

    def set_position(self, position: tuple[int]) -> None:
        y,x = position
        self.y, self.x = y, x
        self.position = (y,x)

    def push(self, direction):
        dy, dx = direction_dict[direction]
        new_y, new_x = self.y+dy, self.x+dx
        self.set_position((new_y, new_x))

    def look_ahead(self, direction: str, field) -> dict:
        dy, dx = direction_dict[direction]
        next_tile = (self.y+dy, self.x+dx)
        if field.is_barrier[next_tile]:
            return {next_tile: 'barrier'}
        for b in field.boxes:
            if next_tile in b.both_positions():
                return {next_tile: b} | b.look_ahead(direction, field)

        return {next_tile: 'free'}


class Box:
    def __init__(self, position_left: Position, position_right: Position) -> None:
        self.left = position_left
        self.right = position_right

    def push(self, direction: str) -> None:
        self.left.push(direction)
        self.right.push(direction)

    def both_positions(self) -> list[tuple[int]]:
        return [self.left.position, self.right.position]

    def look_ahead(self, direction: str, field) -> dict:
        if direction in ['^', 'v']:
            return self.left.look_ahead(direction, field) | self.right.look_ahead(direction, field)
        elif direction == '>':
            return self.right.look_ahead(direction, field)
        elif direction == '<':
            return self.left.look_ahead(direction, field)


class Field:
    def __init__(self, input_filename, verbose=False) -> None:
        ''' in this task, every x value is twice as wide! '''
        with open(input_filename, 'r') as f:
            lines = f.readlines()
        the_field, self.instructions = ''.join(lines).split('\n\n')
        lines = the_field.split('\n')
        self.Ny, self.Nx = len(lines), 2*len(lines[0])
        self.barriers, self.boxes, self.is_barrier = [], [], {(y,x): False for x in range(self.Nx) for y in range(self.Ny)}
        for y, line in enumerate(lines):
            for x, s in enumerate(line):
                self.add_tile(y,2*x,s)
        self.verbose = verbose

        if self.verbose:
            print(f'Created Field object!')

    def __repr__(self) -> str:
        data = [['.' for i in range(self.Nx)] for j in range(self.Ny)]
        data[self.robot.y][self.robot.x] = '@'
        for barrier in self.barriers:
            data[barrier[0]][barrier[1]] = '#'
        for box in self.boxes:
            data[box.left.y][box.left.x] = '['
            data[box.right.y][box.right.x] = ']'
        return '\n'.join([''.join(s) for s in data])

    def add_tile(self, y: int, x: int, s: str) -> None:
        match s:
            case '@':
                self.robot = Position(y,x)
            case '#':
                self.barriers.append((y,x))
                self.is_barrier[(y,x)] = True
                self.barriers.append((y,x+1))
                self.is_barrier[(y,x+1)] = True
            case 'O':
                self.boxes.append(Box(Position(y,x), Position(y,x+1)))

    def execute_instructions(self) -> None:
        for move in self.instructions:
            self.apply(move)
            if self.verbose == True:
                print(self)

    def tile_north(self) -> tuple[int]:
        return (self.robot.y-1, self.robot.x)

    def tile_east(self) -> None:
        return (self.robot.y, self.robot.x+1)

    def tile_south(self) -> None:
        return (self.robot.y+1, self.robot.x)

    def tile_west(self) -> None:
        return (self.robot.y, self.robot.x-1)

    def apply(self, move):
        match move:
            case '^':
                next_tile = self.tile_north()
            case '>':
                next_tile = self.tile_east()
            case 'v':
                next_tile = self.tile_south()
            case '<':
                next_tile = self.tile_west()
            case _:
                return

        if self.is_barrier[next_tile]:
            return
        # check what's on next positions in front of affected boxes
        no_box = True
        for b in self.boxes:
            if next_tile in b.both_positions():
                box_to_move = b
                no_box = False
                break
        if no_box:
            self.robot.set_position(next_tile)
            return

        tiles_ahead = box_to_move.look_ahead(move, self)
        if any([t == 'barrier' for t in tiles_ahead.values()]):
            return

        self.robot.set_position(next_tile)
        box_to_move.push(move)
        boxes_to_move = set([obj for obj in tiles_ahead.values() if isinstance(obj, Box)])
        for box in boxes_to_move:
            box.push(move)

    def sum_gps(self) -> int:
        counter = 0
        for box in self.boxes:
            counter += box.left.y * 100 + box.left.x
        return counter


if __name__ == '__main__':
    input_filename = 'z-15-01-input.txt'
    # input_filename = 'z-15-02-actual-example.txt'
    # input_filename = 'z-15-03-small.txt'
    # input_filename = 'z-15-04-another-one.txt'
    field = Field(input_filename)
    # print(field)
    field.execute_instructions()
    print(f'The sum of final GPS coordinates is {field.sum_gps()}.')


