"""Tool functions for the SICONFI feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption

SICONFI — QUIRK IMPORTANTE (evitar erro):
    No SICONFI, o campo `uf` dos entes tem comportamento diferente por esfera:
    - Municípios (esfera='M'): campo `uf` = sigla do estado (ex: "SP", "RJ")
    - Estados     (esfera='E'): campo `uf` = "BR" (sempre, independente do estado)
    - Federal     (esfera='U'): campo `uf` = None, cod_ibge = 1

    PORTANTO:
    ✅ Municípios de SP  → listar_entes_siconfi(uf='SP', esfera='M')
    ✅ Estado de SP      → listar_entes_siconfi(nome='São Paulo', esfera='E')
    ✅ Todos os estados  → listar_entes_siconfi(esfera='E')
    ❌ ERRADO            → listar_entes_siconfi(uf='SP', esfera='E')  ← retorna vazio

    Códigos IBGE dos estados (para usar em buscar_rreo / buscar_rgf):
    AC=12, AL=27, AM=13, AP=16, BA=29, CE=23, DF=53, ES=32, GO=52,
    MA=21, MG=31, MS=50, MT=51, PA=15, PB=25, PE=26, PI=22, PR=41,
    RJ=33, RN=24, RO=11, RR=14, RS=43, SC=42, SE=28, SP=35, TO=17
    Governo Federal = 1
"""

from __future__ import annotations

from mcp_brasil._shared.formatting import format_brl, markdown_table
from mcp_brasil.exceptions import HttpClientError

from . import client
from .constants import ANEXOS_RGF, ANEXOS_RREO, DEFAULT_LIMIT, ESFERAS, PODERES

_ESTADOS_IBGE = {
    "AC": 12, "AL": 27, "AM": 13, "AP": 16, "BA": 29, "CE": 23, "DF": 53,
    "ES": 32, "GO": 52, "MA": 21, "MG": 31, "MS": 50, "MT": 51, "PA": 15,
    "PB": 25, "PE": 26, "PI": 22, "PR": 41, "RJ": 33, "RN": 24, "RO": 11,
    "RR": 14, "RS": 43, "SC": 42, "SE": 28, "SP": 35, "TO": 17,
}


async def listar_entes_siconfi(
    uf: str | None = None,
    esfera: str | None = None,
    nome: str | None = None,
) -> str:
    """Lista entes federativos (estados e municípios) cadastrados no SICONFI.

    Retorna os entes com seus códigos IBGE, necessários para consultar RREO e RGF.

    ⚠️ ATENÇÃO — comportamento do campo `uf` no SICONFI:
    - Municípios (esfera='M'): campo `uf` contém a sigla do estado (ex: "SP").
    - Estados (esfera='E'): campo `uf` é SEMPRE "BR", não a sigla do estado.
    - Portanto, `uf='SP', esfera='E'` retorna VAZIO — isso é correto e esperado.

    Como buscar corretamente:
    - Municípios de SP:  uf='SP', esfera='M'
    - Estado de SP:      nome='São Paulo', esfera='E'
    - Todos os estados:  esfera='E'  (sem uf)

    Args:
        uf: Sigla do estado (ex: "SP"). Filtra municípios deste estado.
            NÃO use com esfera='E' — estados têm uf='BR', não a sigla.
        esfera: Esfera de governo: "E" (estadual), "M" (municipal), "U" (federal).
        nome: Nome parcial do ente (ex: "São Paulo", "Campinas", "Recife").

    Returns:
        Tabela com entes federativos e respectivos códigos IBGE.
    """
    # Detect the common mistake: uf + esfera='E' always returns empty
    if uf and esfera and esfera.upper() == "E":
        uf_upper = uf.upper()
        ibge = _ESTADOS_IBGE.get(uf_upper)
        hint = (
            f"\n⚠️ Aviso: estados (esfera='E') têm uf='BR' no SICONFI, não '{uf_upper}'.\n"
            f"Para encontrar o governo estadual de {uf_upper}, use nome='{uf_upper}' ou "
            f"esfera='E' sem uf."
        )
        if ibge:
            hint += (
                f"\nCódigo IBGE do estado {uf_upper} = {ibge} "
                f"(use direto em buscar_rreo/buscar_rgf)."
            )
        # Continue with corrected query (drop uf, search by nome using state name)
        estado_nomes = {
            "AC": "Acre", "AL": "Alagoas", "AM": "Amazonas", "AP": "Amapá",
            "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
            "GO": "Goiás", "MA": "Maranhão", "MG": "Minas Gerais", "MS": "Mato Grosso do Sul",
            "MT": "Mato Grosso", "PA": "Pará", "PB": "Paraíba", "PE": "Pernambuco",
            "PI": "Piauí", "PR": "Paraná", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
            "RO": "Rondônia", "RR": "Roraima", "RS": "Rio Grande do Sul", "SC": "Santa Catarina",
            "SE": "Sergipe", "SP": "São Paulo", "TO": "Tocantins",
        }
        nome_estado = nome or estado_nomes.get(uf_upper)
        try:
            entes = await client.listar_entes(uf=None, esfera="E", nome=nome_estado, limite=5)
        except HttpClientError as exc:
            return f"Erro ao consultar SICONFI: {exc}" + hint
        if entes:
            rows = [
                (
                    str(e.cod_ibge or "—"),
                    (e.ente or "—")[:50],
                    e.uf or "—",
                    ESFERAS.get(e.esfera or "", e.esfera or "—"),
                    f"{e.populacao:,}" if e.populacao else "—",
                )
                for e in entes
            ]
            return (
                hint + "\n\nResultado corrigido automaticamente:\n\n"
                + markdown_table(["Cód. IBGE", "Ente", "UF", "Esfera", "População"], rows)
            )
        return hint + "\n\nNenhum ente estadual encontrado."

    try:
        entes = await client.listar_entes(uf=uf, esfera=esfera, nome=nome, limite=200)
    except HttpClientError as exc:
        return f"Erro ao consultar SICONFI: {exc}"

    if not entes:
        filtros = []
        if uf:
            filtros.append(f"uf='{uf}'")
        if esfera:
            filtros.append(f"esfera='{esfera}'")
        if nome:
            filtros.append(f"nome='{nome}'")
        desc = f" com filtros {', '.join(filtros)}" if filtros else ""
        return f"Nenhum ente encontrado{desc}."

    rows = [
        (
            str(e.cod_ibge or "—"),
            (e.ente or "—")[:50],
            e.uf or "—",
            ESFERAS.get(e.esfera or "", e.esfera or "—"),
            f"{e.populacao:,}" if e.populacao else "—",
        )
        for e in entes
    ]
    header = f"Entes federativos no SICONFI ({len(entes)} encontrados):\n\n"
    return header + markdown_table(["Cód. IBGE", "Ente", "UF", "Esfera", "População"], rows)


async def buscar_rreo(
    cod_ibge: int,
    exercicio: int,
    periodo: int,
    anexo: str = "RREO-Anexo 01",
) -> str:
    """Consulta o RREO (Relatório Resumido de Execução Orçamentária) de um ente.

    O RREO é publicado bimestralmente (6 períodos por ano) e contém dados de
    arrecadação e execução orçamentária. Use listar_entes_siconfi para obter
    o código IBGE do ente desejado.

    Códigos IBGE úteis:
    - Governo Federal = 1
    - SP=35, RJ=33, MG=31, RS=43, PR=41, SC=42, BA=29, GO=52, PE=26, CE=23

    Args:
        cod_ibge: Código IBGE do ente. Use listar_entes_siconfi para buscar.
        exercicio: Ano de referência (ex: 2024).
        periodo: Bimestre de 1 a 6.
        anexo: Anexo do relatório:
               "RREO-Anexo 01" = Receitas Orçamentárias (padrão),
               "RREO-Anexo 02" = Despesas por Função/Subfunção,
               "RREO-Anexo 03" = Receita Corrente Líquida.

    Returns:
        Tabela com contas e valores do RREO.
    """
    try:
        itens = await client.buscar_rreo(
            cod_ibge=cod_ibge,
            exercicio=exercicio,
            periodo=periodo,
            anexo=anexo,
        )
    except HttpClientError as exc:
        return f"Erro ao consultar RREO: {exc}"

    if not itens:
        return (
            f"Nenhum dado encontrado para RREO — cód. IBGE {cod_ibge}, "
            f"exercício {exercicio}, período {periodo}º bimestre, anexo '{anexo}'.\n\n"
            f"Dica: verifique o cod_ibge com listar_entes_siconfi. "
            f"Anexos disponíveis: "
            + ", ".join(f'"{a}"' for a in ANEXOS_RREO)
        )

    inst = itens[0].instituicao or f"Ente {cod_ibge}"
    top_rows = [i for i in itens if i.conta and not i.conta.startswith(" ")][:30]
    display = top_rows or itens[:30]

    rows = [
        (
            (i.conta or "—")[:60],
            i.coluna or "—",
            format_brl(i.valor) if i.valor is not None else "—",
        )
        for i in display
    ]

    header = (
        f"## RREO — {inst}\n"
        f"Exercício: {exercicio} | Período: {periodo}º bimestre | Anexo: {anexo}\n\n"
    )
    return header + markdown_table(["Conta", "Coluna", "Valor"], rows)


async def buscar_rgf(
    cod_ibge: int,
    exercicio: int,
    periodo: int,
    anexo: str = "RGF-Anexo 01",
    poder: str = "E",
    esfera: str = "E",
) -> str:
    """Consulta o RGF (Relatório de Gestão Fiscal) de um ente federativo.

    O RGF é publicado quadrimestralmente (3 períodos por ano) e contém dados
    de despesa com pessoal, dívida pública e operações de crédito, conforme
    a Lei de Responsabilidade Fiscal (LRF).

    Códigos IBGE úteis:
    - Governo Federal = 1  (use esfera='U')
    - SP=35, RJ=33, MG=31, RS=43, PR=41, SC=42, BA=29, GO=52, PE=26, CE=23
      (para estados use esfera='E'; para municípios use esfera='M')

    Args:
        cod_ibge: Código IBGE do ente. Use listar_entes_siconfi para buscar.
        exercicio: Ano de referência (ex: 2024).
        periodo: Quadrimestre de 1 a 3.
        anexo: Anexo do relatório:
               "RGF-Anexo 01" = Despesa com Pessoal (padrão),
               "RGF-Anexo 02" = Dívida Consolidada Líquida,
               "RGF-Anexo 03" = Garantias e Contragarantias,
               "RGF-Anexo 04" = Operações de Crédito.
        poder: Poder: "E" (executivo, padrão), "L" (legislativo), "J" (judiciário),
               "M" (Ministério Público), "D" (Defensoria).
        esfera: Esfera do ente: "E" (estadual, padrão), "M" (municipal), "U" (federal).
                ⚠️ Deve corresponder à esfera do cod_ibge informado.

    Returns:
        Tabela com contas e valores do RGF.
    """
    try:
        itens = await client.buscar_rgf(
            cod_ibge=cod_ibge,
            exercicio=exercicio,
            periodo=periodo,
            anexo=anexo,
            poder=poder,
            esfera=esfera,
        )
    except HttpClientError as exc:
        return f"Erro ao consultar RGF: {exc}"

    if not itens:
        esfera_nome = ESFERAS.get(esfera.upper(), esfera)
        return (
            f"Nenhum dado encontrado para RGF — cód. IBGE {cod_ibge}, "
            f"exercício {exercicio}, período {periodo}º quadrimestre, "
            f"esfera='{esfera}' ({esfera_nome}), poder='{poder}', anexo='{anexo}'.\n\n"
            f"Dica: confirme se a esfera e o cod_ibge correspondem ao mesmo ente. "
            f"Use listar_entes_siconfi para verificar. "
            f"Anexos disponíveis: "
            + ", ".join(f'"{a}"' for a in ANEXOS_RGF)
        )

    inst = itens[0].instituicao or f"Ente {cod_ibge}"
    poder_nome = PODERES.get(poder.upper(), poder)
    esfera_nome = ESFERAS.get(esfera.upper(), esfera)

    rows = [
        (
            (i.conta or "—")[:60],
            i.coluna or "—",
            format_brl(i.valor) if i.valor is not None else "—",
        )
        for i in itens[:40]
    ]

    header = (
        f"## RGF — {inst}\n"
        f"Exercício: {exercicio} | Período: {periodo}º quadrimestre | "
        f"Poder: {poder_nome} | Esfera: {esfera_nome}\n"
        f"Anexo: {anexo} — {ANEXOS_RGF.get(anexo, '')}\n\n"
    )
    return header + markdown_table(["Conta", "Coluna", "Valor"], rows)
