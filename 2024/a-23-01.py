def read_data(input_filename: str) -> dict[str,set[str]]:
    '''
    Reads in data such that a dictionary is created for each computer: which computers are connected to it?

    Parameters
    ----------
    input_filename: str

    Returns
    -------
    data_dict: dict[str,set[str]]
      keys: computer, values: every computer, which has a connection to key<computer>
    '''
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    data_dict = {}
    for line in lines:
        a,b = line.strip().split('-')
        if a not in data_dict:
            data_dict[a] = set()
        data_dict[a].add(b)
        if b not in data_dict:
            data_dict[b] = set()
        data_dict[b].add(a)
    return data_dict

def find_trios(data_dict: dict[str,set[str]]) -> list[list[str]]:
    '''
    Turn connection data into trio data.

    Parameters
    ----------
    data_dict: dict[str,set[str]]
      keys: computer, values: all computers connected to it

    Returns
    -------
    unique_result: list[list[str]]
      list of all trio connnections (A,B,C with A-B,B-C,A-C in list of connections)
    '''
    print('Finding all trio connections...')
    result = []
    for c1,(k1,v1) in enumerate(data_dict.items()):
        for c2,(k2,v2) in enumerate(data_dict.items()):
            if c1 <= c2: continue
            if k1 not in v2: continue
            for item in list(v1 & v2):
                result.append([k1,k2,item])
    unique_result = []
    for r in result:
        r.sort()
        if r not in unique_result:
            unique_result.append(r)
    unique_result.sort(key=lambda x: x[2])
    unique_result.sort(key=lambda x: x[1])
    unique_result.sort(key=lambda x: x[0])
    return unique_result

def filter_result(trios: list[list[str]], starting_string: str='t') -> int:
    '''
    Count how many trios contain at least one computer starting with "starting_string"

    Parameters
    ----------
    trios: list[list[str]]
    starting_string: str

    Returns
    -------
    total: int
    '''
    total = 0
    for trio in trios:
        if any([t.startswith(starting_string) for t in trio]):
            total += 1
    return total

if __name__ == '__main__':
    input_filename = 'z-23-02-actual-example.txt'
    input_filename = 'z-23-01-input.txt'
    d = read_data(input_filename)
    trios = find_trios(d)
    trios_with_t_computer = filter_result(trios)
    print(f'There are {trios_with_t_computer} trios with at least one computer name starting with t.')
