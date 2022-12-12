from dataclasses import dataclass, field
from typing import Iterator
from tools.grid import Coordinates

INPUT_FILE = "09/input.txt"


@dataclass
class Knot:
    coordinates: Coordinates = field(default_factory=lambda: Coordinates(0, 0))
    id: int = 0
    head: "Knot" = None
    tail: "Knot" = None
    coordinates_history: set = field(default_factory=lambda: set())

    def __post_init__(self):
        self.coordinates_history.add(self.coordinates)

    def __str__(self) -> str:
        return f"{{{self.id}: {self.coordinates}}}"

    def __repr__(self) -> str:
        return self.__str__()

    def make_rope(self, knots_number: int) -> "Knot":
        knot = self
        for id in range(knots_number):
            knot.tail = Knot(head=knot, id=id + 1)
            knot = knot.tail
        return self

    def get_tail(self) -> "Knot":
        if self.tail is None:
            return self
        return self.tail.get_tail()

    def as_string(self) -> str:
        def recursive_string(string: str, knot: "Knot") -> str:
            if knot.tail is not None:
                return recursive_string(f"{string} -> {knot.tail}", knot.tail)
            else:
                return string

        return recursive_string(str(self), self)

    def get_distance_to(self, other: "Knot") -> int:
        return int(
            (
                (self.coordinates.x - other.coordinates.x) ** 2
                + (self.coordinates.y - other.coordinates.y) ** 2
            )
            ** (1 / 2)
        )

    def move(self, direction: str) -> None:
        if direction == "U":
            self.coordinates = Coordinates.at_the_top_of(self.coordinates)
        elif direction == "D":
            self.coordinates = Coordinates.at_the_bottom_of(self.coordinates)
        elif direction == "R":
            self.coordinates = Coordinates.to_the_right_of(self.coordinates)
        elif direction == "L":
            self.coordinates = Coordinates.to_the_left_of(self.coordinates)
        self.coordinates_history.add(self.coordinates)
        self.tail.follow_head()

    def follow_head(self) -> None:
        if self.get_distance_to(self.head) > 1:
            head_coords = self.head.coordinates
            self_coords = self.coordinates
            if head_coords.is_verticaly_aligned(self_coords):
                if head_coords.is_at_the_bottom_of(self_coords):
                    self.coordinates = Coordinates.at_the_bottom_of(self_coords)
                elif head_coords.is_at_the_top_of(self_coords):
                    self.coordinates = Coordinates.at_the_top_of(self_coords)
            elif head_coords.is_horizontaly_aligned(self_coords):
                if head_coords.is_on_the_right_of(self_coords):
                    self.coordinates = Coordinates.to_the_right_of(self_coords)
                elif head_coords.is_on_the_left_of(self_coords):
                    self.coordinates = Coordinates.to_the_left_of(self_coords)
            else:
                # Head and tail are not aligned
                if head_coords.is_at_the_top_left_of(self_coords):
                    self.coordinates = Coordinates.at_the_top_left_of(self_coords)
                elif head_coords.is_at_the_bottom_left_of(self_coords):
                    self.coordinates = Coordinates.at_the_bottom_left_of(self_coords)
                elif head_coords.is_at_the_top_right_of(self_coords):
                    self.coordinates = Coordinates.at_the_top_right_of(self_coords)
                elif head_coords.is_at_the_bottom_right_of(self_coords):
                    self.coordinates = Coordinates.at_the_bottom_right_of(self_coords)
        self.coordinates_history.add(self.coordinates)
        if self.tail is not None:
            self.tail.follow_head()


def print_grid(coordinates_history: set[Coordinates]) -> None:
    all_x_coordinates = [coordinates.x for coordinates in coordinates_history]
    all_y_coordinates = [coordinates.y for coordinates in coordinates_history]
    min_x, max_x = min(all_x_coordinates), max(all_x_coordinates)
    min_y, max_y = min(all_y_coordinates), max(all_y_coordinates)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Coordinates(x, y) in coordinates_history:
                print("#", end="")
            else:
                print(".", end="")
        print()


def read_input_file_as_direction() -> Iterator[str]:
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            direction, steps = line.split()
            for _ in range(int(steps)):
                yield direction


def get_number_of_position(
    number_of_rope_knots: int, print_tail_trace: bool = False, debug_mode=False
) -> int:
    rope = Knot().make_rope(number_of_rope_knots)
    for direction in read_input_file_as_direction():
        rope.move(direction)
        if debug_mode:
            print(rope.as_string())
    tail: Knot = rope.get_tail()
    if print_tail_trace:
        print_grid(tail.coordinates_history)
    return len(tail.coordinates_history)


def part_one() -> int:
    """https://adventofcode.com/2022/day/9"""
    return get_number_of_position(number_of_rope_knots=1)


def part_two() -> int:
    """https://adventofcode.com/2022/day/9#part2"""
    return get_number_of_position(number_of_rope_knots=9)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
