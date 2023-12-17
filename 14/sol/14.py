import sys
from enum import Enum


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


# Part 1:
# def roll(grid: list[str]) -> int:
#     rows = len(grid)
#     cols = len(grid[0])
#     load = 0
#     for col in range(cols):
#         cur_load = 0
#         lo = 0
#         for row in range(rows):
#             s = grid[row][col]
#             if s == ".":
#                 continue
#             elif s == "#":
#                 lo = row + 1
#             elif s == "O":
#                 cur_load += cols - lo
#                 lo += 1
#         load += cur_load
#     return load


class Direction(Enum):
    UP = (1,)
    DOWN = (2,)
    LEFT = (3,)
    RIGHT = 4


class Rock:
    def __init__(self, rc: tuple[int, int]) -> None:
        self.rc = rc
    
    def update(self, rc: tuple[int, int]):
        self.rc = rc

    def __lt__(self, obj: "Rock"):
        return self.rc < obj.rc

    def __repr__(self) -> str:
        return str(self.rc)


def roll_vertical(grid: list[list[str]], rocks: set[Rock], dir: Direction):
    rows = len(grid)
    l = sorted(rocks) if dir == Direction.UP else reversed(sorted(rocks))

    for rock in l:
        r, c = rock.rc
        step = -1 if dir == Direction.UP else 1
        row = r + step
        in_bounds = lambda row: row >= 0 if dir == Direction.UP else row < rows
        air = None
        while in_bounds(row):
            s = grid[row][c]
            if s == ".":
                air = row
            elif s == "#":
                grid[r][c] = "."
                grid[row - step][c] = "O"
                rock.update((row - step, c))
                air = None
                break
            elif s == "O":
                break

            row += step

        if air is not None:
            grid[air][c] = "O"
            grid[r][c] = "."
            rock.update((air, c))


def roll_horizontal(grid: list[list[str]], rocks: set[Rock], dir: Direction):
    cols = len(grid[0])
    l = sorted(rocks) if dir == Direction.LEFT else reversed(sorted(rocks))

    for rock in l:
        r, c = rock.rc
        step = -1 if dir == Direction.LEFT else 1
        col = c + step
        in_bounds = lambda col: col >= 0 if dir == Direction.LEFT else col < cols
        air = None

        while in_bounds(col):
            s = grid[r][col]
            if s == ".":
                air = col
            elif s == "#":
                grid[r][c] = "."
                grid[r][col - step] = "O"
                rock.update((r, col - step))
                air = None
                break
            elif s == "O":
                break

            col += step

        if air is not None:
            grid[r][air] = "O"
            grid[r][c] = "."
            rock.update((r, air))


def find_rocks(grid: list[list[str]]) -> set[Rock]:
    rocks = set()
    for r, l in enumerate(grid):
        for c, s in enumerate(l):
            if s == "O":
                rocks.add(Rock((r, c)))
    return rocks


def solve(input: list[str]):
    grid = [list(s) for s in input]
    rocks = find_rocks(grid)
    seen: dict[str, int] = dict()
    cycles = 1000000000
    i = 0
    found_cycle = False

    while i < cycles:
        config = "".join(["".join(l) for l in grid])
        if config in seen and not found_cycle:
            cycle_length = i - seen[config]
            i += ((cycles - i) // cycle_length) * cycle_length
            found_cycle = True

        seen[config] = i
        roll_vertical(grid, rocks, Direction.UP)
        roll_horizontal(grid, rocks, Direction.LEFT)
        roll_vertical(grid, rocks, Direction.DOWN)
        roll_horizontal(grid, rocks, Direction.RIGHT)
        i += 1

    load = 0
    for rock in rocks:
        load += len(grid) - rock.rc[0]
    return load


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 14.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
