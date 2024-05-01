import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.vorgangsposition_dokumentart import VorgangspositionDokumentart
from ..models.vorgangsposition_typ import VorgangspositionTyp
from ..models.zuordnung import Zuordnung
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aktivitaet_anzeige import AktivitaetAnzeige
    from ..models.beschlussfassung import Beschlussfassung
    from ..models.fundstelle import Fundstelle
    from ..models.ressort import Ressort
    from ..models.ueberweisung import Ueberweisung
    from ..models.urheber import Urheber
    from ..models.vorgangspositionbezug import Vorgangspositionbezug


T = TypeVar("T", bound="Vorgangsposition")


@_attrs_define
class Vorgangsposition:
    """Liefert Metadaten zu einer Vorgangsposition (Vorgangsschritt).

    Attributes:
        id (str):  Example: 173376.
        vorgangsposition (str):  Example: Antrag zur Weitergeltung der Geschäftsordnung.
        zuordnung (Zuordnung): Jeder Vorgangsschritt ist entweder dem Bundestag (BT), dem Bundesrat (BR), der
            Bundesversammlung (BV) oder der Europakammer (EK) zugeordnet. Über die Zuordnung lassen sich bspw.
            Rechtsverordnungen herausfiltern, an denen der Bundestag beteiligt / nicht beteiligt war.
        gang (bool): Alle Vorgangsschritte, die von besonderer Bedeutung für den Fortgang der Beratung sind, werden
            durch das Attribut `gang: true` gekennzeichnet.

            Ist ein solcher Vorgangsschritt mit einer Drucksache verknüpft, werden im Frontend unter der Benennung "Wichtige
            Drucksachen" Herausgeber, Nummer und Typ sowie das Datum der entsprechenden Drucksachen ausgegeben (z.B. BT-Drs
            18/13014 (Beschlussempfehlung), 28.06.2017).
            Ist er mit einem Plenarprotokoll verknüpft, werden im Frontend unter der Benennung "Plenum" der Klartext der
            Vorgangsposition, Datum, Herausgeber und Nummer des Plenarprotokolls mit Anfangsseite/Quadrant und
            Endseite/Quadrant dargestellt (z.B. 2. Beratung: 29.06.2017, BT-PlPr 18/243, S. 24964C - 24973C).
        fortsetzung (bool): Erstreckt sich eine Beratung über mehrere Plenarprotokolle, so müssen entsprechend viele
            Vorgangsschritte mit je gleicher Vorgangsposition im Vorgangsablauf angelegt werden. Der zweite und jeder
            weitere dieser Schritte wird dann als "Fortsetzung" gekennzeichnet (Attribut `fortsetzung: true`).
            Für die Beratung des Gesetzentwurfs für die Feststellung des Haushaltsplanes (Haushaltsberatungen) gelten
            abweichende Regelungen.
        nachtrag (bool): Eine Auswertungseinheit eines Plenarprotokolls kann nur an genau einen Vorgangsschritt
            angebunden werden.
            Müssen aber mehrere Auswertungseinheiten für einen Vorgangsschritt gebildet werden (weil die Ergänzung einer
            Rede erst in einem späteren Protokoll erscheint oder weil sich z.B. bei einer Verbundenen Beratung (§ 24 GO-BT)
            nicht alle Schriftlichen Erklärungen nach § 31 GO-BT auf sämtliche Vorlagen beziehen),
            dann müssen im Vorgangsablauf mehrere Vorgangsschritte mit der gleichen Vorgangsposition angelegt werden. Der
            zweite und jeder weitere dieser Schritte wird dann als "Nachtrag" gekennzeichnet (Attribut `nachtrag: true`)
        vorgangstyp (str): Vorgangstyp des zugehörigen Vorgangs Example: Geschäftsordnung.
        typ (VorgangspositionTyp):  Example: Vorgangsposition.
        titel (str): Titel des zugehörigen Vorgangs Example: Weitergeltung von Geschäftsordnungsrecht.
        dokumentart (VorgangspositionDokumentart):  Example: Drucksache.
        vorgang_id (str): ID des zugehörigen Vorgangs Example: 84343.
        datum (datetime.date): Datum des zugehörigen Dokuments Example: 2017-10-24.
        aktualisiert (datetime.datetime): Letzte Aktualisierung der Entität oder des zugehörigen Dokuments Example:
            2022-08-01T15:30:16+02:00.
        fundstelle (Fundstelle): Liefert im Vorgangsablauf das zu einem Vorgangsschritt gehörende Dokument (Drucksache
            oder Protokoll).

            Beispiel: „BT-Drucksache 19/1 (Antrag Fraktion der CDU/CSU)“ oder beim Vorgangsschritt Beratung „BT-
            Plenarprotokoll 19/1, S. 4C-12A“.
        aktivitaet_anzahl (int): Gesamtzahl der zugehörigen Aktivitäten Example: 2.
        urheber (Union[Unset, List['Urheber']]):
        ueberweisung (Union[Unset, List['Ueberweisung']]):
        aktivitaet_anzeige (Union[Unset, List['AktivitaetAnzeige']]): Zusammenfassung der ersten 4 zur Anzeige
            vorgesehenen Aktivitäten
        ressort (Union[Unset, List['Ressort']]):
        beschlussfassung (Union[Unset, List['Beschlussfassung']]):
        ratsdok (Union[Unset, str]): Ratsdok-Nr. Example: 11018/17.
        kom (Union[Unset, str]): KOM-Nr. Example: (2017) 600 endg..
        sek (Union[Unset, str]): SEK-Nr. Example: (2010) 305 endg..
        mitberaten (Union[Unset, List['Vorgangspositionbezug']]): Es ist eine häufig geübte Praxis, mehrere thematisch
            verwandte Vorlagen (z.B. konkurrierende Anträge der verschiedenen Fraktionen zum Thema Diesel-Fahrverbote) in
            einer Debatte gemeinsam zu beraten ("Zusammenberatung").

            `mitberaten` liefert, von einem Vorgang ausgehend, alle anderen Vorgänge, die Gegenstand der Zusammenberatung
            sind.
        abstract (Union[Unset, str]):  Example: Stellungnahme der BRg zu den Tätigkeitsberichten 2016/2017 der
            Bundesnetzagentur  - Telekommunikation und Post - mit den Sondergutachten der Monopolkommission.
    """

    id: str
    vorgangsposition: str
    zuordnung: Zuordnung
    gang: bool
    fortsetzung: bool
    nachtrag: bool
    vorgangstyp: str
    typ: VorgangspositionTyp
    titel: str
    dokumentart: VorgangspositionDokumentart
    vorgang_id: str
    datum: datetime.date
    aktualisiert: datetime.datetime
    fundstelle: "Fundstelle"
    aktivitaet_anzahl: int
    urheber: Union[Unset, List["Urheber"]] = UNSET
    ueberweisung: Union[Unset, List["Ueberweisung"]] = UNSET
    aktivitaet_anzeige: Union[Unset, List["AktivitaetAnzeige"]] = UNSET
    ressort: Union[Unset, List["Ressort"]] = UNSET
    beschlussfassung: Union[Unset, List["Beschlussfassung"]] = UNSET
    ratsdok: Union[Unset, str] = UNSET
    kom: Union[Unset, str] = UNSET
    sek: Union[Unset, str] = UNSET
    mitberaten: Union[Unset, List["Vorgangspositionbezug"]] = UNSET
    abstract: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        vorgangsposition = self.vorgangsposition

        zuordnung = self.zuordnung.value

        gang = self.gang

        fortsetzung = self.fortsetzung

        nachtrag = self.nachtrag

        vorgangstyp = self.vorgangstyp

        typ = self.typ.value

        titel = self.titel

        dokumentart = self.dokumentart.value

        vorgang_id = self.vorgang_id

        datum = self.datum.isoformat()

        aktualisiert = self.aktualisiert.isoformat()

        fundstelle = self.fundstelle.to_dict()

        aktivitaet_anzahl = self.aktivitaet_anzahl

        urheber: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.urheber, Unset):
            urheber = []
            for urheber_item_data in self.urheber:
                urheber_item = urheber_item_data.to_dict()
                urheber.append(urheber_item)

        ueberweisung: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.ueberweisung, Unset):
            ueberweisung = []
            for ueberweisung_item_data in self.ueberweisung:
                ueberweisung_item = ueberweisung_item_data.to_dict()
                ueberweisung.append(ueberweisung_item)

        aktivitaet_anzeige: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.aktivitaet_anzeige, Unset):
            aktivitaet_anzeige = []
            for aktivitaet_anzeige_item_data in self.aktivitaet_anzeige:
                aktivitaet_anzeige_item = aktivitaet_anzeige_item_data.to_dict()
                aktivitaet_anzeige.append(aktivitaet_anzeige_item)

        ressort: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.ressort, Unset):
            ressort = []
            for ressort_item_data in self.ressort:
                ressort_item = ressort_item_data.to_dict()
                ressort.append(ressort_item)

        beschlussfassung: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.beschlussfassung, Unset):
            beschlussfassung = []
            for beschlussfassung_item_data in self.beschlussfassung:
                beschlussfassung_item = beschlussfassung_item_data.to_dict()
                beschlussfassung.append(beschlussfassung_item)

        ratsdok = self.ratsdok

        kom = self.kom

        sek = self.sek

        mitberaten: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.mitberaten, Unset):
            mitberaten = []
            for mitberaten_item_data in self.mitberaten:
                mitberaten_item = mitberaten_item_data.to_dict()
                mitberaten.append(mitberaten_item)

        abstract = self.abstract

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "vorgangsposition": vorgangsposition,
                "zuordnung": zuordnung,
                "gang": gang,
                "fortsetzung": fortsetzung,
                "nachtrag": nachtrag,
                "vorgangstyp": vorgangstyp,
                "typ": typ,
                "titel": titel,
                "dokumentart": dokumentart,
                "vorgang_id": vorgang_id,
                "datum": datum,
                "aktualisiert": aktualisiert,
                "fundstelle": fundstelle,
                "aktivitaet_anzahl": aktivitaet_anzahl,
            }
        )
        if urheber is not UNSET:
            field_dict["urheber"] = urheber
        if ueberweisung is not UNSET:
            field_dict["ueberweisung"] = ueberweisung
        if aktivitaet_anzeige is not UNSET:
            field_dict["aktivitaet_anzeige"] = aktivitaet_anzeige
        if ressort is not UNSET:
            field_dict["ressort"] = ressort
        if beschlussfassung is not UNSET:
            field_dict["beschlussfassung"] = beschlussfassung
        if ratsdok is not UNSET:
            field_dict["ratsdok"] = ratsdok
        if kom is not UNSET:
            field_dict["kom"] = kom
        if sek is not UNSET:
            field_dict["sek"] = sek
        if mitberaten is not UNSET:
            field_dict["mitberaten"] = mitberaten
        if abstract is not UNSET:
            field_dict["abstract"] = abstract

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.aktivitaet_anzeige import AktivitaetAnzeige
        from ..models.beschlussfassung import Beschlussfassung
        from ..models.fundstelle import Fundstelle
        from ..models.ressort import Ressort
        from ..models.ueberweisung import Ueberweisung
        from ..models.urheber import Urheber
        from ..models.vorgangspositionbezug import Vorgangspositionbezug

        d = src_dict.copy()
        id = d.pop("id")

        vorgangsposition = d.pop("vorgangsposition")

        zuordnung = Zuordnung(d.pop("zuordnung"))

        gang = d.pop("gang")

        fortsetzung = d.pop("fortsetzung")

        nachtrag = d.pop("nachtrag")

        vorgangstyp = d.pop("vorgangstyp")

        typ = VorgangspositionTyp(d.pop("typ"))

        titel = d.pop("titel")

        dokumentart = VorgangspositionDokumentart(d.pop("dokumentart"))

        vorgang_id = d.pop("vorgang_id")

        datum = isoparse(d.pop("datum")).date()

        aktualisiert = isoparse(d.pop("aktualisiert"))

        fundstelle = Fundstelle.from_dict(d.pop("fundstelle"))

        aktivitaet_anzahl = d.pop("aktivitaet_anzahl")

        urheber = []
        _urheber = d.pop("urheber", UNSET)
        for urheber_item_data in _urheber or []:
            urheber_item = Urheber.from_dict(urheber_item_data)

            urheber.append(urheber_item)

        ueberweisung = []
        _ueberweisung = d.pop("ueberweisung", UNSET)
        for ueberweisung_item_data in _ueberweisung or []:
            ueberweisung_item = Ueberweisung.from_dict(ueberweisung_item_data)

            ueberweisung.append(ueberweisung_item)

        aktivitaet_anzeige = []
        _aktivitaet_anzeige = d.pop("aktivitaet_anzeige", UNSET)
        for aktivitaet_anzeige_item_data in _aktivitaet_anzeige or []:
            aktivitaet_anzeige_item = AktivitaetAnzeige.from_dict(aktivitaet_anzeige_item_data)

            aktivitaet_anzeige.append(aktivitaet_anzeige_item)

        ressort = []
        _ressort = d.pop("ressort", UNSET)
        for ressort_item_data in _ressort or []:
            ressort_item = Ressort.from_dict(ressort_item_data)

            ressort.append(ressort_item)

        beschlussfassung = []
        _beschlussfassung = d.pop("beschlussfassung", UNSET)
        for beschlussfassung_item_data in _beschlussfassung or []:
            beschlussfassung_item = Beschlussfassung.from_dict(beschlussfassung_item_data)

            beschlussfassung.append(beschlussfassung_item)

        ratsdok = d.pop("ratsdok", UNSET)

        kom = d.pop("kom", UNSET)

        sek = d.pop("sek", UNSET)

        mitberaten = []
        _mitberaten = d.pop("mitberaten", UNSET)
        for mitberaten_item_data in _mitberaten or []:
            mitberaten_item = Vorgangspositionbezug.from_dict(mitberaten_item_data)

            mitberaten.append(mitberaten_item)

        abstract = d.pop("abstract", UNSET)

        vorgangsposition = cls(
            id=id,
            vorgangsposition=vorgangsposition,
            zuordnung=zuordnung,
            gang=gang,
            fortsetzung=fortsetzung,
            nachtrag=nachtrag,
            vorgangstyp=vorgangstyp,
            typ=typ,
            titel=titel,
            dokumentart=dokumentart,
            vorgang_id=vorgang_id,
            datum=datum,
            aktualisiert=aktualisiert,
            fundstelle=fundstelle,
            aktivitaet_anzahl=aktivitaet_anzahl,
            urheber=urheber,
            ueberweisung=ueberweisung,
            aktivitaet_anzeige=aktivitaet_anzeige,
            ressort=ressort,
            beschlussfassung=beschlussfassung,
            ratsdok=ratsdok,
            kom=kom,
            sek=sek,
            mitberaten=mitberaten,
            abstract=abstract,
        )

        vorgangsposition.additional_properties = d
        return vorgangsposition

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
