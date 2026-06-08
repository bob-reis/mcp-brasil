"""Schemas for the OAB feature."""

from __future__ import annotations

from pydantic import BaseModel


class Advogado(BaseModel):
    nome: str | None = None
    numero_oab: str | None = None
    seccional: str | None = None
    situacao: str | None = None
    subtipo: str | None = None
