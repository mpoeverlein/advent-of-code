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

if __name__ == '__main__':
    # input_filename = 'z-14-02-actual-example.txt'
    input_filename = 'z-14-01-input.txt'
    # time_steps, dim_x, dim_y = 100, 11, 7
    time_steps, dim_x, dim_y = 100, 101, 103
    robots = read_data(input_filename)
    print(robots)
    quadrant_count = {k: 0 for k in range(4)}
    for robot in robots:
        robot.propagate(time_steps, dim_x, dim_y)
        print(robot)
        quad = robot.quadrant(dim_x, dim_y)
        if quad != -1:
            quadrant_count[quad] += 1

    print(quadrant_count)
    print(product(quadrant_count.values()))

# 83445876 is too low
