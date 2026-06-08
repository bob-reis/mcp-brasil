"""Feature IOMAT-MT — Diário Oficial do Estado de Mato Grosso."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="iomat_mt",
    description=(
        "Diário Oficial do Estado de Mato Grosso via IOMAT: busca textual em publicações, "
        "edições do Diário Oficial e Diário da Justiça, matérias por edição e "
        "órgãos publicantes."
    ),
    version="0.1.0",
    api_base="https://api.iomat.mt.gov.br/transparencia/v1",
    requires_auth=False,
    tags=["mt", "diario-oficial", "diario-justica", "publicacoes", "licitacoes", "transparencia"],
)
