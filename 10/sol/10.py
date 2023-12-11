import sys
import typing
from enum import Enum


class Directions(Enum):
    NORTH = (-1,)
    EAST = (2,)
    SOUTH = (1,)
    WEST = -2


class Graph:
    DIRECTIONS_DR_DC = {
        Directions.NORTH: (-1, 0),  # N
        Directions.EAST: (0, 1),  # E
        Directions.SOUTH: (1, 0),  # S
        Directions.WEST: (0, -1),  # W
    }

    def __init__(self, input: list[str]) -> None:
        self.graph = [list(l) for l in input]
        self.start = self.__find_start()[0]

    def __find_start(self) -> list[tuple[int, int]]:
        return [(i, l.index("S")) for i, l in enumerate(self.graph) if "S" in l]

    def __get_neighbor_coords(
        self, r: int, c: int, pipe: str = None
    ) -> dict[Directions, tuple[int, int]]:
        dirs: dict[Directions, tuple[int, int]] = Graph.DIRECTIONS_DR_DC.copy()
        if pipe == "|":
            dirs.pop(Directions.EAST)
            dirs.pop(Directions.WEST)
        elif pipe == "-":
            dirs.pop(Directions.NORTH)
            dirs.pop(Directions.SOUTH)
        elif pipe == "L":
            dirs.pop(Directions.SOUTH)
            dirs.pop(Directions.WEST)
        elif pipe == "F":
            dirs.pop(Directions.WEST)
            dirs.pop(Directions.NORTH)
        elif pipe == "7":
            dirs.pop(Directions.EAST)
            dirs.pop(Directions.NORTH)
        elif pipe == "J":
            dirs.pop(Directions.SOUTH)
            dirs.pop(Directions.EAST)

        neighbors = {}
        for dir, offset in dirs.items():
            new_r, new_c = r + offset[0], c + offset[1]
            neighbors[dir] = (
                (new_r, new_c)
                if self.__is_in_bounds(new_r, new_c) and self.graph[new_r][new_c] != "."
                else None
            )
        return neighbors

    def __is_in_bounds(self, r: int, c: int) -> bool:
        return r >= 0 and r < len(self.graph) and c >= 0 and c < len(self.graph[0])

    def __valid_start_pipes(self) -> list[str]:
        r, c = self.start
        neighbors: dict[Directions, tuple[int, int]] = self.__get_neighbor_coords(r, c)
        valid_pipes = []
        north, east, south, west = (
            neighbors[Directions.NORTH],
            neighbors[Directions.EAST],
            neighbors[Directions.SOUTH],
            neighbors[Directions.WEST],
        )

        # Go through all the cases
        # J,|,7
        # |(S)
        # J,|,L

        # -,F,L  -(S)  -,J,7

        # |,7,F
        # L(S)  -,J,7

        # F(S)  -,J,7
        # |,J,L

        # -,L,F 7(S)
        #       |,J,L

        #       |,7,F
        # -,L,F J(S)

        # Case 1: S = |
        if (
            north
            and south
            and self.graph[north[0]][north[1]] in ("J", "|", "7")
            and self.graph[south[0]][south[1]] in ("J", "|", "L")
        ):
            valid_pipes.append("|")

        # Case 2: S = -
        if (
            west
            and east
            and self.graph[west[0]][west[1]] in ("-", "F", "L")
            and self.graph[east[0]][east[1]] in ("J", "-", "7")
        ):
            valid_pipes.append("-")
        # Case 3: S = L
        if (
            north
            and east
            and self.graph[north[0]][north[1]] in ("F", "|", "7")
            and self.graph[east[0]][east[1]] in ("J", "-", "L")
        ):
            valid_pipes.append("L")
        # Case 4: S = F
        if (
            east
            and south
            and self.graph[east[0]][east[1]] in ("-", "J", "7")
            and self.graph[south[0]][south[1]] in ("J", "|", "L")
        ):
            valid_pipes.append("F")
        # Case 5: S = 7
        if (
            west
            and south
            and self.graph[west[0]][west[1]] in ("-", "L", "F")
            and self.graph[south[0]][south[1]] in ("J", "|", "L")
        ):
            valid_pipes.append("7")
        # Case 6: S = J
        if (
            north
            and west
            and self.graph[north[0]][north[1]] in ("F", "|", "7")
            and self.graph[west[0]][west[1]] in ("-", "L", "F")
        ):
            valid_pipes.append("J")

        return valid_pipes

    def find_loop_max_length(self, start: tuple[int, int]) -> int:
        visited: set[tuple[int, int]] = set()
        r, c = start[0], start[1]
        neighbors = list(self.__get_neighbor_coords(r, c, self.graph[r][c]).values())
        cur_node1 = neighbors[0]
        cur_node2 = neighbors[1]
        visited.add(start)
        steps = 1

        while cur_node1 != cur_node2:
            visited.update([cur_node1, cur_node2])

            cur_node1_neighbors = list(
                self.__get_neighbor_coords(
                    cur_node1[0], cur_node1[1], self.graph[cur_node1[0]][cur_node1[1]]
                ).values()
            )

            cur_node2_neighbors = list(
                self.__get_neighbor_coords(
                    cur_node2[0], cur_node2[1], self.graph[cur_node2[0]][cur_node2[1]]
                ).values()
            )

            cur_node1 = list(filter(lambda n: n not in visited, cur_node1_neighbors))[0]
            cur_node2 = list(filter(lambda n: n not in visited, cur_node2_neighbors))[0]
            steps += 1

        return steps

    def find_main_loop(self) -> int:
        best = -1
        possible_start_pipes: list[str] = self.__valid_start_pipes()
        for pipe in possible_start_pipes:
            r, c = self.start
            self.graph[r][c] = pipe
            best = max(best, self.find_loop_max_length(self.start))
        return best


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def solve(input: list[str]):
    graph = Graph(input)
    return graph.find_main_loop()


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 template.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
