"""Tool functions for the TCU feature.

Rules (ADR-001):
    - tools.py NEVER makes HTTP directly — delegates to client.py
    - Returns formatted strings for LLM consumption
    - Uses Context for structured logging and progress reporting
"""

from __future__ import annotations

from fastmcp import Context

from mcp_brasil._shared.formatting import format_brl

from . import client
from .schemas import ParcelaDebito

# ---------------------------------------------------------------------------
# buscar_acordaos
# ---------------------------------------------------------------------------


async def buscar_acordaos(
    ctx: Context,
    inicio: int = 0,
    quantidade: int = 20,
) -> str:
    """Busca acórdãos (decisões colegiadas) do TCU.

    Acórdãos são as decisões formais do Tribunal de Contas da União, incluindo
    julgamentos de contas, auditorias e recursos. Retorna decisões recentes
    por padrão (mais recentes primeiro).

    Args:
        ctx: Contexto MCP.
        inicio: Índice inicial para paginação (0 = mais recentes).
        quantidade: Quantidade de acórdãos a retornar (máx ~50).

    Returns:
        Lista formatada de acórdãos com título, colegiado, relator e sumário.
    """
    await ctx.info(f"Buscando acórdãos do TCU (início={inicio})...")
    acordaos = await client.buscar_acordaos(inicio=inicio, quantidade=quantidade)

    if not acordaos:
        return "Nenhum acórdão encontrado."

    lines: list[str] = [f"**{len(acordaos)} acórdãos do TCU:**\n"]
    for a in acordaos[:20]:
        lines.append(f"### {a.titulo or 'Sem título'}")
        lines.append(f"- **Colegiado:** {a.colegiado or '—'}")
        lines.append(f"- **Relator:** {a.relator or '—'}")
        lines.append(f"- **Data sessão:** {a.data_sessao or '—'}")
        lines.append(f"- **Situação:** {a.situacao or '—'}")
        if a.sumario:
            sumario = a.sumario[:300] + "..." if len(a.sumario) > 300 else a.sumario
            lines.append(f"- **Sumário:** {sumario}")
        if a.url_acordao:
            lines.append(f"- **Link:** {a.url_acordao}")
        lines.append("")

    if len(acordaos) >= quantidade:
        lines.append(
            f"\n*Página com {quantidade} resultados. "
            f"Use inicio={inicio + quantidade} para próxima página.*"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# consultar_inabilitados
# ---------------------------------------------------------------------------


async def consultar_inabilitados(
    ctx: Context,
    cpf: str | None = None,
    offset: int = 0,
    limit: int = 25,
) -> str:
    """Consulta pessoas inabilitadas para exercer função pública por decisão do TCU.

    Pessoas inabilitadas não podem exercer cargo em comissão ou função de
    confiança na Administração Pública Federal. Permite buscar por CPF
    específico ou listar todos.

    Args:
        ctx: Contexto MCP.
        cpf: CPF para consulta específica (somente números).
        offset: Deslocamento para paginação.
        limit: Quantidade por página (padrão 25).

    Returns:
        Lista de pessoas inabilitadas com dados da sanção.
    """
    await ctx.info("Consultando inabilitados no TCU...")
    resultado = await client.consultar_inabilitados(cpf=cpf, offset=offset, limit=limit)

    if not resultado.items:
        if cpf:
            return f"CPF {cpf} **não consta** na lista de inabilitados do TCU."
        return "Nenhum inabilitado encontrado."

    lines: list[str] = [f"**{resultado.count} inabilitado(s) encontrado(s):**\n"]
    for item in resultado.items:
        lines.append(f"### {item.nome or '—'}")
        lines.append(f"- **CPF:** {item.cpf or '—'}")
        lines.append(f"- **Processo:** {item.processo or '—'}")
        lines.append(f"- **Deliberação:** {item.deliberacao or '—'}")
        lines.append(f"- **UF:** {item.uf or '—'}")
        if item.data_final:
            lines.append(f"- **Inabilitado até:** {item.data_final}")
        lines.append("")

    if resultado.has_more:
        next_offset = resultado.offset + resultado.limit
        lines.append(
            f"*Mais resultados disponíveis. Use offset={next_offset} para próxima página.*"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# consultar_inidoneos
# ---------------------------------------------------------------------------


async def consultar_inidoneos(
    ctx: Context,
    cpf_cnpj: str | None = None,
    offset: int = 0,
    limit: int = 25,
) -> str:
    """Consulta licitantes declarados inidôneos pelo TCU.

    Empresas e pessoas declaradas inidôneas não podem participar de
    licitações na Administração Pública Federal. Permite buscar por
    CPF/CNPJ específico ou listar todos.

    Args:
        ctx: Contexto MCP.
        cpf_cnpj: CPF ou CNPJ para consulta específica (somente números).
        offset: Deslocamento para paginação.
        limit: Quantidade por página (padrão 25).

    Returns:
        Lista de licitantes inidôneos com dados da sanção.
    """
    await ctx.info("Consultando inidôneos no TCU...")
    resultado = await client.consultar_inidoneos(cpf_cnpj=cpf_cnpj, offset=offset, limit=limit)

    if not resultado.items:
        if cpf_cnpj:
            return f"CPF/CNPJ {cpf_cnpj} **não consta** na lista de inidôneos do TCU."
        return "Nenhum inidôneo encontrado."

    lines: list[str] = [f"**{resultado.count} inidôneo(s) encontrado(s):**\n"]
    for item in resultado.items:
        lines.append(f"### {item.nome or '—'}")
        lines.append(f"- **CPF/CNPJ:** {item.cpf_cnpj or '—'}")
        lines.append(f"- **Processo:** {item.processo or '—'}")
        lines.append(f"- **Deliberação:** {item.deliberacao or '—'}")
        lines.append(f"- **UF:** {item.uf or '—'}")
        if item.data_final:
            lines.append(f"- **Inidôneo até:** {item.data_final}")
        lines.append("")

    if resultado.has_more:
        next_offset = resultado.offset + resultado.limit
        lines.append(
            f"*Mais resultados disponíveis. Use offset={next_offset} para próxima página.*"
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# consultar_certidoes_apf
# ---------------------------------------------------------------------------


async def consultar_certidoes_apf(cnpj: str, ctx: Context) -> str:
    """Consulta certidões consolidadas de pessoa jurídica (APF).

    Verifica a situação de uma empresa em 4 cadastros simultaneamente:
    - **TCU Inidôneos**: licitantes declarados inidôneos
    - **CNJ CNIA**: condenações por improbidade administrativa
    - **CGU CEIS**: empresas inidôneas e suspensas
    - **CGU CNEP**: empresas punidas

    Muito útil para due diligence de fornecedores em licitações.

    Args:
        cnpj: CNPJ da empresa (somente números, 14 dígitos).
        ctx: Contexto MCP.

    Returns:
        Situação consolidada da empresa nos 4 cadastros.
    """
    await ctx.info(f"Consultando certidões APF para CNPJ {cnpj}...")
    resultado = await client.consultar_certidoes(cnpj)

    lines: list[str] = []
    lines.append(f"## Certidões APF — {resultado.razao_social or cnpj}")
    if resultado.nome_fantasia:
        lines.append(f"**Nome fantasia:** {resultado.nome_fantasia}")
    lines.append(f"**CNPJ:** {resultado.cnpj or cnpj}")
    lines.append("")

    if not resultado.certidoes:
        lines.append("Nenhuma certidão retornada.")
        return "\n".join(lines)

    for cert in resultado.certidoes:
        situacao = cert.situacao or "—"
        emoji = "NADA_CONSTA" if situacao == "NADA_CONSTA" else "CONSTA"
        status_label = "Nada consta" if emoji == "NADA_CONSTA" else situacao
        lines.append(f"- **{cert.emissor} ({cert.tipo}):** {status_label}")
        if cert.observacao:
            lines.append(f"  - Obs: {cert.observacao}")

    lines.append("")
    if not resultado.cnpj_encontrado_base_tcu:
        lines.append("*CNPJ não encontrado na base do TCU.*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# calcular_debito_tcu
# ---------------------------------------------------------------------------


async def calcular_debito_tcu(
    data_atualizacao: str,
    data_fato: str,
    valor_original: float,
    ctx: Context,
    aplica_juros: bool = True,
    tipo: str = "D",
) -> str:
    """Calcula débito atualizado com correção monetária (variação SELIC).

    Usa a calculadora oficial do TCU para atualizar valores de débitos
    apurados em processos de controle externo. Aplica correção monetária
    pela variação da taxa SELIC e, opcionalmente, juros de mora.

    Args:
        data_atualizacao: Data de atualização no formato DD/MM/AAAA.
        data_fato: Data do fato gerador no formato DD/MM/AAAA.
        valor_original: Valor original do débito em reais.
        ctx: Contexto MCP.
        aplica_juros: Se deve aplicar juros de mora (padrão: True).
        tipo: "D" para débito, "C" para crédito (padrão: "D").

    Returns:
        Detalhamento do cálculo com valor atualizado.
    """
    await ctx.info("Calculando débito atualizado no TCU...")
    parcela = ParcelaDebito(
        data_fato=data_fato,
        indicativo_debito_credito=tipo,
        valor_original=valor_original,
    )
    resultado = await client.calcular_debito(
        data_atualizacao=data_atualizacao,
        aplica_juros=aplica_juros,
        parcelas=[parcela],
    )

    lines = [
        "## Cálculo de Débito — TCU\n",
        f"- **Data do fato:** {data_fato}",
        f"- **Data de atualização:** {resultado.data or data_atualizacao}",
        f"- **Valor original:** {format_brl(valor_original)}",
        f"- **Correção monetária (SELIC):** {format_brl(resultado.saldo_variacao_selic)}",
        f"- **Juros de mora:** {format_brl(resultado.saldo_juros)}",
        f"- **Valor total atualizado:** {format_brl(resultado.saldo_total)}",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# buscar_pedidos_congresso
# ---------------------------------------------------------------------------


async def buscar_pedidos_congresso(
    ctx: Context,
    processo: str | None = None,
    page: int | None = None,
) -> str:
    """Busca solicitações do Congresso Nacional ao TCU.

    Requerimentos e solicitações de informação feitos por parlamentares
    ao Tribunal de Contas da União. Permite buscar por processo específico
    ou listar todos os pedidos.

    Args:
        ctx: Contexto MCP.
        processo: Número do processo TCU para filtrar (ex: "004.808/2026-6").
        page: Página dos resultados.

    Returns:
        Lista de pedidos com autor, assunto e links.
    """
    await ctx.info("Buscando pedidos do Congresso ao TCU...")
    resultado = await client.buscar_pedidos_congresso(processo=processo, page=page)

    if not resultado.items:
        return "Nenhum pedido do Congresso encontrado."

    lines: list[str] = [f"**{len(resultado.items)} pedido(s) do Congresso:**\n"]
    for item in resultado.items[:20]:
        lines.append(f"### {item.tipo or '—'} nº {item.numero or '—'}")
        lines.append(f"- **Autor:** {item.autor or '—'}")
        lines.append(f"- **Processo:** {item.processo_scn or '—'}")
        if item.data_aprovacao:
            lines.append(f"- **Data aprovação:** {item.data_aprovacao}")
        if item.assunto:
            assunto = item.assunto[:300] + "..." if len(item.assunto) > 300 else item.assunto
            lines.append(f"- **Assunto:** {assunto}")
        lines.append("")

    if resultado.has_next:
        next_page = (page or 0) + 1
        lines.append(f"*Mais resultados. Use page={next_page} para próxima página.*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# buscar_contratos_tcu
# ---------------------------------------------------------------------------


async def buscar_contratos_tcu(ctx: Context) -> str:
    """Busca contratos e termos contratuais firmados pelo próprio TCU.

    Retorna a lista completa de contratos do Tribunal de Contas da União,
    incluindo contratações por nota de empenho, pregões e dispensas.
    Útil para transparência dos gastos do próprio órgão de controle.

    Args:
        ctx: Contexto MCP.

    Returns:
        Lista resumida dos contratos mais recentes do TCU.
    """
    await ctx.info("Buscando contratos do TCU...")
    contratos = await client.buscar_contratos_tcu()

    if not contratos:
        return "Nenhum contrato do TCU encontrado."

    # Sort by year desc, show most recent
    contratos.sort(key=lambda c: (c.ano or 0, c.numero or 0), reverse=True)
    amostra = contratos[:20]

    lines: list[str] = [
        f"**{len(contratos)} contratos do TCU** (mostrando {len(amostra)} mais recentes):\n"
    ]
    for c in amostra:
        valor = format_brl(c.valor_atualizado) if c.valor_atualizado else "—"
        lines.append(f"### {c.numero or '—'}/{c.ano or '—'}")
        lines.append(f"- **Fornecedor:** {c.nome_fornecedor or '—'}")
        lines.append(f"- **Objeto:** {c.objeto or '—'}")
        lines.append(f"- **Valor atualizado:** {valor}")
        lines.append(f"- **Modalidade:** {c.modalidade_licitacao or '—'}")
        lines.append(f"- **Processo:** {c.numero_processo or '—'}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# consultar_cadirreg
# ---------------------------------------------------------------------------


async def consultar_cadirreg(cpf: str, ctx: Context) -> str:
    """Consulta pessoa no CADIRREG — Cadastro de Responsáveis com Contas Irregulares.

    Verifica se um CPF possui contas julgadas irregulares pelo TCU.
    Pessoas neste cadastro tiveram suas contas reprovadas em processos
    de controle externo.

    Args:
        cpf: CPF da pessoa (somente números, 11 dígitos).
        ctx: Contexto MCP.

    Returns:
        Dados das contas irregulares ou confirmação de nada consta.
    """
    await ctx.info(f"Consultando CADIRREG para CPF {cpf}...")
    registros = await client.consultar_cadirreg(cpf)

    if not registros:
        return f"CPF {cpf} **não consta** no CADIRREG do TCU."

    lines: list[str] = [f"**{len(registros)} registro(s) no CADIRREG para CPF {cpf}:**\n"]
    for r in registros:
        lines.append(f"### {r.nome_responsavel or '—'}")
        lines.append(f"- **Processo:** {r.num_processo or '—'}/{r.ano_processo or '—'}")
        lines.append(f"- **Julgamento:** {r.julgamento or '—'}")
        lines.append(f"- **Unidade técnica:** {r.unidade_tecnica_processo or '—'}")
        if r.se_detentor_cargo_funcao_publica:
            lines.append(f"- **Detentor de cargo público:** {r.se_detentor_cargo_funcao_publica}")
        lines.append("")

    return "\n".join(lines)
