from enum import Enum


class UrheberRolle(str, Enum):
    B = "B"
    U = "U"

    def __str__(self) -> str:
        return str(self.value)
