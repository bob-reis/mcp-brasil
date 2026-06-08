"""Tool functions for the BNMP (CNJ) feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

import httpx

from mcp_brasil._shared.formatting import markdown_table

from . import client


def _fmt_mandados(mandados: list) -> str:
    if not mandados:
        return "Nenhum mandado encontrado."
    rows = [
        {
            "Nome": m.nome or "",
            "Tipo": m.tipo_peca or "",
            "Situação": m.situacao or "",
            "Data Expedição": m.data_expedicao or "",
            "Órgão": m.orgao_expeditor or "",
            "UF": m.uf or "",
            "Município": m.municipio or "",
        }
        for m in mandados
    ]
    return markdown_table(rows)


async def buscar_mandados(
    nome: str,
    pagina: int = 0,
    tamanho: int = 10,
) -> str:
    """Busca mandados de prisão no BNMP (Banco Nacional de Mandados de Prisão do CNJ).

    Retorna mandados ativos e histórico de prisão por nome da pessoa.
    Mandados sob sigilo judicial não aparecem nesta consulta pública.

    Args:
        nome: Nome completo ou parcial da pessoa.
        pagina: Página de resultados (0 = primeira). Default: 0.
        tamanho: Quantidade de resultados por página (1-20). Default: 10.

    Returns:
        Tabela com mandados encontrados ou mensagem de ausência.
    """
    try:
        mandados = await client.buscar_mandados(nome, pagina, tamanho)
    except httpx.HTTPStatusError as exc:
        return f"Erro HTTP {exc.response.status_code} ao consultar BNMP para '{nome}'."
    except Exception as exc:
        return f"Falha na consulta BNMP para '{nome}': {exc}"

    header = f"**BNMP — Mandados de Prisão: {nome}**\n\n"
    footer = "\n\n_Fonte: BNMP — Banco Nacional de Mandados de Prisão (CNJ) · portalbnmp.cnj.jus.br_"
    if not mandados:
        return (
            header
            + "Nenhum mandado de prisão encontrado para este nome no BNMP público.\n"
            + "Mandados sob sigilo judicial não aparecem nesta base."
            + footer
        )
    return header + _fmt_mandados(mandados) + footer
