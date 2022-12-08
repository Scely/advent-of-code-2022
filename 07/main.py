from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Union
from operator import lt as less_than, gt as greater_than


INPUT_FILE = "07/input.txt"


class ShellWords(Enum):
    CHANGE_DIRECTORY = "cd"
    BANG = "$"
    DIRECTORY = "dir"
    FILE = "file"
    ROOT = "/"
    PARENT = ".."


@dataclass
class File:
    name: str
    size: int = 0

    def get_size(self) -> int:
        return self.size

    def __str__(self):
        return f"- {self.name} ({ShellWords.FILE.value}, {self.size})"

    def __int__(self):
        return self.get_size()


@dataclass
class Directory:
    name: str
    parent: Union["Directory", None]
    children: list["Directory"] = field(default_factory=lambda: [])

    @classmethod
    def root(cls):
        root_instance = cls(ShellWords.ROOT.value, None)
        cls.parent = root_instance
        return root_instance

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

    def create_subdirectory(self, name: str) -> None:
        for child in self.children:
            if isinstance(child, Directory) and child.name == name:
                raise ValueError(f"Directory {name} already exists")
        self.children.append(Directory(name, self))

    def create_file(self, name: str, size: int) -> None:
        self.children.append(File(name, size))

    def __str__(self):
        return f"- {self.name} ('{ShellWords.DIRECTORY.value}, {self.get_size()})"

    def __int__(self):
        return self.get_size()

    def __radd__(self, other: int):
        return self + other


@dataclass
class Filesystem:

    available_space: int = 70000000
    root: Directory = None
    current_directory: Directory = None

    def get_child_directory(self, name: str) -> Directory:
        for child in self.current_directory.children:
            if isinstance(child, Directory) and child.name == name:
                return child
        raise ValueError(f"Child directory {name} not found")

    def change_directory(self, path: str) -> None:
        if path == ShellWords.ROOT.value:
            if not self.root:
                self.root = Directory.root()
            self.current_directory = self.root
        elif path == ShellWords.PARENT.value:
            self.current_directory = self.current_directory.parent
        else:
            self.current_directory = self.get_child_directory(path)

    def create_directory(self, name: str) -> None:
        self.current_directory.create_subdirectory(name)

    def create_file(self, name: str, size: int) -> None:
        self.current_directory.create_file(name, size)

    def get_directories(self) -> list[Directory]:
        directories: list[Directory] = []

        def recursive_search(node: Directory, directories: list[Directory]):
            if isinstance(node, Directory):
                directories.append(node)
                for child in node.children:
                    recursive_search(child, directories)

        recursive_search(self.root, directories)
        return directories

    def tree(self):
        def recursive_tree(node: Directory | File, level=0):
            print(f"{'  ' * level}{str(node)}")
            if isinstance(node, Directory):
                for child in node.children:
                    recursive_tree(child, level + 1)

        recursive_tree(self.root)

    def get_remaining_space(self) -> int:
        return self.available_space - self.root.get_size()

    def get_directory_sizes_when_size_is_(self, operator: Any, size: int) -> list[int]:
        return [
            directory.get_size()
            for directory in self.get_directories()
            if operator(directory.get_size(), size)
        ]


def read_input_file_as_filesystem() -> Filesystem:
    fs = Filesystem()
    with open(INPUT_FILE) as f:
        for line in f.read().splitlines():
            exp = line.split(" ")
            if exp[0] == ShellWords.BANG.value:
                if exp[1] == ShellWords.CHANGE_DIRECTORY.value:
                    fs.change_directory(exp[2])
            else:
                if exp[0] == ShellWords.DIRECTORY.value:
                    fs.create_directory(exp[1])
                else:
                    fs.create_file(exp[1], size=int(exp[0]))
    return fs


def part_one() -> int:
    """https://adventofcode.com/2022/day/7"""
    fs = read_input_file_as_filesystem()
    # fs.tree()
    maximum_dir_size = 100000
    return sum(fs.get_directory_sizes_when_size_is_(less_than, maximum_dir_size))


def part_two() -> int:
    """https://adventofcode.com/2022/day/7#part2"""
    fs = read_input_file_as_filesystem()
    # fs.tree()
    minimum_dir_size = 30000000 - fs.get_remaining_space()
    return min(fs.get_directory_sizes_when_size_is_(greater_than, minimum_dir_size))


if __name__ == "__main__":
    print(part_one())
    print(part_two())
