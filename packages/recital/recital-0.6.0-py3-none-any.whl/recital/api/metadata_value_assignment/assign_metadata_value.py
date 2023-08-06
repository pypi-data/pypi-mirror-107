from typing import Any, Dict, Union

import httpx

from ...client import AuthenticatedClient
from ...models.metadata_date_range import MetadataDateRange
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    metadata_id: int,
    json_body: MetadataDateRange,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    value: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/api/v1/metadata/{metadata_id}/value/".format(client.base_url, metadata_id=metadata_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "folder_id": folder_id,
        "version_id": version_id,
        "value": value,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[None]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    metadata_id: int,
    json_body: MetadataDateRange,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    value: Union[Unset, str] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        metadata_id=metadata_id,
        json_body=json_body,
        folder_id=folder_id,
        version_id=version_id,
        value=value,
    )

    response = httpx.put(
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    metadata_id: int,
    json_body: MetadataDateRange,
    folder_id: Union[Unset, int] = UNSET,
    version_id: Union[Unset, int] = UNSET,
    value: Union[Unset, str] = UNSET,
) -> Response[None]:
    kwargs = _get_kwargs(
        client=client,
        metadata_id=metadata_id,
        json_body=json_body,
        folder_id=folder_id,
        version_id=version_id,
        value=value,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.put(**kwargs)

    return _build_response(response=response)
