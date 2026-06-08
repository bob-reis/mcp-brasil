"""Feature CVM — Comissão de Valores Mobiliários."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="cvm",
    description=(
        "CVM — Comissão de Valores Mobiliários: companhias abertas, fundos de investimento "
        "(FIIs, ações, multimercado), processos administrativos sancionadores (PAS) e dados "
        "do mercado de capitais brasileiro."
    ),
    version="0.1.0",
    api_base="https://dados.cvm.gov.br",
    requires_auth=False,
    tags=["cvm", "mercado-capitais", "fundos", "acoes", "compliance", "sancoes"],
)
