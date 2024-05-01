from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Ueberweisung")


@_attrs_define
class Ueberweisung:
    """Liefert den Ausschuss bzw. die Ausschüsse, an die eine Drucksache überwiesen wurde, unter Angabe der Federführung
    und ggf. der Überweisungsart (z. B. „gemäß § 96 Geschäftsordnung BT“).

        Attributes:
            ausschuss (str):  Example: Ausschuss für Wahlprüfung, Immunität und Geschäftsordnung.
            ausschuss_kuerzel (str):  Example: AfWIuG.
            federfuehrung (bool):  Example: True.
            ueberweisungsart (Union[Unset, str]):  Example: gemäß § 96 Geschäftsordnung BT.
    """

    ausschuss: str
    ausschuss_kuerzel: str
    federfuehrung: bool
    ueberweisungsart: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        ausschuss = self.ausschuss

        ausschuss_kuerzel = self.ausschuss_kuerzel

        federfuehrung = self.federfuehrung

        ueberweisungsart = self.ueberweisungsart

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ausschuss": ausschuss,
                "ausschuss_kuerzel": ausschuss_kuerzel,
                "federfuehrung": federfuehrung,
            }
        )
        if ueberweisungsart is not UNSET:
            field_dict["ueberweisungsart"] = ueberweisungsart

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ausschuss = d.pop("ausschuss")

        ausschuss_kuerzel = d.pop("ausschuss_kuerzel")

        federfuehrung = d.pop("federfuehrung")

        ueberweisungsart = d.pop("ueberweisungsart", UNSET)

        ueberweisung = cls(
            ausschuss=ausschuss,
            ausschuss_kuerzel=ausschuss_kuerzel,
            federfuehrung=federfuehrung,
            ueberweisungsart=ueberweisungsart,
        )

        ueberweisung.additional_properties = d
        return ueberweisung

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
