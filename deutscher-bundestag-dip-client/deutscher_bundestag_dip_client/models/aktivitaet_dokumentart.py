from enum import Enum


class AktivitaetDokumentart(str, Enum):
    DRUCKSACHE = "Drucksache"
    PLENARPROTOKOLL = "Plenarprotokoll"

    def __str__(self) -> str:
        return str(self.value)
