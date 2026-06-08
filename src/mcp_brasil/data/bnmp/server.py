"""BNMP feature server — registers tools."""

from fastmcp import FastMCP

from .tools import buscar_mandados

mcp = FastMCP("mcp-brasil-bnmp")

mcp.tool(buscar_mandados, tags={"busca", "mandados", "prisao", "cnj", "seguranca-publica"})
