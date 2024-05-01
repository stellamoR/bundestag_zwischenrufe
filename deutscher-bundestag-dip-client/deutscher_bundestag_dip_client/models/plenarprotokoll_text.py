import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.plenarprotokoll_dokumentart import PlenarprotokollDokumentart
from ..models.plenarprotokoll_typ import PlenarprotokollTyp
from ..models.zuordnung import Zuordnung
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.fundstelle import Fundstelle
    from ..models.vorgangsbezug import Vorgangsbezug


T = TypeVar("T", bound="PlenarprotokollText")


@_attrs_define
class PlenarprotokollText:
    """
    Attributes:
        id (str):  Example: 908.
        dokumentart (PlenarprotokollDokumentart):  Example: Plenarprotokoll.
        typ (PlenarprotokollTyp):  Example: Dokument.
        dokumentnummer (str):  Example: 19/1.
        herausgeber (Zuordnung): Jeder Vorgangsschritt ist entweder dem Bundestag (BT), dem Bundesrat (BR), der
            Bundesversammlung (BV) oder der Europakammer (EK) zugeordnet. Über die Zuordnung lassen sich bspw.
            Rechtsverordnungen herausfiltern, an denen der Bundestag beteiligt / nicht beteiligt war.
        datum (datetime.date):  Example: 2017-10-24.
        aktualisiert (datetime.datetime): Letzte Aktualisierung der Entität Example: 2022-08-01T15:30:16+02:00.
        titel (str):  Example: Protokoll der 1. Sitzung des 19. Deutschen Bundestages.
        fundstelle (Fundstelle): Liefert im Vorgangsablauf das zu einem Vorgangsschritt gehörende Dokument (Drucksache
            oder Protokoll).

            Beispiel: „BT-Drucksache 19/1 (Antrag Fraktion der CDU/CSU)“ oder beim Vorgangsschritt Beratung „BT-
            Plenarprotokoll 19/1, S. 4C-12A“.
        vorgangsbezug_anzahl (int): Gesamtzahl der zugehörigen Vorgänge Example: 6.
        wahlperiode (Union[Unset, int]):  Example: 19.
        pdf_hash (Union[Unset, str]): MD5-Prüfsumme der PDF-Datei Example: a33af31e7c4524db8db172ef8f9e0f6d.
        vorgangsbezug (Union[Unset, List['Vorgangsbezug']]): Zusammenfassung der ersten 4 zugehörigen Vorgänge
        sitzungsbemerkung (Union[Unset, str]):  Example: Sondersitzung.
        text (Union[Unset, str]): Volltext des Dokuments

            Das Beispiel enthält einen gekürzten Auszug einer Drucksache.
             Example: Deutscher Bundestag Drucksache 19/1
            19. Wahlperiode 24.10.2017

            Antrag
            der Fraktion der CDU/CSU
            Weitergeltung von Geschäftsordnungsrecht
            Der Bundestag wolle beschließen:
            Für die 19. Wahlperiode werden übernommen
            – die Geschäftsordnung des Deutschen Bundestages einschließlich ihrer Anla-
            gen, soweit sie vom Deutschen Bundestag zu beschließen sind, in der Fassung
            der Bekanntmachung vom 2. Juli 1980 (BGBl. I S. 1237), zuletzt geändert
            laut Bekanntmachung vom 12. Juni 2017 (BGBl. I S. 1877), wobei § 126a der
            Geschäftsordnung mit Ablauf der 18. Wahlperiode entfallen ist;
            – die Gemeinsame Geschäftsordnung des Bundestages und des Bundesrates für
            den Ausschuss nach Artikel 77 des Grundgesetzes (Vermittlungsausschuss)
            vom 5. Mai 1951 (BGBl. II S. 103), zuletzt geändert laut Bekanntmachung vom
            30. April 2003 (BGBl. I S. 677);
            – die Geschäftsordnung für den Gemeinsamen Ausschuss vom 23. Juli 1969
            (BGBl. I S. 1102), zuletzt geändert laut Bekanntmachung vom 20. Juli 1993
            (BGBl. I S. 1500);
            – die Geschäftsordnung für das Verfahren nach Artikel 115d des Grundgesetzes
            vom 23. Juli 1969 (BGBl. I S. 1100);
            – die Richtlinien zur Überprüfung auf eine Tätigkeit oder politische Verantwor-
            tung für das Ministerium für Staatssicherheit/Amt für Nationale Sicherheit der
            ehemaligen Deutschen Demokratischen Republik vom 13. Dezember 1991
            (BGBl. 1992 I S. 76), zuletzt geändert laut Bekanntmachung vom 21. Oktober
            2005 (BGBl. I S. 3094).
            Berlin, den 23. Oktober 2017
            Volker Kauder, Alexander Dobrindt und Fraktion
            Satz: Satzweiss.com Print, Web, Software GmbH, Mainzer Straße 116, 66121 Saarbrücken, www.satzweiss.com
            Druck: Printsystem GmbH, Schafwäsche 1-3, 71296 Heimsheim, www.printsystem.de
            Vertrieb: Bundesanzeiger Verlag GmbH, Postfach 10 05 34, 50445 Köln, Telefon (02 21) 97 66 83 40, Fax (02 21) 97
            66 83 44, www.betrifft-gesetze.de
            ISSN 0722-8333
            .
    """

    id: str
    dokumentart: PlenarprotokollDokumentart
    typ: PlenarprotokollTyp
    dokumentnummer: str
    herausgeber: Zuordnung
    datum: datetime.date
    aktualisiert: datetime.datetime
    titel: str
    fundstelle: "Fundstelle"
    vorgangsbezug_anzahl: int
    wahlperiode: Union[Unset, int] = UNSET
    pdf_hash: Union[Unset, str] = UNSET
    vorgangsbezug: Union[Unset, List["Vorgangsbezug"]] = UNSET
    sitzungsbemerkung: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        dokumentart = self.dokumentart.value

        typ = self.typ.value

        dokumentnummer = self.dokumentnummer

        herausgeber = self.herausgeber.value

        datum = self.datum.isoformat()

        aktualisiert = self.aktualisiert.isoformat()

        titel = self.titel

        fundstelle = self.fundstelle.to_dict()

        vorgangsbezug_anzahl = self.vorgangsbezug_anzahl

        wahlperiode = self.wahlperiode

        pdf_hash = self.pdf_hash

        vorgangsbezug: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.vorgangsbezug, Unset):
            vorgangsbezug = []
            for vorgangsbezug_item_data in self.vorgangsbezug:
                vorgangsbezug_item = vorgangsbezug_item_data.to_dict()
                vorgangsbezug.append(vorgangsbezug_item)

        sitzungsbemerkung = self.sitzungsbemerkung

        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "dokumentart": dokumentart,
                "typ": typ,
                "dokumentnummer": dokumentnummer,
                "herausgeber": herausgeber,
                "datum": datum,
                "aktualisiert": aktualisiert,
                "titel": titel,
                "fundstelle": fundstelle,
                "vorgangsbezug_anzahl": vorgangsbezug_anzahl,
            }
        )
        if wahlperiode is not UNSET:
            field_dict["wahlperiode"] = wahlperiode
        if pdf_hash is not UNSET:
            field_dict["pdf_hash"] = pdf_hash
        if vorgangsbezug is not UNSET:
            field_dict["vorgangsbezug"] = vorgangsbezug
        if sitzungsbemerkung is not UNSET:
            field_dict["sitzungsbemerkung"] = sitzungsbemerkung
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.fundstelle import Fundstelle
        from ..models.vorgangsbezug import Vorgangsbezug

        d = src_dict.copy()
        id = d.pop("id")

        dokumentart = PlenarprotokollDokumentart(d.pop("dokumentart"))

        typ = PlenarprotokollTyp(d.pop("typ"))

        dokumentnummer = d.pop("dokumentnummer")

        herausgeber = Zuordnung(d.pop("herausgeber"))

        datum = isoparse(d.pop("datum")).date()

        aktualisiert = isoparse(d.pop("aktualisiert"))

        titel = d.pop("titel")

        fundstelle = Fundstelle.from_dict(d.pop("fundstelle"))

        vorgangsbezug_anzahl = d.pop("vorgangsbezug_anzahl")

        wahlperiode = d.pop("wahlperiode", UNSET)

        pdf_hash = d.pop("pdf_hash", UNSET)

        vorgangsbezug = []
        _vorgangsbezug = d.pop("vorgangsbezug", UNSET)
        for vorgangsbezug_item_data in _vorgangsbezug or []:
            vorgangsbezug_item = Vorgangsbezug.from_dict(vorgangsbezug_item_data)

            vorgangsbezug.append(vorgangsbezug_item)

        sitzungsbemerkung = d.pop("sitzungsbemerkung", UNSET)

        text = d.pop("text", UNSET)

        plenarprotokoll_text = cls(
            id=id,
            dokumentart=dokumentart,
            typ=typ,
            dokumentnummer=dokumentnummer,
            herausgeber=herausgeber,
            datum=datum,
            aktualisiert=aktualisiert,
            titel=titel,
            fundstelle=fundstelle,
            vorgangsbezug_anzahl=vorgangsbezug_anzahl,
            wahlperiode=wahlperiode,
            pdf_hash=pdf_hash,
            vorgangsbezug=vorgangsbezug,
            sitzungsbemerkung=sitzungsbemerkung,
            text=text,
        )

        plenarprotokoll_text.additional_properties = d
        return plenarprotokoll_text

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
