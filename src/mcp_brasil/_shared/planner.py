"""LLM-powered query planner for mcp-brasil."""

from __future__ import annotations

import json
import logging

from pydantic import BaseModel

from .llm import llm_available, llm_complete

logger = logging.getLogger("mcp-brasil.planner")


class EtapaPlano(BaseModel):
    """One step of the execution plan."""

    etapa: int
    """Step number (1-based)."""

    descricao: str
    """What this step does."""

    tool: str
    """Tool name (with feature prefix, e.g. camara_buscar_deputados)."""

    parametros: dict[str, str]
    """Key parameters (may contain placeholders like '{etapa_1.id}')."""

    depende_de: list[int]
    """Steps that must complete before this one (empty = independent)."""

    justificativa: str
    """Why this step is needed."""


class PlanoConsulta(BaseModel):
    """Complete execution plan for a user query."""

    consulta: str
    """Original user query."""

    complexidade: str
    """Query complexity: 'simples', 'moderada', or 'complexa'."""

    resumo: str
    """Brief summary of the plan."""

    etapas: list[EtapaPlano]
    """Ordered execution steps."""

    observacoes: str = ""
    """Optional notes (auth requirements, caveats)."""

    def to_markdown(self) -> str:
        """Render the plan as human-friendly markdown."""
        lines: list[str] = [
            "## Plano de Consulta",
            f"**Consulta:** {self.consulta}",
            f"**Complexidade:** {self.complexidade}",
            f"**Resumo:** {self.resumo}",
            "",
        ]

        for etapa in self.etapas:
            lines.append(f"### Etapa {etapa.etapa}: {etapa.descricao}")
            lines.append(f"- **Tool:** `{etapa.tool}`")

            if etapa.parametros:
                params = ", ".join(f'{k}="{v}"' for k, v in etapa.parametros.items())
                lines.append(f"- **Parâmetros:** {params}")

            if etapa.depende_de:
                deps = ", ".join(f"Etapa {d}" for d in etapa.depende_de)
                lines.append(f"- **Depende de:** {deps}")
            else:
                lines.append("- **Depende de:** (nenhuma)")

            lines.append(f"- **Justificativa:** {etapa.justificativa}")
            lines.append("")

        if self.observacoes:
            lines.append(f"**Observações:** {self.observacoes}")

        return "\n".join(lines)


_SYSTEM_PROMPT = """\
Você é o planejador de consultas do mcp-brasil — um sistema MCP que conecta \
agentes de IA a APIs públicas brasileiras (IBGE, Banco Central, Câmara dos \
Deputados, Senado, Portal da Transparência, DataJud, entre outras).

Sua tarefa: dada uma pergunta do usuário e o catálogo de tools, construir um \
plano de execução estruturado.

## Regras

1. Use APENAS tools que existem no catálogo abaixo. Nunca invente tools.
2. Use os nomes exatos das tools (com prefixo da feature, ex: camara_listar_deputados).
3. Preencha os parâmetros usando os nomes e tipos do catálogo.
4. Para dados que vêm de etapas anteriores, use placeholders: {{etapa_N.campo}} \
(ex: {{etapa_1.id}}, {{etapa_2.nome}}).
5. Responda sempre em português.
6. Máximo de 8 etapas por plano.

## Complexidade

- **simples**: 1 tool, consulta direta (ex: "lista estados do Brasil")
- **moderada**: 2-3 tools, com dependências lineares (ex: "gastos do deputado X")
- **complexa**: 4+ tools, dependências ramificadas ou comparações (ex: "compare \
gastos de dois deputados com a média")

## Composição de fontes

Consultas ricas geralmente cruzam dados de múltiplas features. Estratégias:

- **Enriquecimento**: buscar entidade em uma API e complementar com outra \
(ex: deputado na Câmara + gastos na Transparência).
- **Comparação**: consultar a mesma métrica em fontes diferentes \
(ex: orçamento previsto no SIOP vs executado na Transparência).
- **Contextualização**: adicionar dados demográficos ou econômicos do IBGE/Bacen \
para dar contexto (ex: gasto per capita = despesa ÷ população do estado via IBGE).
- **Paralelismo**: etapas que não dependem uma da outra podem ter `depende_de` vazio \
— isso indica ao executor que podem rodar em paralelo.

Sempre que a pergunta permitir, prefira planos que cruzem 2+ features para \
gerar respostas mais completas. Indique no "resumo" quais fontes serão combinadas.

## Observações

Use o campo "observacoes" para informar:
- Se alguma etapa requer autenticação (veja "Auth:" no catálogo)
- Limitações conhecidas ou dados que podem não estar disponíveis
- Quais cruzamentos entre fontes o plano realiza

## Schema JSON (retorne APENAS JSON válido, sem markdown, sem ```)

{{
  "consulta": "pergunta original do usuário",
  "complexidade": "simples|moderada|complexa",
  "resumo": "resumo breve do plano em 1 frase",
  "etapas": [
    {{
      "etapa": 1,
      "descricao": "o que esta etapa faz",
      "tool": "feature_nome_da_tool",
      "parametros": {{"param": "valor"}},
      "depende_de": [],
      "justificativa": "por que esta etapa é necessária"
    }}
  ],
  "observacoes": "notas sobre autenticação, limitações, etc."
}}

## Exemplos

### Exemplo 1 — consulta moderada (single-feature)

Pergunta: "Quais foram os gastos do deputado Nikolas Ferreira em 2024?"

{{
  "consulta": "Quais foram os gastos do deputado Nikolas Ferreira em 2024?",
  "complexidade": "moderada",
  "resumo": "Buscar o deputado pelo nome na Câmara e consultar suas despesas em 2024.",
  "etapas": [
    {{
      "etapa": 1,
      "descricao": "Buscar deputado pelo nome",
      "tool": "camara_listar_deputados",
      "parametros": {{"nome": "Nikolas Ferreira"}},
      "depende_de": [],
      "justificativa": "Precisamos do ID do deputado para consultar despesas"
    }},
    {{
      "etapa": 2,
      "descricao": "Consultar despesas do deputado em 2024",
      "tool": "camara_despesas_deputado",
      "parametros": {{"id": "{{etapa_1.id}}", "ano": "2024"}},
      "depende_de": [1],
      "justificativa": "Obter os gastos usando o ID encontrado na etapa anterior"
    }}
  ],
  "observacoes": ""
}}

### Exemplo 2 — consulta complexa (cross-feature com paralelismo)

Pergunta: "Qual o gasto per capita com saúde em Minas Gerais?"

{{
  "consulta": "Qual o gasto per capita com saúde em Minas Gerais?",
  "complexidade": "complexa",
  "resumo": "Cruzar Transparência (gastos saúde) com IBGE (população MG).",
  "etapas": [
    {{
      "etapa": 1,
      "descricao": "Buscar gastos federais com saúde em MG",
      "tool": "transparencia_consultar_despesas",
      "parametros": {{"funcao": "saude", "uf": "MG", "ano": "2024"}},
      "depende_de": [],
      "justificativa": "Obter o valor total gasto com saúde no estado"
    }},
    {{
      "etapa": 2,
      "descricao": "Consultar população de Minas Gerais",
      "tool": "ibge_buscar_populacao",
      "parametros": {{"localidade": "31"}},
      "depende_de": [],
      "justificativa": "Obter a população para calcular o valor per capita"
    }}
  ],
  "observacoes": "Etapas 1 e 2 rodam em paralelo. \
Cálculo per capita feito pelo agente após ambas. \
Transparencia requer TRANSPARENCIA_API_KEY."
}}

## Catálogo de Tools

{catalog}
"""


async def planejar_consulta_impl(query: str, catalog: str) -> str:
    """Build a structured execution plan using the configured LLM (Ollama or Anthropic)."""
    ok, err = llm_available()
    if not ok:
        return err

    system_prompt = _SYSTEM_PROMPT.format(catalog=catalog)
    raw_text = await llm_complete(system_prompt, query, max_tokens=2048)

    # Strip <think>...</think> blocks that some models (e.g. qwen3) emit
    import re
    raw_text = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL).strip()

    # Strip markdown code fences if present
    raw_text = re.sub(r"^```[a-z]*\n?", "", raw_text).rstrip("`").strip()

    try:
        plano = PlanoConsulta.model_validate(json.loads(raw_text))
        return plano.to_markdown()
    except (json.JSONDecodeError, Exception):
        logger.warning("Failed to parse plan as JSON, returning raw text")
        return raw_text
