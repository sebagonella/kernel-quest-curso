"""
Preparação comum a todos os testes: o pytest lê este arquivo sozinho, antes deles.

Os testes não abrem janela, não tocam som e nunca chamam o Gemini de verdade.
O mundo dos testes é montado aqui, à mão: pequeno e sempre igual. Assim os
testes não dependem dos seus mapas do Tiled, que você muda quando quiser.
"""
import os

# Antes de importar o pygame: vídeo e áudio de mentira, e a IA falsa ligada.
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["IA_FALSA"] = "1"

import pygame  # noqa: E402  (o noqa avisa ao verificador de estilo: importar aqui é de propósito)
import pytest  # noqa: E402

from src.models import NPC, Bau, Cena, Jogo, Moeda, Retangulo  # noqa: E402
from src.views import Tela  # noqa: E402


class ServicoIAFalso:
    """Objeto falso (fake): o mesmo responder() do ServicoIA, sem rede e sem gastar cota.

    Devolve sempre a mesma fala e anota cada pedido, para o teste conferir depois
    o que o jogo pediu. Desde o M06A, também guarda as conversas como o ServicoIA:
    um "id" por turno em conversas, e nenhum token gasto.
    """

    def __init__(self, fala="Fala de teste."):
        self.fala = fala
        self.pedidos = []  # [(instrucao, fala do jogador)], na ordem em que chegaram
        self.conversas = {}  # nome do NPC -> número do último pedido da conversa com ele
        self.tokens_gastos = 0  # o falso não gasta tokens

    def responder(self, instrucao, fala, conversa=None):
        self.pedidos.append((instrucao, fala))
        if conversa:
            self.conversas[conversa] = len(self.pedidos)
        return self.fala

    def esquecer(self, conversa):
        self.conversas.pop(conversa, None)


def montar_cenas():
    """Duas cenas pequenas: o salão, com tudo o que os testes usam, e a floresta."""
    salao = Cena(
        "Salão de teste", "salao", Retangulo(0, 0, 960, 720),
        npcs=[NPC("Mago de teste", "mago", Retangulo(600, 100, 48, 48),
                  "Você é um mago de teste.")],
        moedas=[Moeda(Retangulo(300, 300, 30, 30))],  # vale 1, o padrão
        colisoes=[Retangulo(0, 600, 960, 48)],  # uma parede embaixo
        portais=[(Retangulo(912, 300, 48, 144), "floresta")],  # na borda direita
        chegadas={"inicio": (100, 100)},
        baus=[Bau(Retangulo(100, 400, 48, 42), moedas=7)],
    )
    floresta = Cena("Floresta de teste", "floresta", Retangulo(0, 0, 960, 720), npcs=[],
                    moedas=[], colisoes=[], portais=[], chegadas={"salao": (60, 360)})
    return {"salao": salao, "floresta": floresta}


@pytest.fixture
def jogo():
    """Um jogo novo em cada teste: explorando o salão, herói no ponto "inicio", bolsa vazia."""
    jogo = Jogo(montar_cenas())
    jogo.novo_jogo(jogo.cenas)
    return jogo


@pytest.fixture
def ia_falsa():
    """O serviço de IA falso, no lugar do Gemini."""
    return ServicoIAFalso()


@pytest.fixture
def tela():
    """A View de verdade, desenhando numa janela que não aparece (vídeo dummy)."""
    pygame.init()
    return Tela(pygame.display.set_mode((800, 600)))
