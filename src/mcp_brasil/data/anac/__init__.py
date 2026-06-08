"""Feature ANAC — Agência Nacional de Aviação Civil."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="anac",
    description=(
        "ANAC — Agência Nacional de Aviação Civil: aeronaves registradas no Brasil "
        "(RAB — Registro Aeronáutico Brasileiro). Permite buscar aeronaves por marca "
        "(prefixo), proprietário, CNPJ/CPF, modelo, fabricante, tipo e situação."
    ),
    version="0.1.0",
    api_base="https://sistemas.anac.gov.br/dadosabertos",
    requires_auth=False,
    tags=["anac", "aviacao", "aeronaves", "rab", "frota-aerea"],
)
