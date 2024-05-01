from enum import Enum


class DeskriptorTyp(str, Enum):
    FREIER_DESKRIPTOR = "Freier Deskriptor"
    GEOGRAPH_BEGRIFFE = "Geograph. Begriffe"
    INSTITUTIONEN = "Institutionen"
    PERSONEN = "Personen"
    RECHTSMATERIALIEN = "Rechtsmaterialien"
    SACHBEGRIFFE = "Sachbegriffe"

    def __str__(self) -> str:
        return str(self.value)
