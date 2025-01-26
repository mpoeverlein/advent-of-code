import importlib
day_20_01 = importlib.import_module('a-20-01')

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
        print(self.position_dictionary)


if __name__ == '__main__':
    lap_file = 'y-20-01-lap.txt'
    input_filename = 'z-20-01-input.txt'
    race_track = RaceTrack(input_filename)
    race_track.read_lap_data(lap_file)

