from fastapi import FastAPI, HTTPException

from api_schemas import DocumentoRequest, DocumentoResponse, RevisaoRequest
from rag.embeddings import indexar_documento
from rag.pipeline import revisar
from rag.schemas import SugestaoCorrecao

app = FastAPI(title="Littera – Revisão de textos acadêmicos")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/documentos", response_model=DocumentoResponse)
def enviar_documento(req: DocumentoRequest):
    """Etapa (1): indexa o documento uma vez; depois é só revisar várias vezes."""
    doc_id, n = indexar_documento(req.texto, req.titulo)
    return DocumentoResponse(documento_id=doc_id, n_chunks=n)

@app.post("/revisar", response_model=SugestaoCorrecao)
def revisar_trecho(req: RevisaoRequest):
    """Etapas (2) a (6): prompt -> contexto -> análise -> LLM -> sugestão."""
    try:
        return revisar(req.documento_id, req.prompt, req.trecho)
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(422, str(e))