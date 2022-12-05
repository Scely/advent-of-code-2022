import re
import collections


INPUT_FILE = "05/input.txt"


def resolve(towers: dict[int, list[str]], rounds: list[dict[str, int]]) -> str:
    for round in rounds:
        print(round)
        for _ in range(round["move"]):
            towers[round["to"]].append(towers[round["from"]].pop())
        print(towers)
    od = collections.OrderedDict(sorted(towers.items()))
    return "".join([tower[-1] for tower in od.values()])


def read_input_file() -> dict:
    regex_hanoi = r"(\W([A-Z])\W)|(\s\s\s\s)"
    regex_moves = r"move\s(?P<move>\d+)\sfrom\s(?P<from>\d+)\sto\s(?P<to>\d+)"
    data = collections.defaultdict(list)

    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            pass
            res = re.findall(
                regex_hanoi,
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
    return data


def part_one() -> str:
    """https://adventofcode.com/2022/day/5"""
    score = 0
    towers = read_input_file()
    rounds = towers.pop(0)
    score = resolve(towers, rounds)
    return score


def part_two() -> int:
    """https://adventofcode.com/2022/day/5#part2"""
    score = 0
    return score


if __name__ == "__main__":
    print(part_one())
    print(part_two())
