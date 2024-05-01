from enum import Enum


class BeschlussfassungMehrheit(str, Enum):
    ABSOLUTE_MEHRHEIT = "Absolute Mehrheit"
    ZWEIDRITTELMEHRHEIT = "Zweidrittelmehrheit"

    def __str__(self) -> str:
        return str(self.value)
