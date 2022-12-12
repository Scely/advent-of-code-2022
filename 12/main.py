from dataclasses import dataclass, field
from enum import Enum


INPUT_FILE = "12/input.txt"


class Marker(Enum):
    START = "S"
    END = "E"


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
    higher_neighbors: list["Cell"] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        return str(
            f"{self.coordinates}: {self.height} -> {[f'{neighbour.coordinates}: {neighbour.height}' for neighbour in self.higher_neighbors]}"
        )

    def __repr__(self) -> str:
        return f"{self.coordinates}: {self.height}"

    def __hash__(self):
        return hash((self.height, self.coordinates))


def read_input_file_as_start_and_end_cells() -> tuple[Cell, Cell]:
    matrix: list[list[Cell]] = []
    start_cell: Cell
    end_cell: Cell

    with open(INPUT_FILE) as f:
        for i, line in enumerate(f.read().splitlines()):
            row = []
            for j, char in enumerate(line):
                coords = Coordinates(i, j)
                if char == Marker.START.value:
                    cell = start_cell = Cell(1, coords)
                elif char == Marker.END.value:
                    cell = end_cell = Cell(27, coords)
                else:
                    cell = Cell(ord(char) - 96, coords)
                row.append(cell)
            matrix.append(row)

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
                if 0 <= coords.x < len(matrix) and 0 <= coords.y < len(matrix[0]):
                    target_cell = matrix[coords.x][coords.y]
                    if target_cell.height <= cell.height + 1:
                        cell.higher_neighbors.append(matrix[coords.x][coords.y])

    return start_cell, end_cell


def get_zone_with_same_height(cell: Cell) -> list[Cell]:
    queue = [cell]
    visited = set()
    while queue:
        cell = queue.pop(0)
        cell: Cell
        if cell in visited:
            continue
        visited.add(cell)
        for neighbour in cell.higher_neighbors:
            if neighbour.height == cell.height:
                queue.append(neighbour)
    return list(visited)


def bfs(start_cell: Cell, end_cell: Cell) -> tuple[int, set[Cell]]:
    queue = [[start_cell, 0]]
    visited = set()
    while queue:
        cell, value = queue.pop(0)
        cell: Cell
        value: int
        if cell in visited:
            continue
        visited.add(cell)
        if cell == end_cell:
            return value, visited
        for neighbour in cell.higher_neighbors:
            if neighbour not in visited:
                queue.append([neighbour, value + 1])
    return -1, visited


def find_shortest_length(start_cell: Cell, end_cell: Cell) -> int:
    queue = [[start_cell, 0]]
    visited = set()
    while queue:
        cell, value = queue.pop(0)
        cell: Cell
        value: int
        if cell in visited:
            continue
        visited.add(cell)
        if cell == end_cell:
            return value
        for neighbour in cell.higher_neighbors:
            if neighbour not in visited:
                queue.append([neighbour, value + 1])
    return -1


def part_one() -> int:
    """https://adventofcode.com/2022/day/12"""
    start_cell, end_cell = read_input_file_as_start_and_end_cells()
    score = find_shortest_length(start_cell, end_cell)
    return score


def part_two() -> int:
    """https://adventofcode.com/2022/day/12#part2"""
    start_cell, end_cell = read_input_file_as_start_and_end_cells()
    start_cells = get_zone_with_same_height(start_cell)
    scores = [find_shortest_length(start_cell, end_cell) for start_cell in start_cells]
    return min(scores)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
