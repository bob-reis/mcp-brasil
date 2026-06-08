"""HTTP client for the DadosAbertos-MT CKAN API.

Endpoints:
    - /package_search          → buscar_datasets
    - /package_show            → detalhar_dataset
    - /organization_list       → listar_organizacoes
    - /organization_show       → detalhar_organizacao
    - /tag_list                → listar_tags
    - /group_list              → listar_grupos
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_brasil._shared.http_client import http_get
from mcp_brasil.exceptions import HttpClientError

from .constants import (
    DEFAULT_ROWS,
    GROUP_LIST_URL,
    ORGANIZATION_LIST_URL,
    ORGANIZATION_SHOW_URL,
    PACKAGE_SEARCH_URL,
    PACKAGE_SHOW_URL,
    TAG_LIST_URL,
)
from .schemas import Dataset, DatasetResultado, Grupo, Organizacao, Recurso

logger = logging.getLogger(__name__)


def _parse_dataset(item: dict[str, Any]) -> Dataset:
    org = item.get("organization") or {}
    tags = [t.get("name", "") for t in (item.get("tags") or []) if isinstance(t, dict)]
    groups = [
        g.get("title") or g.get("name", "")
        for g in (item.get("groups") or [])
        if isinstance(g, dict)
    ]
    resources = [
        Recurso(
            id=r.get("id"),
            name=r.get("name"),
            url=r.get("url"),
            format=r.get("format"),
            description=r.get("description"),
            created=r.get("created"),
            last_modified=r.get("last_modified"),
        )
        for r in (item.get("resources") or [])
        if isinstance(r, dict)
    ]
    return Dataset(
        id=item.get("id"),
        name=item.get("name"),
        title=item.get("title"),
        notes=item.get("notes"),
        organization_name=org.get("name") if isinstance(org, dict) else None,
        organization_title=org.get("title") if isinstance(org, dict) else None,
        tags=tags,
        groups=groups,
        resources=resources,
        metadata_created=item.get("metadata_created"),
        metadata_modified=item.get("metadata_modified"),
        num_resources=item.get("num_resources", len(resources)),
    )


async def buscar_datasets(
    *,
    query: str = "",
    organizacao: str | None = None,
    tag: str | None = None,
    grupo: str | None = None,
    rows: int = DEFAULT_ROWS,
    start: int = 0,
) -> DatasetResultado:
    """Busca datasets no portal CKAN do MT."""
    params: dict[str, Any] = {"rows": rows, "start": start}
    q_parts = []
    if query:
        q_parts.append(query)
    params["q"] = " ".join(q_parts) if q_parts else "*:*"

    fq_parts = []
    if organizacao:
        fq_parts.append(f"organization:{organizacao}")
    if tag:
        fq_parts.append(f"tags:{tag}")
    if grupo:
        fq_parts.append(f"groups:{grupo}")
    if fq_parts:
        params["fq"] = " ".join(fq_parts)

    try:
        data: dict[str, Any] = await http_get(PACKAGE_SEARCH_URL, params=params)
    except (HttpClientError, Exception) as exc:
        logger.warning("DadosAbertos MT API error: %s", exc)
        return DatasetResultado()

    result = data.get("result", {})
    items = result.get("results", [])
    return DatasetResultado(
        total=result.get("count", len(items)),
        datasets=[_parse_dataset(i) for i in items],
    )


async def detalhar_dataset(dataset_id: str) -> Dataset | None:
    """Obtém detalhes completos de um dataset, incluindo todos os recursos."""
    try:
        data: dict[str, Any] = await http_get(PACKAGE_SHOW_URL, params={"id": dataset_id})
    except (HttpClientError, Exception) as exc:
        logger.warning("DadosAbertos MT dataset '%s' error: %s", dataset_id, exc)
        return None
    result = data.get("result")
    if not result or not isinstance(result, dict):
        return None
    return _parse_dataset(result)


async def listar_organizacoes() -> list[Organizacao]:
    """Lista organizações publicadoras do portal MT."""
    try:
        data: dict[str, Any] = await http_get(
            ORGANIZATION_LIST_URL,
            params={"all_fields": "true", "include_dataset_count": "true"},
        )
    except (HttpClientError, Exception) as exc:
        logger.warning("DadosAbertos MT organizations error: %s", exc)
        return []
    items = data.get("result", [])
    return [
        Organizacao(
            id=o.get("id"),
            name=o.get("name"),
            title=o.get("title"),
            description=o.get("description"),
            package_count=o.get("package_count", 0),
        )
        for o in items
        if isinstance(o, dict)
    ]


async def detalhar_organizacao(org_id: str) -> Organizacao | None:
    """Obtém detalhes de uma organização."""
    try:
        data: dict[str, Any] = await http_get(
            ORGANIZATION_SHOW_URL,
            params={"id": org_id, "include_dataset_count": "true"},
        )
    except (HttpClientError, Exception) as exc:
        logger.warning("DadosAbertos MT org '%s' error: %s", org_id, exc)
        return None
    result = data.get("result")
    if not result or not isinstance(result, dict):
        return None
    return Organizacao(
        id=result.get("id"),
        name=result.get("name"),
        title=result.get("title"),
        description=result.get("description"),
        package_count=result.get("package_count", 0),
    )


async def listar_tags(query: str | None = None) -> list[str]:
    """Lista as tags disponíveis no portal."""
    params: dict[str, Any] = {}
    if query:
        params["q"] = query
    try:
        data: dict[str, Any] = await http_get(TAG_LIST_URL, params=params)
    except (HttpClientError, Exception) as exc:
        logger.warning("DadosAbertos MT tags error: %s", exc)
        return []
    result: list[str] = data.get("result", [])
    return result


async def listar_grupos() -> list[Grupo]:
    """Lista grupos temáticos do portal."""
    try:
        data: dict[str, Any] = await http_get(
            GROUP_LIST_URL,
            params={"all_fields": "true", "include_dataset_count": "true"},
        )
    except (HttpClientError, Exception) as exc:
        logger.warning("DadosAbertos MT groups error: %s", exc)
        return []
    items = data.get("result", [])
    return [
        Grupo(
            id=g.get("id"),
            name=g.get("name"),
            title=g.get("title"),
            description=g.get("description"),
            package_count=g.get("package_count", 0),
        )
        for g in items
        if isinstance(g, dict)
    ]
