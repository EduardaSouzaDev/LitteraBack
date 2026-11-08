DIRETRIZES = [
    "Usar linguagem científica e impessoal quando apropriado.",
    "Manter clareza, coesão e coerência textual.",
    "Preservar o significado original do texto.",
    "Manter as citações e referências fornecidas, sem alterá-las.",
    "Não criar informações, dados ou referências que não foram fornecidas.",
    "Respeitar as instruções específicas do usuário.",
]
 
 
def diretrizes_como_texto() -> str:
    return "\n".join(f"- {d}" for d in DIRETRIZES)