"""
Testes dos slimes e do dano, sem janela.

Os slimes são criados aqui mesmo, no mundo de teste do conftest.py: o teste não
depende de onde você pôs os slimes no seu mapa.
"""
from src.config import DANO_SLIME, VELOCIDADE_SLIME, VIDA_MAXIMA
from src.models import Retangulo, Slime


def test_slime_patrulha_e_volta(jogo):
    slime = Slime(Retangulo(300, 500, 48, 48), origem_x=300, alcance=VELOCIDADE_SLIME)
    jogo.cena.slimes.append(slime)
    jogo.mover_slimes(1.0)  # um segundo: chega ao fim da patrulha, à direita
    assert slime.caixa.x == 300 + VELOCIDADE_SLIME
    assert slime.sentido == -1  # e deu meia-volta
    jogo.mover_slimes(1.0)  # mais um: de volta ao meio, indo para a esquerda
    assert slime.caixa.x == 300


def test_encostar_no_slime_doi(jogo):
    heroi = jogo.heroi
    # Um slime parado (alcance 0) exatamente em cima do herói.
    jogo.cena.slimes.append(Slime(Retangulo(heroi.caixa.x, heroi.caixa.y, 48, 48),
                                  origem_x=heroi.caixa.x, alcance=0))
    doeu = jogo.tocar_slimes()
    # TODO: afirme que doeu e quanto de vida o herói tem agora (use as constantes do config).
    assert False, "TODO: escreva as asserções"
