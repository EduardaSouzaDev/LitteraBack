from pydantic import BaseModel, Field

class DocumentoRequest(BaseModel):
    texto: str = Field(..., min_length=50, description="Texto completo do documento acadêmico")
    titulo: str | None = None

class DocumentoResponse(BaseModel):
    documento_id: str
    n_chunks: int

class RevisaoRequest(BaseModel):
    documento_id: str
    prompt: str = Field(..., min_length=3, description="Pedido do usuário")
    trecho: str | None = Field(None, description="Trecho a revisar (opcional se estiver colado no prompt)")