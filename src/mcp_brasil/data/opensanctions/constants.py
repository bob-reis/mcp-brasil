"""Constants for the OpenSanctions feature."""

import os

OPENSANCTIONS_API_BASE = "https://api.opensanctions.org"
AUTH_ENV_VAR = "OPENSANCTIONS_API_KEY"

SEARCH_URL = f"{OPENSANCTIONS_API_BASE}/search/default"
MATCH_URL = f"{OPENSANCTIONS_API_BASE}/match/default"
ENTITY_URL = f"{OPENSANCTIONS_API_BASE}/entities"
DATASETS_URL = f"{OPENSANCTIONS_API_BASE}/datasets"

DEFAULT_LIMIT = 10

# Datasets disponíveis agrupados por categoria
DATASETS_SANCOES = {
    "ofac_sdn": "OFAC SDN List (EUA — sanções principais)",
    "ofac_cons": "OFAC Consolidated List (EUA — sanções secundárias)",
    "eu_fsf": "União Europeia — Financial Sanctions Files",
    "un_sc_sanctions": "ONU — Conselho de Segurança",
    "worldbank_debarred": "Banco Mundial — empresas desabilitadas",
    "interpol_red_notices": "Interpol — notificações vermelhas",
    "gb_hmt_sanctions": "Reino Unido — HMT Financial Sanctions",
    "ch_seco_sanctions": "Suíça — SECO Sanctions",
}

DATASETS_PEPS = {
    "peps": "PEPs globais consolidados",
    "br_tse_candidates": "Candidatos TSE — Brasil",
    "br_cgu_pep": "CGU PEP — Brasil",
    "every_politician": "Every Politician — cargos eletivos globais",
    "wd_peppercat": "Wikidata PEPs — personagens públicos",
}

# Tipos de entidade (schema FtM)
SCHEMA_TYPES = {
    "Person": "Pessoa física",
    "Company": "Empresa ou organização",
    "LegalEntity": "Pessoa física ou jurídica",
    "Vessel": "Embarcação",
    "Aircraft": "Aeronave",
    "Asset": "Ativo/bem",
}

# Tópicos de filtragem
TOPICS = {
    "sanction": "Entidade sancionada",
    "pep": "Pessoa Politicamente Exposta",
    "crime": "Suspeito de crime",
    "debarment": "Desabilitado (licitações/contratos)",
    "terrorism": "Terrorismo",
    "proliferation": "Proliferação de armas",
    "drugs": "Narcotráfico",
}


def _get_api_key() -> str:
    """Return the OpenSanctions API key."""
    return os.environ.get(AUTH_ENV_VAR, "")
