"""Pydantic schemas for the SICONFI feature."""

from __future__ import annotations

from pydantic import BaseModel


class EnteSiconfi(BaseModel):
    """Ente federativo cadastrado no SICONFI."""

    cod_ibge: int | None = None
    ente: str | None = None
    uf: str | None = None
    regiao: str | None = None
    esfera: str | None = None  # E=Estadual, M=Municipal, U=Federal
    capital: str | None = None
    populacao: int | None = None
    cnpj: str | None = None


class ItemDemonstrativo(BaseModel):
    """Linha de um demonstrativo fiscal (RREO ou RGF)."""

    exercicio: int | None = None
    demonstrativo: str | None = None
    periodo: int | None = None
    periodicidade: str | None = None
    instituicao: str | None = None
    cod_ibge: int | None = None
    uf: str | None = None
    anexo: str | None = None
    esfera: str | None = None
    coluna: str | None = None
    cod_conta: str | None = None
    conta: str | None = None
    valor: float | None = None
