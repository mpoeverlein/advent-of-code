import importlib
day_20_01 = importlib.import_module('a-20-01')
from helpers import Position

class RaceTrack(day_20_01.RaceTrack):
    def read_lap_data(self, lap_file: str) -> None:
        with open(lap_file, 'r') as f:
            lines = f.readlines()
        self.lap_index_dictionary = {}
        for line in lines:
            y = int(line.split(',')[0].split('(')[-1])
            x = int(line.split(',')[1].split(')')[0])
            index = int(line.split(':')[-1])

            self.lap_index_dictionary[(y,x)] = index

        self.position_dictionary = {v: k for k,v in self.lap_index_dictionary.items()}
        self.lap = [Position(*self.position_dictionary[k]) for k in range(len(self.position_dictionary))]
        self.lap_set = set(self.lap) # faster look up

    def get_neighboring_tiles_and_distances(self, tile: Position, cheat_time: int= 20) -> tuple[list[Position],list[int]]:
        '''
        Find all tiles at most 20 steps away and return together with distance from <tile>.

        Parameters
        ----------
        tile: Position
        cheat_time: 20

        Returns
        -------
        tile_list, distances: tuple[list[Position],list[int]]
        '''
        dy_list, dx_list = [], []
        for i in range(-cheat_time,cheat_time+1):
            dy = i
            max_dx = cheat_time-abs(dy)
            for dx in range(-max_dx, max_dx+1):
                if (dy,dx) == (0,0):
                    continue
                dy_list.append(dy)
                dx_list.append(dx)

        return [tile+(y,x) for y,x in zip(dy_list, dx_list)], [abs(y)+abs(x) for y,x in zip(dy_list,dx_list)]

    def find_shortcuts(self) -> None:
        '''
        Store savings from shortcuts in self.savings.
        '''
        print('Finding all shortcuts...')
        all_shortcut_savings = []
        for tile, next_tile in zip(self.lap[:-1], self.lap[1:]): # finish line not needed
            tiles_to_check, distances = self.get_neighboring_tiles_and_distances(tile)
            for tile_to_check, distance in zip(tiles_to_check, distances):
                if tile_to_check not in self.lap_set:
                    continue
                saving = self.lap_index_dictionary[tile_to_check.position_tuple] - self.lap_index_dictionary[tile.position_tuple] - distance
                if saving <= 0:
                    continue
                all_shortcut_savings.append(saving)
        self.savings = all_shortcut_savings


if __name__ == '__main__':
    lap_file = 'y-20-01-lap.txt'
    input_filename = 'z-20-01-input.txt'
    # input_filename = 'z-20-02-actual-example.txt'
    race_track = RaceTrack(input_filename)
    race_track.read_lap_data(lap_file)
    race_track.find_shortcuts()
    n_shortcuts = race_track.shortcut_sum()
    print(f'There are {n_shortcuts} shortcuts saving at least 100 picoseconds.')

