"""Tool functions for the ANS feature."""

from __future__ import annotations

from mcp_brasil._shared.formatting import markdown_table
from mcp_brasil.exceptions import HttpClientError

from . import client
from .constants import MODALIDADES


async def buscar_operadoras_ans(
    nome: str | None = None,
    cnpj: str | None = None,
    modalidade: str | None = None,
    uf: str | None = None,
    limite: int = 20,
) -> str:
    """Busca operadoras de planos de saúde ativas cadastradas na ANS.

    Retorna operadoras com registro ANS, CNPJ, modalidade, localização e
    representante legal. Útil para verificar se uma empresa está autorizada
    a operar planos de saúde e obter seus dados cadastrais.

    Modalidades disponíveis:
    - "Medicina de Grupo" — plano médico coletivo empresarial
    - "Cooperativa Médica" — Unimed e similares
    - "Seguradora Especializada em Saúde"
    - "Odontologia de Grupo" — plano exclusivamente odontológico
    - "Cooperativa Odontológica"
    - "Autogestão" — plano próprio da empresa para funcionários
    - "Administradora de Benefícios"
    - "Filantropia"

    Args:
        nome: Nome (razão social ou fantasia) da operadora.
        cnpj: CNPJ da operadora (com ou sem pontuação).
        modalidade: Modalidade da operadora (parcial, ex: "Cooperativa").
        uf: Sigla do estado (ex: "SP", "RJ").
        limite: Máximo de resultados (padrão: 20).

    Returns:
        Tabela com operadoras encontradas e seus dados cadastrais.
    """
    if not any([nome, cnpj, modalidade, uf]):
        return "Informe ao menos um critério: nome, cnpj, modalidade ou uf."

    try:
        ops = await client.buscar_operadoras(
            nome=nome, cnpj=cnpj, modalidade=modalidade, uf=uf, limite=limite
        )
    except Exception as exc:
        return f"Erro ao consultar ANS: {exc}"

    if not ops:
        partes = []
        if nome:
            partes.append(f"nome='{nome}'")
        if cnpj:
            partes.append(f"CNPJ={cnpj}")
        if modalidade:
            partes.append(f"modalidade='{modalidade}'")
        if uf:
            partes.append(f"UF={uf}")
        return f"Nenhuma operadora encontrada para {', '.join(partes)}."

    rows = [
        (
            o.registro_ans or "—",
            o.cnpj or "—",
            (o.razao_social or "—")[:40],
            (o.modalidade or "—")[:30],
            o.uf or "—",
            (o.cidade or "—")[:20],
            o.data_registro_ans or "—",
        )
        for o in ops
    ]
    header = f"Operadoras ANS ativas ({len(ops)} encontradas):\n\n"
    return header + markdown_table(
        ["Registro ANS", "CNPJ", "Razão Social", "Modalidade", "UF", "Cidade", "Registro"],
        rows,
    )
