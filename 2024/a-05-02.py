import importlib
day_05_01 = importlib.import_module('a-05-01')

def sort_by_rules(page_list: list[int], ordering_rules: list[tuple[int]]) -> int:
    '''
    if rules are not followed, this function sorts the page_list and returns the value of the middle page
    if rules are followed, zero is returned
    Parameters
    ----------
    ordering_rules: list[tuple[int]]
    page_lists: list[list[int]]

    Returns
    -------
    value: int
    '''
    for rule in ordering_rules:
        a, b = rule
        if not ((a in page_list) and (b in page_list)):
            continue
        index_a, index_b = page_list.index(a), page_list.index(b)
        if index_a > index_b:
            # swap
            page_list[index_a], page_list[index_b] = page_list[index_b], page_list[index_a]

def get_total_sum(ordering_rules: list[tuple[int]], page_lists: list[list[int]]) -> int:
    '''
    Execute get_middle_page_if_correct_sort() for all page_lists after they were sorted

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
        current_middle = day_05_01.get_middle_page_if_correct_sort(page_list, ordering_rules)
        if current_middle != 0: # don't check the correctly sorted lists
            continue

        while day_05_01.get_middle_page_if_correct_sort(page_list, ordering_rules) == 0:
            sort_by_rules(page_list, ordering_rules)

        actual_middle = day_05_01.get_middle_page_if_correct_sort(page_list, ordering_rules)
        total_sum += actual_middle
    return total_sum


if __name__ == '__main__':
    input_filename = 'z-05-01-input.txt'
    ordering_rules, page_lists = day_05_01.read_data(input_filename)
    total_sum = get_total_sum(ordering_rules, page_lists)
    print(f'The total sum is {total_sum}.')
