class NumPad:
    def __init__(self):
        self.buttons = {
            # key: (y pos, x pos)
            'A': (3,2),
            '0': (3,1),}
        self.buttons.update({str(i+1): (2,i) for i in range(3)})
        self.buttons.update({str(i+4): (1,i) for i in range(3)})
        self.buttons.update({str(i+7): (0,i) for i in range(3)})
        self.position = self.buttons['A']
        self.values = {v: k for k,v in self.buttons.items()}

    def move(self, key) -> str:
        ''' the tile in the bottom left is unused and has to be avoided '''

        new_position = self.buttons[key]
        dy = new_position[0] - self.position[0]
        dx = new_position[1] - self.position[1]
        self.position = new_position

        result = ''
        if dx <= 0 and dy <= 0:
            result += abs(dy) * '^' + abs(dx) * '<'
        elif dx >= 0 and dy >= 0:
            result += abs(dx) * '>' + abs(dy) * 'v'
        elif dx <= 0 and dy >= 0:
            result += abs(dy) * 'v' + abs(dx) * '<'
        elif dx >= 0 and dy <= 0:
            result += abs(dx) * '>' + abs(dy) * '^'

        return result + 'A'

    def execute(self, keystrokes) -> str:
        result = ''
        for key in keystrokes:
            result += self.move(key)
        return result

class DirectionPad:
    def __init__(self):
        self.buttons = {
            # key: (y pos, x pos)
            'A': (0,2),
            '^': (0,1),
            '<': (1,0), 'v': (1,1), '>': (1,2)
            }
        self.position = self.buttons['A']
        self.values = {v: k for k,v in self.buttons.items()}

    def move(self, key) -> str:
        ''' the tile in the top left is unused and has to be avoided '''

        new_position = self.buttons[key]
        dy = new_position[0] - self.position[0]
        dx = new_position[1] - self.position[1]
        self.position = new_position

        result = ''
        if dx <= 0 and dy <= 0:
            result += abs(dy) * '^' + abs(dx) * '<'
        elif dx >= 0 and dy >= 0:
            result += abs(dx) * '>' + abs(dy) * 'v'
        elif dx <= 0 and dy >= 0:
            result += abs(dy) * 'v' + abs(dx) * '<'
        elif dx >= 0 and dy <= 0:
            result += abs(dx) * '>' + abs(dy) * '^'

        return result + 'A'

    def execute(self, keystrokes) -> str:
        result = ''
        for key in keystrokes:
            result += self.move(key)
        return result

    def translate(self, instructions) -> str:
        result = ''
        for instruction in instructions:
            print(instruction, '\t', result, '\t', self.position)
            match instruction:
                case 'A':
                    result += self.values[self.position]
                    dy, dx = 0, 0
                case '^':
                    dy, dx = -1, 0
                case '>':
                    dy, dx = 0, 1
                case 'v':
                    dy, dx = 1, 0
                case '<':
                    dy, dx = 0, -1
            self.position = (self.position[0]+dy, self.position[1]+dx)
        return result

class DirectionPadB:
    def __init__(self):
        self.buttons = {
            # key: (y pos, x pos)
            'A': (0,2),
            '^': (0,1),
            '<': (1,0), 'v': (1,1), '>': (1,2)
            }
        self.position = self.buttons['A']
        self.values = {v: k for k,v in self.buttons.items()}

    def move(self, key) -> str:
        ''' the tile in the top left is unused and has to be avoided '''

        new_position = self.buttons[key]
        dy = new_position[0] - self.position[0]
        dx = new_position[1] - self.position[1]
        self.position = new_position

        result = ''
        if dx <= 0 and dy <= 0:
            result += abs(dy) * '^' + abs(dx) * '<'
        elif dx >= 0 and dy >= 0:
            result += abs(dx) * '>' + abs(dy) * 'v'
        elif dx <= 0 and dy >= 0:
            result += abs(dy) * 'v' + abs(dx) * '<'
        elif dx >= 0 and dy <= 0:
            result += abs(dx) * '>' + abs(dy) * '^'

        return result + 'A'

    def execute(self, keystrokes) -> str:
        self.result = ''
        for key in keystrokes:
            self.result += self.move(key)
        return self.result

def make_sequence(input_sequence: str) -> str:
    numpad = NumPad()
    direction_pad_a = DirectionPad()
    direction_pad_b = DirectionPad()
    direction_a_instructions = numpad.execute(input_sequence)
    print(direction_a_instructions)
    direction_b_instructions = direction_pad_a.execute(direction_a_instructions)
    print(direction_b_instructions)

    return direction_pad_b.execute(direction_b_instructions)

def test_dpad() -> None:
    buttons = ['A', '^', '>', 'v', '<']
    for b in buttons:
        for bb in buttons:
            dp = DirectionPad()
            dp.position = dp.buttons[b]
            move = dp.move(bb)
            print(f'{b} -> {bb}: {move}')

    # test solution
    dp = DirectionPad()
    test = dp.translate('<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A')
    print(dp.translate(test))
    # print(dp.translate('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A'))


if __name__ == '__main__':
    # test_dpad()
    # exit()
    input_sequences = ['029A', '980A', '179A', '456A', '379A',]
#   input_sequences = ['964A', '140A', '413A', '670A', '593A' ]
    input_sequences = ['379A']
    total = 0
    for i in input_sequences:
        o = make_sequence(i)
        print(o, len(o), int(i.replace('A','')))
        total += int(i.replace('A','')) * len(o)
    print(total)
#     # 202612 is too high
# 
# # current wrong
# #              X X
# 'v<<A>>^AvA^Av<<A>>^AAv<A<A>>^AAvAA^<A>Av<A>^AA<A>Av<A<A>>^AAAvA^<A>A 68 379'
# '<v<A>>^AvA^A<v A<  AA>>^AAvA<^A>AAvA^ A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A     64 379'
