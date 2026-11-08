import hashlib
import os
from functools import lru_cache
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from rag.chunking import chunk_documents, create_document

DATA_DIR = Path(os.environ.get("DATA_DIR", "data"))

_embeddings: HuggingFaceEmbeddings | None = None


def _get_embeddings() -> HuggingFaceEmbeddings:
    """Embedder singleton (carrega o modelo só na primeira chamada)."""
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    return _embeddings


def documento_id(texto: str) -> str:
    return hashlib.sha256(texto.strip().encode("utf-8")).hexdigest()[:16]


def _dir(doc_id: str) -> Path:
    return DATA_DIR / doc_id


def _indice_existe(doc_id: str) -> bool:
    return (_dir(doc_id) / "chroma" / "chroma.sqlite3").exists()


def indexar_documento(texto: str, titulo: str | None = None) -> tuple[str, int]:
    """Indexa o documento e devolve (documento_id, n_chunks)."""
    doc_id = documento_id(texto)
    pasta = _dir(doc_id)
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / "texto.txt").write_text(texto.strip(), encoding="utf-8")

    if _indice_existe(doc_id):
        return doc_id, get_vector_store(doc_id)._collection.count()

    chunks = chunk_documents([create_document(texto, titulo)])
    Chroma.from_documents(
        chunks,
        _get_embeddings(),
        persist_directory=str(pasta / "chroma"),
    )
    get_vector_store.cache_clear()
    return doc_id, len(chunks)


@lru_cache(maxsize=16)
def get_vector_store(doc_id: str) -> Chroma:
    if not _indice_existe(doc_id):
        raise FileNotFoundError(f"Documento '{doc_id}' não encontrado. Envie-o primeiro em POST /documentos.")
    return Chroma(
        persist_directory=str(_dir(doc_id) / "chroma"),
        embedding_function=_get_embeddings(),
    )


def carregar_texto(doc_id: str) -> str:
    arq = _dir(doc_id) / "texto.txt"
    if not arq.exists():
        raise FileNotFoundError(f"Documento '{doc_id}' não encontrado.")
    return arq.read_text(encoding="utf-8")