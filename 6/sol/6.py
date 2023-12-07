import sys


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def p1(races: list[tuple[int, int]]):
    ans = 1
    for p in races:
        time, dist = p
        ways = [i for i in range(time + 1) if (time - i) * i > dist]
        ans *= len(ways)
    return ans


def solve(input: list[str]):
    # Part 1:
    # time = list(
    #     map(
    #         lambda s: int(s),
    #         filter(
    #             lambda s: s is not None and s.strip() != "",
    #             input[0].split(":")[1].strip().split(" "),
    #         ),
    #     )
    # )

    # dist = list(
    #     map(
    #         lambda s: int(s),
    #         filter(
    #             lambda s: s is not None and s.strip() != "",
    #             input[1].split(":")[1].strip().split(" "),
    #         ),
    #     )
    # )
    
    # races = list(zip(time, dist))
    time = int("".join(input[0].split(":")[1].strip().split(" ")))
    dist = int("".join(input[1].split(":")[1].strip().split(" ")))
    race = (time, dist)
    print(race)
    return p1([race])


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 6.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
