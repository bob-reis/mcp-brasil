"""Pydantic schemas for the OpenSanctions feature."""

from __future__ import annotations

from pydantic import BaseModel


class EntidadeSancionada(BaseModel):
    """Entidade encontrada em listas de sanções ou monitoramento."""

    id: str | None = None
    schema_tipo: str | None = None  # Person, Company, etc.
    nome: str | None = None
    nomes_alternativos: list[str] = []
    paises: list[str] = []
    nacionalidades: list[str] = []
    datasets: list[str] = []  # listas onde aparece
    topics: list[str] = []  # sanction, pep, crime, etc.
    score: float | None = None  # relevância da busca (0-1)
    data_nascimento: str | None = None
    cpf_cnpj: str | None = None
    posicao: str | None = None  # cargo/função (para PEPs)
    descricao: str | None = None


class DatasetOpenSanctions(BaseModel):
    """Dataset disponível no OpenSanctions."""

    nome: str | None = None
    titulo: str | None = None
    entidades: int | None = None
    paises: list[str] = []
    publicador: str | None = None
    ultima_atualizacao: str | None = None
    url: str | None = None


class ResultadoMatch(BaseModel):
    """Resultado de verificação (match) de entidade contra listas de sanções."""

    entidade_consultada: str | None = None
    matches: list[EntidadeSancionada] = []
    total_matches: int = 0
    is_sanctioned: bool = False
    is_pep: bool = False
    listas_encontradas: list[str] = []
