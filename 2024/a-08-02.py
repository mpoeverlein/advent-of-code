Position_dict = dict[str,list[tuple[int]]]
import importlib
day_08_01 = importlib.import_module('a-08-01')

FieldData = list[list[str]]
empty, antinode = '.', '#'


class AntennaField(day_08_01.AntennaField):
    def __init__(self, filename):
        with open(filename, 'r') as f:
            lines = f.read()

        self.field = [[s for s in line] for line in lines.split('\n')][:-1] # last one is empty list
        self.antinode_field = [[s for s in line] for line in lines.split('\n')][:-1] # last one is empty list
        self.Ny, self.Nx = len(self.field), len(self.field[0])
        self.max_rep = max(self.Ny, self.Nx) # how many possible resonance points to create


    def find_antinodes(self):
        '''
        Store antinodes position in self.antinodes.
        This time, there are many more antinodes, which are found by calculating max_rep
        '''
        anti_nodes = []
        for k, v in self.position_dictionary.items():
            current_anti_nodes = self.find_antinodes_for_one_list(v)
            for item in current_anti_nodes:
                anti_nodes.append(item)
        self.antinodes = anti_nodes

    def find_antinodes_for_one_list(self, positions: list[tuple[int]]) -> list[tuple[int]]:
        the_anti_nodes = []
        N = len(positions)
        for i, (yi,xi) in enumerate(positions):
            for j, (yj,xj) in enumerate(positions):
                if i == j: continue
                dy, dx = yi - yj, xi - xj
                for k in range(self.max_rep):
                    the_anti_nodes.append((yi+k*dy, xi+k*dx))
        return the_anti_nodes



if __name__ == '__main__':
    input_filename = 'z-08-02-actual-example.txt'
    input_filename = 'z-08-01-input.txt'
    field = AntennaField(input_filename)
    field.solve()
    unique_antinodes = field.count_unique_antinodes()
    print(f'There are {unique_antinodes} unique antinodes.')

