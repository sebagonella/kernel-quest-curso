"""
RPG Engine — prova do Model sem janela (M03B).

Cada regra do jogo é chamada direto, sem abrir o pygame, e a linha diz [OK] ou
[FALTA]. Rode da raiz do projeto, depois de cada TODO do models.py:

    python prova_model.py

No M04A, isto vira teste automático de verdade, com o pytest.
"""
from src.controllers import carregar_cenas
from src.models import Estado, Jogo, Retangulo


def conferir(nome, deu_certo):
    print(f"[{'OK' if deu_certo else 'FALTA'}] {nome}")


def main():
    a = Retangulo(0, 0, 10, 10)
    conferir("colide: dois retângulos sobrepostos", a.colide(Retangulo(5, 5, 10, 10)) is True)
    conferir("colide: dois retângulos lado a lado", a.colide(Retangulo(10, 0, 10, 10)) is False)
    conferir("ampliado: maior, com o mesmo centro", a.ampliado(4) == Retangulo(-2, -2, 14, 14))

    jogo = Jogo(carregar_cenas())  # começa no MENU
    jogo.mudar_estado(Estado.EXPLORANDO)
    jogo.mudar_estado(Estado.CREDITOS)  # de EXPLORANDO não se vai aos Créditos
    conferir("mudar_estado: segue a tabela de transições", jogo.estado == Estado.EXPLORANDO)

    jogo.cena = jogo.cenas["floresta"]
    caixa = jogo.heroi.caixa
    moeda = jogo.cena.moedas[0]
    caixa.x, caixa.y = moeda.caixa.x, moeda.caixa.y  # o herói em cima de uma moeda
    antes = len(jogo.cena.moedas)
    pegas = jogo.coletar_moedas() or 0
    conferir("coletar_moedas: a moeda sai do chão e vai para a bolsa",
             pegas >= 1 and len(jogo.cena.moedas) == antes - pegas)

    # Uma parede do mapa, longe das bordas: o herói encostado nela, andando na direção dela.
    parede = next(r for r in jogo.cena.colisoes if r.x > 200 and r.y > 200)
    caixa.x, caixa.y = parede.x - caixa.largura - 1, parede.y
    jogo.mover_heroi(1, 0, "direita", 0.05)  # 10 pixels para a direita: entraria na parede
    conferir("mover_heroi: o herói não atravessa paredes", caixa.colide(parede) is False)

    area = jogo.cena.area
    caixa.x, caixa.y = -500, -500  # muito além do canto de cima à esquerda
    jogo.mover_heroi(0, 0, "baixo", 0.016)
    conferir("mover_heroi: não sai pelo canto de cima à esquerda", (caixa.x, caixa.y) == (area.x, area.y))
    caixa.x, caixa.y = 99999, 99999  # muito além do canto de baixo à direita
    jogo.mover_heroi(0, 0, "baixo", 0.016)
    conferir("mover_heroi: não sai pelo canto de baixo à direita",
             (caixa.x, caixa.y) == (area.largura - caixa.largura, area.altura - caixa.altura))


if __name__ == "__main__":
    main()
