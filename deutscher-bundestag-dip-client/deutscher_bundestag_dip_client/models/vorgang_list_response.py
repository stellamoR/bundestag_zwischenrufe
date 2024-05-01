from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.vorgang import Vorgang


T = TypeVar("T", bound="VorgangListResponse")


@_attrs_define
class VorgangListResponse:
    """
    Attributes:
        num_found (int):  Example: 176.
        cursor (str):  Example: AoJwgNjC_PYCMURydWNrc2FjaGUtMjQ5MjYw.
        documents (List['Vorgang']):
    """

    num_found: int
    cursor: str
    documents: List["Vorgang"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        num_found = self.num_found

        cursor = self.cursor

        documents = []
        for documents_item_data in self.documents:
            documents_item = documents_item_data.to_dict()
            documents.append(documents_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "numFound": num_found,
                "cursor": cursor,
                "documents": documents,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.vorgang import Vorgang

        d = src_dict.copy()
        num_found = d.pop("numFound")

        cursor = d.pop("cursor")

        documents = []
        _documents = d.pop("documents")
        for documents_item_data in _documents:
            documents_item = Vorgang.from_dict(documents_item_data)

            documents.append(documents_item)

        vorgang_list_response = cls(
            num_found=num_found,
            cursor=cursor,
            documents=documents,
        )

        vorgang_list_response.additional_properties = d
        return vorgang_list_response

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
