"""Constants for the ANS feature."""

ANS_CADOP_URL = (
    "https://dadosabertos.ans.gov.br/FTP/PDA/"
    "operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
)

CSV_ENCODING = "utf-8-sig"
CSV_DELIMITER = ";"

# Modalidades de operadoras
MODALIDADES = {
    "Medicina de Grupo": "Plano médico coletivo via grupo empresarial",
    "Cooperativa Médica": "Cooperativa de médicos (Unimed e similares)",
    "Seguradora Especializada em Saúde": "Seguradora autorizada a operar planos",
    "Odontologia de Grupo": "Plano exclusivamente odontológico",
    "Cooperativa Odontológica": "Cooperativa de dentistas",
    "Autogestão": "Plano administrado pela própria empresa para funcionários",
    "Administradora de Benefícios": "Administra planos de terceiros",
    "Filantropia": "Entidade sem fins lucrativos",
}
