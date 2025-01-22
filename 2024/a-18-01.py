FieldData = list[list]
PositionData = tuple[int]

from helpers import Field, Position

def read_data(input_filename: str) -> list[Position]:
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    pos = []
    for line in lines:
        x,y = line.split(',')
        pos.append(Position(int(y),int(x)))
    return pos

class RamField(Field):
    def add_bytes(self, positions: list[Position]) -> None:
        for p in positions:
            self.set_value(p, '#')

    # def __repr__(self) -> str:
    #     result = ''
    def get_neighbors(self, position: Position) -> list[Position]:
        y,x = position.y, position.x
        y_list, x_list = [y-1,y,y+1,y], [x,x+1,x,x-1]
        neighbors = [Position(i,j) for i,j in zip(y_list,x_list)]
        validated = [n for n in neighbors if self.in_bounds(n)]
        validated = [n for n in validated if self.get_value(n) != '#']
        return validated

    def find_path(self) -> None:
        self.position = Position(0,0)
        self.target = Position(self.Ny-1, self.Nx-1)
        path_length = {(0,0): 0}
        tiles_to_check = {(0,0): self.get_neighbors(Position(0,0))}
        print(tiles_to_check)
        while len(tiles_to_check) > 0:
            previous = list(tiles_to_check.keys())[0]
            tile = tiles_to_check[previous].pop()
            if tile.position() not in path_length:
                path_length[tile.position()] = path_length[previous] + 1
                tiles_to_check.update({tile.position(): self.get_neighbors(tile)})

            # print(tiles_to_check)
            tiles_to_check = {k: v for k,v in tiles_to_check.items() if len(v) > 0}
            print(tiles_to_check)

        print(path_length[self.target.position()])
    


if __name__ == '__main__':
    input_filename = 'z-18-01-input.txt'
    # input_filename = 'z-18-02-actual-example.txt'
    empty_input = 'z-18-03-empty-field-large.txt'
    # empty_input = 'z-18-04-empty-field-small.txt'
    pos = read_data(input_filename)
    field = RamField(empty_input, datatype=str)
    print(field)
    print(field.Nx, field.Ny)
    # exit()
    print(field.data_list)
    field.add_bytes(pos[:1024])

    # for p in pos[:12]:
    #     print(field.data_list[p.y])
    #     # field.data_list[p.y][p.x] = '#'
    #     field.set_value(p, '#')

    print(field.find_path())
    # 139 is too low
    # 140 is too low
