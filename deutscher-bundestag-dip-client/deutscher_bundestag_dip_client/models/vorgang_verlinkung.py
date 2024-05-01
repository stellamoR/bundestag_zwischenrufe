from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="VorgangVerlinkung")


@_attrs_define
class VorgangVerlinkung:
    """Verlinkte Verweisung von einem Vorgang auf einen anderen Vorgang, zu dem eine besondere inhaltliche Verbindung
    besteht.

        Attributes:
            id (str): ID eines verknüpften Vorgangs Example: 282237.
            verweisung (str):  Example: Bericht.
            titel (str):  Example: Zwischenbericht zur Reform des Bundeswahlrechts und zur Modernisierung der
                Parlamentsarbeit.
            wahlperiode (int):  Example: 19.
            gesta (Union[Unset, str]):
    """

    id: str
    verweisung: str
    titel: str
    wahlperiode: int
    gesta: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        verweisung = self.verweisung

        titel = self.titel

        wahlperiode = self.wahlperiode

        gesta = self.gesta

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "verweisung": verweisung,
                "titel": titel,
                "wahlperiode": wahlperiode,
            }
        )
        if gesta is not UNSET:
            field_dict["gesta"] = gesta

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        verweisung = d.pop("verweisung")

        titel = d.pop("titel")

        wahlperiode = d.pop("wahlperiode")

        gesta = d.pop("gesta", UNSET)

        vorgang_verlinkung = cls(
            id=id,
            verweisung=verweisung,
            titel=titel,
            wahlperiode=wahlperiode,
            gesta=gesta,
        )

        vorgang_verlinkung.additional_properties = d
        return vorgang_verlinkung

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
