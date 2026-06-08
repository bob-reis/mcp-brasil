"""Feature OpenSanctions — sanções internacionais e PEPs globais."""

from mcp_brasil._shared.feature import FeatureMeta

FEATURE_META = FeatureMeta(
    name="opensanctions",
    description=(
        "OpenSanctions — base consolidada de sanções internacionais e pessoas "
        "politicamente expostas (PEPs): OFAC (EUA), ONU, União Europeia, Banco Mundial, "
        "Interpol e 400+ outras listas. Mais de 300K entidades sancionadas ou monitoradas."
    ),
    version="0.1.0",
    api_base="https://api.opensanctions.org",
    requires_auth=True,
    auth_env_var="OPENSANCTIONS_API_KEY",
    tags=["sancoes", "pep", "compliance", "ofac", "onu", "anticorrupcao", "kyc"],
)
