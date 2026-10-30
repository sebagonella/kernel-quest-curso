"""
RPG Engine — a medição do ritmo do jogo: FPS e pior quadro (desde o M07A).

O main.py registra quanto durou cada volta do game loop; o F3 (depuracao.py)
mostra o resultado. Um congelamento (a IA pensando no meio do loop) aparece
inteiro aqui, num quadro só.
"""
from collections import deque

from src.config import FPS


class Medidor:
    """Quanto durou cada quadro nos últimos 2 segundos: o FPS e o pior quadro (M07A).

    O main.py registra o tempo de cada volta do game loop, antes do teto do dt: um
    congelamento aparece inteiro aqui, mesmo que o jogo não deixe o herói teleportar.
    """

    def __init__(self, quadros=2 * FPS):
        self.duracoes = deque(maxlen=quadros)  # milissegundos; a deque esquece os mais antigos

    def registrar(self, ms):
        self.duracoes.append(ms)

    def fps(self):
        """Quadros por segundo na média da janela (0 enquanto não há medida)."""
        total = sum(self.duracoes)
        return round(len(self.duracoes) * 1000 / total) if total else 0

    def pior_quadro(self):
        return max(self.duracoes, default=0)


# Um medidor só, para o jogo todo: o main.py escreve, o F3 lê.
MEDIDOR = Medidor()
