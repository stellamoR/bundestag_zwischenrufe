import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Verkuendung")


@_attrs_define
class Verkuendung:
    """Liefert die Angaben zur Verkündung eines Gesetzes: Ausfertigungs- und Verkündungsdatum sowie die Fundstelle im
    jeweiligen Verkündungsblatt. Bei Bundesgesetzblatt I und II ist die Fundstelle verlinkt.

        Attributes:
            jahrgang (str):  Example: 2018.
            seite (str):  Example: 409.
            ausfertigungsdatum (datetime.date):  Example: 2018-03-19.
            verkuendungsdatum (datetime.date):  Example: 2018-03-29.
            einleitungstext (str):  Example: Bekanntmachung.
            fundstelle (str):  Example: BGBl I 2018, 409.
            heftnummer (Union[Unset, str]):  Example: 11.
            rubrik_nr (Union[Unset, str]):  Example: V1.
            verkuendungsblatt_bezeichnung (Union[Unset, str]):  Example: Bundesgesetzblatt Teil I.
            verkuendungsblatt_kuerzel (Union[Unset, str]):  Example: BGBl I.
            pdf_url (Union[Unset, str]):  Example: https://www.bgbl.de/xaver/bgbl/start.xav?startbk=Bundesanzeiger_BGBl&star
                t=//*%5b@attr_id=%27bgbl118s0409.pdf%27%5d.
            titel (Union[Unset, str]):  Example: Bekanntmachung über die Übernahme des Beschlusses des Deutschen Bundestages
                betr. Aufhebung der Immunität von Mitgliedern des Bundestages und der Grundsätze in Immunitätsangelegenheiten.
    """

    jahrgang: str
    seite: str
    ausfertigungsdatum: datetime.date
    verkuendungsdatum: datetime.date
    einleitungstext: str
    fundstelle: str
    heftnummer: Union[Unset, str] = UNSET
    rubrik_nr: Union[Unset, str] = UNSET
    verkuendungsblatt_bezeichnung: Union[Unset, str] = UNSET
    verkuendungsblatt_kuerzel: Union[Unset, str] = UNSET
    pdf_url: Union[Unset, str] = UNSET
    titel: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        jahrgang = self.jahrgang

        seite = self.seite

        ausfertigungsdatum = self.ausfertigungsdatum.isoformat()

        verkuendungsdatum = self.verkuendungsdatum.isoformat()

        einleitungstext = self.einleitungstext

        fundstelle = self.fundstelle

        heftnummer = self.heftnummer

        rubrik_nr = self.rubrik_nr

        verkuendungsblatt_bezeichnung = self.verkuendungsblatt_bezeichnung

        verkuendungsblatt_kuerzel = self.verkuendungsblatt_kuerzel

        pdf_url = self.pdf_url

        titel = self.titel

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "jahrgang": jahrgang,
                "seite": seite,
                "ausfertigungsdatum": ausfertigungsdatum,
                "verkuendungsdatum": verkuendungsdatum,
                "einleitungstext": einleitungstext,
                "fundstelle": fundstelle,
            }
        )
        if heftnummer is not UNSET:
            field_dict["heftnummer"] = heftnummer
        if rubrik_nr is not UNSET:
            field_dict["rubrik_nr"] = rubrik_nr
        if verkuendungsblatt_bezeichnung is not UNSET:
            field_dict["verkuendungsblatt_bezeichnung"] = verkuendungsblatt_bezeichnung
        if verkuendungsblatt_kuerzel is not UNSET:
            field_dict["verkuendungsblatt_kuerzel"] = verkuendungsblatt_kuerzel
        if pdf_url is not UNSET:
            field_dict["pdf_url"] = pdf_url
        if titel is not UNSET:
            field_dict["titel"] = titel

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        jahrgang = d.pop("jahrgang")

        seite = d.pop("seite")

        ausfertigungsdatum = isoparse(d.pop("ausfertigungsdatum")).date()

        verkuendungsdatum = isoparse(d.pop("verkuendungsdatum")).date()

        einleitungstext = d.pop("einleitungstext")

        fundstelle = d.pop("fundstelle")

        heftnummer = d.pop("heftnummer", UNSET)

        rubrik_nr = d.pop("rubrik_nr", UNSET)

        verkuendungsblatt_bezeichnung = d.pop("verkuendungsblatt_bezeichnung", UNSET)

        verkuendungsblatt_kuerzel = d.pop("verkuendungsblatt_kuerzel", UNSET)

        pdf_url = d.pop("pdf_url", UNSET)

        titel = d.pop("titel", UNSET)

        verkuendung = cls(
            jahrgang=jahrgang,
            seite=seite,
            ausfertigungsdatum=ausfertigungsdatum,
            verkuendungsdatum=verkuendungsdatum,
            einleitungstext=einleitungstext,
            fundstelle=fundstelle,
            heftnummer=heftnummer,
            rubrik_nr=rubrik_nr,
            verkuendungsblatt_bezeichnung=verkuendungsblatt_bezeichnung,
            verkuendungsblatt_kuerzel=verkuendungsblatt_kuerzel,
            pdf_url=pdf_url,
            titel=titel,
        )

        verkuendung.additional_properties = d
        return verkuendung

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
