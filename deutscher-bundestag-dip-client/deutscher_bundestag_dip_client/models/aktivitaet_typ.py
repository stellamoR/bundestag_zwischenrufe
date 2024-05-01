from enum import Enum


class AktivitaetTyp(str, Enum):
    AKTIVITÄT = "Aktivität"

    def __str__(self) -> str:
        return str(self.value)
