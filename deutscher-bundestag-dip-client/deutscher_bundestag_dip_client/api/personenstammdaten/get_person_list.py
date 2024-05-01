import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_person_list_format import GetPersonListFormat
from ...models.person_list_response import PersonListResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    f_aktualisiert_start: Union[Unset, datetime.datetime] = UNSET,
    f_aktualisiert_end: Union[Unset, datetime.datetime] = UNSET,
    f_datum_start: Union[Unset, datetime.date] = UNSET,
    f_datum_end: Union[Unset, datetime.date] = UNSET,
    f_id: Union[Unset, List[int]] = UNSET,
    f_wahlperiode: Union[Unset, List[int]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    format_: Union[Unset, GetPersonListFormat] = GetPersonListFormat.JSON,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_f_aktualisiert_start: Union[Unset, str] = UNSET
    if not isinstance(f_aktualisiert_start, Unset):
        json_f_aktualisiert_start = f_aktualisiert_start.isoformat()
    params["f.aktualisiert.start"] = json_f_aktualisiert_start

    json_f_aktualisiert_end: Union[Unset, str] = UNSET
    if not isinstance(f_aktualisiert_end, Unset):
        json_f_aktualisiert_end = f_aktualisiert_end.isoformat()
    params["f.aktualisiert.end"] = json_f_aktualisiert_end

    json_f_datum_start: Union[Unset, str] = UNSET
    if not isinstance(f_datum_start, Unset):
        json_f_datum_start = f_datum_start.isoformat()
    params["f.datum.start"] = json_f_datum_start

    json_f_datum_end: Union[Unset, str] = UNSET
    if not isinstance(f_datum_end, Unset):
        json_f_datum_end = f_datum_end.isoformat()
    params["f.datum.end"] = json_f_datum_end

    json_f_id: Union[Unset, List[int]] = UNSET
    if not isinstance(f_id, Unset):
        json_f_id = f_id

    params["f.id"] = json_f_id

    json_f_wahlperiode: Union[Unset, List[int]] = UNSET
    if not isinstance(f_wahlperiode, Unset):
        json_f_wahlperiode = f_wahlperiode

    params["f.wahlperiode"] = json_f_wahlperiode

    params["cursor"] = cursor

    json_format_: Union[Unset, str] = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/person",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, PersonListResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = PersonListResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = cast(Any, None)
        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, PersonListResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    f_aktualisiert_start: Union[Unset, datetime.datetime] = UNSET,
    f_aktualisiert_end: Union[Unset, datetime.datetime] = UNSET,
    f_datum_start: Union[Unset, datetime.date] = UNSET,
    f_datum_end: Union[Unset, datetime.date] = UNSET,
    f_id: Union[Unset, List[int]] = UNSET,
    f_wahlperiode: Union[Unset, List[int]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    format_: Union[Unset, GetPersonListFormat] = GetPersonListFormat.JSON,
) -> Response[Union[Any, PersonListResponse]]:
    """Liefert eine Liste von Personenstammdaten

    Args:
        f_aktualisiert_start (Union[Unset, datetime.datetime]):
        f_aktualisiert_end (Union[Unset, datetime.datetime]):
        f_datum_start (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_datum_end (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_id (Union[Unset, List[int]]):
        f_wahlperiode (Union[Unset, List[int]]):
        cursor (Union[Unset, str]):
        format_ (Union[Unset, GetPersonListFormat]):  Default: GetPersonListFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PersonListResponse]]
    """

    kwargs = _get_kwargs(
        f_aktualisiert_start=f_aktualisiert_start,
        f_aktualisiert_end=f_aktualisiert_end,
        f_datum_start=f_datum_start,
        f_datum_end=f_datum_end,
        f_id=f_id,
        f_wahlperiode=f_wahlperiode,
        cursor=cursor,
        format_=format_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    f_aktualisiert_start: Union[Unset, datetime.datetime] = UNSET,
    f_aktualisiert_end: Union[Unset, datetime.datetime] = UNSET,
    f_datum_start: Union[Unset, datetime.date] = UNSET,
    f_datum_end: Union[Unset, datetime.date] = UNSET,
    f_id: Union[Unset, List[int]] = UNSET,
    f_wahlperiode: Union[Unset, List[int]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    format_: Union[Unset, GetPersonListFormat] = GetPersonListFormat.JSON,
) -> Optional[Union[Any, PersonListResponse]]:
    """Liefert eine Liste von Personenstammdaten

    Args:
        f_aktualisiert_start (Union[Unset, datetime.datetime]):
        f_aktualisiert_end (Union[Unset, datetime.datetime]):
        f_datum_start (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_datum_end (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_id (Union[Unset, List[int]]):
        f_wahlperiode (Union[Unset, List[int]]):
        cursor (Union[Unset, str]):
        format_ (Union[Unset, GetPersonListFormat]):  Default: GetPersonListFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PersonListResponse]
    """

    return sync_detailed(
        client=client,
        f_aktualisiert_start=f_aktualisiert_start,
        f_aktualisiert_end=f_aktualisiert_end,
        f_datum_start=f_datum_start,
        f_datum_end=f_datum_end,
        f_id=f_id,
        f_wahlperiode=f_wahlperiode,
        cursor=cursor,
        format_=format_,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    f_aktualisiert_start: Union[Unset, datetime.datetime] = UNSET,
    f_aktualisiert_end: Union[Unset, datetime.datetime] = UNSET,
    f_datum_start: Union[Unset, datetime.date] = UNSET,
    f_datum_end: Union[Unset, datetime.date] = UNSET,
    f_id: Union[Unset, List[int]] = UNSET,
    f_wahlperiode: Union[Unset, List[int]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    format_: Union[Unset, GetPersonListFormat] = GetPersonListFormat.JSON,
) -> Response[Union[Any, PersonListResponse]]:
    """Liefert eine Liste von Personenstammdaten

    Args:
        f_aktualisiert_start (Union[Unset, datetime.datetime]):
        f_aktualisiert_end (Union[Unset, datetime.datetime]):
        f_datum_start (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_datum_end (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_id (Union[Unset, List[int]]):
        f_wahlperiode (Union[Unset, List[int]]):
        cursor (Union[Unset, str]):
        format_ (Union[Unset, GetPersonListFormat]):  Default: GetPersonListFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, PersonListResponse]]
    """

    kwargs = _get_kwargs(
        f_aktualisiert_start=f_aktualisiert_start,
        f_aktualisiert_end=f_aktualisiert_end,
        f_datum_start=f_datum_start,
        f_datum_end=f_datum_end,
        f_id=f_id,
        f_wahlperiode=f_wahlperiode,
        cursor=cursor,
        format_=format_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    f_aktualisiert_start: Union[Unset, datetime.datetime] = UNSET,
    f_aktualisiert_end: Union[Unset, datetime.datetime] = UNSET,
    f_datum_start: Union[Unset, datetime.date] = UNSET,
    f_datum_end: Union[Unset, datetime.date] = UNSET,
    f_id: Union[Unset, List[int]] = UNSET,
    f_wahlperiode: Union[Unset, List[int]] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    format_: Union[Unset, GetPersonListFormat] = GetPersonListFormat.JSON,
) -> Optional[Union[Any, PersonListResponse]]:
    """Liefert eine Liste von Personenstammdaten

    Args:
        f_aktualisiert_start (Union[Unset, datetime.datetime]):
        f_aktualisiert_end (Union[Unset, datetime.datetime]):
        f_datum_start (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_datum_end (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_id (Union[Unset, List[int]]):
        f_wahlperiode (Union[Unset, List[int]]):
        cursor (Union[Unset, str]):
        format_ (Union[Unset, GetPersonListFormat]):  Default: GetPersonListFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, PersonListResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            f_aktualisiert_start=f_aktualisiert_start,
            f_aktualisiert_end=f_aktualisiert_end,
            f_datum_start=f_datum_start,
            f_datum_end=f_datum_end,
            f_id=f_id,
            f_wahlperiode=f_wahlperiode,
            cursor=cursor,
            format_=format_,
        )
    ).parsed
