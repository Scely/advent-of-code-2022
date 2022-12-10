from enum import Enum


INPUT_FILE = "10/input.txt"


class Pixel(Enum):
    ON = "#"
    OFF = "."

    def __str__(self):
        return self.value


def read_input_file():
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            yield line.split(" ")


def input_as_current_register_value():
    X = 1
    for instruction in read_input_file():
        for i in range(len(instruction)):
            # start of cycle
            yield X
            # end of cycle
            if i == 1:
                X += int(instruction[i])


def part_one() -> int:
    """https://adventofcode.com/2022/day/10"""
    signal_strengths = [
        X * cycle
        for cycle, X in enumerate(input_as_current_register_value(), start=1)
        if cycle % 40 == 20
    ]
    return sum(signal_strengths)


def part_two() -> str:
    """https://adventofcode.com/2022/day/10#part2"""
    output = ""
    for cycle, X in enumerate(input_as_current_register_value(), start=1):
        if cycle % 40 == 1 and cycle != 1:
            output += "\n"
        pixel_position = [X - 1, X, X + 1]
        if (cycle - 1) % 40 in pixel_position:
            output += str(Pixel.ON)
        else:
            output += str(Pixel.OFF)
    return output


if __name__ == "__main__":
    print(part_one())
    print(part_two())
