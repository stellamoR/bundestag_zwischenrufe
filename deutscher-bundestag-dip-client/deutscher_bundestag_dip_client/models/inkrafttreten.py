import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Inkrafttreten")


@_attrs_define
class Inkrafttreten:
    """Liefert im Gesetzgebungsvorgang zu einem verkündeten Gesetz das Datum des Tages, an dem das Gesetz in Kraft tritt
    bzw. an dem Teile eines Gesetzes in Kraft treten.

        Attributes:
            datum (datetime.date):  Example: 2020-06-06.
            erlaeuterung (Union[Unset, str]):  Example: Artikel 1 Nr. 14, Artikel 3 Nr. 4, Artikel 4 Nr. 4.
    """

    datum: datetime.date
    erlaeuterung: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datum = self.datum.isoformat()

        erlaeuterung = self.erlaeuterung

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "datum": datum,
            }
        )
        if erlaeuterung is not UNSET:
            field_dict["erlaeuterung"] = erlaeuterung

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        datum = isoparse(d.pop("datum")).date()

        erlaeuterung = d.pop("erlaeuterung", UNSET)

        inkrafttreten = cls(
            datum=datum,
            erlaeuterung=erlaeuterung,
        )

        inkrafttreten.additional_properties = d
        return inkrafttreten

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
