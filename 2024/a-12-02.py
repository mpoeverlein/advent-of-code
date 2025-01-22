from copy import deepcopy

FieldData = list[list]

import importlib
day_12_01 = importlib.import_module('a-12-01')
from helpers import Field, Position

PositionData = tuple[int]
inside_list = ['above', 'below', 'left', 'right']

class FencePart:
    def __init__(self, pos_a: Position, pos_b: Position, inside: str) -> None:
        '''
        FencePart object is defined by Positions pos_a and pos_b and on which side of the fence is inside the region.

        Parameters
        ----------
        pos_a: Position
        pos_b: Position
        inside: str
        '''
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

class FenceField(day_12_01.FenceField):
    def get_fence_sides(self) -> None:
        '''
        Calculate number of fence sides for each region and stores as list[int] in self.sides.
        '''
        sides = []
        for i in range(self.n_regions):
            masked_data = self.create_masked_region(i)
            fence_coordinates = self.get_fence_coordinates_one_region(masked_data)
            sides.append(self.count_fence_sides_one_region(fence_coordinates))

        self.sides = sides

    @staticmethod
    def count_gaps(data: list[int]) -> int:
        '''
        Count how often the difference in subsequent items in data is not equal to 1, a.k.a. gaps.

        Parameters
        ----------
        data: list[int]

        Returns
        -------
        counter: int
        '''
        counter = 0
        for a,b in zip(data, data[1:]):
            if a+1 != b:
                counter += 1
        return counter

    def count_gaps_one_side(self, values: list[int]) -> int:
        '''
        Count number of fence sides in one row.

        Parameters
        ----------
        values: list[int]

        Returns
        -------
        added_value: int
        '''
        if len(values) == 0:
            return 0
        elif len(values) == 1:
            return 1
        values.sort()
        added_value = 1 + self.count_gaps(values)
        return added_value

    def count_fence_sides_one_region(self, fence_coordinates: list[FencePart]) -> int:
        '''
        Count number of fence sides for one whole region.

        Parameters
        ----------
        fence_coordinates: list[FencePart]
          list of FenceParts around the region

        Returns
        -------
        n_sides: int
        '''
        n_sides = 0
        # count West to East, i.e., fences with NS orientation
        fence_ns = [f for f in fence_coordinates if f.orientation == 'NS']
        fence_ns_left = [f for f in fence_ns if f.inside == 'left']
        fence_ns_right = [f for f in fence_ns if f.inside == 'right']
        for i in range(self.Nx+1): # plus 1 because fences are outside of field
            y_mins = [f.min_y for f in fence_ns_left if f.pos_a.x == i]
            n_sides += self.count_gaps_one_side(y_mins)
            y_mins = [f.min_y for f in fence_ns_right if f.pos_a.x == i]
            n_sides += self.count_gaps_one_side(y_mins)

        # count North to South, i.e., fences with EW orientation
        fence_ew = [f for f in fence_coordinates if f.orientation == 'EW']
        fence_ew_above = [f for f in fence_ew if f.inside == 'above']
        fence_ew_below = [f for f in fence_ew if f.inside == 'below']
        for i in range(self.Ny+1): # plus 1 because fences are outside of field
            x_mins = [f.min_x for f in fence_ew_above if f.pos_a.y == i]
            n_sides += self.count_gaps_one_side(x_mins)
            x_mins = [f.min_x for f in fence_ew_below if f.pos_a.y == i]
            n_sides += self.count_gaps_one_side(x_mins)

        return n_sides

    def get_fence_coordinates_one_region(self, data: FieldData) -> list[FencePart]:
        '''
        Determine fences for one region

        Parameters
        ----------
        data: FieldData

        Returns
        -------
        coordinates: list[FencePart]
        '''
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

    def discount_price(self) -> int:
        '''
        Determine discount price by calculating sum of product of sides and areas for all regions.

        Returns
        -------
        price: int
        '''
        price = 0
        for area, side in zip(self.areas, self.sides):
            price += area * side
        return price


if __name__ == '__main__':
    input_filename = 'z-12-02-actual-example.txt'
    input_filename = 'z-12-01-input.txt'
    fence_field = FenceField(input_filename)
    fence_field.assign_regions()
    fence_field.get_areas()
    fence_field.get_fence_sides()
    discount_price = fence_field.discount_price()
    print(f'The discount price for the fence is {discount_price}.')
