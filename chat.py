"""Teste no terminal:  python chat.py caminho/do/documento.txt"""
import sys
from pathlib import Path

from rag.embeddings import indexar_documento
from rag.pipeline import formatar_saida, revisar

if len(sys.argv) < 2:
    sys.exit("Uso: python chat.py <arquivo.txt|.md>")

texto = Path(sys.argv[1]).read_text(encoding="utf-8")
doc_id, n = indexar_documento(texto, Path(sys.argv[1]).stem)
print(f"Documento indexado ({n} chunks). Digite o pedido (cole o trecho junto). Ctrl+C para sair.\n")

while True:
    pedido = input("Pedido> ").strip()
    if not pedido:
        continue
    try:
        print("\n" + formatar_saida(revisar(doc_id, pedido)) + "\n")
    except (ValueError, FileNotFoundError) as e:
        print(f"Erro: {e}\n")