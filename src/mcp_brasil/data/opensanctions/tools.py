"""Tool functions for the OpenSanctions feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from mcp_brasil._shared.formatting import markdown_table, truncate_list
from mcp_brasil.exceptions import HttpClientError

from . import client
from .constants import DATASETS_PEPS, DATASETS_SANCOES, DEFAULT_LIMIT, SCHEMA_TYPES, TOPICS


def _format_topics(topics: list[str]) -> str:
    """Format topics into human-readable labels."""
    labels = [TOPICS.get(t, t) for t in topics]
    return ", ".join(labels) if labels else "—"


def _format_datasets(datasets: list[str]) -> str:
    """Format dataset list, with known names translated."""
    all_known = {**DATASETS_SANCOES, **DATASETS_PEPS}
    named = [all_known.get(d, d) for d in datasets]
    return truncate_list(named, max_items=5) if named else "—"


async def buscar_sancoes_internacionais(
    nome: str,
    schema: str | None = None,
    paises: str | None = None,
    limite: int = DEFAULT_LIMIT,
) -> str:
    """Busca entidades em listas de sanções internacionais (OFAC, ONU, UE, etc.).

    Verifica se uma pessoa física ou empresa aparece em listas de sanções
    internacionais como OFAC SDN (EUA), sanções da ONU, União Europeia,
    Banco Mundial, Interpol e mais de 400 outras fontes globais.

    Args:
        nome: Nome da pessoa ou empresa a buscar.
        schema: Tipo de entidade: "Person" (pessoa), "Company" (empresa) ou
                "LegalEntity" (qualquer — padrão).
        paises: Códigos de países separados por vírgula para filtrar (ex: "BR,US,RU").
        limite: Número máximo de resultados (padrão: 10, máx: 50).

    Returns:
        Tabela com entidades encontradas e as listas em que aparecem.
    """
    paises_list = [p.strip().upper() for p in paises.split(",")] if paises else None
    limite = min(limite, 50)

    try:
        entidades = await client.buscar_entidades(
            nome=nome,
            schema=schema,
            paises=paises_list,
            limite=limite,
        )
    except HttpClientError as exc:
        return f"Erro ao consultar OpenSanctions: {exc}"

    if not entidades:
        return f"Nenhuma entidade encontrada para '{nome}' nas listas de sanções."

    rows = [
        (
            (e.nome or "—")[:50],
            SCHEMA_TYPES.get(e.schema_tipo or "", e.schema_tipo or "—"),
            ", ".join(e.paises[:3]) if e.paises else "—",
            _format_topics(e.topics),
            _format_datasets(e.datasets[:4]),
            f"{e.score:.0%}" if e.score else "—",
        )
        for e in entidades
    ]
    header = f"Resultados para '{nome}' ({len(entidades)} encontrados):\n\n"
    return header + markdown_table(
        ["Nome", "Tipo", "Países", "Categorias", "Listas", "Score"], rows
    )


async def verificar_compliance(
    nome: str,
    schema: str = "LegalEntity",
    pais: str | None = None,
    data_nascimento: str | None = None,
    cpf_cnpj: str | None = None,
) -> str:
    """Verifica compliance de pessoa ou empresa contra todas as listas de sanções.

    Usa matching fuzzy para encontrar correspondências mesmo com variações de
    nome. Retorna um parecer claro sobre se a entidade está sancionada ou
    é uma PEP (Pessoa Politicamente Exposta).

    Args:
        nome: Nome completo da pessoa ou razão social da empresa.
        schema: "Person" para pessoa física, "Company" para empresa,
                "LegalEntity" para ambos (padrão).
        pais: Código do país (ex: "BR") para melhorar a precisão.
        data_nascimento: Data de nascimento no formato YYYY-MM-DD (para pessoas).
        cpf_cnpj: CPF ou CNPJ para melhorar a precisão do matching.

    Returns:
        Parecer de compliance com matches encontrados e classificação de risco.
    """
    try:
        resultado = await client.verificar_entidade(
            nome=nome,
            schema=schema,
            pais=pais.upper() if pais else None,
            data_nascimento=data_nascimento,
            cpf_cnpj=cpf_cnpj,
        )
    except HttpClientError as exc:
        return f"Erro ao verificar compliance: {exc}"

    # Risk classification
    if resultado.is_sanctioned:
        status = "🔴 SANCIONADO — entidade aparece em listas de sanções internacionais"
        risco = "ALTO"
    elif resultado.is_pep:
        status = "🟡 PEP — Pessoa Politicamente Exposta identificada"
        risco = "MÉDIO"
    elif resultado.total_matches > 0:
        status = "🟠 ATENÇÃO — possíveis correspondências encontradas, revisar manualmente"
        risco = "MÉDIO"
    else:
        status = "🟢 SEM OCORRÊNCIAS — não encontrado nas listas consultadas"
        risco = "BAIXO"

    lines = [
        f"## Verificação de Compliance: {nome}",
        f"",
        f"**Status:** {status}",
        f"**Nível de risco:** {risco}",
        f"**Matches encontrados:** {resultado.total_matches}",
    ]

    if resultado.listas_encontradas:
        all_known = {**DATASETS_SANCOES, **DATASETS_PEPS}
        listas = [all_known.get(d, d) for d in resultado.listas_encontradas]
        lines.append(f"**Listas com ocorrências:** {', '.join(listas)}")

    if resultado.matches:
        lines.append("")
        lines.append("### Matches encontrados")
        for m in resultado.matches[:5]:
            score_str = f" (score: {m.score:.0%})" if m.score else ""
            lines.append(f"- **{m.nome}**{score_str} — {_format_topics(m.topics)}")
            if m.paises:
                lines.append(f"  Países: {', '.join(m.paises[:3])}")
            if m.posicao:
                lines.append(f"  Cargo/Posição: {m.posicao}")
            if m.data_nascimento:
                lines.append(f"  Nascimento: {m.data_nascimento}")
            if m.id:
                lines.append(f"  ID OpenSanctions: `{m.id}`")

    return "\n".join(lines)


async def detalhar_entidade_sancao(entity_id: str) -> str:
    """Obtém detalhes completos de uma entidade pelo ID OpenSanctions.

    Use este tool com o ID retornado por buscar_sancoes_internacionais ou
    verificar_compliance para obter informações detalhadas da entidade.

    Args:
        entity_id: ID da entidade no OpenSanctions (ex: "NK-A7Kf3UJyq5ZoBMczRwHkNA").

    Returns:
        Detalhes completos da entidade: nomes, países, datas, posições e listas.
    """
    try:
        entidade = await client.obter_entidade(entity_id)
    except HttpClientError as exc:
        return f"Erro ao obter entidade: {exc}"

    if not entidade:
        return f"Entidade '{entity_id}' não encontrada no OpenSanctions."

    lines = [
        f"## {entidade.nome or 'Entidade sem nome'}",
        f"",
        f"**ID:** `{entidade.id}`",
        f"**Tipo:** {SCHEMA_TYPES.get(entidade.schema_tipo or '', entidade.schema_tipo or '—')}",
        f"**Categorias:** {_format_topics(entidade.topics)}",
    ]

    if entidade.paises:
        lines.append(f"**Países:** {', '.join(entidade.paises)}")
    if entidade.nacionalidades:
        lines.append(f"**Nacionalidades:** {', '.join(entidade.nacionalidades)}")
    if entidade.data_nascimento:
        lines.append(f"**Nascimento:** {entidade.data_nascimento}")
    if entidade.posicao:
        lines.append(f"**Cargo/Posição:** {entidade.posicao}")
    if entidade.cpf_cnpj:
        lines.append(f"**CPF/CNPJ/Tax ID:** {entidade.cpf_cnpj}")
    if entidade.nomes_alternativos:
        nomes = ", ".join(entidade.nomes_alternativos[:10])
        lines.append(f"**Nomes alternativos:** {nomes}")

    if entidade.datasets:
        lines.append(f"")
        lines.append(f"**Aparece nas listas:**")
        all_known = {**DATASETS_SANCOES, **DATASETS_PEPS}
        for d in entidade.datasets:
            lines.append(f"  - {all_known.get(d, d)}")

    if entidade.descricao:
        lines.append(f"")
        lines.append(f"**Descrição:** {entidade.descricao}")

    return "\n".join(lines)


async def listar_listas_sancoes() -> str:
    """Lista todas as fontes de sanções disponíveis no OpenSanctions.

    Retorna os datasets disponíveis com número de entidades e publicador.
    Útil para entender quais listas são consultadas nas verificações.

    Returns:
        Tabela com listas de sanções disponíveis.
    """
    try:
        datasets = await client.listar_datasets()
    except HttpClientError as exc:
        return f"Erro ao listar datasets: {exc}"

    if not datasets:
        return "Nenhum dataset disponível no momento."

    # Sort: most entities first
    datasets_sorted = sorted(
        datasets,
        key=lambda d: d.entidades or 0,
        reverse=True,
    )

    rows = [
        (
            d.nome or "—",
            (d.titulo or "—")[:60],
            f"{d.entidades:,}" if d.entidades else "—",
            d.publicador or "—",
            d.ultima_atualizacao or "—",
        )
        for d in datasets_sorted[:40]
    ]
    return "Listas de sanções disponíveis (OpenSanctions):\n\n" + markdown_table(
        ["Dataset", "Título", "Entidades", "Publicador", "Atualização"], rows
    )
