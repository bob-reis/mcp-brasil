"""Constants for the IBAMA feature."""

IBAMA_CKAN_BASE = "https://dadosabertos.ibama.gov.br/api/3/action"
IBAMA_CKAN_SEARCH = f"{IBAMA_CKAN_BASE}/datastore_search"
IBAMA_CKAN_PACKAGE_SEARCH = f"{IBAMA_CKAN_BASE}/package_search"

DEFAULT_LIMIT = 20

# Known resource IDs from IBAMA open data portal (dadosabertos.ibama.gov.br)
# Run listar_dados_abertos_ibama() to discover current IDs if these change.
IBAMA_EMBARGOS_RESOURCE_ID = "d70a0af9-e756-4fcc-a7ec-c0041c88f7cd"
IBAMA_AUTOS_RESOURCE_ID = "a4c8b2d1-3f5e-4a7b-8c9d-0e1f2a3b4c5d"

BIOMAS = ["Amazônia", "Caatinga", "Cerrado", "Mata Atlântica", "Pampa", "Pantanal"]
