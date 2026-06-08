"""Tool functions for the DadosAbertos-MT feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import markdown_table

from . import client


async def buscar_datasets_mt(
    ctx: Context,
    query: str = "",
    organizacao: str | None = None,
    tag: str | None = None,
    inicio: int = 0,
    limite: int = 20,
) -> str:
    """Busca datasets no Portal de Dados Abertos de Mato Grosso.

    Pesquisa no catálogo CKAN do governo estadual de MT com datasets de
    saúde, educação, segurança pública, meio ambiente, economia e outros temas.

    Args:
        ctx: Contexto MCP.
        query: Termo de busca livre (ex: "servidores", "despesas", "veículos").
        organizacao: Filtrar por slug da organização (ex: "seplag", "sesp-mt").
        tag: Filtrar por tag (ex: "saude", "educacao").
        inicio: Offset para paginação (padrão 0).
        limite: Quantidade de resultados (padrão 20, máximo 100).

    Returns:
        Lista de datasets com título, organização, recursos e tags.
    """
    await ctx.info(f"Buscando datasets MT: '{query or '*'}'...")
    resultado = await client.buscar_datasets(
        query=query,
        organizacao=organizacao,
        tag=tag,
        rows=limite,
        start=inicio,
    )

    if not resultado.datasets:
        termo = query or "todos"
        return f"Nenhum dataset encontrado para '{termo}' no Portal de Dados Abertos MT."

    lines: list[str] = [
        f"**{resultado.total} datasets** encontrados no Portal Dados Abertos MT.\n"
    ]

    for i, ds in enumerate(resultado.datasets, 1):
        org = ds.organization_title or ds.organization_name or "—"
        tags = ", ".join(ds.tags[:5]) if ds.tags else "—"
        grupos = ", ".join(ds.groups[:3]) if ds.groups else "—"
        titulo = ds.title or ds.name or "Sem título"
        lines.append(f"### {i}. {titulo}")
        lines.append(f"**ID/Slug:** `{ds.name or ds.id}`")
        lines.append(f"**Organização:** {org}")
        lines.append(f"**Recursos:** {ds.num_resources} arquivo(s)")
        if tags != "—":
            lines.append(f"**Tags:** {tags}")
        if grupos != "—":
            lines.append(f"**Grupos:** {grupos}")
        if ds.metadata_modified:
            lines.append(f"**Atualizado:** {ds.metadata_modified[:10]}")
        lines.append("")

    if resultado.total > inicio + limite:
        prox = inicio + limite
        lines.append(
            f"*Mostrando {limite} de {resultado.total}. "
            f"Use `inicio={prox}` para os próximos resultados.*"
        )

    return "\n".join(lines)


async def detalhar_dataset_mt(ctx: Context, dataset_id: str) -> str:
    """Obtém detalhes completos de um dataset do Portal de Dados Abertos MT.

    Retorna descrição, organização, lista de recursos com links de download.
    Use `buscar_datasets_mt` para encontrar o ID/slug do dataset.

    Args:
        ctx: Contexto MCP.
        dataset_id: ID ou slug do dataset (ex: "servidores-ativos-mt").

    Returns:
        Detalhes do dataset com todos os recursos e links de download.
    """
    await ctx.info(f"Detalhando dataset '{dataset_id}'...")
    ds = await client.detalhar_dataset(dataset_id)

    if not ds:
        return f"Dataset '{dataset_id}' não encontrado no Portal Dados Abertos MT."

    org = ds.organization_title or ds.organization_name or "—"
    notas = (ds.notes or "Sem descrição")[:600]
    tags = ", ".join(ds.tags) if ds.tags else "—"
    grupos = ", ".join(ds.groups) if ds.groups else "—"

    lines: list[str] = [
        f"## {ds.title or ds.name}",
        f"\n{notas}",
        f"\n**Organização:** {org}",
        f"**Tags:** {tags}",
        f"**Grupos:** {grupos}",
        f"**Criado:** {(ds.metadata_created or '—')[:10]}",
        f"**Atualizado:** {(ds.metadata_modified or '—')[:10]}",
        f"\n### Recursos ({ds.num_resources})\n",
    ]

    if ds.resources:
        for r in ds.resources:
            nome = r.name or "Sem nome"
            fmt = r.format or "—"
            desc = f" — {r.description[:100]}" if r.description else ""
            lines.append(f"- **[{fmt}]** {nome}{desc}")
            if r.url:
                lines.append(f"  [Download]({r.url})")
    else:
        lines.append("_Nenhum recurso disponível._")

    return "\n".join(lines)


async def listar_organizacoes_mt(ctx: Context) -> str:
    """Lista organizações publicadoras no Portal de Dados Abertos de Mato Grosso.

    Retorna secretarias estaduais, prefeituras, tribunais e demais órgãos
    com seus slugs para uso como filtro em `buscar_datasets_mt`.

    Args:
        ctx: Contexto MCP.

    Returns:
        Tabela de organizações com nome e quantidade de datasets.
    """
    await ctx.info("Listando organizações do Portal Dados Abertos MT...")
    orgs = await client.listar_organizacoes()

    if not orgs:
        return "Nenhuma organização encontrada no Portal Dados Abertos MT."

    orgs_sorted = sorted(orgs, key=lambda o: o.package_count, reverse=True)
    rows = [
        (o.title or o.name or "—", o.name or "—", str(o.package_count))
        for o in orgs_sorted
    ]
    header = f"**{len(orgs)} organizações** no Portal Dados Abertos MT:\n\n"
    table = markdown_table(["Organização", "Slug (usar em filtro)", "Datasets"], rows)
    return header + table


async def listar_grupos_mt(ctx: Context) -> str:
    """Lista os grupos temáticos do Portal de Dados Abertos de Mato Grosso.

    Grupos organizam os datasets por tema (saúde, educação, segurança, etc.).
    Use o slug do grupo como filtro em `buscar_datasets_mt`.

    Args:
        ctx: Contexto MCP.

    Returns:
        Lista de grupos temáticos com quantidade de datasets.
    """
    await ctx.info("Listando grupos temáticos do Portal Dados Abertos MT...")
    grupos = await client.listar_grupos()

    if not grupos:
        return "Nenhum grupo temático encontrado no Portal Dados Abertos MT."

    grupos_sorted = sorted(grupos, key=lambda g: g.package_count, reverse=True)
    rows = [
        (g.title or g.name or "—", g.name or "—", str(g.package_count))
        for g in grupos_sorted
    ]
    header = f"**{len(grupos)} grupos temáticos** no Portal Dados Abertos MT:\n\n"
    return header + markdown_table(["Tema", "Slug", "Datasets"], rows)


async def listar_tags_mt(ctx: Context, busca: str | None = None) -> str:
    """Lista as tags disponíveis no Portal de Dados Abertos de Mato Grosso.

    Tags descrevem o conteúdo dos datasets e podem ser usadas como filtro
    em `buscar_datasets_mt`.

    Args:
        ctx: Contexto MCP.
        busca: Filtrar tags por prefixo ou termo (opcional).

    Returns:
        Lista de tags disponíveis.
    """
    await ctx.info("Listando tags do Portal Dados Abertos MT...")
    tags = await client.listar_tags(query=busca)

    if not tags:
        return "Nenhuma tag encontrada."

    linhas = [f"**{len(tags)} tags** disponíveis:\n"]
    linhas.append(", ".join(f"`{t}`" for t in sorted(tags)))
    return "\n".join(linhas)
