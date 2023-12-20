from __future__ import annotations
from pathlib import Path
import sys
import numpy as np

curr_dir = Path(__file__).parent
sys.path.append(str(curr_dir.parent))
from utils import read_lines, get_neighbours


class Node:
    def __init__(self, pipe_type, coordinates, is_start=False):
        self.pipe_type = pipe_type
        self.coordinates = coordinates
        self.is_start = is_start
        self.connections = set()
        match pipe_type:
            case "|":
                offsets = [(-1, 0), (1, 0)]
            case "-":
                offsets = [(0, -1), (0, 1)]
            case "L":
                offsets = [(-1, 0), (0, 1)]
            case "J":
                offsets = [(-1, 0), (0, -1)]
            case "7":
                offsets = [(1, 0), (0, -1)]
            case "F":
                offsets = [(1, 0), (0, 1)]
            case "S":
                offsets = [(0, 0)]
        self.neighbouring_coordinates = [
            (coordinates[0] + offset[0], coordinates[1] + offset[1])
            for offset in offsets
        ]
        self.start_connection = None if not is_start else True
        self.start_distance = np.inf if not is_start else 0

    def check_connection(self, other: Node):
        dist = np.abs(self.coordinates[0] - other.coordinates[0]) + np.abs(
            self.coordinates[1] - other.coordinates[1]
        )
        # other node is too far
        if dist > 1.0:
            return False
        if self.is_start:
            return True
        if other.coordinates in self.neighbouring_coordinates:
            return True
        return False

    def connect(self, other: Node):
        # check if connection is compatible
        if other is None:
            return
        if self.check_connection(other) and other.check_connection(self):
            self.connections.add(other)
            if self not in other.connections:
                other.connect(self)

    def next(self, prev: Node):
        if prev not in self.connections:
            raise ValueError(
                f"Invalid move from {prev.coordinates} to {self.coordinates} "
                + "(not connected)!"
            )
        if len(self.connections) == 1:
            return None
        else:
            return [x for x in self.connections if x != prev][0]

    def distance_to_start(self, prev: Node = None):
        if self.is_start:
            return 0
        elif not self.start_connection:
            return np.inf
        elif self.start_distance is not None:
            return self.start_distance
        elif prev is None:
            return np.min([x.distance_to_start(self) for x in self.connections]) + 1
        else:
            return self.next(prev).distance_to_start(self) + 1

    def __str__(self):
        return f"{self.pipe_type}"

    def __repr__(self):
        return self.__str__()


print_grid = False
input = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
input = curr_dir / "input"
lines = read_lines(input)
grid = np.array([list(x) for x in lines])
print(grid)
node_grid = np.empty(grid.shape, dtype=object)
n, m = grid.shape
start_idx = None
# add nodes to grid
for i in range(n):
    for j in range(m):
        if grid[i, j] == ".":
            node_grid[i, j] = None
        elif grid[i, j] == "S":
            node_grid[i, j] = Node("S", (i, j), True)
            start_idx = (i, j)
        else:
            node_grid[i, j] = Node(grid[i, j], (i, j), False)

# connect nodes in grid
for i in range(n):
    for j in range(m):
        if node_grid[i, j] is None:
            continue
        match node_grid[i, j].pipe_type:
            # cannot connect willy-nilly...
            case "|":
                if i != 0:
                    node_grid[i, j].connect(node_grid[i - 1, j])
                if i != m - 1:
                    node_grid[i, j].connect(node_grid[i + 1, j])
            case "-":
                if j != 0:
                    node_grid[i, j].connect(node_grid[i, j - 1])
                if j != m - 1:
                    node_grid[i, j].connect(node_grid[i, j + 1])
            case "L":
                if i != 0:
                    node_grid[i, j].connect(node_grid[i - 1, j])
                if j != m - 1:
                    node_grid[i, j].connect(node_grid[i, j + 1])
            case "J":
                if i != 0:
                    node_grid[i, j].connect(node_grid[i - 1, j])
                if j != 0:
                    node_grid[i, j].connect(node_grid[i, j - 1])
            case "7":
                if i != m - 1:
                    node_grid[i, j].connect(node_grid[i + 1, j])
                if j != 0:
                    node_grid[i, j].connect(node_grid[i, j - 1])
            case "F":
                if i != m - 1:
                    node_grid[i, j].connect(node_grid[i + 1, j])
                if j != m - 1:
                    node_grid[i, j].connect(node_grid[i, j + 1])

# spawn walkers from start
# for connection in start connections
# walk; if walk goes back to start, mark all walked as valid connections
sn = node_grid[start_idx]
for cn in sn.connections:
    path = [sn, cn]
    while True:
        next_node = path[-1].next(path[-2])
        if next_node.is_start:
            for i, node in enumerate(path[1:]):
                node.start_connection = True
                if node.start_distance > i + 1:
                    node.start_distance = i + 1
            break
        elif next_node is None:
            for node in path[1:]:
                node.start_connection = False
            break
        else:
            path.append(next_node)

distances = []
for i in range(n):
    for node in node_grid[i, :]:
        if node is not None and node.start_connection:
            distances.append(node.start_distance)
print(f"Max distance from the start is {np.max(distances)}")


if print_grid:
    for i in range(n):
        to_print = ""
        for node in node_grid[i, :]:
            if node is None:
                to_print += "."
            elif node.start_connection:
                to_print += "c"
            else:
                to_print += "u"
        print(to_print)
