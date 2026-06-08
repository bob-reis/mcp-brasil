"""Feature Querido Diário — Diários Oficiais Municipais (Open Knowledge Brasil)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="querido_diario",
    description="Querido Diário (OKBr): busca em diários oficiais municipais — licitações, contratos, decretos",
    version="0.1.0",
    api_base="https://api.queridodiario.ok.org.br",
    requires_auth=False,
    tags=["diario-oficial", "municipios", "licitacoes", "transparencia", "querido-diario"],
)
