from enum import Enum


class DrucksacheTyp(str, Enum):
    DOKUMENT = "Dokument"

    def __str__(self) -> str:
        return str(self.value)
