FieldData = list[list]
PositionData = tuple[int]

from helpers import Field, Position

def read_data(input_filename: str) -> list[Position]:
    '''
    Read in from input_filename, where bytes will be pushed down.

    Parameters
    ----------
    input_filename: str

    Returns
    -------
    pos: list[Position]
    '''
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    pos = []
    for line in lines:
        x,y = line.split(',')
        pos.append(Position(int(y),int(x)))
    return pos

class RamField(Field):
    '''
    Object to store where bytes were pushed down and to find shortest path.
    '''
    def add_bytes(self, positions: list[Position]) -> None:
        '''
        Change value in self.field at (y,x) to # for all items in positions.

        Parameters
        ----------
        positions: list[Position]
        '''
        for p in positions:
            self.set_value(p, '#')

    def get_neighbors(self, position: Position) -> list[Position]:
        '''
        Get neighbors but only if they are not #.

        Parameters
        ----------
        position: Position

        Returns
        -------
        validated: list[Position]
        '''

        y,x = position.y, position.x
        y_list, x_list = [y-1,y,y+1,y], [x,x+1,x,x-1]
        neighbors = [Position(i,j) for i,j in zip(y_list,x_list)]
        validated = [n for n in neighbors if self.in_bounds(n)]
        validated = [n for n in validated if self.get_value(n) != '#']
        return validated

    def find_shortest_path(self) -> int:
        '''
        Find path by computing the minimum path length between the start and every tile.

        Returns
        -------
        shortest_path_length: int
        '''

        self.position = Position(0,0)
        self.target = Position(self.Ny-1, self.Nx-1)
        path_length = {(0,0): 0}
        tiles_to_check = {(0,0): self.get_neighbors(Position(0,0))}
        while len(tiles_to_check) > 0:
            previous = list(tiles_to_check.keys())[0]
            tile = tiles_to_check[previous].pop()
            if tile.position() not in path_length:
                path_length[tile.position()] = path_length[previous] + 1
                tiles_to_check.update({tile.position(): self.get_neighbors(tile)})
            tiles_to_check = {k: v for k,v in tiles_to_check.items() if len(v) > 0}

        return path_length[self.target.position()]


if __name__ == '__main__':
    input_filename = 'z-18-01-input.txt'
    # input_filename = 'z-18-02-actual-example.txt'
    empty_input = 'z-18-03-empty-field-large.txt' # empty input needed to initialize RamField object
    # empty_input = 'z-18-04-empty-field-small.txt'
    pos = read_data(input_filename)
    field = RamField(empty_input, datatype=str)
    field.add_bytes(pos[:1024])
    shortest_path = field.find_shortest_path()
    print(f'The shortest path has {shortest_path} tiles.')
