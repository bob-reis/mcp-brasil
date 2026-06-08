"""OpenSanctions feature server — registers tools, resources, and prompts.

This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .tools import (
    buscar_sancoes_internacionais,
    detalhar_entidade_sancao,
    listar_listas_sancoes,
    verificar_compliance,
)

mcp = FastMCP("mcp-brasil-opensanctions")

# Tools
mcp.tool(
    buscar_sancoes_internacionais,
    tags={"busca", "sancoes", "ofac", "onu", "compliance", "kyc"},
)
mcp.tool(
    verificar_compliance,
    tags={"verificacao", "compliance", "sancoes", "pep", "kyc", "anticorrupcao"},
)
mcp.tool(
    detalhar_entidade_sancao,
    tags={"detalhe", "sancoes", "entidade"},
)
mcp.tool(
    listar_listas_sancoes,
    tags={"listagem", "sancoes", "datasets"},
)
