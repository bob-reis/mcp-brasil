"""DadosAbertos-MT feature server — registers tools, resources, and prompts.

This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .prompts import explorar_tema_mt
from .resources import endpoints_disponiveis
from .tools import (
    buscar_datasets_mt,
    detalhar_dataset_mt,
    listar_grupos_mt,
    listar_organizacoes_mt,
    listar_tags_mt,
)

mcp = FastMCP("mcp-brasil-dadosabertos-mt")

# Tools
mcp.tool(buscar_datasets_mt)
mcp.tool(detalhar_dataset_mt)
mcp.tool(listar_organizacoes_mt)
mcp.tool(listar_grupos_mt)
mcp.tool(listar_tags_mt)

# Resources
mcp.resource("data://endpoints-disponiveis", mime_type="application/json")(endpoints_disponiveis)

# Prompts
mcp.prompt(explorar_tema_mt)
