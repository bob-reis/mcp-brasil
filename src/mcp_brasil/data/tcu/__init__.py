"""Feature TCU — Tribunal de Contas da União (dados abertos)."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="tcu",
    description=(
        "Tribunal de Contas da União: acórdãos, licitantes inidôneos, "
        "inabilitados para função pública, certidões consolidadas (APF), "
        "cálculo de débito, pedidos do Congresso, contratos do TCU e CADIRREG."
    ),
    version="0.1.0",
    api_base="https://dados-abertos.apps.tcu.gov.br",
    requires_auth=False,
    tags=["tcu", "acordaos", "inidoneos", "inabilitados", "certidoes", "contratos"],
)
