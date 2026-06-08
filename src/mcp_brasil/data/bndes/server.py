"""MCP server registration for the BNDES feature."""

from fastmcp import FastMCP

from .tools import buscar_operacoes_bndes

mcp = FastMCP("mcp-brasil-bndes")

mcp.tool(buscar_operacoes_bndes, tags={"busca", "financiamento", "contratos", "bndes", "credito"})
