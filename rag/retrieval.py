from rag.chunking import _norm
from rag.embeddings import get_vector_store

def _sobrepoe(corpo: str, alvo: str) -> bool:
    c = _norm(corpo)
    return bool(c) and (c[:80] in alvo or alvo[:80] in c)

def recuperar_conteudo(doc_id: str, consultas: list[str], trecho: str, k: int = 4) -> list[str]:
    db = get_vector_store(doc_id)
    alvo = _norm(trecho)
    vistos: set[str] = set()
    resultado: list[str] = []

    for consulta in consultas:
        for d in db.similarity_search(consulta, k=k):
            corpo = d.page_content
            if corpo in vistos or _sobrepoe(corpo.split("\n\n", 1)[-1], alvo):
                continue  # ignora duplicados e o próprio trecho que está sendo revisado
            vistos.add(corpo)
            resultado.append(corpo)
    return resultado[:k]