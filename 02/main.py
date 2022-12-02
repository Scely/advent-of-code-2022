from enum import Enum


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

make_win = {
    Shifumi.ROCK: Shifumi.PAPER,
    Shifumi.PAPER: Shifumi.SCISSORS,
    Shifumi.SCISSORS: Shifumi.ROCK,
}

make_lose = {v: k for k, v in make_win.items()}


def get_round_state_from_moves(
    opponent_move: Shifumi, current_move: Shifumi
) -> RoundState:
    if opponent_move is make_win[current_move]:
        return RoundState.LOSE
    elif opponent_move is make_lose[current_move]:
        return RoundState.WIN
    return RoundState.DRAW


def get_move_from_state(opponent_move: Shifumi, expected_state: RoundState) -> Shifumi:
    if expected_state is RoundState.WIN:
        return make_win[opponent_move]
    elif expected_state is RoundState.LOSE:
        return make_lose[opponent_move]
    return opponent_move


def get_points(move: Shifumi, round_state: RoundState) -> int:
    return move.value + round_state.value


def part_one() -> int:
    """https://adventofcode.com/2022/day/2"""
    with open(INPUT_FILE) as f:
        personal_score = 0
        for line in f.read().splitlines():
            opp, cur = line.split(" ")

            opponent_move = input_to_shifumi[opp]
            current_move = input_to_shifumi[cur]
            expected_state = get_round_state_from_moves(opponent_move, current_move)

            personal_score += get_points(current_move, expected_state)
    return personal_score


def part_two():
    """https://adventofcode.com/2022/day/2#part2"""
    with open(INPUT_FILE) as f:
        personal_score = 0
        for line in f.read().splitlines():
            opp, sta = line.split(" ")

            opponent_move = input_to_shifumi[opp]
            expected_state = input_to_state[sta]
            current_move = get_move_from_state(opponent_move, expected_state)

            personal_score += get_points(current_move, expected_state)
    return personal_score


if __name__ == "__main__":
    print(part_one())
    print(part_two())
