import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.drucksache_dokumentart import DrucksacheDokumentart
from ..models.drucksache_herausgeber import DrucksacheHerausgeber
from ..models.drucksache_typ import DrucksacheTyp
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.drucksache_autoren_anzeige_item import DrucksacheAutorenAnzeigeItem
    from ..models.fundstelle import Fundstelle
    from ..models.ressort import Ressort
    from ..models.urheber import Urheber
    from ..models.vorgangsbezug import Vorgangsbezug


T = TypeVar("T", bound="DrucksacheText")


@_attrs_define
class DrucksacheText:
    """
    Attributes:
        id (str):  Example: 68852.
        typ (DrucksacheTyp):  Example: Dokument.
        dokumentart (DrucksacheDokumentart):  Example: Drucksache.
        drucksachetyp (str):  Example: Antrag.
        dokumentnummer (str):  Example: 19/1.
        herausgeber (DrucksacheHerausgeber):  Example: BT.
        datum (datetime.date):  Example: 2017-10-24.
        aktualisiert (datetime.datetime): Letzte Aktualisierung der Entität Example: 2022-08-01T15:30:16+02:00.
        titel (str):  Example: Weitergeltung von Geschäftsordnungsrecht.
        autoren_anzahl (int): Gesamtzahl der Autor:innen Example: 4.
        fundstelle (Fundstelle): Liefert im Vorgangsablauf das zu einem Vorgangsschritt gehörende Dokument (Drucksache
            oder Protokoll).

            Beispiel: „BT-Drucksache 19/1 (Antrag Fraktion der CDU/CSU)“ oder beim Vorgangsschritt Beratung „BT-
            Plenarprotokoll 19/1, S. 4C-12A“.
        vorgangsbezug_anzahl (int): Gesamtzahl der zugehörigen Vorgänge Example: 6.
        wahlperiode (Union[Unset, int]):  Example: 19.
        autoren_anzeige (Union[Unset, List['DrucksacheAutorenAnzeigeItem']]): Zusammenfassung der ersten 4 zur Anzeige
            markierten Autor:innen
        pdf_hash (Union[Unset, str]): MD5-Prüfsumme der PDF-Datei Example: a33af31e7c4524db8db172ef8f9e0f6d.
        urheber (Union[Unset, List['Urheber']]):
        vorgangsbezug (Union[Unset, List['Vorgangsbezug']]): Zusammenfassung der ersten 4 zugehörigen Vorgänge
        ressort (Union[Unset, List['Ressort']]):
        anlagen (Union[Unset, str]):  Example: Verzeichnis der Gutachten des Sachverständigenrates.
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
    typ: DrucksacheTyp
    dokumentart: DrucksacheDokumentart
    drucksachetyp: str
    dokumentnummer: str
    herausgeber: DrucksacheHerausgeber
    datum: datetime.date
    aktualisiert: datetime.datetime
    titel: str
    autoren_anzahl: int
    fundstelle: "Fundstelle"
    vorgangsbezug_anzahl: int
    wahlperiode: Union[Unset, int] = UNSET
    autoren_anzeige: Union[Unset, List["DrucksacheAutorenAnzeigeItem"]] = UNSET
    pdf_hash: Union[Unset, str] = UNSET
    urheber: Union[Unset, List["Urheber"]] = UNSET
    vorgangsbezug: Union[Unset, List["Vorgangsbezug"]] = UNSET
    ressort: Union[Unset, List["Ressort"]] = UNSET
    anlagen: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        typ = self.typ.value

        dokumentart = self.dokumentart.value

        drucksachetyp = self.drucksachetyp

        dokumentnummer = self.dokumentnummer

        herausgeber = self.herausgeber.value

        datum = self.datum.isoformat()

        aktualisiert = self.aktualisiert.isoformat()

        titel = self.titel

        autoren_anzahl = self.autoren_anzahl

        fundstelle = self.fundstelle.to_dict()

        vorgangsbezug_anzahl = self.vorgangsbezug_anzahl

        wahlperiode = self.wahlperiode

        autoren_anzeige: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.autoren_anzeige, Unset):
            autoren_anzeige = []
            for autoren_anzeige_item_data in self.autoren_anzeige:
                autoren_anzeige_item = autoren_anzeige_item_data.to_dict()
                autoren_anzeige.append(autoren_anzeige_item)

        pdf_hash = self.pdf_hash

        urheber: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.urheber, Unset):
            urheber = []
            for urheber_item_data in self.urheber:
                urheber_item = urheber_item_data.to_dict()
                urheber.append(urheber_item)

        vorgangsbezug: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.vorgangsbezug, Unset):
            vorgangsbezug = []
            for vorgangsbezug_item_data in self.vorgangsbezug:
                vorgangsbezug_item = vorgangsbezug_item_data.to_dict()
                vorgangsbezug.append(vorgangsbezug_item)

        ressort: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.ressort, Unset):
            ressort = []
            for ressort_item_data in self.ressort:
                ressort_item = ressort_item_data.to_dict()
                ressort.append(ressort_item)

        anlagen = self.anlagen

        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "typ": typ,
                "dokumentart": dokumentart,
                "drucksachetyp": drucksachetyp,
                "dokumentnummer": dokumentnummer,
                "herausgeber": herausgeber,
                "datum": datum,
                "aktualisiert": aktualisiert,
                "titel": titel,
                "autoren_anzahl": autoren_anzahl,
                "fundstelle": fundstelle,
                "vorgangsbezug_anzahl": vorgangsbezug_anzahl,
            }
        )
        if wahlperiode is not UNSET:
            field_dict["wahlperiode"] = wahlperiode
        if autoren_anzeige is not UNSET:
            field_dict["autoren_anzeige"] = autoren_anzeige
        if pdf_hash is not UNSET:
            field_dict["pdf_hash"] = pdf_hash
        if urheber is not UNSET:
            field_dict["urheber"] = urheber
        if vorgangsbezug is not UNSET:
            field_dict["vorgangsbezug"] = vorgangsbezug
        if ressort is not UNSET:
            field_dict["ressort"] = ressort
        if anlagen is not UNSET:
            field_dict["anlagen"] = anlagen
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.drucksache_autoren_anzeige_item import DrucksacheAutorenAnzeigeItem
        from ..models.fundstelle import Fundstelle
        from ..models.ressort import Ressort
        from ..models.urheber import Urheber
        from ..models.vorgangsbezug import Vorgangsbezug

        d = src_dict.copy()
        id = d.pop("id")

        typ = DrucksacheTyp(d.pop("typ"))

        dokumentart = DrucksacheDokumentart(d.pop("dokumentart"))

        drucksachetyp = d.pop("drucksachetyp")

        dokumentnummer = d.pop("dokumentnummer")

        herausgeber = DrucksacheHerausgeber(d.pop("herausgeber"))

        datum = isoparse(d.pop("datum")).date()

        aktualisiert = isoparse(d.pop("aktualisiert"))

        titel = d.pop("titel")

        autoren_anzahl = d.pop("autoren_anzahl")

        fundstelle = Fundstelle.from_dict(d.pop("fundstelle"))

        vorgangsbezug_anzahl = d.pop("vorgangsbezug_anzahl")

        wahlperiode = d.pop("wahlperiode", UNSET)

        autoren_anzeige = []
        _autoren_anzeige = d.pop("autoren_anzeige", UNSET)
        for autoren_anzeige_item_data in _autoren_anzeige or []:
            autoren_anzeige_item = DrucksacheAutorenAnzeigeItem.from_dict(autoren_anzeige_item_data)

            autoren_anzeige.append(autoren_anzeige_item)

        pdf_hash = d.pop("pdf_hash", UNSET)

        urheber = []
        _urheber = d.pop("urheber", UNSET)
        for urheber_item_data in _urheber or []:
            urheber_item = Urheber.from_dict(urheber_item_data)

            urheber.append(urheber_item)

        vorgangsbezug = []
        _vorgangsbezug = d.pop("vorgangsbezug", UNSET)
        for vorgangsbezug_item_data in _vorgangsbezug or []:
            vorgangsbezug_item = Vorgangsbezug.from_dict(vorgangsbezug_item_data)

            vorgangsbezug.append(vorgangsbezug_item)

        ressort = []
        _ressort = d.pop("ressort", UNSET)
        for ressort_item_data in _ressort or []:
            ressort_item = Ressort.from_dict(ressort_item_data)

            ressort.append(ressort_item)

        anlagen = d.pop("anlagen", UNSET)

        text = d.pop("text", UNSET)

        drucksache_text = cls(
            id=id,
            typ=typ,
            dokumentart=dokumentart,
            drucksachetyp=drucksachetyp,
            dokumentnummer=dokumentnummer,
            herausgeber=herausgeber,
            datum=datum,
            aktualisiert=aktualisiert,
            titel=titel,
            autoren_anzahl=autoren_anzahl,
            fundstelle=fundstelle,
            vorgangsbezug_anzahl=vorgangsbezug_anzahl,
            wahlperiode=wahlperiode,
            autoren_anzeige=autoren_anzeige,
            pdf_hash=pdf_hash,
            urheber=urheber,
            vorgangsbezug=vorgangsbezug,
            ressort=ressort,
            anlagen=anlagen,
            text=text,
        )

        drucksache_text.additional_properties = d
        return drucksache_text

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
