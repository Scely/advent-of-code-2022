from itertools import islice

INPUT_FILE = "03/input.txt"


def char_to_priority_value(char: str) -> int:
    lower_cases = "abcdefghijklmnopqrstuvwxyz"
    upper_cases = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if char in lower_cases:
        return lower_cases.index(char) + 1
    elif char in upper_cases:
        return upper_cases.index(char) + 27
    return 0


def get_points_from_common_char_in_sets(*args: set) -> int:
    common_char: str = next(iter(set.intersection(*args)))
    return char_to_priority_value(common_char)


def read_input_file_as_compartments() -> list[set]:
    with open(INPUT_FILE) as f:
        for rucksack in f.read().splitlines():
            compartments = (
                set(rucksack[: len(rucksack) // 2]),
                set(rucksack[len(rucksack) // 2 :]),
            )
            yield compartments


def read_input_file_as_group_of_rucksacks(nb: int = 3) -> list[set]:
    with open(INPUT_FILE) as f:
        while group := [set(rucksack.replace("\n", "")) for rucksack in islice(f, nb)]:
            yield group


def part_one() -> int:
    """https://adventofcode.com/2022/day/3"""
    score = 0
    for compartments in read_input_file_as_compartments():
        score += get_points_from_common_char_in_sets(*compartments)
    return score


def part_two() -> int:
    """https://adventofcode.com/2022/day/3#part2"""
    score = 0
    for group in read_input_file_as_group_of_rucksacks():
        score += get_points_from_common_char_in_sets(*group)
    return score


if __name__ == "__main__":
    print(part_one())
    print(part_two())
