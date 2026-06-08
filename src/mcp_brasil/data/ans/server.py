"""MCP server registration for the ANS feature."""

from fastmcp import FastMCP

from .tools import buscar_operadoras_ans

mcp = FastMCP("mcp-brasil-ans")

mcp.tool(buscar_operadoras_ans, tags={"busca", "saude", "planos", "operadoras", "ans"})
