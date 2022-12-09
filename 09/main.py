from dataclasses import dataclass, field
from typing import Union


INPUT_FILE = "09/input.txt"


@dataclass
class Coordinates:
    x: int
    y: int

    @classmethod
    def to_the_left_of(cls, original_cell: "Coordinates"):
        return cls(x=original_cell.x - 1, y=original_cell.y)

    @classmethod
    def at_the_top_of(cls, original_cell: "Coordinates"):
        return cls(x=original_cell.x, y=original_cell.y - 1)

    @classmethod
    def to_the_right_of(cls, original_cell: "Coordinates"):
        return cls(x=original_cell.x + 1, y=original_cell.y)

    @classmethod
    def at_the_bottom_of(cls, original_cell: "Coordinates"):
        return cls(x=original_cell.x, y=original_cell.y + 1)

    def __str__(self) -> str:
        return f"[{self.x};{self.y}]"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Knot:
    coordinates: Coordinates = field(default_factory=lambda: Coordinates(0, 0))
    head: "Knot" = None
    tail: "Knot" = None
    previous_coordinates: Coordinates = field(default_factory=lambda: Coordinates(0, 0))
    coordinates_history: set = field(default_factory=lambda: set())
    id = 0

    def __post_init__(self):
        self.coordinates_history.add(self.coordinates)

    def __str__(self) -> str:
        return f"({self.id}: {self.coordinates})"

    def __repr__(self) -> str:
        return f"{self.id}: {self.coordinates} {self.previous_coordinates}"

    def make_rope(self, knots_number: int):
        knot = self
        for id in range(knots_number):
            knot = knot.make_tail()
            knot.id = 1 + id
        return self

    def make_tail(self) -> "Knot":
        self.tail = Knot()
        self.tail.head = self
        return self.tail

    def get_tail(self) -> "Knot":
        if self.tail is None:
            return self
        return self.tail.get_tail()

    def rope_as_string(self):
        def recursive_string(string: str, knot: "Knot") -> str:
            if knot.tail is not None:
                return recursive_string(f"{string} -> {knot.tail}", knot.tail)
            else:
                return string

        return recursive_string(str(self), self)

    def get_distance_to_tail(self) -> int:
        return self.get_distance_to(self.tail)

    def get_distance_to_head(self) -> int:
        return self.get_distance_to(self.head)

    def get_distance_to(self, other: "Knot") -> int:
        return int(
            (
                (self.coordinates.x - other.coordinates.x) ** 2
                + (self.coordinates.y - other.coordinates.y) ** 2
            )
            ** (1 / 2)
        )

    def move(self, direction: str):
        self.previous_coordinates = self.coordinates
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

    def follow_head(self):
        if self.get_distance_to_head() > 1:
            self.previous_coordinates = self.coordinates
            # head is aligned with the tail
            if self.head.coordinates.x == self.coordinates.x:
                if self.head.coordinates.y > self.coordinates.y:
                    self.coordinates = Coordinates(
                        x=self.coordinates.x, y=self.coordinates.y + 1
                    )
                else:
                    self.coordinates = Coordinates(
                        x=self.coordinates.x, y=self.coordinates.y - 1
                    )
            elif self.head.coordinates.y == self.coordinates.y:
                if self.head.coordinates.x > self.coordinates.x:
                    self.coordinates = Coordinates(
                        x=self.coordinates.x + 1, y=self.coordinates.y
                    )
                else:
                    self.coordinates = Coordinates(
                        x=self.coordinates.x - 1, y=self.coordinates.y
                    )
            else:
                # Head and tail are not aligned
                diff_x = self.head.coordinates.x - self.coordinates.x
                diff_y = self.head.coordinates.y - self.coordinates.y
                if diff_x < 0 and diff_y < 0:
                    self.coordinates = Coordinates(
                        x=self.coordinates.x - 1, y=self.coordinates.y - 1
                    )
                elif diff_x < 0 and diff_y > 0:
                    self.coordinates = Coordinates(
                        x=self.coordinates.x - 1, y=self.coordinates.y + 1
                    )
                elif diff_x > 0 and diff_y < 0:
                    self.coordinates = Coordinates(
                        x=self.coordinates.x + 1, y=self.coordinates.y - 1
                    )
                elif diff_x > 0 and diff_y > 0:
                    self.coordinates = Coordinates(
                        x=self.coordinates.x + 1, y=self.coordinates.y + 1
                    )
            self.coordinates_history.add(self.coordinates)
        if self.tail is not None:
            self.tail.follow_head()


def print_grid(history_positions: set):
    min_x = min([position.x for position in history_positions])
    max_x = max([position.x for position in history_positions])
    min_y = min([position.y for position in history_positions])
    max_y = max([position.y for position in history_positions])
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if Coordinates(x, y) in history_positions:
                print("#", end="")
            else:
                print(".", end="")
        print()


def read_input_file():
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            direction, steps = line.split()
            for _ in range(int(steps)):
                yield direction


def part_one() -> int:
    """https://adventofcode.com/2022/day/9"""
    head = Knot().make_rope(1)
    tail = head.get_tail()
    for direction in read_input_file():
        head.move(direction)
    # print_grid(tail.coordinates_history)
    return len(tail.coordinates_history)


def part_two() -> int:
    """https://adventofcode.com/2022/day/9#part2"""
    head = Knot().make_rope(9)
    tail = head.get_tail()
    for direction in read_input_file():
        head.move(direction)
    # print_grid(tail.coordinates_history)
    return len(tail.coordinates_history)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
