with open('z-05-01-input.txt', 'r') as f:
    lines = f.readlines()

seeds = lines[0].split(':')[1].split()
seeds = [int(s) for s in seeds]
range_list = seeds.copy()

def check_number_in_range_list(number, range_list):
    for a, b in zip(range_list[::2], range_list[1::2]):
        if (a<number) and (number<a+b):
            return True
    return False

def get_map(number, l):
    for line in l:
        destination, start, length = [int(s) for s in line.split()]
        if (start <= number) and (number < start+length):
            return destination + number - start

    return number

def get_inverse_map(number, range_list):
    for start, destination, length in range_list:
        if (start <= number) and (number < start+length):
            return destination + number - start

    return number

def make_ranges(l):
    range_list = []
    for line in l:
        destination, start, length = [int(s) for s in line.split()]
        range_list.append([destination, start, length])
    return range_list

s2s = make_ranges(lines[3:45])
s2f = make_ranges(lines[47:96])
f2w = make_ranges(lines[98:130])
w2l = make_ranges(lines[132:179])
l2t = make_ranges(lines[181:202])
t2h = make_ranges(lines[204:241])
h2l = make_ranges(lines[243:])

location = 0
print('This might take a while, but we know from part 1 that the upper bound is 57075758.')
while True:
    if location % 1000000 == 0:
        print(f'Current location: {location}', end='\r')
    humidity = get_inverse_map(location, h2l)
    temperature = get_inverse_map(humidity, t2h)
    light = get_inverse_map(temperature, l2t)
    water = get_inverse_map(light, w2l)
    fertilizer = get_inverse_map(water, f2w)
    soil = get_inverse_map(fertilizer, s2f)
    seed = get_inverse_map(soil, s2s)
    if check_number_in_range_list(seed, range_list):
        print(f'The seed with number {seed} can be obtained from location {location}.')
        exit()
    location += 1

