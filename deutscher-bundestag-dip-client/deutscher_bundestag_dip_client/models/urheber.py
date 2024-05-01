from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.urheber_rolle import UrheberRolle
from ..types import UNSET, Unset

T = TypeVar("T", bound="Urheber")


@_attrs_define
class Urheber:
    """Liefert den körperschaftlichen Urheber einer Bundestags- oder Bundesratsdrucksache, z. B. einen Ausschuss, eine
    Fraktion, die Bundesregierung, ein Bundesland oder dergleichen.

        Attributes:
            bezeichnung (str):  Example: B90/GR.
            titel (str):  Example: Fraktion BÜNDNIS 90/DIE GRÜNEN.
            einbringer (Union[Unset, bool]):
            rolle (Union[Unset, UrheberRolle]):
    """

    bezeichnung: str
    titel: str
    einbringer: Union[Unset, bool] = UNSET
    rolle: Union[Unset, UrheberRolle] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        bezeichnung = self.bezeichnung

        titel = self.titel

        einbringer = self.einbringer

        rolle: Union[Unset, str] = UNSET
        if not isinstance(self.rolle, Unset):
            rolle = self.rolle.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bezeichnung": bezeichnung,
                "titel": titel,
            }
        )
        if einbringer is not UNSET:
            field_dict["einbringer"] = einbringer
        if rolle is not UNSET:
            field_dict["rolle"] = rolle

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        bezeichnung = d.pop("bezeichnung")

        titel = d.pop("titel")

        einbringer = d.pop("einbringer", UNSET)

        _rolle = d.pop("rolle", UNSET)
        rolle: Union[Unset, UrheberRolle]
        if isinstance(_rolle, Unset):
            rolle = UNSET
        else:
            rolle = UrheberRolle(_rolle)

        urheber = cls(
            bezeichnung=bezeichnung,
            titel=titel,
            einbringer=einbringer,
            rolle=rolle,
        )

        urheber.additional_properties = d
        return urheber

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
