# Caso de Uso: Jornalista — Produção de Matérias com Dados

> Como usar o mcp-brasil para apurar, enriquecer e verificar matérias jornalísticas com dados de APIs governamentais em tempo real.

---

## O Diferencial

Diferente do [jornalista investigativo](./jornalista-investigativo.md) (que busca irregularidades), este caso de uso é sobre **jornalismo de dados cotidiano** — produzir matérias com números verificáveis, comparações entre municípios/estados e visualizações baseadas em fontes oficiais.

---

## Matéria 1: "Quanto Custa um Deputado?"

### A Pauta

Comparar as despesas de gabinete dos deputados federais — quem gasta mais, quem gasta menos, e em quê.

### A Apuração

**1. Ranking de despesas**

> Prompt: "Liste os 10 deputados que mais gastaram com a cota parlamentar em 2024"

```
API: camara_despesas_deputado (executar_lote para Top 10)
```

**2. Comparação por partido**

> Prompt: "Qual a média de gastos de gabinete por partido? Qual partido gasta mais per capita?"

```
APIs: camara_buscar_deputados (todos) + camara_despesas_deputado (em lote)
```

**3. Detalhamento das categorias**

> Prompt: "Quanto a Câmara gasta no total com passagens aéreas, alimentação e combustível?"

O LLM agrega os dados e produz:

```
GASTOS DA CÂMARA — COTA PARLAMENTAR 2024

Total gasto por 513 deputados: R$ 187.456.789

| Categoria                | Total          | Média/Dep.   |
|--------------------------|----------------|-------------|
| Divulgação               | R$ 52,3M      | R$ 101.945  |
| Passagens aéreas         | R$ 41,2M      | R$ 80.311   |
| Combustíveis             | R$ 28,9M      | R$ 56.335   |
| Alimentação              | R$ 22,1M      | R$ 43.079   |
| Locação de veículos      | R$ 18,4M      | R$ 35.867   |
| Consultorias             | R$ 14,6M      | R$ 28.460   |
| Outros                   | R$ 9,9M       | R$ 19.298   |

Deputados que NÃO usaram a cota: 3 de 513
Deputados que usaram > 90% da cota: 47 de 513
```

### O Lead da Matéria

> "Os 513 deputados federais gastaram R$ 187,4 milhões com a cota parlamentar em 2024 — uma média de R$ 365 mil por parlamentar. Passagens aéreas e combustíveis representam 37% do total. O deputado [Nome] liderou o ranking com R$ [valor], enquanto [Nome] foi o mais econômico com R$ [valor]."

**Cada número é verificável na API da Câmara.**

---

## Matéria 2: "Mapa da Desigualdade: Saúde Pública por Estado"

### A Pauta

Comparar a infraestrutura de saúde entre estados brasileiros — leitos, profissionais, gastos.

### A Apuração

**1. Infraestrutura por estado**

> Prompt: "Compare o número de leitos hospitalares per capita em todos os estados brasileiros"

```
APIs: saude_buscar_estabelecimentos (por UF) + ibge_listar_estados (população)
```

**2. Gastos com saúde**

> Prompt: "Quanto cada estado gasta com saúde per capita?"

```
APIs: tce_[estado]_despesas + ibge_consultar_agregado (população)
```

**3. Indicadores de resultado**

> Prompt: "Qual a expectativa de vida em cada estado? Qual a mortalidade infantil?"

```
API: ibge_consultar_agregado (indicadores demográficos)
```

### O Infográfico

```
MAPA DA SAÚDE PÚBLICA — 2024

                Leitos/1000hab   Gasto/capita   Exp. Vida
  DF  ████████░     3,2          R$ 1.890      78,1 anos
  SP  ███████░░     2,8          R$ 1.567      77,8 anos
  SC  ████████░     3,1          R$ 1.423      79,2 anos
  ...
  MA  ███░░░░░░     1,1          R$   678      71,4 anos
  PA  ██░░░░░░░     0,9          R$   591      72,1 anos

  Diferença DF vs MA: 2,9x leitos | 2,8x gastos | 6,7 anos de vida
```

---

## Matéria 3: "Selic em Alta: O Impacto no Bolso do Brasileiro"

### A Pauta

Explicar o impacto da alta de juros na vida cotidiana.

### A Apuração

**1. Série histórica da Selic**

> Prompt: "Mostre a evolução da Selic nos últimos 5 anos e compare com a inflação"

```
APIs: bacen_comparar_series(codigos=[432, 433], ultimos=60)
```

**2. Impacto no crédito**

> Prompt: "Qual o custo de um financiamento de R$ 300 mil com a Selic atual vs. a de 2 anos atrás?"

```
API: bacen_consultar_serie (séries de crédito)
```

**3. Comparação internacional**

> Prompt: "Qual a taxa de juros real do Brasil comparada a outros países?"

O LLM calcula: Selic (14,25%) - IPCA (5,06%) = **Juro real de 9,19%**

```
JUROS REAIS — COMPARATIVO INTERNACIONAL

  🇧🇷 Brasil      ██████████████████░   9,19%
  🇲🇽 México      █████████░░░░░░░░░░   5,2%
  🇮🇳 Índia       ███████░░░░░░░░░░░░   3,1%
  🇺🇸 EUA         ████░░░░░░░░░░░░░░░   1,8%
  🇪🇺 Zona Euro   ███░░░░░░░░░░░░░░░░   1,2%
  🇯🇵 Japão       █░░░░░░░░░░░░░░░░░░  -0,1%
```

### O Lead da Matéria

> "Com a Selic em 14,25% e inflação de 5,06%, o Brasil tem o maior juro real do mundo entre as grandes economias: 9,19%. Um financiamento de R$ 300 mil que custava R$ 1.580/mês em 2021 (Selic a 2%) hoje custa R$ 2.890 — 83% a mais. Dados: Banco Central do Brasil."

---

## Matéria 4: "Queimadas Recordes: Os Números do INPE"

### A Pauta

Cobrir a temporada de queimadas com dados reais do INPE.

### A Apuração

**1. Focos de queimada**

> Prompt: "Quantos focos de queimada o INPE registrou na Amazônia em 2024? Compare com os 5 anos anteriores"

```
API: inpe_focos_queimadas(bioma="amazonia", ano=2024)
```

**2. Desmatamento**

> Prompt: "Qual o desmatamento acumulado na Amazônia nos últimos 12 meses?"

```
API: inpe_desmatamento(bioma="amazonia")
```

**3. Recursos hídricos**

> Prompt: "Qual o nível dos reservatórios nas regiões com mais queimadas?"

```
API: ana_monitorar_reservatorios
```

**4. Publicações oficiais**

> Prompt: "Busque publicações no Diário Oficial sobre decretos de emergência ambiental em 2024"

```
API: diario_oficial_buscar(termo="emergencia ambiental queimadas")
```

---

## Matéria 5: "Eleições 2026: O Dinheiro da Pré-Campanha"

### A Pauta

Acompanhar o financiamento de pré-candidatos às eleições de 2026.

### A Apuração

> Prompt: "Liste os pré-candidatos ao governo de SP que já têm prestação de contas registrada no TSE"

```
APIs: tse_buscar_candidatos(cargo="governador", uf="SP", ano=2026)
      tse_receitas_candidato (para cada candidato)
      tse_despesas_candidato (para cada candidato)
```

> Prompt: "Quem são os maiores doadores de campanhas a governador em todo o Brasil?"

```
API: tse_buscar_candidatos + tse_receitas_candidato (em lote)
```

---

## Dicas Para Jornalistas

### 1. Sempre cite a fonte

```
"Segundo dados da API do Banco Central (série SGS 432,
consulta em 23/03/2025), a taxa Selic..."
```

### 2. Use `executar_lote` para comparações

Quando a matéria precisa comparar múltiplos estados/municípios, uma única chamada resolve:

```json
[
  {"tool": "ibge_buscar_municipios", "args": {"uf": "SP"}},
  {"tool": "ibge_buscar_municipios", "args": {"uf": "RJ"}},
  {"tool": "ibge_buscar_municipios", "args": {"uf": "MG"}}
]
```

### 3. Use `planejar_consulta` para matérias complexas

> Prompt: "Preciso fazer uma matéria sobre o impacto das emendas PIX nos municípios do Nordeste. Planeje as consultas"

A ferramenta retorna o roteiro de apuração completo.

### 4. Dados + Redator = Matéria pronta

Combine as APIs de dados com o agente Redator para gerar textos com formatação profissional e dados verificáveis embutidos.

---

_Fontes: APIs do Banco Central, IBGE, Câmara dos Deputados, TSE, Portal da Transparência, INPE, ANA, CNES/DataSUS, TCEs, Diário Oficial._
