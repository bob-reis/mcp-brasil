"""Constants for the ANAC feature."""

ANAC_RAB_URL = (
    "https://sistemas.anac.gov.br/dadosabertos/Aeronaves/RAB/dados_aeronaves.csv"
)

CSV_ENCODING = "utf-8-sig"
CSV_DELIMITER = ";"

# Tipos de aeronave (CD_TIPO)
TIPOS_AERONAVE = {
    "AVIÃO": "Avião a motor",
    "HELICOPTERO": "Helicóptero",
    "PLANADOR": "Planador / veleiro",
    "BLAQ": "Balão",
    "AUTOGIRO": "Autogiro",
    "PARA": "Paraquedas motorizado",
    "ANFIBIO": "Anfíbio",
}

# Operações
TIPOS_OPERACAO = {
    "PRIVADA": "Uso privativo do proprietário",
    "TÁXI AÉREO": "Transporte remunerado não regular",
    "SERVIÇO AEREO ESPECIALIZADO": "Agrícola, fotografia, vigilância",
    "TRANSPORTE AÉREO REGULAR": "Companhia aérea regular",
}
