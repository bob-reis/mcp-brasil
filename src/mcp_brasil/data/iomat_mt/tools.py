"""Tool functions for the IOMAT-MT feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

import re

from fastmcp import Context

from . import client
from .constants import DIARIO_OFICIAL_ID, DIARIOS_NOMES

_HTML_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(text: str) -> str:
    return _HTML_TAG_RE.sub("", text).strip()


async def buscar_publicacoes_mt(
    ctx: Context,
    termo: str,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    pagina: int = 0,
    limite: int = 20,
) -> str:
    """Busca publicações no Diário Oficial do Estado de Mato Grosso por termo livre.

    Realiza busca full-text nas publicações do Diário Oficial e do Diário da Justiça
    do Estado de Mato Grosso. Útil para encontrar licitações, contratos, nomeações,
    portarias, exonerações, sanções e quaisquer atos administrativos estaduais.

    Args:
        ctx: Contexto MCP.
        termo: Termo de busca (nome de empresa, CNPJ, pessoa, modalidade de licitação, etc.).
        data_inicio: Data inicial no formato YYYY-MM-DD (ex: "2024-01-01").
        data_fim: Data final no formato YYYY-MM-DD (ex: "2024-12-31").
        pagina: Página de resultados para paginação (padrão 0).
        limite: Quantidade de resultados por página (padrão 20, máximo 100).

    Returns:
        Lista de publicações com trechos destacados, data e número de edição.
    """
    await ctx.info(f"Buscando '{termo}' no Diário Oficial MT...")
    resultado = await client.buscar_publicacoes(
        termo=termo,
        data_inicio=data_inicio,
        data_fim=data_fim,
        pagina=pagina,
        limite=limite,
    )

    if not resultado.resultados:
        return f"Nenhuma publicação encontrada para '{termo}' no Diário Oficial MT."

    lines: list[str] = [
        f"**{resultado.total} publicações encontradas** para '{termo}' no Diário Oficial MT.\n"
    ]

    for i, item in enumerate(resultado.resultados, 1):
        diario_nome = item.diario or "Diário Oficial"
        lines.append(f"### {i}. {diario_nome} — Edição {item.edicao_numero or '?'}")
        lines.append(f"**Data:** {item.data or '—'} | **Pág:** {item.pagina or '—'}")
        if item.suplemento:
            lines.append(f"**Suplemento:** {item.suplemento}")
        if item.highlight:
            trecho = _strip_html(item.highlight)[:600]
            lines.append(f"\n> {trecho}")
        if item.protocolo:
            lines.append(
                f"\n[Ver edição completa](https://iomat.mt.gov.br/apifront/portal/edicoes/pdf_diario/{item.protocolo}/1)"
            )
        lines.append("")

    if resultado.total > limite:
        prox = pagina + 1
        lines.append(
            f"*Mostrando {limite} de {resultado.total}. "
            f"Use `pagina={prox}` para os próximos resultados.*"
        )

    return "\n".join(lines)


async def listar_edicoes_mt(
    ctx: Context,
    diario_id: int = DIARIO_OFICIAL_ID,
    data: str | None = None,
    pagina: int = 0,
    limite: int = 10,
) -> str:
    """Lista edições do Diário Oficial ou Diário da Justiça de Mato Grosso.

    Retorna as edições publicadas, com data, número e quantidade de páginas.
    Diário Oficial (id=1) cobre atos do Executivo estadual, prefeituras e câmaras.
    Diário da Justiça (id=5) cobre atos do Poder Judiciário.

    Args:
        ctx: Contexto MCP.
        diario_id: ID do diário (1=Diário Oficial, 5=Diário da Justiça).
        data: Data específica no formato YYYY-MM-DD para filtrar edição do dia.
        pagina: Página de resultados (padrão 0).
        limite: Quantidade de edições (padrão 10).

    Returns:
        Lista de edições com data, número e número de páginas.
    """
    nome = DIARIOS_NOMES.get(diario_id, f"Diário {diario_id}")
    await ctx.info(f"Listando edições do {nome} MT...")
    edicoes = await client.listar_edicoes(
        diario_id=diario_id, data=data, pagina=pagina, limite=limite
    )

    if not edicoes:
        return f"Nenhuma edição encontrada para o {nome}."

    lines: list[str] = [f"**{nome} — Mato Grosso**\n"]
    for ed in edicoes:
        lines.append(f"### Edição {ed.numero or ed.id} — {ed.data or '—'}")
        if ed.titulo:
            lines.append(f"*{ed.titulo}*")
        if ed.numpag:
            lines.append(f"**Páginas:** {ed.numpag}")
        if ed.suplemento:
            lines.append(f"**Suplemento:** {ed.suplemento}")
        lines.append(f"**ID interno:** {ed.id}")
        lines.append("")

    return "\n".join(lines)


async def buscar_materias_mt(
    ctx: Context,
    diario_id: int,
    edicao_id: int,
    cliente_id: int | None = None,
) -> str:
    """Lista matérias e artigos de uma edição específica do Diário Oficial MT.

    Retorna os itens publicados em uma edição, organizados por órgão publicante.
    Use junto com `listar_edicoes_mt` para obter o `edicao_id`.

    Args:
        ctx: Contexto MCP.
        diario_id: ID do diário (1=Diário Oficial, 5=Diário da Justiça).
        edicao_id: ID interno da edição (obtido via `listar_edicoes_mt`).
        cliente_id: Filtrar por órgão publicante (opcional, obtido via `listar_orgaos_mt`).

    Returns:
        Lista de matérias com título, órgão e número de página.
    """
    nome = DIARIOS_NOMES.get(diario_id, f"Diário {diario_id}")
    await ctx.info(f"Buscando matérias da edição {edicao_id} do {nome} MT...")
    materias = await client.listar_materias(
        diario_id=diario_id, edicao_id=edicao_id, cliente_id=cliente_id
    )

    if not materias:
        return f"Nenhuma matéria encontrada na edição {edicao_id} do {nome}."

    lines: list[str] = [f"**{nome} — Edição {edicao_id} — {len(materias)} matérias**\n"]
    for m in materias[:50]:
        titulo = m.titulo or m.subtitulo or "Sem título"
        orgao = m.orgao or "—"
        pagina = f"pág. {m.pagina}" if m.pagina else ""
        lines.append(f"- **{titulo}** | {orgao} {pagina}".strip(" |"))

    if len(materias) > 50:
        restantes = len(materias) - 50
        lines.append(f"\n*... e mais {restantes} matérias. Use `cliente_id` para filtrar.*")

    return "\n".join(lines)


async def listar_orgaos_mt(
    ctx: Context,
    classificacao_id: int | None = None,
) -> str:
    """Lista órgãos e entidades que publicam no Diário Oficial de Mato Grosso.

    Retorna secretarias estaduais, prefeituras, câmaras municipais, fundos,
    autarquias e demais entidades publicantes, com seus IDs para uso em filtros.

    Args:
        ctx: Contexto MCP.
        classificacao_id: Filtrar por tipo de órgão:
            1=Secretarias Estaduais, 3=Câmaras Municipais,
            8=Prefeituras, 7=Poderes Independentes.

    Returns:
        Lista de órgãos com ID, nome e classificação.
    """
    await ctx.info("Listando órgãos publicantes do Diário Oficial MT...")
    clientes = await client.listar_clientes(classificacao_id=classificacao_id)

    if not clientes:
        return "Nenhum órgão encontrado."

    lines: list[str] = [f"**{len(clientes)} órgãos publicantes no DO-MT**\n"]
    for c in clientes[:100]:
        nome = c.nome or c.nome_fantasia or "—"
        sigla = f" ({c.sigla})" if c.sigla and c.sigla.strip() else ""
        classificacao = f" — {c.classificacao}" if c.classificacao else ""
        lines.append(f"- **ID {c.cliente_id}:** {nome}{sigla}{classificacao}")

    if len(clientes) > 100:
        restantes = len(clientes) - 100
        lines.append(f"\n*... e mais {restantes} órgãos. Use `classificacao_id` para filtrar.*")

    return "\n".join(lines)


async def listar_classificacoes_mt(ctx: Context) -> str:
    """Lista as categorias de órgãos publicantes do Diário Oficial de Mato Grosso.

    Retorna os tipos de entidades com seus IDs, úteis para filtrar `listar_orgaos_mt`.

    Args:
        ctx: Contexto MCP.

    Returns:
        Lista de classificações com ID e descrição.
    """
    await ctx.info("Listando classificações de órgãos do DO-MT...")
    classificacoes = await client.listar_classificacoes()

    if not classificacoes:
        return "Nenhuma classificação encontrada."

    lines: list[str] = ["**Classificações de órgãos — Diário Oficial MT**\n"]
    for c in classificacoes:
        lines.append(f"- **ID {c.id}:** {c.nome}")

    return "\n".join(lines)
