from enum import Enum


class Quadrant(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    def __str__(self) -> str:
        return str(self.value)
