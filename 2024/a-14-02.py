'''
when do the robots arrange to a christmas tree?
this script prints the robot configuration at every time step and we will
visually find the answer
'''

class Robot:
    def __init__(self, px, py, vx, vy) -> None:
        self.p = [px, py]
        self.v = [vx, vy]
    def propagate(self, time_steps, dim_x, dim_y) -> None:
        self.p = [(self.p[0] + time_steps * self.v[0]) % dim_x,
                  (self.p[1] + time_steps * self.v[1]) % dim_y
        ]

    def __repr__(self):
        return f'Robot at ({self.p[0]},{self.p[1]}) with v=({self.v[0]},{self.v[1]})'

    def quadrant(self, dim_x, dim_y):
        px,py = self.p
        if px == dim_x // 2:
            return -1
        if py == dim_y // 2:
            return -1

        return 2 * int(py > dim_y // 2) + int(px > dim_x // 2)

def read_data(input_filename: str) -> list[Robot]:
    with open(input_filename, 'r') as f:
        lines = f.readlines()

    robots = []
    for line in lines:
        px = int(line.split('=')[1].split(',')[0])
        py = int(line.split(',')[1].split()[0])
        vx = int(line.split('=')[2].split(',')[0])
        vy = int(line.split(',')[2].split()[0])
        robots.append(Robot(px,py,vx,vy))

    return robots

def product(v):
    prod = 1
    for vv in v:
        prod *= vv
    return prod

def make_field_string(robots: list[Robot], dim_x: int, dim_y: int) -> str:
    empty = [[' ' for i in range(dim_x)] for y in range(dim_y)]
    for robot in robots:
        x,y = robot.p
        empty[y][x] = 'O'
    return '\n'.join([''.join(s) for s in empty])

if __name__ == '__main__':
    # input_filename = 'z-14-02-actual-example.txt'
    input_filename = 'z-14-01-input.txt'
    robots = read_data(input_filename)
    time_steps, dim_x, dim_y = 100, 101, 103
    # find christmas tree by visual inspection
    for i in range(1,18_251):
        for robot in robots:
            robot.propagate(1, dim_x, dim_y)
        print(dim_x*'*')
        print(i)
        field_string = make_field_string(robots, dim_x, dim_y)
        if 'OOOOOOOOO' in field_string:
            print(field_string)

    # possible: 18250 is too high


