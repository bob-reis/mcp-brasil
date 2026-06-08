"""MCP server registration for the ANAC feature."""

from fastmcp import FastMCP

from .tools import buscar_aeronaves_anac

mcp = FastMCP("mcp-brasil-anac")

mcp.tool(buscar_aeronaves_anac, tags={"busca", "aviacao", "aeronaves", "rab", "anac"})
