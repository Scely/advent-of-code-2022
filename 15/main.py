import re
from aoctools.grid import Coordinates
from itertools import pairwise
from collections import OrderedDict as odict

INPUT_FILE = "15/input.txt"
LIMIT = 4000000


def read_input_file() -> tuple[Coordinates, Coordinates]:
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            regex = r"Sensor at x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+): closest beacon is at x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)"
            if regex_result := re.match(regex, line):
                coords = regex_result.groupdict()
                sensor = Coordinates(int(coords["sensor_x"]), int(coords["sensor_y"]))
                beacon = Coordinates(int(coords["beacon_x"]), int(coords["beacon_y"]))
                yield [sensor, beacon]


def find_manhattan_distance(
    sensor_coords: Coordinates, beacon_coords: Coordinates
) -> int:
    return abs(sensor_coords.x - beacon_coords.x) + abs(
        sensor_coords.y - beacon_coords.y
    )


def find_segments_on_y_axis(
    y: int, sensors: list[Coordinates], beacons: list[Coordinates]
) -> tuple[Coordinates, Coordinates]:
    res = []
    res_2 = {}
    for sensor, beacon in zip(sensors, beacons):
        sensor: Coordinates
        beacon: Coordinates
        distance = find_manhattan_distance(sensor, beacon)

        if sensor.y > y:
            orthogonal_pivot = Coordinates(sensor.x, sensor.y - distance)
        elif sensor.y <= y:
            orthogonal_pivot = Coordinates(sensor.x, sensor.y + distance)

        if min(orthogonal_pivot.y, sensor.y) <= y <= max(orthogonal_pivot.y, sensor.y):
            n = abs(orthogonal_pivot.y - y)
            start = Coordinates(orthogonal_pivot.x - n, y)
            end = Coordinates(orthogonal_pivot.x + n + 1, y)
            # print(start, end)
            if res_2.get(start):
                res_2[start].append(end)
            else:
                res_2[start] = [end]
    # TODO trier non pas par ordre croissant,
    # Mais il faut reconstruire une range cohérente
    res_2 = odict(sorted(res_2.items()))
    start_tmp = None
    end_tmp = None
    res_3 = []
    # print("AH", res_2)
    # print("sorted", sorted(res_2))
    # print("sorted len", len(sorted(res_2)))
    for k, v in res_2.items():
        if not start_tmp:
            start_tmp = k
            end_tmp = max(v)
        elif k <= end_tmp:
            if k <= start_tmp:
                end_tmp = max(v)
            else:
                end_tmp = max(end_tmp, max(v))
        else:
            res_3.append([start_tmp, end_tmp])
            start_tmp = k
            end_tmp = max(v)
    res_3.append([start_tmp, end_tmp])
    res = []
    [res.append(item) for item in res_3]
    for start_pivot, end_pivot in res:
        if start_pivot.x == end_pivot.x:
            continue
        # print(f"{start_pivot} -> {end_pivot}")
        yield (start_pivot, end_pivot)


def get_coords_with_y_equals(y: int, coords: list[Coordinates]) -> list[Coordinates]:
    return set([coord for coord in coords if coord.y == y])


def part_one() -> int:
    """https://adventofcode.com/2022/day/15"""
    y = LIMIT // 2
    sensors, beacons = zip(*list(read_input_file()))
    d = 0
    d -= len(get_coords_with_y_equals(y, sensors))
    d -= len(get_coords_with_y_equals(y, beacons))
    for start_pivot, end_pivot in find_segments_on_y_axis(y, sensors, beacons):
        d += find_manhattan_distance(start_pivot, end_pivot)
    return d


def part_two() -> int:
    """https://adventofcode.com/2022/day/15#part2"""
    y = 3204480
    sensors, beacons = zip(*list(read_input_file()))
    # for y in range(y, y + 1):
    for y in range(0, LIMIT + 1):
        # for y in range(3204480 - 1, LIMIT + 1):
        d = 0
        tmp = []
        for start_pivot, end_pivot in find_segments_on_y_axis(y, sensors, beacons):
            if end_pivot.x < 0:
                continue
            if start_pivot.x < 0:
                start_pivot = Coordinates(0, start_pivot.y)
            if start_pivot.x > LIMIT:
                break
            if end_pivot.x > LIMIT:
                end_pivot = Coordinates(LIMIT, end_pivot.y)
            d += find_manhattan_distance(start_pivot, end_pivot)
            tmp.append([start_pivot, end_pivot])
        if d != LIMIT:
            result = tmp[0][1]
            return result.x * 4000000 + result.y
    return -1


if __name__ == "__main__":
    # print(part_one())
    # 13784551204480
    print(part_two())
    # 13784551204480
    # python 15/lol.py  < 15/input.txt
