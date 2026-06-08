"""Schemas for the Querido Diário feature."""

from __future__ import annotations

from pydantic import BaseModel


class Gazette(BaseModel):
    data: str | None = None
    municipio: str | None = None
    uf: str | None = None
    edicao: str | None = None
    url: str | None = None
    trechos: list[str] = []


class GazetteSearchResult(BaseModel):
    municipio: str
    territory_id: str | None = None
    query: str
    total: int = 0
    gazettes: list[Gazette] = []
