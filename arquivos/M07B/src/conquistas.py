"""
RPG Engine — conquistas: um assinante do EventBus (desde o M07B).

Ninguém no jogo chama as conquistas: elas assinam os eventos e decidem sozinhas
quando um marco foi atingido. Ao desbloquear, publicam ConquistaDesbloqueada,
que a tela, o log de auditoria e o Discord assinam. Conquista nova é um
método novo aqui e uma linha em CONQUISTAS; quem publica os eventos não muda.
"""
import logging

from src.eventos import CenaAlterada, ConquistaDesbloqueada, ItemRecebido

logger = logging.getLogger(__name__)

# Identificador (o M08A salva) -> o nome que a tela mostra.
CONQUISTAS = {
    "explorador": "Explorador",
    "portador_da_chave": "Portador da Chave",
}


class Conquistas:
    """Ouve os eventos do jogo e desbloqueia cada conquista uma vez só."""

    def __init__(self, eventos):
        self.eventos = eventos
        self.obtidas = []  # identificadores, na ordem em que vieram
        eventos.assinar(CenaAlterada, self.cena_alterada)
        eventos.assinar(ItemRecebido, self.item_recebido)

    def desbloquear(self, id, cena):
        """Marca a conquista e avisa quem assina; a segunda vez não faz nada."""
        if id in self.obtidas:
            return
        self.obtidas.append(id)
        logger.info("Conquista: %s", CONQUISTAS[id])
        self.eventos.publicar(ConquistaDesbloqueada(id, CONQUISTAS[id], cena))

    def item_recebido(self, evento):
        """Portador da Chave: a Chave da Masmorra entrou no inventário."""
        if evento.item == "Chave da Masmorra":
            self.desbloquear("portador_da_chave", evento.cena)

    def cena_alterada(self, evento):
        """Explorador: o herói chegou à floresta pela primeira vez."""
        # TODO (Passo 3): se o destino do evento é a floresta, desbloqueie "explorador"
        # (o desbloquear() já cuida do "uma vez só"; a cena é o próprio destino).
