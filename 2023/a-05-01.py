with open('z-05-01-input.txt', 'r') as f:
    lines = f.readlines()

seeds = lines[0].split(':')[1].split()
seeds = [int(s) for s in seeds]

def get_map(number, l):
    for line in l:
        destination, start, length = [int(s) for s in line.split()]
        if (start < number) and (number < start+length):
            diff = number - start
            return destination + diff

    return number


location_list = []
for seed in seeds:
    soil = get_map(seed, lines[3:45])
    fertilizer = get_map(soil, lines[47:96])
    water = get_map(fertilizer, lines[98:130])
    light = get_map(water, lines[132:179])
    temperature = get_map(light, lines[181:202])
    humidity = get_map(temperature, lines[204:241])
    location = get_map(humidity, lines[243:])
    location_list.append(location)

print(f'The solution is: {min(location_list)}')

