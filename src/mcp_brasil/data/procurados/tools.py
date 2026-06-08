"""Tool functions for the Procurados (Interpol + PF) feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

import httpx

from mcp_brasil._shared.formatting import markdown_table

from . import client


def _fmt_notices(notices: list) -> str:
    if not notices:
        return "Nenhum aviso encontrado."
    rows = [
        {
            "Nome": n.nome or "",
            "Nacionalidade": n.nacionalidade or "",
            "Nascimento": n.data_nascimento or "",
            "Fonte": n.fonte,
            "Link": n.link or "",
        }
        for n in notices
    ]
    return markdown_table(rows)


async def buscar_interpol(
    nome: str,
    nacionalidade: str = "BR",
    max_resultados: int = 5,
) -> str:
    """Busca avisos vermelhos (Red Notices) da Interpol por nome.

    Localiza pessoas procuradas internacionalmente com vínculo ao Brasil.
    Útil para cruzar com investigações sobre foragidos, crimes financeiros e evasão fiscal.

    Args:
        nome: Nome completo ou parcial da pessoa (ex: "João Silva").
        nacionalidade: Código ISO do país (ex: "BR", "US", "FR"). Default: "BR".
        max_resultados: Máximo de resultados (1-10). Default: 5.

    Returns:
        Tabela com avisos vermelhos encontrados ou mensagem de ausência.
    """
    header = f"**Interpol Red Notices — {nome}**\n\n"
    footer = "\n\n_Fonte: Interpol Notices API · interpol.int_"

    try:
        notices = await client.buscar_interpol(nome, nacionalidade, max_resultados)
    except httpx.HTTPStatusError as exc:
        return f"Erro HTTP {exc.response.status_code} ao consultar API Interpol."
    except Exception as exc:
        return f"Falha ao consultar Interpol para '{nome}': {exc}"

    if not notices:
        return (
            header
            + f"Nenhum aviso vermelho Interpol encontrado para '{nome}' "
            f"(nacionalidade: {nacionalidade}).\n"
            "Isso não exclui outros tipos de aviso ou processos nacionais."
            + footer
        )
    return header + _fmt_notices(notices) + footer
