"""Pydantic schemas for the IBAMA feature."""

from __future__ import annotations

from pydantic import BaseModel


class AreaEmbargada(BaseModel):
    """Área embargada pelo IBAMA."""

    numero_auto: str | None = None
    cpf_cnpj: str | None = None
    nome_embargado: str | None = None
    municipio: str | None = None
    uf: str | None = None
    bioma: str | None = None
    area_ha: float | None = None
    data_embargo: str | None = None
    motivo: str | None = None
    status: str | None = None


class AutoInfracao(BaseModel):
    """Auto de infração emitido pelo IBAMA."""

    numero_auto: str | None = None
    cpf_cnpj: str | None = None
    nome_autuado: str | None = None
    municipio: str | None = None
    uf: str | None = None
    tipo_infracao: str | None = None
    valor_multa: float | None = None
    data_infracao: str | None = None
    status: str | None = None
    artigo_infringido: str | None = None


class DatasetIBAMA(BaseModel):
    """Dataset disponível no portal de dados abertos do IBAMA."""

    nome: str | None = None
    titulo: str | None = None
    descricao: str | None = None
    resource_id: str | None = None
    formato: str | None = None
    ultima_atualizacao: str | None = None
