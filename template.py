import sys
import typing


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def solve(input: list[str]):
    pass


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 template.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    solve(input)


if __name__ == "__main__":
    main()
