"""Schemas for the BNMP (CNJ) feature."""

from __future__ import annotations

from pydantic import BaseModel


class MandadoPrisao(BaseModel):
    nome: str | None = None
    tipo_peca: str | None = None
    orgao_expeditor: str | None = None
    data_expedicao: str | None = None
    situacao: str | None = None
    municipio: str | None = None
    uf: str | None = None
