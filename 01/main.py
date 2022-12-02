INPUT_FILE = "01/input.txt"


def get_snacks() -> list[int]:
    with open(INPUT_FILE) as f:
        acc = 0
        max_list = []
        for i in f.read().splitlines():
            if i:
                acc += int(i)
            else:
                max_list.append(acc)
                acc = 0
        return list(reversed(sorted(max_list)))


def part_one() -> int:
    """https://adventofcode.com/2022/day/1"""
    return get_snacks()[0]


def part_two() -> int:
    """https://adventofcode.com/2022/day/1#part2"""
    return sum(get_snacks()[:3])


if __name__ == "__main__":
    print(part_one())
    print(part_two())
