from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.app_status import AppStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="HealthCheckOut")


@attr.s(auto_attribs=True)
class HealthCheckOut:
    """ A pydantic schema for health reports. """

    version: str
    status: AppStatus
    sql_connection: Union[Unset, bool] = True
    mongodb_connection: Union[Unset, bool] = True
    rabbitmq_connection: Union[Unset, bool] = True
    queued_jobs: Union[Unset, int] = 0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        version = self.version
        status = self.status.value

        sql_connection = self.sql_connection
        mongodb_connection = self.mongodb_connection
        rabbitmq_connection = self.rabbitmq_connection
        queued_jobs = self.queued_jobs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "version": version,
                "status": status,
            }
        )
        if sql_connection is not UNSET:
            field_dict["sql_connection"] = sql_connection
        if mongodb_connection is not UNSET:
            field_dict["mongodb_connection"] = mongodb_connection
        if rabbitmq_connection is not UNSET:
            field_dict["rabbitmq_connection"] = rabbitmq_connection
        if queued_jobs is not UNSET:
            field_dict["queued_jobs"] = queued_jobs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        version = d.pop("version")

        status = AppStatus(d.pop("status"))

        sql_connection = d.pop("sql_connection", UNSET)

        mongodb_connection = d.pop("mongodb_connection", UNSET)

        rabbitmq_connection = d.pop("rabbitmq_connection", UNSET)

        queued_jobs = d.pop("queued_jobs", UNSET)

        health_check_out = cls(
            version=version,
            status=status,
            sql_connection=sql_connection,
            mongodb_connection=mongodb_connection,
            rabbitmq_connection=rabbitmq_connection,
            queued_jobs=queued_jobs,
        )

        health_check_out.additional_properties = d
        return health_check_out

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
