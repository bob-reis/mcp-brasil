"""IBAMA feature server — registers tools, resources, and prompts.

This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .tools import buscar_autos_infracao_ibama, buscar_embargos_ibama, listar_dados_abertos_ibama

mcp = FastMCP("mcp-brasil-ibama")

# Tools
mcp.tool(buscar_embargos_ibama, tags={"busca", "embargo", "ambiental", "ibama"})
mcp.tool(buscar_autos_infracao_ibama, tags={"busca", "infracao", "ambiental", "ibama", "multa"})
mcp.tool(listar_dados_abertos_ibama, tags={"listagem", "datasets", "ibama", "ambiental"})
