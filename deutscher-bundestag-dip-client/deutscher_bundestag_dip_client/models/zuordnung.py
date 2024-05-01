from enum import Enum


class Zuordnung(str, Enum):
    BR = "BR"
    BT = "BT"
    BV = "BV"
    EK = "EK"

    def __str__(self) -> str:
        return str(self.value)
