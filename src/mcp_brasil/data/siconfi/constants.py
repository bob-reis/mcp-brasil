"""Constants for the SICONFI feature."""

SICONFI_API_BASE = "https://apidatalake.tesouro.gov.br/ords/siconfi/tt"

ENTES_URL = f"{SICONFI_API_BASE}/entes"
RREO_URL = f"{SICONFI_API_BASE}/rreo"
RGF_URL = f"{SICONFI_API_BASE}/rgf"
DCA_URL = f"{SICONFI_API_BASE}/dca"

DEFAULT_LIMIT = 100

# Esferas de governo
ESFERAS = {
    "E": "Estadual",
    "M": "Municipal",
    "U": "Federal (União)",
    "D": "Distrital",
}

# Poderes
PODERES = {
    "E": "Executivo",
    "L": "Legislativo",
    "J": "Judiciário",
    "M": "Ministério Público",
    "D": "Defensoria",
}

# Anexos RREO mais usados
ANEXOS_RREO = {
    "RREO-Anexo 01": "Receitas Orçamentárias",
    "RREO-Anexo 02": "Despesas por Função/Subfunção",
    "RREO-Anexo 03": "Demonstrativo da Receita Corrente Líquida",
    "RREO-Anexo 06": "Despesas por Função/Subfunção (Educação e Saúde)",
}

# Anexos RGF mais usados
ANEXOS_RGF = {
    "RGF-Anexo 01": "Demonstrativo da Despesa com Pessoal",
    "RGF-Anexo 02": "Demonstrativo da Dívida Consolidada Líquida",
    "RGF-Anexo 03": "Demonstrativo das Garantias e Contragarantias",
    "RGF-Anexo 04": "Demonstrativo das Operações de Crédito",
}
