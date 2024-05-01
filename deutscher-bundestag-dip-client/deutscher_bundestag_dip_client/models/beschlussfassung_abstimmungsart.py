from enum import Enum


class BeschlussfassungAbstimmungsart(str, Enum):
    ABSTIMMUNG_DURCH_AUFRUF_DER_LÄNDER = "Abstimmung durch Aufruf der Länder"
    GEHEIME_WAHL = "Geheime Wahl"
    HAMMELSPRUNG = "Hammelsprung"
    NAMENTLICHE_ABSTIMMUNG = "Namentliche Abstimmung"
    VERHÄLTNISWAHL = "Verhältniswahl"

    def __str__(self) -> str:
        return str(self.value)
