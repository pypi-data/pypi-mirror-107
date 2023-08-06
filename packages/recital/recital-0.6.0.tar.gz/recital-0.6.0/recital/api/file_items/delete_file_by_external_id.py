from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    external_id: str,
) -> Dict[str, Any]:
    url = "{}/api/v1/files/external/{external_id}/".format(client.base_url, external_id=external_id)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[HTTPValidationError, None]]:
    if response.status_code == 204:
        response_204 = None

        return response_204
    if response.status_code == 401:
        response_401 = None

        return response_401
    if response.status_code == 404:
        response_404 = None

        return response_404
    if response.status_code == 403:
        response_403 = None

        return response_403
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[HTTPValidationError, None]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    external_id: str,
) -> Response[Union[HTTPValidationError, None]]:
    kwargs = _get_kwargs(
        client=client,
        external_id=external_id,
    )

    response = httpx.delete(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    external_id: str,
) -> Optional[Union[HTTPValidationError, None]]:
    """Deletes a file item by external id.

    All of the related file item data are deleted.
    - Basic users can only delete files in folders they have write rights on.
    - Orgadmins can delete files in any of their organization's folders."""

    return sync_detailed(
        client=client,
        external_id=external_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    external_id: str,
) -> Response[Union[HTTPValidationError, None]]:
    kwargs = _get_kwargs(
        client=client,
        external_id=external_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.delete(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    external_id: str,
) -> Optional[Union[HTTPValidationError, None]]:
    """Deletes a file item by external id.

    All of the related file item data are deleted.
    - Basic users can only delete files in folders they have write rights on.
    - Orgadmins can delete files in any of their organization's folders."""

    return (
        await asyncio_detailed(
            client=client,
            external_id=external_id,
        )
    ).parsed
