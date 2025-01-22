from copy import deepcopy

def read_data(input_filename: str) -> dict[str,set[str]]:
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

def get_unique(data_dict: dict[str,set[str]]) -> set[str]:
    unique = set([])
    for k,items in data_dict.items():
        unique.add(k)
        for item in items:
            unique.add(item)
    return unique


# def read_data(input_filename: str) -> list[tuple[str]]:
#     with open(input_filename, 'r') as f:
#         lines = f.readlines()
#     connections = []
#     for line in lines:
#         a,b = line.strip().split('-')
#         connections.append((a,b))
#     return connections

def find_trios(data_dict: dict[str,set[str]]) -> dict[tuple[str],set[str]]:
    result = []
    for c1,(k1,v1) in enumerate(data_dict.items()):
        for c2,(k2,v2) in enumerate(data_dict.items()):
            if c1 <= c2: continue
            if k1 not in v2: continue
            result.append([k1,k2,v1&v2])
    new_dict = {(k1,k2): item for k1,k2,item in result}
    return {k: v for k,v in new_dict.items() if len(v) > 0}

def find_quads(connection_dict: dict[str,set[str]], data_dict: dict[set[str], set[str]]) -> dict[tuple[str], set[str]]:
    result = {}
    for k,v in data_dict.items():
        if len(v) < 2: continue
        for c1,v1 in enumerate(v):
            print(k,v1)
            key = k+tuple([v1])
            result.update({key: set([])})
            print(result)
            # exit()
            for c2,v2 in enumerate(v):
                # if c1 <= c2: continue
                if v1 == v2: continue
                print(v1,v2)
                if v1 in connection_dict[v2]:
                    result[key].add(v2)
                else:
                    print('NON!')

                    # new_connnections.append([
            print(result)

    exit()

def merge_n_pairs(connection_dict: dict[str,set[str]], data_dict: dict[tuple[str], set[str]]) -> dict[tuple[str], set[str]]:
    N = len(list(data_dict.keys())[0]) # number of connected partners currently identified
    result = {}
    for k,v in data_dict.items():
        if len(v) < 2: continue
        for c1,v1 in enumerate(v):
            print(k,v1)
            key = k+tuple([v1])
            result.update({key: set([])})
            print(result)
            # exit()
            for c2,v2 in enumerate(v):
                # if c1 <= c2: continue
                if v1 == v2: continue
                print(v1,v2)
                if v1 in connection_dict[v2]:
                    result[key].add(v2)
                else:
                    print('NON!')

                    # new_connnections.append([
            print(result)
    result = clean_up(result)
    print(result)
    return result

def clean_up(result: dict[tuple[str], set[str]]) -> dict[tuple[str], set[str]]:
    keys = result.keys()
    keys = [tuple(sorted(list(k))) for k in keys]
    result = {k: v for k,v in zip(keys, result.values())}
    return {k: result[k] for k in keys}


    for c1,(k1,v1) in enumerate(data_dict.items()):
        s1 = set(k1)
        for c2,(k2,v2) in enumerate(data_dict.items()):
            s2 = set(k2)
            if c1 <= c2: continue
            # if k1 not in v2: continue
            # if len
            if len(s1 & s2) != 1: continue
            if len(v1 & v2) == 0: continue
            result.append([s1|s2,v1&v2])
    new_dict = {tuple(k): v for k,v in result}
    return {tuple(k): v for k,v in new_dict.items() if len(v) > 0}
    # unique_result = []
    # for r in result:
    #     r.sort()
    #     if r not in unique_result:
    #         unique_result.append(r)
    # unique_result.sort(key=lambda x: x[2])
    # unique_result.sort(key=lambda x: x[1])
    # unique_result.sort(key=lambda x: x[0])
    # return unique_result

# def merge_n_pairs(pair_list: list[tuple[str]]) -> list[tuple[str]]:
#     N = len(pair_list[0]) # number of items in a pair
#     new_list = []
#     for c1, v1 in enumerate(pair_list):
#         v1 = set(v1)
#         for c2, v2 in enumerate(pair_list):
#             v2 = set(v2)
#             if c1 <= c2: continue
#             if len(v1 & v2) == N-1:
#                 # this_list = []
#                 new_list.append(list(v1 | v2))
# 
#     new_list = [tuple(sorted(i)) for i in new_list]
#     count_tuples = {}
#     for tup in new_list:
#         if tup not in count_tuples:
#             count_tuples[tup] = 1
#         else:
#             count_tuples[tup] += 1
# 
#     filtered_new_list = [tup for tup,v in count_tuples.items() if v > 1]
# 
#     return filtered_new_list

# def new_find_trios(connections: list[tuple[str]]) -> list[tuple[str]]:
#     trios = set([])
#     for ai, tuple_a in enumerate(connections):
#         va = set(tuple_a)
#         for bi, tuple_b in enumerate(connections):
#             if ai <= bi: continue
#             vb = set(tuple_b)
#             if len(va & vb) == 1:ZZ

def find_n_pairs(connections: list[tuple[str]]) -> list[tuple[str]]:
    for c1, v1 in enumerate(pair_list):
        v1 = set(v1)
        for c2, v2 in enumerate(pair_list):
            v2 = set(v2)
            if c1 <= c2: continue
            if len(v1 & v2) == N-1:
                combined_list = list(v1 | v2)
                pair_list = remove_combined(pair_list, combined_list)
                new_list.append(combined_list)

def remove_combined(pair_list, combined_list) -> list[tuple[str]]:
    pass


if __name__ == '__main__':
    input_filename = 'z-23-03-custom.txt'
    # input_filename = 'z-23-02-actual-example.txt'
    # input_filename = 'z-23-01-input.txt'
    connection_dict = read_data(input_filename)
    unique = get_unique(connection_dict)
    print(unique)
    print(len(connection_dict))
    print(connection_dict)
    trios = find_trios(connection_dict)
    print(len(trios))
    print(trios)
    quads = merge_n_pairs(connection_dict, trios)
    # jprint(quads)
    # exit()
    # tmp_list = find_trios(d)
    # quads = merge_n_pairs(trios)
    tmp_list = deepcopy(quads)
    while len(tmp_list) > 1:
        print(len(tmp_list))
        tmp_list = merge_n_pairs(connection_dict, tmp_list)
    # max_pair = find_largest_n_pair(d)
    print(tmp_list)
    print(','.join(tmp_list[0]))
