"""Pydantic schemas for the DadosAbertos-MT feature."""

from __future__ import annotations

from pydantic import BaseModel


class Recurso(BaseModel):
    id: str | None = None
    name: str | None = None
    url: str | None = None
    format: str | None = None
    description: str | None = None
    created: str | None = None
    last_modified: str | None = None


class Dataset(BaseModel):
    id: str | None = None
    name: str | None = None
    title: str | None = None
    notes: str | None = None
    organization_name: str | None = None
    organization_title: str | None = None
    tags: list[str] = []
    groups: list[str] = []
    resources: list[Recurso] = []
    metadata_created: str | None = None
    metadata_modified: str | None = None
    num_resources: int = 0


class DatasetResultado(BaseModel):
    total: int = 0
    datasets: list[Dataset] = []


class Organizacao(BaseModel):
    id: str | None = None
    name: str | None = None
    title: str | None = None
    description: str | None = None
    package_count: int = 0


class Grupo(BaseModel):
    id: str | None = None
    name: str | None = None
    title: str | None = None
    description: str | None = None
    package_count: int = 0
