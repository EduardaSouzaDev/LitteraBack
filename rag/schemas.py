from pydantic import BaseModel, Field

class Contexto(BaseModel):
    """Saída da etapa 3 (Entrada de dados)."""
    problema: str = Field(..., description="Ex.: falta de coesão entre as ideias do parágrafo")
    elemento_revisado: str = Field(..., description="Ex.: parágrafo da seção de fundamentação teórica")
    objetivo: str = Field(..., description="Ex.: melhorar a articulação entre as ideias, preservando o significado e as citações")
    trecho_original: str = Field(..., description="Texto exato que será revisado")

class Analise(BaseModel):
    """Saída da etapa 4 (Análise da solicitação)."""
    tipo_revisao: str  
    informacoes_relevantes: list[str]
    consultas_recuperacao: list[str]  

class Alteracao(BaseModel):
    descricao: str
    justificativa: str

class SugestaoCorrecao(BaseModel):
    """Saída da etapa 6."""
    texto_original: str
    texto_revisado: str
    alteracoes: list[Alteracao]
    justificativa: str