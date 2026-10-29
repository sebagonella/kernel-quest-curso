"""
Testes das regras do jogo (o Model), sem janela e sem IA.

Rode da raiz do projeto:  python -m pytest -q
Cada teste recebe um jogo novo (a fixture "jogo", do conftest.py) e segue três
partes: prepara a situação, executa a regra e afirma o resultado (assert).
"""
from src.models import POCAO, Estado


def test_coletar_moeda(jogo):
    # Prepara: o herói em cima da moeda do salão.
    moeda = jogo.cena.moedas[0]
    jogo.heroi.caixa.x, jogo.heroi.caixa.y = moeda.caixa.x, moeda.caixa.y
    # Executa: a regra que o jogo chama a cada quadro.
    pegas = jogo.coletar_moedas()
    # Afirma: pegou uma moeda, e a bolsa tem o valor dela.
    assert pegas == 1
    assert jogo.heroi.moedas == 1


def test_abrir_bau(jogo):
    bau = jogo.cena.baus[0]  # guarda 7 moedas
    ganhou = jogo.abrir_bau(bau)
    assert ganhou == 7
    assert jogo.heroi.moedas == 7
    assert bau.aberto


def test_bau_abre_uma_vez_so(jogo):
    bau = jogo.cena.baus[0]
    jogo.abrir_bau(bau)
    ganhou = jogo.abrir_bau(bau)  # a segunda vez
    # TODO: afirme o que a segunda abertura devolve e quanto a bolsa tem agora (dois assert).
    assert False, "TODO: escreva as asserções"


def test_comprar_sem_saldo(jogo):
    jogo.heroi.moedas = 3  # a poção custa 5
    recusa = jogo.comprar(POCAO)
    # TODO: três coisas provam que a compra não saiu: o que comprar() devolveu (o motivo da
    #       recusa, ou None se a compra saiu), a bolsa e o inventário. Um assert para cada.
    assert False, "TODO: escreva as asserções"


def test_transicao_de_cena(jogo):
    portal, destino = jogo.cena.portais[0]  # leva à floresta
    jogo.heroi.caixa.x, jogo.heroi.caixa.y = portal.x, portal.y
    jogo.tocar_portal()
    for _ in range(10):  # 10 quadros de 0,1 s: dá tempo de escurecer, trocar o mapa e clarear
        if jogo.estado == Estado.TRANSICAO:
            jogo.atualizar_transicao(0.1)
    # TODO: afirme em que cena o jogo termina (jogo.cenas[destino] é a de destino; compare
    #       com `is`, "é o mesmo objeto") e em que estado.
    assert False, "TODO: escreva as asserções"
