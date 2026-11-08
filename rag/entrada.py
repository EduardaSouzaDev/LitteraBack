from pydantic import BaseModel
from rag.chunking import _norm, localizar_secao
from rag.llm_json import gerar_json
from rag.schemas import Contexto

PROMPT = """Você analisa pedidos de revisão de textos acadêmicos.
Leia a solicitação do usuário e extraia:
- "problema": qual dificuldade o usuário relata (ex.: falta de coesão entre as ideias do parágrafo)
- "objetivo": o que ele quer alcançar, incluindo o que deve ser preservado (ex.: melhorar a articulação entre as ideias, preservando o significado original e as citações)
{instrucao_trecho}

SOLICITAÇÃO:
{prompt}

Responda apenas com JSON neste formato:
{{"problema": "...", "objetivo": "...", "trecho_original": "..."}}
"""

INSTR_COM_TRECHO = '- "trecho_original": o trecho já foi informado separadamente; deixe como string vazia.'
INSTR_SEM_TRECHO = (
    '- "trecho_original": copie, sem alterar uma vírgula, o texto que o usuário colou na '
    "solicitação para ser revisado (se não houver, deixe vazio)."
)

OBJETIVO_PADRAO = "Melhorar o texto preservando o significado original e as citações."


class _Extraido(BaseModel):
    problema: str = ""
    objetivo: str = ""
    trecho_original: str = ""


def montar_contexto(documento: str, prompt_usuario: str, trecho: str | None = None) -> Contexto:
    trecho = (trecho or "").strip()
    extraido = gerar_json(
        PROMPT.format(
            instrucao_trecho=INSTR_COM_TRECHO if trecho else INSTR_SEM_TRECHO,
            prompt=prompt_usuario,
        ),
        _Extraido,
    )

    if not trecho:
        trecho = extraido.trecho_original.strip()
        valido = _norm(trecho) in _norm(prompt_usuario) or _norm(trecho) in _norm(documento)
        if not trecho or not valido:
            raise ValueError(
                "Não foi possível identificar o trecho a revisar. "
                "Envie-o no campo 'trecho' ou cole-o dentro do prompt."
            )

    secao = localizar_secao(documento, trecho)
    tipo = "parágrafo" if "\n\n" not in trecho else "trecho"
    elemento = f'{tipo} da seção "{secao}"' if secao else f"{tipo} do documento"

    return Contexto(
        problema=extraido.problema.strip() or "Não especificado pelo usuário",
        elemento_revisado=elemento,
        objetivo=extraido.objetivo.strip() or OBJETIVO_PADRAO,
        trecho_original=trecho,
    )