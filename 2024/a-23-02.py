import importlib
day_23_01 = importlib.import_module('a-23-01')
from copy import deepcopy

def find_trios(data_dict: dict[str,set[str]]) -> dict[tuple[str],tuple[str]]:
    '''
    Turn connection data into trio data.

    Parameters
    ----------
    data_dict: dict[str,set[str]]
      keys: computer, values: all computers connected to it

    Returns
    -------
    new_dict: dict[tuple[str],tuple[str]]
      keys: a pair of two computers that are connected, values: all computers that are connected to *both* of the computers in key.
    '''
    result = []
    for c1,(k1,v1) in enumerate(data_dict.items()):
        for c2,(k2,v2) in enumerate(data_dict.items()):
            if c1 <= c2: continue
            if k1 not in v2: continue
            result.append([k1,k2,tuple(v1&v2)])
    new_dict = {(k1,k2): item for k1,k2,item in result}
    return {k: v for k,v in new_dict.items() if len(v) > 0}


def merge_pairs(connection_dict: dict[str,set[str]], data_dict: dict[tuple[str],tuple[str]]) -> dict[tuple[str],tuple[str]]:
    '''
    Merge data_dict, which has n-tuple keys such that the keys will be (n+1)-tuples
    Parameters
    ----------
    connection_dict: dict[str,set[str]]
      keys: computer, values: all computers connected to it
    data_dict: dict[tuple[str],tuple[str]]
      keys: tuple of n computers, which are all connected to each other
      values: all computers that are connected to all n computers (except for the ones that are already in the key)

    Returns
    -------
    new_dict: dict[tuple[str],tuple[str]]
    '''
    new_dict = {}
    connection_set = set([])
    for pair, connections in data_dict.items():
        if len(connections) == 0:
            continue
        if len(connections) == 1:
            new_pair = tuple(sorted(list(pair+tuple([connections[0]]))))
            if new_pair in connection_set:
                continue

            connection_set.add(new_pair)
            new_dict.update({new_pair: tuple([])})
            continue

        for connection in connections:
            test_connections = list(connections[:])
            test_connections.remove(connection)
            if not all([test in connection_dict[connection] for test in test_connections]):
                continue

            new_pair = tuple(sorted(list(pair+tuple([connection]))))
            if new_pair in connection_set:
                continue

            connection_set.add(new_pair)
            new_dict.update({new_pair: tuple(test_connections)})

    return new_dict

def find_largest_clique(connection_dict: dict[str,set[str]], n_iterations: int=100) -> str:
    '''
    Given connection_dict, find largest clique and return computer names joined by ,

    Parameters
    ----------
    connection_dict: dict[str,set[str]]
    n_iterations: int

    Returns
    -------
    computers: str
    '''
    trios = find_trios(connection_dict)
    merged_connections = deepcopy(trios)
    print('Merging connections! This might take some time...')
    clique = ''
    for i in range(n_iterations):
        print(i)
        merged_connections = merge_pairs(connection_dict, merged_connections)
        for k,v in merged_connections.items():
            if len(v) == 0:
                clique =','.join(k)

    return clique


if __name__ == '__main__':
    input_filename = 'z-23-03-custom.txt'
    input_filename = 'z-23-02-actual-example.txt'
    input_filename = 'z-23-01-input.txt'
    connection_dict = day_23_01.read_data(input_filename)
    clique = find_largest_clique(connection_dict)
    print(f'The largest clique is {clique}.')
