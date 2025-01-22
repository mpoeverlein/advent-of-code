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

def adv(reg_a, translated_combo): return reg_a / 2**translated_combo
def bxl(literal_operand, reg_b): return literal_operand ^ reg_b
def bst(translated_combo): return translated_combo % 8
def bxc(reg_b, reg_c): return reg_b ^ reg_c

if __name__ == '__main__':
    input_filename = 'z-17-02-actual-example.txt'
    input_filename = 'z-17-01-input.txt'
    reg_a, reg_b, reg_c, instructions = read_data(input_filename)
    print(instructions)
    outs = []
    instruction_pointer = 0
    while instruction_pointer < len(instructions):
        current_instruction = instructions[instruction_pointer]
        print(instruction_pointer, current_instruction)
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

    print(','.join([str(s) for s in outs]))
