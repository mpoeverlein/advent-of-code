def read_data(input_filename: str) -> dict[str,str]:
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

def find_trios(data_dict: dict[str,str]) -> list[tuple[str]]:
    result = []
    for c1,(k1,v1) in enumerate(data_dict.items()):
        for c2,(k2,v2) in enumerate(data_dict.items()):
            if c1 <= c2: continue
            if k1 not in v2: continue
            # print(k1, v1)
            # print(k2, v2)
            # print(k1, k2, v1 & v2)
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

def filter_result(r: list[tuple[str]], starting_string: str='t'):
    new = []
    for rr in r:
        for item in rr:
            if item.startswith(starting_string):
                new.append(rr)
                break

    return new

if __name__ == '__main__':
    input_filename = 'z-23-02-actual-example.txt'
    input_filename = 'z-23-01-input.txt'
    d = read_data(input_filename)
    print(d)
    trios = find_trios(d)
    print(filter_result(trios))
    print(len(filter_result(trios)))
