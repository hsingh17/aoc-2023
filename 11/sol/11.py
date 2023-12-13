import sys
import typing

# UP DOWN LEFT RIGHT
DR = (-1, 1, 0, 0)
DC = (0, 0, -1, 1)
N_ROW = None
N_COL = None


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def find_col_row_with_no_galaxies(graph: list[list[str]]) -> tuple[set[int], set[int]]:
    rows_no_galaxies, cols_no_galaxies = set(), set()

    for r, _ in enumerate(graph):
        c = 0
        while in_bounds(r, c) and graph[r][c] == ".":
            c += 1

        if c == N_COL:
            rows_no_galaxies.add(r)

    for c, _ in enumerate(graph[0]):
        r = 0
        while in_bounds(r, c) and graph[r][c] == ".":
            r += 1

        if r == N_ROW:
            cols_no_galaxies.add(c)

    return rows_no_galaxies, cols_no_galaxies


def in_bounds(r: int, c: int):
    return r >= 0 and r < N_ROW and c >= 0 and c < N_COL

def solve(input: list[str]):
    expansion_factor = 1e6
    graph = [list(row) for row in input]
    galaxies = set()
    global N_ROW
    N_ROW = len(graph)

    global N_COL
    N_COL = len(graph[0])

    for r, row in enumerate(graph):
        for c, _ in enumerate(row):
            if graph[r][c] == "#":
                graph[r][c] = len(galaxies)
                galaxies.add((r, c))

    shortest_path: dict[int, list[int]] = {}
    for i in range(len(galaxies)):
        shortest_path[i] = [0] * len(galaxies)

    rows_no_galaxies, cols_no_galaxies = find_col_row_with_no_galaxies(graph)
    for r1, c1 in galaxies:
        for r2, c2 in galaxies:
            if (r1, c1) == (r2, c2):
                continue
            
            g1 = graph[r1][c1]
            g2 = graph[r2][c2]
            if not shortest_path.get(g1)[g2]:
                path_length = abs(r2-r1) + abs(c2-c1)
                for rng in rows_no_galaxies:
                    if min(r1, r2) <= rng <= max(r1, r2):
                        path_length += expansion_factor - 1

                for cng in cols_no_galaxies:
                    if min(c1, c2) <= cng <= max(c1, c2):
                        path_length += expansion_factor - 1
                        
                shortest_path.get(g1)[g2] = shortest_path.get(g2)[
                    g1
                ] = path_length

    for k, v in shortest_path.items():
        print(f"{k}: {str(v)}")
    
    return sum([sum(vals[0:i+1]) for i, vals in enumerate(shortest_path.values())])

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
