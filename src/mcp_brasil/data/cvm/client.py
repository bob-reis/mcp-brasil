"""HTTP client for the CVM open data API.

Uses the CKAN-based CVM data portal (dados.cvm.gov.br).

Endpoints:
    - /api/3/action/datastore_search  → buscar_companhias, buscar_processos, buscar_fundos
    - /api/3/action/package_search    → listar_datasets
"""

from __future__ import annotations

import json
import logging
from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import (
    CVM_CIA_ABERTA_RESOURCE_ID,
    CVM_CKAN_PACKAGE_SEARCH,
    CVM_CKAN_SEARCH,
    CVM_FI_RESOURCE_ID,
    CVM_PAS_RESOURCE_ID,
    DEFAULT_LIMIT,
)
from .schemas import CompanhiaAberta, FundoInvestimento, ProcessoCVM

logger = logging.getLogger(__name__)


def _parse_float(val: Any) -> float | None:
    """Safely parse a float value."""
    if val is None:
        return None
    try:
        return float(str(val).replace(".", "").replace(",", "."))
    except (ValueError, TypeError):
        return None


def _parse_cia(raw: dict[str, Any]) -> CompanhiaAberta:
    """Parse a public company record."""
    return CompanhiaAberta(
        cnpj=raw.get("CNPJ_CIA") or raw.get("cnpj"),
        nome=raw.get("DENOM_SOCIAL") or raw.get("DENOM_COMERC") or raw.get("nome"),
        tipo=raw.get("TP_MERC") or raw.get("tipo"),
        situacao=raw.get("SIT") or raw.get("situacao"),
        setor=raw.get("SETOR_ATIV") or raw.get("setor"),
        data_registro=raw.get("DT_REG") or raw.get("data_registro"),
        data_cancel=raw.get("DT_CANCEL") or raw.get("data_cancelamento"),
        email=raw.get("EMAIL") or raw.get("email"),
    )


def _parse_processo(raw: dict[str, Any]) -> ProcessoCVM:
    """Parse a CVM administrative proceeding record."""
    return ProcessoCVM(
        numero=raw.get("NUMERO_PAS") or raw.get("numero") or raw.get("NUM_PAS"),
        acusado=raw.get("NOME_ACUSADO") or raw.get("acusado") or raw.get("nome"),
        cpf_cnpj=raw.get("CPF_CNPJ") or raw.get("cpf_cnpj"),
        relator=raw.get("RELATOR") or raw.get("relator"),
        decisao=raw.get("RESULTADO") or raw.get("decisao") or raw.get("DECISAO"),
        data_julgamento=raw.get("DATA_JULGAMENTO") or raw.get("data"),
        penalidade=raw.get("TIPO_PENALIDADE") or raw.get("penalidade"),
        valor_multa=_parse_float(raw.get("VALOR_MULTA") or raw.get("valor_multa")),
        artigo=raw.get("ARTIGO") or raw.get("artigo"),
    )


def _parse_fundo(raw: dict[str, Any]) -> FundoInvestimento:
    """Parse an investment fund record."""
    return FundoInvestimento(
        cnpj=raw.get("CNPJ_FUNDO") or raw.get("cnpj"),
        denominacao=raw.get("DENOM_SOCIAL") or raw.get("denominacao") or raw.get("nome"),
        classe=raw.get("CLASSE") or raw.get("classe"),
        tipo=raw.get("TP_FUNDO") or raw.get("tipo"),
        situacao=raw.get("SIT") or raw.get("situacao"),
        administrador=raw.get("ADMIN") or raw.get("administrador"),
        data_registro=raw.get("DT_REG") or raw.get("data_registro"),
        patrimonio_liquido=_parse_float(
            raw.get("VL_PATRIM_LIQ") or raw.get("patrimonio")
        ),
    )


async def _ckan_search(
    resource_id: str,
    *,
    q: str | None = None,
    filters: dict[str, str] | None = None,
    limit: int = DEFAULT_LIMIT,
    offset: int = 0,
) -> list[dict[str, Any]]:
    """Query a CVM CKAN datastore resource."""
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
        result = await http_get(CVM_CKAN_SEARCH, params=params)
        if isinstance(result, dict):
            records = result.get("result", {}).get("records", [])
            return records if isinstance(records, list) else []
        return []
    except Exception:
        logger.warning("CVM CKAN query failed for resource_id=%s", resource_id)
        return []


async def buscar_companhias(
    *,
    nome: str | None = None,
    cnpj: str | None = None,
    situacao: str | None = None,
    pagina: int = 1,
) -> list[CompanhiaAberta]:
    """Fetch public companies registered with CVM.

    Args:
        nome: Company name or partial name.
        cnpj: CNPJ (digits only or formatted).
        situacao: Status filter (ex: "ATIVO", "CANCELADO").
        pagina: Page number (default: 1).
    """
    filters: dict[str, str] = {}
    if situacao:
        filters["SIT"] = situacao.upper()

    q = cnpj or nome
    offset = (pagina - 1) * DEFAULT_LIMIT

    records = await _ckan_search(
        CVM_CIA_ABERTA_RESOURCE_ID,
        q=q,
        filters=filters or None,
        limit=DEFAULT_LIMIT,
        offset=offset,
    )
    return [_parse_cia(r) for r in records]


async def buscar_processos(
    *,
    nome: str | None = None,
    cpf_cnpj: str | None = None,
    pagina: int = 1,
) -> list[ProcessoCVM]:
    """Fetch CVM administrative proceedings (PAS).

    Args:
        nome: Name of the accused.
        cpf_cnpj: CPF or CNPJ of the accused.
        pagina: Page number (default: 1).
    """
    q = cpf_cnpj or nome
    offset = (pagina - 1) * DEFAULT_LIMIT

    records = await _ckan_search(
        CVM_PAS_RESOURCE_ID,
        q=q,
        limit=DEFAULT_LIMIT,
        offset=offset,
    )
    return [_parse_processo(r) for r in records]


async def buscar_fundos(
    *,
    nome: str | None = None,
    cnpj: str | None = None,
    classe: str | None = None,
    pagina: int = 1,
) -> list[FundoInvestimento]:
    """Fetch investment funds registered with CVM.

    Args:
        nome: Fund name or partial name.
        cnpj: CNPJ of the fund.
        classe: Fund class (ex: "Renda Fixa", "Ações", "Multimercado").
        pagina: Page number (default: 1).
    """
    filters: dict[str, str] = {}
    if classe:
        filters["CLASSE"] = classe

    q = cnpj or nome
    offset = (pagina - 1) * DEFAULT_LIMIT

    records = await _ckan_search(
        CVM_FI_RESOURCE_ID,
        q=q,
        filters=filters or None,
        limit=DEFAULT_LIMIT,
        offset=offset,
    )
    return [_parse_fundo(r) for r in records]
