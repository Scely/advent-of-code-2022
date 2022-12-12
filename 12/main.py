from dataclasses import dataclass, field
from enum import Enum
from tools.grid import Coordinates

INPUT_FILE = "12/input.txt"


class Marker(Enum):
    START = "S"
    END = "E"


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
                coords = Coordinates(j, i)
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
                if 0 <= coords.x < len(matrix[0]) and 0 <= coords.y < len(matrix):
                    target_cell = matrix[coords.y][coords.x]
                    if target_cell.height <= cell.height + 1:
                        cell.higher_neighbors.append(matrix[coords.y][coords.x])

    return start_cell, end_cell


def breadth_first_search(
    start_cell: Cell, end_cell: Cell = None
) -> tuple[int, set[Cell]]:
    # If end_cell is None, we want to find the zone with the same height
    # Else, we want to find the shortest path to the end_cell
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
            if [neighbour.height == cell.height, neighbour not in visited][
                bool(end_cell)
            ]:
                queue.append([neighbour, value + 1])
    return -1, visited


def find_shortest_length(start_cell: Cell, end_cell: Cell) -> int:
    v, _ = breadth_first_search(start_cell, end_cell)
    return v


def get_zone_with_same_height(cell: Cell) -> list[Cell]:
    _, z = breadth_first_search(cell)
    return list(z)


def part_one() -> int:
    """https://adventofcode.com/2022/day/12"""
    start_cell, end_cell = read_input_file_as_start_and_end_cells()
    score = find_shortest_length(start_cell, end_cell)
    return score


def part_two() -> int:
    """https://adventofcode.com/2022/day/12#part2"""
    original_cell, end_cell = read_input_file_as_start_and_end_cells()
    start_cells = get_zone_with_same_height(original_cell)
    scores = [find_shortest_length(start_cell, end_cell) for start_cell in start_cells]
    return min(scores)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
