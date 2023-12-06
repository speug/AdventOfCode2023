from pathlib import Path
import sys
import numpy as np

curr_file = Path(__file__)
sys.path.append(str(curr_file.parent.parent))
from utils import read_lines
from copy import deepcopy


def parse_input_lines(lines):
    seeds = [int(x) for x  in lines[0].split(': ')[1].split()]
    mapping_dicts = []
    current_ranges = []
    current_dict = {}
    for l in lines[2:]:
        if 'map' in l:
            current_dict['source'] = l.split('-to-')[0]
            current_dict['destination'] = l.split('-to-')[1].split()[0]
        # line is empty
        elif not l:
            current_dict['ranges'] = current_ranges
            mapping_dicts.append(deepcopy(current_dict))
            current_ranges = []
            current_dict = {}
        else:
            destination_start, source_start, number = [int(x) for x in l.split()]
            current_ranges.append((destination_start, source_start, number))
    current_dict['ranges'] = current_ranges
    mapping_dicts.append(deepcopy(current_dict))
    
    return seeds, mapping_dicts


def map_number(to_map, ranges):
    for d_start, s_start, num in ranges:
        if (to_map >= s_start) and (to_map < s_start + num):
            return d_start + (to_map - s_start)
    return to_map


input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
# input = curr_file.parent / 'input'
lines = read_lines(input)
seeds, mapping_dicts = parse_input_lines(lines)
for mp in mapping_dicts:
    print(mp)
mapped = seeds
for mp in mapping_dicts:
    print(mapped)
    for i, num in enumerate(mapped):
        mapped[i] = map_number(num, mp['ranges'])
print(f'Lowest location number is {np.min(mapped)}')

# part 2
# for each range: map entire range, split if necessary until you get all the location ranges; find minimum
# do this likely recursively?
def combine_ranges(check_range, map_range):
    # return tuple of overlapping/nonoverlapping portion and the rest of check_range (as list)
    # now we have 4 possibilities:
    # 1. map_range is contained within check_range, splitting into three
    if (map_range[0] >= check_range[0]) and (map_range[1] < check_range[1]):
        overlap = map_range

    # 2. check_range overlaps with the start of map_range
    # 3. check_range overlaps with the end of map_range
    # 4. check_range is either entirely inside or outside the map_range; no split


max_idx = len(mapping_dicts)
def check_range(range, maps, map_idx):
    if map_idx == max_idx:
        return range
    mp = maps[map_idx]
    map_ranges = mp['ranges']
    sub_ranges = []
    stack = [range]
    for _, s_start, num in map_ranges:
        mr = (s_start, s_start + num)
        # for each map_range: map what is applicable, then just 1-to-1 map the rest
        # we could map the applicable range recursively, then put the remaining subranges to stack to process


