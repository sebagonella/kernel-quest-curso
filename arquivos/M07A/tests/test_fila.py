"""
Testes da FilaIA: pedir() devolve na hora, a thread responde, coletar() entrega.

Aqui a thread é de verdade: a FilaIA embrulha um serviço falso que demora um
pouco (como a rede). Por isso alguns testes esperam, com um limite de tempo,
em vez de supor que a resposta já chegou.
"""
import time

from src.controllers import Controle
from src.fila_ia import FilaIA
from src.models import Estado
from src.resposta import so_fala


class Lento:
    """Embrulha o serviço falso do conftest com uma espera antes de responder, como a rede."""

    def __init__(self, servico):
        self.servico = servico
        self.tokens_gastos = 0

    def responder(self, instrucao, fala, conversa=None):
        time.sleep(0.2)
        return self.servico.responder(instrucao, fala, conversa)


def esperar(fila, limite=2.0):
    """Chama coletar() até chegar alguma coisa (ou o limite acabar)."""
    fim = time.perf_counter() + limite
    while time.perf_counter() < fim:
        chegou = fila.coletar()
        if chegou:
            return chegou
        time.sleep(0.01)
    return []


def test_pedir_devolve_na_hora(jogo, ia_falsa):
    fila = FilaIA(Lento(ia_falsa))
    inicio = time.perf_counter()
    assert fila.pedir(jogo.cena.npcs[0], "Bom dia.")
    assert time.perf_counter() - inicio < 0.05  # não esperou os 0,2 s da "rede"


def test_a_thread_poe_a_resposta_na_fila(jogo, ia_falsa):
    mago = jogo.cena.npcs[0]
    fila = FilaIA(ia_falsa)
    fila.pedir(mago, "Bom dia.")
    npc, resposta = fila.respostas.get(timeout=2)  # espera a thread, no máximo 2 s
    assert npc is mago
    assert resposta == so_fala("Fala de teste.")


def test_coletar_nao_espera(jogo, ia_falsa):
    fila = FilaIA(Lento(ia_falsa))
    fila.pedir(jogo.cena.npcs[0], "Bom dia.")
    inicio = time.perf_counter()
    assert fila.coletar() == []  # ainda não chegou nada, e ele não fica esperando
    assert time.perf_counter() - inicio < 0.05


def test_coletar_entrega_o_que_chegou_uma_vez_so(jogo, ia_falsa):
    mago = jogo.cena.npcs[0]
    fila = FilaIA(Lento(ia_falsa))
    fila.pedir(mago, "Bom dia.")
    assert esperar(fila) == [(mago, so_fala("Fala de teste."))]
    assert fila.coletar() == []  # já foi entregue
    assert fila.aguardando == set()  # o mago pode pedir de novo


def test_mesmo_npc_nao_pede_duas_vezes(jogo, ia_falsa):
    mago = jogo.cena.npcs[0]
    fila = FilaIA(Lento(ia_falsa))
    assert fila.pedir(mago, "Bom dia.")
    assert not fila.pedir(mago, "Bom dia de novo.")  # ainda esperando: recusado
    esperar(fila)
    assert len(ia_falsa.pedidos) == 1  # uma chamada só
    assert fila.pedir(mago, "Agora sim.")  # respondeu: pode pedir de novo


def test_a_fila_entrega_a_resposta_ao_jogo(jogo, tela, ia_falsa):
    mago = jogo.cena.npcs[0]
    controle = Controle(jogo, tela, FilaIA(Lento(ia_falsa)))
    controle.servico_ia.pedir(mago, "Bom dia.")  # o que o ESPAÇO faz perto do mago
    controle.atualizar(0.016)
    assert jogo.estado == Estado.EXPLORANDO  # a resposta não chegou: o herói segue andando
    fim = time.perf_counter() + 2
    while jogo.estado == Estado.EXPLORANDO and time.perf_counter() < fim:
        controle.atualizar(0.016)  # um quadro: é aqui que o coletar() roda
        time.sleep(0.01)
    assert jogo.estado == Estado.DIALOGO  # chegou, e a caixa abriu na thread principal
    assert controle.dialogo.paginas[0][0] == "Fala de teste."
