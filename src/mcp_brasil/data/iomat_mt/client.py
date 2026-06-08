"""HTTP client for the IOMAT-MT API.

Endpoints:
    - /buscas                                  → buscar_publicacoes
    - /diarios                                 → listar_diarios
    - /diarios/{id}/edicoes                    → listar_edicoes
    - /diarios/{id}/edicoes/{id}/materias      → listar_materias
    - /clientes                                → listar_clientes
    - /classificacoes                          → listar_classificacoes
"""

from __future__ import annotations

from typing import Any

from mcp_brasil._shared.http_client import http_get

from .constants import (
    BUSCAS_URL,
    CLASSIFICACOES_URL,
    CLIENTES_URL,
    DEFAULT_LIMITE,
    DIARIOS_URL,
)
from .schemas import (
    Classificacao,
    Cliente,
    Diario,
    Edicao,
    Materia,
    ResultadoBusca,
)


async def buscar_publicacoes(
    *,
    termo: str,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    pagina: int = 0,
    limite: int = DEFAULT_LIMITE,
) -> ResultadoBusca:
    """Busca publicações no Diário Oficial MT por termo livre."""
    params: dict[str, Any] = {"termo": termo, "pagina": pagina, "limite": limite}
    if data_inicio:
        params["data-inicio"] = data_inicio
    if data_fim:
        params["data-fim"] = data_fim
    data: dict[str, Any] = await http_get(BUSCAS_URL, params=params)
    from .schemas import ItemBusca
    resultados = [ItemBusca(**r) for r in data.get("resultados", [])]
    return ResultadoBusca(
        total=data.get("total", 0),
        pagina=data.get("pagina", 0),
        resultados=resultados,
    )


async def listar_diarios() -> list[Diario]:
    """Lista os diários disponíveis (Diário Oficial, Diário da Justiça, etc.)."""
    data: list[dict[str, Any]] = await http_get(DIARIOS_URL)
    return [Diario(**d) for d in data]


async def listar_edicoes(
    *,
    diario_id: int,
    data: str | None = None,
    pagina: int = 0,
    limite: int = DEFAULT_LIMITE,
) -> list[Edicao]:
    """Lista edições de um diário, opcionalmente filtradas por data (YYYY-MM-DD)."""
    url = f"{DIARIOS_URL}/{diario_id}/edicoes"
    params: dict[str, Any] = {"pagina": pagina, "limite": limite}
    if data:
        params["data"] = data
    result: list[dict[str, Any]] | dict[str, Any] = await http_get(url, params=params)
    items = result if isinstance(result, list) else result.get("data", [])
    return [Edicao(**e) for e in items]


async def listar_materias(
    *,
    diario_id: int,
    edicao_id: int,
    cliente_id: int | None = None,
) -> list[Materia]:
    """Lista matérias/artigos de uma edição específica."""
    url = f"{DIARIOS_URL}/{diario_id}/edicoes/{edicao_id}/materias"
    params: dict[str, Any] = {}
    if cliente_id:
        params["cliente_id"] = cliente_id
    result: list[dict[str, Any]] | dict[str, Any] = await http_get(url, params=params)
    items = result if isinstance(result, list) else result.get("data", [])
    return [Materia(**m) for m in items]


async def listar_clientes(
    *,
    tipo_pessoa: str | None = None,
    classificacao_id: int | None = None,
) -> list[Cliente]:
    """Lista órgãos e entidades que publicam no Diário Oficial MT."""
    params: dict[str, Any] = {}
    if tipo_pessoa:
        params["tipo_pessoa"] = tipo_pessoa
    if classificacao_id:
        params["classificacao_id"] = classificacao_id
    data: list[dict[str, Any]] = await http_get(CLIENTES_URL, params=params)
    return [Cliente(**c) for c in data]


async def listar_classificacoes() -> list[Classificacao]:
    """Lista as classificações de órgãos publicantes."""
    data: list[dict[str, Any]] = await http_get(CLASSIFICACOES_URL)
    return [Classificacao(**c) for c in data]
