from pathlib import Path
import sys
import numpy as np

curr_file = Path(__file__)
sys.path.append(str(curr_file.parent.parent))
from utils import read_lines, get_neighbours


# nice edgecase tester from
# https://www.reddit.com/r/adventofcode/comments/189q9wv/2023_day_3_another_sample_grid_to_use/
# input = """12.......*..
# +.........34
# .......-12..
# ..78........
# ..*....60...
# 78.........9
# .5.....23..$
# 8...90*12...
# ............
# 2.2......12.
# .*.........*
# 1.1..503+.56"""
input = curr_file.parent / "input"
lines = read_lines(input)
grid = []
for line in lines:
    grid.append(list(line))
grid = np.array(grid)

# parse grid
part_numbers = []
max_i, max_j = grid.shape
for i in range(max_i):
    digits = []
    coords = []
    for j in range(max_j):
        if grid[i, j].isdigit():
            digits.append(grid[i, j])
            coords.append((i, j))
        if not grid[i, j].isdigit() or j == max_j - 1:
            if digits:
                number = int("".join(digits))
                part_numbers.append((number, coords))
                digits = []
                coords = []

# part 1
part_sum = 0
for number, digit_coords in part_numbers:
    found = False
    coord_set = set()
    for i, j in digit_coords:
        neighbours, coords = get_neighbours(grid, i, j, diagonals=True)
        coord_set = coord_set | set(coords)
    coord_set = coord_set - set(digit_coords)
    for coord in coord_set:
        if grid[coord] != "." and not grid[coord].isdigit():
            part_sum += number
            break

print(f"Sum of part numbers is {part_sum}")

# part 2
# get gear candidates
gear_is, gear_js = np.where(grid == "*")
gear_ratios = 0
start_idx = 0
for i, j in zip(gear_is, gear_js):
    _, n_coords = get_neighbours(grid, i, j, diagonals=True)
    overlapping_numbers = []
    for number, number_coords in part_numbers[start_idx:]:
        # if the number row is two above, we can move the start of the search
        if number_coords[0][0] < i - 1:
            start_idx += 1
        # if the number row is two below, we will no longer find neigbouring digits
        if number_coords[0][0] > i + 1:
            break
        intersection = set(n_coords) & set(number_coords)
        if intersection:
            overlapping_numbers.append(number)
            if len(overlapping_numbers) > 2:
                break
    if len(overlapping_numbers) == 2:
        gear_ratios += overlapping_numbers[0] * overlapping_numbers[1]
print(f"Sum of gear ratios is {gear_ratios}")
