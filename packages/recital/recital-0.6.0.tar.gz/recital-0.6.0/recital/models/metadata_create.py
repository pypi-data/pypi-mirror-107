from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.metadata_date_range import MetadataDateRange
from ..models.metadata_type import MetadataType
from ..types import UNSET, Unset

T = TypeVar("T", bound="MetadataCreate")


@attr.s(auto_attribs=True)
class MetadataCreate:
    """ Metadata schema for metadata creation. """

    name: str
    value_type: Union[Unset, MetadataType] = UNSET
    value: Union[MetadataDateRange, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        value_type: Union[Unset, str] = UNSET
        if not isinstance(self.value_type, Unset):
            value_type = self.value_type.value

        value: Union[Dict[str, Any], Unset, str]
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, MetadataDateRange):
            value = UNSET
            if not isinstance(self.value, Unset):
                value = self.value.to_dict()

        else:
            value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if value_type is not UNSET:
            field_dict["value_type"] = value_type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        _value_type = d.pop("value_type", UNSET)
        value_type: Union[Unset, MetadataType]
        if isinstance(_value_type, Unset):
            value_type = UNSET
        else:
            value_type = MetadataType(_value_type)

        def _parse_value(data: object) -> Union[MetadataDateRange, Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _value_type_0 = data
                value_type_0: Union[Unset, MetadataDateRange]
                if isinstance(_value_type_0, Unset):
                    value_type_0 = UNSET
                else:
                    value_type_0 = MetadataDateRange.from_dict(_value_type_0)

                return value_type_0
            except:  # noqa: E722
                pass
            return cast(Union[MetadataDateRange, Unset, str], data)

        value = _parse_value(d.pop("value", UNSET))

        metadata_create = cls(
            name=name,
            value_type=value_type,
            value=value,
        )

        metadata_create.additional_properties = d
        return metadata_create

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
