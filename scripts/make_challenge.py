import argparse
import requests
from io import FileIO, TextIOWrapper
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass


@dataclass
class GenerateChallenge:
    """Generate a challenge from a template and a data file."""

    day: int
    year: int = 2022

    def __post_init__(self) -> None:
        if self.day < 1 or self.day > 25:
            raise ValueError("Invalid day: input must be between 1 and 25")
        if self.year < 2015:
            raise ValueError("Invalid year: challenges started in 2015")

    @classmethod
    def from_cli(cls) -> "GenerateChallenge":
        """Create a GenerateChallenge instance from the command line.

        :return: GenerateChallenge instance.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("day", help="Challenge's day", type=int)
        return cls(vars(parser.parse_args())["day"])

    def get_day_str(self) -> str:
        """Return the day as a string with a leading zero if needed."""
        return str(self.day) if self.day > 9 else f"0{self.day}"

    def get_input_file_content(self) -> bytes:
        """Get the input file content from the website.

        :return: Input file content.
        """
        url = f"https://adventofcode.com/2022/day/{self.day}/input"
        with open("cookie.txt") as f:
            cookie = f.read().strip()
            resp = requests.Session().get(
                url,
                allow_redirects=True,
                cookies={
                    "session": cookie,
                },
            )
        if resp.status_code == 404:
            raise ValueError(
                f"HTTP status code {resp.status_code}. It may be that the challenge has not been released yet."
            )
        return resp.content

    def get_main_file_content(self) -> str:
        """Get the main file content from the template.

        :return: Main file content."""
        day_str = self.get_day_str()
        environment = Environment(loader=FileSystemLoader("templates/"))
        template = environment.get_template("main.jinja")
        return template.render(day=self.day, day_str=day_str, year=self.year)

    def get_day_folder(self) -> Path:
        """Return the day folder.

        :return: Day folder."""
        return Path(self.get_day_str())

    def _make_file(
        self, file_name: str, open_mode: str, get_file_content: callable
    ) -> None:
        """Create a file.

        :param file_name: File name.
        :param open_mode: Open mode.
        :param get_file_content: Function that returns the file content.
        """
        folder = self.get_day_folder()
        file = folder / file_name
        if file.exists():
            print(f"{file} already exists. Skipping...")
            return
        file_content = get_file_content()
        folder.mkdir(exist_ok=True)
        with file.open(open_mode) as f:
            f: TextIOWrapper | FileIO
            f.write(file_content)

    def make_main_file(self) -> None:
        """Create the main file."""
        self._make_file("main.py", "w", self.get_main_file_content)

    def make_input_file(self) -> None:
        """Create the input file."""
        self._make_file("input.txt", "wb", self.get_input_file_content)

    def make(self) -> None:
        """Create the main file and the input file."""
        self.make_input_file()
        self.make_main_file()


if __name__ == "__main__":
    GenerateChallenge.from_cli().make()
