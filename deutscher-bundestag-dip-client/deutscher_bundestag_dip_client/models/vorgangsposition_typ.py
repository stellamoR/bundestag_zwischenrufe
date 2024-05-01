from enum import Enum


class VorgangspositionTyp(str, Enum):
    VORGANGSPOSITION = "Vorgangsposition"

    def __str__(self) -> str:
        return str(self.value)
