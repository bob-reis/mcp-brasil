"""HTTP client for the BNMP (Banco Nacional de Mandados de Prisão) API."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from mcp_brasil._shared.rate_limiter import RateLimiter

from .schemas import MandadoPrisao

logger = logging.getLogger(__name__)

_rate_limiter = RateLimiter(max_requests=20, period=60.0)

_BNMP_URL = "https://portalbnmp.cnj.jus.br/bnmpportal/api/pesquisa-pecas/filter"
_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


async def buscar_mandados(nome: str, pagina: int = 0, tamanho: int = 10) -> list[MandadoPrisao]:
    """Search for arrest warrants in BNMP by person name."""
    async with _rate_limiter:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(
                _BNMP_URL,
                json={
                    "blespidasDesdeDataFato": False,
                    "nomePessoa": nome,
                    "page": pagina,
                    "size": min(tamanho, 20),
                    "sort": ["dataExpedicao,DESC"],
                },
                headers=_HEADERS,
            )
            resp.raise_for_status()
            data = resp.json()
            content: list[dict[str, Any]] = []
            if isinstance(data, dict):
                content = data.get("content", [])
            elif isinstance(data, list):
                content = data
            return [
                MandadoPrisao(
                    nome=item.get("nomePessoa"),
                    tipo_peca=item.get("tipoPeca"),
                    orgao_expeditor=item.get("orgaoExpeditor"),
                    data_expedicao=item.get("dataExpedicao"),
                    situacao=item.get("situacao"),
                    municipio=item.get("municipio"),
                    uf=item.get("uf"),
                )
                for item in content[:tamanho]
            ]
