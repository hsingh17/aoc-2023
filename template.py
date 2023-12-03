import sys
import typing


def read_puzzle_input() -> list[str]:
    with open("../input/input.txt", "r") as f:
        return f.read().splitlines()


def solve(input: list[str]):
    pass


def main():
    args = sys.argv
    input: list[str] = read_puzzle_input()
    solve(input)


if __name__ == "__main__":
    main()
