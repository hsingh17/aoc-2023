import sys
import math
from typing import Dict


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def solve(input: list[str]):
    cards: Dict[int, int] = dict()
    for i, card in enumerate(input):
        # Initialize how many instances we have of the current scratchcard
        instances = cards.get(i + 1)
        cards.update({i + 1: 1 if instances is None else instances + 1})
        instances = cards.get(i + 1)

        # Find out how many winning numbers we have
        info = card.split(":")[1].split("|")
        winning, mine = set(info[0].strip().split(" ")), set(info[1].strip().split(" "))

        winning = set(filter(lambda s: (s is not None and s != ""), winning))
        mine = set(filter(lambda s: (s is not None and s != ""), mine))
        my_winner = mine.intersection(winning)  # Find how many winning numbers I have

        print(cards)
        # Based on how many cards we won iterate over the next "cards_won" cards
        # and update them to add on how many instances we have of the current card (since each instance wins 1)
        for j in range(1, len(my_winner) + 1):
            next_game = i + 1 + j
            cur = cards.get(next_game)
            cards.update({next_game: instances if cur is None else instances + cur})
    return sum(cards.values())


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 template.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
