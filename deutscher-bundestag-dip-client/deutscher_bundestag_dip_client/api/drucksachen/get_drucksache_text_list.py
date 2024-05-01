import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.drucksache_text_list_response import DrucksacheTextListResponse
from ...models.get_drucksache_text_list_format import GetDrucksacheTextListFormat
from ...models.zuordnung import Zuordnung
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    f_aktualisiert_start: Union[Unset, datetime.datetime] = UNSET,
    f_aktualisiert_end: Union[Unset, datetime.datetime] = UNSET,
    f_datum_start: Union[Unset, datetime.date] = UNSET,
    f_datum_end: Union[Unset, datetime.date] = UNSET,
    f_dokumentnummer: Union[Unset, List[str]] = UNSET,
    f_drucksachetyp: Union[Unset, str] = UNSET,
    f_id: Union[Unset, List[int]] = UNSET,
    f_ressort_fdf: Union[Unset, List[str]] = UNSET,
    f_titel: Union[Unset, List[str]] = UNSET,
    f_urheber: Union[Unset, List[str]] = UNSET,
    f_vorgangstyp: Union[Unset, List[str]] = UNSET,
    f_vorgangstyp_notation: Union[Unset, List[int]] = UNSET,
    f_wahlperiode: Union[Unset, List[int]] = UNSET,
    f_zuordnung: Union[Unset, Zuordnung] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    format_: Union[Unset, GetDrucksacheTextListFormat] = GetDrucksacheTextListFormat.JSON,
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

    json_f_dokumentnummer: Union[Unset, List[str]] = UNSET
    if not isinstance(f_dokumentnummer, Unset):
        json_f_dokumentnummer = f_dokumentnummer

    params["f.dokumentnummer"] = json_f_dokumentnummer

    params["f.drucksachetyp"] = f_drucksachetyp

    json_f_id: Union[Unset, List[int]] = UNSET
    if not isinstance(f_id, Unset):
        json_f_id = f_id

    params["f.id"] = json_f_id

    json_f_ressort_fdf: Union[Unset, List[str]] = UNSET
    if not isinstance(f_ressort_fdf, Unset):
        json_f_ressort_fdf = f_ressort_fdf

    params["f.ressort_fdf"] = json_f_ressort_fdf

    json_f_titel: Union[Unset, List[str]] = UNSET
    if not isinstance(f_titel, Unset):
        json_f_titel = f_titel

    params["f.titel"] = json_f_titel

    json_f_urheber: Union[Unset, List[str]] = UNSET
    if not isinstance(f_urheber, Unset):
        json_f_urheber = f_urheber

    params["f.urheber"] = json_f_urheber

    json_f_vorgangstyp: Union[Unset, List[str]] = UNSET
    if not isinstance(f_vorgangstyp, Unset):
        json_f_vorgangstyp = f_vorgangstyp

    params["f.vorgangstyp"] = json_f_vorgangstyp

    json_f_vorgangstyp_notation: Union[Unset, List[int]] = UNSET
    if not isinstance(f_vorgangstyp_notation, Unset):
        json_f_vorgangstyp_notation = f_vorgangstyp_notation

    params["f.vorgangstyp_notation"] = json_f_vorgangstyp_notation

    json_f_wahlperiode: Union[Unset, List[int]] = UNSET
    if not isinstance(f_wahlperiode, Unset):
        json_f_wahlperiode = f_wahlperiode

    params["f.wahlperiode"] = json_f_wahlperiode

    json_f_zuordnung: Union[Unset, str] = UNSET
    if not isinstance(f_zuordnung, Unset):
        json_f_zuordnung = f_zuordnung.value

    params["f.zuordnung"] = json_f_zuordnung

    params["cursor"] = cursor

    json_format_: Union[Unset, str] = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/drucksache-text",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, DrucksacheTextListResponse]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DrucksacheTextListResponse.from_dict(response.json())

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
) -> Response[Union[Any, DrucksacheTextListResponse]]:
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
    f_dokumentnummer: Union[Unset, List[str]] = UNSET,
    f_drucksachetyp: Union[Unset, str] = UNSET,
    f_id: Union[Unset, List[int]] = UNSET,
    f_ressort_fdf: Union[Unset, List[str]] = UNSET,
    f_titel: Union[Unset, List[str]] = UNSET,
    f_urheber: Union[Unset, List[str]] = UNSET,
    f_vorgangstyp: Union[Unset, List[str]] = UNSET,
    f_vorgangstyp_notation: Union[Unset, List[int]] = UNSET,
    f_wahlperiode: Union[Unset, List[int]] = UNSET,
    f_zuordnung: Union[Unset, Zuordnung] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    format_: Union[Unset, GetDrucksacheTextListFormat] = GetDrucksacheTextListFormat.JSON,
) -> Response[Union[Any, DrucksacheTextListResponse]]:
    """Liefert eine Liste von Volltexten und Metadaten zu Drucksachen

    Args:
        f_aktualisiert_start (Union[Unset, datetime.datetime]):
        f_aktualisiert_end (Union[Unset, datetime.datetime]):
        f_datum_start (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_datum_end (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_dokumentnummer (Union[Unset, List[str]]):
        f_drucksachetyp (Union[Unset, str]):
        f_id (Union[Unset, List[int]]):
        f_ressort_fdf (Union[Unset, List[str]]):
        f_titel (Union[Unset, List[str]]):
        f_urheber (Union[Unset, List[str]]):
        f_vorgangstyp (Union[Unset, List[str]]):
        f_vorgangstyp_notation (Union[Unset, List[int]]):
        f_wahlperiode (Union[Unset, List[int]]):
        f_zuordnung (Union[Unset, Zuordnung]): Jeder Vorgangsschritt ist entweder dem Bundestag
            (BT), dem Bundesrat (BR), der Bundesversammlung (BV) oder der Europakammer (EK)
            zugeordnet. Über die Zuordnung lassen sich bspw. Rechtsverordnungen herausfiltern, an
            denen der Bundestag beteiligt / nicht beteiligt war.
        cursor (Union[Unset, str]):
        format_ (Union[Unset, GetDrucksacheTextListFormat]):  Default:
            GetDrucksacheTextListFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DrucksacheTextListResponse]]
    """

    kwargs = _get_kwargs(
        f_aktualisiert_start=f_aktualisiert_start,
        f_aktualisiert_end=f_aktualisiert_end,
        f_datum_start=f_datum_start,
        f_datum_end=f_datum_end,
        f_dokumentnummer=f_dokumentnummer,
        f_drucksachetyp=f_drucksachetyp,
        f_id=f_id,
        f_ressort_fdf=f_ressort_fdf,
        f_titel=f_titel,
        f_urheber=f_urheber,
        f_vorgangstyp=f_vorgangstyp,
        f_vorgangstyp_notation=f_vorgangstyp_notation,
        f_wahlperiode=f_wahlperiode,
        f_zuordnung=f_zuordnung,
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
    f_dokumentnummer: Union[Unset, List[str]] = UNSET,
    f_drucksachetyp: Union[Unset, str] = UNSET,
    f_id: Union[Unset, List[int]] = UNSET,
    f_ressort_fdf: Union[Unset, List[str]] = UNSET,
    f_titel: Union[Unset, List[str]] = UNSET,
    f_urheber: Union[Unset, List[str]] = UNSET,
    f_vorgangstyp: Union[Unset, List[str]] = UNSET,
    f_vorgangstyp_notation: Union[Unset, List[int]] = UNSET,
    f_wahlperiode: Union[Unset, List[int]] = UNSET,
    f_zuordnung: Union[Unset, Zuordnung] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    format_: Union[Unset, GetDrucksacheTextListFormat] = GetDrucksacheTextListFormat.JSON,
) -> Optional[Union[Any, DrucksacheTextListResponse]]:
    """Liefert eine Liste von Volltexten und Metadaten zu Drucksachen

    Args:
        f_aktualisiert_start (Union[Unset, datetime.datetime]):
        f_aktualisiert_end (Union[Unset, datetime.datetime]):
        f_datum_start (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_datum_end (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_dokumentnummer (Union[Unset, List[str]]):
        f_drucksachetyp (Union[Unset, str]):
        f_id (Union[Unset, List[int]]):
        f_ressort_fdf (Union[Unset, List[str]]):
        f_titel (Union[Unset, List[str]]):
        f_urheber (Union[Unset, List[str]]):
        f_vorgangstyp (Union[Unset, List[str]]):
        f_vorgangstyp_notation (Union[Unset, List[int]]):
        f_wahlperiode (Union[Unset, List[int]]):
        f_zuordnung (Union[Unset, Zuordnung]): Jeder Vorgangsschritt ist entweder dem Bundestag
            (BT), dem Bundesrat (BR), der Bundesversammlung (BV) oder der Europakammer (EK)
            zugeordnet. Über die Zuordnung lassen sich bspw. Rechtsverordnungen herausfiltern, an
            denen der Bundestag beteiligt / nicht beteiligt war.
        cursor (Union[Unset, str]):
        format_ (Union[Unset, GetDrucksacheTextListFormat]):  Default:
            GetDrucksacheTextListFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DrucksacheTextListResponse]
    """

    return sync_detailed(
        client=client,
        f_aktualisiert_start=f_aktualisiert_start,
        f_aktualisiert_end=f_aktualisiert_end,
        f_datum_start=f_datum_start,
        f_datum_end=f_datum_end,
        f_dokumentnummer=f_dokumentnummer,
        f_drucksachetyp=f_drucksachetyp,
        f_id=f_id,
        f_ressort_fdf=f_ressort_fdf,
        f_titel=f_titel,
        f_urheber=f_urheber,
        f_vorgangstyp=f_vorgangstyp,
        f_vorgangstyp_notation=f_vorgangstyp_notation,
        f_wahlperiode=f_wahlperiode,
        f_zuordnung=f_zuordnung,
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
    f_dokumentnummer: Union[Unset, List[str]] = UNSET,
    f_drucksachetyp: Union[Unset, str] = UNSET,
    f_id: Union[Unset, List[int]] = UNSET,
    f_ressort_fdf: Union[Unset, List[str]] = UNSET,
    f_titel: Union[Unset, List[str]] = UNSET,
    f_urheber: Union[Unset, List[str]] = UNSET,
    f_vorgangstyp: Union[Unset, List[str]] = UNSET,
    f_vorgangstyp_notation: Union[Unset, List[int]] = UNSET,
    f_wahlperiode: Union[Unset, List[int]] = UNSET,
    f_zuordnung: Union[Unset, Zuordnung] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    format_: Union[Unset, GetDrucksacheTextListFormat] = GetDrucksacheTextListFormat.JSON,
) -> Response[Union[Any, DrucksacheTextListResponse]]:
    """Liefert eine Liste von Volltexten und Metadaten zu Drucksachen

    Args:
        f_aktualisiert_start (Union[Unset, datetime.datetime]):
        f_aktualisiert_end (Union[Unset, datetime.datetime]):
        f_datum_start (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_datum_end (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_dokumentnummer (Union[Unset, List[str]]):
        f_drucksachetyp (Union[Unset, str]):
        f_id (Union[Unset, List[int]]):
        f_ressort_fdf (Union[Unset, List[str]]):
        f_titel (Union[Unset, List[str]]):
        f_urheber (Union[Unset, List[str]]):
        f_vorgangstyp (Union[Unset, List[str]]):
        f_vorgangstyp_notation (Union[Unset, List[int]]):
        f_wahlperiode (Union[Unset, List[int]]):
        f_zuordnung (Union[Unset, Zuordnung]): Jeder Vorgangsschritt ist entweder dem Bundestag
            (BT), dem Bundesrat (BR), der Bundesversammlung (BV) oder der Europakammer (EK)
            zugeordnet. Über die Zuordnung lassen sich bspw. Rechtsverordnungen herausfiltern, an
            denen der Bundestag beteiligt / nicht beteiligt war.
        cursor (Union[Unset, str]):
        format_ (Union[Unset, GetDrucksacheTextListFormat]):  Default:
            GetDrucksacheTextListFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, DrucksacheTextListResponse]]
    """

    kwargs = _get_kwargs(
        f_aktualisiert_start=f_aktualisiert_start,
        f_aktualisiert_end=f_aktualisiert_end,
        f_datum_start=f_datum_start,
        f_datum_end=f_datum_end,
        f_dokumentnummer=f_dokumentnummer,
        f_drucksachetyp=f_drucksachetyp,
        f_id=f_id,
        f_ressort_fdf=f_ressort_fdf,
        f_titel=f_titel,
        f_urheber=f_urheber,
        f_vorgangstyp=f_vorgangstyp,
        f_vorgangstyp_notation=f_vorgangstyp_notation,
        f_wahlperiode=f_wahlperiode,
        f_zuordnung=f_zuordnung,
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
    f_dokumentnummer: Union[Unset, List[str]] = UNSET,
    f_drucksachetyp: Union[Unset, str] = UNSET,
    f_id: Union[Unset, List[int]] = UNSET,
    f_ressort_fdf: Union[Unset, List[str]] = UNSET,
    f_titel: Union[Unset, List[str]] = UNSET,
    f_urheber: Union[Unset, List[str]] = UNSET,
    f_vorgangstyp: Union[Unset, List[str]] = UNSET,
    f_vorgangstyp_notation: Union[Unset, List[int]] = UNSET,
    f_wahlperiode: Union[Unset, List[int]] = UNSET,
    f_zuordnung: Union[Unset, Zuordnung] = UNSET,
    cursor: Union[Unset, str] = UNSET,
    format_: Union[Unset, GetDrucksacheTextListFormat] = GetDrucksacheTextListFormat.JSON,
) -> Optional[Union[Any, DrucksacheTextListResponse]]:
    """Liefert eine Liste von Volltexten und Metadaten zu Drucksachen

    Args:
        f_aktualisiert_start (Union[Unset, datetime.datetime]):
        f_aktualisiert_end (Union[Unset, datetime.datetime]):
        f_datum_start (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_datum_end (Union[Unset, datetime.date]): Liefert das Datum eines Dokuments (Drucksache
            oder Protokoll).
        f_dokumentnummer (Union[Unset, List[str]]):
        f_drucksachetyp (Union[Unset, str]):
        f_id (Union[Unset, List[int]]):
        f_ressort_fdf (Union[Unset, List[str]]):
        f_titel (Union[Unset, List[str]]):
        f_urheber (Union[Unset, List[str]]):
        f_vorgangstyp (Union[Unset, List[str]]):
        f_vorgangstyp_notation (Union[Unset, List[int]]):
        f_wahlperiode (Union[Unset, List[int]]):
        f_zuordnung (Union[Unset, Zuordnung]): Jeder Vorgangsschritt ist entweder dem Bundestag
            (BT), dem Bundesrat (BR), der Bundesversammlung (BV) oder der Europakammer (EK)
            zugeordnet. Über die Zuordnung lassen sich bspw. Rechtsverordnungen herausfiltern, an
            denen der Bundestag beteiligt / nicht beteiligt war.
        cursor (Union[Unset, str]):
        format_ (Union[Unset, GetDrucksacheTextListFormat]):  Default:
            GetDrucksacheTextListFormat.JSON.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, DrucksacheTextListResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            f_aktualisiert_start=f_aktualisiert_start,
            f_aktualisiert_end=f_aktualisiert_end,
            f_datum_start=f_datum_start,
            f_datum_end=f_datum_end,
            f_dokumentnummer=f_dokumentnummer,
            f_drucksachetyp=f_drucksachetyp,
            f_id=f_id,
            f_ressort_fdf=f_ressort_fdf,
            f_titel=f_titel,
            f_urheber=f_urheber,
            f_vorgangstyp=f_vorgangstyp,
            f_vorgangstyp_notation=f_vorgangstyp_notation,
            f_wahlperiode=f_wahlperiode,
            f_zuordnung=f_zuordnung,
            cursor=cursor,
            format_=format_,
        )
    ).parsed
