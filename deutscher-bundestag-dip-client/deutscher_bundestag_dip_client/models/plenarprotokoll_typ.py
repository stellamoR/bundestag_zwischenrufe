from enum import Enum


class PlenarprotokollTyp(str, Enum):
    DOKUMENT = "Dokument"

    def __str__(self) -> str:
        return str(self.value)
