from typing import Union
from pathlib import Path


def read_lines(input: Union[Path, str]):
    if isinstance(input, Path):
        with open(input, 'r') as f:
            lines = f.readlines()
        return lines
    else:
        lines = input.split('\n')
        if lines[-1] == '\n' or lines[-1] == '':
            lines = lines[:-1]
        return lines
