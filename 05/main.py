import re
import collections


INPUT_FILE = "05/input.txt"


def _with_mover_9000(towers: dict[int, list[str]], rounds: list[dict[str, int]]) -> str:
    for round in rounds:
        for _ in range(round["move"]):
            towers[round["to"]].append(towers[round["from"]].pop())
    return "".join(
        [
            tower[-1]
            for tower in collections.OrderedDict(sorted(towers.items())).values()
        ]
    )


def _with_mover_9001():
    pass


def top_crates(towers: dict[int, list[str]], rounds: list[dict[str, int]]) -> str:
    for round in rounds:
        tmp = []
        for _ in range(round["move"]):
            tmp.append(towers[round["from"]].pop())
        tmp.reverse()
        for i in tmp:
            towers[round["to"]].append(i)
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
            res = re.findall(
                regex_towers,
                line,
            )
            if res:
                for i in range(0, len(res)):
                    elem = res[i][1]
                    if elem:
                        data[i + 1].insert(0, elem)
            res = re.match(regex_moves, line)
            if res:
                data[0].append({k: int(v) for k, v in res.groupdict().items()})

    towers = data
    rounds = towers.pop(0)
    return towers, rounds


def part_one() -> str:
    """https://adventofcode.com/2022/day/5"""
    towers, rounds = read_input_file()
    top_crate = _with_mover_9000(towers, rounds)
    return top_crate


def part_two() -> str:
    """https://adventofcode.com/2022/day/5#part2"""
    towers, rounds = read_input_file()
    top_crate = top_crates(towers, rounds)
    return top_crate


if __name__ == "__main__":
    print(part_one())
    print(part_two())
