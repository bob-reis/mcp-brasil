"""HTTP client for the ANS open data (CSV download).

Source: https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/
Updated: daily. ~339KB, ~1100 active operators.
"""

from __future__ import annotations

import csv
import io
import logging

import httpx

from .constants import ANS_CADOP_URL, CSV_DELIMITER, CSV_ENCODING
from .schemas import OperadoraANS

logger = logging.getLogger(__name__)


def _parse_operadora(row: dict[str, str]) -> OperadoraANS:
    ddd = row.get("DDD", "").strip()
    tel = row.get("Telefone", "").strip()
    telefone = f"({ddd}) {tel}" if ddd and tel else tel or None

    return OperadoraANS(
        registro_ans=row.get("REGISTRO_OPERADORA", "").strip() or None,
        cnpj=row.get("CNPJ", "").strip() or None,
        razao_social=row.get("Razao_Social", "").strip() or None,
        nome_fantasia=row.get("Nome_Fantasia", "").strip() or None,
        modalidade=row.get("Modalidade", "").strip() or None,
        logradouro=row.get("Logradouro", "").strip() or None,
        numero=row.get("Numero", "").strip() or None,
        complemento=row.get("Complemento", "").strip() or None,
        bairro=row.get("Bairro", "").strip() or None,
        cidade=row.get("Cidade", "").strip() or None,
        uf=row.get("UF", "").strip() or None,
        cep=row.get("CEP", "").strip() or None,
        telefone=telefone,
        email=row.get("Endereco_eletronico", "").strip() or None,
        representante=row.get("Representante", "").strip() or None,
        data_registro_ans=row.get("Data_Registro_ANS", "").strip() or None,
    )


async def buscar_operadoras(
    *,
    nome: str | None = None,
    cnpj: str | None = None,
    modalidade: str | None = None,
    uf: str | None = None,
    limite: int = 20,
) -> list[OperadoraANS]:
    """Download and filter ANS active health plan operators.

    Args:
        nome: Partial name search (razao_social or nome_fantasia).
        cnpj: CNPJ filter (digits only or formatted).
        modalidade: Operator modality (partial match).
        uf: State abbreviation (e.g. "SP").
        limite: Max results.
    """
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(ANS_CADOP_URL)
        resp.raise_for_status()

    content = resp.content.decode(CSV_ENCODING, errors="replace")
    reader = csv.DictReader(io.StringIO(content), delimiter=CSV_DELIMITER)

    cnpj_digits = "".join(c for c in (cnpj or "") if c.isdigit())
    nome_lower = (nome or "").lower().strip()
    mod_lower = (modalidade or "").lower().strip()
    uf_upper = (uf or "").upper().strip()

    results: list[OperadoraANS] = []
    for row in reader:
        if cnpj_digits:
            row_cnpj = "".join(c for c in row.get("CNPJ", "") if c.isdigit())
            if cnpj_digits not in row_cnpj:
                continue
        if nome_lower:
            razao = row.get("Razao_Social", "").lower()
            fantasia = row.get("Nome_Fantasia", "").lower()
            if nome_lower not in razao and nome_lower not in fantasia:
                continue
        if mod_lower:
            if mod_lower not in row.get("Modalidade", "").lower():
                continue
        if uf_upper:
            if row.get("UF", "").strip().upper() != uf_upper:
                continue

        results.append(_parse_operadora(row))
        if len(results) >= limite:
            break

    return results
