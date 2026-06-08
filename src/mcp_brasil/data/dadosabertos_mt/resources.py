"""Static reference data for the DadosAbertos-MT feature."""

from __future__ import annotations

import json


def endpoints_disponiveis() -> str:
    """Endpoints disponíveis na API CKAN do Portal Dados Abertos MT."""
    endpoints = [
        {
            "ferramenta": "buscar_datasets_mt",
            "descricao": "Busca datasets por termo, organização ou tag",
            "filtros": ["query", "organizacao", "tag", "inicio", "limite"],
        },
        {
            "ferramenta": "detalhar_dataset_mt",
            "descricao": "Detalhes completos de um dataset com links de download",
            "filtros": ["dataset_id"],
        },
        {
            "ferramenta": "listar_organizacoes_mt",
            "descricao": "Organizações publicadoras com slugs para filtro",
            "filtros": [],
        },
        {
            "ferramenta": "listar_grupos_mt",
            "descricao": "Grupos temáticos (saúde, educação, segurança, etc.)",
            "filtros": [],
        },
        {
            "ferramenta": "listar_tags_mt",
            "descricao": "Tags dos datasets, com filtro por prefixo",
            "filtros": ["busca"],
        },
    ]
    return json.dumps(endpoints, ensure_ascii=False, indent=2)
