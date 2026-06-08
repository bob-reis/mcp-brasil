"""MCP server registration for the SICONFI feature."""

from fastmcp import FastMCP

from .tools import buscar_rgf, buscar_rreo, listar_entes_siconfi

mcp = FastMCP("mcp-brasil-siconfi")

mcp.tool(listar_entes_siconfi, tags={"busca", "entes", "municipios", "estados", "siconfi"})
mcp.tool(buscar_rreo, tags={"busca", "orcamento", "receita", "despesa", "siconfi", "fiscal"})
mcp.tool(buscar_rgf, tags={"busca", "pessoal", "divida", "fiscal", "lrf", "siconfi"})
