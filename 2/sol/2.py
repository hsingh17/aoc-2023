import sys
import typing

BAG: dict[str, int] = {"red": 12, "green": 13, "blue": 14}


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


# Part 1
# def is_game_possible(moves: str) -> bool:
#     moves_list: list[str] = moves.split(";")
#     is_game_possible = True
#     for move in moves_list:
#         cubes: list[str] = move.split(",")
#         for cube in cubes:
#             split = cube.strip().split(" ")
#             num, color = int(split[0]), split[1]
#             if num > BAG.get(color):
#                 is_game_possible = False
#                 break
#     print(is_game_possible)
#     return is_game_possible


# Part 2
def find_power(moves: str) -> int:
    moves_list: list[str] = moves.split(";")
    max_red = max_green = max_blue = 1

    for move in moves_list:
        cubes: list[str] = move.split(",")
        for cube in cubes:
            split = cube.strip().split(" ")
            num, color = int(split[0]), split[1]
            if color == "green":
                max_green = max(num, max_green)
            elif color == "red":
                max_red = max(num, max_red)
            else:
                max_blue = max(num, max_blue)
    return max_red * max_blue * max_green


def solve(input: list[str]):
    sum = 0
    for i, game in enumerate(input):
        moves = game.split(":")[1]
        power = find_power(moves)
        print(power)
        sum += power

    return sum


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 2.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
