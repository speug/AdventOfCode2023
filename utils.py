from typing import Union
from pathlib import Path
import numpy as np


def read_lines(input: Union[Path, str]):
    if isinstance(input, Path):
        with open(input, 'r') as f:
            lines = f.readlines()
        lines = [l.rstrip() for l in lines]
        return lines
    else:
        lines = input.split('\n')
        if lines[-1] == '\n' or lines[-1] == '':
            lines = lines[:-1]
        return lines


def get_neighbours(grid, i, j, diagonals=False, return_coords=True):
    max_i, max_j = grid.shape
    out = [None] * 8 if diagonals else [None] * 4
    coords = [(i-1, j),
              (i+1, j),
              (i, j-1),
              (i, j+1)]
    if (i != 0):
        out[0] = grid[i-1, j]
    if (i < max_i-1):
        out[1] = grid[i+1, j]
    if (j != 0):
        out[2] = grid[i, j-1]
    if (j < max_j-1):
        out[3] = grid[i, j+1]
    if diagonals:
        # NW
        diag_coords = [(i-1, j-1), (i-1, j+1), (i+1, j+1), (i+1, j-1)]
        coords += diag_coords
        if (i != 0) and (j!= 0):
            out[4] = grid[i-1, j-1]
        # NE
        if (i != 0) and (j != max_j - 1):
            out[5] = grid[i-1, j+1]
        # SE
        if (i != max_i - 1) and (j != max_j - 1):
            out[6] = grid[i+1, j+1]
        # SW
        if (i != max_i - 1) and (j != 0):
            out[7] = grid[i+1, j-1]
    if return_coords:
        coords = [c for c, x in zip(coords, out) if x is not None]
        out = [x for x in out if x is not None]
        return out, coords
    else:
        out = [x for x in out if x is not None]
        return out
