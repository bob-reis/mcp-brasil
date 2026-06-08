"""Feature OAB — Cadastro Nacional de Advogados."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="oab",
    description="OAB: consulta de advogados por nome, número de inscrição ou seccional",
    version="0.1.0",
    api_base="https://cna.oab.org.br",
    requires_auth=False,
    tags=["juridico", "oab", "advogados", "cadastro"],
)
