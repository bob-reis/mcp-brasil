"""Pydantic schemas for the BNDES feature."""

from __future__ import annotations

from pydantic import BaseModel


class OperacaoBNDES(BaseModel):
    """Operação de financiamento não-automática do BNDES."""

    cliente: str | None = None
    cnpj: str | None = None
    descricao_do_projeto: str | None = None
    uf: str | None = None
    municipio: str | None = None
    numero_do_contrato: str | int | None = None
    data_da_contratacao: str | None = None
    valor_contratado_reais: float | None = None
    valor_desembolsado_reais: float | None = None
    fonte_de_recurso_desembolsos: str | None = None
    custo_financeiro: str | None = None
    prazo_amortizacao_meses: int | None = None
    modalidade_de_apoio: str | None = None
    forma_de_apoio: str | None = None
    produto: str | None = None
    setor_bndes: str | None = None
    subsetor_bndes: str | None = None
    porte_do_cliente: str | None = None
    natureza_do_cliente: str | None = None
    situacao_do_contrato: str | None = None
