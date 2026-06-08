"""Querido Diário feature server — registers tools."""

from fastmcp import FastMCP

from .tools import buscar_cidade, buscar_diarios_municipais

mcp = FastMCP("mcp-brasil-querido-diario")

mcp.tool(buscar_diarios_municipais, tags={"busca", "diario-oficial", "municipios", "licitacoes", "transparencia"})
mcp.tool(buscar_cidade, tags={"consulta", "municipios", "querido-diario"})
