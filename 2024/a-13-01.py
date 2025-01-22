'''
Matrix inversion makes solving this task quite easy.
'''
Vector = list[int]
Matrix = list[list[int]]

def read_data(input_filename: str) -> list[str]:
    '''
    Turn data in input file into list of game strings.

    Parameters
    ----------
    input_filename: str

    Returns
    -------
    list[str]
    '''
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    return ''.join(lines).split('\n\n')

def analyze(game: str) -> list[int]:
    '''
    Turn game string into values for A and B increments and goal position.

    Parameters
    ----------
    game: str
      Contains three lines, starting with "Button", "Button", and "Prize"

    Returns
    -------
    x_a, y_a, x_b, y_b: int, int, int, int
      X/Y increment for pushing button A/B
    x_goal, y_goal: int, int
      x,y goal position
    '''
    x_a = game.split('X+')[1].split(',')[0]
    y_a = game.split('Y+')[1].split('\n')[0]
    x_b = game.split('X+')[2].split(',')[0]
    y_b = game.split('Y+')[2].split('\n')[0]
    x_goal = game.split('X=')[1].split(',')[0]
    y_goal = game.split('Y=')[1].split('\n')[0]
    return [int(s) for s in [x_a, y_a, x_b, y_b, x_goal, y_goal]]

def invert_matrix(m: Matrix):
    '''
    Find inverse of 2x2 matrix m, i.e.,
    m = (a b // c d)
    and the inverse is defined such that the matrix multiplication between m and m_inv returns the identity matrix.
    '''
    a, b, c, d = m[0][0], m[0][1], m[1][0], m[1][1]
    det = a*d - b*c
    if det == 0:
        raise ValueError('To solve the equation, the determinant of the matrix must not be zero!')
    return [[d/det, -b/det], [-c/det, a/det]]

def matrix_mult(m: Matrix, v: Vector) -> Vector:
    assert len(m[0]) == len(v), 'Shapes of m and v must be nxk and k'
    result_vector = []
    for i in range(len(m)):
        current_value = 0
        for j in range(len(m[i])):
            current_value += m[i][j] * v[j]
        result_vector.append(current_value)
    return result_vector

def win_one(game: str):
    ''' The two vectors of buttons A and B form a basis.
    We are solving a set of linear equations, i.e., basis_matrix @ button_presses = goal_vector
    where @ is the matrix multiplication.
    For a 2x2 matrix, the solutions can be found by inverting the matrix.
    '''
    x_a, y_a, x_b, y_b, x_goal, y_goal = analyze(game)
    m = [[x_a, x_b], [y_a, y_b]]
    goal_vector = [x_goal, y_goal]
    m_inv = invert_matrix(m)
    return matrix_mult(m_inv, goal_vector)

def close_to_int(n: float, eps: float=1e-6, n_digits: int=0) -> bool:
    return abs(n-round(n, n_digits)) < eps

if __name__ == '__main__':
    # input_filename = 'z-13-02-actual-example.txt'
    input_filename = 'z-13-01-input.txt'
    price_a, price_b = 3, 1
    n_digits = 5
    games = read_data(input_filename)
    total_tokens = 0
    for game in games:
        result_buttons = win_one(game)
        if not all([close_to_int(n) for n in result_buttons]):
            continue
        if not all([n <= 100 for n in result_buttons]): # puzzle says only 100 button presses max
            continue
        total_tokens += price_a * int(round(result_buttons[0]))
        total_tokens += price_b * int(round(result_buttons[1]))

    print(f'The number of total tokens is {total_tokens}.')
