"""LLM client factory for mcp-brasil.

Supports two providers via a single async interface:
- "ollama"    → OpenAI-compatible API at OLLAMA_BASE_URL (local)
- "anthropic" → Anthropic Messages API (cloud)

Selected by LLM_PROVIDER env var.
"""

from __future__ import annotations

import logging

from ..settings import (
    ANTHROPIC_API_KEY,
    LLM_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)

logger = logging.getLogger("mcp-brasil.llm")


async def llm_complete(system_prompt: str, user_message: str, max_tokens: int = 2048) -> str:
    """Send a system+user prompt to the configured LLM and return the text response."""
    if LLM_PROVIDER == "ollama":
        return await _ollama_complete(system_prompt, user_message, max_tokens)
    return await _anthropic_complete(system_prompt, user_message, max_tokens)


def llm_available() -> tuple[bool, str]:
    """Return (ok, error_msg). error_msg is empty when ok=True."""
    if LLM_PROVIDER == "ollama":
        return True, ""
    if not ANTHROPIC_API_KEY:
        return False, (
            "Erro: ANTHROPIC_API_KEY não configurada. "
            "Defina LLM_PROVIDER=ollama para usar o modelo local, ou configure ANTHROPIC_API_KEY.\n\n"
            "Alternativa: use a tool 'search_tools' para buscar por palavras-chave."
        )
    return True, ""


async def _ollama_complete(system_prompt: str, user_message: str, max_tokens: int) -> str:
    try:
        from openai import AsyncOpenAI
    except ImportError:
        return (
            "Erro: pacote 'openai' não instalado. "
            "Execute: uv add openai"
        )

    client = AsyncOpenAI(
        base_url=f"{OLLAMA_BASE_URL.rstrip('/')}/v1",
        api_key="ollama",  # Ollama ignores the key but the client requires a non-empty value
    )
    try:
        response = await client.chat.completions.create(
            model=OLLAMA_MODEL,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        logger.error("Erro ao chamar Ollama (%s): %s", OLLAMA_MODEL, e)
        return f"Erro ao consultar Ollama ({OLLAMA_MODEL}): {e}\n\nUse 'search_tools' como alternativa."


async def _anthropic_complete(system_prompt: str, user_message: str, max_tokens: int) -> str:
    try:
        import anthropic
    except ImportError:
        return (
            "Erro: pacote 'anthropic' não instalado. "
            "Execute: pip install 'mcp-brasil[llm]'"
        )

    client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    try:
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        block = response.content[0]
        return str(getattr(block, "text", ""))
    except Exception as e:
        logger.error("Erro ao chamar Anthropic API: %s", e)
        return f"Erro ao consultar Anthropic: {e}\n\nUse 'search_tools' como alternativa."
