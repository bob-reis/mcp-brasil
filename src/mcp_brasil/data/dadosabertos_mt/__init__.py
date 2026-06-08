"""Feature DadosAbertos-MT — Portal de Dados Abertos de Mato Grosso (CKAN)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="dadosabertos_mt",
    description=(
        "Portal de Dados Abertos de Mato Grosso (dadosabertos.mt.gov.br): "
        "catálogo CKAN com datasets de secretarias estaduais, municípios e "
        "órgãos do governo de MT — saúde, educação, segurança, meio ambiente, "
        "economia e mais."
    ),
    version="0.1.0",
    api_base="https://dadosabertos.mt.gov.br/api/3/action",
    requires_auth=False,
    tags=["mt", "dados-abertos", "ckan", "datasets", "transparencia"],
)
