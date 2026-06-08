# mcp-brasil Documentation

**MCP Server para 27 APIs publicas brasileiras**

205 tools · 58 resources · 47 prompts · 24 APIs sem chave

---

## O que e o mcp-brasil?

O mcp-brasil e um pacote Python que expoe APIs publicas brasileiras como um servidor [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). Ele permite que AI agents (Claude, GPT, Copilot, etc.) consultem dados governamentais oficiais do Brasil em linguagem natural.

### O que ele cobre

| Categoria | O que voce pode perguntar |
|-----------|--------------------------|
| **Economico** | Selic, IPCA, cambio, PIB, estados, municipios, dados demograficos |
| **Legislativo** | Deputados, senadores, projetos de lei, votacoes, despesas parlamentares |
| **Transparencia** | Contratos federais, despesas, servidores, sancoes, bolsa familia |
| **Judiciario** | Processos judiciais, jurisprudencia do STF/STJ/TST, acordaos do TCU |
| **Eleitoral** | Candidatos, resultados de eleicoes, prestacao de contas |
| **Ambiental** | Focos de queimadas, desmatamento, reservatorios, estacoes hidrologicas |
| **Saude** | Estabelecimentos de saude, profissionais, leitos |
| **Compras Publicas** | Licitacoes, contratos (PNCP + ComprasNet/SIASG) |
| **Utilidades** | CEP, CNPJ, bancos, FIPE, diarios oficiais, datasets abertos |

## Documentacao

| Pagina | Descricao |
|--------|-----------|
| [Quick Start](guide/quickstart.md) | Instalacao e configuracao em 2 minutos |
| [Arquitetura](concepts/architecture.md) | Como o projeto funciona por dentro |
| [Catalogo de Features](reference/features.md) | Todas as 27 features e suas 205 tools |
| [Smart Tools](reference/smart-tools.md) | Meta-tools: planner, batch, discovery |
| [Adicionando Features](guide/adding-features.md) | Guia para contribuir com novas APIs |
| [Configuracao](reference/configuration.md) | Variaveis de ambiente e opcoes |
| [Desenvolvimento](guide/development.md) | Setup de dev, testes, lint, CI |
