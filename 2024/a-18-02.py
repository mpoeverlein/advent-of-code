FieldData = list[list]
PositionData = tuple[int]

from helpers import Field, Position
import importlib
day_18_01 = importlib.import_module('a-18-01')

class RamField(day_18_01.RamField):
    def find_path_lengths(self) -> dict[tuple[int],int]:
        '''
        Find minimum path to all tiles.

        Returns
        -------
        path_length: dict[tuple[int],int]
          keys: positions on field, values: path lengths from start position away

        '''
        path_length = {(0,0): 0}
        tiles_to_check = {(0,0): self.get_neighbors(Position(0,0))}
        while len(tiles_to_check) > 0:
            previous = list(tiles_to_check.keys())[0]
            tile = tiles_to_check[previous].pop()
            if tile.position() not in path_length:
                path_length[tile.position()] = path_length[previous] + 1
                tiles_to_check.update({tile.position(): self.get_neighbors(tile)})

            tiles_to_check = {k: v for k,v in tiles_to_check.items() if len(v) > 0}

        return path_length

    def find_cutting_off_byte(self, positions: list[Position]) -> tuple[int]:
        '''
        Test if path to goal is free for all bytes step-by-step.

        Parameters
        ----------
        positions: list[Position]
          The bytes that fall down

        Returns
        -------
        y,x: int,int
          Tile position of cutting-off byte
        '''
        print('Testing bytes whether they cut off the path...')
        self.target = Position(self.Ny-1, self.Nx-1)
        # we know that the first 1024 are ok
        self.add_bytes(pos[:1024])
        for b in positions[1024:]:
            self.add_bytes([b])
            path_length = self.find_path_lengths()
            if self.target.position() not in path_length:
                return b.position_tuple

if __name__ == '__main__':
    input_filename = 'z-18-01-input.txt'
    # input_filename = 'z-18-02-actual-example.txt'
    empty_input = 'z-18-03-empty-field-large.txt'
    # empty_input = 'z-18-04-empty-field-small.txt'
    pos = day_18_01.read_data(input_filename)
    field = RamField(empty_input, datatype=str)

    y,x = field.find_cutting_off_byte(pos)
    print(f'The byte cutting off the path is on {x},{y}.')
