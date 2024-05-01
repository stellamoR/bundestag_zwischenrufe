from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListResponseBase")


@_attrs_define
class ListResponseBase:
    """
    Attributes:
        num_found (int):  Example: 176.
        cursor (str):  Example: AoJwgNjC_PYCMURydWNrc2FjaGUtMjQ5MjYw.
    """

    num_found: int
    cursor: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        num_found = self.num_found

        cursor = self.cursor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "numFound": num_found,
                "cursor": cursor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        num_found = d.pop("numFound")

        cursor = d.pop("cursor")

        list_response_base = cls(
            num_found=num_found,
            cursor=cursor,
        )

        list_response_base.additional_properties = d
        return list_response_base

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
