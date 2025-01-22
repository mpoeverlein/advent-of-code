import importlib
day_13_01 = importlib.import_module('a-13-01')

Vector = list[int]
Matrix = list[list[int]]

def win_one(game: str, offset: list[int]=[10000000000000, 10000000000000]) -> list[float]:
    '''
    The two vectors of buttons A and B form a basis.
    We are solving a set of linear equations, i.e., basis_matrix @ button_presses = goal_vector
    where @ is the matrix multiplication.
    For a 2x2 matrix, the solutions can be found by inverting the matrix.
    The goal is offset by <offset>

    Parameters
    ----------
    game: str
      Game definition in string form
    offset: list[int]
      offset of x and y goal position

    Returns
    -------
    result: list[float]
      Result of matrix multiplication of inverted matrix with goal vector
    '''
    x_a, y_a, x_b, y_b, x_goal, y_goal = day_13_01.analyze(game)
    m = [[x_a, x_b], [y_a, y_b]]
    goal_vector = [x_goal+offset[0], y_goal+offset[1]]
    m_inv = day_13_01.invert_matrix(m)
    return day_13_01.matrix_mult(m_inv, goal_vector)

if __name__ == '__main__':
    # input_filename = 'z-13-02-actual-example.txt'
    input_filename = 'z-13-01-input.txt'
    price_a, price_b = 3, 1
    n_digits = 5
    games = day_13_01.read_data(input_filename)
    total_tokens = 0
    for game in games:
        result_buttons = win_one(game)
        if not all([day_13_01.close_to_int(n, eps=1e-4) for n in result_buttons]):
            continue

        total_tokens += price_a * int(round(result_buttons[0]))
        total_tokens += price_b * int(round(result_buttons[1]))

    print(f'The number of total tokens is {total_tokens}.')
