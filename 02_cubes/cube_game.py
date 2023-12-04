from pathlib import Path
import sys
import numpy as np

curr_file = Path(__file__)
sys.path.append(str(curr_file.parent.parent))
from utils import read_lines
from collections import defaultdict


def parse_game(line):
    splitted = line.split(" ")
    game_id = int(splitted[1][:-1])
    rounds = line.split(": ")[1].split("; ")
    rounds_parsed = []
    for round in rounds:
        sets = []
        for set in round.split(", "):
            amount, color = set.split(" ")
            sets.append((int(amount), color))
        rounds_parsed.append(sets)
    return game_id, rounds_parsed


def check_max(parsed_game, inventory):
    _, rounds = parsed_game
    for round in rounds:
        for amount, color in round:
            if color not in inventory:
                return False
            elif inventory[color] < amount:
                return False
    return True


input = curr_file.parent / "input"
lines = read_lines(input)
parsed = [parse_game(l) for l in lines]
inventory = {"red": 12, "green": 13, "blue": 14}
valid_games = 0
for game in parsed:
    if check_max(game, inventory):
        valid_games += game[0]
print(f"Sum of valid game ids is {valid_games}.")

# part 2
def minimum_sets(parsed_game):
    minimum_inventory = defaultdict(int)
    for round in parsed_game[1]:
        for amount, color in round:
            if minimum_inventory[color] < amount:
                minimum_inventory[color] = amount
    return minimum_inventory


powers = 0
for game in parsed:
    inventory = minimum_sets(game)
    powers += np.product([x for x in inventory.values()])
print(f"Cube power is {powers}")
