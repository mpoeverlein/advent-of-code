class Robot:
    def __init__(self, px, py, vx, vy) -> None:
        '''
        Create Robot object with position and velocity.

        Parameters
        ----------
        px, py: int, int
          Position of Robot
        vx, vy: int, int
          Velocity of Robot, i.e. how many steps moving in 1 second
        '''
        self.p = [px, py]
        self.v = [vx, vy]

    def __repr__(self):
        return f'Robot at ({self.p[0]},{self.p[1]}) with v=({self.v[0]},{self.v[1]})'

    def propagate(self, time_steps: int, dim_x: int, dim_y: int) -> None:
        '''
        Propagate Robot position for <time_steps> seconds, accounting for boundary conditions due to dim_x, dim_y.

        Parameters
        ----------
        time_steps: int
          Number of seconds for which to propagate
        dim_x, dim_y: int, int
          Number of tiles in x/y direction
        '''
        self.p = [(self.p[0] + time_steps * self.v[0]) % dim_x,
                  (self.p[1] + time_steps * self.v[1]) % dim_y
        ]

    def quadrant(self, dim_x: int, dim_y: int):
        '''
        Determine in which quadrant Robot is located.
        Return -1 if Robot is exactly on border between two quadrants.

        Parameters
        ----------
        dim_x, dim_y: int, int
          Number of tiles in x/y direction

        Returns
        -------
        n_quadrant: int, 0, 1, 2 or 3
        '''
        px,py = self.p
        if px == dim_x // 2:
            return -1
        if py == dim_y // 2:
            return -1

        return 2 * int(py > dim_y // 2) + int(px > dim_x // 2)

def read_data(input_filename: str) -> list[Robot]:
    '''
    Read info from input file and create robots.

    Parameters
    ----------
    input_filename: str

    Returns
    -------
    robots: list[Robot]
    '''
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

def product(v: list[int]) -> int:
    '''
    Calculate product of all items in v.

    Returns
    -------
    prod: int
    '''
    prod = 1
    for vv in v:
        prod *= vv
    return prod

def determine_quadrant_count(robots: list[Robot], time_steps: int, dim_x: int, dim_y: int) -> int:
    '''
    Determine in which quadrant each robot is after <time_steps> seconds and calculate the product of the values.

    Parameters
    ----------
    robots: list[Robot]
    time_steps: int
    dim_x, dim_y: int, int

    Returns
    product_quadrant_count: int
    '''
    quadrant_count = {k: 0 for k in range(4)}
    for robot in robots:
        robot.propagate(time_steps, dim_x, dim_y)
        quad = robot.quadrant(dim_x, dim_y)
        if quad != -1:
            quadrant_count[quad] += 1

    return product(quadrant_count.values())

if __name__ == '__main__':
    # input_filename = 'z-14-02-actual-example.txt'
    input_filename = 'z-14-01-input.txt'
    time_steps, dim_x, dim_y = 100, 101, 103
    robots = read_data(input_filename)
    quadrant_count = determine_quadrant_count(robots, time_steps, dim_x, dim_y)
    print(f'The quadrant count is {quadrant_count}.')

