from pathlib import Path
import sys
import numpy as np

curr_dir = Path(__file__).parent
sys.path.append(str(curr_dir.parent))
from utils import read_lines


def predict_next(history, previous=False):
    diffs = [history, np.diff(history)]
    while not np.all(diffs[-1] == 0):
        diffs.append(np.diff(diffs[-1]))
    new_vals = [None] * len(diffs)
    for i, d in enumerate(reversed(diffs)):
        if i == 0:
            new_vals[i] = 0
        else:
            if previous:
                new_vals[i] = d[0] - new_vals[i - 1]
            else:
                new_vals[i] = d[-1] + new_vals[i - 1]
    return new_vals


input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
input = curr_dir / "input"
lines = read_lines(input)
check_value = 0
prev_vals = 0
for line in lines:
    history = np.array([int(x) for x in line.split() if x != " "], dtype=int)
    predicted = predict_next(history)
    previous = predict_next(history, previous=True)
    check_value += predicted[-1]
    prev_vals += previous[-1]
print(f"Total of predictions is {check_value}")
print(f"Total of previous is {prev_vals}")
