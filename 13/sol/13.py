import sys
import typing


def read_puzzle_input(path: str) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()


def get_patterns(input: list[str]) -> list[list[str]]:
    patterns = []
    cur = []
    for s in input:
        if s == "":
            patterns.append(cur[:])
            cur.clear()
        else:
            cur.append(s)

    patterns.append(cur[:])
    return patterns


def rotate(pattern: list[str]) -> list[str]:
    N = len(pattern[0])
    rotated = []
    for i in range(N):
        rotated.append("".join([s[i] for s in pattern]))
    return rotated


def x_reflections(
    pattern: list[str], find_smudge: bool = False, initial_reflection: int = None
) -> int:
    N = len(pattern)
    for i in range(N):
        if i == N - 1:
            continue

        lo, hi = i, i + 1
        is_perfect_reflection = True
        fixed_smudge = False
        while lo >= 0 and hi < N:
            # Reflected patterns don't match and we're either not trying to find the smudge or we already fixed it
            if pattern[lo] != pattern[hi] and (not find_smudge or fixed_smudge):
                is_perfect_reflection = False
                break

            # Reflected patterns are exact matches continue on
            if pattern[lo] == pattern[hi]:
                lo -= 1
                hi += 1
                continue

            # Find the smudge
            diff = [1 for s1, s2 in zip(pattern[lo], pattern[hi]) if s1 != s2]

            # Strings can only differ by exactly 1 for smudge to be fixed
            if len(diff) != 1:
                is_perfect_reflection = False
                break

            # If diff is 1, we consider this to be the smudge fixed row
            fixed_smudge = True
            lo -= 1
            hi += 1

        # If we have a perfect reflection and we're not trying to find the smudge return the rows above
        # Otherwise, if we're trying to find the smudge, only return if the initial reflection is not as the one currently found
        if is_perfect_reflection and (
            not find_smudge or (find_smudge and i + 1 != initial_reflection)
        ):
            return i + 1

    return None


def solve(input: list[str]):
    patterns = get_patterns(input)
    ret = 0
    for pattern in patterns:
        rotated_pattern = rotate(pattern)
        initial_x = x_reflections(pattern)
        initial_y = x_reflections(rotated_pattern)
        fixed_x = x_reflections(pattern, find_smudge=True, initial_reflection=initial_x)
        fixed_y = x_reflections(
            rotated_pattern, find_smudge=True, initial_reflection=initial_y
        )

        if fixed_x:
            ret += 100 * fixed_x
        else:
            ret += fixed_y
    return ret


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 13.py <path_to_file>")
        return

    path = args[1]
    input: list[str] = read_puzzle_input(path)
    print(solve(input))


if __name__ == "__main__":
    main()
