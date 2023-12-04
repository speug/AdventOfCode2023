from pathlib import Path
import sys

curr_file = Path(__file__)
sys.path.append(str(curr_file.parent.parent))
from utils import read_lines


digit_names = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def check_subline(word, check_idx):
    if word[check_idx].isdigit():
        return word[check_idx]
    for dname in digit_names:
        if dname in word:
            return digit_names[dname]
    return False


def process_line(line):
    left = 0
    right = len(line) - 1
    while not check_subline(line[: left + 1], -1):
        left += 1
    left_digit = check_subline(line[: left + 1], -1)
    while not check_subline(line[right:], 0):
        right -= 1
    right_digit = check_subline(line[right:], 0)
    return int("".join((left_digit, right_digit)))


input = curr_file.parent / "input"
lines = read_lines(input)
val = 0
for line in lines:
    val += process_line(line)

print(f"Calibration value is {val}")

# part 2
# replace digit names with digits (first pass)
val = 0
for line in lines:
    val += process_line(line)

print(f"Calibration value (when accounting for digit names) is {val}")
