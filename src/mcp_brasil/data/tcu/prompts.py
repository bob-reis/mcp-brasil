"""Analysis prompts for the TCU feature."""

from __future__ import annotations


def investigar_empresa_tcu(cnpj: str) -> str:
    """Investigação completa de empresa nos cadastros do TCU.

    Verifica a situação de uma empresa em todos os cadastros de
    sanções do TCU, incluindo inidoneidade, certidões consolidadas
    e contratos com o tribunal.

    Args:
        cnpj: CNPJ da empresa (somente números, 14 dígitos).
    """
    return (
        f"Investigue a empresa com CNPJ {cnpj} nos cadastros do TCU:\n\n"
        "1. Use `consultar_certidoes_apf` para verificar a situação "
        "consolidada em 4 cadastros (TCU Inidôneos, CNJ CNIA, CGU CEIS, CGU CNEP)\n"
        "2. Use `consultar_inidoneos` com o CNPJ para verificar se a empresa "
        "está na lista de licitantes inidôneos\n"
        "3. Apresente um resumo claro da situação da empresa:\n"
        "   - Se possui restrições em algum cadastro\n"
        "   - Detalhes das sanções encontradas\n"
        "   - Se está apta a participar de licitações públicas\n"
    )
