"""Tool functions for the IBAMA feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from mcp_brasil._shared.formatting import format_brl, markdown_table
from mcp_brasil.exceptions import HttpClientError

from . import client
from .constants import DEFAULT_LIMIT


def _pagination_hint(count: int, pagina: int) -> str:
    if count >= DEFAULT_LIMIT:
        return f"\n\n> Use `pagina={pagina + 1}` para ver mais resultados."
    if pagina > 1 and count < DEFAULT_LIMIT:
        return "\n\n> Última página de resultados."
    return ""


async def buscar_embargos_ibama(
    cpf_cnpj: str | None = None,
    uf: str | None = None,
    bioma: str | None = None,
    pagina: int = 1,
) -> str:
    """Busca áreas embargadas pelo IBAMA por CPF/CNPJ, estado ou bioma.

    O embargo ambiental impede qualquer atividade econômica na área até que
    os danos ambientais sejam reparados. São mais de 79 mil áreas cadastradas.

    Args:
        cpf_cnpj: CPF ou CNPJ do proprietário/responsável pela área embargada.
        uf: Sigla do estado (ex: "PA", "MT", "AM").
        bioma: Bioma (Amazônia, Cerrado, Caatinga, Mata Atlântica, Pampa, Pantanal).
        pagina: Página de resultados (padrão: 1).

    Returns:
        Tabela com áreas embargadas encontradas.
    """
    try:
        embargos = await client.buscar_embargos(
            cpf_cnpj=cpf_cnpj, uf=uf, bioma=bioma, pagina=pagina
        )
    except HttpClientError as exc:
        return f"Erro ao consultar embargos IBAMA: {exc}"

    if not embargos:
        filtro = cpf_cnpj or uf or bioma or "filtros informados"
        return f"Nenhuma área embargada encontrada para '{filtro}'."

    rows = [
        (
            e.numero_auto or "—",
            (e.nome_embargado or "—")[:40],
            e.cpf_cnpj or "—",
            e.municipio or "—",
            e.uf or "—",
            e.bioma or "—",
            f"{e.area_ha:.2f} ha" if e.area_ha else "—",
            e.data_embargo or "—",
        )
        for e in embargos
    ]
    header = "Áreas embargadas IBAMA:\n\n"
    table = header + markdown_table(
        ["Auto", "Embargado", "CPF/CNPJ", "Município", "UF", "Bioma", "Área", "Data"], rows
    )
    return table + _pagination_hint(len(embargos), pagina)


async def buscar_autos_infracao_ibama(
    cpf_cnpj: str | None = None,
    uf: str | None = None,
    pagina: int = 1,
) -> str:
    """Busca autos de infração ambiental emitidos pelo IBAMA.

    Autos de infração são punições por crimes ambientais como desmatamento
    ilegal, pesca predatória, tráfico de animais silvestres e poluição.

    Args:
        cpf_cnpj: CPF ou CNPJ do autuado.
        uf: Sigla do estado (ex: "PA", "MT").
        pagina: Página de resultados (padrão: 1).

    Returns:
        Tabela com autos de infração encontrados.
    """
    try:
        autos = await client.buscar_autos_infracao(
            cpf_cnpj=cpf_cnpj, uf=uf, pagina=pagina
        )
    except HttpClientError as exc:
        return f"Erro ao consultar autos de infração IBAMA: {exc}"

    if not autos:
        filtro = cpf_cnpj or uf or "filtros informados"
        return f"Nenhum auto de infração encontrado para '{filtro}'."

    rows = [
        (
            a.numero_auto or "—",
            (a.nome_autuado or "—")[:40],
            a.cpf_cnpj or "—",
            a.municipio or "—",
            a.uf or "—",
            (a.tipo_infracao or "—")[:50],
            format_brl(a.valor_multa) if a.valor_multa else "—",
            a.data_infracao or "—",
        )
        for a in autos
    ]
    header = "Autos de infração IBAMA:\n\n"
    table = header + markdown_table(
        ["Auto", "Autuado", "CPF/CNPJ", "Município", "UF", "Infração", "Multa", "Data"], rows
    )
    return table + _pagination_hint(len(autos), pagina)


async def listar_dados_abertos_ibama() -> str:
    """Lista datasets disponíveis no portal de dados abertos do IBAMA.

    Retorna os conjuntos de dados ambientais públicos disponíveis para consulta,
    incluindo IDs de recursos úteis para consultas avançadas.

    Returns:
        Lista de datasets com nome, descrição, formato e resource ID.
    """
    try:
        datasets = await client.listar_datasets()
    except HttpClientError as exc:
        return f"Erro ao listar datasets IBAMA: {exc}"

    if not datasets:
        return "Nenhum dataset disponível no portal IBAMA no momento."

    rows = [
        (
            d.titulo or d.nome or "—",
            (d.descricao or "—")[:80],
            d.formato or "—",
            d.resource_id or "—",
        )
        for d in datasets[:30]
    ]
    return "Datasets IBAMA disponíveis:\n\n" + markdown_table(
        ["Título", "Descrição", "Formato", "Resource ID"], rows
    )
