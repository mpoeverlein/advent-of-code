import numpy as np
import scipy as sp

def read_data(input_filename: str) -> sp.sparse.csr_array:
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    connection_list = []
    computer_set = set()
    for line in lines:
        a,b = line.strip().split('-')
        connection_list.append([a,b])
        computer_set.add(a)
        computer_set.add(b)

    computer_list = list(computer_set)
    computer_list.sort()
    print(computer_list)
    N = len(computer_list)
    adjacency_matrix = sp.sparse.csr_array((N,N), dtype=np.uint8)
    for a,b in connection_list:
        ai, bi = computer_list.index(a), computer_list.index(b)
        adjacency_matrix[ai,bi] = 1
        adjacency_matrix[bi,ai] = 1

    return adjacency_matrix

def iterate(adjacency_matrix: sp.sparse.csr_array) -> sp.sparse.csr_array:
    previous = adjacency_matrix.copy()

    counter = 1
    while True:
        print(counter)
        new = adjacency_matrix @ previous
        if new.nnz == previous.nnz:
            break

        previous = new.copy()
        counter += 1

    return new

def count_nonzero_rows(adjacency_matrix: sp.sparse.csr_array) -> np.array:
    return np.array([adjacency_matrix[:,v].nonzero()[0] for v in range(adjacency_matrix.shape[1])])

def find_most_connected(adjacency_matrix: sp.sparse.csr_array) -> None:
    print(type(adjacency_matrix))
    N,_ = adjacency_matrix.shape
    for i in range(N,-1,-1):
        print(count_nonzero_rows(adjacency_matrix))

if __name__ == '__main__':
    input_filename = 'z-23-02-actual-example.txt'
    # input_filename = 'z-23-01-input.txt'
    adjacency_matrix = read_data(input_filename)
    print(adjacency_matrix.toarray())
    print(type(adjacency_matrix))
    # iterated = iterate(adjacency_matrix)
    # print(iterated.toarray())
    print(find_most_connected(adjacency_matrix))
