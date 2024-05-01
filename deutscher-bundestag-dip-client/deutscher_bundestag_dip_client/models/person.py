import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.person_role import PersonRole


T = TypeVar("T", bound="Person")


@_attrs_define
class Person:
    """Liefert Personenstammdaten zu einer Person

    Attributes:
        id (str):  Example: 1728.
        nachname (str):  Example: Leyen.
        vorname (str):  Example: Ursula.
        typ (str):  Example: Person.
        aktualisiert (datetime.datetime): Letzte Aktualisierung der Entität Example: 2022-08-01T15:30:16+02:00.
        titel (str):  Example: Dr.  Ursula von der Leyen, Bundesmin., Bundesministerium der Verteidigung.
        namenszusatz (Union[Unset, str]):  Example: von der.
        wahlperiode (Union[Unset, int]): Wahlperiode des ersten zugehörigen Dokuments Example: 15.
        basisdatum (Union[Unset, datetime.date]): Datum des ersten zugehörigen Dokuments Example: 2003-09-09.
        datum (Union[Unset, datetime.date]): Datum des letzten zugehörigen Dokuments Example: 2019-06-25.
        person_roles (Union[Unset, List['PersonRole']]): Nebeneinträge mit bspw. abweichenden Funktionen oder
            Namensänderungen
    """

    id: str
    nachname: str
    vorname: str
    typ: str
    aktualisiert: datetime.datetime
    titel: str
    namenszusatz: Union[Unset, str] = UNSET
    wahlperiode: Union[Unset, int] = UNSET
    basisdatum: Union[Unset, datetime.date] = UNSET
    datum: Union[Unset, datetime.date] = UNSET
    person_roles: Union[Unset, List["PersonRole"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        nachname = self.nachname

        vorname = self.vorname

        typ = self.typ

        aktualisiert = self.aktualisiert.isoformat()

        titel = self.titel

        namenszusatz = self.namenszusatz

        wahlperiode = self.wahlperiode

        basisdatum: Union[Unset, str] = UNSET
        if not isinstance(self.basisdatum, Unset):
            basisdatum = self.basisdatum.isoformat()

        datum: Union[Unset, str] = UNSET
        if not isinstance(self.datum, Unset):
            datum = self.datum.isoformat()

        person_roles: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.person_roles, Unset):
            person_roles = []
            for person_roles_item_data in self.person_roles:
                person_roles_item = person_roles_item_data.to_dict()
                person_roles.append(person_roles_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "nachname": nachname,
                "vorname": vorname,
                "typ": typ,
                "aktualisiert": aktualisiert,
                "titel": titel,
            }
        )
        if namenszusatz is not UNSET:
            field_dict["namenszusatz"] = namenszusatz
        if wahlperiode is not UNSET:
            field_dict["wahlperiode"] = wahlperiode
        if basisdatum is not UNSET:
            field_dict["basisdatum"] = basisdatum
        if datum is not UNSET:
            field_dict["datum"] = datum
        if person_roles is not UNSET:
            field_dict["person_roles"] = person_roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.person_role import PersonRole

        d = src_dict.copy()
        id = d.pop("id")

        nachname = d.pop("nachname")

        vorname = d.pop("vorname")

        typ = d.pop("typ")

        aktualisiert = isoparse(d.pop("aktualisiert"))

        titel = d.pop("titel")

        namenszusatz = d.pop("namenszusatz", UNSET)

        wahlperiode = d.pop("wahlperiode", UNSET)

        _basisdatum = d.pop("basisdatum", UNSET)
        basisdatum: Union[Unset, datetime.date]
        if isinstance(_basisdatum, Unset):
            basisdatum = UNSET
        else:
            basisdatum = isoparse(_basisdatum).date()

        _datum = d.pop("datum", UNSET)
        datum: Union[Unset, datetime.date]
        if isinstance(_datum, Unset):
            datum = UNSET
        else:
            datum = isoparse(_datum).date()

        person_roles = []
        _person_roles = d.pop("person_roles", UNSET)
        for person_roles_item_data in _person_roles or []:
            person_roles_item = PersonRole.from_dict(person_roles_item_data)

            person_roles.append(person_roles_item)

        person = cls(
            id=id,
            nachname=nachname,
            vorname=vorname,
            typ=typ,
            aktualisiert=aktualisiert,
            titel=titel,
            namenszusatz=namenszusatz,
            wahlperiode=wahlperiode,
            basisdatum=basisdatum,
            datum=datum,
            person_roles=person_roles,
        )

        person.additional_properties = d
        return person

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
