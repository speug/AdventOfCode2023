from pathlib import Path
import sys
import numpy as np

curr_file = Path(__file__)
sys.path.append(str(curr_file.parent.parent))
from utils import read_lines

input = """Time:      7  15   30
Distance:  9  40  200
"""
input = curr_file.parent / 'input'
lines = read_lines(input)
times = [int(x) for x in lines[0].split(':')[1].split(' ') if x != '']
distances = [int(x) for x in lines[1].split(':')[1].split(' ') if x != '']

# part 1
# just brute-force
valid_solutions = np.zeros(len(times), dtype=int)
for i in range(len(times)):
    time = times[i]
    record_dist = distances[i]
    for t in range(time):
        d = t * (time - t)
        if d > record_dist:
            valid_solutions[i] += 1
print(f'Product of valid solutions is {np.product(valid_solutions)}')
# part 2
# binary search the start and end points

def find_hold_times(time_limit, record_distance):
    # find leftmost (time to start to hold the button) record time
    left, right = 0, time_limit // 2
    while left < right:
        middle = (left + right) // 2
        if middle * (time_limit - middle) < record_distance:
            left = middle + 1
        else:
            right = middle
    hold_start = left
    # find rightmost
    left, right = time_limit // 2 + 1, time_limit
    while left < right:
        middle = (left + right) // 2
        if middle * (time_limit - middle) > record_distance:
            left = middle + 1
        else:
            right = middle
    hold_end = right
    return hold_start, hold_end


hs, ht = find_hold_times(int(''.join([str(x) for x in times])),
                int(''.join([str(x) for x in distances])))
print(hs, ht)
print(ht - hs)