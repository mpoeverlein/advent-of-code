def get_score(winning_number_list, my_number_list):
    counter = 0
    for mm in my_number_list:
        if mm in winning_number_list:
            counter += 1
    return counter

def get_info(line):
    game = int(line.split(':')[0].split()[-1])
    w, m = line.split(':')[-1].split('|')
    w, m = w.split(), m.split()
    return game, get_count(w, m)


with open('z-04-01-input.txt', 'r') as f:
    lines = f.readlines()

n_points = {}

for line in lines:
    game, score = get_info(line)
    n_points[game] = score

scratch_cards = list(n_points.keys())

total = 0
for scratch_card in scratch_cards:
    score = n_points[scratch_card]
    for i in range(scratch_card+1, scratch_card+1+score):
        scratch_cards.append(i)
    total += 1

print(f'The solution is: {total}')
