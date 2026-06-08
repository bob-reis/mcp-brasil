"""IOMAT-MT feature server — registers tools, resources, and prompts.

This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import investigar_licitacao_mt, monitorar_orgao_mt
from .resources import diarios_disponiveis, endpoints_disponiveis
from .tools import (
    buscar_materias_mt,
    buscar_publicacoes_mt,
    listar_classificacoes_mt,
    listar_edicoes_mt,
    listar_orgaos_mt,
)

mcp = FastMCP("mcp-brasil-iomat-mt")

# Tools
mcp.tool(buscar_publicacoes_mt)
mcp.tool(listar_edicoes_mt)
mcp.tool(buscar_materias_mt)
mcp.tool(listar_orgaos_mt)
mcp.tool(listar_classificacoes_mt)

# Resources
mcp.resource("data://endpoints-disponiveis", mime_type="application/json")(endpoints_disponiveis)
mcp.resource("data://diarios-disponiveis", mime_type="application/json")(diarios_disponiveis)

# Prompts
mcp.prompt(monitorar_orgao_mt)
mcp.prompt(investigar_licitacao_mt)
