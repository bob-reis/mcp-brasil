"""Static reference data for the IOMAT-MT feature."""

from __future__ import annotations

import json


def endpoints_disponiveis() -> str:
    """Endpoints disponíveis na API IOMAT do Diário Oficial de Mato Grosso."""
    endpoints = [
        {
            "ferramenta": "buscar_publicacoes_mt",
            "descricao": "Busca full-text em todas as publicações do DO e DJ de MT",
            "filtros": ["termo", "data_inicio", "data_fim", "pagina", "limite"],
            "total_indexado": "110.000+ publicações",
        },
        {
            "ferramenta": "listar_edicoes_mt",
            "descricao": "Lista edições do Diário Oficial (id=1) ou Diário da Justiça (id=5)",
            "filtros": ["diario_id", "data", "pagina", "limite"],
        },
        {
            "ferramenta": "buscar_materias_mt",
            "descricao": "Lista matérias/artigos de uma edição específica",
            "filtros": ["diario_id", "edicao_id", "cliente_id"],
        },
        {
            "ferramenta": "listar_orgaos_mt",
            "descricao": "Lista órgãos publicantes (secretarias, prefeituras, câmaras, etc.)",
            "filtros": ["classificacao_id"],
        },
        {
            "ferramenta": "listar_classificacoes_mt",
            "descricao": "Lista tipos de órgãos para uso como filtro em listar_orgaos_mt",
            "filtros": [],
        },
    ]
    return json.dumps(endpoints, ensure_ascii=False, indent=2)


def diarios_disponiveis() -> str:
    """Diários disponíveis na API IOMAT de Mato Grosso."""
    diarios = [
        {
            "id": 1,
            "nome": "Diário Oficial",
            "sigla": "D.O.",
            "abreviacao": "diario_oficial",
            "cobertura": "Executivo estadual, secretarias, prefeituras, câmaras, autarquias",
        },
        {
            "id": 5,
            "nome": "Diário da Justiça",
            "sigla": "D.J.",
            "abreviacao": "diario_justica",
            "cobertura": "Poder Judiciário do Estado de Mato Grosso",
        },
    ]
    return json.dumps(diarios, ensure_ascii=False, indent=2)
