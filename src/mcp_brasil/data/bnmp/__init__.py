"""Feature BNMP — Banco Nacional de Mandados de Prisão (CNJ)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="bnmp",
    description="BNMP (CNJ): mandados de prisão ativos e histórico — busca por nome",
    version="0.1.0",
    api_base="https://portalbnmp.cnj.jus.br",
    requires_auth=False,
    tags=["judiciario", "cnj", "prisao", "mandados", "seguranca-publica"],
)
