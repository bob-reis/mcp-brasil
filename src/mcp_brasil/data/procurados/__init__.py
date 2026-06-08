"""Feature Procurados — Interpol Red Notices e Polícia Federal."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="procurados",
    description="Procurados: Interpol Red Notices e busca de foragidos da Polícia Federal",
    version="0.1.0",
    api_base="https://ws-public.interpol.int",
    requires_auth=False,
    tags=["seguranca-publica", "interpol", "policia-federal", "procurados", "foragidos"],
)
