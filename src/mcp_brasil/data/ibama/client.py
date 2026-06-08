"""HTTP client for the IBAMA open data API.

Uses the CKAN-based IBAMA open data portal (dadosabertos.ibama.gov.br).

Endpoints:
    - /api/3/action/datastore_search  → buscar_embargos, buscar_autos_infracao
    - /api/3/action/package_search    → listar_datasets
"""

from __future__ import annotations

import json
import logging
from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import (
    DEFAULT_LIMIT,
    IBAMA_AUTOS_RESOURCE_ID,
    IBAMA_CKAN_PACKAGE_SEARCH,
    IBAMA_CKAN_SEARCH,
    IBAMA_EMBARGOS_RESOURCE_ID,
)
from .schemas import AreaEmbargada, AutoInfracao, DatasetIBAMA

logger = logging.getLogger(__name__)


def _parse_float(val: Any) -> float | None:
    """Safely parse a float value from various formats."""
    if val is None:
        return None
    try:
        return float(str(val).replace(".", "").replace(",", "."))
    except (ValueError, TypeError):
        return None


def _parse_embargo(raw: dict[str, Any]) -> AreaEmbargada:
    """Parse a raw IBAMA embargo record."""
    return AreaEmbargada(
        numero_auto=raw.get("NUM_AUTO") or raw.get("numero_auto") or raw.get("auto"),
        cpf_cnpj=raw.get("CPF_CNPJ") or raw.get("cpf_cnpj") or raw.get("cpf") or raw.get("cnpj"),
        nome_embargado=raw.get("NOME_EMBARGADO") or raw.get("nome") or raw.get("embargado"),
        municipio=raw.get("MUNICIPIO") or raw.get("municipio"),
        uf=raw.get("UF") or raw.get("uf") or raw.get("estado"),
        bioma=raw.get("BIOMA") or raw.get("bioma"),
        area_ha=_parse_float(raw.get("AREA_HA") or raw.get("area_ha") or raw.get("area")),
        data_embargo=raw.get("DAT_EMBARGO") or raw.get("data_embargo") or raw.get("data"),
        motivo=raw.get("MOTIVO_EMBARGO") or raw.get("motivo") or raw.get("descricao"),
        status=raw.get("STATUS_EMBARGO") or raw.get("status"),
    )


def _parse_auto(raw: dict[str, Any]) -> AutoInfracao:
    """Parse a raw IBAMA enforcement action record."""
    return AutoInfracao(
        numero_auto=raw.get("NUM_AUTO") or raw.get("numero_auto") or raw.get("auto"),
        cpf_cnpj=raw.get("CPF_CNPJ") or raw.get("cpf_cnpj") or raw.get("cpf") or raw.get("cnpj"),
        nome_autuado=raw.get("NOME_AUTUADO") or raw.get("nome") or raw.get("autuado"),
        municipio=raw.get("MUNICIPIO") or raw.get("municipio"),
        uf=raw.get("UF") or raw.get("uf") or raw.get("estado"),
        tipo_infracao=raw.get("DES_INFRACAO") or raw.get("tipo_infracao") or raw.get("infracao"),
        valor_multa=_parse_float(
            raw.get("VAL_AUTO") or raw.get("valor_multa") or raw.get("multa")
        ),
        data_infracao=raw.get("DAT_AUTO") or raw.get("data_infracao") or raw.get("data"),
        status=raw.get("DES_STATUS_AUTO") or raw.get("status"),
        artigo_infringido=raw.get("DES_ARTIGO_INFRINGIDO") or raw.get("artigo"),
    )


async def _ckan_search(
    resource_id: str,
    *,
    q: str | None = None,
    filters: dict[str, str] | None = None,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Query a CKAN datastore resource."""
    params: dict[str, Any] = {
        "resource_id": resource_id,
        "limit": limit,
        "offset": offset,
    }
    if q:
        params["q"] = q
    if filters:
        params["filters"] = json.dumps(filters)

    try:
        result = await http_get(IBAMA_CKAN_SEARCH, params=params)
        if isinstance(result, dict):
            records = result.get("result", {}).get("records", [])
            return records if isinstance(records, list) else []
        return []
    except Exception:
        logger.warning("CKAN query failed for resource_id=%s", resource_id)
        return []


async def buscar_embargos(
    *,
    cpf_cnpj: str | None = None,
    uf: str | None = None,
    bioma: str | None = None,
    pagina: int = 1,
) -> list[AreaEmbargada]:
    """Fetch IBAMA embargoed areas.

    Args:
        cpf_cnpj: CPF or CNPJ of the embargoed entity.
        uf: State abbreviation (e.g. "PA", "MT").
        bioma: Biome name (e.g. "Amazônia", "Cerrado").
        pagina: Page number (default: 1).
    """
    filters: dict[str, str] = {}
    if uf:
        filters["UF"] = uf.upper()
    if bioma:
        filters["BIOMA"] = bioma

    q = cpf_cnpj if cpf_cnpj else None
    offset = (pagina - 1) * DEFAULT_LIMIT

    records = await _ckan_search(
        IBAMA_EMBARGOS_RESOURCE_ID,
        q=q,
        filters=filters or None,
        limit=DEFAULT_LIMIT,
        offset=offset,
    )
    return [_parse_embargo(r) for r in records]


async def buscar_autos_infracao(
    *,
    cpf_cnpj: str | None = None,
    uf: str | None = None,
    pagina: int = 1,
) -> list[AutoInfracao]:
    """Fetch IBAMA enforcement actions (autos de infração).

    Args:
        cpf_cnpj: CPF or CNPJ of the fined entity.
        uf: State abbreviation.
        pagina: Page number (default: 1).
    """
    filters: dict[str, str] = {}
    if uf:
        filters["UF"] = uf.upper()

    q = cpf_cnpj if cpf_cnpj else None
    offset = (pagina - 1) * DEFAULT_LIMIT

    records = await _ckan_search(
        IBAMA_AUTOS_RESOURCE_ID,
        q=q,
        filters=filters or None,
        limit=DEFAULT_LIMIT,
        offset=offset,
    )
    return [_parse_auto(r) for r in records]


async def listar_datasets() -> list[DatasetIBAMA]:
    """List available datasets in the IBAMA open data portal."""
    try:
        result = await http_get(IBAMA_CKAN_PACKAGE_SEARCH, params={"rows": 50})
        if not isinstance(result, dict):
            return []

        packages = result.get("result", {}).get("results", [])
        datasets: list[DatasetIBAMA] = []
        for pkg in packages:
            for resource in pkg.get("resources", []):
                datasets.append(
                    DatasetIBAMA(
                        nome=pkg.get("name"),
                        titulo=pkg.get("title"),
                        descricao=(pkg.get("notes") or "")[:200],
                        resource_id=resource.get("id"),
                        formato=resource.get("format"),
                        ultima_atualizacao=resource.get("last_modified"),
                    )
                )
        return datasets
    except Exception:
        logger.warning("Failed to list IBAMA datasets")
        return []
