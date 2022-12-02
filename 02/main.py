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


def game(get_current_move_and_round_state: callable) -> int:
    with open(INPUT_FILE) as f:
        score = 0
        for line in f.read().splitlines():
            input_a, input_b = line.split(" ")
            current_move, round_state = get_current_move_and_round_state(
                input_a, input_b
            )
            score += get_points(current_move, round_state)
    return score


def part_one() -> int:
    """https://adventofcode.com/2022/day/2"""

    def by_finding_round_state(
        input_a: str, input_b: str
    ) -> tuple[Shifumi, RoundState]:
        opponent_move: Shifumi = input_to_shifumi[input_a]
        current_move: Shifumi = input_to_shifumi[input_b]
        round_state = get_round_state_from_moves(opponent_move, current_move)
        return current_move, round_state

    return game(by_finding_round_state)


def part_two() -> int:
    """https://adventofcode.com/2022/day/2#part2"""

    def by_finding_best_move(input_a: str, input_b: str) -> tuple[Shifumi, RoundState]:
        opponent_move: Shifumi = input_to_shifumi[input_a]
        expected_state: Shifumi = input_to_state[input_b]
        current_move = get_best_move_from_state(opponent_move, expected_state)
        return current_move, expected_state

    return game(by_finding_best_move)


if __name__ == "__main__":
    print(part_one())
    print(part_two())
