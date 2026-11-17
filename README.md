# Littera

Back-end do **Littera**: um pipeline de **RAG** (Retrieval-Augmented Generation) que roda 100% local. Ele indexa um conteúdo em um banco vetorial (Chroma), busca os trechos mais relevantes para cada pergunta e usa um LLM rodando no Ollama para gerar a resposta em português.

---

## Visão geral do fluxo

1. **Ingestão** — lê o conteúdo de entrada, divide em *chunks*, gera os *embeddings* e persiste os vetores em `chroma_dbs/<hash>/` (um diretório por fonte normalizada).
2. **Consulta** — via `chat.py` (CLI) ou `api.py` (FastAPI): busca os trechos semelhantes, monta o contexto e o LLM gera a resposta em português.

```
Documento ──► chunking ──► embeddings ──► Chroma (chroma_dbs/<hash>/)
                                               │
Pergunta ──► embeddings ──► retrieval ◄────────┘
                               │
                               ▼
                    contexto + prompt ──► LLM (Ollama) ──► resposta
```

---

## Estrutura do projeto

```
LitteraBack/
├── api.py               # API REST (FastAPI)
├── api_schemas.py       # Schemas de request/response da API
├── chat.py              # Interface de linha de comando (CLI)
├── meu_documento.txt    # Documento de exemplo
├── requirements.txt     # Dependências Python
├── data/                # Dados locais (índices Chroma e textos)
└── rag/
    ├── entrada.py       # Entrada/leitura do conteúdo
    ├── chunking.py      # Divisão do texto em chunks
    ├── embeddings.py    # Geração de embeddings
    ├── retrieval.py     # Busca dos trechos mais relevantes
    ├── llm.py           # Comunicação com o LLM (Ollama)
    ├── llm_json.py      # Respostas estruturadas (JSON) do LLM
    ├── guidelines.py    # Diretrizes/regras aplicadas nas respostas
    ├── analise.py       # Análise do conteúdo
    ├── suggestion.py    # Geração de sugestões
    ├── schemas.py       # Modelos de dados do pipeline
    └── pipeline.py      # Orquestra o fluxo ponta a ponta
```

---

## Pré-requisitos

| Requisito | Detalhes |
| --- | --- |
| **Python** | 3.12 ou superior |
| **Ollama** | [Download](https://ollama.com/download) — executa o modelo de chat localmente |
| **Espaço em disco** | PyTorch + modelo de embedding + Chroma ocupam alguns GB |

---

## Tutorial: uso local

### 1. Clonar o repositório e criar o ambiente virtual

```bash
git clone <URL_DO_REPOSITORIO>
cd LitteraBack

python -m venv .venv
```

Ativar o ambiente:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate
```

### 2. Instalar as dependências

Na pasta do repositório:

```bash
pip install -r requirements.txt
```

### 3. Instalar o modelo de chat no Ollama

```bash
ollama pull qwen2:7b
```

Para usar outro modelo, defina a variável `OLLAMA_MODEL` e faça o `pull` correspondente:

```bash
# Exemplo (Windows PowerShell)
$env:OLLAMA_MODEL = "llama3.1:8b"
ollama pull llama3.1:8b

# Exemplo (Linux / macOS)
export OLLAMA_MODEL="llama3.1:8b"
ollama pull llama3.1:8b
```

### 4. Rodar o pipeline (CLI)

Com o Ollama em execução:

```bash
python chat.py meu_documento.txt
```

Na primeira execução o documento é indexado; nas seguintes o índice existente é reaproveitado e você já pode fazer perguntas.

- O índice fica em `chroma_dbs/<hash>/`.
- O legado `./chroma_db` ainda é suportado pela API, caso exista.

### 5. Rodar a API (FastAPI)

```bash
uvicorn api:app --reload
```

> Se o `uvicorn` não estiver no `requirements.txt`, instale com `pip install uvicorn`.

Com a API no ar, a documentação interativa (Swagger) fica disponível em:

- http://localhost:8000/docs

---

## Configuração

| Variável | Descrição | Padrão |
| --- | --- | --- |
| `OLLAMA_MODEL` | Modelo de chat usado pelo Ollama | `qwen2:7b` |

---

## Solução de problemas

- **Erro de conexão com o Ollama** — confirme que o Ollama está rodando (`ollama serve`) e que o modelo foi baixado (`ollama list`).
- **Respostas lentas** — modelos de 7B+ em CPU são lentos; use uma GPU ou um modelo menor.
- **Índice desatualizado** — apague o diretório correspondente em `chroma_dbs/<hash>/` para forçar uma nova ingestão.
- **Erro ao instalar PyTorch** — verifique se você está usando Python 3.12+ e se há espaço em disco suficiente.