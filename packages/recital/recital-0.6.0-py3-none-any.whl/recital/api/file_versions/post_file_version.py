from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.body_post_file_version_api_v1_files_versions_item_item_id_post import (
    BodyPostFileVersionApiV1FilesVersionsItemItemIdPost,
)
from ...models.version import Version
from ...types import UNSET, File, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    item_id: int,
    multipart_data: BodyPostFileVersionApiV1FilesVersionsItemItemIdPost,
    idx_task_id: Union[Unset, int] = UNSET,
    incremental: Union[Unset, bool] = False,
    force_ocr: Union[Unset, bool] = False,
) -> Dict[str, Any]:
    url = "{}/api/v1/files/versions/item/{item_id}/".format(client.base_url, item_id=item_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {
        "idx_task_id": idx_task_id,
        "incremental": incremental,
        "force_ocr": force_ocr,
    }
    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    files = {}
    data = {}
    for key, value in multipart_data.to_dict().items():
        if isinstance(value, File):
            files[key] = value
        else:
            data[key] = value

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": files,
        "data": data,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[None, Version]]:
    if response.status_code == 201:
        response_201 = Version.from_dict(response.json())

        return response_201
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 400:
        response_400 = None

        return response_400
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 422:
        response_422 = None

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[None, Version]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    item_id: int,
    multipart_data: BodyPostFileVersionApiV1FilesVersionsItemItemIdPost,
    idx_task_id: Union[Unset, int] = UNSET,
    incremental: Union[Unset, bool] = False,
    force_ocr: Union[Unset, bool] = False,
) -> Response[Union[None, Version]]:
    kwargs = _get_kwargs(
        client=client,
        item_id=item_id,
        multipart_data=multipart_data,
        idx_task_id=idx_task_id,
        incremental=incremental,
        force_ocr=force_ocr,
    )

    response = httpx.post(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    item_id: int,
    multipart_data: BodyPostFileVersionApiV1FilesVersionsItemItemIdPost,
    idx_task_id: Union[Unset, int] = UNSET,
    incremental: Union[Unset, bool] = False,
    force_ocr: Union[Unset, bool] = False,
) -> Optional[Union[None, Version]]:
    """Creates a new version of a file item.<br/>
    When a new version is created, it is automatically marked as the latest one
    and its name and display_name are inherited from the parent file item.<br/>
    If the number of versions of the parent item exceeds the maximum one
    specified in the organization versioning policy, the oldest version is deleted.

    An optional idx_task_id query parameter may be passed to the route,
    which will be saved on the file.

    An incremental query parameter could be passed
    to specify if the task item number should be incremented.

    - If the user is basic, they can only add files in folders they have write rights on.
    - If the user is orgadmin, they can add files in any of their organization's folders."""

    return sync_detailed(
        client=client,
        item_id=item_id,
        multipart_data=multipart_data,
        idx_task_id=idx_task_id,
        incremental=incremental,
        force_ocr=force_ocr,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    item_id: int,
    multipart_data: BodyPostFileVersionApiV1FilesVersionsItemItemIdPost,
    idx_task_id: Union[Unset, int] = UNSET,
    incremental: Union[Unset, bool] = False,
    force_ocr: Union[Unset, bool] = False,
) -> Response[Union[None, Version]]:
    kwargs = _get_kwargs(
        client=client,
        item_id=item_id,
        multipart_data=multipart_data,
        idx_task_id=idx_task_id,
        incremental=incremental,
        force_ocr=force_ocr,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.post(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    item_id: int,
    multipart_data: BodyPostFileVersionApiV1FilesVersionsItemItemIdPost,
    idx_task_id: Union[Unset, int] = UNSET,
    incremental: Union[Unset, bool] = False,
    force_ocr: Union[Unset, bool] = False,
) -> Optional[Union[None, Version]]:
    """Creates a new version of a file item.<br/>
    When a new version is created, it is automatically marked as the latest one
    and its name and display_name are inherited from the parent file item.<br/>
    If the number of versions of the parent item exceeds the maximum one
    specified in the organization versioning policy, the oldest version is deleted.

    An optional idx_task_id query parameter may be passed to the route,
    which will be saved on the file.

    An incremental query parameter could be passed
    to specify if the task item number should be incremented.

    - If the user is basic, they can only add files in folders they have write rights on.
    - If the user is orgadmin, they can add files in any of their organization's folders."""

    return (
        await asyncio_detailed(
            client=client,
            item_id=item_id,
            multipart_data=multipart_data,
            idx_task_id=idx_task_id,
            incremental=incremental,
            force_ocr=force_ocr,
        )
    ).parsed
