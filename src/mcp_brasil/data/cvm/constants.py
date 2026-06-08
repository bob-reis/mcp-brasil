"""Constants for the CVM feature."""

CVM_CKAN_BASE = "https://dados.cvm.gov.br/api/3/action"
CVM_CKAN_SEARCH = f"{CVM_CKAN_BASE}/datastore_search"
CVM_CKAN_PACKAGE_SEARCH = f"{CVM_CKAN_BASE}/package_search"

DEFAULT_LIMIT = 20

# Known CVM CKAN resource IDs (dados.cvm.gov.br)
# Run buscar_datasets_cvm() to discover current IDs if these need to be updated.
CVM_CIA_ABERTA_RESOURCE_ID = "9c03abdb-2ed6-4b6b-844c-a4fc0a1e4f0d"
CVM_PAS_RESOURCE_ID = "e5e78eb5-7c98-4ffd-a9a1-db49bcb01e10"
CVM_FI_RESOURCE_ID = "eb51acab-1e77-4a7f-b6f2-f9023e8ec9e3"

CLASSES_FUNDO = [
    "Renda Fixa",
    "Ações",
    "Multimercado",
    "Cambial",
    "Fundo Imobiliário",
    "FIDC",
    "Previdência",
]
