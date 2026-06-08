# Caso de Uso: Jornalista Investigativo

> Como um jornalista investigativo pode usar o mcp-brasil para cruzar dados públicos e descobrir irregularidades em minutos — trabalho que antes levava semanas.

---

## O Problema

Jornalismo investigativo brasileiro depende de dados dispersos em dezenas de portais governamentais. Um repórter que quer investigar gastos de um político precisa consultar manualmente:

- Portal da Transparência (contratos, despesas)
- TSE (financiamento de campanha)
- Câmara/Senado (votações, proposições)
- TCU (irregularidades, condenações)
- TCEs (gastos estaduais/municipais)
- PNCP (licitações)
- DataJud (processos judiciais)
- Diário Oficial (publicações, nomeações)

**Cada portal tem interface diferente, API diferente, formato diferente.** Cruzar essas bases manualmente consome semanas de trabalho. Com o mcp-brasil, um LLM faz em minutos.

---

## Investigação 1: "Quem Ganha com as Emendas?"

### A Pauta

Rastrear o caminho das emendas parlamentares — do deputado que destina até a empresa que executa o serviço no município.

### O Roteiro de Consultas

**1. Mapear as emendas de um deputado**

> Prompt: "Liste todas as emendas parlamentares do deputado [Nome] em 2024, valores e municípios de destino"

```
APIs: transparencia_emendas_parlamentares + transferegov_buscar_emendas
```

**2. Identificar os beneficiários finais**

> Prompt: "Para cada município que recebeu emenda, quais empresas foram contratadas com esse dinheiro?"

```
APIs: tce_[estado]_contratos + pncp_buscar_contratacoes
```

**3. Verificar se os beneficiários doaram para a campanha**

> Prompt: "Alguma dessas empresas ou seus sócios doaram para a campanha do deputado?"

```
APIs: tse_receitas_candidato + brasilapi_consultar_cnpj (dados da empresa)
```

**4. Checar antecedentes dos beneficiários**

> Prompt: "Essas empresas têm penalidades no TCU ou processos no DataJud?"

```
APIs: tcu_buscar_licitantes_inidoneos + datajud_buscar_processos
```

### O Que o Jornalista Encontra

```
CADEIA DOCUMENTAL:

Deputado X (PL-SP)
├── Emenda R$ 5M → Município Y/SP (TransfereGov)
│   ├── Contrato R$ 4,8M → Empresa ABC Ltda (TCE-SP)
│   │   ├── Sócios: João da Silva, Maria Santos (BrasilAPI)
│   │   └── João da Silva doou R$ 50K para Dep. X (TSE 2022)
│   └── Dispensa de licitação - valor abaixo de R$ 5M (PNCP)
│
├── Emenda R$ 3M → Município Z/SP (TransfereGov)
│   ├── Contrato R$ 2,9M → Empresa DEF Ltda (TCE-SP)
│   │   └── Mesmo endereço que Empresa ABC (BrasilAPI)
│   └── Empresa DEF tem penalidade no TCE-RJ (TCE-RJ)
│
└── Emenda R$ 2M → Município W/SP (TransfereGov)
    └── Sem contratação registrada ⚠️ Cadê o dinheiro?
```

**Cada elo da cadeia é verificável em fontes oficiais.** O jornalista tem números de documentos, CNPJs, datas e valores para citar na reportagem.

---

## Investigação 2: "Os Fantasmas do Funcionalismo"

### A Pauta

Identificar servidores fantasmas — pessoas que recebem salário mas não trabalham efetivamente.

### O Roteiro de Consultas

**1. Buscar servidores de um órgão**

> Prompt: "Liste os servidores do [Órgão] com os maiores salários em 2024"

```
API: transparencia_servidores(orgao="...")
```

**2. Cruzar com outros vínculos**

> Prompt: "Algum desses servidores também tem vínculo em outro órgão ou mandato eletivo?"

```
APIs: transparencia_servidores + camara_buscar_deputados + senado_buscar_senadores
```

**3. Verificar se há processos judiciais**

> Prompt: "Algum desses servidores tem processos relacionados a improbidade administrativa?"

```
APIs: datajud_buscar_processos(assunto="improbidade")
```

**4. Buscar no Diário Oficial**

> Prompt: "Busque publicações no Diário Oficial sobre nomeação e exoneração desses servidores"

```
API: diario_oficial_buscar(termo="[nome do servidor]")
```

---

## Investigação 3: "Licitações Dirigidas"

### A Pauta

Identificar licitações em que sempre vence a mesma empresa, sugerindo direcionamento.

### O Roteiro de Consultas

**1. Buscar licitações de um município**

> Prompt: "Liste todas as licitações da Prefeitura de [Município] nos últimos 2 anos"

```
APIs: tce_[estado]_licitacoes + pncp_buscar_contratacoes
```

**2. Agrupar por vencedor**

> Prompt: "Quais empresas venceram mais licitações? Alguma venceu em múltiplas categorias diferentes?"

O LLM agrupa automaticamente e identifica concentração:

```
CONCENTRAÇÃO DE VENCEDORES:

Empresa GHI Ltda:
  ├── Pregão 001/2023 - Material escolar      R$ 890K   ✅ venceu
  ├── Pregão 015/2023 - Material de limpeza   R$ 650K   ✅ venceu
  ├── Pregão 023/2024 - Combustíveis          R$ 1,2M   ✅ venceu
  ├── Pregão 031/2024 - Alimentação escolar   R$ 780K   ✅ venceu
  └── Total: 4 de 4 licitações = 100% de aproveitamento
      ⚠️ Empresa vende material escolar E combustíveis E alimentos?
```

**3. Verificar se houve impugnação**

> Prompt: "Alguma dessas licitações foi impugnada ou questionada judicialmente?"

```
APIs: tcu_buscar_acordaos(assunto="licitação [município]") + datajud_buscar_processos
```

**4. Checar vínculos entre empresa e gestores**

> Prompt: "Consulte o CNPJ da empresa vencedora e verifique quem são os sócios"

```
API: brasilapi_consultar_cnpj(cnpj="...")
```

---

## Investigação 4: "Saúde Pública em Colapso"

### A Pauta

Investigar a situação da saúde pública em um município — infraestrutura, profissionais e gastos.

### O Roteiro de Consultas

**1. Infraestrutura de saúde**

> Prompt: "Quantos hospitais, UPAs e UBSs existem em [Município]? Quantos leitos?"

```
API: saude_buscar_estabelecimentos(municipio="...", tipo="hospital")
```

**2. Gastos com saúde**

> Prompt: "Quanto a prefeitura gastou com saúde em 2024? Cumpriu o mínimo de 15%?"

```
APIs: tce_[estado]_despesas(funcao="Saúde") + tce_[estado]_receitas
```

**3. Transferências federais**

> Prompt: "Quanto o município recebeu do SUS em transferências federais?"

```
API: transparencia_transferencias(municipio="...", funcao="Saúde")
```

**4. Comparar com municípios vizinhos**

> Prompt: "Compare os gastos per capita com saúde de [Município] com os 5 municípios vizinhos"

```
APIs: ibge_buscar_municipios + tce_[estado]_despesas (em lote)
```

**5. Verificar óbitos e causas**

> Prompt: "Há dados sobre mortalidade evitável nesse município?"

```
API: ibge_consultar_agregado(agregado=...) — indicadores de saúde
```

---

## Ferramentas do Jornalista no mcp-brasil

### `planejar_consulta` — O Editor de Pauta Digital

> Prompt: "Quero investigar possíveis irregularidades na prefeitura de [Município]. Crie um plano de investigação"

A ferramenta retorna um plano estruturado:

```
Plano de Investigação: Prefeitura de [Município]
═══════════════════════════════════════════════

1. PANORAMA FISCAL
   ├── tce_[estado]_despesas → gastos por função
   ├── tce_[estado]_receitas → arrecadação
   └── Meta: verificar limites LRF (pessoal, endividamento)

2. LICITAÇÕES E CONTRATOS
   ├── tce_[estado]_licitacoes → processos licitatórios
   ├── pncp_buscar_contratacoes → contratações federais
   └── Meta: identificar concentração de fornecedores

3. EMENDAS E TRANSFERÊNCIAS
   ├── transferegov_buscar_emendas → emendas PIX
   ├── transparencia_transferencias → repasses federais
   └── Meta: rastrear destino dos recursos

4. VERIFICAÇÃO DE IRREGULARIDADES
   ├── tcu_buscar_acordaos → decisões do TCU
   ├── tcu_buscar_licitantes_inidoneos → lista suja
   └── datajud_buscar_processos → processos judiciais
```

### `executar_lote` — A Apuração em Paralelo

Uma única chamada dispara consultas em múltiplas APIs simultaneamente:

```json
[
  {"tool": "tce_sp_despesas", "args": {"municipio": "São Paulo", "ano": 2024}},
  {"tool": "transparencia_contratos", "args": {"orgao": "Prefeitura SP"}},
  {"tool": "pncp_buscar_contratacoes", "args": {"orgao": "São Paulo"}},
  {"tool": "tcu_buscar_acordaos", "args": {"entidade": "Prefeitura São Paulo"}}
]
```

4 fontes, 1 chamada, todos os dados em paralelo.

### `recomendar_tools` — Quando Não Sabe Por Onde Começar

> Prompt: "Quero investigar fraudes em licitações. Quais ferramentas devo usar?"

```
API: recomendar_tools(query="fraudes em licitações municipais")
```

Retorna as tools mais relevantes com explicação de quando usar cada uma.

---

## Checklist do Jornalista Investigativo

| Etapa | O Que Verificar | APIs |
|-------|----------------|------|
| 1. Financiamento | Quem doou para a campanha | TSE |
| 2. Votações | Como votou e em favor de quem | Câmara/Senado |
| 3. Emendas | Para onde destinou recursos | Transparência/TransfereGov |
| 4. Contratos | Quem recebeu os contratos | TCE/PNCP/Transparência |
| 5. Vínculos | Doadores = Contratados? | TSE + BrasilAPI + TCE |
| 6. Antecedentes | Empresa/pessoa na lista suja? | TCU + DataJud |
| 7. Publicações | O que foi publicado oficialmente | Diário Oficial |
| 8. Jurisprudência | Há processos ou condenações? | DataJud + STF/STJ |

**Cada elo pode ser documentado com fonte oficial — essencial para publicação jornalística.**

---

_Fontes: APIs da Câmara, Senado, TSE, Portal da Transparência, TCU, 9 TCEs, PNCP, Compras.gov.br, DataJud, Jurisprudência STF/STJ, Diário Oficial, BrasilAPI, IBGE, CNES/DataSUS, TransfereGov._
