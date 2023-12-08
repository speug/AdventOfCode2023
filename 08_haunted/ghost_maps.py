from math import lcm
from pathlib import Path
import sys
import numpy as np
from itertools import cycle

curr_dir = Path(__file__).parent
sys.path.append(str(curr_dir.parent))
from utils import read_lines


def parse_maps(lines):
    instructions = list(lines[0].rstrip())
    tree = {}
    for l in lines[2:]:
        node, children = l.split(' = ')
        left, right = children.split(', ')
        # trim parentheses
        left = left[1:]
        right = right[:-1]
        tree[node] = {'L': left, 'R': right}
    return tree, instructions


input = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
input = curr_dir / 'input'
lines = read_lines(input)
tree, instructions = parse_maps(lines)
root = 'AAA'
goal = 'ZZZ'
pointer = root
steps = 0
for instruction in cycle(instructions):
    if pointer == goal:
        break
    pointer = tree[pointer][instruction]
    steps += 1
print(f'Took a total of {steps} steps.')

# part 2
# try to brute-force
# otherwise need to record length of loops and do some number shenannigans
# also, looks like there is only one goal per cycle


def find_cycle(start_node, tree, instructions):
    traversed = []
    pointer = start_node
    steps_until_loop = 0
    steps_until_first_goal = None
    for instruction in cycle(instructions):
        if pointer[-1] == 'Z' and pointer in traversed:
            break
        if pointer[-1] == 'Z' and steps_until_first_goal is None:
            steps_until_first_goal = steps_until_loop
        traversed.append(pointer)
        pointer = tree[pointer][instruction]
        steps_until_loop += 1
    idx_of_loop = traversed.index(pointer)
    goal_indices = [i+1 for i, x in enumerate(traversed[idx_of_loop:])
                    if x[-1] == 'Z']
    loop_length = len(traversed) - idx_of_loop
    return steps_until_first_goal, loop_length, goal_indices


def extended_gdc(a, b):
    # https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_r, old_s, old_t


def sync_with_offset(period1, offset1, period2, offset2):
    gdc, s, t = extended_gdc(period1, period2)
    offset_diff = offset1 - offset2
    od_mult, od_remainder = divmod(offset_diff, gdc)
    if od_remainder:
        raise ValueError('The ghosts will never sync!')
    comb_period = period1 // gdc * period2
    comb_offset = (offset1 - s * od_mult * period1) % comb_period
    return comb_period, comb_offset


# all both the methods above are useless
# BECAUSE THERE IS A SECRET PROPERTY that the cycle period == offset
# for all ghosts
pointers = [x for x in tree.keys() if x[-1] == 'A']
cycle_properties = []
for s in pointers:
    _, loop_length, _ = find_cycle(s, tree, instructions)
    cycle_properties.append(loop_length)

# loop over list of cycle properties, combine as you goal
print(f'All ghosts sync up after {lcm(*cycle_properties)} steps.')
