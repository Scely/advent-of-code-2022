INPUT_FILE = "13/input.txt"

import ast
from collections import UserList
from typing import Iterator, Union

from aoctools.math import mul


class Packet(UserList):
    def __init__(self, iterable) -> None:
        super().__init__(list(iterable))

    @staticmethod
    def _recursive_comparison(item_left: list | int, item_right: list | int) -> bool:
        if isinstance(item_left, int) and isinstance(item_right, int):
            if item_left != item_right:
                return item_left < item_right

        elif isinstance(item_left, list) and isinstance(item_right, list):
            for i in range(min(len(item_left), len(item_right))):
                if item_left[i] != item_right[i]:
                    return Packet._recursive_comparison(item_left[i], item_right[i])
            if len(item_left) != len(item_right):
                return len(item_left) < len(item_right)

        elif isinstance(item_left, int) and isinstance(item_right, list):
            return Packet._recursive_comparison([item_left], item_right)

        elif isinstance(item_left, list) and isinstance(item_right, int):
            return Packet._recursive_comparison(item_left, [item_right])

        return True

    @staticmethod
    def compare(
        item_left: Union["Packet", list, int], item_right: Union["Packet", list, int]
    ) -> bool:
        data_left = item_left.data if isinstance(item_left, Packet) else item_left
        data_right = item_right.data if isinstance(item_right, Packet) else item_right
        return Packet._recursive_comparison(data_left, data_right)

    def __lt__(self, other: Union["Packet", list, int]) -> bool:
        return self.compare(self.data, other)

    def __gt__(self, other: Union["Packet", list, int]) -> bool:
        return self.compare(other, self.data)


def read_input_file_as_packet() -> Iterator[list]:
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            if line:
                yield Packet(ast.literal_eval(line))


def read_input_file_as_pair_of_packets() -> Iterator[tuple[Packet]]:
    packets_iter = read_input_file_as_packet()
    for packets in packets_iter:
        yield (packets, next(packets_iter))


def part_one() -> int:
    """https://adventofcode.com/2022/day/13"""
    score = 0
    for i, packets in enumerate(read_input_file_as_pair_of_packets(), start=1):
        packet_left, packet_right = packets
        if packet_left < packet_right:
            score += i
    return score


def part_two() -> int:
    """https://adventofcode.com/2022/day/13#part2"""
    divider_packets = [Packet([[2]]), Packet([[6]])]
    all_packets = sorted(list(read_input_file_as_packet()) + divider_packets)
    return mul(
        [all_packets.index(divider_packet) + 1 for divider_packet in divider_packets]
    )


if __name__ == "__main__":
    print(part_one())
    print(part_two())
