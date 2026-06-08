"""Feature SICONFI — Sistema de Informações Contábeis e Fiscais do Setor Público Brasileiro."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="siconfi",
    description=(
        "SICONFI — Sistema de Informações Contábeis e Fiscais do Setor Público Brasileiro "
        "(Tesouro Nacional): entes federativos, RREO (Relatório Resumido de Execução "
        "Orçamentária), RGF (Relatório de Gestão Fiscal) e contas anuais de estados, "
        "municípios e União."
    ),
    version="0.1.0",
    api_base="https://apidatalake.tesouro.gov.br/ords/siconfi/tt",
    requires_auth=False,
    tags=["siconfi", "orcamento", "fiscal", "municipios", "estados", "transparencia"],
)
