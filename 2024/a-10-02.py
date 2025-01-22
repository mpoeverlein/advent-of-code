FieldData = list[list]
PositionData = tuple[int]

from helpers import Field, Position

class TrailField(Field):
    def find_trails_one_start(self, trailhead: Position) -> list[list[Position]]:
        trail = [[trailhead]]
        goal_value = 1
        while goal_value < 10:
            new_list = []
            for position in trail[-1]:
                for neighbor_position in self.get_neighbors(position):
                    if self.get_value(neighbor_position) == goal_value:
                        new_list.append(neighbor_position)

            new_new_list = new_list[:]
            # for item in new_list:
            #     if item in new_new_list: continue
            #     new_new_list.append(item)

            if len(new_list) == 0:
                break
            goal_value += 1
            trail.append(new_new_list)

        return trail

    def find_all_trailheads(self):
        trailheads = []
        for (y,x), d in self.linearized:
            if d == 0:
                trailheads.append(Position(y,x))
        self.trailheads = trailheads

    def find_all_trails(self) -> list[int]:
        scores = []
        for p in self.trailheads:
            trails = self.find_trails_one_start(p)
        return [len(self.find_trails_one_start(p)[-1]) for p in self.trailheads]


if __name__ == '__main__':
    input_filename = 'z-10-02-actual-example.txt'
    input_filename = 'z-10-01-input.txt'
    field = TrailField(input_filename, datatype=int)
    # field = read_data(input_filename)
    print(field)
    print(field.find_trails_one_start(Position(0,2)))
    field.find_all_trailheads()
    print(field.find_all_trails())
    print(sum(field.find_all_trails()))

