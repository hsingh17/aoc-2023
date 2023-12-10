import sys
from enum import Enum


class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class Hand:
    def __init__(self, s: str) -> None:
        splt = s.split(" ")
        self.hand = splt[0]
        self.bid = int(splt[1])
        self.type: HandType = self.__get_hand_type()

    def __get_hand_type(self) -> int:
        freq: dict[str, int] = {card: self.hand.count(card) for card in set(self.hand)}
        N = len(freq.keys())

        type_before_jokers = None
        if N == 1:
            type_before_jokers = HandType.FIVE_OF_A_KIND
        elif N == 4:
            type_before_jokers = HandType.ONE_PAIR
        elif N == 5:
            type_before_jokers = HandType.HIGH_CARD
        elif N == 2:
            if 4 in freq.values():
                type_before_jokers = HandType.FOUR_OF_A_KIND
            else:
                type_before_jokers = HandType.FULL_HOUSE
        elif N == 3:
            if 3 in freq.values():
                type_before_jokers = HandType.THREE_OF_A_KIND
            else:
                type_before_jokers = HandType.TWO_PAIR

        jokers = freq.pop("J", None)

        # No jokers in hand
        if not jokers or type_before_jokers == HandType.FIVE_OF_A_KIND:
            return type_before_jokers

        max_freq = jokers + max(freq.values())
        if max_freq == 5:
            return HandType.FIVE_OF_A_KIND
        elif max_freq == 4:
            return HandType.FOUR_OF_A_KIND
        elif max_freq == 3:
            if type_before_jokers == HandType.ONE_PAIR:
                return HandType.THREE_OF_A_KIND
            elif type_before_jokers == HandType.TWO_PAIR:
                return HandType.FULL_HOUSE
        elif max_freq == 2:
            return HandType.ONE_PAIR

        raise Exception(f"Case not considered! {self.hand}")

    def __lt__(self, other: "Hand"):
        cards = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
        # Hand type is not the same
        if self.type != other.type:
            return self.type.value < other.type.value

        # Hand type is same
        l_idx = None
        r_idx = None

        for l, r in zip(self.hand, other.hand):
            l_idx, r_idx = cards.index(l), cards.index(r)
            if l_idx != r_idx:
                break

        return l_idx > r_idx

    def __repr__(self) -> str:
        return self.hand

    def __str__(self) -> str:
        return self.hand


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def solve(input: list[str]):
    hands = [Hand(s) for s in input]
    hands.sort()
    ret = 0
    for i, hand in enumerate(hands):
        ret += (i + 1) * hand.bid
    return ret


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 7.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
