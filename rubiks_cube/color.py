from enum import Enum


class Color(Enum):
    BLUE = 0
    RED = 1
    YELLOW = 2
    GREEN = 3
    ORANGE = 4
    WHITE = 5

    def to_char(self) -> str:
        return self.name[0]
