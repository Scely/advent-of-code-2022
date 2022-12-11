import re
from collections import defaultdict as ddict
from collections import OrderedDict as odict
from typing import Iterator


INPUT_FILE = "05/input.txt"


def with_mover_9000(towers: ddict[int, list[str]], instruction: dict[str, int]) -> None:
    for _ in range(instruction["move"]):
        crates_to_add = towers[instruction["from"]].pop()
        tower = towers[instruction["to"]]
        tower.append(crates_to_add)


def with_mover_9001(towers: ddict[int, list[str]], instruction: dict[str, int]) -> None:
    crates_to_add = towers[instruction["from"]][-instruction["move"] :]
    del towers[instruction["from"]][-instruction["move"] :]
    tower = towers[instruction["to"]]
    tower.extend(crates_to_add)


def top_crates(
    towers: ddict[int, list[str]], instructions: list[dict[str, int]], mover: callable
) -> str:
    for instruction in instructions:
        mover(towers, instruction)
    return "".join([tower[-1] for tower in odict(sorted(towers.items())).values()])


def read_input_file() -> Iterator[tuple[ddict[int, list[str]], list[dict[str, int]]]]:
    regex_towers = r"(\W([A-Z])\W)|(\s\s\s\s)"
    regex_instructions = r"move\s(?P<move>\d+)\sfrom\s(?P<from>\d+)\sto\s(?P<to>\d+)"

    instructions: list[dict[str, int]] = []
    towers: ddict[int, list[str]] = ddict(list)

    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            if regex_result := re.findall(regex_towers, line):
                for i in range(len(regex_result)):
                    if crate := regex_result[i][1]:
                        towers[i + 1].insert(0, crate)
            elif regex_result := re.match(regex_instructions, line):
                instructions.append(
                    {k: int(v) for k, v in regex_result.groupdict().items()}
                )

    return towers, instructions


def part_one() -> str:
    """https://adventofcode.com/2022/day/5"""
    towers, instructions = read_input_file()
    return top_crates(towers, instructions, with_mover_9000)


def part_two() -> str:
    """https://adventofcode.com/2022/day/5#part2"""
    towers, instructions = read_input_file()
    return top_crates(towers, instructions, with_mover_9001)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
