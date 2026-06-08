"""Feature ANS — Agência Nacional de Saúde Suplementar."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="ans",
    description=(
        "ANS — Agência Nacional de Saúde Suplementar: operadoras de planos de saúde "
        "ativas no Brasil. Permite buscar operadoras por nome, CNPJ, modalidade "
        "(médico-hospitalar, odontológica, administradora de benefícios) e estado."
    ),
    version="0.1.0",
    api_base="https://dadosabertos.ans.gov.br",
    requires_auth=False,
    tags=["ans", "saude", "planos-de-saude", "operadoras", "convenio"],
)
