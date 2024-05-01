from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.deskriptor_typ import DeskriptorTyp

T = TypeVar("T", bound="Deskriptor")


@_attrs_define
class Deskriptor:
    """Liefert die mit einer Aktivität zu deren inhaltlichen Beschreibung verknüpften Schlagwörter. Die Schlagwörter
    (Deskriptoren) entstammen dem kontrollierten Vokabular des Parlamentsthesaurus ANTHES/PARTHES und stehen in
    thematischer Beziehung zueinander.

    Siehe auch: VorgangDeskriptor

        Attributes:
            name (str):  Example: Parlamentarische Geschäftsordnung.
            typ (DeskriptorTyp):  Example: Sachbegriffe.
    """

    name: str
    typ: DeskriptorTyp
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        typ = self.typ.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "typ": typ,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        typ = DeskriptorTyp(d.pop("typ"))

        deskriptor = cls(
            name=name,
            typ=typ,
        )

        deskriptor.additional_properties = d
        return deskriptor

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
