"""
RPG Engine — o aviso no Discord: um assinante que fala HTTP (desde o M07B).

Um webhook de entrada é uma URL que o Discord cria para um canal: quem faz um
POST nela, com um corpo JSON {"content": "texto"}, publica uma mensagem no
canal. Aqui, nós chamamos o Discord (o M09A mostra o outro lado: alguém chama
o nosso servidor).

    POST https://discord.com/api/webhooks/<id>/<token>     <- método e URL
    {"content": "Ada desbloqueou a conquista Explorador"}  <- corpo JSON
    204 No Content                                         <- código de status: aceito
    429 Too Many Requests, Retry-After: 2                  <- devagar: tente daqui a 2 s

A rede demora, como a IA do M07A. Por isso o assinante só põe o texto numa fila
e devolve na hora; quem espera o Discord é uma thread só dele.
"""
import logging
import queue
import threading
import time

import httpx

from src.config import NOME, TENTATIVAS_DISCORD, TIMEOUT_DISCORD
from src.eventos import ConquistaDesbloqueada, ItemRecebido

logger = logging.getLogger(__name__)
# O httpx escreve cada requisição no log, com a URL inteira; a URL do webhook é um
# segredo, então o log dele só mostra avisos.
logging.getLogger("httpx").setLevel(logging.WARNING)


class NotificacaoDiscord:
    """Assina conquistas e itens e manda cada um, em texto curto, ao canal do Discord."""

    def __init__(self, eventos, url, cliente=None):
        self.url = url
        self.ligado = False
        # TODO (Passo 5): sem URL (texto vazio), registre no log que o Discord está desligado
        # e saia do __init__ aqui, antes de assinar qualquer evento.
        self.ligado = True
        # O cliente vem de fora nos testes (um Discord falso); no jogo, um de verdade.
        self.cliente = cliente or httpx.Client(timeout=TIMEOUT_DISCORD)
        self.avisos = queue.Queue()  # textos esperando a vez de ir ao Discord
        eventos.assinar(ConquistaDesbloqueada, self.conquista)
        eventos.assinar(ItemRecebido, self.item)
        threading.Thread(target=self.trabalhar, name="discord", daemon=True).start()

    # Os assinantes: rodam na thread do jogo, então só enfileiram (nada de rede aqui).
    # Só o evento vai ao Discord (quem, o quê, onde), nunca o texto das conversas.
    def conquista(self, evento):
        self.avisos.put(f"{NOME} desbloqueou a conquista **{evento.nome}** ({evento.cena}).")

    def item(self, evento):
        self.avisos.put(f"{NOME} recebeu: {evento.item} ({evento.cena}).")

    def trabalhar(self):
        """O laço da thread do Discord: espera um aviso e envia."""
        while True:
            self.enviar(self.avisos.get())

    def enviar(self, texto):
        """Um POST no webhook. Devolve True se o Discord aceitou a mensagem."""
        # allowed_mentions vazio: nenhum texto do jogo consegue chamar @everyone no canal.
        corpo = {"content": texto, "allowed_mentions": {"parse": []}}
        for _ in range(TENTATIVAS_DISCORD):
            try:
                resposta = self.cliente.post(self.url, json=corpo)
            except httpx.HTTPError as erro:  # sem rede, DNS, timeout: o jogo não cai
                logger.warning("Discord fora de alcance: %s", type(erro).__name__)
                return False
            # TODO (Passo 6): com o código 429, leia os segundos do cabeçalho Retry-After
            # (1, se não vier), registre no log, durma esse tempo e tente de novo (continue).
            if resposta.is_success:  # 2xx; o webhook responde 204 (aceito, sem corpo)
                logger.info("Discord: aviso entregue (%d)", resposta.status_code)
                return True
            logger.warning("Discord recusou o aviso: %d", resposta.status_code)
            return False
        logger.warning("Discord: desisti depois de %d tentativas", TENTATIVAS_DISCORD)
        return False
