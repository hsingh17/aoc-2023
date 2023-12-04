import sys
from typing import Set, List, Tuple


def read_puzzle_input(path: str) -> List[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


# Part 1:
# def find_symbols(row: int, line: str) -> List[Tuple[int]]:
#     return [(row, col) for col, c in enumerate(line) if c != "." and not c.isalnum()]


# def find_num_coords(
#     symbol_coords: Set[Tuple[int]], input: List[str]
# ) -> Set[Tuple[int]]:
#     dirs = [
#         [-1, 0],  # N
#         [-1, 1],  # NE
#         [0, 1],  # E
#         [1, 1],  # SE
#         [1, 0],  # S
#         [1, -1],  # SW
#         [0, -1],  # W
#         [-1, -1],  # NW
#     ]

#     rows = len(input)
#     cols = len(input[0])

#     num_coords = set()
#     for coord in symbol_coords:
#         row, col = coord
#         for dir in dirs:
#             dr, dc = dir
#             new_r, new_c = row + dr, col + dc
#             if in_bound(new_r, new_c, rows, cols) and input[new_r][new_c].isnumeric():
#                 num_coords.add((new_r, new_c))

#     return num_coords


# def find_starting_coord_nums(
#     num_coords: Set[Tuple[int]], input: List[str]
# ) -> Set[Tuple[int]]:
#     def find_starting_coord_num(coord: Tuple[int]) -> Tuple[int]:
#         row, col = coord
#         starting_coord = coord
#         while in_bound(row, col, rows, cols) and input[row][col].isnumeric():
#             starting_coord = (row, col)
#             col -= 1
#         return starting_coord

#     rows = len(input)
#     cols = len(input[0])
#     nums_starting_coords = set()
#     for coord in num_coords:
#         nums_starting_coords.add(find_starting_coord_num(coord))
#     return nums_starting_coords


# def get_nums(nums_starting_coords: Set[Tuple[int]], input: List[str]) -> List[int]:
#     rows = len(input)
#     cols = len(input[0])
#     nums = list()
#     for coord in nums_starting_coords:
#         row, col = coord
#         num = ""
#         while in_bound(row, col, rows, cols) and input[row][col].isnumeric():
#             num += input[row][col]
#             col += 1
#         nums.append(int(num))
#     return nums


def find_possible_gears(row: int, line: str) -> List[Tuple[int]]:
    return [(row, col) for col, c in enumerate(line) if c == "*"]


def find_gears(symbol_coords: Set[Tuple[int]], input: List[str]) -> List[int]:
    dirs = [
        [-1, 0],  # N
        [-1, 1],  # NE
        [0, 1],  # E
        [1, 1],  # SE
        [1, 0],  # S
        [1, -1],  # SW
        [0, -1],  # W
        [-1, -1],  # NW
    ]

    rows = len(input)
    cols = len(input[0])

    gear_ratios = list()
    for coord in symbol_coords:
        row, col = coord
        possible_nums_for_gear = set()
        for dir in dirs:
            dr, dc = dir
            new_r, new_c = row + dr, col + dc
            if in_bound(new_r, new_c, rows, cols) and input[new_r][new_c].isnumeric():
                possible_nums_for_gear.add((new_r, new_c))

        # New condition: Check if next to exactly 2 numbers then it's a gear
        num_starting_coords = find_starting_coord_nums(possible_nums_for_gear, input)
        if len(num_starting_coords) == 2:
            part_numbers = get_nums(num_starting_coords, input)
            gear_ratios.append(part_numbers[0] * part_numbers[1])

    return gear_ratios


def find_starting_coord_nums(
    num_coords: Set[Tuple[int]], input: List[str]
) -> Set[Tuple[int]]:
    def find_starting_coord_num(coord: Tuple[int]) -> Tuple[int]:
        row, col = coord
        starting_coord = coord
        while in_bound(row, col, rows, cols) and input[row][col].isnumeric():
            starting_coord = (row, col)
            col -= 1
        return starting_coord

    rows = len(input)
    cols = len(input[0])
    nums_starting_coords = set()
    for coord in num_coords:
        nums_starting_coords.add(find_starting_coord_num(coord))
    return nums_starting_coords


def get_nums(nums_starting_coords: Set[Tuple[int]], input: List[str]) -> List[int]:
    rows = len(input)
    cols = len(input[0])
    nums = list()
    for coord in nums_starting_coords:
        row, col = coord
        num = ""
        while in_bound(row, col, rows, cols) and input[row][col].isnumeric():
            num += input[row][col]
            col += 1
        nums.append(int(num))
    return nums


def in_bound(row: int, col: int, rows: int, cols: int) -> bool:
    return row >= 0 and row < rows and col >= 0 and col < cols


def solve(input: List[str]) -> int:
    # Part 1:
    # symbol_coords = set()
    # for i, row in enumerate(input):
    #     # Step 1: Find all the symbols since part numbers can only be next to symbols
    #     symbols_on_row = find_symbols(i, row)
    #     symbol_coords.update(symbols_on_row)

    # # Step 2: From all the symbol coords by checking all 8 directions for numbers
    # num_coords = find_num_coords(symbol_coords, input)

    # # Step 3: For each of the numbers found, find the starting coord of the number
    # num_starting_coords = find_starting_coord_nums(num_coords, input)

    # # Step 4: Get the numbers
    # nums: list[int] = get_nums(num_starting_coords, input)

    # # Step 5: Sum up eveything
    # return sum(nums)

    possible_gears = set()
    for i, row in enumerate(input):
        # Step 1: Find all the * symbols
        possible_gears_on_row = find_possible_gears(i, row)
        possible_gears.update(possible_gears_on_row)

    # Step 2: Find all the actual gears and their ratios
    gear_ratios = find_gears(possible_gears, input)

    # Step 3: Sum up eveything
    return sum(gear_ratios)


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 3.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
