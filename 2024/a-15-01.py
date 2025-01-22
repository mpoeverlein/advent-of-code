class Position:
    def __init__(self, y: int, x: int):
        self.y, self.x = y, x
        self.position = (y,x)

    def __eq__(self, a) -> bool:
        return (self.position == a.position)

    def set_position(self, position: tuple[int]) -> None:
        y,x = position
        self.y, self.x = y, x
        self.position = (y,x)
    def __repr__(self) -> str:
        return f'Position ({self.y}, {self.x})'

class Field:
    def __init__(self, input_filename) -> None:
        with open(input_filename, 'r') as f:
            lines = f.readlines()
        the_field, self.instructions = ''.join(lines).split('\n\n')
        self.barriers, self.boxes = [], []
        for y, line in enumerate(the_field.split('\n')):
            for x, s in enumerate(line):
                self.add_tile(y,x,s)
        self.Ny, self.Nx = y, x

    def __repr__(self) -> str:
        data = [['.' for i in range(self.Nx+1)] for j in range(self.Ny+1)]
        data[self.robot.y][self.robot.x] = '@'
        for barrier in self.barriers:
            data[barrier[0]][barrier[1]] = '#'
        for box in self.boxes:
            data[box[0]][box[1]] = 'O'
        return '\n'.join([''.join(s) for s in data])

    def add_tile(self, y: int, x: int, s: str) -> None:
        match s:
            case '@':
                self.robot = Position(y,x)
            case '#':
                self.barriers.append((y,x))
            case 'O':
                self.boxes.append((y,x))

    def execute_instructions(self) -> None:
        for move in self.instructions:
            print(move)
            self.apply(move)
            print(self)

    def move_north(self) -> None:
        return [Position(i, self.robot.x) for i in range(self.robot.y-1,-1,-1)]

    def move_east(self) -> None:
        return [Position(self.robot.y, i) for i in range(self.robot.x+1,self.Nx+1,1)]

    def move_south(self) -> None:
        return [Position(i, self.robot.x) for i in range(self.robot.y+1,self.Ny+1,1)]

    def move_west(self) -> None:
        return [Position(self.robot.y, i) for i in range(self.robot.x-1,-1,-1)]

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

        # move robot and N boxes
        for counter, tile in enumerate(ray):
            if tile.position in self.barriers: # cannot move
                return
            elif tile.position in self.boxes:
                continue
            else: # empty
                break

        self.robot.set_position(ray[0].position)
        # current value of counter is where the first box goes
        if counter > 0:
            self.boxes.remove(ray[0].position)
            self.boxes.append(ray[counter].position)

    def sum_gps(self) -> int:
        counter = 0
        for box in self.boxes:
            counter += box[0] * 100 + box[1]
        return counter


if __name__ == '__main__':
    input_filename = 'z-15-01-input.txt'
    # input_filename = 'z-15-02-actual-example.txt'
    # input_filename = 'z-15-03-small.txt'
    field = Field(input_filename)
    print(field)
    field.execute_instructions()
    print(field.sum_gps())


