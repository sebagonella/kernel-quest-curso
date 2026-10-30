"""
RPG Engine — a IA em segundo plano: uma thread e duas filas (desde o M07A).

Até o M06B, o Controller chamava a IA e o jogo inteiro esperava a resposta: o
game loop parava, e a tela congelava. Agora o Controller só faz dois pedidos
rápidos, um por vez: pedir() deixa o pedido numa fila e devolve na hora;
coletar(), a cada quadro, entrega o que já chegou. Quem espera a rede é a
thread de trabalho, que roda trabalhar() o tempo todo, ao lado do jogo: as duas
threads se revezam (concorrência), e enquanto uma espera a rede, a outra desenha.

    Controller (thread principal)            thread de trabalho
    pedir(npc, fala) -> fila de pedidos ---> pedidos.get()
                                             servico_ia.responder(...)  (espera a rede)
    coletar() <------ fila de respostas <--- respostas.put((npc, resposta))

A thread nunca mexe no jogo: ela só põe a resposta na fila. Quem aplica a
resposta (caixa, balão, ação) é a thread principal, ao coletar.
"""
import logging
import queue
import threading
import time

logger = logging.getLogger(__name__)


class FilaIA:
    """A IA do jogo, sem congelar: pedir() devolve na hora, coletar() entrega o que chegou.

    Por fora, é o que o Controller usa (pedir, coletar, esquecer, tokens_gastos);
    por dentro, um ServicoIA comum, chamado na thread de trabalho. O M09A troca
    o que fica por dentro (o servidor do jogo) sem mudar o Controller.
    """

    def __init__(self, servico_ia):
        self.servico_ia = servico_ia
        self.pedidos = queue.Queue()  # (npc, fala): o que a thread ainda vai pedir à IA
        self.respostas = queue.Queue()  # (npc, RespostaNPC): o que já voltou
        self.aguardando = set()  # nomes dos NPCs com um pedido em andamento
        # daemon=True: a thread não segura o programa aberto quando a janela fecha.
        threading.Thread(target=self.trabalhar, name="ia", daemon=True).start()

    @property
    def tokens_gastos(self):
        return self.servico_ia.tokens_gastos  # o F3 lê daqui, como antes

    def esquecer(self, conversa):
        self.servico_ia.esquecer(conversa)

    def pedir(self, npc, fala):
        """Registra o pedido e devolve na hora. False se esse NPC já está esperando resposta."""
        # TODO (Passo 6): se esse NPC já está esperando resposta, recuse (devolva False)
        self.aguardando.add(npc.nome)
        self.pedidos.put((npc, fala))
        return True

    def trabalhar(self):
        """O laço da thread de trabalho: espera um pedido, chama a IA e põe a resposta na fila."""
        while True:
            npc, fala = self.pedidos.get()  # dorme até chegar um pedido
            inicio = time.perf_counter()
            # TODO (Passo 2): peça a resposta ao servico_ia (como o Controller pedia até hoje),
            # registre no log o nome do NPC, os segundos que ela levou e a resposta, e ponha
            # (npc, resposta) na fila de respostas.

    def coletar(self):
        """O que chegou desde a última chamada, sem esperar: uma lista de (npc, resposta)."""
        # TODO (Passo 3): escreva o coletar() do zero
        return []  # TODO (Passo 3): provisório, até o coletar() existir
