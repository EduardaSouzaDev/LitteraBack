import os
from functools import lru_cache

from langchain_ollama import ChatOllama

@lru_cache(maxsize=2)
def get_llm(json_mode: bool = False) -> ChatOllama:
    return ChatOllama(
        model=os.environ.get("OLLAMA_MODEL", "qwen2:7b"),
        temperature=0,
        base_url=os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434"),
        num_ctx=int(os.environ.get("OLLAMA_NUM_CTX", "8192")),
        format="json" if json_mode else None,
    )

def generate(prompt: str, system: str | None = None, json_mode: bool = False) -> str:
    mensagens = []
    if system:
        mensagens.append(("system", system))
    mensagens.append(("human", prompt))
    return get_llm(json_mode).invoke(mensagens).content