"""Tool functions for the Querido Diário feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
"""

from __future__ import annotations

import httpx

from . import client


def _fmt_gazette(gz) -> str:
    lines = [f"**{gz.data}** — {gz.municipio}/{gz.uf}"]
    if gz.edicao:
        lines.append(f"Edição: {gz.edicao}")
    if gz.url:
        lines.append(f"PDF: {gz.url}")
    for trecho in gz.trechos:
        lines.append(f"> {trecho.strip()}")
    return "\n".join(lines)


async def buscar_diarios_municipais(
    municipio: str,
    query: str = "",
    max_resultados: int = 5,
) -> str:
    """Busca publicações em diários oficiais municipais via Querido Diário (Open Knowledge Brasil).

    Permite pesquisar licitações, contratos, nomeações, decretos e qualquer ato
    publicado no diário oficial de municípios brasileiros. Cobre centenas de cidades.

    Args:
        municipio: Nome da cidade (ex: "Uberlândia", "São Paulo", "Curitiba").
        query: Termo de busca no diário (ex: "licitação", "contrato", nome de empresa).
               Se vazio, retorna publicações recentes do município.
        max_resultados: Máximo de publicações retornadas (1-10). Default: 5.

    Returns:
        Publicações encontradas com data, edição, trechos relevantes e link para o PDF.
    """
    header = f"**Querido Diário — {municipio}**"
    if query:
        header += f" · Busca: _{query}_"
    header += "\n\n"
    footer = "\n\n_Fonte: Querido Diário — Open Knowledge Brasil · queridodiario.ok.org.br_"

    try:
        resultado = await client.buscar_diarios(municipio, query, max_resultados)
    except httpx.HTTPStatusError as exc:
        return f"Erro HTTP {exc.response.status_code} ao consultar Querido Diário."
    except Exception as exc:
        return f"Falha ao consultar Querido Diário para '{municipio}': {exc}"

    if not resultado.territory_id:
        return (
            header
            + f"Cidade '{municipio}' não encontrada no Querido Diário. "
            "Tente o nome completo sem acentos ou verifique se o município "
            "já aderiu ao projeto em queridodiario.ok.org.br"
            + footer
        )

    if not resultado.gazettes:
        return (
            header
            + f"Nenhuma publicação encontrada para '{query or municipio}' em {municipio}.\n"
            f"Total de diários indexados para esta cidade: {resultado.total}"
            + footer
        )

    entries = "\n\n---\n\n".join(_fmt_gazette(gz) for gz in resultado.gazettes)
    summary = f"Encontradas {resultado.total} publicação(ões). Exibindo {len(resultado.gazettes)}:\n\n"
    return header + summary + entries + footer


async def buscar_cidade(municipio: str) -> str:
    """Verifica se um município está disponível no Querido Diário e retorna seu código IBGE.

    Use antes de buscar diários para confirmar cobertura do município.

    Args:
        municipio: Nome da cidade.

    Returns:
        Código IBGE e confirmação de disponibilidade, ou mensagem de ausência.
    """
    try:
        territory_id = await client.buscar_territorio(municipio)
    except Exception as exc:
        return f"Erro ao buscar município '{municipio}': {exc}"

    if territory_id:
        return (
            f"✅ **{municipio}** está disponível no Querido Diário.\n"
            f"Código IBGE: `{territory_id}`\n"
            "Use `querido_diario_buscar_diarios_municipais` para pesquisar publicações."
        )
    return (
        f"❌ **{municipio}** não encontrado no Querido Diário.\n"
        "O município pode não ter aderido ao projeto ainda. "
        "Consulte queridodiario.ok.org.br para ver a cobertura atual."
    )
