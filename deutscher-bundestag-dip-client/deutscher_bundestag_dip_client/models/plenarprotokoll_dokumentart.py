from enum import Enum


class PlenarprotokollDokumentart(str, Enum):
    PLENARPROTOKOLL = "Plenarprotokoll"

    def __str__(self) -> str:
        return str(self.value)
