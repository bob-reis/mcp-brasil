"""Pydantic schemas for the ANAC feature."""

from __future__ import annotations

from pydantic import BaseModel


class AeronaveRAB(BaseModel):
    """Aeronave registrada no RAB (Registro Aeronáutico Brasileiro)."""

    marcas: str | None = None          # Prefixo (ex: PP-XPT)
    proprietarios: str | None = None   # Nome|CNPJ/CPF|%|UF (pipe-separated)
    operadores: str | None = None
    nr_certificado: str | None = None
    tipo: str | None = None            # AVIÃO, HELICOPTERO, etc.
    modelo: str | None = None
    fabricante: str | None = None
    ano_fabricacao: str | None = None
    nr_passageiros_max: str | None = None
    nr_assentos: str | None = None
    tp_motor: str | None = None
    qt_motor: str | None = None
    tp_operacao: str | None = None     # PRIVADA, TÁXI AÉREO, etc.
    categoria_homologacao: str | None = None
    dt_matricula: str | None = None
    dt_canc: str | None = None
    motivo_canc: str | None = None
    interdicao: str | None = None
    gravame: str | None = None
