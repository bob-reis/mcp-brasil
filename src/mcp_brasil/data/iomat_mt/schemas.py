"""Pydantic schemas for the IOMAT-MT feature."""

from __future__ import annotations

from pydantic import BaseModel


class ResultadoBusca(BaseModel):
    total: int = 0
    pagina: int = 0
    resultados: list[ItemBusca] = []


class ItemBusca(BaseModel):
    highlight: str | None = None
    protocolo: int | None = None
    edicao_numero: int | None = None
    data: str | None = None
    pagina: int | None = None
    diario: str | None = None
    suplemento: str | None = None


class Diario(BaseModel):
    id: int
    nome: str | None = None
    sigla: str | None = None
    abreviacao: str | None = None


class Edicao(BaseModel):
    id: int
    data: str | None = None
    numpag: int | None = None
    numero: int | None = None
    diario: str | None = None
    titulo: str | None = None
    diario_abreviacao: str | None = None
    suplemento: str | None = None
    capa: str | None = None


class Materia(BaseModel):
    id: int | None = None
    protocolo: int | None = None
    titulo: str | None = None
    subtitulo: str | None = None
    orgao: str | None = None
    pagina: int | None = None
    texto: str | None = None


class Cliente(BaseModel):
    cliente_id: int | None = None
    nome: str | None = None
    sigla: str | None = None
    tipo_pessoa: str | None = None
    classificacao: str | None = None
    ug: str | None = None
    nome_fantasia: str | None = None
    razao_social: str | None = None


class Classificacao(BaseModel):
    id: int | None = None
    nome: str | None = None
