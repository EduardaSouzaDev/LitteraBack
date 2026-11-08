import re
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 800    
CHUNK_OVERLAP = 100

_MD = re.compile(r"^#{1,6}\s+(.+?)\s*$")
_NUM = re.compile(r"^\d+(?:\.\d+)*\.?\s+[A-ZÀ-Ý].*$")
_CAPS = re.compile(r"^[A-ZÀ-Ý][A-ZÀ-Ý0-9 \-–:,]{3,80}$")

SECAO_INICIAL = "Início do documento"

def _norm(texto: str) -> str:
    return re.sub(r"\s+", " ", texto).strip().lower()

def _titulo(linha: str) -> str | None:
    """Devolve o título se a linha parecer um título de seção; senão None."""
    l = linha.strip()
    if not l:
        return None
    m = _MD.match(l)
    if m:
        return m.group(1)
    if len(l) <= 100 and len(l.split()) <= 12 and l[-1] not in ".;,:":
        if _NUM.match(l) or _CAPS.match(l):
            return l
    return None

def create_document(text: str, title: str | None = None) -> Document:
    return Document(page_content=text.strip(), metadata={"title": title or "Documento"})

def split_by_sections(text: str) -> list[tuple[str, str]]:
    """Divide o texto em (título_da_seção, conteúdo)."""
    secoes: list[tuple[str, str]] = []
    atual, buffer = SECAO_INICIAL, []

    for linha in text.splitlines():
        t = _titulo(linha)
        if t:
            conteudo = "\n".join(buffer).strip()
            if conteudo:
                secoes.append((atual, conteudo))
            atual, buffer = t, []
        else:
            buffer.append(linha)

    conteudo = "\n".join(buffer).strip()
    if conteudo:
        secoes.append((atual, conteudo))
    return secoes

def localizar_secao(documento: str, trecho: str) -> str | None:
    """Descobre em qual seção do documento o trecho está."""
    alvo = _norm(trecho)[:200]
    if not alvo:
        return None
    for titulo, conteudo in split_by_sections(documento):
        if alvo in _norm(conteudo):
            return titulo
    return None

def chunk_documents(documents: list[Document]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", "; ", " ", ""],  # prioriza parágrafos e frases
    )

    chunks: list[Document] = []
    for doc in documents:
        indice = 0
        for secao, conteudo in split_by_sections(doc.page_content):
            for pedaco in splitter.split_text(conteudo):
                chunks.append(
                    Document(
                        page_content=f"Seção: {secao}\n\n{pedaco}",
                        metadata={**doc.metadata, "section": secao, "chunk_index": indice},
                    )
                )
                indice += 1
    return chunks