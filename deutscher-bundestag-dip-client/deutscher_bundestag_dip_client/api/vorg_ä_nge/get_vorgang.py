from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_vorgang_format import GetVorgangFormat
from ...models.vorgang import Vorgang
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: int,
    *,
    format_: Union[Unset, GetVorgangFormat] = GetVorgangFormat.JSON,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_format_: Union[Unset, str] = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/vorgang/{id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Vorgang]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Vorgang.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Vorgang]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    format_: Union[Unset, GetVorgangFormat] = GetVorgangFormat.JSON,
) -> Response[Union[Any, Vorgang]]:
    """Liefert Metadaten zu einem Vorgang

    Args:
        id (int):
        format_ (Union[Unset, GetVorgangFormat]):  Default: GetVorgangFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Vorgang]]
    """

    kwargs = _get_kwargs(
        id=id,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    format_: Union[Unset, GetVorgangFormat] = GetVorgangFormat.JSON,
) -> Optional[Union[Any, Vorgang]]:
    """Liefert Metadaten zu einem Vorgang

    Args:
        id (int):
        format_ (Union[Unset, GetVorgangFormat]):  Default: GetVorgangFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Vorgang]
    """

    return sync_detailed(
        id=id,
        client=client,
        format_=format_,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    format_: Union[Unset, GetVorgangFormat] = GetVorgangFormat.JSON,
) -> Response[Union[Any, Vorgang]]:
    """Liefert Metadaten zu einem Vorgang

    Args:
        id (int):
        format_ (Union[Unset, GetVorgangFormat]):  Default: GetVorgangFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Vorgang]]
    """

    kwargs = _get_kwargs(
        id=id,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    format_: Union[Unset, GetVorgangFormat] = GetVorgangFormat.JSON,
) -> Optional[Union[Any, Vorgang]]:
    """Liefert Metadaten zu einem Vorgang

    Args:
        id (int):
        format_ (Union[Unset, GetVorgangFormat]):  Default: GetVorgangFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Vorgang]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            format_=format_,
        )
    ).parsed
