INPUT_FILE = "14/input.txt"

from dataclasses import dataclass, field
from enum import Enum
from functools import reduce
from typing import Iterator
from aoctools.grid import Coordinates

SAND_SOURCE = Coordinates(500, 0)


class Pixel(Enum):
    SAND_SOURCE = "+"
    SAND = "o"
    ROCK = "#"
    FLOWING_SAND = "~"
    AIR = "."


@dataclass
class Cell:
    coordinates: Coordinates
    value: Pixel = Pixel.AIR

    def __str__(self) -> str:
        return self.value.value

    def __repr__(self) -> str:
        return str(self)

    def is_traversable(self) -> bool:
        return self.value in (Pixel.AIR, Pixel.FLOWING_SAND)


# @dataclass
class Grid:
    cells = list[list[Cell]]
    without_floor: bool = True

    def __init__(self, without_floor=True) -> None:
        self.without_floor = without_floor

    def __str__(self) -> str:
        return "\n".join("".join(str(cell) for cell in row) for row in self.cells)

    def __repr__(self) -> str:
        return str(self)

    def get_cell(self, coordinates: Coordinates) -> Cell:
        return self.cells[coordinates.y - self.start_min_y][
            coordinates.x - self.start_min_x
        ]

    def find_cells_between(
        self, start_coord: Coordinates, end_coord: Coordinates
    ) -> None:
        current_coord = start_coord
        resp = []
        while current_coord != end_coord:
            if end_coord.is_verticaly_aligned(current_coord):
                if end_coord.is_at_the_top_of(current_coord):
                    current_coord = self.get_cell(
                        Coordinates.at_the_top_of(current_coord)
                    ).coordinates

                elif end_coord.is_at_the_bottom_of(current_coord):
                    current_coord = self.get_cell(
                        Coordinates.at_the_bottom_of(current_coord)
                    ).coordinates

            elif end_coord.is_horizontaly_aligned(current_coord):
                if end_coord.is_on_the_left_of(current_coord):
                    current_coord = self.get_cell(
                        Coordinates.to_the_left_of(current_coord)
                    ).coordinates

                elif end_coord.is_on_the_right_of(current_coord):
                    current_coord = self.get_cell(
                        Coordinates.to_the_right_of(current_coord)
                    ).coordinates
            resp.append(current_coord)
        resp.pop()
        return resp

    def from_straight_lines(self, straight_lines: list[list[Coordinates]]) -> "Grid":

        self.start_min_y = 0
        if self.without_floor:
            self.start_max_y = self._find_start_max_y(straight_lines)
            self.start_min_x = self._find_start_min_x(straight_lines)
            self.start_max_x = self._find_start_max_x(straight_lines)
        else:
            self.start_max_y = self._find_start_max_y(straight_lines, padding=2)
            self.start_min_x = SAND_SOURCE.x - self.start_max_y
            self.start_max_x = SAND_SOURCE.x + self.start_max_y

            straight_lines += [
                [
                    Coordinates(self.start_min_x, self.start_max_y),
                    Coordinates(self.start_max_x, self.start_max_y),
                ]
            ]
        self.cells = [
            [
                Cell(Coordinates(x, y))
                for x in range(self.start_min_x, self.start_max_x + 1)
            ]
            for y in range(self.start_min_y, self.start_max_y + 1)
        ]
        rock_coords = [
            coords for straight_line in straight_lines for coords in straight_line
        ]

        rock_coords += [
            coords
            for straight_line in straight_lines
            for i in range(len(straight_line) - 1)
            for coords in self.find_cells_between(
                straight_line[i], straight_line[i + 1]
            )
        ]

        for coord in set(rock_coords):
            self.get_cell(coord).value = Pixel.ROCK

        self.get_cell(SAND_SOURCE).value = Pixel.SAND_SOURCE

    def _find_start_min_x(
        self, straight_lines: list[list[Coordinates]], padding: int = 1
    ) -> int:
        return (
            min(
                coordinates.x
                for straight_line in straight_lines
                for coordinates in straight_line
            )
            - padding
        )

    def _find_start_max_x(
        self, straight_lines: list[list[Coordinates]], padding: int = 1
    ) -> int:
        return (
            max(
                coordinates.x
                for straight_line in straight_lines
                for coordinates in straight_line
            )
            + padding
        )

    def _find_start_max_y(
        self, straight_lines: list[list[Coordinates]], padding: int = 1
    ) -> int:
        return (
            max(
                coordinates.y
                for straight_line in straight_lines
                for coordinates in straight_line
            )
            + padding
        )

    def fall_sand(self, cell: Cell):
        cell_coords = cell.coordinates

        for get_adjacent_coords_of in (
            Coordinates.at_the_bottom_of,
            Coordinates.at_the_bottom_left_of,
            Coordinates.at_the_bottom_right_of,
        ):
            get_adjacent_coords_of: callable
            cell_below_coords: Coordinates = get_adjacent_coords_of(cell_coords)
            if not cell_below_coords.is_valid(
                width=self.start_max_x + 1, height=self.start_max_y + 1
            ):
                cell.value = Pixel.FLOWING_SAND
                return False
            cell_below = self.get_cell(cell_below_coords)
            if cell_below.is_traversable():
                if cell.value != Pixel.SAND_SOURCE:
                    cell.value = Pixel.FLOWING_SAND
                cell_below.value = Pixel.SAND
                return self.fall_sand(cell_below)

        if cell.value == Pixel.SAND_SOURCE:
            cell.value = Pixel.SAND
            return True
        return True

    def put_sand(self):
        cell = self.get_cell(SAND_SOURCE)
        if cell.value == Pixel.SAND:
            return False
        return self.fall_sand(cell)


def read_input_file_as_straight_line() -> Iterator[list[Coordinates]]:
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            yield [
                Coordinates(*[int(value) for value in coord.split(",")])
                for coord in line.split(" -> ")
            ]


def number_of_sand_cells(grid: Grid, print_mode=False):
    grid.from_straight_lines(list(read_input_file_as_straight_line()))
    i = 0
    while grid.put_sand():
        if print_mode:
            print(f"ROUND {i}\n{grid}\n\n")
        i += 1
    return i


def part_one() -> int:
    """https://adventofcode.com/2022/day/14"""
    return number_of_sand_cells(Grid())


def part_two() -> int:
    """https://adventofcode.com/2022/day/14#part2"""
    return number_of_sand_cells(Grid(without_floor=False))


if __name__ == "__main__":
    print(part_one())
    print(part_two())
