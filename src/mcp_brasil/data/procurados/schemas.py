"""Schemas for the Procurados (Interpol + PF) feature."""

from __future__ import annotations

from pydantic import BaseModel


class InterpolNotice(BaseModel):
    nome: str | None = None
    nacionalidade: str | None = None
    data_nascimento: str | None = None
    link: str | None = None
    fonte: str = "Interpol Red Notice"
