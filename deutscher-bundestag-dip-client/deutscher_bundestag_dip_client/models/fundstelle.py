import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.fundstelle_dokumentart import FundstelleDokumentart
from ..models.quadrant import Quadrant
from ..models.zuordnung import Zuordnung
from ..types import UNSET, Unset

T = TypeVar("T", bound="Fundstelle")


@_attrs_define
class Fundstelle:
    """Liefert im Vorgangsablauf das zu einem Vorgangsschritt gehörende Dokument (Drucksache oder Protokoll).

    Beispiel: „BT-Drucksache 19/1 (Antrag Fraktion der CDU/CSU)“ oder beim Vorgangsschritt Beratung „BT-Plenarprotokoll
    19/1, S. 4C-12A“.

        Attributes:
            id (str): ID einer Drucksache oder eines Plenarprotokolls Example: 68852.
            dokumentart (FundstelleDokumentart):  Example: Drucksache.
            dokumentnummer (str):  Example: 19/1.
            datum (datetime.date):  Example: 2017-10-24.
            herausgeber (Zuordnung): Jeder Vorgangsschritt ist entweder dem Bundestag (BT), dem Bundesrat (BR), der
                Bundesversammlung (BV) oder der Europakammer (EK) zugeordnet. Über die Zuordnung lassen sich bspw.
                Rechtsverordnungen herausfiltern, an denen der Bundestag beteiligt / nicht beteiligt war.
            urheber (List[str]):
            pdf_url (Union[Unset, str]):  Example: https://dserver.bundestag.de/btd/19/000/1900001.pdf.
            drucksachetyp (Union[Unset, str]):  Example: Antrag.
            verteildatum (Union[Unset, datetime.date]):  Example: 2017-10-25.
            seite (Union[Unset, str]):  Example: 4292B.
            anfangsseite (Union[Unset, int]):  Example: 4251.
            endseite (Union[Unset, int]):  Example: 4298.
            anfangsquadrant (Union[Unset, Quadrant]): Teil der Fundstelle eines Plenarprotokolls. Jede Seite im
                Plenarprotokoll ist in vier gleich große Viertel unterteilt (Quadranten) mit den Bezeichnungen A, B, C, D.
            endquadrant (Union[Unset, Quadrant]): Teil der Fundstelle eines Plenarprotokolls. Jede Seite im Plenarprotokoll
                ist in vier gleich große Viertel unterteilt (Quadranten) mit den Bezeichnungen A, B, C, D.
            frage_nummer (Union[Unset, str]):  Example: C.4.
            anlagen (Union[Unset, str]):  Example: Verzeichnis der Gutachten des Sachverständigenrates.
            top (Union[Unset, int]):  Example: 2.
            top_zusatz (Union[Unset, str]):  Example: b.
    """

    id: str
    dokumentart: FundstelleDokumentart
    dokumentnummer: str
    datum: datetime.date
    herausgeber: Zuordnung
    urheber: List[str]
    pdf_url: Union[Unset, str] = UNSET
    drucksachetyp: Union[Unset, str] = UNSET
    verteildatum: Union[Unset, datetime.date] = UNSET
    seite: Union[Unset, str] = UNSET
    anfangsseite: Union[Unset, int] = UNSET
    endseite: Union[Unset, int] = UNSET
    anfangsquadrant: Union[Unset, Quadrant] = UNSET
    endquadrant: Union[Unset, Quadrant] = UNSET
    frage_nummer: Union[Unset, str] = UNSET
    anlagen: Union[Unset, str] = UNSET
    top: Union[Unset, int] = UNSET
    top_zusatz: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        dokumentart = self.dokumentart.value

        dokumentnummer = self.dokumentnummer

        datum = self.datum.isoformat()

        herausgeber = self.herausgeber.value

        urheber = self.urheber

        pdf_url = self.pdf_url

        drucksachetyp = self.drucksachetyp

        verteildatum: Union[Unset, str] = UNSET
        if not isinstance(self.verteildatum, Unset):
            verteildatum = self.verteildatum.isoformat()

        seite = self.seite

        anfangsseite = self.anfangsseite

        endseite = self.endseite

        anfangsquadrant: Union[Unset, str] = UNSET
        if not isinstance(self.anfangsquadrant, Unset):
            anfangsquadrant = self.anfangsquadrant.value

        endquadrant: Union[Unset, str] = UNSET
        if not isinstance(self.endquadrant, Unset):
            endquadrant = self.endquadrant.value

        frage_nummer = self.frage_nummer

        anlagen = self.anlagen

        top = self.top

        top_zusatz = self.top_zusatz

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "dokumentart": dokumentart,
                "dokumentnummer": dokumentnummer,
                "datum": datum,
                "herausgeber": herausgeber,
                "urheber": urheber,
            }
        )
        if pdf_url is not UNSET:
            field_dict["pdf_url"] = pdf_url
        if drucksachetyp is not UNSET:
            field_dict["drucksachetyp"] = drucksachetyp
        if verteildatum is not UNSET:
            field_dict["verteildatum"] = verteildatum
        if seite is not UNSET:
            field_dict["seite"] = seite
        if anfangsseite is not UNSET:
            field_dict["anfangsseite"] = anfangsseite
        if endseite is not UNSET:
            field_dict["endseite"] = endseite
        if anfangsquadrant is not UNSET:
            field_dict["anfangsquadrant"] = anfangsquadrant
        if endquadrant is not UNSET:
            field_dict["endquadrant"] = endquadrant
        if frage_nummer is not UNSET:
            field_dict["frage_nummer"] = frage_nummer
        if anlagen is not UNSET:
            field_dict["anlagen"] = anlagen
        if top is not UNSET:
            field_dict["top"] = top
        if top_zusatz is not UNSET:
            field_dict["top_zusatz"] = top_zusatz

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        dokumentart = FundstelleDokumentart(d.pop("dokumentart"))

        dokumentnummer = d.pop("dokumentnummer")

        datum = isoparse(d.pop("datum")).date()

        herausgeber = Zuordnung(d.pop("herausgeber"))

        urheber = cast(List[str], d.pop("urheber"))

        pdf_url = d.pop("pdf_url", UNSET)

        drucksachetyp = d.pop("drucksachetyp", UNSET)

        _verteildatum = d.pop("verteildatum", UNSET)
        verteildatum: Union[Unset, datetime.date]
        if isinstance(_verteildatum, Unset):
            verteildatum = UNSET
        else:
            verteildatum = isoparse(_verteildatum).date()

        seite = d.pop("seite", UNSET)

        anfangsseite = d.pop("anfangsseite", UNSET)

        endseite = d.pop("endseite", UNSET)

        _anfangsquadrant = d.pop("anfangsquadrant", UNSET)
        anfangsquadrant: Union[Unset, Quadrant]
        if isinstance(_anfangsquadrant, Unset):
            anfangsquadrant = UNSET
        else:
            anfangsquadrant = Quadrant(_anfangsquadrant)

        _endquadrant = d.pop("endquadrant", UNSET)
        endquadrant: Union[Unset, Quadrant]
        if isinstance(_endquadrant, Unset):
            endquadrant = UNSET
        else:
            endquadrant = Quadrant(_endquadrant)

        frage_nummer = d.pop("frage_nummer", UNSET)

        anlagen = d.pop("anlagen", UNSET)

        top = d.pop("top", UNSET)

        top_zusatz = d.pop("top_zusatz", UNSET)

        fundstelle = cls(
            id=id,
            dokumentart=dokumentart,
            dokumentnummer=dokumentnummer,
            datum=datum,
            herausgeber=herausgeber,
            urheber=urheber,
            pdf_url=pdf_url,
            drucksachetyp=drucksachetyp,
            verteildatum=verteildatum,
            seite=seite,
            anfangsseite=anfangsseite,
            endseite=endseite,
            anfangsquadrant=anfangsquadrant,
            endquadrant=endquadrant,
            frage_nummer=frage_nummer,
            anlagen=anlagen,
            top=top,
            top_zusatz=top_zusatz,
        )

        fundstelle.additional_properties = d
        return fundstelle

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
