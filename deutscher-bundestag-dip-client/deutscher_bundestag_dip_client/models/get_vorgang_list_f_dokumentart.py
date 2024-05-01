from enum import Enum


class GetVorgangListFDokumentart(str, Enum):
    DRUCKSACHE = "Drucksache"
    PLENARPROTOKOLL = "Plenarprotokoll"

    def __str__(self) -> str:
        return str(self.value)
