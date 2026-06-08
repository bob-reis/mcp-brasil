"""Static reference data for the TCU feature."""

from __future__ import annotations

import json


def tipos_certidoes_apf() -> str:
    """Tipos de certidões consolidadas disponíveis no sistema APF do TCU.

    O sistema APF (Administração Pública Federal) consulta 4 cadastros
    de sanções simultaneamente para verificar a situação de uma empresa.
    """
    tipos = [
        {
            "orgao_emissor": "TCU",
            "sigla": "Inidoneos",
            "descricao": "Licitantes Inidôneos — empresas/pessoas declaradas "
            "inidôneas pelo TCU para participar de licitações",
        },
        {
            "orgao_emissor": "CNJ",
            "sigla": "CNIA",
            "descricao": "Cadastro Nacional de Condenações Cíveis por Ato de "
            "Improbidade Administrativa e Inelegibilidade",
        },
        {
            "orgao_emissor": "Portal da Transparência",
            "sigla": "CEIS",
            "descricao": "Cadastro Nacional de Empresas Inidôneas e Suspensas — mantido pela CGU",
        },
        {
            "orgao_emissor": "Portal da Transparência",
            "sigla": "CNEP",
            "descricao": "Cadastro Nacional de Empresas Punidas — mantido pela CGU",
        },
    ]
    return json.dumps(tipos, ensure_ascii=False, indent=2)
