"""Tool functions for the CVM feature.

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


async def buscar_companhias_cvm(
    nome: str | None = None,
    cnpj: str | None = None,
    situacao: str | None = None,
    pagina: int = 1,
) -> str:
    """Busca companhias abertas registradas na CVM.

    Retorna empresas com ações ou títulos negociados no mercado de capitais
    brasileiro, incluindo status de registro, setor e contato oficial.

    Args:
        nome: Nome ou razão social da empresa (busca parcial).
        cnpj: CNPJ da empresa (aceita formatado ou somente dígitos).
        situacao: Situação do registro (ATIVO, CANCELADO, SUSPENSO).
        pagina: Página de resultados (padrão: 1).

    Returns:
        Tabela com companhias encontradas.
    """
    try:
        cias = await client.buscar_companhias(
            nome=nome, cnpj=cnpj, situacao=situacao, pagina=pagina
        )
    except HttpClientError as exc:
        return f"Erro ao consultar companhias CVM: {exc}"

    if not cias:
        filtro = nome or cnpj or "filtros informados"
        return f"Nenhuma companhia encontrada para '{filtro}'."

    rows = [
        (
            c.cnpj or "—",
            (c.nome or "—")[:50],
            c.tipo or "—",
            c.situacao or "—",
            (c.setor or "—")[:40],
            c.data_registro or "—",
        )
        for c in cias
    ]
    header = "Companhias abertas (CVM):\n\n"
    table = header + markdown_table(
        ["CNPJ", "Nome", "Tipo", "Situação", "Setor", "Data Registro"], rows
    )
    return table + _pagination_hint(len(cias), pagina)


async def buscar_processos_cvm(
    nome: str | None = None,
    cpf_cnpj: str | None = None,
    pagina: int = 1,
) -> str:
    """Busca Processos Administrativos Sancionadores (PAS) da CVM.

    Os processos PAS são instaurados contra empresas e pessoas físicas por
    irregularidades no mercado de capitais — insider trading, manipulação
    de mercado, fraude contábil, irregularidades em fundos, etc.

    Args:
        nome: Nome do acusado (busca parcial).
        cpf_cnpj: CPF ou CNPJ do acusado.
        pagina: Página de resultados (padrão: 1).

    Returns:
        Tabela com processos encontrados.
    """
    try:
        processos = await client.buscar_processos(
            nome=nome, cpf_cnpj=cpf_cnpj, pagina=pagina
        )
    except HttpClientError as exc:
        return f"Erro ao consultar processos CVM: {exc}"

    if not processos:
        filtro = nome or cpf_cnpj or "filtros informados"
        return f"Nenhum processo CVM encontrado para '{filtro}'."

    rows = [
        (
            p.numero or "—",
            (p.acusado or "—")[:40],
            p.cpf_cnpj or "—",
            p.decisao or "—",
            p.penalidade or "—",
            format_brl(p.valor_multa) if p.valor_multa else "—",
            p.data_julgamento or "—",
        )
        for p in processos
    ]
    header = "Processos Administrativos Sancionadores (CVM):\n\n"
    table = header + markdown_table(
        ["Número", "Acusado", "CPF/CNPJ", "Decisão", "Penalidade", "Multa", "Data"], rows
    )
    return table + _pagination_hint(len(processos), pagina)


async def buscar_fundos_investimento(
    nome: str | None = None,
    cnpj: str | None = None,
    classe: str | None = None,
    pagina: int = 1,
) -> str:
    """Busca fundos de investimento registrados na CVM.

    Cobre fundos de renda fixa, ações, multimercado, FIIs e demais classes.
    Útil para verificar situação regulatória e identificar administradores.

    Args:
        nome: Nome ou denominação social do fundo.
        cnpj: CNPJ do fundo.
        classe: Classe do fundo (Renda Fixa, Ações, Multimercado, Fundo Imobiliário, etc.).
        pagina: Página de resultados (padrão: 1).

    Returns:
        Tabela com fundos encontrados.
    """
    try:
        fundos = await client.buscar_fundos(
            nome=nome, cnpj=cnpj, classe=classe, pagina=pagina
        )
    except HttpClientError as exc:
        return f"Erro ao consultar fundos CVM: {exc}"

    if not fundos:
        filtro = nome or cnpj or classe or "filtros informados"
        return f"Nenhum fundo de investimento encontrado para '{filtro}'."

    rows = [
        (
            f.cnpj or "—",
            (f.denominacao or "—")[:50],
            f.classe or "—",
            f.situacao or "—",
            (f.administrador or "—")[:40],
            f.data_registro or "—",
        )
        for f in fundos
    ]
    header = "Fundos de investimento (CVM):\n\n"
    table = header + markdown_table(
        ["CNPJ", "Denominação", "Classe", "Situação", "Administrador", "Data Registro"], rows
    )
    return table + _pagination_hint(len(fundos), pagina)
