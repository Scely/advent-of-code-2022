from dataclasses import dataclass
from functools import reduce
import re
import operator
from typing import Iterator

INPUT_FILE = "11/input.txt"

ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


@dataclass
class Monkey:
    id: int
    operation: list[str]
    divisor: int
    id_true: int
    id_false: int
    current_items: list[int]
    inspection_score: int = 0

    def __lt__(self, other: "Monkey") -> bool:
        return self.id < other.id

    def __str__(self) -> str:
        return f"-- ID {self.id} --\n  {self.inspection_score=}\n  {self.operation=}\n  {self.divisor=}\n  {self.id_true=}\n  {self.id_false=}\n  {self.current_items=}\n"

    @classmethod
    def generated_from_string(cls, string: str) -> "Monkey":
        reg = r"Monkey (?P<id>\d+).*\n  Starting items: *(?P<current_items>(.*))\n\D*= old (?P<operation>.*)\n\D*(?P<divisor>\d+)\n\D*(?P<id_true>\d+)\n\D*(?P<id_false>\d+)"

        regex_result = re.match(reg, string)
        monkey = regex_result.groupdict()
        monkey["current_items"] = [
            int(item) for item in monkey["current_items"].split(", ")
        ]
        monkey["operation"] = monkey["operation"].split(" ")
        monkey["divisor"] = int(monkey["divisor"])
        monkey["id_true"] = int(monkey["id_true"])
        monkey["id_false"] = int(monkey["id_false"])
        return cls(**monkey)

    def inspect_and_throw(self, with_weak_limiter: bool = True) -> int:
        worry_level = self.current_items.pop(0)

        if self.operation[1] == "old":
            multiplier = worry_level
        else:
            multiplier = int(self.operation[1])
        worry_level = ops[self.operation[0]](worry_level, multiplier)

        if with_weak_limiter:
            worry_level = int(worry_level / 3)

        self.inspection_score += 1
        return (
            self.id_true if worry_level % self.divisor == 0 else self.id_false,
            worry_level,
        )

    def receive(self, worry_level: int) -> None:
        self.current_items.append(worry_level)


def mul(l: list[int]) -> int:
    return reduce(lambda x, y: x * y, l)


def read_input_file_as_monkey() -> Iterator[Monkey]:
    acc = ""
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            if not line:
                yield Monkey.generated_from_string(acc)
                acc = ""
            else:
                acc += line + "\n"
    yield Monkey.generated_from_string(acc)


def get_monkey_business_level(max_round: int, with_weak_limiter=True) -> int:
    monkeys = sorted(list(read_input_file_as_monkey()))
    n = mul([monkey.divisor for monkey in monkeys])
    for _ in range(1, max_round + 1):
        for monkey in monkeys:
            monkey: Monkey
            while monkey.current_items:
                targeted_index, item = monkey.inspect_and_throw(with_weak_limiter)
                item = item % n  # to improve performances
                monkeys[targeted_index].receive(item)
    scores = sorted([monkey.inspection_score for monkey in monkeys], reverse=True)
    return mul(scores[:2])


def part_one() -> int:
    """https://adventofcode.com/2022/day/11"""
    return get_monkey_business_level(max_round=20)


def part_two() -> int:
    """https://adventofcode.com/2022/day/11#part2"""
    return get_monkey_business_level(max_round=10000, with_weak_limiter=False)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
