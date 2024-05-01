from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="DokumentTextBase")


@_attrs_define
class DokumentTextBase:
    """Liefert zusätzlich zu den Metadaten den Volltext eines Dokuments.

    Attributes:
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

    text: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        text = self.text

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if text is not UNSET:
            field_dict["text"] = text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        text = d.pop("text", UNSET)

        dokument_text_base = cls(
            text=text,
        )

        dokument_text_base.additional_properties = d
        return dokument_text_base

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
