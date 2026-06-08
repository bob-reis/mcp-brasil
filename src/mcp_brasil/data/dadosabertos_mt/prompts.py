"""Analysis prompts for the DadosAbertos-MT feature."""

from __future__ import annotations


def explorar_tema_mt(tema: str) -> str:
    """Exploração de datasets de um tema no Portal Dados Abertos MT.

    Descobre e analisa todos os datasets disponíveis sobre um tema
    no catálogo do governo de Mato Grosso.

    Args:
        tema: Tema de interesse (ex: "saúde", "educação", "segurança", "meio ambiente").
    """
    return (
        f"Explore os dados disponíveis sobre '{tema}' no Portal Dados Abertos MT:\n\n"
        "1. Use `listar_grupos_mt` para identificar o grupo temático correspondente\n"
        f"2. Use `buscar_datasets_mt` com query='{tema}' para listar datasets relevantes\n"
        "3. Para datasets de interesse, use `detalhar_dataset_mt` para ver os recursos\n"
        "4. Use `listar_organizacoes_mt` para identificar quais órgãos publicam sobre o tema\n\n"
        "Consolide um inventário com:\n"
        "- Datasets disponíveis e suas fontes\n"
        "- Formatos e frequência de atualização\n"
        "- Links de download dos principais recursos\n"
        "- Gaps ou dados ausentes identificados\n"
    )
