import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.vorgang_typ import VorgangTyp
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.inkrafttreten import Inkrafttreten
    from ..models.verkuendung import Verkuendung
    from ..models.vorgang_deskriptor import VorgangDeskriptor
    from ..models.vorgang_verlinkung import VorgangVerlinkung


T = TypeVar("T", bound="Vorgang")


@_attrs_define
class Vorgang:
    """Liefert Metadaten zu einem Vorgang.

    Attributes:
        id (str):  Example: 84343.
        typ (VorgangTyp):  Example: Vorgang.
        vorgangstyp (str):  Example: Geschäftsordnung.
        wahlperiode (int):  Example: 19.
        aktualisiert (datetime.datetime): Letzte Aktualisierung der Entität Example: 2022-08-01T15:30:16+02:00.
        titel (str):  Example: Weitergeltung von Geschäftsordnungsrecht.
        beratungsstand (Union[Unset, str]):  Example: Abgeschlossen.
        initiative (Union[Unset, List[str]]):
        datum (Union[Unset, datetime.date]): Datierung des letzten zugehörigen Dokuments Example: 2019-03-27.
        abstract (Union[Unset, str]):  Example: Übernahme von Geschäftsordnungen durch den 19. Deutschen Bundestag:
            Geschäftsordnung des Deutschen Bundestages, Gemeinsame Geschäftsordnung für den Vermittlungsausschuss,
            Geschäftsordnung für den Gemeinsamen Ausschuss, Geschäftsordnung für das Verfahren nach Art. 115d GG,
            Richtlinien zur Überprüfung auf eine Stasi-Tätigkeit.
        sachgebiet (Union[Unset, List[str]]):
        deskriptor (Union[Unset, List['VorgangDeskriptor']]):
        gesta (Union[Unset, str]): GESTA-Ordnungsnummer Example: B101.
        zustimmungsbeduerftigkeit (Union[Unset, List[str]]):
        kom (Union[Unset, str]): KOM-Nr. Example: (2017) 600 endg..
        ratsdok (Union[Unset, str]): Ratsdok-Nr. Example: 11018/17.
        verkuendung (Union[Unset, List['Verkuendung']]):
        inkrafttreten (Union[Unset, List['Inkrafttreten']]):
        archiv (Union[Unset, str]): Archivsignatur Example: XIX/288.
        mitteilung (Union[Unset, str]):  Example: Tag des Inkrafttretens bestimmter Teile des Gesetzes wird durch das
            BMI im BGBl bekanntgemacht, weiteres siehe im BGBl.
        vorgang_verlinkung (Union[Unset, List['VorgangVerlinkung']]):
        sek (Union[Unset, str]): SEK-Nr. Example: (2010) 305 endg..
    """

    id: str
    typ: VorgangTyp
    vorgangstyp: str
    wahlperiode: int
    aktualisiert: datetime.datetime
    titel: str
    beratungsstand: Union[Unset, str] = UNSET
    initiative: Union[Unset, List[str]] = UNSET
    datum: Union[Unset, datetime.date] = UNSET
    abstract: Union[Unset, str] = UNSET
    sachgebiet: Union[Unset, List[str]] = UNSET
    deskriptor: Union[Unset, List["VorgangDeskriptor"]] = UNSET
    gesta: Union[Unset, str] = UNSET
    zustimmungsbeduerftigkeit: Union[Unset, List[str]] = UNSET
    kom: Union[Unset, str] = UNSET
    ratsdok: Union[Unset, str] = UNSET
    verkuendung: Union[Unset, List["Verkuendung"]] = UNSET
    inkrafttreten: Union[Unset, List["Inkrafttreten"]] = UNSET
    archiv: Union[Unset, str] = UNSET
    mitteilung: Union[Unset, str] = UNSET
    vorgang_verlinkung: Union[Unset, List["VorgangVerlinkung"]] = UNSET
    sek: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        typ = self.typ.value

        vorgangstyp = self.vorgangstyp

        wahlperiode = self.wahlperiode

        aktualisiert = self.aktualisiert.isoformat()

        titel = self.titel

        beratungsstand = self.beratungsstand

        initiative: Union[Unset, List[str]] = UNSET
        if not isinstance(self.initiative, Unset):
            initiative = self.initiative

        datum: Union[Unset, str] = UNSET
        if not isinstance(self.datum, Unset):
            datum = self.datum.isoformat()

        abstract = self.abstract

        sachgebiet: Union[Unset, List[str]] = UNSET
        if not isinstance(self.sachgebiet, Unset):
            sachgebiet = self.sachgebiet

        deskriptor: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.deskriptor, Unset):
            deskriptor = []
            for deskriptor_item_data in self.deskriptor:
                deskriptor_item = deskriptor_item_data.to_dict()
                deskriptor.append(deskriptor_item)

        gesta = self.gesta

        zustimmungsbeduerftigkeit: Union[Unset, List[str]] = UNSET
        if not isinstance(self.zustimmungsbeduerftigkeit, Unset):
            zustimmungsbeduerftigkeit = self.zustimmungsbeduerftigkeit

        kom = self.kom

        ratsdok = self.ratsdok

        verkuendung: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.verkuendung, Unset):
            verkuendung = []
            for verkuendung_item_data in self.verkuendung:
                verkuendung_item = verkuendung_item_data.to_dict()
                verkuendung.append(verkuendung_item)

        inkrafttreten: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.inkrafttreten, Unset):
            inkrafttreten = []
            for inkrafttreten_item_data in self.inkrafttreten:
                inkrafttreten_item = inkrafttreten_item_data.to_dict()
                inkrafttreten.append(inkrafttreten_item)

        archiv = self.archiv

        mitteilung = self.mitteilung

        vorgang_verlinkung: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.vorgang_verlinkung, Unset):
            vorgang_verlinkung = []
            for vorgang_verlinkung_item_data in self.vorgang_verlinkung:
                vorgang_verlinkung_item = vorgang_verlinkung_item_data.to_dict()
                vorgang_verlinkung.append(vorgang_verlinkung_item)

        sek = self.sek

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "typ": typ,
                "vorgangstyp": vorgangstyp,
                "wahlperiode": wahlperiode,
                "aktualisiert": aktualisiert,
                "titel": titel,
            }
        )
        if beratungsstand is not UNSET:
            field_dict["beratungsstand"] = beratungsstand
        if initiative is not UNSET:
            field_dict["initiative"] = initiative
        if datum is not UNSET:
            field_dict["datum"] = datum
        if abstract is not UNSET:
            field_dict["abstract"] = abstract
        if sachgebiet is not UNSET:
            field_dict["sachgebiet"] = sachgebiet
        if deskriptor is not UNSET:
            field_dict["deskriptor"] = deskriptor
        if gesta is not UNSET:
            field_dict["gesta"] = gesta
        if zustimmungsbeduerftigkeit is not UNSET:
            field_dict["zustimmungsbeduerftigkeit"] = zustimmungsbeduerftigkeit
        if kom is not UNSET:
            field_dict["kom"] = kom
        if ratsdok is not UNSET:
            field_dict["ratsdok"] = ratsdok
        if verkuendung is not UNSET:
            field_dict["verkuendung"] = verkuendung
        if inkrafttreten is not UNSET:
            field_dict["inkrafttreten"] = inkrafttreten
        if archiv is not UNSET:
            field_dict["archiv"] = archiv
        if mitteilung is not UNSET:
            field_dict["mitteilung"] = mitteilung
        if vorgang_verlinkung is not UNSET:
            field_dict["vorgang_verlinkung"] = vorgang_verlinkung
        if sek is not UNSET:
            field_dict["sek"] = sek

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.inkrafttreten import Inkrafttreten
        from ..models.verkuendung import Verkuendung
        from ..models.vorgang_deskriptor import VorgangDeskriptor
        from ..models.vorgang_verlinkung import VorgangVerlinkung

        d = src_dict.copy()
        id = d.pop("id")

        typ = VorgangTyp(d.pop("typ"))

        vorgangstyp = d.pop("vorgangstyp")

        wahlperiode = d.pop("wahlperiode")

        aktualisiert = isoparse(d.pop("aktualisiert"))

        titel = d.pop("titel")

        beratungsstand = d.pop("beratungsstand", UNSET)

        initiative = cast(List[str], d.pop("initiative", UNSET))

        _datum = d.pop("datum", UNSET)
        datum: Union[Unset, datetime.date]
        if isinstance(_datum, Unset):
            datum = UNSET
        else:
            datum = isoparse(_datum).date()

        abstract = d.pop("abstract", UNSET)

        sachgebiet = cast(List[str], d.pop("sachgebiet", UNSET))

        deskriptor = []
        _deskriptor = d.pop("deskriptor", UNSET)
        for deskriptor_item_data in _deskriptor or []:
            deskriptor_item = VorgangDeskriptor.from_dict(deskriptor_item_data)

            deskriptor.append(deskriptor_item)

        gesta = d.pop("gesta", UNSET)

        zustimmungsbeduerftigkeit = cast(List[str], d.pop("zustimmungsbeduerftigkeit", UNSET))

        kom = d.pop("kom", UNSET)

        ratsdok = d.pop("ratsdok", UNSET)

        verkuendung = []
        _verkuendung = d.pop("verkuendung", UNSET)
        for verkuendung_item_data in _verkuendung or []:
            verkuendung_item = Verkuendung.from_dict(verkuendung_item_data)

            verkuendung.append(verkuendung_item)

        inkrafttreten = []
        _inkrafttreten = d.pop("inkrafttreten", UNSET)
        for inkrafttreten_item_data in _inkrafttreten or []:
            inkrafttreten_item = Inkrafttreten.from_dict(inkrafttreten_item_data)

            inkrafttreten.append(inkrafttreten_item)

        archiv = d.pop("archiv", UNSET)

        mitteilung = d.pop("mitteilung", UNSET)

        vorgang_verlinkung = []
        _vorgang_verlinkung = d.pop("vorgang_verlinkung", UNSET)
        for vorgang_verlinkung_item_data in _vorgang_verlinkung or []:
            vorgang_verlinkung_item = VorgangVerlinkung.from_dict(vorgang_verlinkung_item_data)

            vorgang_verlinkung.append(vorgang_verlinkung_item)

        sek = d.pop("sek", UNSET)

        vorgang = cls(
            id=id,
            typ=typ,
            vorgangstyp=vorgangstyp,
            wahlperiode=wahlperiode,
            aktualisiert=aktualisiert,
            titel=titel,
            beratungsstand=beratungsstand,
            initiative=initiative,
            datum=datum,
            abstract=abstract,
            sachgebiet=sachgebiet,
            deskriptor=deskriptor,
            gesta=gesta,
            zustimmungsbeduerftigkeit=zustimmungsbeduerftigkeit,
            kom=kom,
            ratsdok=ratsdok,
            verkuendung=verkuendung,
            inkrafttreten=inkrafttreten,
            archiv=archiv,
            mitteilung=mitteilung,
            vorgang_verlinkung=vorgang_verlinkung,
            sek=sek,
        )

        vorgang.additional_properties = d
        return vorgang

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
