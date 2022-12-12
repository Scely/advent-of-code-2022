from dataclasses import dataclass, field


INPUT_FILE = "12/input.txt"


@dataclass
class Coordinates:
    x: int
    y: int

    @classmethod
    def to_the_left_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x - 1, y=other.y)

    @classmethod
    def at_the_top_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x, y=other.y - 1)

    @classmethod
    def to_the_right_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x + 1, y=other.y)

    @classmethod
    def at_the_bottom_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x, y=other.y + 1)

    @classmethod
    def at_the_top_left_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x - 1, y=other.y - 1)

    @classmethod
    def at_the_top_right_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x + 1, y=other.y - 1)

    @classmethod
    def at_the_bottom_left_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x - 1, y=other.y + 1)

    @classmethod
    def at_the_bottom_right_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x + 1, y=other.y + 1)

    def is_verticaly_aligned(self, other: "Coordinates") -> bool:
        return self.x == other.x

    def is_horizontaly_aligned(self, other: "Coordinates") -> bool:
        return self.y == other.y

    def is_on_the_left_of(self, other: "Coordinates") -> bool:
        return self.x < other.x

    def is_at_the_top_of(self, other: "Coordinates") -> bool:
        return self.y < other.y

    def is_on_the_right_of(self, other: "Coordinates") -> bool:
        return self.x > other.x

    def is_at_the_bottom_of(self, other: "Coordinates") -> bool:
        return self.y > other.y

    def is_at_the_top_left_of(self, other: "Coordinates") -> bool:
        return self.is_on_the_left_of(other) and self.is_at_the_top_of(other)

    def is_at_the_top_right_of(self, other: "Coordinates") -> bool:
        return self.is_on_the_right_of(other) and self.is_at_the_top_of(other)

    def is_at_the_bottom_left_of(self, other: "Coordinates") -> bool:
        return self.is_on_the_left_of(other) and self.is_at_the_bottom_of(other)

    def is_at_the_bottom_right_of(self, other: "Coordinates") -> bool:
        return self.is_on_the_right_of(other) and self.is_at_the_bottom_of(other)

    def __str__(self) -> str:
        return f"[{self.x};{self.y}]"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self):
        return hash((self.x, self.y))


@dataclass
class Cell:
    height: int
    coordinates: Coordinates
    # marked: bool = False
    higher_neighbors: list["Cell"] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        return str(
            f"{self.coordinates}: {self.height} -> {[f'{neighbour.coordinates}: {neighbour.height}' for neighbour in self.higher_neighbors]}"
        )

    def __repr__(self) -> str:
        return f"{self.coordinates}: {self.height}"


def read_input_file():
    matrix: list[list[Cell]] = []
    start_cell: Cell
    end_cell: Cell

    with open(INPUT_FILE) as f:
        for i, line in enumerate(f.read().splitlines()):
            row = []
            for j, char in enumerate(line):
                coords = Coordinates(i, j)
                if char == "S":
                    cell = start_cell = Cell(0, coords)
                elif char == "E":
                    cell = end_cell = Cell(27, coords)
                else:
                    cell = Cell(ord(char) - 96, coords)
                row.append(cell)
            matrix.append(row)

    def valid_coordinates(coords: Coordinates, matrix):
        return 0 <= coords.x < len(matrix) and 0 <= coords.y < len(matrix[0])

    # Find neighbours
    for row in matrix:
        for cell in row:
            cell: Cell
            for coords in [
                Coordinates.to_the_left_of(cell.coordinates),
                Coordinates.at_the_top_of(cell.coordinates),
                Coordinates.to_the_right_of(cell.coordinates),
                Coordinates.at_the_bottom_of(cell.coordinates),
            ]:
                if valid_coordinates(coords, matrix):
                    target_cell = matrix[coords.x][coords.y]
                    if target_cell.height in [cell.height, cell.height + 1]:
                        cell.higher_neighbors.append(matrix[coords.x][coords.y])

    # TODO debug
    for row in matrix:
        for cell in row:
            print(cell)

    return start_cell, end_cell


def find_len():
    pass


def part_one() -> int:
    """https://adventofcode.com/2022/day/12"""
    score = 0
    start_cell, end_cell = read_input_file()
    # find_len(start_cell)
    return score


def part_two() -> int:
    """https://adventofcode.com/2022/day/12#part2"""
    score = 0
    return score


if __name__ == "__main__":
    print(part_one())
    print(part_two())
