import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.extract_paragraph_config import ExtractParagraphConfig
from ..models.extract_question_config import ExtractQuestionConfig
from ..models.extract_type import ExtractType
from ..models.extract_value_config import ExtractValueConfig

T = TypeVar("T", bound="ExtractModelOut")


@attr.s(auto_attribs=True)
class ExtractModelOut:
    """ Extract model schema to be received on the GET /extract/models response. """

    config: Union[ExtractParagraphConfig, ExtractQuestionConfig, ExtractValueConfig]
    id: int
    org_id: int
    name: str
    type: ExtractType
    created_on: datetime.datetime
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        if isinstance(self.config, ExtractValueConfig):
            config = self.config.to_dict()

        elif isinstance(self.config, ExtractParagraphConfig):
            config = self.config.to_dict()

        else:
            config = self.config.to_dict()

        id = self.id
        org_id = self.org_id
        name = self.name
        type = self.type.value

        created_on = self.created_on.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
                "id": id,
                "org_id": org_id,
                "name": name,
                "type": type,
                "created_on": created_on,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_config(data: object) -> Union[ExtractParagraphConfig, ExtractQuestionConfig, ExtractValueConfig]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_type_0 = ExtractValueConfig.from_dict(data)

                return config_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                config_type_1 = ExtractParagraphConfig.from_dict(data)

                return config_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            config_type_2 = ExtractQuestionConfig.from_dict(data)

            return config_type_2

        config = _parse_config(d.pop("config"))

        id = d.pop("id")

        org_id = d.pop("org_id")

        name = d.pop("name")

        type = ExtractType(d.pop("type"))

        created_on = isoparse(d.pop("created_on"))

        extract_model_out = cls(
            config=config,
            id=id,
            org_id=org_id,
            name=name,
            type=type,
            created_on=created_on,
        )

        extract_model_out.additional_properties = d
        return extract_model_out

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
