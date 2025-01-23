'''
The numpad and the dpads are represented by objects to check if a given input sequence is allowed.
The robot might wander off-grid otherwise.
Recursively, the shortest possible sequences are found

The levels are:
    - input sequence: '329A', e.g.
    - numpad sequence: '>>A^^A etc.'
    - dpad A sequence: '>>A^A<A etc.'
    - dpad B sequence: '>>A^A<A etc.'
'''
from helpers import Position
from copy import deepcopy
import itertools as it

movement_dictionary = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

def determine_moves_to_do(dy: int, dx: int) -> str:
    '''
    Given a delta y and delta x, which movements are needed.
    The result is unordered, but all_permutations() will create all relevant sequences to check.

    Parameters
    ----------
    dy, dx: int, int

    Returns
    -------
    moves_to_do: str
      E.g. dy=-2,dx=-2 returns '<<^^'
    '''
    moves_to_do = ''
    if dy > 0:
        moves_to_do += dy * 'v'
    elif dy < 0:
        moves_to_do += abs(dy) * '^'

    if dx > 0:
        moves_to_do += dx * '>'
    elif dx < 0:
        moves_to_do += abs(dx) * '<'

    return moves_to_do

def all_permutations(moves_to_do: str) -> list[str]:
    '''
    Finds all permutations of the moves that are to be done.
    Parameters
    ----------
    moves_to_do: str

    Returns
    -------
    sequences_to_check: list[str]
    '''

    sequences_to_check = set([])
    for sequence in it.permutations(moves_to_do):
        sequences_to_check.add(sequence)

    sequences_to_check = list(sequences_to_check)
    return sequences_to_check

class DirectionPadB:
    def __init__(self):
        '''
        Store NumPad info here.
        self.buttons is a dictionary with keypad symbols as keys and their position on a grid as values.
        self.position is a Position object to keep track of the location of the robot.
        self.values is the inverse of the self.buttons dictionary.
        '''
        self.buttons = {
            # key: (y pos, x pos)
                        '^': (0,1), 'A': (0,2),
            '<': (1,0), 'v': (1,1), '>': (1,2)
            }
        self.movement_dict = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
        self.position = Position(*self.buttons['A'])
        self.values = {Position(*v): k for k,v in self.buttons.items()}

    def is_valid(self, start: str, sequence: str) -> bool:
        '''
        Moves are valid if the Robot does not wander off the grid. For DirectionPadB, this is irrelevant.

        Parameters
        ----------
        start: str
        sequence: str

        Returns
        -------
        validity: bool, here always True
        '''
        return True

class DirectionPadA(DirectionPadB):
    def is_valid(self, start: str, sequence: str) -> bool:
        '''
        Moves are valid if the Robot does not wander off the grid.

        Parameters
        ----------
        start: str
        sequence: str

        Returns
        -------
        validity: bool
        '''
        self.position = Position(*self.buttons[start])
        for move in sequence:
            self.position += movement_dictionary[move]
            if self.position not in self.values:
                return False

        return True

class NumPad:
    def __init__(self):
        '''
        Store NumPad info here.
        self.buttons is a dictionary with keypad symbols as keys and their position on a grid as values.
        self.position is a Position object to keep track of the location of the robot.
        self.values is the inverse of the self.buttons dictionary.
        '''
        self.buttons = {
            # key: (y pos, x pos)
            'A': (3,2),
            '0': (3,1),}
        self.buttons.update({str(i+1): (2,i) for i in range(3)})
        self.buttons.update({str(i+4): (1,i) for i in range(3)})
        self.buttons.update({str(i+7): (0,i) for i in range(3)})
        self.position = self.buttons['A']
        self.values = {Position(*v): k for k,v in self.buttons.items()}

    def is_valid(self, start: str, sequence: str) -> bool:
        '''
        Moves are valid if the Robot does not wander off the grid.

        Parameters
        ----------
        start: str
        sequence: str

        Returns
        -------
        validity: bool
        '''
        self.position = Position(*self.buttons[start])
        for move in sequence:
            self.position += movement_dictionary[move]
            if self.position not in self.values:
                return False

        return True

def find_shortest_sequence_numpad(sequence: str) -> str:
    '''
    Returns input sequence in Dpad B language

    Parameters
    ----------
    Returns
    -------
    '''
    shortest_sequence = find_shortest_sequence_numpad_one_step('A', sequence[0])
    for a,b in zip(sequence, sequence[1:]):
        shortest_sequence += find_shortest_sequence_numpad_one_step(a,b)
    return shortest_sequence

def find_shortest_sequence_numpad_one_step(start: str, end: str) -> str:
    '''
    Find shortest Dpad B sequence to get from <start> to <end> on Numpad

    Parameters
    ----------
    start, end: str, str
      Keys on NumPad

    Returns
    -------
    new_sequence: str
      sequence on Dpad B
    '''
    dy = NumPad().buttons[end][0] - NumPad().buttons[start][0]
    dx = NumPad().buttons[end][1] - NumPad().buttons[start][1]
    moves_to_do = determine_moves_to_do(dy, dx)

    possible_sequences = []
    for sequence in all_permutations(moves_to_do):
        if not NumPad().is_valid(start, ''.join(sequence)):
            continue
        possible_sequences.append(find_shortest_sequence_dpad_a(''.join(sequence)+'A'))

    return min(possible_sequences, key=lambda item: len(item))

def find_shortest_sequence_dpad_a(sequence: str) -> str:
    '''
    Returns NumPad sequence in Dpad B language

    Parameters
    ----------
    sequence: str
      NumPad sequence

    Returns
    -------
    new_sequence: str
      Dpad B sequence
    '''
    shortest_sequence = find_shortest_sequence_dpad_a_one_step('A', sequence[0])
    for a,b in zip(sequence, sequence[1:]):
        shortest_sequence += find_shortest_sequence_dpad_a_one_step(a,b)
    return shortest_sequence

def find_shortest_sequence_dpad_a_one_step(start: str, end: str) -> str:
    '''
    Find shortest Dpad B sequence to get from <start> to <end> on Dpad A
    Parameters
    ----------
    start, end: str, str
      Keys on Dpad A

    Returns
    -------
    new_sequence: str
      sequence on Dpad B
    '''
    dy = DirectionPadA().buttons[end][0] - DirectionPadA().buttons[start][0]
    dx = DirectionPadA().buttons[end][1] - DirectionPadA().buttons[start][1]
    moves_to_do = determine_moves_to_do(dy, dx)

    possible_sequences = []
    for sequence in all_permutations(moves_to_do):
        if not DirectionPadA().is_valid(start, ''.join(sequence)):
            continue
        possible_sequences.append(find_shortest_sequence_dpad_b(''.join(sequence)+'A'))

    return min(possible_sequences, key=lambda item: len(item))

def find_shortest_sequence_dpad_b(sequence: str) -> str:
    '''
    Returns Dpad A sequence in Dpad B language

    Parameters
    ----------
    sequence: str
      on dpad A
    Returns
    -------
    new_sequence: str
      sequence in dpad B
    '''
    shortest_sequence = find_shortest_sequence_dpad_b_one_step('A', sequence[0])
    for a,b in zip(sequence, sequence[1:]):
        shortest_sequence += find_shortest_sequence_dpad_b_one_step(a,b)
    return shortest_sequence

def find_shortest_sequence_dpad_b_one_step(start: str, end: str) -> str:
    '''
    Find shortest Dpad B sequence to get from <start> to <end> on Dpad B
    Parameters
    ----------
    start, end: str, str
      Keys on Dpad A

    Returns
    -------
    new_sequence: str
      sequence on Dpad B
    '''
    dy = DirectionPadB().buttons[end][0] - DirectionPadB().buttons[start][0]
    dx = DirectionPadB().buttons[end][1] - DirectionPadB().buttons[start][1]
    moves_to_do = determine_moves_to_do(dy, dx)
    for sequence in all_permutations(moves_to_do):
        if not DirectionPadB().is_valid(start, ''.join(sequence)):
            continue
        return ''.join(sequence) + 'A'

def get_complexities_sum(input_sequences: list[str]) -> int:
    total = 0
    for i in input_sequences:
        o = find_shortest_sequence_numpad(i)
        total += int(i.replace('A','')) * len(o)
    return total

if __name__ == '__main__':
    numpad = NumPad()
    # input_sequences = ['029A', '980A', '179A', '456A', '379A',]
    input_sequences = ['964A', '140A', '413A', '670A', '593A' ]
    complexity = get_complexities_sum(input_sequences)
    print(f'The sum of complexities is {complexity}.')

