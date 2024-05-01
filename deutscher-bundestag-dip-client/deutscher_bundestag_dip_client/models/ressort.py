from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Ressort")


@_attrs_define
class Ressort:
    """Liefert das Ressort (Bundesministerium), das innerhalb der Bundesregierung federführend für die Ausarbeitung z. B.
    eines Gesetzentwurfs oder eines Antrags oder die Beantwortung von Anfragen ist. Wird nur verwendet, wenn Urheber
    einer Drucksache die Bundesregierung ist.

    Das Ressort wird auch bei persönlichen Urhebern verwendet, um die Funktion von Angehörigen der Bundesregierung zu
    präzisieren, z. B. „Dr. Robert Habeck, Bundesmin., Bundesministerium für Wirtschaft und Klimaschutz“ oder „Dr.
    Florian Toncar, Parl. Staatssekr., Bundesministerium der Finanzen“.

        Attributes:
            federfuehrend (bool):  Example: True.
            titel (str):  Example: Bundesministerium für Wirtschaft und Energie.
    """

    federfuehrend: bool
    titel: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        federfuehrend = self.federfuehrend

        titel = self.titel

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "federfuehrend": federfuehrend,
                "titel": titel,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        federfuehrend = d.pop("federfuehrend")

        titel = d.pop("titel")

        ressort = cls(
            federfuehrend=federfuehrend,
            titel=titel,
        )

        ressort.additional_properties = d
        return ressort

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
