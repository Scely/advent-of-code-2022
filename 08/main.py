from dataclasses import dataclass
from aoctools.grid import Coordinates
from aoctools.math import mul

INPUT_FILE = "08/input.txt"


@dataclass
class Tree:
    height: int
    coordinates: Coordinates
    visible: bool = False

    def __repr__(self):
        return f"({self.coordinates}={self.height})"

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Forest:
    trees: list[list[Tree]]

    def __str__(self) -> str:
        return "\n".join(str(row) for row in self.trees)

    def make_trees_horizontally_visible(self, from_left: bool) -> "Forest":
        for row in self.trees:
            current_tree_heigth = -1
            for tree in row if from_left else reversed(row):
                if tree.height > current_tree_heigth:
                    tree.visible = True
                    current_tree_heigth = tree.height
        return self

    def make_trees_vertically_visible(self, from_top: bool) -> "Forest":
        for column in range(len(self.trees[0])):
            current_tree_heigth = -1
            for row in self.trees if from_top else reversed(self.trees):
                if row[column].height > current_tree_heigth:
                    row[column].visible = True
                    current_tree_heigth = row[column].height
        return self

    def make_trees_visible_from_left(self) -> "Forest":
        return self.make_trees_horizontally_visible(from_left=True)

    def make_trees_visible_from_right(self) -> "Forest":
        return self.make_trees_horizontally_visible(from_left=False)

    def make_trees_visible_from_top(self) -> "Forest":
        return self.make_trees_vertically_visible(from_top=True)

    def make_trees_visible_from_bottom(self) -> "Forest":
        return self.make_trees_vertically_visible(from_top=False)

    def make_trees_visible_from_outside(self) -> "Forest":
        self.make_trees_visible_from_left()
        self.make_trees_visible_from_right()
        self.make_trees_visible_from_top()
        self.make_trees_visible_from_bottom()
        return self

    def get_tree(self, coords: Coordinates) -> Tree | None:
        if coords.is_valid(len(self.trees), len(self.trees[0])):
            return self.trees[coords.y][coords.x]
        return None

    def get_tree_on_the_right(self, tree: Tree) -> Tree | None:
        return self.get_tree(Coordinates.to_the_right_of(tree.coordinates))

    def get_tree_on_the_left(self, tree: Tree) -> Tree | None:
        return self.get_tree(Coordinates.to_the_left_of(tree.coordinates))

    def get_tree_on_the_top(self, tree: Tree) -> Tree | None:
        return self.get_tree(Coordinates.at_the_top_of(tree.coordinates))

    def get_tree_on_the_bottom(self, tree: Tree) -> Tree | None:
        return self.get_tree(Coordinates.at_the_bottom_of(tree.coordinates))

    def is_tree_at_the_edge(self, tree: Tree) -> bool:
        return (
            tree.coordinates.x == 0
            or tree.coordinates.x == len(self.trees) - 1
            or tree.coordinates.y == 0
            or tree.coordinates.y == len(self.trees[0]) - 1
        )

    def count_visible_trees(self) -> int:
        count = 0
        for row in self.trees:
            for tree in row:
                if tree.visible:
                    count += 1
        return count

    def get_scenic_score(self, tree: Tree) -> int:
        score_multipliers: list[int] = []

        for get_adjacent_tree in [
            self.get_tree_on_the_top,
            self.get_tree_on_the_left,
            self.get_tree_on_the_bottom,
            self.get_tree_on_the_right,
        ]:
            score = 0
            selected_tree: Tree = tree
            while adjacent_tree := get_adjacent_tree(selected_tree):
                score += 1
                if adjacent_tree.height >= tree.height:
                    break
                selected_tree = adjacent_tree
            score_multipliers.append(score)
        return mul(score_multipliers)

    def get_highest_scenic_score(self) -> int:
        scores: list[int] = []
        for row in self.trees:
            for tree in row:
                if tree.visible and not self.is_tree_at_the_edge(tree):
                    scores.append(self.get_scenic_score(tree))
        return max(scores)


def read_input_file_as_forest() -> Forest:
    trees: list[list[Tree]] = []
    with open(INPUT_FILE) as f:
        for y, line in enumerate(f.read().splitlines()):
            trees.append(
                [Tree(int(tree), Coordinates(x, y)) for x, tree in enumerate(line)]
            )
    return Forest(trees).make_trees_visible_from_outside()


def part_one() -> int:
    """https://adventofcode.com/2022/day/8"""
    forest = read_input_file_as_forest()
    return forest.count_visible_trees()


def part_two() -> int:
    """https://adventofcode.com/2022/day/8#part2"""
    forest = read_input_file_as_forest()
    return forest.get_highest_scenic_score()


if __name__ == "__main__":
    print(part_one())
    print(part_two())
