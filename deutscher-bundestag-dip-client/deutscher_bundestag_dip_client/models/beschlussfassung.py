from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.beschlussfassung_abstimmungsart import BeschlussfassungAbstimmungsart
from ..models.beschlussfassung_mehrheit import BeschlussfassungMehrheit
from ..types import UNSET, Unset

T = TypeVar("T", bound="Beschlussfassung")


@_attrs_define
class Beschlussfassung:
    """Liefert die Beschlussfassung (z. B. Annahme, Ablehnung, Kenntnisnahme) zu einer Drucksache mit Fundstelle im
    Plenarprotokoll sowie Angaben zu ggf. erforderlichen qualifizierten Mehrheiten (`mehrheit`) bzw. der besonderen
    Abstimmungsverfahren (`abstimmungsart`).

        Attributes:
            beschlusstenor (str):  Example: Annahme der Vorlage.
            seite (Union[Unset, str]):  Example: 11B.
            abstimmungsart (Union[Unset, BeschlussfassungAbstimmungsart]):
            abstimm_ergebnis_bemerkung (Union[Unset, str]):  Example: einstimmig.
            grundlage (Union[Unset, str]):  Example: Art. 80 Abs. 2 GG.
            dokumentnummer (Union[Unset, str]):  Example: 19/8.
            mehrheit (Union[Unset, BeschlussfassungMehrheit]):
    """

    beschlusstenor: str
    seite: Union[Unset, str] = UNSET
    abstimmungsart: Union[Unset, BeschlussfassungAbstimmungsart] = UNSET
    abstimm_ergebnis_bemerkung: Union[Unset, str] = UNSET
    grundlage: Union[Unset, str] = UNSET
    dokumentnummer: Union[Unset, str] = UNSET
    mehrheit: Union[Unset, BeschlussfassungMehrheit] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        beschlusstenor = self.beschlusstenor

        seite = self.seite

        abstimmungsart: Union[Unset, str] = UNSET
        if not isinstance(self.abstimmungsart, Unset):
            abstimmungsart = self.abstimmungsart.value

        abstimm_ergebnis_bemerkung = self.abstimm_ergebnis_bemerkung

        grundlage = self.grundlage

        dokumentnummer = self.dokumentnummer

        mehrheit: Union[Unset, str] = UNSET
        if not isinstance(self.mehrheit, Unset):
            mehrheit = self.mehrheit.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "beschlusstenor": beschlusstenor,
            }
        )
        if seite is not UNSET:
            field_dict["seite"] = seite
        if abstimmungsart is not UNSET:
            field_dict["abstimmungsart"] = abstimmungsart
        if abstimm_ergebnis_bemerkung is not UNSET:
            field_dict["abstimm_ergebnis_bemerkung"] = abstimm_ergebnis_bemerkung
        if grundlage is not UNSET:
            field_dict["grundlage"] = grundlage
        if dokumentnummer is not UNSET:
            field_dict["dokumentnummer"] = dokumentnummer
        if mehrheit is not UNSET:
            field_dict["mehrheit"] = mehrheit

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        beschlusstenor = d.pop("beschlusstenor")

        seite = d.pop("seite", UNSET)

        _abstimmungsart = d.pop("abstimmungsart", UNSET)
        abstimmungsart: Union[Unset, BeschlussfassungAbstimmungsart]
        if isinstance(_abstimmungsart, Unset):
            abstimmungsart = UNSET
        else:
            abstimmungsart = BeschlussfassungAbstimmungsart(_abstimmungsart)

        abstimm_ergebnis_bemerkung = d.pop("abstimm_ergebnis_bemerkung", UNSET)

        grundlage = d.pop("grundlage", UNSET)

        dokumentnummer = d.pop("dokumentnummer", UNSET)

        _mehrheit = d.pop("mehrheit", UNSET)
        mehrheit: Union[Unset, BeschlussfassungMehrheit]
        if isinstance(_mehrheit, Unset):
            mehrheit = UNSET
        else:
            mehrheit = BeschlussfassungMehrheit(_mehrheit)

        beschlussfassung = cls(
            beschlusstenor=beschlusstenor,
            seite=seite,
            abstimmungsart=abstimmungsart,
            abstimm_ergebnis_bemerkung=abstimm_ergebnis_bemerkung,
            grundlage=grundlage,
            dokumentnummer=dokumentnummer,
            mehrheit=mehrheit,
        )

        beschlussfassung.additional_properties = d
        return beschlussfassung

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
