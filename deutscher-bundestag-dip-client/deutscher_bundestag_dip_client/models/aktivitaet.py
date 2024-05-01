import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.aktivitaet_dokumentart import AktivitaetDokumentart
from ..models.aktivitaet_typ import AktivitaetTyp
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.deskriptor import Deskriptor
    from ..models.fundstelle import Fundstelle
    from ..models.vorgangspositionbezug import Vorgangspositionbezug


T = TypeVar("T", bound="Aktivitaet")


@_attrs_define
class Aktivitaet:
    """Liefert Metadaten zu einer Aktivität.

    Attributes:
        id (str):  Example: 1493545.
        aktivitaetsart (str):  Example: Rede.
        typ (AktivitaetTyp):  Example: Aktivität.
        dokumentart (AktivitaetDokumentart):  Example: Plenarprotokoll.
        wahlperiode (int):  Example: 19.
        datum (datetime.date):  Example: 2020-12-11.
        aktualisiert (datetime.datetime): Letzte Aktualisierung der Entität oder des zugehörigen Dokuments Example:
            2022-08-01T15:30:16+02:00.
        titel (str):  Example: Olaf Scholz, Bundesmin., Bundesministerium der Finanzen.
        fundstelle (Fundstelle): Liefert im Vorgangsablauf das zu einem Vorgangsschritt gehörende Dokument (Drucksache
            oder Protokoll).

            Beispiel: „BT-Drucksache 19/1 (Antrag Fraktion der CDU/CSU)“ oder beim Vorgangsschritt Beratung „BT-
            Plenarprotokoll 19/1, S. 4C-12A“.
        vorgangsbezug_anzahl (int): Gesamtzahl der zugehörigen Vorgänge Example: 18.
        vorgangsbezug (Union[Unset, List['Vorgangspositionbezug']]): Zusammenfassung der ersten 4 zugehörigen Vorgänge
        deskriptor (Union[Unset, List['Deskriptor']]):
        abstract (Union[Unset, str]):  Example: Zusammenberaten mit Finanzplan.
    """

    id: str
    aktivitaetsart: str
    typ: AktivitaetTyp
    dokumentart: AktivitaetDokumentart
    wahlperiode: int
    datum: datetime.date
    aktualisiert: datetime.datetime
    titel: str
    fundstelle: "Fundstelle"
    vorgangsbezug_anzahl: int
    vorgangsbezug: Union[Unset, List["Vorgangspositionbezug"]] = UNSET
    deskriptor: Union[Unset, List["Deskriptor"]] = UNSET
    abstract: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id

        aktivitaetsart = self.aktivitaetsart

        typ = self.typ.value

        dokumentart = self.dokumentart.value

        wahlperiode = self.wahlperiode

        datum = self.datum.isoformat()

        aktualisiert = self.aktualisiert.isoformat()

        titel = self.titel

        fundstelle = self.fundstelle.to_dict()

        vorgangsbezug_anzahl = self.vorgangsbezug_anzahl

        vorgangsbezug: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.vorgangsbezug, Unset):
            vorgangsbezug = []
            for vorgangsbezug_item_data in self.vorgangsbezug:
                vorgangsbezug_item = vorgangsbezug_item_data.to_dict()
                vorgangsbezug.append(vorgangsbezug_item)

        deskriptor: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.deskriptor, Unset):
            deskriptor = []
            for deskriptor_item_data in self.deskriptor:
                deskriptor_item = deskriptor_item_data.to_dict()
                deskriptor.append(deskriptor_item)

        abstract = self.abstract

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "aktivitaetsart": aktivitaetsart,
                "typ": typ,
                "dokumentart": dokumentart,
                "wahlperiode": wahlperiode,
                "datum": datum,
                "aktualisiert": aktualisiert,
                "titel": titel,
                "fundstelle": fundstelle,
                "vorgangsbezug_anzahl": vorgangsbezug_anzahl,
            }
        )
        if vorgangsbezug is not UNSET:
            field_dict["vorgangsbezug"] = vorgangsbezug
        if deskriptor is not UNSET:
            field_dict["deskriptor"] = deskriptor
        if abstract is not UNSET:
            field_dict["abstract"] = abstract

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.deskriptor import Deskriptor
        from ..models.fundstelle import Fundstelle
        from ..models.vorgangspositionbezug import Vorgangspositionbezug

        d = src_dict.copy()
        id = d.pop("id")

        aktivitaetsart = d.pop("aktivitaetsart")

        typ = AktivitaetTyp(d.pop("typ"))

        dokumentart = AktivitaetDokumentart(d.pop("dokumentart"))

        wahlperiode = d.pop("wahlperiode")

        datum = isoparse(d.pop("datum")).date()

        aktualisiert = isoparse(d.pop("aktualisiert"))

        titel = d.pop("titel")

        fundstelle = Fundstelle.from_dict(d.pop("fundstelle"))

        vorgangsbezug_anzahl = d.pop("vorgangsbezug_anzahl")

        vorgangsbezug = []
        _vorgangsbezug = d.pop("vorgangsbezug", UNSET)
        for vorgangsbezug_item_data in _vorgangsbezug or []:
            vorgangsbezug_item = Vorgangspositionbezug.from_dict(vorgangsbezug_item_data)

            vorgangsbezug.append(vorgangsbezug_item)

        deskriptor = []
        _deskriptor = d.pop("deskriptor", UNSET)
        for deskriptor_item_data in _deskriptor or []:
            deskriptor_item = Deskriptor.from_dict(deskriptor_item_data)

            deskriptor.append(deskriptor_item)

        abstract = d.pop("abstract", UNSET)

        aktivitaet = cls(
            id=id,
            aktivitaetsart=aktivitaetsart,
            typ=typ,
            dokumentart=dokumentart,
            wahlperiode=wahlperiode,
            datum=datum,
            aktualisiert=aktualisiert,
            titel=titel,
            fundstelle=fundstelle,
            vorgangsbezug_anzahl=vorgangsbezug_anzahl,
            vorgangsbezug=vorgangsbezug,
            deskriptor=deskriptor,
            abstract=abstract,
        )

        aktivitaet.additional_properties = d
        return aktivitaet

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
