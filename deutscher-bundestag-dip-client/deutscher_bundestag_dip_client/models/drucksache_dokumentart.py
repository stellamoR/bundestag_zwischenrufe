from enum import Enum


class DrucksacheDokumentart(str, Enum):
    DRUCKSACHE = "Drucksache"

    def __str__(self) -> str:
        return str(self.value)
