import sys
import typing


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def extrapolate_forward(history: list[int]):
    history.append(0)
    while not all(num == 0 for num in history[: len(history) - 1]):
        temp = [v - history[i - 1] for i, v in enumerate(history) if i != 0]
        history = temp
    return history[len(history) - 1] * -1


def extrapolate_backward(history: list[int]):
    history.insert(0, 0)
    levels = 0
    while not all(num == 0 for num in history[1 : len(history)]):
        temp = [v - history[i - 1] for i, v in enumerate(history) if i != 0]
        levels += 1
        history = temp
    return history[0] * (1 if levels % 2 else -1)


def solve(input: list[str]):
    histories = [list(map(lambda i: int(i), s.split(" "))) for s in input]
    ret = 0
    for history in histories:
        ret += extrapolate_backward(history)
    return ret


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 9.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
