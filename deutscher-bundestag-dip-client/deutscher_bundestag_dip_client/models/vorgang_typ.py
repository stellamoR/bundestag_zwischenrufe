from enum import Enum


class VorgangTyp(str, Enum):
    VORGANG = "Vorgang"

    def __str__(self) -> str:
        return str(self.value)
