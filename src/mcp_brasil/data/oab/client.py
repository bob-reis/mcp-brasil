"""HTTP client for the OAB (Conselho Federal da OAB) API."""

from __future__ import annotations

import logging

import httpx

from mcp_brasil._shared.rate_limiter import RateLimiter

from .schemas import Advogado

logger = logging.getLogger(__name__)

_rate_limiter = RateLimiter(max_requests=20, period=60.0)

_OAB_BASE = "https://cna.oab.org.br/api/v1/advogados"
_HEADERS = {"Accept": "application/json"}


async def buscar_por_nome(nome: str, seccional: str = "") -> list[Advogado]:
    """Search lawyers by name, optionally filtered by state section."""
    params: dict[str, str] = {"nome": nome}
    if seccional:
        params["seccional"] = seccional.upper()

    async with _rate_limiter:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(_OAB_BASE, params=params, headers=_HEADERS)
            resp.raise_for_status()
            data = resp.json()
            items = data if isinstance(data, list) else data.get("content", data.get("data", []))
            if not isinstance(items, list):
                return []
            return [
                Advogado(
                    nome=adv.get("nome"),
                    numero_oab=adv.get("inscricao"),
                    seccional=adv.get("uf"),
                    situacao=adv.get("tipoInscricao"),
                    subtipo=adv.get("subtipo"),
                )
                for adv in items[:15]
            ]


async def buscar_por_numero(numero_oab: str, seccional: str) -> Advogado | None:
    """Lookup a lawyer by OAB registration number and state section."""
    url = f"{_OAB_BASE}/{seccional.upper()}/{numero_oab}"
    async with _rate_limiter:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(url, headers=_HEADERS)
            if resp.status_code == 404:
                return None
            resp.raise_for_status()
            data = resp.json()
            if not isinstance(data, dict) or not data.get("nome"):
                return None
            return Advogado(
                nome=data.get("nome"),
                numero_oab=data.get("inscricao", numero_oab),
                seccional=data.get("uf", seccional),
                situacao=data.get("tipoInscricao"),
                subtipo=data.get("subtipo"),
            )
