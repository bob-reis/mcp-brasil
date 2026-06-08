"""Constants for the IOMAT-MT feature."""

API_BASE = "https://api.iomat.mt.gov.br/transparencia/v1"

BUSCAS_URL = f"{API_BASE}/buscas"
DIARIOS_URL = f"{API_BASE}/diarios"
CLIENTES_URL = f"{API_BASE}/clientes"
CLASSIFICACOES_URL = f"{API_BASE}/classificacoes"

# IDs dos diários conforme retornado pela API
DIARIO_OFICIAL_ID = 1
DIARIO_JUSTICA_ID = 5

DIARIOS_NOMES = {
    1: "Diário Oficial",
    5: "Diário da Justiça",
}

DEFAULT_LIMITE = 20
MAX_LIMITE = 100
