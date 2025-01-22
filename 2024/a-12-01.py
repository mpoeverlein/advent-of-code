from copy import deepcopy

FieldData = list[list]
PositionData = tuple[int]

from helpers import Field, Position

class FenceField(Field):
    def assign_regions(self) -> None:
        '''
        Create FenceField.region_dict, which has the positions in the field as keys and the region ID as values.
        '''
        self.region_dict = {k: -1 for k in self.position_list}
        current_region = 0
        while len(self.fields_with_undetermined_region()) > 0:
            test_field = self.fields_with_undetermined_region()[0]
            self.region_dict[test_field.data()] = current_region
            self.assign_all_neighbors(test_field, current_region)
            current_region += 1

        self.n_regions = current_region

    def assign_all_neighbors(self, test_field: Position, current_region: int) -> None:
        '''
        For a given test_field, assign all neighbors with same value to the same region (current_region).

        Parameters
        ----------
        test_field: Position
          position of which neighbors to check
        current_region: int
          id value of this region
        '''
        possible_tests = self.get_neighbors(test_field)
        while len(possible_tests) > 0:
            current_test = possible_tests.pop()
            if self.region_dict[current_test.data()] != -1:
                continue
            if self.get_value(current_test) == self.get_value(test_field):
                self.region_dict[current_test.data()] = current_region
                for item in self.get_neighbors(current_test):
                    possible_tests.append(item)

    def get_fields_of_region(self, region: int) -> list[Position]:
        '''
        Return all positions belonging to a region with id <region>.

        Parameters
        ----------
        region: int
          The region for which to get the positions

        Returns
        position_list: list[Position]
        '''
        return [Position(*k) for k,v in self.region_dict.items() if v == region]

    def create_masked_field(self, mask: list[Position]) -> FieldData:
        '''
        Create field where all positions given by <mask> are marked by '.'

        Parameters
        ----------
        mask: list[Position]

        Returns
        -------
        masked_data: FieldData
        '''
        masked_data = deepcopy(self.field)
        for position in mask:
            masked_data[position.y][position.x] = '.'
        return masked_data

    def create_masked_region(self, region: int) -> FieldData:
        '''
        Create field where all positions not belonging to region with id <region> are marked by '.'

        Parameters
        ----------
        region: int

        Returns
        -------
        masked_data: FieldData
        '''
        actual_data = deepcopy(self.field)
        masked_data = deepcopy(self.field)
        for y, line in enumerate(masked_data):
            for x, s in enumerate(line):
                masked_data[y][x] = '.'

        for position in self.get_fields_of_region(region):
            masked_data[position.y][position.x] = actual_data[position.y][position.x]

        return masked_data

    def fields_with_undetermined_region(self) -> list[Position]:
        '''
        Return all positions not belonging to any regions so far.

        Returns
        -------
        list[Position]
        '''
        return [Position(*k) for k,v in self.region_dict.items() if v == -1]

    @staticmethod
    def make_field_string(data) -> str:
        return '\n'.join([''.join([str(symbol) for symbol in yline]) for yline in data])

    @staticmethod
    def print_data(data) -> str:
        result = '\n'.join([''.join([str(symbol) for symbol in yline]) for yline in data])
        return 80 * '*' + '\n' + result + '\n' + 80 * '*' + '\n'

    def show_regions(self) -> None:
        for i in range(self.n_regions):
            masked_data = self.create_masked_region(i)

    def get_areas(self):
        '''
        Calculate area of each region and store in self.areas, which is list[int]
        '''
        self.areas = []
        for i in range(self.n_regions):
            masked_data = self.create_masked_region(i)
            area = self.count_occurrence(masked_data)
            self.areas.append(area)

    def get_fence_lengths(self):
        '''
        Calculate fence length of each region and store in self.fence_lengths, which is list[int]
        '''
        self.fence_lengths = []
        for i in range(self.n_regions):
            masked_data = self.create_masked_region(i)
            length = self.get_one_fence(masked_data)
            self.fence_lengths.append(length)

    @staticmethod
    def count_occurrence(data: FieldData) -> int:
        counter = 0
        for y, line in enumerate(data):
            for x, s in enumerate(line):
                if s != '.':
                    counter += 1
        return counter

    def get_one_fence(self, data: FieldData) -> int:
        counter = 0

        # count West to East
        for y, line in enumerate(data):
            if line[0] != '.': counter += 1
            for x0, x1 in zip(line,line[1:]):
                if x0 != x1: counter += 1
            if line[-1] != '.': counter += 1

        # count North to South
        data = self.transpose(data) # use this transpose such that the code above can be re-used
        for y, line in enumerate(data):
            if line[0] != '.': counter += 1
            for x0, x1 in zip(line,line[1:]):
                if x0 != x1: counter += 1
            if line[-1] != '.': counter += 1

        return counter

    @staticmethod
    def transpose(data: FieldData) -> FieldData:
        new_data = []
        for x in range(len(data[0])):
            line = [l[x] for l in data]
            new_data.append(line)

        return new_data

    def total_price(self) -> int:
        price = 0
        for area, length in zip(self.areas, self.fence_lengths):
            price += area * length
        return price

if __name__ == '__main__':
    input_filename = 'z-12-02-actual-example.txt'
    input_filename = 'z-12-01-input.txt'
    fence_field = FenceField(input_filename)
    fence_field.assign_regions()
    fence_field.get_areas()
    fence_field.get_fence_lengths()
    total_price = fence_field.total_price()
    print(f'The total price for the fence is {total_price}.')
