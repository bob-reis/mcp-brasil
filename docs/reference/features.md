# Catalogo de Features

27 features · 205 tools · 58 resources · 47 prompts

---

## Economico

### `ibge` — IBGE (9 tools)

Instituto Brasileiro de Geografia e Estatistica — estados, municipios, nomes, agregados estatisticos, CNAE, malhas geograficas.

| Tool | Descricao |
|------|-----------|
| `ibge_listar_estados` | Lista os 27 estados com codigo, nome, sigla e regiao |
| `ibge_buscar_municipios` | Municipios por codigo do estado |
| `ibge_listar_regioes` | Lista as 5 regioes do Brasil |
| `ibge_consultar_nome` | Frequencia de nomes pelo censo do IBGE |
| `ibge_ranking_nomes` | Nomes mais comuns por estado/municipio |
| `ibge_consultar_agregado` | Agregados estatisticos (populacao, PIB, area, series de pesquisa) |
| `ibge_listar_pesquisas` | Lista programas de pesquisa do IBGE |
| `ibge_obter_malha` | Malhas geograficas (GeoJSON) de estados/municipios |
| `ibge_buscar_cnae` | Busca codigos CNAE de atividades economicas |

**Chave:** Nenhuma

---

### `bacen` — Banco Central do Brasil (9 tools)

Selic, IPCA, cambio, PIB, +190 series do SGS, Boletim Focus.

| Tool | Descricao |
|------|-----------|
| `bacen_consultar_serie` | Consulta qualquer serie BCB/SGS por codigo |
| `bacen_ultimos_valores` | Ultimos N valores de uma serie |
| `bacen_metadados_serie` | Metadados (nome, unidade, periodicidade) |
| `bacen_series_populares` | Lista curada de series populares (Selic, IPCA, dolar, etc.) |
| `bacen_buscar_serie` | Busca series por palavra-chave |
| `bacen_indicadores_atuais` | Busca paralela: Selic, IPCA, IPCA-12m, dolar, IBC-Br |
| `bacen_calcular_variacao` | Variacao percentual entre duas datas |
| `bacen_comparar_series` | Compara 2-5 series lado a lado |
| `bacen_expectativas_focus` | Expectativas do mercado (Boletim Focus) |

**Chave:** Nenhuma

---

## Legislativo

### `camara` — Camara dos Deputados (10 tools)

Deputados, proposicoes, votacoes, despesas, comissoes, frentes parlamentares.

| Tool | Descricao |
|------|-----------|
| `camara_listar_deputados` | Lista deputados com filtros (nome, partido, UF) |
| `camara_buscar_deputado` | Detalhes de um deputado por ID |
| `camara_buscar_proposicao` | Projetos de lei por tipo, ano, tema, autor |
| `camara_consultar_tramitacao` | Historico de tramitacao de uma proposicao |
| `camara_buscar_votacao` | Sessoes de votacao |
| `camara_votos_nominais` | Votos nominais (como cada deputado votou) |
| `camara_despesas_deputado` | Relatorio de despesas de deputados |
| `camara_agenda_legislativa` | Calendario legislativo |
| `camara_buscar_comissoes` | Comissoes da Camara |
| `camara_frentes_parlamentares` | Frentes parlamentares |

**Chave:** Nenhuma

---

### `senado` — Senado Federal (26 tools)

Senadores, materias, votacoes, comissoes, agenda, liderancas.

**Senadores (4):** `senado_listar_senadores`, `senado_buscar_senador`, `senado_buscar_senador_por_nome`, `senado_votacoes_senador`

**Materias (5):** `senado_buscar_materia`, `senado_detalhe_materia`, `senado_consultar_tramitacao_materia`, `senado_textos_materia`, `senado_votos_materia`

**Votacoes (3):** `senado_listar_votacoes`, `senado_detalhe_votacao`, `senado_votacoes_recentes`

**Comissoes (4):** `senado_listar_comissoes`, `senado_detalhe_comissao`, `senado_membros_comissao`, `senado_reunioes_comissao`

**Agenda (2):** `senado_agenda_plenario`, `senado_agenda_comissoes`

**Auxiliar (6):** `senado_legislatura_atual`, `senado_partidos_senado`, `senado_ufs_senado`, `senado_tipos_materia`, `senado_emendas_materia`, `senado_listar_blocos`

**Extra (2):** `senado_listar_liderancas`, `senado_relatorias_senador`

**Chave:** Nenhuma

---

## Transparencia / Fiscal

### `transparencia` — Portal da Transparencia (18 tools)

Contratos federais, despesas, servidores, sancoes, bolsa familia, emendas, viagens, cartoes de pagamento.

| Tool | Descricao |
|------|-----------|
| `transparencia_buscar_contratos` | Contratos federais |
| `transparencia_consultar_despesas` | Despesas por funcao/UF/ano |
| `transparencia_buscar_servidores` | Servidores publicos federais |
| `transparencia_buscar_licitacoes` | Processos licitatorios |
| `transparencia_consultar_bolsa_familia` | Beneficiarios do Bolsa Familia |
| `transparencia_buscar_sancoes` | Sancoes (CEIS/CNEP/CEPIM/CEAF) |
| `transparencia_buscar_emendas` | Emendas parlamentares |
| `transparencia_consultar_viagens` | Viagens a servico do governo |
| `transparencia_buscar_convenios` | Convenios |
| `transparencia_buscar_cartoes_pagamento` | Transacoes de cartoes de pagamento |
| `transparencia_buscar_pep` | Pessoas politicamente expostas |
| `transparencia_buscar_acordos_leniencia` | Acordos de leniencia |
| `transparencia_buscar_notas_fiscais` | Notas fiscais |
| `transparencia_consultar_beneficio_social` | Beneficios sociais |
| `transparencia_consultar_cpf` | Consulta CPF |
| `transparencia_consultar_cnpj` | Consulta CNPJ |
| `transparencia_detalhar_contrato` | Detalhes de um contrato |
| `transparencia_detalhar_servidor` | Detalhes de um servidor |

**Chave:** Opcional — [cadastro gratuito](http://portaldatransparencia.gov.br/api-de-dados/cadastrar-email)

---

### `tcu` — Tribunal de Contas da Uniao (8 tools)

Acordaos, licitantes inabilitados/inidoneos, certidoes APF, debitos, contratos.

| Tool | Descricao |
|------|-----------|
| `tcu_buscar_acordaos` | Acordaos do TCU |
| `tcu_consultar_inabilitados` | Pessoas inabilitadas |
| `tcu_consultar_inidoneos` | Empresas inidoneas |
| `tcu_consultar_certidoes_apf` | Certidoes APF (TCU + CNJ + CGU) |
| `tcu_calcular_debito_tcu` | Correcao de debito via SELIC |
| `tcu_buscar_pedidos_congresso` | Pedidos do Congresso ao TCU |
| `tcu_buscar_contratos_tcu` | Contratos do TCU |
| `tcu_consultar_cadirreg` | Registro de irregularidades (CADIRREG) |

**Chave:** Nenhuma

---

### Tribunais de Contas Estaduais (9 features)

| Feature | UF | Tools | Cobertura |
|---------|-----|-------|-----------|
| `tce_sp` | Sao Paulo | 3 | Despesas, receitas, municipios |
| `tce_rj` | Rio de Janeiro | 7 | Licitacoes, contratos, obras, penalidades |
| `tce_rs` | Rio Grande do Sul | 5 | Educacao, saude, gestao fiscal (LRF) |
| `tce_sc` | Santa Catarina | 2 | Municipios, unidades gestoras |
| `tce_pe` | Pernambuco | 5 | Licitacoes, contratos, despesas, fornecedores |
| `tce_ce` | Ceara | 4 | Licitacoes, contratos, empenhos |
| `tce_rn` | Rio Grande do Norte | 5 | Jurisdicionados, licitacoes, contratos |
| `tce_pi` | Piaui | 5 | Prefeituras, despesas, receitas |
| `tce_to` | Tocantins | 3 | Processos, pautas de sessoes |

**Chave:** Nenhuma (todas)

---

## Judiciario

### `datajud` — DataJud / CNJ (7 tools)

Processos judiciais de todos os tribunais brasileiros, movimentacoes, busca avancada.

| Tool | Descricao |
|------|-----------|
| `datajud_buscar_processos` | Processos com filtros diversos |
| `datajud_buscar_processo_por_numero` | Processo por numero (formato CNJ) |
| `datajud_buscar_processos_por_classe` | Por codigo de classe processual |
| `datajud_buscar_processos_por_assunto` | Por codigo de assunto |
| `datajud_buscar_processos_por_orgao` | Por tribunal/orgao julgador |
| `datajud_buscar_processos_avancado` | Busca avancada com paginacao `search_after` |
| `datajud_consultar_movimentacoes` | Movimentacoes de um processo |

**Chave:** Opcional — [cadastro gratuito](https://datajud-wiki.cnj.jus.br/api-publica/acesso)

---

### `jurisprudencia` — STF, STJ, TST (6 tools)

Decisoes dos tribunais superiores, sumulas, repercussao geral, informativos.

| Tool | Descricao |
|------|-----------|
| `jurisprudencia_buscar_jurisprudencia_stf` | Decisoes do STF |
| `jurisprudencia_buscar_jurisprudencia_stj` | Decisoes do STJ |
| `jurisprudencia_buscar_jurisprudencia_tst` | Decisoes trabalhistas do TST |
| `jurisprudencia_buscar_sumulas` | Sumulas de todos os tribunais |
| `jurisprudencia_buscar_repercussao_geral` | Temas de repercussao geral (STF) |
| `jurisprudencia_buscar_informativos` | Boletins informativos dos tribunais |

**Chave:** Nenhuma

---

## Eleitoral

### `tse` — Tribunal Superior Eleitoral (15 tools)

Eleicoes, candidatos, resultados, prestacao de contas, apuracao.

| Tool | Descricao |
|------|-----------|
| `tse_anos_eleitorais` | Anos com eleicoes disponiveis |
| `tse_listar_eleicoes` | Eleicoes por ano |
| `tse_listar_eleicoes_suplementares` | Eleicoes suplementares |
| `tse_listar_estados_suplementares` | Estados com eleicoes suplementares |
| `tse_listar_cargos` | Cargos em disputa |
| `tse_listar_candidatos` | Candidatos com filtros |
| `tse_buscar_candidato` | Detalhes de um candidato |
| `tse_resultado_eleicao` | Resultado de uma eleicao |
| `tse_consultar_prestacao_contas` | Prestacao de contas de candidatos |
| `tse_resultado_nacional` | Resultado nacional via CDN |
| `tse_resultado_por_estado` | Resultado por estado |
| `tse_mapa_resultado_estados` | Mapa de resultados (27 estados em paralelo) |
| `tse_listar_municipios_eleitorais` | Municipios eleitorais |
| `tse_resultado_por_municipio` | Resultado por municipio |
| `tse_apuracao_status` | Status da apuracao |

**Chave:** Nenhuma

---

## Ambiental

### `inpe` — INPE (4 tools)

Focos de queimadas, desmatamento (PRODES e DETER), dados de satelite.

| Tool | Descricao |
|------|-----------|
| `inpe_buscar_focos_queimadas` | Focos ativos de incendio |
| `inpe_consultar_desmatamento` | Dados de desmatamento (PRODES) |
| `inpe_alertas_deter` | Alertas de desmatamento (DETER) |
| `inpe_dados_satelite` | Dados por sensor de satelite |

**Chave:** Nenhuma

---

### `ana` — Agencia Nacional de Aguas (3 tools)

Estacoes hidrologicas, telemetria (chuva, vazao, nivel), reservatorios.

| Tool | Descricao |
|------|-----------|
| `ana_buscar_estacoes` | Estacoes de monitoramento hidrologico |
| `ana_consultar_telemetria` | Leituras de telemetria |
| `ana_monitorar_reservatorios` | Monitoramento de reservatorios (SAR/ANA) |

**Chave:** Nenhuma

---

## Saude

### `saude` — CNES / DataSUS (4 tools)

Estabelecimentos de saude, profissionais, leitos.

| Tool | Descricao |
|------|-----------|
| `saude_buscar_estabelecimentos` | Estabelecimentos de saude (CNES) |
| `saude_buscar_profissionais` | Profissionais de saude |
| `saude_listar_tipos_estabelecimento` | Tipos de estabelecimento |
| `saude_consultar_leitos` | Disponibilidade de leitos |

**Chave:** Nenhuma

---

## Compras Publicas

### `compras/pncp` — PNCP (6 tools)

Portal Nacional de Contratacoes Publicas (Lei 14.133/2021).

| Tool | Descricao |
|------|-----------|
| `compras_pncp_buscar_contratacoes` | Contratacoes por texto, CNPJ, data |
| `compras_pncp_buscar_contratos` | Contratos por texto, CNPJ do fornecedor |
| `compras_pncp_buscar_atas` | Atas de registro de preco |
| `compras_pncp_consultar_fornecedor` | Dados do fornecedor por CNPJ |
| `compras_pncp_buscar_itens` | Itens de contratacao |
| `compras_pncp_consultar_orgao` | Orgaos contratantes |

**Chave:** Nenhuma

---

### `compras/dadosabertos` — ComprasNet / SIASG (8 tools)

Dados legados de compras publicas (ate ~2020).

| Tool | Descricao |
|------|-----------|
| `compras_dadosabertos_buscar_licitacoes` | Processos licitatorios por data |
| `compras_dadosabertos_buscar_pregoes` | Pregoes eletronicos |
| `compras_dadosabertos_buscar_dispensas` | Dispensas/inexigibilidades |
| `compras_dadosabertos_buscar_contratos` | Contratos por vigencia |
| `compras_dadosabertos_consultar_fornecedor` | Fornecedores por CNPJ/CPF |
| `compras_dadosabertos_buscar_material_catmat` | Catalogo CATMAT (materiais) |
| `compras_dadosabertos_buscar_servico_catser` | Catalogo CATSER (servicos) |
| `compras_dadosabertos_buscar_uasg` | Codigos UASG de orgaos |

**Chave:** Nenhuma

---

## Utilidades

### `brasilapi` — BrasilAPI (16 tools)

CEP, CNPJ, DDD, bancos, cambio, FIPE, feriados, PIX, ISBN, NCM.

| Tool | Descricao |
|------|-----------|
| `brasilapi_consultar_cep` | Consulta CEP |
| `brasilapi_consultar_cnpj` | Consulta CNPJ |
| `brasilapi_consultar_ddd` | Consulta DDD |
| `brasilapi_listar_bancos` | Lista bancos |
| `brasilapi_consultar_banco` | Detalhes de um banco |
| `brasilapi_listar_moedas` | Lista moedas disponiveis |
| `brasilapi_consultar_cotacao` | Cotacao de moeda |
| `brasilapi_consultar_feriados` | Feriados nacionais por ano |
| `brasilapi_consultar_taxa` | Taxas (SELIC/CDI/IPCA/TR) |
| `brasilapi_listar_tabelas_fipe` | Tabelas FIPE |
| `brasilapi_listar_marcas_fipe` | Marcas na FIPE |
| `brasilapi_buscar_veiculos_fipe` | Veiculos na FIPE |
| `brasilapi_consultar_isbn` | Consulta ISBN de livros |
| `brasilapi_buscar_ncm` | Nomenclatura Comum do Mercosul |
| `brasilapi_consultar_pix_participantes` | Participantes do PIX |
| `brasilapi_consultar_registro_br` | Dominios .br |

**Chave:** Nenhuma

---

### `dados_abertos` — Portal Dados Abertos (4 tools)

Catalogo de datasets de dados.gov.br.

| Tool | Descricao |
|------|-----------|
| `dados_abertos_buscar_conjuntos` | Busca datasets |
| `dados_abertos_detalhar_conjunto` | Detalhes de um dataset |
| `dados_abertos_listar_organizacoes` | Organizacoes publicadoras |
| `dados_abertos_buscar_recursos` | Recursos/arquivos dentro de um dataset |

**Chave:** Nenhuma

---

### `diario_oficial` — Querido Diario (4 tools)

Diarios oficiais de 5.000+ municipios brasileiros.

| Tool | Descricao |
|------|-----------|
| `diario_oficial_buscar_diarios` | Busca full-text em diarios oficiais |
| `diario_oficial_buscar_trechos` | Trechos de um municipio especifico |
| `diario_oficial_buscar_cidades` | Busca municipios por nome (codigo IBGE) |
| `diario_oficial_listar_territorios` | Territorios com diarios disponiveis |

**Chave:** Nenhuma

---

### `transferegov` — TransfereGov (5 tools)

Emendas parlamentares PIX (transferencias especiais).

| Tool | Descricao |
|------|-----------|
| `transferegov_buscar_emendas_pix` | Emendas PIX por ano/estado |
| `transferegov_buscar_emenda_por_autor` | Emendas por nome do parlamentar |
| `transferegov_detalhe_emenda` | Detalhes por ID do plano de acao |
| `transferegov_emendas_por_municipio` | Emendas para um municipio |
| `transferegov_resumo_emendas_ano` | Resumo anual de emendas PIX |

**Chave:** Nenhuma

---

## Agentes IA

### `redator` — Redator Oficial (5 tools + 6 prompts + 10 resources)

Agente inteligente para redacao oficial brasileira — oficio, despacho, memorando, portaria, parecer, nota tecnica.

**Tools:**

| Tool | Descricao |
|------|-----------|
| `redator_formatar_data_extenso` | Formata data por extenso em portugues |
| `redator_gerar_numeracao` | Gera numeracao oficial de documentos |
| `redator_consultar_pronome_tratamento` | Pronome de tratamento correto por cargo |
| `redator_validar_documento` | Valida CPF/CNPJ |
| `redator_listar_tipos_documento` | Lista tipos de documento suportados |

**Prompts:** `redator_despacho`, `redator_memorando`, `redator_oficio`, `redator_portaria`, `redator_parecer`, `redator_nota_tecnica`

**Resources:** 7 templates de documentos + 3 documentos normativos (manual de redacao, pronomes, fechos)

**Chave:** Nenhuma
