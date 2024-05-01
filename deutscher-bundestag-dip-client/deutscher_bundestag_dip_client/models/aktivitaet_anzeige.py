from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AktivitaetAnzeige")


@_attrs_define
class AktivitaetAnzeige:
    """Liefert im Vorgangsablauf die beim Vorgangsschritt zur Anzeige vorgesehenen Aktivitäten, z. B. eine Rede eines MdB
    beim Vorgangsschritt 1. Beratung in einem Gesetzgebungsvorgang.

        Attributes:
            aktivitaetsart (str):  Example: Rede.
            titel (str):  Example: Prof. Dr. Patrick Sensburg, MdB, CDU/CSU.
            pdf_url (Union[Unset, str]):  Example: https://dserver.bundestag.de/btp/19/19083.pdf#P.9800.
            seite (Union[Unset, str]):  Example: 9800D.
    """

    aktivitaetsart: str
    titel: str
    pdf_url: Union[Unset, str] = UNSET
    seite: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        aktivitaetsart = self.aktivitaetsart

        titel = self.titel

        pdf_url = self.pdf_url

        seite = self.seite

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "aktivitaetsart": aktivitaetsart,
                "titel": titel,
            }
        )
        if pdf_url is not UNSET:
            field_dict["pdf_url"] = pdf_url
        if seite is not UNSET:
            field_dict["seite"] = seite

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        aktivitaetsart = d.pop("aktivitaetsart")

        titel = d.pop("titel")

        pdf_url = d.pop("pdf_url", UNSET)

        seite = d.pop("seite", UNSET)

        aktivitaet_anzeige = cls(
            aktivitaetsart=aktivitaetsart,
            titel=titel,
            pdf_url=pdf_url,
            seite=seite,
        )

        aktivitaet_anzeige.additional_properties = d
        return aktivitaet_anzeige

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
