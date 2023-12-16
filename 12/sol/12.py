import sys
import typing

DP: dict[str, list[int]] = {}


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def count_groups(row: list[str]) -> list[int]:
    group_arrangement = []
    i, N = 0, len(row)

    while i < N:
        in_group = 0
        while i < N and row[i] == "#":
            in_group += 1
            i += 1

        if in_group != 0:
            group_arrangement.append(in_group)
        else:
            i += 1

    return group_arrangement


def parse_input(input: list[str]) -> list[tuple[list[str], list[int]]]:
    return [
        (
            list(s.split(" ")[0]),
            list(map(lambda num: int(num), s.split(" ")[1].split(","))),
        )
        for s in input
    ]


def find_arrangements(p: tuple[list[str], list[int]]):
    def recurse(i: int):
        # Base case 1: Reached the end, so check the groupings
        # If current groupings match the desired, return True
        # Else return False
        if i == N:
            if count_groups(spring) == desired_group:
                nonlocal arrangments
                arrangments += 1
            return

        if spring[i] != "?":
            recurse(i + 1)
        else:
            # At each unknown spot, we can either have an operational spring or damaged spring
            spring[i] = "."
            recurse(i + 1)

            spring[i] = "#"
            recurse(i + 1)

            spring[i] = "?"

    arrangments = 0
    spring, desired_group = p
    N = len(spring)
    recurse(0)

    return arrangments


def solve(input: list[str]):
    parsed_input = parse_input(input)
    ret = 0
    for p in parsed_input:
        ret += find_arrangements(p)
    return ret


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 12.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
