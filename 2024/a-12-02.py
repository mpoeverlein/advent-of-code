from copy import deepcopy
from collections.abc import Callable

FieldData = list[list]
PositionData = tuple[int]

from helpers import Field, Position

# class Inside:
#     above = 'above'
#     below = 'below'
#     right = 'right'
#     left = 'left'

inside_list = ['above', 'below', 'left', 'right']

class FencePart:
    def __init__(self, pos_a: Position, pos_b: Position, inside: str) -> None:
        dx = abs(pos_a.x - pos_b.x)
        dy = abs(pos_a.y - pos_b.y)
        assert ((dx==0) and (dy==1)) or ((dx==1) and (dy==0)), f'X or Y Difference should be 1, current value: {dx} and {dy}'
        self.pos_a = pos_a
        self.pos_b = pos_b
        self.pos_ab = [pos_a, pos_b]
        self.orientation = 'NS' if dy == 1 else 'EW'
        self.max_x, self.max_y = max(pos_a.x, pos_b.x), max(pos_a.y, pos_b.y)
        self.min_x, self.min_y = min(pos_a.x, pos_b.x), min(pos_a.y, pos_b.y)
        self.dx, self.dy = dx, dy
        self.data = {pos_a.data(), pos_b.data()}
        assert inside in inside_list, f'Please specify valid inside ({inside} not in {inside_list}).'
        self.inside = inside

    def __repr__(self) -> str:
        return f'FencePart. A: {self.pos_a.__repr__()}, B: {self.pos_b.__repr__()}, Orientation: {self.orientation}'

class FenceField(Field):
    def assign_regions(self) -> None:
        self.region_dict = {k: -1 for k in self.position_list}
        current_region = 0
        while len(self.fields_with_undetermined_region()) > 0:
            test_field = self.fields_with_undetermined_region()[0]
            self.region_dict[test_field.data()] = current_region
            self.assign_all_neighbors(test_field, current_region)
            current_region += 1

        self.n_regions = current_region

    def assign_all_neighbors(self, test_field: Position, current_region: int) -> None:
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
        return [Position(*k) for k,v in self.region_dict.items() if v == region]

    def create_masked_field(self, mask: list[Position]) -> FieldData:
        masked_data = deepcopy(self.field)
        for position in mask:
            masked_data[position.y][position.x] = '.'
        return masked_data

    def create_masked_region(self, region: int) -> FieldData:
        actual_data = deepcopy(self.field)
        masked_data = deepcopy(self.field)
        for y, line in enumerate(masked_data):
            for x, s in enumerate(line):
                masked_data[y][x] = '.'

        for position in self.get_fields_of_region(region):
            masked_data[position.y][position.x] = actual_data[position.y][position.x]

        return masked_data

    def fields_with_undetermined_region(self) -> list[Position]:
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
            print(self.print_data(masked_data))

    def get_areas(self):
        self.areas = []
        for i in range(self.n_regions):
            masked_data = self.create_masked_region(i)
            area = self.count_occurrence(masked_data)
            self.areas.append(area)

    def get_fence_sides(self) -> None:
        sides = []
        for i in range(self.n_regions):
            masked_data = self.create_masked_region(i)
            fence_coordinates = self.get_fence_coordinates_one_region(masked_data)
            print(fence_coordinates)
            sides.append(self.count_fence_sides_one_region(fence_coordinates))

        self.sides = sides

    @staticmethod
    def count_gaps(data: list[int]) -> int:
        counter = 0
        for a,b in zip(data, data[1:]):
            # print('AB', a,b)
            if a+1 != b:
                counter += 1
        # print('RESULT OCUNTER', counter)
        return counter

    def count_gaps_one_side(self, values: list[int]) -> int:
        if len(values) == 0:
            return 0
        elif len(values) == 1:
            return 1
        values.sort()
        # print(values)
        added_value = 1 + self.count_gaps(values)
        # print(values)
        # print('ADDED value', added_value)
        return added_value

    def count_fence_sides_one_region(self, fence_coordinates: list[FencePart]) -> int:
        n_sides = 0
        # count West to East, i.e., fences with NS orientation
        fence_ns = [f for f in fence_coordinates if f.orientation == 'NS']
        fence_ns_left = [f for f in fence_ns if f.inside == 'left']
        fence_ns_right = [f for f in fence_ns if f.inside == 'right']
        for i in range(self.Nx+1): # plus 1 because fences are outside of field
            # print('IIII', i)
            y_mins = [f.min_y for f in fence_ns_left if f.pos_a.x == i]
            # print(i,y_mins,'left')
            n_sides += self.count_gaps_one_side(y_mins)
            y_mins = [f.min_y for f in fence_ns_right if f.pos_a.x == i]
            # print(i,y_mins,'right')
            n_sides += self.count_gaps_one_side(y_mins)
            # print(i,n_sides,'NSIDES')
        # for i in range(self.Nx+1): # plus 1 because fences are outside of field
        #     current_fences = [f for f in fence_ns_right if f.pos_a.x == i]
        #     if len(current_fences) == 0:
        #         continue
        #     n_sides += 1
        #     if len(current_fences) == 1:
        #         continue
        #     current_fences.sort(key=lambda f: f.min_y)
        #     y_mins = [f.min_y for f in current_fences]
        #     n_sides += self.count_gaps(y_mins)

        # count North to South, i.e., fences with EW orientation
        fence_ew = [f for f in fence_coordinates if f.orientation == 'EW']
        # print(len(fence_ew))
        fence_ew_above = [f for f in fence_ew if f.inside == 'above']
        fence_ew_below = [f for f in fence_ew if f.inside == 'below']
        for i in range(self.Ny+1): # plus 1 because fences are outside of field
            x_mins = [f.min_x for f in fence_ew_above if f.pos_a.y == i]
            # print(i,x_mins,'above')
            n_sides += self.count_gaps_one_side(x_mins)
            x_mins = [f.min_x for f in fence_ew_below if f.pos_a.y == i]
            # print(i,x_mins,'below')
            n_sides += self.count_gaps_one_side(x_mins)
            # print(i,n_sides,'NSIDES')

        print('NSIDES', n_sides)
        return n_sides

    def get_fence_coordinates(self):
        self.fences = []
        for i in range(self.n_regions):
            masked_data = self.create_masked_region(i)
            fence_coordinates = self.get_fence_coordinates_one_region(masked_data)
            fence_coordinates = self.sort_fences(fence_coordinates)
            self.fences.append(fence_coordinates)

    def get_fence_coordinates_one_region(self, data: FieldData) -> list[FencePart]:
        coordinates = []
        # count West to East
        for y, line in enumerate(data):
            if line[0] != '.': coordinates.append(((y,0), (y+1,0), 'right'))
            for x1i, (x0s, x1s) in enumerate(zip(line,line[1:]), start=1):
                if x0s == '.' and x1s != '.':
                    coordinates.append(((y,x1i), (y+1,x1i), 'right'))
                elif x0s != '.' and x1s == '.':
                    coordinates.append(((y,x1i), (y+1,x1i), 'left'))
            if line[-1] != '.': coordinates.append(((y,self.Nx), (y+1,self.Nx), 'left'))

        # count North to South
        data = self.transpose(data)
        for x, line in enumerate(data): # data transposed, so we iterate over x
            if line[0] != '.': coordinates.append(((0,x), (0,x+1), 'below'))
            for y1i, (y0s, y1s) in enumerate(zip(line,line[1:]), start=1):
                if y0s == '.' and y1s != '.':
                    coordinates.append(((y1i,x), (y1i,x+1), 'below'))
                elif y0s != '.' and y1s == '.':
                    coordinates.append(((y1i,x), (y1i,x+1), 'above'))
            if line[-1] != '.': coordinates.append(((self.Ny,x), (self.Ny,x+1), 'above'))

        fence_parts = [FencePart(Position(y1,x1), Position(y2,x2), inside) for (y1,x1), (y2, x2), inside in coordinates]

        return fence_parts

    @staticmethod
    def sort_fences(fence_coordinates: list[FencePart]) -> tuple[list[FencePart]]:
        # start at top left most FencePart
        fence_coordinates.sort(key=lambda p: p.min_y)
        fence_coordinates.sort(key=lambda p: p.min_x)
        fence_coordinates.sort(key=lambda p: p.dy)

        current_fence, fences_to_check = fence_coordinates[0], fence_coordinates[1:]
        sorted_fences = [fence_coordinates[0]]
        starting_fence = fence_coordinates[0]
        while len(fences_to_check) > 0:
            print('FENCES TO CEHCK', len(fences_to_check), fences_to_check)
            for fence in fences_to_check:
                print('current vs. test', current_fence.data, fence.data)
                if current_fence.data & fence.data:
                    fences_to_check.remove(fence)
                    sorted_fences.append(fence)
                    current_fence = fence
                    break

            if len(sorted_fences) > 3:
                print(current_fence.data, starting_fence.data)
                if current_fence.data & starting_fence.data:
                    sorted_fences.append(current_fence)
                    return sorted_fences, fences_to_check



        # sorted_fences.append(fences_to_check[0])
        # return sorted_fences

    def turn_fence_coordinates_to_lines(self):
        self.sides = []
        for i in range(self.n_regions):
            masked_data = self.create_masked_region(i)
            fence_coordinates = self.get_fence_coordinates_one_region(masked_data)
            fence_coordinates, fences_to_check = self.sort_fences(fence_coordinates)
            print('FENCE COORD', fence_coordinates)
            print('FENCES TO CHECK', fences_to_check)
            self.sides.append(self.get_number_of_sides(fence_coordinates))

    def fence_to_line(self, fences: list[Position]) -> list[Position] :
        # find top left fence and go clockwise around area
        fence_parts = []

        print(fences)
        exit()
        fences.sort(key=lambda p: p.y)
        fences.sort(key=lambda p: p.x)
        current_fence = fences[0]
        print(fences)
        print(fences[0])
        fences_to_check = fences[1:]
        while len(fences_to_check) > 1:
            print(fences_to_check)
            for fence_to_check in fences_to_check:
                dy, dx = fence_to_check.y - current_fence.y, fence_to_check.x - current_fence.x
                found_part = False
                y_list, x_list = [-1, 0, 1, 0], [0, 1, 0, -1]
                # priority: NORTH > EAST > SOUTH > WEST
                for test_y, test_x in zip(y_list, x_list):
                    if dy == test_y and dx == test_x:
                        fence_parts.append(FencePart(current_fence, fence_to_check))
                        found_part = True
                        break

                if found_part:
                    current_fence = fence_to_check
                    fences_to_check.remove(current_fence)
                    break

        fence_parts.append(FencePart(fences_to_check[0], fences[0]))
        print(fence_parts)


        exit()


    def get_fence_lengths(self):
        self.fence_lengths = []
        for i in range(self.n_regions):
            masked_data = self.create_masked_region(i)
            length = self.get_one_fence(masked_data)
            print(length)
            self.fence_lengths.append(length)

    def count_sides(self):
        self.sides = []
        for i in range(self.n_regions):
            masked_data = self.create_masked_region(i)
            side = self.get_side_one_region(masked_data)
            print(side)
            self.sides.append(side)

    def get_side_one_region(self, data: FieldData) -> int:
        return 0

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
        data = self.transpose(data)
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

    def discount_price(self) -> int:
        price = 0
        for area, side in zip(self.areas, self.sides):
            print(area, side)
            price += area * side
        return price

    @staticmethod
    def get_number_of_sides(fence_coordinates: list[FencePart]) -> int:
        orientations = [f.orientation for f in fence_coordinates]
        print(orientations)
        n_sides = 0
        for a,b in zip(orientations, orientations[1:]):
            if a != b:
                n_sides += 1

        if orientations[-1] != orientations[0]:
            n_sides += 1

        return n_sides



if __name__ == '__main__':
    input_filename = 'z-12-02-actual-example.txt'
    input_filename = 'z-12-01-input.txt'
    fence_field = FenceField(input_filename)
    print(fence_field)
    fence_field.assign_regions()
    # fence_field.show_regions()
    fence_field.get_areas()
    fence_field.count_sides()
    # fence_field.get_fence_lengths()
    # fence_field.get_fence_coordinates()
    # fence_field.turn_fence_coordinates_to_lines()
    fence_field.get_fence_sides()
    print(fence_field.discount_price())
    # 900404 is too low
    # 907046 is too low
