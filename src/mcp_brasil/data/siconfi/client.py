"""HTTP client for the SICONFI API.

Docs: https://apidatalake.tesouro.gov.br/ords/siconfi/tt/swagger-ui/index.html

Endpoints:
    - GET /entes           → listar_entes
    - GET /rreo            → buscar_rreo
    - GET /rgf             → buscar_rgf
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import DEFAULT_LIMIT, ENTES_URL, RGF_URL, RREO_URL
from .schemas import EnteSiconfi, ItemDemonstrativo

logger = logging.getLogger(__name__)


def _parse_ente(raw: dict[str, Any]) -> EnteSiconfi:
    return EnteSiconfi(
        cod_ibge=raw.get("cod_ibge"),
        ente=raw.get("ente"),
        uf=raw.get("uf"),
        regiao=raw.get("regiao"),
        esfera=raw.get("esfera"),
        capital=raw.get("capital", "").strip() or None,
        populacao=raw.get("populacao"),
        cnpj=raw.get("cnpj"),
    )


def _parse_item(raw: dict[str, Any]) -> ItemDemonstrativo:
    return ItemDemonstrativo(
        exercicio=raw.get("exercicio"),
        demonstrativo=raw.get("demonstrativo"),
        periodo=raw.get("periodo"),
        periodicidade=raw.get("periodicidade"),
        instituicao=raw.get("instituicao"),
        cod_ibge=raw.get("cod_ibge"),
        uf=raw.get("uf"),
        anexo=raw.get("anexo"),
        esfera=raw.get("esfera"),
        coluna=raw.get("coluna"),
        cod_conta=raw.get("cod_conta"),
        conta=raw.get("conta"),
        valor=raw.get("valor"),
    )


async def listar_entes(
    *,
    uf: str | None = None,
    esfera: str | None = None,
    nome: str | None = None,
    limite: int = DEFAULT_LIMIT,
) -> list[EnteSiconfi]:
    """List public entities (states, municipalities) registered in SICONFI.

    The API does not support server-side filtering, so all results are fetched
    and filtered client-side.

    Args:
        uf: State abbreviation filter (e.g. "SP", "RJ").
        esfera: Government sphere: "E" (state), "M" (municipal), "U" (federal).
        nome: Partial name search (case-insensitive).
        limite: Max results.
    """
    # Fetch a large page — API doesn't support server-side UF/esfera filters
    params: dict[str, Any] = {"limit": 5000}

    result = await http_get(ENTES_URL, params=params)
    if not isinstance(result, dict):
        return []

    items = result.get("items") or []
    entes = [_parse_ente(i) for i in items]

    # Client-side filtering
    if uf:
        uf_upper = uf.upper()
        entes = [e for e in entes if e.uf == uf_upper]
    if esfera:
        esfera_upper = esfera.upper()
        entes = [e for e in entes if e.esfera == esfera_upper]
    if nome:
        nome_lower = nome.lower()
        entes = [e for e in entes if nome_lower in (e.ente or "").lower()]

    return entes[:limite]


async def buscar_rreo(
    *,
    cod_ibge: int,
    exercicio: int,
    periodo: int,
    anexo: str = "RREO-Anexo 01",
) -> list[ItemDemonstrativo]:
    """Fetch RREO (Relatório Resumido de Execução Orçamentária) for an entity.

    Args:
        cod_ibge: IBGE code of the entity (1 = Federal Government).
        exercicio: Fiscal year (e.g. 2024).
        periodo: Bimonthly period (1-6).
        anexo: Report annex name (default: "RREO-Anexo 01" = Budget Revenue).
    """
    params: dict[str, Any] = {
        "an_exercicio": exercicio,
        "nr_periodo": periodo,
        "co_tipo_demonstrativo": "RREO",
        "no_anexo": anexo,
        "id_ente": cod_ibge,
    }
    result = await http_get(RREO_URL, params=params)
    if not isinstance(result, dict):
        return []
    return [_parse_item(i) for i in (result.get("items") or [])]


async def buscar_rgf(
    *,
    cod_ibge: int,
    exercicio: int,
    periodo: int,
    anexo: str = "RGF-Anexo 01",
    poder: str = "E",
    esfera: str = "E",
) -> list[ItemDemonstrativo]:
    """Fetch RGF (Relatório de Gestão Fiscal) for an entity.

    Args:
        cod_ibge: IBGE code of the entity.
        exercicio: Fiscal year (e.g. 2024).
        periodo: Quarterly period (1-3).
        anexo: Report annex (default: "RGF-Anexo 01" = Personnel Expenditure).
        poder: Government branch: "E" (executive), "L" (legislative), "J" (judiciary).
        esfera: Sphere: "E" (state), "M" (municipal), "U" (federal).
    """
    params: dict[str, Any] = {
        "an_exercicio": exercicio,
        "in_periodicidade": "Q",
        "nr_periodo": periodo,
        "co_tipo_demonstrativo": "RGF",
        "no_anexo": anexo,
        "co_esfera": esfera.upper(),
        "co_poder": poder.upper(),
        "id_ente": cod_ibge,
    }
    result = await http_get(RGF_URL, params=params)
    if not isinstance(result, dict):
        return []
    return [_parse_item(i) for i in (result.get("items") or [])]
