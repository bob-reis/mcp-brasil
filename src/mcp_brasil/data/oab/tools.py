"""Tool functions for the OAB (Conselho Federal) feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

import httpx

from mcp_brasil._shared.formatting import markdown_table

from . import client


def _fmt_advogados(advogados: list) -> str:
    if not advogados:
        return "Nenhum advogado encontrado."
    rows = [
        {
            "Nome": a.nome or "",
            "Nº OAB": a.numero_oab or "",
            "Seccional": a.seccional or "",
            "Situação": a.situacao or "",
            "Subtipo": a.subtipo or "",
        }
        for a in advogados
    ]
    return markdown_table(rows)


async def consultar_advogado(
    nome: str = "",
    numero_oab: str = "",
    seccional: str = "",
) -> str:
    """Consulta advogados no Cadastro Nacional de Advogados (CNA) da OAB.

    Permite buscar por nome, por número de inscrição OAB com seccional,
    ou combinar os dois filtros. Retorna situação cadastral e tipo de inscrição.

    Args:
        nome: Nome do advogado (parcial ou completo).
        numero_oab: Número de inscrição OAB (ex: "123456").
        seccional: Seccional estadual (ex: "SP", "RJ", "MG").
                   Obrigatório quando informado o número OAB.

    Returns:
        Tabela com advogados encontrados ou mensagem de erro.
    """
    if not nome and not numero_oab:
        return "Informe ao menos o nome do advogado ou o número OAB com seccional."

    header = f"**OAB — Consulta de Advogados**\n\n"
    footer = "\n\n_Fonte: OAB — Cadastro Nacional de Advogados · cna.oab.org.br_"

    try:
        if numero_oab and seccional:
            adv = await client.buscar_por_numero(numero_oab, seccional)
            advogados = [adv] if adv else []
        else:
            advogados = await client.buscar_por_nome(nome, seccional)
    except httpx.HTTPStatusError as exc:
        return f"Erro HTTP {exc.response.status_code} ao consultar CNA/OAB."
    except Exception as exc:
        return (
            f"Falha na consulta OAB: {exc}\n"
            "A API do CNA pode estar temporariamente indisponível. "
            "Verifique diretamente em cna.oab.org.br"
        )

    if not advogados:
        return header + "Nenhum advogado encontrado para os critérios informados." + footer
    return header + _fmt_advogados(advogados) + footer
