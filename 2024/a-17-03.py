# for i in range(8):
#     for j in range(8):
#         print(i,j,i^j)

instruction_string = '2,4,1,3,7,5,0,3,1,5,4,1,5,5,3,0'

def hardcode_one_step(reg_a: int) -> list[int]:
    '''
    I translated the instruction string by hand to have it in explicit form.

    Parameters
    ----------
    reg_a: int
      Value in register A.

    Returns
    -------
    remaining_value: int
    out_value: int
      value in register B
    '''

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
    out = reg_b % 8
    # 3,0: jnz 0
    # if reg_a == 0:
    #     jump = False
    return reg_a, out


for i in range(1,64):
    print(hardcode_one_step(i))

print(hardcode(10000))
