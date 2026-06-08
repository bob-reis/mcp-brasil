"""Feature IBAMA — fiscalização ambiental e áreas embargadas."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="ibama",
    description=(
        "IBAMA — Instituto Brasileiro do Meio Ambiente e dos Recursos Naturais Renováveis: "
        "áreas embargadas, autos de infração e dados de fiscalização ambiental. "
        "Permite verificar embargos e infrações por CPF/CNPJ, estado ou bioma."
    ),
    version="0.1.0",
    api_base="https://dadosabertos.ibama.gov.br",
    requires_auth=False,
    tags=["ibama", "ambiental", "embargo", "fiscalizacao", "infracao", "desmatamento"],
)
