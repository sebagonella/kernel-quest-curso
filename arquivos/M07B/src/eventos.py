"""
RPG Engine — eventos: quem publica não conhece quem assina (desde o M07B).

Um evento é um fato que já aconteceu no jogo ("o herói entrou na floresta").
Quem faz acontecer (o Model, o Controller) só publica o fato no EventBus; quem
quer reagir (conquistas, aviso na tela, log de auditoria, Discord) assina o tipo
de evento que lhe interessa. Para um assinante novo, nenhuma linha muda em quem
publica.

    Jogo ---- publicar(CenaAlterada) ---> EventBus ---> Conquistas.cena_alterada
                                                   ---> Auditoria.registrar
"""
from dataclasses import dataclass


# Os eventos: só dados, com o nome no passado (já aconteceu). frozen=True: ninguém
# muda um fato depois de publicado.
@dataclass(frozen=True)
class CenaAlterada:
    origem: str  # o mapa de onde o herói saiu ("salao", "floresta", "masmorra")
    destino: str  # o mapa onde ele chegou


@dataclass(frozen=True)
class NPCInteragido:
    npc: str  # o nome do NPC
    cena: str  # o mapa da conversa


@dataclass(frozen=True)
class ItemRecebido:
    item: str  # o nome do item
    cena: str  # o mapa onde o herói o recebeu


@dataclass(frozen=True)
class ConquistaDesbloqueada:
    id: str  # o identificador, que o M08A salva ("explorador")
    nome: str  # o que a tela mostra ("Explorador")
    cena: str


# TODO (Passo 1): escreva aqui, do zero, a classe EventBus, com três métodos:
#   __init__(self): começa sem assinantes, num dicionário self.assinantes
#       (tipo do evento -> lista de funções que o recebem);
#   assinar(self, tipo, funcao): daqui em diante, todo evento desse tipo chega a funcao(evento);
#   publicar(self, evento): entrega o evento a quem assinou o tipo dele, na ordem em que
#       assinaram; sem assinantes, não faz nada.
# Os testes de tests/test_eventos.py dizem quando ela está certa.
