from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_plenarprotokoll_format import GetPlenarprotokollFormat
from ...models.plenarprotokoll import Plenarprotokoll
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: int,
    *,
    format_: Union[Unset, GetPlenarprotokollFormat] = GetPlenarprotokollFormat.JSON,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_format_: Union[Unset, str] = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    params["apikey"] = "rgsaY4U.oZRQKUHdJhF9qguHMkwCGIoLaqEcaHjYLF"

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/plenarprotokoll/{id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Plenarprotokoll]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Plenarprotokoll.from_dict(response.json())

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
) -> Response[Union[Any, Plenarprotokoll]]:
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
    format_: Union[Unset, GetPlenarprotokollFormat] = GetPlenarprotokollFormat.JSON,
) -> Response[Union[Any, Plenarprotokoll]]:
    """Liefert Metadaten zu einem Plenarprotokoll

    Args:
        id (int):
        format_ (Union[Unset, GetPlenarprotokollFormat]):  Default: GetPlenarprotokollFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Plenarprotokoll]]
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
    format_: Union[Unset, GetPlenarprotokollFormat] = GetPlenarprotokollFormat.JSON,
) -> Optional[Union[Any, Plenarprotokoll]]:
    """Liefert Metadaten zu einem Plenarprotokoll

    Args:
        id (int):
        format_ (Union[Unset, GetPlenarprotokollFormat]):  Default: GetPlenarprotokollFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Plenarprotokoll]
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
    format_: Union[Unset, GetPlenarprotokollFormat] = GetPlenarprotokollFormat.JSON,
) -> Response[Union[Any, Plenarprotokoll]]:
    """Liefert Metadaten zu einem Plenarprotokoll

    Args:
        id (int):
        format_ (Union[Unset, GetPlenarprotokollFormat]):  Default: GetPlenarprotokollFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Plenarprotokoll]]
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
    format_: Union[Unset, GetPlenarprotokollFormat] = GetPlenarprotokollFormat.JSON,
) -> Optional[Union[Any, Plenarprotokoll]]:
    """Liefert Metadaten zu einem Plenarprotokoll

    Args:
        id (int):
        format_ (Union[Unset, GetPlenarprotokollFormat]):  Default: GetPlenarprotokollFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Plenarprotokoll]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            format_=format_,
        )
    ).parsed
