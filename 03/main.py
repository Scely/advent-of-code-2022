from itertools import islice

INPUT_FILE = "03/input.txt"


def char_to_prioity_value(char: str) -> int:
    lower_cases = "abcdefghijklmnopqrstuvwxyz"
    upper_cases = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if char in lower_cases:
        return lower_cases.index(char) + 1
    elif char in upper_cases:
        return upper_cases.index(char) + 27
    return 0


def get_points_from_common_char_in_sets(*args: set) -> int:
    common_char: str = next(iter(set.intersection(*args)))
    return char_to_prioity_value(common_char)


def part_one() -> int:
    """https://adventofcode.com/2022/day/3"""
    score = 0
    with open(INPUT_FILE) as f:
        for rucksack in f.read().splitlines():
            compartments = (
                set(rucksack[: len(rucksack) // 2]),
                set(rucksack[len(rucksack) // 2 :]),
            )
            score += get_points_from_common_char_in_sets(*compartments)
    return score


def part_two() -> int:
    """https://adventofcode.com/2022/day/3#part2"""
    score = 0
    with open(INPUT_FILE) as f:
        while True:
            group = [set(rucksack.replace("\n", "")) for rucksack in islice(f, 3)]
            if len(group) < 3:
                break
            score += get_points_from_common_char_in_sets(*group)
    return score


if __name__ == "__main__":
    print(part_one())
    print(part_two())
