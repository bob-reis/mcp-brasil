"""OAB feature server — registers tools."""

from fastmcp import FastMCP

from .tools import consultar_advogado

mcp = FastMCP("mcp-brasil-oab")

mcp.tool(consultar_advogado, tags={"consulta", "oab", "advogados", "juridico"})
