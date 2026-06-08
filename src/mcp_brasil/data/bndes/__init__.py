"""Feature BNDES — Banco Nacional de Desenvolvimento Econômico e Social."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="bndes",
    description=(
        "BNDES — Banco Nacional de Desenvolvimento Econômico e Social: operações de "
        "financiamento não-automáticas contratadas com empresas e entes públicos. "
        "Permite buscar contratos por beneficiário, CNPJ, estado, setor e situação."
    ),
    version="0.1.0",
    api_base="https://dadosabertos.bndes.gov.br",
    requires_auth=False,
    tags=["bndes", "financiamento", "desenvolvimento", "credito", "contratos"],
)
