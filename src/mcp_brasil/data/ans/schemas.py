"""Pydantic schemas for the ANS feature."""

from __future__ import annotations

from pydantic import BaseModel


class OperadoraANS(BaseModel):
    """Operadora de plano de saúde ativa cadastrada na ANS."""

    registro_ans: str | None = None
    cnpj: str | None = None
    razao_social: str | None = None
    nome_fantasia: str | None = None
    modalidade: str | None = None
    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str | None = None
    uf: str | None = None
    cep: str | None = None
    telefone: str | None = None
    email: str | None = None
    representante: str | None = None
    data_registro_ans: str | None = None
