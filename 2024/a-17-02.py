'''
The instruction string for today's problem translates into the following instructions:

    2,4     bst A       A mod 8 -> B
    1,3     bxl 3       B XOR 3 -> B
    7,5     cdv B       floor(A/2**B) -> C
    0,3     adv 3       A / 2**3 -> A
    1,5     bxl 5       B XOR 5 -> B
    4,1     bxc 1       B XOR C -> B
    5,5     out B       print(B % 8)
    5,0     jnz 0       jump to instruction zero if A is non-zero

Since register B and register C are initialized again in each loop,
the printed value of B%8 does not depend on the register A value of the previous iteration.
As a consequence, the final output only depends on the most significant octal digit.
Therefore, the solution can be found by searching for numbers that result in exact matches for
the ending of the instruction string.
'''

import importlib
day_17_01 = importlib.import_module('a-17-01')

def hardcoded_run(reg_a: int, reg_b: int, reg_c: int) -> str:
    '''
    I translated the instruction string by hand to have it in explicit form.

    Parameters
    ----------
    reg_a: int
      Value in register A.

    Returns
    -------
    outs: str
      concatenated values in register B (modulo 8)
    '''
    outs = ''
    jump = True
    while jump:
        # 2,4: bst A
        reg_b = reg_a % 8
        # 1,3: bxl 3
        reg_b ^= 3
        # 7,5: cdv B
        reg_c = reg_a >> reg_b
        # 0,3: adv 3
        reg_a = reg_a >> 3
        # 1,5: bxl 5
        reg_b ^= 5
        # 4,1: bxc 1
        reg_b ^= reg_c
        # 5,5: out B
        outs += f'{reg_b % 8},'
        # 3,0: jnz 0
        if reg_a == 0:
            jump = False
    return outs

def find_last_digit(reg_b: int, reg_c: int, instructions: list[int], previous_list: list[int]) -> list[int]:
    '''
    The last digit is independent from all other digits
    '''
    new_list = []
    instructions_string = ','.join([str(s) for s in instructions])
    for previous in previous_list:
        for i in range(8):
            reg_a = previous*8 + i
            outs = day_17_01.run(reg_a, reg_b, reg_c, instructions)
            if instructions_string.endswith(outs):
                new_list.append(reg_a)
    return new_list

def find_all_digits(reg_b, reg_c, instructions) -> int:
    previous_list = [0]
    for i in range(len(instructions)):
        previous_list = find_last_digit(reg_b, reg_c, instructions, previous_list)

    return min(previous_list)

if __name__ == '__main__':
    input_filename = 'z-17-02-actual-example.txt'
    # input_filename = 'z-17-03-short-example.txt'
    input_filename = 'z-17-01-input.txt'
    reg_a, reg_b, reg_c, instructions = day_17_01.read_data(input_filename)
    minimum_value = find_all_digits(reg_b, reg_c, instructions)
    print(f'The minimum number to give back the instructions string is {minimum_value}.')


    exit()

def read_data(input_filename: str) -> list[int,list[int]]:
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    reg_a, reg_b, reg_c = [int(s.split()[-1]) for s in lines[:3]]
    s = lines[-1].split()[1]
    instructions = [int(ss) for ss in s.split(',')]

    return [reg_a, reg_b, reg_c, instructions]

def translate_combo(literal_operand, reg_a, reg_b, reg_c):
    combos = [0, 1, 2, 3, reg_a, reg_b, reg_c, None]
    return combos[literal_operand]

def binary_representation(outs):
    sum_ = 0
    for c,i in enumerate(outs.split(',')):
        sum_ += int(i) * 8 ** c
    return f'{sum_:b}'

def adv(reg_a, translated_combo): return reg_a / 2**translated_combo
def bxl(literal_operand, reg_b): return literal_operand ^ reg_b
def bst(translated_combo): return translated_combo % 8
def bxc(reg_b, reg_c): return reg_b ^ reg_c

def run(reg_a, reg_b, reg_c, instructions) -> str:
    outs = []
    instruction_pointer = 0
    while instruction_pointer < len(instructions):
        current_instruction = instructions[instruction_pointer]
        literal_operand = instructions[instruction_pointer+1]
        translated_combo = translate_combo(literal_operand, reg_a, reg_b, reg_c)

        match current_instruction:
            case 0:
                reg_a = int(adv(reg_a, translated_combo))
            case 1:
                reg_b = bxl(literal_operand, reg_b)
            case 2:
                reg_b = bst(translated_combo)
            case 3:
                if reg_a != 0:
                    instruction_pointer = literal_operand - 2 # to undo the final incrementation
            case 4:
                reg_b = bxc(reg_b, reg_c)
            case 5:
                outs.append(bst(translated_combo))
            case 6:
                reg_b = int(adv(reg_a, translated_combo))
            case 7:
                reg_c = int(adv(reg_a, translated_combo))

        instruction_pointer += 2

    return ','.join([str(s) for s in outs])

def translate_solution(instructions_string):
    mappings = [6, 7, 4, 5, -1, 2, 3, 1]
    exponent = 1
    the_number = 0
    for a in instructions_string.split(',')[::]:
        mapped = mappings[int(a)]
        the_number += mapped * exponent
        exponent *= 8

    return the_number

def make_instructions_string(instructions, n_items=1):
    return ','.join([str(s) for s in instructions[:n_items]])

def find_all_starting_with_first_item(reg_b, reg_c, instructions_string):
    solutions = []
    for i in range(1,8**6):
        reg_a = i
        outs = run(reg_a, reg_b, reg_c, instructions)
        if outs.startswith(make_instructions_string(instructions, n_items=1)):
            # print(f'{reg_a:30b}', f'{reg_a:30o}')
            solutions.append(reg_a)
    return set([s%8 for s in solutions])

def find_all_starting_with_first_second_item(reg_b, reg_c, instructions_string):
    solutions = []
    for i in range(1,8**6):
        reg_a = i
        outs = run(reg_a, reg_b, reg_c, instructions)
        if outs.startswith(make_instructions_string(instructions, n_items=2)):
            # print(f'{reg_a:30b}', f'{reg_a:30o}')
            solutions.append(reg_a)
    return set([s%(8**2) for s in solutions])

def find_all_starting_with_third_item(reg_b, reg_c, instructions_string):
    solutions = []
    for i in range(1,8**6):
        reg_a = i
        outs = run(reg_a, reg_b, reg_c, instructions)
        if outs.startswith(make_instructions_string(instructions, n_items=3)):
            # print(f'{reg_a:30b}', f'{reg_a:30o}')
            solutions.append(reg_a)
    return set([s%(8**3) for s in solutions])

def find_all_starting_n_item(reg_b, reg_c, instructions_string, n=1):
    solutions = []
    for i in range(1,8**6):
        reg_a = i
        outs = run(reg_a, reg_b, reg_c, instructions)
        if outs.startswith(make_instructions_string(instructions, n_items=n)):
            # print(f'{reg_a:30b}', f'{reg_a:30o}')
            solutions.append(reg_a)
    return set([s%(8**n) for s in solutions])

def find_next_number(reg_b, reg_c, instructions_string, previous, n):
    solutions = []
    for i in previous:
        for j in range(1,8):
            reg_a = i + j*8**(n-1)
            print(f'{reg_a:o}')
            outs = run(reg_a, reg_b, reg_c, instructions)
            if outs.startswith(make_instructions_string(instructions, n_items=n)):
                solutions.append(reg_a)

    return set([s%(8**n) for s in solutions])



if __name__ == '__main__':
    input_filename = 'z-17-02-actual-example.txt'
    # input_filename = 'z-17-03-short-example.txt'
    input_filename = 'z-17-01-input.txt'
    reg_a, reg_b, reg_c, instructions = day_17_01.read_data(input_filename)
    print(run(reg_a, reg_b, reg_c, instructions))
    previous_list = [0]
    print(instructions)
    for i in range(len(instructions)):
        previous_list = find_last_digit(reg_b, reg_c, instructions, previous_list)

    print(previous_list)
