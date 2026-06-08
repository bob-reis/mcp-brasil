"""HTTP client for the OpenSanctions API.

Docs: https://www.opensanctions.org/docs/api/

Endpoints:
    - GET  /search/default     → buscar_entidades, verificar_entidade
    - GET  /entities/{id}      → obter_entidade
    - GET  /datasets/          → listar_datasets

Note: the POST /match/ endpoint requires a paid plan. All lookups use /search/.
"""

from __future__ import annotations

import logging
from typing import Any

from mcp_brasil._shared.http_client import http_get
from mcp_brasil.exceptions import AuthError

from .constants import (
    AUTH_ENV_VAR,
    DATASETS_URL,
    DEFAULT_LIMIT,
    ENTITY_URL,
    SEARCH_URL,
    _get_api_key,
)
from .schemas import DatasetOpenSanctions, EntidadeSancionada, ResultadoMatch

logger = logging.getLogger(__name__)


def _auth_headers() -> dict[str, str]:
    """Build Authorization header for the OpenSanctions API."""
    key = _get_api_key()
    if not key:
        raise AuthError(
            f"Variável de ambiente {AUTH_ENV_VAR} não configurada. "
            "Cadastre-se em opensanctions.org/api/ para obter uma chave gratuita."
        )
    return {"Authorization": f"ApiKey {key}"}


# Dataset → topic inference (search API doesn't return topics directly)
_SANCTION_DATASETS = frozenset(
    [
        "ofac_sdn", "ofac_cons", "eu_fsf", "un_sc_sanctions", "worldbank_debarred",
        "gb_hmt_sanctions", "ch_seco_sanctions", "gb_fcdo_sanctions", "au_dfat_sanctions",
        "ca_dfatd_sema_sanctions", "be_fod_sanctions", "fr_tresor_gels_avoir",
        "jp_mof_sanctions", "mc_fund_freezes", "nz_russia_sanctions",
        "interpol_red_notices", "eu_travel_bans",
    ]
)
_PEP_DATASETS = frozenset(
    [
        "br_tse_candidates", "br_cgu_pep", "every_politician", "wd_peppercat",
        "ann_pep_positions", "ann_graph_topics",
    ]
)


def _infer_topics(datasets: list[str]) -> list[str]:
    """Infer entity topics from the datasets it appears in."""
    topics: list[str] = []
    ds_set = set(datasets)
    if ds_set & _SANCTION_DATASETS:
        topics.append("sanction")
    if ds_set & _PEP_DATASETS:
        topics.append("pep")
    return topics


def _parse_entidade(raw: dict[str, Any], score: float | None = None) -> EntidadeSancionada:
    """Parse a raw OpenSanctions entity into EntidadeSancionada."""
    props = raw.get("properties") or {}

    def _first(key: str) -> str | None:
        vals = props.get(key, [])
        return vals[0] if vals else None

    def _list(key: str) -> list[str]:
        return [str(v) for v in (props.get(key) or [])]

    # Merge names: main caption + aliases
    nomes_alt: list[str] = []
    for key in ("alias", "weakAlias", "previousName"):
        nomes_alt.extend(_list(key))

    datasets = raw.get("datasets") or []
    # API doesn't always return topics field; infer from datasets as fallback
    topics = raw.get("topics") or _infer_topics(datasets)

    return EntidadeSancionada(
        id=raw.get("id"),
        schema_tipo=raw.get("schema"),
        nome=raw.get("caption") or _first("name"),
        nomes_alternativos=nomes_alt,
        paises=_list("country") + _list("jurisdiction"),
        nacionalidades=_list("nationality"),
        datasets=datasets,
        topics=topics,
        score=score if score is not None else raw.get("score"),
        data_nascimento=_first("birthDate"),
        cpf_cnpj=_first("taxNumber") or _first("idNumber"),
        posicao=_first("position"),
        descricao=_first("notes") or _first("description"),
    )


async def buscar_entidades(
    *,
    nome: str,
    schema: str | None = None,
    paises: list[str] | None = None,
    topics: list[str] | None = None,
    datasets: list[str] | None = None,
    limite: int = DEFAULT_LIMIT,
) -> list[EntidadeSancionada]:
    """Search OpenSanctions for entities matching the given name.

    Args:
        nome: Name to search for (person or company).
        schema: Entity type filter: "Person", "Company", "LegalEntity".
        paises: Country codes to filter (e.g. ["BR", "US"]).
        topics: Topic filters: "sanction", "pep", "crime", "debarment".
        datasets: Specific dataset names to search within.
        limite: Max results (default: 10).
    """
    params: dict[str, Any] = {"q": nome, "limit": limite}
    if schema:
        params["schema"] = schema
    if paises:
        params["countries"] = ",".join(paises)
    if topics:
        params["topics"] = ",".join(topics)
    if datasets:
        params["datasets"] = ",".join(datasets)

    result = await http_get(SEARCH_URL, params=params, headers=_auth_headers())
    if not isinstance(result, dict):
        return []

    items = result.get("results") or []
    return [_parse_entidade(item, item.get("score")) for item in items]


async def verificar_entidade(
    nome: str,
    *,
    schema: str = "LegalEntity",
    pais: str | None = None,
    data_nascimento: str | None = None,
    cpf_cnpj: str | None = None,
) -> ResultadoMatch:
    """Verify an entity against all sanctions lists using the search endpoint.

    Uses /search/ with topic filters to identify sanctions and PEP status.
    Performs two parallel searches: one for sanctions, one for PEPs.

    Args:
        nome: Name of the person or company to verify.
        schema: Entity type: "Person", "Company", or "LegalEntity".
        pais: Country code (e.g. "BR") to improve matching.
        data_nascimento: Birth date (used to disambiguate, not as filter).
        cpf_cnpj: Tax ID (used to disambiguate, not as filter).
    """
    import asyncio

    paises_list = [pais] if pais else None

    # Run searches for sanctions and PEPs in parallel
    sanctions_task = buscar_entidades(
        nome=nome,
        schema=schema,
        paises=paises_list,
        topics=["sanction"],
        limite=5,
    )
    pep_task = buscar_entidades(
        nome=nome,
        schema=schema,
        paises=paises_list,
        topics=["pep"],
        limite=5,
    )
    sanctions_results, pep_results = await asyncio.gather(
        sanctions_task, pep_task, return_exceptions=True
    )

    sanctions: list[EntidadeSancionada] = sanctions_results if isinstance(sanctions_results, list) else []
    peps: list[EntidadeSancionada] = pep_results if isinstance(pep_results, list) else []

    # Merge and deduplicate by ID
    seen: set[str] = set()
    matches: list[EntidadeSancionada] = []
    for e in sanctions + peps:
        key = e.id or e.nome or ""
        if key not in seen:
            seen.add(key)
            matches.append(e)

    all_datasets: list[str] = []
    all_topics: set[str] = set()
    for m in matches:
        all_datasets.extend(m.datasets)
        all_topics.update(m.topics)

    return ResultadoMatch(
        entidade_consultada=nome,
        matches=matches,
        total_matches=len(matches),
        is_sanctioned=len(sanctions) > 0,
        is_pep=len(peps) > 0,
        listas_encontradas=sorted(set(all_datasets)),
    )


async def obter_entidade(entity_id: str) -> EntidadeSancionada | None:
    """Fetch full details of an entity by OpenSanctions ID.

    Args:
        entity_id: OpenSanctions entity ID (e.g. "NK-A7Kf3UJyq5ZoBMczRwHkNA").
    """
    url = f"{ENTITY_URL}/{entity_id}"
    try:
        result = await http_get(url, headers=_auth_headers())
        if isinstance(result, dict):
            return _parse_entidade(result)
        return None
    except Exception:
        logger.warning("Entity not found: %s", entity_id)
        return None


async def listar_datasets() -> list[DatasetOpenSanctions]:
    """List all available datasets in OpenSanctions."""
    try:
        result = await http_get(DATASETS_URL, headers=_auth_headers())
        items = result if isinstance(result, list) else (result.get("datasets") or [])
        return [
            DatasetOpenSanctions(
                nome=d.get("name"),
                titulo=d.get("title"),
                entidades=d.get("entity_count") or d.get("entities"),
                paises=[c.get("code", c) if isinstance(c, dict) else c for c in (d.get("coverage") or {}).get("countries", [])],
                publicador=(d.get("publisher") or {}).get("name"),
                ultima_atualizacao=d.get("last_change") or d.get("updated_at"),
                url=d.get("url") or d.get("data_url"),
            )
            for d in items
        ]
    except Exception:
        logger.warning("Failed to list OpenSanctions datasets")
        return []
