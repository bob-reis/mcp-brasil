"""HTTP client for Interpol Red Notices and wanted persons search."""

from __future__ import annotations

import logging

import httpx

from mcp_brasil._shared.rate_limiter import RateLimiter

from .schemas import InterpolNotice

logger = logging.getLogger(__name__)

_rate_limiter = RateLimiter(max_requests=15, period=60.0)

_INTERPOL_BASE = "https://ws-public.interpol.int/notices/v1"
_HEADERS = {"Accept": "application/json"}


async def buscar_interpol(nome: str, nacionalidade: str = "BR", max_results: int = 5) -> list[InterpolNotice]:
    """Search Interpol Red Notices by name."""
    parts = nome.strip().split()
    params: dict[str, object] = {
        "resultPerPage": min(max_results, 10),
    }
    if nacionalidade:
        params["nationality"] = nacionalidade.upper()
    if len(parts) >= 2:
        params["forename"] = parts[0]
        params["name"] = parts[-1]
    else:
        params["name"] = nome

    async with _rate_limiter:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(f"{_INTERPOL_BASE}/red", params=params, headers=_HEADERS)
            if resp.status_code != 200:
                logger.warning("Interpol API returned HTTP %s", resp.status_code)
                return []
            data = resp.json()
            notices = data.get("_embedded", {}).get("notices", [])
            return [
                InterpolNotice(
                    nome=(n.get("forename", "") + " " + n.get("name", "")).strip(),
                    nacionalidade=", ".join(n.get("nationalities", [])),
                    data_nascimento=n.get("date_of_birth"),
                    link=n.get("_links", {}).get("self", {}).get("href"),
                )
                for n in notices[:max_results]
            ]
