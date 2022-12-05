import re
import collections


INPUT_FILE = "05/input.txt"


def with_mover_9000(towers: dict[int, list[str]], instruction: dict[str, int]) -> None:
    for _ in range(instruction["move"]):
        towers[instruction["to"]].append(towers[instruction["from"]].pop())


def with_mover_9001(towers: dict[int, list[str]], instruction: dict[str, int]) -> None:
    towers[instruction["to"]].extend(
        towers[instruction["from"]][-instruction["move"] :]
    )
    del towers[instruction["from"]][-instruction["move"] :]


def top_crates(
    towers: dict[int, list[str]], instructions: list[dict[str, int]], mover: callable
) -> str:
    for instruction in instructions:
        mover(towers, instruction)
    return "".join(
        [
            tower[-1]
            for tower in collections.OrderedDict(sorted(towers.items())).values()
        ]
    )


def read_input_file() -> tuple[dict[int, str], list]:
    regex_towers = r"(\W([A-Z])\W)|(\s\s\s\s)"
    regex_moves = r"move\s(?P<move>\d+)\sfrom\s(?P<from>\d+)\sto\s(?P<to>\d+)"
    data = collections.defaultdict(list)

    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            pass
            if res := re.findall(regex_towers, line):
                for i in range(0, len(res)):
                    elem = res[i][1]
                    if elem:
                        data[i + 1].insert(0, elem)
            elif res := re.match(regex_moves, line):
                data[0].append({k: int(v) for k, v in res.groupdict().items()})

    towers = data
    rounds = towers.pop(0)
    return towers, rounds


def part_one() -> str:
    """https://adventofcode.com/2022/day/5"""
    towers, rounds = read_input_file()
    return top_crates(towers, rounds, with_mover_9000)


def part_two() -> str:
    """https://adventofcode.com/2022/day/5#part2"""
    towers, rounds = read_input_file()
    return top_crates(towers, rounds, with_mover_9001)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
