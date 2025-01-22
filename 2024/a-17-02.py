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
    reg_a, reg_b, reg_c, instructions = read_data(input_filename)
    print(instructions)
    instructions_string = ','.join([str(s) for s in instructions])
    previous = find_all_starting_n_item(reg_b, reg_c, instructions_string, n=1)
    print([f'{s:o}' for s in previous])
    for n in range(2,len(instructions)+1):
        next_ = find_next_number(reg_b, reg_c, instructions_string, previous, n=n)
        print([f'{s:o}' for s in next_])
        previous = next_
        break
    # for i in range(1,6):
    #     solutions = find_all_starting_n_item(reg_b, reg_c, instructions_string, n=i)
    #     print([f'{s:o}' for s in solutions])
    # jsolutions = find_all_starting_with_first_item(reg_b, reg_c, instructions_string)
    # jprint([f'{s:o}' for s in solutions])
    # jsolutions = find_all_starting_with_first_second_item(reg_b, reg_c, instructions_string)
    # jprint([f'{s:o}' for s in solutions])
    # jsolutions = find_all_starting_with_third_item(reg_b, reg_c, instructions_string)
    # jprint([f'{s:o}' for s in solutions])
    exit()
    # brute force find correct way. works only for small example ... 
    reg_a = 0
    # reg_a = translate_solution(instructions_string)
    # find first 4 digits by brute force
    # solutions = [[]]
    for i in range(8**5,8**8):
        reg_a = i
        outs = run(reg_a, reg_b, reg_c, instructions)
        if outs.startswith(make_instructions_string(instructions, n_items=4)):
            four_digit_solution = reg_a % (8**4)
            break

    print(reg_a, four_digit_solution, f'{reg_a:o}')
    print(reg_a, f'{reg_a:b}', f'{reg_a:o}', outs, binary_representation(outs), translate_solution(outs), f'{four_digit_solution:b}')
    # solutions.append([])

    # find next 4 digits
    for i in range(1,8**7):
        reg_a = four_digit_solution + i * 8**4
        print(f'{four_digit_solution:b}')
        print(f'{reg_a:b}')
        print(f'{four_digit_solution:o}')
        print(f'{reg_a:o}')
        outs = run(i, reg_b, reg_c, instructions)
        if outs.startswith(make_instructions_string(instructions, n_items=8)):
            eight_digit_solution = reg_a % (8**8)
            break

    # print(solutions)
    print(reg_a, eight_digit_solution, f'{reg_a:o}')
    print(reg_a, f'{reg_a:b}', f'{reg_a:o}', outs, binary_representation(outs), translate_solution(outs), f'{eight_digit_solution:b}')
    exit()
