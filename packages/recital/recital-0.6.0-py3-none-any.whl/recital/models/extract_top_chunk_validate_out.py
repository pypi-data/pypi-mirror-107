from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.extract_top_chunk_validate_out_coordinates import ExtractTopChunkValidateOutCoordinates
from ..models.extract_top_chunk_validate_out_div_idxs import ExtractTopChunkValidateOutDivIdxs
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExtractTopChunkValidateOut")


@attr.s(auto_attribs=True)
class ExtractTopChunkValidateOut:
    """ Top chunk schema in extract result to validate. """

    rank: int
    chunk_id: str
    page: int
    text: str
    result_id: int
    distance: Union[Unset, float] = UNSET
    div_idxs: Union[Unset, ExtractTopChunkValidateOutDivIdxs] = UNSET
    coordinates: Union[Unset, ExtractTopChunkValidateOutCoordinates] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        rank = self.rank
        chunk_id = self.chunk_id
        page = self.page
        text = self.text
        result_id = self.result_id
        distance = self.distance
        div_idxs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.div_idxs, Unset):
            div_idxs = self.div_idxs.to_dict()

        coordinates: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.coordinates, Unset):
            coordinates = self.coordinates.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "rank": rank,
                "chunk_id": chunk_id,
                "page": page,
                "text": text,
                "result_id": result_id,
            }
        )
        if distance is not UNSET:
            field_dict["distance"] = distance
        if div_idxs is not UNSET:
            field_dict["div_idxs"] = div_idxs
        if coordinates is not UNSET:
            field_dict["coordinates"] = coordinates

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        rank = d.pop("rank")

        chunk_id = d.pop("chunk_id")

        page = d.pop("page")

        text = d.pop("text")

        result_id = d.pop("result_id")

        distance = d.pop("distance", UNSET)

        _div_idxs = d.pop("div_idxs", UNSET)
        div_idxs: Union[Unset, ExtractTopChunkValidateOutDivIdxs]
        if isinstance(_div_idxs, Unset):
            div_idxs = UNSET
        else:
            div_idxs = ExtractTopChunkValidateOutDivIdxs.from_dict(_div_idxs)

        _coordinates = d.pop("coordinates", UNSET)
        coordinates: Union[Unset, ExtractTopChunkValidateOutCoordinates]
        if isinstance(_coordinates, Unset):
            coordinates = UNSET
        else:
            coordinates = ExtractTopChunkValidateOutCoordinates.from_dict(_coordinates)

        extract_top_chunk_validate_out = cls(
            rank=rank,
            chunk_id=chunk_id,
            page=page,
            text=text,
            result_id=result_id,
            distance=distance,
            div_idxs=div_idxs,
            coordinates=coordinates,
        )

        extract_top_chunk_validate_out.additional_properties = d
        return extract_top_chunk_validate_out

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
