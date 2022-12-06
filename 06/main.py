INPUT_FILE = "06/input.txt"


def find_marker_index(buffer_size: int, start_at: int = 0) -> int:
    buffer = []
    with open(INPUT_FILE) as f:
        f.seek(start_at)
        while True:
            if not (char := f.read(1)):
                break
            buffer.append(char)
            if len(buffer) > buffer_size:
                buffer.pop(0)
            if len(set(buffer)) == buffer_size:
                return f.tell()
    return -1


def part_one() -> int:
    """https://adventofcode.com/2022/day/6"""
    return find_marker_index(4)


def part_two() -> int:
    """https://adventofcode.com/2022/day/6#part2"""
    return find_marker_index(14, start_at=part_one())


if __name__ == "__main__":
    print(part_one())
    print(part_two())
