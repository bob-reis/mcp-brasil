"""Procurados feature server — registers tools."""

from fastmcp import FastMCP

from .tools import buscar_interpol

mcp = FastMCP("mcp-brasil-procurados")

mcp.tool(buscar_interpol, tags={"busca", "interpol", "procurados", "foragidos", "seguranca-publica"})
