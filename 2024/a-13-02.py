Vector = list[int]
Matrix = list[list[int]]

def read_data(input_filename: str) -> list[str]:
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    return ''.join(lines).split('\n\n')

def analyze(game: str) -> list[int]:
    x_a = game.split('X+')[1].split(',')[0]
    y_a = game.split('Y+')[1].split('\n')[0]
    x_b = game.split('X+')[2].split(',')[0]
    y_b = game.split('Y+')[2].split('\n')[0]
    x_goal = game.split('X=')[1].split(',')[0]
    y_goal = game.split('Y=')[1].split('\n')[0]
    return [int(s) for s in [x_a, y_a, x_b, y_b, x_goal, y_goal]]

def invert_matrix(m: Matrix):
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

def win_one(game: str, offset=[10000000000000, 10000000000000]):
    ''' The two vectors of buttons A and B form a basis.
    We are solving a set of linear equations, i.e., basis_matrix @ button_presses = goal_vector
    where @ is the matrix multiplication.
    For a 2x2 matrix, the solutions can be found by inverting the matrix.
    '''
    x_a, y_a, x_b, y_b, x_goal, y_goal = analyze(game)
    m = [[x_a, x_b], [y_a, y_b]]
    goal_vector = [x_goal+offset[0], y_goal+offset[1]]
    m_inv = invert_matrix(m)
    return matrix_mult(m_inv, goal_vector)

def close_to_int(n, eps=1e-4, n_digits=0):
    return abs(n-round(n, n_digits)) < eps

input_filename = 'z-13-02-actual-example.txt'
input_filename = 'z-13-01-input.txt'
price_a, price_b = 3, 1
n_digits = 5
games = read_data(input_filename)
total_tokens = 0
for game in games:
    result_buttons = win_one(game)
    print(result_buttons)
    if not all([close_to_int(n) for n in result_buttons]):
        continue

    print(game)

    # print(result_buttons)
    # total_tokens += price_a * int(round(result_buttons[0], n_digits))
    # total_tokens += price_b * int(round(result_buttons[1], n_digits))
    total_tokens += price_a * int(round(result_buttons[0]))
    total_tokens += price_b * int(round(result_buttons[1]))

print(total_tokens)
# 26251649139461 is too low
# 75200131617108
