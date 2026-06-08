"""HTTP client for the BNDES open data API (CKAN).

Docs: https://dadosabertos.bndes.gov.br

Endpoints (CKAN datastore):
    - datastore_search → buscar_operacoes
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import (
    DATASTORE_SEARCH_URL,
    DEFAULT_LIMIT,
    RESOURCE_OPERACOES_NAO_AUTO,
)
from .schemas import OperacaoBNDES

logger = logging.getLogger(__name__)


def _parse_operacao(raw: dict[str, Any]) -> OperacaoBNDES:
    def _int(v: Any) -> int | None:
        try:
            return int(v) if v is not None else None
        except (ValueError, TypeError):
            return None

    def _float(v: Any) -> float | None:
        try:
            return float(v) if v is not None else None
        except (ValueError, TypeError):
            return None

    return OperacaoBNDES(
        cliente=raw.get("cliente"),
        cnpj=raw.get("cnpj"),
        descricao_do_projeto=raw.get("descricao_do_projeto"),
        uf=raw.get("uf"),
        municipio=raw.get("municipio"),
        numero_do_contrato=raw.get("numero_do_contrato"),
        data_da_contratacao=raw.get("data_da_contratacao"),
        valor_contratado_reais=_float(raw.get("valor_contratado_reais")),
        valor_desembolsado_reais=_float(raw.get("valor_desembolsado_reais")),
        fonte_de_recurso_desembolsos=raw.get("fonte_de_recurso_desembolsos"),
        custo_financeiro=raw.get("custo_financeiro"),
        prazo_amortizacao_meses=_int(raw.get("prazo_amortizacao_meses")),
        modalidade_de_apoio=raw.get("modalidade_de_apoio"),
        forma_de_apoio=raw.get("forma_de_apoio"),
        produto=raw.get("produto"),
        setor_bndes=raw.get("setor_bndes"),
        subsetor_bndes=raw.get("subsetor_bndes"),
        porte_do_cliente=raw.get("porte_do_cliente"),
        natureza_do_cliente=raw.get("natureza_do_cliente"),
        situacao_do_contrato=raw.get("situacao_do_contrato"),
    )


async def buscar_operacoes(
    *,
    nome: str | None = None,
    cnpj: str | None = None,
    uf: str | None = None,
    setor_bndes: str | None = None,
    situacao: str | None = None,
    limite: int = DEFAULT_LIMIT,
) -> list[OperacaoBNDES]:
    """Search BNDES non-automatic financing operations.

    Args:
        nome: Client/beneficiary name (full-text search).
        cnpj: CNPJ of the client.
        uf: State code to filter (e.g. "SP").
        setor_bndes: BNDES sector name filter.
        situacao: Contract status: "CONTRATADO", "LIQUIDADO", "CANCELADO".
        limite: Max results (default: 20).
    """
    params: dict[str, Any] = {
        "resource_id": RESOURCE_OPERACOES_NAO_AUTO,
        "limit": min(limite, 100),
    }

    # Build filters dict for CKAN
    filters: dict[str, str] = {}
    if cnpj:
        # normalize CNPJ to match stored format XX.XXX.XXX/XXXX-XX
        cleaned = "".join(c for c in cnpj if c.isdigit())
        if len(cleaned) == 14:
            filters["cnpj"] = (
                f"{cleaned[:2]}.{cleaned[2:5]}.{cleaned[5:8]}/"
                f"{cleaned[8:12]}-{cleaned[12:]}"
            )
    if uf:
        filters["uf"] = uf.upper()
    if situacao:
        filters["situacao_do_contrato"] = situacao.upper()

    if filters:
        import json
        params["filters"] = json.dumps(filters)

    # Full-text search (nome or setor_bndes)
    search_terms = []
    if nome:
        search_terms.append(nome)
    if setor_bndes and not filters.get("setor_bndes"):
        search_terms.append(setor_bndes)
    if search_terms:
        params["q"] = " ".join(search_terms)

    result = await http_get(DATASTORE_SEARCH_URL, params=params)
    if not isinstance(result, dict):
        return []

    records = (result.get("result") or {}).get("records") or []
    return [_parse_operacao(r) for r in records]
