"""HTTP client for the ANAC RAB open data (CSV download).

Source: https://sistemas.anac.gov.br/dadosabertos/Aeronaves/RAB/
Updated: daily. ~12MB, ~18800 registered aircraft.

The CSV has a metadata header on the first line ("Atualizado em: YYYY-MM-DD")
that must be skipped before parsing.
"""

from __future__ import annotations

import csv
import io
import logging

import httpx

from .constants import ANAC_RAB_URL, CSV_DELIMITER, CSV_ENCODING
from .schemas import AeronaveRAB

logger = logging.getLogger(__name__)


def _parse_aeronave(row: dict[str, str]) -> AeronaveRAB:
    return AeronaveRAB(
        marcas=row.get("MARCAS", "").strip() or None,
        proprietarios=row.get("PROPRIETARIOS", "").strip() or None,
        operadores=row.get("OPERADORES", "").strip() or None,
        nr_certificado=row.get("NR_CERT_MATRICULA", "").strip() or None,
        tipo=row.get("CD_TIPO", "").strip() or None,
        modelo=row.get("DS_MODELO", "").strip() or None,
        fabricante=row.get("NM_FABRICANTE", "").strip() or None,
        ano_fabricacao=row.get("NR_ANO_FABRICACAO", "").strip() or None,
        nr_passageiros_max=row.get("NR_PASSAGEIROS_MAX", "").strip() or None,
        nr_assentos=row.get("NR_ASSENTOS", "").strip() or None,
        tp_motor=row.get("TP_MOTOR", "").strip() or None,
        qt_motor=row.get("QT_MOTOR", "").strip() or None,
        tp_operacao=row.get("TP_OPERACAO", "").strip() or None,
        categoria_homologacao=row.get("DS_CATEGORIA_HOMOLOGACAO", "").strip() or None,
        dt_matricula=row.get("DT_MATRICULA", "").strip() or None,
        dt_canc=row.get("DT_CANC", "").strip() or None,
        motivo_canc=row.get("DS_MOTIVO_CANC", "").strip() or None,
        interdicao=row.get("CD_INTERDICAO", "").strip() or None,
        gravame=row.get("DS_GRAVAME", "").strip() or None,
    )


async def buscar_aeronaves(
    *,
    marcas: str | None = None,
    proprietario: str | None = None,
    cnpj_cpf: str | None = None,
    modelo: str | None = None,
    fabricante: str | None = None,
    tipo: str | None = None,
    operacao: str | None = None,
    apenas_ativas: bool = True,
    limite: int = 20,
) -> list[AeronaveRAB]:
    """Download and filter ANAC aircraft registry (RAB).

    Args:
        marcas: Aircraft prefix/registration mark (e.g. "PP-XPT", partial ok).
        proprietario: Owner name (partial match).
        cnpj_cpf: CNPJ or CPF of owner/operator (digits only or formatted).
        modelo: Aircraft model (partial match, e.g. "C172", "737").
        fabricante: Manufacturer name (partial match, e.g. "CESSNA", "BOEING").
        tipo: Aircraft type: "AVIÃO", "HELICOPTERO", "PLANADOR", "BLAQ".
        operacao: Operation type: "PRIVADA", "TÁXI AÉREO", "SERVIÇO AEREO".
        apenas_ativas: If True (default), exclude cancelled aircraft.
        limite: Max results.
    """
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.get(ANAC_RAB_URL)
        resp.raise_for_status()

    # Skip first metadata line ("Atualizado em: YYYY-MM-DD")
    raw = resp.content.decode(CSV_ENCODING, errors="replace")
    lines = raw.splitlines()
    data = "\n".join(lines[1:]) if lines and not lines[0].startswith('"MARCAS"') else raw

    reader = csv.DictReader(io.StringIO(data), delimiter=CSV_DELIMITER)

    doc_digits = "".join(c for c in (cnpj_cpf or "") if c.isdigit())
    marcas_upper = (marcas or "").upper().strip()
    prop_lower = (proprietario or "").lower().strip()
    modelo_upper = (modelo or "").upper().strip()
    fab_upper = (fabricante or "").upper().strip()
    tipo_upper = (tipo or "").upper().strip()
    op_upper = (operacao or "").upper().strip()

    results: list[AeronaveRAB] = []
    for row in reader:
        # Filter cancelled if requested
        if apenas_ativas and row.get("DT_CANC", "").strip():
            continue

        if marcas_upper and marcas_upper not in row.get("MARCAS", "").upper():
            continue

        if prop_lower:
            props = row.get("PROPRIETARIOS", "").lower()
            ops = row.get("OPERADORES", "").lower()
            if prop_lower not in props and prop_lower not in ops:
                continue

        if doc_digits:
            props_raw = row.get("PROPRIETARIOS", "") + row.get("OPERADORES", "")
            if doc_digits not in "".join(c for c in props_raw if c.isdigit()):
                continue

        if modelo_upper and modelo_upper not in row.get("DS_MODELO", "").upper():
            continue

        if fab_upper and fab_upper not in row.get("NM_FABRICANTE", "").upper():
            continue

        if tipo_upper and tipo_upper not in row.get("CD_TIPO", "").upper():
            continue

        if op_upper and op_upper not in row.get("TP_OPERACAO", "").upper():
            continue

        results.append(_parse_aeronave(row))
        if len(results) >= limite:
            break

    return results
