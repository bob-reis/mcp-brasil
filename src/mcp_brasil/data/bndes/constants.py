"""Constants for the BNDES feature."""

BNDES_CKAN_BASE = "https://dadosabertos.bndes.gov.br/api/3/action"

DATASTORE_SEARCH_URL = f"{BNDES_CKAN_BASE}/datastore_search"
PACKAGE_SHOW_URL = f"{BNDES_CKAN_BASE}/package_show"

# Resource IDs dos principais datasets
RESOURCE_OPERACOES_NAO_AUTO = "6f56b78c-510f-44b6-8274-78a5b7e931f4"
RESOURCE_OPERACOES_AUTO = "612faa0b-b6be-4b2c-9317-da5dc2c0b901"
RESOURCE_DESEMBOLSOS_UF = "51094971-4f4f-4c43-9912-3b2f1c9c60ed"

DEFAULT_LIMIT = 20

# Situações de contrato
SITUACOES_CONTRATO = {
    "CONTRATADO": "Em vigor",
    "LIQUIDADO": "Liquidado (encerrado)",
    "CANCELADO": "Cancelado",
    "INADIMPLENTE": "Inadimplente",
}
