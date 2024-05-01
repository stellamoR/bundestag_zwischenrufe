from enum import Enum


class DrucksacheHerausgeber(str, Enum):
    BR = "BR"
    BT = "BT"

    def __str__(self) -> str:
        return str(self.value)
