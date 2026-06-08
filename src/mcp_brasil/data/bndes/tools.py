"""Tool functions for the BNDES feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

from mcp_brasil._shared.formatting import format_brl, markdown_table
from mcp_brasil.exceptions import HttpClientError

from . import client
from .constants import DEFAULT_LIMIT, SITUACOES_CONTRATO


async def buscar_operacoes_bndes(
    nome: str | None = None,
    cnpj: str | None = None,
    uf: str | None = None,
    setor: str | None = None,
    situacao: str | None = None,
    limite: int = DEFAULT_LIMIT,
) -> str:
    """Busca operações de financiamento não-automáticas contratadas com o BNDES.

    Permite verificar contratos de financiamento do BNDES por empresa, CNPJ,
    estado ou setor. Inclui projetos de infraestrutura, energia, indústria,
    agronegócio e outros setores financiados pelo banco.

    Args:
        nome: Nome do cliente/beneficiário (busca por texto).
        cnpj: CNPJ do beneficiário (com ou sem pontuação).
        uf: Sigla do estado (ex: "SP", "RJ", "MG").
        setor: Setor BNDES (ex: "Indústria", "Energia", "Agropecuária").
        situacao: Situação do contrato: "CONTRATADO", "LIQUIDADO", "CANCELADO".
        limite: Número máximo de resultados (padrão: 20, máx: 100).

    Returns:
        Tabela com operações encontradas e valores contratados/desembolsados.
    """
    if not any([nome, cnpj, uf, setor, situacao]):
        return (
            "Informe ao menos um critério de busca: nome, cnpj, uf, setor ou situacao."
        )

    limite = min(limite, 100)

    try:
        operacoes = await client.buscar_operacoes(
            nome=nome,
            cnpj=cnpj,
            uf=uf,
            setor_bndes=setor,
            situacao=situacao,
            limite=limite,
        )
    except HttpClientError as exc:
        return f"Erro ao consultar BNDES: {exc}"

    if not operacoes:
        partes = []
        if nome:
            partes.append(f"nome='{nome}'")
        if cnpj:
            partes.append(f"CNPJ={cnpj}")
        if uf:
            partes.append(f"UF={uf}")
        if setor:
            partes.append(f"setor='{setor}'")
        return f"Nenhuma operação encontrada para {', '.join(partes)}."

    rows = [
        (
            (o.cliente or "—")[:40],
            o.cnpj or "—",
            o.uf or "—",
            (o.produto or "—")[:30],
            format_brl(o.valor_contratado_reais) if o.valor_contratado_reais else "—",
            format_brl(o.valor_desembolsado_reais) if o.valor_desembolsado_reais else "—",
            SITUACOES_CONTRATO.get(o.situacao_do_contrato or "", o.situacao_do_contrato or "—"),
            o.data_da_contratacao or "—",
        )
        for o in operacoes
    ]

    header = f"Operações BNDES ({len(operacoes)} encontradas):\n\n"
    return header + markdown_table(
        ["Cliente", "CNPJ", "UF", "Produto", "Contratado", "Desembolsado", "Situação", "Data"],
        rows,
    )
