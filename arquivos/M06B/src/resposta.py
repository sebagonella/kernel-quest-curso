"""
RPG Engine — a resposta estruturada da IA (saída estruturada, validada com Pydantic).

Desde o M06B, o NPC não devolve só um texto: devolve dados, num JSON com forma
fixa. A fala vai para a caixa de diálogo, a emoção vira um balão acima do NPC e
a ação é uma SUGESTÃO que o jogo confere antes de executar (validar_acao, no Model).
Este arquivo não sabe de rede nem de tela: só diz qual é a forma da resposta e
como transformar o texto da IA nessa forma, sem deixar um JSON quebrado derrubar o jogo.
"""
import logging
from typing import Literal

from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

# As emoções que têm balão (assets/interface/emocao_<nome>.png).
EMOCOES = ["feliz", "bravo", "surpreso", "pensativo"]
# As únicas ações que a IA pode sugerir. Literal: qualquer outro texto é recusado pelo Pydantic.
Acao = Literal["nenhuma", "dar_item", "abrir_loja", "abrir_portao"]

# A fala do NPC quando a resposta da IA não vale (JSON quebrado ou fora da forma).
FALA_PADRAO = "O personagem hesita e não diz nada que faça sentido. Tente de novo."


class RespostaNPC(BaseModel):
    """A forma da resposta. O Gemini recebe o schema desta classe e responde nela."""
    # As descrições vão junto no schema: são instruções para o modelo, campo a campo.
    fala: str = Field(description="O que o personagem diz, no tom da persona.")
    emocao: str = Field(description="A emoção da fala: feliz, bravo, surpreso ou pensativo.")
    acao: Acao = Field(description="O que o personagem faz no jogo; quase sempre nenhuma.")


def so_fala(fala, emocao="pensativo"):
    """Uma resposta sem ação: as falas fixas (erro, IA falsa) também têm a forma da IA."""
    return RespostaNPC(fala=fala, emocao=emocao, acao="nenhuma")


def interpretar(texto):
    """O texto JSON da IA vira uma RespostaNPC validada; resposta inválida vira a FALA_PADRAO."""
    # TODO (Passo 2): um JSON quebrado (ou com uma ação fora da lista) levanta ValidationError
    # e derruba o jogo. Capture o erro: registre um aviso no log e devolva a FALA_PADRAO.
    return RespostaNPC.model_validate_json(texto)  # TODO (Passo 2): e se o texto não validar?


# IA falsa (IA_FALSA=1): uma palavra na frase do jogador vira a ação, sem rede e sem cota.
# Ela obedece a qualquer pedido, como um modelo convencido por uma injeção de prompt.
PEDIDOS_FALSOS = {"portão": "abrir_portao", "portao": "abrir_portao", "loja": "abrir_loja",
                  "chave": "dar_item"}


def resposta_falsa(fala, primeiro_turno):
    """A resposta da IA falsa à `fala`; do segundo turno em diante, ela repete o que ouviu."""
    for palavra, acao in PEDIDOS_FALSOS.items():
        if palavra in fala.lower():
            return RespostaNPC(fala=f"(IA falsa) Você pediu, eu sugiro: {acao}.",
                               emocao="surpreso", acao=acao)
    if primeiro_turno:
        return so_fala("(IA falsa) Arquitetura antes de feitiço, aprendiz. Volte com um plano.")
    return so_fala(f"(IA falsa) Você disse: \"{fala}\". Sem rede, eu só repito.")
