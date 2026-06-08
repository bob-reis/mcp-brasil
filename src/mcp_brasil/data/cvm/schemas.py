"""Pydantic schemas for the CVM feature."""

from __future__ import annotations

from pydantic import BaseModel


class CompanhiaAberta(BaseModel):
    """Companhia aberta registrada na CVM."""

    cnpj: str | None = None
    nome: str | None = None
    tipo: str | None = None
    situacao: str | None = None
    setor: str | None = None
    data_registro: str | None = None
    data_cancel: str | None = None
    email: str | None = None


class ProcessoCVM(BaseModel):
    """Processo Administrativo Sancionador (PAS) da CVM."""

    numero: str | None = None
    acusado: str | None = None
    cpf_cnpj: str | None = None
    relator: str | None = None
    decisao: str | None = None
    data_julgamento: str | None = None
    penalidade: str | None = None
    valor_multa: float | None = None
    artigo: str | None = None


class FundoInvestimento(BaseModel):
    """Fundo de investimento registrado na CVM."""

    cnpj: str | None = None
    denominacao: str | None = None
    classe: str | None = None
    tipo: str | None = None
    situacao: str | None = None
    administrador: str | None = None
    data_registro: str | None = None
    patrimonio_liquido: float | None = None
