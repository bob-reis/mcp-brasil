"""Pydantic schemas for the TCU feature."""

from __future__ import annotations

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Acórdãos
# ---------------------------------------------------------------------------


class Acordao(BaseModel):
    """Acórdão (decisão colegiada) do TCU."""

    key: str | None = None
    tipo: str | None = None
    ano_acordao: str | None = None
    titulo: str | None = None
    numero_acordao: str | None = None
    numero_ata: str | None = None
    colegiado: str | None = None
    data_sessao: str | None = None
    relator: str | None = None
    situacao: str | None = None
    sumario: str | None = None
    url_acordao: str | None = None


# ---------------------------------------------------------------------------
# Inabilitados
# ---------------------------------------------------------------------------


class Inabilitado(BaseModel):
    """Pessoa inabilitada para função pública por decisão do TCU."""

    nome: str | None = None
    cpf: str | None = None
    processo: str | None = None
    deliberacao: str | None = None
    data_transito_julgado: str | None = None
    data_final: str | None = None
    data_acordao: str | None = None
    uf: str | None = None
    municipio: str | None = None


class InabilitadoResultado(BaseModel):
    """Resultado paginado de inabilitados (ORDS)."""

    items: list[Inabilitado] = []
    has_more: bool = False
    limit: int = 25
    offset: int = 0
    count: int = 0


# ---------------------------------------------------------------------------
# Inidôneos
# ---------------------------------------------------------------------------


class Inidoneo(BaseModel):
    """Licitante declarado inidôneo pelo TCU."""

    nome: str | None = None
    cpf_cnpj: str | None = None
    processo: str | None = None
    deliberacao: str | None = None
    data_transito_julgado: str | None = None
    data_final: str | None = None
    data_acordao: str | None = None
    uf: str | None = None
    municipio: str | None = None


class InidoneoResultado(BaseModel):
    """Resultado paginado de inidôneos (ORDS)."""

    items: list[Inidoneo] = []
    has_more: bool = False
    limit: int = 25
    offset: int = 0
    count: int = 0


# ---------------------------------------------------------------------------
# Certidões APF
# ---------------------------------------------------------------------------


class TipoCertidao(BaseModel):
    """Tipo de certidão disponível no sistema APF."""

    orgao_emissor: str
    sigla: str
    descricao: str


class CertidaoItem(BaseModel):
    """Certidão individual dentro do resultado consolidado."""

    emissor: str | None = None
    tipo: str | None = None
    data_hora_emissao: str | None = None
    descricao: str | None = None
    situacao: str | None = None
    observacao: str | None = None
    link_consulta_manual: str | None = None


class CertidaoResultado(BaseModel):
    """Resultado consolidado de certidões para um CNPJ."""

    razao_social: str | None = None
    nome_fantasia: str | None = None
    cnpj: str | None = None
    uf: str | None = None
    certidoes: list[CertidaoItem] = []
    cnpj_encontrado_base_tcu: bool = False


# ---------------------------------------------------------------------------
# Cálculo de débito
# ---------------------------------------------------------------------------


class ParcelaDebito(BaseModel):
    """Parcela de débito para cálculo."""

    data_fato: str
    indicativo_debito_credito: str = "D"
    valor_original: float


class CalculoDebitoResultado(BaseModel):
    """Resultado do cálculo de débito atualizado."""

    data: str | None = None
    saldo_debito: float = 0.0
    saldo_variacao_selic: float = 0.0
    saldo_juros: float = 0.0
    saldo_total: float = 0.0


# ---------------------------------------------------------------------------
# Pedidos do Congresso
# ---------------------------------------------------------------------------


class PedidoCongresso(BaseModel):
    """Solicitação do Congresso Nacional ao TCU."""

    tipo: str | None = None
    numero: int | None = None
    data_aprovacao: str | None = None
    assunto: str | None = None
    autor: str | None = None
    processo_scn: str | None = None
    link_proposicao: str | None = None


class PedidoCongressoResultado(BaseModel):
    """Resultado paginado de pedidos do Congresso."""

    items: list[PedidoCongresso] = []
    has_next: bool = False


# ---------------------------------------------------------------------------
# Termos contratuais do TCU
# ---------------------------------------------------------------------------


class UnidadeFiscalizadora(BaseModel):
    """Unidade fiscalizadora do TCU."""

    codigo: int | None = None
    sigla: str | None = None
    nome: str | None = None


class TermoContratual(BaseModel):
    """Contrato ou termo contratual firmado pelo TCU."""

    tipo_contratacao: str | None = None
    numero: int | None = None
    ano: int | None = None
    unidade_gestora: str | None = None
    nome_fornecedor: str | None = None
    cnpj_fornecedor: str | None = None
    objeto: str | None = None
    valor_inicial: float | None = None
    valor_atualizado: float | None = None
    data_assinatura: str | None = None
    data_inicio_vigencia: str | None = None
    data_termino_vigencia: str | None = None
    modalidade_licitacao: str | None = None
    numero_processo: str | None = None
    numero_aditamentos: int | None = None
    unidades_fiscalizadoras: list[UnidadeFiscalizadora] = []


# ---------------------------------------------------------------------------
# CADIRREG
# ---------------------------------------------------------------------------


class PessoaCadirreg(BaseModel):
    """Pessoa com contas julgadas irregulares pelo TCU."""

    nome_responsavel: str | None = None
    cpf: str | None = None
    num_processo: str | None = None
    ano_processo: str | None = None
    julgamento: str | None = None
    unidade_tecnica_processo: str | None = None
    se_detentor_cargo_funcao_publica: str | None = None
    se_falecido: str | None = None
