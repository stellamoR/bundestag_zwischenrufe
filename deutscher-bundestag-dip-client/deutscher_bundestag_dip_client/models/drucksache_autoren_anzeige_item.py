from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DrucksacheAutorenAnzeigeItem")


@_attrs_define
class DrucksacheAutorenAnzeigeItem:
    """
    Attributes:
        id (str): ID von Personenstammdaten Example: 546.
        title (str):  Example: Kai Gehring, MdB, BÜNDNIS 90/DIE GRÜNEN.
        autor_titel (str):  Example: Kai Gehring.
    """

    id: str
    title: str
    autor_titel: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        title = self.title

        autor_titel = self.autor_titel

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "autor_titel": autor_titel,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        title = d.pop("title")

        autor_titel = d.pop("autor_titel")

        drucksache_autoren_anzeige_item = cls(
            id=id,
            title=title,
            autor_titel=autor_titel,
        )

        drucksache_autoren_anzeige_item.additional_properties = d
        return drucksache_autoren_anzeige_item

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
