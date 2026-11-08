from rag.analise import analisar_solicitacao
from rag.embeddings import carregar_texto
from rag.entrada import montar_contexto
from rag.retrieval import recuperar_conteudo
from rag.schemas import SugestaoCorrecao
from rag.suggestion import gerar_sugestao

def revisar(doc_id: str, prompt_usuario: str, trecho: str | None = None) -> SugestaoCorrecao:
    documento = carregar_texto(doc_id)                                      
    contexto = montar_contexto(documento, prompt_usuario, trecho)              
    analise = analisar_solicitacao(contexto, prompt_usuario)                
    consultas = analise.consultas_recuperacao or [contexto.trecho_original[:300]]
    conteudo = recuperar_conteudo(doc_id, consultas, contexto.trecho_original) 
    return gerar_sugestao(contexto, analise, prompt_usuario, conteudo)        

def formatar_saida(s: SugestaoCorrecao) -> str:
    alt = "\n".join(f"- {a.descricao} ({a.justificativa})" for a in s.alteracoes)
    return (
        f"Texto original:\n{s.texto_original}\n\n"
        f"Correção sugerida:\n{s.texto_revisado}\n\n"
        f"Alterações propostas:\n{alt}\n\n"
        f"Justificativa de alteração:\n{s.justificativa}"
    )