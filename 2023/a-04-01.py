def get_score(winning_number_list, my_number_list):
    counter = 0
    for mm in my_number_list:
        if mm in winning_number_list:
            counter += 1

    if counter == 0:
        return 0

    return 2**(counter-1)


with open('z-04-01-input.txt', 'r') as f:
    lines = f.readlines()

winning_numbers, my_numbers = [], []
for line in lines:
    numbers = line.split(':')[-1]
    w, m = numbers.split('|')
    w, m = w.split(), m.split()
    winning_numbers.append(w)
    my_numbers.append(m)

total = 0
for w, m in zip(winning_numbers, my_numbers):
    total += get_count(w, m)

print(f'The solution is: {total}')
