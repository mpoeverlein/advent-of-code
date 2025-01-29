from helpers import Position, Field
PositionData = tuple[int]

class RaceTrack(Field):
    '''
    This object stores on which tiles the track is and on which tiles the barriers are (plus start and end)
    '''
    def __init__(self, input_filename: str) -> None:
        '''
        Parameters
        ----------
        input_filename: str
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
                self.is_free[barrier.one_d_pos] = False
            case 'S':
                self.start = Position(y,x)
                self.free_fields.append(Position(y,x))
            case 'E':
                self.end = Position(y,x)
                self.free_fields.append(Position(y,x))
            case '.':
                self.free_fields.append(Position(y,x))

    def make_lap(self) -> None:
        '''
        Store lap as a list of Position objects ordered from their distance from the Start
        '''
        print('Creating lap...')
        tiles_to_check = self.free_fields
        lap = [self.start]
        tiles_to_check.remove(self.start)

        while len(tiles_to_check) > 0:
            for tile in tiles_to_check:
                if not tile.is_direct_neighbor(lap[-1]):
                    continue
                lap.append(tile)
                tiles_to_check.remove(tile)

        self.lap = lap
        self.lap_set = set(lap) # faster look up
        self.lap_index_dictionary = {v.position_tuple: k for k,v in enumerate(self.lap)} # faster look up for lap index

    def write_lap_to_file(self, output_filename: str) -> None:
        '''
        Write out lap for later use.

        Parameters
        ----------
        output_filename: str
        '''
        with open(output_filename, 'w') as o:
            for k,v in self.lap_index_dictionary.items():
                o.write(f'{k}: {v}\n')

    def get_neighboring_tiles(self, tile: Position) -> list[Position]:
        '''
        Get all tiles that are 2 steps away from current tile.

        Parameters
        ----------
        tile: Position

        Returns
        -------
        neighboring_tiles: list[Position]
        '''
        dy_list = [-2, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 2]
        dx_list = [ 0, -1,  0,  1,-2,-1, 1, 2,-1, 0, 1, 0]
        return [tile+(y,x) for y,x in zip(dy_list, dx_list)]

    def find_shortcuts(self) -> None:
        '''
        Store savings from shortcuts in self.savings.
        '''
        print('Finding all shortcuts...')
        all_shortcut_savings = []
        for tile, next_tile in zip(self.lap[:-1], self.lap[1:]): # finish line not needed
            tiles_to_check = self.get_neighboring_tiles(tile)
            for tile_to_check in tiles_to_check:
                if tile_to_check not in self.lap_set:
                    continue
                saving = self.lap_index_dictionary[tile_to_check.position_tuple] - self.lap_index_dictionary[tile.position_tuple] - 2
                if saving <= 0:
                    continue
                all_shortcut_savings.append(saving)
        self.savings = all_shortcut_savings

    def histogram(self) -> dict[int,int]:
        '''
        Bin self.savings.

        Returns
        -------
        histogram: dict[int,int]
        '''
        histogram_dict = {}
        for saving in self.savings:
            if saving in histogram_dict:
                histogram_dict[saving] += 1
            else:
                histogram_dict[saving] = 1
        histogram_dict = dict(sorted(histogram_dict.items()))

        return histogram_dict

    def shortcut_sum(self) -> int:
        '''
        Sum up all savings at least 100 picoseconds.

        Returns
        -------
        total: int
        '''
        total = 0
        for saving, count in self.histogram().items():
            if saving < 100:
                continue
            total += count
        return total


if __name__ == '__main__':
    input_filename = 'z-20-02-actual-example.txt'
    input_filename = 'z-20-01-input.txt'
    race_track = RaceTrack(input_filename)
    race_track.make_lap()
    race_track.find_shortcuts()
    n_shortcuts = race_track.shortcut_sum()
    print(f'There are {n_shortcuts} shortcuts saving at least 100 picoseconds.')

