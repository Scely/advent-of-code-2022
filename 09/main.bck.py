from dataclasses import dataclass
from typing import Union


INPUT_FILE = "09/input.txt"


@dataclass
class Cell:
    x: int
    y: int

    @classmethod
    def to_the_left_of(cls, original_cell: "Cell"):
        return cls(x=original_cell.x - 1, y=original_cell.y)

    @classmethod
    def at_the_top_of(cls, original_cell: "Cell"):
        return cls(x=original_cell.x, y=original_cell.y - 1)

    @classmethod
    def to_the_right_of(cls, original_cell: "Cell"):
        return cls(x=original_cell.x + 1, y=original_cell.y)

    @classmethod
    def at_the_bottom_of(cls, original_cell: "Cell"):
        return cls(x=original_cell.x, y=original_cell.y + 1)

    def __str__(self) -> str:
        return f"[{self.x};{self.y}]"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self):
        return hash((self.x, self.y))

    def get_distance_to(self, other: Union["Cell", None]) -> int:
        if other is None:
            other = Cell(0, 0)
        return int(((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** (1 / 2))


def read_input_file():
    head_path: list[Cell] = [Cell(0, 0)]
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            movement, steps = line.split()
            for _ in range(int(steps)):
                if movement == "U":
                    head_path.append(Cell.at_the_top_of(head_path[-1]))
                elif movement == "D":
                    head_path.append(Cell.at_the_bottom_of(head_path[-1]))
                elif movement == "R":
                    head_path.append(Cell.to_the_right_of(head_path[-1]))
                elif movement == "L":
                    head_path.append(Cell.to_the_left_of(head_path[-1]))
    return head_path


def part_one() -> int:
    """https://adventofcode.com/2022/day/9"""
    head_path = read_input_file()
    tail_path: list[Cell] = [Cell(0, 0)]

    tmp = None
    for cell in head_path:
        if cell.get_distance_to(tail_path[-1]) > 1:
            tail_path.append(tmp)
        tmp = cell

    return len(set(tail_path))


def part_two() -> int:
    """https://adventofcode.com/2022/day/9#part2"""
    head_path = read_input_file()
    middle_path: list[Cell] = [Cell(0, 0) for _ in range(len(head_path))]
    tail_path: list[Cell] = [Cell(0, 0) for _ in range(len(head_path))]

    matrix = [head_path, middle_path]
    print(head_path)
    print(middle_path)
    for path_index in range(len(matrix) - 1):
        for step_index in range(1, len(matrix[path_index])):
            d = matrix[path_index][step_index].get_distance_to(
                matrix[path_index + 1][step_index - 1]
            )
            if d > 1:
                matrix[path_index + 1][step_index] = matrix[path_index][step_index - 1]
            pass
            print(matrix[path_index][step_index], matrix[path_index + 1][step_index], d)
    pass
    return

    for i, head_cell in enumerate(head_path):
        moving_cell = head_cell
        for knot_path in [tail_path]:
            following_cell = knot_path[-1]
            if moving_cell.get_distance_to(following_cell) > 1:
                knot_path.append(moving_cell)
            moving_cell = following_cell
        print(head_cell, tail_path[-1])

    return len(set(tail_path))


if __name__ == "__main__":
    print(part_one())
    print(part_two())
