"""Tool functions for the ANAC feature."""

from __future__ import annotations

from mcp_brasil._shared.formatting import markdown_table

from . import client


async def buscar_aeronaves_anac(
    marcas: str | None = None,
    proprietario: str | None = None,
    cnpj_cpf: str | None = None,
    modelo: str | None = None,
    fabricante: str | None = None,
    tipo: str | None = None,
    operacao: str | None = None,
    apenas_ativas: bool = True,
    limite: int = 20,
) -> str:
    """Busca aeronaves registradas no RAB (Registro Aeronáutico Brasileiro) da ANAC.

    O RAB é o cadastro oficial de todas as aeronaves matriculadas no Brasil.
    Permite verificar se uma empresa ou pessoa possui aeronaves registradas,
    identificar frotas corporativas, investigar propriedade de aeronaves e
    obter dados técnicos como modelo, capacidade e tipo de operação.

    O campo `proprietarios` é formatado como: NOME|CNPJ_OU_CPF|PARTICIPACAO|UF

    Args:
        marcas: Prefixo de registro da aeronave (ex: "PP-XPT", "PT-", parcial ok).
        proprietario: Nome do proprietário ou operador (busca parcial).
        cnpj_cpf: CNPJ ou CPF do proprietário/operador (com ou sem pontuação).
        modelo: Modelo da aeronave (ex: "C172", "737", "ROBINSON R44").
        fabricante: Fabricante (ex: "CESSNA", "BOEING", "EMBRAER", "ROBINSON").
        tipo: Tipo: "AVIÃO", "HELICOPTERO", "PLANADOR", "BLAQ" (balão).
        operacao: Tipo de operação: "PRIVADA", "TÁXI AÉREO", "SERVIÇO AEREO".
        apenas_ativas: Se True (padrão), exclui aeronaves canceladas/baixadas.
        limite: Máximo de resultados (padrão: 20).

    Returns:
        Tabela com aeronaves encontradas e seus dados cadastrais.
    """
    if not any([marcas, proprietario, cnpj_cpf, modelo, fabricante, tipo, operacao]):
        return (
            "Informe ao menos um critério: marcas, proprietario, cnpj_cpf, "
            "modelo, fabricante, tipo ou operacao."
        )

    try:
        aeronaves = await client.buscar_aeronaves(
            marcas=marcas,
            proprietario=proprietario,
            cnpj_cpf=cnpj_cpf,
            modelo=modelo,
            fabricante=fabricante,
            tipo=tipo,
            operacao=operacao,
            apenas_ativas=apenas_ativas,
            limite=limite,
        )
    except Exception as exc:
        return f"Erro ao consultar ANAC RAB: {exc}"

    if not aeronaves:
        partes = []
        if marcas:
            partes.append(f"marcas='{marcas}'")
        if proprietario:
            partes.append(f"proprietario='{proprietario}'")
        if cnpj_cpf:
            partes.append(f"CNPJ/CPF={cnpj_cpf}")
        if modelo:
            partes.append(f"modelo='{modelo}'")
        if fabricante:
            partes.append(f"fabricante='{fabricante}'")
        status = " (apenas ativas)" if apenas_ativas else ""
        return f"Nenhuma aeronave encontrada para {', '.join(partes)}{status}."

    rows = []
    for a in aeronaves:
        # Extract owner name from pipe-separated format NAME|CNPJ|%|UF
        prop_nome = (a.proprietarios or "").split("|")[0][:35]
        rows.append((
            a.marcas or "—",
            (a.modelo or "—")[:20],
            (a.fabricante or "—")[:20],
            a.tipo or "—",
            a.ano_fabricacao or "—",
            a.tp_operacao or "—",
            prop_nome or "—",
        ))

    status_txt = "ativas" if apenas_ativas else "todas"
    header = f"Aeronaves no RAB/ANAC ({len(aeronaves)} {status_txt} encontradas):\n\n"
    return header + markdown_table(
        ["Marcas", "Modelo", "Fabricante", "Tipo", "Ano", "Operação", "Proprietário"],
        rows,
    )
