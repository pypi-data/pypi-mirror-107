from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.filter_operator import FilterOperator
from ..models.metadata_date_range import MetadataDateRange
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchFilter")


@attr.s(auto_attribs=True)
class SearchFilter:
    """ Search metadata schema. """

    operator: FilterOperator
    value: Union[List[MetadataDateRange], List[str], MetadataDateRange, Unset, str] = ""
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        operator = self.operator.value

        value: Union[Dict[str, Any], List[Dict[str, Any]], List[str], Unset, str]
        if isinstance(self.value, Unset):
            value = UNSET
        elif isinstance(self.value, list):
            value = UNSET
            if not isinstance(self.value, Unset):
                value = self.value

        elif isinstance(self.value, MetadataDateRange):
            value = UNSET
            if not isinstance(self.value, Unset):
                value = self.value.to_dict()

        elif isinstance(self.value, list):
            value = UNSET
            if not isinstance(self.value, Unset):
                value = []
                for value_type_3_item_data in self.value:
                    value_type_3_item = value_type_3_item_data.to_dict()

                    value.append(value_type_3_item)

        else:
            value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "operator": operator,
            }
        )
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        operator = FilterOperator(d.pop("operator"))

        def _parse_value(data: object) -> Union[List[MetadataDateRange], List[str], MetadataDateRange, Unset, str]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_1 = cast(List[str], data)

                return value_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _value_type_2 = data
                value_type_2: Union[Unset, MetadataDateRange]
                if isinstance(_value_type_2, Unset):
                    value_type_2 = UNSET
                else:
                    value_type_2 = MetadataDateRange.from_dict(_value_type_2)

                return value_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, list):
                    raise TypeError()
                value_type_3 = UNSET
                _value_type_3 = data
                for value_type_3_item_data in _value_type_3 or []:
                    value_type_3_item = MetadataDateRange.from_dict(value_type_3_item_data)

                    value_type_3.append(value_type_3_item)

                return value_type_3
            except:  # noqa: E722
                pass
            return cast(Union[List[MetadataDateRange], List[str], MetadataDateRange, Unset, str], data)

        value = _parse_value(d.pop("value", UNSET))

        search_filter = cls(
            operator=operator,
            value=value,
        )

        search_filter.additional_properties = d
        return search_filter

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
