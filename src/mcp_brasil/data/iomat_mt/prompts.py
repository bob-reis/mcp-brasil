"""Analysis prompts for the IOMAT-MT feature."""

from __future__ import annotations


def monitorar_orgao_mt(orgao: str) -> str:
    """Monitoramento de publicações de um órgão no Diário Oficial MT.

    Busca e analisa todas as publicações recentes de um órgão público no
    Diário Oficial do Estado de Mato Grosso.

    Args:
        orgao: Nome do órgão, secretaria ou entidade
            (ex: "Secretaria de Saúde", "Prefeitura de Cuiabá").
    """
    return (
        f"Monitore as publicações de '{orgao}' no Diário Oficial de Mato Grosso:\n\n"
        "1. Use `buscar_publicacoes_mt` com o nome do órgão como termo"
        " para encontrar publicações recentes\n"
        "2. Use `listar_orgaos_mt` para encontrar o ID do órgão e confirmar o nome exato\n"
        "3. Use `listar_edicoes_mt` para ver as edições mais recentes do Diário Oficial\n"
        "4. Use `buscar_materias_mt` com o `cliente_id` do órgão"
        " para listar todas as matérias publicadas\n\n"
        "Consolide um relatório com:\n"
        "- Volume e frequência de publicações\n"
        "- Tipos de atos (licitações, contratos, nomeações, portarias)\n"
        "- Datas das publicações mais relevantes\n"
        "- Links para as edições completas\n"
    )


def investigar_licitacao_mt(termo: str) -> str:
    """Investigação de licitações publicadas no Diário Oficial MT.

    Busca e analisa publicações de licitações, pregões e dispensas no
    Diário Oficial do Estado de Mato Grosso.

    Args:
        termo: Termo de busca (empresa, objeto, número de pregão, CNPJ, etc.).
    """
    return (
        f"Investigue licitações relacionadas a '{termo}' no Diário Oficial MT:\n\n"
        "1. Use `buscar_publicacoes_mt` com o termo para encontrar publicações relevantes\n"
        "2. Refine a busca com `data_inicio` e `data_fim` se necessário\n"
        "3. Para publicações de interesse, use `listar_edicoes_mt` para localizar a edição\n"
        "4. Use `buscar_materias_mt` para obter o conteúdo completo das matérias da edição\n\n"
        "Analise e consolide:\n"
        "- Modalidades de licitação (pregão, tomada de preços, concorrência)\n"
        "- Valores estimados e homologados\n"
        "- Órgãos contratantes\n"
        "- Empresas vencedoras\n"
        "- Eventuais irregularidades ou dispensas injustificadas\n"
    )
