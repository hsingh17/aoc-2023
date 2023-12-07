import sys
from typing import List, Tuple, Set
from functools import reduce


class Interval:
    def __init__(self, s: str) -> None:
        l = s.split(" ")
        self.dst_start, self.src_start, self.length = int(l[0]), int(l[1]), int(l[2])

    # Part 1:
    def get_num_mapping(self, num) -> int:
        return (
            self.dst_start + (num - self.src_start)
            if self.src_start <= num <= self.src_start + self.length
            else None
        )

    # Part 2:
    def get_interval_mapping(self, interval: Tuple[int, int]) -> Tuple[Tuple[int, int]]:
        src_start, src_end = self.src_start, self.src_start + self.length - 1
        int_start, int_end = interval[0], interval[1]

        if (
            src_start <= int_start <= int_end <= src_end
        ):  # Case 1: Complete overlap where src covers interval
            return (
                (
                    self.dst_start + (int_start - src_start),
                    self.dst_start + (int_end - src_start),
                ),
                None,
                None,
            )
        elif (
            int_start < src_start < src_end < int_end
        ):  # Case 2: Complete overlap where interval covers src
            return (
                (
                    self.dst_start,
                    self.dst_start + (src_end - src_start),
                ),
                (int_start, src_start - 1),
                (src_end + 1, int_end),
            )
        elif (
            int_start <= int_end < src_start <= src_end
            or src_start <= src_end < int_start <= int_end
        ):  # Case 3: No overlap
            return (None, (int_start, int_end), None)
        elif (
            int_start < src_start <= int_end <= src_end
        ):  # Case 4: Partial overlap interval partially overlaps the src on left
            return (
                (
                    self.dst_start,
                    self.dst_start + (int_end - src_start),
                ),
                (int_start, src_start - 1),  # Unmapped part,
                None,
            )
        elif (
            src_start <= int_start <= src_end < int_end
        ):  # Case 5: Partial overlap interval partially overlaps the src on right
            return (
                (
                    self.dst_start + (int_start - src_start),
                    self.dst_start + (src_end - src_start),
                ),
                (src_end + 1, int_end),  # Unmapped part,
                None,
            )
        else:
            raise Exception(
                f"Case not considered! SRC Start {src_start}, SRC End {src_end}, Int Start:{int_end}, Int End {int_end}"
            )

    def __str__(self) -> str:
        return f"DST Start: {self.dst_start}, SRC Start: {self.src_start}, Length: {self.length}"


class MapperWrapper:
    def __init__(self, *args: List[Interval]) -> None:
        self.interval_mappings = args

    # Part 1:
    def map_num(self, num: int) -> int:
        for map in self.interval_mappings:
            mapping = None
            for interval in map:
                mapping = interval.get_num_mapping(num)
                if mapping is not None:
                    break

            # No mapping was found so it maps to itself
            if mapping is None:
                mapping = num
            num = mapping
        return num

    # Part 2:
    def map_interval(
        self, intervals_to_map: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        for map in self.interval_mappings:
            qa = []
            for interval in map:
                qb = []
                while intervals_to_map:
                    to_map = intervals_to_map.pop()
                    t1, t2, t3 = interval.get_interval_mapping(to_map)
                    if t1:
                        qa.append(t1)  # Ready for the next mapping
                    if t2:
                        qb.append(
                            t2
                        )  # Unmapped, continue processing into next interval
                    if t3:
                        qb.append(
                            t3
                        )  # Unmapped, continue processing into next interval
                intervals_to_map = qb
            intervals_to_map = intervals_to_map + qa
        return intervals_to_map


def read_puzzle_input(path: str) -> List[str]:
    with open(path, "r") as f:
        return [s for s in f.read().strip().splitlines() if len(s) != 0]


def get_seeds(input: List[str]) -> Set[Tuple[int]]:
    seeds_and_range = input[0].split(":")[1].strip().split(" ")
    return {
        (int(seed), int(seed) + int(seeds_and_range[i + 1]) - 1)
        for i, seed in enumerate(seeds_and_range)
        if i % 2 == 0
    }


def get_intervals(input: List[str]):
    sts_idx = input.index("seed-to-soil map:")
    stf_idx = input.index("soil-to-fertilizer map:")
    ftw_idx = input.index("fertilizer-to-water map:")
    wtl_idx = input.index("water-to-light map:")
    ltt_idx = input.index("light-to-temperature map:")
    tth_idx = input.index("temperature-to-humidity map:")
    htl_idx = input.index("humidity-to-location map:")
    return (
        list(map(lambda s: Interval(s), input[sts_idx + 1 : stf_idx])),
        list(map(lambda s: Interval(s), input[stf_idx + 1 : ftw_idx])),
        list(map(lambda s: Interval(s), input[ftw_idx + 1 : wtl_idx])),
        list(map(lambda s: Interval(s), input[wtl_idx + 1 : ltt_idx])),
        list(map(lambda s: Interval(s), input[ltt_idx + 1 : tth_idx])),
        list(map(lambda s: Interval(s), input[tth_idx + 1 : htl_idx])),
        list(map(lambda s: Interval(s), input[htl_idx + 1 : len(input)])),
    )


def solve(input: List[str]):
    seeds = get_seeds(input)
    intervals = get_intervals(input)
    mapper_wrapper = MapperWrapper(*intervals)
    mapped_intervals = mapper_wrapper.map_interval(seeds)
    return min(mapped_intervals)


def main():
    args = sys.argv
    if len(args) < 2:
        print(f"Usage: python3 template.py <path_to_file>")
        return

    path = args[1]
    input = read_puzzle_input(path)
    print(min(solve(input)))


if __name__ == "__main__":
    main()
