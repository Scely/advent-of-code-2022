INPUT_FILE = "01/input.txt"


def read_input_file_as_calories():
    with open(INPUT_FILE) as f:
        calories = 0
        for i in f.read().splitlines():
            if i:
                calories += int(i)
            else:
                yield calories
                calories = 0


def get_snacks() -> list[int]:
    snacks = list(read_input_file_as_calories())
    return sorted(snacks, reverse=True)


def part_one() -> int:
    """https://adventofcode.com/2022/day/1"""
    return max(get_snacks())


def part_two() -> int:
    """https://adventofcode.com/2022/day/1#part2"""
    return sum(get_snacks()[:3])


if __name__ == "__main__":
    print(part_one())
    print(part_two())
