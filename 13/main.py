INPUT_FILE = "13/input.txt"

import ast
from dataclasses import dataclass
from typing import Iterator

from aoctools.math import mul


@dataclass
class Packet(list):
    value: list

    def __getitem__(self, item):
        return self.value[item]

    def __repr__(self) -> str:
        return str(self.value)

    def __add__(self, other: "Packet"):
        return Packet(self.value + other.value)

    @staticmethod
    def compare(item_left: list | int, item_right: list | int) -> bool:
        if isinstance(item_left, int) and isinstance(item_right, int):
            if item_left != item_right:
                return item_left < item_right
        elif isinstance(item_left, list) and isinstance(item_right, list):
            for i in range(min(len(item_left), len(item_right))):
                if item_left[i] != item_right[i]:
                    return Packet.compare(item_left[i], item_right[i])
            if len(item_left) > len(item_right):
                return False
        elif type(item_left) != type(item_right):
            if isinstance(item_left, int):
                return Packet.compare([item_left], item_right)
            else:
                return Packet.compare(item_left, [item_right])
        return True

    def __lt__(self, other: "Packet"):
        result = Packet.compare(self.value, other.value)
        return result


def read_input_file_as_packets() -> Iterator[tuple[Packet]]:
    packets_iter = read_input_file_as_packet()
    for packets in packets_iter:
        yield (packets, next(packets_iter))


def read_input_file_as_packet() -> Iterator[Packet]:
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            if line:
                yield Packet(ast.literal_eval(line))


def part_one() -> int:
    """https://adventofcode.com/2022/day/13"""
    score = 0
    for i, packets in enumerate(read_input_file_as_packets(), start=1):
        packet_left, packet_right = packets
        if packet_left < packet_right:
            score += i
    return score


def part_two() -> int:
    """https://adventofcode.com/2022/day/13#part2"""

    divider_packets = [Packet([[2]]), Packet([[6]])]

    all_packets = sorted(
        [packet for packet in read_input_file_as_packet()] + divider_packets
    )
    return mul(
        [all_packets.index(divider_packet) + 1 for divider_packet in divider_packets]
    )


if __name__ == "__main__":
    print(part_one())
    print(part_two())
