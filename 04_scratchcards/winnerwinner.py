from pathlib import Path
import sys
import numpy as np

curr_file = Path(__file__)
sys.path.append(str(curr_file.parent.parent))
from utils import read_lines


def parse_card(card):
    card_id = int(card.split()[1][:-1])
    numbers = card.split(": ")[1]
    winning_numbers, card_numbers = numbers.split(" | ")
    winning_numbers = [int(x) for x in winning_numbers.split()]
    card_numbers = [int(x) for x in card_numbers.split()]
    return card_id, winning_numbers, card_numbers


def calculate_matches(card_numbers, winning_numbers):
    matches = 0
    for cn in card_numbers:
        matches += cn in winning_numbers
    return matches


# input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
# """
input = curr_file.parent / "input"
lines = read_lines(input)
cards = [parse_card(l) for l in lines]
total_points = 0
for card_id, card_numbers, winning_numbers in cards:
    matches = calculate_matches(card_numbers, winning_numbers)
    total_points += int(2 ** (matches - 1))
print(f"Total points: {total_points}")

# part 2
# now we need to collect multipliers for cards
n_cards = len(cards)
total_cards = np.ones(n_cards)
for card_id, card_numbers, winning_numbers in cards:
    matches = calculate_matches(card_numbers, winning_numbers)
    if matches:
        if card_id + matches < n_cards:
            total_cards[card_id: card_id + matches] += total_cards[card_id - 1]
        else:
            total_cards[card_id:] += total_cards[card_id - 1]
print(f"Total cards: {int(np.sum(total_cards))}")
