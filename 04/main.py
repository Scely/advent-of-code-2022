from dataclasses import dataclass
from typing import Iterator


INPUT_FILE = "04/input.txt"


@dataclass
class Section:
    start: int
    end: int

    def __contains__(self, item: "Section") -> bool:
        return self.start <= item.start <= item.end <= self.end

    def __ge__(self, item: "Section") -> bool:
        "section_1 >= section 2 means section_1 is a superset of section_2"
        return item in self

    def __le__(self, item: "Section") -> bool:
        "section_1 <= section 2 means section_1 is a subset of section_2"
        return self in item

    def __eq__(self, item: "Section") -> bool:
        return self.start == item.start and self.end == item.end

    def __str__(self) -> str:
        return f"{self.start}-{self.end}"


def is_section_subset_of_the_other(sections_raw: list[str]) -> bool:
    section_1, section_2 = [
        Section(*map(int, section_raw.split("-"))) for section_raw in sections_raw
    ]
    return any([section_1 <= section_2, section_1 >= section_2])


def is_section_overlap_with_the_other(sections_raw: list[str]) -> bool:
    section_1, section_2 = [
        Section(*map(int, section_raw.split("-"))) for section_raw in sections_raw
    ]
    return section_1.start <= section_2.end and section_2.start <= section_1.end


def read_input_file_as_sections() -> Iterator[list[str]]:
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            sections = line.split(",")
            yield sections


def part_one() -> int:
    """https://adventofcode.com/2022/day/4"""
    score = 0
    for sections in read_input_file_as_sections():
        score += int(is_section_subset_of_the_other(sections))
    return score


def part_two() -> int:
    """https://adventofcode.com/2022/day/4#part2"""
    score = 0
    for sections in read_input_file_as_sections():
        score += int(is_section_overlap_with_the_other(sections))
    return score


if __name__ == "__main__":
    print(part_one())
    print(part_two())
