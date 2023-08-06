import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.extract_paragraph_config import ExtractParagraphConfig
from ..models.extract_question_config import ExtractQuestionConfig
from ..models.extract_task_status import ExtractTaskStatus
from ..models.extract_type import ExtractType
from ..models.extract_value_config import ExtractValueConfig
from ..models.source_filters import SourceFilters
from ..models.source_type import SourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtractWithConfigOut")


@attr.s(auto_attribs=True)
class ExtractWithConfigOut:
    """ Extract task schema to be returned as the GET /extract/tasks response. """

    model_id: int
    org_id: int
    type: ExtractType
    name: str
    created_by_id: int
    created_by_name: str
    created_on: datetime.datetime
    status: ExtractTaskStatus
    id: int
    total_documents: Union[Unset, int] = 0
    manual_documents: Union[Unset, int] = 0
    auto_documents: Union[Unset, int] = 0
    per_folder: Union[Unset, bool] = False
    questionnaire_id: Union[Unset, int] = UNSET
    completed_on: Union[Unset, datetime.datetime] = UNSET
    source_type: Union[Unset, SourceType] = UNSET
    source_filters: Union[Unset, SourceFilters] = UNSET
    config: Union[ExtractParagraphConfig, ExtractQuestionConfig, ExtractValueConfig, Unset] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        model_id = self.model_id
        org_id = self.org_id
        type = self.type.value

        name = self.name
        created_by_id = self.created_by_id
        created_by_name = self.created_by_name
        created_on = self.created_on.isoformat()

        status = self.status.value

        id = self.id
        total_documents = self.total_documents
        manual_documents = self.manual_documents
        auto_documents = self.auto_documents
        per_folder = self.per_folder
        questionnaire_id = self.questionnaire_id
        completed_on: Union[Unset, str] = UNSET
        if not isinstance(self.completed_on, Unset):
            completed_on = self.completed_on.isoformat()

        source_type: Union[Unset, str] = UNSET
        if not isinstance(self.source_type, Unset):
            source_type = self.source_type.value

        source_filters: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.source_filters, Unset):
            source_filters = self.source_filters.to_dict()

        config: Union[Dict[str, Any], Unset]
        if isinstance(self.config, Unset):
            config = UNSET
        elif isinstance(self.config, ExtractValueConfig):
            config = UNSET
            if not isinstance(self.config, Unset):
                config = self.config.to_dict()

        elif isinstance(self.config, ExtractParagraphConfig):
            config = UNSET
            if not isinstance(self.config, Unset):
                config = self.config.to_dict()

        else:
            config = UNSET
            if not isinstance(self.config, Unset):
                config = self.config.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model_id": model_id,
                "org_id": org_id,
                "type": type,
                "name": name,
                "created_by_id": created_by_id,
                "created_by_name": created_by_name,
                "created_on": created_on,
                "status": status,
                "id": id,
            }
        )
        if total_documents is not UNSET:
            field_dict["total_documents"] = total_documents
        if manual_documents is not UNSET:
            field_dict["manual_documents"] = manual_documents
        if auto_documents is not UNSET:
            field_dict["auto_documents"] = auto_documents
        if per_folder is not UNSET:
            field_dict["per_folder"] = per_folder
        if questionnaire_id is not UNSET:
            field_dict["questionnaire_id"] = questionnaire_id
        if completed_on is not UNSET:
            field_dict["completed_on"] = completed_on
        if source_type is not UNSET:
            field_dict["source_type"] = source_type
        if source_filters is not UNSET:
            field_dict["source_filters"] = source_filters
        if config is not UNSET:
            field_dict["config"] = config

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        model_id = d.pop("model_id")

        org_id = d.pop("org_id")

        type = ExtractType(d.pop("type"))

        name = d.pop("name")

        created_by_id = d.pop("created_by_id")

        created_by_name = d.pop("created_by_name")

        created_on = isoparse(d.pop("created_on"))

        status = ExtractTaskStatus(d.pop("status"))

        id = d.pop("id")

        total_documents = d.pop("total_documents", UNSET)

        manual_documents = d.pop("manual_documents", UNSET)

        auto_documents = d.pop("auto_documents", UNSET)

        per_folder = d.pop("per_folder", UNSET)

        questionnaire_id = d.pop("questionnaire_id", UNSET)

        _completed_on = d.pop("completed_on", UNSET)
        completed_on: Union[Unset, datetime.datetime]
        if isinstance(_completed_on, Unset):
            completed_on = UNSET
        else:
            completed_on = isoparse(_completed_on)

        _source_type = d.pop("source_type", UNSET)
        source_type: Union[Unset, SourceType]
        if isinstance(_source_type, Unset):
            source_type = UNSET
        else:
            source_type = SourceType(_source_type)

        _source_filters = d.pop("source_filters", UNSET)
        source_filters: Union[Unset, SourceFilters]
        if isinstance(_source_filters, Unset):
            source_filters = UNSET
        else:
            source_filters = SourceFilters.from_dict(_source_filters)

        def _parse_config(
            data: object,
        ) -> Union[ExtractParagraphConfig, ExtractQuestionConfig, ExtractValueConfig, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _config_type_0 = data
                config_type_0: Union[Unset, ExtractValueConfig]
                if isinstance(_config_type_0, Unset):
                    config_type_0 = UNSET
                else:
                    config_type_0 = ExtractValueConfig.from_dict(_config_type_0)

                return config_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _config_type_1 = data
                config_type_1: Union[Unset, ExtractParagraphConfig]
                if isinstance(_config_type_1, Unset):
                    config_type_1 = UNSET
                else:
                    config_type_1 = ExtractParagraphConfig.from_dict(_config_type_1)

                return config_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _config_type_2 = data
            config_type_2: Union[Unset, ExtractQuestionConfig]
            if isinstance(_config_type_2, Unset):
                config_type_2 = UNSET
            else:
                config_type_2 = ExtractQuestionConfig.from_dict(_config_type_2)

            return config_type_2

        config = _parse_config(d.pop("config", UNSET))

        extract_with_config_out = cls(
            model_id=model_id,
            org_id=org_id,
            type=type,
            name=name,
            created_by_id=created_by_id,
            created_by_name=created_by_name,
            created_on=created_on,
            status=status,
            id=id,
            total_documents=total_documents,
            manual_documents=manual_documents,
            auto_documents=auto_documents,
            per_folder=per_folder,
            questionnaire_id=questionnaire_id,
            completed_on=completed_on,
            source_type=source_type,
            source_filters=source_filters,
            config=config,
        )

        extract_with_config_out.additional_properties = d
        return extract_with_config_out

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
