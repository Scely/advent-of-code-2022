from enum import Enum
from typing import Iterator


INPUT_FILE = "02/input.txt"


class Shifumi(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class RoundState(Enum):
    WIN = 6
    LOSE = 0
    DRAW = 3


input_to_shifumi = {
    "A": Shifumi.ROCK,
    "B": Shifumi.PAPER,
    "C": Shifumi.SCISSORS,
    "X": Shifumi.ROCK,
    "Y": Shifumi.PAPER,
    "Z": Shifumi.SCISSORS,
}

input_to_state = {
    "X": RoundState.LOSE,
    "Y": RoundState.DRAW,
    "Z": RoundState.WIN,
}

winner = {
    Shifumi.ROCK: Shifumi.PAPER,
    Shifumi.PAPER: Shifumi.SCISSORS,
    Shifumi.SCISSORS: Shifumi.ROCK,
}

loser = {v: k for k, v in winner.items()}


def get_round_state_from_moves(
    opponent_move: Shifumi, current_move: Shifumi
) -> RoundState:
    if current_move is winner[opponent_move]:
        return RoundState.WIN
    elif current_move is loser[opponent_move]:
        return RoundState.LOSE
    return RoundState.DRAW


def get_best_move_from_state(
    opponent_move: Shifumi, expected_state: RoundState
) -> Shifumi:
    if expected_state is RoundState.WIN:
        return winner[opponent_move]
    elif expected_state is RoundState.LOSE:
        return loser[opponent_move]
    return opponent_move


def get_points(move: Shifumi, round_state: RoundState) -> int:
    return move.value + round_state.value


def read_input_file(input_map_a: dict, input_map_b: dict) -> Iterator[list]:
    with open(INPUT_FILE) as file:
        for line in file.read().splitlines():
            input_a, input_b = line.split(" ")
            yield [input_map_a[input_a], input_map_b[input_b]]


def part_one() -> int:
    """https://adventofcode.com/2022/day/2"""
    score = 0
    for opponent_move, current_move in read_input_file(
        input_to_shifumi, input_to_shifumi
    ):
        round_state = get_round_state_from_moves(opponent_move, current_move)
        score += get_points(current_move, round_state)
    return score


def part_two() -> int:
    """https://adventofcode.com/2022/day/2#part2"""
    score = 0
    for opponent_move, expected_state in read_input_file(
        input_to_shifumi, input_to_state
    ):
        current_move = get_best_move_from_state(opponent_move, expected_state)
        score += get_points(current_move, expected_state)
    return score


if __name__ == "__main__":
    print(part_one())
    print(part_two())
