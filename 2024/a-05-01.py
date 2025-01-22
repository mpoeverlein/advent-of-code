def read_data(input_filename: str) -> tuple[list]:
    '''
    Return contents of <input_filename> as list of page ordering rules and list of page sequences

    Parameters
    ----------
    input_filename: str
      Name of the input file

    Returns
    -------
    ordering_rules: list[tuple[int]]
    page_lists: list[list[int]]
    '''
    with open(input_filename, 'r') as f:
        lines = f.read()

    rules_string, lists_string = lines.split('\n\n')

    ordering_rules = []
    for line in rules_string.split('\n'):
        a,b = line.split('|')
        ordering_rules.append((int(a), int(b)))

    page_lists = []
    for line in lists_string.split('\n'):
        if line == '': continue
        page_lists.append([int(s) for s in line.split(',')])

    return (ordering_rules, page_lists)

def get_middle_page_if_correct_sort(page_list: list[int], ordering_rules: list[tuple[int]]) -> int:
    '''
    Check if rules are correctly followed and if yes, return middle page

    Parameters
    ----------
    ordering_rules: list[tuple[int]]
    page_list: list[int]

    Returns
    -------
    middle_page: int
      This value is zero if rules are not being followed
    '''

    for rule in ordering_rules:
        a, b = rule
        if not ((a in page_list) and (b in page_list)):
            continue
        index_a, index_b = page_list.index(a), page_list.index(b)
        if index_a > index_b:
            return 0

    return page_list[len(page_list)//2]

def get_total_sum(ordering_rules: list[tuple[int]], page_lists: list[list[int]]) -> int:
    '''
    Execute get_middle_page_if_correct_sort() for all page_lists

    Parameters
    ----------
    ordering_rules: list[tuple[int]]
    page_lists: list[list[int]]

    Returns
    -------
    total_sum: int
    '''
    total_sum = 0
    for page_list in page_lists:
        total_sum += get_middle_page_if_correct_sort(page_list, ordering_rules)
    return total_sum

if __name__ == '__main__':
    input_filename = 'z-05-01-input.txt'
    ordering_rules, page_lists = read_data(input_filename)
    total_sum = get_total_sum(ordering_rules, page_lists)
    print(f'The total sum is {total_sum}.')
