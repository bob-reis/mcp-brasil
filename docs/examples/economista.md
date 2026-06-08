# Caso de Uso: Economista — Análise e Modelagem com Dados Oficiais

> Como economistas, analistas de mercado e pesquisadores podem usar o mcp-brasil para acessar séries temporais do Banco Central, indicadores do IBGE e dados fiscais em tempo real.

---

## O Diferencial Para Economistas

O Banco Central do Brasil disponibiliza mais de **40.000 séries temporais** via Sistema Gerador de Séries (SGS). O mcp-brasil oferece acesso direto a essas séries com ferramentas otimizadas para análise econômica:

| Tool | O Que Faz |
|------|----------|
| `bacen_indicadores_atuais` | Snapshot instantâneo: Selic, IPCA, câmbio, PIB, desemprego |
| `bacen_consultar_serie` | Consulta qualquer série do SGS por código |
| `bacen_ultimos_valores` | Últimos N valores de uma série |
| `bacen_metadados_serie` | Nome, unidade, periodicidade, última atualização |
| `bacen_series_populares` | Catálogo curado por categoria |
| `bacen_buscar_serie` | Busca textual no catálogo |
| `bacen_calcular_variacao` | Estatísticas: média, desvio, min/max, variação |
| `bacen_comparar_series` | Compara múltiplas séries lado a lado |

---

## Análise 1: Curva de Juros e Expectativas de Inflação

### O Cenário

Um economista precisa analisar a relação entre a Selic, as expectativas de inflação (Focus) e o IPCA realizado.

> Prompt: "Compare a evolução da Selic meta, do IPCA acumulado 12 meses e das expectativas Focus para os próximos 12 meses"

### Ferramentas Utilizadas

```
bacen_comparar_series(
  codigos=[432, 13522, 29043],
  ultimos=24
)
# 432   = Selic meta
# 13522 = IPCA acumulado 12m
# 29043 = Expectativa Focus IPCA 12m
```

### Resultado

```
SELIC vs. IPCA vs. EXPECTATIVAS — Últimos 24 meses

Mês        Selic   IPCA(12m)  Focus(12m)  Juro Real
─────────────────────────────────────────────────────
Mar/2024   10,75%   3,93%      3,52%       6,82%
Jun/2024   10,50%   4,23%      3,96%       6,27%
Set/2024   10,75%   4,42%      4,38%       6,33%
Dez/2024   12,25%   4,83%      4,95%       7,42%
Mar/2025   14,25%   5,06%      5,12%       9,19%
─────────────────────────────────────────────────────

Observações:
• IPCA acelerou de 3,93% para 5,06% (+1,13 p.p.)
• Selic subiu 3,50 p.p. no mesmo período
• Expectativas desancoradas: Focus > meta desde Set/24
• Juro real passou de 6,8% para 9,2% — restritivo
```

---

## Análise 2: Decomposição do IPCA — O Que Está Puxando a Inflação?

> Prompt: "Decomponha o IPCA por grupo de despesa nos últimos 12 meses. Quais componentes mais contribuíram para a alta?"

### Ferramentas

```
bacen_series_populares(categoria="inflacao")
→ Retorna séries de IPCA por grupo

bacen_comparar_series(
  codigos=[7170, 7171, 7172, 7173, 7174, 7175, 7176, 7177, 7178],
  ultimos=12
)
# Séries de IPCA por grupo: Alimentação, Habitação,
# Transportes, Saúde, Educação, Vestuário, etc.
```

### Resultado

```
DECOMPOSIÇÃO DO IPCA — Mar/2025 (12 meses)

Grupo                  Variação   Peso    Contribuição
────────────────────────────────────────────────────────
Alimentação e bebidas   6,82%     21,7%    1,48 p.p.
Habitação               5,23%     15,9%    0,83 p.p.
Transportes             4,91%     20,1%    0,99 p.p.
Saúde e cuidados        7,12%      9,1%    0,65 p.p.
Educação                6,34%      6,3%    0,40 p.p.
Vestuário               2,45%      4,5%    0,11 p.p.
Artigos de residência   1,89%      3,7%    0,07 p.p.
Comunicação             2,12%      4,9%    0,10 p.p.
Despesas pessoais       5,67%     10,1%    0,57 p.p.
────────────────────────────────────────────────────────
IPCA Total              5,06%    100,0%    5,06 p.p.

Principal vetor: Alimentação (1,48 p.p. = 29% do IPCA)
```

---

## Análise 3: Política Fiscal — Receita vs. Despesa

### O Cenário

Analisar a trajetória fiscal do governo federal — receitas, despesas e resultado primário.

> Prompt: "Monte um painel fiscal do governo federal: receitas vs. despesas dos últimos 5 anos, resultado primário e dívida/PIB"

### Ferramentas

```
bacen_consultar_serie(codigo=4503)    # Receita total governo central
bacen_consultar_serie(codigo=4504)    # Despesa total governo central
bacen_consultar_serie(codigo=4505)    # Resultado primário
bacen_consultar_serie(codigo=4513)    # Dívida bruta/PIB
bacen_consultar_serie(codigo=4514)    # Dívida líquida/PIB
```

### Resultado

```
PAINEL FISCAL — GOVERNO CENTRAL

Ano    Receita    Despesa    Primário    Dív.Bruta/PIB
──────────────────────────────────────────────────────
2020   R$ 1,48T   R$ 2,06T   -R$ 583B    88,6%
2021   R$ 1,87T   R$ 1,94T   -R$  72B    78,3%
2022   R$ 2,17T   R$ 1,96T   +R$ 209B    72,9%
2023   R$ 2,19T   R$ 2,10T   +R$  90B    74,4%
2024   R$ 2,36T   R$ 2,28T   +R$  81B    76,2%
──────────────────────────────────────────────────────

Tendência: Resultado primário positivo mas em queda
Risco: Dívida/PIB voltando a subir
```

---

## Análise 4: Câmbio e Balança Comercial

> Prompt: "Analise a relação entre o câmbio real/dólar e a balança comercial nos últimos 10 anos. O real mais fraco melhora as exportações?"

### Ferramentas

```
bacen_comparar_series(
  codigos=[1, 22707, 22708],
  ultimos=120  # 10 anos mensais
)
# 1     = Dólar PTAX
# 22707 = Exportações (FOB)
# 22708 = Importações (FOB)
```

```
bacen_calcular_variacao(codigo=1, ultimos=120)
# Estatísticas do câmbio
```

### Resultado

```
CÂMBIO vs. BALANÇA COMERCIAL — 2015-2025

Período         Dólar Médio   Exportações   Saldo Comercial
─────────────────────────────────────────────────────────────
2015 (Dilma)    R$ 3,33       $191B         +$19,7B
2016 (Temer)    R$ 3,48       $185B         +$47,7B
2017            R$ 3,19       $218B         +$67,0B
2018            R$ 3,65       $239B         +$58,7B
2019 (Bolson.)  R$ 3,95       $224B         +$46,7B
2020 (COVID)    R$ 5,16       $210B         +$50,4B
2021            R$ 5,39       $280B         +$61,0B
2022            R$ 5,17       $335B         +$62,3B
2023 (Lula)     R$ 4,99       $340B         +$98,8B
2024            R$ 5,18       $337B         +$74,5B
─────────────────────────────────────────────────────────────

Correlação câmbio x exportações: +0,67 (moderada positiva)
Conclusão: Real mais fraco ajuda exportações, mas não é o
único fator (demanda global, preço das commodities importam)
```

---

## Análise 5: Mercado de Crédito

> Prompt: "Como está o mercado de crédito brasileiro? Taxas médias, inadimplência e volume"

### Ferramentas

```
bacen_series_populares(categoria="credito")
→ Retorna séries de crédito disponíveis

bacen_comparar_series(
  codigos=[20714, 21082, 20539],
  ultimos=36
)
# 20714 = Taxa média de juros - pessoa física
# 21082 = Inadimplência - pessoa física (%)
# 20539 = Saldo de crédito total
```

---

## Análise 6: Comparação Internacional — PIB Per Capita

> Prompt: "Compare o PIB per capita do Brasil com os BRICS e principais economias. Use dados do IBGE e Banco Central"

### Ferramentas

```
bacen_indicadores_atuais()  # PIB Brasil
ibge_consultar_agregado(agregado=6579)  # PIB por estado
```

O LLM pode contextualizar com dados internacionais conhecidos:

```
PIB PER CAPITA — 2024 (USD PPP)

  🇺🇸 EUA         ███████████████████   $85.370
  🇩🇪 Alemanha    █████████████░░░░░░   $66.470
  🇫🇷 França      ████████████░░░░░░░   $58.770
  🇨🇳 China       ██████████░░░░░░░░░   $23.580
  🇧🇷 Brasil      █████████░░░░░░░░░░   $20.810
  🇲🇽 México      ████████░░░░░░░░░░░   $22.640
  🇿🇦 África Sul  ██████░░░░░░░░░░░░░   $16.090
  🇮🇳 Índia       ████░░░░░░░░░░░░░░░   $10.120

  Brasil: 24% do PIB/capita dos EUA
  Mas internamente: DF (R$ 91K) vs MA (R$ 15K) = 6x
```

---

## Séries Mais Usadas por Economistas

### Macroeconomia

| Código SGS | Série | Periodicidade |
|-----------|-------|---------------|
| 432 | Selic meta | Diária |
| 433 | IPCA mensal | Mensal |
| 13522 | IPCA acumulado 12m | Mensal |
| 1 | Dólar PTAX | Diária |
| 4380 | PIB mensal | Mensal |
| 24364 | Desemprego (PNAD) | Trimestral |

### Fiscal

| Código SGS | Série | Periodicidade |
|-----------|-------|---------------|
| 4503 | Receita governo central | Mensal |
| 4504 | Despesa governo central | Mensal |
| 4505 | Resultado primário | Mensal |
| 4513 | Dívida bruta/PIB | Mensal |
| 4514 | Dívida líquida/PIB | Mensal |

### Crédito

| Código SGS | Série | Periodicidade |
|-----------|-------|---------------|
| 20714 | Taxa média PF | Mensal |
| 21082 | Inadimplência PF | Mensal |
| 20539 | Saldo crédito total | Mensal |

### Setor Externo

| Código SGS | Série | Periodicidade |
|-----------|-------|---------------|
| 22707 | Exportações (FOB) | Mensal |
| 22708 | Importações (FOB) | Mensal |
| 22709 | Saldo balança comercial | Mensal |

> Prompt: "Busque séries sobre reservas internacionais"
> API: `bacen_buscar_serie(termo="reservas internacionais")`

---

## Fluxo de Trabalho do Economista

```
1. SNAPSHOT
   └── bacen_indicadores_atuais() → painel rápido

2. DEEP DIVE
   └── bacen_consultar_serie(codigo=X) → série específica
   └── bacen_calcular_variacao() → estatísticas

3. COMPARAÇÃO
   └── bacen_comparar_series() → múltiplas séries
   └── executar_lote() → múltiplas análises em paralelo

4. CONTEXTO
   └── ibge_consultar_agregado() → dados estruturais
   └── transparencia_despesas_por_funcao() → gastos do governo

5. RELATÓRIO
   └── Agente Redator → nota técnica formatada
```

---

_Fontes: API do Banco Central (SGS — 40.000+ séries), API do IBGE (Servicodados), API do Portal da Transparência._

_Nota: Códigos de séries são reais do SGS/BCB. Use `bacen_series_populares` ou `bacen_buscar_serie` para descobrir séries adicionais._
