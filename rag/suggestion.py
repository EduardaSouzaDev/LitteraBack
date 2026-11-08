from rag.guidelines import diretrizes_como_texto
from rag.llm_json import gerar_json
from rag.schemas import Analise, Contexto, SugestaoCorrecao

SYSTEM = (
    "Você é um assistente de revisão de textos acadêmicos em português. "
    "Você revisa, não reescreve do zero, e segue rigorosamente as diretrizes."
)

PROMPT = """## CONTEXTO
- Problema: {problema}
- Elemento revisado: {elemento}
- Objetivo: {objetivo}
- Tipo de revisão: {tipo}

## INSTRUÇÃO DO USUÁRIO
{prompt}

## TRECHO A REVISAR
{trecho}

## CONTEÚDO RELEVANTE DO DOCUMENTO (apenas para manter coerência; não reescreva estes trechos)
{conteudo}

## INFORMAÇÕES RELEVANTES
{info}

## DIRETRIZES DE ESCRITA ACADÊMICA
{diretrizes}

Retorne JSON com os campos:
- texto_original: o trecho original, sem alterações
- texto_revisado: o trecho revisado
- alteracoes: lista de objetos {{"descricao": "...", "justificativa": "..."}} (uma por mudança relevante)
- justificativa: síntese de por que a revisão melhora o texto
"""

def montar_prompt(contexto: Contexto, analise: Analise, prompt_usuario: str, conteudo: list[str]) -> str:
    return PROMPT.format(
        problema=contexto.problema,
        elemento=contexto.elemento_revisado,
        objetivo=contexto.objetivo,
        tipo=analise.tipo_revisao,
        prompt=prompt_usuario,
        trecho=contexto.trecho_original,
        conteudo="\n---\n".join(conteudo) or "(nenhum)",
        info="\n".join(f"- {i}" for i in analise.informacoes_relevantes),
        diretrizes=diretrizes_como_texto(),
    )

def gerar_sugestao(contexto: Contexto, analise: Analise, prompt_usuario: str, conteudo: list[str]) -> SugestaoCorrecao:
    sugestao = gerar_json(montar_prompt(contexto, analise, prompt_usuario, conteudo), SugestaoCorrecao, system=SYSTEM)
    sugestao.texto_original = contexto.trecho_original  # garante que o original nunca é alterado
    return sugestao