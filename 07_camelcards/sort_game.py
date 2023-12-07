from pathlib import Path
import sys
import numpy as np

curr_file = Path(__file__)
sys.path.append(str(curr_file.parent.parent))
from utils import read_lines
from functools import cmp_to_key


card_vals = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10
}


def cards_to_int(hand):
    out = np.zeros(5, dtype=int)
    for i, c in enumerate(list(hand)):
        if c.isdigit():
            out[i] = int(c)
        else:
            out[i] = card_vals[c]
    return out


def evaluate_hand(hand_str, card_list):
    _, counts = np.unique(card_list, return_counts=True)
    counts = list(sorted(counts, reverse=True))
    match counts:
        # five-of-a-kind
        case [5]:
            return 6
        # four-of-a-kind
        case [4, 1]:
            return 5
        # full house
        case [3, 2]:
            return 4
        # three-of-a-kind
        case [3, 1, 1]:
            return 3
        # two pairs
        case [2, 2, 1]:
            return 2
        # one pair
        case [2, 1, 1, 1]:
            return 1
        # high
        case [1, 1, 1, 1, 1]:
            return 0


def compare_hands(hand_bid1, hand_bid2, eval_fun=evaluate_hand):
    hand1_str = hand_bid1[0]
    hand2_str = hand_bid2[0]
    hand1, hand2 = cards_to_int(hand1_str), cards_to_int(hand2_str)
    score1, score2 = eval_fun(hand1_str, hand1), eval_fun(hand2_str, hand2)
    if score1 != score2:
        return score1 - score2
    else:
        for c1, c2 in zip(hand1, hand2):
            if c1 != c2:
                return c1 - c2
        raise ValueError(f'{hand1} and {hand2} are of equal value!')


input = """AAAAA 2
22222 3
AAAAK 5
22223 7
AAAKK 11
22233 13
AAAKQ 17
22234 19
AAKKQ 23
22334 29
AAKQJ 31
22345 37
AKQJT 41
23456 43"""
input = curr_file.parent / 'input'
lines = read_lines(input)
split = [x.split() for x in lines]
sorted_hands = sorted(split, key=cmp_to_key(compare_hands))
total_winnings = 0
for i, (_, bid) in enumerate(sorted_hands):
    total_winnings += (i + 1) * int(bid)
print(f'Total winnings are {total_winnings}')

# part 2
# now we want to map Js to jokers
card_vals['J'] = 1

def evaluate_hand_with_jokers(hand_str, card_list):
    hand_list = cards_to_int(hand_str)
    if 'J' not in hand_str or hand_str == 'JJJJJ':
        return evaluate_hand(hand_str, hand_list)

    other_cards_in_hand = set([x for x in list(hand_str) if x != 'J']) 
    max_value = 0
    for c in other_cards_in_hand:
        new_str = hand_str.replace('J', c)
        new_list = cards_to_int(new_str)
        score = evaluate_hand(new_str, new_list)
        if score > max_value:
            max_value = score
    return max_value


sorted_hands = sorted(split,
                      key=cmp_to_key(
    lambda a, b: compare_hands(a, b, evaluate_hand_with_jokers)))
total_winnings = 0
for i, (_, bid) in enumerate(sorted_hands):
    total_winnings += (i + 1) * int(bid)
print(f'Total winnings with jokers are {total_winnings}')
