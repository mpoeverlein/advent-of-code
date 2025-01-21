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
    def __init__(self, input_filename) -> None:
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
            # print(move)
            self.apply(move)
            # print(self)

    def move_north(self) -> list[tuple[int]]:
        return [(i, self.robot.x) for i in range(self.robot.y-1,-1,-1)]

    def move_east(self) -> None:
        return [(self.robot.y, i) for i in range(self.robot.x+1,self.Nx+1,1)]

    def move_south(self) -> None:
        return [(i, self.robot.x) for i in range(self.robot.y+1,self.Ny+1,1)]

    def move_west(self) -> None:
        return [(self.robot.y, i) for i in range(self.robot.x-1,-1,-1)]

    def apply(self, move):
        match move:
            case '^':
                ray = self.move_north()
            case '>':
                ray = self.move_east()
            case 'v':
                ray = self.move_south()
            case '<':
                ray = self.move_west()
            case _:
                return

        next_tile = ray[0]
        # move robot and boxes
        if self.is_barrier[next_tile]:
            return
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
        # print(tiles_ahead)
        if any([t == 'barrier' for t in tiles_ahead.values()]):
            return

        self.robot.set_position(next_tile)
        box_to_move.push(move)
        boxes_to_move = set([])
        for tile_position, obj in tiles_ahead.items():
            if isinstance(obj, Box):
                boxes_to_move.add(obj)
        for box in boxes_to_move:
            box.push(move)
        return
        
        boxes_to_move = set([])
        box_to_move = None
        for counter, tile_position in enumerate(ray):
            box_present = False
            for b in self.boxes:
                if tile_position in b.both_positions():
                    box_to_move = b
                    box_present = True
                    break
            if self.is_barrier[tile_position]: # cannot move
            # if tile.position in self.barriers: # cannot move
                return
            elif box_present:
                boxes_to_move.add(box_to_move)
            else: # empty
                break

        self.robot.set_position(ray[0])
        # current value of counter is where the first box goes
        if counter > 0:
            for b in boxes_to_move:
                b.push(move)

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
    print(field)
    field.execute_instructions()
    print(field.sum_gps())


