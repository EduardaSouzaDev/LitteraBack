from rag.guidelines import diretrizes_como_texto
from rag.llm_json import gerar_json
from rag.schemas import Analise, Contexto
 
PROMPT = """Analise a solicitação de revisão abaixo.
 
CONTEXTO:
- Problema: {problema}
- Elemento: {elemento}
- Objetivo: {objetivo}
- Trecho: {trecho}
 
SOLICITAÇÃO ORIGINAL: {prompt}
 
DIRETRIZES DE ESCRITA ACADÊMICA:
{diretrizes}
 
Retorne:
- tipo_revisao: um entre coesão, clareza, concisão, gramática, formalidade, estrutura
- informacoes_relevantes: lista curta do que importa para a revisão (citações a preservar, termos-chave, restrições do usuário)
- consultas_recuperacao: 1 a 3 consultas curtas para buscar, no restante do documento, trechos que ajudem a manter a coerência (termos, conceitos, seção)
"""

def analisar_solicitacao(contexto: Contexto, prompt_usuario: str) -> Analise:
    return gerar_json(
        PROMPT.format(
            problema=contexto.problema,
            elemento=contexto.elemento_revisado,
            objetivo=contexto.objetivo,
            trecho=contexto.trecho_original,
            prompt=prompt_usuario,
            diretrizes=diretrizes_como_texto(),
        ),
        Analise,
    )