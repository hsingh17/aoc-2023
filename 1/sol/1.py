import sys
import typing

NUMS_SPELLED_OUT: dict[str, int] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def find_spelled_out_possible(input: str) -> list[list[int]]:
    min_idx = 1e9
    min_val = 1e9
    max_idx = -1
    max_val = -1

    for k, v in NUMS_SPELLED_OUT.items():
        idxs = []
        i = 0

        # This loop is needed in case k (spelled out number)
        # Shows up multiple times in a string
        while i < len(input):
            find = input.find(k, i)
            if (find == -1):
                break
            idxs.append(find)
            i += len(k)

        if (not idxs or len(idxs) == 0) :
            continue

        min_idx = min(min_idx, idxs[0])
        if min_idx == idxs[0]:
            min_val = v

        max_idx = max(max_idx, idxs[-1])
        if max_idx == idxs[-1]:
            max_val = v

    return [[min_idx, min_val], [max_idx, max_val]]


def find_digits_possible(input: str) -> list[list[int]]:
    min_idx = 1e9
    min_val = 1e9
    max_idx = -1
    max_val = -1

    for idx, c in enumerate(input):
        if not c.isnumeric():
            continue

        min_idx = min(min_idx, idx)
        if min_idx == idx:
            min_val = int(c)

        max_idx = max(min_idx, idx)
        if max_idx == idx:
            max_val = int(c)

    return [[min_idx, min_val], [max_idx, max_val]]


def solve(input: list[str]) -> int:
    calibration_value = 0
    for idx, line in enumerate(input):
        spelled_out_possible = find_spelled_out_possible(line)
        digits_possible = find_digits_possible(line)

        first_digit = (
            spelled_out_possible[0][1]
            if spelled_out_possible[0][0] < digits_possible[0][0]
            else digits_possible[0][1]
        )

        last_digit = (
            spelled_out_possible[1][1]
            if spelled_out_possible[1][0] > digits_possible[1][0]
            else digits_possible[1][1]
        )

        print(f"{idx+1}: {first_digit}{last_digit}")
        calibration_value += int(f"{first_digit}{last_digit}")

    return calibration_value


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 1.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    ret = solve(input)
    print(ret)


if __name__ == "__main__":
    main()
