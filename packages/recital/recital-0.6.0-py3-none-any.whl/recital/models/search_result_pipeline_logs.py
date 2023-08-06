from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.search_result_pipeline_logs_borda_chunks import SearchResultPipelineLogsBordaChunks
from ..models.search_result_pipeline_logs_documents import SearchResultPipelineLogsDocuments
from ..models.search_result_pipeline_logs_lexical_chunks import SearchResultPipelineLogsLexicalChunks
from ..models.search_result_pipeline_logs_semantic_chunks import SearchResultPipelineLogsSemanticChunks
from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchResultPipelineLogs")


@attr.s(auto_attribs=True)
class SearchResultPipelineLogs:
    """ Schema for search pipeline logs """

    documents: Union[Unset, SearchResultPipelineLogsDocuments] = UNSET
    lexical_chunks: Union[Unset, SearchResultPipelineLogsLexicalChunks] = UNSET
    semantic_chunks: Union[Unset, SearchResultPipelineLogsSemanticChunks] = UNSET
    borda_chunks: Union[Unset, SearchResultPipelineLogsBordaChunks] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        documents: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.documents, Unset):
            documents = self.documents.to_dict()

        lexical_chunks: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.lexical_chunks, Unset):
            lexical_chunks = self.lexical_chunks.to_dict()

        semantic_chunks: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.semantic_chunks, Unset):
            semantic_chunks = self.semantic_chunks.to_dict()

        borda_chunks: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.borda_chunks, Unset):
            borda_chunks = self.borda_chunks.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if documents is not UNSET:
            field_dict["documents"] = documents
        if lexical_chunks is not UNSET:
            field_dict["lexical_chunks"] = lexical_chunks
        if semantic_chunks is not UNSET:
            field_dict["semantic_chunks"] = semantic_chunks
        if borda_chunks is not UNSET:
            field_dict["borda_chunks"] = borda_chunks

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _documents = d.pop("documents", UNSET)
        documents: Union[Unset, SearchResultPipelineLogsDocuments]
        if isinstance(_documents, Unset):
            documents = UNSET
        else:
            documents = SearchResultPipelineLogsDocuments.from_dict(_documents)

        _lexical_chunks = d.pop("lexical_chunks", UNSET)
        lexical_chunks: Union[Unset, SearchResultPipelineLogsLexicalChunks]
        if isinstance(_lexical_chunks, Unset):
            lexical_chunks = UNSET
        else:
            lexical_chunks = SearchResultPipelineLogsLexicalChunks.from_dict(_lexical_chunks)

        _semantic_chunks = d.pop("semantic_chunks", UNSET)
        semantic_chunks: Union[Unset, SearchResultPipelineLogsSemanticChunks]
        if isinstance(_semantic_chunks, Unset):
            semantic_chunks = UNSET
        else:
            semantic_chunks = SearchResultPipelineLogsSemanticChunks.from_dict(_semantic_chunks)

        _borda_chunks = d.pop("borda_chunks", UNSET)
        borda_chunks: Union[Unset, SearchResultPipelineLogsBordaChunks]
        if isinstance(_borda_chunks, Unset):
            borda_chunks = UNSET
        else:
            borda_chunks = SearchResultPipelineLogsBordaChunks.from_dict(_borda_chunks)

        search_result_pipeline_logs = cls(
            documents=documents,
            lexical_chunks=lexical_chunks,
            semantic_chunks=semantic_chunks,
            borda_chunks=borda_chunks,
        )

        search_result_pipeline_logs.additional_properties = d
        return search_result_pipeline_logs

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
