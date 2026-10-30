"""
RPG Engine — Módulo 07A: Sem congelar.

O jogo (menu, mapas do Tiled, moedas, baú, slimes e vida, HUD, a conversa com o
Gemini, com memória, balões de emoção e ações que o jogo valida, a loja do Brok,
a Chave e o Guarda do Portão, o Tux no Linux e o Quadro da Vigia) fica em camadas
dentro de src/; a IA pensa numa thread, e o jogo segue a 60 FPS. No Linux, ./run.sh
ativa a venv e roda este arquivo. As regras se provam com os testes de tests/, que
o GitHub Actions roda a cada push:
  models.py       dados e regras, sem pygame (testável sem janela), e validar_acao
  views.py        desenho e som; só lê o Model (com campo_texto.py e paineis.py)
  controllers.py  teclado e coordenação; monta o Model a partir dos mapas
  ia.py           a chamada ao Gemini; resposta.py diz a forma da resposta
  fila_ia.py      a IA em segundo plano: pedir() e coletar(), com uma thread e filas
  depuracao.py    F3: os retângulos do Model desenhados por cima do jogo (e o medidor.py)
Este arquivo liga o log, monta as peças e roda o game loop.
"""
import logging

import pygame

from src.config import ALTURA, FPS, LARGURA, MODELO_IA, NIVEL_LOG, NOME_JOGO, TETO_DT, TIMEOUT_IA_MS
from src.controllers import Controle, carregar_cenas
from src.fila_ia import FilaIA
from src.ia import ServicoIA
from src.medidor import MEDIDOR
from src.models import Jogo
from src.views import Tela


def main():
    # Log no terminal: hora, nível, de onde veio e a mensagem. Configurado uma vez, aqui.
    logging.basicConfig(level=NIVEL_LOG, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
                        datefmt="%H:%M:%S")
    pygame.init()  # também liga o áudio (pygame.mixer), se houver dispositivo de som
    superficie = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(NOME_JOGO)
    relogio = pygame.time.Clock()

    # Injeção de dependências: cada peça é criada aqui e entregue pronta a quem usa.
    jogo = Jogo(carregar_cenas())  # Model
    tela = Tela(superficie)  # View
    controle = Controle(jogo, tela, ServicoIA(MODELO_IA, TIMEOUT_IA_MS))  # TODO (Passo 4b): a FilaIA

    tempo = 0.0
    # Game loop: a cada volta, ler eventos, atualizar e desenhar (60 vezes por segundo).
    while controle.rodando:
        # tick() segura o ritmo em 60 FPS e devolve os milissegundos desde o último quadro.
        ms = relogio.tick(FPS)  # milissegundos desde o último quadro
        MEDIDOR.registrar(ms)  # o F3 mostra o FPS e o pior quadro (um congelamento aparece aqui)
        dt = ms / 1000  # delta time: segundos desde o último quadro
        dt = min(dt, TETO_DT)  # depois de um congelamento (a IA pensando), nada de teletransporte
        tempo += dt
        for evento in pygame.event.get():
            controle.tratar_evento(evento)
        controle.atualizar(dt)
        tela.desenhar(jogo, controle, dt, tempo)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
