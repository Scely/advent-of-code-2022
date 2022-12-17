from dataclasses import dataclass


@dataclass
class Coordinates:
    x: int
    y: int

    @classmethod
    def to_the_left_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x - 1, y=other.y)

    @classmethod
    def at_the_top_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x, y=other.y - 1)

    @classmethod
    def to_the_right_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x + 1, y=other.y)

    @classmethod
    def at_the_bottom_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x, y=other.y + 1)

    @classmethod
    def at_the_top_left_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x - 1, y=other.y - 1)

    @classmethod
    def at_the_top_right_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x + 1, y=other.y - 1)

    @classmethod
    def at_the_bottom_left_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x - 1, y=other.y + 1)

    @classmethod
    def at_the_bottom_right_of(cls, other: "Coordinates") -> "Coordinates":
        return cls(x=other.x + 1, y=other.y + 1)

    def is_verticaly_aligned(self, other: "Coordinates") -> bool:
        return self.x == other.x

    def is_horizontaly_aligned(self, other: "Coordinates") -> bool:
        return self.y == other.y

    def is_on_the_left_of(self, other: "Coordinates") -> bool:
        return self.x < other.x

    def is_at_the_top_of(self, other: "Coordinates") -> bool:
        return self.y < other.y

    def is_on_the_right_of(self, other: "Coordinates") -> bool:
        return self.x > other.x

    def is_at_the_bottom_of(self, other: "Coordinates") -> bool:
        return self.y > other.y

    def is_at_the_top_left_of(self, other: "Coordinates") -> bool:
        return self.is_on_the_left_of(other) and self.is_at_the_top_of(other)

    def is_at_the_top_right_of(self, other: "Coordinates") -> bool:
        return self.is_on_the_right_of(other) and self.is_at_the_top_of(other)

    def is_at_the_bottom_left_of(self, other: "Coordinates") -> bool:
        return self.is_on_the_left_of(other) and self.is_at_the_bottom_of(other)

    def is_at_the_bottom_right_of(self, other: "Coordinates") -> bool:
        return self.is_on_the_right_of(other) and self.is_at_the_bottom_of(other)

    def is_valid(self, width: int, height: int = None) -> bool:
        if height is None:
            height = width
        return 0 <= self.x < width and 0 <= self.y < height

    def __str__(self) -> str:
        return f"[{self.x};{self.y}]"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Coordinates):
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def __le__(self, other):
        return self.x < other.x or (self.x == other.x and self.y <= other.y)
