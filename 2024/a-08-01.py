Position_dict = dict[str,list[tuple[int]]]
Field = list[list[str]]
empty, antinode = '.', '#'

class AntennaField:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            lines = f.read()

        self.field = [[s for s in line] for line in lines.split('\n')][:-1] # last one is empty list
        self.antinode_field = [[s for s in line] for line in lines.split('\n')][:-1] # last one is empty list
        self.Ny, self.Nx = len(self.field), len(self.field[0])

    def __repr__(self):
        result = 'Field object\n'
        if self.field:
            result += self.make_data_string(self.field) + '\n'
        if self.antinode_field:
            result += self.make_data_string(self.antinode_field) + '\n'

        return result

    @staticmethod
    def make_data_string(field: Field) -> str:
        return 80*'*' + '\n' + '\n'.join([''.join([symbol for symbol in yline]) for yline in field]) + '\n' + 80*'*'

    def make_position_dictionary(self):
        position_dictionary = {}
        for y,line in enumerate(self.field):
            for x,symbol in enumerate(line):
                if symbol == '.':
                    continue
                if symbol not in position_dictionary:
                    position_dictionary[symbol] = []
                position_dictionary[symbol].append((y,x))
        self.position_dictionary = position_dictionary

    def find_antinodes(self):
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
                the_anti_nodes.append((yi+dy, xi+dx))
        return the_anti_nodes
    
    def validate_antinodes(self):
        validated = []
        for i, (yi,xi) in enumerate(self.antinodes):
            if yi < 0 or yi >= self.Ny or xi < 0 or xi >= self.Nx:
                continue
            # if self.field[yi][xi] != empty:
            #     continue
            validated.append((yi,xi))
        self.validated = validated

    def make_antinode_field(self):
        for (yi,xi) in self.validated:
            self.antinode_field[yi][xi] = antinode

    def solve(self):
        self.make_position_dictionary()
        self.find_antinodes()
        self.validate_antinodes()
        self.make_antinode_field()

    def count_unique_antinodes(self) -> int:
        counter = 0
        for line in self.antinode_field:
            for symbol in line:
                if symbol == antinode:
                    counter += 1
        return counter


input_filename = 'z-08-02-actual-example.txt'
# input_filename = 'z-08-01-input.txt'
field = AntennaField(input_filename)
print(field)
field.solve()
print(field)
print(field.count_unique_antinodes())

