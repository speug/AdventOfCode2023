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
    # print(f'At {pointer}. Stepping {instruction} to {tree[pointer][instruction]}')
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
    goal_indices = [i+1 for i, x in enumerate(traversed[idx_of_loop:]) if x[-1] == 'Z']
    print(f'Ghost from {start_node}:')
    print(f'\tHits first goal after {steps_until_first_goal} steps')
    print(f'\tEnters a loop after {steps_until_loop} steps')
    print(f'\tAfter that, hits a goal after {goal_indices} steps')
    loop_length = len(traversed) - idx_of_loop
    return steps_until_first_goal, loop_length



# tree, instructions = parse_maps(read_lines(input))
pointers = [x for x  in tree.keys() if x[-1] == 'A']
for s in pointers:
    steps_to_goal, loop_length = find_cycle(s, tree, instructions)