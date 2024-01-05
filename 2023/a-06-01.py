'''
This puzzle can be solved using mathematical analysis.
The race can be divided in two stages:
from 0 to t, the boat is charged,
from t to T, the boat is travelling.
The distance d travelled is expressed as a function of time t=(T-t_a) and velocity v=t_a.

    d(t) = t * (T-t)

which forms a parabola with a maximum at t_max = T/2.
In order to win against the winning time W, the following inequality must hold:

    d(t) > W    or      d(t) >= W+1 since we deal with integer values.

        dw(t) = d(t)-(W+1) = -t^2 + T*t - (W+1) >= 0

The range of possible winning values is given by the difference between the zero points of dw(t).

    x1 = (-T + sqrt(T^2-4*(-1)*(-1*(W+1))) / (2)
    x2 = (-T - sqrt(T^2-4*(-1)*(-1*(W+1))) / (2)

    n_winning = (floor(x1)-ceil(x2)) + 1
'''

from math import sqrt, ceil, floor
with open('z-06-01-input.txt', 'r') as f:
    lines = f.readlines()

times = [int(s) for s in lines[0].split()[1:]]
distances = [int(s) for s in lines[1].split()[1:]]

def get_possible_distances(time):
    return [x * (time - x) for x in range(time+1)]

product = 1
for t, d in zip(times, distances):
    winning_combinations = [possible_distance for possible_distance in get_possible_distances(t) if possible_distance > d]
    product *= len(winning_combinations)

print(product)

product = 1
for t, d in zip(times, distances):
    x1 = t/2 + sqrt(t**2 - 4*(d+1)) / 2
    x2 = t/2 - sqrt(t**2 - 4*(d+1)) / 2
    winning_combinations = (floor(x1) - ceil(x2)) + 1
    # winning_combinations = [possible_distance for possible_distance in get_possible_distances(t) if possible_distance > d]
    product *= winning_combinations

print(product)
