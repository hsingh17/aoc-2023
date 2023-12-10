import sys
import typing


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()

def make_graph(input: list[str]):
    graph = dict()
    for s in input:
        tmp =  s.split("=")
        node, neighbors = tmp[0].strip(), tmp[1].split(",")
        graph[node] = (neighbors[0].strip().split("(")[1][0:3], neighbors[1].strip()[0:3])
    return graph

def solve(input: list[str]):
    path = input[0]
    N = len(path)
    graph: dict[str, tuple[str, str]] =  make_graph(input[2:])
    cur_node = "AAA"
    path_idx = 0
    steps = 0
    while cur_node != "ZZZ":
        left_right_idx = 0 if path[path_idx % N] == "L" else 1
        cur_node = graph[cur_node][left_right_idx]
        path_idx += 1
        steps += 1
    return steps


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 8.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
