"""HTTP client for the Querido Diário API (Open Knowledge Brasil)."""

from __future__ import annotations

import logging
from urllib.parse import quote_plus

import httpx

from mcp_brasil._shared.rate_limiter import RateLimiter

from .schemas import Gazette, GazetteSearchResult

logger = logging.getLogger(__name__)

_rate_limiter = RateLimiter(max_requests=30, period=60.0)

_QD_BASE = "https://api.queridodiario.ok.org.br"

# Códigos IBGE para as capitais e principais cidades
_IBGE_CODES: dict[str, str] = {
    "uberlandia": "3170206",
    "sao paulo": "3550308",
    "rio de janeiro": "3304557",
    "belo horizonte": "3106200",
    "brasilia": "5300108",
    "curitiba": "4106902",
    "salvador": "2927408",
    "fortaleza": "2304400",
    "recife": "2611606",
    "porto alegre": "4314902",
    "goiania": "5208707",
    "manaus": "1302603",
    "campinas": "3509502",
    "patos de minas": "3148004",
    "uberaba": "3170107",
    "juiz de fora": "3136702",
    "florianopolis": "4205407",
    "vitoria": "3205309",
    "natal": "2408102",
    "joao pessoa": "2507507",
    "maceio": "2704302",
    "campo grande": "5002704",
    "teresina": "2211001",
    "sao luis": "2111300",
    "aracaju": "2800308",
    "cuiaba": "5103403",
    "belem": "1501402",
    "macapa": "1600303",
    "palmas": "1721000",
    "boa vista": "1400100",
    "porto velho": "1100205",
    "rio branco": "1200401",
    "ribeirao preto": "3543402",
    "sao bernardo do campo": "3548708",
    "santo andre": "3547809",
    "osasco": "3534401",
    "sorocaba": "3552205",
    "londrina": "4113700",
    "joinville": "4209102",
    "contagem": "3118601",
    "aparecida de goiania": "5201405",
    "feira de santana": "2910800",
    "caxias do sul": "4305108",
    "mogi das cruzes": "3530607",
    "sao jose dos campos": "3549904",
}


async def buscar_territorio(municipio: str) -> str | None:
    """Resolve city name to IBGE territory_id via Querido Diário API."""
    # Check local cache first
    key = municipio.lower().strip()
    for variation in [key, key.replace("-", " "), key.replace("'", "")]:
        if variation in _IBGE_CODES:
            return _IBGE_CODES[variation]

    # Fallback to API search
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{_QD_BASE}/cities", params={"city_name": municipio})
        if resp.status_code == 200:
            cities = resp.json().get("cities", [])
            if cities:
                return cities[0].get("territory_id")
    return None


async def buscar_diarios(
    municipio: str,
    query: str = "",
    max_results: int = 5,
) -> GazetteSearchResult:
    """Search municipal official gazettes by city and optional query string."""
    territory_id = await buscar_territorio(municipio)
    if not territory_id:
        return GazetteSearchResult(
            municipio=municipio,
            query=query,
            total=0,
            gazettes=[],
        )

    search_query = query if query else municipio
    params: dict[str, object] = {
        "territory_ids": territory_id,
        "querystring": search_query,
        "excerpt_size": 400,
        "number_of_excerpts": 2,
        "size": min(max_results, 10),
        "sort_by": "descending_date",
    }

    async with _rate_limiter:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.get(f"{_QD_BASE}/gazettes", params=params)
            resp.raise_for_status()
            data = resp.json()
            total = data.get("total_gazettes", 0)
            gazettes: list[Gazette] = [
                Gazette(
                    data=gz.get("date"),
                    municipio=gz.get("territory_name", municipio),
                    uf=gz.get("state_code"),
                    edicao=gz.get("edition"),
                    url=gz.get("url"),
                    trechos=[e[:400] for e in gz.get("excerpts", [])[:2]],
                )
                for gz in data.get("gazettes", [])[:max_results]
            ]
            return GazetteSearchResult(
                municipio=municipio,
                territory_id=territory_id,
                query=search_query,
                total=total,
                gazettes=gazettes,
            )
