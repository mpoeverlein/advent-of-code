FieldData = list[list]
PositionData = tuple[int]

import importlib
day_10_01 = importlib.import_module('a-10-01')
from helpers import Field, Position

class TrailField(day_10_01.TrailField):
    def find_trails_one_start(self, trailhead: Position) -> list[list[Position]]:
        '''
        Find all *distinct* trails starting at one position.

        Parameters
        ----------
        trailhead: Position
          The position at which to check as the start

        Returns
        -------
        trail: list[list[Position]]
          list of possible trails
        '''
        trail = [[trailhead]]
        goal_value = 1
        while goal_value < 10:
            new_list = []
            for position in trail[-1]:
                for neighbor_position in self.get_neighbors(position):
                    if self.get_value(neighbor_position) == goal_value:
                        new_list.append(neighbor_position)

            new_new_list = new_list[:]

            if len(new_list) == 0:
                break
            goal_value += 1
            trail.append(new_new_list)

        return trail



if __name__ == '__main__':
    input_filename = 'z-10-02-actual-example.txt'
    input_filename = 'z-10-01-input.txt'
    field = TrailField(input_filename, datatype=int)
    field.find_all_trailheads()
    rating_sum = sum(field.find_all_trails())
    print(f'The sum of all ratings is {rating_sum}.')

