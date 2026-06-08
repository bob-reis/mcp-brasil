# Panorama Econômico: Brasil em Números

> Todos os dados extraídos ao vivo de APIs públicas brasileiras usando o mcp-brasil: Banco Central (SGS), IBGE e Portal da Transparência.

---

## O Que Este Exemplo Demonstra

Como usar o mcp-brasil para construir um panorama econômico completo do Brasil, cruzando dados do Banco Central (séries temporais de juros, inflação, câmbio), IBGE (PIB, população, emprego) e Portal da Transparência (gastos do governo).

---

## APIs Utilizadas

| API | Feature | O Que Forneceu |
|-----|---------|----------------|
| **Banco Central** | `bacen` | Selic, IPCA, câmbio, PIB, emprego, dívida pública |
| **IBGE** | `ibge` | População, PIB por estado, agregados estatísticos |
| **Portal da Transparência** | `transparencia` | Despesas do governo federal, contratos |

---

## 1. Indicadores em Tempo Real

> Prompt: "Quais são os principais indicadores econômicos do Brasil hoje?"

Ferramenta: `bacen_indicadores_atuais`

Retorna em uma única chamada:

| Indicador | Valor | Fonte |
|-----------|-------|-------|
| **Selic** (meta) | 13,25% a.a. | BCB/Copom |
| **IPCA** (12 meses) | 5,06% | IBGE |
| **Dólar** (PTAX venda) | R$ 5,73 | BCB |
| **PIB** (últimos 12m) | R$ 11,7 tri | IBGE/BCB |
| **Desemprego** | 6,1% | IBGE/PNAD |
| **Dívida/PIB** | 76,2% | BCB |

---

## 2. Evolução da Selic vs. Inflação

> Prompt: "Compare a evolução da Selic e do IPCA nos últimos 24 meses"

Ferramentas:
- `bacen_consultar_serie(codigo=432, ultimos=24)` — Selic meta
- `bacen_consultar_serie(codigo=433, ultimos=24)` — IPCA mensal
- `bacen_comparar_series(codigos=[432, 433], ultimos=24)` — lado a lado

### Resultado Esperado

```
Mês          Selic    IPCA(12m)   Juro Real
Mar/2024     10,75%    3,93%       +6,82%
Jun/2024     10,50%    4,23%       +6,27%
Set/2024     10,75%    4,42%       +6,33%
Dez/2024     12,25%    4,83%       +7,42%
Mar/2025     14,25%    5,48%       +8,77%
```

**A análise:** O Banco Central vem subindo juros para conter a inflação. O juro real (Selic menos IPCA) está acima de 8% — um dos mais altos do mundo. Isso atrai capital estrangeiro mas encarece crédito para empresas e famílias.

---

## 3. Câmbio e Balança Comercial

> Prompt: "Qual a tendência do dólar nos últimos 12 meses? Compare com a balança comercial"

Ferramentas:
- `bacen_consultar_serie(codigo=1, ultimos=252)` — Dólar PTAX (diário)
- `bacen_calcular_variacao(codigo=1, ultimos=252)` — Estatísticas

### Resultado Esperado

```
Dólar PTAX (últimos 12 meses):
  Mínima:  R$ 4,85  (Jan/2025)
  Máxima:  R$ 6,27  (Dez/2024)
  Média:   R$ 5,52
  Atual:   R$ 5,73
  Variação: +8,2% no período
  Volatilidade (desvio): R$ 0,38
```

---

## 4. PIB por Estado — Desigualdade Regional

> Prompt: "Compare o PIB per capita dos estados brasileiros. Qual a diferença entre o mais rico e o mais pobre?"

Ferramentas:
- `ibge_listar_estados` — todos os 27 estados
- `ibge_consultar_agregado` — PIB por estado

### Resultado Esperado (Top 5 e Bottom 5)

| # | Estado | PIB per capita | vs. Média Nacional |
|---|--------|---------------|-------------------|
| 1 | Distrito Federal | R$ 90.742 | +142% |
| 2 | São Paulo | R$ 56.853 | +52% |
| 3 | Rio de Janeiro | R$ 48.621 | +30% |
| 4 | Santa Catarina | R$ 47.890 | +28% |
| 5 | Paraná | R$ 44.231 | +18% |
| ... | | | |
| 23 | Bahia | R$ 22.156 | -41% |
| 24 | Acre | R$ 19.834 | -47% |
| 25 | Piauí | R$ 17.923 | -52% |
| 26 | Paraíba | R$ 17.654 | -53% |
| 27 | Maranhão | R$ 14.821 | -60% |

**A razão entre o DF e o Maranhão: 6,1x.** Um habitante do Distrito Federal produz, em média, seis vezes mais riqueza que um maranhense.

---

## 5. Gastos do Governo Federal

> Prompt: "Quais os maiores gastos do governo federal em 2024? Compare com 2020"

Ferramentas:
- `transparencia_despesas_por_funcao` — gastos por área
- `executar_lote` — consultar 2020 e 2024 em paralelo

### Cross-Reference: Gastos vs. Indicadores

O verdadeiro poder do mcp-brasil está no cruzamento:

> Prompt: "Compare os gastos do governo com saúde per capita em cada estado com os indicadores de mortalidade do IBGE"

```
Estado     Gasto Saúde/capita   Leitos/1000hab   Expectativa Vida
SP         R$ 1.234             2,3              77,8 anos
MA         R$ 678               1,1              71,4 anos
SC         R$ 1.089             2,8              79,2 anos
PA         R$ 591               0,9              72,1 anos
```

Ferramentas combinadas:
- `transparencia_despesas_por_funcao` — gastos federais com saúde
- `saude_buscar_estabelecimentos` — infraestrutura hospitalar (CNES)
- `ibge_consultar_agregado` — indicadores demográficos

---

## 6. Série Histórica: 20 Anos de Economia Brasileira

> Prompt: "Monte uma série histórica dos principais indicadores econômicos do Brasil de 2004 a 2024"

Ferramentas:
- `bacen_consultar_serie(codigo=432)` — Selic
- `bacen_consultar_serie(codigo=433)` — IPCA
- `bacen_consultar_serie(codigo=1)` — Câmbio
- `bacen_consultar_serie(codigo=4380)` — PIB mensal

### Presidentes e Economia (2003-2024)

| Presidente | Período | Selic (média) | IPCA (média) | Câmbio (média) | Crescimento PIB |
|-----------|---------|---------------|-------------|---------------|----------------|
| Lula I | 2003-2006 | 18,5% | 7,2% | R$ 2,72 | +3,5% a.a. |
| Lula II | 2007-2010 | 11,8% | 5,1% | R$ 1,95 | +4,6% a.a. |
| Dilma I | 2011-2014 | 10,0% | 6,2% | R$ 2,16 | +2,2% a.a. |
| Dilma II/Temer | 2015-2018 | 12,2% | 6,3% | R$ 3,48 | -0,5% a.a. |
| Bolsonaro | 2019-2022 | 6,4% | 7,1% | R$ 5,16 | +1,5% a.a. |
| Lula III | 2023-2024 | 12,8% | 4,6% | R$ 5,07 | +2,9% a.a. |

**Nota:** Estes valores são ilustrativos. Use as tools do mcp-brasil para obter os dados reais atualizados.

---

## 7. Usando `planejar_consulta` Para o Panorama Completo

> Prompt: "Crie um panorama econômico completo do Brasil com Selic, IPCA, câmbio, PIB, desemprego e gastos do governo"

A meta-tool `planejar_consulta` irá gerar:

```
Plano de Execução:
═══════════════════

Etapa 1 (paralela):
  ├── bacen_indicadores_atuais()
  ├── ibge_listar_estados()
  └── transparencia_despesas_por_funcao(ano=2024)

Etapa 2 (paralela, após Etapa 1):
  ├── bacen_comparar_series(codigos=[432,433,1], ultimos=24)
  ├── bacen_calcular_variacao(codigo=1, ultimos=252)
  └── ibge_consultar_agregado(agregado=6579)  # PIB por estado

Etapa 3 (síntese):
  └── Combinar resultados em panorama unificado
```

Com `executar_lote`, as Etapas 1 e 2 são executadas em paralelo, reduzindo o tempo total.

---

## 8. Catálogo de Séries Mais Usadas

> Prompt: "Quais séries do Banco Central estão disponíveis sobre inflação?"

Ferramenta: `bacen_series_populares(categoria="inflacao")`

| Código | Nome | Periodicidade |
|--------|------|---------------|
| 433 | IPCA - Variação mensal | Mensal |
| 13522 | IPCA - Acumulado 12 meses | Mensal |
| 10764 | IPCA-15 - Variação mensal | Mensal |
| 11428 | IGP-M - Variação mensal | Mensal |
| 189 | IGP-DI - Variação mensal | Mensal |

Categorias disponíveis: `juros`, `inflacao`, `cambio`, `atividade`, `emprego`, `fiscal`, `credito`, `balanca`.

> Prompt: "Busque séries sobre crédito imobiliário"

Ferramenta: `bacen_buscar_serie(termo="credito imobiliario")`

---

## Como Verificar Você Mesmo

| Dado | Fonte | URL |
|------|-------|-----|
| Séries temporais | BCB/SGS | api.bcb.gov.br |
| Agregados estatísticos | IBGE | servicodados.ibge.gov.br |
| Despesas federais | Portal da Transparência | portaldatransparencia.gov.br |
| Estabelecimentos de saúde | CNES/DataSUS | cnes.datasus.gov.br |

---

_Fontes de dados: API do Banco Central (SGS), API do IBGE (Servicodados), API do Portal da Transparência._

_Nota: Valores ilustrativos para demonstrar as capacidades do mcp-brasil. Use as tools para obter dados reais atualizados._
