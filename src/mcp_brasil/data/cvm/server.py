"""CVM feature server — registers tools, resources, and prompts.

This file only registers components. Zero business logic (ADR-001 rule #4).
"""

from fastmcp import FastMCP

from .tools import buscar_companhias_cvm, buscar_fundos_investimento, buscar_processos_cvm

mcp = FastMCP("mcp-brasil-cvm")

# Tools
mcp.tool(buscar_companhias_cvm, tags={"busca", "companhias", "mercado-capitais", "cvm"})
mcp.tool(buscar_processos_cvm, tags={"busca", "pas", "sancoes", "compliance", "cvm"})
mcp.tool(buscar_fundos_investimento, tags={"busca", "fundos", "mercado-capitais", "cvm", "fii"})
