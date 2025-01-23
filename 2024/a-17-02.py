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

Example with fake numbers:
Number              Output
5                   0
54                  2,0
547                 3,2,0
5472                6,3,2,0
etc.
'''

import importlib
day_17_01 = importlib.import_module('a-17-01')

def find_last_digit(reg_b: int, reg_c: int, instructions: list[int], previous_list: list[int]) -> list[int]:
    '''
    The last digit is independent from all other digits
    Parameters
    ----------
    reg_b, reg_c: int, int
    instructions: list[int]
    previous_list: list[int]
      These numbers gave the correct result in the previous round of the instructions.

    Returns
    -------
    new_list: list[int]
      These numbers give the correct result and can be used to find the subsequent octal digit.
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

def find_all_digits(reg_b: int, reg_c: int, instructions: list[int]) -> int:
    '''
    Find the smallest number which returns the instructions string when put into register A.

    Parameters
    ----------
    reg_b, reg_c: int, int
    instructions: list[int]

    Returns
    -------
    minimum_number: int
    '''

    previous_list = [0]
    for i in range(len(instructions)):
        previous_list = find_last_digit(reg_b, reg_c, instructions, previous_list)

    return min(previous_list)

if __name__ == '__main__':
    input_filename = 'z-17-02-actual-example.txt'
    input_filename = 'z-17-01-input.txt'
    reg_a, reg_b, reg_c, instructions = day_17_01.read_data(input_filename)
    minimum_value = find_all_digits(reg_b, reg_c, instructions)
    print(f'The minimum number to give back the instructions string is {minimum_value}.')

