from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.bundesland import Bundesland
from ..types import UNSET, Unset

T = TypeVar("T", bound="PersonRole")


@_attrs_define
class PersonRole:
    """Liefert den Eintrag einer Person in einer bestimmten Rolle oder Funktion.

    Attributes:
        funktion (str):  Example: LMin Soz u. Frauen.
        nachname (str):  Example: Leyen.
        vorname (str):  Example: Ursula.
        funktionszusatz (Union[Unset, str]):  Example: Stellv. MdBR.
        fraktion (Union[Unset, str]):  Example: CDU/CSU.
        namenszusatz (Union[Unset, str]):  Example: von der.
        wahlperiode_nummer (Union[Unset, List[int]]): Wahlperioden, für die der Personeneintrag zutrifft Example: [17,
            18, 19].
        wahlkreiszusatz (Union[Unset, str]):  Example: Hannover.
        ressort_titel (Union[Unset, str]):  Example: Bundesministerium für Familie, Senioren, Frauen und Jugend.
        bundesland (Union[Unset, Bundesland]): Das Bundesland wird bei persönlichen Urhebern verwendet, die Mitglieder
            des Bundesrates sind, z. B. „Reinhold Hilbers, MdBR (Finanzminister), Niedersachsen“ Example: Niedersachsen.
    """

    funktion: str
    nachname: str
    vorname: str
    funktionszusatz: Union[Unset, str] = UNSET
    fraktion: Union[Unset, str] = UNSET
    namenszusatz: Union[Unset, str] = UNSET
    wahlperiode_nummer: Union[Unset, List[int]] = UNSET
    wahlkreiszusatz: Union[Unset, str] = UNSET
    ressort_titel: Union[Unset, str] = UNSET
    bundesland: Union[Unset, Bundesland] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        funktion = self.funktion

        nachname = self.nachname

        vorname = self.vorname

        funktionszusatz = self.funktionszusatz

        fraktion = self.fraktion

        namenszusatz = self.namenszusatz

        wahlperiode_nummer: Union[Unset, List[int]] = UNSET
        if not isinstance(self.wahlperiode_nummer, Unset):
            wahlperiode_nummer = self.wahlperiode_nummer

        wahlkreiszusatz = self.wahlkreiszusatz

        ressort_titel = self.ressort_titel

        bundesland: Union[Unset, str] = UNSET
        if not isinstance(self.bundesland, Unset):
            bundesland = self.bundesland.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "funktion": funktion,
                "nachname": nachname,
                "vorname": vorname,
            }
        )
        if funktionszusatz is not UNSET:
            field_dict["funktionszusatz"] = funktionszusatz
        if fraktion is not UNSET:
            field_dict["fraktion"] = fraktion
        if namenszusatz is not UNSET:
            field_dict["namenszusatz"] = namenszusatz
        if wahlperiode_nummer is not UNSET:
            field_dict["wahlperiode_nummer"] = wahlperiode_nummer
        if wahlkreiszusatz is not UNSET:
            field_dict["wahlkreiszusatz"] = wahlkreiszusatz
        if ressort_titel is not UNSET:
            field_dict["ressort_titel"] = ressort_titel
        if bundesland is not UNSET:
            field_dict["bundesland"] = bundesland

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        funktion = d.pop("funktion")

        nachname = d.pop("nachname")

        vorname = d.pop("vorname")

        funktionszusatz = d.pop("funktionszusatz", UNSET)

        fraktion = d.pop("fraktion", UNSET)

        namenszusatz = d.pop("namenszusatz", UNSET)

        wahlperiode_nummer = cast(List[int], d.pop("wahlperiode_nummer", UNSET))

        wahlkreiszusatz = d.pop("wahlkreiszusatz", UNSET)

        ressort_titel = d.pop("ressort_titel", UNSET)

        _bundesland = d.pop("bundesland", UNSET)
        bundesland: Union[Unset, Bundesland]
        if isinstance(_bundesland, Unset):
            bundesland = UNSET
        else:
            bundesland = Bundesland(_bundesland)

        person_role = cls(
            funktion=funktion,
            nachname=nachname,
            vorname=vorname,
            funktionszusatz=funktionszusatz,
            fraktion=fraktion,
            namenszusatz=namenszusatz,
            wahlperiode_nummer=wahlperiode_nummer,
            wahlkreiszusatz=wahlkreiszusatz,
            ressort_titel=ressort_titel,
            bundesland=bundesland,
        )

        person_role.additional_properties = d
        return person_role

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
