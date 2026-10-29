"""
RPG Engine — modo depuração (F3): os retângulos do Model desenhados por cima do jogo.

Faz parte da View: só LÊ o jogo. Cada retângulo que as regras usam (a caixa do
herói, os obstáculos, as áreas de conversa, os portais, as moedas) ganha um
contorno colorido. Quando uma regra parece errada ("por que não consigo falar
com o Brok daqui?"), o F3 mostra o que o Model está vendo.
"""
import pygame

from src.config import ALTURA, COR_PAINEL, COR_TEXTO

# Uma cor por tipo de retângulo; a legenda no rodapé repete esta ordem.
COR_HEROI = (80, 255, 120)  # verde
COR_OBSTACULO = (255, 70, 70)  # vermelho: paredes, árvores e NPCs (o herói não atravessa)
COR_AREA = (255, 215, 0)  # amarelo: perto o bastante para interagir
COR_PORTAL = (70, 160, 255)  # azul
COR_MOEDA = (255, 150, 40)  # laranja


def contorno(tela, retangulo, cor, camera_x, camera_y):
    """Desenha só a borda (2 px) de um Retangulo do Model, deslocado pela câmera."""
    pygame.draw.rect(tela, cor, (retangulo.x - camera_x, retangulo.y - camera_y,
                                 retangulo.largura, retangulo.altura), 2)


def desenhar_depuracao(tela, fonte, jogo, camera_x, camera_y):
    """Os retângulos da cena atual, na mesma câmera do mundo, e a legenda das cores."""
    cena = jogo.cena
    for parede in cena.colisoes:
        contorno(tela, parede, COR_OBSTACULO, camera_x, camera_y)
    for portal, _ in cena.portais:
        contorno(tela, portal, COR_PORTAL, camera_x, camera_y)
    for moeda in cena.moedas:
        contorno(tela, moeda.caixa, COR_MOEDA, camera_x, camera_y)
    for npc in cena.npcs:
        contorno(tela, npc.caixa, COR_OBSTACULO, camera_x, camera_y)
        contorno(tela, npc.area_conversa, COR_AREA, camera_x, camera_y)
    contorno(tela, jogo.heroi.caixa, COR_HEROI, camera_x, camera_y)

    legenda = [("herói", COR_HEROI), ("obstáculo", COR_OBSTACULO), ("interação", COR_AREA),
               ("portal", COR_PORTAL), ("moeda", COR_MOEDA)]
    fundo = pygame.Surface((560, 30), pygame.SRCALPHA)
    fundo.fill(COR_PAINEL)
    tela.blit(fundo, (10, ALTURA - 40))
    x = 20
    tela.blit(fonte.render("F3", False, COR_TEXTO), (x, ALTURA - 40))
    x += 40
    for nome, cor in legenda:
        pygame.draw.rect(tela, cor, (x, ALTURA - 30, 12, 12), 2)
        imagem = fonte.render(nome, False, COR_TEXTO)
        tela.blit(imagem, (x + 18, ALTURA - 40))
        x += imagem.get_width() + 36
