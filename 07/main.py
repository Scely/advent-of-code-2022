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
    parent: "Directory" = None
    children: list[Union["Directory", File]] = field(default_factory=lambda: [])

    @classmethod
    def root(cls):
        root_instance = cls(ShellWords.ROOT.value, None)
        cls.parent = root_instance
        return root_instance

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

    def get_child(self, name) -> Union["Directory", File]:
        for child in self.children:
            if child.name == name:
                return child
        raise ValueError(f"Child {name} not found")

    def check_if_child_already_exists(self, name: str, inst: type) -> None:
        for child in self.children:
            if isinstance(child, inst) and child.name == name:
                raise ValueError(f"{inst.__name__} {name} already exists")

    def make_subdirectory(self, name: str) -> "Directory":
        self.check_if_child_already_exists(name, Directory)
        new_directory = Directory(name, self)
        self.children.append(new_directory)
        return new_directory

    def make_file(self, name: str, size: int) -> File:
        self.check_if_child_already_exists(name, File)
        new_file = File(name, size)
        self.children.append(new_file)
        return new_file

    def get_directories(self) -> list["Directory"]:
        directories: list[Directory] = []

        def recursive_search(node: Directory, directories: list[Directory]):
            if isinstance(node, Directory):
                directories.append(node)
                for child in node.children:
                    recursive_search(child, directories)

        recursive_search(self, directories)
        return directories

    def tree(self) -> None:
        def recursive_tree(node: Directory | File, level=0):
            print(f"{'  ' * level}{str(node)}")
            if isinstance(node, Directory):
                for child in node.children:
                    recursive_tree(child, level + 1)

        recursive_tree(self)

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

    def change_directory(self, path: str) -> "Filesystem":
        if path == ShellWords.ROOT.value:
            if not self.root:
                self.root = Directory.root()
            self.to_root()
        elif path == ShellWords.PARENT.value:
            self.current_directory = self.current_directory.parent
        else:
            self.current_directory = self.current_directory.get_child(path)
        return self

    def to_root(self) -> "Filesystem":
        self.current_directory = self.root
        return self

    def make_directory(self, name: str) -> "Filesystem":
        self.current_directory.make_subdirectory(name)
        return self

    def make_file(self, name: str, size: int) -> "Filesystem":
        self.current_directory.make_file(name, size)
        return self

    def get_directories(self) -> list[Directory]:
        return self.current_directory.get_directories()

    def tree(self) -> None:
        self.current_directory.tree()

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
                    fs.make_directory(exp[1])
                else:
                    fs.make_file(exp[1], size=int(exp[0]))
    return fs.to_root()


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
